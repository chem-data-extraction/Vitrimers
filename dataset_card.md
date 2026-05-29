# Dataset card — Vitrimer thermomechanical properties and network relaxation kinetics

## Dataset title

Vitrimer thermomechanical properties and network relaxation kinetics dataset (v0.3.0)

## Dataset summary

Tabular collection of experimentally reported and high-throughput screening benchmarks for covalent adaptable networks (vitrimers). The dataset includes structural multi-component monomer SMILES mixtures, dynamic linkage classifications, catalyst profiles, and critical physical parameters such as glass transition temperatures ($T_g$), topology relaxation times ($\tau^*$), and Arrhenius activation energies ($E_a$).

## Scientific task

Support structure–property modeling (QSPR/ML) and machine learning surrogate model training to evaluate how monomer composition, dynamic covalent chemistries, catalyst configuration, and mechanical recycling cycles dictate network dynamics, thermal stability, and reprocessability.

## Record unit

One row = one experimentally reported or computational screening measurement for a specific vitrimer formulation under defined physical testing conditions from one identified source.

## Data sources

Defined in `specs/source_map.json`: primary literature papers (e.g., Montarnal 2011, Denissen 2015), comprehensive review matrices (Hayashi 2025), and high-throughput screening data from the Vashisth Lab GitHub repository.

## Data extraction procedure

1. PDF: `scripts/extract_pdf.py` guided by tables in primary papers.
2. Web: `scripts/extract_web.py` executing programmatic ingestion of the `vashisth-lab/VitrimerScreening` raw data stream.
3. Logs: Automated append-only pipeline metadata written to `data/extracted/extraction_log.jsonl`.

## Data cleaning and normalization

`scripts/build_dataset.py` handles multi-source consolidation, executes duplicate column axis removal, maps case-heterogeneous keys into canonical schema fields (`polymer_SMILES`), generates stable composite IDs (`rec_web_auto_*`), and filters out any rows completely lacking structural chemical descriptors.

## Dataset schema

Field definitions, types, and constraints are located in `specs/dataset_schema.json`. Final columns are strictly aligned with the QA matrix requirements in `data/processed/dataset.csv`.

## Validation

Monitored via `specs/validation_rules.json`; verified locally using `scripts/validate_project.py` and structural validation suite via `pytest` (100% test completion).

## Known limitations

- Computational records from screening datasets represent modeled bounds rather than physical experimental assays.
- Trivial structural abbreviations from primary texts required external resolution via PubChem API mapping.
- Atmospheric post-curing profiles and exact temperature curing ramps are unstandardized and relegated to text buffers in the `notes` column.

## Recommended use

Predictive thermomechanical modeling, chemical space exploration for smart polymer networks, and benchmarking automated parsing architectures on polymer property tables.

## Not recommended use

Direct industrial synthesis optimization without re-verifying exact multi-step curing timeline protocols from the primary reference publications.

## License

CC-BY-SA 4.0 License (see `LICENSE`).

## Citation

See `CITATION.cff`. Updated with current author affiliations and repository URL.