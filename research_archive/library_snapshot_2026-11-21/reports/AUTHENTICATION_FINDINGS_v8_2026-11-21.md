# Bangladesh–EU CN8 official-source authentication — priority 1 audit (v8)

**Audit date:** 21 November 2026 (UTC+6).  
**Primary research:** *Bangladesh's Prospective EU Market-Access Exposure Following LDC Graduation: A Product-Level Assessment of Tariff Preference Erosion and Export Competitiveness*.  
**Decision:** **PARTIAL / NOT YET AUTHENTICATED AGAINST THE ORIGINAL EUROSTAT RAW DOWNLOADS.**  
**This report is an executed audit, not a claim that inaccessible official CSV files were retrieved.**

## 1. Definitive evidence inventory

| Item | Available bytes / external evidence | Result |
|---|---|---|
| User-supplied `eu_imports_bangladesh_cn8_2012_2025.csv` | **Available**, exact 1,731,439 bytes; SHA-256 `7af0f75024828471b2c65ac0085fd2232926a61efbc29da080b0c68bd1a5d03e` | Passed uploaded-file integrity and arithmetic checks; not an original native Eurostat response or authenticated original export receipt |
| `independent_reconciliation.csv` | **Available**, exact 3,996 bytes; SHA-256 `c41c1d18e0909abb1142c8c4f436d028443a0ed4f22c46e04becb4490648cd41` | Only 14 yearly summary rows; contains unverified claimed source URLs and 64-character SHA-256 values, not raw Eurostat records |
| Eurostat `DS-059322` dataset existence | Official Easy Comext and Eurostat metadata independently confirm it | Official dataset identification **CONFIRMED**; file's source linkage **UNCONFIRMED** |
| Eurostat `DS-045409` dataset existence and Comext API format | Official Eurostat Data Browser and official API manual | Official dataset and filtered download route **CONFIRMED**; raw file **NOT RETRIEVED** |
| Official DG Trade Bangladesh factsheet dated **20 May 2026** | Verified visually from page 3 of official PDF | 2025 EU imports **€21,179 million** under Comext statistical regime 4; source comparison confirmed |
| Earlier official DG Trade Bangladesh factsheet dated **8 May 2025** | Older PDF snapshot captured for same URL | 2024 EU imports **€19,880 million**; the 2026 factsheet reports **€19,923 million** for 2024 |
| Live 2025 Comext API re-download | **Attempted** on 21 Nov 2026; see `live_attempt/raw_retrieval_log.json` | DNS `NameResolutionError` before HTTP response; **ZERO** official raw observations obtained |
| Eurostat dataflow / bulk web probes | Attempted official links | Dataflow returned unsupported SDMX XML in web retrieval; bulk-list URL returned 404; neither produced official raw CSV |

### Scope and format of the uploaded row-level file

All **27,780** observed rows have: dataset `DS-059322`, annual frequency `A`, reporter `EU27_2020`, partner `BD`, flow `1` (imports), statistical procedure `T`, indicator `VALUE_IN_EUR` and eight-digit product codes. The data span 2012–2025, include **4,953** distinct CN8 codes and **155** explicit zero-value records. There were **no** duplicate product-year keys, malformed eight-digit product codes or negative euro amounts. All annual sums reproduce Codex's originally reported detailed CN8 values.

**Important:** the reference `TOTAL` values used below do **not** appear as `TOTAL` rows in this CSV. They were supplied separately by Codex. Consequently, the apparent reconciliation below verifies arithmetic against **reported aggregate references**, not an independently downloaded official aggregate series.

## 2. Exact reconciliation between the two alleged datasets

