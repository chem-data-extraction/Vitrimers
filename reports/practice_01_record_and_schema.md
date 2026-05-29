# Practice 1 — Record definition and dataset schema

## Topic

Vitrimer thermomechanical properties and network relaxation kinetics.

## Scientific task

Collect experimentally reported glass transition temperatures ($T_g$), characteristic topology relaxation times ($\tau^*$), and Arrhenius activation energies ($E_a$) for covalent adaptable networks (vitrimers). This dataset enables downstream structure–property modeling (QSPR/ML) to evaluate how monomer composition, dynamic linkage type, catalyst profile, and mechanical recycling cycles dictate network dynamics and thermal stability.

## One-record definition

**One record** = one experimentally reported or high-throughput computational screening measurement for a specific vitrimer network formulation (defined by its multi-component monomer SMILES mixture, dynamic covalent bond chemistry, and catalyst configuration) under specific physical testing conditions from one identified source (one row in `data/processed/dataset.csv`).

## Examples of records

| Example | Why it counts |
|---------|----------------|
| $T_g = 45.2^\circ\text{C}$ and $\tau^* = 85\text{ s}$ at $170^\circ\text{C}$ for an epoxy-acid network (DGEBA + sebacic acid) with 5.0 mol% $\text{Zn(acac)}_2$, cycles = 0, Montarnal 2011, Table 1, DSC/Rheometry. | Single experimental measurement payload + exact component SMILES mixture + catalyst loading + characterization method + provenance. |
| $\tau^* = 92\text{ s}$ at $170^\circ\text{C}$ for catalyst-free poly(vinylogous urethane) vitrimer, cycles = 4, Denissen 2015, Figure 3, DMA. | Single stress relaxation kinetic entry tied to a specific chemical structure and an explicit degradation/recycling cycle iteration. |
| $T_g = 105^\circ\text{C}$ and $E_a = 93.4\text{ kJ/mol}$ for modeled epoxy-transesterification network, computational screening profile, vashisth_lab, ID rec_web_auto_00124. | Single high-throughput screening or simulation payload mapping an automated structural formulation onto physical limits. |

## Ambiguous cases

| Situation | Decision |
|-----------|-------------------------|
| Same vitrimer formulation measured across a high-temperature isothermal sweep (e.g., $\tau^*$ at $140^\circ\text{C}$, $150^\circ\text{C}$, $160^\circ\text{C}$). | Split into separate records for each isotherm; repeat structural fields and $E_a$, while varying `temperature_C` and `relaxation_time_s`. |
| $T_g$ reported via both DSC midpoint and DMA ($\tan \delta$ peak) for the exact same sample. | Generate two independent rows to capture distinct operational variables; track methods in notes and numerical targets in `temperature_C`. |
| Kinetic parameters reported as a explicit range bounds (e.g., $E_a = 85 \pm 3\text{ kJ/mol}$ or $T_g = 50\text{--}55^\circ\text{C}$). | Store the mathematical arithmetic midpoint as the primary scalar value; log the raw textual uncertainty bounds within the notes buffer. |
| Structural parameters provided only as trade acronyms or local synthesis labels (e.g., DGEBA, TREN, IPDI). | Resolve structural nomenclature via PubChem API into explicit dot-separated canonical component SMILES strings. |
| Qualitative property statements (e.g., "dynamic network shows complete stress relaxation above room temperature") without discrete numbers. | Reject the row from quantitative evaluation arrays; preserve text context inside the notes field if structural composition is verified. |