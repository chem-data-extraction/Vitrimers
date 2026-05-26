# Practice 2 — Source map

## Source search strategy

*Keywords used:* `vitrimer stress relaxation activation energy Tg dynamic covalent bond`, `covalent adaptable networks vitrimers rheology Arrhenius plot tau`, `epoxy vitrimer transesterification transamination catalyst loading kinetics`, `polyurethane vitrimer transamination catalyst-free`

*Platforms searched:*

- Google Scholar — tracking primary literature and landmark citation networks
- Elsevier ScienceDirect / Progress in Polymer Science — state-of-the-art comprehensive vitrimer reviews
- ACS Publications (Macromolecules / JACS) — high-fidelity synthesis protocols and physical property sweeps
- Royal Society of Chemistry (RSC Chemical Science) — core theoretical frameworks and dynamic covalent library profiles

*Snowballing:* Comprehensive reviews by Van Zee 2020 and Hayashi 2025 served as the primary hubs for literature snowballing. Backward citation tracking from these reviews led directly to the discovery of foundational experimental profiles (Montarnal 2011 for epoxy-acid networks and Denissen 2015 for vinylogous urethanes). Forward snowballing from Wang 2018 allowed for the integration of biobased Schiff base dynamic network variants.

## Source groups

*scientific_papers (5 sources)*

| source_id | citation | DOI | records | license |
|-----------|----------|-----|---------|---------|
| paper_montarnal_2011 | Montarnal et al. 2011 (*Science*) | 10.1126/science.1212648 | ~15 | Publisher Copyright |
| paper_denissen_2015 | Denissen et al. 2015 (*Adv. Funct. Mater.*) | 10.1002/adfm.201502283 | ~20 | Publisher Copyright |
| paper_wang_2018 | Wang et al. 2018 (*Macromolecules*) | 10.1021/acs.macromol.8b01360 | ~12 | Publisher Copyright |
| paper_li_2018 | Li et al. 2018 (*Macromolecules*) | 10.1021/acs.macromol.8b00922 | ~10 | Publisher Copyright |
| review_hayashi_2025 | Hayashi & Ricarte 2025 (*Prog. Polym. Sci.*) | 10.1016/j.progpolymsci.2025.102026 | ~85 | Publisher Copyright |

*paper_montarnal_2011* — The foundational experimental baseline for transesterification-based epoxy-acid vitrimers. Contains essential kinetic sequences tracking $\tau^*$ over varied high-temperature isotherms, alongside explicit concentration effects of zinc catalysts ($\text{Zn(Acac)}_2$). Extracted via `pdf_table` and `pdf_text_regex`.

*paper_denissen_2015* — Core source for catalyst-free transamination of vinylogous urethane vitrimers. Crucial for structural tracking over mechanical aging loops, providing continuous measurements for samples undergoing multiple mechanical reprocessing steps (`recycling_cycles` from 0 to 4). Extracted via `pdf_table`.

*paper_wang_2018* — Supplies experimental thermomechanical and relaxation parameters for bio-based Schiff base (imine-exchange) covalent adaptable networks derived from vanillin precursors. Extracted via manual curation and `pdf_table`.

*paper_li_2018* — Focuses on dual-network topologies containing mixed permanent and dynamic cross-links. Vital for analyzing creep suppression and its direct coupling to topology rearrangement kinetics. Extracted via `pdf_table`.

*review_hayashi_2025* — The primary bulk aggregation matrix for this project. Compiles independently reported physical benchmarks ($T_g, \tau^*, E_a$) for ~85 distinct chemical systems across diverse linkage families into comprehensive evaluation tables. Extracted using programmatic ingestion (`api` via pandas transformation of spreadsheet assets or text mining).

*databases (0 sources)*

No open centralized database (such as PoLyInfo or Polymer Genome) natively tracks dynamic vitrimer relaxation lifetimes ($\tau^*$) or Arrhenius activation energy ($E_a$) bounds alongside structural monomer SMILES matrices. Literature curation remains the sole pathway for data aggregation.

*aggregators (1 source)*

| source_id | service | purpose |
|-----------|----------|--------------|
| agg_pubchem_api | PubChem PUG-REST API | Resolution of trivial monomer names and trade acronyms (e.g., DGEBA, MHHPA, IPDA) into clear, canonical multi-component SMILES strings |

*ml_datasets (1 source)*

| source_id | URL / DOI | records | use |
|-----------|-----------|---------|-----|
| review_lucherelli_2022 | 10.1016/j.progpolymsci.2022.101515 | ~40 | Supplementary data cross-validation for bio-based vitrimer matrices |

## Priority sources

