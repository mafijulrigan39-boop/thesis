#!/usr/bin/env python3
"""Build workbook using artifact_tool only (not pandas/openpyxl)."""
import csv,sys
from pathlib import Path
from artifact_tool import Workbook, SpreadsheetFile

ROOT=Path(__file__).resolve().parent
NAVY='#183046';TEAL='#096B70';LIGHT='#EAF3F4';PALE='#F3F6FA';WHITE='#FFFFFF';YELLOW='#FFF1CA';RED='#AE4035';INK='#213547'
wb=Workbook.create()

def load(filename):
 with open(ROOT/filename,encoding='utf-8',newline='') as f:return list(csv.DictReader(f))

def sh(name,title,subtitle,cols,rows,widths=None):
 ws=wb.worksheets.add(name)
 n=len(cols);last=chr(64+n) if n<=26 else 'Z'
 ws.get_range(f'A1:{last}1').merge();ws.get_range('A1').values=[[title]]
 ws.get_range(f'A1:{last}1').format={'fill':NAVY,'font':{'color':WHITE,'bold':True,'size':16},'row_height':35,'vertical_alignment':'center'}
 ws.get_range(f'A2:{last}2').merge();ws.get_range('A2').values=[[subtitle]]
 ws.get_range(f'A2:{last}2').format={'fill':LIGHT,'font':{'color':INK,'size':10},'row_height':28,'vertical_alignment':'center'}
 ws.get_range_by_indexes(3,0,1,n).values=[cols]
 ws.get_range_by_indexes(3,0,1,n).format={'fill':TEAL,'font':{'bold':True,'color':WHITE},'row_height':35,'wrap_text':True,'vertical_alignment':'center'}
 if rows:
  ws.get_range_by_indexes(4,0,len(rows),n).values=rows
  ws.get_range_by_indexes(4,0,len(rows),n).format.row_height=20
 ws.freeze_panes.freeze_rows(4)
 for j,w in enumerate(widths or [15]*n):
  ws.get_range_by_indexes(0,j,max(5,len(rows)+4),1).format.column_width=w
 return ws

annual=load('annual_integrity_and_concentration_2012_2025.csv')
ann_cols=['Year','CN8 rows','Zero rows','CN8 EUR','Reported TOTAL EUR','CN8−TOTAL EUR','Difference %',
          'HS61 EUR','HS62 EUR','HS63 EUR','HS61–63 EUR','HS61–63 share %','CN8 HHI','Top10 share %',
          'Top50 share %','Top200 share %','New observed codes','Lost observed codes']
ann_rows=[]
for r in annual:
 ann_rows.append([int(r['year']),int(r['cn8_rows']),int(r['explicit_zero_rows']),int(r['cn8_sum_eur']),
 int(r['codex_reported_total_eur']),None,None,int(r['hs61_eur']),int(r['hs62_eur']),int(r['hs63_eur']),
 int(r['hs61_63_eur']),float(r['hs61_63_share_pct']),float(r['cn8_hhi_0_to_10000']),
 float(r['top10_share_pct']),float(r['top50_share_pct']),float(r['top200_share_pct']),
 int(r['newly_seen_vs_prior_year']) if r['newly_seen_vs_prior_year'] else None,
 int(r['not_seen_vs_prior_year']) if r['not_seen_vs_prior_year'] else None])
wa=sh('Annual_Data','ANNUAL CN8 RECONCILIATION | 2012–2025',
 'Original user-provided DS-059322 CN8 file; TOTAL amounts were reported by Codex, not separately downloaded.',
 ann_cols,ann_rows,[12,13,12,22,23,20,17,21,21,21,22,19,17,17,17,19,16,18])
wa.get_range('F5').formulas=[['=D5-E5']];wa.get_range('F5:F18').fill_down()
wa.get_range('G5').formulas=[['=IF(E5=0,"",100*F5/E5)']];wa.get_range('G5:G18').fill_down()
wa.get_range('D5:F18').set_number_format('#,##0;[Red](#,##0)')
wa.get_range('H5:K18').set_number_format('#,##0')
wa.get_range('G5:G18').set_number_format('0.0000;[Red](0.0000)')
wa.get_range('L5:P18').set_number_format('0.00')
wa.get_range('F5:G18').format.fill=YELLOW

