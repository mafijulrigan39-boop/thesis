#!/usr/bin/env python3
"""Task F real empirical calculations from audited Task C/D/E and Article33 source.
Never convert unreported cells to zero. Trade: 2025; tariff: NOV-01-2026 baseline.
Only HS2 chapter growth released as defensible broad-group historical comparison,
no unverified exact-CN8 2012-25 CAGR.
"""
from __future__ import annotations
import csv,gzip,json,math,hashlib,pathlib,datetime,statistics
from collections import Counter,defaultdict
from decimal import Decimal
BASE=pathlib.Path("task_f_empirical/full")
C=pathlib.Path("task_c_competitor_data/full")
D=pathlib.Path("task_d_quantities/full")
E=pathlib.Path("task_e_tariff_matrix/nov2026_taric")
A=pathlib.Path("task_f_empirical/article33")
B=pathlib.Path("cn8_harmonization_2012_2025")
ORIGINS=['BD','CN','IN','VN','PK','KH','TR']
COMP=['CN','IN','VN','PK','KH','TR']
CHAPTERS=['61','62','63']
D0=Decimal(0)
def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def rd(path):
 with open(path,newline='',encoding='utf-8-sig') as f:return list(csv.DictReader(f))
def write(name,cols,rows):
 p=BASE/name;p.parent.mkdir(parents=True,exist_ok=True)
 with open(p,"w",newline="",encoding='utf-8') as f:w=csv.DictWriter(f,fieldnames=cols,extrasaction="ignore");w.writeheader();w.writerows(rows)
