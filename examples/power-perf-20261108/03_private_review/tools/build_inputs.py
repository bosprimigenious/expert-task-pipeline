"""Generate explicitly SYNTHETIC, internal-use power-performance review fixtures.
Not genuine corporate records. No historical task/score is reproduced.
Python 3.10+ standard library only. Public file export is deterministic.
"""
from pathlib import Path
from decimal import Decimal as D
import csv, json, calendar, hashlib

import argparse
_parser=argparse.ArgumentParser();_parser.add_argument('--output',default='public');ROOT=Path(_parser.parse_args().output)
PACKS=['A00_contract','A01_organization','A02_metering','A03_commercial','A04_incidents','A05_reviews','A06_delivery']
for p in PACKS:(ROOT/p).mkdir(parents=True,exist_ok=True)

def text(p,s):
    p=ROOT/p;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s.strip()+'\n',encoding='utf-8')
def js(p,o):text(p,json.dumps(o,ensure_ascii=False,indent=2))
def csvout(p,rows,fields=None):
    rows=list(rows); p=ROOT/p;p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields or list(rows[0]));w.writeheader();w.writerows(rows)

def num(x):return format(D(x),'f')

units=[('U1','县公司A','COUNTY'),('U2','县公司B','COUNTY'),('U3','营销部','FUNCTION'),('U4','设备部','FUNCTION'),('U5','变电运维中心','OPERATIONS'),('U6','信通公司','SUPPORT'),('U7','营销服务中心','SUPPORT'),('U8','晋陵实业（模拟）','SUBSIDIARY')]
csvout('A01_organization/units.csv',[dict(unit_id=u,name=n,unit_type=t,k3_applicable=str(u in ['U1','U2','U3','U8']).lower(),source_id='ORG-001') for u,n,t in units])
alias=[]
for u,n,_ in units:
    alias += [dict(alias=u,unit_id=u,valid_from='2025-01-01',valid_to='2026-12-31',source_id='ORG-ALIAS'),dict(alias=n,unit_id=u,valid_from='2025-01-01',valid_to='2026-12-31',source_id='ORG-ALIAS')]
alias += [dict(alias='运检中心',unit_id='U5',valid_from='2025-01-01',valid_to='2026-12-31',source_id='ORG-ALIAS'),dict(alias='县B',unit_id='U2',valid_from='2025-01-01',valid_to='2026-12-31',source_id='ORG-ALIAS')]
csvout('A01_organization/unit_aliases.csv',alias)
assign=[]
for i in range(1,25):
    fid=f'F{i:02d}';u='U1' if i<=12 else 'U2'
    assign.append(dict(assignment_id=f'O-{fid}-1',asset_id=fid,version=1,known_at='2026-01-05T09:00:00+08:00',valid_from='2025-01-01',valid_to='2025-12-31',operator_unit=u,device_unit='U4',source_id=f'ORG-{fid}'))
    if i in [17,18]:
        assign[-1]['valid_to']='2025-06-30'
        assign.append(dict(assignment_id=f'O-{fid}-2',asset_id=fid,version=1,known_at='2026-01-05T09:00:00+08:00',valid_from='2025-07-01',valid_to='2025-12-31',operator_unit='U1',device_unit='U4',source_id=f'HANDOVER-{fid}'))
        if i==18:
            # Same document key amended after first cutoff: transition actually August 1.
            assign.append({**assign[-2],'assignment_id':'O-F18-1','version':2,'known_at':'2026-01-23T10:00:00+08:00','valid_to':'2025-07-31','source_id':'HANDOVER-F18-CORR'})
            assign.append({**assign[-2],'assignment_id':'O-F18-2','version':2,'known_at':'2026-01-23T10:00:00+08:00','valid_from':'2025-08-01','valid_to':'2025-12-31','operator_unit':'U1','source_id':'HANDOVER-F18-CORR'})
for asset,op,dev in [('B01','U5','U4'),('B02','U5','U4'),('NET01','U6','U6')]:
    assign.append(dict(assignment_id='O-'+asset,asset_id=asset,version=1,known_at='2026-01-05T09:00:00+08:00',valid_from='2025-01-01',valid_to='2025-12-31',operator_unit=op,device_unit=dev,source_id='ORG-SPECIAL'))
