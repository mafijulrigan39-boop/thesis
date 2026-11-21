#!/usr/bin/env python3
"""Row-level audit and purely descriptive ranking for user-supplied Eurostat Easy Comext CN8 CSV.

No network calls. Does NOT verify Eurostat authenticity, cross-year product concordance,
market share, tariffs, rules of origin, or competitor values. Missing codes stay missing.
Usage: python validate_and_rank_cn8.py --input /path/to/eu_imports_bangladesh_cn8_2012_2025.csv --out /path/to/output
"""
from __future__ import annotations
import argparse, csv, hashlib, json, re, collections, datetime
from decimal import Decimal
from pathlib import Path

YEARS=list(range(2012,2026))
# Official aggregate totals AS REPORTED BY THE USER/CODEX, not independently downloaded.
REPORTED_TOTAL={2012:8190980243,2013:9115978459,2014:10421299379,2015:12715949830,
2016:13779755619,2017:14251416207,2018:15201621962,2019:16291646246,
2020:13532808957,2021:15735974326,2022:23990994617,2023:18944474058,
2024:19925531672,2025:21244359364}
FIXED={'DATASET':'DS-059322','FREQ':'A','REPORTER':'EU27_2020','PARTNER':'BD',
       'FLOW':'1','STAT_PROCEDURE':'T','INDICATORS':'VALUE_IN_EUR'}
REQUIRED=['DATASET','FREQ','REPORTER','PARTNER','PRODUCT','FLOW','STAT_PROCEDURE','INDICATORS','TIME_PERIOD','OBS_VALUE']
CN8=re.compile(r'^[0-9]{8}$')

def csv_out(out, name, cols, rows):
 p=out/name
 with p.open('w',newline='',encoding='utf-8') as f:
  w=csv.writer(f);w.writerow(cols);w.writerows(rows)
 return p

