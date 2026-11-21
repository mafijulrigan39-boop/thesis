# Bangladesh–EU Market Access Validation Pipeline v3

Evidence date: 17 November 2026. This is a versioned improvement to the archived v1 and v2 pipelines. It has been syntax-checked and smoke-tested for one Comext request. The live request failed before an HTTP response because the execution environment could not resolve `ec.europa.eu`. **No new trade or tariff observations were downloaded.**

## What v3 corrects

1. **Year-specific product identity.** CN8 strings are not pooled across years. Annual top-N rankings are built using each year's CN8 records. Competitor and extra-EU denominator requests use that same year's selected CN8 codes.
2. **Concordance gate.** Period rankings and year-on-year growth are produced only when every observed CN8-year key has an exact/high-quality, sourced stable-product mapping. A blank concordance template is generated; otherwise the script writes a not-calculated status.
3. **Full missingness audit.** A code-by-year panel is produced for the union of observed CN8 codes. A not-returned cell is explicitly not interpreted as zero; official annual CN code lists are still needed to distinguish true zero trade from code changes or missing coverage.
4. **Raw API retention.** Successful Comext JSON responses are saved under `raw_api/`; failed requests are written to `raw_api/request_failures.jsonl` and a partial run manifest is written.
5. **Article 33 denominator guard.** The 37% ratio is not calculated unless the user supplies a legally reviewed, year-specific beneficiary map, an explicit year-level completeness attestation, and complete Chapter 61, 62 and 63 coverage for every mapped beneficiary. The separate 6% ratio requires all-origin extra-EU totals for all three chapters.
6. **Historical legal interpretation.** 2012–2025 shares are labelled retrospective simulations under Regulation (EU) 2026/1395, not legal application of Article 33 before the new regime applies from 1 January 2027.
7. **Unit values.** Net mass in 100-kg units is converted to kg; EUR/kg is calculated only when both value and positive net mass are reported.

## Execute on an internet-enabled Python machine

Python 3.10+ and `requests` are required.

```bash
python -m pip install requests
python run_full_validation_v3.py --start 2012 --end 2025 --topn 200 --out bangladesh_eu_full_validation_v3
```

If WITS TRAINS is unavailable, use `--skip-wits`:

```bash
python run_full_validation_v3.py --start 2012 --end 2025 --topn 200 --skip-wits --out bangladesh_eu_full_validation_v3
```

Do not run multiple copies concurrently. Comext calls are sequential. The 2012–2025 extraction is substantial: it queries Bangladesh's full CN8 universe and then selected same-year products from all partners, quantities, extra-EU totals and the full Chapter 61–63 origin panel.

## Primary trade source: Eurostat Comext DS-045409

Dataset: https://ec.europa.eu/eurostat/databrowser/view/DS-045409

Official Comext API base: `https://ec.europa.eu/eurostat/api/comext/dissemination`

Filtered annual request example (single year, Bangladesh, value):

```text
https://ec.europa.eu/eurostat/api/comext/dissemination/statistics/1.0/data/DS-045409?format=JSON&lang=en&freq=A&reporter=EU27_2020&flow=1&partner=BD&indicators=VALUE_IN_EUROS&sinceTimePeriod=2024&untilTimePeriod=2024
```

Net mass indicator: `QUANTITY_IN_100KG`. The Comext endpoint requires filtered requests; full dataset downloads are disabled on this API due to size.

### Bulk-download fallback (do not guess filenames)

Official bulk download documentation: https://ec.europa.eu/eurostat/en/web/user-guides/data-browser/download-data/bulk-download

Official file API inventory listing for the Comext product directory (retrieve this inventory first in an internet-enabled browser/script):

```text
https://ec.europa.eu/eurostat/api/dissemination/files?format=csv&dir=comext/COMEXT_DATA/PRODUCTS&hierarchy=false&sizeFormat=READABLE&dateFormat=READABLE
```

The official migration guide documents the file API pattern `https://ec.europa.eu/eurostat/api/dissemination/files?file=<relative-path>` and gives `comext/COMEXT_DATA/PRODUCTS/full202305.7z` as an example. Select the actual annual/monthly file names from the live inventory for the years needed. Do **not** rely on the earlier guessed `full_v2_202512.7z` name unless it appears in the current inventory.

Comext documentation: https://ec.europa.eu/eurostat/en/web/user-guides/data-browser/api-data-access/api-getting-started/comext-database

## Competitor panel and market shares

For each year, the script selects up to 200 CN8 products by Bangladesh import value across all sectors and up to 200 additional S-11b CN8 lines (Chapters 61–63). It queries all partner origins for those year-specific codes. The top-five suppliers are ranked from observed non-EU country partners, excluding Bangladesh. Bangladesh market share uses the matching `EXT_EU27_2020` extra-EU total for the same CN8-year. Missing partner observations remain missing.

This selection is a screening panel, not an all-products competitor panel. The top 100–200 Bangladesh lines are reported for the latest observed year; annual rankings preserve year-specific CN8 codes.

## Nomenclature and period rankings

The pipeline creates:
- `cn8_year_observation_classification_audit.csv`
- `cn8_nomenclature_year_template.csv`
- `cn8_year_to_stable_product_concordance_template.csv`

Fill the concordance with official annual CN/HS correspondence tables and a stable product identifier. Only `exact` or `high` mappings with a source are accepted for period ranking/growth. HS6 prefix extraction is not a formal concordance. If the mapping is incomplete, period ranking and growth are deliberately not calculated.

## Article 33 / Section S-11b denominator

Regulation (EU) 2026/1395: https://eur-lex.europa.eu/eli/reg/2026/1395/oj/eng

