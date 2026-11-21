# Actual Bangladesh–EU CN8 source file: verified descriptive analysis (v7)

The user's original 27,780-record CSV is NOW ACTUALLY PRESENT. The full 2012–2025 file has been parsed and audited by executable Python scripts, and the 2025 rankings and chapter-concentration statistics are real results derived from that file (not demonstration or synthetic data).

**Status:** Internal row-level validation PASSED; independent Eurostat re-download, source vintage, CN concordance and all other-country tariff/quantity inputs remain open.

## Files to open

1. `AUDIT_REPORT_ACTUAL_CN8_v7.md` — verdict, 14-year reconciliation, key findings, limits and source provenance.
2. `Bangladesh_EU_CN8_RowLevel_Validation_v7.xlsx` — Excel workbook with 2025 top-200, raw-code 2012–2025 top-200, annual checks, chapter breakdown, second-extract comparison and source gaps.
3. `top_200_cn8_2025_UNHARMONIZED.csv` — standalone top-200 ranking.
4. `cn8_product_year_matrix_missing_not_zero.csv` — complete 4,953-code × 14-year observed values. Blank means not reported, not zero.
5. `eu_imports_bangladesh_cn8_2012_2025.csv` — untouched source (SHA256 in report).

## Reproduce with Python 3.10+

```bash
python validate_and_rank_cn8.py --input eu_imports_bangladesh_cn8_2012_2025.csv --independent independent_reconciliation_DS045409_as_uploaded.csv --out ./results
python test_actual_uploaded_source.py eu_imports_bangladesh_cn8_2012_2025.csv
```

Only Python standard library is required to run the validation/ranking pipeline. `build_audit_workbook.py` uses `artifact_tool` and is optional; a completed workbook is included.

## Thesis interpretation

The **2025 cross-section** is available for descriptive product ranking and concentration. The period ranking is unharmonized: a raw CN8 string is not independently confirmed to identify the same product definition throughout 2012–2025. The current file has no competitor-origin imports, origin-neutral total EU product demand, net mass, supplementary units or tariffs. Do not treat it as a completed causal or scenario-analysis panel.
