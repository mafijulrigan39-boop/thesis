# Section 4.3 — Independent Mathematical Audit and Proof-Based Defence

**Date:** 22 November 2026  
**Verdict:** **PASS — no material arithmetic or reproducibility errors detected.**  
**Scope:** 2025 Bangladesh-origin EU import product data (n=200), six-comparator matrix (n=1,200), 1 November 2026 EU tariff candidates, 40 conditional scenario rows, and 2012–2025 annual Article 33 screens (14 years).

## Audit protocol

The auditor independently reopened the original source data and executing scripts. Numerical outputs were recomputed from **original row-level values** rather than accepted on the basis of preprinted summaries. The randomized tests were separately replayed in Python with their original observation order, seed and Monte Carlo specifications. Calculations and methodological limitations were compared with the full manuscript's Equations (4.1)–(4.31).

| Equations / table | Independent calculation and result | Verdict |
|---|---|---|
| **4.1–4.7**; descriptive shares and basket | 200 shares based on official all-extra-EU product totals; €20,789,281,101 selected sum; HHI **0.0442128698310564**, scaled **442.12869831**; top-10 **48.67563957%**, top-50 **82.90651345%**; CN8 61091000 Bangladesh market share **50.97497973%**, basket weight **16.83189585%**, China share **6.02890120%** | **PASS** |
| **4.8–4.9**; unit values | 1,186 valid matched ratios of 1,200; example Bangladesh **€11.85967554/kg** and China **€18.86943515/kg**; ratio **0.62851248316** | **PASS** |
| **4.10–4.11**; tariff margins and coverage | 196 numerically qualified MFN product rates; 1,183 numeric comparator rate candidates; qualified 2025 import value **€20,658,197,864**; missing **€131,083,237**; value coverage **99.36946720%** | **PASS** |
| **4.12–4.15**; H1 mean and sampling | 152 HS61–63 rates average **11.7598684211%**, 44 other rates average **7.8204545455%**; gap **3.9394138756 pp**; re-executed 9,999 permutations seed 20261121 → **0** extreme; **p=0.0001**; bootstrap 1,999 seed 20261123 → **[2.3987440191, 5.4197368421] pp** | **PASS**, exchangeability conditional |
| **4.16–4.19**; H2 rank correlation | Re-ranked all 196 products; pooled rho **0.18872981194**; seed 20261122 → **86** extreme out of 9,999, **p=0.0087**; within-HS2 rho **-0.00958723056**; seed 20261124 → **8,429** extreme, **p=0.8430** | **PASS**; pooled association fails within-HS2 sensitivity |
| **4.20–4.23**; H3 exact signs and BH | Exact signs: CN **129/200**, IN **154/200**, VN **171/198**, PK **96/198**, KH **151/190**, TR **179/200**. Independently computed six binomial-tail p-values and all six BH-adjusted probabilities, matching archived results to floating-point precision | **PASS**, dependence/inference caveat |
| **4.24–4.27**; conditional MFN exposure | 196 rate-qualified lines; product 61091000 duty equivalent **€419,907,617.16**; entire 196-line static total **€2,443,135,906.98**; weighted rate gap **11.8264716171 pp** | **PASS**, not a future customs assessment |
| **4.28**; 4 unresolved rate stresses | (€2,443,135,906.98 + €131,083,237\times h/100), (h\in\{0,5,10,15,20\}) pp: all five displayed values reproduced | **PASS**, hypothetical rates only |
| **4.29–4.31**; safeguard ratios | For **all 14 years 2012–2025**, separate 37% GSP-roster and 6% all-import shares plus residual sensitivity recalculated without deviation at reported precision. 2025: **48.7099007177%**, **18.3717101628%**, residual sensitivity **47.2092089250%** | **PASS**, illustrative 2027-roster backcast |
| **Tables 4.5–4.6**, all scenarios | Independently reassembled 5 rate-scenario formulas × 8 ranked/sector/classification subsets from the 200 line values and 1,400 source tariff candidates, checking product counts, covered trade values and 40 static equivalents | **40/40 PASS**, maximum floating-point difference **€0.0000024** |

