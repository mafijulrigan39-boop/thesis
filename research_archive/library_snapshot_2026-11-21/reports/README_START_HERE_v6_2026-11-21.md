# Bangladesh–EU CN8 market-access research: verified-process package v6

**Prepared:** 21 November 2026  
**Library target:** `/Thesis Research/Bangladesh EU Market Access Validation/Integrated Research Pack`  
**Study:** *Bangladesh's Prospective EU Market-Access Exposure Following LDC Graduation: A Product-Level Assessment of Tariff Preference Erosion and Export Competitiveness.*

## Explicit status — read before interpreting results

**This is an executed validation/analysis toolchain and drafted manuscript; it is not a completed empirical dataset.** The principal source CSV reportedly extracted in Codex (27,780 CN8 observations) is **not present** in the current runtime. There are **zero independently downloaded CN8 source records, zero matching competitor values, and zero verified tariff-line rates** in this v6 package. The only trade values are **annual sums copied from the Codex report in this conversation and explicitly labelled as user reported**. Do not rebrand those sums as an original Eurostat download.

The environment attempted official Eurostat Comext, UN Comtrade, and the Commission TARIC host. All three failed at DNS resolution before HTTP; saved exceptions are in `logs/official_source_network_probe_v6.json`. Documentation was independently verified through web research, not raw dataset acquisition.

## Included deliverables

- `bangladesh_eu_mitb_thesis_pre_empirical_v6.docx` — 13-page Word working draft of research foundations, literature, methodology, and an explicitly incomplete empirical-results section; **not a submission-ready completed thesis**.
- `docs/bangladesh_eu_thesis_manuscript_v6_DRAFT.md` — editable source text for the thesis.
- `bd_eu_trade_research_audit_workbook_v6.xlsx` — professionally formatted Excel workbook with summary, formula-based annual reconciliations, DG Trade vintage caveat, legal chronology, task register, origin-policy matrix, sources, data dictionary, and restrictions.
- `data/input/codex_reported_annual_totals_2012_2025.csv` — all 14 annual figures supplied by the user, with computed discrepancy percentages. Not raw CN8 data.
- `data/input/dg_trade_crosscheck_provisional.csv` — 2022–2025 previously reported Commission aggregate comparison; **vintage/definition not yet verified**.
- `docs/checklist_v6.csv` — 27 auditable work items, statuses and blockers.
- `docs/source_register_v6.csv` — original source URLs, source types and which data were not downloaded.
- `docs/competitor_legal_regimes_v6.csv` — official country-level EU tariff-arrangement context, **no tariff-rate observations**.
- `docs/data_dictionary_v6.csv` — data definitions and gates.
- `code/audit_and_analyze_v6.py` — executed against *clearly synthetic test fixtures only*. When actual Comext exports are added, the program validates CN8 and produces annual top-200, annual product HHI, missingness, conditional competitor shares and unit values, source-backed harmonised period rankings, verified-rate exposure, and Article 33 calculations only under stated coverage requirements.
- `code/run_full_validation_v3_reference.py` and `code/eurostat_comext_bd_cn8_verified_v4.py` — archived previously prepared network acquisition tools, **not run successfully to download official trade rows in this environment**. The v4 network script's strict reconciliation threshold is unsuitable for a published confidential-detail residual; prefer the v6 offline audit for interpreting gaps.
- `code/probe_official_sources_v6.py`, `logs/official_source_network_probe_v6.json` — executed network evidence.
- `tests/test_v6.py` — executed isolated synthetic fixtures, proving leading-zero handling, duplicate rejection, annual totals, origin comparisons, and EUR/kg logic. Synthetic data are not included as research observations.
- `data/input/*EMPTY_TEMPLATE.csv` — empty source requirements, not fabricated tariff or partner data.

## How to complete stages with real data

**Step 1: Bangladesh CN8.** Copy the original Codex file `eu_imports_bangladesh_cn8_2012_2025.csv` into a real source directory. Preserve the original byte stream and metadata: the Codex export command/selection, statistical procedure T, retrieval timestamp, source URL/portal, reporter, flow, partner, indicator, and as-extracted headings. Do not use the annual-summary CSV in place of the raw CN8 source.

Run offline validation:

```bash
python code/audit_and_analyze_v6.py \
  --bd path/to/eu_imports_bangladesh_cn8_2012_2025.csv \
  --out path/to/analysis_output
```