csvout('A01_organization/assignments.csv',assign)
# Energy: business keys are feeder, period, measure; independent raw supply and sold values.
energy=[]
for i in range(1,25):
    for m in range(1,13):
        supply=D(4200000+i*23000+m*17000)
        rate=D('3.22')+D((i*7+m*3)%49)/100
        sold=supply*(1-rate/100)
        for measure,value in [('supply',supply),('sold',sold)]:
            unit='10k_kWh' if (i+m)%5==0 else 'kWh'
            v=value/10000 if unit=='10k_kWh' else value
            rid=f'M-{i:02d}-{m:02d}-{measure}-1'
            row=dict(record_id=rid,feeder_id=f'F{i:02d}',period=f'2025-{m:02d}',measure=measure,version=1,known_at='2026-01-06T10:00:00+08:00',status='POSTED',value=num(v),unit=unit,reason='ORIGINAL',source_id=f'METER-{i:02d}-{m:02d}')
            energy.append(row)
            if (i*12+m)%19==0:
                energy.append({**row,'record_id':rid+'-EXPORT2','version':99,'reason':'DUPLICATE_EXPORT','source_id':row['source_id']+'-COPY'})
            if measure=='sold' and (i+m)%11==0:
                corrected=value-D(2500+i*11)
                energy.append({**row,'record_id':rid[:-1]+'2','version':2,'known_at':'2026-01-21T11:00:00+08:00','value':num(corrected/10000 if unit=='10k_kWh' else corrected),'reason':'CORRECTION','source_id':f'CORR-{i:02d}-{m:02d}'})
# Cancel final record, later restore; never fall back while cancelled.
original=next(r for r in energy if r['record_id']=='M-24-12-sold-1')
energy.append({**original,'record_id':'M-24-12-sold-2','version':2,'known_at':'2026-01-20T10:00:00+08:00','status':'CANCELLED','reason':'RETRACT','source_id':'M24-RETRACT'})
energy.append({**original,'record_id':'M-24-12-sold-3','version':3,'known_at':'2026-02-02T10:00:00+08:00','value':num(D(original['value'])-D('1700')),'reason':'CORRECTION','source_id':'M24-RESTORE'})
# Future knowledge must not affect any requested snapshot.
original=next(r for r in energy if r['record_id']=='M-01-01-sold-1')
energy.append({**original,'record_id':'M-01-01-sold-9','version':9,'known_at':'2026-02-12T10:00:00+08:00','value':'0','reason':'LATER_REVISION','source_id':'FUTURE-OUT-OF-SCOPE'})
csvout('A02_metering/energy_records.csv',energy)
exposure=[]
for i in range(1,25):
    for m in range(1,13):
        exposure.append(dict(feeder_id=f'F{i:02d}',period=f'2025-{m:02d}',customers=2000+i*83+m*2,minutes=calendar.monthrange(2025,m)[1]*1440,source_id='EXP-'+str(i)+'-'+str(m)))
csvout('A02_metering/customer_exposure.csv',exposure)
outages=[]
for j in range(1,97):
    i=(j*5)%24+1;m=(j*7)%12+1
    outages.append(dict(record_id=f'R-OUT-{j:03d}',outage_id=f'OUT-{j:03d}',version=1,feeder_id=f'F{i:02d}',gas_not_used='NA',period=f'2025-{m:02d}',customer_minutes=180000+(j*3571)%150000,known_at='2026-01-06T10:00:00+08:00',status='POSTED',reason='ORIGINAL',source_id=f'DISPATCH-{j:03d}'))
    if j%13==0:outages.append({**outages[-1],'record_id':f'R-OUT-{j:03d}-COPY','reason':'DUPLICATE_EXPORT'})
# Remove unrelated terminology from the power dataset.
for r in outages:r.pop('gas_not_used')
csvout('A02_metering/outages.csv',outages)
# Commercial balances. Final balance revisions do not add to the original.
bills=[]
for u in ['U1','U2','U3','U8']:
    for m in range(1,13):
        for b in range(1,3):
            iid=f'INV-{u}-{m:02d}-{b}';due=D(1800000+int(u[1])*23000+m*13000+b*9000)
            paid=due*(D('0.991')+D((m+b+int(u[1]))%9)/2000)
            r=dict(record_id=iid+'-V1',invoice_id=iid,unit_alias='县B' if u=='U2' else u,service_month=f'2025-{m:02d}',version=1,known_at='2026-01-06T09:00:00+08:00',status='POSTED',due_yuan=num(due),paid_yuan=num(paid),reason='ORIGINAL',source_id='BILL-'+iid)
            bills.append(r)
            if m in [4,9] and b==2:
                bills.append({**r,'record_id':iid+'-V2','version':2,'known_at':'2026-01-22T11:00:00+08:00','paid_yuan':num(min(due,paid+13000)),'reason':'BANK_RECONCILIATION','source_id':'BANK-'+iid})
            if m%4==0 and b==1:bills.append({**r,'record_id':iid+'-EXPORT','version':8,'reason':'DUPLICATE_EXPORT'})
