from pathlib import Path
import hashlib,json,re,subprocess,sys

ROOT=Path(__file__).resolve().parents[1]
DATE='2026-10-29'
if (ROOT/'03-report/R03-SECOND-CHECK-READOUT.md').exists():
    raise SystemExit('Historical first-pass finalizer: R03 second challenge is now applied. Preserve the first-pass check; use the current second-check workflow.')
def read(p):return json.loads(p.read_text())
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')

review=ROOT/'08-qa/R03-independent-review.md'
assert review.exists(),'Independent integrated review required before completion.'
fp=ROOT/'05-analysis/findings.json';findings=read(fp)
rows=[
 ('FND-024','A configured connection and technical processing states do not demonstrate complete, authorised and reconciled payroll outcomes.',
  [f'CLM-{n:04}' for n in range(206,214)],
  'Primary product definitions and official guidance supply operating conditions, not comparative success rates or product tests.',
  'Assess the actual handoff, accepted/rejected records, identity/period, source ownership, timing, access, correction authority and downstream result.'),
 ('FND-025','Payroll execution, payment execution, authority and retained work must be mapped separately.',
  ['CLM-0214','CLM-0215','CLM-0216','CLM-0217','CLM-0219','CLM-0220','CLM-0221','CLM-0222'],
  'Official and supplier scope examples establish possible arrangements; they do not show actual service under a particular contract.',
  'Compare service components and actual entitlement, keep input/approval/oversight explicit, and test exception closure across boundaries.'),
 ('FND-026','Task mechanism, supplier availability, actual use and assessed benefit are distinct in automation and AI analysis.',
  [f'CLM-{n:04}' for n in range(229,235)],
  'Guidance and supplier configuration/release material do not establish cohort adoption, efficacy, uniform deployment or numerical savings.',
  'Define the task and permitted action, preserve established alternatives, verify scope and review burden, and assess results separately from deployment.'),
 ('FND-027','Controlled transition, continuity, useful outputs, support and demonstrated benefits can have different results and dates.',
  [f'CLM-{n:04}' for n in range(223,229)],
  'Two selected public employers; external audit, employer-reported internal assurance and management self-review have different strength and time scope.',
  'Retain positive and mixed evidence; state the assessed outcome, period and limits. Do not make go-live a proxy for every benefit or infer a vendor success rate.'),
 ('FND-028','Options can be combined and their suitability depends on the diagnosed gap, existing controls and practical prerequisites.',
  ['CLM-0215','CLM-0219','CLM-0220','CLM-0222','CLM-0229','CLM-0231'],
  'Analytical option map informed by primary conditions, not a tested ranking, lowest-cost rule or recommendation to retain an inadequate arrangement.',
  'Compare process/configuration, integration, assistance, platform, service and capability changes; preserve no-immediate-purchase where justified and carry unresolved material needs forward.')]
for ident,statement,support,limits,implication in rows:
    if any(r['finding_id']==ident for r in findings['records']):continue
    findings['records'].append({'finding_id':ident,'topic_ids':['R03'],'statement':statement,
      'supporting_claim_ids':support,'contradicting_claim_ids':[],'participant_observation_ids':[],
      'interpretation':limits,'decision_implication':implication,
      'confidence_rationale':'Bounded primary definitions, guidance and dated cases, with explicit alternatives and integrated review; no original fieldwork or evaluated products.',
      'outstanding_questions':['Actual task/context, stage, alternatives, retained work, result and materiality in permissioned practitioner cases.'],
      'publication_status':'internal_research_design','reviewed_on':DATE})
findings['status']='R01_R02_R03_internal_desktop_synthesis';write(fp,findings)

wp=ROOT/'00-control/work-packages.json';packages=read(wp)
packages.update(updated_on=DATE,active_work_package='WP06',next_action='Begin R04 desktop research on decision authority and pathways; no external sending.')
for r in packages['records']:
    if r['work_package_id']=='WP05':r.update(status='completed_desktop_research_practitioner_integration_pending',desktop_completed_on=DATE,evidence_of_completion='Primary integration/identity/state definitions, component-level delivery scope, task-level automation/AI and two bounded employer cases; eight-path analytical map, linked records, independent synthesis review and preservation checks. Original input/final publication checks remain open.')
    elif r['work_package_id']=='WP06':r['status']='ready_for_desktop_research'
