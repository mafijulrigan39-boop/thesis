# Task F — Bangladesh–EU empirical analysis, verified results and remaining gates

**Research:** *Assessing Bangladesh’s Post‑LDC Graduation Market‑Access Exposure in the European Union: A Product-Level Analysis of Tariff Preference Erosion and Export Competitiveness*  
**Analytical release:** v20 · 21 November 2026  
**Reference trade series:** Eurostat Comext `DS-045409`, annual, EU27_2020, import flow 1, `VALUE_IN_EUROS` (trade years 2012–2025).  
**Tariff benchmark:** Official DG TAXUD CIRCABC TARIC workbooks, **1 November 2026** snapshot.  
**Legal basis:** Regulation (EU) 2026/1395, particularly Articles 7, 8, 33 and Annexes I, III and IV.  
**Source archive and executable code:** https://github.com/mafijulrigan39-boop/thesis/tree/main/task_f_empirical

## Executive conclusion

The principal 2025 cross-sectional quantitative research has been **executed and independently reproduced**. A complete 2025 top-200 product ranking is joined to all-origin EU market denominators, six primary competitors, 2025 EUR/kg data, and the November 2026 conditional EU tariff-source matrix. The Article 33 GSP beneficiary and all-origin denominators have also been calculated directly from official chapter-level Comext records.

The independent Task F QA completed successfully with **zero issues**: 11 upstream source file hashes verified; 200 market shares independently recalculated; 1,200 origin-product comparisons checked; all 40 scenario-by-scope exposure entries recalculated; and 14 official chapter-source response checksums verified.

**Two claims are explicitly NOT certified:** (i) 2012–2025 harmonized CN8 product-level CAGR, because original year-by-year classification/concordance source files in Task B remain unauthenticated; and (ii) legally payable 2027/post-EBA Standard GSP/GSP+ tariffs, which depend on future rates, country eligibility, product-specific origin conditions, safeguards and actual import documentation.

## 1. Product market share and origin positions, 2025

The **200 largest Bangladesh-origin native CN8 products** generated **€20,789,281,101** of 2025 EU imports, while total EU extra-EU imports in those same product markets were **€137,346,619,291**. Bangladesh therefore held a **15.1364% pooled import-value share** across this specifically selected universe. It is **not** Bangladesh's share of all EU imports.

All non-EU country origins were ranked directly from the 312,194 official origin–product–year records in Task C. Across the selected 200 EU markets:

| Named non-EU supplier | Rank | 2025 value (€ billion) | Share of total selected markets |
|---|---:|---:|---:|
| China | 1 | 43.321 | 31.54% |
| Bangladesh | 2 | 20.789 | 15.14% |
| Vietnam | 3 | 12.186 | 8.87% |
| Türkiye | 4 | 9.508 | 6.92% |
| India | 5 | 7.646 | 5.57% |
| Pakistan | 6 | 5.443 | 3.96% |
| Cambodia | 7 | 5.408 | 3.94% |
| Morocco | 8 | 2.933 | 2.14% |
| United Kingdom | 9 | 2.808 | 2.04% |
| Indonesia | 10 | 2.732 | 1.99% |

The country-origin sums are intentionally not forced to equal Eurostat's extra-EU total; the source-wide residual across the 200 products is **€1.144 billion**, and individual country-origin absence is not automatically zero. At the product level, the top five actual non-EU suppliers have been calculated separately for every line.

**Examples of real 2025 Bangladesh product-market shares:** CN8 `61091000` 50.97%; `61103099` 22.59%; `61102099` 34.58%; `62034231` 33.67%; `61102091` 31.89%; `61046200` 38.94%.

## 2. Product and supplier concentration

The **full Bangladesh-origin CN8 2025 basket** from the independently audited original `DS-059322` file has product-value **HHI 423.66** (0–10,000 scale), with the top 10 products accounting for **47.65%** and the leading 200 accounting for **97.89%**. The 200-product *conditional* basket has HHI **442.13** and a within-selected top-10 share of **48.68%**. These two denominators must never be mixed.

A separate source-backed *named-origin supplier HHI* was calculated for each EU product market. Its median for the selected 200 is approximately **2,169.91**, but **163/200 products** have a residual exceeding 0.1% of Eurostat's published extra-EU aggregate. These source-origin HHIs are **provisional descriptive indices**, not certified exact all-origin concentration measures. The full country-origin residual and sensitivity audit is available in Task C.

## 3. Relative EUR/kg positioning and tariff preference margins

For matched 2025 CN8 product-country observations, 1,186 of 1,200 Bangladesh–competitor unit-value ratios were valid. Their unweighted median ratios are:

