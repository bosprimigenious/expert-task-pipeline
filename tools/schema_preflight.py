#!/usr/bin/env python3
"""Schema preflight for POWER-PERF submissions.

Read-only. Does not execute solver code. Any hard finding means INVALID_SCHEMA;
do not run the grader on an invalid submission.
"""
import argparse, csv, json, sys, zipfile
from pathlib import Path

REQUIRED_CSV = [
 'selected_records.csv','exception_log.csv','organization_mapping.csv',
 'monthly_kpis.csv','indicator_results.csv','event_assessment.csv',
 'appeal_decisions.csv','final_decisions.csv','change_impact.csv',
 'legacy_audit.csv','evidence_index.csv']
REQUIRED_JSON = ['review_plan.json','self_check.json','manifest.json']
REQUIRED_MD = ['review_memo.md']
REQUIRED_XLSX = ['Power_Performance_Review.xlsx']

def load_schema(public):
    p=Path(public)/'A06_delivery'/'output_schema.json'
    return json.load(open(p,encoding='utf-8'))

def read_csv(path):
    with open(path,encoding='utf-8-sig',newline='') as f:
        r=csv.DictReader(f); return r.fieldnames or [], list(r)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--submission',required=True)
    ap.add_argument('--public',required=True)
    ap.add_argument('--output',default=None)
    a=ap.parse_args()
    sub=Path(a.submission); schema=load_schema(a.public)
    findings=[]; summary={}
    for fn in REQUIRED_CSV:
        p=sub/fn
        if not p.exists(): findings.append({'severity':'blocker','file':fn,'problem':'missing file'}); continue
        fields,rows=read_csv(p); summary[fn]={'rows':len(rows),'columns':len(fields)}
        spec=schema['files'].get(fn,{})
        for c in spec.get('columns',[]):
            if c not in fields: findings.append({'severity':'blocker','file':fn,'problem':f'missing column {c}'})
        keys=spec.get('key',[])
        if rows and all(k in fields for k in keys):
            seen=set()
            for i,r in enumerate(rows,2):
                k=tuple(r.get(x,'') for x in keys)
                if k in seen: findings.append({'severity':'blocker','file':fn,'line':i,'problem':f'duplicate key {k}'}); break
                seen.add(k)
        if 'snapshot' in fields:
            snaps=set(r.get('snapshot','') for r in rows)
            missing={'R0','R1','R2','RB'}-snaps
            if missing: findings.append({'severity':'blocker','file':fn,'problem':f'missing snapshots {sorted(missing)}'})
    # enum checks
    p=sub/'indicator_results.csv'
    if p.exists():
        _,rows=read_csv(p)
        bad=sorted({r.get('status','') for r in rows if r.get('status') not in ('DETERMINED','UNDETERMINED','NOT_APPLICABLE')})
        if bad: findings.append({'severity':'blocker','file':'indicator_results.csv','problem':f'invalid status enum {bad}; use DETERMINED/UNDETERMINED/NOT_APPLICABLE'})
    p=sub/'final_decisions.csv'
    if p.exists():
        _,rows=read_csv(p)
        bad=sorted({r.get('score_status','') for r in rows if r.get('score_status') not in ('FINAL','PROVISIONAL')})
        if bad: findings.append({'severity':'blocker','file':'final_decisions.csv','problem':f'invalid score_status enum {bad}'})
        numeric=['kpi_penalty','event_penalty','provisional_score','final_score','shift_count']
        for i,r in enumerate(rows,2):
            for c in numeric:
                v=(r.get(c) or '').strip()
                if v=='' or v.upper()=='HOLD': continue
                try: float(v)
                except Exception: findings.append({'severity':'blocker','file':'final_decisions.csv','line':i,'problem':f'non-numeric {c}={v!r}'})
    for fn in REQUIRED_JSON+REQUIRED_MD+REQUIRED_XLSX:
        if not (sub/fn).exists(): findings.append({'severity':'blocker','file':fn,'problem':'missing file'})
    # workbook sheets (optional openpyxl)
    xp=sub/'Power_Performance_Review.xlsx'
    if xp.exists():
        try:
            import openpyxl
            wb=openpyxl.load_workbook(xp,read_only=True,data_only=False)
            required=schema['workbook_interface']['required_sheets']
            for sn in required:
                if sn not in wb.sheetnames: findings.append({'severity':'blocker','file':xp.name,'problem':f'missing sheet {sn}'})
            wb.close()
        except Exception as e:
            findings.append({'severity':'warning','file':xp.name,'problem':f'workbook not checked: {e}'})
    result={'status':'PASS' if not findings else 'INVALID_SCHEMA','findings':findings,'summary':summary}
    if a.output:
        Path(a.output).write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(result,ensure_ascii=False,indent=2))
    return 0 if result['status']=='PASS' else 1

if __name__=='__main__':
    sys.exit(main())
