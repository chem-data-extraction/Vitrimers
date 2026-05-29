# Practice 2 — Source map

## Source search strategy

*Keywords used:* `vitrimer stress relaxation activation energy Tg dynamic covalent bond`, `covalent adaptable networks vitrimers rheology Arrhenius plot tau`, `epoxy vitrimer transesterification transamination catalyst loading kinetics`, `polyurethane vitrimer transamination catalyst-free`

*Platforms searched:*
- Google Scholar — tracking primary literature citation networks and foundational landing texts.
- Elsevier ScienceDirect / Progress in Polymer Science — high-fidelity comprehensive review matrices.
- ACS Publications (Macromolecules / JACS) — synthetic protocols, materials screening, and raw kinetic sweeps.

*Snowballing:* Foundational review sheets (Hayashi 2025) served as citation anchors. Backward tracking led directly to landmark experimental protocols (Leibler/Montarnal 2011 for transesterification, Denissen 2015 for vinylogous urethanes). Forward tracking from Tretbar 2019 enabled extraction of exceptional thermal stability variants, while the high-throughput screening data stream from the Vashisth Lab repository provided statistical weight.

## Source groups

*journal_papers*

| source_id | citation | DOI | records | license |
|-----------|----------|-----|---------|---------|
| leibler_2011 | Montarnal et al. 2011 (*Science*) | 10.1126/science.1212648 | ~15 | Publisher Copyright |
| denissen_2015 | Denissen et al. 2015 (*Adv. Funct. Mater.*) | 10.1002/adfm.201502499 | ~12 | Publisher Copyright |
| tretbar_2019 | Tretbar et al. 2019 (*JACS*) | 10.1021/jacs.9b08876 | ~10 | Publisher Copyright |
| wang_2018 | Wang et al. 2018 (*Macromolecules*) | 10.1021/acs.macromol.8b01369 | ~11 | Publisher Copyright |
| hayashi_2025 | Hayashi et al. 2025 (*Prog. Polym. Sci.*) | 10.1016/j.progpolymsci.2025.102026 | ~30 | Publisher Copyright |

*supplementary_materials*

| source_id | parent_source_id | file_name | description |
|-----------|------------------|-----------|-------------|
| tretbar_2019_si | tretbar_2019 | tretbar_2019_jacs_si.pdf | Supporting information containing detailed raw relaxation points and synthesis ratios. |

*github_repositories*

| source_id | url | records | license |
|-----------|-----|---------|---------|
| vashisth_lab | https://github.com/vashisth-lab/VitrimerScreening | 8424 | Open Source / MIT |

## Normalization strategy

| source_group | normalization rule |
| :--- | :--- |
| `journal_papers` | Reconstruct operational metrics to standard metric integers; parse embedded graphs into numerical stress-relaxation lists. |
| `github_repositories` | Perform programmatic regex parsing to map raw case-heterogeneous properties into canonical schema parameters. |

## Conflict resolution

- **Overlapping records:** If a review matrix (Hayashi 2025) pools data rows directly from an explicit primary publication (Leibler 2011), the original experimental text is prioritized as the source of truth to avoid artificial sample inflation.
- **Divergent property definitions:** Retain entries as separate lines if independent operational validation modes are identified (e.g., tracking $T_g$ shifts across DSC vs. rheological loss peaks).

## Coverage gaps

| gap | reason | plan |
| :--- | :--- | :--- |
| Unstructured chemical acronyms | Literature uses commercial labels (e.g., DGEBA) instead of structural notations. | Deploy automated PubChem mapping to resolve nomenclature into multi-component component SMILES. |
| Missing metadata variables | Multi-component mixtures occasionally omit structural details for internal crosslinkers. | Set unresolvable accessory fragments to `NaN` fields, preserving validated structural backbones. |