#!/usr/bin/env python3
"""Download/validate EU27_2020 imports from Bangladesh, CN8, 2012–2025.

Official Eurostat Comext dataset: DS-045409 (NOT DS-059322).

Requirements: Python 3.10+, requests
    pip install requests
    python eurostat_comext_bd_cn8_verified_v4.py --out ./bd_cn8_run

Only writes `eu_imports_bangladesh_cn8_2012_2025_VALIDATED.csv` when *every*
year passes: API success, unique CN8-year observations, full-period coverage,
valid numeric import values, and successful reconciliation against the same
source's annual TOTAL. It preserves source responses and writes a failure log.
The absence of a record is NOT silently interpreted as zero.
"""
from __future__ import annotations
import argparse
import csv
import hashlib
import io
import json
import os
import re
import sys
import time
from collections import defaultdict
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from pathlib import Path
from urllib.parse import urlencode

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

BASE = 'https://ec.europa.eu/eurostat/api/comext/dissemination/sdmx/2.1/data/DS-045409'
DATASET = 'DS-045409'
REPORTER = 'EU27_2020'
PARTNER = 'BD'
FLOW = '1'
FREQUENCY = 'A'
CN8_RE = re.compile(r'^[0-9]{8}$')
YEARS = list(range(2012, 2026))

class ValidationError(Exception):
    pass


def utc_now():
    return datetime.now(timezone.utc).isoformat()


def session_with_retries():
    s = requests.Session()
    retry = Retry(total=3, connect=3, read=2, status=3, backoff_factor=1.5,
                  status_forcelist=[429, 500, 502, 503, 504],
                  allowed_methods=['GET'], respect_retry_after_header=True)
    s.mount('https://', HTTPAdapter(max_retries=retry))
    s.headers.update({'User-Agent': 'AcademicDataValidation/1.0 (Eurostat Comext)',
                      'Accept': 'text/csv,application/csv,*/*'})
    return s


def request_url(year: int, indicator: str = 'VALUE_IN_EUROS', product: str = '') -> str:
    """Comext SDMX 2.1 key order: FREQ.REPORTER.PARTNER.PRODUCT.FLOW.INDICATORS."""
    key = f'{FREQUENCY}.{REPORTER}.{PARTNER}.{product}.{FLOW}.{indicator}'
    return f'{BASE}/{key}?' + urlencode({'format': 'SDMX-CSV',
                                        'startPeriod': year, 'endPeriod': year})


def get_raw(s, url, raw_path: Path):
    r = s.get(url, timeout=(15, 90))
    r.raise_for_status()
    # Eurostat can reply with HTML error pages and HTTP 200; never parse those as data.
    data = r.content
    if not data:
        raise ValidationError('Empty HTTP response')
    sample = data[:1500].decode('utf-8-sig', errors='replace').lstrip().lower()
    if sample.startswith('<!doctype html') or sample.startswith('<html'):
        raise ValidationError('Received HTML, not SDMX-CSV')
    raw_path.parent.mkdir(parents=True, exist_ok=True)
    raw_path.write_bytes(data)
    return data, {'status_code': r.status_code,
                  'content_type': r.headers.get('Content-Type', ''),
                  'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest(),
                  'url': r.url, 'saved_to': str(raw_path)}


