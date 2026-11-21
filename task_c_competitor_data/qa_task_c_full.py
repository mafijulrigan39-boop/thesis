#!/usr/bin/env python3
"""Independent Task C source/hash/market-share audit, with bounded supplier concentration."""
import csv,gzip,hashlib,json,pathlib,re
from collections import defaultdict
from decimal import Decimal
from datetime import datetime,timezone
R=pathlib.Path('task_c_competitor_data/full')
EU=set("AT BE BG HR CY CZ DK EE FI FR DE EL HU IE IT LV LT LU MT NL PL PT RO SK SI ES SE".split())
ISO=set("""AD AE AF AG AI AL AM AO AQ AR AS AT AU AW AX AZ BA BB BD BE BF BG BH BI BJ BL BM BN BO BQ BR BS BT BV BW BY BZ CA CC CD CF CG CH CI CK CL CM CN CO CR CU CV CW CX CY CZ DE DJ DK DM DO DZ EC EE EG EH ER ES ET FI FJ FK FM FO FR GA GB GD GE GF GG GH GI GL GM GN GP GQ GR GS GT GU GW GY HK HM HN HR HT HU ID IE IL IM IN IO IQ IR IS IT JE JM JO JP KE KG KH KI KM KN KP KR KW KY KZ LA LB LC LI LK LR LS LT LU LV LY MA MC MD ME MF MG MH MK ML MM MN MO MP MQ MR MS MT MU MV MW MX MY MZ NA NC NE NF NG NI NL NO NP NR NU NZ OM PA PE PF PG PH PK PL PM PN PR PS PT PW PY QA RE RO RS RU RW SA SB SC SD SE SG SH SI SJ SK SL SM SN SO SR SS ST SV SX SY SZ TC TD TF TG TH TJ TK TL TM TN TO TR TT TV TW TZ UA UG UM US UY UZ VA VC VE VG VI VN VU WF WS YE YT ZA ZM ZW XK EL""".split())
def readcsv(p):
    with p.open(newline='',encoding='utf-8-sig') as f:return list(csv.DictReader(f))
def writecsv(p,fields,records):
    with p.open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(records)
