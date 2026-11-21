# Bangladesh–EU thesis — Task B follow-up audit (v13)
**Date:** 21 November 2026  
**Research:** Post-LDC graduation EU market-access exposure and export competitiveness  
**Scope:** preservation of unreported cells, authentication of official CN inputs, and complex harmonized-group review.

## Executive decision
**Partial execution achieved; full Task B remains NOT CERTIFIED.** This package makes the missing-value rule enforceable, publishes a corrected 69,342-cell DS-059322 observed-versus-unreported matrix from actual uploaded observations, creates a fail-closed transformer for the GitHub-derived DS-045409 harmonized panel, and prioritizes ambiguous historical families. It does **not** provide the missing 14 original official CN annual inputs or 13 original predecessor/successor tables. No cross-year product-growth rate is certified.

## Provenance and files actually inspected
- Original user-uploaded `eu_imports_bangladesh_cn8_2012_2025.csv` (DS-059322; annual EU27_2020 imports from Bangladesh; stat procedure T): SHA-256 `7af0f75024828471b2c65ac0085fd2232926a61efbc29da080b0c68bd1a5d03e`.
- User's public GitHub folder: <https://github.com/mafijulrigan39-boop/thesis/tree/main/cn8_harmonization_2012_2025>; pinned earlier audit commit [`541b38090afba8d7462fe6bcd43aff8bc5c73f3a`](https://github.com/mafijulrigan39-boop/thesis/commit/541b38090afba8d7462fe6bcd43aff8bc5c73f3a). The six derived CSVs and their Git blob SHA-1s are recorded in `GITHUB_DERIVED_FILES_SOURCE_REGISTER.csv`. Those blob hashes identify *derived files*, not official Eurostat inputs. GitHub's `coverage_audit.csv` was re-opened and inspected; the large derived panels are covered by the earlier v11/v12 independent audit, not re-downloaded to this environment.
- Existing independent GitHub v12 audit: `TASK_B_GITHUB_INDEPENDENT_AUDIT_v12.md`, archived in this package for continuity. The numbers described below for full DS-045409 panel and complex groups derive from its previously executed GitHub-file checks, except the actual DS-059322 missingness grid and the top-200 review queue, which were independently regenerated in v13.
- Eurostat official guidance on annual CN edition and version conversion: https://ec.europa.eu/eurostat/cache/metadata/en/ext_go_detail_sims.htm ; https://ec.europa.eu/eurostat/en/web/products-eurostat-news/-/cn-20221107-1 ; https://op.europa.eu/en/web/eu-vocabularies/eurostat ; https://taxation-customs.ec.europa.eu/customs/common-customs-tariff-cct/tariff-classification-goods/combined-nomenclature_en .

## 1. Missingness — executed correction and rules

### A. Independently regenerated *original* DS-059322 code-year grid
The only original input directly present in this runtime is the unchanged 27,780-row DS-059322 trade CSV. `create_DS059322_missingness_grid.py` was executed. It created `DS059322_observed_vs_absent_CODE_VALIDITY_UNKNOWN.csv` with the 4,953 distinct observed CN8 codes crossed with 2012–2025 (69,342 cells):

| Status | Cells | Value treatment |
|---|---:|---|
| `OBSERVED_POSITIVE` | 27,625 | Original reported nonzero value |
| `OBSERVED_ZERO` | 155 | Explicit reported 0, retained as real observed zero |
| `NO_REPORTED_OBSERVATION_VALIDITY_UNKNOWN` | 41,562 | **Blank/NA**; official code validity **not inferred** |
| Total | 69,342 | Sum of reported non-missing values €213,281,751,867 |

An unreported row here may be a valid code with no report **or** an invalid/nonexistent code for that year; this source cannot distinguish the two. The matrix is a missingness audit, not a substitute for an official CN-validity mapping. All 14 original years and numeric values are preserved without imputation.

### B. Derived *GitHub DS-045409* panel (prepared, not rerun on full remote file in this environment)
Prior v12 GitHub-file audit examined 154,210 rows and identified **27,846** `OBSERVED_TRADE` rows including **156** explicit zeros, **105,740** inferred/labelled `VERIFIED_ZERO` entries for active unreported codes, and **20,624** inactive slots. Those counts reconcile exactly: 27,846 + 105,740 + 20,624 = 154,210.

The v13 conversion `create_missing_safe_harmonization.py` leaves original records unchanged and writes a **separate** file adding:
- `OBSERVED_POSITIVE` / `OBSERVED_ZERO` for actual `OBSERVED_TRADE` rows;
- `ACTIVE_BUT_NO_REPORTED_TRADE` and blank `STRICT_OBSERVED_VALUE_EUR` when original row was labelled `VERIFIED_ZERO`;
- `INACTIVE_CODE` and blank observed value for inactive year-codes;
- a distinct `IMPUTED_ZERO_SENSITIVITY_EUR` *for optional closed-world sensitivity only*, explicitly **not observed**.

