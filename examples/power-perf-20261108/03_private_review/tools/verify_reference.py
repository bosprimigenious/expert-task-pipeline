"""Independent SQL-window/Fraction verification. Does NOT import reference_engine.
Checks scope explicitly reported: record selection, four KPI families, key case transitions,
roles, final constraints, history replay and exhaustive planning.
Not a substitute for an independent human domain review.
"""
from pathlib import Path
from fractions import Fraction as F
from collections import defaultdict
import sqlite3,csv,json,argparse,math,itertools,time

def read(p):
 with p.open(encoding='utf-8-sig') as f:return list(csv.DictReader(f))
def main(pub,ref):
 p,r=Path(pub),Path(ref);checks=[]
 def ck(id,ok,detail=''):checks.append({'test_id':id,'passed':bool(ok),'detail':detail})
 def close(a,b,tol=F(1,1000000)):
  if a=='':return b is None
  return b is not None and abs(F(a)-b)<=tol
 families=[('ENERGY','A02_metering/energy_records.csv',['feeder_id','period','measure']),('BILL','A03_commercial/receivables.csv',['invoice_id']),('OUTAGE','A02_metering/outages.csv',['outage_id']),('COMPLAINT','A03_commercial/complaints.csv',['ticket_id'])]
 raw={f:read(p/path) for f,path,_ in families};conn=sqlite3.connect(':memory:')
 for fam,_,keys in families:
  cols=list(raw[fam][0]);conn.execute('CREATE TABLE '+fam+' ('+','.join('"'+x+'" TEXT' for x in cols)+')')
  conn.executemany('INSERT INTO '+fam+' VALUES ('+','.join('?' for _ in cols)+')',[[row[c] for c in cols] for row in raw[fam]])
 contract=json.loads((p/'A00_contract/review_contract.json').read_text());selected=read(r/'selected_records.csv');kpis=read(r/'indicator_results.csv');maps=read(p/'A01_organization/assignments.csv');exp=read(p/'A02_metering/customer_exposure.csv');waivers=read(p/'A03_commercial/waivers.csv');aliases={x['alias']:x['unit_id'] for x in read(p/'A01_organization/unit_aliases.csv')};base={x['unit_id']:F(x['customers']) for x in read(p/'A03_commercial/customer_base.csv')}
 def num(row):return F(row['value'])*(10000 if row['unit']=='10k_kWh' else 1)
 for sc in contract['snapshots']:
  sn,cut=sc['snapshot'],sc['as_of'];latest={}
  for fam,_,keys in families:
   query='SELECT record_id,status FROM (SELECT *,ROW_NUMBER() OVER(PARTITION BY '+','.join(keys)+' ORDER BY CAST(version AS INTEGER) DESC, known_at DESC, record_id DESC) AS rn FROM '+fam+" WHERE reason <> 'DUPLICATE_EXPORT' AND known_at <= ?) WHERE rn=1"
   got=set(conn.execute(query,(cut,)).fetchall());want={(x['record_id'],x['status']) for x in selected if x['snapshot']==sn and x['family']==fam};ck(f'SQL_{sn}_{fam}',got==want)
   ids={x[0] for x in got if x[1]=='POSTED'};latest[fam]=[x for x in raw[fam] if x['record_id'] in ids]
  versions={}
  for x in sorted(maps,key=lambda x:(int(x['version']),x['known_at'])):
   if x['known_at']<=cut:versions[x['assignment_id']]=x
  def own(asset,day):
   v=[x for x in versions.values() if x['asset_id']==asset and x['valid_from']<=day<=x['valid_to']];assert len(v)==1;return v[0]['operator_unit']
  ed={(x['feeder_id'],x['period'],x['measure']):num(x) for x in latest['ENERGY']}
  agg={u:{'sup':[F(0),F(0)],'loss':[F(0),F(0)],'missing':False,'exp':F(0),'out':F(0),'due':F(0),'paid':F(0),'complaints':0} for u in base}
  for x in exp:
   f,mo=x['feeder_id'],x['period'];u=own(f,mo+'-01');ix=0 if int(mo[-2:])<=6 else 1;a=agg[u];a['exp']+=F(x['customers'])*F(x['minutes'])
   if (f,mo,'supply') not in ed or (f,mo,'sold') not in ed:a['missing']=True
   if (f,mo,'supply') in ed:a['sup'][ix]+=ed[(f,mo,'supply')]
   if (f,mo,'supply') in ed and (f,mo,'sold') in ed:a['loss'][ix]+=ed[(f,mo,'supply')]-ed[(f,mo,'sold')]
  for x in latest['OUTAGE']:agg[own(x['feeder_id'],x['period']+'-01')]['out']+=F(x['customer_minutes'])
  for x in latest['BILL']:
   u=aliases[x['unit_alias']];a=agg[u];a['due']+=F(x['due_yuan']);a['paid']+=F(x['paid_yuan'])
   for w in waivers:
    if w['invoice_id']==x['invoice_id'] and w['target_unit']==u and w['indicator']=='K3' and w['issuer']=='CITY_GOV' and w['signed']=='true' and w['status']=='APPROVED' and w['known_at']<=cut and w['effective_at']<=cut:a['due']-=F(w['amount_yuan'])
  unique={(x['customer_id'],x['incident_key'],x['unit_id']) for x in latest['COMPLAINT'] if x['substantiated']=='true'}
  for _,_,u in unique:agg[u]['complaints']+=1
  for x in [x for x in kpis if x['snapshot']==sn]:
   u,k=x['unit_id'],x['indicator'];a=agg[u];n=d=rate=None;pen=F(0);status='DETERMINED'
   if k in ['K1','K2'] and a['exp']==0 or k=='K3' and u not in ['U1','U2','U3','U8']:status='NOT_APPLICABLE'
   elif k=='K1':
    d=sum(a['sup']);n=None if a['missing'] else sum(a['loss'])
    if n is None:pen=None;status='UNDETERMINED'
    else:
     rate=100*n/d
     pen=sum(min(F(12),max(F(0),100*ll/ss-th)/F('0.02')*2)*ss/d for ll,ss,th in zip(a['loss'],a['sup'],[F('3.42'),F('3.45')]) if ss)
   elif k=='K2':n=a['out'];d=a['exp'];rate=100*(1-n/d);pen=min(F(6),math.ceil(max(F(0),F('99.95')-rate)/F('.01'))*2)
   elif k=='K3':n=a['paid'];d=a['due'];rate=100*n/d;pen=min(F(6),math.ceil(max(F(0),F('99.5')-rate)/F('.1')))
   else:n=F(a['complaints']);d=base[u];rate=10000*n/d;pen=min(F(6),math.ceil(max(F(0),rate-2)/F('.5')))
   ck(f'FRACTION_{sn}_{u}_{k}',status==x['status'] and all(close(x[f],v) for f,v in [('numerator',n),('denominator',d),('rate',rate),('penalty',pen)]))
 # Explicit, separately written transition expectations. No import of the main solver.
 events=read(r/'event_assessment.csv');ix={(x['snapshot'],x['case_id']):x for x in events}
 pending={'R0':{'C06','C07','C08','C10'},'R1':{'C08','C10'},'R2':{'C08'},'RB':{'C06','C07','C08','C10'}}
 for sn in ['R0','R1','R2','RB']:
  ck('STATE_'+sn,{x['case_id'] for x in events if x['snapshot']==sn and x['state']=='PENDING'}==pending[sn])
  ck('C03_ROLE_'+sn,ix[(sn,'C03')]['operator_unit']==('U1' if sn in ['R0','RB'] else 'U2') and ix[(sn,'C03')]['device_unit']=='U4' and ix[(sn,'C03')]['operator_penalty']=='5' and ix[(sn,'C03')]['device_penalty']=='4')
 ck('REVOKED_R2',{x['case_id'] for x in events if x['snapshot']=='R2' and x['state']=='REVOKED'}=={'C07','C12'})
 fd=read(r/'final_decisions.csv');fin={x['unit_id']:x for x in fd if x['snapshot']=='R2'}
 ck('R2_EVENT_TOTALS',[F(fin['U'+str(i)]['event_penalty']) for i in range(1,9)]==list(map(F,[20,5,0,28,10,12,0,0])))
 ck('R2_PENDING_ONLY_U5',[x['unit_id'] for x in fin.values() if x['final_grade']=='HOLD']==['U5'] and fin['U5']['final_score']=='')
 for f in ['selected_records.csv','monthly_kpis.csv','indicator_results.csv','event_assessment.csv','final_decisions.csv','appeal_decisions.csv']:
  rr=read(r/f);normalize=lambda sn:sorted(json.dumps({k:v for k,v in x.items() if k!='snapshot'},sort_keys=True) for x in rr if x['snapshot']==sn)
  ck('REPLAY_'+f,normalize('R0')==normalize('RB'))
 # Exhaustive combinations by cardinality, independent from bitmask reference planner.
 acts=read(p/'A06_delivery/review_actions.csv');feasible=[]
 for n in range(len(acts)+1):
  for ch in itertools.combinations(acts,n):
   ids={x['action_id'] for x in ch};cover=set().union(*(set(x['covers'].split('|')) for x in ch)) if ch else set()
   valid=all(set(filter(None,x['prerequisites'].split('|')))<=ids and not(set(filter(None,x['exclusive_with'].split('|')))&ids) for x in ch);cost=sum(int(x['cost']) for x in ch)
   if valid and set(['G1','G2','G3','G4'])<=cover and cost<=10:feasible.append((cost,sorted(ids)))
 best=min(x[0] for x in feasible);opts=[x[1] for x in feasible if x[0]==best]
 ck('PLAN_OPTIMUM',best==7 and sorted(opts)==sorted([['A1','A2','A3'],['A1','A8']]))
 return {'status':'PASS' if all(x['passed'] for x in checks) else 'FAIL','passed':sum(x['passed'] for x in checks),'total':len(checks),'checks':checks,'optimal_plans':opts,'method':'SQL window + Fraction + separately encoded transition expectations + combinations enumeration','not_claimed':['independent human domain review','live Doubao self-test','platform acceptance','global proof of all narrative evidence semantics']}
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--public',required=True);ap.add_argument('--reference',required=True);ap.add_argument('--output',required=True);args=ap.parse_args();start=time.perf_counter();rr=main(args.public,args.reference);rr['elapsed_seconds']=time.perf_counter()-start;Path(args.output).write_text(json.dumps(rr,ensure_ascii=False,indent=2),encoding='utf-8');print(rr['status'],rr['passed'],rr['total']);raise SystemExit(0 if rr['status']=='PASS' else 1)
