# Task E — Bangladesh/EU CN8–TARIC10 tariff and preference eligibility matrix

**Audit version:** v18  
**Prepared:** 21 November 2026  
**TARIC reference date:** 1 November 2026  
**Research:** University of Dhaka, MITB; Bangladesh post-LDC EU market access  
**Result:** Current source-dated source *candidate* tariff matrix built and independently audited; prospective post-graduation rate certification and product-specific rules of origin **not yet complete**.

## 1. What was independently established

All source records derive from the European Commission DG TAXUD public CIRCABC November 2026 TARIC archive, not an unverified tariff-rate website. Nine original XLSX files were downloaded via `https://circabc.europa.eu/service/api/node/workspace/SpacesStore/<node-id>/content`, timestamped and SHA-256 hashed. The original files, exact source URLs and their checksums are preserved in the GitHub thesis repository (`task_e_tariff_matrix/nov2026/official_source_xlsx/` and `source_file_receipts.json`). The independently executed audit (`refined_v18/INDEPENDENT_TARIFF_QA.json`) reported **passed=true**, **zero issues**, and verified **all 9 source hashes**.

Code: `task_e_tariff_matrix/build_official_taric2026.py`, `refine_taric_scenario.py`, and `qa_official_taric.py`. All are stored in the research repository. Source and computation outputs are reproducible without assuming a single CN8 has a single universal tariff for all origins and circumstances.

## 2. Dimensions and coverage

| Dimension | Verified result |
|---|---:|
| 2025 Bangladesh top-ranked CN8 products requested | 200 |
| CN8 products with current 2026 declarable TARIC10 matching leaves | 200 |
| 2026 TARIC10 leaves covering those CN8 products | 321 |
| Origin–TARIC10 rows, Bangladesh and six competitors | 2,247 |
| Origin–CN8 source-qualified summary rows | 1,400 |
| Relevant official active raw TARIC measure records | 2,997 |
| Applicable origin–tariff-measure candidates and conditions preserved | 16,202 |
| Current 2026 EBA Bangladesh tariff preference 0% at all relevant TARIC10 leaves | 321 / 321 |
| CN8 products with the same simple MFN ad valorem percentage across all relevant TARIC10 leaves | 196 / 200 |
| Distinct 2026 scheme-proxy TARIC10 records, three arrangements | 963 |
| Historical official duty rates for 2012–2025 | Not collected; reference date is 2026-11-01 |
| Effective post-2029/2032 Bangladesh duty amounts | Not enacted or independently established |

The official raw input comprises **Duties Import 01-99**, **Geographical areas composition**, **Measure exclusions**, **Measure conditions**, **Nomenclature EN**, **Declarable codes**, **Legal basis**, **Geographical areas description**, and **Measure footnotes**.

### Current 2026 source-qualified origin-rate coverage (of 200 CN8 products)

| Origin | Uniform simple MFN | Uniform type-142 tariff preference | Uniform type-106 customs union | One uniform simple *candidate* rate |
|---|---:|---:|---:|---:|
| Bangladesh (BD) | 196 | 200 | 0 | 200 |
| China (CN) | 196 | 0 | 0 | 196 |
| India (IN) | 196 | 184 | 0 | 196 |
| Vietnam (VN) | 196 | 192 | 0 | 193 |
| Pakistan (PK) | 196 | 197 | 0 | 199 |
| Cambodia (KH) | 196 | 152 | 0 | 200 |
| Türkiye (TR) | 196 | 4 | 193 | 199 |

**Important:** *Simple candidate* describes the published measure expression and origin/scheme match, not proof that an EU customs declaration satisfied origin, quota, anti-dumping, licensing, documentary, or other conditions; it is not the duty empirically paid. A 2026 snapshot is not legally valid for an arbitrary future date.

## 3. Concrete source-matched example: CN8 61091000, 1 November 2026

The 2026 TARIC nomenclature contains two relevant leaf subdivisions (`6109100010`, `6109100090`). The following percentages are identical across those leaves, based on corresponding official measures and source acts.

