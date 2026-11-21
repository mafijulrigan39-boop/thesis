#!/usr/bin/env python3
"""Independent verification of Task F: raw-source hashes, Article33 denominator, tariff exposure,
market shares, structural zero/missingness and growth against individual source rows.
Different calculation path from run_empirical_analysis.py.
"""
import json,csv,gzip,hashlib,io,pathlib,math
from collections import defaultdict,Counter
from decimal import Decimal,localcontext
from datetime import datetime,timezone
R=pathlib.Path('task_f_empirical/full')
A=pathlib.Path('task_f_empirical/article33')
C=pathlib.Path('task_c_competitor_data/full')
D=pathlib.Path('task_d_quantities/full')
E=pathlib.Path('task_e_tariff_matrix/nov2026_taric')
G=pathlib.Path('cn8_harmonization_2012_2025')
def read(path):
 with open(path,newline='',encoding='utf-8-sig') as f:return list(csv.DictReader(f))
def dec(x):return Decimal(str(x)) if str(x).strip() else None
def err_if(cond,msg,errors):
 if cond:errors.append(msg)
def main():
 errors=[]
 report=json.loads((R/'TASK_F_EMPIRICAL_RESULTS.json').read_text())
 for rec in report['source_inputs_sha256']:
  path=pathlib.Path(rec['file'])
  if not path.exists():errors.append('Input missing: '+str(path))
  elif hashlib.sha256(path.read_bytes()).hexdigest()!=rec['sha256']:errors.append('Input hash changed '+str(path))
 # Validate independent source-data empirical arithmetic, not just copies of derived outputs.
 choices=read(C/'selected_top200_2025.csv')
 market=read(R/'product_2025_value_share_price_tariff_exposure.csv')
 country=read(R/'competitor_country_aggregate_positioning_2025.csv')
 origin=read(R/'product_origin_2025_competitiveness_2026_tariff_candidates.csv')
 scenarios=read(R/'scenario_scope_tariff_exposure_sensitivity.csv')
 growth=read(R/'HS2_61_62_63_chapter_level_growth_2012_2025.csv')
 art=read(A/'official_article33_annual_screen_2012_2025.csv')
 roster=read(A/'gsp_2027_annexI_roster_64.csv')
 uv=read(D/'relative_unit_values_2025.csv')
 source_margin=read(E/'cn8_2026_origin_regime_aware_screen.csv')
 source_mfn=read(E/'top200_seven_origin_nov2026_tariff_scenarios_NO_IMPUTATION.csv')
 if len(choices)!=len(market)!=200:errors.append('200 row mismatch')
 if len(origin)!=1200:errors.append('Origin comparisons not 1200')
 if len(roster)!=64 or len({x['partner'] for x in roster})!=64:errors.append('GSP roster size/unique invalid')
 B={x['cn8']:Decimal(x['bd_2025_source_eur']) for x in choices}
 M={x['cn8_2025']:x for x in market}
 total=sum(B.values(),Decimal(0))
 if total!=Decimal(report['all_200_BD_2025_value_eur']):errors.append('Selected 200 value mismatch')
 if abs(total-Decimal('20789281101'))>0:errors.append('Expected 2025 selected BD source total changed')
 share={x['cn8']:x for x in read(C/'product_year_bd_market_share_2012_2025.csv') if x['year']=='2025'}
 mfn={x['cn8_2025']:dec(x['mfn_pct']) for x in source_mfn if x['origin']=='BD'}
 tariff={(x['cn8_2025'],x['origin']):x for x in source_margin}
 uv_by={(x['cn8'],x['comparison_origin']):x for x in uv}
 for p in B:
  row=M[p]
  if dec(row['bangladesh_import_value_eur_2025'])!=B[p]:errors.append('Product trade mismatch '+p)
  if dec(row['all_origin_extraEU_value_eur_2025'])!=dec(share[p]['extra_eu_eur']):errors.append('EU denominator mismatch '+p)
  computed=100*B[p]/dec(share[p]['extra_eu_eur'])
  if abs(computed-dec(row['bangladesh_share_extraEU_pct_2025']))>Decimal('1e-15'):
   errors.append('EU share mismatch '+p)
  if mfn[p] is None:
   if row['MFN_reference_static_duty_equivalent_eur']:errors.append('Unverified MFN imputed '+p)
  else:
   expected=B[p]*mfn[p]/100
   if dec(row['MFN_reference_static_duty_equivalent_eur'])!=expected:
    errors.append('MFN exposure wrong '+p)
  if tariff[(p,'BD')]['potential_eligible_advalorem_pct']!='0.000':
   errors.append('Unexpected Bangladesh EBA scheme benchmark '+p)
 # Independent country-level tariff margin & UV pair matching.
 for row in origin:
  p,o=row['cn8_2025'],row['origin']
  t=tariff[(p,o)]
  candidate=dec(t['potential_eligible_advalorem_pct'])
  if candidate is None and row['bd_preference_margin_vs_origin_pp']:errors.append('Unverified tariff origin rate imputed '+p+o)
  if candidate is not None and dec(row['bd_preference_margin_vs_origin_pp'])!=candidate:
   errors.append('Competitor tariff margin '+p+o)
  orig=uv_by[(p,o)]
  if row['unit_value_status']!=orig['status']:errors.append('Unit-value comparability status '+p+o)
  if orig['bd_to_competitor_unit_value_ratio']:
   if abs(dec(row['bd_to_competitor_eur_per_kg_ratio_2025'])-dec(orig['bd_to_competitor_unit_value_ratio']))>Decimal('1e-19'):
    errors.append('Unit value ratio '+p+o)
  elif row['bd_to_competitor_eur_per_kg_ratio_2025']:
   errors.append('Missing unit value assigned '+p+o)
 # Cross validate every static scenario exact 2025 subset and values.
 F=lambda row:row['scenario']
 expected_scenarios={
  'MFN_2026_SHOCK_IF_EBA_LOST':lambda p:mfn[p],
  'INDIA_2026_STANDARD_GSP_CHANNEL_PROXY_NOT_FUTURE_BD_RATE':lambda p:dec(tariff[(p,'IN')]['potential_eligible_advalorem_pct']) if tariff[(p,'IN')]['duty_channel']=='TARIFF_PREFERENCE_CANDIDATE' else None,
  'PAKISTAN_2026_GSP_PLUS_CHANNEL_PROXY_NOT_FUTURE_BD_RATE':lambda p:dec(tariff[(p,'PK')]['potential_eligible_advalorem_pct']) if tariff[(p,'PK')]['duty_channel']=='TARIFF_PREFERENCE_CANDIDATE' else None,
  'S11B_STANDARD_GSP_ART7_20PCT_MFN_REDUCTION_2026_RATE_REFERENCE':lambda p:mfn[p]*Decimal('.8') if p[:2] in ('61','62','63') and mfn[p] is not None else None,
  'S11B_ART33_HYPOTHETICAL_MFN_AFTER_EBA_EXIT_AND_IMPLEMENTING_ACT':lambda p:mfn[p] if p[:2] in ('61','62','63') else None,
 }
 for r in scenarios:
  if r['subset']=='TOP200':pool=list(B)
  elif r['subset']=='TOP10':pool=list(B)[:10]
  elif r['subset']=='TOP50':pool=list(B)[:50]
  elif r['subset']=='TOP100':pool=list(B)[:100]
  elif r['subset']=='S11B_APPAREL_61_63':pool=[p for p in B if p[:2] in ('61','62','63')]
  elif r['subset']=='NON_S11B':pool=[p for p in B if p[:2] not in ('61','62','63')]
  elif r['subset']=='NO_COMPLEX_GROUP_LABEL':pool=[p for p in B if M[p]['classification_2025_type_derived']=='1:1_exact']
  elif r['subset']=='2025_CN8_COMPLEX_GROUPS':pool=[p for p in B if M[p]['classification_2025_type_derived']!='1:1_exact']
  else:errors.append('Unknown subset '+r['subset']);continue
  f=expected_scenarios.get(r['scenario'])
  if f is None:errors.append('Unknown scenario');continue
  valid=[p for p in pool if f(p) is not None]
  actual=sum(B[p]*f(p)/100 for p in valid)
  if dec(r['static_additional_duty_equivalent_eur'])!=actual:errors.append('Scenario arithmetic '+r['scenario']+' '+r['subset'])
  if Decimal(r['trade_value_qualified_eur'])!=sum((B[p] for p in valid),Decimal(0)):
   errors.append('Scenario covered value '+r['scenario']+' '+r['subset'])
  if int(r['products_numeric_qualified'])!=len(valid):errors.append('Scenario count '+r['scenario']+' '+r['subset'])
 # Independent Article33 raw source reconstruction, with GSP roster from Official Journal:
 roster_set={z['partner'] for z in roster}
 for y in range(2012,2026):
  rec=next(z for z in read(A/'official_chapter_request_receipts.csv') if z['year']==str(y))
  payload=gzip.decompress((A/'raw'/f'{y}_chapter61_63.csv.gz').read_bytes())
  if hashlib.sha256(payload).hexdigest()!=rec['sha256']:errors.append('Article33 source hash '+str(y))
  data={(r['product'],r['partner']):Decimal(r['OBS_VALUE']) for r in csv.DictReader(io.StringIO(payload.decode('utf-8-sig')))}
  year=next(z for z in art if z['year']==str(y))
  bd=sum((data[(chapter,'BD')] for chapter in ('61','62','63')),Decimal(0))
  eu=sum((data[(chapter,'EXT_EU27_2020')] for chapter in ('61','62','63')),Decimal(0))
  gsp=sum((data.get((chapter,p),Decimal(0)) for chapter in ('61','62','63') for p in roster_set),Decimal(0))
  if bd!=Decimal(year['bd_S11b_eur']):errors.append('Article33 numerator '+str(y))
  if eu!=Decimal(year['extraEU_all_origins_S11b_eur']):errors.append('Article33 world denominator '+str(y))
  if gsp!=Decimal(year['gsp_beneficiaries_S11b_eur_2027_roster']):errors.append('Article33 GSP denominator '+str(y))
  if abs(100*bd/gsp-Decimal(year['BD_share_of_2027_GSP_roster_percent']))>Decimal('1e-18'):
   errors.append('Article33 37 percent share '+str(y))
  if abs(100*bd/eu-Decimal(year['BD_share_of_extraEU_all_origins_percent']))>Decimal('1e-18'):
   errors.append('Article33 6 percent share '+str(y))
  if year['current_EBA_exception'] not in ('True','true','1'):
   errors.append('EBA legal exemption lost '+str(y))
 if len(growth)!=42:errors.append('Chapter growth rows not 42')
 for row in growth:
  if row['2012_2025_CAGR_percent'] and row['year']!='2025':errors.append('CAGR on unexpected year')
 if (R/'CERTIFIED_2012_2025_CN8_HARMONIZED_CAGR.csv').stat().st_size>100:
  errors.append('CN8 certification gate apparently bypassed')
 qr={'verified_at_utc':datetime.now(timezone.utc).isoformat(),'passed':not errors,
 'issues':errors[:150], 'source_inputs_verified_sha256':len(report['source_inputs_sha256']),
 'product_shares_recomputed':len(B),'competitor_origin_pairs_verified':len(origin),
 'tariff_exposure_scenario_sensitivity_rows_recomputed':len(scenarios),
 'article33_annual_source_response_sha_verified':14,
 'article33_2025_37_share_pct':next(x['BD_share_of_2027_GSP_roster_percent'] for x in art if x['year']=='2025'),
 'article33_2025_6_share_pct':next(x['BD_share_of_extraEU_all_origins_percent'] for x in art if x['year']=='2025'),
 'CN8_growth_certified':False,'future_2032_rates_certified':False,
 'important_policy':'Never call static tariff duty-equivalent cost lost export revenue or legal future duty.'}
 (R/'INDEPENDENT_QA.json').write_text(json.dumps(qr,indent=2))
 print(json.dumps(qr,indent=2),flush=True)
 if errors:raise RuntimeError('Task F QA: '+str(errors[:10]))
if __name__=='__main__':main()
