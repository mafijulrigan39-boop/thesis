# Task C — Official EU competitor-origin trade and market-share dataset

**Project:** Bangladesh's Prospective EU Market-Access Exposure Following LDC Graduation — University of Dhaka MITB thesis  
**Verified:** 21 November 2026, approx. 07:13 UTC  
**Status: COMPLETE for selected 2025 top-200 product universe, raw official-origin values, extra-EU denominators, missingness controls and source audit. Historical product comparability remains conditional on Task B. Supplier HHI remains qualified.**

## Executive findings

An independent GitHub Actions extraction successfully accessed **Eurostat Comext DS-045409** (filtered SDMX-CSV, annual EU27_2020 reporter, partner origin unrestricted, imports flow 1, `VALUE_IN_EUROS`) using one 200-product batch per year. Eurostat source response contains `LAST UPDATE` **13/11/26 11:00:00** (at least in the inspected 2025 response). The original 14 official response CSVs, gzip-compressed, and complete URL/date/checksum receipts have been archived in the user's GitHub thesis repository.

| Metric | Audited outcome |
|---|---:|
| Calendar years | 2012–2025 (14) |
| Native CN8 products | 200, selected by 2025 Bangladesh import value |
| Requested product-year combinations | 2,800 |
| Direct official raw responses | 14 of 14 |
| Raw response SHA-256 matches | 14 of 14 |
| All-partner country and aggregate records | 312,194 |
| Strict seven-origin product-year rows | 19,600 |
| Valid Bangladesh product-level EU extra-EU shares | 2,686 of 2,800 |
| Ineligible/missing product-year shares | 114 — blank, **not zero** |
| Valid 2025 product-level shares | 200 of 200 |
| Leading 2025 non-EU suppliers per product | 5 per product; 1,000 records |
| Failed retrieval requests | 0 |
| Independent QA assertions | PASS, no reported issues |

Core origin-country panel: **Bangladesh (BD), China (CN), India (IN), Viet Nam (VN), Pakistan (PK), Cambodia (KH), and Türkiye (TR)**. In addition, the full response archives preserve *all reported partner origins*. The leading five non-EU suppliers per 2025 product were selected dynamically and can also include Tunisia, Egypt or other origins rather than being restricted to the six preselected competitors.

The market-share denominator is **the published extra-EU aggregate `EXT_EU27_2020` for the same year and CN8 product**, never the sum of intra-EU + extra-EU origins and never an inferred world total. Missing EU product-year shares are uncomputed and explicitly flagged.

## First thesis-relevant competitiveness result

For the 200 selected products in 2025, Bangladesh-origin EU imports sum to **€20,789,281,101**, compared with **€137,346,619,291** in extra-EU imports across the same 200 product codes, yielding a **15.1364% pooled value share**. This pooled figure is distinct from any individual product's EU market share and should not be generalized to all CN8 product lines. The Bangladesh values for these 200 products represent **97.8864%** of the original Bangladesh-only 2025 CN8 basket (€21,238,163,196).

Examples of authenticated 2025 Bangladesh CN8 market shares:

| CN8 | Bangladesh value (EUR) | Extra-EU value (EUR) | Bangladesh product-market share |
|---|---:|---:|---:|
| 61091000 | 3,499,230,143 | 6,864,603,305 | 50.975% |
| 61103099 | 961,964,570 | 4,259,004,154 | 22.587% |
| 61102099 | 887,954,807 | 2,567,653,081 | 34.582% |
| 62034231 | 855,241,796 | 2,539,762,383 | 33.674% |
| 61102091 | 793,043,236 | 2,486,783,052 | 31.890% |

The largest non-Bangladesh competitors on the sampled lines vary by product. For 61091000, Türkiye, India and China follow Bangladesh; for 61103099, China leads and Türkiye and Cambodia follow Bangladesh. Competition cannot be faithfully summarized by one country across all products.

## Annual market-share coverage

| Year | Share-ready CN8 codes | Not share-ready |
|---|---:|---:|
| 2012 | 187 | 13 |
| 2013 | 188 | 12 |
| 2014 | 189 | 11 |
| 2015 | 189 | 11 |
| 2016 | 189 | 11 |
| 2017 | 189 | 11 |
| 2018 | 189 | 11 |
| 2019 | 190 | 10 |
| 2020 | 189 | 11 |
| 2021 | 189 | 11 |
| 2022 | 199 | 1 |
| 2023 | 200 | 0 |
| 2024 | 199 | 1 |
| 2025 | 200 | 0 |
| **Total** | **2,686** | **114** |

Incomplete historical product-year observations must be interpreted in conjunction with **Task B's year-specific Combined Nomenclature classification validity and concordance records**. A code absent from older Eurostat records is not assumed to have zero trade; it may have been introduced after that date or changed definition.

## Independent technical audit

The dedicated QA program independently reconstructed the 312,194 raw country/product/year records from the 14 stored original Eurostat CSV responses, rechecked response hashes against the official request receipts, verified unique origin-product-year keys, checked all 19,600 named-origin cell values and missing-status flags, and recomputed all 2,800 market-share formulas using their matching extra-EU aggregate. **Independent QA passed with no issues.**