| Source scheme/origin | Candidate ad valorem percentage | Important qualification |
|---|---:|---|
| MFN / third-country type 103 | 12.0% | Other measures and customs conditions may apply |
| Bangladesh EBA (GSP type 142) | 0.0% | Requires preferential originating status/documentation |
| China (MFN) | 12.0% | Additional measures must be assessed independently |
| India Standard GSP | 9.6% | 2026 recorded preference, conditional |
| Vietnam FTA | 0.0% | Qualifying FTA origin rules required |
| Pakistan GSP+ | 0.0% | 2026 beneficiary and qualifying originating goods |
| Cambodia | 12.0% | This line affected by partial EBA withdrawal; no recorded 0% preference candidate |
| Türkiye customs union | 0.0% | Measure type **106**, not 142; A.TR/free-circulation and scope conditions |

Do **not** generalize the Cambodian or Turkish result to all products. The published measures vary by product, TARIC10 branch, and legal treatment.

The four 2025 Bangladesh CN8 lines lacking a single simple uniform 2026 MFN ad valorem percentage are `19023010`, `24012035`, `24012085`, and `39269097`. Their numeric MFN data remain **blank** in the simple-rate summary; all source expressions and qualifying TARIC10 subdivisions remain preserved in the detailed candidate matrix. The 2026 Bangladesh EBA measure is 0% in each but subject to originating-goods conditions.

## 4. Scenario interpretation and what has NOT been proved

- **2026 EBA baseline:** Bangladesh was included in the official group `2005` (`GSP-EBA`) on the dated snapshot; 0% basic preferential customs duty appears on all 321 TARIC10 leaf branches for the selected 200 CN8 lines. This does *not* establish preference utilisation.
- **2026 Standard GSP template:** group `2020` (India). A simple source-measure rate was available for 277/321 TARIC10 leaves; the other 44 are explicitly **not numerically populated**. Published source expressions remain in the candidate records.
- **2026 GSP+ template:** group `2027` (Pakistan). Simple source rates were available for 315/321 leaves; the remaining 6 are not filled by assumptions.
- **From 2027:** Regulation (EU) 2026/1395 replaces the prior GSP framework. Bangladesh will not automatically become a GSP+ beneficiary after losing EBA status. Eligibility, Commission designation, sensitive/non-sensitive product rules, possible graduation/section safeguards and rules of origin must be respected. India/Pakistan **2026** tariff rates are historical templates, *not* a certified Bangladesh statutory-rate matrix for 2027–2032.
- **LDC timetable:** Bangladesh's scheduled LDC graduation is 24 November 2029. The EBA transition under Article 17(2) provides for three years after a country ceases LDC status, but actual customs-effective withdrawal requires further EU legal action. **Late 2032 is a scenario date, not an enacted withdrawal date.**
- **Origin rule gap:** European Commission GSP guidance directs product-specific origin requirements to Annex 22-03 of Commission Delegated Regulation (EU) 2015/2446. Individual 200-product rules, origin-cumulation eligibility, certification and actual customs preference-utilisation have not been matched and authenticated in this matrix. This must remain a thesis limitation until completed.
- **TARIC temporal limitations:** source as-of 1 November 2026; daily 2–21 November updates have *not* been applied. The matrix is suitable as an explicitly dated comparison and scenario-input baseline, not for a claim of precise duties payable on 21 November.
- **TARIC nomenclature:** 2025 native CN8 trade codes mapped onto 2026 valid TARIC10 subdivisions. Year-specific historical concordance is still a Task B limitation.
- **Additional duty risk:** contingent duties, tariff quotas, anti-dumping, trade-defence, exemptions, sector/quantity-specific measures and documentary measures are retained in the detailed candidate file. Do not set an ad valorem number when conditions, multiple rates, compound duty expressions or different leaf rates obstruct a unique assignment.

## 5. Data artifact map (committed, preserved and verifiable)

