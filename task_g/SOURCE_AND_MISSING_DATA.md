# Task G: final source and missing-data register (pre-supervisor approval)

| Record type | Actual provenance | Verification & limitation |
|---|---|---|
| 2025 Bangladesh top200 products | Eurostat DS-045409 via GitHub Task C (main EU27_2020 reporter/imports) | 200 2025 CN8 lines; EUR 20,789,281,101; source-year code validity does not establish historical concordance |
| Country and all-partner comparator panel | Task C full 2012–2025 all-partner official downloads, six origins and published extraEU denominators | Named country total may not equal officially published extraEU aggregate; allocation residual retained |
| Product market shares | 200 2025 products, Task F product_2025_value_share_price_tariff_exposure.csv | 2025 source shares; no causal effect or forecast |
| Net mass and unit values | Task D full data and source receipts | 1186/1200 valid EUR/kg paired comparisons; no equal-quality assumption |
| Tariff 2026-11-01 | DG TAXUD TARIC original official workbooks and dated conditions, Task E nov2026_taric | 196/200 numeric MFN; 4 missing rates; 1183/1200 competitor candidate rates; not future BD payable duty |
| Classification and missingness | Task B 2025 derived flags, DS059322 observed/absent register | 20 nonexact/complex 2025 codes; 14 source year-specific original CN nomenclatures and 13 predecessor-successor concordance tables are unavailable; *no certified CN8-level 2012–2025 growth* |
| Article33 S11b | Task F 14 annual HS2 (61–63) raw official responses; 2027 GSP Annex I roster | 2023,24,25 annual shares using 2027 roster backcast are scenario screens; 37% test uses GSP beneficiary denominator; 6% exemption uses all extra-EU imports; current EBA exemption applies |
| Legal source | Regulation (EU) 2026/1395 Art33 and Annex IV | Threshold alone does not trigger a duty rate; Commission implementing act and change of EBA status are separate conditions |
| Academic guideline | DU MITB curriculum 2023–24 | Project paper & viva 3 credits confirmed; no rubric proving any particular statistical test is compulsory |
| Reproducibility | Task F JSON has 11 source SHA256 fingerprints, rechecked by Task G workflow | Failed SHA mismatch must block release; source freeze anchored to commit in README |

## Missingness and constraints

1. MFN rates absent for CN8 24012085 (EUR 68,239,963), 24012035 (EUR 46,706,933), 19023010 (EUR 8,938,828), 39269097 (EUR 7,197,513), totalling **EUR 131,083,237**. No tariff filled; 0/5/10/15/20 percentage-point cases are explicitly **hypothetical stress inputs**, not empirical estimates.
2. 14/1200 competing-origin EUR/kg ratios unavailable or invalid due to unmatched quantities; exclude, never treat as parity or zero.
3. 17/1200 source-dated competitor tariff candidates not numerically comparable; rates remain missing rather than falling back silently.
4. 163/200 products have country supplier residual >0.1% of reported extraEU; their origin-country HHI remains qualified.
5. Full historical 2012–2025 source-authenticated CN8 code harmonization blocked by 27 missing source files; 2025 cross-sectional selection and 2012–2025 Chapter61–63 aggregated descriptive trends remain admissible.
6. Future Bangladesh Standard GSP or GSP+ eligibility, legal RoO, actual proof/usage, quota and future TARIC effective dates remain uncertified.
7. Article33 2027 Annex I GSP roster applied to 2023–2025 historic trade must never be mislabeled the actually operative yearly beneficiary roster; the 37% numerical calculation does not by itself impose the safeguard while Bangladesh is EBA.
8. Supervisor scope and official formatting instructions remain unapproved. Do not publish Task G as fully complete before approval.

Never label unreported observations as VERIFIED_ZERO; never silently substitute tariff zero for missing. Frozen 2025 top200 cross-section is a release candidate, not a frozen full CN8 longitudinal panel.