write(wp,packages)
cp=ROOT/'00-control/changes.json';changes=read(cp)
if not any(r['change_id']=='CHG-008' for r in changes['records']):
    changes['records'].append({'change_id':'CHG-008','date':DATE,'type':'R03 desktop research completion','description':'Assessed integration, delivery components, task-level automation/AI and two employer implementation cases; reconciled seventeen new primary routes and twenty-nine contextual records, with eight combinable response paths and five internal findings. Preserved beta/UI/date/performance limits, client drafts, questionnaire and R02 outputs. No product/API trials or external actions.'})
write(cp,changes)
gaps=ROOT/'05-analysis/CONTRADICTIONS-AND-GAPS.md';text=gaps.read_text()
if '## R03 interpretation and freshness controls' not in text:
    text+='''
## R03 interpretation and freshness controls

- CLM-0218: dated Cintra pages differ on in-house calculation/status visibility. Hold universal UI behaviour; processing/payment separation is supported separately. No defect/resolution inference.
- CLM-0209–0210: async/import documentation includes beta access. Technical state definitions are not general availability or successful outcomes.
- Staffology retained body dates differ from cached web-reader headers. Retained live body controls metadata; no capability-change trend.
- CLM-0232–0234: supplier availability, development direction and expert/early-adopter savings wording are distinct from verified adoption or demonstrated payroll savings. No numerical benchmark adopted.
- CLM-0223–0228: two public employers, different implementations and evidence classes. Scottish Government retrospective events, management's publication-time assessment and future plans remain separate. No October2026 status or payroll-only ROI inferred.
- Public-sector sourcing/AI guidance is a transferable design lens, not a private-employer procurement or legal mandate. Historical service tiers are not current package rights.
'''
    gaps.write_text(text)

client=[]
for version in ['0.1','0.2']:
    for r in read(ROOT/f'06-client-checkpoints/week-one-v{version}/checkpoint-manifest.json')['files']:
        sha=hashlib.sha256((ROOT/r['path']).read_bytes()).hexdigest();assert sha==r['sha256']
        client.append({'path':r['path'],'sha256':sha,'unchanged':True})
for r in read(ROOT/'08-qa/R02-second-check-completion.json')['artifacts']:
    assert hashlib.sha256((ROOT/r['path']).read_bytes()).hexdigest()==r['sha256'],'Prior R02 artifact changed: '+r['path']
q=read(ROOT/'01-method/question-map.json');assert q==read(ROOT/'01-method/question-map-v0.2.json')
assert len(q['records'])==14 and not q['client_approved']
mapping=read(ROOT/'08-qa/R03-record-map.json')
assert len(mapping['source_map'])==17 and len(mapping['claim_map'])==29
sources=read(ROOT/'02-evidence/registers/sources.json')['records'];claims=read(ROOT/'02-evidence/registers/claims.json')['records']
files=['03-report/R03-DESKTOP-READOUT.md','03-report/R03-OPTIONS-AND-TRADEOFFS.md','03-report/R03-option-map.json','03-report/modules/R03-technology-and-operating-model-tradeoffs.md','08-qa/R03-independent-review.md','08-qa/R03-record-map.json','08-qa/R03-captures.json']
result={'date':DATE,'status':'passed_for_internal_R03_desktop_synthesis','new_source_routes':17,'new_claim_or_guardrail_records':29,
 'source_records':len(sources),'claim_records':len(claims),'source_records_with_retained_original':sum(bool(s.get('capture_path')) for s in sources),
 'internal_findings':len(findings['records']),'option_paths':8,'case_employers':2,
 'capture_log_files_hash_checked':len(read(ROOT/'08-qa/R03-captures.json')['files']),
 'client_files':client,'prior_R02_artifacts_unchanged':True,'fourteen_core_questions_unchanged':True,
 'artifacts':[{'path':f,'sha256':hashlib.sha256((ROOT/f).read_bytes()).hexdigest()} for f in files],
 'new_practitioner_observations':0,'product_or_API_tests':0,'final_publication_approved':False,'external_actions':[],
 'next':'R04 decision authority/pathways; original practitioner integration and final publication checks remain open.'}
write(ROOT/'08-qa/R03-completion-check.json',result)
print(json.dumps({k:v for k,v in result.items() if k not in ['artifacts','client_files']},indent=2))
