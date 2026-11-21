#!/usr/bin/env python3
"""Official Eurostat DS-045409 Task C, EU27_2020 importer, 2012-2025 CN8 all-origin panel.
Extracts all partner-country entries for 200 2025 top Bangladesh product lines. Runs
one request per year (splitting recursively if necessary). Preserves original CSV gzip,
SHA256/URLs, separate missingness, explicit extra-EU denominator. No data simulation.
Historical values require separate year-specific CN8 concordance for economic comparison.
"""
from __future__ import annotations
import csv,gzip,io,json,hashlib,pathlib,urllib.request,urllib.parse,time,re,sys
from collections import defaultdict
from datetime import datetime,timezone
from decimal import Decimal

ROOT=pathlib.Path("task_c_competitor_data/full")
BASE="https://ec.europa.eu/eurostat/api/comext/dissemination/sdmx/2.1/data/DS-045409/"
SOURCE=pathlib.Path("cn8_harmonization_2012_2025/cn8_2025_exact.csv")
FAST=pathlib.Path("task_c_competitor_data/quick2025/response_01.csv.gz")
CORE=['BD','CN','IN','VN','PK','KH','TR']
EU=set("AT BE BG HR CY CZ DK EE FI FR DE EL HU IE IT LV LT LU MT NL PL PT RO SK SI ES SE".split())
ISO=set("""AD AE AF AG AI AL AM AO AQ AR AS AT AU AW AX AZ BA BB BD BE BF BG BH BI BJ BL BM BN BO BQ BR BS BT BV BW BY BZ CA CC CD CF CG CH CI CK CL CM CN CO CR CU CV CW CX CY CZ DE DJ DK DM DO DZ EC EE EG EH ER ES ET FI FJ FK FM FO FR GA GB GD GE GF GG GH GI GL GM GN GP GQ GR GS GT GU GW GY HK HM HN HR HT HU ID IE IL IM IN IO IQ IR IS IT JE JM JO JP KE KG KH KI KM KN KP KR KW KY KZ LA LB LC LI LK LR LS LT LU LV LY MA MC MD ME MF MG MH MK ML MM MN MO MP MQ MR MS MT MU MV MW MX MY MZ NA NC NE NF NG NI NL NO NP NR NU NZ OM PA PE PF PG PH PK PL PM PN PR PS PT PW PY QA RE RO RS RU RW SA SB SC SD SE SG SH SI SJ SK SL SM SN SO SR SS ST SV SX SY SZ TC TD TF TG TH TJ TK TL TM TN TO TR TT TV TW TZ UA UG UM US UY UZ VA VC VE VG VI VN VU WF WS YE YT ZA ZM ZW XK EL""".split())
def utc():return datetime.now(timezone.utc).isoformat()
def sha(x):return hashlib.sha256(x).hexdigest()
def write_csv(path,header,rows):
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=header,extrasaction='ignore');w.writeheader();w.writerows(rows)
def products():
    with SOURCE.open(encoding='utf-8-sig',newline='') as h:orig=list(csv.DictReader(h))
    orig=[r for r in orig if int(r['OBS_VALUE_EUR'])>0]
    orig.sort(key=lambda x:(-int(x['OBS_VALUE_EUR']),x['PRODUCT']))
    assert len(orig)>=200 and orig[0]['PRODUCT']=='61091000'
    return orig[:200]
def parse(raw,yr,requested,store):
    reader=csv.DictReader(io.StringIO(raw.decode('utf-8-sig')))
    required={'partner','product','reporter','flow','freq','indicators','TIME_PERIOD','OBS_VALUE'}
    if not required.issubset(reader.fieldnames or []):raise ValueError('Invalid SDMX CSV header')
    n=0
    for r in reader:
        if (r['TIME_PERIOD']!=str(yr) or r['reporter']!='EU27_2020' or
            r['flow']!='1' or r['freq']!='A' or r['indicators']!='VALUE_IN_EUROS'):
            raise ValueError('Series definition differs from requested series')
        if r['product'] not in requested:raise ValueError('Unexpected product '+r['product'])
        val=Decimal(r['OBS_VALUE'])
        if val<0:raise ValueError('Negative import value')
        key=(yr,r['product'],r['partner'])
        if key in store:raise ValueError('Duplicate EU origin product-year record '+str(key))
        store[key]=int(val) if val==int(val) else str(val)
        n+=1
    return n
