# Final report

## Project summary

**Project Title:** Vitrimer thermomechanical properties and network relaxation kinetics dataset  
**Author:** Gleb Bondarenko  
**Dataset Version:** 0.3.0  
**Status:** Completed & Validated (100% Pytest Passing)

## Dataset goal

The dataset targets the consolidation of structural compositions and physical properties of covalent adaptable networks (vitrimers). It bridges the gap between traditional manual experimental trials and modern automated computational screening models. The collection supports quantitative structure–property relationship (QSPR) modeling and machine learning surrogate engineering to predict how monomer formulation, catalyst loading, and temperature controls dictate network topology relaxation, thermal stability, and recycling limits.

## Source summary

The database aggregates information from three key source sectors:
- **Journal Papers (5 sources):** High-fidelity experimental data points spanning classical transesterification baselines (Leibler 2011) to recent state-of-the-art polymer reviews (Hayashi 2025).
- **Supplementary Appendices:** Explicit stoichiometry matrices tracking crosslinker metrics and structural configurations.
- **GitHub High-Throughput Archives (1 source):** Large-scale molecular simulation arrays from the Vashisth Lab repository, contributing 8,424 records.
All data is compiled and distributed under the international CC-BY-4.0 license framework.

## Extraction summary

- **PDF Pipeline:** Extracted manually and via `pdfplumber` across 5 primary journal volumes. Addressed issues regarding unstructured acronym resolution and graphical coordinate recovery.
- **Web Pipeline:** Programmatically ingested 8,424 rows from the Vashisth Lab raw content interface using an automated Python script (`extract_web.py`).
Detailed stage insights are available within the Practice 3 and 4 reports.

## Cleaning and normalization summary

Data consolidation follows a multi-stage approach split across two specialized scripts:
1. `build_dataset.py` handles multi-source structural concatenation, renames heterogeneous input labels, resolves data row overlap, and assigns unique, trackable index hashes (`rec_web_auto_*`) to entries missing predefined primary keys.
2. `clean_dataset.py` applies string cleaning rules to eliminate carriage returns and whitespace from SMILES strings, maps non-standard textual missing value tokens (`none`, `-`, `nd`) to standard null states, and structures fields against the schema.

## Validation summary

Data integrity is fully verified. Running `python scripts/validate_project.py` completes cleanly with zero blocking validation failures. The comprehensive test suite (`pytest`) returns a perfect score: **9 passed tests out of 9 possible entries**, ensuring strict schema alignment and total source map traceability.

## Limitations

- Computational values obtained via molecular modeling represent idealized limits that do not capture real-world synthesis artifacts like incomplete curing or localized moisture contamination.
- Synthesis curing profiles and specific temperature-time ramps remain unstandardized across literature, requiring qualitative capture in the `notes` column.

## Final artifacts

| Artifact | Path |
|----------|------|
| Processed dataset | `data/processed/dataset.csv` |
| Interim merged database | `data/interim/merged_records.csv` |
| Dataset Schema Spec | `specs/dataset_schema.json` |
| Source Map Registry | `specs/source_map.json` |
| Dataset Metadata Card | `dataset_card.md` |
| Citation Blueprint | `CITATION.cff` |
| Project License | `LICENSE` |