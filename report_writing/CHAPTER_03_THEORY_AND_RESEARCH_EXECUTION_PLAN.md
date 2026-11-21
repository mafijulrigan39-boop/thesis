# Thesis research: theory-selection audit and complete execution plan

**Audit date:** 22 November 2026
**Working title:** Assessing Bangladesh’s Post-LDC Graduation Market-Access Exposure in the European Union: A Product-Level Analysis of Tariff Preference Erosion and Export Competitiveness.
**Status:** Research design and verified numerical cross-section reviewed; theory revised; **not supervisor-approved / not a causal design**.

## 1. Research-direction decision

**Retain the existing topic and empirical design.** The aim is to provide a transparent, source-dated, Bangladesh-specific *product-level exposure and observed EU market-position assessment*, not forecast actual losses or resurrect the earlier SEZ/FDI/OLI project. The current title is defensible only if “export competitiveness” is expressly operationalized as observed destination-market positioning and selected comparative indicators, not firm productivity or true comparative advantage.

Primary theory: structural gravity's **relative trade-cost reasoning** plus preferential trade treatment and trade diversion.
Measured outcomes: 2025 EU import-market share, imports by origin, selected basket concentration, and valid origin-matched EUR/kg indicators.
Constructed conditional measures: statutory MFN/preferential duty candidates at 2026-11-01 and alternative fixed-trade-value tariff scenarios.
Institutional modifiers: origin qualification, preference use, GSP/EBA eligibility, EU Article 33 denominators and implementing acts.
Contextual but unmeasured mechanisms: GVC governance, firm heterogeneity, purchasing relationships and duty pass-through.
Excluded principal model: OLI and general institutional-quality theory, because FDI choice and governance-quality measures are not observed.

## 2. Verified baseline and unresolved gates

| Component | Verified status from versioned repository | Qualification/next gate |
|---|---|---|
| 2025 selected Bangladesh product cohort | 200 CN8 lines, €20,789,281,101; Task F / Task G SHA-confirmed | Purposive high-value sample, not all products |
| EU comparator markets | EU27_2020 imports; six origins CN, IN, VN, PK, KH, TR; 1,200 product-origin pairs and all-origin official denominators | 163/200 product supplier HHIs have >0.1% residual, report bounded HHI |
| Quantity comparisons | 1,186/1,200 valid matched EUR/kg ratios | Missing 14 must remain missing; EUR/kg not quality/cost |
| MFN tariff reference date | 2026-11-01 official TARIC; 196/200 numeric source candidates; qualified value €20,658,197,864 | 4 missing numeric rates worth €131,083,237; legal conditions / 2025-to-2026 nomenclature qualification |
| Comparator tariff candidates | 1,183/1,200 numerically comparable candidates in Task F | 17 unresolved; origin preference may be legally conditional; Türkiye customs union A.TR not automatic origin preference |
| Static MFN reference equivalent | €2,443,135,906.98 on qualified 2025 value, independently recomputed | **Not tariff collected or loss of exports**; no 2032 payable tariff certified |
| Article 33 numerical backcast | 2023–2025 Chapter 61–63 annual screens and 2027 Annex I beneficiary roster sensitivity checked | 37% GSP-beneficiary share vs 6% all Union import share are different tests; EBA exception; no implementing act |
| Exploratory tests | H1, H2 and H3 executed; 11 source SHA-256 verified, independent QA PASS | H2 pooled positive but within-HS2 adjustment null; tests post-hoc, selected cohort, no causal inference |
| Historical CN8 growth | 2012–2025 CN8 harmonization not certified; output table of certified product CAGR has no observations | Recover 14 nomenclatures + 13 correspondence source files or restrict history to HS2 |
| Actual preferences used | National preference-use aggregates in official literature, not verified 2025 CN8 line-by-line claims | Do not multiply all lines by a 96% national figure as if observed |
| Supervisor acceptance | Pending | Obtain written approval of objective-RQ-H1–H3 alignment, scope and formatting |

