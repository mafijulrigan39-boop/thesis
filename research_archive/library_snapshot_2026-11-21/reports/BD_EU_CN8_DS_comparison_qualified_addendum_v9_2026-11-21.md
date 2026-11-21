# Bangladesh–EU Comext CN8 reconciliation — qualified addendum v9

**Dated:** 21 November 2026. **Supersedes the causal interpretation in v8, not the underlying source files.**

## Evidence-level definitions

- **Reproduced here:** mathematical reconciliation of the user-provided ten-code comparison; exact SHA256 and absence of ten codes in the uploaded `DS-059322` Bangladesh CSV.
- **Reported from an external comparison, not independently re-examined here:** 66 additional `DS-045409` product-year observations, their individual values, the claimed ten-code catalogue explanation, and the 270 matched record differences. The 27,846-row raw DS-045409 extract and catalogue snapshots have not been supplied here.
- **Undetermined:** why the two datasets differ in product coverage; whether confidentiality, release vintage, catalogue structure, statistical procedure or another mechanism is responsible.

## Arithmetic decomposition

| Measure | DS-045409 (externally reported) | DS-059322 (directly inspected) |
|---|---:|---:|
| CN8 observations | 27,846 | 27,780 |
| CN8 value | €213,283,256,355 | €213,281,751,867 |
| Difference | 66 observations | €1,504,488 |

**Breakdown of the €1,504,488 net discrepancy:**

- Extra product-year rows attributed to ten numeric CN8 codes: **66 observations**, totaling **€1,504,471** (arithmetic independently checked).
- Net difference attributed to **270 matched product-year records with small value differences**: **€17**, as reported by the user; this last row comparison **cannot be independently reproduced without the DS-045409 source rows**.
- Sum: **€1,504,471 + €17 = €1,504,488**.

| CN8 code | Additional product-years reported | Additional DS-045409 value reported | Confirmation available here |
|---|---:|---:|---|
| `20098936` | 12 | €424,361 | **Absent from the uploaded DS-059322 BD extract** |
| `20098973` | 11 | €586,920 | **Absent from the uploaded DS-059322 BD extract** |
| `20098997` | 10 | €168,037 | **Absent from the uploaded DS-059322 BD extract** |
| `20098988` | 8 | €136,842 | **Absent from the uploaded DS-059322 BD extract** |
| `20098199` | 6 | €113,885 | **Absent from the uploaded DS-059322 BD extract** |
| `20098119` | 6 | €23,080 | **Absent from the uploaded DS-059322 BD extract** |
| `20099095` | 4 | €16,892 | **Absent from the uploaded DS-059322 BD extract** |
| `84521019` | 4 | €51 | **Absent from the uploaded DS-059322 BD extract** |
| `20098934` | 3 | €7,256 | **Absent from the uploaded DS-059322 BD extract** |
| `20098131` | 2 | €27,147 | **Absent from the uploaded DS-059322 BD extract** |
| **Total** | **66** | **€1,504,471** | **All ten codes absent from uploaded DS-059322 BD rows** |

## Independent original-file check

- Local file: `/mnt/data/eu_imports_bangladesh_cn8_2012_2025.csv`.
- Actual rows inspected: **27,780**.
- SHA256: `7af0f75024828471b2c65ac0085fd2232926a61efbc29da080b0c68bd1a5d03e`.
- All ten listed codes are absent from the uploaded Bangladesh-filtered `DS-059322` extract.

**Important distinction:** Absence from a filtered country/product observation file does not independently demonstrate absence from the full live Eurostat PRODUCT catalogue. Establishing catalogue exclusion requires the actual product-code catalogue for each dataset and retrieval timestamp. The user's external comparison reports that these codes are missing from the current `DS-059322` catalogue; that claim remains external evidence in this local audit until the catalogue snapshot is archived.

## Mechanism: do not attribute the difference to confidentiality

- The ten codes are numeric eight-digit CN codes in the reported comparison, not an identified confidentiality-residual series.
- Eurostat explains that some confidential products can be concealed in published product detail or published at a higher aggregation level. That **general possibility does not establish that these exact ten codes were suppressed**.
- Confidentiality-marker representations vary by dataset, period and dissemination method; do not assume that `X` or `S` patterns establish the cause of this specific mismatch without original flag definitions and values.

**Defensible interpretation:** “The two extracts differ by 66 historical product-year observations associated with ten numeric CN8 codes, plus a net €17 difference among matched observations. Available evidence is consistent with differing product coverage or catalogue treatment; the underlying administrative or confidentiality mechanism is not established.”

Official methodology and catalogue context:

- https://ec.europa.eu/eurostat/cache/metadata/en/ext_go_detail_sims.htm
- https://ec.europa.eu/eurostat/web/user-guides/data-browser/download-data/code-lists
- https://ec.europa.eu/eurostat/comext/newxtweb/setupdimselection.do

## Remaining Priority 1 closure requirements

1. Archive official `DS-045409` raw annual records and the actual source response hashes and retrieval timestamps.
2. Archive the actual versioned `PRODUCT` codelists for `DS-059322` and `DS-045409` (and any dimensions/procedures that distinguish them), proving the ten-code catalogue exclusion on that date.
3. Independently verify the 66 row keys/values and the small matched-row differences; capture a machine-readable diff file with provenance.
4. Confirm relevant official observation-status/confidentiality flags, or explicitly conclude that the mechanism is unknown.
5. Separately reconcile DG Trade 2025 €21.179bn against the Comext-reported €21.244359bn using matched statistical definitions and release vintages. The ten-code difference of €1.504488m does **not** explain the much larger €65.359364m DG Trade discrepancy.

## Status

- **Internal DS-059322 validation:** Passed.
- **Comparison arithmetic:** Passed for supplied values.
- **Specific absent codes in DS-059322 BD observations:** Independently confirmed.
- **DS-045409 external raw observations, catalogue claim and 270 matches:** Not independently inspected.
- **Causal explanation:** Unknown. Confidentiality attribution withdrawn.
- **Priority 1 overall:** **Partial**, pending official provenance and DG Trade reconciliation.