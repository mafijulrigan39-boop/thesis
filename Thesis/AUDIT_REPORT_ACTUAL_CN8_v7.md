# Bangladesh-origin EU CN8 import dataset — completed row-level verification

**Audit date:** 21 November 2026

**Verdict: PASS for uploaded-file integrity and arithmetic; NOT YET independently authenticated against Eurostat download receipts or a live re-extraction.**

## Verified uploaded extract

- File: `eu_imports_bangladesh_cn8_2012_2025.csv`; original file preserved unchanged in this package.
- Dataset recorded in every row: `DS-059322`; frequency `A`; reporter `EU27_2020`; partner `BD`; flow `1`; procedure `T`; indicator `VALUE_IN_EUR`.
- Full original SHA-256: `7af0f75024828471b2c65ac0085fd2232926a61efbc29da080b0c68bd1a5d03e`.
- Observed rows **27,780**; distinct product codes **4,953**; fourteen years **2012–2025**; **0** duplicate year–code keys; **0** malformed eight-digit codes; **0** negative or nonnumeric values; **155** explicit zeros; **1,337** rows with leading-zero product codes.
- **690** product codes appear in each of the fourteen annual files and **1,242** appear only in one year; these are *observed* coverage counts, not validity dates or definitive classification-change counts.
- Original 27,780-row extract exactly reproduces all fourteen historical CN8-sum amounts reported by Codex. It contains no `TOTAL` rows: the reference TOTAL series comes from Codex's earlier separate summary, not this file.

## Annual CN8 reconciliation against *Codex-reported* aggregate TOTAL

| Year | CN8 rows | Sum CN8 (EUR) | Reported TOTAL (EUR) | Difference (EUR) | % of TOTAL |
|---|---:|---:|---:|---:|---:|
| 2012 | 1,480 | 8,186,942,161 | 8,190,980,243 | -4,038,082 | -0.0493% |
| 2013 | 1,548 | 9,113,287,140 | 9,115,978,459 | -2,691,319 | -0.0295% |
| 2014 | 1,570 | 10,418,891,392 | 10,421,299,379 | -2,407,987 | -0.0231% |
| 2015 | 1,632 | 12,710,351,692 | 12,715,949,830 | -5,598,138 | -0.0440% |
| 2016 | 1,639 | 13,775,900,951 | 13,779,755,619 | -3,854,668 | -0.0280% |
| 2017 | 1,687 | 14,248,189,646 | 14,251,416,207 | -3,226,561 | -0.0226% |
| 2018 | 1,792 | 15,199,003,676 | 15,201,621,962 | -2,618,286 | -0.0172% |
| 2019 | 1,828 | 16,289,349,186 | 16,291,646,246 | -2,297,060 | -0.0141% |
| 2020 | 1,851 | 13,520,013,340 | 13,532,808,957 | -12,795,617 | -0.0946% |
| 2021 | 2,400 | 15,734,009,564 | 15,735,974,326 | -1,964,762 | -0.0125% |
| 2022 | 2,589 | 23,986,230,411 | 23,990,994,617 | -4,764,206 | -0.0199% |
| 2023 | 2,635 | 18,940,758,006 | 18,944,474,058 | -3,716,052 | -0.0196% |
| 2024 | 2,534 | 19,920,661,506 | 19,925,531,672 | -4,870,166 | -0.0244% |
| 2025 | 2,595 | 21,238,163,196 | 21,244,359,364 | -6,196,168 | -0.0292% |

**Period total (actual observed CN8 records): €213,281,751,867.** The accumulated gap relative to the supplied aggregate totals is **€-61,039,072**, or **-0.02861%**. Every yearly gap is small and negative. Confidentiality / residual product categories are *plausible explanations* in Eurostat methodology, not established causes for this dataset. Do not rebalance CN8 values artificially.

## First empirically calculated results (Bangladesh's own product basket)

- 2025 Bangladesh-origin EU CN8 imports in this dataset: **€21,238,163,196**; change from 2024: **6.614%**.
- Chapters 61, 62 and 63 together: **€19,860,241,894** in 2025, or **93.512%** of the Bangladesh-origin CN8 basket.
- 2025 chapters 61 / 62 / 63: €11,778,130,101 / €7,696,236,209 / €385,875,584.
- 2025 CN8 within-Bangladesh concentration index **HHI = 423.66** on a 0–10,000 scale; top 10 observed lines explain **47.65%** of the basket and top 200 **97.89%**.
- These are Bangladesh-basket shares, **not** Bangladesh market shares in total EU demand. No competitiveness claims against other origin countries are justified by this CSV alone.

### Top ten Bangladesh CN8 product lines by 2025 recorded import value