def main():
    issues=[]
    receipts=readcsv(R/'official_request_receipts.csv')
    coverage=readcsv(R/'yearly_coverage.csv')
    selection=readcsv(R/'selected_top200_2025.csv')
    shares=readcsv(R/'product_year_bd_market_share_2012_2025.csv')
    panel=readcsv(R/'seven_origin_2012_2025.csv')
    top5=readcsv(R/'top5_non_eu_suppliers_2025.csv')
    codes={r['cn8'] for r in selection}
    if len(codes)!=200:issues.append('Selection not 200 unique CN8')
    if len(panel)!=19600:issues.append('Seven-origin panel wrong length')
    if len(shares)!=2800:issues.append('Shares wrong length')
    if len(top5)!=1000:issues.append('Top-5 supplier table wrong length')
    yearcount={int(r['year']):0 for r in coverage}
    records={}
    hashcount=0
    for receipt in receipts:
        if not receipt['sha256']:continue
        path=pathlib.Path(receipt['raw_path'])
        if not path.exists():issues.append('Missing raw archive '+str(path));continue
        raw=gzip.decompress(path.read_bytes())
        actual=hashlib.sha256(raw).hexdigest()
        if actual!=receipt['sha256']:issues.append('SHA256 mismatch '+str(path));continue
        hashcount+=1
        rows=list(csv.DictReader(__import__('io').StringIO(raw.decode('utf-8-sig'))))
        if len(rows)!=int(receipt['records']):issues.append('Row count != receipt '+str(path))
        for row in rows:
            if(row['reporter']!='EU27_2020' or row['flow']!='1' or row['freq']!='A' or row['indicators']!='VALUE_IN_EUROS'):
                issues.append('Incorrect series metadata '+str(path));break
            key=(int(row['TIME_PERIOD']),row['product'],row['partner'])
            if key in records:issues.append('Duplicate origin product year '+str(key))
            records[key]=Decimal(row['OBS_VALUE'])
            yearcount[int(row['TIME_PERIOD'])]=yearcount.get(int(row['TIME_PERIOD']),0)+1
    # All raw annual observations backed by sources and hashes
    if hashcount!=14:issues.append(f'Expected 14 raw source archives, verified {hashcount}')
    if len(records)!=312194:issues.append(f'Unexpected raw record count {len(records)}')
    # Check every country-origin row, including true missingness distinction
    seen=set()
    for row in panel:
        key=(int(row['year']),row['cn8'],row['origin'])
        if key in seen:issues.append('Duplicated seven-origin key '+str(key))
        seen.add(key)
        actual=records.get(key)
        if actual is None:
            if row['value_eur'] or row['observation_status']!='NO_REPORTED_RECORD_NOT_ZERO':
                issues.append('Missingness misclassified '+str(key))
        else:
            if not row['value_eur'] or Decimal(row['value_eur'])!=actual or row['observation_status']!='OBSERVED':
                issues.append('Panel source mismatch '+str(key))
    v=0;miss=0;sum2025=Decimal(0);value2025=Decimal(0)
    for row in shares:
        k=(int(row['year']),row['cn8'])
        bd=records.get((*k,'BD'));total=records.get((*k,'EXT_EU27_2020'))
        valid=bd is not None and total is not None and total>0 and bd<=total
        if valid:
            v+=1
            if row['status']!='VALID' or not row['bd_share_of_extra_eu_pct']:
                issues.append('Valid share omitted '+str(k));continue
            if abs(Decimal(row['bd_share_of_extra_eu_pct'])-100*bd/total)>Decimal('.0000001'):
                issues.append('Incorrect share '+str(k))
            if int(row['year'])==2025:sum2025+=bd;value2025+=total
        else:
            miss+=1
            if row['status']=='VALID' or row['bd_share_of_extra_eu_pct']:
                issues.append('Ineligible share assigned '+str(k))
    # Descriptive supplier HHI sensitivity: country partners may not exhaust published extra-EU total
    concentration=[];negative=0;positive=0;near_zero=0
    for p in codes:
        year=2025
        total=records.get((year,p,'EXT_EU27_2020'))
        if total is None or total<=0:continue
        vals=[v for (y,code,origin),v in records.items()
            if y==year and code==p and origin in ISO and origin not in EU and origin!='GR']
        summed=sum(vals,Decimal(0));residual=total-summed;rpct=100*residual/total
        hhi=sum((v/total)**2 for v in vals)*10000
        # Not certified when country total exceeds extraEU total or residual meaningful.
        qualification=('NEEDS_ORIGIN_RECONCILIATION' if residual<0 or abs(rpct)>Decimal('.1')
             else 'PROVISIONAL_NEAR_RECONCILED')
        if residual<0:negative+=1
        elif residual>0:positive+=1
        if abs(rpct)<=Decimal('.1'):near_zero+=1
        concentration.append({'year':year,'cn8':p,'extra_eu_eur':str(total),
            'sum_named_non_eu_eur':str(summed),'unallocated_or_statistical_residual_eur':str(residual),
            'residual_pct':str(rpct),'named_supplier_hhi_on_extra_eu_base':str(hhi),
            'hhi_plus_single_residual_supplier_if_residual_nonnegative':str(hhi+10000*(residual/total)**2) if residual>=0 else '',
            'interpretation':qualification})
    concentration.sort(key=lambda d:(-Decimal(d['named_supplier_hhi_on_extra_eu_base']),d['cn8']))
    writecsv(R/'supplier_concentration_bounded_2025.csv',[
        'year','cn8','extra_eu_eur','sum_named_non_eu_eur','unallocated_or_statistical_residual_eur',
        'residual_pct','named_supplier_hhi_on_extra_eu_base',
        'hhi_plus_single_residual_supplier_if_residual_nonnegative','interpretation'],concentration)
    summary={'qa_utc':datetime.now(timezone.utc).isoformat(),'source':'Official EUROSTAT DS-045409 archived raw responses',
      'passed':not issues,'issues':issues[:100],'source_archive_hashes_verified':hashcount,
      'raw_unique_origin_product_year_records':len(records),
      'seven_origin_panel_rows':len(panel),'market_share_total':len(shares),
      'valid_share_rows':v,'ineligible_share_rows':miss,
      'top5_nonEU_suppliers_rows':len(top5),
      '2025_total_bd_value_selected_products_eur':str(sum2025),
      '2025_total_extraEU_product_values_sum_eur':str(value2025),
      '2025_supplier_hhi_products':len(concentration),
      'products_with_negative_country_sum_residual':negative,'positive_country_sum_residual':positive,
      'near_reconciled_within_0_1_percent':near_zero,
      'analysis_warnings':['No unreported observation is treated as zero',
        'CN8 2012-2024 longitudinal comparability awaits Task B official concordance',
        'Country-origin HHI is provisional where national-origin values do not reconcile to published extraEU aggregates',
        'Selection covers only leading 2025 Bangladesh CN8 products, not every EU CN8 trade product',
        'ExtraEU shares use publisher-provided EXT_EU27_2020 aggregate rather than summed individual origin values']}
    (R/'INDEPENDENT_QA_RESULT.json').write_text(json.dumps(summary,indent=2))
    print(json.dumps({k:v for k,v in summary.items() if k!='issues'},indent=2),flush=True)
    if issues:raise RuntimeError('Independent QA failed: '+str(issues[:10]))
if __name__=='__main__':main()
