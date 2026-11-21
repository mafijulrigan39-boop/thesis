#!/usr/bin/env python3
"""Task E downstream policy comparison, preserving three separate channels:
third-country MFN duty, tariff-preference measure (142), customs-union duty (106).
No 2027/2032 scenario rate imputed from a 2026 source.
"""
import csv,datetime,json,pathlib,re
from collections import defaultdict,Counter
from decimal import Decimal
ROOT=pathlib.Path("task_e_tariff_matrix/nov2026_taric")
SCHEMES={"BD":"EBA_2026","CN":"MFN_2026","IN":"STANDARD_GSP_2026_SUBJECT_TO_GRADUATION","VN":"EU_VIETNAM_FTA_2026",
"PK":"GSP_PLUS_2026_SUBJECT_TO_WD","KH":"CAMBODIA_EBA_PARTIALLY_WITHDRAWN_2026",
"TR":"EU_TURKIYE_CUSTOMS_UNION_FREE_CIRCULATION_OR_OTHER"}
FIELDS=["reference_date","cn8_2025","taric10_2026","origin","scheme","eligible_rate_pct",
"eligible_rate_expression","rate_route","eligibility_status","MFN_pct","preference_pct","customs_union_pct",
"other_taric_measures","measure_document_start","measure_document_end","measure_type","origin_group","legal_basis",
"conditions","footnotes","taric_reuse_status","source_url"]
def read(p):
 with p.open("r",encoding="utf-8-sig",newline="") as f:return list(csv.DictReader(f))
def write(p,cols,rows):
 with p.open("w",encoding="utf-8",newline="") as f:w=csv.DictWriter(f,fieldnames=cols,extrasaction="ignore");w.writeheader();w.writerows(rows)
def basic(measures):
 if not measures:return None,None
 if any(not m["simple_adval_pct"] or m["additional_code"] or m["quota_order"] or int(m["condition_row_count"])>0 for m in measures):return None,None
 rates={Decimal(m["simple_adval_pct"]) for m in measures}
 if len(rates)!=1:return None,None
 rate=next(iter(rates));return str(rate),next(iter({m["duty_expression"] for m in measures}))