def de(x):return Decimal(str(x)) if str(x).strip() else None
def per(x):return str(x) if x is not None else ''
def mean(s):return sum(s,D0)/len(s) if s else None
def median(s):
 s=sorted(s)
 if not s:return None
 n=len(s)
 return s[n//2] if n%2 else (s[n//2]+s[n//2-1])/2
def hhi(vals):
 total=sum(vals,D0)
 return sum((v/total)**2 for v in vals)*10000 if total else None
def main():
 BASE.mkdir(parents=True,exist_ok=True)
 source_files=[C/'selected_top200_2025.csv',C/'product_year_bd_market_share_2012_2025.csv',
  C/'top5_non_eu_suppliers_2025.csv',C/'supplier_concentration_bounded_2025.csv',
  D/'seven_origin_quantity_unit_value_2012_2025.csv',
  D/'relative_unit_values_2025.csv',E/'cn8_2026_origin_regime_aware_screen.csv',
  E/'top200_seven_origin_nov2026_tariff_scenarios_NO_IMPUTATION.csv',
  A/'official_article33_annual_screen_2012_2025.csv',A/'annual_chapter_denominator_audit.csv',
  B/'cn8_2025_exact.csv']
 inputs=[{"file":str(p),"sha256":hashlib.sha256(p.read_bytes()).hexdigest(),"bytes":p.stat().st_size} for p in source_files]
 choices=rd(C/'selected_top200_2025.csv')
 assert len(choices)==200 and choices[0]['cn8']=='61091000'
 codes=[r['cn8'] for r in choices];cn8set=set(codes)
 vrank={p:i+1 for i,p in enumerate(codes)}
 bdval={r['cn8']:Decimal(r['bd_2025_source_eur']) for r in choices}
 source_bd_total=sum(bdval.values(),D0)
 # Task C raw partner/product/year transactions, exact all-origin official source.
 byproduct=defaultdict(dict); allorigin=defaultdict(Decimal)
 with gzip.open(C/'all_partners_2012_2025.csv.gz','rt',encoding='utf-8-sig',newline='') as fh:
  for r in csv.DictReader(fh):
   if int(r['year'])!=2025:continue
   k=(r['cn8'],r['origin'])
   assert r['cn8'] in cn8set
   if k in byproduct[r['cn8']]:raise ValueError('Duplicate source partner code')
   v=Decimal(r['value_eur']);byproduct[r['cn8']][r['origin']]=v
   if r['origin'] in COMP:allorigin[r['origin']]+=v
 # Official 2025 total and market shares within top200 product markets.
 shares=rd(C/'product_year_bd_market_share_2012_2025.csv')
 s25={r['cn8']:r for r in shares if r['year']=='2025'}
 assert len(s25)==200 and all(r['status']=='VALID' for r in s25.values())
 check=0
 for p in codes:
  if Decimal(s25[p]['bd_eur'])!=bdval[p]:raise ValueError('Top 200 Bangladesh value mismatch')
  v=byproduct[p]
  if Decimal(s25[p]['extra_eu_eur'])!=v['EXT_EU27_2020']:raise ValueError('ExtraEU denominator mismatch')
  if Decimal(s25[p]['bd_eur'])!=v['BD']:raise ValueError('Bangladesh import value mismatch')
  calc=100*v['BD']/v['EXT_EU27_2020']
  if abs(calc-Decimal(s25[p]['bd_share_of_extra_eu_pct']))>Decimal('1e-15'):
   raise ValueError('Product share mismatch '+p)
  check+=1
 # Task E dated regime-specific MFN and preference candidates
 tarrows=rd(E/'cn8_2026_origin_regime_aware_screen.csv')
 duty={(r['cn8_2025'],r['origin']):r for r in tarrows}
 assert len(duty)==1400
 mfn=rd(E/'top200_seven_origin_nov2026_tariff_scenarios_NO_IMPUTATION.csv')
 mfn_b={r['cn8_2025']:de(r['mfn_pct']) for r in mfn if r['origin']=='BD'}
 assert len(mfn_b)==200
 # Product and classification risk label source (derived Task B; not official input certification)
 codeinfo={r['PRODUCT']:r for r in rd(B/'cn8_2025_exact.csv')}
 # D quantity and comparison raw cells; never assume missing quantity=0.
 val2025={}
 for r in rd(D/'seven_origin_quantity_unit_value_2012_2025.csv'):
  if r['year']=='2025':val2025[(r['cn8'],r['origin'])]=r
 assert len(val2025)==1400
 relat=rd(D/'relative_unit_values_2025.csv')
 assert len(relat)==1200
 relative={(r['cn8'],r['comparison_origin']):r for r in relat}
 # Name all real country winners in product and share comparisons
 top5=rd(C/'top5_non_eu_suppliers_2025.csv')
 top5_map=defaultdict(list)
 for r in top5:top5_map[r['cn8']].append(r)
 supplier=rd(C/'supplier_concentration_bounded_2025.csv')
 countryhhi={r['cn8']:r for r in supplier}
 assert len(countryhhi)==200
 prod=[];origin_rates=[];unitstats=[]
 for p in codes:
  base=bdval[p];n=byproduct[p]['EXT_EU27_2020'];hs=p[:2]
  m=mfn_b[p];bdtar=duty[(p,'BD')]
  bd_eba=de(bdtar['potential_eligible_advalorem_pct'])
  assert bd_eba is not None and bd_eba==0
  ud=val2025[(p,'BD')]
  nc=codeinfo.get(p,{})
  annual=codeinfo.get(p,{}).get('CONTINUITY_TYPE','NOT_AVAILABLE')
  exposure=base*m/100 if m is not None else None
  row={"rank_2025":vrank[p],"cn8_2025":p,"hs2":hs,"bangladesh_import_value_eur_2025":str(base),
   "all_origin_extraEU_value_eur_2025":str(n),
   "bangladesh_share_extraEU_pct_2025":s25[p]['bd_share_of_extra_eu_pct'],
   "bangladesh_export_basket_share_top200_pct":str(100*base/source_bd_total),
   "bangladesh_2025_unit_value_eur_per_kg":ud['eur_per_kg'],
   "unit_value_status":ud['status'],
   "country_supplier_hhi_provisional":countryhhi[p]['named_supplier_hhi_on_extra_eu_base'],
   "country_supplier_residual_pct":countryhhi[p]['residual_pct'],
   "top_nonEU_origin":top5_map[p][0]['origin'] if top5_map[p] else '',
   "top_nonEU_origin_2025_eur":top5_map[p][0]['value_eur'] if top5_map[p] else '',
   "mfn_2026_reference_pct":per(m),
   "eba_BD_2026_candidate_pct":str(bd_eba),
   "mfnbaseline_delta_percent_points":per(m-bd_eba) if m is not None else '',
   "MFN_reference_static_duty_equivalent_eur":per(exposure),
   "tariff_join_status":"MFN_AND_EBA_NUMERIC_CONDITIONAL" if m is not None else "MFN_COMPLEX_NO_IMPUTATION",
   "classification_2025_type_derived":annual,
   "2012_2025_CN8_CAGR":"", "historical_growth_status":"BLOCKED_TASK_B_SOURCE_PROVENANCE",
   "tariff_date":"2026-11-01","trade_year":"2025"}
  prod.append(row)
  for origin in COMP:
   tariff=duty[(p,origin)]
   rate=de(tariff['potential_eligible_advalorem_pct'])
   uv=relative[(p,origin)]
   uv_ratio=de(uv['bd_to_competitor_unit_value_ratio'])
   orig=byproduct[p].get(origin)
   origin_rates.append({"cn8_2025":p,"origin":origin,"bd_imports_eur_2025":str(base),
      "competitor_imports_eur_2025":per(orig),
      "competitor_eu_extraEU_market_share_pct_2025":str(100*orig/n) if orig is not None else '',
      "competitor_2026_source_conditional_rate_pct":per(rate),
      "bd_eba_2026_source_candidate_pct":str(bd_eba),
      "bd_preference_margin_vs_origin_pp":per(rate-bd_eba) if rate is not None else '',
      "applied_tariff_status":"NOT_OBSERVED_PROOF_OF_ORIGIN_OR_A_TR",
      "tariff_route":tariff['duty_channel'],
      "tariff_comparison_status":"NUMERIC_CANDIDATE" if rate is not None else "MISSING_COMPLEX_CONDITIONAL",
      "bd_to_competitor_eur_per_kg_ratio_2025":per(uv_ratio),
      "unit_value_status":uv['status'],
      "comparison_year_2025":"2025","tariff_reference_date_2026":"2026-11-01"})
 # Explicit market positioning and top-five derived rankings
 market=[]
 for p in codes:
  x=next(z for z in prod if z["cn8_2025"]==p)
  ranked=top5_map.get(p,[])
  market.append({"rank_by_BD_import_value":vrank[p],"cn8_2025":p,"BD_eur_2025":x['bangladesh_import_value_eur_2025'],
   "EU_extraEU_denominator_eur_2025":x["all_origin_extraEU_value_eur_2025"],
   "BD_share_extraEU_pct":x['bangladesh_share_extraEU_pct_2025'],
   "winner_origin":ranked[0]["origin"] if ranked else "",
   "winner_import_eur":ranked[0]["value_eur"] if ranked else "",
   "top5_nonEU_origins":"|".join(r["origin"] for r in ranked),
   "top5_nonEU_values_eur":"|".join(r["value_eur"] for r in ranked),
   "top5_nonEU_market_shares_pct":"|".join(r["share_of_extra_eu_pct"] for r in ranked),
   "supplier_hhi_provisional":x['country_supplier_hhi_provisional'],
   "supplier_residual_pct":x["country_supplier_residual_pct"]})
 # Country rankings and unit value means/margins sensitivity
 byorigin=defaultdict(list)
 for r in origin_rates:byorigin[r['origin']].append(r)
 country=[]
 for o in COMP:
  rr=byorigin[o];valids=[r for r in rr if r['bd_preference_margin_vs_origin_pp']!='']
  ratios=[Decimal(r['bd_to_competitor_eur_per_kg_ratio_2025']) for r in rr if r['bd_to_competitor_eur_per_kg_ratio_2025']!='']
  weights=[(Decimal(r["bd_imports_eur_2025"]),Decimal(r["bd_to_competitor_eur_per_kg_ratio_2025"])) for r in rr if r['bd_to_competitor_eur_per_kg_ratio_2025']]
  uvweight=sum((w*x for w,x in weights),D0)/sum((w for w,x in weights),D0)
  high=[Decimal(r["bd_to_competitor_eur_per_kg_ratio_2025"]) for r in rr
    if r['bd_to_competitor_eur_per_kg_ratio_2025'] and
    Decimal(r["bd_imports_eur_2025"])>=Decimal(1000000) and
    r["competitor_imports_eur_2025"] and Decimal(r["competitor_imports_eur_2025"])>=Decimal(1000000)
    and Decimal("0.1")<=Decimal(r["bd_to_competitor_eur_per_kg_ratio_2025"])<=Decimal(10)]
  pw=sum((Decimal(r['bd_imports_eur_2025'])*Decimal(r['bd_preference_margin_vs_origin_pp']) for r in valids),D0)
  pwn=sum((Decimal(r['bd_imports_eur_2025']) for r in valids),D0)
  country.append({"origin":o,"observed_import_value_selected_markets_2025_eur":str(allorigin[o]),
    "origin_observation_count":sum(r['competitor_imports_eur_2025']!='' for r in rr),
    "reported_200_line_coverage":len(rr),
    "2026_conditional_tariff_candidates":len(valids),
    "mean_BD_preference_margin_pp_weighted_by_BD_eur":str(pw/pwn) if pwn else '',
    "median_BD_to_competitor_eur_per_kg_ratio":per(median(ratios)),
    "weighted_mean_BD_to_competitor_eur_per_kg_ratio":str(uvweight),
    "micro_and_outlier_excluded_median_uv_ratio":per(median(high)),
    "valid_unit_value_pairs":len(ratios),"high_value_and_trimmed_pairs":len(high),
    "counts_BD_lower_unit_value_than_comparison":sum(x<1 for x in ratios),
    "trade_scope":"2025 selected top 200 CN8 product markets",
    "tariff_claim_scope":"POTENTIAL_CONDITIONAL_NOT_PAID"})
 # Sensitivity: all selected ranks, apparel/non-apparel, exact vs complex CN8 definition
 sensitivity=[]
 subsets={
 "TOP10":codes[:10],"TOP50":codes[:50],"TOP100":codes[:100],"TOP200":codes,
 "S11B_APPAREL_61_63":[p for p in codes if p[:2] in ('61','62','63')],
 "NON_S11B":[p for p in codes if p[:2] not in ('61','62','63')],
 "NO_COMPLEX_GROUP_LABEL":[p for p in codes if codeinfo.get(p,{}).get('CONTINUITY_TYPE')=='1:1_exact'],
 "2025_CN8_COMPLEX_GROUPS":[p for p in codes if codeinfo.get(p,{}).get('CONTINUITY_TYPE')!='1:1_exact'],
 }
 def newscenario(label,predicate,rate):
  for sub,ps in subsets.items():
   allvalue=sum((bdval[p] for p in ps),D0)
   eligible=[p for p in ps if predicate(p)]
   v=sum((bdval[p] for p in eligible),D0)
   unverified=allvalue-v
   exposure=sum((bdval[p]*rate(p)/100 for p in eligible),D0)
   sensitivity.append({"scenario":label,"subset":sub,"products_total":len(ps),
     "products_numeric_qualified":len(eligible),
     "products_unverified":len(ps)-len(eligible),
     "2025_trade_value_all_eur":str(allvalue),
     "trade_value_qualified_eur":str(v),
     "trade_value_missing_tariff_eur":str(unverified),
     "trade_coverage_pct":str(100*v/allvalue) if allvalue else '',
     "static_additional_duty_equivalent_eur":str(exposure),
     "rate_year":"2026-11-01",
     "reference_trade_year":2025,"not_export_loss":True})
 newscenario("MFN_2026_SHOCK_IF_EBA_LOST",lambda p:mfn_b[p] is not None,lambda p:mfn_b[p])
 newscenario("INDIA_2026_STANDARD_GSP_CHANNEL_PROXY_NOT_FUTURE_BD_RATE",
   lambda p:duty[(p,'IN')]['duty_channel']=='TARIFF_PREFERENCE_CANDIDATE' and
            de(duty[(p,'IN')]['potential_eligible_advalorem_pct']) is not None,
   lambda p:de(duty[(p,'IN')]['potential_eligible_advalorem_pct']))
 newscenario("PAKISTAN_2026_GSP_PLUS_CHANNEL_PROXY_NOT_FUTURE_BD_RATE",
   lambda p:duty[(p,'PK')]['duty_channel']=='TARIFF_PREFERENCE_CANDIDATE' and
            de(duty[(p,'PK')]['potential_eligible_advalorem_pct']) is not None,
   lambda p:de(duty[(p,'PK')]['potential_eligible_advalorem_pct']))
 newscenario("S11B_STANDARD_GSP_ART7_20PCT_MFN_REDUCTION_2026_RATE_REFERENCE",
   lambda p:p[:2] in ('61','62','63') and mfn_b[p] is not None,
   lambda p:mfn_b[p]*Decimal(".8"))
 newscenario("S11B_ART33_HYPOTHETICAL_MFN_AFTER_EBA_EXIT_AND_IMPLEMENTING_ACT",
   lambda p:p[:2] in ('61','62','63') and mfn_b[p] is not None,
   lambda p:mfn_b[p])
 # Article33 source-backed historical chapter-level broad growth (consistent HS2 chapters).
 articles=rd(A/"official_article33_annual_screen_2012_2025.csv")
 chap=rd(A/"annual_chapter_denominator_audit.csv")
 assert len(articles)==14 and len(chap)==42
 growth=[]
 chap_index={(int(r['year']),r['chapter']):r for r in chap}
 for item in CHAPTERS:
  yearvalues={yr:Decimal(chap_index[(yr,item)]['bd_eur']) for yr in range(2012,2026)}
  for year in range(2012,2026):
   val=yearvalues[year];prev=yearvalues.get(year-1)
   growth.append({"year":year,"hs2_chapter":item,"BD_imports_eur":str(val),
    "yoy_growth_percent":str(100*(val/prev-1)) if prev is not None and prev>0 else "",
    "2012_2025_CAGR_percent":str(100*((yearvalues[2025]/yearvalues[2012])**(Decimal(1)/Decimal(13))-1)) if year==2025 else "",
    "status":"HS2_AGGREGATE_TRENDS_PERMITTED_CN_COMPOSITION_CHANGES_POSSIBLE",
    "not_equivalent_to_verified_CN8_harmonization":True,
    "source_dataset":"DS-045409","origin":"BD"})
 # 2025 BD portfolio within top 200 concentration
 top10=sum(bdval[p] for p in codes[:10])
 top50=sum(bdval[p] for p in codes[:50])
 concentration={"selected_2025_product_count":200,"selected_2025_BD_value_eur":str(source_bd_total),
  "top10_share_of_selected_basket_pct":str(100*top10/source_bd_total),
  "top50_share_of_selected_basket_pct":str(100*top50/source_bd_total),
  "product_hhi_within_selected200":str(hhi(list(bdval.values()))),
  "product_hhi_not_full_bangladesh_CN8":"Use separate verified complete 2025 basket from v7 for all-CN8 HHI",
  "sum_200_extraEU_products_eur":str(sum((Decimal(s25[p]['extra_eu_eur']) for p in codes),D0)),
  "pooled_BD_share_in_200_selected_extraEU_product_markets_pct":str(100*source_bd_total/
    sum((Decimal(s25[p]['extra_eu_eur']) for p in codes),D0))}
 # Scenario ranking by exposure; no nonmatched rate values assigned.
 shocks=sorted((z for z in prod if z['MFN_reference_static_duty_equivalent_eur']),
  key=lambda z:-Decimal(z['MFN_reference_static_duty_equivalent_eur']))
 product_margin=[{"rank_2025":z["rank_2025"],"cn8_2025":z["cn8_2025"],
  "trade_value_2025_eur":z["bangladesh_import_value_eur_2025"],
  "MFN_2026_pct":z["mfn_2026_reference_pct"],
  "BD_EBA_2026_pct":z["eba_BD_2026_candidate_pct"],
  "static_MFN_exposure_eur":z["MFN_reference_static_duty_equivalent_eur"],
  "is_S11b":z["hs2"] in ('61','62','63')} for z in shocks]
 # Cross year product comparisons = no certified outputs due task B official chain absent.
 write("product_2025_value_share_price_tariff_exposure.csv",list(prod[0]),prod)
 write("product_2025_top5_nonEU_suppliers.csv",list(market[0]),market)
 write("product_origin_2025_competitiveness_2026_tariff_candidates.csv",list(origin_rates[0]),origin_rates)
 write("competitor_country_aggregate_positioning_2025.csv",list(country[0]),country)
 write("scenario_scope_tariff_exposure_sensitivity.csv",list(sensitivity[0]),sensitivity)
 write("HS2_61_62_63_chapter_level_growth_2012_2025.csv",list(growth[0]),growth)
 write("largest_2025_products_by_static_MFN_exposure.csv",list(product_margin[0]),product_margin)
 write("CERTIFIED_2012_2025_CN8_HARMONIZED_CAGR.csv",
   ["cn8","year_start","year_end","growth_pct","certification_status","reason"],[])
 # Ensure empty file is not described as completed product growth.
 sc={r["scenario"]:{x["subset"]:x for x in sensitivity if x["scenario"]==r["scenario"]} for r in sensitivity}
 report={"calculation_utc":utc(),"taskF_version":"v20_data_and_scenarios",
   "source_inputs_sha256":inputs,"selected_product_count":len(codes),
   "all_200_BD_2025_value_eur":str(source_bd_total),
   "official_2025_product_share_tests":check,
   "2025_competitor_origin_rows":len(origin_rates),
   "valid_2025_origin_unit_value_pairs":sum(x["unit_value_status"]=="COMPARABLE_SAME_CN8_SAME_YEAR_KG" for x in origin_rates),
   "2026_conditional_rate_rows_numeric":sum(x["tariff_comparison_status"]=="NUMERIC_CANDIDATE" for x in origin_rates),
   "relative_unit_value_country_summary":country,
   "2025_product_basket_concentration":concentration,
   "sensitivity_scenarios":sensitivity,
   "top10_static_mfn_exposure":product_margin[:10],
   "Article33_2025":next(x for x in articles if x["year"]=="2025"),
   "Article33_gsp_roster":"2027 Annex I column C, backcast to 2025 for scenario, 64 countries",
   "missingness":"NA not 0; no reported partner/product/year is not an observed zero",
   "HARMONIZED_CN8_CAGR_CERTIFIED":False,
   "fully_projected_treaty_tariffs_2032_verified":False,
   "future_tariff_scenarios_certified":False,
   "estimates_are_static_tariff_equivalents_not_export_losses":True,
   "known_limitations":[
    "Task B original annual CN lists / concordances not authenticated: CN8 CAGRs withheld.",
    "Article33 numerator and denominator are real official EU chapter-level values; roster 2027 applied retrospectively to 2012-2025 descriptive screens.",
    "2026 TARIC on 2025 trade not actual paid 2025 tariff; scenarios are illustrative counterfactuals.",
    "EU GSP or customs-union preferential candidate rates depend on origin certification, A.TR where required and relevant conditions.",
    "No automatic safe case MFN assigned where 2026 TARIC origin duty has compound/missing leaves.",
    "Article33 safeguard would need end of EBA exemption and Commission implementing act, not automatic from >37%.",
    "Unit values descriptive and composition-sensitive, not production cost/quality/margin.",
    "Country supplier HHI subject to extraEU minus named-country residual; provenance recorded.",
    "Any future 2032/2029 policy tariffs must be legally updated; 2026 India/Pakistan tariff proxies are NOT future BD legal duties."]}
 (BASE/"TASK_F_EMPIRICAL_RESULTS.json").write_text(json.dumps(report,indent=2))
 print(json.dumps({k:v for k,v in report.items() if k not in ("source_inputs_sha256","relative_unit_value_country_summary",
  "sensitivity_scenarios","known_limitations","top10_static_mfn_exposure")},indent=2),flush=True)
if __name__=="__main__":main()
