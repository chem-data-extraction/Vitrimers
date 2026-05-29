#!/usr/bin/env python3
"""Validate repository artifacts against specs/dataset_schema.json and validation rules."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

# Core repository structure for the Vitrimer project
REQUIRED_FILES = [
    "project.json",
    "specs/dataset_schema.json",
    "specs/source_map.json",
    "specs/pdf_extraction_manifest.json",
    "specs/web_extraction_manifest.json",
    "specs/cleaning_pipeline.json",
    "specs/validation_rules.json",
    "data/processed/dataset.csv",
    "scripts/build_dataset.py",
    "scripts/clean_dataset.py",
]


def load_json(path: Path) -> dict:
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def schema_field_names(schema: dict) -> list[str]:
    return [field["name"] for field in schema["fields"]]


def source_ids_from_map(source_map: dict) -> set[str]:
    """Dynamically extracts source IDs from source_map groups, 

    handling both list and dictionary representations.
    """
    ids: set[str] = set()
    source_groups = source_map.get("source_groups", {})
    
    # Handle list of groups or direct group dictionary
    groups_to_process = source_groups.values() if isinstance(source_groups, dict) else source_groups
    
    for group in groups_to_process:
        if isinstance(group, list):
            for entry in group:
                sid = entry.get("source_id")
                if sid:
                    ids.add(sid)
        elif isinstance(group, dict):
            for key, entry in group.items():
                if isinstance(entry, dict):
                    sid = entry.get("source_id") or key
                    ids.add(sid)
                else:
                    ids.add(key)
    return ids


def check_required_files(root: Path = ROOT) -> list[str]:
    issues = []
    for rel in REQUIRED_FILES:
        if not (root / rel).is_file():
            issues.append(f"Missing required file: {rel}")
    return issues


def check_json_parseable(root: Path = ROOT) -> list[str]:
    issues = []
    for path in root.rglob("*.json"):
        if any(p in path.parts for p in (".pytest_cache", "venv", ".git", "__pycache__")):
            continue
        try:
            load_json(path)
        except json.JSONDecodeError as exc:
            issues.append(f"Invalid JSON: {path.relative_to(root)} ({exc})")
    return issues


def load_dataset(root: Path = ROOT) -> pd.DataFrame:
    path = root / "data/processed/dataset.csv"
    return pd.read_csv(path, encoding="utf-8")


def check_dataset_columns(df: pd.DataFrame, schema: dict) -> list[str]:
    expected = schema_field_names(schema)
    actual = list(df.columns)
    issues = []
    if actual != expected:
        issues.append(
            f"Dataset columns mismatch.\nExpected fields: {expected}\nActual fields: {actual}"
        )
    return issues


def check_record_id(df: pd.DataFrame) -> list[str]:
    issues = []
    if "record_id" not in df.columns:
        return ["Critical: 'record_id' column is missing from the dataset."]
        
    if df["record_id"].isna().any() or (df["record_id"].astype(str).str.strip() == "").any():
        issues.append("record_id contains null or empty values")
    if df["record_id"].duplicated().any():
        dupes = df.loc[df["record_id"].duplicated(), "record_id"].unique().tolist()
        issues.append(f"Duplicate record_id values found: {dupes}")
    return issues


def check_source_id(df: pd.DataFrame, source_map: dict) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    
    if "source_id" not in df.columns:
        return ["Critical: 'source_id' column is missing."], []

    valid_ids = source_ids_from_map(source_map)

    if df["source_id"].isna().any() or (df["source_id"].astype(str).str.strip() == "").any():
        errors.append("source_id contains null or empty values")

    unknown = set(df["source_id"].dropna().astype(str)) - valid_ids
    if unknown:
        warnings.append(f"source_id values not registered in source_map.json: {sorted(unknown)}")
    return errors, warnings


def check_dynamic_schema_types(df: pd.DataFrame, schema: dict) -> list[str]:
    """Dynamically validates data types and constraints based on dataset_schema.json."""
    issues = []
    for field in schema.get("fields", []):
        col = field["name"]
        if col not in df.columns:
            continue
            
        field_type = field.get("type", "string")
        allowed_values = field.get("allowed_values")
        
        # 1. Check numeric fields
        if field_type in ("number", "integer", "float"):
            for idx, val in df[col].items():
                if pd.isna(val) or str(val).strip() == "":
                    if field.get("required", False):
                        issues.append(f"Required numeric field '{col}' is missing at row {idx}")
                    continue
                try:
                    float(val)
                except (TypeError, ValueError):
                    issues.append(f"Field '{col}' must be numeric. Found invalid value at row {idx}: {val!r}")
                    
        # 2. Check categorical controlled vocabularies (allowed_values)
        if allowed_values:
            for idx, val in df[col].dropna().items():
                val_str = str(val).strip()
                if val_str not in allowed_values:
                    issues.append(
                        f"Field '{col}' has invalid controlled vocabulary value {val!r} at row {idx}. "
                        f"Allowed values: {allowed_values}"
                    )
    return issues


def validate(root: Path = ROOT) -> tuple[list[str], list[str]]:
    """Runs all schema verification rules. Returns (errors, warnings)."""
    errors: list[str] = []
    warnings: list[str] = []

    errors.extend(check_required_files(root))
    errors.extend(check_json_parseable(root))

    dataset_path = root / "data/processed/dataset.csv"
    if not dataset_path.is_file():
        errors.append("Processed dataset.csv file does not exist.")
        return errors, warnings

    schema = load_json(root / "specs/dataset_schema.json")
    source_map = load_json(root / "specs/source_map.json")
    df = load_dataset(root)

    errors.extend(check_dataset_columns(df, schema))
    errors.extend(check_record_id(df))
    
    src_errors, src_warnings = check_source_id(df, source_map)
    errors.extend(src_errors)
    warnings.extend(src_warnings)
    
    # Run dynamic type and controlled vocabulary validations
    errors.extend(check_dynamic_schema_types(df, schema))

    return errors, warnings


def main() -> int:
    print("=== Launching Project Quality Assurance Matrix ===")
    errors, warnings = validate()
    
    for w in warnings:
        print(f"QA_WARNING: {w}")
    for e in errors:
        print(f"QA_ERROR: {e}")
        
    if errors:
        print(f"\n[FAILURE] Project validation failed with {len(errors)} error(s).")
        return 1
        
    print("\n[SUCCESS] All data pipeline integrity checks passed cleanly.")
    if warnings:
        print(f"({len(warnings)} non-blocking warning(s) flagged)")
    return 0


if __name__ == "__main__":
    sys.exit(main())