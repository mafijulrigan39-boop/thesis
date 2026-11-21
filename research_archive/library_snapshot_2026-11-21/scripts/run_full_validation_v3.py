#!/usr/bin/env python3
"""Download and validate Bangladesh-EU trade and tariff data for the MITB thesis.

Primary trade source: Eurostat Comext DS-045409 (official Eurostat API).
Tariff source: WITS / UNCTAD TRAINS SDMX API, with a separate TARIC raw-data check.

Run from an internet-enabled machine:
    python -m pip install requests
    python run_full_validation_v3.py --start 2012 --end 2025 --topn 200

The script does NOT turn absent records into zeroes. It keeps missing observations
explicit, writes raw API responses, and produces a run manifest for auditability.
"""
from __future__ import annotations
import argparse, csv, json, math, os, re, sys, time, xml.etree.ElementTree as ET
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import quote

try:
    import requests
except ImportError:
    raise SystemExit("Missing dependency. Install with: python -m pip install requests")

COMEXT_URL = "https://ec.europa.eu/eurostat/api/comext/dissemination/statistics/1.0/data/DS-045409"
ACTIVE_MANIFEST = None
ACTIVE_OUTDIR = None
WITS_URL = "https://wits.worldbank.org/API/V1/SDMX/V21/datasource/TRN/reporter/{reporter}/partner/{partner}/product/{product}/year/{year}/datatype/reported?format=JSON"
USER_AGENT = "Bangladesh-MITB-research/1.0 (academic data collection; contact via user)"
EU27 = {"AT","BE","BG","HR","CY","CZ","DK","EE","FI","FR","DE","GR","EL","HU","IE","IT","LV","LT","LU","MT","NL","PL","PT","RO","SK","SI","ES","SE","EU","EA"}
# Numeric WITS TRAINS partner codes for Bangladesh and relevant competitor origins; 000 is World/MFN.
WITS_COMPETITORS = ["050", "704", "156", "356", "586", "116", "792", "504", "788", "144", "818", "360"]
WITS_MFN_PARTNER = "000"  # WITS TRAINS: World / MFN partner code.
WITS_EU_REPORTER = "918"  # WITS numeric reporter code for European Union.
WITS_AVAILABILITY_URL = "https://wits.worldbank.org/API/V1/wits/datasource/trn/dataavailability/country/918/year/all"
WITS_COUNTRY_META_URL = "https://wits.worldbank.org/API/V1/wits/datasource/trn/country/ALL"


def safe_float(x: Any):
    if x is None or x == "" or x in (":", "..", "NA", "NaN"):
        return None
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def jsonstat_records(doc: dict[str, Any]):
    """Decode JSON-stat (Eurostat API format=JSON) into dimension/value rows."""
    ids = doc.get("id")
    sizes = doc.get("size")
    dims = doc.get("dimension")
    vals = doc.get("value")
    if not isinstance(ids, list) or not isinstance(sizes, list) or not isinstance(dims, dict) or vals is None:
        raise ValueError("Response is not a recognised JSON-stat object; raw response will be retained.")
    codes_by_dim, labels_by_dim = [], []
    for dim_id in ids:
        meta = dims[dim_id].get("category", {})
        idx = meta.get("index", {})
        if isinstance(idx, list):
            codes = idx
        elif isinstance(idx, dict):
            codes = [k for k, _ in sorted(idx.items(), key=lambda kv: kv[1])]
        else:
            raise ValueError(f"Cannot decode JSON-stat index for {dim_id}")
        codes_by_dim.append(codes)
        labels_by_dim.append(meta.get("label", {}) or {})
    if isinstance(vals, dict):
        pairs = ((int(k), v) for k, v in vals.items())
    else:
        pairs = enumerate(vals)
    for flat, val in pairs:
        if val is None:
            continue
        rem = int(flat)
        coords = [0] * len(sizes)
        for j in range(len(sizes) - 1, -1, -1):
            coords[j] = rem % int(sizes[j])
            rem //= int(sizes[j])
        row = {"value": safe_float(val)}
        for j, dim_id in enumerate(ids):
            code = codes_by_dim[j][coords[j]]
            row[dim_id] = code
            row[dim_id + "_label"] = labels_by_dim[j].get(code, code)
        yield row



def parse_wits_sdmx_json(doc: dict[str, Any]):
    """Flatten WITS SDMX-JSON observations into one row per tariff observation.

    WITS returns SDMX-JSON with indexed series/observation dimensions. The parser
    retains all dimension and attribute fields instead of assuming a fixed tariff
    schema. Values in the observation array begin with OBS_VALUE; remaining entries
    map to observation attributes in the order declared by the structure.
    """
    structure = doc.get("structure", {})
    dims = structure.get("dimensions", {})
    attrs = structure.get("attributes", {})
    series_dims = dims.get("series", []) or []
    obs_dims = dims.get("observation", []) or []
    series_attr_defs = attrs.get("series", []) or []
    obs_attr_defs = attrs.get("observation", []) or []

    def decode_values(defs, indices):
        out = {}
        for i, definition in enumerate(defs):
            if i >= len(indices):
                continue
            try:
                pos = int(indices[i])
            except (ValueError, TypeError):
                continue
            values = definition.get("values", []) or []
            if 0 <= pos < len(values):
                item = values[pos]
                out[definition.get("id", f"dim_{i}")] = item.get("id", item.get("name", pos))
                out[f"{definition.get('id', f'dim_{i}')}_label"] = item.get("name", item.get("id", pos))
        return out

    def decode_attrs(defs, raw_indices):
        out = {}
        for i, definition in enumerate(defs):
            if i >= len(raw_indices):
                continue
            try:
                pos = int(raw_indices[i])
            except (ValueError, TypeError):
                continue
            values = definition.get("values", []) or []
            if 0 <= pos < len(values):
                item = values[pos]
                key = definition.get("id", f"attr_{i}")
                out[key] = item.get("id", item.get("name", pos))
        return out

    output = []
    for dataset in doc.get("dataSets", []) or []:
        series_map = dataset.get("series", {}) or {}
        for series_key, series_obj in series_map.items():
            row_base = decode_values(series_dims, str(series_key).split(":"))
            row_base.update(decode_attrs(series_attr_defs, series_obj.get("attributes", []) or []))
            observations = series_obj.get("observations", {}) or {}
            for obs_key, obs_value in observations.items():
                if not isinstance(obs_value, list) or not obs_value:
                    continue
                row = dict(row_base)
                row.update(decode_values(obs_dims, str(obs_key).split(":")))
                row["OBS_VALUE"] = safe_float(obs_value[0])
                row.update(decode_attrs(obs_attr_defs, obs_value[1:]))
                output.append(row)
    return output


