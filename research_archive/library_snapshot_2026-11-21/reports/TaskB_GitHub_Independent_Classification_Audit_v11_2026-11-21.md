# Bangladesh–EU CN8 Task B: independent GitHub harmonization audit (v11)

**Date:** 21 November 2026  
**Status:** **PARTIAL / CONDITIONALLY USABLE**. Code-year mappings, transition linkage, annual value conservation and 2025 product classifications were independently inspected and passed structural arithmetic checks. **Full academic certification remains open** because raw upstream official classification source files, extraction procedures and status-provenance evidence are not archived in the linked GitHub folder; inferred zeros and overly broad historical connected components must be handled conservatively.

## Immutable research source

GitHub repository: https://github.com/mafijulrigan39-boop/thesis/tree/main/cn8_harmonization_2012_2025  
Main-branch commit reviewed: `541b38090afba8d7462fe6bcd43aff8bc5c73f3a` (commit time 2026-11-21 06:34:21 UTC; message “Add final CN8 harmonization results”). The commit SHA is the stable snapshot; branch head can change.

| GitHub file | Git blob SHA | Inspected rows |
|---|---|---:|
| `cn8_2025_exact.csv` | `8d60ec268e11b9d06f60e0cca6be7cacc12e95d0` | 9,778 |
| `cn8_code_year_crosswalk.csv` | `0fa2acdd9b0868f74fc6272838e4ca098d78cd8f` | 133,586 |
| `cn8_transition_edges.csv` | `b5fc5481e9fcbbeb750aeabe775e808c3fcf8fcd` | 125,535 |
| `cn8_validity_trade_panel.csv` | `7e400e9f17fff169f933750f88538f18b9ac4e36` | 154,210 |
| `coverage_audit.csv` | `527a068e9fde0962e7c2477ce4cd8ad6aced216f` | 14 |
| `hcn8_group_year_trade.csv` | `4f2535e2c96892c005ab5edb2d9ab771f9b6c25a` | 121,110 |

All six were opened through the linked GitHub connector and analyzed in memory. **They are derived research outputs.** The folder does **not** contain the original 14 official CN classifications, 13 full predecessor/successor downloads, a data-source manifest (URLs, download times, HTTP metadata and raw-file SHA-256 hashes), or code describing the complete transformation.

## Confirmed internal integrity

- Exactly **133,586** unique active code-year mappings; **zero duplicated code-year keys**.
- Exactly **125,535** year-adjacent transition edges. Every edge connects extant mapped endpoints and both endpoints have the same harmonized-component ID. **Zero missing endpoints or inconsistent IDs** were found.
- Edge classifications: `1:1_exact` 121,785; `1:1_renamed` 572; `split_group` 1,275; `merged_group` 563; `complex_MN` 1,340. Edge sources: `SAME_CODE_VALIDITY` 122,086; `CN8-PRED-SUCC` 3,449.
- Code-year descriptions: `CELLAR_ANNUAL_CN` 86,600; `COMEXT_CN_MASTER` 46,986. There are 313 description-change flags and 779 same-code scope-change flags; no `1:1_exact` code-year was marked with either of those flags.
- Panel contains 154,210 unique product-year slots: **27,846** `OBSERVED_TRADE` (including **156** explicitly zero-valued), **105,740** `VERIFIED_ZERO`, **20,624** `INACTIVE` with blank—not zero—values. The panel is a complete 14-by-11,015 union-code grid.
- Observed trade total **€213,283,256,355**. The harmonized group-year values sum to precisely the same annual values as the `DS-045409` coverage register for all 14 years. Group-year observed-member counts also match reported observation counts.
- This uses the `DS-045409` annual numeric basis, **not** the older `DS-059322` `STAT_PROCEDURE=T` basis. The original uploaded 27,780-row series totals €213,281,751,867, or €1,504,488 less.
- The disputed ten historical codes were independently filtered from GitHub's panel: **66 observed product-years totaling €1,504,471**, exactly matching the previously supplied code-by-code reconciliation. The €17 residual on matched rows is not independently reconciled here against every row of the earlier 27,780-row file.

## 2025 exact classification, shares and provisional longitudinal candidate subset

