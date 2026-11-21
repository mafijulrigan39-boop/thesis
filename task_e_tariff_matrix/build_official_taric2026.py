#!/usr/bin/env python3
"""Task E: Official EU TAXUD TARIC extraction, goods/date/origin matrix.
Source: CIRCABC November 2026 monthly TARIC XLSX tables.
Deliberately does NOT claim current GSP rates are guaranteed 2027/2032 rates.
Produces auditable candidate measures and simple-rate cells; ambiguous rates blank.
"""
from __future__ import annotations
import urllib.request,base64,datetime,hashlib,pathlib,json,csv,io,re,zipfile,xml.etree.ElementTree as ET,collections
REF_DATE=datetime.date(2026,11,1)
ROOT=pathlib.Path('task_e_tariff_matrix/nov2026')
SOURCE_DIR=ROOT/'official_source_xlsx'
SOURCE_DIR.mkdir(parents=True,exist_ok=True)
SOURCE_BASE='https://circabc.europa.eu/service/api/node/workspace/SpacesStore'
ITEMS={
 'Duties Import 01-99.xlsx':'d0b85541-ed40-4f11-81c3-d245b15adc1d',
 'Geographical areas composition.xlsx':'e8a814f1-7ca2-4c0b-a34a-b8d82d0eeeeb',
 'Measure exclusions.xlsx':'215b5316-d9f4-46ca-a6d4-1eb1355eae4d',
 'Measure conditions.xlsx':'dcf72a54-9a49-4d57-b8fa-a641e889faf9',
 'Nomenclature EN.xlsx':'41fc5fcb-88b0-4153-9d30-0bc0b01b3fde',
 'Declarable codes.xlsx':'adb9dd82-8089-4c78-8ae7-bd36eced8de8',
 'Legal basis.xlsx':'6edb3f45-4c2e-4137-b567-e112fd4fa464',
 'Geographical areas description.xlsx':'acbd49e1-0b7a-47e3-8509-534db940f0bb',
 'Measure footnotes.xlsx':'ef9e8bb1-1553-4889-b638-d37855f0c74a'
}
CODES_FILE=pathlib.Path('task_c_competitor_data/full/selected_top200_2025.csv')
ORIGINS=['BD','CN','IN','VN','PK','KH','TR']
XNS='{http://schemas.openxmlformats.org/spreadsheetml/2006/main}'
HEAD={'Authorization':'Basic '+base64.b64encode(b'guest:').decode(),'User-Agent':'Mozilla/5.0 (University-of-Dhaka-MITB-TARIC-Research/1.0)'}
def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(x):return hashlib.sha256(x).hexdigest()
def date(s):
 if not s:return None
 try:return datetime.datetime.strptime(s,'%d-%m-%Y').date()
 except:return None
def active(start,end,reference=REF_DATE):
 a=date(start);b=date(end)
 return (not a or a<=reference) and (not b or reference<=b)
def outcsv(name,fields,rows):
 p=ROOT/name;p.parent.mkdir(parents=True,exist_ok=True)
 with p.open('w',newline='',encoding='utf-8') as f:
  writer=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore');writer.writeheader();writer.writerows(rows)
def load_source(name,node):
 path=SOURCE_DIR/name;url=f'{SOURCE_BASE}/{node}/content'
 if path.exists():blob=path.read_bytes();cached=True
 else:
  req=urllib.request.Request(url,headers=HEAD)
  with urllib.request.urlopen(req,timeout=180) as res:blob=res.read(100_000_000)
  assert 1000<len(blob)<100_000_000 and blob[:2]==b'PK'
  path.write_bytes(blob);cached=False
 return path,{'filename':name,'source_url':url,'downloaded_utc':utc(),'bytes':len(blob),
      'sha256':sha(blob),'source':'European Commission DG TAXUD CIRCABC TARIC public monthly extraction',
      'reference_date':'2026-11-01','used_cached_copy':cached}
