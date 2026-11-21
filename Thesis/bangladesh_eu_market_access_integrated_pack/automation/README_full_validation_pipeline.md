# Full Bangladesh–EU trade and tariff data validation pipeline

## Why this pipeline exists

The preliminary workbook is a 2024 screening exercise, not the complete 2012–2025 dataset. This reproducible pipeline is designed to retrieve the larger data extract from official/public endpoints on an internet-enabled machine.

## Sources and design

### Trade: Eurostat Comext DS-045409

Eurostat documents DS-045409 as EU trade since 1988 by HS2/HS4/HS6 and CN8. The Comext API has a dedicated base URL and filtered queries; large unfiltered full-dataset queries are intentionally disallowed. The pipeline therefore:

1. Queries EU27_2020 imports from Bangladesh for one calendar year at a time, retrieving the product dimension.
2. Retains CN8 records and identifies the top 200 product lines by latest-year value, by full-period value, and for chapters 61–63.
3. Queries all partner origins only for those selected CN8 products, one year at a time.
4. Queries the extra-EU aggregate separately so partner-level shares use an appropriate external-import denominator.
5. Retrieves HS2 chapter values for 61, 62 and 63 by partner for the Section S-11b denominator.
6. Produces a balanced product-year panel and explicitly marks non-returned cells rather than automatically filling zeros.

**Annual 2012–2025 caveat:** 2025 is included as the latest full calendar year in the specified range, but check Eurostat's data availability and revisions before treating the year as final. The dataset was updated 15 September 2026 in the observed release.

### Tariffs: WITS / UNCTAD TRAINS and EU TARIC

The pipeline requests HS6 tariff schedules from WITS TRAINS for EU reporter code 918, using partner `000` for World/MFN and selected competing origin countries. It stores raw JSON responses and a request manifest. WITS TRAINS data are HS6 averages and reported schedules; they are not a substitute for exact CN8/CN10 tariff lines.

For current, exact tariff-line checks, use the European Commission's TARIC raw-data download. TARIC includes third-country duties, tariff preferences, quotas and other measures and publishes raw data in Excel format. Check the tariff-line's effective date, origin country, preference measure, additional codes and any specific-duty component. A pure ad valorem percentage is not a complete tariff where a specific duty applies.

WITS partner `000` is the world/MFN code. Country-specific preference data may be recorded under a partner group rather than a country code. If a country-specific query returns no rate, inspect WITS TRAINS Tariff Measures and Preference Beneficiaries before concluding that no preference exists.

## Installation and execution

Requires Python 3.10+ and `requests`.

```bash
python -m pip install requests
python run_full_validation.py --start 2012 --end 2025 --topn 200 --out bangladesh_eu_full_validation
```

If WITS API requests are unavailable or too slow, run:

```bash
python run_full_validation.py --start 2012 --end 2025 --topn 200 --skip-wits --out bangladesh_eu_full_validation
```

The script saves raw JSON responses, CSV extracts, QA summaries and a request manifest. It sends requests sequentially, not in parallel, to respect Eurostat's fair-use guidance. Do not launch many copies concurrently.

## Output files

- `bd_eu_imports_all_cn8_annual.csv` — EU imports from Bangladesh by CN8 and year.
- `top_products_latest_all_sectors.csv` — top 100–200 CN8 lines by the latest year.
- `top_products_period_all_sectors.csv` — top lines by accumulated period value.
- `top_products_latest_S11b_ch61_63.csv` — top apparel/textile lines in chapters 61–63.
- `top_products_period_S11b_ch61_63.csv` — corresponding full-period ranking.
- `eu_selected_products_all_partners_annual.csv` — product-year-partner values for selected product lines.
- `eu_selected_products_extraEU_totals_annual.csv` — total extra-EU imports for share denominators.
- `top5_competitors_by_product_year.csv` — top five competitors per product-year.
- `market_share_by_product_year.csv` — Bangladesh share of extra-EU imports.
- `s11b_chapters_61_63_by_partner_annual.csv` — Chapter 61–63 values by origin.
- `s11b_partner_totals_annual.csv` — partner totals for the three chapters.
- `gsp_beneficiary_status_template.csv` — year-specific beneficiary status mapping template.
- `wits_raw_json/` and `run_manifest.json` — raw tariff response and request audit.

## Required validation after download

1. Check the run manifest for request errors and record counts.
2. Confirm that `EU27_2020`, partner `BD`, annual frequency and import flow were used.
3. Confirm one year of CN8 totals against Comext Data Browser totals and the old 2024 WITS/Comtrade screen. Differences may arise from source, reporter/mirror, valuation, scope and classification.
4. Keep CN8 raw codes and labels. Create a nomenclature-year crosswalk before aggregating across HS revisions; HS6 prefix extraction is only a preliminary mapping, not a formally harmonised concordance.
5. Use the separate extra-EU aggregate for market-share denominators; do not include EU internal trade or aggregate partner rows in competitor rankings.
6. Join Section S-11b partner values to a year-specific GSP beneficiary/status table derived from the effective legal annex for that year. Do not infer GSP status from the trade data.
7. For statutory Article 33 calculations, compare Bangladesh's S-11b imports to all beneficiary-country S-11b imports (37% threshold) and separately to all-origin EU S-11b imports (6% exception). Include all three chapters 61, 62 and 63.
8. Review WITS tariff response partner groups and `EXCLUDEDFROM` attributes. Do not interpret no country-code record as no preference until group coverage has been checked.
9. Compare HS6 WITS tariff averages to CN8/CN10 TARIC lines for the largest products. Keep specific rates separate; do not collapse mixed/compound rates into an ad valorem figure without a justified ad valorem equivalent.
10. Rules-of-origin eligibility and actual preference utilisation are separate variables. Do not claim utilisation from eligibility.