def process(inp:Path,out:Path,independent:Path|None=None):
 out.mkdir(parents=True,exist_ok=True)
 source_hash=hashlib.sha256(inp.read_bytes()).hexdigest()
 by_year:dict[int,dict[str,int]]={y:{} for y in YEARS}; by_product=collections.defaultdict(dict)
 duplicate=[]; invalid=[]; fixed_anomalies=[]; zero_rows=0; leading_zero=0; rows_count=0; missing_values=[]
 with inp.open(newline='',encoding='utf-8-sig') as f:
  rd=csv.DictReader(f)
  if not rd.fieldnames or not set(REQUIRED).issubset(rd.fieldnames):
   raise ValueError('Missing required source columns: '+str(set(REQUIRED)-set(rd.fieldnames or [])))
  for line,row in enumerate(rd,start=2):
   rows_count+=1
   for k,want in FIXED.items():
    if row[k]!=want:fixed_anomalies.append([line,k,row[k],want])
   code=row['PRODUCT']; raw=row['OBS_VALUE'].strip(); yr=row['TIME_PERIOD']
   if not CN8.fullmatch(code):invalid.append([line,code]);continue
   if code.startswith('0'):leading_zero+=1
   if not re.fullmatch(r'\d+',raw):
    if not raw:missing_values.append(line)
    else:invalid.append([line,'bad value '+repr(raw)])
    continue
   if not re.fullmatch(r'\d{4}',yr) or int(yr) not in YEARS:invalid.append([line,'bad year '+repr(yr)]);continue
   y=int(yr);value=int(raw)
   if code in by_year[y]:duplicate.append([y,code,line])
   by_year[y][code]=value;by_product[code][y]=value
   if value==0:zero_rows+=1
 if duplicate or invalid or fixed_anomalies or missing_values:
  raise ValueError(f'Validation failed: duplicates {len(duplicate)}, invalid {len(invalid)}, fixed fields {len(fixed_anomalies)}, blank values {len(missing_values)}')
 assert rows_count==sum(len(x) for x in by_year.values())
 independent_map={}
 if independent and independent.exists():
  with independent.open(newline='',encoding='utf-8-sig') as f:
   for row in csv.DictReader(f):independent_map[int(row['YEAR'])]=row
 sums={y:sum(d.values()) for y,d in by_year.items()}
 total_years=sum(sums.values()); code_period={c:sum(v.values()) for c,v in by_product.items()}
 annual=[];code_changes=[];chapteryear=[];independent_compare=[]
 for y in YEARS:
  v=by_year[y];s=sums[y];positive=sorted(v.values(),reverse=True)
  hhi=10000*sum((value/s)**2 for value in v.values()) if s else None
  gap=s-REPORTED_TOTAL[y];prev_codes=set(by_year[y-1]) if y>2012 else set()
  new_codes=len(set(v)-prev_codes) if y>2012 else ''
  retired_codes=len(prev_codes-set(v)) if y>2012 else ''
  sect={c:sum(val for code,val in v.items() if code[:2]==c) for c in ('61','62','63')}
  annual.append([y,len(v),sum(x==0 for x in v.values()),s,REPORTED_TOTAL[y],gap,
                 100*gap/REPORTED_TOTAL[y],sect['61'],sect['62'],sect['63'],sum(sect.values()),
                 100*sum(sect.values())/s,round(hhi,8),
                 100*sum(positive[:10])/s,100*sum(positive[:50])/s,100*sum(positive[:200])/s,
                 new_codes,retired_codes])
  code_changes.append([y,len(v),new_codes,retired_codes,sum(x==0 for x in v.values())])
  ch=collections.defaultdict(int)
  for code,value in v.items():ch[code[:2]]+=value
  chapteryear.extend([[y,k,val,100*val/s] for k,val in sorted(ch.items())])
  if y in independent_map:
   row=independent_map[y]
   independent_compare.append([y,len(v),int(row['CN8_ROWS']),len(v)-int(row['CN8_ROWS']),
        s,int(row['CN8_SUM_EUR']),s-int(row['CN8_SUM_EUR']),
        REPORTED_TOTAL[y],int(row['REPORTED_TOTAL_EUR']),REPORTED_TOTAL[y]-int(row['REPORTED_TOTAL_EUR']),
        'DS-059322 procedure T versus DS-045409; extraction definitions and source vintage not independently reconciled'])
 annual_cols=['year','cn8_rows','explicit_zero_rows','cn8_sum_eur','codex_reported_total_eur','cn8_minus_total_eur','cn8_minus_total_pct',
              'hs61_eur','hs62_eur','hs63_eur','hs61_63_eur','hs61_63_share_pct','cn8_hhi_0_to_10000',
              'top10_share_pct','top50_share_pct','top200_share_pct','newly_seen_vs_prior_year','not_seen_vs_prior_year']
 csv_out(out,'annual_integrity_and_concentration_2012_2025.csv',annual_cols,annual)
 csv_out(out,'chapter_by_year_descriptive.csv',['year','hs2_chapter','import_value_eur','share_within_available_cn8_pct'],chapteryear)
 if independent_compare:
  csv_out(out,'ds059322_vs_ds045409_comparison.csv',
   ['year','ds059322_cn8_rows','ds045409_reported_cn8_rows','row_count_difference','ds059322_cn8_sum_eur',
    'ds045409_reported_cn8_sum_eur','cn8_sum_difference_eur','codex_reported_total_eur',
    'ds045409_reported_total_eur','reported_total_difference_eur','interpretation'],independent_compare)
 # Latest-year ranking: strictly observed 2025 CN8 codes (no imputation).
 rank_2025=sorted(by_year[2025].items(), key=lambda kv:(-kv[1],kv[0]));latest=[]
 for idx,(code,value) in enumerate(rank_2025[:200],start=1):
  years=by_product[code];last=years.get(2024);v2012=years.get(2012)
  yoy=(100*(value/last-1)) if last and last>0 else ''
  latest.append([idx,code,code[:2],value,100*value/sums[2025],last if last is not None else '',
    yoy,v2012 if v2012 is not None else '',len(years),code_period[code],
    'Not verified; do not infer same CN8 definition through time'])
 latest_cols=['rank_2025','cn8_code_TEXT','hs2_chapter','value_2025_eur','share_of_bd_2025_cn8_pct',
    'value_2024_eur_if_reported','raw_code_2024_to_2025_yoy_pct_unharmonized',
    'value_2012_eur_if_reported','observed_year_count','raw_code_period_value_2012_2025_eur',
    'classification_comparability_warning']
 csv_out(out,'top_200_cn8_2025_UNHARMONIZED.csv',latest_cols,latest)
 # period rank: no cross-year concordance, use for exploration only
 period=[]
 for idx,(code,value) in enumerate(sorted(code_period.items(),key=lambda kv:(-kv[1],kv[0]))[:200],start=1):
  years=by_product[code]
  period.append([idx,code,code[:2],value,100*value/total_years,len(years),
    years.get(2025,''), years.get(2012,''),'Raw CN8 code; year-to-year concordance NOT validated'])
 period_cols=['raw_code_period_rank','cn8_code_TEXT','hs2_chapter','period_sum_eur_2012_2025',
    'period_share_of_bd_cn8_pct','observed_year_count','value_2025_eur_if_reported',
    'value_2012_eur_if_reported','classification_comparability_warning']
 csv_out(out,'top_200_raw_code_period_2012_2025_UNHARMONIZED.csv',period_cols,period)
 # Full product-year wide matrix. Blank is missing/not reported, distinct from explicit zero.
 matrix=[]
 for c,values in sorted(by_product.items()):
  matrix.append([c,c[:2],len(values)]+[values.get(y,'') for y in YEARS])
 csv_out(out,'cn8_product_year_matrix_missing_not_zero.csv',['cn8_code_TEXT','hs2_chapter','observed_years']+[f'eur_{y}' for y in YEARS],matrix)
 # Year-specific code coverage is provisional, not official CN validity.
 csv_out(out,'cn8_code_observation_coverage.csv',['cn8_code_TEXT','first_observed','last_observed','observed_years',
       'missing_vs_dataset_years','source_backed_cn8_concordance_status'],[
   [c,min(d),max(d),len(d),14-len(d),'NOT VERIFIED - observation availability is not legal classification validity']
   for c,d in sorted(by_product.items())])
 # Source/audit statement: file observations independently checked, not independently redownloaded.
 manifest={'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'source_file_name':inp.name,'source_file_sha256':source_hash,'source_file_bytes':inp.stat().st_size,
 'source_is_user_supplied':True,'original_eurostat_export_or_receipt_verified':False,
 'all_columns_present':True,'schema_expected':REQUIRED,'fixed_filters':FIXED,
 'actual_cn8_rows':rows_count,'years':YEARS,'distinct_cn8_codes':len(by_product),
 'duplicates':len(duplicate),'invalid_cn8_or_value_or_year':len(invalid),'fixed_dim_anomalies':len(fixed_anomalies),
 'explicit_zeros':zero_rows,'leading_zero_code_rows':leading_zero,
 'annual_reconciliation_source':'Codex-reported TOTAL figures quoted in prior messages, not downloaded in this environment',
 'other_input_reconciliation':'DS-045409 independently reported 14-year summary without raw responses',
 'cannot_calculate':['EU product market shares','competitor rankings','CN8 concordances','net mass','supplementary units',
  'relative unit values','country-specific tariff rates','rules of origin compliance','tariff-cost exposure',
  'Article 33 denominator or ratio','causal economic impact']}
 (out/'audit_manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
 all_gap=sum(x[5] for x in annual);all_official=sum(REPORTED_TOTAL.values());annual_diffs=sum((x[6] for x in annual))
 results={'manifest':manifest,'annual':annual,'annual_cols':annual_cols,'latest':latest,'latest_cols':latest_cols,
          'period':period,'period_cols':period_cols,'chapter':chapteryear,'independent_compare':independent_compare,
          'period_cn8_sum':total_years,'period_reported_total':all_official,'period_gap':all_gap,
          'period_gap_pct':100*all_gap/all_official,'latest_value':sums[2025],
          'latest_growth_pct':100*(sums[2025]/sums[2024]-1),
          '2025_hs61_63_pct':100*sum(int(v) for v in [annual[-1][7],annual[-1][8],annual[-1][9]])/sums[2025],
          '2025_hhi':annual[-1][12],
          'codes_14_yrs':sum(len(d)==14 for d in by_product.values()),
          'codes_one_year':sum(len(d)==1 for d in by_product.values())}
 (out/'key_metrics.json').write_text(json.dumps({k:v for k,v in results.items() if k not in ('latest','period','annual','chapter','independent_compare')},indent=2),encoding='utf-8')
 print(json.dumps({k:results[k] for k in ('period_cn8_sum','period_reported_total','period_gap','period_gap_pct',
 'latest_value','latest_growth_pct','2025_hs61_63_pct','2025_hhi','codes_14_yrs','codes_one_year')},indent=2))
 return results

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--input',required=True);p.add_argument('--out',required=True);p.add_argument('--independent')
 a=p.parse_args();process(Path(a.input),Path(a.out),Path(a.independent) if a.independent else None)
