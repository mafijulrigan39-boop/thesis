# Task G: measurable hypotheses and testing plan

Date: 2026-11-21. Classification: **EXPLORATORY, PROPOSED, NOT SUPERVISOR APPROVED**. These hypotheses were established after examination of Task F, not preregistered. A top-200 value-selected CN8 cohort is not a random sample of Bangladesh products; p-values describe exchangeability assumptions and must not be projected onto a national product population.

| Test | Exact measurable estimand | H0 / H1 | Method | N and unit |
|---|---|---|---|---|
| H1 | Difference of arithmetic mean 2026 MFN rate candidates for selected 2025 CN8 lines in HS2 61–63 minus other selected lines | H0 gap <=0 / H1 gap >0 | Product-label permutation one-sided, 9,999 reshuffles, seed 20261121; 1,999-resample separate-group bootstrap 95% descriptive interval | 152 apparel and 44 other numeric-rate 2025 CN8 products |
| H2 | Spearman rank rho between Bangladesh 2025 EU import-market share and 2026 MFN tariff candidate in matched product lines | H0 rho =0 / H1 rho !=0 | Tied midranks; 9,999 random-permutation two-sided p-value, seed 20261122 | 196 rated 2025 CN8 products |
| H3-CN/IN/VN/PK/KH/TR | Proportion of valid same-CN8/year BD EUR/kg ratios less than 1 compared with each origin | H0 proportion <=0.5 / H1 >0.5 | Exact one-sided paired sign/binomial test, exclude ratio=1 ties; Benjamini-Hochberg over six origin tests | 200,200,198,198,190,200 valid ratio pairs, subject to ties |
| H4 — deterministic | For each 2023–2025 year, 100 x BD 61–63 EU imports / 2027-roster GSP countries 61–63 imports | Compare 37% Annex IV trigger and 6% Article33(2) exception separately | Arithmetic, no significance test; 2027 beneficiary roster is backcast | 3 annual HS2 aggregate observations |
| H5 — deterministic | Static duty equivalent sum of observed 2025 BD value x source-dated 2026 rate difference /100 | Product-line reconciliation to EUR 0.01 and sample-value coverage | Exact reproducibility identity, not a hypothesis of trade effects | 200 product lines, 196 qualified |

H1 and H2 are related and exploratory. If the supervisor wants formal confirmatory inference, define a truly held-out period or new independent dataset first; do not relabel these post-hoc findings as preregistered. H3 six related origin tests use BH FDR correction, but product/partner dependence and purposive top-200 sample require interpretation caution.

**Additional descriptive sensitivity axes:** alternate 2023/24/25 annual Chapter 61–63 shares; six rival countries and two tariff candidate groups China+India versus Viet Nam+Pakistan+Cambodia+Türkiye; 2025 1:1 exact versus nonexact classifications (not a certified historical concordance); top10/50/100/200 baskets; alternative source-date benchmark tariffs (MFN, India 2026 proxy, Pakistan 2026 proxy, Article 7 illustrative 20% relative reduction for Section 11b, hypothetical Article33 MFN). Rate coverage differs by scenario. Stress four unknown MFN lines at 0/5/10/15/20 percentage points, explicitly NOT imputing verified rates.

**No causal identification:** Bangladesh has not exited EBA in these observations. Scenario value x rate assumes fixed 2025 imports and says nothing about foreign tariff incidence, elasticities, consumer demand, exporter profits, export losses or welfare. EUR/kg proxy differs from transaction prices and quality. Higher market share versus higher tariff candidates is association, not tariff effect.

The public DU MITB 2023–24 curriculum confirms a 3-credit Project Paper and Viva Voce and courses in statistics/research methods; it does not set any explicit compulsory t-test/regression hypothesis rubric. Obtain supervisor-specific instructions on tests, citation style and project format before claiming academic approval.

Curriculum: https://ssl.du.ac.bd/fontView/images/syllabus/1761544555LastUpdatedMITBSyllebus%282023-2024%29.pdf

**Added post-hoc H2 robustness:** Within-HS2 categorical partial-rank correlation (demean pooled midranks within each HS2 chapter), 9,999 two-sided within-chapter permutations; report separately from pooled H2 and do not treat the unadjusted positive association as robust if this result is null. This sensitivity is additionally post-hoc and was added only after inspecting H2.
