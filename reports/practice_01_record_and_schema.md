# Practice 1 — Record definition and dataset schema

## Topic

Vitrimer Thermomechanical Properties and Network Relaxation Kinetics Dataset.

## Scientific task

Collect experimentally reported glass transition temperatures ($T_g$), characteristic topology relaxation times ($\tau^*$), and Arrhenius activation energies ($E_a$) for covalent adaptable networks (vitrimers). This data will be used for downstream structure–property modeling (QSPR/ML) to evaluate how monomer composition, dynamic linkage type, catalyst identity/loading, and mechanical recycling cycles dictate network dynamics and thermal stability.

## One-record definition

**One record** = one experimentally reported thermomechanical or kinetic measurement for a specific vitrimer formulation (defined by its multi-component monomer SMILES mixture, dynamic linkage, and catalyst profile) under specific physical testing conditions from one identified source (one row in `data/processed/dataset.csv`).

## Examples of records

| Example | Why it counts |
|---------|----------------|
| Tg = 45.2°C and tau = 85 s at 170°C for epoxy-acid network (DGEBA + sebacic acid) with 5.0 mol% Zn(Acac)2, cycles = 0, Montarnal 2011, Table 1, DSC/Rheometry | Single measurement payload + component SMILES mixture + catalyst details + methods + source |
| tau = 92 s at 170°C for catalyst-free poly(vinylogous urethane) vitrimer, cycles = 4, Denissen 2015, Fig 3, DMA | Single kinetic measurement tied to a specific chemical formulation and a defined recycling cycle state |
| Tg = -53.0°C for catalyst-free PDMS network governed by silyl ether metathesis, cycles = 0, Zheng 2022, Table S2, DSC | Single thermomechanical properties baseline point + canonical components + identified source |

## Non-record examples

| Example | Why it is not a record |
|---------|-------------------------|
| "Epoxy-acid vitrimers typically undergo topology rearrangement and relax between 130°C and 180°C" | Vague statement, lacks a discrete numerical value or a specific stoichiometric monomer mixture |
| Raw stress relaxation curve plot (normalized modulus G/G0 over time) without tabulated or explicitly extracted tau values | Unparsed visual graphics; requires digitization or parsing to extract a single numeric value |
| Activation energy (Ea) predicted via Molecular Dynamics (MD) or Density Functional Theory (DFT) simulations | Not experimental; purely computational values are out of scope |
| Vitrimer recipe and relaxation kinetic data without knowing which paper or patent reported it | Missing provenance — cannot assign source_id or map lineage |

## Dataset fields

See `specs/dataset_schema.json` for full definitions. Summary:

| Field | Type | Required | Notes |
|-------|-------|----------|--------|
| `record_id` | string | yes | Stable unique ID, e.g., `rec_vit_epoxy_montarnal2011_pdf_001` |
| `polymer_name` | string | yes | Descriptive network name as given in source |
| `monomer_components_smiles` | string | yes | Dot-separated canonical SMILES of all monomers; sorted alphabetically |
| `dynamic_link_type` | string | yes | Predominant exchangeable bond pathway (e.g., transesterification) |
| `catalyst_name` | string | yes | Chemical name/abbreviation of catalyst; store "none" if catalyst-free |
| `catalyst_loading_mol_pct` | number | optional | Concentration in mol% relative to exchange groups; 0.0 if "none" |
| `tg_value_c` | number | yes | Glass transition temperature standardized to Celsius (°C) |
| `tg_measurement_method` | string | yes | Experimental technique for Tg: DSC / DMA_tan_delta / DMA_E_loss / TMA |
| `relaxation_time_s` | number | optional | Characteristic stress relaxation time ($\tau^*$) at 1/e threshold, in seconds |
| `relaxation_temp_c` | number | optional | Isothermal temperature condition (°C) during relaxation test |
| `relaxation_measurement_method` | string | optional | Rheometry_isothermal / DMA_stress_relaxation (Required if relaxation_time_s present) |
| `activation_energy_kj_mol` | number | optional | Arrhenius activation energy ($E_a$) for bond exchange kinetics |
| `recycling_cycles` | integer | yes | Mechanical processing run index; 0 = pristine/as-cured sample |
| `source_id` | string | yes | Links directly to source_map.json |
| `source_type` | string | yes | scientific_paper / database / github_repository / ml_dataset |
| `doi` | string | optional | Digital Object Identifier string when available |
| `conflict_flag` | boolean | optional | True if separate sources report highly anomalous kinetics for identical mix |
| `extraction_method` | string | optional | pdf_table / pdf_text_regex / manual / api |
| `notes` | string | optional | Curation notes, non-stoichiometric ratios, or curing profiles |

## Ambiguous cases

| Situation | Decision |
|-----------|-------------------------|
| Same vitrimer formulation measured across a high-temperature isothermal sweep (e.g., tau at 140°C, 150°C, 160°C) | Separate records for each isotherm; repeat chemical composition and Ea fields, but vary relaxation_temp_c and relaxation_time_s values |
| Tg reported via both DSC and DMA (tan delta peak) for the exact same network sample | Generate two independent records; capture respective methods in tg_measurement_method and unique values in tg_value_c |
| Kinetic parameters reported as a range (e.g., Ea = 85 ± 3 kJ/mol or Tg = 50–55°C) | Store the arithmetic midpoint or primary tabulated scalar value in the numeric field; preserve full range bounds string within the notes field |
| Cross-source duplication where the identical vitrimer recipe and data appear in both a paper and an aggregate database | Select the primary literature paper as the single source of truth; reject the duplicate database entry via pipeline deduplication rules |
| Qualitative property statements (e.g., "Tg reported as above room temperature") without a discrete scalar number | Exclude from numeric data fields; log qualitative context in notes or reject row if mandatory fields fail validation |
| Vitrimer components provided only as trade acronyms or abbreviations (e.g., DGEBA, MHHPA, Zn(acac)2) | Resolve acronyms into individual canonical structure notations in monomer_components_smiles; store full expansions in notes |