| Competitor | Valid product pairs | Median BD / competitor EUR/kg | Value-weighted mean conditional 2026 tariff margin (percentage points) |
|---|---:|---:|---:|
| China | 200 | 0.880 | 11.83 |
| India | 200 | 0.793 | 9.38 |
| Vietnam | 198 | 0.639 | 0.20 |
| Pakistan | 198 | 1.005 | 0.03 |
| Cambodia | 190 | 0.785 | 3.94 |
| Türkiye | 200 | 0.536 | 0.00 |

**Interpretation:** A ratio below 1 means the Bangladesh import value per kilogram is lower for the same CN8 and year. It does not establish equal goods quality, actual selling prices, production costs or exporter profitability. The tariff margins are *rate differences between source-recorded conditional 2026 tariff candidates*, not observed utilization on declarations.

Türkiye's industrial customs-union treatment is kept separate from origin-based FTA and GSP measures: its 0% candidate can depend on A.TR/free-circulation requirements. Cambodia's source tariffs reflect product-specific EBA withdrawal. The matrix retains explicit complex-duty and legal-condition flags.

## 4. Static tariff-cost exposure scenarios

Each scenario fixes the observed **2025 Bangladesh EU import value** and multiplies it by the difference between a specified November 2026 tariff-rate benchmark and Bangladesh's source-recorded 0% EBA candidate. A result is a **static tariff duty equivalent**, not a forecasted loss of exports, a finding that exporters pay the cost, or the legally payable duty after EBA cessation.

| Scenario | Qualified products | Value covered (€ billion) | Static extra duty equivalent (€ billion) | Unresolved source lines |
|---|---:|---:|---:|---:|
| MFN fallback, leading 200 | 196 | 20.658 | **2.443** | 4 |
| 2026 India Standard GSP tariff-channel proxy | 184 | 20.451 | **1.916** | 16 |
| 2026 Pakistan GSP+ tariff-channel proxy | 197 | 20.766 | **0.00524** | 3 |
| S-11b Standard GSP illustrative 20% reduction of 2026 MFN rates | 152 | 19.630 | **1.869** | 0 |
| S-11b MFN hypothetical safeguard after EBA exit | 152 | 19.630 | **2.336** | 0 |

**Coverage:** The MFN calculation covers **99.369%** of the selected 200 products' Bangladesh import value; the four unmatched rates collectively correspond to **€131,083,237**. The S-11b calculation covers all **152 of the top-200 apparel/made-up textile lines** (these are not *all* EU imports in chapters 61–63).

**Scenario sensitivity already executed:** top 10 MFN equivalent **€1.214bn**; top 50 **€2.063bn**; top 100, 98 rate-qualified lines, **€2.317bn**; entire top 200 **€2.443bn**. Excluding the 20 Task B-derived non-exact classification group labels leaves 177 MFN-qualified lines and **€2.279bn** static equivalent. These products have genuinely different values, so this is a sample-composition sensitivity rather than proof of harmonized historical comparability.

The *India* and *Pakistan* figures are source-dated tariff-channel counterfactuals, not future Bangladesh-specific statutory rights. The S-11b Standard GSP scenario applies the 20% *relative reduction* for sensitive apparel under Article 7 to **2026 MFN values held constant**, subject to any applicable special safeguards, product definitions and future law.

## 5. Article 33 legal-threshold calculations — correct denominators

**Official 2025 chapter totals**, independently retrieved at HS2 from `DS-045409`:

| GSP Section S-11b, chapters 61–63 | EU import value |
|---|---:|
| Bangladesh-origin imports | **€19,865,351,190** |
| Imports from 64 GSP beneficiary origins in **2027 Annex I** (using 2025 trade observations) | **€40,782,984,357** |
| Imports from **all** extra-EU origins (official aggregate) | **€108,130,114,257** |

From those three values:

- **Article 33(1) share:** Bangladesh / all covered GSP beneficiaries = **48.7099%**, above the 37% threshold in Annex IV.
- **Article 33(2) exception share:** Bangladesh / all extra-EU origins = **18.3717%**, above the separate 6% exemption boundary.
- **EBA exception:** Article 33(2) **does not apply** to Bangladesh while it remains an EBA beneficiary. The two numerical tests do not override this statutory exemption.
- **Implementation:** Under Article 33(3), any future withdrawal requires a Commission implementing act and becomes applicable **two months after publication**. Neither publication nor Bangladesh's future GSP+ eligibility can be inferred from threshold arithmetic.