## Statistical and logical qualifications retained

1. **Arithmetic proof is not causal proof.** Correct denominators, sums and scenario rates establish an identity for the recorded dataset only.
2. **H1 permutation** shuffles sector labels under a *strong exchangeability reference assumption*; the directional composite null mean difference ≤0 alone does not justify the randomization p-value as a universal exact test.
3. **H2 robustness is decisive for wording.** The observed pooled rho (0.18873) is positive, but the within-HS2 rho (−0.00959) and p (0.843) do not support a robust within-sector relationship. Never argue that nominal MFN tariffs caused Bangladesh's 2025 market shares.
4. **H3 is not price or productivity estimation.** Unit values are CIF-side EUR/kg proxies, not homogeneous goods' factory prices. Pakistan (**96/198**) is an explicit exception; BH independence/dependence requirements are not verified for national inference.
5. **Tariff scenario numbers are conditional duty equivalents.** 2025 EU-reported import value is paired with 2026 legal rate *candidates*; missing product rates, rules of origin and preference take-up remain unresolved. A future Bangladesh GSP/GSP+ entitlement or 2032 duty is not established.
6. **Article 33 requires legal status.** The 37% denominator is relevant GSP-beneficiary imports; 6% denominator is all relevant Union imports. The 2027 GSP-beneficiary roster is projected backward to 2023–2025. The mechanism exempts EBA and requires a Commission implementing act.
7. **Cross-year product growth remains restricted.** The 2012–2025 CN8 product correspondence is not independently certified; historical HS2 Chapter 61–63 context must not be treated as a verified CN8 growth panel.
8. **Source level versus verification level:** the exact mathematics and recorded code-run outcomes have passed reproducibility checks. Tariff legal conditions, origin proof and future behaviour require different evidence and are not validated by numeric QA.

## Binding standard for defending each finding

Use the sequence **Claim → original observation/legal source → unit and denominator → formula → numeric substitution → independent check → sensitivity/counterexample → justified conclusion → limitation**.

| Research question | Reproducible positive evidence | Maximum defensible conclusion |
|---|---|---|
| RQ1 | Top-200 imports **€20.789bn**; basket HHI **442.13** | Observed 2025 top-200 position, not full national productivity or causal competitiveness |
| RQ2 | Sign tests: majority lower EUR/kg versus five of six selected origins | Descriptive unit-value direction; **not** lower quality-adjusted costs or superiority over Pakistan |
| RQ3 | H1 gap **3.9394 pp**; pooled H2 rho **0.1887** but within-HS2 rho **−0.0096** | Tariff-schedule sector heterogeneity exists in cohort; no robust within-sector market-share association identified |
| RQ4 | Static MFN-versus-EBA candidate reference **€2.443bn** on 196 lines | Value of hypothetical nominal rate gap on unchanged 2025 import values; **not** export loss |
| RQ5 | 2025 backcast **48.7099%** GSP-roster share and **18.3717%** all-import share | Numerical historical screen only; EBA excluded and no future implementing act inferred |

**Audit outcome:** All checked numbers and formula applications were consistent. Methodological interpretation was strengthened in Section 4.3 to state the distinction between the H1 directional hypothesis and the exchangeability assumption. No p-value has been converted into causal evidence or any static scenario value into export revenue losses.

**Original methodological references:** Athey and Imbens (2017), Benjamini and Hochberg (1995), Benjamini and Yekutieli (2001), Efron and Tibshirani (1993), Phipson and Smyth (2010), Spearman (1904). **Official sources:** Eurostat international-trade-in-goods detailed metadata; Regulation (EU) 2026/1395, Art. 33 and Annex IV.

**Outstanding source/legal verification:** 4 unresolved MFN products, 17 unresolved comparator candidates, 14 unavailable matched-unit-value ratios, transaction-level preference use, official historical CN8 concordances, operative-year GSP beneficiary rosters and future EU regulatory changes. Supervisor approval is pending.