def parse_sdmx_csv(data: bytes, year: int, indicator: str):
    """Return (CN8 rows, official TOTAL, aggregate stats).

    Reject unexpected dimensions so it cannot silently mix indicators or years.
    Missing OBS_VALUE is never changed into zero.
    """
    try:
        txt = data.decode('utf-8-sig')
    except UnicodeDecodeError as e:
        raise ValidationError(f'Bad SDMX-CSV encoding: {e}') from e
    reader = csv.DictReader(io.StringIO(txt))
    if not reader.fieldnames:
        raise ValidationError('Missing CSV header')
    # Ignore optional SDMX-CSV preamble? Eurostat SDMX-CSV typically has one header.
    cols = {name.strip().upper(): name for name in reader.fieldnames}
    required = ['PRODUCT', 'TIME_PERIOD', 'OBS_VALUE']
    missing = [c for c in required if c not in cols]
    if missing:
        raise ValidationError(f'Missing expected columns {missing}; received {reader.fieldnames}')

    code_col = cols['PRODUCT']; year_col = cols['TIME_PERIOD']; val_col = cols['OBS_VALUE']
    unique = set(); cn8 = []; totals = []; aggregates = defaultdict(int)
    for lineno, row in enumerate(reader, start=2):
        p = (row.get(code_col) or '').strip()
        y = (row.get(year_col) or '').strip()
        if not p and not y:
            continue
        if y != str(year):
            raise ValidationError(f'Year mismatch at CSV row {lineno}: {y!r} != {year}')
        for dimension, expected in [('REPORTER', REPORTER), ('PARTNER', PARTNER),
                                    ('FLOW', FLOW), ('FREQ', FREQUENCY),
                                    ('INDICATORS', indicator)]:
            if dimension in cols:
                observed = (row.get(cols[dimension]) or '').strip()
                if observed and observed != expected:
                    raise ValidationError(f'Unexpected {dimension}={observed!r} at line {lineno}')
        raw_v = (row.get(val_col) or '').strip()
        value = None
        if raw_v:
            try:
                value = Decimal(raw_v)
            except InvalidOperation as e:
                raise ValidationError(f'Bad value at row {lineno}: {raw_v!r}') from e
            if not value.is_finite() or value < 0:
                raise ValidationError(f'Invalid nonnegative import value at row {lineno}: {raw_v!r}')
        if CN8_RE.fullmatch(p):
            if p in unique:
                raise ValidationError(f'Duplicate CN8-year key {p}/{year} (row {lineno})')
            unique.add(p)
            cn8.append({'PRODUCT': p, 'TIME_PERIOD': str(year),
                        'OBS_VALUE': '' if value is None else str(value),
                        'OBS_FLAG': (row.get(cols.get('OBS_FLAG', ''), '') or '').strip(),
                        'VALUE_MISSING': value is None})
        elif p.upper() == 'TOTAL':
            totals.append(value)
        else:
            aggregates['other_product_rows'] += 1
    if not cn8:
        raise ValidationError('No CN8 codes returned for this year')
    if len(totals) > 1:
        raise ValidationError(f'Multiple TOTAL records detected in {year}')
    total = totals[0] if totals else None
    return cn8, total, dict(aggregates)


def get_total_separately(session, year, raw_dir, manifest):
    url = request_url(year, product='TOTAL')
    data, meta = get_raw(session, url, raw_dir / f'{DATASET}_{year}_BD_TOTAL.csv')
    manifest.append(meta)
    _, total, _ = parse_total_only(data, year)
    if total is None:
        raise ValidationError(f'No official TOTAL value returned for {year}')
    return total


def parse_total_only(data, year):
    text = data.decode('utf-8-sig')
    reader = csv.DictReader(io.StringIO(text))
    fields = {name.strip().upper(): name for name in (reader.fieldnames or [])}
    if not {'PRODUCT', 'TIME_PERIOD', 'OBS_VALUE'}.issubset(fields):
        raise ValidationError('Separate TOTAL query returned unexpected schema')
    totals = []
    for r in reader:
        if r[fields['TIME_PERIOD']] != str(year):
            raise ValidationError('Unexpected time period in TOTAL response')
        if r[fields['PRODUCT']].strip().upper() == 'TOTAL':
            x = r[fields['OBS_VALUE']].strip()
            if x:
                totals.append(Decimal(x))
    if len(totals) > 1:
        raise ValidationError('Duplicate official TOTAL records')
    return None, totals[0] if totals else None, {}


def reconcile(cn8, total, tolerance_eur=Decimal('1'), rel_tolerance=Decimal('0.0000001')):
    if total is None or total < 0:
        raise ValidationError('Cannot reconcile without a valid official annual TOTAL')
    missing_vals = sum(1 for r in cn8 if r['VALUE_MISSING'])
    # Missing values make the CN8 sum incomplete. Never call it a validated total.
    observed_sum = sum((Decimal(r['OBS_VALUE']) for r in cn8 if not r['VALUE_MISSING']), Decimal(0))
    diff = observed_sum - total
    tolerance = max(tolerance_eur, total * rel_tolerance)
    passed = missing_vals == 0 and abs(diff) <= tolerance
    return {'CN8_Count':len(cn8),'Missing_CN8_Values':missing_vals,
            'CN8_Sum_EUR':str(observed_sum),'Reported_Total_EUR':str(total),
            'Diff_EUR':str(diff),'Tolerance_EUR':str(tolerance),
            'Reconciliation_Passed':passed}