latest=load('top_200_cn8_2025_UNHARMONIZED.csv')
rank_cols=['Rank','CN8 (text)','HS2','2025 EUR','Share of BD %','2024 EUR (if observed)','Raw-code YoY %','Period 2012–25 EUR','Years observed','Comparability']
rank_rows=[]
for r in latest:
 rank_rows.append([int(r['rank_2025']),str(r['cn8_code_TEXT']),str(r['hs2_chapter']),
 int(r['value_2025_eur']),None,
 int(r['value_2024_eur_if_reported']) if r['value_2024_eur_if_reported'] else None,
 None,int(r['raw_code_period_value_2012_2025_eur']),int(r['observed_year_count']),
 'CN8 cross-year definition not confirmed'])
wr=sh('Top200_2025','TOP 200 BANGLADESH CN8 LINES | 2025',
 'Actual observed 2025 values; Bangladesh basket share is NOT EU market share. No year-specific CN8 concordance yet.',
 rank_cols,rank_rows,[10,16,10,22,18,22,19,23,16,34])
wr.get_range('B5:B204').set_number_format('@');wr.get_range('C5:C204').set_number_format('@')
wr.get_range('E5').formulas=[['=IFERROR(100*D5/Annual_Data!$D$18,"")']]
wr.get_range('E5:E204').fill_down()
wr.get_range('G5').formulas=[['=IF(OR(F5="",F5=0),"",100*(D5/F5-1))']]
wr.get_range('G5:G204').fill_down()
wr.get_range('D5:D204').set_number_format('#,##0')
wr.get_range('F5:F204').set_number_format('#,##0')
wr.get_range('H5:H204').set_number_format('#,##0')
wr.get_range('E5:E204').set_number_format('0.0000')
wr.get_range('G5:G204').set_number_format('0.00;[Red](0.00)')

period=load('top_200_raw_code_period_2012_2025_UNHARMONIZED.csv')
per_cols=['Rank','CN8 (text)','HS2','Raw-code period EUR','Period share of BD %',
          'Years observed','2025 EUR if observed','2012 EUR if observed','Comparability']
per_rows=[]
for r in period:
 per_rows.append([int(r['raw_code_period_rank']),str(r['cn8_code_TEXT']),str(r['hs2_chapter']),
 int(r['period_sum_eur_2012_2025']),None,int(r['observed_year_count']),
 int(r['value_2025_eur_if_reported']) if r['value_2025_eur_if_reported'] else None,
 int(r['value_2012_eur_if_reported']) if r['value_2012_eur_if_reported'] else None,
 'Unharmonized descriptive sum'])
wp=sh('Top200_Period','TOP 200 RAW-CODE TOTALS | 2012–2025',
 'WARNING: These are unharmonized CN8 code sums. Not a validated longitudinal product ranking.',
 per_cols,per_rows,[10,16,10,23,22,16,24,24,35])
wp.get_range('B5:B204').set_number_format('@');wp.get_range('C5:C204').set_number_format('@')
wp.get_range('E5').formulas=[['=IFERROR(100*D5/SUM(Annual_Data!$D$5:$D$18),"")']]
wp.get_range('E5:E204').fill_down();wp.get_range('E5:E204').set_number_format('0.0000')
wp.get_range('D5:D204').set_number_format('#,##0');wp.get_range('G5:H204').set_number_format('#,##0')

ind=load('ds059322_vs_ds045409_comparison.csv')
ind_cols=['Year','DS059322 rows','DS045409 rows','Difference rows',
 'DS059322 CN8 EUR','DS045409 CN8 EUR','Difference EUR','DS059322 TOTAL','DS045409 TOTAL','Difference TOTAL']
indrows=[]
for r in ind:
 indrows.append([int(r['year']),int(r['ds059322_cn8_rows']),int(r['ds045409_reported_cn8_rows']),None,
               int(r['ds059322_cn8_sum_eur']),int(r['ds045409_reported_cn8_sum_eur']),None,
               int(r['codex_reported_total_eur']),int(r['ds045409_reported_total_eur']),None])
