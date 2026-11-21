# Task B: historical CN8 nomenclature concordance — audit v10

**Date:** 21 November 2026  
**Thesis:** Bangladesh's Prospective EU Market-Access Exposure Following LDC Graduation: A Product-Level Assessment of Tariff Preference Erosion and Export Competitiveness.  
**Verdict: PARTIALLY COMPLETE.** The input trade-data observation audit and classification-risk assessment were executed on the 27,780-row original file; the complete legally validated 2012–2025 concordance could **not** be constructed because the full official 14 annual CN8 lists and 13 consecutive-year change tables could not be retrieved as source files.

## Directly reproducible findings (actual user-uploaded Bangladesh trade extract)

- Original input CSV: `eu_imports_bangladesh_cn8_2012_2025.csv`, SHA-256 recorded in `data/audit_manifest_taskB.json`.
- 27,780 observed CN8/year/value records; 4,953 different eight-digit CN codes; 2012–2025 inclusive.
- Exactly 690 codes are present as **observed trade records** in all 14 years. The sum of their 2025 observed values is **€20,243,152,283**, or **95.314986%** of the recorded 2025 basket (€21,238,163,196).
- The existence of a repeated numeric code is **not evidence** that its legal definition and composition are unchanged. Consequently **none of these 690 series is released as semantically harmonized CN8 growth**.
- The 2025 top 200 are retained as the **native-year 2025 ranking**; no annual classification conversion is necessary to rank products within 2025. However, the 2025 official code descriptions and legal-validity dates are not yet verified in the complete annual catalogue.
- Pairwise observed-code overlap, new appearances and disappearance counts are tabulated **only as empirical coverage**, never as official changes to classifications. Code absence can reflect no recorded flow, disclosure, code invalidity, or other causes, not automatically a true zero.
- Annual HS2 chapter totals are calculated only as *descriptive chapter aggregation using observed code prefixes*. Their year-to-year changes must not be mistaken for fully harmonized CN8 product-level growth.

## Secondary historical-change cross-check (2012–2022 only)

The publicly published R `harmonizer` package includes a CN8 concordance table derived from the former Eurostat RAMON system, covering 1988–2022. The GitHub `cran/harmonizer` text file was fetched and inspected on 21 Nov 2026; Git blob SHA was `1933b8d69051ffb7a9f1f30afdc0a4976696f219`. It contains 16,823 non-header change links. 2012–2022 matches were assessed against the **actual** top-200 2025 CN8 codes, after stripping spaces in the source-code notation.

- **20 of the 2025 top-200 CN8 code strings appear as a source or destination in this historical change list** for 2012–2022.
- These 20 product lines carry **€1,386,480,826 (6.5283%)** of 2025 reported Bangladesh-origin value.
- These matches are **a historical change-risk indicator**, not proof of a semantic change in 2025, not a reconstructed 2012–2025 family, and not evidence that the other 180 top lines are stable. They provide practical priorities for crosswalk validation.
- Especially important transition points include the 2017 and 2022 HS revisions. The crosswalk source **ends in 2022**; it cannot certify 2023, 2024, or 2025.

Source: https://github.com/cran/harmonizer/blob/master/inst/extdata/CN8/CN8_concordances_1988_2022.csv  
Package method: https://cran.rstudio.org/web/packages/harmonizer/vignettes/harmonizer.html

## Official sources located, but not downloaded as classification records

1. **Eurostat EU Vocabularies CN annual classifications** (pages list editions 2017 through 2025): https://op.europa.eu/en/web/eu-vocabularies/eurostat ; the 2025 edition's legal basis is Commission Implementing Regulation (EU) 2024/2522.
2. **Lithuania's official statistics portal, Combined Nomenclature page**, contains the legal source editions from 2012 onward plus downloadable conversion tables (including several years 2018→2024): https://osp.stat.gov.lt/en/web/guest/kombinuotoji-nomenklatura-kn
3. **Statistics Denmark's official CN page** provides the complete 2025 official-text list, new/deleted code lists, and 2024→2025 / 2025→2024 change tables: https://www.dst.dk/en/Indberet/oplysningssider/intrastat/udenrigsoekonomi
4. **Eurostat statement on classification changes and methodology**: https://ec.europa.eu/eurostat/cache/metadata/en/ext_go_detail_sims.htm
5. **Eurostat guidance on access to statistical classifications via EU Vocabularies / ShowVoc**: https://ec.europa.eu/eurostat/en/web/products-eurostat-news/-/cn-20221107-1

A source page is **not** a downloaded catalogue. No complete official annual code list, English description column, nor year-pair correspondence XLS has been imported into this project at v10. The source requirement log identifies all 27 files and their preferred official publication portals.

## Retrieval attempt log

Direct `requests.get()` from the execution container attempted:
- `https://osp.stat.gov.lt/documents/10180/11799020/CN%2B2024-CN%2B2023%2BEN.xlsx/30990486-ba58-4fbe-ad01-b9d105f34aac`
- `https://www.nbb.be/en/statistics/topics/foreign-trade/nomenclature-and-codes`
- `https://op.europa.eu/en/web/eu-vocabularies/eurostat`

All three failed **before HTTP** with DNS `NameResolutionError` (host resolution unavailable). Official source webpages were discoverable through the web research interface, but actual XLS/XLSX binaries could not be inspected or saved through that interface. A GitHub connector successfully retrieved the **secondary** RAMON-derived concordance text only. No official data files are represented as downloaded.

## Methodological safeguards implemented

- The `code/certify_cn8_concordance_strict.py` program requires **14 annual catalogue files** and **13 adjacent-year complete official correspondence files** plus file-level SHA-256 and provenance manifest. It refuses to certify without them.
- Code family graph is built across `(year, CN8)` nodes, permitting explicit 1:1 mappings and official multi-to-one / one-to-many lineage, while not incorrectly equating identical numeric codes when descriptions change.
- A numerical code repeated in adjacent annual catalogues is automatically linked only if the complete official year-pair change table was supplied and its descriptions agree. Otherwise it is flagged for review.
- It requires every valid member of a family/year to be observed in the trade dataset to give a complete family-year total; absent trade records remain **missing**, not zero.
- It writes 2012–2025 family CAGR only for complete source-verified lineage with complete year coverage and positive starting value; otherwise leaves it blank.
- A fully isolated synthetic test with a deliberate 2016→2017 split and a missing family-year record **passed**, demonstrating the gating logic, not supplying any empirical harmonized result.
- The strict live-input run printed `Missing 27 of 27 required source files; no certified crosswalk produced` as intended. This is the truthful completion status.

## Completion criterion and decision

**NOT MET** for a full original-source-verified 2012–2025 classification concordance. Pending inputs are the original annual CN8 files, the 13 official full change tables, and provenance manifests. Import them through the normalized `official_input_templates/` format, audit their original hashes and source dates, rerun the strict script and inspect its classification lineage flags. **Do not promote any unverified CN8 time series, raw-code CAGR, period rankings or HS6-prefix approximations as harmonized findings** in the thesis.

**Safe to use now:** the native 2025 product values and ranking; labelled chapter-level descriptive compositions; observed-code coverage counts. **Not safe to use now:** 2012–2025 CN8 product growth, stable-code claims, corrected historical code splits or any value that depends on a non-existent official concordance.