#!/usr/bin/env python3
"""Task E: collect official DG TAXUD November 2026 TARIC source XLSX and build
evidence-preserving CN8/TARIC10 tariff measures. NO imputed rates.
Snapshot 2026-11-01. Sources direct CIRCABC official node URLs.
"""
import csv,datetime,hashlib,io,json,pathlib,re,urllib.request,base64,time,zipfile,xml.etree.ElementTree as ET
from collections import defaultdict,Counter
from decimal import Decimal
BASE="https://circabc.europa.eu/service/api/node/workspace/SpacesStore"
DATE=datetime.date(2026,11,1)
DIR=pathlib.Path("task_e_tariff_matrix/nov2026_taric")
ORIGINS=["BD","CN","IN","VN","PK","KH","TR"]
NODES={
 "Duties Import 01-99.xlsx":"d0b85541-ed40-4f11-81c3-d245b15adc1d",
 "Geographical areas composition.xlsx":"e8a814f1-7ca2-4c0b-a34a-b8d82d0eeeeb",
 "Measure exclusions.xlsx":"215b5316-d9f4-46ca-a6d4-1eb1355eae4d",
 "Measure conditions.xlsx":"dcf72a54-9a49-4d57-b8fa-a641e889faf9",
 "Measure footnotes.xlsx":"ef9e8bb1-1553-4889-b638-d37855f0c74a",
 "Nomenclature EN.xlsx":"41fc5fcb-88b0-4153-9d30-0bc0b01b3fde",
 "Declarable codes.xlsx":"adb9dd82-8089-4c78-8ae7-bd36eced8de8",
 "Legal basis.xlsx":"6edb3f45-4c2e-4137-b567-e112fd4fa464",
 "Geographical areas description.xlsx":"acbd49e1-0b7a-47e3-8509-534db940f0bb"
}
NS="{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
HEADERS={"User-Agent":"Mozilla/5.0 (University of Dhaka MITB thesis - TARIC source verification)","Authorization":"Basic "+base64.b64encode(b"guest:").decode()}
def stamp():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def date(s):
 s=str(s or "").strip()
 if not s:return None
 try:return datetime.datetime.strptime(s,"%d-%m-%Y").date()
 except ValueError:return None
def live(row,start="Start date",end="End date"):
 d=date(row.get(start));e=date(row.get(end))
 return (not d or d<=DATE) and (not e or e>=DATE)
def csvfile(p,fields,rows):
 p.parent.mkdir(parents=True,exist_ok=True)
 with p.open("w",encoding="utf-8",newline="") as f:
  w=csv.DictWriter(f,fieldnames=fields,extrasaction="ignore");w.writeheader();w.writerows(rows)
def sha(x):return hashlib.sha256(x).hexdigest()
def coln(s):
 i=0
 for c in re.match(r"[A-Z]+",s).group(0):i=i*26+ord(c)-64
 return i-1
def xlsx_rows(p,fn):
 """Streaming XLSX reader based only on Python XML/ZIP, preserves blank columns."""
 with zipfile.ZipFile(p) as z:
  shared=[]
  if "xl/sharedStrings.xml" in z.namelist():
   with z.open("xl/sharedStrings.xml") as f:
    for event,el in ET.iterparse(f,events=("end",)):
     if el.tag==NS+"si":
      shared.append("".join(x.text or "" for x in el.iter(NS+"t")));el.clear()
  sheet=next(x for x in z.namelist() if x=="xl/worksheets/sheet1.xml")
  header=None;n=0
  with z.open(sheet) as f:
   for event,el in ET.iterparse(f,events=("end",)):
    if el.tag!=NS+"row":continue
    cells={}
    for c in el.iter(NS+"c"):
     ref=c.attrib.get("r","")
     if not re.match(r"^[A-Z]+[0-9]+$",ref):continue
     v=c.find(NS+"v")
     x=v.text if v is not None else ""
     if c.attrib.get("t")=="s" and x:x=shared[int(x)]
     if c.attrib.get("t")=="inlineStr":
      t=c.find(NS+"is");x="".join(c.text or "" for c in t.iter(NS+"t")) if t is not None else ""
     cells[coln(ref)]=str(x or "").strip()
    if header is None:
     header=[cells.get(i,"") for i in range(max(cells)+1)]
    else:
     row={h:cells.get(i,"") for i,h in enumerate(header) if h}
     fn(row);n+=1
    el.clear()
  return n,header
