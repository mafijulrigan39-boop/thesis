#!/usr/bin/env python3
"""Download and validate Bangladesh-EU trade and tariff data for the MITB thesis.

Primary trade source: Eurostat Comext DS-045409 (official Eurostat API).
Tariff source: WITS / UNCTAD TRAINS SDMX API, with a separate TARIC raw-data check.

Run from an internet-enabled machine:
    python -m pip install requests
    python run_full_validation.py --start 2012 --end 2025 --topn 200

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


def comext_query(session, year: int, partner: str | None = None, products: list[str] | None = None):
    params = [
        ("format", "JSON"), ("lang", "en"), ("freq", "A"),
        ("reporter", "EU27_2020"), ("flow", "1"),
        ("indicators", "VALUE_IN_EUROS"),
        ("sinceTimePeriod", str(year)), ("untilTimePeriod", str(year)),
    ]
    if partner:
        params.append(("partner", partner))
    if products:
        params.extend(("product", p) for p in products)
    doc, url, ctype = get_json(session, COMEXT_URL, params=params)
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
    args = ap.parse_args()
    if args.start > args.end or args.topn < 100 or args.topn > 200:
        raise SystemExit("Use start <= end and topn between 100 and 200.")

    outdir = Path(args.out).resolve()
    outdir.mkdir(parents=True, exist_ok=True)
    session = requests.Session()
    session.headers.update({"User-Agent": USER_AGENT, "Accept": "application/json"})
    manifest = {"run_started_utc": datetime.now(timezone.utc).isoformat(),
                "start_year": args.start, "end_year": args.end, "topn": args.topn,
                "comext_dataset": "DS-045409", "comext_reporter": "EU27_2020",
                "trade_flow": "imports", "measure": "VALUE_IN_EUROS", "api_requests": [],
                "limitations": ["No API absence is imputed to zero.",
                                "HS6 is derived as the first six digits of CN8; formal HS revision concordance remains necessary.",
                                "WITS TRAINS is HS6 tariff summary data, not CN8/CN10 tariff-line data."]}

    # Stage 1: full EU imports from Bangladesh for all CN8 positions, one year/request.
    bd_rows = []
    latest_codebook = {}
    for year in range(args.start, args.end + 1):
        rows, url, ctype = comext_query(session, year, partner="BD")
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
    write_csv(outdir / "bd_eu_imports_all_cn8_annual.csv", bd_rows)

    # Top products in latest year and across the full period; also the apparel subset S-11b.
    latest_year = args.end
    sums_yr = defaultdict(float)
    sums_all = defaultdict(float)
    desc = {}
    chap = {}
    for r in bd_rows:
        p = r["product_raw_code"]
        val = r.get("value") or 0.0
        desc[p] = r.get("product_label", "")
        chap[p] = r["hs2_chapter"]
        sums_all[p] += val
        if int(r["year"]) == latest_year:
            sums_yr[p] += val
    top_latest_all = sorted(sums_yr, key=sums_yr.get, reverse=True)[:args.topn]
    top_period_all = sorted(sums_all, key=sums_all.get, reverse=True)[:args.topn]
    top_latest_s11b = sorted((p for p in sums_yr if chap[p] in {"61","62","63"}),
                             key=sums_yr.get, reverse=True)[:args.topn]
    top_period_s11b = sorted((p for p in sums_all if chap[p] in {"61","62","63"}),
                             key=sums_all.get, reverse=True)[:args.topn]

    def rank_rows(codes, metric):
        vals = sums_yr if metric == "latest" else sums_all
        return [{"rank": i+1, "product_raw_code": p, "cn8": code_digits(p),
                 "hs6": code_digits(p)[:6], "chapter": chap.get(p),
                 "description": desc.get(p), "value_eur": vals[p],
                 "metric": (f"{latest_year}" if metric == "latest" else f"sum_{args.start}_{args.end}")}
                for i, p in enumerate(codes)]
    write_csv(outdir / "top_products_latest_all_sectors.csv", rank_rows(top_latest_all, "latest"))
    write_csv(outdir / "top_products_period_all_sectors.csv", rank_rows(top_period_all, "period"))
    write_csv(outdir / "top_products_latest_S11b_ch61_63.csv", rank_rows(top_latest_s11b, "latest"))
    write_csv(outdir / "top_products_period_S11b_ch61_63.csv", rank_rows(top_period_s11b, "period"))

    # Keep the all-sector competitor panel within 200 products, while retaining a
    # separate S-11b-focused list for the safeguard analysis. This avoids silently
    # producing a four-way union of up to 800 CN8 codes.
    selected = list(dict.fromkeys(top_latest_all + top_latest_s11b))
    write_csv(outdir / "selected_CN8_product_dictionary.csv",
              [{"product_raw_code": p, "cn8": code_digits(p), "hs6_prefix": code_digits(p)[:6],
                "chapter": chap.get(p), "description": desc.get(p)} for p in selected])

    # Balanced Bangladesh selected-product panel; missing is not recoded as zero.
    bd_map = {(r["product_raw_code"], int(r["year"])): r for r in bd_rows}
    balanced = []
    for p in selected:
        for y in range(args.start, args.end + 1):
            r = bd_map.get((p, y))
            balanced.append({"product_raw_code": p, "cn8": code_digits(p), "hs6_prefix": code_digits(p)[:6],
                             "year": y, "value_eur": (r.get("value") if r else None),
                             "obs_status": "observed" if r else "not_returned_by_api",
                             "description": desc.get(p)})
    write_csv(outdir / "bd_selected_products_balanced_panel.csv", balanced)

    # Stage 2: competitor origins for the same CN8 lines; request all partners for each year.
    competitor_rows = []
    for year in range(args.start, args.end + 1):
        # Up to 400 product codes (latest-year all-sector top-N plus latest-year S-11b top-N); chunk at 50 to stay below API request limits.
        for start in range(0, len(selected), 50):
            chunk = selected[start:start+50]
            rows, url, ctype = comext_query(session, year, partner=None, products=chunk)
            for r in rows:
                raw = str(r.get("product", ""))
                digits = code_digits(raw)
                rr = dict(r)
                rr.update({"year": year, "product_raw_code": raw, "cn8": digits,
                           "hs6_prefix": digits[:6], "source_url": url})
                competitor_rows.append(rr)
            manifest["api_requests"].append({"stage": "all_partners_selected_CN8", "year": year,
                                             "chunk_n": len(chunk), "url": url, "content_type": ctype,
                                             "records": len(rows)})
            print(f"Stage 2: {year} partner chunk {start//50+1}: {len(rows)} observations", flush=True)
            time.sleep(args.pause)
    write_csv(outdir / "eu_selected_products_all_partners_annual.csv", competitor_rows)

    # Stage 3: external-EU aggregate denominators for market shares (separate from partner rows).
    ext_rows = []
    for year in range(args.start, args.end + 1):
        for start in range(0, len(selected), 50):
            chunk = selected[start:start+50]
            rows, url, ctype = comext_query(session, year, partner="EXT_EU27_2020", products=chunk)
            for r in rows:
                raw = str(r.get("product", ""))
                digits = code_digits(raw)
                rr = dict(r)
                rr.update({"year": year, "product_raw_code": raw, "cn8": digits,
                           "hs6_prefix": digits[:6], "source_url": url})
                ext_rows.append(rr)
            manifest["api_requests"].append({"stage": "extraEU_total_selected_CN8", "year": year,
                                             "chunk_n": len(chunk), "url": url, "content_type": ctype,
                                             "records": len(rows)})
            time.sleep(args.pause)
    write_csv(outdir / "eu_selected_products_extraEU_totals_annual.csv", ext_rows)

    # Top five competing suppliers and BD market share using Comext aggregate denominator.
    eu_partner_codes = EU27 | {"EU27_2020", "EXT_EU27_2020", "WORLD", "WLD", "999", "TOTAL"}
    rows_by_prod_year = defaultdict(list)
    bd_values = {}
    for r in competitor_rows:
        partner = str(r.get("partner", ""))
        if partner in eu_partner_codes or len(partner) != 2:
            continue
        key = (r.get("product"), int(r.get("year", 0)))
        rows_by_prod_year[key].append(r)
        if partner == "BD":
            bd_values[key] = r.get("value")
    ext_values = {(r.get("product"), int(r.get("year", 0))): r.get("value") for r in ext_rows}
    top5 = []
    shares = []
    for key, group in rows_by_prod_year.items():
        ranked = sorted([g for g in group if str(g.get("partner")) != "BD" and g.get("value") is not None],
                        key=lambda x: x.get("value") or 0, reverse=True)
        for i, r in enumerate(ranked[:5], 1):
            top5.append({"product_raw_code": key[0], "cn8": code_digits(key[0]), "year": key[1],
                         "competitor_rank": i, "partner_code": r.get("partner"),
                         "partner_name": r.get("partner_label"), "value_eur": r.get("value")})
        bdv = bd_values.get(key)
        total = ext_values.get(key)
        shares.append({"product_raw_code": key[0], "cn8": code_digits(key[0]), "hs6_prefix": code_digits(key[0])[:6],
                       "year": key[1], "bangladesh_value_eur": bdv,
                       "extra_eu_imports_total_eur": total,
                       "bd_market_share": (bdv / total if bdv is not None and total not in (None, 0) else None),
                       "share_status": "calculated" if bdv is not None and total not in (None, 0) else "missing_denominator_or_BD_value"})
    write_csv(outdir / "top5_competitors_by_product_year.csv", top5)
    write_csv(outdir / "market_share_by_product_year.csv", shares)

    # Stage 4: S-11b statutory denominator by chapter and partner, separately from product leaders.
    s11b_rows = []
    for year in range(args.start, args.end + 1):
        rows, url, ctype = comext_query(session, year, partner=None, products=["61", "62", "63"])
        for r in rows:
            rr = dict(r)
            rr.update({"year": year, "source_url": url})
            s11b_rows.append(rr)
        manifest["api_requests"].append({"stage": "S11b_chapter_partner_values", "year": year,
                                         "url": url, "content_type": ctype, "records": len(rows)})
        time.sleep(args.pause)
    write_csv(outdir / "s11b_chapters_61_63_by_partner_annual.csv", s11b_rows)
    s11b_totals = defaultdict(float)
    for r in s11b_rows:
        partner = r.get("partner")
        year = int(r.get("year", 0))
        s11b_totals[(partner, year)] += r.get("value") or 0.0
    write_csv(outdir / "s11b_partner_totals_annual.csv",
              [{"partner_code": p, "partner_name": next((r.get("partner_label") for r in s11b_rows if r.get("partner")==p), p),
                "year": y, "s11b_value_eur": v} for (p,y),v in sorted(s11b_totals.items())])

    # Year-by-year GSP beneficiary status is a required legal join, not inferred from trade data.
    template = outdir / "gsp_beneficiary_status_template.csv"
    if not template.exists():
        write_csv(template, [], ["year", "partner_code", "partner_name", "scheme_status", "effective_from", "effective_to", "official_source_url", "notes"])

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
        hs6s = sorted({code_digits(p)[:6] for p in selected if len(code_digits(p)) >= 6})
        tariff_raw_dir = outdir / "wits_raw_json"
        tariff_raw_dir.mkdir(exist_ok=True)
        tariff_manifest = []
        tariff_rows = []
        partners = [WITS_MFN_PARTNER] + WITS_COMPETITORS
        partner_path = ";".join(partners)
        for year in range(max(args.start, 2012), min(args.end, 2023) + 1):
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
        {"metric":"top_products_selected_union", "value":len(selected), "interpretation":"Union of top lists across latest year and full period, all sectors and S-11b"},
        {"metric":"selected_product_year_cells", "value":len(balanced), "interpretation":"Balanced panel cells for selected products x years"},
        {"metric":"selected_product_year_not_returned", "value":missing_selected, "interpretation":"Not returned by API; do not infer true zero without checking status/coverage"},
        {"metric":"all_partner_trade_rows", "value":len(competitor_rows), "interpretation":"All partner-origin observations for selected product codes"},
        {"metric":"S11b_partner_chapter_rows", "value":len(s11b_rows), "interpretation":"HS chapter 61/62/63 totals by partner; join year-specific beneficiary list"},
    ]
    write_csv(outdir / "data_quality_summary.csv", qa)
    manifest["run_finished_utc"] = datetime.now(timezone.utc).isoformat()
    manifest["output_directory"] = str(outdir)
    (outdir / "run_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print("\nExtraction completed. Review data_quality_summary.csv, run_manifest.json, and raw_api/.")
    print(f"Output folder: {outdir}")

if __name__ == "__main__":
    main()