**Evidence provenance:** `task_f_empirical/full/TASK_F_EMPIRICAL_RESULTS.json`, `task_f_empirical/full/INDEPENDENT_QA.json`, `task_g/verified_results/QA_SUMMARY.json`, `task_g/verified_results/HYPOTHESIS_TESTS.csv`, `task_e_tariff_matrix/nov2026_taric/REGIME_AWARE_QA_SUMMARY.json`, and `task_f_empirical/article33/ARTICLE33_SOURCE_AND_QA.json`. Frozen input snapshot `acda0fd118b6ec019c5b37e34d07dc76e28fb878`; verified GitHub Actions Task G run `44885066470`.

## 3. Objective–research question–theory alignment

| Objective/RQ | Theoretical reason for inclusion | Observable or conditional constructs | Inference |
|---|---|---|---|
| O1/RQ1: concentration and EU market position | Comparative-advantage measurement limitations and destination-market outcomes | `V_BD,p,2025`, published `V_extraEU,p,2025`, selected-basket weights and HHI | Description; sample-conditional |
| O2/RQ2: six competitor comparisons | Relative trade-cost / trade-diversion incentives | Matched origin trade value, supplier share, customs value per valid kg, source-condition-qualified tariff candidates | Descriptive comparisons; H3 exploratory |
| O3/RQ3: tariff-margin structure | Preferential-access/reference-rate framework and product/sector heterogeneity | 2026-11-01 MFN and origin-specific candidate rate; HS2 sector; Bangladesh market share | Rate arithmetic and H1/H2 exploratory associations, not identified effects |
| O4/RQ4: conditional erosion | Trade-cost shock as *hypothesis*; fixed-value accounting as *method* | Sum of qualified 2025 import values times specified rate difference /100 | Static duty equivalent; neither tariff incidence nor predicted export loss |
| O5/RQ5: special safeguard screen | Legal eligibility/thresholds as institutional constraints | Bangladesh HS61–63 numerator, 2027-roster GSP denominator and separate all-extraEU denominator, 2023–2025 | Historical numeric backcast; no actual/future legal trigger |

## 4. Execution sequence and deliverables

### Gate A — Lock the approved research design and thesis language

- Confirm current title and narrow operational meaning of “export competitiveness” with supervisor; if the supervisor expects a complete RCA indicator or causal tariff response, explicitly state additional data/design requirements rather than suggesting current metrics provide them.
- Confirm seven-chapter template, APA 7, inclusion of H1–H3 as **post-hoc exploratory**, and secondary quantitative non-interview design.
- Finalize controlled scope: EU27_2020 imports by origin; 2025 top 200 CN8; six selected competitors; 2026-11-01 TARIC reference; 2023–2025 Article 33 historical screens; other historical chapter data only.
- **Completion evidence:** approved one-page research brief, objective-RQ-variable mapping, supervisor confirmation; any conditions logged.

### Gate B — Complete Chapter 3, section by section

1. **3.1 Selected theory [REVISED DRAFT COMPLETE].** Keep relative trade-cost/structural gravity concepts primary, preference margins and rules of origin operational, comparative advantage as a measurement lens, GVC and firm heterogeneity contextual. Do not call the model an estimated structural gravity.
2. **3.2 Application to research variables [NEXT].** Produce a data dictionary with: exact names, units, period, grain (CN8; CN8×origin; annual HS2), numerator, denominator, rate source, missingness status, eligibility assumptions, descriptive/constructed/exploratory designation, theory and RQ mapping. Distinguish RHS/LHS only for actual exploratory associations H1/H2/H3; do not call scenario duty arithmetic a dependent-variable regression.
3. **3.3 Conceptual framework diagram [NEXT].** Create a clean one-page chart showing (a) observed 2025 import/market position, (b) reference 2026 tariff rates and legal qualifications, (c) alternative scenario arithmetic, (d) unmeasured response mechanisms as dashed *not tested* links, and (e) sector/qualification/classification as caveats. Diagram caption: conceptual connections are not estimated causal pathways.
4. **3.4 Academic citation support [NEXT].** Provide short theory-to-construct evidence matrix; validate original article titles/year/DOI against issuing journals; map all research variables to credible literature and distinguish EU legislation from academic theory. Merge duplicates at chapter end.
- **Chapter 3 completion evidence:** every construct traceable to published theory or official law; all arrows appropriately labelled; zero unsupported tested-mechanism claims; consistent citations.