**Sensitivity:** Excluding fully withdrawn Belarus from the GSP denominator gives **48.7285%**. Published extra-EU aggregate less verified named-country totals leaves approximately **€1.296bn** unallocated; attributing all of that amount to GSP beneficiaries still yields **47.2092%**. These screens stay above 37%, but the actual applicable-year beneficiary roster and legal status must be re-evaluated in any future assessment.

**Critical chronology:** The 64-country roster is sourced from the official **2027** Annex I and backcast onto **2025** import observations. It is an informative prospective calculation, **not** the exact 2025 scheme membership or an Article 33 legal determination for 2025. All 14 annual numerical screens (2012–2025) use the same explicit 2027-roster backcast and retain this label.

## 6. Historical growth and classification restrictions

At a **broad HS2 aggregate level**, genuine official chapter-level data permit descriptive 2012–2025 comparisons without representing raw same-code CN8 lines as harmonized.

For Sections 61–63 combined:
- Bangladesh-origin EU imports **€7.637bn in 2012 → €19.865bn in 2025**.
- **Compound annual growth rate: approximately 7.63%** over 13 annual intervals.
- **2024–2025 growth: 6.36%** using chapter aggregates.
- Bangladesh share of all EU extra-EU Chapter 61–63 imports **11.72% in 2012 → 18.37% in 2025** (a rise of **6.65 percentage points**).

At **individual CN8 product level**, historical growth remains blocked by Task B's provenance requirement. The six GitHub-derived harmonization outputs do not include the 14 original annual CN code lists and 13 raw predecessor–successor tables needed for full source authentication. Derived `VERIFIED_ZERO` labels for absent reports are not accepted as observations. The delivered `CERTIFIED_2012_2025_CN8_HARMONIZED_CAGR.csv` deliberately has **no data rows**. It must remain empty until genuine classification and missingness tests pass.

## 7. Strict publication and inference rules

1. Use 2025 CN8 product-market shares, supplier rankings and comparable 2025 unit values as current validated cross-sectional findings.
2. Use 2012–2025 Chapter 61–63 trends as broad-section historical evidence; label all fixed-2025-code historical product growth as uncertified.
3. Report **both** exact Article 33 denominators, the beneficiary-roster year and the EBA exemption; never substitute Bangladesh's world import share for the 37% test.
4. Treat 2026 MFN, EBA, Standard GSP-country and GSP+ country tariff lines as **conditional source-dated candidates**, not observed utilization or guaranteed future duties.
5. Never describe static duty equivalents as export losses, GDP costs, margins, tax incidence or causal estimates.
6. Keep supplier-origin HHI and missing origin records qualified, and audit extra-EU country-sum residuals.
7. Update product classifications, tariff dates, origin rules, scheme eligibility and Commission acts before assigning a future legally applicable post-EBA shock.

## 8. Reproducibility and exact data sources

**Official trade, all-origin and market share:**  
https://github.com/mafijulrigan39-boop/thesis/tree/main/task_c_competitor_data/full  
**Quantity and unit-value original data:**  
https://github.com/mafijulrigan39-boop/thesis/tree/main/task_d_quantities/full  
**Original DG TAXUD TARIC source workbooks and legal conditions:**  
https://github.com/mafijulrigan39-boop/thesis/tree/main/task_e_tariff_matrix/nov2026_taric  
**Article 33 14 dated source responses, 2027 scheme roster, denominators and raw hashes:**  
https://github.com/mafijulrigan39-boop/thesis/tree/main/task_f_empirical/article33  
**Task F 2025 product-level empirical results and 40 scenario sensitivity rows:**  
https://github.com/mafijulrigan39-boop/thesis/tree/main/task_f_empirical/full  
**Executable Task F calculation:**  
https://github.com/mafijulrigan39-boop/thesis/blob/main/task_f_empirical/run_empirical_analysis.py  
**Independent Task F calculation auditor:**  
https://github.com/mafijulrigan39-boop/thesis/blob/main/task_f_empirical/qa_task_f.py  
**Independent QA manifest (passed, zero issues):**  
https://github.com/mafijulrigan39-boop/thesis/blob/main/task_f_empirical/full/INDEPENDENT_QA.json  
**Legal text (EU 2026/1395):**  
https://eur-lex.europa.eu/eli/reg/2026/1395/oj/eng

**Final certification decision:** The **2025 competitiveness, 2026-source tariff benchmark, static exposure sensitivities and numerically correct Article 33 screens are executed and reproducible**. The user's broader Task F completion criterion is **not yet fully met** because legally verified forward tariff rates and source-authenticated historical CN8 harmonization remain incomplete. These are explicitly separated from the completed numerical findings, not silently imputed.