#!/usr/bin/env python3
"""Download official EC DG TAXUD November 2026 TARIC XLSX sources, archive receipts,
and inspect raw XLSX structure using only Python ZIP/XML standard library."""
import pathlib,urllib.request,base64,hashlib,zipfile,xml.etree.ElementTree as ET,json,datetime,os,io,time
BASE="https://circabc.europa.eu/service/api/node/workspace/SpacesStore"
ITEMS={
 "Duties Import 01-99.xlsx":"d0b85541-ed40-4f11-81c3-d245b15adc1d",
 "Geographical areas composition.xlsx":"e8a814f1-7ca2-4c0b-a34a-b8d82d0eeeeb",
 "Measure exclusions.xlsx":"215b5316-d9f4-46ca-a6d4-1eb1355eae4d",
 "Measure conditions.xlsx":"dcf72a54-9a49-4d57-b8fa-a641e889faf9",
 "Nomenclature EN.xlsx":"41fc5fcb-88b0-4153-9d30-0bc0b01b3fde",
 "Declarable codes.xlsx":"adb9dd82-8089-4c78-8ae7-bd36eced8de8",
 "Legal basis.xlsx":"6edb3f45-4c2e-4137-b567-e112fd4fa464",
 "Geographical areas description.xlsx":"acbd49e1-0b7a-47e3-8509-534db940f0bb",
 "Measure footnotes.xlsx":"ef9e8bb1-1553-4889-b638-d37855f0c74a"
}
OUT=pathlib.Path("task_e_tariff_matrix/official_2026_11");OUT.mkdir(parents=True,exist_ok=True)
NS="{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
H={'Authorization':'Basic '+base64.b64encode(b'guest:').decode(),'User-Agent':'Mozilla/5.0 MITB Research TARIC Audit/1.0'}
def xlsx_schema(p):
 with zipfile.ZipFile(p) as z:
  files=[x for x in z.namelist() if x.startswith('xl/worksheets/sheet') and x.endswith('.xml')]
  strings=[]
  if 'xl/sharedStrings.xml' in z.namelist():
   with z.open('xl/sharedStrings.xml') as f:
    for ev,el in ET.iterparse(f,events=('end',)):
     if el.tag==NS+'si':
      strings.append(''.join(node.text or '' for node in el.iter(NS+'t')))
      el.clear()
  ans=[]
  for file in files:
   rows=[]
   with z.open(file) as f:
    for ev,el in ET.iterparse(f,events=('end',)):
     if el.tag==NS+'row':
      record=[]
      for cell in el.iter(NS+'c'):
       v=cell.find(NS+'v')
       s=cell.attrib.get('t');inline=cell.find(NS+'is')
       raw=v.text if v is not None else ''
       if s=='s' and raw and raw.isdigit() and int(raw)<len(strings):raw=strings[int(raw)]
       if s=='inlineStr' and inline is not None:raw=''.join(x.text or '' for x in inline.iter(NS+'t'))
       record.append({'ref':cell.attrib.get('r'),'value':raw})
      rows.append(record)
      el.clear()
      if len(rows)>=6:break
   ans.append({'sheet_filename':file,'sample_rows':rows})
  return {'xl_shared_strings_count':len(strings),'sheets':ans,'xlsx_members':len(z.namelist())}
results=[]
for name,node in ITEMS.items():
 url=f'{BASE}/{node}/content'
 entry={'file':name,'source_url':url,'downloaded_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 try:
  req=urllib.request.Request(url,headers=H)
  with urllib.request.urlopen(req,timeout=150) as response:
   raw=response.read(100_000_000)
   entry['http_status']=response.status
   entry['content_type']=response.headers.get('Content-Type')
  if len(raw)>=100_000_000:raise ValueError('Data exceeds 100MB safety cap')
  entry['bytes']=len(raw);entry['sha256']=hashlib.sha256(raw).hexdigest()
  path=OUT/name;path.write_bytes(raw)
  entry['xlsx_schema']=xlsx_schema(path)
  entry['locally_archived']=True
  print('OK',name,len(raw),'bytes',flush=True)
 except Exception as ex:
  entry['error']=type(ex).__name__+': '+str(ex)[:400]
  print('FAIL',name,entry['error'],flush=True)
 results.append(entry)
# Don't commit large source files yet; keep receipts, source file location in runner only
(OUT/'SOURCE_PROBE_RECEIPTS.json').write_text(json.dumps(results,indent=2))
print(json.dumps([{'file':r['file'],'bytes':r.get('bytes'),'sha':r.get('sha256'),
 'sample':r.get('xlsx_schema',{}).get('sheets',[])[:1], 'error':r.get('error')} for r in results],indent=2),flush=True)
