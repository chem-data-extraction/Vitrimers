# Processed data

This folder holds the **publication-ready** dataset: one row per record, columns aligned with `specs/dataset_schema.json`.

## Main file

- `dataset.csv` — Final schema-compliant dataset produced sequentially by the pipeline through `scripts/build_dataset.py` (aggregation) and `scripts/clean_dataset.py` (deep normalization and filtering), and fully verified via `scripts/validate_project.py`.

## Guidelines

- Always regenerate this file automatically by running the modular pipeline scripts; manual data overrides or direct cell editing within the CSV spreadsheet are strictly prohibited to ensure end-to-end procedural reproducibility.
- All template rows and structural test placeholding items must be completely overwritten by verified, project-specific vitrimer and network kinetics records before production deployment.
- Maintain rigorous provenance tracking by logging the current generation date, row metrics, and the repository commit hash in both `reports/final_report.md` and the definitive `dataset_card.md` artifact.
