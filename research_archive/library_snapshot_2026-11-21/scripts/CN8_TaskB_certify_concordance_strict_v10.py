#!/usr/bin/env python3
"""Strict official 2012–2025 CN8 concordance certification engine.

The *real* research output is never produced unless every annual full official
catalogue and all 13 complete, official adjacent-year change tables are supplied,
accompanied by full-file SHA256 and source origin metadata. No derived HS6-only
or identical-number-only crosswalk is silently accepted.

See README for normalized input requirements.
"""
import argparse,csv,re,hashlib,json,sys
from collections import defaultdict
from pathlib import Path
from datetime import datetime,timezone

FIRST,LAST=2012,2025
CODE=re.compile('^[0-9]{8}$')
RELATIONS={'change','split','merge','complex','unchanged_explicit','1_to_1'}

def read_csv(p,fields):
    with open(p,encoding='utf-8-sig',newline='') as f:
        r=csv.DictReader(f)
        if not set(fields).issubset(r.fieldnames or []):raise RuntimeError(f'{p}: expected columns {fields}, got {r.fieldnames}')
        return list(r)

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def save_csv(path,fields,rows):
    with open(path,'w',newline='',encoding='utf-8-sig') as f:
        w=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore');w.writeheader();w.writerows(rows)

def clean_desc(s):return ' '.join(s.strip().lower().split())

class Disjoint:
    def __init__(self):self.parent={};self.ranks={}
    def add(self,x):
        if x not in self.parent:self.parent[x]=x;self.ranks[x]=0
    def root(self,x):
        p=self.parent[x]
        if p!=x:self.parent[x]=self.root(p)
        return self.parent[x]
    def union(self,a,b):
        self.add(a);self.add(b)
        ra,rb=self.root(a),self.root(b)
        if ra==rb:return
        if self.ranks[ra]<self.ranks[rb]:ra,rb=rb,ra
        self.parent[rb]=ra
        if self.ranks[ra]==self.ranks[rb]:self.ranks[ra]+=1

