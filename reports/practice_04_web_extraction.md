# Practice 4 — Web extraction

## Selected web sites

| source_id | page_id | URL |
|-----------|---------|-----|
| vashisth_lab | vitrimer_screening_labeled | https://github.com/vashisth-lab/VitrimerScreening/blob/main/data/labeled.csv |

## Why these sites were selected

1. This asset contains the results of an end-to-end high-throughput screening (HTS) framework evaluating dynamic polymer network formulations via molecular dynamics and quantum chemistry.
2. The dataset contributes 8,424 structured rows, providing the statistical sample density required to train robust machine learning surrogate models.
3. It maps structural topologies (`polymer_SMILES`) directly to critical physical constants, including the glass transition temperature ($T_g$) and bond-exchange activation thresholds ($E_a$).

## Page structure

The target data source is a structured tabular data matrix hosted within a remote version-controlled repository tree.
- **Data Format:** Comma-Separated Values (CSV).
- **UI Layout:** Bypassed during extraction by routing requests directly around the GitHub blob interface to connect to the underlying raw content delivery network (`raw.githubusercontent.com`).
- **Metadata:** Top-row headers define property features; data lines flow continuously as a single automated block without pagination constraints.

## Extraction methods

Extraction was implemented in Python using an automated pipeline script (`scripts/extract_web.py`). The script initializes network connections using the `requests` library, streams the large remote payload safely via data chunks, saves the raw file to local storage, and parses the fields into memory using the `pandas` analytical framework.

## Data schema mapping

- Raw structural sequences map directly to `polymer_SMILES`.
- Operational temperatures map to `temperature_C`.
- Modeled kinetics and target markers map cleanly to `relaxation_time_s` or related parameters.
- Source tracking attributes are statically assigned to `vashisth_lab`.

## Extraction problems

1. **GitHub UI Wrapper Resolution:** Direct requests to the repository tree path retrieve HTML layout metadata rather than the underlying data matrix. This was resolved by dynamically altering the URI layout to target the raw text distribution server.
2. **Memory Overhead Protection:** Processing the large multi-megabyte stream in a single block can trigger buffer inflation. This was mitigated by implementing streaming chunk loops to protect system memory.
3. **Missing Value Standardization:** Discrepancies in empty-field formatting across columns were intercepted programmatically and mapped to standard null structures.

## Output files

- `data/raw/web/vitrimer_screening_labeled.csv` — Local cache of the unedited source file.
- `data/extracted/web_extracted_records.csv` — Formatted extraction matrix containing 8,424 rows.
- `data/extracted/extraction_log.jsonl` — Verification line documenting pipeline completion status.