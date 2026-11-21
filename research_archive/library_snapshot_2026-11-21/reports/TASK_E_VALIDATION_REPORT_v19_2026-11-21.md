# Task E — Bangladesh/EU 200-product tariff and preference matrix

**Research record:** 21 November 2026 | **Customs measure reference date:** 1 November 2026  
**Dataset scope:** 200 2025 Bangladesh-origin CN8 lines; EU TARIC10; origins BD, CN, IN, VN, PK, KH, TR.  
**Decision:** **PASS for a source-linked, conditionally applicable 2026 tariff *candidate* matrix; NOT COMPLETE for legally operative prospective 2027/2032 Bangladesh GSP/GSP+ rates, actual preferential utilization, and product-specific origin verification.**

## 1. Authentic source and reproducibility

The pipeline downloaded **nine original Microsoft Excel tables directly from the European Commission DG TAXUD CIRCABC** November 2026 TARIC publication (`https://circabc.europa.eu/service/api/node/workspace/SpacesStore/<node-id>/content`). It did not infer rates from secondary websites or use generic rates by sector. Source receipts preserve exact URLs, UTC retrieval times, hashes, original source files and schema.

Primary source archive (GitHub): https://github.com/mafijulrigan39-boop/thesis/tree/main/task_e_tariff_matrix/nov2026_taric/official_sources  
Checksum receipts: https://github.com/mafijulrigan39-boop/thesis/blob/main/task_e_tariff_matrix/nov2026_taric/official_source_receipts.csv  
European Commission TARIC background: https://taxation-customs.ec.europa.eu/online-services/online-services-and-databases-customs/eu-customs-tariff-taric_en  
Original CIRCABC source directory: https://circabc.europa.eu/ui/group/0e5f18c2-4b2f-42e9-aed4-dfe50ae1263b/library/64db9d0f-e7c9-4084-afe9-f47e70e53c10

### Verified source SHA-256

| Original official workbook | SHA-256 |
|---|---|
| Duties Import 01-99.xlsx | `89865ebad02ce9d601e060025f4d709bdac4e008d2657c503f34f7efe019d3e2` |
| Geographical areas composition.xlsx | `c954658f3f9922d4115c3635d48e27344754d57fb252fada76bdbc86e6caf812` |
| Measure exclusions.xlsx | `8905b84789015edb0bfddb990214d2c535dd723402354ac150728a11a00bc78a` |
| Measure conditions.xlsx | `2c31f655a7ed19704246f457b3fb81137ab539879fb3ac88076b95931c6fac40` |
| Measure footnotes.xlsx | `761adb80947f8d8f0925adb28a14ae3c0bd36daa1ba304b68aafa4fe0dd6ab92` |
| Nomenclature EN.xlsx | `aee62e8b83da6cb8bb7605d7bce9a9ed13dc7055c956020173ed316415898ed0` |
| Declarable codes.xlsx | `56c63bfa579543b47287f3a202539caa567a68169d77a642201fad997303f75e` |
| Legal basis.xlsx | `8b9d3a5370a728a65162bd1ef1a48901012bc7a8229b0da020fd986e2dd2551a` |
| Geographical areas description.xlsx | `8a619c021144b7765d324b19ce38908392ec4aa341cfabcb66d56190816e1eea` |

Source hash verification: **9/9 passed**, independent GitHub-executed QA. Two independently implemented parsers agreed on **all 1,400 CN8-origin rate candidates**, with no rate/coverage mismatches.

## 2. Empirical source extraction

| Result | Count |
|---|---:|
| Selected 2025 CN8 product lines mapped to dated 2026 TARIC | 200/200 |
| Active declarable 10-digit TARIC leaves | 321 |
| TARIC10 × seven-origin combinations | 2,247 |
| CN8 × seven-origin combinations | 1,400 |
| Active raw TARIC duty and other-measure records relevant to goods | 2,997 |
| Source-linked origin × TARIC10 × measure evidence records | 16,202 |
| Consistent single-simple-ad-valorem candidate at CN8-origin level | 1,383 |
| Unresolved or non-simple duty candidate cells (blank, not imputed) | 17 |
| Independently checked source files | 9/9 |
| Independently cross-checked CN8-origin rate candidates | 1,400/1,400 |

The **1,383 valid candidates are conditional source measures, not necessarily applied border duties**. A rate can require preferential origin, REX/other proof, free-circulation/A.TR, a specific country or product, commodity subclassification, quota limits, or further conditions. Other charges and trade defence measures remain distinct.

### By origin (200 products each)

