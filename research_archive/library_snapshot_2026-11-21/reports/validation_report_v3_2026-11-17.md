# Bangladesh–EU market-access validation: v3 execution report

**Run date:** 17 November 2026  
**Library project:** `/Thesis Research/Bangladesh EU Market Access Validation/Integrated Research Pack`  
**Execution status:** incomplete — no new empirical trade or tariff observations retrieved.

## 1. Archive inspected

Reviewed the original integrated workbook, integrated research/validation report, audit memo, README and v1 script. The original archive explicitly states that the full 2012–2025 Comext panel, complete competitor panel, full Chapter 61–63 denominator, year-specific nomenclature concordance and tariff-line extraction were not complete. The earlier pipeline was a prepared script, not completed data collection.

## 2. Execution performed in this run

- Created `run_full_validation_v3.py` as a versioned correction to the v2 pipeline.
- Python syntax compilation passed.
- Ran a one-year 2024 Comext smoke test with `--skip-wits`; the first filtered request failed after five attempts because the container could not resolve `ec.europa.eu`.
- Exact request, DNS error and partial run manifest were saved. No Comext raw response was received.
- WITS and TARIC raw files were not downloaded.
- No top-product ranking, competitor matrix, market shares, unit values, HHI, Article 33 ratio or tariff preference margin has been newly calculated.

### Exact failed request

```text
https://ec.europa.eu/eurostat/api/comext/dissemination/statistics/1.0/data/DS-045409?format=JSON&lang=en&freq=A&reporter=EU27_2020&flow=1&indicators=VALUE_IN_EUROS&sinceTimePeriod=2024&untilTimePeriod=2024&partner=BD
```

Error: `NameResolutionError: Failed to resolve 'ec.europa.eu' ([Errno -3] Temporary failure in name resolution)` after five retries. This is an execution-environment failure, not evidence that the official endpoint lacks data.

## 3. Pipeline corrections

The v3 pipeline now:
- keeps year-specific CN8 codes and builds annual top-N rankings;
- queries competitors and extra-EU totals using each year's selected codes, rather than carrying 2025 CN8 codes backward;
- blocks period rankings and YoY growth until a complete official concordance is supplied;
- creates an all-code × year missingness audit and does not recode absent cells to zero;
- saves successful raw Comext JSON and a partial manifest/request failure log if a query fails;
- requires a year-level completeness attestation and complete Chapter 61–63 coverage for every mapped GSP beneficiary before calculating Article 33 shares;
- labels 2012–2025 Article 33 values as retrospective simulations, not legal application before 2027.

## 4. Checklist status

| Checklist item | Status | Coverage / result |
|---|---|---|
| Bangladesh EU imports, 2012–2025 CN8 | **Not complete** | Requested 2012–2025; 0 new years downloaded |
| At least five competitors for same products | **Not complete** | Year-specific query logic prepared; 0 competitor observations downloaded |
| Top 100–200 Bangladesh product lines | **Not complete** | Annual 100–200 ranking logic prepared; 0 new ranked lines |
| Values, quantities and unit values | **Not complete** | Net-mass query and EUR/kg logic prepared; no new observations |
| EU market shares and concentration | **Partial (existing screen only)** | 2024 HS61+62 sample retained; no full-basket new calculation |
| Missingness and classification audit | **Partial (framework only)** | v3 audit output prepared; official code lists/concordance not downloaded |
| EU MFN and Bangladesh/competitor preferential tariff matrix | **Not complete** | TARIC template and WITS extraction route; 0 tariff records downloaded |
| Effective dates, scheme eligibility and rules of origin | **Partial (legal framework only)** | Legal sources identified; product-specific mapping incomplete |
| Article 33 37% beneficiary denominator | **Not complete** | Correct denominator logic and coverage gate prepared; no trade or historical beneficiary map to calculate |
| Article 33 6% all-origin denominator | **Not complete** | Separate all-origin Chapter 61–63 query prepared; no data |

## 5. Existing evidence retained (not newly downloaded)

The prior 2024 WITS/UN Comtrade screening values remain: EU imports in HS 61+62 of US$92.570bn; Bangladesh-origin imports US$19.785bn; Bangladesh share 21.37%. Ten selected HS6 lines represented about 60.34% of Bangladesh's recorded HS61+62 value in that screen. The selected-ten-line HHI of 1,677.8 is not the full-basket HHI. These are preliminary screening figures, not a validated 2012–2025 panel.

## 6. Article 33 legal denominator and interpretation

Regulation (EU) 2026/1395 Article 33(1)(b) compares a beneficiary country's value of S-11b imports with the value of S-11b imports from **all GSP beneficiary countries**. Annex III defines S-11b as Chapters 61, 62 and 63; Annex IV point 3 sets 37%. Article 33(2) separately exempts EBA beneficiaries from preference removal and countries with a share no more than 6% of total Union imports of the same products. These are different denominators. The 6% test requires a separate all-origin total. The new regulation applies from 1 January 2027; ratios calculated for 2012–2025 would be retrospective simulations, not historical legal decisions under Article 33.

The 2027 Annex I seed has 64 country rows (46 marked EBA and 18 marked Standard GSP in the seed file). It is not a historical beneficiary mapping, and its footnotes/temporary withdrawals require product-scope review. Do not backcast it.

## 7. Tariff source routes and blockers

- **Comext:** Official dataset and dedicated API documentation verified. The raw API request failed at DNS. Bulk fallback should start by fetching the live inventory for `comext/COMEXT_DATA/PRODUCTS`; select filenames from the returned inventory, not guessed names.
- **TARIC:** Commission portal confirms TARIC contains third-country duties, preferences, quotas, nomenclature and additional codes; raw data are offered in Excel. The portal's current raw-data link returned 404 at its CIRCABC destination in this web retrieval session. Reopen the portal for the current link.
- **Access2Markets:** Product/origin-specific tariff and rules-of-origin cross-check is available, but is interactive rather than a bulk historical tariff dataset.
- **WITS TRAINS:** HS6 historical tariff cross-check; verify year coverage, partner groups, excluded countries and non-ad-valorem lines. No raw response downloaded.
- **Preference utilisation:** no complete product-level utilisation dataset retrieved; eligibility must not be treated as utilisation.

## 8. Artifacts created

- `run_full_validation_v3.py`
- `README_full_validation_pipeline_v3.md`
- `gsp_beneficiary_status_template.csv`
- `gsp_beneficiary_mapping_coverage_template.csv`
- `cn8_year_to_stable_product_concordance_template.csv`
- `cn8_nomenclature_year_template.csv`
- `taric_tariff_matrix_template.csv`
- `tariff_source_coverage_template.csv`
- `data_dictionary_v3.csv`
- `source_log_v3.csv`
- `access_test_results_2026-11-17_v3.csv`
- `raw_extract_inventory_status_v3.csv`
- `smoke_run_2024_v3/run_manifest_partial.json`
- `smoke_run_2024_v3/raw_api/request_failures.jsonl`

## 9. Next action

Run v3 or the Comext bulk fallback from an internet-enabled machine. Preserve raw extracts and run manifest. Then obtain year-specific Combined Nomenclature code lists and official correspondence tables, complete the GSP beneficiary map with a legal coverage attestation, and download/parse TARIC raw Excel. Do not finalise the thesis title or claim causal effects until the product panel, tariff exposure and identification strategy are validated.