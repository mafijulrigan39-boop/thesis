# Task G — pre-writing quality-assurance release, 21 November 2026

STATUS: PRELIMINARY ANALYTICAL FREEZE ONLY — SUPERVISOR APPROVAL PENDING.

Frozen source snapshot: acda0fd118b6ec019c5b37e34d07dc76e28fb878.

Included executable: task_g/run_task_g.py (pure Python standard library); on push, workflow .github/workflows/task_g_qa.yml verifies the 11 SHA-256 fingerprints published in Task F, reconciles the 200 product-year rows and 1200 competitor comparisons, runs exploratory H1-H3 tests, documents alternative years, competitor groups, classification exclusions, and tariff scenarios. It exports CSV and JSON via GitHub Actions artifact TaskG-Executed-QA-Tables.

2025 principal cohort is intentionally limited to top-200 Bangladesh CN8 products; trade reporter EU27_2020, flow EU import, source DS-045409; tariff benchmark 2026-11-01 DG TAXUD TARIC; static duty amounts, not export losses. Historical official Chapter 61–63 changes are descriptive. Historical CN8 code-level growth is UNCERTIFIED because original annual concordance sources are missing. 2027 GSP beneficiary roster projected backwards onto 2023–25 Article 33 imports is counterfactual and never a legal determination. EBA exception currently applies.

H1 (post-hoc exploratory): mean source-dated 2026 MFN tariff candidate rate on HS2 61–63 > that on other selected codes, one-sided permutation.
H2 (post-hoc exploratory): 2025 product market share and 2026 MFN rate have a nonzero Spearman rho, two-sided permutation.
H3 (post-hoc exploratory): Bangladesh 2025 EUR/kg lower than each comparator CN, IN, VN, PK, KH and TR for more than half of valid matched products, one-sided exact sign tests with BH adjustment for six origins.
H4: Article 33 numeric thresholds; arithmetic checks only.
H5: static tariff equivalent identity; arithmetic checks only.

NOT preregistered; no causal or population-inferential claims from the purposively selected 200 codes. Supervisor should approve statistical expectations and writing scope before final thesis findings.

Other files in this folder: HYPOTHESES.md, BIBLIOGRAPHY_AUDIT.md, SOURCE_AND_MISSING_DATA.md, SUPERVISOR_APPROVAL_FORM.md.

### Alternate-year raw-code observations

The independently verified source table has a 200-row *design grid* for each year, not 200 real observations. The validation runner additionally exports YEAR_BY_YEAR_MISSINGNESS.csv: 2012 valid 187, missing Bangladesh values 3, missing extraEU totals 10; 2023 valid 200; 2024 valid 199 and missing Bangladesh value 1; 2025 native valid 200. The 2012–2024 CN8 meanings are **not source-harmonized** and cannot justify product-growth trends. This is coverage robustness only.