| Origin | Source-reported consistent simple candidate | Unresolved | Predominant source channel |
|---|---:|---:|---|
| Bangladesh (BD) | 200 | 0 | EBA tariff preference (200 zero candidates) |
| China (CN) | 196 | 4 | Third-country MFN benchmark |
| India (IN) | 196 | 4 | Standard GSP preference for 184, MFN for 12, subject to actual origin conditions |
| Vietnam (VN) | 193 | 7 | EVFTA preferences for 192, MFN for one |
| Pakistan (PK) | 199 | 1 | GSP+ preference for 197, MFN for two |
| Cambodia (KH) | 200 | 0 | EBA preference on 152; 48 fall back to MFN in this dated extraction (partial withdrawal matters) |
| Türkiye (TR) | 199 | 1 | Customs-union duty candidate on 193, other preferences on 4, MFN on 2 |
| **Total** | **1,383** | **17** | |

**No rate has been inserted for an unresolved origin-product combination.** Distinct unresolved lines include `19023010`, `24012085`, `24012035`, `39269097`, `62014010`, `62014090`, `62024090`, `64039996`, `64039998` (with different unresolved origin combinations). Complex expressions, e.g. `0.000% + 24.600 EUR DTN` for a Türkiye customs-union measure on `19023010`, are not simplified to zero or assigned an unsupported ad-valorem equivalent.

## 3. Selected product examples — all from the 1-Nov-2026 source

**Candidate preferential treatment is conditional, not an observed paid tariff.**

| CN8 | MFN | BD EBA | CN | IN | VN | PK | KH | TR |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 61091000 | 12% | 0% | 12% MFN | 9.6% GSP | 0% FTA | 0% GSP+ | 12% MFN candidate | 0% customs-union candidate |
| 61103099 | 12% | 0% | 12% MFN | 9.6% GSP | 0% FTA | 0% GSP+ | 0% EBA | 0% customs-union candidate |
| 64041990 | 16.9% | 0% | 16.9% MFN | 11.9% GSP | 0% FTA | 0% GSP+ | 0% EBA | 0% customs-union candidate |
| 03061792 | 12% | 0% | 12% MFN | 4.2% GSP | 0% FTA | 3.6% GSP+ | 0% EBA | 0% tariff-preference candidate |
| 19023010 | complex source measures | 0% EBA candidate | unresolved | unresolved | 0% candidate | unresolved | 0% EBA candidate | unresolved compound customs-union expression |

**Important correction:** For Türkiye, **measure type 106 Customs Union Duty** is separate from measure type **142 Tariff preference**. An A.TR/free-circulation eligibility assessment is necessary; applying MFN merely because there is no 142 tariff-preference record would be wrong. For Cambodia, EBA concessions have been partially withdrawn on certain lines, so it is not lawful to assign zero tariffs indiscriminately.

## 4. Documentary legal conditions recorded

Matching original source workbooks yielded:

- **452** applicable `Measure conditions.xlsx` rows;
- **117** applicable `Measure exclusions.xlsx` rows;
- **485** applicable `Measure footnotes.xlsx` rows.

These records preserve measure conditions, certificates, exclusion codes and footnotes exactly as printed in the official source. They are not substitutes for checking each product's **legal rules of preferential origin**. The European Commission explains that origin compliance and proper proof are requirements for claiming tariff preferences: https://trade.ec.europa.eu/access-to-markets/en/content/generalised-scheme-preferences-gsp and https://trade.ec.europa.eu/access-to-markets/en/content/quick-guide-rules-origin

Source tables and conditions:
- https://github.com/mafijulrigan39-boop/thesis/blob/main/task_e_tariff_matrix/nov2026_taric/dated_taric10_origin_measure_evidence.csv
- https://github.com/mafijulrigan39-boop/thesis/blob/main/task_e_tariff_matrix/nov2026_taric/measure_conditions_selected_original_source_rows.csv
- https://github.com/mafijulrigan39-boop/thesis/blob/main/task_e_tariff_matrix/nov2026_taric/measure_exclusions_selected_original_source_rows.csv
- https://github.com/mafijulrigan39-boop/thesis/blob/main/task_e_tariff_matrix/nov2026_taric/measure_footnotes_selected_original_source_rows.csv

## 5. Bangladesh GSP/EBA scenario legal boundary

Three **2026 comparator scheme extracts**, separately labelled templates (not legally operative future Bangladesh rates), contain:

| Source sample | TARIC10 scheme-template records | Meaning |
|---|---:|---|
| Bangladesh EBA 2026 | 321 | Present 2026 EBA measure candidates |
| India Standard GSP 2026 | 277 | Benchmark for potential future Standard GSP comparison, **not Bangladesh's statutory future rate** |
| Pakistan GSP+ 2026 | 315 | Benchmark for potential future GSP+, **not proof Bangladesh will qualify or receive those rates** |