def get(name,node,logs):
 out=DIR/"official_sources"/name;out.parent.mkdir(parents=True,exist_ok=True)
 url=f"{BASE}/{node}/content"
 e={"source_file":name,"source_url":url,"reference_date":str(DATE),"retrieved_utc":stamp()}
 if out.exists():
  b=out.read_bytes();e["cached"]=True
 else:
  with urllib.request.urlopen(urllib.request.Request(url,headers=HEADERS),timeout=150) as response:
   b=response.read(80000000);e["http_status"]=response.status
  if not b.startswith(b"PK"):raise ValueError(name+" not XLSX")
  out.write_bytes(b)
 e.update({"sha256":sha(b),"bytes":len(b),"http_status":e.get("http_status",200)})
 logs.append(e);print("Downloaded",name,len(b),flush=True)
 return out
def main():
 DIR.mkdir(parents=True,exist_ok=True)
 products=[]
 with open("task_c_competitor_data/full/selected_top200_2025.csv",newline="",encoding="utf-8") as f:
  for row in csv.DictReader(f):products.append(row["cn8"])
 assert len(set(products))==200 and all(re.fullmatch(r"\d{8}",p) for p in products)
 receipts=[];files={}
 for name,node in NODES.items():
  files[name]=get(name,node,receipts)
 csvfile(DIR/"official_source_receipts.csv",list(receipts[0]),receipts)
 # 2026-11-01 active nomenclature tree and declarable leaf TARIC10
 nodes={};allnodes=Counter()
 def take_nom(r):
  code=r.get("Goods code","").split()[0].strip()
  if len(code)!=10 or not code.isdigit() or not live(r):return
  try:hp=int(float(r.get("Hier. Pos.","0")))
  except:hp=0
  if hp not in (2,4,6,8,10):return
  suff=r.get("Goods code","").split()[-1] if " " in r.get("Goods code","") else ""
  if suff=="80":
   nodes[code]={"hier":hp,"description":r.get("Description",""),"nom_start":r.get("Start date",""),"nom_end":r.get("End date","")}
   allnodes[hp]+=1
 _,h=xlsx_rows(files["Nomenclature EN.xlsx"],take_nom)
 print("Nomenclature active suffix80 codes",len(nodes),flush=True)
 leaves=defaultdict(list)
 def take_decl(r):
  full=r.get("Goods code","");code=full.split()[0]
  if (len(code)==10 and code[:8] in products and r.get("IS_LEAF")=="1" and live(r)):
   if code not in leaves[code[:8]]:leaves[code[:8]].append(code)
 xlsx_rows(files["Declarable codes.xlsx"],take_decl)
 for p in leaves:leaves[p].sort()
 # groups and membership validity
 members=defaultdict(set);groups=defaultdict(set)
 def take_group(r):
  group=r.get("Country group","");member=r.get("Member country","")
  if not group or member not in ORIGINS:return
  if not live(r,"Mbship start date","Mbship end date"):return
  # Ignore groups that have ended as of snapshot.
  if date(r.get("End date")) and date(r.get("End date"))<DATE:return
  members[group].add(member);groups[member].add(group)
 xlsx_rows(files["Geographical areas composition.xlsx"],take_group)
 # Relevant ancestor/leaf measure code: hierarchy-aware *not* naive rstrip('0')
 code_to_products=defaultdict(set);codetoparent=defaultdict(set)
 for cn8,ls in leaves.items():
  for leaf in ls:
   for code,info in nodes.items():
    n=info["hier"]
    if leaf[:n]==code[:n]:
     codetoparent[leaf].add(code);code_to_products[code].add(cn8)
 print("leaf products",len(leaves),"eligible ancestor codes",len(code_to_products),flush=True)
 # Relevant measure metadata indexed by exact identity (geog start/end/add code)
 def measurekey(r):
  return (r.get("Goods code",""),r.get("Add code",""),r.get("Order No.",""),
          r.get("Start date",""),r.get("End date",""),
          r.get("Origin code",""),r.get("Meas. type code",""))
 exclusions=defaultdict(set);condcounts=Counter();footnotes=defaultdict(set)
 def get_ex(r):
  if r.get("Goods code","") not in code_to_products or not live(r):return
  excluded=r.get("Excluded country","")
  if len(excluded)==2:exclusions[measurekey(r)].add(excluded)
 def get_cond(r):
  if r.get("Goods code","") in code_to_products and live(r):
   condcounts[measurekey(r)]+=1
 def get_foot(r):
  if r.get("Goods code","") in code_to_products and live(r):
   footnotes[measurekey(r)].add(r.get("Footnote",""))
 xlsx_rows(files["Measure exclusions.xlsx"],get_ex)
 xlsx_rows(files["Measure conditions.xlsx"],get_cond)
 xlsx_rows(files["Measure footnotes.xlsx"],get_foot)
 measures_by_code=defaultdict(list);raw_measures=[];mt=Counter()
 def take_duty(r):
  c=r.get("Goods code","")
  if c not in code_to_products or not live(r):return
  mt[r.get("Meas. type code","")]+=1
  obj=dict(r);obj["simple_adval_pct"]=""
  expression=r.get("Duty","").strip()
  m=re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)\s*%",expression)
  if m:obj["simple_adval_pct"]=m.group(1)
  key=measurekey(r)
  obj["condition_row_count"]=condcounts.get(key,0)
  obj["footnotes"]="|".join(sorted(footnotes.get(key,set())))
  obj["excluded_countries"]="|".join(sorted(exclusions.get(key,set())))
  measures_by_code[c].append(obj);raw_measures.append(obj)
 xlsx_rows(files["Duties Import 01-99.xlsx"],take_duty)
 print("Relevant active measures",len(raw_measures),"typecounts",mt.most_common(10),flush=True)
 raw_fields=["Goods code","Add code","Order No.","Start date","End date","RED_IND","Origin","Measure type","Legal base","Duty","Origin code","Meas. type code","simple_adval_pct","condition_row_count","footnotes","excluded_countries"]
 csvfile(DIR/"relevant_active_taric_measures_2026_11_01.csv",raw_fields,raw_measures)
 # Map dated goods-origin-measure rows, do not assume A.TR circulation, origin proof or GSP+
 fact=[];matrix=[];issues=[]
 basicmeta=['reference_date','cn8_2025','taric10_2026','origin','scheme','goods_measure_code',
            'measure_hier_pos','match_depth','measure_type_code','measure_type','start_date','end_date',
            'geo_code','geo_description','geo_matching','legal_base','duty_expression','simple_adval_pct',
            'additional_code','quota_order','condition_row_count','footnotes','excluded_countries',
            'claim_status','source_file','source_url']
 def origin_match(r,origin):
  g=r["Origin code"]
  if origin in exclusions.get(measurekey(r),set()):return None
  if g==origin:return "EXPLICIT_COUNTRY"
  if g=="1011" or r.get("Origin","")=="ERGA OMNES":return "ERGA_OMNES"
  if origin in members.get(g,set()):return "OFFICIAL_COUNTRY_GROUP"
  return None
 for cn8 in products:
  leafs=leaves.get(cn8,[])
  for leaf in leafs:
   for origin in ORIGINS:
    eligible=[]
    for parent in codetoparent.get(leaf,[]):
     for r in measures_by_code.get(parent,[]):
      kind=origin_match(r,origin)
      if kind is None:continue
      typ=r["Meas. type code"];kindstr=r.get("Measure type","")
      if typ=="103" or kindstr=="Third country duty":scheme="MFN"
      elif typ=="142" or kindstr=="Tariff preference":scheme="PREFERENCE_MEASURE"
      elif "quota" in kindstr.lower():scheme="QUOTA_OR_CONDITIONAL"
      elif "customs union" in kindstr.lower():scheme="CUSTOMS_UNION"
      else:scheme="OTHER_TARIC_MEASURE"
      claim="REQUIRES_PROOF_OF_ORIGIN_AND_LEGAL_ELIGIBILITY" if scheme=="PREFERENCE_MEASURE" else "CONDITIONAL_MAY_REQUIRE_ADDITIONAL_CHECKS"
      info=nodes.get(parent,{});hier=info.get("hier",0)
      el={"reference_date":str(DATE),"cn8_2025":cn8,"taric10_2026":leaf,"origin":origin,
          "scheme":scheme,"goods_measure_code":parent,"measure_hier_pos":hier,
          "match_depth":hier,"measure_type_code":typ,"measure_type":kindstr,
          "start_date":r["Start date"],"end_date":r["End date"],
          "geo_code":r["Origin code"],"geo_description":r["Origin"],
          "geo_matching":kind,"legal_base":r["Legal base"],"duty_expression":r["Duty"],
          "simple_adval_pct":r["simple_adval_pct"],"additional_code":r["Add code"],
          "quota_order":r["Order No."],"condition_row_count":r["condition_row_count"],
          "footnotes":r["footnotes"],"excluded_countries":r["excluded_countries"],
          "claim_status":claim,
          "source_file":"Duties Import 01-99.xlsx","source_url":f"{BASE}/{NODES['Duties Import 01-99.xlsx']}/content"}
      eligible.append(el)
    fact.extend(eligible)
    mfn=[e for e in eligible if e["scheme"]=="MFN" and e["simple_adval_pct"] and not e["additional_code"] and not e["quota_order"] and int(e["condition_row_count"])==0]
    pref=[e for e in eligible if e["scheme"]=="PREFERENCE_MEASURE" and e["simple_adval_pct"] and not e["additional_code"] and not e["quota_order"] and int(e["condition_row_count"])==0]
    mf_rates=set(e["simple_adval_pct"] for e in mfn);pfrates=set(e["simple_adval_pct"] for e in pref)
    # Only single-valued if no competing non-ad-valorem MFN/pref in SAME code-origin.
    mfn_all=[e for e in eligible if e["scheme"]=="MFN"]
    pref_all=[e for e in eligible if e["scheme"]=="PREFERENCE_MEASURE"]
    def status(allmeasures,rates,kind):
     if not allmeasures:return "NO_ACTIVE_MEASURE_FOUND"
     if len(rates)!=1:return "MULTIPLE_OR_COMPLEX_DUTIES" if rates or len(allmeasures)>1 else "NON_ADVALOREM_OR_CONDITIONAL"
     if any(not e["simple_adval_pct"] or e["additional_code"] or e["quota_order"] or int(e["condition_row_count"])>0 for e in allmeasures):
      return "COMPLEX_CONDITIONAL_MEASURE_PRESENT"
     return "SINGLE_SIMPLE_ADVALOREM_CANDIDATE"
    status_mfn=status(mfn_all,mf_rates,"MFN")
    status_pref=status(pref_all,pfrates,"PREF")
    matrix.append({"reference_date":str(DATE),"cn8_2025":cn8,"taric10_2026":leaf,"origin":origin,
     "mfn_duty_pct":next(iter(mf_rates)) if status_mfn=="SINGLE_SIMPLE_ADVALOREM_CANDIDATE" else "",
     "mfn_status":status_mfn,"preference_candidate_pct":next(iter(pfrates)) if status_pref=="SINGLE_SIMPLE_ADVALOREM_CANDIDATE" else "",
     "preference_status":status_pref,
     "mfn_measure_count":len(mfn_all),"preference_measure_count":len(pref_all),"all_measure_count":len(eligible),
     "origin_pref_eligibility":"NOT_VERIFIED_ROO_ACTUAL_CLAIM",
     "benchmark_note":"2026-11-01 TARIC snapshot only; NOT legal forecast of 2027 or post-2029 duty",
     "source_url":f"{BASE}/{NODES['Duties Import 01-99.xlsx']}/content"})
  if not leafs:issues.append({"cn8_2025":cn8,"reason":"NO_ACTIVE_2026_DECLARABLE_TARIC10_FOUND","implication":"DO_NOT_IMPUTE_RATE"})
 csvfile(DIR/"dated_taric10_origin_measure_evidence.csv",basicmeta,fact)
 fields=["reference_date","cn8_2025","taric10_2026","origin","mfn_duty_pct","mfn_status",
         "preference_candidate_pct","preference_status","mfn_measure_count","preference_measure_count",
         "all_measure_count","origin_pref_eligibility","benchmark_note","source_url"]
 csvfile(DIR/"dated_taric10_origin_rate_candidates.csv",fields,matrix)
 csvfile(DIR/"unmatched_2025_cn8_to_2026_taric.csv",["cn8_2025","reason","implication"],issues)
 # CN8-level comparability: refuse averaging divergent TARIC10 leaves.
 group=defaultdict(list)
 for row in matrix:group[(row["cn8_2025"],row["origin"])].append(row)
 summaryRows=[]
 for cn8 in products:
  for origin in ORIGINS:
   rows=group.get((cn8,origin),[])
   mf={r["mfn_duty_pct"] for r in rows if r["mfn_status"]=="SINGLE_SIMPLE_ADVALOREM_CANDIDATE"}
   pre={r["preference_candidate_pct"] for r in rows if r["preference_status"]=="SINGLE_SIMPLE_ADVALOREM_CANDIDATE"}
   mfok=bool(rows) and len(mf)==1 and all(r["mfn_status"]=="SINGLE_SIMPLE_ADVALOREM_CANDIDATE" for r in rows)
   preok=bool(rows) and len(pre)==1 and all(r["preference_status"]=="SINGLE_SIMPLE_ADVALOREM_CANDIDATE" for r in rows)
   summaryRows.append({"reference_date":str(DATE),"cn8_2025":cn8,"origin":origin,
      "taric10_leaf_count":len(rows),"mfn_pct":next(iter(mf)) if mfok else "",
      "mfn_status":"ALL_LEAVES_SAME_SIMPLE_MFN" if mfok else "NOT_SINGLE_RATE_VERIFIED",
      "preferential_candidate_pct":next(iter(pre)) if preok else "",
      "preference_status":"ALL_LEAVES_SAME_SIMPLE_PREFERENCE" if preok else "NOT_SINGLE_RATE_VERIFIED",
      "eligibility":"PREFERENCE_NOT_AUTOMATIC; VERIFY_ORIGIN_CERTIFICATE, GROUP_MEMBERSHIP, CONDITIONS, DATE",
      "future_gsp_plus_bangladesh_pct":"",
      "future_standard_gsp_bangladesh_pct":"",
      "future_scenario_status":"CONDITIONAL_NOT_YET_TARIFF_LINE_VERIFIED",
      "source_url":f"{BASE}/{NODES['Duties Import 01-99.xlsx']}/content"})
 csvfile(DIR/"top200_seven_origin_nov2026_tariff_scenarios_NO_IMPUTATION.csv",
 ["reference_date","cn8_2025","origin","taric10_leaf_count","mfn_pct","mfn_status","preferential_candidate_pct",
  "preference_status","eligibility","future_gsp_plus_bangladesh_pct","future_standard_gsp_bangladesh_pct",
  "future_scenario_status","source_url"],summaryRows)
 summary={"generated_utc":stamp(),"source":"Official European Commission DG TAXUD CIRCABC TARIC snapshot","as_of":str(DATE),
 "products_2025_cn8":len(products),"source_files":len(files),"unmatched_cn8_2026":len(issues),
 "products_with_one_or_more_active_taric_leaves":len(leaves),
 "taric10_leaf_count":sum(len(x) for x in leaves.values()),
 "active_measures_relevant":len(raw_measures),"applicable_origin_measure_records":len(fact),
 "taric10_origin_rows":len(matrix),"cn8_origin_rows":len(summaryRows),
 "cn8_origin_mfn_single_simple":sum(bool(r["mfn_pct"]) for r in summaryRows),
 "cn8_origin_pref_single_simple":sum(bool(r["preferential_candidate_pct"]) for r in summaryRows),
 "measure_type_counts":dict(mt),"source_receipts":receipts,
 "caveats":["Products selected from 2025 CN8; 2026 TARIC10 leaf validity must be checked.",
 "Monthly source reflects 2026-11-01, not live customs tariff on 2026-11-21.",
 "Preference availability is distinct from claim, utilization, origin proof, and importer eligibility.",
 "Possible duties inherited from ancestor codes matched using nomenclature hierarchy, not string trimming.",
 "Divergent leaf or conditional duty expressions never averaged or assigned a guessed ad valorem rate.",
 "2027 post-LDC GSP and GSP+ tariff lines must be matched after 2027 entry into application and legal scenario eligibility verified.",
 "Additional antidumping, safeguards, quotas, conditions and exclusions must be studied separately."]}
 (DIR/"SOURCE_AND_SCOPE_AUDIT.json").write_text(json.dumps(summary,indent=2))
 print("RESULT",json.dumps({k:v for k,v in summary.items() if k not in ("source_receipts","caveats")},indent=2),flush=True)
if __name__=="__main__":main()
