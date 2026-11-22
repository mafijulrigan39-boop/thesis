# CHAPTER 4: RESEARCH METHODS

## 4.3 Quantitative Methods and Statistical Tools

The quantitative analysis was constructed to answer five distinct research questions about Bangladesh's observed product-market position in the European Union (EU), its position relative to competing origins, the structure of relevant tariff preferences, and conditional exposure to changing market-access rules. It combines **descriptive measurements, product-matched comparisons, three groups of post-hoc exploratory statistical tests, and deterministic accounting and legal-screening calculations**. These procedures are not interchangeable. Descriptive indicators document the available import records; exploratory tests summarize patterns under explicit statistical assumptions; and fixed-value tariff or safeguard calculations implement arithmetic identities and legal definitions. None identifies the causal effect of an eventual withdrawal of the EU's Everything But Arms (EBA) arrangement, which has not occurred in the observed data. Inferences of a policy treatment effect would require an appropriate counterfactual and identification strategy (Athey & Imbens, 2017), whereas the present study measures **source-dated statutory exposure and observed competitiveness indicators**.

### 4.3.1 Analytical Population, Variables, and Computation Sequence

The principal reference dataset is **Eurostat Comext DS-045409**, with reporter **EU27_2020**, flow **imports**, partner **country of origin**, reference year **2025**, and product classification **CN8**. Eurostat values are recorded in **euros** on an import-side statistical valuation basis, generally cost, insurance and freight (CIF), rather than as Bangladesh's own FOB export declarations (Eurostat, 2025). The 200 CN8 lines selected by descending Bangladesh-origin import value form the primary cross-section. For each line, the study uses the corresponding official all-extra-EU-origin import total. It additionally considers six comparator origins—China (CN), India (IN), Viet Nam (VN), Pakistan (PK), Cambodia (KH), and Türkiye (TR)—yielding **200 × 6 = 1,200** planned CN8-by-competitor comparisons. Historical **2023–2025 HS Chapters 61–63** comprise a separate annual dataset for the legal safeguard screen, not a historical version of the 2025 CN8 product sample.

The tariff reference is **1 November 2026**, using source-date EU TARIC measures, which contain conditions and legislation as well as numeric tariff candidates (European Commission, Directorate-General for Taxation and Customs Union, n.d.). Consequently, a 2026 tariff candidate paired with a 2025 import observation is a **comparative benchmark**, not a tariff demonstrably imposed on that earlier shipment. The core usable sample counts and their meanings are shown in Table 4.3.

**Table 4.3. Observational units, effective sample sizes, and coverage**

| Measurement or calculation | Initial frame | Effective coverage | Exclusion or qualification |
|---|---:|---:|---|
| Bangladesh-origin 2025 CN8 products | 200 | 200 | Purposive highest-value lines |
| Bangladesh EU market-share calculations | 200 | 200 independently checked | Official all-extra-EU denominator |
| Six origin-matched product comparisons | 1,200 | 1,200 constructed pairs | Not a census of all EU suppliers |
| Valid Bangladesh/comparator EUR/kg ratios | 1,200 | 1,186 | 14 invalid or unavailable ratios |
| Numeric 2026 MFN product rate candidates | 200 | 196 | Four unresolved CN8 candidates |
| Numeric source-conditional comparator tariff candidates | 1,200 | 1,183 | Seventeen unresolved candidates |
| H1 and pooled/adjusted H2 products | 200 | 196 | Complete numeric MFN candidate and relevant recorded variables |
| Historical Article 33 annual source screens | 2012–2025 (14 years) | 2023–2025 (3 years) emphasized | 2027-roster historical backcast, not legally operative historical test |

*Source: Author's calculations and independent verification of Eurostat 2025 trade records, source-dated 2026 TARIC candidate measures, and the stated legal screening data. “Usable” refers to mathematical or source-defined completeness, not unconditional legal applicability.*

The sequence of the work is explicit. First, retain CN8 identifiers as eight-character product codes and select 200 highest-valued Bangladesh-origin lines. Second, attach the published product-specific extra-EU import totals and matched origin records. Third, compute descriptive values, shares, concentration, and valid unit values. Fourth, join source-dated tariff candidates without converting missing, ambiguous, specific or mixed legal duties into fabricated numeric ad valorem rates. Fifth, conduct the exploratory comparisons **H1–H3** on their respective complete-case groups. Sixth, construct fixed-trade-value scenario totals and the separately sourced Article 33 ratios. Finally, verify sample counts, formulas, source consistency and missing-value flags independently.

### 4.3.2 Descriptive Statistics: Shares, Concentration, and a Worked CN8 Observation

Let \(p\) index the selected 2025 CN8 products, \(c\) an extra-EU origin, \(V_{c,p}\) the EU's reported import value in euros, and \(V_{\mathrm{all},p}\) the published **all-extra-EU-origin** value for product \(p\). Bangladesh's EU product-market share is:

\[
MS_{BD,p}=100\frac{V_{BD,p}}{V_{\mathrm{all},p}}\quad(\%).
\tag{4.1}
\]

The denominator is **not** the six competing origins summed together, and a missing or zero denominator is not treated as a zero share. The total Bangladesh import value among selected lines is:

\[
V_{200}=\sum_{p=1}^{200}V_{BD,p}
       =\mathbf{€20,789,281,101}.
\tag{4.2}
\]

Define the within-basket share \(w_p=V_{BD,p}/V_{200}\) and the conditional product concentration index:

\[
HHI_{200}=\sum_{p=1}^{200}w_p^2,\qquad
HHI_{200}^{(10,000)}=10,000\,HHI_{200}.
\tag{4.3}
\]

Direct recomputation of the 200 product values yields \(HHI_{200}=0.04421287\), equivalent to **442.13** on the 0–10,000 scale. The ten highest-valued products account for **48.6756%** of the selected basket, while the top fifty account for **82.9065%**. These quantities describe concentration **within the purposively selected top-200 portfolio**, not the full universe of Bangladesh exports. An HHI calculated for EU supplier origins is a different measure: it requires all origin-country shares and must be marked provisional or bounded when identified origin rows do not fully reconcile to the official all-origin total.

A directly reproducible worked example is **CN8 61091000**. The EU's reported 2025 import value originating in Bangladesh was **€3,499,230,143**, against the official all-extra-EU total **€6,864,603,305** for this product. Thus,

\[
MS_{BD,61091000}
=100\frac{3,499,230,143}{6,864,603,305}
=\mathbf{50.9750\%}.
\tag{4.4}
\]

Its contribution to the selected Bangladesh basket is

\[
100\frac{3,499,230,143}{20,789,281,101}
=\mathbf{16.8319\%}.
\tag{4.5}
\]

The distinction between these denominators matters: **50.9750%** measures Bangladesh's position in one EU product market; **16.8319%** measures that product's weight in the selected Bangladesh-origin basket. Neither number is the conventional worldwide Balassa revealed comparative advantage index or a causal estimate of the effect of preferential market access (French, 2017).

### 4.3.3 Matched Supplier Comparisons and Customs Unit Values

The same official product-market denominator is used for each competitor's market share,

\[
MS_{c,p}=100\frac{V_{c,p}}{V_{\mathrm{all},p}}.
\tag{4.6}
\]

For CN8 61091000, **China-origin EU imports were €413,860,151**, representing

\[
MS_{CN,61091000}
=100\frac{413,860,151}{6,864,603,305}
=\mathbf{6.0289\%}.
\tag{4.7}
\]

The fact that Bangladesh's share and China's share are calculated against the same product total makes this a destination-product comparison; it does not explain their difference by tariffs alone.

Where valid positive net-mass observations \(Q_{c,p}\) exist, customs unit value and the Bangladesh-to-comparator ratio are defined as:

\[
UV_{c,p}=\frac{V_{c,p}}{Q_{c,p}}\quad(\mathrm{EUR/kg}),
\qquad
R_{BD,c,p}=\frac{UV_{BD,p}}{UV_{c,p}}.
\tag{4.8}
\]

For CN8 61091000, Bangladesh's recorded unit value is **€11.85968/kg** and the matched ratio relative to China is **0.6285125**. The corresponding China unit value is therefore approximately

\[
UV_{CN,61091000}
=\frac{11.85967554}{0.62851248}
=\mathbf{€18.86944/kg}.
\tag{4.9}
\]

A ratio below one means only that **the recorded import customs value per kg** is lower for Bangladesh within that CN8 code. It does not establish equal quality, a lower factory-gate price, or superior productivity; unit values can reflect quality, item mix, freight and other differences (Gervais, 2015). Invalid or unavailable masses are excluded, resulting in **1,186 usable ratios** from **1,200 candidate comparisons**. Each of the six countries is analysed separately, avoiding the false independence that would arise from treating six rows sharing the same Bangladesh product as six unrelated Bangladesh observations.

### 4.3.4 Tariff Benchmarks, Preference Margins, and Observed Coverage

Let \(t^{MFN}_{p,2026}\) be the source-qualified **1 November 2026** MFN candidate for CN8 product \(p\), and \(t^{BD}_{p,2026}\) Bangladesh's EBA candidate rate where legally eligible. Let \(t^{c}_{p,2026}\) be a conditional rate candidate for comparison origin \(c\). The **MFN-reference margin** and **relative tariff advantage** are defined as:

\[
PM_{BD,p}=t^{MFN}_{p,2026}-t^{BD}_{p,2026},
\qquad
A_{BD,c,p}=t^c_{p,2026}-t^{BD}_{p,2026}.
\tag{4.10}
\]

These differences are measured in **percentage points**. A source rate is only a candidate: beneficiary status, precise product classification, rules of origin, documentary compliance and actual preferential claims must be assessed separately. The EU tariff database identifies measures and conditions, while the revised GSP regulation governs relevant preferences and legal mechanisms (European Commission, Directorate-General for Taxation and Customs Union, n.d.; European Parliament & Council of the European Union, 2026). Empirical research shows why legal entitlement does not imply universal utilisation (Cipollina et al., 2017; Sytsma, 2021).

Of the 200 selected products, **196** contain numeric 2026 MFN candidates; **four** lack a qualified numeric rate. Their trade-value coverage is:

\[
\begin{aligned}
V_{\mathrm{rated}}&=\mathbf{€20,658,197,864},\\
V_{\mathrm{missing}}&=\mathbf{€131,083,237},\\
\mathrm{Coverage}&=100\frac{20,658,197,864}{20,789,281,101}
=\mathbf{99.3695\%}.
\end{aligned}
\tag{4.11}
\]

This is **trade-value coverage**, not the percentage of shipments that claimed a preference. The product-count coverage is \(196/200=98\%\). The candidate-rate matrix for the six competitors contains **1,183** numeric origin-product entries out of 1,200; the remaining seventeen are unresolved. Product and value coverage must be reported for **each** scenario because legally distinct rate pathways do not always produce the same set of qualified products.

### 4.3.5 Hypothesis H1: One-Sided Permutation Test and Bootstrap Stability Interval

**H1** examines the difference between unweighted mean MFN candidates for the selected HS2 **61–63** products and the selected **other-HS2** products. For the **196** numerically rated lines, the group sizes are \(n_A=152\) and \(n_O=44\). The statistic is:

\[
T_{H1}=\overline{t}_{A}-\overline{t}_{O},
\quad
H_0:T_{H1}\le 0,\quad
H_A:T_{H1}>0.
\tag{4.12}
\]

From the observed rate candidates:

\[
\begin{aligned}
\overline{t}_A&=\mathbf{11.75986842\%},\\
\overline{t}_O&=\mathbf{7.82045455\%},\\
T_{H1}&=11.75986842-7.82045455
=\mathbf{3.93941388\ \text{percentage points}}.
\end{aligned}
\tag{4.13}
\]

The exploratory Monte Carlo permutation proceeds in the following order. Pool the **196** observed rates; retain the fixed group sizes **152 and 44**; randomly shuffle the pooled rates; assign the first 152 rates to the first simulated group and the remaining 44 to the second; recompute the difference in arithmetic means; repeat **9,999** times with base pseudorandom seed **20261121**; and count simulated statistics at least as large as the observed gap, using a numerical tolerance of \(10^{-12}\). The reported upper-tail Monte Carlo p-value is

\[
\widehat{p}_{H1}=\frac{b+1}{9,999+1},
\tag{4.14}
\]

where \(b\) is the count of extreme permutations (Phipson & Smyth, 2010). **Permutation-inference qualification:** The directional null \(H_0:T_{H1}\le0\) describes the substantive mean-rate contrast. Shuffling the observed sector labels requires the **stronger exchangeability assumption of identical rate distributions under the randomization-reference null**. The calculated p-value is not an exact test for every conceivable distribution having a nonpositive mean gap. Sector labels were not randomly assigned; the p-value is consequently a conditional exploratory diagnostic, not a proof of a causal or population-level difference.

The archived execution produced **\(b=0\)** and \(\widehat{p}_{H1}=\mathbf{0.0001}\). It would be incorrect to report \(p=0\), to interpret the result as tariff-policy causality, or to assume the administrative sector labels were randomized.

For a separate descriptive stability check, **1,999 bootstrap resamples** were drawn independently **with replacement within each group**, using seed **20261123**, and the mean-rate difference was recomputed for each. The sorted simulated differences were used to obtain the empirical **2.5th and 97.5th percentiles**:

\[
CI^{boot}_{2.5\%,97.5\%}
=\mathbf{[2.3987,\ 5.4197]\ \text{percentage points}}.
\tag{4.15}
\]

These endpoints indicate how the estimated mean difference varies under resampling the **selected rates**; they are **not** design-based confidence limits for a probability sample of Bangladesh's complete export universe (Efron & Tibshirani, 1993). The comparison chiefly describes tariff-schedule heterogeneity rather than any observed change in trade.

### 4.3.6 Hypothesis H2: Spearman Correlation and Within-HS2 Robustness

**H2** evaluates the *monotonic association* between Bangladesh's **2025** product-level EU import-market share \(MS_{BD,p}\) and the separately dated **2026** MFN candidate \(t^{MFN}_{p,2026}\) among the **196 qualified products**. The two-sided hypotheses are \(H_0:\rho_S=0\) and \(H_A:\rho_S\ne0\). Since ties in tariff rates are common, each variable is converted to **pooled midranks**, with equal values assigned their mean rank. Spearman's coefficient is the ordinary Pearson correlation of those midranks (Spearman, 1904; Conover, 1999):

\[
\rho_S=
\frac{\sum_{p=1}^{196}(R_{MS,p}-\overline{R}_{MS})(R_{t,p}-\overline{R}_{t})}
{\sqrt{\sum_{p=1}^{196}(R_{MS,p}-\overline{R}_{MS})^2
\sum_{p=1}^{196}(R_{t,p}-\overline{R}_{t})^2}}.
\tag{4.16}
\]

The observed pooled association is \(\rho_S=\mathbf{0.18872981}\). To calculate a **two-sided permutation p-value**, retain the share-rank vector, shuffle the tariff-rank vector **9,999 times** with seed **20261122**, and compare the **absolute** permuted correlation with \(|\rho_S|\). Applying the plus-one calculation gives:

\[
\widehat p_{H2}=
\frac{86+1}{9,999+1}
=\mathbf{0.0087}.
\tag{4.17}
\]

A small pooled permutation p-value is insufficient on its own because **2025 market shares and 2026 MFN schedules both differ systematically across HS chapters**. The executed **post-hoc within-HS2 sensitivity** first computes pooled midranks for both variables and then subtracts the mean pooled rank of the product's own HS2 group:

\[
R^{*}_{MS,p}=R_{MS,p}-\overline{R}_{MS,\,HS2(p)},
\qquad
R^{*}_{t,p}=R_{t,p}-\overline{R}_{t,\,HS2(p)}.
\tag{4.18}
\]

The residualized-rank correlation is \(\rho_{S,HS2}=\operatorname{corr}(R^{*}_{MS},R^{*}_{t})\). For its permutation check, the **tariff-rank residuals are shuffled only within each HS2 chapter** using **9,999 iterations** and seed **20261124**. The calculated sensitivity is:

\[
\rho_{S,HS2}=\mathbf{-0.00958723},
\qquad
\widehat p_{HS2}=\frac{8,429+1}{10,000}
=\mathbf{0.8430}.
\tag{4.19}
\]

This sensitivity indicates that **the pooled positive association does not persist within HS2 chapters** under the chosen method. It is not an estimated treatment effect and is not a fitted multivariate regression. Importantly, the HS2 check was itself specified **after examination of the pooled result**; both analyses are exploratory and must be reported together rather than selectively emphasizing the pooled statistic.

### 4.3.7 Hypothesis H3: Exact Matched-Sign Tests and Benjamini–Hochberg Adjustment

**H3** assesses whether Bangladesh has a lower recorded **customs EUR/kg unit value** than a particular competitor in **more than half of the available matched 2025 CN8 products**. For each comparison origin \(c\), construct the ratio \(R_{BD,c,p}\) in Equation (4.8). Exclude missing/nonpositive ratios and ties satisfying \(|R_{BD,c,p}-1|\le10^{-10}\). Let \(k_c\) denote the number of remaining ratios below one and \(n_c\) the number of valid non-tied matched products. The observed directional proportion is

\[
\widehat\pi_c=\frac{k_c}{n_c}.
\tag{4.20}
\]

For the one-sided hypotheses \(H_0:\pi_c\le0.5\) and \(H_A:\pi_c>0.5\), the reference **exact paired-sign/binomial-tail** probability is

\[
p_c=\sum_{j=k_c}^{n_c}\binom{n_c}{j}(0.5)^{n_c}.
\tag{4.21}
\]

The exact sign approach does not require normally distributed *magnitudes* of paired differences, although its probability interpretation assumes an appropriate null model for their directions (Conover, 1999). Table 4.4 presents **all six observed counts, test proportions, original exact p-values, and multiplicity-adjusted values** so the quantitative assessment is fully visible.

**Table 4.4. Completed exploratory matched-sign calculations, six competing origins**

| Comparator | Valid \(n_c\) | BD lower \(k_c\) | \(k_c/n_c\) | Exact one-sided \(p_c\) | BH-adjusted \(q_c\) |
|---|---:|---:|---:|---:|---:|
| China | 200 | 129 | 0.6450 | 2.4865 × 10⁻⁵ | 2.9838 × 10⁻⁵ |
| India | 200 | 154 | 0.7700 | 4.0852 × 10⁻¹⁵ | 6.1278 × 10⁻¹⁵ |
| Viet Nam | 198 | 171 | 0.8636 | 4.3235 × 10⁻²⁷ | 1.2971 × 10⁻²⁶ |
| Pakistan | 198 | 96 | 0.4848 | 0.6905 | 0.6905 |
| Cambodia | 190 | 151 | 0.7947 | 4.6979 × 10⁻¹⁷ | 9.3957 × 10⁻¹⁷ |
| Türkiye | 200 | 179 | 0.8950 | 9.7348 × 10⁻³³ | 5.8409 × 10⁻³² |

*Note.* \(\widehat\pi_c\) refers only to the **observed selected product matches**, not a randomly sampled population of all exports. Values are calculated from valid same-CN8/year customs EUR/kg ratios and are **not** tests of quality-adjusted prices, production costs or future resilience.

Because six tests are conducted, the **Benjamini–Hochberg (BH) adjustment** is applied to this family of **six H3 tests**, not retroactively to the descriptive results or the two separate exploratory tariff analyses. Sort the six \(p\)-values in ascending order \(p_{(1)},\ldots,p_{(6)}\), then compute

\[
q_{(i)}=\min\left[1,\ \min_{j\ge i}\left(\frac{6}{j}p_{(j)}\right)\right],
\tag{4.22}
\]

and return the values to their original country labels (Benjamini & Hochberg, 1995). In the ordered list, **China ranks fifth**; its adjustment provides a worked example:

\[
q_{CN}=\min\!\left(1,\frac65\times2.48648674\times10^{-5},\ldots\right)
=\mathbf{2.98378409\times10^{-5}}.
\tag{4.23}
\]