### Gate C — Strengthen the tariff, source, and legal evidence

- Reconcile native 2025 CN8 descriptions with 2026 10-digit TARIC descendants by verified code provenance; flag exact vs complex associations and validate rules of origin separately. Do not assume the 2026 candidate is automatically legally applied to 2025 cargo.
- Inspect four unresolved 2026 MFN candidates and 17 unresolved competitor tariff cases using original EU legal/coding sources; if unresolved, preserve NA and record the value coverage instead of imputing rates.
- Make every tariff scenario legally labelled: **MFN 2026 benchmark**, **2026 India Standard-GSP-channel proxy**, **2026 Pakistan GSP+-channel proxy**, **illustrative Article 7 rate**, and **Article 33 scenario conditional on later eligibility and implementing act**. Do not relabel proxies as future Bangladesh legal rights.
- Try to obtain product/origin-specific actual 2025 eligible-value and preferential-claim data from qualified EU official sources. If inaccessible, restrict the thesis to statutory/source-dated tariff candidates and separately labelled utilisation sensitivities.
- Cite UN 2026 graduation extension and actual EU Article 17 / Article 33 terms using original law. Update legal source register upon any new EU acts; don't infer new regulations from old sources.
- **Completion evidence:** join audit, origin×CN8 legal eligibility flags, missing-rate register, effective-date and official source ledger, documented no-imputation.

### Gate D — Decide whether historical CN8 harmonization is in scope

- Obtain the missing official **14 annual nomenclature lists and 13 adjacent-year concordance tables** (27 source items) if genuine 2012–2025 product-line growth is desired.
- Trace one-to-one, splits, mergers and complex product families; recompute only rates/series whose economic definitions are shown to be consistent. Source-authenticate every correspondence.
- If this validation cannot be done, **do not include CN8 CAGR, product survival, or historical CN8 fixed-share decomposition as findings**. Retain official HS2 61–63 annual context and 2025 native CN8 cross-section.
- **Completion evidence:** nonempty certified harmonized results with provenance and tests, OR an explicit documented decision to exclude product-line historical inference. Do not treat an empty `CERTIFIED_2012_2025_CN8_HARMONIZED_CAGR.csv` as completion.

### Gate E — Rerun empirical and legal QA with final inputs

- Preserve `task_g/run_task_g.py`, all source SHA-256 digests, independent arithmetic checks, and unmodified archived outputs as evidence for the currently verified results.
- Verify O1 all-origin denominators, product rank and 2025 valuation basis; O2 matched competitor origin pairs, 1,186 valid mass comparisons, and supplier-origin residual/HHI bounds.
- Verify O3 rate-source date, product coverage, classifications, legally conditional status and sector comparison; report H1 exploratory tariff-schedule gap, not trade impact.
- Verify O3 exploratory pooled H2 together with within-HS2 adjustment and missingness sensitivity; **do not suppress the non-significant sector-adjusted result**. Report H3 six paired sign tests and Benjamini–Hochberg multiple-testing correction; no productivity claim.
- Verify O4 alternative scenario `value × rate difference /100` on exact covered lines; sensitivity by top10/50/100/200, sectors, classification status, competitor origin and unverified-rate stress; **no resulting number is projected export losses**.
- Verify O5 both Article 33 numerators and denominators with roster-year notes, EBA exemption, and administrative implementation; present historical scenarios only.
- **Completion evidence:** independent QA PASS, updated data/source hash ledger, tested formulas, named executable receipt, coverage tables, all null findings retained.

### Gate F — Write Chapters 4–7 from the frozen evidence

- **Chapter 4 Methods:** explain actual observational quantitative design, EU reporter/partner/flow, source dates, purposive sampling, formulas, inclusion/exclusion rules, missingness, reproducibility scripts and H1–H3 exact methods. Retain 4.2 qualitative “not applicable” if required by the outline; do not invent interviews, regressions or SEM.
- **Chapter 5 Results:** populate tables directly from executed CSV/JSON, with every measure labelled by year, currency, origin, CN code, denominator, coverage, and scenario assumptions. Report H2 pooled and within-HS2 together; avoid policy interpretation.
- **Chapter 6 Discussion:** answer all five RQs; compare findings to empirical scholarship; distinguish exposure measures from economic outcomes; discuss implication for Bangladeshi exporters, trade institutions and EU market diversification. Treat labour/GVC transmission channels as literature-backed possibilities, not verified effects.
- **Chapter 7 Conclusion:** summarize empirical contribution and limitations without introducing new numerical claims; state implications contingent on future laws and trade arrangements.
- **Completion evidence:** approved table/figure inventory, cross-referenced RQ/O-to-results traceability, exact reproduced numbers and one complete APA bibliography.