1. **Original DG TAXUD source files / nine XLSX**: https://github.com/mafijulrigan39-boop/thesis/tree/main/task_e_tariff_matrix/nov2026/official_source_xlsx
2. **Source URLs, retrieval timestamp and original SHA-256**: https://github.com/mafijulrigan39-boop/thesis/blob/main/task_e_tariff_matrix/nov2026/source_file_receipts.json
3. **All source-backed candidate measures, legal dates, origin groups, conditions, additional codes and act refs**: https://github.com/mafijulrigan39-boop/thesis/blob/main/task_e_tariff_matrix/nov2026/all_tariff_measure_candidates_with_conditions.csv
4. **TARIC10 origin-by-origin refined rates and flags**: https://github.com/mafijulrigan39-boop/thesis/blob/main/task_e_tariff_matrix/refined_v18/taric10_country_refined_measure_matrix.csv
5. **200 CN8 × seven origins rate screen (1,400 rows)**: https://github.com/mafijulrigan39-boop/thesis/blob/main/task_e_tariff_matrix/refined_v18/CN8_country_source_qualified_rate_screen.csv
6. **2026 EBA / Standard GSP / GSP+ source templates (963 tariff10 rows)**: https://github.com/mafijulrigan39-boop/thesis/blob/main/task_e_tariff_matrix/refined_v18/Bangladesh_EBA_StandardGSP_GSPplus_2026_source_templates.csv
7. **Officially mapped product leaves**: https://github.com/mafijulrigan39-boop/thesis/blob/main/task_e_tariff_matrix/nov2026/taric10_leaf_mapping.csv
8. **Independent source and tariff candidate QA (passed; zero issues)**: https://github.com/mafijulrigan39-boop/thesis/blob/main/task_e_tariff_matrix/refined_v18/INDEPENDENT_TARIFF_QA.json
9. **Complete generated source metadata and coverage**: https://github.com/mafijulrigan39-boop/thesis/blob/main/task_e_tariff_matrix/nov2026/TASK_E_SOURCE_AND_COVERAGE.json
10. **Code / workflows**: https://github.com/mafijulrigan39-boop/thesis/tree/main/task_e_tariff_matrix

## 6. Strict research completion decision

**PASS for:** extraction of 1 November 2026 official 200-product EU tariff and origin-specific preference measures; 321 matched TARIC10 leaves; dated source legal references and conditions; origin grouping and Türkiye customs union; conditional present-day 2026 Standard GSP/GSP+ template; independently verified original source hashes and completeness.

**NOT YET PASS for:** certified *future* 2027/2032 country-specific EU duties for Bangladesh; verified 200-product rules of origin and actual preference use; monthly source updated to 21 November 2026; non-uniform and compound rates translated to an accurate ad valorem equivalent; fully harmonized historic tariff comparisons. These are not evidence of lost EU access or a tariff-induced fall in exports.

**Next empirical use:** after scheme/rule and scenario restrictions are documented, join only rates with unambiguous source-dated definitions to Task C's 2025 Bangladesh import values to compute explicitly labelled *static tariff-cost exposure*, separate from behavioural export-loss forecasts. Qualify all cases with missing rates or TARIC subdivisions and run MFN/GSP+/Standard GSP scenario sensitivity tests, with a distinct Article 33 safeguard assessment.

## 7. Official legal and methodological reference links

- TARIC (European Commission): https://taxation-customs.ec.europa.eu/customs/customs-tariff/eu-customs-tariff-taric_en
- Official TARIC snapshot distribution (CIRCABC): https://circabc.europa.eu/ui/group/0e5f18c2-4b2f-42e9-aed4-dfe50ae1263b/library/64db9d0f-e7c9-4084-afe9-f47e70e53c10
- Regulation (EU) 2026/1395: https://eur-lex.europa.eu/eli/reg/2026/1395/oj/eng
- Commission GSP origin rules: https://taxation-customs.ec.europa.eu/customs/rules-origin-goods/preferential-rules-origin/generalised-system-preferences-gsp_en
- Access2Markets GSP treatment / rules: https://trade.ec.europa.eu/access-to-markets/en/content/generalised-scheme-preferences-gsp
- Current EU-TR customs-union documentation: https://taxation-customs.ec.europa.eu/customs/customs-tariff/preferential-arrangements/preferential-origin/customs-unions_en