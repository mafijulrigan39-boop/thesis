# Methods and statistical design memorandum — publication-oriented and noncausal

**Purpose:** lock a defensible analysis-to-theory match before MITB seven-chapter manuscript writing. This is a methodological recommendation, not a claim that all proposals have been executed or that a supervisor approved them.

## 1. Define the actual estimands

### 1.1 Sampling universe and observed data
- Reporter: EU27_2020 statistical entity, extra-EU imports (country of origin), Eurostat Comext DS-045409.
- Native reference trade year: **2025**; sample is the **200 CN8 product lines with the highest Bangladesh-origin EU imports** in that year.
- Competitor country origins: **CN, IN, VN, PK, KH, TR**. These provide six-country *comparators*, not a census of all exporters; official extra-EU import all-origin totals are the market-share denominator.
- Current benchmark tariff date: **1 November 2026**, legal/tariff origin-dependent source candidates from TARIC and Task E. The study does **not** observe a realized post-EBA tariff shock.
- Time series in the repo 2012–2025: HS2 Chapters 61–63 aggregate annual data are permissible trend context. Individual historic CN8 lines are **not** confirmed harmonized; do not estimate historical CN8 CAGR, product switching, or fully longitudinal CMSA.

### 1.2 Product market share and basket concentration

For CN8 product p in 2025:

**EU import market share of Bangladesh:** MS(BD,p) = 100 × V(BD,p) / V(all_extraEU,p).

Denominator must be the published all-origin **extra-EU** product total, not the sum of six named partners nor GSP beneficiaries. If denominator missing or 0, share is NA, not 0.

**Bangladesh top-200 basket weight:** w(p) = V(BD,p) / sum over 200 products V(BD,p).

**Basket HHI:** HHI_products = sum over observed top200 [w(p)^2]; explicitly a *conditional top200 basket concentration* rather than national export HHI across all tariff codes. A normalized HHI based on the full Bangladesh-EU product universe needs that universe's denominator and must be differently named.

**Supplier country HHI within product:** HHI_origin(p)=sum over *all* actual partner countries [V(origin,p)/V(extraEU,p)]^2. If only a subset observed or the partner value subtotal falls below the Eurostat official aggregate, use a **provisional partial lower contribution**, with an upper sensitivity that assigns all positive unexplained residual to one country. Do not turn remaining origin residual into exactly zero, interpret HHI as final or double count reported partners.

### 1.3 Customs unit value and competitors

UV(origin,p,2025)=V(origin,p,2025)/net_mass_kg(origin,p,2025) only for valid positive net mass in the *same* current-year CN8. Relative BD-to-rival unit value = UV(BD,p)/UV(origin,p). Status should encode missing source mass, nonpositive mass, noncomparable unit, country/product mismatch and any suppression.

**Never assert UV=quality, price paid by exporter, cost, wage, or efficiency.** It is a landed/customs value proxy, vulnerable to within-CN8 product mix and CIF/FOB/transport differences. Source Task G: 1,186/1,200 valid paired ratios; 14 missing/invalid.

### 1.4 Legal tariff margins

For destination EU, source time t, product p and claimed origin c:

**Legal MFN preference margin for Bangladesh:** PM_BD(p,t) = t_MFN(p,t) - t_BD_eligible(p,t). This is only legally accurate when the specific product, origin, duty type and rules of origin are verified.

**Relative advantage vs supplier c:** A_BD,c(p,t) = t_c_applicable(p,t) - t_BD_applicable(p,t). When only source candidates exist, label **candidate advantage**, and report their exact coverage. Do not assume a Vietnam FTA rate automatically applies to all Vietnamese cargo, a Pakistan GSP+ rate applies without origin certification, or Türkiye zero by Customs Union without the actual goods/conditions.

**Effective use correction:** actual use of the stated legal preference is transaction-specific. To adjust exposure for utilization, collect partner×CN8×year eligible value, qualifying preference-claimed value, and tariff measures. A nationwide 2024 96% utilization statistic is a **macro external validity anchor**; multiplying all 2025 lines by 0.96 can be an illustrative uniform sensitivity only, not verified realized 2025 tariff payments.

### 1.5 Counterfactual duty equivalent — NOT export losses

For a *clearly specified conditional* rate scenario s, baseline b:

C_s = sum over VALID numeric p of V(BD,p,2025) × [ t_s(p; reference-date) - t_b(p; reference-date) ] / 100.

This is **accounting exposure with fixed 2025 import values**, not 2029/2032 forecast duty, export revenue loss, trade diversion, consumer welfare or incidence. If customs duty is specific, mixed, quota-bound, subject to suspension or conditional, record as **not numerically qualified** until unit conversion and legal status proven. Never silently impute 0 to missing rates.

