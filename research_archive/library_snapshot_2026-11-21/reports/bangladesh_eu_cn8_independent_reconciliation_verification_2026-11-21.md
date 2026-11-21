# Bangladesh–EU CN8 2012–2025: uploaded reconciliation audit

**Audit date:** 21 November 2026  
**Input:** User-provided `independent_reconciliation.csv` (14 summary rows).  
**Input file SHA-256:** `c41c1d18e0909abb1142c8c4f436d028443a0ed4f22c46e04becb4490648cd41`  
**Validation decision:** **SUMMARY ARITHMETIC VERIFIED; ORIGINAL PRODUCT-YEAR DATA AND RAW RESPONSE HASHES NOT VERIFIED.**

## Scope of validation

The uploaded CSV is an annual reconciliation summary, **not** the CN8 product-year trade panel. It does not contain `PRODUCT` or individual `OBS_VALUE` records. Therefore it cannot establish unique product-year keys, code validity, historical nomenclature consistency, product rankings, or origin-specific competitiveness.

## Checks actually executed

- Exactly 14 annual summary rows, one per year 2012–2025.
- Every `DIFF_EUR` equals `CN8_SUM_EUR − REPORTED_TOTAL_EUR`.
- Every `DIFF_PERCENT` equals `100 × DIFF_EUR / REPORTED_TOTAL_EUR`, to six-decimal reported precision.
- All reported differences are negative; maximum absolute annual proportional gap is approximately 0.093400% (2020).
- All 14 `SOURCE_SHA256` fields are 64-character lowercase hexadecimal strings, **but** raw response bytes were not attached and the hashes cannot be verified against original exports.
- The source URL column states Eurostat Comext `DS-045409`, annual EU27_2020 reporter, BD partner, import flow, euro value indicator; no successful network fetch or raw payload validation was performed from this file.

## Period summary

| Metric | Uploaded reconciliation | Earlier Codex report | Difference |
|---|---:|---:|---:|
| Number of annual entries | 14 | 14 | 0 |
| Total reported CN8 product-year rows | 27,846 | 27,780 | +66 |
| Sum of annual CN8 values (€) | 213,283,256,355 | 213,281,751,867 | +1,504,488 |
| Sum of annual reported TOTAL values (€) | 213,342,790,942 | 213,342,790,939 | +3 |
| CN8 minus TOTAL (€) | -59,534,587 | -61,039,072 | +1,504,485 |
| Aggregate residual / reported TOTAL | -0.027906% | -0.028611% | — |

## Annual source reconciliation and cross-extract comparison

| Year | Reported CN8 rows | Uploaded CN8 value (€) | Uploaded TOTAL (€) | Gap (€) | Gap % | New CN8 minus earlier Codex (€) | New TOTAL minus earlier (€) |
|---|---:|---:|---:|---:|---:|---:|---:|
| 2012 | 1,482 | 8,186,962,160 | 8,190,980,243 | -4,018,083 | -0.049055% | +19,999 | +0 |
| 2013 | 1,551 | 9,113,304,068 | 9,115,978,458 | -2,674,390 | -0.029337% | +16,928 | -1 |
| 2014 | 1,574 | 10,419,000,337 | 10,421,299,379 | -2,299,042 | -0.022061% | +108,945 | +0 |
| 2015 | 1,635 | 12,710,410,629 | 12,715,949,829 | -5,539,200 | -0.043561% | +58,937 | -1 |
| 2016 | 1,642 | 13,776,027,170 | 13,779,755,619 | -3,728,449 | -0.027057% | +126,219 | +0 |
| 2017 | 1,692 | 14,248,264,592 | 14,251,416,204 | -3,151,612 | -0.022114% | +74,946 | -3 |
| 2018 | 1,798 | 15,199,083,229 | 15,201,621,963 | -2,538,734 | -0.016700% | +79,553 | +1 |
| 2019 | 1,835 | 16,289,487,304 | 16,291,646,245 | -2,158,941 | -0.013252% | +138,118 | -1 |
| 2020 | 1,856 | 13,520,169,329 | 13,532,808,960 | -12,639,631 | -0.093400% | +155,989 | +3 |
| 2021 | 2,405 | 15,734,144,431 | 15,735,974,328 | -1,829,897 | -0.011629% | +134,867 | +2 |
| 2022 | 2,592 | 23,986,304,014 | 23,990,994,619 | -4,690,605 | -0.019552% | +73,603 | +2 |
| 2023 | 2,641 | 18,940,922,701 | 18,944,474,058 | -3,551,357 | -0.018746% | +164,695 | +0 |
| 2024 | 2,541 | 19,920,851,710 | 19,925,531,672 | -4,679,962 | -0.023487% | +190,204 | +0 |
| 2025 | 2,602 | 21,238,324,681 | 21,244,359,365 | -6,034,684 | -0.028406% | +161,485 | +1 |

## Interpretation and unresolved questions

1. The source summary is **internally consistent**. Its monetary total differs from the earlier Codex CN8 totals by **€1,504,488**, while the aggregate `TOTAL` sums differ by only **€3**.
2. The row-count mismatch (**27,846 vs 27,780**) cannot be resolved from annual aggregates. It might reflect code selection, raw dataset vintage, confidential/special product code treatment, or a processing difference. None is proven.
3. Eurostat states that product confidentiality can hide detailed trade codes while leaving aggregate trade intact. This can explain the general possibility of small aggregate discrepancies; **the cause of these exact gaps has not been demonstrated**.
4. A hash is an integrity check only after its purported raw file is available. The source hashes in the uploaded summary do not themselves authenticate Eurostat observations.
5. The previously noted 2025 difference from a DG Trade country factsheet remains unresolved. The new file's 2025 aggregate differs from the earlier reported Codex aggregate by only €1 and does not resolve different statistical scope or data-release vintage.

## Next mandatory evidence

- Attach the actual independent extraction product-year file (all individual `PRODUCT`, `TIME_PERIOD`, `OBS_VALUE` records) and any code lists/extraction log. Ideally also attach Codex's original 27,780-row Easy Comext CSV.
- Attach raw annual `DS-045409` response files named by year to verify the 14 SHA-256 hashes, query dimensions and processing logs.
- Check per-year code uniqueness, eight-digit codes with leading zeros, non-negative values, zero/missing/confidentiality handling and historical CN8 code validity. Recompute annual totals from row-level values.
- Reconcile the two raw extracts at `year × CN8` including matched keys, additions, removals, value revisions and confidentiality/special-code treatment.
- Only after these steps produce verified top-200 rankings, competitor panels and tariff exposures.

## Official methodological references

- Eurostat, detailed trade statistics: https://ec.europa.eu/eurostat/cache/metadata/en/ext_go_detail_sims.htm
- Eurostat Comext DS-045409: https://ec.europa.eu/eurostat/databrowser/view/DS-045409
- European Commission EU trade relations with Bangladesh: https://policy.trade.ec.europa.eu/eu-trade-relationships-country-and-region/countries-and-regions/bangladesh_en

**Do not mark a full 27,780- or 27,846-row dataset as independently verified on the basis of this 14-row summary alone.**