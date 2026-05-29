#!/usr/bin/env python3
"""
Production PDF-CSV extraction driver.
Reads pre-extracted CSV tables with ';' separator, maps to schema, 
generates unique record IDs, and writes extraction logs.
"""

import json
import uuid
import pandas as pd
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW_PDF_CSV_DIR = ROOT / "data/raw/pdf_csv"
OUTPUT_PATH = ROOT / "data/extracted/pdf_extracted_records.csv"
LOG_PATH = ROOT / "data/extracted/extraction_log.jsonl"

# Mapping filenames to source_id and doi based on source_map.json
SOURCE_MAP = {
    "leibler_2011": {"source_id": "leibler_2011", "doi": "10.1126/science.1212648"},
    "denissen_2015": {"source_id": "denissen_2015", "doi": "10.1002/adfm.201502499"},
    "tretbar_2019": {"source_id": "tretbar_2019", "doi": "10.1021/jacs.9b08876"},
    "wang_2018": {"source_id": "wang_2018", "doi": "10.1021/acs.macromol.8b01369"},
    "hayashi_2025": {"source_id": "hayashi_2025", "doi": "10.1016/j.progpolymsci.2025.102026"}
}

def append_log(entry: dict) -> None:
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")

def identify_source(filename: str) -> dict:
    for key, meta in SOURCE_MAP.items():
        if key in filename.lower():
            return meta
    return {"source_id": "unknown_pdf", "doi": None}

def main() -> None:
    print("=== Starting PDF-CSV Data Extraction ===")
    
    if not RAW_PDF_CSV_DIR.exists():
        print(f"Error: Directory {RAW_PDF_CSV_DIR} not found.")
        return

    input_files = list(RAW_PDF_CSV_DIR.glob("*.csv"))
    extracted_rows = []
    processed_count = 0

    for file_path in input_files:
        filename = file_path.name
        source_info = identify_source(filename)
        
        try:
            # Read local CSV tables (using ';' separator)
            df = pd.read_csv(file_path, sep=';', encoding='utf-8', skipinitialspace=True)
            
            for _, row in df.iterrows():
                # Extract polymer SMILES (handling potential case differences)
                smiles = row.get("polymer_SMILES", row.get("polymer_smiles", None))
                if pd.isna(smiles):
                    continue
                
                # Build the record mapping fields if they exist
                record = {
                    "record_id": f"pdf_{source_info['source_id']}_{uuid.uuid4().hex[:8]}",
                    "source_id": source_info["source_id"],
                    "doi": source_info["doi"],
                    "polymer_SMILES": str(smiles).strip(),
                    "dynamic_bond_type": row.get("dynamic_bond_type", "unknown"),
                    "temperature_C": row.get("temperature_C", None),
                    "relaxation_time_s": row.get("relaxation_time_s", None),
                    "normalized_stress": row.get("normalized_stress", None),
                    "storage_modulus_Pa": row.get("storage_modulus_Pa", None),
                    "catalyst_smiles": row.get("catalyst_smiles", row.get("catalyst_SMILES", None)),
                    "crosslinker": row.get("crosslinker", None),
                    "normalized_inverse_temperature": row.get("normalized_inverse_temperature", None),
                    "log_viscosity": row.get("log_viscosity", None),
                    "time_s": row.get("time_s", None),
                    "tan_delta": row.get("tan_delta", None),
                    "normalized_fluorescence_intensity": row.get("normalized_fluorescence_intensity", None),
                    "domain_distance_nm": row.get("domain_distance_nm", None)
                }
                extracted_rows.append(record)
            
            processed_count += 1
            print(f"  Processed: {filename}")
            
        except Exception as e:
            append_log({
                "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
                "step": "pdf_extraction",
                "source_id": filename,
                "status": "failed",
                "tool": "extract_pdf.py",
                "issue": str(e)
            })

    if extracted_rows:
        OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
        result_df = pd.DataFrame(extracted_rows)
        result_df.to_csv(OUTPUT_PATH, index=False, encoding='utf-8')
        
        append_log({
            "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            "step": "pdf_extraction",
            "source_id": "batch_pdf_csv",
            "status": "success",
            "tool": "extract_pdf.py",
            "output": str(OUTPUT_PATH.relative_to(ROOT)),
            "issue": f"Parsed {processed_count} files, extracted {len(result_df)} rows"
        })
        print(f"Saved {len(result_df)} records to {OUTPUT_PATH.relative_to(ROOT)}\n")
    else:
        print("No valid data extracted.")

if __name__ == "__main__":
    main()