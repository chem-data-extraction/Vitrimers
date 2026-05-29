# Practice 5 — Cleaning, normalization and publication

> Follow `specs/cleaning_pipeline.json`. Run `scripts/build_dataset.py` and `scripts/validate_project.py`.

## Input files

- `data/extracted/pdf_extracted_records.csv`
- `data/extracted/web_extracted_records.csv`
- `data/interim/merged_records.csv`

## Cleaning steps

The pipeline executes systematic concatenation of rows (prioritizing manual PDF extractions). It triggers a column de-duplication filter (`~df.columns.duplicated()`) to strip out redundant axis artifacts, cleans random trailing spaces across critical structural fields, maps legacy identifiers (`dynamic_link_type`, `relaxation_temp_c`) to strictly requested validation tokens, and dynamically flags missing data structures.

## Normalization rules

- Structural identifiers are standardized into canonical dot-separated multi-component SMILES arrays.
- Numeric features ($T_g$, $\tau^*$, $E_a$) undergo continuous safe casting through floating-point filters, writing explicit `NaN` fields upon non-numeric data encounters to secure downstream computational consumption.
- Temperature records are uniformly mapped to Celsius (°C).

## Deduplication strategy

Row deduplication is enforced strictly using the unique `record_id` composite key. For web data lines arriving without pre-formatted keys, a safe incremental generator injects sequential strings (`rec_web_auto_00001`), protecting authentic screening entries from accidental collapse during `drop_duplicates` stages.

## Validation results

All criteria met perfectly:
- Errors: 0
- Warnings: 0 (The non-blocking `vashisth_lab` validation warning was successfully resolved by introducing comprehensive metadata configurations into `specs/source_map.json`).

## Final dataset description

- **Row count:** 8482 records
- **Targets covered:** Multi-component vitrimer polymer matrices across diverse chemistry classes (epoxy-acid, vinylogous urethanes, Schiff base imine networks, and silyl ether variants).
- **Date built:** 2026-05-29
- **Path:** `data/processed/dataset.csv`

## Publication readiness checklist

- [x] `dataset.csv` matches `specs/dataset_schema.json`
- [x] All `source_id` values documented in source map
- [x] LICENSE replaced
- [x] `CITATION.cff` completed
- [x] `dataset_card.md` updated
- [x] `reports/final_report.md` complete