Benchmark executed Task G: 200 selected 2025 products; Bangladesh EU imports EUR 20,789,281,101; 196 products numeric 2026 MFN candidates; missing 4 products worth EUR 131,083,237; qualified value EUR 20,658,197,864 (99.369% of cohort); MFN source-reference static benchmark EUR 2,443,135,906.98. These figures are source-vintage-specific.

Sensitivity controls should use:
- TOP10 / TOP50 / TOP100 / TOP200 product cohorts;
- S11b HS2 Chapters 61–63, other industries, and 2025 1:1 exact vs 20 complex/nonexact codes;
- Alternative 2026 available rate benchmark candidates: MFN, standard-GSP analogous, Pakistan GSP+ analogous, Article 7 section duty reduction, hypothetical Article33 *only with later implementing act*;
- Exclude four unverified tariff CN8 codes; stress precisely labeled **hypothetical** extra rates 0/5/10/15/20 pp separately as accounting sensitivity — never a legal rate estimate;
- Alternative six-country and two named competitor groupings with rate coverage explicitly unequal.

### 1.6 Article 33 numerator and two noninterchangeable denominators

For year y and section S11b = Chapters 61–63 goods under Annex III mapping:

Numerator B(y) = EU imports of S11b products **originating Bangladesh**.

37% screening denominator G(y) = EU imports of the relevant section **originating in all applicable GSP beneficiary countries** (Article 33 and Annex IV). Check each country’s eligibility/withdrawal/status in *that year*; a 2027 Annex I list backcast onto 2025 is an illustrative **counterfactual roster sensitivity**, not a legally operative historical test.

6% exception denominator U(y) = **all Union imports of same S11b goods** (as required by law), not G(y). Article 33(2) additionally **exempts EBA beneficiaries**. The threshold in a potential future legally eligible year is not self-executing: the Commission implements it via an act, with notices/effective dates.

2025 archived source-date backcast: B=EUR 19,865,351,190; G(2027-roster backcast)=EUR 40,782,984,357 ⇒ 48.7099%; U=EUR 108,130,114,257 ⇒ 18.3717%. Those figures are historical numerical illustrations and cannot prove the safeguard actually applied to Bangladesh in 2025 or will apply in 2032.

## 2. Hypotheses and statistical tests — executed versus appropriate

### 2.1 Already executed ex-post Task G
- **H1:** Difference in mean 2026 MFN candidate duty rates, S11b versus non-S11b top200 products. Permutation test one-sided 9,999. Observed gap +3.9394 percentage points; exploratory p=0.0001. This is largely a difference in *administrative tariff schedules*, not a causal competitiveness result.
- **H2:** Spearman market-share versus 2026 MFN rate among 196 numerically qualified products. Pooled rho ≈ +0.18873, two-sided permutation p=0.0087. **With HS2 sector-control residualized-rank sensitivity, rho≈−0.00959, permutation p≈0.843**. Treat pooled H2 as **not robust to sector composition**; do not highlight its p alone.
- **H3:** Six same-CN8 matched partner EUR/kg comparisons; exact one-sided sign tests with Benjamini-Hochberg FDR on the six countries, but paired products/partner outcomes are not independent draws from a national population. These test relative unit value direction, **not productivity**.
- **H4/H5:** annual legal ratio screens and tariff-exposure arithmetic are **deterministic calculations**, not stochastic hypotheses requiring p-values.
- Tests were specified **after inspecting Task F results**. Thus all H1–H3 are **post-hoc descriptive exploratory checks**; no preregistration or confirmatory population inference.

### 2.2 Why conventional cross-sectional OLS/regression is weak here

A proposed 2025 OLS relation such as EU share(p) = α + β × 2026 tariff candidate(p) + ε(p) would be vulnerable to:
- temporal reverse mismatch (2026 scheduled duty vs 2025 realized trade),
- near-common tariff rates within HS2 and categorical sector confounding,
- purposive selection of 200 high Bangladesh-value outcomes (collider/sample selection),
- omitted quality, buyer networks, costs, RoO, non-tariff compliance and price formation,
- mechanical correlation between market share and cohort selection,
- nonindependence of products within HS chapters and of six competitor-country rows per product.

Such regression cannot identify a graduation impact merely by adding standard errors, controls or PPML. Clustered errors do not fix omitted treatment variation or policy timing.

### 2.3 Publication-strength statistical strategy without pretending causal evidence