csvout('A03_commercial/receivables.csv',bills)
waivers=[]
for j,(u,m,amt,known,issuer,signed,scope) in enumerate([
('U1',3,11000,'2026-01-07','CITY_GOV','true','K3'),
('U2',9,17000,'2026-01-22','CITY_GOV','true','K3'),
('U3',6,9000,'2026-01-07','DEPT','true','K3'),
('U3',7,13000,'2026-01-07','CITY_GOV','false','K3'),
('U8',8,18000,'2026-01-22','CITY_GOV','true','K3'),
('U1',10,14000,'2026-01-07','CITY_GOV','true','K2'),
('U3',11,22000,'2026-02-03','CITY_GOV','true','K3'),
('U2',12,16000,'2026-02-12','CITY_GOV','true','K3')],1):
    waivers.append(dict(waiver_id=f'WV{j:02d}',invoice_id=f'INV-{u}-{m:02d}-1',target_unit=u,indicator=scope,amount_yuan=amt,issuer=issuer,signed=signed,status='APPROVED',known_at=known+'T09:00:00+08:00',effective_at=known+'T09:00:00+08:00',source_id=f'WAIVER-{j:02d}'))
csvout('A03_commercial/waivers.csv',waivers)
complaints=[]
for j in range(1,113):
    u='U'+str((j-1)%8+1);cid=f'CUS-{u}-{j:03d}';ev=f'SEV-{j:03d}';m=(j*5)%12+1
    for n,ch in enumerate(['95598','GOV','LOCAL'][:1+(j%3)]):
        r=dict(record_id=f'COMP-{j:03d}-{n}',ticket_id=f'TKT-{j:03d}-{n}',version=1,customer_id=cid,incident_key=ev,unit_id=u,period=f'2025-{m:02d}',channel=ch,substantiated='false' if j%9==0 else 'true',known_at='2026-01-07T11:00:00+08:00',status='POSTED',reason='ORIGINAL',source_id=f'COMPLAINT-{j:03d}')
        complaints.append(r)
        if j%17==0:complaints.append({**r,'record_id':r['record_id']+'-CP','reason':'DUPLICATE_EXPORT'})
# One latest-cancelled ticket whose other channel can still support the same complaint.
r=next(x for x in complaints if x['ticket_id']=='TKT-010-0');complaints.append({**r,'record_id':r['record_id']+'-V2','version':2,'status':'CANCELLED','known_at':'2026-01-20T10:00:00+08:00','source_id':'COMPLAINT-010-RETRACTION'})
csvout('A03_commercial/complaints.csv',complaints)
csvout('A03_commercial/customer_base.csv',[dict(unit_id=u,customers=45000+int(u[1])*4000,source_id='CUSTOMER-BASE') for u,_,_ in units])
# Incident evidence: textual case reports plus workflow documents, no final assessment labels.
cases=[
('C01','F03','2025-03-15','DEVICE','设备试验确认机构内部卡涩，操作记录符合规程。'),
('C02','F17','2025-09-12','OPERATION','倒闸前未执行复核；设备试验排除固有缺陷。'),
('C03','F18','2025-07-15','EQUAL','设备缺陷与现场操作失误共同成立，责任比例为各50%。'),
('C04','F07','2025-05-09','EXTERNAL','外力破坏；履责检查未发现内部失职。'),
('C05','NET01','2025-08-04','NETWORK','确认网络侵入与未修补漏洞之间的责任关系。'),
('C06','F11','2025-10-02','DEVICE','设备缺陷成立；初始材料只有调查草稿。'),
('C07','F19','2025-11-06','OPERATION','早期认为操作错误，后续原始时间戳表明外部原因。'),
('C08','B01','2025-12-07','OPERATION','运行记录存在矛盾；缺少法定验收回执，责任尚待确认。'),
('C09','F21','2025-06-12','EQUAL','设备和运行均有证据；后续更正只取消运行责任。'),
('C10','F12','2025-02-18','OPERATION','部门负责人出具意见；归口委员会随后审议。'),
('C11','B02','2025-12-11','OPERATION','运行失误已被确认，整改完成并不撤销历史责任。'),
('C12','F01','2025-04-28','DEVICE','初认设备缺陷；复核撤销原认定，确认非责任。')]
csvout('A04_incidents/case_index.csv',[dict(case_id=c,asset_id=a,event_date=d,initial_allegation=k,source_id='CASE-'+c,evidence_file='case_reports/'+c+'.md') for c,a,d,k,t in cases])
for c,a,d,k,t in cases:
    text(f'A04_incidents/case_reports/{c}.md',f'''# 事故材料 {c}（模拟业务证据）
source_id: CASE-{c}
known_at: 2026-01-08T09:00:00+08:00
对象：{a}。事件日：{d}。
事实摘要：{t}
本材料只证明调查中已记录的事实和待核验事项；它不替代正式裁决文书。直接设备责任与运行责任的单位，应按事件日有效、在审阅截点已可知的职责文书核对。不得按当前机构名称倒推。
关联工单：T-{c}-01、T-{c}-02；两张工单共享同一物理事故登记号，均属于本事故，不得重复计罚。其他事故登记号与本案不相同。
处理权限和生效条件见公开P-03；处分文字见decisions_initial.csv及后续复核包。
''')
decisions=[]
def dec(c,v,kind,classification,known,served,issuer='COMMITTEE',effective=None):
    decisions.append(dict(document_id=f'D-{c}-{v}',case_id=c,version=v,document_kind=kind,finding=classification,issuer=issuer,known_at=known+'T09:00:00+08:00',served_at=(served+'T09:00:00+08:00') if served else '',effective_at=(effective or known)+'T09:00:00+08:00',source_id=f'D-{c}-{v}'))