def iterxlsx(path):
 """Read original XLSX XML via standard lib, preserving printed code strings."""
 with zipfile.ZipFile(path) as z:
  strings=[]
  if 'xl/sharedStrings.xml' in z.namelist():
   with z.open('xl/sharedStrings.xml') as ff:
    for _,el in ET.iterparse(ff,events=('end',)):
     if el.tag==XNS+'si':
      strings.append(''.join(e.text or '' for e in el.iter(XNS+'t')))
      el.clear()
  header=None
  with z.open('xl/worksheets/sheet1.xml') as ff:
   for _,el in ET.iterparse(ff,events=('end',)):
    if el.tag!=XNS+'row':continue
    values={}
    for c in el.iter(XNS+'c'):
     ref=c.attrib.get('r','')
     m=re.match(r'([A-Z]+)',ref)
     if not m:continue
     col=0
     for char in m.group(1):col=col*26+ord(char)-64
     v=c.find(XNS+'v');q=v.text if v is not None and v.text is not None else ''
     t=c.attrib.get('t')
     if t=='s' and q:q=strings[int(q)]
     elif t=='inlineStr':
      p=c.find(XNS+'is')
      q=''.join(e.text or '' for e in p.iter(XNS+'t')) if p is not None else ''
     values[col]=q
    if header is None:
     header={i:s.strip() for i,s in values.items()}
     el.clear();continue
    yield {header[i]:values.get(i,'').strip() for i in header}
    el.clear()
def ancestrynames(code):
 # 2/4/6/8/10-level TARIC inheritance, codes all 10-digit zero padded
 return {code[:n].ljust(10,'0') for n in (2,4,6,8,10)}
def key_measure(r):
 return tuple(r.get(k,'') for k in ('Goods code','Add code','Order No.','Start date','End date','Origin code','Meas. type code'))
def load_trade_selection():
 with CODES_FILE.open(newline='',encoding='utf-8') as ff:rows=list(csv.DictReader(ff))
 x=[r['cn8'] for r in rows]
 assert len(x)==200 and all(re.fullmatch(r'\d{8}',p) for p in x)
 return x
