#!/usr/bin/env python3
"""Probe official CIRCABC public TARIC monthly classification and duties source.
Read-only guest API, capture metadata only; no guessed rates."""
import urllib.request,base64,xml.etree.ElementTree as ET,json,pathlib,re,datetime
OUT=pathlib.Path("task_e_tariff_matrix/probe");OUT.mkdir(parents=True,exist_ok=True)
base="https://circabc.europa.eu/service/api/node/workspace/SpacesStore"
rootid="64db9d0f-e7c9-4084-afe9-f47e70e53c10"
headers={'Authorization':'Basic '+base64.b64encode(b'guest:').decode(),'User-Agent':'Mozilla/5.0 (Academic Thesis TARIC Source Audit)'}
def fetch(folder):
 url=f"{base}/{folder}/children"
 with urllib.request.urlopen(urllib.request.Request(url,headers=headers),timeout=45) as res:
  b=res.read(2000000)
 print('GET',url,'bytes',len(b),flush=True)
 (OUT/f'folder_{folder}.xml').write_bytes(b)
 root=ET.fromstring(b)
 arr=[]
 for a in root.findall('{http://www.w3.org/2005/Atom}entry'):
  title=a.findtext('{http://www.w3.org/2005/Atom}title') or ''
  node=''
  for link in a.findall('{http://www.w3.org/2005/Atom}link'):
   href=link.attrib.get('href','')
   if link.attrib.get('rel')=='self':
    m=re.search(r'SpacesStore/i/([a-f0-9-]{36})',href)
    if m:node=m.group(1)
  content=a.find('{http://www.w3.org/2005/Atom}content')
  arr.append({'title':title,'id':node,'mime':content.attrib.get('type') if content is not None else ''})
 return arr
log={'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'folder_root':rootid}
try:
 years=fetch(rootid);log['years']=years
 match=next((x for x in years if x['title'].strip()=='2026'),None)
 if match:
  months=fetch(match['id']);log['months']=months
  latest=next((x for x in months if x['title'].startswith('11 ')),None) or next((x for x in months if x['title'].startswith('10 ')),None)
  if latest:
   files=fetch(latest['id']);log['selected_month']=latest;log['files']=files
except Exception as exc:
 log['error']=type(exc).__name__+': '+str(exc)
(OUT/'official_circabc_navigation.json').write_text(json.dumps(log,indent=2))
print(json.dumps({k:([{'title':x['title'],'id':x['id']} for x in v] if isinstance(v,list) else v) for k,v in log.items()},indent=2),flush=True)