| Rank | CN8 | 2025 EUR | Share of Bangladesh CN8 basket |
|---|---|---:|---:|
| 1 | `61091000` | 3,499,230,143 | 16.476% |
| 2 | `61103099` | 961,964,570 | 4.529% |
| 3 | `61102099` | 887,954,808 | 4.181% |
| 4 | `62034231` | 855,241,796 | 4.027% |
| 5 | `61102091` | 793,043,236 | 3.734% |
| 6 | `61046200` | 725,241,235 | 3.415% |
| 7 | `62034235` | 714,304,536 | 3.363% |
| 8 | `62046231` | 599,879,636 | 2.825% |
| 9 | `61051000` | 551,341,769 | 2.596% |
| 10 | `62052000` | 531,113,807 | 2.501% |

**Critical caveat:** Product names, year-specific CN8 code validity, splits/mergers and concordance are absent from the uploaded file. The 2025 ranking requires only 2025 values and is well-defined within the extract. The *2012–2025 raw-code ranking* and any raw-code YoY calculations are descriptive only, not classification-harmonized comparisons. `NA` product-year combinations are preserved as blank, not forced to zero.

## Difference from independently reported DS-045409 annual summary

The 14-year summary previously uploaded as `independent_reconciliation.csv` reports **27,846** CN8 observations for `DS-045409`, or **66 more** than the `DS-059322` CSV. Its CN8 sum is **€1,504,488 higher** while the aggregate TOTAL amounts differ by **€3 across the fourteen years** in total. This is not evidence of duplicates: data set, statistical procedure, source vintage, and handling of residual codes must be cross-reconciled using the underlying DS-045409 raw source records. The 14 SHA strings in the summary cannot be verified without the original downloads.

## What this **does not** validate

1. Actual upstream Eurostat file authenticity: the original Easy Comext export receipt, URL query parameters and raw original response are not included. A live re-extraction and reconciliation against the current public data release is necessary for full independent external verification.
2. CN8 classification validity and 2012–2025 concordances: official annual code lists and code-to-code correspondence tables are needed.
3. Competitor values, all-origin product-year totals and Bangladesh EU market shares: the provided file has only partner `BD`, so no competitor comparisons can be computed.
4. Net mass, supplementary quantities and comparable unit values: the file contains `VALUE_IN_EUR` only.
5. EU MFN / EBA / GSP / FTA origin-specific tariff matrices, rules of origin, preference utilisation and historical legal validity periods: none are present.
6. Article 33 Section S-11b beneficiary denominator / safeguard ratio and any post-LDC tariff-cost exposure: both require separate official inputs.

## Source URLs for independent external checking

- [Easy Comext dataset directory](https://ec.europa.eu/eurostat/comext/newxtweb/setupdimselection.do) — confirms `DS-059322` as an official dataset.
- [Comext API documentation](https://ec.europa.eu/eurostat/en/web/user-guides/data-browser/api-data-access/api-getting-started/comext-database).
- [Eurostat detailed trade methodology](https://ec.europa.eu/eurostat/cache/metadata/en/ext_go_detail_sims.htm) — confidentiality, source revisions, data scope and classification correspondence.
- [Eurostat EU Vocabularies](https://op.europa.eu/en/web/eu-vocabularies/eurostat) — year-specific CN code lists.

## Reproduce

```bash
python validate_and_rank_cn8.py --input eu_imports_bangladesh_cn8_2012_2025.csv --independent independent_reconciliation_DS045409_as_uploaded.csv --out ./results
python test_actual_uploaded_source.py eu_imports_bangladesh_cn8_2012_2025.csv
```

### Delivered files

- `annual_integrity_and_concentration_2012_2025.csv` — complete annual checks and HHI; reference TOTAL is external reported data.
- `top_200_cn8_2025_UNHARMONIZED.csv` — verified 2025 ranking; 2024 raw-code comparisons clearly labelled.
- `top_200_raw_code_period_2012_2025_UNHARMONIZED.csv` — exploratory period totals, not official CN8 concorded.
- `cn8_product_year_matrix_missing_not_zero.csv` — all 4,953 codes, 2012–2025, missing cells blank.
- `cn8_code_observation_coverage.csv` — observed years, **not** official classification-validity intervals.
- `chapter_by_year_descriptive.csv` — HS2 composition by year.
- `ds059322_vs_ds045409_comparison.csv` — 14-year summary comparison.
- `audit_manifest.json` — SHA, checks and data limitations.
- `Bangladesh_EU_CN8_RowLevel_Validation_v7.xlsx` — professionally formatted summary workbook with live formulas and source notes.
- Original uploaded extract, audit scripts, tests and earlier independent reconciliation CSV.

**Study-use decision:** Approved for transparently labelled *descriptive analysis of Bangladesh-origin reported 2025 CN8 values* and preliminary within-basket concentration. Not yet approved for harmonized longitudinal product analysis, competitive EU market shares, Article 33 calculations or quantified post-LDC tariff scenarios.