#!/usr/bin/env python3
"""Create missing-safe derived trade and group data from the user's GitHub CSVs.

NO OFFICIAL CN CERTIFICATION IS IMPLIED. Original GitHub files are not mutated.
Input repo directory must contain cn8_validity_trade_panel.csv and
hcn8_group_year_trade.csv from the same pinned commit. This script does not
turn a missing record into an observed zero or certify connected-component
harmony as economic product comparability.

Usage:
 python create_missing_safe_harmonization.py --repo-dir /path/to/cn8_harmonization_2012_2025 --out /path/to/corrected
"""
import argparse, csv, json
from pathlib import Path
from collections import Counter, defaultdict


def read_records(path):
    with open(path, encoding='utf-8-sig', newline='') as f:
        yield from csv.DictReader(f)


def first_nonempty(row, *keys):
    for k in keys:
        if row.get(k) not in ('', None): return row[k]
    return ''


def run(folder: Path, out: Path):
    out.mkdir(parents=True, exist_ok=True)
    panel=folder/'cn8_validity_trade_panel.csv'
    groups=folder/'hcn8_group_year_trade.csv'
    if not panel.exists() or not groups.exists():
        raise FileNotFoundError('Both original GitHub derived CSVs must be available locally; no generated replacement is acceptable')
    orig = ['YEAR','PRODUCT','HCN8_ID','ACTIVITY_STATUS','OBS_VALUE_EUR']
    sums=defaultdict(int); observed=Counter(); status_count=Counter(); years=Counter()
    panel_output=out/'cn8_validity_trade_panel_MISSING_SAFE.csv'
    with panel.open(encoding='utf-8-sig',newline='') as fi, panel_output.open('w',encoding='utf-8',newline='') as fo:
        rd=csv.DictReader(fi)
        for col in orig:
            if col not in rd.fieldnames: raise ValueError(f'Panel missing required column {col}')
        fields=list(rd.fieldnames)+['ANALYSIS_STATUS','STRICT_OBSERVED_VALUE_EUR','ZERO_OBSERVED_IN_SOURCE','IMPUTED_ZERO_SENSITIVITY_EUR','ORIGINAL_STATUS_VERIFICATION_REQUIRED']
        wr=csv.DictWriter(fo,fieldnames=fields);wr.writeheader()
        unique_keys=set()
        for row in rd:
            year,code,group,src_status=row['YEAR'],row['PRODUCT'],row['HCN8_ID'],row['ACTIVITY_STATUS']
            key=(year,code)
            if key in unique_keys: raise AssertionError(f'Duplicate {key}')
            unique_keys.add(key)
            if len(code)!=8 or not code.isdigit(): raise ValueError(f'Unexpected CN8 product code {code}')
            if not year.isdigit() or not 2012<=int(year)<=2025:raise ValueError('unexpected year')
            years[year]+=1
            if src_status=='OBSERVED_TRADE':
                raw=row['OBS_VALUE_EUR']
                val=int(raw)
                if val<0:raise ValueError('Negative import value')
                analysis='OBSERVED_ZERO' if val==0 else 'OBSERVED_POSITIVE'
                strict=raw; sensitivity=raw; zero='1' if val==0 else '0'; original_status='SOURCE_REPORTED'
                sums[(year,group)]+=val;observed[(year,group)]+=1
            elif src_status=='VERIFIED_ZERO':
                # Existing GitHub label is insufficient to establish a source-reported zero.
                # The original value, typically zero, remains untouched for provenance.
                analysis='ACTIVE_BUT_NO_REPORTED_TRADE';strict='';sensitivity='0';zero='0';original_status='UNVERIFIED_ZERO_LABEL_NO_SOURCE_RECORD'
            elif src_status=='INACTIVE':
                analysis='INACTIVE_CODE';strict='';sensitivity='';zero='0';original_status='INACTIVE_BY_DERIVED_CLASSIFICATION'
            else: raise ValueError(f'Unrecognized status {src_status}')
            row.update(ANALYSIS_STATUS=analysis,STRICT_OBSERVED_VALUE_EUR=strict,
                       ZERO_OBSERVED_IN_SOURCE=zero,IMPUTED_ZERO_SENSITIVITY_EUR=sensitivity,
                       ORIGINAL_STATUS_VERIFICATION_REQUIRED=original_status)
            status_count[analysis]+=1
            wr.writerow(row)

    grow=[]; ever_chapters=defaultdict(set)
    year_chapters={}; year_group_rows=set()
    # Read all group records once to evaluate year-specific and longitudinal chapter mixing.
    for row in read_records(groups):
        key=(row['YEAR'],row['HCN8_ID'])
        if key in year_group_rows: raise AssertionError(f'Duplicate group-year {key}')
        year_group_rows.add(key)
        members=[x.strip() for x in first_nonempty(row,'ACTIVE_PRODUCTS').split('|') if x.strip()]
        this_ch={m[:2] for m in members if len(m)==8 and m.isdigit()}
        ever_chapters[row['HCN8_ID']]|=this_ch
        year_chapters[key]=this_ch
        grow.append(row)

    out_group=out/'hcn8_group_year_MISSING_SAFE_REVIEW.csv'
    review_rows=[]
    with out_group.open('w',newline='',encoding='utf-8') as fo:
        keys=['OBSERVED_MEMBERS_FROM_PANEL','UNREPORTED_ACTIVE_MEMBER_COUNT','STRICT_OBSERVED_SUBTOTAL_EUR',
              'FULL_GROUP_OBSERVED_VALUE_EUR_IF_COMPLETE','PROVISIONAL_COMPLETE_EXACT_VALUE_EUR',
              'CURRENT_YEAR_HS2_MIX','EVER_IN_HISTORY_HS2_MIX','EVER_SEEN_HS2_CHAPTERS',
              'UNVERIFIED_GROUP_COMPARABILITY','RESEARCH_LONGITUDINAL_STATUS']
        wr=csv.DictWriter(fo,fieldnames=list(grow[0].keys())+keys);wr.writeheader()
        for row in grow:
            key=(row['YEAR'],row['HCN8_ID'])
            n=int(row['ACTIVE_MEMBER_COUNT']); nobs=observed[key]; s=sums[key]
            if nobs!=int(row['OBSERVED_MEMBER_COUNT']):raise AssertionError(f'Observed membership differs at {key}')
            if s!=int(row['OBS_VALUE_EUR']):raise AssertionError(f'Observed sum differs at {key}')
            missing=n-nobs
            if missing<0:raise AssertionError('observed active members > active members')
            currentmix=len(year_chapters[key])>1
            evermix=len(ever_chapters[row['HCN8_ID']])>1
            typ=row.get('CONTINUITY_TYPE','')
            comparable=(typ=='1:1_exact' and not evermix)
            row.update(OBSERVED_MEMBERS_FROM_PANEL=nobs,UNREPORTED_ACTIVE_MEMBER_COUNT=missing,
                       STRICT_OBSERVED_SUBTOTAL_EUR=s,
                       FULL_GROUP_OBSERVED_VALUE_EUR_IF_COMPLETE=s if missing==0 else '',
                       PROVISIONAL_COMPLETE_EXACT_VALUE_EUR=s if missing==0 and comparable else '',
                       CURRENT_YEAR_HS2_MIX=int(currentmix), EVER_IN_HISTORY_HS2_MIX=int(evermix),
                       EVER_SEEN_HS2_CHAPTERS='|'.join(sorted(ever_chapters[row['HCN8_ID']])),
                       UNVERIFIED_GROUP_COMPARABILITY=int(not comparable),
                       RESEARCH_LONGITUDINAL_STATUS='REVIEW_OR_EXCLUDE' if not comparable else 'PROVISIONAL_EXACT_PENDING_OFFICIAL_SOURCE')
            wr.writerow(row)
            if str(row['YEAR'])=='2025' and (currentmix or evermix or typ!='1:1_exact'):
                review_rows.append({
                    'HCN8_ID':row['HCN8_ID'], 'CONTINUITY_TYPE':typ,
                    'ACTIVE_MEMBER_COUNT_2025':n,'OBSERVED_MEMBER_COUNT_2025':nobs,
                    'MISSING_ACTIVE_MEMBERS_2025':missing,
                    'OBSERVED_2025_EUR':s, 'CURRENT_YEAR_HS2_MIX':int(currentmix),
                    'EVER_HS2_MIX':int(evermix), 'EVER_SEEN_HS2':row['EVER_SEEN_HS2_CHAPTERS'],
                    'PUBLISH_LONGITUDINAL_GROWTH':'NO_SOURCE_VERIFICATION_REQUIRED'
                })

    report={
        'status':'DERIVED_MISSINGNESS_CORRECTION; NOT OFFICIAL_SOURCE_AUTHENTICATION',
        'source':str(folder), 'observed_trade_rows':status_count['OBSERVED_ZERO']+status_count['OBSERVED_POSITIVE'],
        'explicitly_observed_zeros':status_count['OBSERVED_ZERO'],
        'observed_positive':status_count['OBSERVED_POSITIVE'],
        'no_report_on_active_codes':status_count['ACTIVE_BUT_NO_REPORTED_TRADE'],
        'inactive_codes':status_count['INACTIVE_CODE'],
        'original_panel_rows':sum(status_count.values()),
        'observed_trade_total_eur':sum(sums.values()),
        'all_group_year_rows':len(grow),
        'groups_2025_requiring_review':len(review_rows),
        'cross_chapter_2025_current':sum(x['CURRENT_YEAR_HS2_MIX'] for x in review_rows),
        'cross_chapter_2025_ever_history':sum(x['EVER_HS2_MIX'] for x in review_rows),
        'year_panel_rows':dict(years),
        'important_note':'In group-year output, STRICT_OBSERVED_SUBTOTAL_EUR is not a complete-group estimate if UNREPORTED_ACTIVE_MEMBER_COUNT>0. PROVISIONAL complete values still require official source verification.'
    }
    with (out/'missingness_integrity_summary.json').open('w',encoding='utf-8') as f:json.dump(report,f,indent=2)
    with (out/'hcn8_2025_COMPLEX_GROUP_REVIEW_REGISTER.csv').open('w',newline='',encoding='utf-8') as f:
        wr=csv.DictWriter(f,fieldnames=list(review_rows[0].keys())) if review_rows else None
        if wr:wr.writeheader();wr.writerows(sorted(review_rows,key=lambda r:-r['OBSERVED_2025_EUR']))
    print(json.dumps({k:v for k,v in report.items() if k not in ('year_panel_rows','source','important_note')},indent=2))
    return report

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--repo-dir',type=Path,required=True);p.add_argument('--out',type=Path,required=True)
    x=p.parse_args();run(x.repo_dir,x.out)