# Task D — Official Eurostat Comext quantities and comparable unit values

**Audit date:** 21 November 2026 (UTC).  
**Decision:** **PASS** for net-mass extraction, within-year EUR/kg and explicit exclusions for the selected 200 CN8 products and seven origin countries. **NOT CERTIFIED** for price per supplementary unit or longitudinal harmonized CN8 unit-value trends.

## Official sources, population and provenance

- Eurostat `DS-045409` official SDMX-CSV, reporter `EU27_2020`, flow `1` (imports), frequency `A`, years **2012–2025**, selected 200 native 2025 CN8 product codes.
- Origins: Bangladesh (BD), China (CN), India (IN), Vietnam (VN), Pakistan (PK), Cambodia (KH), Türkiye (TR).
- Monetary values: **`VALUE_IN_EUROS`** from the already authenticated matching Task C panel (the identical official dataset and product/origin/year identifiers).
- Quantities: **`QUANTITY_IN_100KG`** and **`SUPPLEMENTARY_QUANTITY`** from 14 new official annual SDMX-CSV responses; net mass (kg) is 100 × `QUANTITY_IN_100KG`.
- Original response SHA256 hashes, URLs and retrieval timestamps are in `task_d_quantities/full/official_quantity_receipts.csv`. Raw gzip response archives reside in `task_d_quantities/full/raw/`.
- Official source snapshot returned `LAST UPDATE` **13/11/26 11:00:00** (verified in preliminary API probes). Official metadata: https://ec.europa.eu/eurostat/cache/metadata/en/ext_go_agg_esms.htm and https://ec.europa.eu/eurostat/comext/newxtweb/mainxtnet.do.
- GitHub source root: https://github.com/mafijulrigan39-boop/thesis/tree/main/task_d_quantities/full

## Independently validated scope

| Check | Verified outcome |
|---|---:|
| Official annual quantity responses downloaded | **14 / 14**, no request failures |
| Source gzip response hashes independently verified | **14 / 14** |
| Distinct origin-product-year-indicator quantity records | **537,945** |
| Seven-origin selected product-year cells | **19,600** |
| Valid same-origin/year/product EUR/kg | **18,582** |
| Excluded unit-value cells | **1,018** |
| Exclusions — no reported trade-value observation | **1,016** |
| Exclusions — reported net mass = zero | **2** |
| Raw supplementary-quantity observations, seven origins | **13,618** |
| 2025 Bangladesh-to-six-competitor EUR/kg comparisons | **1,200 possible** |
| 2025 valid comparative ratios | **1,186** |
| Independent QA issues | **0** |

The two explicit zero-mass exclusions are 2012 `46021990` / Pakistan (EUR 3, mass 0.00 × 100 kg) and 2015 `63029100` / Cambodia (EUR 7, mass 0.00 × 100 kg). These are **not** assigned finite unit values.

## Coverage by year

| Year | Eligible cells | Valid EUR/kg | No reported value | Zero mass | Raw supplemental quantity cells |
|---:|---:|---:|---:|---:|---:|
| 2012 | 1,400 | 1,293 | 106 | 1 | 950 |
| 2013 | 1,400 | 1,302 | 98 | 0 | 952 |
| 2014 | 1,400 | 1,302 | 98 | 0 | 950 |
| 2015 | 1,400 | 1,305 | 94 | 1 | 953 |
| 2016 | 1,400 | 1,306 | 94 | 0 | 952 |
| 2017 | 1,400 | 1,305 | 95 | 0 | 952 |
| 2018 | 1,400 | 1,307 | 93 | 0 | 954 |
| 2019 | 1,400 | 1,308 | 92 | 0 | 952 |
| 2020 | 1,400 | 1,309 | 91 | 0 | 952 |
| 2021 | 1,400 | 1,312 | 88 | 0 | 955 |
| 2022 | 1,400 | 1,380 | 20 | 0 | 1,024 |
| 2023 | 1,400 | 1,387 | 13 | 0 | 1,024 |
| 2024 | 1,400 | 1,380 | 20 | 0 | 1,022 |
| 2025 | 1,400 | 1,386 | 14 | 0 | 1,026 |
| **Total** | **19,600** | **18,582** | **1,016** | **2** | **13,618** |

## Sample empirically calculated 2025 Bangladesh import unit values

| Native CN8 code | Bangladesh EUR/kg |
|---|---:|
| `61091000` | 11.86 |
| `61103099` | 13.15 |
| `61102099` | 13.27 |
| `62034231` | 12.35 |
| `61102091` | 13.20 |
| `61046200` | 12.22 |
| `62034235` | 13.85 |
| `62046231` | 12.34 |
| `61051000` | 14.59 |
| `62052000` | 21.18 |

