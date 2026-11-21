# Eurostat Comext Bangladesh CN8 extractor — v4

**Prepared:** 21 November 2026. **Data status: NO OFFICIAL TRADE RECORDS DOWNLOADED in this environment.**

## Purpose

A corrected, executable alternative to a pasted script that attempted to extract EU27_2020 imports from Bangladesh for 2012–2025. Unlike the pasted `DS-059322` URL, this version uses the Eurostat official documented `DS-045409` SDMX 2.1 endpoint. The two datasets are distinct and their API keys must not be interchanged.

## Execute

```bash
python -m pip install requests
python eurostat_comext_bd_cn8_verified_v4.py --out ./bd_cn8_comext_validation_v4 --start 2012 --end 2025
```

Requires an **internet-enabled Python environment** that resolves `ec.europa.eu`. Run it once; do not hammer the endpoint concurrently. It makes filtered annual queries, one year at a time.

## Core query

`https://ec.europa.eu/eurostat/api/comext/dissemination/sdmx/2.1/data/DS-045409/A.EU27_2020.BD..1.VALUE_IN_EUROS?format=SDMX-CSV&startPeriod=2024&endPeriod=2024`

Eurostat documentation:
- https://ec.europa.eu/eurostat/en/web/user-guides/data-browser/api-data-access/api-getting-started/comext-database
- https://ec.europa.eu/eurostat/en/web/user-guides/data-browser/api-data-access/api-detailed-guidelines/asynchronous-api
- https://ec.europa.eu/eurostat/web/international-trade-in-goods/database

## Controls

- Parses CN8 codes only as exactly eight digits, preserving leading zeroes.
- Does **not** aggregate HS2/4/6 and `TOTAL` along with CN8 lines.
- Checks fixed reporter, partner, import flow, value indicator and annual year.
- Rejects duplicate product/year records and invalid numeric values.
- Reconciles sum of observed CN8 values against the official `TOTAL` value for each year; queries `TOTAL` separately if absent.
- Rejects a year if any CN8 observation has a missing value, if its total is absent, or if the sum discrepancy exceeds `max(1 EUR, official_total × 1e-7)`.
- Preserves raw responses in `raw/`, SHA-256 source hashes in `run_manifest_v4.json`, and annual checks in `annual_reconciliation_v4.csv`.
- Writes `eu_imports_bangladesh_cn8_2012_2025_VALIDATED.csv` **only if all 14 years pass**.
- No absent product-year cell is filled with zero.

A reconciled file is still a **basic numerical integrity check**. Before cross-year growth or regression, you must validate annual CN nomenclature changes, document missing/non-disclosed products, and create sourced product concordances. For the thesis, separate competitor origin data, quantity data, tariffs, rules of origin, and preference utilisation also remain necessary.

## Live attempt on 21 November 2026

Ran a one-year 2024 connectivity/validation attempt and received no Eurostat data:

- Request: `https://ec.europa.eu/eurostat/api/comext/dissemination/sdmx/2.1/data/DS-045409/A.EU27_2020.BD..1.VALUE_IN_EUROS?format=SDMX-CSV&startPeriod=2024&endPeriod=2024`
- Error: `ConnectionError ... NameResolutionError ... Failed to resolve 'ec.europa.eu' ([Errno -3] Temporary failure in name resolution)`.
- **HTTP status:** none (DNS resolution failed before HTTP).
- Official data rows downloaded: **0**.
- CSV validated/exported: **no**.

The script's parser, duplicate detection and reconciliation logic passed separate **offline illustrative fixture tests**; these fixtures are not real trade observations and were not exported as empirical data.

## If the SDMX query fails when networking is available

1. Save the HTTP status, response headers and first several hundred bytes of the body. A valid dataset/query may change its format or dimension values; do not guess.
2. Inspect the live DS-045409 SDMX data constraints and dataset metadata.
3. Fall back to Eurostat Comext official bulk inventory/files for the corresponding annual years. Select actual filenames from the live inventory instead of assuming them.
4. Do not silently substitute DS-059322; verify its `STAT_PROCEDURE` dimension, `INDICATORS` options and `PERIOD` representation before using it.

This v4 version is **not evidence of an executed full extraction**.