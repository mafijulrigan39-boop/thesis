#!/usr/bin/env python3
"""Task C: obtain official Eurostat Comext DS-045409 CN8 year x ALL partners.
One frozen 2025 product set, 2012–2025, fixed EU27_2020 reporter, import flow 1.
No implicit zeros. Preserve raw responses and hashes. Refuse unsupported shares.
"""
from __future__ import annotations
import csv, gzip, hashlib, io, json, pathlib, time, urllib.error, urllib.parse, urllib.request
from collections import Counter,defaultdict
from datetime import datetime,timezone
from decimal import Decimal,InvalidOperation

ROOT=pathlib.Path("task_c_competitor_data")
INPUT=pathlib.Path("cn8_harmonization_2012_2025/cn8_2025_exact.csv")
BASE="https://ec.europa.eu/eurostat/api/comext/dissemination/sdmx/2.1/data/DS-045409/"
DSET="DS-045409"
CORE=["BD","CN","IN","VN","PK","KH","TR"]
EXTRA="EXT_EU27_2020"
EU27=set("AT BE BG HR CY CZ DK EE FI FR DE EL HU IE IT LV LT LU MT NL PL PT RO SK SI ES SE".split())
# Valid country origins, including EU's EL and Kosovo XK, as distinct from Comext aggregates.
ISO2=set("""AD AE AF AG AI AL AM AO AQ AR AS AT AU AW AX AZ BA BB BD BE BF BG BH BI BJ BL BM BN BO BQ BR BS BT BV BW BY BZ CA CC CD CF CG CH CI CK CL CM CN CO CR CU CV CW CX CY CZ DE DJ DK DM DO DZ EC EE EG EH ER ES ET FI FJ FK FM FO FR GA GB GD GE GF GG GH GI GL GM GN GP GQ GR GS GT GU GW GY HK HM HN HR HT HU ID IE IL IM IN IO IQ IR IS IT JM JO JP KE KG KH KI KM KN KP KR KW KY KZ LA LB LC LI LK LR LS LT LU LV LY MA MC MD ME MF MG MH MK ML MM MN MO MP MQ MR MS MT MU MV MW MX MY MZ NA NC NE NF NG NI NL NO NP NR NU NZ OM PA PE PF PG PH PK PL PM PN PR PS PT PW PY QA RE RO RS RU RW SA SB SC SD SE SG SH SI SJ SK SL SM SN SO SR SS ST SV SX SY SZ TC TD TF TG TH TJ TK TL TM TN TO TR TT TV TW TZ UA UG UM US UY UZ VA VC VE VG VI VN VU WF WS YE YT ZA ZM ZW XK EL""".split())
def stamp():return datetime.now(timezone.utc).isoformat()
def sha(raw):return hashlib.sha256(raw).hexdigest()
def csvwrite(path,fieldnames,rows):
  path.parent.mkdir(parents=True,exist_ok=True)
  with path.open("w",newline="",encoding="utf-8") as handle:
    writer=csv.DictWriter(handle,fieldnames=fieldnames,extrasaction="ignore");writer.writeheader();writer.writerows(rows)
def load_products():
  with INPUT.open(encoding="utf-8-sig",newline="") as f:
    rows=list(csv.DictReader(f))
  for row in rows:
    assert len(row['PRODUCT'])==8 and row['PRODUCT'].isdigit()
  rows=[r for r in rows if Decimal(r['OBS_VALUE_EUR'])>0]
  rows.sort(key=lambda r:(-Decimal(r['OBS_VALUE_EUR']),r['PRODUCT']))
  top=rows[:200]
  assert len(top)==200 and top[0]['PRODUCT']=='61091000'
  return top
def retrieve(url,dest,receipts,year,chunk):
  entry={'year':year,'chunk':chunk,'url':url,'retrieved_utc':stamp(),'http_status':'','sha256':'','bytes':'','error':''}
  if dest.exists():
    content=gzip.decompress(dest.read_bytes())
    entry.update({'http_status':200,'sha256':sha(content),'bytes':len(content),'cached':True})
    receipts.append(entry);return content
  for attempt in range(1,4):
    try:
      req=urllib.request.Request(url,headers={'User-Agent':'MITB-University-of-Dhaka-academic-trade-research/1.0','Accept':'text/csv,*/*'})
      with urllib.request.urlopen(req,timeout=100) as response:
        data=response.read(120_000_000)
        entry['http_status']=response.status
        entry['content_type']=response.headers.get('Content-Type','')
        entry['etag']=response.headers.get('ETag','')
      if b'TIME_PERIOD' not in data[:1500] or b'OBS_VALUE' not in data[:1500]:
        raise ValueError('No SDMX CSV columns: '+repr(data[:200]))
      dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(gzip.compress(data,compresslevel=7))
      entry.update({'sha256':sha(data),'bytes':len(data),'attempts':attempt})
      receipts.append(entry);return data
    except Exception as exc:
      entry.update({'error':type(exc).__name__+': '+str(exc)[:300],'attempts':attempt})
      if attempt<3:time.sleep(3*attempt)
  receipts.append(entry);return None
