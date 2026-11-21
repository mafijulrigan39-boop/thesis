# CHAPTER 4: RESEARCH METHODS

## 4.3 Quantitative Methods and Statistical Tools

The quantitative component applies **descriptive statistics, matched product–origin comparisons, exploratory randomization-based procedures, and deterministic tariff and legal accounting** to the source-defined observations specified in Section 4.1. The selection of methods follows the five research objectives and the distinction established in Chapter 3 between observed trade patterns, source-dated preferential conditions, and theoretical but unobserved adjustment mechanisms. In particular, the statistical comparisons described below are **post-hoc exploratory** exercises on a purposively selected set of products; they do not estimate the causal effects of Bangladesh's future loss of Everything But Arms (EBA) treatment. Applied policy-evaluation literature emphasizes that claims of causal effects require a defensible identification strategy, rather than merely the selection of a familiar estimator (Athey & Imbens, 2017). The current design does not provide such identification.

### 4.3.1 Quantitative Structure, Units, and Computational Environment

The principal quantitative analysis uses **2025 Eurostat Comext (DS-045409)** imports reported by the **EU27_2020** statistical entity for Bangladesh's **200 highest-valued CN8 products**, with the origin-country comparisons defined in Section 3.2. The analytical grain is either a **CN8 product** or a **CN8 product × comparator origin**; annual HS2 Chapter 61–63 totals are treated separately for the historical Article 33 exercise. These distinct grains are not analysed as though they were repeated observations from one harmonized product panel. Eurostat (2025) provides the statistical source definitions for country of origin, imports and detailed CN product classifications; the 2026 tariff candidates and regulatory criteria form separate policy-reference data.