The original BH procedure has conditions for false-discovery-rate control, and the matched product sets and overlapping supplier comparisons may be dependent. No formal verification of the required dependence assumptions was undertaken; accordingly, the adjusted values are **exploratory diagnostics**, not confirmatory population claims. Benjamini and Yekutieli (2001) discuss the relevance of dependence to multiple-testing guarantees. In particular, the Pakistan comparison does **not** support the one-sided hypothesis that Bangladesh's customs unit value is lower in a majority of its valid matched products.

### 4.3.8 Deterministic Static Tariff Exposure: Full Formula and Worked Amounts

The prospective tariff-exposure component is an **accounting identity**, not a statistical forecast. For each scenario \(s\), define \(P_s\) as the set of products with numerically qualified, appropriately specified scenario and baseline tariff-rate candidates. Let \(t_{s,p}\) and \(t_{b,p}\) be their respective percentage rates. The fixed-trade-value additional duty equivalent is:

\[
C_s=\sum_{p\in P_s}V_{BD,p,2025}
\left(\frac{t_{s,p}-t_{b,p}}{100}\right).
\tag{4.24}
\]

Each product-level contribution is independently checked by substituting its **2025 observed EU import value** and the corresponding **1 November 2026 tariff-rate gap**. For **CN8 61091000**, the selected legal benchmark contains a **12% MFN candidate** and a **0% Bangladesh EBA candidate**, subject to eligibility. Its hypothetical MFN-versus-EBA contribution is therefore

\[
C_{61091000}=
€3,499,230,143\left(\frac{12-0}{100}\right)
=\mathbf{€419,907,617.16}.
\tag{4.25}
\]

Summing these values for all **196** numerically qualified products gives

\[
\boxed{C_{MFN,2026}=\mathbf{€2,443,135,906.98}}
\tag{4.26}
\]

on **€20,658,197,864** in covered 2025 trade. The corresponding **value-weighted average rate difference** is:

\[
\overline{\Delta t}_{w}
=100\frac{2,443,135,906.98}{20,658,197,864}
=\mathbf{11.82647\ \text{percentage points}}.
\tag{4.27}
\]

This is a **static, source-vintage-specific duty equivalent**, not an amount actually collected in 2025, a future EU legal assessment, or a loss of Bangladesh export revenue. A behavioural forecast would additionally require tariff incidence, substitution elasticities, prices and supply responses of the kind specified in genuine partial- or general-equilibrium models (Rahman & Strutt, 2024; Bekkers & Cariola, 2025).

The executed scenario analysis reports **the qualified count, covered value and duty equivalent separately for each scenario**.

**Table 4.5. Conditional rate-reference scenarios, fixed 2025 values**

| Tariff-reference scenario | Qualified lines | Covered 2025 EU value | Coverage of top-200 value | Static duty equivalent |
|---|---:|---:|---:|---:|
| 2026 MFN instead of the EBA reference | 196 | €20,658,197,864 | 99.3695% | €2,443,135,906.98 |
| India 2026 Standard-GSP-channel **proxy** | 184 | €20,450,872,864 | 98.3722% | €1,916,058,587.69 |
| Pakistan 2026 GSP+-channel **proxy** | 197 | €20,766,255,464 | 99.8892% | €5,239,942.31 |
| Section S-11b illustrative Article 7 duty reduction | 152 | €19,629,907,994 | 94.4232% | €1,868,777,048.07 |
| Section S-11b **hypothetical** Article 33 MFN treatment | 152 | €19,629,907,994 | 94.4232% | €2,335,971,310.08 |

*Note.* Each row is a separately qualified **illustration** with its own rate assumptions and missingness. India- or Pakistan-channel rates are **not established future Bangladesh entitlements**; the hypothetical Article 33 scenario requires a future change in Bangladesh's eligibility and a Commission implementing act. The rows cannot be ranked as forecasts or treated as strictly comparable total economic losses because their coverage differs.

### 4.3.9 Coverage, Cohort, Sector, Classification, and Missing-Rate Sensitivities

Because tariff scenarios are calculated over subsets of products, **coverage is an integral part of the result**, not a footnote. For the MFN-reference comparison, the calculation is reproduced for progressively larger cohorts ranked by **2025 Bangladesh-origin value**:

**Table 4.6. MFN-reference sensitivity to selected product-cohort size**

| Cohort | Numeric-rate products | Qualified 2025 trade value | Static MFN duty equivalent |
|---|---:|---:|---:|
| Top 10 | 10/10 | €10,119,315,537 | €1,214,317,864.44 |
| Top 50 | 50/50 | €17,235,668,132 | €2,062,863,853.63 |
| Top 100 | 98/100 | €19,458,249,463 | €2,317,111,695.17 |
| Top 200 | 196/200 | €20,658,197,864 | €2,443,135,906.98 |

The all-200 benchmark is also separated by sector. Among the **152 selected HS61–63 products**, the qualified fixed-value MFN equivalent is **€2,335,971,310.08**. The **remaining 48 products**, of which 44 have valid MFN candidates, contribute **€107,164,596.90**; the two values sum to **€2,443,135,906.98**, with a one-cent rounding difference possible when displaying separately rounded subtotals. In a separate **2025 classification-match sensitivity**, 180 products are labelled exact one-to-one and 20 complex or nonexact, with respective calculated duty equivalents of **€2,279,472,482.53** and **€163,663,424.46**. These classifications do **not** establish an authenticated harmonized product series for 2012–2025; annual CN8 changes still require validated concordances (Baumgartner et al., 2023).

