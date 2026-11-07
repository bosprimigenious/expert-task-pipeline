#!/usr/bin/env python3
"""Preflight then grade. Invalid schema is never sent to the grader."""
import argparse, json, subprocess, sys
from pathlib import Path
ap=argparse.ArgumentParser()
ap.add_argument('--submission',required=True); ap.add_argument('--public',required=True)
ap.add_argument('--reference',required=True); ap.add_argument('--output',required=True)
a=ap.parse_args()
here=Path(__file__).resolve().parent
pre=subprocess.run([sys.executable,str(here/'schema_preflight.py'),'--submission',a.submission,'--public',a.public],text=True,capture_output=True)
print(pre.stdout)
if pre.returncode!=0:
    Path(a.output).write_text(json.dumps({'status':'INVALID_SCHEMA','grader':'NOT_RUN'},ensure_ascii=False,indent=2),encoding='utf-8')
    sys.exit(2)
g=subprocess.run([sys.executable,str(here/'grader.py'),'--submission',a.submission,'--reference',a.reference,'--public',a.public,'--output',a.output],text=True,capture_output=True)
print(g.stdout); print(g.stderr,file=sys.stderr)
sys.exit(g.returncode)
