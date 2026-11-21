#!/usr/bin/env python3
"""Independent Task G standard-library robustness and hypothesis QA.
Tests are EXPLORATORY on a nonrandom top-200 cohort; NO causal identification.
"""
import csv,hashlib,json,math,random,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"task_g"/"out"; SEED=20261121
FILES={
"p":"task_f_empirical/full/product_2025_value_share_price_tariff_exposure.csv",
"c":"task_f_empirical/full/product_origin_2025_competitiveness_2026_tariff_candidates.csv",
"s":"task_f_empirical/full/scenario_scope_tariff_exposure_sensitivity.csv",
"a":"task_f_empirical/article33/official_article33_annual_screen_2012_2025.csv",
"f":"task_f_empirical/full/TASK_F_EMPIRICAL_RESULTS.json"
}
def data(path):
 with path.open(newline="",encoding="utf-8-sig") as f:return list(csv.DictReader(f))
def N(v):return float(v) if v is not None and v!="" else None
def mean(v):return sum(v)/len(v)
def median(v):
 v=sorted(v); n=len(v)
 return (v[n//2] if n%2 else (v[n//2-1]+v[n//2])/2) if n else None
def ranks(v):
 a=sorted(enumerate(v),key=lambda z:z[1]);res=[0.0]*len(v);i=0
 while i<len(a):
  j=i+1
  while j<len(a) and a[i][1]==a[j][1]:j+=1
  for k in range(i,j):res[a[k][0]]=(i+1+j)/2
  i=j
 return res
def pearson(x,y):
 mx,my=mean(x),mean(y); xx=[a-mx for a in x];yy=[a-my for a in y]
 den=math.sqrt(sum(v*v for v in xx)*sum(v*v for v in yy))
 return sum(a*b for a,b in zip(xx,yy))/den if den else 0
def perm_diff(x,y,reps=9999):
 rng=random.Random(SEED); obs=mean(x)-mean(y); pool=x+y;hits=0;n=len(x)
 for _ in range(reps):
  rng.shuffle(pool)
  if mean(pool[:n])-mean(pool[n:])>=obs-1e-12:hits+=1
 return obs,(hits+1)/(reps+1)
def perm_rho(x,y,reps=9999):
 rng=random.Random(SEED+1); rx=ranks(x);ry=ranks(y);obs=pearson(rx,ry);hits=0
 for _ in range(reps):
  rng.shuffle(ry)
  if abs(pearson(rx,ry))>=abs(obs)-1e-12:hits+=1
 return obs,(hits+1)/(reps+1)
def bootstrap(x,y,reps=1999):
 rng=random.Random(SEED+2);b=[]
 for _ in range(reps):
  b.append(mean([x[rng.randrange(len(x))] for _ in x])-mean([y[rng.randrange(len(y))] for _ in y]))
 b.sort()
 return [b[int((reps-1)*.025)],b[int((reps-1)*.975)]]
def p_sign(k,n):
 return sum(math.comb(n,j) for j in range(k,n+1))/2**n
def emit(name,records,columns):
 with (OUT/name).open("w",newline="",encoding="utf-8") as f:
  w=csv.DictWriter(f,fieldnames=columns);w.writeheader();w.writerows(records)
def main():
 OUT.mkdir(parents=True,exist_ok=True)
 p,c,s,a=(data(ROOT/FILES[k]) for k in ("p","c","s","a"))
 f=json.loads((ROOT/FILES["f"]).read_text())
 assert len(p)==200 and len({r["cn8_2025"] for r in p})==200
 assert len(c)==1200 and len({(r["cn8_2025"],r["origin"]) for r in c})==1200
 assert len(s)==40 and len(a)==14
 assert all(r["historical_growth_status"]=="BLOCKED_TASK_B_SOURCE_PROVENANCE" for r in p)
 assert f["HARMONIZED_CN8_CAGR_CERTIFIED"] is False and f["future_tariff_scenarios_certified"] is False
 receipts=[]
 for item in f["source_inputs_sha256"]:
  path=ROOT/item["file"];sha=hashlib.sha256(path.read_bytes()).hexdigest()
  receipts.append(dict(file=item["file"],expected_sha256=item["sha256"],observed_sha256=sha,passed=sha==item["sha256"]))
 assert all(r["passed"] for r in receipts),"Source data checksum failure"
 for key,path in FILES.items():
  receipts.append(dict(file=path,expected_sha256="record_only",observed_sha256=hashlib.sha256((ROOT/path).read_bytes()).hexdigest(),passed="documented"))
 emit("SOURCE_CHECKSUMS.csv",receipts,["file","expected_sha256","observed_sha256","passed"])
 v=lambda r:N(r["bangladesh_import_value_eur_2025"])
 q=[r for r in p if N(r["mfn_2026_reference_pct"]) is not None]
 missing=[r for r in p if N(r["mfn_2026_reference_pct"]) is None]
 total=sum(map(v,p));qual=sum(map(v,q))
 mfn=sum(N(r["MFN_reference_static_duty_equivalent_eur"]) or 0 for r in p)
 assert total==20789281101 and len(q)==196 and len(missing)==4
 assert sum(map(v,missing))==131083237 and abs(mfn-2443135906.980)<.01
 for r in q:
  expected=v(r)*(N(r["mfn_2026_reference_pct"])-N(r["eba_BD_2026_candidate_pct"]))/100
  assert abs(expected-N(r["MFN_reference_static_duty_equivalent_eur"]))<.01
 ap=[r for r in q if r["hs2"] in ("61","62","63")]
 ot=[r for r in q if r["hs2"] not in ("61","62","63")]
 x=[N(r["mfn_2026_reference_pct"]) for r in ap]
 y=[N(r["mfn_2026_reference_pct"]) for r in ot]
 difference,pg=perm_diff(x,y); ci=bootstrap(x,y)
 rho,pr=perm_rho([N(r["bangladesh_share_extraEU_pct_2025"]) for r in q],
                 [N(r["mfn_2026_reference_pct"]) for r in q])
 tests=[
 dict(h="H1",test="one-sided permutation: mean 2026 MFN rate S11b > other",n=196,effect=difference,p_value=pg,q_value="",interval=str(ci),interpretation="exploratory tariff-rate gap, no impact identification"),
 dict(h="H2",test="two-sided permutation Spearman: 2025 market share vs 2026 MFN rate",n=196,effect=rho,p_value=pr,q_value="",interval="",interpretation="exploratory association, not causal")]
 for origin in ("CN","IN","VN","PK","KH","TR"):
  r=[N(z["bd_to_competitor_eur_per_kg_ratio_2025"]) for z in c if z["origin"]==origin]
  r=[z for z in r if z is not None and z>0 and abs(z-1)>1e-10];k=sum(z<1 for z in r)
  tests.append(dict(h="H3_"+origin,test="one-sided exact paired sign: BD EUR/kg < competitor",n=len(r),effect=k/len(r),p_value=p_sign(k,len(r)),q_value="",interval="",interpretation="valid CN8 matched unit values, not equal product quality"))
 six=sorted(range(2,8),key=lambda i:tests[i]["p_value"]);minq=1.0
 for pos in range(5,-1,-1):
  idx=six[pos];minq=min(minq,6*tests[idx]["p_value"]/(pos+1))
  tests[idx]["q_value"]=minq
 # Sensitivity: partial-rank association after removing HS2 chapter fixed effects.
 # This is NOT a causal model; many small HS2 groups have no rate variation.
 rank_share=ranks([N(r["bangladesh_share_extraEU_pct_2025"]) for r in q])
 rank_tariff=ranks([N(r["mfn_2026_reference_pct"]) for r in q])
 hs2_groups={}
 for i,r in enumerate(q):hs2_groups.setdefault(r["hs2"],[]).append(i)
 share_res=rank_share[:];rate_res=rank_tariff[:]
 for indices in hs2_groups.values():
  mx=mean([rank_share[i] for i in indices]);my=mean([rank_tariff[i] for i in indices])
  for i in indices:share_res[i]-=mx;rate_res[i]-=my
 adjusted_rho=pearson(share_res,rate_res)
 rng=random.Random(SEED+3);adjusted_hits=0
 for _ in range(9999):
  shuffled=rate_res[:]
  for indices in hs2_groups.values():
   sh=[shuffled[i] for i in indices];rng.shuffle(sh)
   for i,vv in zip(indices,sh):shuffled[i]=vv
  if abs(pearson(share_res,shuffled))>=abs(adjusted_rho)-1e-12:adjusted_hits+=1
 adjusted_p=(adjusted_hits+1)/10000
 tests.append(dict(h="H2_HS2_ADJUSTED",test="post-hoc within-HS2 partial-rank permutation, two-sided",
     n=len(q),effect=adjusted_rho,p_value=adjusted_p,q_value="",interval="",
     interpretation="sector-adjusted exploratory sensitivity; NOT confirmatory or causal"))
 emit("HYPOTHESIS_TESTS.csv",tests,["h","test","n","effect","p_value","q_value","interval","interpretation"])
 robustness=[]
 def put(kind,case,n_,value,unit,note):robustness.append(dict(kind=kind,case=case,n=n_,value=value,unit=unit,note=note))
 for year in (2023,2024,2025):
  r=next(v for v in a if int(v["year"])==year)
  expected=100*N(r["bd_S11b_eur"])/N(r["gsp_beneficiaries_S11b_eur_2027_roster"])
  assert abs(expected-N(r["BD_share_of_2027_GSP_roster_percent"]))<1e-8
  worst=N(r["BD_GSP_share_if_all_positive_residual_GSP_percent"])
  assert expected>37 and worst>37
  put("YEAR_2027_ROSTER_BACKCAST",str(year),None,expected,"pct","not an actual-year legal finding")
  put("YEAR_RESIDUAL_ALL_GSP",str(year),None,worst,"pct","positive country residual assigned wholly to GSP")
 for label,subset in [
  ("TOP200",p),
  ("2025_EXACT_1_TO_1",[r for r in p if r["classification_2025_type_derived"]=="1:1_exact"]),
  ("2025_COMPLEX_NONEXACT",[r for r in p if r["classification_2025_type_derived"]!="1:1_exact"]),
  ("HS2_61_63",[r for r in p if r["hs2"] in ("61","62","63")]),
  ("OTHER_HS2",[r for r in p if r["hs2"] not in ("61","62","63")])]:
  put("CLASSIFICATION_SECTOR",label,len(subset),
      sum(N(r["MFN_reference_static_duty_equivalent_eur"]) or 0 for r in subset),
      "EUR","2025 values times Nov2026 conditional tariff rates; not losses")
 for r in s:
  if r["subset"]=="TOP200":
   put("2026_SOURCE_TARIFF_SCENARIO",r["scenario"],int(r["products_numeric_qualified"]),
       N(r["static_additional_duty_equivalent_eur"]),"EUR","different coverage across scenarios")
 for pp in (0,5,10,15,20):
  put("4_MISSING_RATE_STRESS",str(pp)+"pp",4,mfn+131083237*pp/100,"EUR","hypothetical extra rate; NOT legal imputation")
 for o in ("CN","IN","VN","PK","KH","TR"):
  cc=[r for r in c if r["origin"]==o and N(r["competitor_2026_source_conditional_rate_pct"]) is not None]
  wavg=sum(N(r["bd_imports_eur_2025"])*N(r["bd_preference_margin_vs_origin_pp"]) for r in cc)/sum(N(r["bd_imports_eur_2025"]) for r in cc)
  put("SINGLE_ORIGIN",o,len(cc),wavg,"percentage_points","conditional 2026 margin, not utilisation")
 for name,origins in (("CN_IN",("CN","IN")),("VN_PK_KH_TR",("VN","PK","KH","TR"))):
  cc=[r for r in c if r["origin"] in origins and N(r["competitor_2026_source_conditional_rate_pct"]) is not None]
  wavg=sum(N(r["bd_imports_eur_2025"])*N(r["bd_preference_margin_vs_origin_pp"]) for r in cc)/sum(N(r["bd_imports_eur_2025"]) for r in cc)
  put("SUPPLIER_GROUP",name,len(cc),wavg,"percentage_points","unequal rate coverage: comparability conditional")
 # Alternate-year raw-code coverage audit. All 200 rows are a designed matrix, NOT 200 observed cells.
 historic=data(ROOT/"task_c_competitor_data/full/product_year_bd_market_share_2012_2025.csv")
 year_audit=[]
 for year in (2012,2023,2024,2025):
  sub=[r for r in historic if int(r["year"])==year]
  assert len(sub)==200,"Expected fixed-2025-code extraction grid, not observed-row count"
  vc=sum(r["status"]=="VALID" for r in sub)
  miss_bd=sum(r["status"]=="MISSING_BANGLADESH_VALUE" for r in sub)
  miss_all=sum(r["status"]=="MISSING_EXTRA_EU_TOTAL" for r in sub)
  assert vc+miss_bd+miss_all==200,"Unknown missingness status"
  for st in ("VALID","MISSING_BANGLADESH_VALUE","MISSING_EXTRA_EU_TOTAL"):
   cnt=sum(r["status"]==st for r in sub)
   put("FIXED_2025_CODE_YEAR_COVERAGE",str(year)+"_"+st,cnt,float(cnt)/2,"percent_of_200",
       "Rectangular raw-code audit; 2012-2024 CN8 meaning NOT harmonized; missing is not zero")
  year_audit.append(dict(year=year,fixed_2025_code_grid_rows=200,
     valid_value_and_denominator=vc,missing_bd_value=miss_bd,missing_extra_eu_total=miss_all,
     historical_cn8_compatibility="2025_NATIVE" if year==2025 else "UNCERTIFIED"))
 emit("YEAR_BY_YEAR_MISSINGNESS.csv",year_audit,
      ["year","fixed_2025_code_grid_rows","valid_value_and_denominator",
       "missing_bd_value","missing_extra_eu_total","historical_cn8_compatibility"])
 emit("ROBUSTNESS_RESULTS.csv",robustness,["kind","case","n","value","unit","note"])
 gaps=[
 ("M01","MFN rates",4,"131083237 EUR","No rate imputed"),
 ("M02","historical CN code and crosswalk originals",27,"14+13 files","Historical CN8 CAGR blocked"),
 ("M03","matched unit values",14,"out of 1200","Exclude invalid EUR/kg pairs"),
 ("M04","conditional partner tariff candidates",17,"out of 1200","No rate imputation"),
 ("M05","supplier HHI origin residual",163,"out of 200","Supplier-origin HHI provisional"),
 ("M06","future Bangladesh GSP/ROO and utilisation","unknown","legal/process","Not forward payable tariff"),
 ("M07","applicable-year GSP roster","unknown","2027 roster backcast","Article33 numerical only"),
 ("M08","MITB supervisor signoff","pending","project paper","Not approved"),
 ]
 emit("MISSING_DATA_REGISTER.csv",[dict(id=i,domain=d,count=n,quantity=q,decision=t) for i,d,n,q,t in gaps],
      ["id","domain","count","quantity","decision"])
 result={
 "qa":"PASS_NUMERICAL_WITH_OPEN_ACADEMIC_GATES",
 "source_sha256_passed":len(f["source_inputs_sha256"]),
 "product_lines":len(p),"bd_eur_2025":int(total),"mfn_numeric_lines":196,
 "mfn_rate_missing_value_eur":131083237,"mfn_static_duty_equivalent_eur":round(mfn,3),
 "H1_gap_pp":difference,"H1_p":pg,"H1_bootstrap_ci_pp":ci,
 "H2_spearman_rho":rho,"H2_p":pr,
 "historical_product_growth_certified":False,"future_tariffs_certified":False,
 "supervisor_scope_approval":"PENDING",
 "statistical_limits":"post-hoc exploratory associations; nonrandom top-200 CN8; no causal identification"}
 result["H2_within_HS2_partial_rank_rho"]=adjusted_rho
 result["H2_within_HS2_permutation_p"]=adjusted_p
 (OUT/"QA_SUMMARY.json").write_text(json.dumps(result,indent=2)+"\n")
 print(json.dumps(result,indent=2))
 print("TASK_G_OUTPUT_FILES:",",".join(sorted(p.name for p in OUT.iterdir())))
if __name__=="__main__":
 try:main()
 except Exception as e:
  print("TASK_G_FAILED",repr(e),file=sys.stderr)
  raise