for c,_,_,k,_ in cases:
    if c in ['C06','C08']:dec(c,1,'DRAFT',k,'2026-01-08','')
    elif c=='C07':dec(c,1,'FINAL',k,'2026-01-08','2026-01-20')
    elif c=='C10':dec(c,1,'FINAL',k,'2026-01-08','2026-01-09','DEPARTMENT')
    else:dec(c,1,'FINAL',k,'2026-01-08','2026-01-09')
csvout('A04_incidents/decisions_initial.csv',decisions)
decisions=[]
dec('C06',2,'FINAL','DEVICE','2026-01-24','2026-01-25')
dec('C07',2,'REVOKED','EXTERNAL','2026-02-04','2026-02-05')
dec('C09',2,'FINAL','DEVICE','2026-01-23','2026-01-24')
dec('C10',2,'FINAL','OPERATION','2026-02-03','2026-02-04')
dec('C12',2,'REVOKED','EXTERNAL','2026-02-04','2026-02-05')
# Later document outside all requested review cutoffs.
dec('C08',2,'FINAL','OPERATION','2026-02-12','2026-02-13')
csvout('A05_reviews/decisions_updates.csv',decisions)
csvout('A05_reviews/appeals.csv',[
 dict(appeal_id='AP01',unit_id='U3',subject='K3_WAIVER',request='使用WV07调整应收口径',evidence_id='WV07',filed_at='2026-01-25T09:00:00+08:00',source_id='AP01'),
 dict(appeal_id='AP02',unit_id='U3',subject='K3_WAIVER',request='使用未签字WV04调整应收口径',evidence_id='WV04',filed_at='2026-01-10T09:00:00+08:00',source_id='AP02'),
 dict(appeal_id='AP03',unit_id='U7',subject='K4_SINGLE_CHANNEL',request='只保留95598渠道',evidence_id='LOCAL-NOTE',filed_at='2026-01-10T09:00:00+08:00',source_id='AP03'),
 dict(appeal_id='AP04',unit_id='U2',subject='REVOKE',request='撤销C07',evidence_id='C07',filed_at='2026-01-22T09:00:00+08:00',source_id='AP04'),
 dict(appeal_id='AP05',unit_id='U5',subject='REMEDIATION',request='C11整改已完成，请撤销扣分',evidence_id='C11-REMEDY',filed_at='2026-01-20T09:00:00+08:00',source_id='AP05'),
 dict(appeal_id='AP06',unit_id='U4',subject='REVOKE',request='撤销C12',evidence_id='C12',filed_at='2026-01-22T09:00:00+08:00',source_id='AP06')])