- Article 33(1)(b) uses the share of a beneficiary country's S-11b imports relative to imports of S-11b from **all GSP beneficiary countries** during the calendar year.
- Annex III defines S-11b as Chapters 61, 62 and 63.
- Annex IV point 3 sets the threshold at 37%.
- Article 33(2) excludes EBA beneficiaries from the preference-removal mechanism and separately exempts a country whose share of the same products is no more than 6% of total Union imports.
- The 6% denominator is a separate all-origin total. It is not the 37% beneficiary-country denominator.

The pipeline does not infer GSP status from trade data. Fill `gsp_beneficiary_status_template.csv` and `gsp_beneficiary_mapping_coverage_template.csv` from the legally effective Annex I/II and relevant Commission acts for each year. The coverage file must explicitly attest `mapping_complete=true`, include the expected beneficiary count, a legal source URL and a reviewer attestation. The script also requires complete reported Chapter 61–63 values for every mapped beneficiary; absent chapter observations are not silently zero-filled.

The 2027 Annex I seed is a one-date legal starting point only. It must not be backcast to 2012–2026. Because Regulation (EU) 2026/1395 applies from 1 January 2027, any 2012–2025 calculation is a retrospective exposure simulation, not a legal determination under Article 33 for those earlier years. EBA status, temporary withdrawals and product-specific scope must be reviewed separately.

## Tariffs and rules of origin

### TARIC (exact current EU CN8/CN10 measures)

Official TARIC portal: https://taxation-customs.ec.europa.eu/online-services/online-services-and-databases-customs/eu-customs-tariff-taric_en

The Commission states TARIC raw data are freely available in Excel. The current raw-data link is exposed from the portal; in this session its CIRCABC route returned HTTP 404 through the web retrieval path. Reopen the portal and use its current “TARIC raw data” link rather than relying on the stale CIRCABC URL.

Preserve every measure separately: third-country/MFN duty, preferential measure, tariff quota, additional code, origin/geographical-area scope, legal base, effective-from/to dates, and duty expression. Keep ad valorem, specific, compound, agricultural component and quota measures in separate fields. Do not convert specific/compound rates to ad valorem without a defensible AVE.

TARIC extraction explanations (Commission, 9 June 2026): https://circabc.europa.eu/sd/d/3d892b27-176f-4b8c-bbf5-4e0ee63f7e5a/Explanation%20for%20the%20Taric%20database%20extractions.pdf

### Access2Markets / ROSA

My Trade Assistant: https://trade.ec.europa.eu/access-to-markets/en/my-trade-assistant

Use it for product-specific applied/preferential duty, formalities and rules-of-origin cross-checks. It is interactive and should not be treated as a bulk historical tariff API. Record product code, origin, destination, retrieval date and source data for each check.

### WITS / UNCTAD TRAINS

API docs: https://wits.worldbank.org/witsapiintro.aspx
API guide: https://wits.worldbank.org/data/public/WITSAPI_UserGuide.pdf
TRAINS tariff measures and preference beneficiaries: https://wits.worldbank.org/wits/wits/WITSHELP/content/Utilities/D3.Using_TRAINS_Tariff_Measures.htm

WITS is an HS6-level historical cross-check. Inspect tariff type, year, HS nomenclature, partner-group membership, excluded origins and non-ad-valorem line counts. Do not treat a missing country-specific PREF row as proof that no preference exists. Do not claim 2024–2025 tariff coverage unless the API availability table confirms it.

### Rules of origin and utilisation

For each product/year/origin, distinguish:
1. country scheme eligibility;
2. product's preferential measure and rate;
3. product-specific origin rule and cumulation conditions;
4. shipment's actual originating status and documentary compliance;
5. actual preference utilisation.

Eligibility does not prove that the preference was claimed or used. A complete product-level utilisation dataset has not been retrieved.

## Output inventory

- `bd_eu_imports_all_cn8_annual.csv`
- `bd_eu_imports_all_cn8_quantity_annual.csv`
- `top_products_annual_cn8_year_specific.csv`
- `top_products_latest_all_sectors.csv`
- `top_products_latest_S11b_ch61_63.csv`
- `top_products_period_harmonised.csv` only if concordance is complete
- `product_growth_harmonised.csv` only if concordance is complete
- `cn8_year_observation_classification_audit.csv`
- `bd_selected_products_year_specific_panel.csv`
- `eu_selected_products_all_partners_annual.csv`
- `eu_selected_products_all_partners_quantity_annual.csv`
- `eu_selected_products_all_partners_annual_with_unit_values.csv`
- `eu_selected_products_extraEU_totals_annual.csv`
- `top5_competitors_by_product_year.csv`
- `market_share_by_product_year.csv`
- `s11b_chapters_61_63_by_partner_annual.csv`
- `s11b_partner_chapter_coverage.csv`
- `s11b_partner_totals_annual.csv`
- `s11b_all_origin_extraEU_totals_annual.csv`
- `article33_s11b_share_scenarios.csv` (only calculated with complete legal and trade coverage)
- `wits_raw_json/`, `raw_api/`, `run_manifest.json` or `run_manifest_partial.json`

## Current execution status

The 2024 smoke test of v3 attempted the exact filtered Comext request above. It failed after five retries with `NameResolutionError: Failed to resolve 'ec.europa.eu' ([Errno -3] Temporary failure in name resolution)`. The partial manifest and `request_failures.jsonl` preserve the URL and error. No trade observations were downloaded. WITS and TARIC raw files were not downloaded either. This is an execution-environment access blocker, not evidence that the official sources lack the requested data.