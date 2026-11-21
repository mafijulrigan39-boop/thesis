#!/usr/bin/env python3
"""Independent Eurostat Comext raw-data authentication and row-level comparison.

Examples:
 python verify_raw_eurostat_v8.py --input eu_imports_bangladesh_cn8_2012_2025.csv \
     --summary independent_reconciliation.csv --out stage1 --fetch --years 2025
 python verify_raw_eurostat_v8.py --input eu_imports_bangladesh_cn8_2012_2025.csv \
     --summary independent_reconciliation.csv --raw-dir /path/to/raw_ds045409_years \
     --out stage1

NOTE: Only user-supplied files and Eurostat API responses constitute data. No synthetic
records are generated. If DNS/HTTP fails, all output flags remain NOT_AUTHENTICATED.
"""
import argparse,collections,csv,datetime,hashlib,json,pathlib,sys,time
from decimal import Decimal,InvalidOperation
from urllib.parse import urlparse
try: import requests
except ImportError: requests=None

def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(p):
 h=hashlib.sha256()
 with open(p,'rb') as f:
  for chunk in iter(lambda:f.read(1024*1024),b''):h.update(chunk)
 return h.hexdigest()
def int_eur(s):
 try:
  d=Decimal(str(s).strip());
  if not d.is_finite() or d!=d.to_integral_value():raise ValueError('non-integral or infinite euro value')
  return int(d)
 except (InvalidOperation,ValueError):raise ValueError(f'Unexpected EUR value: {s!r}')
def load_user(path):
 data={};meta=collections.defaultdict(set)
 with open(path,encoding='utf-8-sig',newline='') as f:
  dr=csv.DictReader(f)
  for i,r in enumerate(dr,2):
   k=(int(r['TIME_PERIOD']),r['PRODUCT'])
   if len(k[1])!=8 or not k[1].isdigit():raise ValueError(f'Invalid CN8 at line {i}: {k[1]}')
   if k in data:raise ValueError(f'Duplicate {k} in user input')
   data[k]=int_eur(r['OBS_VALUE'])
   for fld in ('DATASET','FREQ','REPORTER','PARTNER','FLOW','STAT_PROCEDURE','INDICATORS'):meta[fld].add(r.get(fld,''))
 return data,{k:sorted(v) for k,v in meta.items()}
def load_official(path,year):
 obs={};totals=[];rows=0;invalid=[];bad_filters=[]
 with open(path,encoding='utf-8-sig',newline='') as f:
  dr=csv.DictReader(f)
  names=dr.fieldnames or []
  for field in ('PRODUCT','TIME_PERIOD','OBS_VALUE'):
   if field not in names:raise ValueError(f'{path} missing field {field}; got {names}')
  for i,r in enumerate(dr,2):
   if r.get('TIME_PERIOD')!=str(year): continue
   if any((k in names and r.get(k)!=v) for k,v in [('REPORTER','EU27_2020'),('PARTNER','BD'),('FLOW','1'),('FREQ','A')]):
    bad_filters.append(i);continue
   if 'INDICATORS' in names and r['INDICATORS'] not in ('VALUE_IN_EUROS','VALUE_IN_EUR'):
    continue
   p=r['PRODUCT'];v=r.get('OBS_VALUE','').strip()
   if not v:invalid.append((i,p,'missing OBS_VALUE'));continue
   value=int_eur(v)
   if p=='TOTAL':totals.append(value)
   elif len(p)==8 and p.isdigit():
    k=(year,p)
    if k in obs:raise ValueError(f'Duplicate official row {k} in {path}')
    if value<0:invalid.append((i,p,'negative'))
    obs[k]=value;rows+=1
  if bad_filters:raise ValueError(f'{len(bad_filters)} official rows do not match EU27_2020/BD/import/annual filter')
  if invalid:raise ValueError(f'Invalid/missing official observations: {invalid[:3]}')
  if len(totals)>1: raise ValueError('More than one official TOTAL row, inspect API dimensions')
 return obs,(totals[0] if totals else None),names