def main():
 rates=read(ROOT/"dated_taric10_origin_rate_candidates.csv")
 facts=read(ROOT/"dated_taric10_origin_measure_evidence.csv")
 raw=read(ROOT/"top200_seven_origin_nov2026_tariff_scenarios_NO_IMPUTATION.csv")
 bykey=defaultdict(list)
 for row in facts:bykey[(row["cn8_2025"],row["taric10_2026"],row["origin"])].append(row)
 out=[];count=Counter()
 for r in rates:
  key=(r["cn8_2025"],r["taric10_2026"],r["origin"])
  rows=bykey.get(key,[])
  channel=lambda code:[x for x in rows if x["measure_type_code"]==code]
  mfn,pr,cu=channel("103"),channel("142"),channel("106")
  mfn_rate,mfn_expr=basic(mfn);pr_rate,pr_expr=basic(pr);cu_rate,cu_expr=basic(cu)
  if cu_rate is not None and r["origin"]=="TR":
   src=cu;use=cu_rate;expr=cu_expr;route="CUSTOMS_UNION_DUTY_CANDIDATE"
   qualify="REQUIRES_A_TR_FREE_CIRCULATION_AND_SCOPE_VERIFICATION_NOT_AUTOMATIC"
  elif pr_rate is not None:
   src=pr;use=pr_rate;expr=pr_expr;route="TARIFF_PREFERENCE_CANDIDATE"
   qualify="REQUIRES_VALID_PREFERENCE_ORIGIN_PROOF_AND_COUNTRY_PRODUCT_ELIGIBILITY"
  elif mfn_rate is not None and not pr and not cu:
   src=mfn;use=mfn_rate;expr=mfn_expr;route="MFN_FALLBACK_CANDIDATE"
   qualify="THIRD_COUNTRY_DUTY_BENCHMARK_NOT_FINAL_PAYABLE_DUTY"
  else:
   src=[];use="";expr="";route="NOT_VERIFIED_COMPLEX_CONFLICT_OR_MISSING"
   qualify="DO_NOT_IMPUTE_APPLIED_DUTY"
  count[route]+=1
  srcrow=src[0] if src else {}
  other=sum(x["scheme"] not in ("MFN","PREFERENCE_MEASURE","CUSTOMS_UNION") for x in rows)
  out.append({"reference_date":r["reference_date"],"cn8_2025":r["cn8_2025"],
   "taric10_2026":r["taric10_2026"],"origin":r["origin"],
   "scheme":SCHEMES.get(r["origin"],"UNVERIFIED"),"eligible_rate_pct":use,
   "eligible_rate_expression":expr,"rate_route":route,"eligibility_status":qualify,
   "MFN_pct":mfn_rate or "","preference_pct":pr_rate or "","customs_union_pct":cu_rate or "",
   "other_taric_measures":other,
   "measure_document_start":srcrow.get("start_date",""),"measure_document_end":srcrow.get("end_date",""),
   "measure_type":srcrow.get("measure_type",""),"origin_group":srcrow.get("geo_code",""),
   "legal_basis":srcrow.get("legal_base",""),"conditions":srcrow.get("condition_row_count",""),
   "footnotes":srcrow.get("footnotes",""),"taric_reuse_status":"SOURCE_DATE_2026_11_01_CURRENT_ONLY",
   "source_url":r["source_url"]})
 write(ROOT/"origin_taric10_regime_aware_duty_candidates_2026.csv",FIELDS,out)
 # Aggregation only if every active declarable 2026 TARIC10 leaf of 2025 CN8
 # has the same rate and same eligibility channel (or distinct routes recorded).
 grouped=defaultdict(list)
 for r in out:grouped[(r["cn8_2025"],r["origin"])].append(r)
 ans=[];codes=sorted({r["cn8_2025"] for r in raw},key=lambda p:list(dict.fromkeys(x["cn8_2025"] for x in raw)).index(p))
 for p in codes:
  for o in SCHEMES:
   rr=grouped.get((p,o),[])
   values={r["eligible_rate_pct"] for r in rr if r["eligible_rate_pct"]}
   routes={r["rate_route"] for r in rr}
   strict=(bool(rr) and len(values)==1 and
      all(x["eligible_rate_pct"] for x in rr) and len(routes)==1 and
      not any(x["rate_route"]=="NOT_VERIFIED_COMPLEX_CONFLICT_OR_MISSING" for x in rr))
   ans.append({"date_2026_11_01":"2026-11-01","cn8_2025":p,"origin":o,
     "scheme_regime_2026":SCHEMES[o],"number_taric10_leaves":len(rr),
     "potential_eligible_advalorem_pct":next(iter(values)) if strict else "",
     "duty_channel":next(iter(routes)) if strict else "",
     "status":"CONSISTENT_ALL_LEAVES_CONDITIONAL" if strict else "NOT_UNIQUE_OR_COMPLEX_CANNOT_AGGREGATE",
     "claim_status":"NOT_VERIFIED_ACTUAL_PROOF_OF_ORIGIN_OR_FREE_CIRCULATION",
     "2027_standard_GSP_BD_rate":"","2027_GSP_PLUS_BD_rate":"","2032_after_EBA_transition_BD_rate":"",
     "future_scenarios_status":"UNCONFIRMED_FUTURE_CONDITIONAL","source_url":rr[0]["source_url"] if rr else ""})
 write(ROOT/"cn8_2026_origin_regime_aware_screen.csv",
 ["date_2026_11_01","cn8_2025","origin","scheme_regime_2026","number_taric10_leaves",
 "potential_eligible_advalorem_pct","duty_channel","status","claim_status","2027_standard_GSP_BD_rate",
 "2027_GSP_PLUS_BD_rate","2032_after_EBA_transition_BD_rate","future_scenarios_status","source_url"],ans)
 cov=Counter(r["status"] for r in ans);byorigin=defaultdict(Counter)
 for r in ans:byorigin[r["origin"]][r["status"]]+=1
 report={"date":"2026-11-01","generated_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),
 "taric10_origin_records":len(out),"cn8_origin_records":len(ans),"route_counts":dict(count),
 "cn8_coverage":dict(cov),"by_origin":{o:dict(c) for o,c in byorigin.items()},
 "warnings":["Türkiye 106 customs union duty is NOT equal to preferential origin measure 142 and depends on A.TR free circulation.",
 "A current 2026 preference is only a candidate, not automatically utilized.",
 "Complex, specific, compound, conditional duties do not acquire a numeric ad valorem by assumption.",
 "November 2026 source only; do not infer a 2027 legal rate from older GSP schedules.",
 "Product continuity from 2025 CN8 to 2026 TARIC is not yet source-certified against 2025 code lists."]}
 (ROOT/"REGIME_AWARE_QA_SUMMARY.json").write_text(json.dumps(report,indent=2))
 print(json.dumps(report,indent=2),flush=True)
if __name__=="__main__":main()
