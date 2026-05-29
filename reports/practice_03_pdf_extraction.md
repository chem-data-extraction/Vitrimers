# Practice 3 — PDF extraction

> Aligned with `specs/pdf_extraction_manifest.json` and `data/extracted/pdf_extracted_records.csv`.

## Selected PDF sources

| source_id | pdf_id | Year (approx.) | Path |
|-----------|--------|----------------|------|
| leibler_2011 | science.1212648 | 2011 | data/raw/pdf/ |
| denissen_2015 | adfm.201502499 | 2015 | data/raw/pdf/ |
| tretbar_2019 | jacs.9b08876 | 2019 | data/raw/pdf/ |
| wang_2018 | macromol.8b01369 | 2018 | data/raw/pdf/ |
| hayashi_2025 | progpolymsci.102026 | 2025 | data/raw/pdf/ |

## Why these PDFs were selected

These files define the experimental anchor bounds of modern vitrimer engineering. They span diverse dynamic covalent pathways—ranging from classical catalyzed transesterification networks to catalyst-free vinylogous urethanes and exceptionally stable silyl ether metathesis frameworks. Including these primary papers guarantees high-fidelity, hand-verified benchmarks that complement the large-scale computational screening data.

## Pages used

- **leibler_2011:** Main text page 3 (Table 1 for relaxation metrics), page 4 (stress relaxation curves).
- **denissen_2015:** Pages 4–5 (rheological charts and characteristic topology timescales).
- **tretbar_2019:** Page 2 (Arrhenius tracking plots), plus Supplementary pages 12–15 for explicit structural stoichiometry.
- **hayashi_2025:** Pages 10–18 (comprehensive review index summarizing property clusters from adjacent literature).

## Extraction methods

Extraction combined manual tabular serialization with automated data extraction tools. `pdfplumber` was utilized to parse primary data layout structures from clean digital tables (Hayashi 2025), while manual transcription was applied to unstructured textual sentences and supplementary synthesis captions to avoid parsing artifacts. Continuous relaxation plots were digitized into discrete data points using graphical axis mapping software.

## Extracted fields

Primary structural data fields were mapped to `polymer_SMILES` and `dynamic_bond_type`. Operational conditions were logged in `temperature_C` and `time_s`, while performance metrics were standardly mapped into `relaxation_time_s`, `normalized_stress`, and `storage_modulus_Pa`.

## Extraction problems

- **Hidden multi-component stoichiometry:** Papers often report mass ratios or volumetric equivalents of monomers rather than structured chemical representations. This required external molecular weight calculations to reconstruct precise network mixtures.
- **Graphical data locking:** Critical relaxation rates were frequently embedded in log-scale figures without tabular counterparts, necessitating manual pixel-coordinate mapping to restore numerical values.

## Output files

- `data/extracted/pdf_extracted_records.csv` — Tabular collection of manual literature extractions.
- `data/extracted/extraction_log.jsonl` — Validation event logs tracing the successful ingestion of the PDF data streams.