| Year | `DS-059322` CN8 rows (actual) | `DS-045409` CN8 rows (claimed) | Row delta | `DS-045409` minus `DS-059322` CN8 EUR | Aggregate `TOTAL` EUR difference |
|---|---:|---:|---:|---:|---:|
| 2012 | 1,480 | 1,482 | +2 | +19,999 | 0 |
| 2013 | 1,548 | 1,551 | +3 | +16,928 | -1 |
| 2014 | 1,570 | 1,574 | +4 | +108,945 | 0 |
| 2015 | 1,632 | 1,635 | +3 | +58,937 | -1 |
| 2016 | 1,639 | 1,642 | +3 | +126,219 | 0 |
| 2017 | 1,687 | 1,692 | +5 | +74,946 | -3 |
| 2018 | 1,792 | 1,798 | +6 | +79,553 | +1 |
| 2019 | 1,828 | 1,835 | +7 | +138,118 | -1 |
| 2020 | 1,851 | 1,856 | +5 | +155,989 | +3 |
| 2021 | 2,400 | 2,405 | +5 | +134,867 | +2 |
| 2022 | 2,589 | 2,592 | +3 | +73,603 | +2 |
| 2023 | 2,635 | 2,641 | +6 | +164,695 | 0 |
| 2024 | 2,534 | 2,541 | +7 | +190,204 | 0 |
| 2025 | 2,595 | 2,602 | +7 | +161,485 | +1 |
| **Total** | **27,780** | **27,846** | **+66** | **+1,504,488** | **+3** |

- Observed detailed total in uploaded `DS-059322` file: **€213,281,751,867**.
- Reported detailed total in `DS-045409` annual summary: **€213,283,256,355**.
- Reference aggregate total for `DS-059322` (previous Codex report): **€213,342,790,939**.
- Reference aggregate total for `DS-045409` (independent summary): **€213,342,790,942**.
- Detailed shortfalls against their respective reference aggregates: **€61,039,072** (0.0286108%) and **€59,534,587** (0.0279056%).

**What this does and does not prove:** The two file-level summaries differ in 66 *reported row counts*, and the second has €1,504,488 more in its reported CN8 total. It does **not** prove there are 66 genuinely new product-year records. The second file could contain additional records, revisions to shared records, or both. It is therefore incorrect to declare the causal explanation resolved without the 27,846 raw product-year records. The fact that the two reported `TOTAL` series differ by just €3 is a numerical comparison, **not** an independently authenticated reconciliation, because both totals may derive from the same prior source.

## 3. Comparison with DG Trade — source-vintage audit

The official DG Trade factsheet dated **20 May 2026** gives:

| Reference year | Codex reported `TOTAL` (million EUR) | DG Trade 20 May 2026 (million EUR) | Codex minus DG (million EUR) |
|---|---:|---:|---:|
| 2022 | 23,990.995 | 23,991 | -0.005 |
| 2023 | 18,944.474 | 18,939 | +5.474 |
| 2024 | 19,925.532 | 19,923 | +2.532 |
| 2025 | 21,244.359 | 21,179 | **+65.359** |

The DG Trade official values are rounded to **million EUR**, which can explain differences up to about €0.5 million, **not** the 2025 €65.359 million gap. The difference represents **0.3077% of Codex's 2025 reference `TOTAL`**, or **0.3086% of DG Trade's 2025 published value**.

**Evidence of source-vintage changes:** The DG Trade factsheet dated **8 May 2025** reported **€19,880 million** for 2024. The **20 May 2026** edition reports **€19,923 million** for the *same 2024 reference year*, a change of **€43 million** between snapshots. The 2022 and 2023 values also changed between those two editions. This establishes that published DG Trade historical totals are not static; it does **not** establish the source or exact explanation for the November 2026 2025 gap.

**Not yet established:** Statistical procedure `T` in the submitted extract cannot be assumed *from its label alone* to be numerically identical to DG Trade's 'statistical regime 4' for the same dataset, dates, origin treatment and vintage. Both appear to refer to broad or total trade concepts, but authoritative equivalence requires source-level codebook or contemporaneous Eurostat data confirmation. Revisions, confidentiality, adjustment lines and publication cutoffs are live hypotheses, not measured causes of the gap.

## 4. Source authenticity and procurement test

The 2025 annual official-source query provided in the independent summary was attempted:

```text
https://ec.europa.eu/eurostat/api/comext/dissemination/sdmx/2.1/data/DS-045409/A.EU27_2020.BD..1.VALUE_IN_EUROS?format=SDMX-CSV&startPeriod=2025&endPeriod=2025
```