All origin rows and product market shares are therefore source-backed, but **supplier-origin concentration is intentionally qualified**. The named-country sum does not exactly equal the published extra-EU aggregate for each product. On the independent QA's whitelist of individual non-EU partner-country codes, all 200 of the 2025 products have a positive residual; 37 fall within 0.1% of the extra-EU total and 163 exceed that tolerance. The `supplier_concentration_bounded_2025.csv` file retains the observed supplier-share-squared index and a sensitivity bound assigning any positive residual to one unobserved supplier. Neither is represented as an exact complete-country HHI when the country sum is unreconciled. This residual can include classification/territory codes or other statistical differences; its administrative cause is **not established**.

**Do not use the year-specific raw 2025 CN8 code strings to infer fully harmonized 2012–2025 product growth without Task B concordance certification.** Origin comparisons *within each observed product-year* are source-consistent because they use the identical DS-045409 series. The 2025 comparison is native-2025 CN8.

## Deliverables and official source links

GitHub base: <https://github.com/mafijulrigan39-boop/thesis/tree/main/task_c_competitor_data/full>

1. **Official raw source archives:** [`full/raw/`](https://github.com/mafijulrigan39-boop/thesis/tree/main/task_c_competitor_data/full/raw) — 14 compressed official responses.
2. **Request provenance:** [`official_request_receipts.csv`](https://github.com/mafijulrigan39-boop/thesis/blob/main/task_c_competitor_data/full/official_request_receipts.csv) — URL, year, UTC retrieval date, SHA256, bytes and records.
3. **Full origin panel:** [`all_partners_2012_2025.csv.gz`](https://github.com/mafijulrigan39-boop/thesis/blob/main/task_c_competitor_data/full/all_partners_2012_2025.csv.gz) — all reported individual and aggregate partners, with values.
4. **Seven-origin clean panel:** [`seven_origin_2012_2025.csv`](https://github.com/mafijulrigan39-boop/thesis/blob/main/task_c_competitor_data/full/seven_origin_2012_2025.csv) — 19,600 rows.
5. **Extra-EU denominators and market shares:** [`product_year_bd_market_share_2012_2025.csv`](https://github.com/mafijulrigan39-boop/thesis/blob/main/task_c_competitor_data/full/product_year_bd_market_share_2012_2025.csv).
6. **Missingness:** [`missingness_market_share_register.csv`](https://github.com/mafijulrigan39-boop/thesis/blob/main/task_c_competitor_data/full/missingness_market_share_register.csv).
7. **Dynamic competitors:** [`top5_non_eu_suppliers_2025.csv`](https://github.com/mafijulrigan39-boop/thesis/blob/main/task_c_competitor_data/full/top5_non_eu_suppliers_2025.csv).
8. **Supplier concentration sensitivity:** [`supplier_concentration_bounded_2025.csv`](https://github.com/mafijulrigan39-boop/thesis/blob/main/task_c_competitor_data/full/supplier_concentration_bounded_2025.csv).
9. **Independent QA:** [`INDEPENDENT_QA_RESULT.json`](https://github.com/mafijulrigan39-boop/thesis/blob/main/task_c_competitor_data/full/INDEPENDENT_QA_RESULT.json).
10. **Source-backed annual coverage:** [`yearly_coverage.csv`](https://github.com/mafijulrigan39-boop/thesis/blob/main/task_c_competitor_data/full/yearly_coverage.csv).
11. **Reproducible scripts:** [`extract_task_c_fast_all_years.py`](https://github.com/mafijulrigan39-boop/thesis/blob/main/task_c_competitor_data/extract_task_c_fast_all_years.py) and [`qa_task_c_full.py`](https://github.com/mafijulrigan39-boop/thesis/blob/main/task_c_competitor_data/qa_task_c_full.py).

Dataset: Eurostat Comext DS-045409, SDMX CSV API <https://ec.europa.eu/eurostat/api/comext/dissemination/sdmx/2.1/data/DS-045409>; `freq=A`, `reporter=EU27_2020`, `flow=1`, `indicator=VALUE_IN_EUROS`, native CN8 `product`, annual `TIME_PERIOD`, unrestricted `partner`, with the explicit extra-EU group `EXT_EU27_2020`.

## Final decision and downstream dependencies

**Task C's acquisition and source-backed market-share requirement is now achieved for the agreed top-200 product universe.** The previously missing six competitor origins and other actual top suppliers, all-origin trade rows, extra-EU denominators, 14-year annual coverage, 114 missingness cases and source receipts exist in auditable files. This satisfies the Task C data completion criterion without pretending every historical cell is observed.

**Remaining elsewhere in the thesis project:** (a) official Task B CN8 historical concordance and economic product continuity; (b) Task D net mass/supplementary quantities (not included in this value-only dataset); (c) tariff and preferential scheme matrix (Task E), which is needed before preference erosion and exposure calculations; (d) final empirical scenario and robustness analyses. These are distinct from Task C and should not be marked complete by its success.