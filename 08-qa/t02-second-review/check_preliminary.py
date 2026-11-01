from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parents[2];B=R/'04-table/research-notes/t02-second-check';O=R/'08-qa/t02-second-review';checks=[]
def rd(p):return json.loads(p.read_text())
def ck(v,n):checks.append({'name':n,'passed':bool(v)});assert v,n
def hs(p):return hashlib.sha256(p.read_bytes()).hexdigest()
base=rd(R/'08-qa/T02-second-check-baseline.json')['files'];ck(len(base)==158,'158 protected baseline file records')
for x in base:ck(hs(R/x['path'])==x['sha256'],'baseline bytes '+x['path'])
for folder in ['history','market','competitors']:
 path=B/folder/'capture-manifest.json'
 for x in rd(path)['records']:
  for pk,hk in [('capture_path','capture_sha256'),('parsed_path','parsed_sha256'),('text_path','text_sha256')]:
   if x.get(pk):ck(hs(R/x[pk])==x[hk],f'{folder} retained file hash '+x[pk])
market=rd(B/'market/claim-candidates.json')['records'];ck([x['candidate_id']for x in market]==['TM2-C01','TM2-C02','TM2-C03'],'three bounded market design records')
for c in market:
 ck(c['value']is None and c['unit']is None and c['denominator']is None,'no market numerical outcome '+c['candidate_id'])
 ck(bool(c['limitations']) and bool(c['locator']),'locator and transfer limit '+c['candidate_id'])
 ck(c['evidence_class'].startswith('researcher_'),'offer refinement explicit researcher application '+c['candidate_id'])
for name,path in [('sources','02-evidence/registers/sources.json'),('claims','02-evidence/registers/claims.json'),('findings','05-analysis/findings.json')]:
 before=rd(B/'before-review'/path);current=rd(R/path)
 if name=='sources':ck(len(before['records'])==223,'before-source count223')
 if name=='claims':ck(len(before['records'])==432,'before-claim count432')
 if name=='findings':ck(len(before['records'])==81,'before-findings count81')
 ck(before['records']==current['records'],f'preliminary {name} unchanged before merge')
text=(B/'history/captures/TH2-S01.parsed.txt').read_text();ck('Revisions are updates' in text and 'correction of errors' in text and '9 August 2024'in text,'ONS distinction and date present in raw-derived text')
isg=(B/'market/captures/SRC-0227.parsed.txt').read_text();ck('context to the published study'in isg and 'On-Demand'in isg,'ISG published inquiry and separate On-Demand visible')
prop=rd(R/'04-table/T02-proposition-map.json');ck([x['proposition_id']for x in prop['propositions']]==['TP01','TP02','TP03'],'original three products')
ck(prop['report_free_to_practitioner_preserved']and prop['JGA_commissioned_IP_not_restricted_by_drafts']and not prop['signed_project_scope_changed'],'original free benefit/IP/scope boundary')
ck(prop['original_report_questions']==14 and prop['extra_mandatory_questions']==0 and not prop['fieldwork_activated'],'original14 and inactive fieldwork')
ck(prop['original_hypotheses']==['T02-H01','T02-H02','T02-H03','T02-H04'],'original four hypotheses')
for k in ['actual_buyer_validation','actual_member_validation','actual_offer_exposures','actual_rights_grants','financial_inputs','external_actions','prices']:ck(prop[k]==[],'original unperformed data empty '+k)
result=dict(status='passed_preliminary_T02_second_challenge_source_review_integration_pending',date='2026-10-30',check_count=len(checks),checks=checks,manual_review=['Market claims matched QQE fit/context/sample/ethics and ISG/iVentiv public sections; no buyer-value outcome assumed.','ONS error/revision policy is an analogy only; actual agreement section6 defect correction/remedy and written change rules remain governing.','ISG published-study inquiry boundary does not forbid relevant tailored interpretation.'],open_substantive_issues=[],integration_review_pending=True)
(O/'preliminary-checks.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n');print(json.dumps({k:v for k,v in result.items()if k!='checks'},indent=2))
