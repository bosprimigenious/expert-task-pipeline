"""Known-error acceptance tests for grader sensitivity. Not target-model experiments."""
from pathlib import Path
import argparse,csv,json,hashlib,tempfile,shutil
from grader import assess

def mutate_csv(root,file,predicate,field,value):
 p=root/file
 with p.open(encoding='utf-8-sig') as f:rs=list(csv.DictReader(f))
 matches=[r for r in rs if predicate(r)]
 if not matches:raise AssertionError('Mutation matched zero rows')
 matches[0][field]=value
 with p.open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rs[0]));w.writeheader();w.writerows(rs)
def manifest(root):
 rr=[]
 for p in sorted(root.rglob('*')):
  if p.is_file() and p.name!='manifest.json':
   d=p.read_bytes();rr.append(dict(path=p.relative_to(root).as_posix(),bytes=len(d),sha256=hashlib.sha256(d).hexdigest()))
 (root/'manifest.json').write_text(json.dumps({'schema_version':'1.0','files':rr},indent=2),encoding='utf-8')
def run(public,reference):
 public,reference=Path(public),Path(reference)
 mutations=[
 ('future_version','C01',lambda d:mutate_csv(d,'selected_records.csv',lambda r:r['snapshot']=='R0' and r['business_key']=='F01|2025-01|sold','record_id','M-01-01-sold-9')),
 ('cancelled_resurrection','C01',lambda d:mutate_csv(d,'selected_records.csv',lambda r:r['snapshot']=='R1' and r['business_key']=='F24|2025-12|sold','status','POSTED')),
 ('current_owner_for_history','C02',lambda d:mutate_csv(d,'organization_mapping.csv',lambda r:r['snapshot']=='R1' and r['asset_id']=='F18' and r['period']=='2025-07','operator_unit','U1')),
 ('wrong_k1','C03',lambda d:mutate_csv(d,'indicator_results.csv',lambda r:r['snapshot']=='R2' and r['unit_id']=='U1' and r['indicator']=='K1','rate','0')),
 ('wrong_k2','C04',lambda d:mutate_csv(d,'indicator_results.csv',lambda r:r['snapshot']=='R2' and r['unit_id']=='U1' and r['indicator']=='K2','penalty','0')),
 ('wrong_k3','C05',lambda d:mutate_csv(d,'indicator_results.csv',lambda r:r['snapshot']=='R2' and r['unit_id']=='U3' and r['indicator']=='K3','penalty','0')),
 ('wrong_complaint_dedup','C06',lambda d:mutate_csv(d,'indicator_results.csv',lambda r:r['snapshot']=='R2' and r['unit_id']=='U1' and r['indicator']=='K4','numerator','24')),
 ('draft_as_final','C09',lambda d:mutate_csv(d,'event_assessment.csv',lambda r:r['snapshot']=='R0' and r['case_id']=='C06','state','FINAL')),
 ('unsigned_waiver_supported','C10',lambda d:mutate_csv(d,'appeal_decisions.csv',lambda r:r['snapshot']=='R2' and r['appeal_id']=='AP02','outcome','SUPPORTED')),
 ('equal_share_four_four','C11',lambda d:mutate_csv(d,'event_assessment.csv',lambda r:r['snapshot']=='R2' and r['case_id']=='C03','operator_penalty','4')),
 ('hold_as_A','C13',lambda d:mutate_csv(d,'final_decisions.csv',lambda r:r['snapshot']=='R2' and r['unit_id']=='U5','final_grade','A')),
 ('rollback_contaminated','C14',lambda d:mutate_csv(d,'final_decisions.csv',lambda r:r['snapshot']=='RB' and r['unit_id']=='U1','provisional_score','99')),
 ('missing_workbook','C18',lambda d:(d/'Power_Performance_Review.xlsx').unlink()),
 ]
 logs=[]
 for name,c,mut in mutations:
  with tempfile.TemporaryDirectory(prefix='powerperf-mut-') as td:
   d=Path(td)/'submission';shutil.copytree(reference,d);mut(d);manifest(d);result=assess(d,reference,public)
   found=any(t['criterion_id']==c and not t['passed'] for t in result['tests'])
   logs.append(dict(test_id=name,expected_criterion=c,detected=found,failed_test_ids=[t['test_id'] for t in result['tests'] if not t['passed']],score_interval=result['score_interval'],final_score=result['final_score']))
 with tempfile.TemporaryDirectory(prefix='powerperf-empty-') as td:
  result=assess(td,reference,public);logs.append(dict(test_id='empty_submission_not_full_credit',detected=result['machine_checks_passed']==0 and result['final_score'] is None,passed_checks=result['machine_checks_passed']))
 return dict(status='PASS' if all(x['detected'] for x in logs) else 'FAIL',passed=sum(x['detected'] for x in logs),total=len(logs),tests=logs,note='Mutation detection is not independent validation of all ground truth and is not a Doubao score.')
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--public',required=True);p.add_argument('--reference',required=True);p.add_argument('--output',required=True);a=p.parse_args();r=run(a.public,a.reference);Path(a.output).write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8');print(r['status'],r['passed'],r['total']);raise SystemExit(0 if r['status']=='PASS' else 1)
