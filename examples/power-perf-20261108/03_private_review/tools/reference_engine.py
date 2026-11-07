"""Private executable reference for POWER-PERF-T2. Standard-library only.
The solver receives ONLY public fixture directories, never an answer fixture.
Usage: python reference_engine.py --input <unpacked seven packages> --output <dir>
"""
import argparse,csv,json,itertools,calendar
from pathlib import Path
from decimal import Decimal as D, ROUND_CEILING, ROUND_HALF_UP
from collections import defaultdict

ZERO=D(0);ONE=D(1);HUNDRED=D(100)
def read(root,path):
    with (root/path).open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def out(path,rows,fields=None):
    rows=list(rows)
    with path.open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields or list(rows[0]));w.writeheader();w.writerows([{k:fmt(v) for k,v in r.items()} for r in rows])
def fmt(x):
    if x is None:return ''
    if isinstance(x,D):return format(x,'f')
    if isinstance(x,bool):return str(x).lower()
    return x

def select(rows,key,cutoff,family,snap,selected,exceptions):
    groups=defaultdict(list)
    for r in rows:
        k='|'.join(r[x] for x in key)
        reason=None
        if r.get('reason')=='DUPLICATE_EXPORT':reason='DUPLICATE_EXPORT'
        elif r['known_at']>cutoff:reason='AFTER_CUTOFF'
        if reason:
            exceptions.append(dict(snapshot=snap,family=family,record_id=r['record_id'],business_key=k,reason=reason,source_id=r['source_id']));continue
        groups[k].append(r)
    ans={}
    for k,rs in groups.items():
        r=max(rs,key=lambda t:(int(t['version']),t['known_at'],t['record_id']))
        selected.append(dict(snapshot=snap,family=family,business_key=k,record_id=r['record_id'],status=r['status'],source_id=r['source_id']))
        for old in rs:
            if old is not r:exceptions.append(dict(snapshot=snap,family=family,record_id=old['record_id'],business_key=k,reason='SUPERSEDED',source_id=old['source_id']))
        if r['status']=='POSTED':ans[k]=r
        else:exceptions.append(dict(snapshot=snap,family=family,record_id=r['record_id'],business_key=k,reason='LATEST_CANCELLED',source_id=r['source_id']))
    return ans

def assignments_at(rows,cutoff):
    groups=defaultdict(list)
    for r in rows:
        if r['known_at']<=cutoff:groups[r['assignment_id']].append(r)
    return [max(v,key=lambda r:(int(r['version']),r['known_at'])) for v in groups.values()]
def owner(rows,asset,date):
    rs=[r for r in rows if r['asset_id']==asset and r['valid_from']<=date<=r['valid_to']]
    if len(rs)!=1:raise ValueError(f'Expected exactly one assignment: {asset}/{date}, found {len(rs)}')
    return rs[0]
def value(r):
    return D(r['value'])*(10000 if r['unit']=='10k_kWh' else 1)
def stepped(gap,step,mult,cap):return min(D(cap),max(ZERO,(gap/D(step)).to_integral_value(rounding=ROUND_CEILING))*D(mult))
def grade(score):return 'A' if score>=90 else 'B' if score>=80 else 'C' if score>=70 else 'D'
def valid_waiver(w,cutoff):return w['known_at']<=cutoff and w['effective_at']<=cutoff and w['issuer']=='CITY_GOV' and w['signed']=='true' and w['status']=='APPROVED' and w['indicator']=='K3'
def plan(root):
    acts=read(root,'A06_delivery/review_actions.csv');c=json.loads((root/'A06_delivery/review_plan_contract.json').read_text())
    solutions=[]
    for mask in range(1<<len(acts)):
        chosen=[a for i,a in enumerate(acts) if mask>>i&1];ids={a['action_id'] for a in chosen};cover=set();ok=True
        for a in chosen:
            cover.update(filter(None,a['covers'].split('|')))
            if not set(filter(None,a['prerequisites'].split('|')))<=ids:ok=False
            if set(filter(None,a['exclusive_with'].split('|')))&ids:ok=False
        cost=sum(int(a['cost']) for a in chosen)
        if ok and set(c['required_gaps'])<=cover and cost<=c['budget']:solutions.append((cost,sorted(ids)))
    if not solutions:raise ValueError('No feasible review plan')
    best=min(c for c,_ in solutions)
    return dict(status='PLAN_ONLY_NOT_EXECUTED',cost=best,actions=next(ids for c,ids in solutions if c==best),required_gaps=c['required_gaps'],objective=c['objective']),[ids for c,ids in solutions if c==best]

