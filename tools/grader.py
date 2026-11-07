"""Independent submission comparator / consistency checks; does NOT execute solver code.
20 criteria x5 (candidate scheme 5/2/0). C01-C19 machine checks, C20 human review.
Confounded downstream failures are withheld for root-cause adjudication, not double-penalized.
Usage: python grader.py --submission DIR --reference DIR --public DIR --output report.json
"""
from pathlib import Path
from decimal import Decimal as D
import csv,json,zipfile,hashlib,argparse,re,xml.etree.ElementTree as ET
from collections import defaultdict
N={'m':'http://schemas.openxmlformats.org/spreadsheetml/2006/main','r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
CRITERIA=[
('C01','版本选择与撤回','各族先过滤known_at与重复，再选最终版本；撤回不回退'),
('C02','历史归口','按月初及当时可知职责重建馈线归口'),
('C03','K1双制度期核算','分子分母及区间加权扣分；缺失不补零'),
('C04','K2曝光与扣分','使用独立客户分钟分母与正确档位'),
('C05','K3账量和豁免','余额替代、授权范围及分母调整'),
('C06','K4全渠道去重','同客户同事件，保留独立客户投诉'),
('C07','事故身份覆盖','12个物理事故，不按工单重复'),
('C08','事故日双角色归口','设备与运行责任分开、追溯更正正确'),
('C09','权限送达与效力','只用有权且已知/生效/送达的正式文书'),
('C10','申诉裁决','六项按各截点分别判断，不把申请当撤销'),
('C11','角色处罚执行','按已裁定类型正确执行4/5等责任与限制'),
('C12','汇总分数勾稽','自身明细到总表正确汇总、暂计分不伪装正式分'),
('C13','等级未决与排名','先降级后封顶，HOLD排除，名次按等级/分数'),
('C14','历史回放不污染','RB与R0的选择、指标、事件和裁决一致'),
('C15','更新和不变集合','两相邻视图11字段全部比较，保持项不遗漏'),
('C16','旧稿审核','8项旧意见的结论、规则依据与定位'),
('C17','补证计划','覆盖、前置、互斥、预算和最优性'),
('C18','工作簿模型','可读、无危险特性、关键计算保留引用公式'),
('C19','交付一致性','表结构、总表值、引用覆盖、哈希清单一致'),
('C20','业务备忘录与证据审查','人工检查事实支持、变化解释、未决边界及完成声明')]
KEYS={'selected_records.csv':['snapshot','family','business_key'],'organization_mapping.csv':['snapshot','asset_id','period'],'indicator_results.csv':['snapshot','unit_id','indicator'],'event_assessment.csv':['snapshot','case_id'],'appeal_decisions.csv':['snapshot','appeal_id'],'final_decisions.csv':['snapshot','unit_id'],'monthly_kpis.csv':['snapshot','unit_id','period','indicator'],'change_impact.csv':['from_snapshot','to_snapshot','unit_id','field'],'exception_log.csv':['snapshot','family','record_id'],'legacy_audit.csv':['claim_id'],'evidence_index.csv':['snapshot','object_type','object_id']}
NUM={'numerator','denominator','rate','penalty','device_penalty','operator_penalty','device_shift','operator_shift','device_cap','operator_cap','kpi_penalty','event_penalty','provisional_score','final_score','shift_count','rank','exemption_yuan'}
def load(p):
 try:
  with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
 except (FileNotFoundError,UnicodeError,csv.Error):return []
def eq(a,b,field=''):
 if a is None:a=''
 if b is None:b=''
 if field in NUM:
  if a=='' or b=='':return a==b
  try:return abs(D(str(a))-D(str(b)))<=D('0.000001')
  except:return False
 if field=='pending_items' or field=='pending_units':return set(filter(None,str(a).split('|')))==set(filter(None,str(b).split('|')))
 return str(a).strip()==str(b).strip()
def compare(a,b,keys,fields=None):
 if not b:return not a
 if not a:return False
 try:
  aa={tuple(r[k] for k in keys):r for r in a};bb={tuple(r[k] for k in keys):r for r in b}
  if len(aa)!=len(a) or set(aa)!=set(bb):return False
  fields=fields or list(b[0])
  return all(all(eq(aa[k].get(f),bb[k].get(f),f) for f in fields) for k in bb)
 except (KeyError,ValueError):return False

def xlsx(p):
 with zipfile.ZipFile(p) as z:
  xml=ET.fromstring(z.read('xl/workbook.xml'));rels=ET.fromstring(z.read('xl/_rels/workbook.xml.rels'))
  rel={x.attrib['Id']:x.attrib['Target'] for x in rels}
  strings=[]
  if 'xl/sharedStrings.xml' in z.namelist():
   for si in ET.fromstring(z.read('xl/sharedStrings.xml')).findall('m:si',N):strings.append(''.join(t.text or '' for t in si.findall('.//m:t',N)))
  sheets={};hidden=[]
  for sh in xml.findall('m:sheets/m:sheet',N):
   name=sh.attrib['name'];target=rel[sh.attrib['{'+N['r']+'}id']];target=target.lstrip('/') if target.startswith('/') else 'xl/'+target
   if sh.attrib.get('state','visible')!='visible':hidden.append(name)
   cells={}
   for c in ET.fromstring(z.read(target)).findall('.//m:sheetData/m:row/m:c',N):
    t=c.attrib.get('t');v=c.find('m:v',N);fv=c.find('m:f',N);vv=v.text if v is not None else ''
    if t=='s' and vv!='':vv=strings[int(vv)]
    elif t=='inlineStr':vv=''.join(q.text or '' for q in c.findall('.//m:t',N))
    cells[c.attrib['r']]={'value':vv,'formula':fv.text if fv is not None else None,'type':t}
   sheets[name]=cells
  return {'sheets':sheets,'hidden':hidden,'names':z.namelist()}


def workbook_table(cells, fields):
 """Locate a public-schema header row; do not require fixed coordinates or column order."""
 grouped=defaultdict(dict)
 for address,cell in cells.items():
  m=re.fullmatch(r'([A-Z]+)([1-9][0-9]*)',address)
  if m:grouped[int(m[2])][m[1]]=cell
 for rn in sorted(grouped):
  names={str(v.get('value','')).strip():col for col,v in grouped[rn].items()}
  if not set(fields)<=set(names):continue
  result=[]
  for idx in sorted(k for k in grouped if k>rn):
   row={f:grouped[idx].get(names[f],{'value':'','formula':None}) for f in fields}
   if row.get('snapshot',{}).get('value') not in ['R0','R1','R2','RB']:continue
   if not row.get('unit_id',{}).get('value'):continue
   result.append(row)
  return result
 return []

def has_link_formula(cell):
 f=cell.get('formula') or ''
 return bool(f and (re.search(r'\$?[A-Z]{1,3}\$?\d+',f) or '[' in f))

def assess(sub,ref,public):
 sub,ref,public=Path(sub),Path(ref),Path(public)
 aa={f:load(sub/f) for f in KEYS};bb={f:load(ref/f) for f in KEYS};checks=[]
 def test(c,letter,desc,fn):
  try:ok=bool(fn());error=None
  except Exception as e:ok=False;error=type(e).__name__+': '+str(e)
  checks.append(dict(test_id=c+'-'+letter,criterion_id=c,description=desc,passed=ok,error=error))
 def rows(d,f,sn):return [r for r in d[f] if r.get('snapshot')==sn]
 for ix,fam in enumerate(['ENERGY','BILL','COMPLAINT','OUTAGE']):
  test('C01','abcd'[ix],fam+' selected identities and statuses',lambda fam=fam:compare([r for r in aa['selected_records.csv'] if r['family']==fam],[r for r in bb['selected_records.csv'] if r['family']==fam],KEYS['selected_records.csv'],['record_id','status']))
 for ix,sn in enumerate(['R0','R1','R2','RB']):
  letter='abcd'[ix]
  test('C02',letter,sn+' assignment mapping',lambda sn=sn:compare(rows(aa,'organization_mapping.csv',sn),rows(bb,'organization_mapping.csv',sn),KEYS['organization_mapping.csv'],['operator_unit','device_unit']))
  for c,k in [('C03','K1'),('C04','K2'),('C05','K3'),('C06','K4')]:
   test(c,letter,sn+' '+k+' values',lambda sn=sn,k=k:compare([r for r in rows(aa,'indicator_results.csv',sn) if r['indicator']==k],[r for r in rows(bb,'indicator_results.csv',sn) if r['indicator']==k],KEYS['indicator_results.csv'],['numerator','denominator','rate','penalty','status']))
  test('C07',letter,sn+' physical case identity',lambda sn=sn:compare(rows(aa,'event_assessment.csv',sn),rows(bb,'event_assessment.csv',sn),KEYS['event_assessment.csv'],['case_id','asset_id']))
  test('C08',letter,sn+' case-day roles',lambda sn=sn:compare(rows(aa,'event_assessment.csv',sn),rows(bb,'event_assessment.csv',sn),KEYS['event_assessment.csv'],['device_unit','operator_unit']))
  test('C09',letter,sn+' legal effectiveness within stipulated policy',lambda sn=sn:compare(rows(aa,'event_assessment.csv',sn),rows(bb,'event_assessment.csv',sn),KEYS['event_assessment.csv'],['state','finding','decision_doc','pending_units']))
  test('C10',letter,sn+' appeal outcomes',lambda sn=sn:compare(rows(aa,'appeal_decisions.csv',sn),rows(bb,'appeal_decisions.csv',sn),KEYS['appeal_decisions.csv'],['outcome']))
  def consequences(sn=sn):
   rr=rows(aa,'event_assessment.csv',sn)
   if len(rr)!=12:return False
   for r in rr:
    p={'DEVICE':(8,0,0,0,3,1),'OPERATION':(0,10,0,0,1,3),'EQUAL':(4,5,1,1,1,1),'EXTERNAL':(0,0,0,0,1,1),'NETWORK':(12,0,0,0,4,1)}.get(r['finding']) if r['state']=='FINAL' else (0,0,0,0,1,1)
    if p is None:return False
    fields=['device_penalty','operator_penalty','device_shift','operator_shift','device_cap','operator_cap']
    if not all(eq(r.get(f),v,f) for f,v in zip(fields,p)):return False
   return True
  test('C11',letter,sn+' follows submitted valid-classification arithmetic',consequences)
  def sums(sn=sn):
   rr=rows(aa,'final_decisions.csv',sn);kk=rows(aa,'indicator_results.csv',sn);ee=rows(aa,'event_assessment.csv',sn)
   if len(rr)!=8 or len(kk)!=32 or len(ee)!=12:return False
   for r in rr:
    u=r['unit_id'];kp=sum((D(t['penalty']) for t in kk if t['unit_id']==u and t['penalty']!=''),D(0));ep=sum((D(t['device_penalty']) for t in ee if t['device_unit']==u),D(0))+sum((D(t['operator_penalty']) for t in ee if t['operator_unit']==u),D(0))
    if not all(eq(r[f],v,f) for f,v in [('kpi_penalty',kp),('event_penalty',ep),('provisional_score',max(D(0),100-kp-ep))]):return False
   return True
  test('C12',letter,sn+' downstream self-consistency rather than duplicate truth penalty',sums)
  def grades(sn=sn):
   rr=rows(aa,'final_decisions.csv',sn);ee=rows(aa,'event_assessment.csv',sn);kk=rows(aa,'indicator_results.csv',sn)
   if len(rr)!=8 or len(ee)!=12 or len(kk)!=32:return False
   for r in rr:
    u=r['unit_id'];score=D(r['provisional_score']);raw='A' if score>=90 else 'B' if score>=80 else 'C' if score>=70 else 'D'
    shift=sum(int(t['device_shift']) for t in ee if t['device_unit']==u)+sum(int(t['operator_shift']) for t in ee if t['operator_unit']==u)
    cap=max([1]+[int(t['device_cap']) for t in ee if t['device_unit']==u]+[int(t['operator_cap']) for t in ee if t['operator_unit']==u])
    pending=any(u in t['pending_units'].split('|') for t in ee) or any(t['unit_id']==u and t['status']=='UNDETERMINED' for t in kk)
    fg='HOLD' if pending else 'ABCD'[max(min(4,'ABCD'.index(raw)+1+shift),cap)-1]
    if r['raw_grade']!=raw or not eq(r['shift_count'],shift,'shift_count') or r['grade_cap']!='ABCD'[cap-1] or r['final_grade']!=fg:return False
    if pending:
     if r['final_score']!='' or r['rank']!='' or r['score_status']!='PROVISIONAL':return False
    else:
     if not eq(r['final_score'],score,'final_score') or r['score_status']!='FINAL':return False
     rank=1+sum(1 for t in rr if t['final_grade']!='HOLD' and ('ABCD'.index(t['final_grade']),-D(t['final_score']))<('ABCD'.index(fg),-score))
     if not eq(r['rank'],rank,'rank'):return False
   return True
  test('C13',letter,sn+' grade/hold/rank applied to own evidence',grades)
 for letter,f in zip('abcd',['selected_records.csv','indicator_results.csv','event_assessment.csv','final_decisions.csv']):
  test('C14',letter,'RB replays R0: '+f,lambda f=f:bool(rows(aa,f,'R0')) and compare(rows(aa,f,'R0'),rows(bb,f,'R0'),KEYS[f],KEYS[f]) and compare([{**r,'snapshot':'R0'} for r in rows(aa,f,'RB')],rows(aa,f,'R0'),KEYS[f],[x for x in (bb[f][0] if bb[f] else []) if x not in ['source_rule','source_id','assignment_source']]))
 changes=aa['change_impact.csv'];fd={(r['snapshot'],r['unit_id']):r for r in aa['final_decisions.csv']}
 test('C15','a','Complete 176 change/invariance keys',lambda:compare(changes,bb['change_impact.csv'],KEYS['change_impact.csv'],KEYS['change_impact.csv']))
 for letter,side,snapfield in [('b','before','from_snapshot'),('c','after','to_snapshot')]:
  test('C15',letter,side+' matches submitted decision snapshot',lambda side=side,snapfield=snapfield:bool(changes) and all(eq(r[side],fd[(r[snapfield],r['unit_id'])][r['field']],r['field']) for r in changes))
 test('C15','d','Changed flags reflect semantic difference',lambda:bool(changes) and all(r['changed'].lower()==str(not eq(r['before'],r['after'],r['field'])).lower() for r in changes))
 for i in range(4):
  ids={f'L{2*i+1:02d}',f'L{2*i+2:02d}'}
  test('C16','abcd'[i],'Old-draft objections '+','.join(sorted(ids)),lambda ids=ids:len([r for r in aa['legacy_audit.csv'] if r['claim_id'] in ids])==2 and all(r['verdict']=='REJECTED' and r['policy_ids'] and r['reason'] and r['workbook_location'] for r in aa['legacy_audit.csv'] if r['claim_id'] in ids))
 try:plan=json.loads((sub/'review_plan.json').read_text(encoding='utf-8'));acts={r['action_id']:r for r in load(public/'A06_delivery/review_actions.csv')};ids=set(plan['actions']);act=[acts[i] for i in ids]
 except Exception:plan={};ids=set();act=[]
 def planvalid():return bool(act) and len(ids)==len(plan.get('actions',[])) and all(set(filter(None,a['prerequisites'].split('|')))<=ids and not (set(filter(None,a['exclusive_with'].split('|')))&ids) for a in act)
 test('C17','a','All four required gaps covered',lambda: set(['G1','G2','G3','G4'])<=set().union(*(set(a['covers'].split('|')) for a in act)))
 test('C17','b','Prerequisites, exclusions, no duplicate actions',planvalid)
 test('C17','c','True cost and budget',lambda: bool(act) and sum(int(a['cost']) for a in act)==plan['cost'] and plan['cost']<=10)
 test('C17','d','Minimum cost and plan-only boundary',lambda:planvalid() and plan['cost']==7 and plan['status']=='PLAN_ONLY_NOT_EXECUTED')
 try:book=xlsx(sub/'Power_Performance_Review.xlsx')
 except Exception:book={'sheets':{},'hidden':[],'names':[]}
 sheets=book['sheets'];required=['Review Summary','Monthly Inputs','Indicator Model','Case Decisions','Appeal Decisions','Change Log','Legacy Audit','Review Plan','Sources']
 test('C18','a','Readable workbook, required sheets',lambda:set(required)<=set(sheets))
 test('C18','b','No macros/external workbook links/hidden sheets',lambda:bool(sheets) and not book['hidden'] and not any('vbaproject' in n.lower() or 'externallinks' in n.lower() for n in book['names']))
 summary_fields=['snapshot','unit_id','kpi_penalty','event_penalty','provisional_score','score_status','final_score','raw_grade','shift_count','grade_cap','final_grade','rank','pending_items']
 summary_table=workbook_table(sheets.get('Review Summary',{}),summary_fields)
 indicator_fields=['snapshot','unit_id','indicator','numerator','denominator','rate','penalty','status']
 indicator_table=workbook_table(sheets.get('Indicator Model',{}),indicator_fields)
 def formulas():
  ss=[{k:v.get('value','') for k,v in row.items()} for row in summary_table]
  ii=[{k:v.get('value','') for k,v in row.items()} for row in indicator_table]
  if not compare(ss,aa['final_decisions.csv'],['snapshot','unit_id'],['snapshot','unit_id']) or len(ss)!=32:return False
  if not compare(ii,aa['indicator_results.csv'],['snapshot','unit_id','indicator'],['snapshot','unit_id','indicator']) or len(ii)!=128:return False
  for row in summary_table:
   required=['kpi_penalty','event_penalty','provisional_score','raw_grade']
   if row['score_status']['value']=='FINAL':required+=['final_score','final_grade','rank']
   if not all(has_link_formula(row[f]) for f in required):return False
  for row in indicator_table:
   if row['status']['value']=='DETERMINED' and not all(has_link_formula(row[f]) for f in ['numerator','denominator','rate','penalty']):return False
  return True
 test('C18','c','Schema-located summary and indicator linkage formulas (layout independent)',formulas)
 test('C18','d','Cached values present and free of Excel errors',lambda:bool(sheets) and len(summary_table)==32 and all(c['type']!='e' for sh in sheets.values() for c in sh.values()) and all(row['provisional_score'].get('value','') not in ['',None] for row in summary_table))
 try:schema=json.loads((public/'A06_delivery/output_schema.json').read_text())
 except:schema={'files':{}}
 def structures():
  if not schema['files']:return False
  for f,spec in schema['files'].items():
   rr=aa.get(f,load(sub/f))
   if not rr or not set(spec['columns'])<=set(rr[0]):return False
   keys=spec['key']
   if len({tuple(r[k] for k in keys) for r in rr})!=len(rr):return False
  return True
 test('C19','a','Required CSV schemas and unique keys',structures)
 def cross():
  rr=[{f:cell.get('value','') for f,cell in row.items()} for row in summary_table]
  return len(rr)==32 and compare(rr,aa['final_decisions.csv'],['snapshot','unit_id'],summary_fields)
 test('C19','b','Workbook summary equals submitted CSV',cross)
 test('C19','c','All unit/case decisions have traceable evidence entries',lambda:{(r['snapshot'],'UNIT',r['unit_id']) for r in aa['final_decisions.csv']}|{(r['snapshot'],'CASE',r['case_id']) for r in aa['event_assessment.csv']} <= {(r['snapshot'],r['object_type'],r['object_id']) for r in aa['evidence_index.csv'] if r['source_locator'] and r['policy_id'] and r['explanation']} and len(aa['evidence_index.csv'])>=80)
 def manifests():
  m=json.loads((sub/'manifest.json').read_text());actual={p.relative_to(sub).as_posix() for p in sub.rglob('*') if p.is_file() and p.name!='manifest.json'}
  rr=m['files'];listed={r['path'] for r in rr}
  if actual!=listed or len(listed)!=len(rr):return False
  for r in rr:
   p=(sub/r['path']).resolve()
   if not p.is_relative_to(sub.resolve()):return False
   data=p.read_bytes()
   if len(data)!=r['bytes'] or hashlib.sha256(data).hexdigest()!=r['sha256']:return False
  return True
 test('C19','d','Output manifest binds actual bytes without self-hash',manifests)
 results=[];by={c:[t for t in checks if t['criterion_id']==c] for c,_,_ in CRITERIA}
 dependencies={'C02':['C01'],'C03':['C01','C02'],'C04':['C01','C02'],'C05':['C01'],'C06':['C01'],'C08':['C02'],'C09':['C08'],'C10':['C05','C09']}
 failed={c for c,ts in by.items() if ts and not all(t['passed'] for t in ts)}
 lo=hi=0
 for c,name,desc in CRITERIA:
  ts=by[c];n=sum(t['passed'] for t in ts)
  if c=='C20':status='MANUAL_PENDING';score=None
  elif c in failed and any(x in failed for x in dependencies.get(c,[])):status='ROOT_CAUSE_REVIEW_REQUIRED';score=None
  else:status='MACHINE_CHECKED';score=5 if n==4 else 2 if n>=2 else 0
  if score is None:hi+=5
  else:lo+=score;hi+=score
  results.append(dict(criterion_id=c,name=name,description=desc,passed_tests=n,test_count=len(ts),status=status,provisional_points=score))
 return dict(task_id='POWER-PERF-T2',scoring_scheme='CANDIDATE_20x5_5_2_0',final_score=None,score_interval=[lo,hi],machine_checks_passed=sum(t['passed'] for t in checks),machine_checks_total=len(checks),criteria=results,tests=checks,manual_review_required=['C20 narrative/evidence/follow-through judgment']+[r['criterion_id']+' root-cause attribution' for r in results if r['status']=='ROOT_CAUSE_REVIEW_REQUIRED'],note='This is not a Doubao run. A final grade requires human review; follow-through checks use submitted upstream values. No arbitrary root-error multiplier.')

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--submission',required=True);p.add_argument('--reference',required=True);p.add_argument('--public',required=True);p.add_argument('--output',required=True);a=p.parse_args();r=assess(a.submission,a.reference,a.public);Path(a.output).write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps({k:r[k] for k in ['machine_checks_passed','machine_checks_total','score_interval','final_score']},ensure_ascii=False))
