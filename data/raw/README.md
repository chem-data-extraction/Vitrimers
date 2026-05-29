# Raw data

Store **unaltered** source files here. Do not edit files in this folder after download; add new versions with clear names instead.

## What belongs here

| Subfolder | Contents |
|-----------|----------|
| `pdf/` | Original primary literature PDF papers and supplementary characterization data files referenced in `specs/pdf_extraction_manifest.json` |
| `web/` | Raw CSV downloads or API payloads streamed from remote version-controlled repositories referenced in `specs/web_extraction_manifest.json` |
| `external/` | Third-party molecular screening reference files, material catalogs, or external high-throughput array snapshots |

## What does not belong here

- Consolidated or integrated database matrices (use `data/interim/`)
- Fully normalized, schema-compliant validation outputs (use `data/processed/`)
- Raw parsing outputs directly from extraction scripts (use `data/extracted/`)

Document each file’s specific `source_id`, download date, and upstream licensing parameters in your source map (`specs/source_map.json`) and corresponding practice reports.
