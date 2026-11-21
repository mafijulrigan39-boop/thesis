#!/usr/bin/env python3
"""Independent Task D: authenticate 14 raw Eurostat response hashes, recalculate each
EUR/kg and relative unit value, verify missingness and excluded zero/missing weights."""
import pathlib,csv,gzip,json,hashlib,io
from decimal import Decimal
from collections import Counter
from datetime import datetime,timezone
BASE=pathlib.Path('task_d_quantities/full')
def read(path):
 with open(path,newline='',encoding='utf-8-sig') as f:return list(csv.DictReader(f))
def main():
 receipts=read(BASE/'official_quantity_receipts.csv')
 panel=read(BASE/'seven_origin_quantity_unit_value_2012_2025.csv')
 exc=read(BASE/'unit_value_exclusions.csv')
 rel=read(BASE/'relative_unit_values_2025.csv')
 coverage=read(BASE/'coverage_by_year.csv')
 supp=read(BASE/'supplementary_quantities_UNVERIFIED_UNITS.csv')
 errors=[];original={};sourcehash=0
 for rec in receipts:
  p=pathlib.Path(rec['source_raw_path'])
  if not p.exists():errors.append('Raw file missing '+str(p));continue
  data=gzip.decompress(p.read_bytes())
  if hashlib.sha256(data).hexdigest()!=rec['sha256']:errors.append('SHA mismatch '+str(p))
  else:sourcehash+=1
  rows=list(csv.DictReader(io.StringIO(data.decode('utf-8-sig'))))
  if len(rows)!=int(rec['records']):errors.append('Receipt row count mismatch '+str(p))
  for row in rows:
   if row['reporter']!='EU27_2020' or row['flow']!='1' or row['freq']!='A' or row['indicators'] not in ('QUANTITY_IN_100KG','SUPPLEMENTARY_QUANTITY'):
    errors.append('Invalid metadata '+str(p));break
   k=(int(row['TIME_PERIOD']),row['product'],row['partner'],row['indicators'])
   if k in original:errors.append('Duplicate quantity record '+str(k))
   original[k]=Decimal(row['OBS_VALUE'])
 if len(panel)!=19600:errors.append('Panel must contain 19,600 rows')
 if len(receipts)!=14 or sourcehash!=14:errors.append('Quantity archives not all authenticated')
 stat=Counter();bad=0;seen=set();vindex={}
 for row in panel:
  y=int(row['year']);p=row['cn8'];o=row['origin'];key=(y,p,o)
  if key in seen:errors.append('Duplicate origin-year-product '+str(key))
  seen.add(key);vindex[key]=row
  m=original.get((*key,'QUANTITY_IN_100KG'))
  su=original.get((*key,'SUPPLEMENTARY_QUANTITY'))
  if (not row['mass_100kg']) != (m is None):bad+=1
  elif m is not None and Decimal(row['mass_100kg'])!=m:bad+=1
  if (not row['supplementary_qty_raw']) != (su is None):bad+=1
  elif su is not None and Decimal(row['supplementary_qty_raw'])!=su:bad+=1
  if m is not None:
   if not row['net_mass_kg'] or Decimal(row['net_mass_kg'])!=m*100:bad+=1
  elif row['net_mass_kg']:bad+=1
  val=Decimal(row['value_eur']) if row['value_eur'] else None
  good=val is not None and m is not None and m>0
  if good:
   if row['status']!='VALID_EUR_PER_KG' or not row['eur_per_kg'] or abs(Decimal(row['eur_per_kg'])-val/(m*100))>Decimal('1e-20'):bad+=1
  elif row['eur_per_kg'] or row['status']=='VALID_EUR_PER_KG':bad+=1
  if row['supplementary_eur_per_unit'] or row['supplementary_unit_code']!='UNVERIFIED':bad+=1
  if y<2025 and row['class_concordance']!='YEAR_SPECIFIC_CN8_NOT_HARMONIZED':bad+=1
  if y==2025 and row['class_concordance']!='2025_NATIVE':bad+=1
  stat[row['status']]+=1
 if bad:errors.append('Cell arithmetic/status inconsistencies '+str(bad))
 if len(exc)!=19600-stat['VALID_EUR_PER_KG']:errors.append('Exclusion register size mismatch')
 if len(rel)!=1200:errors.append('2025 comparison pairs not 1,200')
 validrel=0
 for row in rel:
  p=row['cn8'];o=row['comparison_origin'];a=vindex.get((2025,p,'BD'));b=vindex.get((2025,p,o))
  if a is None or b is None:errors.append('Relative comparison missing origin '+p);continue
  if a['eur_per_kg'] and b['eur_per_kg'] and Decimal(b['eur_per_kg'])>0:
   validrel+=1
   x=Decimal(a['eur_per_kg'])/Decimal(b['eur_per_kg'])
   if row['status']!='COMPARABLE_SAME_CN8_SAME_YEAR_KG' or abs(Decimal(row['bd_to_competitor_unit_value_ratio'])-x)>Decimal('1e-20'):
    errors.append('Relative ratio mismatch '+p+o)
  elif row['status']!='EXCLUDED_MISSING_OR_ZERO_UNIT_VALUE' or row['bd_to_competitor_unit_value_ratio']:
   errors.append('Ineligible ratio '+p+o)
 validcoverage=sum(int(r['valid_eur_kg']) for r in coverage)
 if validcoverage!=stat['VALID_EUR_PER_KG']:errors.append('Coverage summary inconsistent')
 if sum(int(r['supp_quantity_cells']) for r in coverage)!=len(supp):errors.append('Supplementary count mismatch')
 report={'qa_utc':datetime.now(timezone.utc).isoformat(),'passed':not errors,'issues':errors[:100],
  'raw_files_authenticated':sourcehash,'raw_quantity_records':len(original),
  'seven_origin_rows':len(panel),'valid_eur_per_kg':stat['VALID_EUR_PER_KG'],
  'excluded_rows':len(exc),'exclusion_breakdown':dict(stat),
  'supp_raw_rows':len(supp),'2025_relative_pairs':len(rel),'2025_valid_relative_pairs':validrel,
  'historical_restriction':'2012-2024 code meanings require official CN8 concordance; no raw-code longitudinal growth conclusions',
  'supplementary_restriction':'Supplementary quantity unit mapping unverified, so no EUR per supplementary unit values are certified'}
 (BASE/'INDEPENDENT_QA.json').write_text(json.dumps(report,indent=2))
 print(json.dumps(report,indent=2),flush=True)
 if errors:raise RuntimeError('Task D independent QA failed')
if __name__=='__main__':main()