**No defensible prediction of the 2027 or post-EBA tariff regime can be read straight from the 2026 TARIC snapshot.** The new GSP regulation **Regulation (EU) 2026/1395** applies principally from 1 Jan 2027; country eligibility, sensitive product treatment, specific duties and later measures must be established under the actual effective legal instrument. Bangladesh is currently scheduled for UN LDC graduation on 24 Nov 2029; a three-year EU EBA transition end around late 2032 is a scenario inference, not an automatically enacted customs date. GSP+ is **not automatic** and requires eligibility and approval.

Relevant law: https://eur-lex.europa.eu/eli/reg/2026/1395/oj/eng

*Future 2027/2032 Standard GSP, GSP+ and post-EBA MFN rates are left BLANK in the scenario matrices where unverified.*

## 6. Data files, reproducible code and exact interpretation

| Output | Link |
|---|---|
| CN8-origin **2026 conditional** rate screen, 1,400 records | https://github.com/mafijulrigan39-boop/thesis/blob/main/task_e_tariff_matrix/nov2026_taric/cn8_2026_origin_regime_aware_screen.csv |
| TARIC10-origin dated regime-aware candidates, 2,247 records | https://github.com/mafijulrigan39-boop/thesis/blob/main/task_e_tariff_matrix/nov2026_taric/origin_taric10_regime_aware_duty_candidates_2026.csv |
| Full source-measure evidence, 16,202 records | https://github.com/mafijulrigan39-boop/thesis/blob/main/task_e_tariff_matrix/nov2026_taric/dated_taric10_origin_measure_evidence.csv |
| Conditional 2026 EBA/GSP/GSP+ scenario benchmark template | https://github.com/mafijulrigan39-boop/thesis/blob/main/task_e_tariff_matrix/refined_v18/Bangladesh_EBA_StandardGSP_GSPplus_2026_source_templates.csv |
| Joined 2025 Bangladesh import trade values to 2026 tariff candidates | https://github.com/mafijulrigan39-boop/thesis/blob/main/task_e_tariff_matrix/nov2026_taric/TaskE_tariff_2026_join_2025_trade_values.csv |
| Independent QA of official sources and all 1,400 candidates | https://github.com/mafijulrigan39-boop/thesis/blob/main/task_e_tariff_matrix/nov2026_taric/INDEPENDENT_QA_AND_CROSSCHECK.json |
| Independent second processor QA | https://github.com/mafijulrigan39-boop/thesis/blob/main/task_e_tariff_matrix/refined_v18/INDEPENDENT_TARIFF_QA.json |
| Conditions and footnotes source retention QA | https://github.com/mafijulrigan39-boop/thesis/blob/main/task_e_tariff_matrix/nov2026_taric/LEGAL_CONDITIONS_PROVENANCE_AUDIT.json |
| Full original official Excel source workbook archive | https://github.com/mafijulrigan39-boop/thesis/tree/main/task_e_tariff_matrix/nov2026_taric/official_sources |
| Scripts to reproduce source downloads and analyses | https://github.com/mafijulrigan39-boop/thesis/tree/main/task_e_tariff_matrix |

## 7. Final decision and remaining work

**Task E 2026 source collection:** DONE, audited. **Task E future-scenario legal certification:** STILL OPEN. To close it fully before final thesis conclusions:

1. Validate CN8 2025→TARIC10 Nov 2026 product identity and classification-specific footnotes using official annual source lists and final Task B concordance.
2. Compile **legally applicable 2027+** Standard GSP product-sensitive treatment, including special tariff expressions and protective measures under Regulation (EU) 2026/1395; compare with current 2026 source templates without assuming they persist.
3. Treat Bangladesh GSP+ eligibility explicitly as conditional on application, convention compliance and EU approval; no proof of future qualification in the source.
4. Review product-specific rules of origin, evidence (REX; preference proof; A.TR for Türkiye), and relevant FTA staging. The study lacks shipment-level preference-utilization data.
5. Manually resolve or exclude 17 complex/ambiguous product-origin rate cells; preserve TARIC10 detail where CN8 aggregation is invalid.
6. Revalidate customs effective-date differences and any daily November TARIC updates before the analysis is frozen.

### Thesis-use language

Use: **“Indicative source-recorded tariff preference margins for the 1 November 2026 EU TARIC baseline, subject to product-specific origin rules and measure conditions.”**

Do not use: “Confirmed tariff Bangladesh will pay in 2032,” “all competitors pay MFN,” “observed trade losses caused by preference withdrawal,” or “zero is a certified realized duty without origin documents.”