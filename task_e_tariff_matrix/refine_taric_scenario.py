#!/usr/bin/env python3
"""Task E refined CN8 tariff and conditional scheme matrix, November 2026.
Uses archived source-backed candidate rows. Adds customs-union measure type 106,
reconciles MFN/142/106 by TARIC10, preserves 2026 Standard GSP/GSP+ template
without falsely claiming 2027/2032 effective duty or proof of origin.
"""
import pathlib,csv,json,re,collections,datetime,hashlib
from decimal import Decimal
SRC=pathlib.Path('task_e_tariff_matrix/nov2026')
OUT=pathlib.Path('task_e_tariff_matrix/refined_v18')
OUT.mkdir(parents=True,exist_ok=True)
COUNTRIES=['BD','CN','IN','VN','PK','KH','TR']
def read(path):
 with path.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def write(name,header,rows):
 with (OUT/name).open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=header,extrasaction='ignore');w.writeheader();w.writerows(rows)
def select(rs):
 if not rs:return {'status':'NOT_IN_OFFICIAL_SNAPSHOT','expr':'','pct':'','code':'','legal':'','source_origin':''}
 maxdepth=max(len(r['measure_source_goods_code'].rstrip('0')) for r in rs)
 best=[r for r in rs if len(r['measure_source_goods_code'].rstrip('0'))==maxdepth]
 if len(best)!=1:return {'status':'MULTIPLE_APPLICABLE_MEASURES','expr':'|'.join(sorted({r['duty_expression'] for r in best})),
  'pct':'','code':'|'.join(sorted({r['measure_source_goods_code'] for r in best})),
  'legal':'|'.join(sorted({r['legal_base'] for r in best})),
  'source_origin':'|'.join(sorted({r['country_group_or_code'] for r in best}))}
 v=best[0]
 clean=(v['simple_ad_valorem_pct'] and not v['additional_code'] and not v['quota_order_number']
       and int(v['number_of_conditions'] or 0)==0)
 return {'status':'SINGLE_SIMPLE_AD_VALOREM' if clean else 'SINGLE_BUT_COMPLEX_OR_CONDITIONAL',
  'expr':v['duty_expression'],'pct':v['simple_ad_valorem_pct'] if clean else '',
  'code':v['measure_source_goods_code'],'legal':v['legal_base'],'source_origin':v['country_group_or_code']}