The four products lacking numeric MFN candidates collectively represent **€131,083,237** of the 2025 selected trade value. They remain **missing** in the primary calculation. An expressly hypothetical stress exercise assigns the *unresolved value as a block* a possible additional rate of \(h\) percentage points, with \(h\in\{0,5,10,15,20\}\), without presenting this assumption as an actual EU duty:

\[
C^{stress}(h)=€2,443,135,906.98
+€131,083,237\left(\frac{h}{100}\right).
\tag{4.28}
\]

The resulting arithmetic values are:

| Hypothetical rate on four unresolved products | Illustrative total |
|---:|---:|
| 0 percentage points | €2,443,135,906.98 |
| 5 percentage points | €2,449,690,068.83 |
| 10 percentage points | €2,456,244,230.68 |
| 15 percentage points | €2,462,798,392.53 |
| 20 percentage points | €2,469,352,554.38 |

This is a **bounded scenario sensitivity**, not rate imputation. Origin-specific relative tariff margins are similarly averaged using the **Bangladesh 2025 import value of only the qualified product–origin pairs** as weights, so each origin's sample size and weighting denominator are explicit. The resulting conditional weighted average margins are **11.8265 percentage points** for China (196 rate-qualified matches), **9.3779** for India (196), **0.2000** for Viet Nam (193), **0.0274** for Pakistan (199), **3.9410** for Cambodia (200), and **0.0000** for Türkiye (199). These describe the particular **2026 candidate pathways** chosen, not the tariff actually claimed by every shipment from those origins. The value and statistical significance of the earlier H3 unit-value comparisons must not be inferred from the pattern of these tariff margins.

### 4.3.10 Article 33 Legal-Threshold Calculations: Three Historical Years

The separate safeguard calculation concerns the legal **Section S-11b** grouping represented by **HS Chapters 61–63**, not the selected 200-product CN8 cohort. For historical year \(y\), let \(B_y\) denote EU imports originating in Bangladesh, \(G_{y,R}\) imports from the relevant **GSP-beneficiary origins under specified roster \(R\)**, and \(U_y\) the official EU imports from **all extra-EU origins**. The ratios are

\[
S_{37,y,R}=100\frac{B_y}{G_{y,R}},
\qquad
S_{6,y}=100\frac{B_y}{U_y}.
\tag{4.29}
\]

The **37% threshold** and the separate **6% all-import-share exception** have different denominators; the 2026 revised EU regulation also excludes EBA beneficiary countries from this special safeguard mechanism and requires a Commission implementing act for operative measures (European Parliament & Council of the European Union, 2026, art. 33; Annex IV).

**Table 4.7. Historical section-level numeric screens using the 2027 Annex I GSP-roster backcast**

| Year | Bangladesh imports, \(B_y\) | 2027-roster GSP imports, \(G_{y,R}\) | All-extra-EU section imports, \(U_y\) | \(S_{37}\) | \(S_6\) |
|---|---:|---:|---:|---:|---:|
| 2023 | €17,790,826,006 | €36,123,308,681 | €96,587,773,768 | 49.2503% | 18.4193% |
| 2024 | €18,677,925,088 | €37,947,732,077 | €101,912,600,479 | 49.2201% | 18.3274% |
| 2025 | €19,865,351,190 | €40,782,984,357 | €108,130,114,257 | 48.7099% | 18.3717% |

*Note.* The **2027 Annex I roster** is applied retrospectively and deliberately to **2023–2025** observations; the table therefore represents **illustrative numerical backcasts**, not historically operative country eligibility, Commission decisions or predictions of future safeguard imposition.

The 2025 values can be recalculated directly:

\[
S_{37,2025}
=100\frac{19,865,351,190}{40,782,984,357}
=\mathbf{48.7099\%},
\tag{4.30}
\]

\[
S_{6,2025}
=100\frac{19,865,351,190}{108,130,114,257}
=\mathbf{18.3717\%}.
\tag{4.31}
\]

They are **not the same ratio**, and the observation that the historical \(S_{37}\) value exceeds 37% does not mean that the Article 33 mechanism actually applied to Bangladesh. As a denominator-reconciliation sensitivity, the calculation allocates all positive unassigned country-origin residual to the GSP denominator. The 2025 screening ratio falls from **48.7099%** to **47.2092%** under that deliberately conservative arithmetic assumption; corresponding figures for 2023 and 2024 are **47.8804%** and **47.8424%**. These remain *historical, roster-conditioned screens*. No p-value, confidence interval or inferred probability of a future Commission decision is attached to these legal calculations.

### 4.3.11 Software Implementation, Verification Sequence, and Statistical Boundaries

