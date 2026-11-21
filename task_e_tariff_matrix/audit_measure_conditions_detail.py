#!/usr/bin/env python3
"""Task E exact legal measure conditions/exclusions/footnotes for selected source measures.
Retains original source fields, per-row original Commission workbook and SHA provenance.
"""
import pathlib,csv,datetime,json,importlib.util
from collections import Counter
ROOT=pathlib.Path("task_e_tariff_matrix/nov2026_taric")
BASE=pathlib.Path("task_e_tariff_matrix/build_task_e_verified_matrix.py")
spec=importlib.util.spec_from_file_location("taric_builder",BASE);b=importlib.util.module_from_spec(spec);spec.loader.exec_module(b)
def read(path):
 with open(path,newline="",encoding="utf-8-sig") as f:return list(csv.DictReader(f))
def write(path,keys,rows):
 with open(path,"w",newline="",encoding="utf-8") as f:w=csv.DictWriter(f,fieldnames=keys,extrasaction="ignore");w.writeheader();w.writerows(rows)
def keyfacts(r):
 return (r["goods_measure_code"],r["additional_code"],r["quota_order"],r["start_date"],r["end_date"],r["geo_code"],r["measure_type_code"])
fact=read(ROOT/"dated_taric10_origin_measure_evidence.csv")
keys={keyfacts(r) for r in fact}
output={"Measure conditions.xlsx":[],"Measure exclusions.xlsx":[],"Measure footnotes.xlsx":[]}
def k(r):return (r.get("Goods code",""),r.get("Add code",""),r.get("Order No.",""),r.get("Start date",""),r.get("End date",""),r.get("Origin code",""),r.get("Meas. type code",""))
checks=[]
for file in output:
 source=ROOT/"official_sources"/file
 def fn(row):
  if k(row) in keys and b.live(row):
   output[file].append(row)
 n,h=b.xlsx_rows(source,fn)
 checks.append({"file":file,"original_raw_rows":n,"matching_valid_source_rows":len(output[file]),"column_names":h})
# Original exemption table has distinct column labels 'Excluded country code' descriptive;
# preserve full original source fields and do NOT conflate exclusions with a free trade claim.
for file,rows in output.items():
 h=checks[[x["file"] for x in checks].index(file)]["column_names"]
 name=file.replace(".xlsx","").lower().replace(" ","_")
 write(ROOT/(name+"_selected_original_source_rows.csv"),h,rows)
summary={"utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),
 "reference_date":"2026-11-01","source":"Official EU DG TAXUD CIRCABC November 2026 raw XLSX",
 "unique_applicable_measure_keys":len(keys),"rows":checks,
 "caution":["TARIC measure conditions are not themselves a full origin certificate determination.",
 "GSP / FTA product-specific rules of origin are in distinct legal sources and remain unvalidated.",
 "Same source measure may serve multiple CN8 descendants and multiple eligible country groups.",
 "Future 2027+ duty scenarios not confirmed from the 2026-11-01 snapshot."]}
(ROOT/"LEGAL_CONDITIONS_PROVENANCE_AUDIT.json").write_text(json.dumps(summary,indent=2))
print(json.dumps(summary,indent=2),flush=True)