wi=sh('Cross_Source_Check','DS-059322 VERSUS DS-045409 | REPORTED SUMMARIES',
 'Different datasets/export routes. DS-045409 source CSV unavailable; reported summary alone cannot resolve differences.',
 ind_cols,indrows,[12,17,17,17,23,24,22,23,23,23])
for cell,fill in [('D5','=B5-C5'),('G5','=E5-F5'),('J5','=H5-I5')]:wi.get_range(cell).formulas=[[fill]]
for col in ('D','G','J'):wi.get_range(f'{col}5:{col}18').fill_down()
wi.get_range('E5:J18').set_number_format('#,##0;[Red](#,##0)')

chap_rows=load('chapter_by_year_descriptive.csv')
chap25=[r for r in chap_rows if r['year']=='2025']
chap25.sort(key=lambda d: -int(d['import_value_eur']))
chapter_cols=['HS chapter','2025 CN8 EUR','Share of BD CN8 %']
wc=sh('Chapters_2025','2025 IMPORT STRUCTURE BY HS2',
 'Shares refer to Bangladesh-origin CN8 imports (NOT Bangladesh\'s share of total EU demand).',chapter_cols,
 [[r['hs2_chapter'],int(r['import_value_eur']),None] for r in chap25],[18,24,23])
wc.get_range(f'A5:A{4+len(chap25)}').set_number_format('@')
wc.get_range('C5').formulas=[['=IFERROR(100*B5/Annual_Data!$D$18,"")']]
wc.get_range(f'C5:C{4+len(chap25)}').fill_down();wc.get_range(f'C5:C{4+len(chap25)}').set_number_format('0.00')
wc.get_range(f'B5:B{4+len(chap25)}').set_number_format('#,##0')

source_notes=[
 ['DATA','Uploaded original CSV','eu_imports_bangladesh_cn8_2012_2025.csv','User upload; raw Eurostat receipt not supplied'],
 ['SOURCE DATASET','Eurostat Easy Comext','https://ec.europa.eu/eurostat/comext/newxtweb/setupdimselection.do','User CSV has DATASET=DS-059322 / STAT_PROCEDURE=T / INDICATORS=VALUE_IN_EUR'],
 ['SOURCE METHODOLOGY','Eurostat detailed trade metadata','https://ec.europa.eu/eurostat/cache/metadata/en/ext_go_detail_sims.htm','Confidentiality, revisions, and CN annual changes matter'],
 ['SOURCE CODES','Eurostat CN classifications','https://op.europa.eu/en/web/eu-vocabularies/eurostat','No year-specific CN code-to-code concordance included'],
 ['RECONCILIATION','Codex reported TOTAL','Prior chat (14 annual aggregate values)','Not independent same-file official TOTAL; counts and sums checked against supplied aggregates'],
 ['SECOND EXTRACT','DS-045409 reconciliation','independent_reconciliation.csv','Only yearly summaries and SHA strings, not raw extract'],
 ['INTERPRETATION','Historical product comparability','Not independently verified','Do not treat raw-code period ranks as harmonized-product findings'],
 ['LIMITATION','EU market shares','All-origin product-year imports unavailable','2025 shares in this workbook are within BANGLADESH product basket only'],
 ['LIMITATION','Competitor benchmarking','Other-origin product-year panel unavailable','No competitor share or unit-value claim is calculated'],
 ['LIMITATION','Tariff exposure','EU TARIC tariff-line matrix unavailable','No tariff-cost / post-LDC scenario exposure is calculated'],
 ['LIMITATION','Article 33 S-11b','GSP beneficiary-origin denominator unavailable','Do not infer Article 33 result from Bangladesh-only trade values'],
 ['LIMITATION','Net mass / supplements','Uploaded CSV contains euro values only','No quantity or unit-value calculations possible'],
]
ws=sh('Provenance_Gaps','SOURCE PROVENANCE & UNRESOLVED INPUTS',
 'Evidence log: row-level integrity passes; upstream source authenticity and cross-source comparability remain unresolved.',
 ['Area','Evidence type','Source / local artifact','Implication'],source_notes,[20,26,62,84])
ws.get_range('A5:D16').format.wrap_text=True
ws.get_range('A5:D16').format.row_height=42