The 21 Nov 2026 run failed before HTTP, with DNS `NameResolutionError: Failed to resolve 'ec.europa.eu'`. The web retrieval environment confirmed the official filtered Comext endpoint but did not provide the data response. No file was constructed, labelled as an official download, or assigned a fabricated HTTP status.

**Exact completion method:** On a machine able to access the official host, run:

```bash
python -m pip install requests
python verify_raw_eurostat_v8.py \
  --input eu_imports_bangladesh_cn8_2012_2025.csv \
  --summary independent_reconciliation.csv \
  --out official_authentication_result --fetch
```

This fetches 14 documented annual Comext queries, saves **real response bytes** under `raw_ds045409/`, records request time, source URL, returned HTTP metadata and SHA-256, checks year/reporter/partner/flow/product uniqueness and compares the full product-year records to the user-supplied `DS-059322` file. On a failed download it refuses authentication. It records all additional, absent, and value-changed product-year keys separately, so the +66/+€1,504,488 discrepancy can finally be **explained from rows rather than guessed from totals**. The returned headers and raw files must be archived as part of the thesis evidence pack. It compares the retrieved raw SHA values to the previous 14 claimed hashes without assuming that mismatches across different release dates are proof of errors.

To source-verify `DS-059322` itself, preserve the **original native Easy Comext export** and its source query/selection parameters, extraction timestamp, native file hash and release reference (if available); if the currently uploaded CSV is a transformed/filtered result, preserve both original raw bytes and the transformation script. If a new export differs because data have been revised, retain both vintages and a documented difference file rather than overwriting earlier evidence.

## 5. Verdict and staged study-use decision

| Check | Verdict |
|---|---|
| File content checksum, 27,780 rows, dimensions, product codes, uniqueness, sums | **PASS — file-level integrity** |
| Annual arithmetic against both *reported* aggregate reference series | **PASS — arithmetic only** |
| Official existence of both named datasets and official API route | **PASS — independently documented** |
| Raw `DS-045409` records matched to the claimed 27,846-row summary | **BLOCKED — absent raw files** |
| Original `DS-059322` downloaded native source/receipt authenticated | **BLOCKED — no source receipt/response** |
| 66-row and €1,504,488 discrepancy attributed to actual product-year records | **BLOCKED — absent DS-045409 raw records** |
| Same-vintage 2025 DG Trade/Comext reconciliation | **OPEN — €65.359m mismatch**, cause unknown |
| **Priority 1 completion criterion** | **NOT YET SATISFIED** |

**Recommended research status:** retain v7 for *provisional* descriptive analysis of the Bangladesh-origin product basket, with a transparent provenance warning. **Do not certify it as an independently authenticated official Eurostat export until the above source-level tests are passed.** Do not proceed to claimed market-share, tariff-exposure or safeguarded interpretations on the strength of these totals alone.

## Official sources and evidence

1. Eurostat Easy Comext: https://ec.europa.eu/eurostat/comext/newxtweb/mainxtnet.do
2. Eurostat metadata confirming `DS-059322`: https://ec.europa.eu/eurostat/cache/metadata/en/cult_trd_go_esms.htm
3. Eurostat `DS-045409` data browser: https://ec.europa.eu/eurostat/databrowser/view/DS-045409
4. Eurostat Comext API guide: https://ec.europa.eu/eurostat/en/web/user-guides/data-browser/api-data-access/api-getting-started/comext-database
5. Eurostat detailed trade metadata (confidentiality and revisions): https://ec.europa.eu/eurostat/cache/metadata/en/ext_go_detail_sims.htm
6. DG Trade country PDF (20 May 2026 edition, p.3, and older 8 May 2025 snapshot): https://webgate.ec.europa.eu/isdb_results/factsheets/country/details_bangladesh_en.pdf
7. Eurostat international trade data information: https://ec.europa.eu/eurostat/web/international-trade-in-goods/information-data

**Reproducibility:** `audit_offline_v8.py` executed successfully; `verify_raw_eurostat_v8.py` was executed with `--fetch --years 2025` and logged the DNS blocker without producing false observations. The workbook `EU_Bangladesh_Comext_source_authentication_v8.xlsx` contains formula-verified yearly and publication-vintage comparisons. `authentication_audit_manifest.json` is an immutable file-level evidence record for the current project inputs.