Expected outputs include `bd_cn8_clean.csv`, `bd_cn8_reconciliation.csv`, `bd_cn8_row_errors.csv`, `bd_excluded_aggregate_rows.csv`, `top200_by_year_raw_cn8.csv`, `annual_portfolio_hhi_disclosed.csv`, `cn8_year_observation_missingness_audit.csv` and `run_manifest.json`. A missing original TOTAL within the source file is explicitly flagged; do not silently match to an unproven summary figure.

**Step 2: Competitors.** Download the same product-year EU27_2020 import observations for China, India, Viet Nam, Pakistan, Cambodia, Türkiye **and all relevant origin suppliers**. Include the explicit `EXT_EU27_2020` product-year extra-EU aggregate as the market-share denominator. The comma-separated file must contain `year`, `product`, `origin`, and `value_eur` (or Eurostat aliases `TIME_PERIOD`, `PRODUCT`, `PARTNER`, `OBS_VALUE`). Additional `net_mass_kg` or `quantity_100kg`, `supp_quantity`, and `supp_unit` are optional but must be observed, not guessed. A sample set of only six peers cannot establish the global top five suppliers.

**Step 3: Classification and quantities.** Obtain official 2012–2025 CN nomenclature definitions and correspondence tables (EU Vocabularies/ShowVoc/CIRCABC); provide high-confidence stable mappings `year,product,stable_product_id,quality,concordance_source`. Do not call an unchanged HS6 prefix a full CN8 concordance. Join official quantity observations on exact partner, product, year, unit and procedure.

**Step 4: Tariffs.** Extract official TARIC/Access2Markets origin-specific duty measures for exact product/tariff-line and effective date. Populate `product,origin,scenario,effective_from,effective_to,ad_valorem_pct,source_url,verified` along with TARIC10, specific duty, quotas, legal basis and origin rules. The v6 exposure code deliberately rejects unverified, compound, quota or ambiguous TARIC10 rates. It requires source-backed EBA at the 2025 baseline and prospective rates valid at the specified hypothetical scenario date; this is an analytic assumption, **not a confirmed end-of-EBA date**.

**Step 5: Article 33.** Supply all Chapters 61, 62 and 63 origin/year import values, the full contemporaneous GSP beneficiary map with complete-coverage attestation, and the independent all-origin Chapter 61–63 denominator. The 37% test uses **all GSP beneficiaries**; the separate 6% test uses **all origins**; while EBA applies, a beneficiary is exempt from this preference withdrawal mechanism. Historical retrospective screens are not legally operative determinations.

Run with additional inputs only after they are populated:

```bash
python code/audit_and_analyze_v6.py \
  --bd path/to/actual_bd_cn8.csv \
  --competitors path/to/actual_competitors_and_extraEU.csv \
  --concordance path/to/official_cn8_concordance.csv \
  --tariffs path/to/verified_tariff_matrix.csv \
  --s11b-chapters path/to/actual_chapter_origin_trade.csv \
  --gsp-status path/to/verified_beneficiary_map.csv \
  --s11b-all-origins path/to/actual_all_origin_chapters.csv \
  --scenario-date 2033-01-01 \
  --out path/to/analysis_output
```

Before citing a generated result, check `run_manifest.json` for relevant stage coverage, input SHA-256 and warning flags. Prospective 2033 is an **illustrative evaluation date**, not a Commission-confirmed transition expiry.

**Step 6: Thesis manuscript.** Insert the real validated product tables/charts and scenario results into the draft Word document. Apply supervisor's requested University of Dhaka formatting, reference style and chapter boundaries. Write the findings and recommendations only after source-verified analysis; supervisor sign-off is outside the assistant's control.

## Reproducibility checks executed

- `python -m py_compile code/audit_and_analyze_v6.py` — passed.
- `python tests/test_v6.py` — passed, synthetic fixtures only.
- `python code/probe_official_sources_v6.py` — completed; 3 official hosts returned DNS errors before HTTP.
- `bd_eu_trade_research_audit_workbook_v6.xlsx` — created and inspected: formula-calculated €61,039,072 gap and 0.0286108%; no formula errors detected.
- Word draft — rendered and visually inspected at first and last pages.

## Non-negotiable interpretation

Without actual CN8 source rows, tariff-line observations and matching origins, any full top-200 list, product-level exposure, partner HHI, preference margin, unit-value table, or Article 33 ratio presented as observed empirical results would be fabricated. This package purposely does not do that.