#!/usr/bin/env python3
"""2025 all non-EU origin supplier ranking in same 200 selected CN8 product markets."""
import csv,gzip,pathlib,datetime,json,importlib.util
from collections import defaultdict
from decimal import Decimal
BASE=pathlib.Path('task_f_empirical/full')
SRC=pathlib.Path('task_c_competitor_data/full/all_partners_2012_2025.csv.gz')
spec=importlib.util.spec_from_file_location("taskcqa","task_c_competitor_data/qa_task_c_full.py")
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
ISO=m.ISO; EU=m.EU|{'GR'}
total=defaultdict(lambda:Decimal(0))
count=defaultdict(int)
alltotal=Decimal(0);BDvalue=Decimal(0)
with gzip.open(SRC,'rt',encoding='utf-8-sig',newline='') as f:
 for r in csv.DictReader(f):
  if r['year']!='2025':continue
  if r['origin']=='EXT_EU27_2020':alltotal+=Decimal(r['value_eur'])
  if r['origin']=='BD':BDvalue+=Decimal(r['value_eur'])
  if r['origin'] in ISO and r['origin'] not in EU:
   total[r['origin']]+=Decimal(r['value_eur']);count[r['origin']]+=1
ranked=sorted(total.items(),key=lambda r:(-r[1],r[0]))
rows=[{'origin_rank':i,'origin':o,'2025_total_value_eur_in_200_product_markets':str(v),
 'observed_product_lines':count[o],'share_of_sum_published_extraEU_product_denominators_percent':str(100*v/alltotal),
 'no_reported_row_is_not_assumed_zero':True} for i,(o,v) in enumerate(ranked,1)]
with open(BASE/'2025_all_nonEU_origin_rank_selected200.csv','w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
report={'source':'Official DS-045409 Task C 2025 all partner values','200_products':200,
 'origin_count':len(rows),'BD_rank_in_all_named_nonEU_origins':next(z['origin_rank'] for z in rows if z['origin']=='BD'),
 'BD_eur_2025':str(BDvalue),'sum_200_extraEU_denominators_eur':str(alltotal),
 'sum_all_named_countries_eur':str(sum(total.values())),'residual_eur':str(alltotal-sum(total.values())),
 'leading_20_origins':rows[:20],
 'limitation':'Ranks named-country origins only; country residual and trade scope remain flagged.'}
(BASE/'2025_ORIGIN_RANK_AUDIT.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
