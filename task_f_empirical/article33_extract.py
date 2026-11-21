#!/usr/bin/env python3
"""Task F Article 33 2026/1395: independently sourced chapter-level 61-63 EU origin values.
Use full 2027 Annex I column C GSP beneficiary roster (64 codes, transcribed from official OJ
2026/1395 pages 35-41), with Belarus full withdrawal sensitivity. Backcast historical
trade with 2027 roster is explicitly DESCRIPTIVE, not retrospective legal test.
No zeros imputed for unreported partner rows; all-origin denominators are official EXT aggregate.
"""
import pathlib,csv,io,gzip,urllib.request,hashlib,datetime,json,time,decimal
from decimal import Decimal
from collections import Counter,defaultdict
import importlib.util
ROOT=pathlib.Path("task_f_empirical/article33")
SRC="https://ec.europa.eu/eurostat/api/comext/dissemination/sdmx/2.1/data/DS-045409/"
ACT="https://eur-lex.europa.eu/eli/reg/2026/1395/oj/eng"
CHAPTERS=["61","62","63"]
# Annex I column C, applicable 2027; source Official Journal 2026, pp.35-41.
GSP27=set("AF AO BD BF BI BJ BO BT BY CD CF CG CK CV DJ ER ET FM GM GN GW HT IN KG KH KI KM LA LK LR LS MG ML MM MN MR MW MZ NE NG NP NU PH PK RW SB SD SL SN SO SS ST SY TD TG TJ TL TV TZ UG UZ VU YE ZM".split())
EBA=set("AF AO BD BF BI BJ BT CD CF DJ ER ET GM GN GW HT KH KI KM LA LR LS MG ML MM MR MW MZ NE NP RW SB SD SL SN SO SS ST TD TG TL TV TZ UG YE ZM".split())
TRANS_GSP_PLUS=set("BO CV KG LK MN PH PK UZ".split())
# EU countries have no place in the extra-EU origin denominator.
EU=set("AT BE BG HR CY CZ DK EE FI FR DE EL HU IE IT LV LT LU MT NL PL PT RO SK SI ES SE GR".split())
# Reuse the independently vetted two-letter country-code roster from Task C's audit.
spec=importlib.util.spec_from_file_location('task_c_country_audit','task_c_competitor_data/qa_task_c_full.py')
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
ISO2=mod.ISO
def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def h(raw):return hashlib.sha256(raw).hexdigest()
def write(name,cols,rows):
 p=ROOT/name
 with p.open("w",newline="",encoding="utf-8") as f:w=csv.DictWriter(f,fieldnames=cols,extrasaction="ignore");w.writeheader();w.writerows(rows)
def load_raw(url,year,dest):
 entry={"year":year,"source_url":url,"requested_utc":utc(),"retrieval_error":""}
 for attempt in range(3):
  try:
   with urllib.request.urlopen(urllib.request.Request(url,headers={"User-Agent":"University-of-Dhaka-Article33-2026-EU-GSP-academic/1.0"}),timeout=90) as resp:
    b=resp.read(16_000_000)
    entry["status"]=resp.status
    entry["content_type"]=resp.headers.get("Content-Type","")
   rows=list(csv.DictReader(io.StringIO(b.decode("utf-8-sig"))))
   if not rows or not all(r["product"] in CHAPTERS and r["reporter"]=="EU27_2020" and r["flow"]=="1" and r["indicators"]=="VALUE_IN_EUROS" and r["TIME_PERIOD"]==str(year) for r in rows):raise ValueError("Unexpected series")
   entry.update({"sha256":h(b),"bytes":len(b),"record_count":len(rows),"content_last_update":rows[0].get("LAST UPDATE","")})
   dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(gzip.compress(b,compresslevel=6))
   return entry,rows
  except Exception as e:
   entry["retrieval_error"]=repr(e)
   if attempt<2:time.sleep(2*(attempt+1))
 return entry,None
