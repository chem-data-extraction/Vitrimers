#!/usr/bin/env python3
"""Extract vitrimer screening data from the web (GitHub repository) based on web_extraction_manifest.json."""

from __future__ import annotations

import io
import json
from pathlib import Path
import sys
import pandas as pd
import requests

ROOT = Path(__file__).resolve().parents[1]


def load_manifest() -> dict:
    manifest_path = ROOT / "specs/web_extraction_manifest.json"
    if not manifest_path.is_file():
        print(f"Error: Manifest not found at {manifest_path}")
        sys.exit(1)
    with manifest_path.open(encoding="utf-8") as f:
        return json.load(f)


def main() -> int:
    print("=== Starting Web Extraction (GitHub: VitrimerScreening) ===")
    
    manifest = load_manifest()
    
    if not manifest.get("input_pages"):
        print("Error: No input pages defined in web_extraction_manifest.json")
        return 1
        
    page_config = manifest["input_pages"][0]
    source_id = page_config["source_id"]
    url = page_config["url"]
    
    # Форсируем raw-url для скачивания напрямую
    if "github.com" in url and "raw.githubusercontent.com" not in url:
        url = url.replace("github.com", "raw.githubusercontent.com").replace("/blob/", "/")
        
    print(f"Fetching data from: {url}")
    
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error downloading data: {e}")
        return 1

    print("Successfully downloaded web data. Parsing raw entries...")
    
    try:
        # Читаем CSV с автоматическим определением разделителя (запятая)
        df_raw = pd.read_csv(io.StringIO(response.text))
    except Exception as e:
        print(f"Error parsing CSV data: {e}")
        return 1

    print(f"Raw data parsed. Found {len(df_raw)} rows.")

    processed_records = []
    
    for idx, row in df_raw.iterrows():
        record_id = f"rec_vit_web_{source_id}_{idx+1:04d}"
        
        # Извлекаем компоненты
        acid_smiles = str(row.get("acid", "")).strip()
        epoxide_smiles = str(row.get("epoxide", "")).strip()
        
        # Если критически важные компоненты пусты — пропускаем строку
        if not acid_smiles or not epoxide_smiles or acid_smiles == "nan" or epoxide_smiles == "nan":
            continue
            
        # Объединяем через точку в соответствии с правиламиdataset_schema.json
        combined_smiles = f"{acid_smiles}.{epoxide_smiles}"
        
        # Конвертируем температуру Tg из Кельвинов в Цельсии
        tg_k = row.get("tg")
        try:
            tg_c = float(tg_k) - 273.15 if pd.notna(tg_k) else float("nan")
        except (ValueError, TypeError):
            tg_c = float("nan")
            
        # Формируем запись, заполняя недостающие экспериментальные поля явными NaN
        record = {
            "record_id": record_id,
            "source_id": source_id,
            "polymer_name": "Screened Epoxy-Acid Vitrimer Network",
            "monomer_components_smiles": combined_smiles,
            "dynamic_link_type": "transesterification",  # Классика для эпокси-кислотных систем
            "catalyst_name": float("nan"),               # В скрининге катализатор не указан
            "catalyst_loading_mol_pct": float("nan"),
            "tg_value_c": tg_c,
            "relaxation_time_s": float("nan"),
            "relaxation_temp_c": float("nan"),
            "activation_energy_kj_mol": float("nan"),
            "data_provenance": "github_repository",
            "doi": page_config.get("doi") if pd.notna(page_config.get("doi")) else float("nan"),
            "conflict_flag": False,
            "extraction_method": "api",
            "notes": "Extracted from Vashisth Lab screening dataset. Tg converted from Kelvin to Celsius."
        }
        processed_records.append(record)

    df_out = pd.DataFrame(processed_records)
    
    # Путь сохранения CSV
    output_path = ROOT / "data/extracted/web_extracted_records.csv"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    df_out.to_csv(output_path, index=False, encoding="utf-8")
    print(f"Saved {len(df_out)} web records to {output_path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())