- 2025 contains **9,778 valid CN8 roster codes** plus **2 separate Comext auxiliary codes**. Of the 9,778 valid codes, 2,601 have `OBSERVED_TRADE`, 7,177 have `VERIFIED_ZERO`.
- 2025 valid-CN8 value: **€21,238,245,136**. Comext auxiliary trade value **€79,545**, giving all-numeric `DS-045409` value **€21,238,324,681**. The older `DS-059322` series reports **€21,238,163,196**, lower by **€161,485** for 2025. Do not combine these source vintages without a disclosure.
- 2025 CN8 roster continuity classifications (code count): `1:1_exact` **7,747**; `1:1_renamed` **356**; `split_group` **652**; `merged_group` **116**; `complex_MN` **907**.
- `1:1_exact` codes account for **€19,810,225,640**, or **93.276%** of the 2025 valid-CN8 trade basket. **7,740** such codes are present in the active code roster for all 14 years (93.275% of the 2025 trade value), although this does not prove that each product traded every year.
- Across the 2025 top-200 value-ranked product codes, **180** are `1:1_exact`; **20** are non-exact (17 complex, 2 merged, 1 split) with a combined 2025 value **€1,386,480,826**. This corresponds to **6.528%** of the 2025 valid-CN8 trade basket.
- A **candidate** conservative historical set comprises **1,027** 2025-positive `1:1_exact` product codes with a reported 2012 observation; they represent **€19,713,186,362** in 2025, approximately **92.82%** of valid-CN8 value. Of the 2025 top 200, **177** have exact-one-to-one continuity plus positive observed values at both the 2012 and 2025 endpoints, representing **€19,345,209,720** in 2025. These may support *provisional* 2012–2025 CAGR, subject to upstream source authentication and code-definition checks. Do not assign zero to a missing endpoint.

## Material methodological exceptions

### E1. Missing-versus-zero evidence

`VERIFIED_ZERO` is assigned to **105,740 active CN8 product-years without a reported trade observation** (and 7,177 in the 2025 valid-code roster). The six files do not provide a source-status flag or official metadata proving every unreported cell is an observed zero. The panel does correctly preserve `INACTIVE` as blank, but that is a *different* distinction. For the thesis, retain `OBSERVED_TRADE` and its **156** genuine reported zeros as a separate class. Relabel `VERIFIED_ZERO` provisionally as `NO_REPORTED_OBSERVATION_ON_VALID_CODE` or `INFERRED_ZERO_IF_COMPLETE_CENSUS`; do not use these zeros in continuity or growth calculations without an explicit completeness and confidentiality-policy audit.

### E2. Over-connected product families

The historical groups are graph connected components; **16** 2025 groups contain codes in more than one HS2 chapter, spanning **257** currently valid codes and **€10,669,513** of 2025 trade (**0.0502%** of valid-CN8 value). Example `HCN8_5178E4DFAD8F` combines **114** 2025 codes across chapters **84, 85, 90, 93 and 96** (2025 value €595,231), and `HCN8_4AAF0877E571` groups products from chapters **04, 16, 17, 18, 19, 21 and 24**. Among the 2025 top-200 CN8 lines, `39269097` (€7,197,513) participates in a family spanning chapters 39, 76 and 96. The component relationship is graph-consistent, but those groups must not automatically be interpreted as homogeneous product markets. Exclude them from product-level historical comparisons or conduct manual source-backed mapping and economic-scope checks.

### E3. Incomplete source authentication

The derived files show `CELLAR_ANNUAL_CN`, `COMEXT_CN_MASTER`, and `CN8-PRED-SUCC` evidence labels, but those labels are not a substitute for actual source-file receipts or hyperlinks identifying each annual source and predecessor/successor table. Retrieve and archive original 14 classification files and 13 annual transition tables, their URLs and hashes, and the code transforming them into group IDs. In the crosswalk, COMEXT open-ended validity intervals such as `2500-12-31` are **not legal proof of unchanged product meaning through the year 2500**.

### E4. Need for value-scenario separation

`DS-045409` annual numeric data and the 2025 valid-CN8-only dataset are different comparison universes because the former includes **€79,545** in an auxiliary code in 2025. Treat real CN8 trade and Comext auxiliary residuals separately. Also preserve the provenance of the original 27,780-row `DS-059322` as a separate input. Do not silently mix totals, denominator scopes or dataset vintages.

## Final decision / thesis application

**Task B is not yet fully certified for all 2012–2025 product growth and continuity results.** However, it has advanced materially: the complete derived crosswalk, code catalogue, transition graph, trade value conservation and 2025 product descriptions have been independently inspected. The method is sufficiently structured to support a **restricted provisional 1:1-exact continuity panel** while awaiting official-source audit. The 2025 native-CN8 ranking remains valid within its own source universe. Broad graph-connected product families and inferred zeros must remain excluded from claims of comparable long-term product growth.

**Exact remaining actions:** (1) attach original official annual source files and manifest; (2) document how reported zeros, missing trade and suppressed values are distinguished; (3) review and, where appropriate, split cross-chapter and other complex graph components; (4) independently reproduce raw CN8-to-HCN8 transpositions against the original source data and report no-double-counting/reallocation checks; (5) freeze and version the restricted validated harmonized panel with code-validity and observation-status flags.

**Official context:** CN classification is revised annually, and the 2025 definition is established by Commission Implementing Regulation (EU) 2024/2522. Sources: https://data.europa.eu/data/datasets/combined-nomenclature-2025?locale=en ; https://ec.europa.eu/eurostat/en/web/international-trade-in-goods/methodology ; https://ec.europa.eu/eurostat/en/web/products-eurostat-news/-/cn-20221107-1 .

**This audit was actually performed:** the six GitHub CSVs were read through the connected GitHub plugin, with in-memory row counts and cross-file checks. No direct official Eurostat re-download succeeded and no unprovided raw official source data were fabricated.