# Task B — Independent GitHub harmonization review (v12)

**Research:** Bangladesh's Prospective EU Market-Access Exposure Following LDC Graduation: A Product-Level Assessment of Tariff Preference Erosion and Export Competitiveness  
**Audit date:** 21 November 2026  
**Decision:** **INTERNAL ARITHMETIC AND REFERENTIAL INTEGRITY: PASS. OFFICIAL-SOURCE CLASSIFICATION EQUIVALENCE AND MISSING-VALUE SEMANTICS: NOT CERTIFIED.**

## Snapshot and provenance

- Repository: <https://github.com/mafijulrigan39-boop/thesis/tree/main/cn8_harmonization_2012_2025>
- Pinned commit: [`541b38090afba8d7462fe6bcd43aff8bc5c73f3a`](https://github.com/mafijulrigan39-boop/thesis/commit/541b38090afba8d7462fe6bcd43aff8bc5c73f3a) — committed 2026-11-21 06:34:21 UTC.
- Dataset files and Git blob SHAs:

| File | Blob SHA | Audit scope |
|---|---|---|
| `cn8_2025_exact.csv` | `8d60ec268e11b9d06f60e0cca6be7cacc12e95d0` | Full 2025 native-code output |
| `cn8_code_year_crosswalk.csv` | `0fa2acdd9b0868f74fc6272838e4ca098d78cd8f` | 2012–2025 active classification nodes |
| `cn8_transition_edges.csv` | `b5fc5481e9fcbbeb750aeabe775e808c3fcf8fcd` | Year-to-year transition edges |
| `cn8_validity_trade_panel.csv` | `7e400e9f17fff169f933750f88538f18b9ac4e36` | Reported and nonreported product-year grid |
| `coverage_audit.csv` | `527a068e9fde0962e7c2477ce4cd8ad6aced216f` | Annual coverage and reconciliation |
| `hcn8_group_year_trade.csv` | `4f2535e2c96892c005ab5edb2d9ab771f9b6c25a` | Harmonized-group-year aggregations |

Git blob SHAs identify the committed *derived outputs*. They are **not** hashes of the original official Eurostat/CELLAR raw inputs.

## Independent tests performed on the GitHub connector's actual file contents

- Crosswalk: **133,586** unique YEAR×PRODUCT mappings, no duplicate keys, malformed numeric CN8 codes, or mismatched year-specific validity windows; 133,553 `VALID_CN8` and 33 `COMEXT_AUXILIARY` classification nodes.
- Transition graph: **125,535** edges; **0** missing endpoints, **0** cross-group-ID edges and **0** non-adjacent year edges. Sources: 122,086 `SAME_CODE_VALIDITY`; 3,449 `CN8-PRED-SUCC`.
- Year-code value panel: **154,210** unique product-year entries; **27,846** `OBSERVED_TRADE` rows worth **€213,283,256,355**; **105,740** entries marked `VERIFIED_ZERO`; **20,624** `INACTIVE` slots. Actual explicitly recorded zero-valued `OBSERVED_TRADE` rows = **156**.
- Harmonized group-year data: **121,110** entries; all independently reconciled against the panel with **zero** discrepancies in value, active-member counts or observed-member counts. The observed trade total is preserved at **€213,283,256,355**.
- The ten previously disputed historical CN8 codes contribute **66 observed product-years, €1,504,471** in the derived `DS-045409` panel. The remaining €17 difference versus original `DS-059322` is not independently decomposed from individual matched source rows by this package.
- Derived 2025 `VALID_CN8` roster: **9,778** codes; **2,601** report trade including **22** explicit reported zero values; **7,177** are marked `VERIFIED_ZERO`. Valid-code value = **€21,238,245,136**. The auxiliary code `99510000` has an additional **€79,545** of reported trade; the other auxiliary `99500000` is marked as nonreported zero. Combined numeric value = **€21,238,324,681**. Do not add auxiliary codes to the exact-CN8 product ranking.

## Product-level classification risks identified

- The largest 200 product codes in the 2025 derived roster have identical identities to the original uploaded `DS-059322` 2025 top-200 codes, while their aggregated euro values differ by **€2**. The **original uploaded** top-200 value is **€20,789,281,099**, whereas the **GitHub derived** top-200 value is **€20,789,281,101**.
- Of these 200 codes, **180** have a generated `1:1_exact` classification label. **20** require non-exact historical handling (17 `complex_MN`, 2 `merged_group`, 1 `split_group`). The 20 have **€1,386,480,826** of 2025 Bangladesh-origin trade.
- A further **3** exact-code products lack a *positive reported* 2012 endpoint in the original uploaded trade series. The remaining **177** are candidates for historical analysis because they have exact-code labels and positive reported endpoint values. Their 2025 original `DS-059322` value is **€19,345,209,718**. The candidate label is **not** a certified harmonized CAGR or proof of stable product meaning.
- **16** derived 2025 harmonized groups span more than one HS2 chapter (257 currently valid CN8 codes, **€10,669,513** in 2025). One illustrative component, `HCN8_B970D83498AE`, contains code `39269097` and spans chapters 39, 76 and 96; component value **€7,485,405**. Graph-connected groups can be internally consistent without defining economically comparable products.

## Two critical interpretive corrections

### 1. `VERIFIED_ZERO` does not mean the same as an observed zero

The six GitHub outputs provide no original Comext status records demonstrating that each of the 105,740 valid-but-unreported product-year combinations genuinely had zero trade. For academic growth, continuity and survival tests, rename them **`NO_REPORTED_OBSERVATION_ON_VALID_CODE`** and treat trade value as **missing** by default. Consider zero imputation only as an explicit, justified complete-census sensitivity case, never as an unqualified observed fact. Existing `OBSERVED_TRADE` entries equal to 0 are genuine reported zeros.

### 2. Classification-node connectivity is not economic comparability

Historical predecessor/successor graph connected components can span splits, mergers, renaming and transitive links. Verify sources and scope changes before interpreting the resulting HCN8 groups as constant product markets. Exclude or review cross-chapter and material `complex_MN` groups rather than computing unqualified growth across them.

## Completion decision

**Task B cannot yet be marked fully COMPLETE.** The GitHub files are valuable usable *derived harmonization outputs*, and all stated structural/audit arithmetic was independently examined. The repo contains only these six CSV outputs, not the 14 underlying official annual classification downloads, 13 predecessor-successor source files, dated source manifest or derivation code. Claimed column values such as `CELLAR_ANNUAL_CN` and `COMEXT_CN_MASTER` are not themselves proof that every code description and mapping was independently reproduced from an official origin.

To complete Task B:

1. Archive official original annual CN classification sources for **2012–2025** and predecessor-successor files for **2012→2013 through 2024→2025**, with canonical links, retrieval times, hashes and transformation code.
2. Resolve the reported-zero versus inferred-zero coding. Publish a corrected strictly observed panel retaining no-reporting cells as null; keep a separate clearly labelled zero-imputation scenario if needed.
3. Audit the **20 non-exact top-200 codes** and **16 cross-chapter** components against original source mappings, revising problematic group definitions or excluding them from longitudinal inference.
4. Independently replay the full origin-code-to-harmonized-group mapping, year-by-year conservation, and sample continuity checks from authenticated raw official inputs.
5. Freeze a baseline (`DS-059322` or `DS-045409`) and explicitly separate valid CN8 products from Comext auxiliary codes.

**Current permitted use:** 2025 native-CN8 ranking and provisional 177-code historical-analysis candidate shortlist; descriptive comparisons should use strictly reported values and state their source baseline. **Not permitted:** claim that every unreported cell is a true zero, or publish a fully certified 2012–2025 growth table for all harmonized groups.