The empirical calculations were made using **Python 3.12**, with an independently executed verification routine written in the Python standard library. The procedure used CSV parsing for input matrices, floating-point arithmetic for exploratory statistics, exact integer binomial coefficients for sign-test tails, deterministic seeded pseudorandom permutations, and **SHA-256** source-file fingerprints. To reproduce the statistical checks, the following implementation sequence was applied:

1. Verify the specified source fingerprints and assert **200 unique CN8 product records**, **1,200 unique CN8–competitor records**, **40 scenario-subset rows**, and **14 annual safeguard-screen rows**.
2. Read numeric trade values and tariff candidates without treating blank numeric fields as zero; assert the selected basket total **€20,789,281,101**, **196** numeric MFN lines, and **four** unresolved lines with combined value **€131,083,237**.
3. Recalculate every qualified product's MFN-reference duty equivalent as **value × (MFN minus EBA candidate rate)/100**, checking product contributions to **€0.01**, and reconcile their aggregate to **€2,443,135,906.98**.
4. Split the **196** rated lines by HS2 61–63 versus other chapters; calculate H1 using **9,999** product-label permutations and **1,999** group-stratified bootstrap resamples.
5. Compute **pooled midrank Spearman** correlation for H2, its **9,999** unrestricted two-sided tariff-rank permutations, and a distinct **within-HS2 residualized-rank** correlation with **9,999** within-chapter permutations.
6. For each of the six countries, retain valid non-tied EUR/kg ratios; count ratios below unity; calculate the one-sided exact binomial-tail probability; then apply BH adjustment to the six values.
7. Recompute all defined tariff scenarios by their own valid-rate product sets; record qualified product counts, covered import values and missing cases; conduct cohort, sector, classification and explicitly hypothetical missing-rate sensitivities.
8. For 2023–2025, check **both** Article 33 denominators against their official source totals, reproduce the 2027-roster backcast and residual sensitivities, and retain the EBA exception and implementing-act qualifications.
9. Record all exclusions, numeric outputs and source checks, then conduct an independent arithmetic audit of product shares, tariff scenarios and Article 33 calculations.

The implemented stochastic seeds are **20261121** (H1 permutation), **20261122** (H2 permutation), **20261123** (H1 bootstrap), and **20261124** (H2 within-HS2 permutation). Each permutation analysis uses **9,999** draws, so its reported Monte Carlo p-values have the resolution associated with a denominator of **10,000**. Bootstrap percentiles are calculated from **1,999** sorted group-resampled differences. Source verification covered **11** upstream file fingerprints; independent numerical verification checked **200** product shares, **1,200** competitor pairs, **40** scenario rows and the available annual safeguard figures. This establishes internal **arithmetic and computational consistency of the specified source snapshot**, not certification of all possible future origin qualifications or applicable duties.

The scope of inference requires three final cautions. **First**, the 200 products were selected by observed value, not by probability sampling, and H1–H3 were formulated **after the earlier dataset was inspected**. Their p-values and bootstrap limits are consequently **exploratory diagnostics for a selected cohort**, not preregistered estimates of a national product-population parameter. **Second**, tariff-rate variables refer to **2026**, whereas most market-position variables refer to **2025**, and the eventual Bangladeshi post-EBA event is unobserved. No regression, difference-in-differences design, SEM model or structural gravity equation is claimed to have been estimated; neither product matching nor conventional significance testing alone supplies causal identification (Athey & Imbens, 2017). **Third**, customs unit values cannot be relabelled quality or productivity measures, and no amount calculated from an unchanged trade value can be described as lost export earnings or welfare. These boundaries are necessary for valid use of the observed statistical results and conditional policy arithmetic.

### 4.3.12 Proof-Oriented Validation and Interpretation of Research Findings

All study claims follow the sequence **original source → exact unit and denominator → transparent equation → numeric substitution → independent reproduction → sensitivity analysis → warranted inference → explicit limitation**. This chain distinguishes *arithmetic verification* from *statistical model support* and from *legal applicability*. A correctly calculated number establishes only the mathematical implication of its source values and assumptions; it does not, by itself, establish causation, a firm's costs, or a future tariff rule.

A second, independent calculation of the source records reproduced the 2025 selected-basket value, 200 product market-share computations, concentration index, 1,200 comparison-frame rows, 196 product MFN-rate candidates, H1 group means, H2 pooled and HS2-demeaned rank correlations, six H3 binomial tails, their Benjamini–Hochberg adjustments, all 40 scenario-by-subset rows and all 14 historical Article 33 ratios. The 9,999-draw H1 and H2 permutations, the 1,999-draw H1 bootstrap and the within-HS2 permutations were separately executed with the original order, assigned seeds and code-equivalent calculations; **every simulated count, p-value and reported endpoint was reproduced**. Recomputing the 40 scenarios using ordinary binary floating-point rather than the archived decimal arithmetic produced a maximum numerical difference below **€0.000003**; there were no sample-count, coverage or substantive money-value discrepancies. The independent verification demonstrates **numerical reproducibility**, not universal source legality or identification of future behaviour.