def retrieve(year,codes,receipts,store,issue_log,source_archive_index):
    key='+'.join(codes)
    url=BASE+'A.EU27_2020..'+key+'.1.VALUE_IN_EUROS?'+urllib.parse.urlencode({
        'format':'SDMX-CSV','startPeriod':year,'endPeriod':year})
    attempt={'year':year,'products_requested':len(codes),'url':url,'retrieved_utc':utc(),
        'status':'','http_status':'','sha256':'','bytes':'','records':'','error':'','raw_path':''}
    try:
        if year==2025 and len(codes)==200 and FAST.exists():
            raw=gzip.decompress(FAST.read_bytes());status=200
            attempt['status']='REUSED_VERIFIED_2025_OFFICIAL_RESPONSE'
        else:
            req=urllib.request.Request(url,headers={'User-Agent':'University-of-Dhaka-MITB-Thesis-Eurostat-Comext/1.0'})
            with urllib.request.urlopen(req,timeout=110) as response:raw=response.read(100_000_000);status=response.status
            attempt['status']='HTTP_SUCCESS'
        attempt['http_status']=status
        if b'OBS_VALUE' not in raw[:2000]:raise ValueError('Missing CSV observation column')
        count=parse(raw,year,set(codes),store)
        fname=f"Y{year}_{len(source_archive_index)+1:03d}.csv.gz"
        f=ROOT/'raw'/fname;f.parent.mkdir(parents=True,exist_ok=True);f.write_bytes(gzip.compress(raw,compresslevel=6))
        attempt.update({'sha256':sha(raw),'bytes':len(raw),'records':count,'raw_path':str(f)})
        source_archive_index.append(str(f))
        receipts.append(attempt)
        print(year,'valid',len(codes),'products',count,'records',flush=True)
    except Exception as e:
        attempt.update({'status':'FAILED_OR_SPLIT','error':type(e).__name__+': '+str(e)[:300]})
        receipts.append(attempt)
        if len(codes)>10:
            mid=len(codes)//2
            print(year,'split',len(codes),'due to',str(e)[:160],flush=True)
            retrieve(year,codes[:mid],receipts,store,issue_log,source_archive_index)
            retrieve(year,codes[mid:],receipts,store,issue_log,source_archive_index)
        else:
            issue_log.append({'year':year,'products':'|'.join(codes),'issue':'UNRETRIEVED','details':attempt['error']})
    time.sleep(.4)