def main():
 assert len(GSP27)==64
 assert GSP27.issuperset(EBA) and "BD" in EBA and "BY" in GSP27
 ROOT.mkdir(parents=True,exist_ok=True)
 roster=[]
 for c in sorted(GSP27):
  status=("FULLY_WITHDRAWN" if c=="BY" else "PARTIALLY_WITHDRAWN" if c=="KH" else
    "EBA_STATUS_2027" if c in EBA else
    "TRANSITIONAL_GSP_PLUS_TO_2028" if c in TRANS_GSP_PLUS else "STANDARD_GSP")
  roster.append({"partner":c,"annex_I_2027_status":status,
   "include_in_primary_denominator":1,
   "include_in_belarus_exclusion_sensitivity":int(c!="BY"),
   "source":ACT+" Annex I columns A and C, pp. 35–41"})
 write("gsp_2027_annexI_roster_64.csv",
  ["partner","annex_I_2027_status","include_in_primary_denominator","include_in_belarus_exclusion_sensitivity","source"],roster)
 rec=[];error=[];long=[];yearly=[];byorigin=[]
 for year in range(2012,2026):
  url=SRC+f"A.EU27_2020..61+62+63.1.VALUE_IN_EUROS?format=SDMX-CSV&startPeriod={year}&endPeriod={year}"
  receipt,rows=load_raw(url,year,ROOT/"raw"/f"{year}_chapter61_63.csv.gz")
  rec.append(receipt)
  if rows is None:error.append({"year":year,"error":receipt["retrieval_error"]});continue
  for r in rows:
   long.append({"year":year,"chapter":r["product"],"origin":r["partner"],"value_eur":r["OBS_VALUE"]})
  data={(r["product"],r["partner"]):Decimal(r["OBS_VALUE"]) for r in rows}
  assert len(data)==len(rows),"Duplicated chapter origin key"
  countries={o for chap,o in data if o in ISO2 and o not in EU}
  total_gsp=Decimal(0);total_gsp_noBY=Decimal(0);total_all=Decimal(0);total_bd=Decimal(0)
  details=[]
  for chap in CHAPTERS:
   euro=data.get((chap,"EXT_EU27_2020"));bd=data.get((chap,"BD"))
   if euro is None or bd is None:raise ValueError("Required official EU extraEU and BD chapter missing "+str((year,chap)))
   value_gsp=sum((data.get((chap,o),Decimal(0)) for o in GSP27),Decimal(0))
   value_gsp_noby=value_gsp-data.get((chap,"BY"),Decimal(0))
   total_gsp+=value_gsp;total_gsp_noBY+=value_gsp_noby;total_all+=euro;total_bd+=bd
   named=sum((data.get((chap,o),Decimal(0)) for o in countries),Decimal(0))
   details.append({"year":year,"chapter":chap,"bd_eur":str(bd),"extraEU_eur":str(euro),
      "gsp2027_roster_reported_eur":str(value_gsp),"all_named_nonEU_eur":str(named),
      "country_origin_residual_eur":str(euro-named),"countries_with_unreported_gsp_row":sum((chap,o) not in data for o in GSP27)})
  # Establish robust band: if residual unallocated imports are all GSP beneficiaries, share lower.
  residual=total_all-sum((data.get((chap,o),Decimal(0)) for chap in CHAPTERS for o in countries),Decimal(0))
  denom_low=total_gsp
  denom_high=total_gsp+max(Decimal(0),residual)
  if total_bd<=0 or total_all<=0 or total_gsp<=0:raise ValueError("Invalid official Article33 denominator")
  ratio=100*total_bd/total_gsp
  ratio_exBY=100*total_bd/total_gsp_noBY if total_gsp_noBY>0 else None
  ratio_all=100*total_bd/total_all
  bnd_low=100*total_bd/denom_high
  status="ABOVE_37" if ratio>Decimal(37) else "AT_OR_BELOW_37"
  lowerstatus="ABOVE_37" if bnd_low>Decimal(37) else "POSSIBLY_AT_OR_BELOW_37"
  yearly.append({"year":year,"bd_S11b_eur":str(total_bd),"extraEU_all_origins_S11b_eur":str(total_all),
    "gsp_beneficiaries_S11b_eur_2027_roster":str(total_gsp),
    "gsp_excluding_full_withdrawal_BY_eur":str(total_gsp_noBY),
    "BD_share_of_2027_GSP_roster_percent":str(ratio),
    "BD_share_of_GSP_excluding_BY_percent":str(ratio_exBY),
    "BD_share_of_extraEU_all_origins_percent":str(ratio_all),
    "country_origin_residual_eur":str(residual),
    "BD_GSP_share_if_all_positive_residual_GSP_percent":str(bnd_low),
    "threshold_37_status":status,"residual_sensitivity_status":lowerstatus,
    "threshold_6_exception_applicable_if_no_EBA":str(ratio_all<=Decimal(6)),
    "current_EBA_exception":True,
    "actual_article33_safeguard_2025":"INAPPLICABLE_TO_BD_WHILE_EBA",
    "roster_year":"2027_AS_BACKCAST_REFERENCE",
    "legal_interpretation":"COUNTERFACTUAL_NUMERICAL_SCREEN_NO_IMPLEMENTING_ACT",
    "source_trade_dataset":"DS-045409","reference_law":"EU_2026_1395_Article33_AnnexIV"})
  byorigin+=details
  print("YEAR",year,"S11b BD",total_bd,"all",total_all,"GSP",total_gsp,"share",str(ratio)[:10],flush=True)
  time.sleep(.35)
 write("official_annual_chapter_origin_observations.csv",["year","chapter","origin","value_eur"],long)
 write("annual_chapter_denominator_audit.csv",
   ["year","chapter","bd_eur","extraEU_eur","gsp2027_roster_reported_eur","all_named_nonEU_eur",
    "country_origin_residual_eur","countries_with_unreported_gsp_row"],byorigin)
 write("official_article33_annual_screen_2012_2025.csv",
  ["year","bd_S11b_eur","extraEU_all_origins_S11b_eur","gsp_beneficiaries_S11b_eur_2027_roster",
   "gsp_excluding_full_withdrawal_BY_eur","BD_share_of_2027_GSP_roster_percent",
   "BD_share_of_GSP_excluding_BY_percent","BD_share_of_extraEU_all_origins_percent",
   "country_origin_residual_eur","BD_GSP_share_if_all_positive_residual_GSP_percent",
   "threshold_37_status","residual_sensitivity_status",
   "threshold_6_exception_applicable_if_no_EBA","current_EBA_exception",
   "actual_article33_safeguard_2025","roster_year","legal_interpretation",
   "source_trade_dataset","reference_law"],yearly)
 write("official_chapter_request_receipts.csv",
  ["year","source_url","requested_utc","retrieval_error","status","content_type","sha256","bytes","record_count","content_last_update"],rec)
 write("official_chapter_request_failures.csv",["year","error"],error)
 summary={"created_utc":utc(),"official_data_requests":len(rec),"hash_verified_source_files":sum(bool(x.get("sha256")) for x in rec),
 "source_rows":len(long),"expected_annual_screens":14,"computed_screens":len(yearly),"complete":not error and len(yearly)==14,
 "gsp_2027_roster_size":len(GSP27),
 "primary_roster_source":"EU 2026/1395 Annex I column C, Official Journal pp.35-41",
 "article33_legal_source":ACT,
 "BD_2025":next((x for x in yearly if x["year"]==2025),None),
 "correct_37_percent_denominator":"all GSP beneficiary origins under the stated roster, not BD own world totals or only competitor six",
 "correct_6_percent_denominator":"official extraEU aggregate all origin EU imports Chapters61-63",
 "limits":["The 2027 Annex I beneficiary roster is backcast onto earlier trade observations; it is not the exact roster for earlier years.",
 "Annex I includes Belarus despite Annex II full withdrawal; we report a BY-exclusion sensitivity.",
 "Missing partner-origin records are not imputed zeros. The aggregate-minus-verified-country residual excludes non-country regional aggregate partner codes and is audited.",
 "EBA status exempts Bangladesh from Art33 automatic safeguard until a legally effective eligibility change.",
 "Art33 removal requires implementing act (not automatic consequence of arithmetic), with legal start date.",
 "Trade observations are EU imports using reported trade values, not preference utilisation." ]}
 (ROOT/"ARTICLE33_SOURCE_AND_QA.json").write_text(json.dumps(summary,indent=2))
 print("SUMMARY",json.dumps(summary,indent=2),flush=True)
 if error:raise RuntimeError("Article33 request failures")
if __name__=="__main__":main()