def get_json(session: requests.Session, url: str, params=None, timeout=180, retries=5):
    last = None
    for attempt in range(retries):
        try:
            r = session.get(url, params=params, timeout=timeout)
            if r.status_code in (429, 500, 502, 503, 504):
                last = RuntimeError(f"HTTP {r.status_code}: {r.text[:250]}")
                time.sleep(min(2 ** attempt, 20))
                continue
            r.raise_for_status()
            try:
                return r.json(), r.url, r.headers.get("content-type", "")
            except Exception:
                raise RuntimeError(f"Expected JSON; got {r.headers.get('content-type')}: {r.text[:500]}")
        except Exception as e:
            last = e
            if attempt < retries - 1:
                time.sleep(min(2 ** attempt, 20))
    raise RuntimeError(f"Request failed after {retries} attempts: {last}")


def get_text(session: requests.Session, url: str, timeout=180, retries=5):
    last = None
    for attempt in range(retries):
        try:
            r = session.get(url, timeout=timeout)
            if r.status_code in (429, 500, 502, 503, 504):
                last = RuntimeError(f"HTTP {r.status_code}: {r.text[:250]}")
                time.sleep(min(2 ** attempt, 20))
                continue
            r.raise_for_status()
            return r.text, r.url, r.headers.get("content-type", "")
        except Exception as e:
            last = e
            if attempt < retries - 1:
                time.sleep(min(2 ** attempt, 20))
    raise RuntimeError(f"Text request failed after {retries} attempts: {last}")


def comext_query(session, year: int, partner: str | None = None, products: list[str] | None = None,
                 indicator: str = "VALUE_IN_EUROS", raw_dir: Path | None = None,
                 raw_stem: str | None = None):
    """Query one calendar year and one Comext indicator.

    VALUE_IN_EUROS is the value measure; QUANTITY_IN_100KG is net mass in
    100-kg units. The latter supports unit-value calculations only when present
    and positive. Missing quantity observations are kept missing, never imputed.
    """
    params = [
        ("format", "JSON"), ("lang", "en"), ("freq", "A"),
        ("reporter", "EU27_2020"), ("flow", "1"),
        ("indicators", indicator),
        ("sinceTimePeriod", str(year)), ("untilTimePeriod", str(year)),
    ]
    if partner:
        params.append(("partner", partner))
    if products:
        params.extend(("product", p) for p in products)
    prepared_url = requests.Request("GET", COMEXT_URL, params=params).prepare().url
    try:
        doc, url, ctype = get_json(session, COMEXT_URL, params=params)
    except Exception as exc:
        failure = {"stage":"comext_request_failed","year":year,"partner":partner,
                   "products":products,"indicator":indicator,"url":prepared_url,
                   "error":str(exc),"data_downloaded":False}
        if raw_dir is not None:
            failure_dir=raw_dir/"raw_api"; failure_dir.mkdir(parents=True,exist_ok=True)
            with (failure_dir/"request_failures.jsonl").open("a",encoding="utf-8") as f:
                f.write(json.dumps(failure,ensure_ascii=False)+"\n")
        if ACTIVE_MANIFEST is not None and ACTIVE_OUTDIR is not None:
            ACTIVE_MANIFEST.setdefault("api_requests",[]).append(failure)
            ACTIVE_MANIFEST["run_status"]="failed"
            ACTIVE_MANIFEST["last_error"]=str(exc)
            ACTIVE_MANIFEST["run_finished_utc"]=datetime.now(timezone.utc).isoformat()
            ACTIVE_MANIFEST["output_directory"]=str(ACTIVE_OUTDIR)
            (ACTIVE_OUTDIR/"run_manifest_partial.json").write_text(json.dumps(ACTIVE_MANIFEST,indent=2),encoding="utf-8")
        raise
    if raw_dir is not None and raw_stem:
        write_raw_response(raw_dir, raw_stem, doc)
    return list(jsonstat_records(doc)), url, ctype


def code_digits(code: Any) -> str:
    s = str(code)
    m = re.search(r"(\d{8})$", s)
    if m:
        return m.group(1)
    m = re.search(r"(\d{6})$", s)
    return m.group(1) if m else ""


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str] | None = None):
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = sorted({k for r in rows for k in r.keys()}) if rows else ["note"]
    with path.open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def read_product_codes(rows: list[dict[str, Any]]):
    out = {}
    for r in rows:
        raw = str(r.get("product", ""))
        digits = code_digits(raw)
        if len(digits) == 8:
            out[raw] = {"product_raw_code": raw, "cn8": digits,
                        "hs6": digits[:6], "description": r.get("product_label", ""),
                        "latest_value_eur": r.get("value")}
    return out