### Gate G — Consolidate, audit, and obtain supervisor clearance

- Conduct full-text verification of significant scholarly paraphrases, reference DOI/issue-year checks, official legal act/date verification and APA 7 author–year consistency across Chapters 1–7.
- Reconcile all tables, figures, notes, code, source receipts, appendices and GitHub archive with the final chapter claims. Run plagiarism/originality checks and mandatory academic formatting.
- Obtain supervisor feedback and document revisions; confirm whether the university requires a final viva presentation, standalone research proposal, word-count conventions, or ethical statements.
- **Completion evidence:** versioned complete manuscript and appendices, supervisor-reviewed changes, reproducible citation and numerical audit, and submission-format approval.

## 5. Work prioritization

| Priority | Critical activity | Why it matters |
|---|---|---|
| **P0 — essential now** | Revised 3.1, complete 3.2–3.4, supervisor approval, preserve boundaries in 2025 data and 2026 tariffs | Keeps all chapters theoretically and methodologically consistent |
| **P0 — must not misstate** | H2 null sector adjustment, legal EBA transition, missing 4+17 tariffs, Article 33 EBA exemption, no observed export loss | Prevents invalid headline findings |
| **P1 — strong empirical enhancement** | Retrieve genuine line-level preference claims and legally verified RoO, resolve missing rates and 2025→2026 product mapping | Improves policy precision and publication credibility |
| **P1 — conditional on historical ambition** | Full original CN8 classification files and certified annual concordance | Required only if thesis makes long-run CN8 product claims |
| **P2 — later causal/publication extension** | Separate post-policy sample, identifying variation, credible counterfactual demand/elasticity model, tariff incidence and destination diversification | Necessary to move from *exposure* to estimated *impact*; **not completed by the existing dataset** |

## 6. Roadmap milestone order

1. **Framework lock:** 3.1 revised → draft 3.2 → draft 3.3 → draft 3.4 and supervisor approval.
2. **Legal/data qualification:** reopen relevant TARIC sources, join dates, RoO and actual preference claims; codify unresolved cases.
3. **Numerical freeze:** rerun QA and scenario sensitivity with a recorded source-versioned result set; choose whether historical CN8 harmonization is worth the required provenance work.
4. **Academic writing:** Chapters 4 and 5 (methods and literal results) → Chapter 6 (interpretation) → Chapter 7 (conclusion).
5. **Final editorial pass:** update earlier chapters if legal/data findings change; consolidate references; supervisor and institutional checks.

This is a **sequence of work packages**, not a claim that the assistant will perform work asynchronously. Completion of each gate depends on verifiable sources or actual supervisor decisions.

## 7. Research question integrity and stop rules

- **Stop** if the future tariff is labelled as determined when only a 2026 rate is available.
- **Stop** if a product-year blank becomes zero.
- **Stop** if EU imports are mislabelled as Bangladesh-reported FOB exports or a top-200 cohort statistic as nationwide.
- **Stop** if a 2027 GSP-roster backcast is reported as the operative roster in 2023–2025.
- **Stop** if an Article 33 arithmetic ratio is treated as an implemented safeguard.
- **Stop** if positive pooled H2 is described as robust without disclosing within-HS2 near-null sensitivity.
- **Stop** if GVC/heterogeneous-firm or OLI arguments are described as directly tested with EU origin-CN8 observations.
- **Stop** if literature is described as fully systematically reviewed when it was a screened narrative review with partial full texts.

**Principal decision:** The theoretical framework and data support a rigorous, reproducible **product-level prospective EU market-access exposure thesis**. Stronger claims about causal export contraction or comprehensive competitiveness require a different or expanded research design.