## Legal and research context to combine with the data

- UNGA Resolution A/RES/81/8 (29 October 2026) extends Bangladesh's preparatory period before LDC graduation to 24 November 2029.
- Regulation (EU) 2026/1395 applies from 1 January 2027. Article 17(2) provides a three-year transition after a country ceases to meet the LDC criterion before EBA removal; the exact operative date must be confirmed by the Commission's subsequent status/implementation act.
- Article 33 and Annex IV provide the special safeguard thresholds for GSP section S-11b, Chapters 61–63: 37% of EU imports in the section from all GSP beneficiaries, alongside the separate 6% all-origin EU import share exception. Article 33 does not apply to EBA beneficiaries.
- GSP+ is not automatic. Country eligibility, ratification and effective implementation of required international conventions, and Commission approval must be assessed independently.
- Existing export-survival research in Bangladesh means survival is not a novel gap by itself: Nicita, Shirotori & Tumurchudur Klok (2013) included 46,770 Bangladesh product-destination spells for 1993–2007; World Bank's recent Bangladesh Country Economic Memorandum analyses firm-level exporter dynamics and survival using customs data for 2005–2016. A new survival thesis would need a sharply distinct product-market mechanism, not merely newer dates.
- Relevant prior work includes Brenton, Saborowski & von Uexkull (2010) on developing-country export-flow survival; Fugazza & McLaren (2014) on relative market access and Peruvian export survival; Sytsma (2021) on rules of origin and preference utilisation among LDCs; Ginting, Razzaque & Hasan (2024) on Bangladesh export diversification and policy impediments; Bari & Jayanthakumaran (2021) on Bangladesh exporter networks and export success.

## Important limitations

This pipeline has not been executed in the current ChatGPT session because the execution environment cannot resolve external hosts (DNS failure). The script is a reproducible extraction tool, not evidence that the panel has already been downloaded. The preliminary 2024 extracts remain screening data only.


## Selection rule note (revised)

The all-partner panel is intentionally limited to the union of the latest-year top 200 all-sector CN8 lines and the latest-year top 200 Section S-11b CN8 lines (maximum 400 unique CN8 codes). Separate ranking files preserve the latest-year and full-period rankings. This avoids accidentally expanding the partner panel to an 800-line union while still keeping a focused statutory-safeguard basket.

## Additional API and tariff extraction notes (checked 17 November 2026)

- Eurostat's Statistics API accepts `sinceTimePeriod` and `untilTimePeriod` together to restrict time to a defined interval; either can be used with the Comext-specific base endpoint. The script uses both for one year at a time. Any dimension filter can be passed by its dataset dimension code. See the Eurostat API detailed guidelines: https://ec.europa.eu/eurostat/en/web/user-guides/data-browser/api-data-access/api-detailed-guidelines/api-statistics
- Comext's separate API endpoint is mandatory for DS-prefixed reference data. Eurostat disables an unfiltered complete-dataset API download for Comext because of dataset size; filtered queries or the separate CSV bulk files are the intended routes. See: https://ec.europa.eu/eurostat/en/web/user-guides/data-browser/api-data-access/api-getting-started/comext-database
- WITS TRAINS provides HS6-level MFN and preferential tariff observations. Its output distinguishes `TARIFFTYPE` (MFN/PREF), simple average, number of national tariff lines, preferential/MFN lines, non-ad-valorem lines, min/max rates, nomenclature and country exclusions. It supports partner groups and semicolon-delimited product/partner lists. See: https://wits.worldbank.org/witsapiintro.aspx and https://wits.worldbank.org/data/public/WITSAPI_UserGuide.pdf
- The script now flattens WITS SDMX-JSON tariff observations and creates `wits_tariff_rates_long.csv` and `wits_preference_margins_hs6.csv` when the API request succeeds. It computes a margin only where MFN and PREF observations can be directly matched by HS6/year; partner-group coverage still requires mapping from WITS metadata and is not silently allocated to country origins.
- For the exact EU CN8/CN10 tariff-line checks, use official TARIC raw data, including origin, measure, additional code, effective start/end dates, and specific/compound duty elements: https://taxation-customs.ec.europa.eu/online-services/online-services-and-databases-customs/eu-customs-tariff-taric_en
- A missing tariff record is not a zero tariff. A missing trade observation is not automatically zero trade. Both require a separate status and source-coverage check.

## What this package does not claim

The pipeline has not been executed successfully in this ChatGPT container: the most recent test failed at DNS resolution for `ec.europa.eu`. The prepared scripts, templates and the partial data extracts are deliverables; they are not the requested complete 2012–2025 trade and tariff panels. The 2024 competitor sample (10 HS6 lines) and two selected 2025 line snapshots are clearly labelled as screening evidence only.