def write_csv(path,head,rows):
 with open(path,'w',encoding='utf-8',newline='') as f:
  wr=csv.writer(f);wr.writerow(head);wr.writerows(rows)

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--input',required=True);ap.add_argument('--summary',required=True);ap.add_argument('--raw-dir');ap.add_argument('--out',default='verification_stage1');ap.add_argument('--fetch',action='store_true');ap.add_argument('--years',nargs='*',type=int,default=list(range(2012,2026)));args=ap.parse_args()
 out=pathlib.Path(args.out);out.mkdir(parents=True,exist_ok=True)
 raw=pathlib.Path(args.raw_dir or str(out/'raw_ds045409'));raw.mkdir(parents=True,exist_ok=True)
 user,usermeta=load_user(args.input)
 summary={}
 with open(args.summary,encoding='utf-8-sig',newline='') as f:
  for r in csv.DictReader(f):summary[int(r['YEAR'])]=r
 logs=[];deltas=[];annual=[];all_verified=True
 for year in args.years:
  if year not in summary:raise ValueError(f'Missing year {year} in reference summary')
  ref=summary[year];url=ref['SOURCE_URL'];path=raw/f'ds045409_{year}.csv'
  log={'year':year,'attempt_utc':now(),'source_url_claimed':url,'summary_claimed_sha256':ref.get('SOURCE_SHA256'),'downloaded_file':str(path),'status':'NO_RAW_SOURCE'}
  if args.fetch:
   if requests is None: log.update(status='REQUESTS_NOT_INSTALLED')
   elif urlparse(url).hostname!='ec.europa.eu':log.update(status='UNTRUSTED_HOST_REFUSED')
   else:
    try:
     r=requests.get(url,timeout=(8,45),headers={'User-Agent':'AcademicEurostatIntegrityVerification/1.0','Accept':'text/csv,*/*'})
     log.update(http_status=r.status_code,content_type=r.headers.get('Content-Type'),response_date=r.headers.get('Date'),response_etag=r.headers.get('ETag'),last_modified=r.headers.get('Last-Modified'))
     r.raise_for_status()
     if b'PRODUCT' not in r.content[:1000] or b'OBS_VALUE' not in r.content[:1000]:raise ValueError('Response not recognized as SDMX-CSV')
     path.write_bytes(r.content);log['status']='DOWNLOADED'
    except Exception as e: log.update(status='HTTP_DNS_OR_FORMAT_FAILED',error=type(e).__name__+': '+str(e)[:500])
  if path.exists():
   log['actual_raw_sha256']=sha(path);log['hash_matches_claimed']=log['actual_raw_sha256']==ref.get('SOURCE_SHA256')
   try:
    official,total,fields=load_official(path,year)
    before={p:v for (y,p),v in user.items() if y==year}
    after={p:v for (y,p),v in official.items() if y==year}
    for p in sorted(set(before)|set(after)):
     old=before.get(p);new=after.get(p)
     if old!=new:deltas.append([year,p,'only_059322' if new is None else ('only_045409' if old is None else 'value_changed'),old,new,None if new is None or old is None else new-old])
    src_sum=sum(after.values());ref_sum=int(ref['CN8_SUM_EUR']);src_count=len(after)
    log.update(status='PARSED_OFFICIAL_RAW',raw_fields=fields,official_cn8_rows=src_count,official_cn8_sum_eur=src_sum,claimed_cn8_rows=int(ref['CN8_ROWS']),claimed_cn8_sum_eur=ref_sum,row_count_claim_matches=src_count==int(ref['CN8_ROWS']),sum_claim_matches=src_sum==ref_sum,official_total_from_response=total)
    if src_count!=int(ref['CN8_ROWS']) or src_sum!=ref_sum:log['status']='RAW_CONFLICTS_WITH_CLAIMED_SUMMARY';all_verified=False
    if total is not None and total!=int(ref['REPORTED_TOTAL_EUR']):log['status']='TOTAL_CONFLICTS_WITH_CLAIMED_SUMMARY';all_verified=False
    annual.append([year,src_count,src_sum,len(before),sum(before.values()),src_count-len(before),src_sum-sum(before.values()),total,log['status']])
   except Exception as e:log.update(status='RAW_PARSE_FAILED',error=repr(e));all_verified=False
  else: all_verified=False
  logs.append(log)
  time.sleep(0.5 if args.fetch else 0)
 write_csv(out/'annual_actual_raw_comparison.csv',['year','ds045409_rows_actual','ds045409_sum_actual_eur','ds059322_rows_actual','ds059322_sum_actual_eur','row_difference','sum_difference_eur','ds045409_total_in_response','validation_status'],annual)
 write_csv(out/'cn8_year_row_differences.csv',['year','product','difference_type','DS059322_eur','DS045409_eur','delta_when_both_present_eur'],deltas)
 (out/'raw_retrieval_log.json').write_text(json.dumps({'created_utc':now(),'all_years_raw_parsed_and_summary_consistent':all_verified,'source_metadata_059322':usermeta,'logs':logs},indent=2)+'\n',encoding='utf-8')
 print(json.dumps({'all_years_verified':all_verified,'raw_years_parsed':len(annual),'differences_by_code':len(deltas),'log_path':str(out/'raw_retrieval_log.json')},indent=2))
 if not all_verified:sys.exit(2)
if __name__=='__main__':main()