text('A05_reviews/remediation.md','''# C11整改验收摘录（模拟）
source_id: C11-REMEDY
known_at: 2026-01-18T09:00:00+08:00
C11的设备复归检查已完成，现场恢复运行。本记录不含责任撤销、减轻扣分或取消等级限制决定。P-03明确整改状态不自动改变历史责任。
# AP03部门说明（模拟）
source_id: LOCAL-NOTE
known_at: 2026-01-09T09:00:00+08:00
申请部门建议只统计95598渠道；未提供对P-02三渠道口径的正式修订或有效授权。
''')
actions=[('A1',2,'G1','',''),('A2',3,'G2|G3','A1','A4'),('A3',2,'G4','','A7'),('A4',6,'G1|G2|G3','','A2'),('A5',5,'G2|G4','',''),('A6',3,'G3','A1',''),('A7',3,'G1|G4','','A3'),('A8',5,'G2|G3|G4','','A2')]
csvout('A06_delivery/review_actions.csv',[dict(action_id=a,cost=c,covers=g,prerequisites=p,exclusive_with=x,description={'A1':'调取移交原件','A2':'联合验收与授权复核','A3':'复核投诉全渠道','A4':'外部联合取证包','A5':'验收与投诉联合核验','A6':'单项授权核验','A7':'移交与投诉合并复核','A8':'综合证据抽查'}[a]) for a,c,g,p,x in actions])
js('A06_delivery/review_plan_contract.json',{'required_gaps':['G1','G2','G3','G4'],'budget':10,'objective':'MIN_TOTAL_COST','gap_meanings':{'G1':'交接归口复核留档','G2':'C08缺验收材料的补证安排','G3':'豁免授权复核','G4':'全渠道投诉去重复核'},'note':'仅规划未来审核动作，不代表证据已获取；不得据此改变R2中仍未决的C08。成本单位为模拟审核资源点，不是元。可接受任意同成本最优解。'})
js('A00_contract/review_contract.json',{'task_id':'POWER-PERF-T2','version':'DEV-20261107-v1','data_origin':'SYNTHETIC_INTERNAL_RESEARCH','assessment_year':2025,'timezone':'Asia/Shanghai','snapshots':[{'snapshot':'R0','as_of':'2026-01-12T17:00:00+08:00'},{'snapshot':'R1','as_of':'2026-01-26T17:00:00+08:00'},{'snapshot':'R2','as_of':'2026-02-09T17:00:00+08:00'},{'snapshot':'RB','as_of':'2026-01-12T17:00:00+08:00'}],'delivery':'single_turn_all_seven_packages_visible','precision':{'kWh':'0.001','rates_percent':'0.000001','penalties':'0.000001','scores_display':'0.01'},'grade_thresholds':{'A':90,'B':80,'C':70,'D':0},'k1_rules':[{'start_month':1,'end_month':6,'threshold_percent':'3.42','step_pp':'0.02','points_per_step':'2','cap':'12'},{'start_month':7,'end_month':12,'threshold_percent':'3.45','step_pp':'0.02','points_per_step':'2','cap':'12'}],'k2':{'threshold_percent':'99.95','step_pp':'0.01','points_per_step':'2','cap':'6'},'k3':{'threshold_percent':'99.5','step_pp':'0.1','points_per_step':'1','cap':'6'},'k4':{'threshold_per_10000':'2','step':'0.5','points_per_step':'1','cap':'6'}})
# Draft assertions are intentionally unverified business proposals, not hidden tests.
csvout('A06_delivery/legacy_claims.csv',[
 dict(claim_id='L01',subject='版本',claim='只要版本号最大就选取，不必看known_at。',source_id='LEGACY-NOTE'),
 dict(claim_id='L02',subject='撤回',claim='最终记录CANCELLED时恢复上一条POSTED。',source_id='LEGACY-NOTE'),
 dict(claim_id='L03',subject='归口',claim='F18全年按当前接收单位U1核算。',source_id='LEGACY-NOTE'),
 dict(claim_id='L04',subject='线损',claim='年度线损率等于12个月百分比的算术平均。',source_id='LEGACY-NOTE'),
 dict(claim_id='L05',subject='投诉',claim='每个渠道的工单单独计一次投诉。',source_id='LEGACY-NOTE'),
 dict(claim_id='L06',subject='限级',claim='先把原始等级封顶C，再累计降级。',source_id='LEGACY-NOTE'),
 dict(claim_id='L07',subject='申诉',claim='申诉一经受理，原责任决定就不再执行。',source_id='LEGACY-NOTE'),
 dict(claim_id='L08',subject='补证',claim='提交补证计划后可视为C08证据齐备。',source_id='LEGACY-NOTE')])
# Data vocabulary and source directories remain public. No private expected outputs.
counts={}
for p in ROOT.rglob('*.csv'):
    with p.open(encoding='utf-8-sig') as f:counts[p.relative_to(ROOT).as_posix()]=sum(1 for _ in csv.DictReader(f))
js('A00_contract/input_counts.json',counts)
print(json.dumps(counts,ensure_ascii=False,indent=2))