For an **observational product risk-profile article**, recommended core estimands and tables:
1. Value-weighted product and HS2 exposure distribution (weighted quantiles, share of basket exposed to each rate tier), and HHI/cumulative basket shares with explicit top200 scope.
2. Relative tariff advantage by origin and product *conditional on rate qualification*, plus alternative source paths and coverage percentages; group comparisons weighted by observed Bangladesh import value of the valid paired lines.
3. Market share and matched EUR/kg distributions per product and section, with missingness/outlier documentation and no quality labels.
4. H1–H3 **exploratory in a clearly subordinate robustness subsection**, and H2 sector-adjusted null equally prominent.
5. Multidimensional **exposure-ranking matrix** by baseline value, possible tariff percentage-point change, competitor share, quantity comparability and legal-certainty/missingness; avoid adding arbitrary scores without prespecified weights.
6. 2023–2025 HS2 Article 33 historical sensitivity with exact denominator definitions, 2027-roster backcast label, and no p-value for administrative thresholds.
7. Value-at-risk across hypothetical rate/coverage scenarios only; no elasticities invented, no causal effect. If desired, bounded demand scenarios require explicit literature-sourced elasticities and are separately a *modelled illustrative exercise*.

Descriptive uncertainty: bootstrap if useful as a stability-of-200-codes sensitivity and correctly label these as **resampling of the selected cohort**, not 95% confidence intervals for the population of all Bangladeshi export codes. Prefer exact published values and clearly specified scenario bounds.

## 3. If seeking true causal or publishable impact identification — additional data required

**Option A: 2020 Cambodia partial EBA withdrawal as external validation.** Build a treatment panel of affected versus unaffected Cambodia products with origin/destination-year import data, careful trade coverage, dates and treatment definitions. Test parallel trends, placebo/event-study, policy interactions, spillovers/other shocks, post-period sensitivity and alternative donor groups. This is a **different research article**, not evidence of Bangladesh future causal outcomes, and source data must be built first. Tanaka (2022, DOI 10.1111/twec.13329) is directly relevant.

**Option B: Bangladesh actual post-EBA event study** is unavailable as of Nov 2026 because the event has not yet occurred. A future post-2032 analysis might use EU Member State importers, other exporters or treated lines with validated tariffs and effective utilization; identification cannot be asserted now.

**Option C: Structural/partial equilibrium trade simulation** could be added now only if published appropriate product/sector substitution elasticities, baseline origin shares, tariff utilization, tariff rate legal conditions and import-demand calibration are retrieved, validated, modelled and stress-tested. Otherwise no demand response estimate should be made. Distinguish this clearly from Task F's static accounting.

**Option D: Future rigorous panel (2012–2025)** requires **14 year-specific original CN source files + 13 official pairwise predecessor-successor correspondence tables**, definitive code family construction, controlled split/merge handling and missing data provenance. Even with this, pre-event data alone cannot identify post-event treatment effects.

## 4. Reproducibility, transparent reporting and journal review

All numerically reported findings require:
- exact repository commit SHA, input SHA-256 fingerprints, original official source query parameters, download/validity date and licence/redistribution terms,
- product-year and origin-country filters, CN8 code as zero-padded string, statistical reporter and valuation units,
- code and sorted deterministic tables, independent results reconciliation and tests with fixed permutation seed,
- denominator audit and strict missing/zero distinction,
- qualified product count/value and exclusions for every scenario,
- complete bibliography, legal reference and correction log,
- pre-analysis status: clearly flag existing H1–H3 post hoc, and preregister new true holdout tests only if collecting additional independent data.

Publication outlet logic: *applied trade policy or customs/statistical methodology* with high transparency and descriptive contribution is the natural target. A strong-causal-econometrics journal would expect convincing natural experiment or structural identification beyond current design. No acceptance guarantee.

## 5. Thesis chapter method-congruence under supplied guideline

Chapter 3: conceptual arrows reflect theories, not proven causal signs. Chapter 4: explicitly quantitative secondary-data **cross-sectional observational** design, 4.2 interviews/cases N/A unless performed, 4.3 actual descriptive/permutation/sign calculations and Python 3.12, 4.4 purposive sample and all data source vintages, 4.5 source QA and hypothesis protocols, no results.

Chapter 5: show computed tables/test outputs with neutral captions, no interpretation. Chapter 6: compare to literature, acknowledge the H2 sector-adjusted null, explain policy implications conditionally and comprehensively list limitations. APA in-text author-year and full original reference verification.

## 6. Do not add unsupported features to the thesis

Unobserved: firm labor costs, bargaining power, EBA customs use per CN8 2025, transaction-level rules-of-origin certificates, 2029/2032 binding future rates, EBA withdrawal decision, true causal competitiveness, 2012–2025 certified CN8 family CAGR, extrapolations from an observed random sample, true exporter quality and consumer welfare.

The research must not claim those variables are observed, estimated or statistically supported merely because they appear in prior peer-reviewed studies.