| priority | source_id | reason |
|-----------|----------|--------------|
| 1 | review_hayashi_2025 | Highest data volume (~85 records); provides an independently curated, unified table of kinetics spanning multiple vitrimer subfamilies |
| 2 | paper_denissen_2015 | Authoritative source for recycling loop trajectories (cycles 0–4) and catalyst-free kinetics |
| 2 | paper_montarnal_2011 | Baseline standard for transesterification and catalyst loading dependency configurations |
| 3 | paper_wang_2018 | Expanded chemical library diversity covering bio-derived imine exchange systems |
| 3 | paper_li_2018 | Essential baseline for networks with non-dynamic cross-link background noise |
| 4 | review_lucherelli_2022 | Out-of-sample data validation specifically for sustainable/bio-derived formulations |
| 4 | agg_pubchem_api | Structural verification pipeline stage — resolves building-block notation errors into SMILES |

## Access conditions

| source_id | terms of service | extraction_method | data available |
|-----------|------------------|-------------------|----------------|
| paper_montarnal_2011 | Copyrighted — research access only | pdf_table / pdf_text_regex | Main text tables and SI data spreadsheets |
| paper_denissen_2015 | Copyrighted — research access only | pdf_table | Tabulated stress-relaxation arrays and text points |
| paper_wang_2018 | Copyrighted — research access only | manual | Text profiles and localized table data |
| paper_li_2018 | Copyrighted — research access only | pdf_table | Detailed physical characterization appendix |
| review_hayashi_2025 | Copyrighted — research access only | api (pandas ingestion) | Comprehensive literature compilation tables |
| agg_pubchem_api | Public Domain | api (PUG-REST requests) | Monomer canonical identifier strings |
| review_lucherelli_2022 | Copyrighted — research access only | manual | Focused bio-based vitrimer performance indexes |

## Expected data types

| source_id | format | fields available in schema |
|-----------|--------|----------------------------|
| paper_montarnal_2011 | PDF | polymer_name, catalyst_name, catalyst_loading_mol_pct, tg_value_c, tg_measurement_method, relaxation_time_s, relaxation_temp_c, activation_energy_kj_mol |
| paper_denissen_2015 | PDF | polymer_name, dynamic_link_type, tg_value_c, tg_measurement_method, relaxation_time_s, relaxation_temp_c, recycling_cycles |
| paper_wang_2018 | PDF | polymer_name, dynamic_link_type, tg_value_c, relaxation_time_s, relaxation_temp_c, activation_energy_kj_mol |
| paper_li_2018 | PDF | polymer_name, tg_value_c, relaxation_time_s, relaxation_temp_c, notes |
| review_hayashi_2025 | PDF / XLSX | polymer_name, monomer_components_smiles, dynamic_link_type, catalyst_name, tg_value_c, relaxation_time_s, relaxation_temp_c, activation_energy_kj_mol |
| agg_pubchem_api | JSON | monomer_components_smiles |
| review_lucherelli_2022 | PDF | polymer_name, dynamic_link_type, tg_value_c, activation_energy_kj_mol, notes |

*Fields not covered by any automated, programmatic extraction framework:* detailed multi-step temperature curing timelines and exact post-curing atmospheric settings. These factors are routed as unstructured character buffers directly into the optional `notes` field.

## Expected conflicts and overlaps

| overlap | sources | resolution rule |
|---------|---------|-----------------|
| Foundational records (e.g., Montarnal 2011 formulations) compiled inside the `review_hayashi_2025` bulk data matrix | `review_hayashi_2025` + `paper_montarnal_2011` | Retain both rows; flag original tracking via `source_id`. If property values match identically, mark review entries with a reference note. If numerical properties deviate due to review-level averaging, trigger `conflict_flag = True`. |
| Bio-derived formulations shared across separate systemic evaluations | `review_lucherelli_2022` + `review_hayashi_2025` | Enforce primary authorship hierarchy; fallback to the oldest primary literature source containing explicit testing method logs (`tg_measurement_method`). |
| Multi-method records for identical chemical strings within a single publication | `paper_*` | Retain all records as separate lines if physical parameters or measurement conditions differ (e.g., different rheology configurations or distinct $T_g$ methods). |

## Coverage gaps

| gap | reason | plan |
| :--- | :--- | :--- |
| Unstructured / missing monomer SMILES | Papers typically report trivial abbreviations (e.g., TREN, DGEBA) rather than canonical structural strings | Route abbreviations through `agg_pubchem_api` via an automated preprocessing script to resolve structures into canonical dot-separated SMILES. |
| Missing catalyst loading parameters | Complex multicomponent descriptions often omit clear molar base ratios relative to active link sites | Calculate ratios programmatically from stoichiometry text patterns where possible; otherwise, input `null` and document the system as non-stoichiometric in `notes`. |
| Ambiguity in $T_g$ measurement configurations | Comprehensive review tables often pool DSC, DMA ($\tan \delta$), and TMA values into a single column without explicit classification labels | Cross-reference conflicting rows against primary source text to reconstruct the missing `tg_measurement_method` classification. |
| Extrapolation error within relaxation datasets | Some reports plot Arrhenius curves visually without explicitly indexing data points in tabular form | Utilize automated digitization tools to digitize coordinates from linear charts, map points to numerical pairs, and record them with a "digitized" tag in `extraction_method`. |
