# Bangladesh-origin EU27 imports, CN8, 2012–2025 — external verification memo

**Review date:** 21 November 2026  
**Outcome:** PROVISIONAL — annual arithmetic verified, row-level CSV NOT AVAILABLE for examination, and 2025 cross-source discrepancy unresolved.

## Provenance and scope

User supplied a summary from a separate Codex workspace of an Easy Comext DS-059322 export, statistical procedure `T`, EU27 imports from Bangladesh, 2012–2025, reported as 27,780 eight-digit product-year observations with no duplicate keys. The CSV was reportedly at `/workspace/output/eu_imports_bangladesh_cn8_2012_2025.csv` within Codex, but that path is **not mounted in this environment**. It was not present in conversation files or the saved research Library folder when checked on 21 November 2026. **No row-level assertions in the Codex summary can be independently verified until the actual CSV and export parameters are supplied.**

Easy Comext official dataset list, confirming DS-059322 exists: https://ec.europa.eu/eurostat/comext/newxtweb/mainxtnet.do

## Annual arithmetic verified from the figures supplied

| Year | CN8 sum (EUR) | Reported TOTAL (EUR) | Unallocated difference (EUR) | Absolute difference as % of reported TOTAL |
|---|---:|---:|---:|---:|
| 2012 | 8,186,942,161 | 8,190,980,243 | -4,038,082 | 0.0493% |
| 2013 | 9,113,287,140 | 9,115,978,459 | -2,691,319 | 0.0295% |
| 2014 | 10,418,891,392 | 10,421,299,379 | -2,407,987 | 0.0231% |
| 2015 | 12,710,351,692 | 12,715,949,830 | -5,598,138 | 0.0440% |
| 2016 | 13,775,900,951 | 13,779,755,619 | -3,854,668 | 0.0280% |
| 2017 | 14,248,189,646 | 14,251,416,207 | -3,226,561 | 0.0226% |
| 2018 | 15,199,003,676 | 15,201,621,962 | -2,618,286 | 0.0172% |
| 2019 | 16,289,349,186 | 16,291,646,246 | -2,297,060 | 0.0141% |
| 2020 | 13,520,013,340 | 13,532,808,957 | -12,795,617 | 0.0946% |
| 2021 | 15,734,009,564 | 15,735,974,326 | -1,964,762 | 0.0125% |
| 2022 | 23,986,230,411 | 23,990,994,617 | -4,764,206 | 0.0199% |
| 2023 | 18,940,758,006 | 18,944,474,058 | -3,716,052 | 0.0196% |
| 2024 | 19,920,661,506 | 19,925,531,672 | -4,870,166 | 0.0244% |
| 2025 | 21,238,163,196 | 21,244,359,364 | -6,196,168 | 0.0292% |

**Fourteen-year CN8 sum:** EUR 213,281,751,867. **Reported official TOTAL sum:** EUR 213,342,790,939. **Unallocated gap:** EUR 61,039,072, or 0.0286% of summed reported totals. These are arithmetic checks of user-supplied values, not independent source-download validation.

## Independent official aggregate comparison

The European Commission's **European Union, Trade with Bangladesh** factsheet, dated **20 May 2026** (page 3, Source Eurostat Comext, statistical regime 4), gives the following annual values **rounded to EUR million**:

| Year | Codex-reported annual TOTAL, EUR million | Commission fact sheet, EUR million | Difference, EUR million |
|---|---:|---:|---:|
| 2022 | 23,990.995 | 23,991 | -0.005 |
| 2023 | 18,944.474 | 18,939 | +5.474 |
| 2024 | 19,925.532 | 19,923 | +2.532 |
| 2025 | 21,244.359 | 21,179 | +65.359 |

**Source:** https://webgate.ec.europa.eu/isdb_results/factsheets/country/details_bangladesh_en.pdf (table 'Total goods: EU Trade flows and balance', page printed 3; PDF page index 2). The latest official factsheet page itself indicates 20-05-2026. Its 2025 value is **EUR 21,179 million**, which is EUR 65.359 million below the Codex-reported `TOTAL` (roughly 0.31%). This difference exceeds rounding and must be accounted for before claiming exact reconciliation with an independent series. However, a November 2026 Easy Comext extract may reflect statistical revisions after the Commission's May 2026 PDF, so this is a *flag*, not a finding of error.

Eurostat explains that confidentiality can cause true product values to be withheld at detailed level but remain in reporting-country totals, which is a plausible explanation for the small within-extract CN8-to-TOTAL gaps. It does **not**, without further evidence, explain a difference between separate published total-series vintages. See: https://ec.europa.eu/eurostat/cache/metadata/en/ext_go_detail_sims.htm

## Conditions for full verification

1. Obtain the actual CSV (the Codex `/workspace/output/...` path is not accessible across environments). Obtain the raw Easy Comext export or export manifest showing dataset, date/time/vintage, reporter, partner, flow, frequency/year, statistical procedure, indicator, and coverage.
2. Read CN8 as text, preserving leading zeroes. Verify exactly 14 years, 2012–2025; expected row count 27,780; unique `(year, CN8)` keys; year-level row counts, valid eight-digit products, numeric EUR values, no negative values unless the provider explicitly documents them; no duplicate records or unexpected dimensions.
3. Confirm `T` in DS-059322 means what the user claims and whether it is comparable to the statistical regime 4 series used in the Commission factsheet. Check whether any eight-digit aggregate/confidentiality codes are being treated as ordinary products.
4. Recompute annual totals from the CSV and compare line-for-line with the 14 reported CN8 sums; independently retrieve annual `TOTAL` from the **same export vintage and filter**, documenting reconciliation residuals.
5. Cross-check at least 2022, 2024 and 2025 against a **same-vintage** Comext `DS-045409` extraction with the equivalent reporter/origin/flow scope and investigate the 2025 difference from the Commission's May 2026 reference.
6. Obtain official annual CN lists / concordance before longitudinal product growth, top-200 cumulative rankings or regression; unreported cells are not automatically zero.

## Downstream thesis data still missing

Competitor-origin CN8-year trade values and market-share denominators, product quantities/unit values, year-specific CN nomenclature concordances, exact TARIC MFN/precedence preferences and effective dates, RoO eligibility, and preference-utilisation data remain outside the Codex-reported Bangladesh value-only extract.

**Decision:** label the Codex extract `REPORTED_OBTAINED; INDEPENDENT_FILE_QA_PENDING`, not `FULLY_VERIFIED`.