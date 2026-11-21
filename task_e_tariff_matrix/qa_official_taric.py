#!/usr/bin/env python3
"""Task E independent source-certification and tariff data QA, fail on inconsistencies."""
import csv,json,pathlib,hashlib,collections,re,datetime
ROOT=pathlib.Path('task_e_tariff_matrix')
A=ROOT/'nov2026';B=ROOT/'refined_v18'
def read(p):
 with p.open(newline='',encoding='utf-8-sig') as f:return list(csv.DictReader(f))
def main():
 failures=[]
 originals=json.loads((A/'source_file_receipts.json').read_text())
 for r in originals:
  p=A/'official_source_xlsx'/r['filename']
  if not p.exists():failures.append('Source missing '+r['filename']);continue
  blob=p.read_bytes()
  if hashlib.sha256(blob).hexdigest()!=r['sha256']:failures.append('Source hash mismatch '+r['filename'])
  if len(blob)!=r['bytes']:failures.append('Source length mismatch '+r['filename'])
  if not r['source_url'].startswith('https://circabc.europa.eu/service/api/node/workspace/SpacesStore/'):
   failures.append('Non official source URL')
 leaves=read(A/'taric10_leaf_mapping.csv')
 conc=read(A/'actual_2026_taric10_origin_matrix.csv')
 raw_candidates=read(A/'all_tariff_measure_candidates_with_conditions.csv')
 origin=read(B/'taric10_country_refined_measure_matrix.csv')
 cn8=read(B/'CN8_country_source_qualified_rate_screen.csv')
 schemes=read(B/'Bangladesh_EBA_StandardGSP_GSPplus_2026_source_templates.csv')
 unmatch=read(A/'unmatched_cn8.csv')
 if len(originals)!=9 or len(leaves)!=321 or len(origin)!=2247 or len(cn8)!=1400 or len(schemes)!=963 or unmatch:
  failures.append('Expected source/coverage matrix shape mismatch')
 keyset=set();originmap={}
 for r in origin:
  key=(r['cn8_2025'],r['taric10_2026'],r['origin'])
  if key in keyset:failures.append('Duplicate tariff10 country row '+str(key))
  keyset.add(key);originmap[key]=r
  if r['source_reference_date']!='2026-11-01':failures.append('Wrong source snapshot date')
  if r['actual_paid_duty']!='NOT_OBSERVED':failures.append('Actual customs paid incorrectly claimed')
  if r['future_2027_2032_duty_status']!='CONDITIONAL_FUTURE_SCENARIO_NOT_OBSERVED':
   failures.append('Future scenario claimed as observed')
  for k in ('mfn_advalorem_pct','preference_advalorem_pct','customs_union_advalorem_pct','lowest_simple_candidate_pct_not_final_duty'):
   if r[k]:
    try:float(r[k])
    except:failures.append('Invalid numeric duty '+str(key)+' '+k)
 # Audit specific exact tariff measures: verify candidate is from source-backed rows
 cindex=collections.defaultdict(list)
 for r in raw_candidates:
  k=(r['cn8_2025'],r['taric10_2026'],r['country'])
  cindex[k].append(r)
 for key,r in originmap.items():
  x=cindex[key]
  for typ,field in [('103','mfn_advalorem_pct'),('142','preference_advalorem_pct'),('106','customs_union_advalorem_pct')]:
   if r[field]:
    if not any(z['measure_type_code']==typ and z['simple_ad_valorem_pct']==r[field]
      and not z['additional_code'] and not z['quota_order_number'] and z['number_of_conditions']=='0' for z in x):
     failures.append('Rate unsupported by exact source candidate '+str(key)+' '+typ)
    if r['candidate_status']=='SIMPLE_RATE_CANDIDATE_UNDER_SCHEME_CONDITIONS' and not r['lowest_simple_candidate_pct_not_final_duty']:
     failures.append('Final simple candidate blank '+str(key))
 # source review: verify tariff treatment group codes for GSP
 sc=collections.Counter();sn=collections.Counter()
 for r in schemes:
  sc[r['scheme']]+=1
  if r['2026_template_advalorem_pct']:sn[r['scheme']]+=1
  if r['scenario_2027_2032_statutory_pct']:failures.append('Future scheme rate falsely certified')
  k=(r['cn8_2025'],r['taric10_2026'],r['proxy_country_source'])
  if r['2026_template_advalorem_pct']:
   if not any(z['measure_type_code']=='142' and z['country_group_or_code']==r['official_treatment_group_code']
          and z['simple_ad_valorem_pct']==r['2026_template_advalorem_pct']
          and not z['additional_code'] and not z['quota_order_number'] and z['number_of_conditions']=='0' for z in cindex[k]):
    failures.append('GSP 2026 template not source supported '+str(k))
 if dict(sc)!={'EBA_2026_RECORD':321,'STANDARD_GSP_2026_TEMPLATE':321,'GSP_PLUS_2026_TEMPLATE':321}:
  failures.append('Scenario template line coverage unexpected')
 if sn.get('EBA_2026_RECORD')!=321 or any(r['2026_template_advalorem_pct'] not in ('','0','0.000') for r in schemes if r['scheme']=='EBA_2026_RECORD'):
  failures.append('EBA rate data inconsistent')
 affected=collections.Counter()
 for r in cn8:
  origin_code=r['origin']
  if r['2026_simple_candidate_pct_all_leaves']!='':affected[origin_code]+=1
 if len(cn8)!=1400 or len(set((x['cn8_2025'],x['origin']) for x in cn8))!=1400:failures.append('Duplicate CN8 country')
 for r in cn8:
  if r['2027_2032_guaranteed_rate']:failures.append('Future guarantee found')
  if r['cn8_2025'].startswith('61') and r['origin']=='TR' and r['customs_union_pct_all_leaf_unambiguous']=='':
   failures.append('Apparel Turkish customs union missing '+r['cn8_2025'])
 info={'qa_timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'passed':not failures,'issues':failures[:100],
    'official_circabc_source_xlsx_sha_verified':len(originals),
    'unique_taric10_leaf_count':len(leaves),'unique_origin_taric10_records':len(originmap),
    'tariff_measure_evidence_records':len(raw_candidates),
    'cn8_origin_record_count':len(cn8),'conditional_scenario_rows':len(schemes),
    'uniform_simple_2026_candidate_cn8_by_origin':dict(affected),
    '2026_scheme_template_available_taric10':dict(sn),
    'GSP_plus_2027_BD_future_rate_is_verified':False,
    'future_year_effective_rate_is_certified':False,
    'product_specific_RoO_complete':False,
    'scope_limit':'Nov 1 2026 TARIC snapshot plus source-linked 2026 GSP templates; no future-duty guarantee'}
 (B/'INDEPENDENT_TARIFF_QA.json').write_text(json.dumps(info,indent=2))
 print(json.dumps(info,indent=2),flush=True)
 if failures:raise RuntimeError('Tariff QA failed '+str(failures[:15]))
if __name__=='__main__':main()
