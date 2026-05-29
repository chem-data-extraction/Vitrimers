#!/usr/bin/env python3
"""Consolidate extracted PDF and Web records into an interim dataset."""

from __future__ import annotations

from pathlib import Path
import sys
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]


def smart_find_smiles_column(df: pd.DataFrame) -> str | None:
    """Find any column that likely contains SMILES strings."""
    possible_names = [
        "polymer_smiles", "polymer_SMILES", "monomer_components_smiles", 
        "smiles", "SMILES", "structure"
    ]
    for name in possible_names:
        for col in df.columns:
            if str(col).strip().lower() == name.lower():
                return col
    for col in df.columns:
        if "smiles" in str(col).lower():
            return col
    return None


def main() -> int:
    print("=== Starting Dataset Consolidation Pipeline ===")
    
    pdf_path = ROOT / "data/extracted/pdf_extracted_records.csv"
    web_path = ROOT / "data/extracted/web_extracted_records.csv"
    
    if pdf_path.is_file():
        df_pdf = pd.read_csv(pdf_path)
        print(f"Loaded PDF extracted records: {len(df_pdf)} rows.")
    else:
        df_pdf = pd.DataFrame()
        print("Warning: PDF extracted file not found.")
        
    if web_path.is_file():
        df_web = pd.read_csv(web_path)
        print(f"Loaded Web extracted records: {len(df_web)} rows.")
    else:
        df_web = pd.DataFrame()
        print("Warning: Web extracted file not found.")

    if not df_pdf.empty:
        pdf_smiles_col = smart_find_smiles_column(df_pdf)
        if pdf_smiles_col:
            df_pdf["polymer_SMILES"] = df_pdf[pdf_smiles_col]
            
    if not df_web.empty:
        web_smiles_col = smart_find_smiles_column(df_web)
        if web_smiles_col:
            df_web["polymer_SMILES"] = df_web[web_smiles_col]

    rename_inputs = {
        "dynamic_link_type": "dynamic_bond_type",
        "bond_type": "dynamic_bond_type",
        "temp_c": "temperature_C",
        "relaxation_temp_c": "temperature_C"
    }
    if not df_pdf.empty:
        df_pdf.rename(columns=rename_inputs, inplace=True)
    if not df_web.empty:
        df_web.rename(columns=rename_inputs, inplace=True)

    df_merged = pd.concat([df_pdf, df_web], ignore_index=True)
    df_merged = df_merged.loc[:, ~df_merged.columns.duplicated(keep='first')]
    
    if "record_id" in df_merged.columns:
        df_merged["record_id"] = df_merged["record_id"].fillna(
            df_merged.index.to_series().apply(lambda x: f"rec_web_auto_{x:05d}")
        )
    else:
        df_merged["record_id"] = df_merged.index.to_series().apply(lambda x: f"rec_web_auto_{x:05d}")
    
    interim_path = ROOT / "data/interim/merged_records.csv"
    interim_path.parent.mkdir(parents=True, exist_ok=True)
    df_merged.to_csv(interim_path, index=False, encoding="utf-8")
    print(f"Interim merged file created: {interim_path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())