def ingest(data,year,requested,store,issues):
  reader=csv.DictReader(io.StringIO(data.decode('utf-8-sig')))
  expected={'TIME_PERIOD','OBS_VALUE','product','partner','reporter','flow','freq','indicators'}
  if not expected.issubset(set(reader.fieldnames or [])):
    raise ValueError('Unexpected Comext header: '+str(reader.fieldnames))
  n=0;codes=set(requested)
  for row in reader:
    if (row['TIME_PERIOD']!=str(year) or row['reporter']!='EU27_2020' or
        row['flow']!='1' or row['freq']!='A' or row['indicators']!='VALUE_IN_EUROS'):
      raise ValueError('Unexpected series: '+repr(row))
    if row['product'] not in codes:raise ValueError('Unrequested CN8 in response')
    try:v=Decimal(row['OBS_VALUE'])
    except (InvalidOperation,TypeError):raise ValueError('Non-numeric trade value')
    if v<0:raise ValueError('Negative trade value')
    key=(str(year),row['product'],row['partner'])
    if key in store:raise ValueError('Duplicate product-year-partner '+str(key))
    store[key]=int(v) if v==int(v) else str(v)
    n+=1
  return n
def main():
  top=load_products()
  products=[r['PRODUCT'] for r in top]
  ROOT.mkdir(parents=True,exist_ok=True)
  csvwrite(ROOT/'product_selection_2025.csv',['rank','cn8','bangladesh_value_2025_ds045409_eur','selection_source'],[
    {'rank':i+1,'cn8':r['PRODUCT'],'bangladesh_value_2025_ds045409_eur':r['OBS_VALUE_EUR'],'selection_source':str(INPUT)}
    for i,r in enumerate(top)])
  store={};receipts=[]; issues=[]; coverage=[]
  for year in range(2025,2011,-1):
    n=0
    for idx in range(0,len(products),10):
      codes=products[idx:idx+10];name=f'{year}_{idx//10+1:02d}'
      key="A.EU27_2020.."+('+'.join(codes))+".1.VALUE_IN_EUROS"
      query=urllib.parse.urlencode({'format':'SDMX-CSV','startPeriod':year,'endPeriod':year})
      url=BASE+key+'?'+query
      raw=retrieve(url,ROOT/'raw'/str(year)/(name+'.csv.gz'),receipts,year,name)
      if raw is None:
        issues.append({'year':year,'chunk':name,'issue':'REQUEST_FAILED','details':receipts[-1]['error']})
      else:
        try:
          got=ingest(raw,year,codes,store,issues)
          n+=got
        except Exception as exc:
          issues.append({'year':year,'chunk':name,'issue':'VALIDATION_FAILED','details':str(exc)})
      time.sleep(0.6)
    coverage.append({'year':year,'requested_products':len(products),'all_partner_observations':n,
        'failed_chunk_count':sum(a['year']==year for a in issues)})
    print('year',year,'records',n,'issues',coverage[-1]['failed_chunk_count'],flush=True)
  csvwrite(ROOT/'request_receipts.csv',['year','chunk','url','retrieved_utc','http_status','sha256','bytes','content_type','etag','attempts','cached','error'],receipts)
  csvwrite(ROOT/'coverage_by_year.csv',['year','requested_products','all_partner_observations','failed_chunk_count'],coverage)
  csvwrite(ROOT/'request_issues.csv',['year','chunk','issue','details'],issues)
  allrows=[{'year':int(y),'cn8':p,'origin':origin,'value_eur':value} for (y,p,origin),value in sorted(store.items())]
  # A separate gzip CSV preserves every original country, aggregate, and special partner value.
  rawtext=io.StringIO();wr=csv.DictWriter(rawtext,fieldnames=['year','cn8','origin','value_eur']);wr.writeheader();wr.writerows(allrows)
  (ROOT/'all_partner_product_year_values.csv.gz').write_bytes(gzip.compress(rawtext.getvalue().encode('utf-8'),compresslevel=6))
  selected=[];shares=[];supplier=[];five=[];denominator_issues=[]
  for year in range(2012,2026):
    for p in products:
      d={(origin):value for (y,pr,origin),value in store.items() if y==str(year) and pr==p}
      ext=d.get(EXTRA);bd=d.get('BD')
      ext_decimal=Decimal(str(ext)) if ext is not None else None
      bd_decimal=Decimal(str(bd)) if bd is not None else None
      possible_issue=any(a['year']==year and int(a['chunk'].split('_')[-1])==products.index(p)//10+1 for a in issues)
      if possible_issue: denom_status='SOURCE_CHUNK_FAILED'
      elif ext_decimal is None:denom_status='NO_REPORTED_EXTRA_EU_AGGREGATE'
      elif ext_decimal==0:denom_status='ZERO_EXTRA_EU_DENOMINATOR'
      elif bd_decimal is None:denom_status='NO_REPORTED_BANGLADESH_VALUE'
      elif bd_decimal>ext_decimal:denom_status='BD_EXCEEDS_EXTRA_EU'
      else: denom_status='OK'
      shares.append({'year':year,'cn8':p,'bd_value_eur':str(bd) if bd is not None else '',
        'extra_eu_value_eur':str(ext) if ext is not None else '',
        'bd_share_extra_eu_percent':str(100*bd_decimal/ext_decimal) if denom_status=='OK' else '',
        'status':denom_status})
      if denom_status!='OK':denominator_issues.append({'year':year,'cn8':p,'reason':denom_status})
      for origin in CORE:
        val=d.get(origin)
        selected.append({'year':year,'cn8':p,'origin':origin,'value_eur':str(val) if val is not None else '',
          'status':'OBSERVED' if val is not None else ('SOURCE_CHUNK_FAILED' if possible_issue else 'NO_REPORTED_RECORD'),
          'dataset':DSET,'reporter':'EU27_2020','flow':'1','frequency':'A','indicator':'VALUE_IN_EUROS'})
      if year==2025:
        candidates=[(k,Decimal(str(v))) for k,v in d.items() if k in ISO2 and k not in EU27 and k!='GR']
        candidates.sort(key=lambda pair:(-pair[1],pair[0]))
        othersum=sum((value for _,value in candidates),Decimal(0))
        supplier.append({'year':year,'cn8':p,'extra_eu_value_eur':str(ext) if ext is not None else '',
          'sum_identified_non_eu_country_values_eur':str(othersum),'residual_extra_eu_eur':str(ext_decimal-othersum) if ext_decimal is not None else '',
          'supplier_count':len(candidates),'supplier_hhi_status':'NOT_CERTIFIED_WHERE_RESIDUAL_OR_UNSPECIFIED_ORIGINS_PRESENT'})
        for rank,(origin,val) in enumerate(candidates[:5],1):
          five.append({'year':year,'cn8':p,'supplier_rank':rank,'origin':origin,'value_eur':str(val),
            'share_of_extra_eu_percent':str(100*val/ext_decimal) if ext_decimal and val<=ext_decimal else '',
            'rank_basis':'All named non-EU country-origin records (excludes aggregates; residual may remain)'})
  csvwrite(ROOT/'seven_origin_panel.csv',['year','cn8','origin','value_eur','status','dataset','reporter','flow','frequency','indicator'],selected)
  csvwrite(ROOT/'bd_extra_eu_market_shares.csv',['year','cn8','bd_value_eur','extra_eu_value_eur','bd_share_extra_eu_percent','status'],shares)
  csvwrite(ROOT/'top5_non_eu_supplier_per_product_2025.csv',['year','cn8','supplier_rank','origin','value_eur','share_of_extra_eu_percent','rank_basis'],five)
  csvwrite(ROOT/'supplier_denominator_audit_2025.csv',['year','cn8','extra_eu_value_eur','sum_identified_non_eu_country_values_eur','residual_extra_eu_eur','supplier_count','supplier_hhi_status'],supplier)
  csvwrite(ROOT/'unresolved_denominator.csv',['year','cn8','reason'],denominator_issues)
  n2025valid=sum(r['status']=='OK' for r in shares if r['year']==2025)
  summary={'generated_utc':stamp(),'dataset':DSET,'reference_snapshot':'November 2026','reporter':'EU27_2020','flow':'1','indicator':'VALUE_IN_EUROS',
    'product_selection':'200 largest positive Bangladesh observations in 2025 native CN8 from repo CN8 exact file',
    'years':'2012-2025','raw_response_count':sum(bool(x['sha256']) for x in receipts),'requested_response_count':280,
    'all_partner_records':len(store),'complete_requests':len(issues)==0,'valid_market_share_product_years':sum(x['status']=='OK' for x in shares),
    'requested_share_product_years':len(shares),'valid_2025_shares':n2025valid,'requested_2025_shares':200,'source_failures':issues,
    'years_with_unverified_cn8_historical_meaning':'2012-2024','missingness':'Blank is not zero, including no reported origin/partner record',
    'cross_origin_comparability':'All values use DS-045409 same reporter/flow/frequency/indicator',
    'origin_ranking_limit':'Origin country list excludes intra-EU and aggregates; residual extra-EU country allocation separately audited',
    'authenticated':'Official HTTP source responses captured by GitHub runner, hashes stored in request_receipts.csv'}
  (ROOT/'source_validation_manifest.json').write_text(json.dumps(summary,indent=2))
  print(json.dumps({k:v for k,v in summary.items() if k not in ('source_failures',)},indent=2),flush=True)
  # Fail overall run only if all requests fail; incomplete requests are logged, not disguised.
  if not store:raise RuntimeError('No official data retrieved')
if __name__=='__main__':main()
