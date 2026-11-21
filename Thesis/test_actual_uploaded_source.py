#!/usr/bin/env python3
"""Regression tests on the actual user-uploaded CSV and its derived outputs."""
from pathlib import Path
import csv,hashlib,sys
ROOT=Path(__file__).resolve().parent
INP=Path(sys.argv[1]) if len(sys.argv)>1 else ROOT/'eu_imports_bangladesh_cn8_2012_2025.csv'
assert INP.exists(),f'File missing: {INP}'
with INP.open(encoding='utf-8-sig',newline='') as f: rows=list(csv.DictReader(f))
assert len(rows)==27780,len(rows)
assert len(set((r['PRODUCT'],r['TIME_PERIOD']) for r in rows))==27780
assert all(len(r['PRODUCT'])==8 and r['PRODUCT'].isdigit() for r in rows)
assert len(set(r['PRODUCT'] for r in rows))==4953
assert sum(int(r['OBS_VALUE'])==0 for r in rows)==155
assert sum(r['PRODUCT'].startswith('0') for r in rows)==1337
s25=sum(int(r['OBS_VALUE']) for r in rows if r['TIME_PERIOD']=='2025')
assert s25==21238163196,s25
s12=sum(int(r['OBS_VALUE']) for r in rows if r['TIME_PERIOD']=='2012')
assert s12==8186942161,s12
vtop=max((int(r['OBS_VALUE']),r['PRODUCT']) for r in rows if r['TIME_PERIOD']=='2025')
assert vtop==(3499230143,'61091000'),vtop
print('PASS: 27,780 rows, uniqueness, 8-digit strings, 4,953 codes, 155 zeros, 1,337 leading-zero rows, 2012/2025 sums, top code.')
print('SHA256',hashlib.sha256(INP.read_bytes()).hexdigest())