def solve(root,output):
    root=Path(root);output=Path(output);output.mkdir(parents=True,exist_ok=True)
    contract=json.loads((root/'A00_contract/review_contract.json').read_text())
    units=read(root,'A01_organization/units.csv');uid=[u['unit_id'] for u in units]
    asgn=read(root,'A01_organization/assignments.csv');aliases={r['alias']:r['unit_id'] for r in read(root,'A01_organization/unit_aliases.csv')}
    energy=read(root,'A02_metering/energy_records.csv');exposure=read(root,'A02_metering/customer_exposure.csv');outages=read(root,'A02_metering/outages.csv')
    bills=read(root,'A03_commercial/receivables.csv');waivers=read(root,'A03_commercial/waivers.csv');complaints=read(root,'A03_commercial/complaints.csv');base={r['unit_id']:D(r['customers']) for r in read(root,'A03_commercial/customer_base.csv')}
    cases=read(root,'A04_incidents/case_index.csv');docs=read(root,'A04_incidents/decisions_initial.csv')+read(root,'A05_reviews/decisions_updates.csv');appeals=read(root,'A05_reviews/appeals.csv')
    selected=[];exceptions=[];monthly=[];kpis=[];case_results=[];decisions=[];appeal_results=[];orgmap=[]
    for sc in contract['snapshots']:
        sn,cut=sc['snapshot'],sc['as_of'];aa=assignments_at(asgn,cut)
        er=select(energy,['feeder_id','period','measure'],cut,'ENERGY',sn,selected,exceptions)
        oo=select(outages,['outage_id'],cut,'OUTAGE',sn,selected,exceptions)
        br=select(bills,['invoice_id'],cut,'BILL',sn,selected,exceptions)
        cc=select(complaints,['ticket_id'],cut,'COMPLAINT',sn,selected,exceptions)
        # Monthly source aggregates are the audit boundary between selection and financial modelling.
        mo={};m1={};m2={};m3={};m4={}
        for u in uid:
            for m in range(1,13):mo[(u,m)]={'supply':ZERO,'sold':ZERO,'missing':0,'customer_minutes':ZERO,'exposure':ZERO,'due':ZERO,'paid':ZERO,'exempt':ZERO,'complaints':ZERO}
        for e in exposure:
            f,p=e['feeder_id'],e['period'];m=int(p[-2:]);a=owner(aa,f,p+'-01');u=a['operator_unit'];r=mo[(u,m)]
            orgmap.append(dict(snapshot=sn,asset_id=f,period=p,operator_unit=u,device_unit=a['device_unit'],source_id=a['source_id']))
            supply=er.get(f+'|'+p+'|supply');sold=er.get(f+'|'+p+'|sold')
            if supply:r['supply']+=value(supply)
            if sold:r['sold']+=value(sold)
            if not supply or not sold:r['missing']+=1
            r['exposure']+=D(e['customers'])*D(e['minutes'])
        for r in oo.values():
            a=owner(aa,r['feeder_id'],r['period']+'-01');mo[(a['operator_unit'],int(r['period'][-2:]))]['customer_minutes']+=D(r['customer_minutes'])
        for r in br.values():
            u=aliases[r['unit_alias']];m=int(r['service_month'][-2:]);a=mo[(u,m)];a['due']+=D(r['due_yuan']);a['paid']+=D(r['paid_yuan'])
            ws=[w for w in waivers if w['invoice_id']==r['invoice_id'] and w['target_unit']==u and valid_waiver(w,cut)]
            exempt=sum((D(w['amount_yuan']) for w in ws),ZERO)
            if exempt>D(r['due_yuan']):raise ValueError('Waiver exceeds due')
            a['exempt']+=exempt
        cg=defaultdict(list)
        for r in cc.values():
            if r['substantiated']=='true':cg[(r['customer_id'],r['incident_key'])].append(r)
        for key,rs in cg.items():
            # Public rule says same complaint's unit/month agree across channels; no implicit fuzzy merge.
            if len({(r['unit_id'],r['period']) for r in rs})!=1:raise ValueError('Conflicting complaint identity')
            r=rs[0];mo[(r['unit_id'],int(r['period'][-2:]))]['complaints']+=1
        for u in uid:
            for m in range(1,13):
                r=mo[(u,m)];period=f'2025-{m:02d}'
                for indicator,n,d,app,status in [
                    ('K1',r['supply']-r['sold'] if r['missing']==0 else None,r['supply'],r['exposure']>0,'UNDETERMINED' if r['missing'] else 'DETERMINED'),
                    ('K2',r['customer_minutes'],r['exposure'],r['exposure']>0,'DETERMINED'),
                    ('K3',r['paid'],r['due']-r['exempt'],u in ['U1','U2','U3','U8'],'DETERMINED'),
                    ('K4',r['complaints'],base[u],True,'DETERMINED')]:
                    if not app:continue
                    rate=None if n is None else (100*(1-n/d) if indicator=='K2' else (10000 if indicator=='K4' else 100)*n/d)
                    monthly.append(dict(snapshot=sn,unit_id=u,period=period,indicator=indicator,numerator=n,denominator=d,rate=rate,status=status,exemption_yuan=r['exempt'] if indicator=='K3' else ZERO,source_rule='P-02-'+indicator))
            applicable={'K1':sum(mo[(u,m)]['exposure'] for m in range(1,13))>0,'K2':sum(mo[(u,m)]['exposure'] for m in range(1,13))>0,'K3':u in ['U1','U2','U3','U8'],'K4':True}
            for k in ['K1','K2','K3','K4']:
                if not applicable[k]:
                    kpis.append(dict(snapshot=sn,unit_id=u,indicator=k,numerator=None,denominator=None,rate=None,penalty=ZERO,status='NOT_APPLICABLE',source_rule='P-02-'+k));continue
                a=[r for r in monthly if r['snapshot']==sn and r['unit_id']==u and r['indicator']==k]
                n=None if any(r['numerator'] is None for r in a) else sum((r['numerator'] for r in a),ZERO)
                den=sum((r['denominator'] for r in a),ZERO) if k!='K4' else base[u]
                rate=None if n is None else (100*(1-n/den) if k=='K2' else (10000 if k=='K4' else 100)*n/den)
                if n is None:penalty=None;status='UNDETERMINED'
                else:
                    status='DETERMINED'
                    if k=='K1':
                        penalty=ZERO
                        for rule in contract['k1_rules']:
                            sub=[r for r in a if rule['start_month']<=int(r['period'][-2:])<=rule['end_month']]
                            sd=sum((r['denominator'] for r in sub),ZERO);nn=sum((r['numerator'] for r in sub),ZERO)
                            if sd:penalty+=min(D(rule['cap']),max(ZERO,100*nn/sd-D(rule['threshold_percent']))/D(rule['step_pp'])*D(rule['points_per_step']))*sd/den
                    elif k=='K2':penalty=stepped(D('99.95')-rate,'.01','2','6')
                    elif k=='K3':penalty=stepped(D('99.5')-rate,'.1','1','6')
                    else:penalty=stepped(rate-D(2),'.5','1','6')
                kpis.append(dict(snapshot=sn,unit_id=u,indicator=k,numerator=n,denominator=den,rate=rate,penalty=penalty,status=status,source_rule='P-02-'+k))
        tot={u:dict(penalty=ZERO,shift=0,cap=1,pending=set()) for u in uid};cr={}
        for c in cases:
            a=owner(aa,c['asset_id'],c['event_date']);dev,op=a['device_unit'],a['operator_unit']
            eligible=[d for d in docs if d['case_id']==c['case_id'] and d['known_at']<=cut and d['effective_at']<=cut and d['served_at'] and d['served_at']<=cut and d['issuer']=='COMMITTEE' and d['document_kind'] in ['FINAL','REVOKED']]
            d=max(eligible,key=lambda x:(int(x['version']),x['known_at'],x['document_id'])) if eligible else None
            state='REVOKED' if d and d['document_kind']=='REVOKED' else 'FINAL' if d else 'PENDING'
            finding=d['finding'] if d else c['initial_allegation'];pd=po=ZERO;sd=so=0;cd=co=1;pending=[]
            if state=='PENDING':
                pending=[dev] if finding in ['DEVICE','NETWORK'] else [op] if finding=='OPERATION' else sorted(set([dev,op]))
                for u in pending:tot[u]['pending'].add(c['case_id'])
            elif state=='FINAL':
                if finding=='DEVICE':pd=D(8);cd=3
                elif finding=='OPERATION':po=D(10);co=3
                elif finding=='EQUAL':pd=D(4);po=D(5);sd=so=1
                elif finding=='NETWORK':pd=D(12);cd=4
            for u,p,s,cp in [(dev,pd,sd,cd),(op,po,so,co)]:tot[u]['penalty']+=p;tot[u]['shift']+=s;tot[u]['cap']=max(tot[u]['cap'],cp)
            row=dict(snapshot=sn,case_id=c['case_id'],asset_id=c['asset_id'],device_unit=dev,operator_unit=op,state=state,finding=finding,device_penalty=pd,operator_penalty=po,device_shift=sd,operator_shift=so,device_cap=cd,operator_cap=co,pending_units='|'.join(sorted(set(pending))),decision_doc=d['document_id'] if d else '',assignment_source=a['source_id'],source_rule='P-03')
            case_results.append(row);cr[c['case_id']]=row
        for u in uid:
            kk=[r for r in kpis if r['snapshot']==sn and r['unit_id']==u];pending=sorted(tot[u]['pending'])+[r['indicator'] for r in kk if r['status']=='UNDETERMINED']
            kp=sum((r['penalty'] for r in kk if r['penalty'] is not None),ZERO);score=max(ZERO,HUNDRED-kp-tot[u]['penalty']);raw=grade(score)
            final_rank=max(min(4,'ABCD'.index(raw)+1+tot[u]['shift']),tot[u]['cap']);fg='HOLD' if pending else 'ABCD'[final_rank-1]
            decisions.append(dict(snapshot=sn,unit_id=u,kpi_penalty=kp,event_penalty=tot[u]['penalty'],provisional_score=score,score_status='PROVISIONAL' if pending else 'FINAL',final_score=None if pending else score,raw_grade=raw,shift_count=tot[u]['shift'],grade_cap='ABCD'[tot[u]['cap']-1],final_grade=fg,rank=None,pending_items='|'.join(pending),source_rule='P-04'))
        elig=[r for r in decisions if r['snapshot']==sn and r['final_grade']!='HOLD']
        for r in elig:r['rank']=1+sum(1 for t in elig if ('ABCD'.index(t['final_grade']),-t['final_score'])<('ABCD'.index(r['final_grade']),-r['final_score']))
        for ap in appeals:
            if ap['filed_at']>cut:st='NOT_FILED';e=''
            elif ap['subject']=='K3_WAIVER':
                w=next(w for w in waivers if w['waiver_id']==ap['evidence_id']);st='PENDING' if w['known_at']>cut else 'SUPPORTED' if valid_waiver(w,cut) else 'REJECTED';e=w['source_id'] if w['known_at']<=cut else ''
            elif ap['subject'] in ['K4_SINGLE_CHANNEL','REMEDIATION']:st='REJECTED';e=ap['evidence_id']
            else:st='SUPPORTED' if cr[ap['evidence_id']]['state']=='REVOKED' else 'PENDING';e=cr[ap['evidence_id']]['decision_doc']
            appeal_results.append(dict(snapshot=sn,appeal_id=ap['appeal_id'],unit_id=ap['unit_id'],outcome=st,evidence_id=e,source_rule='P-05'))
    changes=[]
    for a,b in [('R0','R1'),('R1','R2')]:
        for u in uid:
            old=next(r for r in decisions if r['snapshot']==a and r['unit_id']==u);new=next(r for r in decisions if r['snapshot']==b and r['unit_id']==u)
            for field in ['kpi_penalty','event_penalty','provisional_score','score_status','final_score','raw_grade','shift_count','grade_cap','final_grade','rank','pending_items']:
                changes.append(dict(from_snapshot=a,to_snapshot=b,unit_id=u,field=field,before=fmt(old[field]),after=fmt(new[field]),changed=old[field]!=new[field]))
    for name,rows in [('selected_records.csv',selected),('exception_log.csv',exceptions),('organization_mapping.csv',orgmap),('monthly_kpis.csv',monthly),('indicator_results.csv',kpis),('event_assessment.csv',case_results),('appeal_decisions.csv',appeal_results),('final_decisions.csv',decisions),('change_impact.csv',changes)]:out(output/name,rows)
    pp,opts=plan(root);(output/'review_plan.json').write_text(json.dumps(pp,ensure_ascii=False,indent=2),encoding='utf-8')
    return {'decisions':decisions,'kpis':kpis,'monthly':monthly,'cases':case_results,'changes':changes,'optimal_plans':opts,'plan':pp,'selected':selected,'exceptions':exceptions}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--input',required=True);p.add_argument('--output',required=True);a=p.parse_args();result=solve(a.input,a.output)
    print(json.dumps({'status':'REFERENCE_COMPUTED_NOT_HUMAN_REVIEWED','decisions':[{k:fmt(v) for k,v in r.items()} for r in result['decisions'] if r['snapshot']=='R2'],'plan':result['plan']},ensure_ascii=False,indent=2))