def write_raw_response(outdir: Path, stem: str, doc: Any):
    p = outdir / "raw_api" / f"{stem}.json"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(doc, ensure_ascii=False), encoding="utf-8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--start", type=int, default=2012)
    ap.add_argument("--end", type=int, default=2025)
    ap.add_argument("--topn", type=int, default=200)
    ap.add_argument("--out", default="bangladesh_eu_full_validation")
    ap.add_argument("--skip-wits", action="store_true", help="Skip WITS TRAINS tariff API calls")
    ap.add_argument("--pause", type=float, default=0.35)
    ap.add_argument("--gsp-status-map", default="gsp_beneficiary_status_template.csv",
                    help="Year-country GSP status map; must be legally reviewed.")
    ap.add_argument("--gsp-coverage", default="gsp_beneficiary_mapping_coverage_template.csv",
                    help="Year-level mapping completeness attestation; calculations are blocked without it.")
    ap.add_argument("--concordance", default="cn8_year_to_stable_product_concordance_template.csv",
                    help="Year-specific CN8 to stable-product crosswalk; period rankings/growth require complete mapping.")
    args = ap.parse_args()
    if args.start > args.end or args.topn < 100 or args.topn > 200:
        raise SystemExit("Use start <= end and topn between 100 and 200.")

    outdir = Path(args.out).resolve()
    outdir.mkdir(parents=True, exist_ok=True)
    global ACTIVE_MANIFEST, ACTIVE_OUTDIR
    ACTIVE_OUTDIR = outdir
    session = requests.Session()
    session.headers.update({"User-Agent": USER_AGENT, "Accept": "application/json"})
    manifest = {"run_started_utc": datetime.now(timezone.utc).isoformat(),
                "start_year": args.start, "end_year": args.end, "topn": args.topn,
                "comext_dataset": "DS-045409", "comext_reporter": "EU27_2020",
                "trade_flow": "imports", "measure": "VALUE_IN_EUROS", "api_requests": [],
                "limitations": ["No API absence is imputed to zero.",
                                "HS6 is derived as the first six digits of CN8; formal HS revision concordance remains necessary.",
                                "WITS TRAINS is HS6 tariff summary data, not CN8/CN10 tariff-line data.",
                                "Article 33 ratios are only calculated for years with a complete contemporaneous GSP beneficiary map; the 2027 Annex I must not be backcast.",
                                "EUR/kg unit values use reported net mass in 100-kg units and are only calculated when both value and mass are non-missing and positive."]}
    ACTIVE_MANIFEST = manifest

    # Stage 1: full EU imports from Bangladesh for all CN8 positions, one year/request.
    bd_rows = []
    latest_codebook = {}
    for year in range(args.start, args.end + 1):
        rows, url, ctype = comext_query(session, year, partner="BD", raw_dir=outdir, raw_stem=f"comext_bd_value_{year}")
        n8 = 0
        for r in rows:
            raw = str(r.get("product", ""))
            digits = code_digits(raw)
            if len(digits) != 8:
                continue
            n8 += 1
            rr = dict(r)
            rr.update({"year": year, "product_raw_code": raw, "cn8": digits,
                       "hs6_prefix": digits[:6], "hs2_chapter": digits[:2],
                       "source_dataset": "Eurostat Comext DS-045409", "source_url": url})
            bd_rows.append(rr)
            latest_codebook[raw] = {"product_raw_code": raw, "cn8": digits,
                                    "hs6_prefix": digits[:6], "description": r.get("product_label", "")}
        manifest["api_requests"].append({"stage": "BD_all_CN8", "year": year, "url": url,
                                         "content_type": ctype, "records_8digit": n8})
        print(f"Stage 1: {year}: {n8} CN8 observations", flush=True)
        time.sleep(args.pause)
    if not bd_rows:
        raise RuntimeError("No CN8 rows returned. Check API product dimension codes or use the official Comext CSV bulk download.")

    # Stage 1B: net-mass quantities for the complete Bangladesh product-year panel.
    # This allows value-per-kg calculations where the quantity observation exists.
    bd_qty_rows = []
    for year in range(args.start, args.end + 1):
        qrows, qurl, qctype = comext_query(session, year, partner="BD", indicator="QUANTITY_IN_100KG", raw_dir=outdir, raw_stem=f"comext_bd_netmass_{year}")
        for q in qrows:
            qr = dict(q); qr.update({"year": year, "source_url": qurl, "indicator": "QUANTITY_IN_100KG", "quantity_in_100kg": q.get("value")})
            bd_qty_rows.append(qr)
        manifest["api_requests"].append({"stage":"BD_all_CN8_net_mass_100kg", "year":year,
                                         "url":qurl, "content_type":qctype, "records":len(qrows)})
        print(f"Stage 1B: {year}: {len(qrows)} quantity observations", flush=True)
        time.sleep(args.pause)
    qty_map = {(str(r.get("product")), int(r.get("year", 0))): r.get("value") for r in bd_qty_rows}
    for r in bd_rows:
        q = qty_map.get((str(r.get("product")), int(r.get("year", 0))))
        r["quantity_in_100kg"] = q
        r["unit_value_eur_per_kg"] = (r.get("value") / (q * 100.0)
                                      if r.get("value") is not None and q not in (None, 0) else None)
    write_csv(outdir / "bd_eu_imports_all_cn8_annual.csv", bd_rows)
    write_csv(outdir / "bd_eu_imports_all_cn8_quantity_annual.csv", bd_qty_rows)

    # Establish the latest year actually returned; do not assume 2025 is complete.
    observed_years = sorted({int(r["year"]) for r in bd_rows})
    latest_year = max(observed_years)
    years = list(range(args.start, args.end + 1))
    bd_map = {(r["product_raw_code"], int(r["year"])): r for r in bd_rows}
    qty_map = {(str(r.get("product")), int(r.get("year", 0))): r.get("value") for r in bd_qty_rows}

    # Annual rankings preserve the year-specific CN8 classification. Never sum
    # identical-looking CN8 strings across years without an official concordance.
    annual_rankings = []
    selected_by_year = {}
    annual_top_all = {}
    annual_top_s11b = {}
    desc_by_year = {}
    chapter_by_year = {}
    for year in years:
        year_rows = [r for r in bd_rows if int(r["year"]) == year and r.get("value") is not None]
        vals = defaultdict(float)
        desc = {}
        chap = {}
        for r in year_rows:
            code = r["product_raw_code"]
            vals[code] += r["value"]
            desc[code] = r.get("product_label", "")
            chap[code] = r["hs2_chapter"]
        all_codes = sorted(vals, key=vals.get, reverse=True)[:args.topn]
        s11b_codes = sorted((c for c in vals if chap.get(c) in {"61", "62", "63"}),
                            key=vals.get, reverse=True)[:args.topn]
        annual_top_all[year] = all_codes
        annual_top_s11b[year] = s11b_codes
        desc_by_year[year] = desc
        chapter_by_year[year] = chap
        selected_by_year[year] = list(dict.fromkeys(all_codes + s11b_codes))
        for metric, codes in (("all_sector", all_codes), ("S11b_ch61_63", s11b_codes)):
            for rank, code in enumerate(codes, 1):
                annual_rankings.append({"year": year, "ranking_scope": metric, "rank": rank,
                                        "product_raw_code": code, "cn8": code_digits(code),
                                        "hs6_prefix_unharmonised": code_digits(code)[:6],
                                        "chapter": chap.get(code), "description": desc.get(code),
                                        "value_eur": vals[code],
                                        "classification_identity_across_years": "not_assumed"})
    write_csv(outdir / "top_products_annual_cn8_year_specific.csv", annual_rankings)
    if not annual_top_all.get(latest_year):
        raise RuntimeError(f"No ranked CN8 observations in latest observed year {latest_year}.")

    latest_codes = annual_top_all[latest_year]
    latest_s11b_codes = annual_top_s11b[latest_year]
    latest_desc = desc_by_year[latest_year]
    latest_chap = chapter_by_year[latest_year]
    write_csv(outdir / "top_products_latest_all_sectors.csv",
              [{"rank":i+1,"product_raw_code":c,"cn8":code_digits(c),"hs6_prefix_unharmonised":code_digits(c)[:6],
                "chapter":latest_chap.get(c),"description":latest_desc.get(c),
                "value_eur":next(r.get("value") for r in bd_rows if r["product_raw_code"]==c and int(r["year"])==latest_year),
                "year":latest_year,"classification_identity_across_years":"not_assumed"}
               for i,c in enumerate(latest_codes)])
    write_csv(outdir / "top_products_latest_S11b_ch61_63.csv",
              [{"rank":i+1,"product_raw_code":c,"cn8":code_digits(c),"chapter":latest_chap.get(c),
                "description":latest_desc.get(c),
                "value_eur":next(r.get("value") for r in bd_rows if r["product_raw_code"]==c and int(r["year"])==latest_year),
                "year":latest_year,"classification_identity_across_years":"not_assumed"}
               for i,c in enumerate(latest_s11b_codes)])

    # Create year-specific concordance template from the actual returned CN8-year universe.
    concordance_path = Path(args.concordance)
    if not concordance_path.is_absolute():
        cwd_candidate = Path.cwd() / concordance_path
        concordance_path = cwd_candidate if cwd_candidate.exists() else (outdir / concordance_path.name)
    concordance_rows = []
    for r in sorted(bd_rows, key=lambda x:(int(x["year"]),x["product_raw_code"])):
        concordance_rows.append({"year":int(r["year"]),"cn8":r["cn8"],"product_raw_code":r["product_raw_code"],
                                 "description":r.get("product_label", ""),"cn_version":"",
                                 "stable_product_id":"","concordance_source":"",
                                 "mapping_quality":"","manual_review":"pending"})
    if not concordance_path.exists():
        write_csv(concordance_path, concordance_rows)
    else:
        with concordance_path.open("r",newline="",encoding="utf-8-sig") as f:
            supplied_concordance=list(csv.DictReader(f))
        concordance_rows=supplied_concordance

    # Period rankings and YoY growth are blocked until every observed CN8-year cell
    # has an exact, sourced stable-product mapping. This prevents code-version drift.
    concordance_map = {}
    for cr in concordance_rows:
        try: cy=int(cr.get("year", ""))
        except (TypeError,ValueError): continue
        cc=str(cr.get("cn8", "")).strip()
        sid=str(cr.get("stable_product_id", "")).strip()
        source=str(cr.get("concordance_source", "")).strip()
        quality=str(cr.get("mapping_quality", "")).strip().lower()
        if cy and cc and sid and source and quality in {"exact","high"}:
            concordance_map[(cy,cc)]=sid
    observed_keys={(int(r["year"]),r["cn8"]) for r in bd_rows}
    unmapped=sorted(observed_keys-set(concordance_map))
    if not unmapped:
        period_values=defaultdict(float); period_desc={}
        annual_stable=defaultdict(float)
        for r in bd_rows:
            k=(int(r["year"]),r["cn8"]); sid=concordance_map[k]
            if r.get("value") is not None:
                period_values[sid]+=r["value"]
                annual_stable[(sid,int(r["year"]))]+=r["value"]
                period_desc[sid]=r.get("product_label","")
        write_csv(outdir/"top_products_period_harmonised.csv",
                  [{"rank":i+1,"stable_product_id":sid,"value_eur_period":v,
                    "description_latest_observed":period_desc.get(sid),"period_start":args.start,
                    "period_end":args.end,"concordance_basis":"complete sourced year-specific map"}
                   for i,(sid,v) in enumerate(sorted(period_values.items(),key=lambda kv:kv[1],reverse=True)[:args.topn])])
        growth=[]
        for (sid,year),v in sorted(annual_stable.items()):
            prev=annual_stable.get((sid,year-1))
            growth.append({"stable_product_id":sid,"year":year,"value_eur":v,
                           "previous_year_value_eur":prev,
                           "yoy_growth_pct":((v/prev-1)*100 if prev not in (None,0) else None),
                           "growth_status":"calculated" if prev not in (None,0) else "no_comparable_previous_year"})
        write_csv(outdir/"product_growth_harmonised.csv",growth)
        period_status=[{"status":"complete","observed_cn8_year_keys":len(observed_keys),"unmapped_keys":0,
                        "note":"Period aggregation and YoY growth use only exact/high, sourced stable-product mappings."}]
    else:
        write_csv(outdir/"period_ranking_and_growth_status.csv",
                  [{"status":"not_calculated_missing_concordance","observed_cn8_year_keys":len(observed_keys),
                    "unmapped_keys":len(unmapped),"example_unmapped_year_cn8":";".join(f"{y}:{c}" for y,c in unmapped[:25]),
                    "note":"No cross-year aggregation or YoY growth until a complete official CN/HS concordance is supplied."}])

    # Year-by-year observed-code and product-year presence audit. Non-returned is
    # not silently classified as zero; official CN code lists are still required
    # to distinguish trade zeros from classification exits and true missingness.
    code_years=defaultdict(set); code_labels={}; all_observed_codes=set()
    for r in bd_rows:
        code=r["cn8"]; all_observed_codes.add(code); code_years[code].add(int(r["year"]))
        code_labels[(int(r["year"]),code)]=r.get("product_label","")
    observed_code_year={(int(r["year"]),r["cn8"]):r for r in bd_rows}
    audit=[]
    for year in years:
        for code in sorted(all_observed_codes):
            rr=observed_code_year.get((year,code))
            observed=rr is not None and rr.get("value") is not None
            audit.append({"year":year,"cn8":code,"description":(rr.get("product_label","") if rr else ""),
                          "observed_in_year":observed,"obs_status":"observed" if observed else "not_returned_by_api",
                          "first_observed_year":(min(code_years[code]) if code_years[code] else None),
                          "last_observed_year":(max(code_years[code]) if code_years[code] else None),
                          "years_observed_in_panel":len(code_years[code]),
                          "classification_version":"not_yet_verified",
                          "official_nomenclature_crosswalk_status":"pending",
                          "interpretation":"Not returned is not assumed to be zero; could reflect zero trade, code change, unavailable observation or coverage."})
    write_csv(outdir/"cn8_year_observation_classification_audit.csv",audit)
    write_csv(outdir/"cn8_nomenclature_year_template.csv",
              [{"year":y,"cn_version":"","official_cn_code_list_url":"",
                "downloaded_file":"","download_date":"","review_status":"pending"} for y in years])

    # Product-year selection is year-specific: competitors are queried using that
    # year's CN8 codes, not 2025 codes retrofitted into earlier nomenclatures.
    selected_union=list(dict.fromkeys(c for y in years for c in selected_by_year[y]))
    selected_dictionary=[]
    selected_cells=[]
    for y in years:
        for c in selected_by_year[y]:
            selected_dictionary.append({"year":y,"product_raw_code":c,"cn8":code_digits(c),
                                        "hs6_prefix_unharmonised":code_digits(c)[:6],
                                        "chapter":chapter_by_year[y].get(c),
                                        "description":desc_by_year[y].get(c)})
            selected_cells.append((y,c))
    write_csv(outdir/"selected_CN8_product_dictionary_year_specific.csv",selected_dictionary)
    balanced=[]
    for y,c in selected_cells:
        r=bd_map.get((c,y))
        balanced.append({"year":y,"product_raw_code":c,"cn8":code_digits(c),
                         "value_eur":r.get("value") if r else None,
                         "obs_status":"observed" if r and r.get("value") is not None else "not_returned_by_api",
                         "classification_version":"not_yet_verified"})
    write_csv(outdir/"bd_selected_products_year_specific_panel.csv",balanced)

    # Stage 2: matching all-origin trade values for each year's selected CN8 lines.
    competitor_rows=[]
    for year in years:
        selected=selected_by_year[year]
        for start in range(0,len(selected),50):
            chunk=selected[start:start+50]
            rows,url,ctype=comext_query(session,year,partner=None,products=chunk,raw_dir=outdir,
                                        raw_stem=f"comext_all_partners_value_{year}_batch{start//50+1}")
            for r in rows:
                raw=str(r.get("product","")); digits=code_digits(raw)
                rr=dict(r); rr.update({"year":year,"product_raw_code":raw,"cn8":digits,
                                       "hs6_prefix_unharmonised":digits[:6],"source_url":url})
                competitor_rows.append(rr)
            manifest["api_requests"].append({"stage":"all_partners_year_specific_CN8_value","year":year,
                                             "chunk_n":len(chunk),"url":url,"content_type":ctype,"records":len(rows)})
            time.sleep(args.pause)
    write_csv(outdir/"eu_selected_products_all_partners_annual.csv",competitor_rows)

    # Stage 2B: matching partner net mass and EUR/kg only when both measures exist.
    competitor_qty_rows=[]
    for year in years:
        selected=selected_by_year[year]
        for start in range(0,len(selected),50):
            chunk=selected[start:start+50]
            rows,url,ctype=comext_query(session,year,partner=None,products=chunk,indicator="QUANTITY_IN_100KG",
                                        raw_dir=outdir,raw_stem=f"comext_all_partners_netmass_{year}_batch{start//50+1}")
            for r in rows:
                rr=dict(r); rr.update({"year":year,"indicator":"QUANTITY_IN_100KG","quantity_in_100kg":r.get("value"),"source_url":url})
                competitor_qty_rows.append(rr)
            manifest["api_requests"].append({"stage":"all_partners_year_specific_CN8_netmass","year":year,
                                             "chunk_n":len(chunk),"url":url,"content_type":ctype,"records":len(rows)})
            time.sleep(args.pause)
    qmap={(str(r.get("product")),str(r.get("partner")),int(r.get("year",0))):r.get("value") for r in competitor_qty_rows}
    for r in competitor_rows:
        q=qmap.get((str(r.get("product")),str(r.get("partner")),int(r.get("year",0))))
        r["quantity_in_100kg"]=q
        r["unit_value_eur_per_kg"]=(r.get("value")/(q*100.0) if r.get("value") is not None and q is not None and q>0 else None)
    write_csv(outdir/"eu_selected_products_all_partners_quantity_annual.csv",competitor_qty_rows)
    write_csv(outdir/"eu_selected_products_all_partners_annual_with_unit_values.csv",competitor_rows)

    # Stage 3: extra-EU denominators for same-year CN8 products.
    ext_rows=[]
    for year in years:
        selected=selected_by_year[year]
        for start in range(0,len(selected),50):
            chunk=selected[start:start+50]
            rows,url,ctype=comext_query(session,year,partner="EXT_EU27_2020",products=chunk,raw_dir=outdir,
                                        raw_stem=f"comext_extraEU_selected_value_{year}_batch{start//50+1}")
            for r in rows:
                raw=str(r.get("product","")); rr=dict(r)
                rr.update({"year":year,"product_raw_code":raw,"cn8":code_digits(raw),"source_url":url})
                ext_rows.append(rr)
            manifest["api_requests"].append({"stage":"extraEU_year_specific_CN8_total","year":year,
                                             "chunk_n":len(chunk),"url":url,"content_type":ctype,"records":len(rows)})
            time.sleep(args.pause)
    write_csv(outdir/"eu_selected_products_extraEU_totals_annual.csv",ext_rows)

    # Compute top-five suppliers and Bangladesh market share for every selected
    # product-year. Partner absences stay missing; no silent zero fill.
    eu_partner_codes=EU27|{"EU27_2020","EXT_EU27_2020","WORLD","WLD","999","TOTAL"}
    rows_by_key=defaultdict(list)
    for r in competitor_rows:
        partner=str(r.get("partner",""))
        if partner in eu_partner_codes or len(partner)!=2: continue
        rows_by_key[(int(r.get("year",0)),str(r.get("product")))].append(r)
    ext_map={(int(r["year"]),str(r.get("product"))):r.get("value") for r in ext_rows}
    top5=[]; shares=[]
    for year,code in selected_cells:
        group=rows_by_key.get((year,code),[])
        ranked=sorted([r for r in group if str(r.get("partner"))!="BD" and r.get("value") is not None],
                      key=lambda r:r.get("value") or 0,reverse=True)
        for rank,r in enumerate(ranked[:5],1):
            top5.append({"year":year,"product_raw_code":code,"cn8":code_digits(code),"competitor_rank":rank,
                         "partner_code":r.get("partner"),"partner_name":r.get("partner_label"),"value_eur":r.get("value")})
        bdv=bd_map.get((code,year),{}).get("value")
        total=ext_map.get((year,code))
        shares.append({"year":year,"product_raw_code":code,"cn8":code_digits(code),
                       "bangladesh_value_eur":bdv,"extra_eu_imports_total_eur":total,
                       "bd_market_share":(bdv/total if bdv is not None and total not in (None,0) else None),
                       "competitor_observation_count":len(group),
                       "top5_count":min(5,len(ranked)),
                       "share_status":"calculated" if bdv is not None and total not in (None,0) else "missing_denominator_or_BD_value"})
    write_csv(outdir/"top5_competitors_by_product_year.csv",top5)
    write_csv(outdir/"market_share_by_product_year.csv",shares)

    # Stage 4: S-11b denominator source data, all partner origins, Chapters 61–63.
    s11b_rows=[]
    for year in years:
        rows,url,ctype=comext_query(session,year,partner=None,products=["61","62","63"],raw_dir=outdir,
                                    raw_stem=f"comext_s11b_chapters_all_partners_{year}")
        for r in rows:
            rr=dict(r); rr.update({"year":year,"source_url":url})
            s11b_rows.append(rr)
        manifest["api_requests"].append({"stage":"S11b_chapters_61_63_by_partner","year":year,
                                         "url":url,"content_type":ctype,"records":len(rows)})
        time.sleep(args.pause)
    write_csv(outdir/"s11b_chapters_61_63_by_partner_annual.csv",s11b_rows)
    chapter_presence=defaultdict(set); chapter_values=defaultdict(dict); partner_labels={}
    for r in s11b_rows:
        try: y=int(r.get("year",0))
        except (TypeError,ValueError): continue
        partner=str(r.get("partner","")); chapter=str(r.get("product",""))
        if chapter in {"61","62","63"}:
            chapter_presence[(y,partner)].add(chapter)
            chapter_values[(y,partner)][chapter]=r.get("value")
            partner_labels[partner]=r.get("partner_label",partner)
    s11b_totals={}; s11b_coverage=[]
    all_partners=sorted({p for _,p in chapter_presence})
    for year in years:
        for partner in all_partners:
            present=chapter_presence.get((year,partner),set())
            missing=sorted({"61","62","63"}-present)
            complete=not missing
            vals=chapter_values.get((year,partner),{})
            total=sum(v for v in vals.values() if v is not None) if complete else None
            s11b_totals[(partner,year)]=total
            s11b_coverage.append({"year":year,"partner_code":partner,"partner_name":partner_labels.get(partner,partner),
                                  "chapters_observed":";".join(sorted(present)),"chapters_missing":";".join(missing),
                                  "complete_ch61_63":complete,"s11b_value_eur":total,
                                  "status":"complete" if complete else "incomplete_not_zero_filled"})
    write_csv(outdir/"s11b_partner_chapter_coverage.csv",s11b_coverage)
    write_csv(outdir/"s11b_partner_totals_annual.csv",
              [{"partner_code":p,"partner_name":partner_labels.get(p,p),"year":y,"s11b_value_eur":v,
                "status":"complete" if v is not None else "incomplete_not_zero_filled"}
               for (p,y),v in sorted(s11b_totals.items(),key=lambda x:(x[0][1],x[0][0]))])

    # Separate all-origin denominator for Article 33(2)'s <=6% exception.
    s11b_all_origin_rows=[]; all_origin_s11b={}; all_origin_coverage=[]
    for year in years:
        rows,url,ctype=comext_query(session,year,partner="EXT_EU27_2020",products=["61","62","63"],raw_dir=outdir,
                                    raw_stem=f"comext_s11b_all_origin_extraEU_{year}")
        by_ch={str(r.get("product")):r.get("value") for r in rows}
        for r in rows:
            rr=dict(r); rr.update({"year":year,"source_url":url}); s11b_all_origin_rows.append(rr)
        missing=sorted({"61","62","63"}-set(by_ch))
        complete=not missing
        total=sum(v for v in by_ch.values() if v is not None) if complete else None
        all_origin_s11b[year]=total
        all_origin_coverage.append({"year":year,"chapters_observed":";".join(sorted(by_ch)),
                                    "chapters_missing":";".join(missing),"complete_ch61_63":complete,
                                    "s11b_all_origin_eur":total,"status":"complete" if complete else "incomplete_not_zero_filled"})
        manifest["api_requests"].append({"stage":"S11b_all_origin_extraEU_total","year":year,"url":url,
                                         "content_type":ctype,"records":len(rows)})
        time.sleep(args.pause)
    write_csv(outdir/"s11b_all_origin_extraEU_totals_annual.csv",s11b_all_origin_rows)
    write_csv(outdir/"s11b_all_origin_coverage_audit.csv",all_origin_coverage)

    # Article 33 calculator: both a complete legal beneficiary map and a complete
    # beneficiary x year x Chapters 61–63 data panel are mandatory. Historical
    # 2012–2025 results are labelled retrospective simulations, not legal decisions.
    status_path=Path(args.gsp_status_map)
    if not status_path.is_absolute():
        cwd_candidate=Path.cwd()/status_path
        status_path=cwd_candidate if cwd_candidate.exists() else (outdir/status_path.name)
    coverage_path=Path(args.gsp_coverage)
    if not coverage_path.is_absolute():
        cwd_candidate=Path.cwd()/coverage_path
        coverage_path=cwd_candidate if cwd_candidate.exists() else (outdir/coverage_path.name)
    if not status_path.exists():
        write_csv(status_path,[],["year","partner_code","partner_name","scheme_status","eligible_for_denominator",
                                  "effective_from","effective_to","official_source_url","product_scope_notes"])
    if not coverage_path.exists():
        write_csv(coverage_path,[],["year","mapping_complete","expected_beneficiary_count","legal_source_url",
                                    "reviewer_attestation","review_date","notes"])
    with status_path.open("r",newline="",encoding="utf-8-sig") as f: beneficiary_rows=list(csv.DictReader(f))
    with coverage_path.open("r",newline="",encoding="utf-8-sig") as f: mapping_coverage=list(csv.DictReader(f))
    by_year_codes=defaultdict(set); duplicate_keys=set(); seen=set()
    for br in beneficiary_rows:
        try: byear=int(br.get("year",""))
        except (TypeError,ValueError): continue
        code=str(br.get("partner_code","")).strip()
        status=str(br.get("scheme_status","")).strip().lower()
        eligible=str(br.get("eligible_for_denominator","")).strip().lower() in {"true","yes","1"}
        if code and eligible and status in {"eba","standard gsp","gsp+","standard_gsp","gsp_plus","gsp+ (transitional)","standard gsp (partial withdrawal)","eba (partial withdrawal)"}:
            key=(byear,code)
            if key in seen: duplicate_keys.add(key)
            seen.add(key); by_year_codes[byear].add(code)
    coverage_by_year={}
    for cr in mapping_coverage:
        try: cy=int(cr.get("year",""))
        except (TypeError,ValueError): continue
        coverage_by_year[cy]=cr
    article33_rows=[]
    for year in years:
        codes=by_year_codes.get(year,set()); cov=coverage_by_year.get(year,{})
        attested=str(cov.get("mapping_complete","")).strip().lower() in {"true","yes","1"}
        try: expected=int(cov.get("expected_beneficiary_count",""))
        except (TypeError,ValueError): expected=-1
        country_rows=[br for br in beneficiary_rows if str(br.get("year","")).strip()==str(year)
                      and str(br.get("partner_code","")).strip() in codes]
        row_sources_ok=all(bool(str(br.get("official_source_url","")).strip()) and bool(str(br.get("effective_from","")).strip())
                           for br in country_rows)
        mapping_ok=(attested and expected>0 and len(codes)==expected and "BD" in codes
                    and not any(y==year for y,c in duplicate_keys) and row_sources_ok
                    and bool(cov.get("legal_source_url")) and bool(cov.get("reviewer_attestation")))
        coverage_ok=all(s11b_totals.get((code,year)) is not None for code in codes) and bool(codes)
        all_origin_ok=all_origin_s11b.get(year) is not None
        bd_s11b=s11b_totals.get(("BD",year))
        ready=mapping_ok and coverage_ok and all_origin_ok and bd_s11b is not None
        beneficiary_denominator=(sum(s11b_totals[(code,year)] for code in codes) if ready else None)
        bd_share=(bd_s11b/beneficiary_denominator if ready and beneficiary_denominator not in (None,0) else None)
        all_share=(bd_s11b/all_origin_s11b[year] if ready and all_origin_s11b[year] not in (None,0) else None)
        bd_status=next((str(br.get("scheme_status","")) for br in beneficiary_rows
                        if str(br.get("partner_code","" )).strip()=="BD" and str(br.get("year","" )).strip()==str(year)),"")
        applicability=("exempt_eba" if bd_status.strip().lower()=="eba" else
                       "potentially_subject_if_standard_gsp_or_gsp_plus" if bd_status.strip().lower() in {"standard gsp","gsp+","standard_gsp","gsp_plus"} else
                       "status_missing_or_not_a_beneficiary")
        article33_rows.append({"year":year,"legal_period":"pre_2027_retrospective_simulation_not_legal_application" if year<2027 else "new_regulation_period",
                               "Bangladesh_S11b_EUR":bd_s11b,"all_GSP_beneficiary_S11b_EUR":beneficiary_denominator,
                               "Bangladesh_share_of_beneficiary_denominator":bd_share,
                               "all_origin_extraEU_S11b_EUR":all_origin_s11b.get(year),
                               "Bangladesh_share_of_all_origin_S11b":all_share,
                               "threshold_37pct_test":("exceeds_37pct" if bd_share is not None and bd_share>0.37 else "does_not_exceed_37pct" if bd_share is not None else "not_calculated"),
                               "threshold_6pct_exception_test":("at_or_below_6pct" if all_share is not None and all_share<=0.06 else "above_6pct" if all_share is not None else "not_calculated"),
                               "Bangladesh_scheme_status":bd_status or None,"Article33_applicability_note":applicability,
                               "mapping_complete_attested":mapping_ok,"beneficiary_partner_count":len(codes),
                               "beneficiary_trade_coverage_complete":coverage_ok,"all_origin_trade_coverage_complete":all_origin_ok,
                               "status":"calculated" if ready else "not_calculated_incomplete_legal_or_trade_coverage",
                               "legal_basis":"Regulation (EU) 2026/1395 Article 33(1)-(3), Annex III S-11b, Annex IV point 3",
                               "interpretation":"37% denominator is imports from all GSP beneficiary countries in S-11b; 6% denominator is total Union imports of the same goods. EBA countries are exempt from removal. 2012-2025 is a retrospective scenario only."})
    write_csv(outdir/"article33_s11b_share_scenarios.csv",article33_rows)

    # Stage 5: WITS TRAINS metadata + HS6 tariff data. Metadata is essential because
    # preferential schedules can be attached to alpha-numeric partner groups rather
    # than directly to the beneficiary country code.
    if not args.skip_wits:
        meta_dir = outdir / "wits_metadata"
        meta_dir.mkdir(exist_ok=True)
        meta_log = []
        for label, url in [("EU_TRAINS_data_availability", WITS_AVAILABILITY_URL),
                           ("TRAINS_country_and_partner_codes", WITS_COUNTRY_META_URL)]:
            try:
                body, final_url, ctype = get_text(session, url, timeout=180, retries=3)
                (meta_dir / f"{label}.xml").write_text(body, encoding="utf-8")
                meta_log.append({"metadata": label, "url": final_url, "content_type": ctype, "status": "downloaded"})
            except Exception as e:
                meta_log.append({"metadata": label, "url": url, "status": "failed", "error": str(e)})
            time.sleep(max(args.pause, 0.5))
        write_csv(outdir / "wits_metadata_manifest.csv", meta_log)
        hs6s_by_year = {y: sorted({code_digits(p)[:6] for p in selected_by_year.get(y, []) if len(code_digits(p)) >= 6}) for y in years}
        tariff_raw_dir = outdir / "wits_raw_json"
        tariff_raw_dir.mkdir(exist_ok=True)
        tariff_manifest = []
        tariff_rows = []
        partners = [WITS_MFN_PARTNER] + WITS_COMPETITORS
        partner_path = ";".join(partners)
        for year in range(max(args.start, 2012), min(args.end, 2023) + 1):
            hs6s = hs6s_by_year.get(year, [])
            for start in range(0, len(hs6s), 30):
                codes = hs6s[start:start+30]
                p_codes = ";".join(codes)
                url = WITS_URL.format(reporter=WITS_EU_REPORTER, partner=partner_path,
                                      product=p_codes, year=year)
                try:
                    doc, final_url, ctype = get_json(session, url, params=None, timeout=180, retries=3)
                    stem = f"wits_r918_multiPartner_{year}_batch{start//30+1}"
                    write_raw_response(outdir, stem, doc)
                    parsed = parse_wits_sdmx_json(doc)
                    for pr in parsed:
                        pr["requested_year"] = year
                        pr["requested_reporter"] = WITS_EU_REPORTER
                        pr["requested_partner_codes"] = partner_path
                        pr["source_url"] = final_url
                    tariff_rows.extend(parsed)
                    tariff_manifest.append({"year": year, "reporter": WITS_EU_REPORTER,
                                            "partner_codes": partner_path, "hs6_batch": p_codes,
                                            "url": final_url, "content_type": ctype,
                                            "status": "downloaded_raw_json"})
                except Exception as e:
                    tariff_manifest.append({"year": year, "reporter": WITS_EU_REPORTER,
                                            "partner_codes": partner_path, "hs6_batch": p_codes,
                                            "url": url, "status": "failed", "error": str(e)})
                time.sleep(max(args.pause, 0.5))
        write_csv(outdir / "wits_tariff_download_manifest.csv", tariff_manifest)
        write_csv(outdir / "wits_tariff_rates_long.csv", tariff_rows)
        # Match MFN partner 000 to origin-specific PREF records only when the
        # partner code matches directly. Group-code preferences require the
        # WITS partner-group membership metadata and are not silently assigned.
        mfn = {}
        pref = {}
        for tr in tariff_rows:
            product = str(tr.get("PRODUCTCODE", tr.get("PRODUCT", "")))
            partner = str(tr.get("PARTNER", ""))
            year = int(tr.get("TIME_PERIOD", tr.get("requested_year", 0)) or 0)
            rate = safe_float(tr.get("OBS_VALUE"))
            tariff_type = str(tr.get("TARIFFTYPE", "")).upper()
            if rate is None or not product:
                continue
            if partner == WITS_MFN_PARTNER and tariff_type == "MFN":
                mfn[(product, year)] = rate
            elif tariff_type == "PREF":
                pref[(product, partner, year)] = rate
        margin_rows = []
        for (product, partner, year), pref_rate in pref.items():
            mfn_rate = mfn.get((product, year))
            margin_rows.append({"hs6": product, "origin_or_partner_group_code": partner, "year": year,
                                "mfn_simple_average_pct": mfn_rate, "preferential_simple_average_pct": pref_rate,
                                "preference_margin_percentage_points": (mfn_rate-pref_rate if mfn_rate is not None else None),
                                "margin_status": "matched" if mfn_rate is not None else "no_mfn_match_check_classification_or_coverage",
                                "caveat": "HS6 simple-average only; partner groups require membership mapping; not CN8 exact line tariff"})
        write_csv(outdir / "wits_preference_margins_hs6.csv", margin_rows)

    # Product concentration across the complete Bangladesh CN8 reporting basket
    # for the latest year, before any CN8-to-HS6 concordance.
    latest_values = defaultdict(float)
    for r in bd_rows:
        if int(r["year"]) == latest_year:
            latest_values[r["product_raw_code"]] += r.get("value") or 0.0
    positive_latest = {k: v for k, v in latest_values.items() if v > 0}
    total_latest = sum(positive_latest.values())
    hhi_latest_cn8 = (sum((v / total_latest) ** 2 for v in positive_latest.values()) * 10000
                      if total_latest else None)
    sorted_latest = sorted(positive_latest.values(), reverse=True)
    cumulative = {}
    for n in (10, 50, 100, 200):
        cumulative[f"top_{n}_share_latest_cn8"] = (sum(sorted_latest[:n]) / total_latest if total_latest else None)

    # Quality control and summary.
    product_year_counts = defaultdict(int)
    for r in bd_rows:
        product_year_counts[(r["product_raw_code"], int(r["year"]))] += 1
    missing_selected = sum(1 for r in balanced if r["obs_status"] != "observed")
    qa = [
        {"metric":"BD_CNs_annual_observations", "value":len(bd_rows), "interpretation":"Non-null CN8 observations returned by Comext"},
        {"metric":f"BD_total_value_{latest_year}_EUR", "value":total_latest, "interpretation":"Sum of returned positive CN8 values; reconcile against Comext aggregate before analysis"},
        {"metric":f"HHI_full_returned_CN8_basket_{latest_year}", "value":hhi_latest_cn8, "interpretation":"HHI from all positive CN8 observations returned for Bangladesh in latest year; not harmonised across CN revisions"},
        *[{"metric":k, "value":v, "interpretation":"Cumulative share of sorted returned CN8 export/import lines in latest year"} for k,v in cumulative.items()],
        {"metric":"unique_CN8_codes", "value":len(set(r['product_raw_code'] for r in bd_rows)), "interpretation":"Raw Comext product dimension codes; preserve classification versions"},
        {"metric":"top_products_selected_union_all_years", "value":len(selected_union), "interpretation":"Union of year-specific top-N all-sector and S-11b CN8 codes; code identity is not assumed across years"},
        {"metric":"selected_product_year_cells", "value":len(balanced), "interpretation":"Year-specific selected CN8 product-year cells"},
        {"metric":"selected_product_year_not_returned", "value":missing_selected, "interpretation":"Not returned by API; do not infer true zero without checking status/coverage"},
        {"metric":"all_partner_trade_rows", "value":len(competitor_rows), "interpretation":"All partner-origin observations for selected product codes"},
        {"metric":"S11b_partner_chapter_rows", "value":len(s11b_rows), "interpretation":"HS chapter 61/62/63 totals by partner; join year-specific beneficiary list"},
        {"metric":"observed_year_count", "value":len(observed_years), "interpretation":f"Years with at least one returned CN8 observation; requested {args.start}-{args.end}"},
        {"metric":"latest_observed_year", "value":latest_year, "interpretation":"Latest year actually returned; not assumed equal to requested end year"},
        {"metric":"unmapped_cn8_year_keys_for_period_ranking", "value":len(unmapped), "interpretation":"Period ranking and YoY growth are blocked unless official concordance is complete"},
    ]
    write_csv(outdir / "data_quality_summary.csv", qa)
    manifest["run_finished_utc"] = datetime.now(timezone.utc).isoformat()
    manifest["output_directory"] = str(outdir)
    manifest["raw_comext_json_files"] = len(list((outdir/"raw_api").glob("comext_*.json"))) if (outdir/"raw_api").exists() else 0
    manifest["important_methodological_guards"] = [
        "No cross-year CN8 aggregation without complete sourced stable-product concordance.",
        "Competitor values and quantities are queried using year-specific CN8 product selections.",
        "Article 33 calculations require explicit year-level completeness attestation plus complete beneficiary trade coverage in all Chapters 61-63.",
        "2012-2025 Article 33 ratios are retrospective scenarios, not legal application of Regulation (EU) 2026/1395 before 2027.",
        "Non-returned partner/chapter/product cells are not imputed to zero."]
    (outdir / "run_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print("\nExtraction completed. Review data_quality_summary.csv, run_manifest.json, and raw_api/.")
    print(f"Output folder: {outdir}")

if __name__ == "__main__":
    main()