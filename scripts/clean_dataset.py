#!/usr/bin/env python3
"""Clean and normalize merged vitrimer records into the final dataset."""

from __future__ import annotations

import json
from pathlib import Path
import sys
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
MERGED_PATH = ROOT / "data/interim/merged_records.csv"
SCHEMA_PATH = ROOT / "specs/dataset_schema.json"
DATASET_PATH = ROOT / "data/processed/dataset.csv"

MISSING_TOKENS = {"", "na", "n/a", "none", "null", "-", "nan", "NaN", "nd", "n.d."}


def load_schema_columns() -> list[str]:
    """Reads the expected fields from the dataset schema specification."""
    if SCHEMA_PATH.is_file():
        try:
            with SCHEMA_PATH.open(encoding="utf-8") as f:
                schema = json.load(f)
                return [field["name"] for field in schema.get("fields", [])]
        except Exception:
            pass
    return [
        'record_id', 'source_id', 'doi', 'polymer_SMILES', 'dynamic_bond_type', 
        'temperature_C', 'relaxation_time_s', 'normalized_stress', 'storage_modulus_Pa', 
        'catalyst_smiles', 'crosslinker', 'normalized_inverse_temperature', 
        'log_viscosity', 'time_s', 'tan_delta', 'normalized_fluorescence_intensity', 
        'domain_distance_nm'
    ]


def clean_smiles(seq: object) -> str | None:
    """Removes invalid whitespace and string artifacts from SMILES."""
    if pd.isna(seq):
        return None
    text = str(seq).strip()
    if text.lower() in MISSING_TOKENS:
        return None
    text = text.replace('\r', '').replace('\n', '').replace('"', '').replace("'", "")
    return text if text else None


def normalize_missing_values(value: object) -> object:
    """Maps recognized missing value tokens to standard NumPy NaN."""
    if pd.isna(value):
        return np.nan
    text = str(value).strip()
    if text.lower() in MISSING_TOKENS or text == "":
        return np.nan
    return value


def main() -> int:
    print("=== Starting Dataset Cleaning Pipeline ===")
    
    if not MERGED_PATH.is_file():
        print(f"Error: Interim file not found at {MERGED_PATH.relative_to(ROOT)}.")
        return 1

    df = pd.read_csv(MERGED_PATH, encoding='utf-8')
    print(f"Loaded {len(df)} rows from interim merged records.")

    columns = load_schema_columns()
    for col in columns:
        if col not in df.columns:
            df[col] = np.nan
            
    df = df[columns]
    
    smiles_columns = ["polymer_SMILES", "catalyst_smiles", "crosslinker"]
    for col in df.columns:
        if col in smiles_columns:
            df[col] = df[col].apply(clean_smiles)
        else:
            df[col] = df[col].apply(normalize_missing_values)
            
    df.dropna(subset=["polymer_SMILES"], inplace=True)
    df.drop_duplicates(subset=["record_id"], keep="first", inplace=True)
    
    DATASET_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(DATASET_PATH, index=False, encoding='utf-8')
    
    print("Dataset cleaning completed successfully.")
    print(f"Wrote {len(df)} cleaned rows to {DATASET_PATH.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())