For **RQ1**, the observed 2025 trade values establish destination-product shares and top-200 conditional concentration through arithmetic but not latent comparative productivity. For **RQ2**, the matched ratios and exact signs demonstrate descriptive unit-value patterns—Bangladesh has a lower unit value in a majority of matched products against five selected origins, **not Pakistan**—but not equal-quality cost superiority. For **RQ3**, a mean 2026 tariff-rate gap is observed between selected product groups; the positive pooled 2025 market-share–2026 tariff rank association does **not** persist after within-HS2 rank-centering, so a robust tariff–market-share relationship cannot be claimed. For **RQ4**, applying source-dated rates to unchanged 2025 imports calculates a **static duty-equivalent exposure** for qualified products, not revenue lost, future tariffs paid, or welfare effects. For **RQ5**, two different denominators produce two different historical legal screens; the backcast roster, EBA exception, and implementing-act requirement prevent any claim that a safeguard actually applied or necessarily will apply.

This evidence hierarchy is mandatory for later results and discussion. Both statistically supportive and contrary robustness results must be reported. In particular, the selected cohort is not a probability sample, H1–H3 were developed after preliminary analysis, the permutation reference distributions depend on exchangeability assumptions, the BH adjustment has unverified dependence guarantees, and the legal scenarios are conditional on future regulatory events. Such restraints follow the distinction between reproducible computation and credible causal policy evaluation (Athey & Imbens, 2017; Phipson & Smyth, 2010). The analysis is defended **only to the strongest level that the recorded observations, mathematical method and legally valid assumptions jointly permit**.

---

## References (APA 7th edition)

Anderson, J. E., & van Wincoop, E. (2003). Gravity with gravitas: A solution to the border puzzle. *American Economic Review, 93*(1), 170–192. https://doi.org/10.1257/000282803321455214

Athey, S., & Imbens, G. W. (2017). The state of applied econometrics: Causality and policy evaluation. *Journal of Economic Perspectives, 31*(2), 3–32. https://doi.org/10.1257/jep.31.2.3

Baumgartner, C., Srhoj, S., & Walde, J. (2023). Harmonization of product classifications: A consistent time series of economic trade activities. *Jahrbücher für Nationalökonomie und Statistik, 243*(6), 643–662. https://doi.org/10.1515/jbnst-2022-0034

Bekkers, E., & Cariola, G. (2025). The impact of LDC graduation on trade: A quantitative assessment. *The Journal of International Trade & Economic Development, 34*(3), 397–427. https://doi.org/10.1080/09638199.2024.2323661

Benjamini, Y., & Hochberg, Y. (1995). Controlling the false discovery rate: A practical and powerful approach to multiple testing. *Journal of the Royal Statistical Society: Series B (Methodological), 57*(1), 289–300. https://doi.org/10.1111/j.2517-6161.1995.tb02031.x

Benjamini, Y., & Yekutieli, D. (2001). The control of the false discovery rate in multiple testing under dependency. *The Annals of Statistics, 29*(4), 1165–1188. https://doi.org/10.1214/aos/1013699998

Cipollina, M., Laborde Debucquet, D., & Salvatici, L. (2017). The tide that does not raise all boats: An assessment of EU preferential trade policies. *Review of World Economics, 153*(1), 199–231. https://doi.org/10.1007/s10290-016-0270-0

Conover, W. J. (1999). *Practical nonparametric statistics* (3rd ed.). John Wiley & Sons.

Efron, B., & Tibshirani, R. J. (1993). *An introduction to the bootstrap*. Chapman & Hall.

European Commission, Directorate-General for Taxation and Customs Union. (n.d.). *EU customs tariff (TARIC)*. https://taxation-customs.ec.europa.eu/online-services/online-services-and-databases-customs/eu-customs-tariff-taric_en

European Parliament, & Council of the European Union. (2026). *Regulation (EU) 2026/1395 of 17 June 2026 on applying a generalised scheme of tariff preferences and repealing Regulation (EU) No 978/2012*. *Official Journal of the European Union*. https://eur-lex.europa.eu/eli/reg/2026/1395/oj/eng

Eurostat. (2025). *International trade in goods—Detailed data (ext_go_detail): Reference metadata*. European Commission. https://ec.europa.eu/eurostat/cache/metadata/en/ext_go_detail_sims.htm

French, S. (2017). Revealed comparative advantage: What is it good for? *Journal of International Economics, 106*, 83–103. https://doi.org/10.1016/j.jinteco.2017.02.002

Gervais, A. (2015). Product quality and firm heterogeneity in international trade. *Canadian Journal of Economics/Revue canadienne d'économique, 48*(3), 1152–1174. https://doi.org/10.1111/caje.12171

Phipson, B., & Smyth, G. K. (2010). Permutation p-values should never be zero: Calculating exact p-values when permutations are randomly drawn. *Statistical Applications in Genetics and Molecular Biology, 9*(1), Article 39. https://doi.org/10.2202/1544-6115.1585

Rahman, M. M., & Strutt, A. (2024). Costs of LDC graduation on market access: Evidence from emerging Bangladesh. *Economic Systems Research, 36*(1), 24–45. https://doi.org/10.1080/09535314.2022.2138271

Spearman, C. (1904). The proof and measurement of association between two things. *The American Journal of Psychology, 15*(1), 72–101. https://doi.org/10.2307/1412159