def main():
    selected=products();codes=[r['PRODUCT'] for r in selected]
    ROOT.mkdir(parents=True,exist_ok=True)
    write_csv(ROOT/'selected_top200_2025.csv',['rank_2025','cn8','bd_2025_source_eur','selection_file'],[
        {'rank_2025':i+1,'cn8':r['PRODUCT'],'bd_2025_source_eur':r['OBS_VALUE_EUR'],'selection_file':str(SOURCE)}
        for i,r in enumerate(selected)])
    records={};receipts=[];issues=[];archives=[]
    for yr in range(2025,2011,-1):
        retrieve(yr,codes,receipts,records,issues,archives)
    write_csv(ROOT/'official_request_receipts.csv',
        ['year','products_requested','url','retrieved_utc','status','http_status','sha256','bytes','records','error','raw_path'],receipts)
    write_csv(ROOT/'official_retrieval_errors.csv',['year','products','issue','details'],issues)
    values=[{'year':yr,'cn8':p,'origin':o,'value_eur':v} for (yr,p,o),v in sorted(records.items())]
    raw=io.StringIO();writer=csv.DictWriter(raw,fieldnames=['year','cn8','origin','value_eur']);writer.writeheader();writer.writerows(values)
    (ROOT/'all_partners_2012_2025.csv.gz').write_bytes(gzip.compress(raw.getvalue().encode('utf-8'),compresslevel=7))
    seven=[];shares=[];top5=[];supplier_audit=[];missing=[];cover=[]
    for year in range(2012,2026):
        yearvals={p:{} for p in codes}
        for (yr,p,o),v in records.items():
            if yr==year:yearvals[p][o]=v
        yearsummary={'year':year,'products_requested':200,'products_with_bd':0,'products_with_extra_eu_total':0,
                     'products_with_valid_share':0,'all_partner_record_count':sum(len(v) for v in yearvals.values()),'unreported_or_bad_shares':0}
        for p in codes:
            d=yearvals[p];bd=d.get('BD');ex=d.get('EXT_EU27_2020')
            if bd is not None:yearsummary['products_with_bd']+=1
            if ex is not None:yearsummary['products_with_extra_eu_total']+=1
            ok=(bd is not None and ex is not None and Decimal(str(ex))>0 and
                Decimal(str(bd))<=Decimal(str(ex)))
            status='VALID' if ok else ('MISSING_EXTRA_EU_TOTAL' if ex is None else
                'MISSING_BANGLADESH_VALUE' if bd is None else 'INVALID_ZERO_OR_SMALL_DENOMINATOR')
            if ok:yearsummary['products_with_valid_share']+=1
            else:
                yearsummary['unreported_or_bad_shares']+=1
                missing.append({'year':year,'cn8':p,'component':'BD_MARKET_SHARE','reason':status})
            shares.append({'year':year,'cn8':p,'bd_eur':bd if bd is not None else '',
                'extra_eu_eur':ex if ex is not None else '',
                'bd_share_of_extra_eu_pct':str(100*Decimal(str(bd))/Decimal(str(ex))) if ok else '',
                'status':status,'historical_cn8_comparability':'UNCERTIFIED' if year<2025 else '2025_NATIVE'})
            for origin in CORE:
                val=d.get(origin)
                label='OBSERVED' if val is not None else 'NO_REPORTED_RECORD_NOT_ZERO'
                seven.append({'year':year,'cn8':p,'origin':origin,
                    'value_eur':val if val is not None else '','observation_status':label,
                    'dataset':'DS-045409','reporter':'EU27_2020','flow':'1',
                    'indicator':'VALUE_IN_EUROS','historical_cn8_comparability':'UNCERTIFIED' if year<2025 else '2025_NATIVE'})
            if year==2025:
                country_pairs=sorted(((o,Decimal(str(v))) for o,v in d.items()
                    if o in ISO and o not in EU and o!='GR'),key=lambda x:-x[1])
                country_total=sum((v for o,v in country_pairs),Decimal(0))
                residual=Decimal(str(ex))-country_total if ex is not None else None
                supplier_audit.append({'year':year,'cn8':p,'country_records':len(country_pairs),
                    'observed_non_eu_country_sum_eur':str(country_total),
                    'extra_eu_total_eur':ex if ex is not None else '',
                    'residual_extra_eu_minus_countries_eur':str(residual) if residual is not None else '',
                    'residual_pct_extra_eu':str(100*residual/Decimal(str(ex))) if ex else '',
                    'supplier_hhi_approved':'NO_UNTIL_ALL_ORIGIN_RECONCILIATION'})
                for rank,(origin,val) in enumerate(country_pairs[:5],1):
                    top5.append({'year':year,'cn8':p,'rank':rank,'origin':origin,
                        'value_eur':str(val),'share_of_extra_eu_pct':str(100*val/Decimal(str(ex))) if ex else '',
                        'supplier_ranking_scope':'observed_named_non_eu_origins'})
        cover.append(yearsummary)
    write_csv(ROOT/'seven_origin_2012_2025.csv',
        ['year','cn8','origin','value_eur','observation_status','dataset','reporter','flow','indicator','historical_cn8_comparability'],seven)
    write_csv(ROOT/'product_year_bd_market_share_2012_2025.csv',
        ['year','cn8','bd_eur','extra_eu_eur','bd_share_of_extra_eu_pct','status','historical_cn8_comparability'],shares)
    write_csv(ROOT/'top5_non_eu_suppliers_2025.csv',
        ['year','cn8','rank','origin','value_eur','share_of_extra_eu_pct','supplier_ranking_scope'],top5)
    write_csv(ROOT/'supplier_origin_residual_audit_2025.csv',
        ['year','cn8','country_records','observed_non_eu_country_sum_eur','extra_eu_total_eur','residual_extra_eu_minus_countries_eur','residual_pct_extra_eu','supplier_hhi_approved'],supplier_audit)
    write_csv(ROOT/'missingness_market_share_register.csv',['year','cn8','component','reason'],missing)
    write_csv(ROOT/'yearly_coverage.csv',['year','products_requested','products_with_bd',
        'products_with_extra_eu_total','products_with_valid_share','all_partner_record_count','unreported_or_bad_shares'],cover)
    report={'finished_utc':utc(),'dataset':'DS-045409','source':'Official Eurostat Comext filtered SDMX-CSV requests',
        'years':'2012-2025','reporter':'EU27_2020','flow':'1','frequency':'A','indicator':'VALUE_IN_EUROS',
        'selected_products':len(codes),'requested_product_year_pairs':2800,'all_partner_country_and_aggregate_records':len(records),
        'selected_origin_panel_rows':len(seven),'valid_bd_market_shares':sum(x['status']=='VALID' for x in shares),
        'valid_2025_market_shares':sum(x['status']=='VALID' and x['year']==2025 for x in shares),
        'raw_response_files':len(archives),'request_failures':len(issues),
        'raw_hashes_logged':all(x['sha256'] for x in receipts if x['status']!='FAILED_OR_SPLIT'),
        'all_requested_batches_successful':not issues,
        '2025_comparability_status':'2025 native CN8, exact product codes retained',
        'historical_comparability_status':'2012-2024 native CN8 series need official CN concordances before causal or harmonized CAGR analysis',
        'missingness_policy':'No reported origin-value row is a missing record, not observed zero',
        'extra_eu_denominator':'EXT_EU27_2020 published aggregate, not sum of country values'}
    (ROOT/'DATA_QA_SUMMARY.json').write_text(json.dumps(report,indent=2))
    print(json.dumps(report,indent=2),flush=True)
    if not records:raise RuntimeError('No official source records downloaded')
if __name__=='__main__':main()
