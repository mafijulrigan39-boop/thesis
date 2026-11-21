#!/usr/bin/env python3
"""Independent Task E v19 QA of official source hashes, CN8/TARIC10 matrix,
source-conditional regime comparison; join trade values only without imputation.
"""
import csv,hashlib,json,pathlib,datetime
from decimal import Decimal
from collections import Counter,defaultdict
ROOT=pathlib.Path("task_e_tariff_matrix/nov2026_taric")
REF=pathlib.Path("task_e_tariff_matrix/refined_v18")
def read(p):
 with p.open("r",encoding="utf-8-sig",newline="") as f:return list(csv.DictReader(f))
def write(p,fields,rows):
 with p.open("w",newline="",encoding="utf-8") as f:w=csv.DictWriter(f,fieldnames=fields,extrasaction="ignore");w.writeheader();w.writerows(rows)
def main():
 errors=[]
 audit=json.loads((ROOT/"SOURCE_AND_SCOPE_AUDIT.json").read_text())
 source_checked=0
 for e in audit["source_receipts"]:
  p=ROOT/"official_sources"/e["source_file"]
  if not p.exists():errors.append("Source missing "+str(p));continue
  actual=hashlib.sha256(p.read_bytes()).hexdigest()
  if actual!=e["sha256"]:errors.append("SOURCE SHA mismatch "+str(p))
  else:source_checked+=1
 if source_checked!=9:errors.append("Not all nine primary source files verified")
 candidates=read(ROOT/"cn8_2026_origin_regime_aware_screen.csv")
 refined=read(REF/"CN8_country_source_qualified_rate_screen.csv")
 by={(r["cn8_2025"],r["origin"]):r for r in refined}
 selection=read(pathlib.Path("task_c_competitor_data/full/selected_top200_2025.csv"))
 cn8={r["cn8"] for r in selection}
 vals={r["cn8"]:Decimal(r["bd_2025_source_eur"]) for r in selection}
 n=0;miss=0;zero=0;byorigin=defaultdict(Counter);summary=defaultdict(dict)
 seen=set()
 for r in candidates:
  key=(r["cn8_2025"],r["origin"])
  if key in seen:errors.append("Duplicate CN8 country "+str(key))
  seen.add(key)
  if key[0] not in cn8:errors.append("Unknown CN8 "+str(key))
  if r["date_2026_11_01"]!="2026-11-01":errors.append("Date mismatch "+str(key))
  other=by.get(key)
  if not other:errors.append("Other extraction missing "+str(key));continue
  a=r["potential_eligible_advalorem_pct"];b=other["2026_simple_candidate_pct_all_leaves"]
  if bool(a)!=bool(b) or (a and Decimal(a)!=Decimal(b)):
   errors.append("Independent extraction rate mismatch "+str(key))
  if a:
   n+=1;byorigin[key[1]]["numeric_candidate"]+=1
   if Decimal(a)==0:zero+=1;byorigin[key[1]]["zero"]+=1
   else:byorigin[key[1]]["positive"]+=1
   if Decimal(a)<0 or Decimal(a)>100:errors.append("Unreasonable percent "+str(key))
  else:
   miss+=1;byorigin[key[1]]["unresolved"]+=1
   if r["status"]=="CONSISTENT_ALL_LEAVES_CONDITIONAL":errors.append("Unresolved marked consistent "+str(key))
  byorigin[key[1]][r["duty_channel"] or "NOT_VERIFIED"]+=1
  summary[key[0]][key[1]]=r
 if len(candidates)!=1400 or len(seen)!=1400:errors.append("CN8-origin matrix not 1400 unique cells")
 if len(cn8)!=200 or len(summary)!=200:errors.append("Not 200 source products")
 if n!=1383 or miss!=17:errors.append("Numerical coverage mismatch")
 if byorigin['BD']['zero']!=200:errors.append("Bangladesh EBA zero candidate not on every product")
 fields=['cn8_2025','bangladesh_import_value_2025_eur','mfn_2026_source_pct','bd_eba_2026_candidate_pct',
         'cn_origin_candidate_pct','in_origin_candidate_pct','vn_origin_candidate_pct','pk_origin_candidate_pct',
         'kh_origin_candidate_pct','tr_origin_candidate_pct',
         'cn_origin_channel','in_origin_channel','vn_origin_channel','pk_origin_channel',
         'kh_origin_channel','tr_origin_channel','unresolved_origin_count',
         'applicability_date','2027_plus_actual_BD_gsp_status','source_trade_year','source_tariff_date']
 joint=[]
 for p in [r["cn8"] for r in selection]:
  d=summary.get(p,{})
  def row(o):return d.get(o,{})
  mfn=row('BD')
  # MFN 2026 selected 200 lines is independently in the source-specific 2026 scenario matrix.
  source_screen=read(ROOT/"top200_seven_origin_nov2026_tariff_scenarios_NO_IMPUTATION.csv") if False else None
  joined={'cn8_2025':p,'bangladesh_import_value_2025_eur':str(vals[p]),
          'mfn_2026_source_pct':'','bd_eba_2026_candidate_pct':row('BD').get("potential_eligible_advalorem_pct",""),
          'applicability_date':'2026-11-01','2027_plus_actual_BD_gsp_status':'NOT_YET_VERIFIED',
          'source_trade_year':'2025','source_tariff_date':'2026-11-01',
          'unresolved_origin_count':sum(not row(o).get("potential_eligible_advalorem_pct","") for o in ('BD','CN','IN','VN','PK','KH','TR'))}
  for o in ['CN','IN','VN','PK','KH','TR']:
   joined[o.lower()+"_origin_candidate_pct"]=row(o).get('potential_eligible_advalorem_pct','')
   joined[o.lower()+"_origin_channel"]=row(o).get('duty_channel','')
  joint.append(joined)
 screen=read(ROOT/"top200_seven_origin_nov2026_tariff_scenarios_NO_IMPUTATION.csv")
 mfn={r['cn8_2025']:r['mfn_pct'] for r in screen if r['origin']=='BD'}
 for z in joint:z["mfn_2026_source_pct"]=mfn.get(z["cn8_2025"],"")
 write(ROOT/"TaskE_tariff_2026_join_2025_trade_values.csv",fields,joint)
 result={"audit_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),
         "passed":not errors,"issues":errors[:100],
         "reference_date":"2026-11-01","official_CIRCABC_XLSX_hashes_verified":source_checked,
         "independent_Cn8_origin_candidate_rate_comparisons":len(candidates),
         "rate_agreements":len(candidates)-sum("rate mismatch" in e for e in errors),
         "consistent_numeric_candidates":n,"uncertified_or_complex":miss,
         "source_bangladesh_2026_eba_zero_candidates":byorigin['BD']['zero'],
         "by_origin":{k:dict(v) for k,v in byorigin.items()},
         "matched_2025_trade_values":len(joint),
         "limitations":["2025 trade basket joined to 2026-11-01 tariff snapshot, not 2025 applied rates",
                        "Country-of-origin preference entitlement and actual utilization not independently verified",
                        "Türkiye customs-union treatment requires A.TR free-circulation verification",
                        "GSP+ and Standard GSP 2027+ Bangladesh scenario rates remain legally unverified",
                        "No automatic substitution for 17 unresolved origin-product rate candidates",
                        "Conditional/specific/compound duties and other charges remain separate",
                        "2025-2026 CN8 validity and product-level rules of origin require final independent audit."]}
 (ROOT/"INDEPENDENT_QA_AND_CROSSCHECK.json").write_text(json.dumps(result,indent=2))
 print(json.dumps(result,indent=2),flush=True)
 if errors:raise RuntimeError("Task E QA failed: "+str(errors[:5]))
if __name__=="__main__":main()