The archived reproducibility pipeline was implemented in **Python 3.12**, with the independent Task G verification script \`task_g/run_task_g.py\` using the Python **standard-library modules** \`csv\`, \`json\`, \`math\`, \`random\`, \`hashlib\` and \`pathlib\`. Its inputs are source-dated CSV/JSON outputs from the preceding trade, quantity, tariff and legal-screen processing stages. A fixed base pseudorandom seed, **20261121**, and fixed numbers of Monte Carlo iterations permit repeatable exploratory tests; SHA-256 fingerprints and independent arithmetic checks provide an additional integrity check. The archived GitHub Actions run generated versioned test, robustness, source-hash and missing-data outputs, including \`HYPOTHESIS_TESTS.csv\`, \`ROBUSTNESS_RESULTS.csv\` and \`QA_SUMMARY.json\`. This statement identifies the **actually executed statistical software**; the thesis does not claim that SPSS, Stata, R, survey software, structural equation modelling (SEM), or a fitted structural gravity model was used.

**Table 4.3. Quantitative techniques used in the study**

| Objective / associated question | Analysis and statistical unit | Method implemented | Role of numerical inference |
|---|---|---|---|
| **O1 / RQ1** — trade structure | 2025 Bangladesh-origin CN8; selected top-200 basket | Value ranking, product/sector shares, basket HHI, official-denominator EU market share | Descriptive; no p-value required |
| **O2 / RQ2** — matched competitor position | 2025 CN8 × six comparator origins | Product-matched market shares and EUR/kg ratios; **H3** six one-sided exact sign tests | Descriptive and post-hoc exploratory |
| **O3 / RQ3** — tariff conditions | Qualified 1 Nov. 2026 rate candidates matched to 2025 products | Rate and margin distributions; **H1** one-sided permutation mean comparison; **H2** two-sided rank-correlation permutation and within-HS2 sensitivity | Exploratory tariff-pattern checks, not a policy treatment |
| **O4 / RQ4** — conditional tariff exposure | Qualified CN8 × specified 2026 benchmark/scenario | Fixed-2025-value duty-equivalent accounting and sensitivity by cohort, sector and rate coverage | Deterministic; no hypothesis-test p-value |
| **O5 / RQ5** — special safeguard screening | Historical 2023–2025 HS61–63 × specified origin grouping | Separate Article 33 37% beneficiary-origin and 6% all-import ratio screens; residual sensitivity | Legal/numerical calculation, not estimated risk probability |

*Note.* O = objective; RQ = research question; H1–H3 = post-hoc exploratory tests. Each method refers to the archived source and executable outputs. No claimed significance test is substituted for a fixed-value identity or a legal condition.

### 4.3.2 Descriptive Trade Measures, Concentration, and Matched Unit Values

For each selected product **p** and extra-EU origin **c**, the observed customs import value, **V(c,p,2025)**, is expressed in **euros**. Bangladesh's share of the corresponding EU import market is calculated against the **official all-extra-EU-origin total for that CN8 product**, rather than only the six comparator origins:

\[
MS_{BD,p}=100\frac{V_{BD,p,2025}}{V_{extraEU,p,2025}}.
\]

Within the selected top-200 cohort, each product's **basket weight**, \(w_p\), is its Bangladesh-origin value divided by the sum of the values of all 200 selected products. The **product-basket HHI** is \(\sum_{p=1}^{200}w_p^2\), with a 0–10,000 version obtained by multiplying that sum by 10,000. Because its weights refer only to the intentionally selected 200 products, this is a **top-200 conditional concentration measure**, not a complete national export HHI. Similarly, any supplier-origin HHI for an EU product market requires all origin shares. Where officially published all-origin imports exceed the sum of identified country-origin observations, the analysis reports the unreconciled residual and treats the computed HHI as provisional or bounded; it does not silently set the missing-origin contribution to zero.

For each same-year CN8 product–origin observation with **positive, valid net mass** \(Q(c,p,2025)\) in kilograms, the **customs unit value** is

\[
UV_{c,p}=V_{c,p,2025}/Q_{c,p,2025},
\]

and the matched Bangladesh-to-comparator unit-value ratio is

\[
R_{BD,c,p}=UV_{BD,p}/UV_{c,p}.
\]

A ratio below unity means that the recorded EU customs value per kilogram for Bangladesh is lower within that matched CN8 product and year. It does **not** demonstrate lower producer costs, equal-quality goods, or higher productive efficiency. Trade-price and quality scholarship explains why observed unit values can incorporate differences in quality, product mix and other factors (Gervais, 2015). Missing or nonpositive mass and invalid ratios are excluded from unit-value statistics and testing rather than being assigned zeros. The archived matched file provides **1,200 candidate product–competitor pairs** and **1,186 valid ratios**; the remaining 14 are retained in the missing-data register. Descriptive means, medians, distributional comparisons and value-weighted tariff differences, where relevant, are clearly distinguished by their respective denominators.

### 4.3.3 H1: One-Sided Permutation Comparison of MFN Tariff Rates

The first exploratory hypothesis evaluates whether **the mean 2026 MFN tariff candidate** is higher for the selected **HS2 Chapters 61–63** than for the remaining selected products. Let \(x_i\) be the qualified MFN rate (in **percentage points**) for an apparel-related product and \(y_j\) the qualified rate for another product. The observed test statistic is the **unweighted difference in arithmetic means**,

\[
T_{H1}=\overline{x}_{61\text{–}63}-\overline{y}_{other}.
\]

The null and alternative are specified operationally as a nonpositive versus positive difference; the Monte Carlo calculation evaluates the upper tail under **exchangeability of product-group labels**. Of the 200 selected products, **196** have qualified numeric 2026 MFN candidates: **152** in HS2 Chapters 61–63 and **44** in other chapters. The groups are defined from the 2025 product classification, while their rates refer to **1 November 2026**. Their difference therefore describes the structure of the tariff schedule within the cohort, not an effect of a tariff change on import values.

The implemented permutation procedure pools the 196 rates, repeatedly shuffles them and divides the shuffled sequence into groups of the original sizes. It recomputes the difference in means **9,999 times**, using the pseudorandom seed **20261121**, and counts permutations whose difference is at least the observed statistic. To avoid reporting a zero Monte Carlo p-value, the empirical upper-tail measure uses the **plus-one correction**, \((b+1)/(9,999+1)\), where \(b\) is the number of equally or more extreme simulated statistics. The correction is consistent with methodological guidance on sampled permutation p-values (Phipson & Smyth, 2010). Because there was **no actual random assignment of CN8 products to tariff groups**, exchangeability is an analytical hypothetical and the p-value is an exploratory calibration rather than a randomized-experiment inference.

For an additional descriptive stability measure, the script separately draws **1,999 bootstrap samples with replacement within each of the two groups**, recalculates the mean-rate gap, sorts the resulting gaps and reports the empirical **2.5th and 97.5th percentile** endpoints (Efron & Tibshirani, 1993). The bootstrap procedure uses seed **20261123**. This interval summarizes the stability of the selected-group contrast under resampling of those observations; it is **not** a design-based 95% confidence interval for the complete population of Bangladeshi exported goods or for an independently sampled population of tariff products.

### 4.3.4 H2: Spearman Rank Association and Within-Sector Sensitivity

The second exploratory test assesses whether the recorded **Bangladesh share of a 2025 EU CN8 import market** is monotonically associated with the corresponding **2026 MFN tariff candidate**. The use of **Spearman's rank correlation** avoids requiring a linear association in the original measurement units and is suitable for an exploratory relationship between two unevenly distributed product indicators (Spearman, 1904; Conover, 1999). The analysis is restricted to the same **196 products with numeric MFN candidates**. The two variables have different reference dates, a distinction that prevents temporal or causal interpretation.

Both variables are transformed into **pooled midranks**, giving tied observations their average rank. The statistic is computed as the Pearson correlation of these rank variables:

\[
\rho_S=\operatorname{corr}\{\operatorname{rank}(MS_{BD,p,2025}),\operatorname{rank}(t^{MFN}_{p,2026})\}.
\]

The implemented **two-sided Monte Carlo permutation** holds the first rank vector fixed, randomly shuffles the second, recomputes its correlation for **9,999 permutations**, and counts the absolute correlations at least as large as the observed absolute statistic. The plus-one calculation is again used, with seed **20261122**. No tariff coefficient, causal elasticity, or regression slope is estimated by this procedure.

The analysis includes a particularly important **post-hoc HS2-adjusted robustness check** because different sectors can have systematically different tariff schedules and market-share distributions. Using the **pooled midrank vectors**, the script subtracts the **within-HS2 chapter mean rank** from each product's rank for both variables. The remaining rank residuals are correlated to form a **within-HS2 residualized-rank association**. For its two-sided permutation check, the tariff-rank residuals are shuffled **only within the original HS2 groups**, with **9,999** iterations and seed **20261124**. The procedure is described precisely as a **chapter-demeaned pooled-rank correlation**, not as a causal fixed-effects regression or an independently identified partial effect. Chapters with little or no within-sector variation contribute limited information to this sensitivity analysis.

The pooled statistic and this sector-adjusted sensitivity must be presented **together**, even if the first produces a conventionally small p-value while the second does not. The tests are exploratory, sector adjustment was added after inspection of the pooled analysis, and the purposive cohort was not drawn as an independent random sample of all Bangladesh exports. Neither association establishes that a high MFN rate caused Bangladesh to obtain a particular 2025 EU market share.

### 4.3.5 H3: Exact Paired-Sign Tests and Multiple-Testing Adjustment

The third exploratory hypothesis considers the **direction of within-product customs unit-value differences** between Bangladesh and each of the six selected comparator origins. The matching unit is a **single 2025 CN8 product** observed for Bangladesh and one comparator. For origin **c**, the relative ratio is \(R_{BD,c,p}\), as defined above. Pairs with invalid, absent or nonpositive ratios are excluded. Pairs with ratios effectively equal to one are treated as **ties and removed from the test denominator**, using the implementation tolerance \(|R-1|\le10^{-10}\).

For each comparator, let \(k_c\) be the number of non-tied products satisfying \(R_{BD,c,p}<1\), and let \(n_c\) be the total number of non-tied valid matched products. The sample-direction statistic is \(k_c/n_c\). The null and alternative are **a probability of a lower Bangladesh unit value at most 0.5**, versus **greater than 0.5**. Under the benchmark exact paired-sign formulation, the one-sided upper-tail probability is calculated as

\[
p_c=\sum_{j=k_c}^{n_c}{n_c\choose j}(0.5)^{n_c}.
\]

This is the exact binomial-tail form of the paired-sign test and does not assume that the unit-value *differences themselves* are normally distributed (Conover, 1999). In the archived output the valid non-tied sample sizes are **200 (China), 200 (India), 198 (Viet Nam), 198 (Pakistan), 190 (Cambodia), and 200 (Türkiye)**. The implementation evaluates the binomial tail through exact integer combinations rather than applying a normal approximation.

Because six country comparisons are evaluated, the reported results include the **Benjamini–Hochberg (BH) false-discovery-rate adjustment** over the **six H3 p-values**, not over H1, H2 and the deterministic legal screens. The procedure orders the six p-values from smallest to largest, scales each by \(m/i\) with \(m=6\) and rank \(i\), and uses the reverse cumulative minimum to ensure nondecreasing adjusted values across the ordered tests (Benjamini & Hochberg, 1995). The archived script assigns the resulting **q-values** to their original comparator origins.

The BH method's theoretical error-rate guarantees have dependence conditions; their interpretation requires caution when the same Bangladesh product observations are compared with several origins and when observations share sector characteristics (Benjamini & Yekutieli, 2001). The project has **not** demonstrated the product-level independence or dependence structure required for a rigorous probability-based population claim. Accordingly, these exact-tail calculations and BH-adjusted values are interpreted as exploratory evidence about the **selected matched products**. They are not evidence that prices are for identical quality, that Bangladeshi production is cheaper, or that the country's future competitive response has been estimated.

### 4.3.6 Conditional Tariff-Exposure Calculations and Sensitivity Analysis

Tariff-exposure estimation is a **deterministic accounting procedure**, distinct from the hypothesis-testing methods above. For each specified scenario \(s\) and benchmark \(b\), the source-qualified tariff-rate difference for product \(p\) is applied to the fixed **2025 Bangladesh-origin EU import value**. The aggregate scenario measure is

\[
C_s=\sum_{p\in P_s}V_{BD,p,2025}\frac{t_{s,p}-t_{b,p}}{100},
\]

where \(P_s\) contains only products for which the two rates can be compared numerically under the stated scenario. A rate difference is expressed in **percentage points** and the resulting duty equivalent in **euros**. The baseline, regime assumptions, rate-reference date and coverage are recorded for each comparison.

The scenarios include source-dated **MFN**, **illustrative Standard GSP-like and GSP+-like pathways**, and specified **textile or safeguard-related alternatives**. The legal status of each measure is qualified using the original EU tariff and regulatory documentation rather than assuming that a 2026 rate available to another origin will be payable by Bangladesh after EBA removal (European Parliament & Council of the European Union, 2026). Product lines lacking an unambiguous comparable rate are excluded from the corresponding primary calculation and reported as missing, not imputed at a duty of zero. The archived 2026 MFN reference contains **196 numerically qualified products and four unresolved products**; this difference in coverage must be disclosed whenever totals from distinct scenarios are compared.

Robustness and coverage checks consider the **top-10/50/100/200 product cohorts**, **HS2 Chapters 61–63 versus other products**, **current-year exact versus nonexact classification mappings**, the **six selected competitor origins** and two specified competitor groupings, and alternatives in which rates for the **four unresolved products** are stressed using openly hypothetical increments of **0, 5, 10, 15 and 20 percentage points**. Those increments are **not** legal rate imputations and do not change the official primary estimate. Aggregated tariff differences across origin groups are weighted according to the **2025 Bangladesh import value on the valid country–product pairs**, with denominators documented separately because candidate-rate coverage can differ among countries.

The static equivalents do not include substitution elasticities, actual tariff incidence, changes in production, or response of trade volumes and prices. Unlike behavioural general-equilibrium or partial-equilibrium assessments of LDC graduation, they cannot estimate welfare or lost export revenue (Rahman & Strutt, 2024; Bekkers & Cariola, 2025). No p-value is attached to an accounting identity.

### 4.3.7 Historical Article 33 Screening: Arithmetic, Denominators, and Legal Status

The special safeguard component applies **deterministic legal-threshold calculations** to EU import totals for **HS Chapters 61–63** for the historical years **2023, 2024 and 2025**. For each year \(y\), \(B_y\) denotes the Bangladesh-origin import value for the relevant product section, \(G_{y,R}\) denotes imports from the set of GSP beneficiary countries specified by roster \(R\), and \(U_y\) denotes the official relevant imports from **all extra-EU origins**. The separate ratios are:

\[
S^{37}_{y,R}=100B_y/G_{y,R},\qquad
S^{6}_y=100B_y/U_y.
\]

The **37%** and **6%** comparisons use **different legally defined denominators**. The primary historic screening uses an explicitly identified **2027 beneficiary roster projected backward to earlier trade years**, so the resulting values are **roster-conditioned arithmetic backcasts**, not legal findings about the exact beneficiary populations that were operative in 2023–2025. Where the sum of available origin rows does not fully reproduce a published official aggregate, the analysis records the discrepancy and evaluates stated residual sensitivity rather than assuming missing origin trade is zero.

Article 33 also contains **an EBA-beneficiary exception and a Commission implementing-act procedure**. Therefore, neither reaching the calculated numerical threshold nor exceeding the all-import-share comparison establishes an actual safeguard against Bangladesh while it remains under EBA or predicts a future implementing decision. These conclusions arise from the original legal criteria, not an estimate of a random variable (European Parliament & Council of the European Union, 2026, art. 33; Annex IV). **No statistical-significance test is applied to the legal threshold arithmetic.**

### 4.3.8 Reproducibility, Interpretation, and Methods Not Used

The archived Task G script independently checks source-file SHA-256 digests before performing the exploratory tests and regenerating its CSV/JSON outputs. Its core inputs include **200 unique product rows**, **1,200 unique matched competitor rows**, a **40-row scenario coverage table**, and a **14-year historical Article 33 screening table**; the principal narrative interpretation of the legal screens remains focused on **2023–2025**. The verification process reconciles the recorded trade values, valid tariff joins and arithmetic identities to the source files, tests missing-data flags, and documents alternative-sector, supplier and source-coverage results. Eleven upstream input fingerprints passed the archived verification, and a separate independent arithmetic audit reported no numerical discrepancies for its specified checks. Those results establish **computational consistency of the frozen outputs**, not that the underlying future legal rates or unobserved exporter responses have been verified.

For academic reporting, **Chapter 4 documents algorithms, sample denominators, assumptions and sources**; the numeric values of test statistics, p-values, q-values, interval endpoints and scenario results are reserved for **Chapter 5**. H1–H3 were specified after reviewing prior analysis and hence are not preregistered confirmatory hypotheses. The approximate exchangeability assumed in the permutation procedures, the independent-sign benchmark of H3, the cross-product dependence of tariff classifications, and the multiple-testing conditions all restrict inferential interpretation. No significance result is used to override an observed lack of robustness when HS2 is taken into account. Nor does the use of a random-number generator make the purposively selected products a random sample.

Consistent with the actual research design, **no survey-scale reliability test, regression coefficient, SEM, difference-in-differences estimate, structural gravity parameter, or causal treatment effect is presented as executed**. The separate directed documentary content analysis in Section 4.2 qualifies the legal meaning of the quantitative inputs; it does not create an independent interview dataset or change the statistical unit of observation. Sections 4.4 and 4.5 document the detailed source filters, sample-selection process, input lineage, transformations, missingness decisions and the sequence of independent numerical checks that make these quantitative procedures reproducible.

---

## References Cited in Section 4.3 (APA 7th Edition)

Athey, S., & Imbens, G. W. (2017). The state of applied econometrics: Causality and policy evaluation. *Journal of Economic Perspectives, 31*(2), 3–32. https://doi.org/10.1257/jep.31.2.3

Benjamini, Y., & Hochberg, Y. (1995). Controlling the false discovery rate: A practical and powerful approach to multiple testing. *Journal of the Royal Statistical Society: Series B (Methodological), 57*(1), 289–300. https://doi.org/10.1111/j.2517-6161.1995.tb02031.x

Benjamini, Y., & Yekutieli, D. (2001). The control of the false discovery rate in multiple testing under dependency. *The Annals of Statistics, 29*(4), 1165–1188. https://doi.org/10.1214/aos/1013699998

Conover, W. J. (1999). *Practical nonparametric statistics* (3rd ed.). John Wiley & Sons.

Efron, B., & Tibshirani, R. J. (1993). *An introduction to the bootstrap*. Chapman & Hall.

European Parliament, & Council of the European Union. (2026). *Regulation (EU) 2026/1395 of 17 June 2026 on applying a generalised scheme of tariff preferences and repealing Regulation (EU) No 978/2012*. *Official Journal of the European Union*. https://eur-lex.europa.eu/eli/reg/2026/1395/oj/eng

Eurostat. (2025). *International trade in goods—Detailed data (ext_go_detail): Reference metadata*. European Commission. https://ec.europa.eu/eurostat/cache/metadata/en/ext_go_detail_sims.htm

Gervais, A. (2015). Product quality and firm heterogeneity in international trade. *Canadian Journal of Economics/Revue canadienne d'économique, 48*(3), 1152–1174. https://doi.org/10.1111/caje.12171

Phipson, B., & Smyth, G. K. (2010). Permutation p-values should never be zero: Calculating exact p-values when permutations are randomly drawn. *Statistical Applications in Genetics and Molecular Biology, 9*(1), Article 39. https://doi.org/10.2202/1544-6115.1585

Rahman, M. M., & Strutt, A. (2024). Costs of LDC graduation on market access: Evidence from emerging Bangladesh. *Economic Systems Research, 36*(1), 24–45. https://doi.org/10.1080/09535314.2022.2138271

Spearman, C. (1904). The proof and measurement of association between two things. *The American Journal of Psychology, 15*(1), 72–101. https://doi.org/10.2307/1412159

Bekkers, E., & Cariola, G. (2025). The impact of LDC graduation on trade: A quantitative assessment. *The Journal of International Trade & Economic Development, 34*(3), 397–427. https://doi.org/10.1080/09638199.2024.2323661