def main():
 codes=load_trade_selection()
 parent_codes=set()
 for p in codes:parent_codes.update(ancestrynames(p+'00'))
 selected_prefix=tuple(codes)
 source_log=[]
 files={}
 for name,node in ITEMS.items():
  f,receipt=load_source(name,node)
  source_log.append(receipt);files[name]=f
  print('SOURCE',name,receipt['bytes'],receipt['sha256'],flush=True)
 (ROOT/'source_file_receipts.json').write_text(json.dumps(source_log,indent=2))
 # Load related countries+membership time windows
 members=collections.defaultdict(set)
 membership_rows=[]
 for r in iterxlsx(files['Geographical areas composition.xlsx']):
  if r.get('Member country') in ORIGINS and active(r.get('Mbship start date'),r.get('Mbship end date')) and active(r.get('Start date'),r.get('End date')):
   members[r['Member country']].add(r.get('Country group',''))
   membership_rows.append({'group':r.get('Country group',''),'group_description':r.get('Country group descr.',''),
     'country':r['Member country'],'member_start':r.get('Mbship start date',''),'member_end':r.get('Mbship end date',''),
     'group_start':r.get('Start date',''),'group_end':r.get('End date','')})
 outcsv('2026_country_group_memberships.csv',['country','group','group_description','member_start','member_end','group_start','group_end'],membership_rows)
 # Additional code applicability and restrictions apply to EXACT goods code and measure identifiers
 exceptions=collections.defaultdict(set)
 for r in iterxlsx(files['Measure exclusions.xlsx']):
  g=r.get('Goods code','')
  if (g in parent_codes or g.startswith(selected_prefix)) and active(r.get('Start date'),r.get('End date')):
   exceptions[key_measure(r)].add(r.get('Excluded country',''))
 conditions=collections.defaultdict(list)
 for r in iterxlsx(files['Measure conditions.xlsx']):
  g=r.get('Goods code','')
  if (g in parent_codes or g.startswith(selected_prefix)) and active(r.get('Start date'),r.get('End date')):
   conditions[key_measure(r)].append(r)
 footnotes=collections.defaultdict(list)
 # Footnote column layout differs from condition/exclusion; make canonical field mapping.
 for r in iterxlsx(files['Measure footnotes.xlsx']):
  g=r.get('Goods code','')
  if (g in parent_codes or g.startswith(selected_prefix)) and active(r.get('Start date'),r.get('End date')):
   k=tuple(r.get(s,'') for s in ('Goods code','Add code','Order No.','Start date','End date','Origin code','Meas. type code'))
   footnotes[k].append(r.get('Footnote',''))
 # Leaf ten-digit code list
 leafmap=collections.defaultdict(list)
 for r in iterxlsx(files['Declarable codes.xlsx']):
  if r.get('IS_LEAF')!='1' or not active(r.get('Start date'),r.get('End date')) or not active(r.get('Decl. start date'),r.get('End date')):continue
  full=(r.get('Goods code') or '').split()[0]
  if len(full)==10 and full[:8] in codes:leafmap[full[:8]].append(full)
 for k in list(leafmap):leafmap[k]=sorted(set(leafmap[k]))
 nomen={}
 for r in iterxlsx(files['Nomenclature EN.xlsx']):
  code=(r.get('Goods code') or '').split()[0]
  if (code in parent_codes or code.startswith(selected_prefix)) and active(r.get('Start date'),r.get('End date')):
   nomen[code]=r
 # Tariff measures, restrict to product codes and their ancestors, active 1 Nov
 duties_by_code=collections.defaultdict(list)
 kept=[]
 measure_types=collections.Counter()
 for r in iterxlsx(files['Duties Import 01-99.xlsx']):
  g=r.get('Goods code','')
  if (g in parent_codes or g.startswith(selected_prefix)) and active(r.get('Start date'),r.get('End date')):
   r['_numlen']=len(g.rstrip('0'))
   duties_by_code[g].append(r);kept.append(r);measure_types[(r.get('Meas. type code'),r.get('Measure type'))]+=1
 outcsv('relevant_active_raw_taric_measures.csv',list(kept[0]) if kept else ['Goods code'],kept)
 # Legal references only cite exact published records; no guessing RoO.
 legal={}
 for r in iterxlsx(files['Legal basis.xlsx']):legal[r.get('Legal base','')]=r
 # For 2026 genuine country-origin matching, return all candidates and selection metadata.
 lines=[];summary=[];candidates=[];nonmatched=[];by_cn8=collections.defaultdict(list)
 for p in codes:
  leaves=leafmap.get(p,[])
  if not leaves:
   nonmatched.append({'cn8':p,'issue':'NO_DECLARABLE_2026_TARIC10_LEAF','detail':'Not present in source dated 2026-11-01'})
  for leaf in leaves:
   lines.append({'cn8_2025':p,'taric10_2026':leaf,'description':nomen.get(leaf,{}).get('Description',''),
     'declarable_leaf':'YES','tariff_source_refdate':'2026-11-01','taric10_exact_valid_2025':'NOT_INDEPENDENTLY_CHECKED'})
   anc=ancestrynames(leaf)
   possible=[]
   for g in anc:possible.extend(duties_by_code.get(g,[]))
   for country in ORIGINS:
    eligible_groups=members.get(country,set())|{country}
    matches=[]
    for r in possible:
     typecode=r.get('Meas. type code','')
     source_area=r.get('Origin code','')
     # for ERGA OMNES, group membership is explicit in CIRCABC, but include 1011 for every origin.
     if source_area not in eligible_groups and source_area!='1011':continue
     k=key_measure(r)
     if country in exceptions.get(k,set()):continue
     start=r.get('Start date','');end=r.get('End date','')
     duty=r.get('Duty','').strip()
     m=re.fullmatch(r'(\d+(?:\.\d+)?)\s*%',duty)
     add=r.get('Add code','')
     order=r.get('Order No.','')
     cond=conditions.get(k,[])
     foot=footnotes.get(k,[])
     legalrow=legal.get(r.get('Legal base',''),{})
     record={'cn8_2025':p,'taric10_2026':leaf,'country':country,
       'measure_source_goods_code':r.get('Goods code',''),'ancestor_inheritance':r.get('Goods code')!=leaf,
       'country_group_or_code':source_area,'measure_type_code':typecode,'measure_type':r.get('Measure type',''),
       'duty_expression':duty,'simple_ad_valorem_pct':m.group(1) if m else '',
       'start_date':start,'end_date':end,'legal_base':r.get('Legal base',''),
       'official_journal':legalrow.get('Off. Journal',''),'legal_publication_date':legalrow.get('Publ. date',''),
       'additional_code':add,'quota_order_number':order,
       'number_of_conditions':len(cond),'condition_certificates':'|'.join(sorted(set(c.get('Certificate','') for c in cond if c.get('Certificate','')))),
       'footnotes':'|'.join(sorted(set(foot))),'source_date':'2026-11-01',
       'source_file':'Duties Import 01-99.xlsx','source_sha256':next(x['sha256'] for x in source_log if x['filename']=='Duties Import 01-99.xlsx')}
     candidates.append(record)
     matches.append(record)
    # When code ancestry overlaps, nearest ancestor wins within measure type and country area.
    # Multiple preferences cannot be assumed interchangeable; all remain in candidates.
    mfn=[r for r in matches if r['measure_type_code']=='103']
    pref=[r for r in matches if r['measure_type_code']=='142']
    other=[r for r in matches if r['measure_type_code'] not in ('103','142')]
    def select(rows):
     if not rows:return {'status':'NO_MATCH','expression':'','simple_pct':'','legal_base':'','measure_goods_code':'','conditions':''}
     # Within same measure type, prefer deepest goods code; no automatic discarding multiple independent options.
     depth=max(len(r['measure_source_goods_code'].rstrip('0')) for r in rows)
     nearest=[r for r in rows if len(r['measure_source_goods_code'].rstrip('0'))==depth]
     uniq={(r['duty_expression'],r['country_group_or_code'],r['additional_code'],r['quota_order_number'],r['legal_base']) for r in nearest}
     simple=[r for r in nearest if r['simple_ad_valorem_pct'] and not r['additional_code'] and not r['quota_order_number'] and not r['number_of_conditions']]
     if len(nearest)==1 and len(simple)==1:
      r=simple[0];status='SINGLE_SIMPLE_UNCONDITIONAL_TARIFF_MEASURE'
      return {'status':status,'expression':r['duty_expression'],'simple_pct':r['simple_ad_valorem_pct'],
         'legal_base':r['legal_base'],'measure_goods_code':r['measure_source_goods_code'],'conditions':''}
     elif len(nearest)==1:
      r=nearest[0]
      return {'status':'ONE_MEASURE_COMPLEX_OR_CONDITIONAL','expression':r['duty_expression'],'simple_pct':'',
         'legal_base':r['legal_base'],'measure_goods_code':r['measure_source_goods_code'],
         'conditions':r['condition_certificates']}
     else:return {'status':'MULTIPLE_MEASURES_NOT_RESOLVED','expression':'|'.join(sorted({r['duty_expression'] for r in nearest})),
       'simple_pct':'','legal_base':'|'.join(sorted({r['legal_base'] for r in nearest})),
       'measure_goods_code':'|'.join(sorted({r['measure_source_goods_code'] for r in nearest})),
       'conditions':'|'.join(sorted({r['condition_certificates'] for r in nearest}))}
    a=select(mfn);b=select(pref)
    status=('PREF_POTENTIAL' if pref else 'MFN_POTENTIAL' if mfn else 'NO_TARIFF_MEASURE')
    chosen=b if pref else a
    summary.append({'cn8_2025':p,'taric10_2026':leaf,'origin_country':country,'date':'2026-11-01',
      'mfn_expression':a['expression'],'mfn_pct_strict':a['simple_pct'],'mfn_status':a['status'],
      'mfn_legal_base':a['legal_base'],'mfn_source_goods_code':a['measure_goods_code'],
      'preference_expression':b['expression'],'preference_pct_strict':b['simple_pct'],
      'preference_status':b['status'],'preference_legal_base':b['legal_base'],
      'preference_source_goods_code':b['measure_goods_code'],'preferred_candidate_kind':status,
      'candidate_expression':chosen['expression'],'candidate_pct_strict':chosen['simple_pct'],
      'other_measures_count':len(other),'conditional_or_other_measures_require_manual_review':bool(other),
      'rules_of_origin_status':'PRODUCT_SPECIFIC_RULES_NOT_YET_CERTIFIED',
      'actual_preference_claim_status':'NOT_OBSERVED_IN_TRADE_DATA',
      'actual_duty_payable_status':'NOT_CONFIRMED_WITHOUT_DECLARATION_DETAILS'})
   by_cn8[p].append(summary[-1])
 outcsv('taric10_leaf_mapping.csv',['cn8_2025','taric10_2026','description','declarable_leaf','tariff_source_refdate','taric10_exact_valid_2025'],lines)
 outcsv('unmatched_cn8.csv',['cn8','issue','detail'],nonmatched)
 if candidates:outcsv('all_tariff_measure_candidates_with_conditions.csv',list(candidates[0]),candidates)
 if summary:outcsv('actual_2026_taric10_origin_matrix.csv',list(summary[0]),summary)
 # CN8 may have several TARIC leaf subdivisions. Only unique simple and identical across
 # all leaves may be represented by a CN8-wide numeric rate.
 aggregate=[]
 for p in codes:
  leaves=leafmap.get(p,[])
  for country in ORIGINS:
   rows=[r for r in summary if r['cn8_2025']==p and r['origin_country']==country]
   def aggregated(field,status):
    rates=[r[field] for r in rows]
    statuses=[r[status] for r in rows]
    if not rows:return ('','NO_VALID_2026_TARIC_SUBDIVISION')
    if len(rows)!=len(leaves):return ('','MISSING_TARIC10_BRANCH')
    if all(x=='SINGLE_SIMPLE_UNCONDITIONAL_TARIFF_MEASURE' for x in statuses) and len(set(rates))==1:
     return (rates[0],'ALL_2026_TARIC10_LEAVES_SAME_SIMPLE_RATE')
    return ('','TARIC10_LINES_DIFFER_OR_MEASURES_CONDITIONAL')
   mf,mfs=aggregated('mfn_pct_strict','mfn_status')
   pref,prefs=aggregated('preference_pct_strict','preference_status')
   aggregate.append({'cn8_2025':p,'origin_country':country,'taric10_leaves':len(leaves),
     'mfn_advalorem_pct_verified':mf,'mfn_status':mfs,
     'preference_advalorem_pct_verified':pref,'preference_status':prefs,
     'current_2026_policy_treatment':'CONDITIONAL_IF_ORIGIN_QUALIFIES' if pref else 'SEE_MFN_AND_TARIC10',
     'reference_date':'2026-11-01','future_2027_2032_rate':'',
     'future_tariff_status':'NOT_CERTIFIED_BY_2026_MONTHLY_TARIC',
     'effective_date_uncertainty':'2027+ scenarios require separate applicable law and future customs act'})
 outcsv('cn8_2026_origin_verified_simple_rate_screen.csv',list(aggregate[0]),aggregate)
 # GSP schema templates: identify eligible geographical groups by official descriptions only.
 schemes=[]
 for x in sorted(set((r['group'],r['group_description']) for r in membership_rows)):
  if any(q in x[1].lower() for q in ('gsp','least-developed','l.d.c','eba','special incentive','standard')):
   schemes.append({'group_code':x[0],'group_description':x[1],'beneficiary_members':'|'.join(sorted(set(r['country'] for r in membership_rows if r['group']==x[0]))),
     'scheme_eligibility_as_of':'2026-11-01','future_2027_bd_status':'NOT_AUTOMATIC'})
 outcsv('gsp_2026_country_group_scheme_inventory.csv',['group_code','group_description','beneficiary_members','scheme_eligibility_as_of','future_2027_bd_status'],schemes)
 detail={'created_utc':utc(),'official_source_reference_date':'2026-11-01','source_month':'2026-11',
   'source_files':len(source_log),'cn8_requested':len(codes),'cn8_with_2026_taric_leaf':len(leafmap),
   'taric10_leaf_lines':len(lines),'taric10_origin_rows':len(summary),'raw_relevant_active_duty_rows':len(kept),
   'candidate_origin_tariff_measures':len(candidates),'sample_origin_group_memberships':len(membership_rows),
   'types':[{ 'type_code':k[0], 'type':k[1], 'raw_rows':v} for k,v in measure_types.most_common(30)],
   'unique_simple_mfn_taric10_country_rows':sum(r['mfn_status']=='SINGLE_SIMPLE_UNCONDITIONAL_TARIFF_MEASURE' for r in summary),
   'unique_simple_preference_taric10_country_rows':sum(r['preference_status']=='SINGLE_SIMPLE_UNCONDITIONAL_TARIFF_MEASURE' for r in summary),
   'cn8_origin_simple_mfn':sum(bool(r['mfn_advalorem_pct_verified']) for r in aggregate),
   'cn8_origin_simple_pref':sum(bool(r['preference_advalorem_pct_verified']) for r in aggregate),
   'limitations':['Reference date 1 Nov 2026, not 21 Nov; daily updates not merged',
      'CN8 2025 trade codes mapped to November 2026 valid TARIC10 leaf where possible, 2025 validity not separately recertified',
      'TARIC codes may inherit parent measures; selected with hierarchy and exact measure group',
      'Country-of-origin eligibility requires proof of origin; actual preference utilisation not observed',
      'Future Standard GSP/GSP+ rates under 2026/1395 not certified as applied Bangladesh rates',
      'MFN and preference candidates do not include customs valuation, VAT, contingent charges, anti-dumping, quotas or proof-of-origin determination unless independently verified',
      'Complex duty expressions, multiple tariff measures, additional codes, quotas and conditions are not assigned a numeric advalorem rate',
      'Exact rules of origin for 200 products are not yet audited'] }
 (ROOT/'TASK_E_SOURCE_AND_COVERAGE.json').write_text(json.dumps(detail,indent=2))
 print(json.dumps(detail,indent=2),flush=True)
if __name__=='__main__':main()
