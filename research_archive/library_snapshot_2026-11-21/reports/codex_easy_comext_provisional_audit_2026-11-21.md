# Codex-reported Eurostat Easy Comext extraction — provisional audit

**Date:** 2026-11-21  
**Status:** Summary claims checked for arithmetic only; raw CSV has **not** been independently inspected.  
**Source route reported by user:** [Easy Comext](https://ec.europa.eu/eurostat/comext/newxtweb/mainxtnet.do), dataset `DS-059322`, statistical procedure `T`, reporter EU27_2020, partner Bangladesh, import flow, value EUR, 2012–2025.  
**Claimed raw file:** `/workspace/output/eu_imports_bangladesh_cn8_2012_2025.csv` (path in Codex's separate workspace; not mounted or present here).  
**Codex-reported row count:** 27,780 CN8-year observations and 0 duplicate product-year pairs (both unverified until file inspection).

## Reported reconciliation (arithmetically checked)

| Year | CN8 sum (EUR) | Official TOTAL (EUR) | Unallocated / TOTAL minus CN8 (EUR) | Difference / TOTAL |
|---|---:|---:|---:|---:|
| 2012 | 8,186,942,161 | 8,190,980,243 | 4,038,082 | 0.0493% |
| 2013 | 9,113,287,140 | 9,115,978,459 | 2,691,319 | 0.0295% |
| 2014 | 10,418,891,392 | 10,421,299,379 | 2,407,987 | 0.0231% |
| 2015 | 12,710,351,692 | 12,715,949,830 | 5,598,138 | 0.0440% |
| 2016 | 13,775,900,951 | 13,779,755,619 | 3,854,668 | 0.0280% |
| 2017 | 14,248,189,646 | 14,251,416,207 | 3,226,561 | 0.0226% |
| 2018 | 15,199,003,676 | 15,201,621,962 | 2,618,286 | 0.0172% |
| 2019 | 16,289,349,186 | 16,291,646,246 | 2,297,060 | 0.0141% |
| 2020 | 13,520,013,340 | 13,532,808,957 | 12,795,617 | 0.0946% |
| 2021 | 15,734,009,564 | 15,735,974,326 | 1,964,762 | 0.0125% |
| 2022 | 23,986,230,411 | 23,990,994,617 | 4,764,206 | 0.0199% |
| 2023 | 18,940,758,006 | 18,944,474,058 | 3,716,052 | 0.0196% |
| 2024 | 19,920,661,506 | 19,925,531,672 | 4,870,166 | 0.0244% |
| 2025 | 21,238,163,196 | 21,244,359,364 | 6,196,168 | 0.0292% |
| **All 14 years** | **213,281,751,867** | **213,342,790,939** | **61,039,072** | **0.0286%** |

## Provisional observations

- Every annual CN8 total is lower than the stated aggregate, consistent with potential unallocated/confidential product detail, but this cause is not yet verified. See [Eurostat ITGS metadata](https://ec.europa.eu/eurostat/cache/metadata/en/ext_go_detail_sims.htm), confidentiality section.
- Largest absolute and relative gap: **2020**, EUR 12,795,617 or 0.0946% of that year's official TOTAL.
- Smallest relative gap: **2021**, 0.0125%.
- 2025 CN8 sum: EUR 21,238,163,196; increase over 2024: **6.61%** (nominal euros). 2022 is the highest observed value in the supplied totals. This is not an independently confirmed Eurostat series.
- A strict zero-difference reconciliation requirement is **inappropriate** if confidentiality or non-allocated products genuinely prevent detailed lines from summing to the aggregate. Maintain the discrepancy as a separate annual measure and examine official flags/special product codes rather than forcing data to match.

## Validation required after receiving the actual CSV

1. Verify file hash, raw Easy Comext export and query selections, especially annual frequency, EU27_2020, partner BD, import flow, `T` statistical procedure, nominal EUR values, and query/export time.
2. Verify file row count 27,780; unique `(PRODUCT, YEAR)` keys; exactly 2012–2025; all CN8 codes eight ASCII digits with leading zeros preserved; numeric values and missing/status indicators.
3. Recalculate every annual sum; compare to an independent Easy Comext `TOTAL` extract with **exactly identical** selections. Audit the mismatch's product/confidentiality mechanism; do not treat it as zero trade or impute values across product lines.
4. Obtain CN8 nomenclature and official concordances for each year before interpreting apparent product entry/exit or product growth.
5. Confirm the export includes only detailed CN8, not aggregate HS2/4/6, special non-CN codes or duplicated revision/measurement dimensions. Check code-year validity.
6. Record Excel/CSV source provenance (export configuration, access date, software, hash, source link).
7. For downstream study: collect **competitor-origin annual CN8 values**, extra-EU/world product denominators, **net mass and supplementary quantities**, product-level **TARIC MFN and preferential tariff matrix**, origin rules and preference utilisation evidence.

## Audit conclusion

**Conditional progress:** If Codex's CSV and provenance checks pass, Bangladesh-only trade *value* for 2012–2025 is substantially complete. **Not yet fully validated in this workspace.** All complementary empirical thesis deliverables remain outstanding.