def main():
 candidates=read(SRC/'all_tariff_measure_candidates_with_conditions.csv')
 leaves=read(SRC/'taric10_leaf_mapping.csv')
 original=read(SRC/'actual_2026_taric10_origin_matrix.csv')
 index=collections.defaultdict(list)
 for r in candidates:
  k=(r['cn8_2025'],r['taric10_2026'],r['country'])
  index[k].append(r)
 region={'BD':'EBA','CN':'MFN','IN':'STANDARD_GSP','VN':'EVFTA','PK':'GSP_PLUS','KH':'EBA_PARTIAL_WITHDRAWAL','TR':'CUSTOMS_UNION'}
 exact=[];scenarios=[];per_cn8=collections.defaultdict(list);warnings=[]
 for row in original:
  k=(row['cn8_2025'],row['taric10_2026'],row['origin_country'])
  rows=index[k]
  mfn=select([x for x in rows if x['measure_type_code']=='103'])
  pref=select([x for x in rows if x['measure_type_code']=='142'])
  union=select([x for x in rows if x['measure_type_code']=='106'])
  q=[x for x in rows if x['measure_type_code'] in ('143','122')]
  trade_defense=[x for x in rows if x['measure_type_code'] in ('552','551','554','555','695','694')]
  extra=[x for x in rows if x['measure_type_code'] not in ('103','142','106','143','122')]
  # Priority indicates an available candidate, not guaranteed duty actually paid.
  choice=pref if pref['status']=='SINGLE_SIMPLE_AD_VALOREM' else (
    union if union['status']=='SINGLE_SIMPLE_AD_VALOREM' else mfn)
  kind='TARIFF_PREFERENCE_142' if choice is pref else ('CUSTOMS_UNION_106' if choice is union else 'THIRD_COUNTRY_103')
  rate=''
  safe=(choice['status']=='SINGLE_SIMPLE_AD_VALOREM'
    and pref['status'] not in ('MULTIPLE_APPLICABLE_MEASURES','SINGLE_BUT_COMPLEX_OR_CONDITIONAL')
    and union['status'] not in ('MULTIPLE_APPLICABLE_MEASURES','SINGLE_BUT_COMPLEX_OR_CONDITIONAL'))
  if safe:rate=choice['pct']
  condition='REQUIRES_PREFERENTIAL_ORIGIN_PROOF_AND_PRODUCT_RULE_OF_ORIGIN' if kind=='TARIFF_PREFERENCE_142' else (
    'CUSTOMS_UNION_FREE_CIRCULATION_AND_DOCUMENTATION_REQUIREMENTS' if kind=='CUSTOMS_UNION_106' else
    'MFN_SUBJECT_TO_OTHER_IMPORT_MEASURES')
  result={
   'cn8_2025':k[0],'taric10_2026':k[1],'origin':k[2],
   'source_reference_date':'2026-11-01','regime_observed':region[k[2]],
   'mfn_measure_type':'103','mfn_expression':mfn['expr'],'mfn_advalorem_pct':mfn['pct'],'mfn_status':mfn['status'],
   'mfn_source_goods_code':mfn['code'],'mfn_legal_base':mfn['legal'],
   'preference_measure_type':'142','preferential_expression':pref['expr'],'preference_advalorem_pct':pref['pct'],
   'preference_status':pref['status'],'preference_legal_base':pref['legal'],
   'customs_union_measure_type':'106','customs_union_expression':union['expr'],
   'customs_union_advalorem_pct':union['pct'],'customs_union_status':union['status'],'customs_union_legal_base':union['legal'],
   'lowest_simple_candidate_pct_not_final_duty':rate,'candidate_kind':kind if safe else 'AMBIGUOUS',
   'candidate_status':'SIMPLE_RATE_CANDIDATE_UNDER_SCHEME_CONDITIONS' if safe else 'NO_UNCONDITIONAL_RATE_ASSIGNMENT',
   'eligibility_and_documentation':condition,
   'quota_measure_count':len(q),'trade_defense_or_additional_duty_count':len(trade_defense),
   'other_import_controls_count':len(extra),
   'total_applied_candidate_measure_records':len(rows),
   'actual_paid_duty':'NOT_OBSERVED','product_specific_roo':'NOT_CERTIFIED',
   'future_2027_2032_duty_status':'CONDITIONAL_FUTURE_SCENARIO_NOT_OBSERVED',
   'official_source_file':'Duties Import 01-99.xlsx'}
  exact.append(result);per_cn8[(k[0],k[2])].append(result)
 # Prospective schemes as current 2026 templates ONLY, matched by generic official groups.
 # India's 2026 group 2020 = Standard GSP, Pakistan's group 2027 = GSP+.
 # BD group 2005 = EBA. All are NOT legally guaranteed Bangladesh future rates.
 for l in leaves:
  p=l['cn8_2025'];leaf=l['taric10_2026']
  group_templates=[
    ('EBA_2026_RECORD','BD','2005','CURRENT_BANGLADESH_EBA_2026_LEGAL_RATE'),
    ('STANDARD_GSP_2026_TEMPLATE','IN','2020','PROSPECTIVE_BANGLADESH_SCENARIO_2027_PLUS_NOT_CERTIFIED'),
    ('GSP_PLUS_2026_TEMPLATE','PK','2027','PROSPECTIVE_BANGLADESH_SCENARIO_2027_PLUS_NOT_CERTIFIED')
  ]
  mfn=select([x for x in index[(p,leaf,'BD')] if x['measure_type_code']=='103'])
  for scheme,proxy,group,legality in group_templates:
   row=select([x for x in index[(p,leaf,proxy)] if x['measure_type_code']=='142' and x['country_group_or_code']==group])
   scenarios.append({
     'cn8_2025':p,'taric10_2026':leaf,'scheme':scheme,
     'proxy_country_source':proxy,'official_treatment_group_code':group,
     '2026_taric_template_expression':row['expr'],
     '2026_template_advalorem_pct':row['pct'],
     '2026_template_rate_status':row['status'],
     'mfn_2026_reference_pct':mfn['pct'],
     'mfn_2026_reference_expression':mfn['expr'],
     'scenario_2027_2032_statutory_pct':'',
     'future_status':legality,
     '2027_law':'Regulation (EU) 2026/1395 - requires line-specific classification and eligibility',
     'transition':'Bangladesh LDC graduation 24-Nov-2029; approximate EBA transition 2032 (not enacted tariff switch)',
     'rules_of_origin':'GENERAL_GSP_RULES_APPLY; CN8_PRODUCT_RULE_NOT_VERIFIED',
     'source_reference_date':'2026-11-01'})
 aggregate=[]
 for (p,o),recs in sorted(per_cn8.items()):
  assert len(recs)==len(set(x['taric10_2026'] for x in recs))
  def uniform(field):
   vals=[x[field] for x in recs]
   if vals and all(v!='' for v in vals) and len(set(vals))==1:return vals[0]
   return ''
  rate=uniform('lowest_simple_candidate_pct_not_final_duty')
  hascomplex=any(x['candidate_status']!='SIMPLE_RATE_CANDIDATE_UNDER_SCHEME_CONDITIONS' for x in recs)
  aggregate.append({
     'cn8_2025':p,'origin':o,'taric10_leaf_count':len(recs),
     'mfn_pct_all_leaf_unambiguous':uniform('mfn_advalorem_pct'),
     'preference_pct_all_leaf_unambiguous':uniform('preference_advalorem_pct'),
     'customs_union_pct_all_leaf_unambiguous':uniform('customs_union_advalorem_pct'),
     '2026_simple_candidate_pct_all_leaves':rate,
     'candidate_reliability':'SOURCE_REPORTED_SIMPLE_WITH_UNVERIFIED_ELIGIBILITY' if rate and not hascomplex else 'RATE_UNRESOLVED',
     'quota_measures_at_least_one_leaf':sum(int(x['quota_measure_count'])>0 for x in recs),
     'additional_trade_defence_measures_at_least_one_leaf':sum(int(x['trade_defense_or_additional_duty_count'])>0 for x in recs),
     'product_specific_roo_verified':'NO',
     'source_reference_date':'2026-11-01',
     '2027_2032_guaranteed_rate':'',
     '2027_2032_applicability':'NOT_ESTABLISHED',
  })
 write('taric10_country_refined_measure_matrix.csv',list(exact[0]),exact)
 write('CN8_country_source_qualified_rate_screen.csv',list(aggregate[0]),aggregate)
 write('Bangladesh_EBA_StandardGSP_GSPplus_2026_source_templates.csv',list(scenarios[0]),scenarios)
 schemeout={}
 for origin in COUNTRIES:
  os=[x for x in aggregate if x['origin']==origin]
  schemeout[origin]={
   'cn8':len(os),'simple_mfn_cn8':sum(x['mfn_pct_all_leaf_unambiguous']!='' for x in os),
   'uniform_pref_cn8':sum(x['preference_pct_all_leaf_unambiguous']!='' for x in os),
   'uniform_customs_union_cn8':sum(x['customs_union_pct_all_leaf_unambiguous']!='' for x in os),
   'uniform_2026_candidate_cn8':sum(x['2026_simple_candidate_pct_all_leaves']!='' for x in os)}
 total={'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
   'reference_date':'2026-11-01','cn8':200,'taric10':len(leaves),
   'taric10_country':len(exact),'scheme_template_taric10':len(scenarios),
   'cn8_country':len(aggregate),'by_origin':schemeout,
   'official_source_root':'task_e_tariff_matrix/nov2026/official_source_xlsx',
   'source_receipts':'task_e_tariff_matrix/nov2026/source_file_receipts.json',
   'cautions':['Simple measure candidates are not legal opinion or paid effective rates',
     'Turkey customs-union measures type 106 are recorded separately; they can require A.TR/free-circulation documentation',
     'Cambodia EBA partially withdrawn: only measure-level source rates used; no universal EBA assumption',
     'MFN expressions are not substituted for preferences where a tariff preference is conditional or ambiguous',
     '2026 generic GSP and GSP+ template values are NOT automatically operative rates after 2027 for Bangladesh',
     'Product-specific origin rules are not yet matched to 200 CN8 / 321 TARIC10 definitions',
     'Additional anti-dumping, safeguard, quotas, suspensions, taxes, composition-based duties and exemptions are separately flagged',
     'Snapshot reference 2026-11-01, not same-day TARIC and not a history of 2012-2025 duties']}
 (OUT/'REFINED_RATE_COVERAGE_AND_LIMITATIONS.json').write_text(json.dumps(total,indent=2))
 print(json.dumps(total,indent=2),flush=True)
if __name__=='__main__':main()