def run(trade,inputs,out,min_catalogue_size=7000,synthetic=False):
    inputs=Path(inputs);out=Path(out);out.mkdir(exist_ok=True,parents=True)
    required=[]
    for year in range(FIRST,LAST+1):required.append(('catalogue',year,year,f'CN_{year}_catalog.csv'))
    for year in range(FIRST,LAST):required.append(('changes',year,year+1,f'CN_{year}_to_{year+1}_changes.csv'))
    missing=[{'file':n,'requirement':k} for k,_,_,n in required if not (inputs/n).exists()]
    completeness=dict(required_files=len(required),files_available=len(required)-len(missing),missing=missing,
       mode='SYNTHETIC_TEST_ONLY' if synthetic else 'REAL_OFFICIAL_CERTIFICATION',
       status='BLOCKED_SOURCE_FILES_MISSING' if missing else 'CHECKING',timestamp=datetime.now(timezone.utc).isoformat())
    (out/'source_completeness.json').write_text(json.dumps(completeness,indent=2))
    if missing:raise RuntimeError(f'Missing {len(missing)} of {len(required)} required source files; no certified crosswalk produced.')
    if not synthetic:
        man=read_csv(inputs/'source_manifest.csv',['filename','sha256','source_url','independently_verified','source_scope'])
        man={m['filename']:m for m in man}
        for kind,start,end,name in required:
            if name not in man:raise RuntimeError(f'{name}: absent from source_manifest.csv')
            m=man[name]
            if m['independently_verified'].upper()!='YES' or not m['source_url'].startswith('https://'):
                raise RuntimeError(f'{name}: official provenance must be checked and documented')
            if m['sha256'].lower()!=sha(inputs/name):raise RuntimeError(f'{name}: SHA256 does not match provenance')
            if kind=='changes' and m['source_scope']!='FULL_OFFICIAL_YEAR_TO_YEAR_CHANGES':
                raise RuntimeError(f'{name}: incomplete changes table may not be used for unchanged-code inference')
            if kind=='catalogue' and m['source_scope']!='FULL_OFFICIAL_ANNUAL_CN8':
                raise RuntimeError(f'{name}: catalogue must be full, not a Bangladesh-only observed-code list')
    cats={}; uf=Disjoint()
    for kind,y,e,n in required:
        if kind!='catalogue':continue
        rows=read_csv(inputs/n,['code','description','source_url']);dic={}
        for r in rows:
            code=r['code'].strip();desc=r['description'].strip()
            if not CODE.fullmatch(code) or not desc:raise RuntimeError(f'{n}: invalid code or missing description {r}')
            if code in dic:raise RuntimeError(f'{n}: duplicate code {code}')
            dic[code]=desc;uf.add((y,code))
        if len(dic)<min_catalogue_size:raise RuntimeError(f'{n}: only {len(dic)} codes; likely incomplete official catalogue')
        cats[y]=dic
    links=[];unresolved=[]
    for y in range(FIRST,LAST):
        n=f'CN_{y}_to_{y+1}_changes.csv';a=read_csv(inputs/n,['from_code','to_code','relation','source_url']);olds=set()
        for r in a:
            s=r['from_code'].strip();t=r['to_code'].strip();relation=r['relation'].strip()
            if not CODE.fullmatch(s) or not CODE.fullmatch(t) or relation not in RELATIONS or not r['source_url'].strip():
                raise RuntimeError(f'{n}: invalid mapping row {r}')
            if s not in cats[y] or t not in cats[y+1]:raise RuntimeError(f'{n}: mapping references code outside annual official catalogues ({s},{t})')
            olds.add(s);uf.union((y,s),(y+1,t));links.append(dict(from_year=y,to_year=y+1,from_code=s,to_code=t,type=relation,evidence='OFFICIAL_EXPLICIT_CORRESPONDENCE'))
        for code,old_desc in cats[y].items():
            if code in olds:continue
            if code in cats[y+1] and clean_desc(cats[y+1][code])==clean_desc(old_desc):
                uf.union((y,code),(y+1,code))
                links.append(dict(from_year=y,to_year=y+1,from_code=code,to_code=code,type='unchanged_in_complete_change_table',
                                  evidence='OFFICIAL_FULL_ANNUAL_LISTS+COMPLETE_YEAR_CHANGE_TABLE+IDENTICAL_DESCRIPTIONS'))
            elif code in cats[y+1]:
                unresolved.append(dict(from_year=y,to_year=y+1,code=code,reason='SAME_CODE_DIFFERENT_DESCRIPTION_NOT_LINKED_BY_OFFICIAL_CHANGE_TABLE'))
    groups=defaultdict(list)
    for node in uf.parent:groups[uf.root(node)].append(node)
    # stable deterministic identifiers: lexicographically smallest (year, code) in each complete-family component
    group_of={}
    for g,nodes in groups.items():
        earliest=min(nodes)
        ident=f'CN8F_{earliest[0]}_{earliest[1]}'
        for node in nodes:group_of[node]=ident
    trade_rows=read_csv(trade,['PRODUCT','TIME_PERIOD','OBS_VALUE'])
    seen=set();observed={};invalid=[]
    for r in trade_rows:
        y=int(r['TIME_PERIOD']);c=r['PRODUCT'].strip();k=(y,c)
        if k in seen:raise RuntimeError(f'Duplicate trade key: {k}')
        seen.add(k)
        if y not in cats or c not in cats[y]:invalid.append(dict(year=y,code=c,value=r['OBS_VALUE'],error='NOT_IN_OFFICIAL_ANNUAL_CN_CATALOGUE'));continue
        v=int(r['OBS_VALUE']);observed[k]=v
    if invalid:
        save_csv(out/'unrecognized_source_codes.csv',['year','code','value','error'],invalid)
        raise RuntimeError(f'{len(invalid)} trade records not in official annual catalogues. No certified output created.')
    mapped=[]
    for (y,c),v in sorted(observed.items()):
        mapped.append(dict(year=y,cn8_code=c,official_description=cats[y][c],
            observed_value_eur=v,certified_family=group_of[(y,c)],
            full_classification_verified='YES' if not synthetic else 'SYNTHETIC_TEST_ONLY'))
    # Every valid CN8 member in a family-year must have a reported trade observation,
    # otherwise the family-year is not admissible for comparisons (missing is NOT zero).
    family_members=defaultdict(set)
    for (y,c),grp in group_of.items():family_members[(grp,y)].add(c)
    family_year=[];fy_by_id=defaultdict(dict)
    for (grp,y),members in sorted(family_members.items()):
        observed_members=set(c for c in members if (y,c) in observed)
        missing_set=members-observed_members
        complete=not missing_set
        v=sum(observed[(y,c)] for c in observed_members) if complete else None
        fy_by_id[grp][y]=v
        family_year.append(dict(family=grp,year=y,required_official_codes=len(members),observed_trade_codes=len(observed_members),
          unreported_code_count=len(missing_set),value_eur_if_complete=v if v is not None else '',
          family_year_completeness='COMPLETE' if complete else 'INCOMPLETE_MISSING_NOT_ZERO',
          missing_codes='|'.join(sorted(missing_set)[:25])))
    certified_growth=[]
    for grp,years in sorted(fy_by_id.items()):
        if set(years)!=set(range(FIRST,LAST+1)):continue
        if any(v is None for v in years.values()):continue
        start,end=years[FIRST],years[LAST]
        if start<=0:continue
        certified_growth.append(dict(family=grp,value_2012_eur=start,value_2025_eur=end,
          growth_2012_2025_pct=100*(end/start-1),cagr_2012_2025_pct=100*((end/start)**(1/13)-1),
          provenance='ALL_14_OFFICIAL_ANNUAL_CODE_LISTS_AND_ALL_13_OFFICIAL_ADJACENT_YEAR_CORRESPONDENCES'))
    save_csv(out/'certified_observed_cn8_to_family_map.csv',list(mapped[0]),mapped)
    save_csv(out/'certified_family_year_status.csv',list(family_year[0]),family_year)
    if certified_growth:save_csv(out/'certified_full_period_growth.csv',list(certified_growth[0]),certified_growth)
    else:save_csv(out/'certified_full_period_growth.csv',['family','value_2012_eur','value_2025_eur','growth_2012_2025_pct','cagr_2012_2025_pct','provenance'],[])
    save_csv(out/'unresolved_same_code_description_edits.csv',['from_year','to_year','code','reason'],unresolved)
    save_csv(out/'verified_family_crosswalk_edges.csv',['from_year','to_year','from_code','to_code','type','evidence'],links)
    summary=dict(status='SYNTHETIC_TEST_ONLY' if synthetic else 'OFFICIAL_FILES_AND_LINEAGE_CHECKS_PASSED',
                 input_sha256=sha(trade),full_official_catalogues=len(cats),full_official_change_tables=LAST-FIRST,
                 certified_cn8_year_observations=len(mapped),families=len(groups),
                 unreported_family_years=sum(x['family_year_completeness']!='COMPLETE' for x in family_year),
                 full_period_growth_families=len(certified_growth),unresolved_same_code_description_years=len(unresolved))
    (out/'certified_manifest.json').write_text(json.dumps(summary,indent=2))
    return summary

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--trade',required=True);p.add_argument('--official-inputs',required=True)
    p.add_argument('--out',required=True);p.add_argument('--synthetic-test-only',action='store_true')
    p.add_argument('--min-catalogue-size',type=int,default=7000)
    a=p.parse_args()
    if a.min_catalogue_size<7000 and not a.synthetic_test_only:p.error('The 7000-code minimum can only be bypassed for synthetic tests')
    try:
        ans=run(a.trade,a.official_inputs,a.out,a.min_catalogue_size,a.synthetic_test_only)
        print(json.dumps(ans,indent=2))
    except Exception as e:
        print(f'BLOCKED — certified outputs NOT produced: {e}',file=sys.stderr);sys.exit(2)