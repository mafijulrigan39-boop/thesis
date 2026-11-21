#!/usr/bin/env python3
"""Task D: live Eurostat DS-045409 quantity data; source-logged and fail-closed.
Universe: Task C 200 selected 2025 CN8 product codes, 2012-2025, all origins.
Quantity in 100KG -> kg * 100. No inferred zeros; suppress invalid denominator.
Supplementary quantity preserved RAW; no EUR/supp unit until officially identified.
"""
import csv,gzip,io,json,hashlib,pathlib,urllib.request,time
from decimal import Decimal,InvalidOperation
from collections import Counter,defaultdict
from datetime import datetime,timezone
ROOT=pathlib.Path('task_d_quantities/full')
SOURCE=pathlib.Path('task_c_competitor_data/full')
CORE=['BD','CN','IN','VN','PK','KH','TR']
IND=['QUANTITY_IN_100KG','SUPPLEMENTARY_QUANTITY']
def utc():return datetime.now(timezone.utc).isoformat()
def sha(x):return hashlib.sha256(x).hexdigest()
def readcsv(path):
    with open(path,newline='',encoding='utf-8-sig') as f:return list(csv.DictReader(f))
def writecsv(path,header,rows):
    path.parent.mkdir(parents=True,exist_ok=True)
    with open(path,'w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=header,extrasaction='ignore');w.writeheader();w.writerows(rows)
def main():
    ROOT.mkdir(parents=True,exist_ok=True)
    codes=[r['cn8'] for r in readcsv(SOURCE/'selected_top200_2025.csv')]
    assert len(codes)==200 and len(set(codes))==200
    # Task C origin/value records: exactly matching dataset and vintage of quantities.
    source_val={}
    with gzip.open(SOURCE/'all_partners_2012_2025.csv.gz','rt',newline='',encoding='utf-8-sig') as f:
        for r in csv.DictReader(f):
            key=(int(r['year']),r['cn8'],r['origin'])
            assert key not in source_val;source_val[key]=Decimal(r['value_eur'])
    assert len(source_val)==312194
    q={};receipts=[];issues=[]
    for year in range(2025,2011,-1):
        url=('https://ec.europa.eu/eurostat/api/comext/dissemination/sdmx/2.1/data/DS-045409/'
             +'A.EU27_2020..'+'+'.join(codes)+'.1.QUANTITY_IN_100KG+SUPPLEMENTARY_QUANTITY'
             +'?format=SDMX-CSV&startPeriod='+str(year)+'&endPeriod='+str(year))
        entry={'year':year,'url':url,'utc':utc(),'sha256':'','records':0,'http_status':'','error':'','source_raw_path':''}
        for attempt in range(3):
            try:
                req=urllib.request.Request(url,headers={'User-Agent':'MITB-Dhaka-EU-Trade-Academic-Research/1.0'})
                with urllib.request.urlopen(req,timeout=120) as res:
                    data=res.read(90000000);entry['http_status']=res.status;entry['content_type']=res.headers.get('Content-Type','')
                rows=list(csv.DictReader(io.StringIO(data.decode('utf-8-sig'))))
                assert rows and len(rows)>5000
                for r in rows:
                    assert r['reporter']=='EU27_2020' and r['flow']=='1' and r['freq']=='A' and r['TIME_PERIOD']==str(year) and r['product'] in codes and r['indicators'] in IND
                    key=(year,r['product'],r['partner'],r['indicators'])
                    assert key not in q
                    v=Decimal(r['OBS_VALUE']);assert v>=0 and v.is_finite()
                    q[key]=v
                dest=ROOT/'raw'/f'{year}_quantities.csv.gz';dest.parent.mkdir(parents=True,exist_ok=True)
                dest.write_bytes(gzip.compress(data,compresslevel=7))
                entry.update({'sha256':sha(data),'records':len(rows),'bytes':len(data),'source_raw_path':str(dest)})
                print('year',year,'quantity rows',len(rows),flush=True)
                break
            except Exception as e:
                entry['error']=type(e).__name__+': '+str(e)[:300]
                if attempt<2:time.sleep(3*(attempt+1))
        if not entry['sha256']:
            issues.append({'year':year,'error':entry['error']})
        receipts.append(entry)
        time.sleep(.4)
    writecsv(ROOT/'official_quantity_receipts.csv',['year','url','utc','sha256','records','http_status','error','source_raw_path','bytes','content_type'],receipts)
    writecsv(ROOT/'official_quantity_errors.csv',['year','error'],issues)
    panel=[];coverage=[];exclusions=[];supp=[];allrows=[]
    for (year,p,o,k),v in sorted(q.items()):
        allrows.append({'year':year,'cn8':p,'origin':o,'indicator':k,'value':str(v)})
    with gzip.open(ROOT/'all_origin_quantities_2012_2025.csv.gz','wt',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=['year','cn8','origin','indicator','value']);w.writeheader();w.writerows(allrows)
    for year in range(2012,2026):
        count=Counter()
        for p in codes:
            for o in CORE:
                key=(year,p,o)
                val=source_val.get(key)
                m100=q.get((*key,'QUANTITY_IN_100KG'))
                supplemental=q.get((*key,'SUPPLEMENTARY_QUANTITY'))
                masskg=m100*100 if m100 is not None else None
                if val is None:
                    status='NO_REPORTED_TRADE_VALUE'
                elif m100 is None:
                    status='NO_REPORTED_NET_MASS'
                elif masskg==0:
                    status='ZERO_NET_MASS'
                elif val<0 or masskg<0:
                    status='INVALID_NEGATIVE'
                else:
                    status='VALID_EUR_PER_KG'
                if status=='VALID_EUR_PER_KG':
                    unitvalue=val/masskg
                else:
                    unitvalue=None
                    exclusions.append({'year':year,'cn8':p,'origin':o,'reason':status,'value_eur':str(val) if val is not None else '',
                      'netmass_kg':str(masskg) if masskg is not None else ''})
                count[status]+=1
                row={'year':year,'cn8':p,'origin':o,'value_eur':str(val) if val is not None else '',
                    'mass_100kg':str(m100) if m100 is not None else '',
                    'net_mass_kg':str(masskg) if masskg is not None else '',
                    'eur_per_kg':str(unitvalue) if unitvalue is not None else '',
                    'supplementary_qty_raw':str(supplemental) if supplemental is not None else '',
                    'supplementary_unit_code':'UNVERIFIED',
                    'supplementary_eur_per_unit':'',
                    'status':status,'class_concordance':'2025_NATIVE' if year==2025 else 'YEAR_SPECIFIC_CN8_NOT_HARMONIZED',
                    'dataset':'DS-045409','reporter':'EU27_2020','flow':'1','indicators':'VALUE_IN_EUROS|QUANTITY_IN_100KG|SUPPLEMENTARY_QUANTITY'}
                panel.append(row)
                if supplemental is not None:supp.append({'year':year,'cn8':p,'origin':o,'raw_quantity':str(supplemental),'unit_code':'UNVERIFIED'})
        coverage.append({'year':year,'expected_origin_cells':1400,'valid_eur_kg':count['VALID_EUR_PER_KG'],
            'no_value':count['NO_REPORTED_TRADE_VALUE'],'no_mass':count['NO_REPORTED_NET_MASS'],
            'zero_mass':count['ZERO_NET_MASS'],'invalid_negative':count['INVALID_NEGATIVE'],
            'supp_quantity_cells':sum(q.get((year,p,o,'SUPPLEMENTARY_QUANTITY')) is not None for p in codes for o in CORE)})
    fields=['year','cn8','origin','value_eur','mass_100kg','net_mass_kg','eur_per_kg','supplementary_qty_raw',
        'supplementary_unit_code','supplementary_eur_per_unit','status','class_concordance','dataset','reporter','flow','indicators']
    writecsv(ROOT/'seven_origin_quantity_unit_value_2012_2025.csv',fields,panel)
    writecsv(ROOT/'unit_value_exclusions.csv',['year','cn8','origin','reason','value_eur','netmass_kg'],exclusions)
    writecsv(ROOT/'coverage_by_year.csv',['year','expected_origin_cells','valid_eur_kg','no_value','no_mass','zero_mass','invalid_negative','supp_quantity_cells'],coverage)
    writecsv(ROOT/'supplementary_quantities_UNVERIFIED_UNITS.csv',['year','cn8','origin','raw_quantity','unit_code'],supp)
    # 2025 relative positioning only: exact same CN8 and year, compared with country value/mass.
    relative=[];vindex={(r['year'],r['cn8'],r['origin']):r for r in panel}
    for p in codes:
        bd=vindex[(2025,p,'BD')]
        bd_uv=Decimal(bd['eur_per_kg']) if bd['eur_per_kg'] else None
        for o in CORE[1:]:
            other=vindex[(2025,p,o)]
            other_uv=Decimal(other['eur_per_kg']) if other['eur_per_kg'] else None
            ok=(bd_uv is not None and other_uv is not None and other_uv>0)
            relative.append({'year':2025,'cn8':p,'comparison_origin':o,
                'bd_eur_per_kg':str(bd_uv) if bd_uv is not None else '',
                'competitor_eur_per_kg':str(other_uv) if other_uv is not None else '',
                'bd_to_competitor_unit_value_ratio':str(bd_uv/other_uv) if ok else '',
                'status':'COMPARABLE_SAME_CN8_SAME_YEAR_KG' if ok else 'EXCLUDED_MISSING_OR_ZERO_UNIT_VALUE'})
    writecsv(ROOT/'relative_unit_values_2025.csv',['year','cn8','comparison_origin','bd_eur_per_kg',
        'competitor_eur_per_kg','bd_to_competitor_unit_value_ratio','status'],relative)
    summary={'source_dataset':'DS-045409','dataset_last_update':'from response, see raw files','date_utc':utc(),
       'reporter':'EU27_2020','flow':'1','years':'2012-2025','product_scope':200,'origin_scope':CORE,
       'quantity_observations':len(q),'quantity_requests':len(receipts),'successful_requests':sum(bool(r['sha256']) for r in receipts),
       'request_failures':issues,'seven_origin_expected':len(panel),
       'valid_eur_per_kg':sum(x['status']=='VALID_EUR_PER_KG' for x in panel),
       'invalid_or_unreported':len(exclusions),'supplementary_raw_observations':len(supp),
       'valid_2025_relative_pairs':sum(r['status']=='COMPARABLE_SAME_CN8_SAME_YEAR_KG' for r in relative),
       'relative_pairs_total':len(relative),
       'supp_unit_policy':'No supplementary unit-price calculated until matched units are documented',
       'missing_policy':'Unreported is not zero','historical_policy':'Unharmonized CN8 across years: no raw-code CAGR or causal interpretation'}
    (ROOT/'SOURCE_QA_SUMMARY.json').write_text(json.dumps(summary,indent=2))
    print(json.dumps(summary,indent=2),flush=True)
    if issues:raise RuntimeError('Not all official annual quantity responses retrieved')
if __name__=='__main__':main()