Group-year output includes `STRICT_OBSERVED_SUBTOTAL_EUR`, `UNREPORTED_ACTIVE_MEMBER_COUNT`, a complete-value field blank when any member has no record, and cross-chapter/continuity review flags. This code passed **9 synthetic-only targeted checks**. Its entire-data execution remains pending because the large GitHub derived CSVs are not mounted locally. It must not be reported as having generated a corrected 154,210-row file yet.

## 2. Authenticating the annual CN inputs — BLOCKED on original files
The GitHub folder has **six derived CSVs**, not the 14 original annual code-list source files or 13 original transition inputs. We created a 27-row `official_classification_27_source_receipt_REGISTER.csv` in which all original file links, download timestamps, raw hashes and exact source revisions are blank and explicitly `NOT_ARCHIVED`. GitHub blob SHA-1 hashes are *not* authoritative source checksums.

`archive_official_CN_sources.py` rejects incomplete or unapproved raw URL lists and will store response URL, HTTP status, timestamp, ETag, Last-Modified, bytes and SHA-256 when an actual official download succeeds. Its real preflight was run and **correctly stopped** because all 27 canonical raw-download URLs were missing. This is an honest provenance blocker, not successful source authentication. After official originals are acquired, their code definitions and edge contents require semantic checking against the derived graph.

## 3. Complex group review — scope and provisional exclusions
The v12 audit on the pinned GitHub-derived groups reported:
- 2025 leading CN8 top 200: **180** `1:1_exact` classification labels, **17** `complex_MN`, **2** `merged_group`, **1** `split_group`.
- **20 non-exact top-200 codes** require explicit split/merge review; collectively **€1,386,480,826** in the original DS-059322 2025 basket (**6.528%** of the 2025 €21,238,163,196 total). The exact 20 identifiers and values are in `top20_nonexact_MANUAL_REVIEW_QUEUE.csv`.
- **3** additional exact-code products lack a positive reported 2012 endpoint; a 2012–2025 CAGR must not be computed for them without valid observations. Value in 2025: **€57,590,555**.
- **177** remaining products have an exact-code label and positive 2012 endpoint; original DS-059322 2025 value **€19,345,209,718**. These are *provisional historical-analysis candidates*, not certified unchanged product meanings.
- **16** 2025 harmonized groups span more than one HS2 chapter in the derived group graph (257 current CN8 code members; **€10,669,513** in 2025). Examples: `HCN8_B970D83498AE` across HS2 39/76/96, and `HCN8_5178E4DFAD8F` across 84/85/90/93/96. These can be legally valid graph components while economically heterogeneous.

### Publication policy
1. **Native 2025:** keep 2025 exact `VALID_CN8` products for rankings and prospective tariff matching. Keep Comext `99...` auxiliary codes separate from valid native CN8 products.
2. **Historical base (conservative):** exclude the 20 non-exact top-200 lines from CN8-level unqualified growth claims until original predecessor/successor tables justify interpretable harmonization. Do not create CAGR for three products missing 2012 positive source observations. Do not call the other 177 certified stable until official source checks pass.
3. **Group sensitivity:** identify groups spanning more than one HS2 **in any year**, not just simultaneously in 2025. Exclude from longitudinal product claims and report year-wise value impact, product list and reasons.
4. **Split/merge economics:** verify semantic description, origin and destination codes, mapping directions, HS chapter, overlaps, ambiguity and whether group composition is interpretable. If not, aggregate only at a verified broader product level, or drop from product-level growth analysis and show coverage loss.
5. **Missingness sensitivity:** release a separate, clearly annotated closed-world zero-imputation sensitivity only after official completeness/status checks, never as the default observed-data baseline.

### Criterion still not met
**No unverified cross-year product comparison in final results** remains pending a reproducible source-authenticated classification chain and review of complex groups. The v13 files deliberately leave historic CAGR and group validity claims blank.

## 4. Executed checks, delivered files and next gate
- **Executed on actual original observations:** original 27,780-record file verified by SHA and reprocessed into 69,342 missingness-preserving product-year cells; 155 source-recorded zeros retained; €213,281,751,867 total unchanged.
- **Executed on real classification flags from prior GitHub audit:** 200-product review register and 20-product manual exclusion queue generated; EUR values reconciled to v12 independently tested counts.
- **Executed on synthetic fixtures:** 9-case missingness/group safety test passed.
- **Verified external official sources:** EU Vocabularies, Eurostat detailed trade metadata and annual CN policy; no full source-data downloads were obtained.
- **Not executed:** whole 154,210-row corrected DS-045409 panel; source re-download, full graph review, certified 2012–2025 CAGRs.

Next gate: acquire the pinned GitHub derived files locally and run the new converter, then obtain and authenticate 27 official raw classification/correspondence inputs. A final full group review and provenance-checked 2012–2025 growth panel can then be certified.