**Worked calculation for `61091000` (2025, BD):** EUR 3,499,230,143 ÷ (2,950,527.72 × 100 kg) = approximately **EUR 11.86/kg**. The source's raw supplementary quantity is 1,913,761,686, but its exact supplementary unit has **not** been independently linked to the official CN8 unit code, so no supplementary unit value is claimed.

### 2025 relative unit-value positioning (descriptive only)

The corresponding source table has **1,186 valid pairs of 1,200**. Median ratio below 1 means Bangladesh's observed EUR/kg is lower within the *same native 2025 CN8 code* for the sampled comparisons, but not necessarily identical item or quality.

| Competitor | Valid pairs | Median BD/competitor EUR/kg | Pairs with BD lower |
|---|---:|---:|---:|
| China | 200 | ~0.88 | 129 |
| India | 200 | ~0.79 | 154 |
| Vietnam | 198 | ~0.64 | 171 |
| Pakistan | 198 | ~1.01 | 96 |
| Cambodia | 190 | ~0.79 | 151 |
| Türkiye | 200 | ~0.54 | 179 |

**These medians are unweighted across the selected product codes.** Do not treat them as overall export price comparisons, product quality rankings, production-cost estimates or causal evidence. Net mass/unit values can include varied mixes and customs-price treatments within a single CN8 code.

## Strict exclusions and interpretation

1. **No imputed zeros:** missing trade-value or quantity observations remain blank; a reported net mass of zero blocks EUR/kg.
2. **No false supplementary-unit comparison:** `SUPPLEMENTARY_QUANTITY` is preserved with unit flag `UNVERIFIED`; unit-specific EUR/pair, EUR/piece or EUR/litre requires the official annual CN8 supplementary-unit code and consistency verification.
3. **No unqualified historical CN8 trend:** the 2012–2024 unit-value rows remain native classification codes and are **not** approved for 14-year comparability until Task B's official split/merge concordances are authenticated.
4. **No cross-product price ranking as a competitiveness conclusion:** net mass of different products reflects different physical goods.
5. **Scope restriction:** results cover the 200 products selected by 2025 Bangladesh import value and seven named origins. Raw all-origin quantities are retained separately; full-origin analysis can use those records with the Task C value extract.

## Deliverable index (GitHub)

- [Source QA summary](https://github.com/mafijulrigan39-boop/thesis/blob/main/task_d_quantities/full/SOURCE_QA_SUMMARY.json)
- [Independent recalculation and checksum QA](https://github.com/mafijulrigan39-boop/thesis/blob/main/task_d_quantities/full/INDEPENDENT_QA.json)
- [Annual quantity coverage](https://github.com/mafijulrigan39-boop/thesis/blob/main/task_d_quantities/full/coverage_by_year.csv)
- [Seven-origin quantity and EUR/kg panel](https://github.com/mafijulrigan39-boop/thesis/blob/main/task_d_quantities/full/seven_origin_quantity_unit_value_2012_2025.csv)
- [Raw all-origin quantities, compressed CSV](https://github.com/mafijulrigan39-boop/thesis/blob/main/task_d_quantities/full/all_origin_quantities_2012_2025.csv.gz)
- [2025 comparable unit-value ratios](https://github.com/mafijulrigan39-boop/thesis/blob/main/task_d_quantities/full/relative_unit_values_2025.csv)
- [All excluded observations](https://github.com/mafijulrigan39-boop/thesis/blob/main/task_d_quantities/full/unit_value_exclusions.csv)
- [Supplementary quantities without verified unit labels](https://github.com/mafijulrigan39-boop/thesis/blob/main/task_d_quantities/full/supplementary_quantities_UNVERIFIED_UNITS.csv)
- [Source receipts with query URLs and checksums](https://github.com/mafijulrigan39-boop/thesis/blob/main/task_d_quantities/full/official_quantity_receipts.csv)
- [Original official annual responses](https://github.com/mafijulrigan39-boop/thesis/tree/main/task_d_quantities/full/raw)
- [Reproducible extractor](https://github.com/mafijulrigan39-boop/thesis/blob/main/task_d_quantities/extract_task_d.py)
- [Independent test script](https://github.com/mafijulrigan39-boop/thesis/blob/main/task_d_quantities/qa_task_d.py)

## Completion decision

**Task D's primary completion criterion is met:** net-mass coverage, same-product/year EUR/kg comparisons, an audited 2012–2025 seven-origin quantity panel, supplementary quantities and explicit exclusions have all been delivered and independently verified. **Secondary work remains:** officially classify the units for supplementary quantities, and finish Task B's historical CN8 concordance before longitudinal price analysis. The preserved original data and current-year unit-value results are still thesis-useful in the interim.
