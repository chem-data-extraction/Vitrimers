# Vitrimer thermomechanical properties and network relaxation kinetics

Publication-ready dataset for the course Extraction and preparation of chemical information.

**Topic:** Vitrimer thermomechanical properties and network relaxation kinetics dataset.

## Scientific task

Collect experimentally or computationally reported glass transition temperatures ($T_g$), characteristic topology relaxation times ($\tau^*$), and etc. for covalent adaptable networks (vitrimers) to enable downstream structure–property modeling (QSPR/ML) evaluating how monomer composition, dynamic linkage type, catalyst profile, and mechanical recycling cycles dictate network dynamics and thermal stability.

## What is one record?

One record = one experimentally or computationaly reported thermomechanical or kinetic measurement for a specific vitrimer formulation (defined by its multi-component monomer SMILES mixture, dynamic linkage, and catalyst profile) under specific physical testing conditions from one identified source (one row in `data/processed/dataset.csv`).

## Repository structure

| Path | Role |
|------|------|
| `project.json` | Machine-readable project metadata |
| `specs/` | JSON schemas, source map, manifests, pipeline, validation rules |
| `data/raw/` | Unmodified PDFs, web snapshots, external exports |
| `data/extracted/` | Extraction outputs (CSV + `extraction_log.jsonl`) |
| `data/interim/` | Merged table before final cleaning |
| `data/processed/` | Publication dataset (`dataset.csv`) |
| `scripts/` | Reproducible extract, build, clean, validate |
| `reports/` | Human-readable practice and final reports |
| `notebooks/` | Optional exploration only |
| `tests/` | Pytest checks for required artifacts |

**Formats:** JSON for specs and manifests; CSV for tabular data; Python for pipelines; Markdown for reports and documentation only. Notebooks are optional.

## Project components

1. **Record definition and dataset schema** — `specs/dataset_schema.json`, Practice 1 report  
2. **Source map** — `specs/source_map.json`, Practice 2 report  
3. **PDF extraction** — `specs/pdf_extraction_manifest.json`, `scripts/extract_pdf.py`, Practice 3 report  
4. **Web extraction** — `specs/web_extraction_manifest.json`, `scripts/extract_web.py`, Practice 4 report  
5. **Cleaning, normalization and publication** — `specs/cleaning_pipeline.json`, cleaning scripts, Practice 5 report  


## Data pipeline

```text
raw (PDF / web streaming interface)
  → extract (pdf + web python tools) → data/extracted/*.csv
  → build (consolidation) → data/interim/merged_records.csv
  → clean (normalization suite) → data/processed/dataset.csv
  → validate (strict automated rule checks + pytest suite)
```

## Required final artifacts

- `data/processed/dataset.csv` aligned with `specs/dataset_schema.json`
- Updated `specs/source_map.json` and extraction manifests
- Practice reports 1–5 and `reports/final_report.md`
- `dataset_card.md`, `LICENSE`, `CITATION.cff`
- Passing validation and tests

## How to run validation

```bash
pip install -r requirements.txt
python scripts/validate_project.py
pytest
```

## How to build the dataset

The dataset generation workflow consists of four sequential stages: extraction, aggregation, normalization, and publication. Each stage is implemented as an independent Python script to ensure reproducibility and modularity of the data processing pipeline.

### 1. Extraction (Data Ingestion)

#### PDF extraction

```bash
python scripts/extract_pdf.py
```

Parses target vitrimer literature using PDF extraction tools and manual verification procedures. Thermomechanical measurements, relaxation kinetics parameters, and associated metadata are extracted from tables, text blocks, and digitized figures and stored in:

```text
data/extracted/pdf_extracted_records.csv
```

#### Web extraction

```bash
python scripts/extract_web.py
```

Retrieves structured vitrimer data from online resources and supplementary datasets. Extracted records are standardized into tabular format and written to:

```text
data/extracted/web_extracted_records.csv
```

### 2. Aggregation and Harmonization

```bash
python scripts/build_dataset.py
```

Combines heterogeneous extraction outputs into a unified intermediate dataset. During this stage, the pipeline:

* merges records from all extraction sources;
* maps source-specific column names to the project schema;
* resolves duplicate or overlapping entries;
* generates unique record identifiers when required;
* exports the consolidated dataset to:

```text
data/interim/merged_records.csv
```

### 3. Normalization and Data Cleaning

```bash
python scripts/clean_dataset.py
```

Processes the merged dataset according to the rules defined in `specs/cleaning_pipeline.json`. The cleaning workflow includes:

* normalization of monomer SMILES representations;
* standardization of categorical values and null tokens;
* whitespace and formatting corrections;
* duplicate removal;
* validation of mandatory fields;
* schema compliance checks.

The finalized publication-ready dataset is exported to:

```text
data/processed/dataset.csv
```

### Complete workflow

To reproduce the dataset from scratch, execute the scripts in the following order:

```bash
python scripts/extract_pdf.py
python scripts/extract_web.py
python scripts/build_dataset.py
python scripts/clean_dataset.py
```

Upon successful completion, the final dataset will be available at:

```text
data/processed/dataset.csv
```


## License and citation

The project is fully prepared and distributed under the Creative Commons Attribution 4.0 International framework (CC-BY-4.0). Detailed indexing configurations and bibliographic records are maintained inside the operational files LICENSE and CITATION.cff.