def write_csv(path: Path, rows, headers):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=headers, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(rows)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--out', default='bd_cn8_comext_validation_v4', help='Output directory')
    ap.add_argument('--start', type=int, default=2012)
    ap.add_argument('--end', type=int, default=2025)
    ap.add_argument('--sleep', type=float, default=0.4, help='Pause between year requests')
    args = ap.parse_args(argv)
    if args.start < 1988 or args.end > 2025 or args.end < args.start:
        ap.error('Choose valid complete years, ending no later than 2025 for this project')
    years = list(range(args.start, args.end + 1))
    out = Path(args.out).resolve(); raw_dir = out / 'raw'
    out.mkdir(parents=True, exist_ok=True)
    session = session_with_retries()
    manifest = {'dataset':DATASET,'execution_time_utc':utc_now(),
                'base_url': BASE, 'years_requested':years,'queries':[],
                'years_successful':[],'failures':[],'validation_status':'NOT_COMPLETE',
                'interpretation':'Missing years and missing CN8 values are NOT zeros.'}
    all_rows = []; recs=[]
    for y in years:
        print(f'Fetching {y} ...', flush=True)
        url = request_url(y)
        try:
            raw, meta = get_raw(session, url, raw_dir / f'{DATASET}_{y}_BD_VALUE.csv')
            manifest['queries'].append(meta)
            rows, total, other = parse_sdmx_csv(raw, y, 'VALUE_IN_EUROS')
            if total is None:
                total = get_total_separately(session, y, raw_dir, manifest['queries'])
            rec = {'year':y, **reconcile(rows, total), **other}
            recs.append(rec)
            if not rec['Reconciliation_Passed']:
                raise ValidationError(f'Year {y} failed reconciliation: {rec}')
            for row in rows:
                all_rows.append({'PRODUCT': row['PRODUCT'], 'TIME_PERIOD':str(y),
                                 'OBS_VALUE':row['OBS_VALUE'], 'OBS_FLAG':row['OBS_FLAG'],
                                 'SOURCE_DATASET':DATASET})
            manifest['years_successful'].append(y)
        except Exception as exc:
            failure = {'year':y, 'url':url, 'error_type':type(exc).__name__,
                       'error':str(exc), 'timestamp_utc':utc_now()}
            manifest['failures'].append(failure)
            print(f'  FAILED {y}: {type(exc).__name__}: {exc}', file=sys.stderr, flush=True)
        time.sleep(args.sleep)
    write_csv(out / 'annual_reconciliation_v4.csv', recs,
              ['year','CN8_Count','Missing_CN8_Values','CN8_Sum_EUR','Reported_Total_EUR',
               'Diff_EUR','Tolerance_EUR','Reconciliation_Passed','other_product_rows'])
    all_passed = len(manifest['years_successful']) == len(years) and not manifest['failures']
    manifest['validation_status'] = 'VALIDATED' if all_passed else 'NOT_COMPLETE'
    manifest['cn8_rows_validated'] = len(all_rows)
    manifest['year_count_validated'] = len(manifest['years_successful'])
    if all_passed:
        dest = out / f'eu_imports_bangladesh_cn8_{args.start}_{args.end}_VALIDATED.csv'
        all_rows.sort(key=lambda d:(d['TIME_PERIOD'],d['PRODUCT']))
        write_csv(dest,all_rows,['PRODUCT','TIME_PERIOD','OBS_VALUE','OBS_FLAG','SOURCE_DATASET'])
        manifest['validated_file'] = str(dest)
        print(f'VALIDATED: {dest} ({len(all_rows):,} product-year rows)')
    else:
        print('NOT VALIDATED. Raw successful responses (if any) and logs preserved. No full-panel CSV generated.')
    (out / 'run_manifest_v4.json').write_text(json.dumps(manifest, indent=2), encoding='utf-8')
    if not all_passed:
        sys.exit(2)

if __name__ == '__main__':
    main()