wd=wb.worksheets.add('Dashboard')
wd.get_range('A1:H1').merge();wd.get_range('A1').values=[['BANGLADESH → EU  |  CN8 EMPIRICAL VALIDATION']]
wd.get_range('A1:H1').format={'fill':NAVY,'font':{'bold':True,'color':WHITE,'size':16},'row_height':38}
wd.get_range('A2:H2').merge();wd.get_range('A2').values=[['Source: uploaded DS-059322 annual CN8 file | 2012–2025 | 27,780 observed records']]
wd.get_range('A2:H2').format={'fill':LIGHT,'font':{'color':INK,'size':11},'row_height':26}
for a,b in [('A4','2025 CN8 import value (EUR)'),('D4','2025 chapters 61–63 (%)'),
            ('A6','Total CN8 observations'),('D6','Distinct CN8 codes'),
            ('A8','2012–2025 CN8 sum (EUR)'),('D8','14-year CN8 to TOTAL gap (EUR)'),
            ('A10','2025 product HHI (0–10,000)'),('D10','2025 Top 200 basket share (%)'),
            ('A12','2025 annual change (%)'),('D12','Rows with leading-zero codes')]:
 wd.get_range(a).values=[[b]]
 wd.get_range(a).format.font.bold=True
for a,f in [('B4','=Annual_Data!D18'),('E4','=Annual_Data!L18'),
 ('B6','=SUM(Annual_Data!B5:B18)'),('E6','=4953'),
 ('B8','=SUM(Annual_Data!D5:D18)'),('E8','=SUM(Annual_Data!F5:F18)'),
 ('B10','=Annual_Data!M18'),('E10','=Annual_Data!P18'),
 ('B12','=100*(Annual_Data!D18/Annual_Data!D17-1)'),('E12','=0')]:
  wd.get_range(a).formulas=[[f]]
wd.get_range('E12').values=[['See audit manifest']]
wd.get_range('B4:B8').set_number_format('#,##0');wd.get_range('E8').set_number_format('#,##0;[Red](#,##0)')
wd.get_range('B10:E12').set_number_format('0.00')
wd.get_range('A14:H14').merge();wd.get_range('A14').values=[['STATUS: CSV row-level integrity PASSED | Official origin/provenance and cross-year CN concordance NOT YET VERIFIED']]
wd.get_range('A14:H14').format={'fill':YELLOW,'font':{'bold':True,'color':RED},'row_height':32}
wd.get_range('A16:H16').merge();wd.get_range('A16').values=[['These are BANGLADESH import-basket values only, not competitors, EU market shares or tariff exposures.']]
wd.get_range('A16:H16').format={'fill':PALE,'font':{'color':INK},'row_height':27}
for col,w in [('A',31),('B',23),('C',4),('D',35),('E',27),('F',13),('G',13),('H',13)]:
 wd.get_range(f'{col}1:{col}23').format.column_width=w
wd.freeze_panes.freeze_rows(2)
# Chart on dashboard below KPIs: standalone years and Euro values from annual sheet
try:
 chart=wd.charts.add('line',{'title':'Bangladesh-origin CN8 imports (EUR), 2012–2025','has_legend':False})
 s=chart.series.add('CN8 value (EUR)')
 s.category_formula="'Annual_Data'!$A$5:$A$18"
 s.formula="'Annual_Data'!$D$5:$D$18"
 chart.set_position('A19','H35')
except Exception as e:
 print('Chart omitted:',type(e).__name__,str(e)[:180])
# Compact verification then export
try:
 print('INSPECT DASHBOARD',wb.inspect({'kind':'table','range':'Dashboard!A4:E12','include':'values,formulas','table_max_rows':10,'table_max_cols':5}).ndjson[:2500])
except Exception as e:print('Inspect note',type(e).__name__,str(e)[:180])
try:
 err=wb.inspect({'kind':'match','search_term':'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A','options':{'use_regex':True,'max_results':15}})
 print('FORMULA ERROR CHECK',err.ndjson[:1600])
except Exception as e:print('Error scan note',type(e).__name__,str(e)[:180])
output=ROOT/'Bangladesh_EU_CN8_RowLevel_Validation_v7.xlsx'
SpreadsheetFile.export_xlsx(wb).save(str(output))
print('EXPORTED',output,output.stat().st_size)
