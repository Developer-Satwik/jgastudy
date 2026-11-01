from pathlib import Path
import json,hashlib,re
ROOT=Path(__file__).resolve().parents[1];DATE='2026-10-29'
def read(p):return json.loads((ROOT/p).read_text())
def write(p,d):(ROOT/p).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
def sha(p):return hashlib.sha256((ROOT/p).read_bytes()).hexdigest()
review='08-qa/R05-second-check-independent-review.md'
assert (ROOT/review).exists(),'Independent integrated review required before close'
assert 'Passed for internal desktop integration' in (ROOT/review).read_text(),'Explicit scoped pass required'
mp=read('08-qa/R05-second-check-record-map.json');cm=mp['claim_map'];model=read('03-report/R05-evidence-map.json')
assert len(cm)==21 and len(mp['source_map'])==12
bridge=read('08-qa/R05-prior-study-bridge-check.json');assert bridge['status']=='passed' and bridge['check_count']==327 and all(x['passed'] for x in bridge['checks'])
assert sha(bridge['bridge_path'])==bridge['bridge_sha256']
for x in read('08-qa/R05-second-check-baseline.json')['records']:assert sha(x['path'])==x['sha256'],x['path']
snapshots=read('03-report/research-notes/r05-second-check/before-review/manifest.json')['records']
for x in snapshots:assert sha(x['snapshot_path'])==x['sha256'],x['snapshot_path']
old=json.loads((ROOT/next(x['snapshot_path'] for x in snapshots if x['original_path']=='03-report/R05-evidence-map.json')).read_text())
for k in ['domains','financial_views','blank_evidence_template','template_fields','current_question_ids','reference_contexts']:
 assert model[k]==old[k],k
assert len(model['cross_cutting_conditions'])==5 and all(not c['mandatory'] and not c['scored'] for c in model['cross_cutting_conditions'])
for p in ['05-analysis/observations.json','05-analysis/charts.json','04-table/financial-inputs.json']:assert read(p)['records']==[]
assert read('01-method/question-map.json')==read('01-method/question-map-v0.2.json')
model['second_challenge_status']='completed_for_internal_desktop_synthesis';write('03-report/R05-evidence-map.json',model)
for f in ['03-report/R05-SECOND-CHECK-READOUT.md','03-report/modules/R05-business-case-evidence-and-risks.md']:
 p=ROOT/f;t=p.read_text().replace('Independent integrated review pending.','Independent integrated review passed for internal desktop synthesis.').replace('Integrated review is pending; no external sending.','Independent integrated review passed for internal desktop synthesis; no external sending.')
 if f.endswith('R05-SECOND-CHECK-READOUT.md'):
  t=t.split('\nVerification:')[0]+'\nVerification: [independent integrated review](../08-qa/R05-second-check-independent-review.md); [prior-study bridge check](../08-qa/R05-prior-study-bridge-check.md). These are bounded source/design and data-linkage checks, not employer fieldwork, financial assurance or final publication approval.\n'
 p.write_text(t)
findings=read('05-analysis/findings.json')
rows=[('FND-050','A business case needs a dated option and scope boundary, including its place within a wider programme.', ['R5H-C02','R5H-C03','R5H-C04','R5H-C05','R5C-C04'],'Historical public programme findings and adviser guidance are scoped context, not a market trend or retrospective proof that a prior decision was irrational.','Record version, material changes, component/wider boundary and next reconsideration point; no universal expiry or reapproval rule.'),
('FND-051','Aggregate value does not settle who bears the work or has funds to deliver it.',['R5H-C02','R5H-C04','R5H-C06'],'Public customer/centre and Synergy arrangements illustrate distribution, not a private-employer transfer mandate or evidence of conflict.','Where material identify cost/work/risk bearer, benefit recipient/timing and actual allocation/shortfall authority.'),
('FND-052','Service unit, retained work and commitment timing can alter a payroll option without changing its headline label.',['R5M-C01','R5M-C02','R5M-C03','R5M-C04','R5M-C05','R5M-C06','R5M-C07','R5M-C08','R5C-C05'],'Supplier declarations/terms are not customer quotes, enforceability advice, tested UI or whole-market rules. Version/quantity conflicts remain held; no amounts adopted.','Establish actual billable population/transaction, retained work, lifecycle obligation and handback. Separate fees, wage principal and any changed funding timing.'),
('FND-053','Existing paid hours and usable decision-critical expertise are different resource claims.',['R5R-C01','R5R-C02','R5H-C01'],'Educational cash examples and public retained-capability context do not prescribe staffing, a contribution formula or a payroll savings rate.','Clarify skill, usable window, extra cover and displaced work rather than infer peak readiness from annual hours or cash savings from salary allocations.'),
('FND-054','Benchmarks and elicited model advice must match the evidence claim they can support.',['R5C-C01','R5C-C02','R5C-C03','R5C-C05'],'Salary methods/populations and declared services differ. Prior C prompts ask for evidence, so repeated verification advice is not independent buyer-priority corroboration.','Retain edition/period/role/geography/pay basis/population and actual assignment evidence. Keep salary, resource, output, availability, funding and realised benefit separate; unaided cases first.')]
for ident,statement,candidates,limits,implication in rows:
 if any(x['finding_id']==ident for x in findings['records']):continue
 findings['records'].append(dict(finding_id=ident,topic_ids=['R05'],statement=statement,supporting_claim_ids=[cm[c] for c in candidates],contradicting_claim_ids=[],participant_observation_ids=[],interpretation=limits,decision_implication=implication,confidence_rationale='User-requested multi-lens primary-source challenge and independent integrated review; bounded qualitative design, not validation or commercial demand proof.',outstanding_questions=['Actual evidence, costs, timing, parties and effects in permissioned practitioner cases.'],publication_status='internal_research_design',reviewed_on=DATE))
findings['status']='R01_to_R05_internal_desktop_synthesis_with_R05_second_challenge';write('05-analysis/findings.json',findings)
changes=read('00-control/changes.json')
if not any(x['change_id']=='CHG-013' for x in changes['records']):
 changes['records'].append(dict(change_id='CHG-013',date=DATE,type='User-requested R05 second challenge',description='Historical, segmented service-market, all-six recruitment comparator/JGA, prior-study and usable-capacity checks. Twelve new primary routes, twenty-one bounded claim/method records and five internal findings. Five optional conditions supplement unchanged nine domains/three views/fourteen questions. Four constructed prompts and 32 saved answers independently linked; no buyer-priority inference. Independent integrated review and first-pass/prior-topic/client preservation passed. No employer forecast, numerical input, product trial, fieldwork or sending.'))
write('00-control/changes.json',changes)
wp=read('00-control/work-packages.json');wp['active_work_package']='WP08';wp['updated_on']=DATE
wp['next_action']='R05 second challenge complete. Next R06 desktop research: actual staying, switching, deferral, rejection and abandonment. Practitioner/final-use work remains open; no external sending without user permission.'
for x in wp['records']:
 if x['work_package_id']=='WP07':
  x.update(second_challenge_status='completed_for_internal_desktop_synthesis',second_challenge_started_on=DATE,second_challenge_completed_on=DATE,second_challenge_readout='03-report/R05-SECOND-CHECK-READOUT.md')
  addition=' Second challenge applied: dated whole-decision boundary, cost/benefit/funding distribution, actual service/unit/retained work/commitment cash, usable skill/time and evidence-fit conditions. Independent integrated review and 327 exact prior-study linkage checks passed; earlier/client/core artifacts preserved. No new original observations or numerical forecasts.'
  if addition not in x['evidence_of_completion']:x['evidence_of_completion']+=addition
write('00-control/work-packages.json',wp)
sources=read('02-evidence/registers/sources.json')['records'];claims=read('02-evidence/registers/claims.json')['records']
counts=f"The register contains {len(sources)} source routes and {len(claims)} claims or guardrails. They include different guidance, product declarations, cases and research populations, not equivalent independent surveys. {sum(bool(x.get('capture_path')) for x in sources)} source records have retained originals in their primary capture fields with checked hashes; additional reviewed captures/extracts are recorded separately. {len(findings['records'])} internal findings are recorded across R01–R05 and completed reviews."
p=ROOT/'00-control/CURRENT-STATUS.md';t=p.read_text();a=t.index('For current substantive findings, start with');b=t.index('\n\n## Main working conclusion',a)
t=t[:a]+'For current substantive findings, start with the [R05 second challenge](../03-report/R05-SECOND-CHECK-READOUT.md), [R05 first-pass readout](../03-report/R05-DESKTOP-READOUT.md) and [business-case checklist](../03-report/R05-BUSINESS-CASE-CHECKLIST.md), building on completed R02–R04. '+counts+' Current topic QA is `08-qa/R05-second-check-completion.json`; first-pass and prior-topic checks remain preserved. No source has final publication approval.'+t[b:]
bullet='- User-requested R05 second challenge completed: historical, market, all-six-comparator/JGA, prior-study and usable-capacity lenses. Five optional conditions supplement unchanged nine domains/three financial views/fourteen questions. Independent integrated review and 327 exact saved-data linkage checks passed; first-pass snapshots, prior topics and eight client files preserved. No numerical forecast or original fieldwork.\n'
if bullet not in t:t=t.replace('\nFor current substantive findings','\n'+bullet+'\nFor current substantive findings')
t=t.replace('R05 now separates cost/resource, incremental cash, affordability, benefit realisation, commercial scope and delivery evidence. Next is R06:', 'R05 and its second challenge now distinguish current scope/version, distribution, actual service/commitment, usable capacity and evidence-fit within cost/resource, cash, funding and delivery. Next is R06:')
p.write_text(t)
p=ROOT/'README.md';t=p.read_text();a=t.index('R01–R05 desktop work is complete');b=t.index('\n\n## Additional review',a)
t=t[:a]+'''R01–R05 desktop work and their targeted reviews are complete for the respective internal design/synthesis purposes. The [R05 second challenge](03-report/R05-SECOND-CHECK-READOUT.md) adds dated scope, distribution, service/unit/commitment, usable capacity and benchmark/evidence-fit conditions to the [business-case checklist](03-report/R05-BUSINESS-CASE-CHECKLIST.md). The nine optional domains and three financial views remain unscored; no employer forecast, rate or compulsory question has been introduced. Prior study prompts are constructed inputs, not buyer evidence. Next is R06: staying, switching, deferral, rejection and abandonment. Original practitioner integration and final publication checks remain open.

WP02 version 0.2 remains prepared for user review: [checkpoint notes and files](06-client-checkpoints/week-one-v0.2/REVIEW-NOTES.md). Earlier topic artifacts, first-pass R05 snapshots, eight client files and fourteen core questions are preserved. '''+counts+' Current R05 QA is `08-qa/R05-second-check-completion.json`; nothing has been sent.'+t[b:];p.write_text(t)
p=ROOT/'05-analysis/CONTRADICTIONS-AND-GAPS.md';t=p.read_text();marker='\n## R05 second challenge controls'
t=t.split(marker)[0]+'''
## R05 second challenge controls

- Record dated case/version, actual payroll component/wider decision, changed inputs and next reconsideration. Historical public audits are not a repeated employer cohort or payroll-market trend; no historical totals adopted. CLM-0323–0327, CLM-0340.
- Whole-case value differs from party funding: distinguish cost/work/risk bearer, benefit recipient/timing and actual allocation/shortfall authority. Do not invent conflict or transfers. CLM-0324, CLM-0326, CLM-0328.
- Licence/payroll/employee/payslip/payment units, retained work, actual contract version and commitment/use/handback timing are case-specific. Ordinary wage principal is not automatically additional transformation cost; changed funding timing can matter. No numerical tariff/funding model. CLM-0329–0336, CLM-0341.
- Retained Payfit 27 October 2026 label versus reader older version is unresolved chronology/applicability, not evidence of policy change. Declared AI controls not tested UI; Cintra hold unchanged. Modulr bundle quantity conflicts excluded from arithmetic. BrightPay/Moorepay earlier holds preserved.
- Usable skill/time/cover/displaced work are different from annual hours or salary allocations. No educational numbers/formula or compulsory hire. CLM-0342–0343.
- Hays live 2026/2025 inputs and RobertHalf live 2027 projected starting salaries retain separate methods/populations. No salary, loading factor, current availability or realised benefit inferred. Portfolio/Frazer reader notes are not retained raw originals. CLM-0337–0341.
- Four selected C prompts explicitly ask for evidence/verification and embed specified leadership/transition/temporary-cover assumptions.32 saved texts and exact linkage do not establish buyer demand/evidence priorities, cost, authority or supplier performance. No recommendation counts or generated tax rules transferred.
- Nine first-pass domains, three views, fourteen core questions and blank financial/observation arrays are unchanged. Five optional conditions add no required questions, fieldwork or final-use approval.
''';p.write_text(t)
client=[x for x in read('08-qa/R05-second-check-baseline.json')['records'] if x['path'].endswith(('.docx','.pdf'))]
for x in client:assert sha(x['path'])==x['sha256']
for x in read('08-qa/R05-second-check-captures.json')['files']:assert sha(x['path'])==x['sha256']
arts=['03-report/R05-SECOND-CHECK-READOUT.md','03-report/R05-DESKTOP-READOUT.md','03-report/R05-BUSINESS-CASE-CHECKLIST.md','03-report/R05-evidence-map.json','03-report/modules/R05-business-case-evidence-and-risks.md',review,'08-qa/R05-second-check-record-map.json','08-qa/R05-prior-study-bridge-check.json']
result=dict(date=DATE,status='passed_for_internal_R05_second_challenge',supersedes_for_current_synthesis='08-qa/R05-completion-check.json',new_source_routes=12,new_claim_or_guardrail_records=21,source_records=len(sources),claim_records=len(claims),source_records_with_primary_retained_original=sum(bool(x.get('capture_path')) for x in sources),internal_findings=len(findings['records']),evidence_domains=9,financial_views=3,selective_conditions=5,prior_bridge_checks_passed=327,selected_prior_questions=4,selected_saved_answer_texts=32,capture_files_hash_checked=len(read('08-qa/R05-second-check-captures.json')['files']),preserved_baseline_records=len(read('08-qa/R05-second-check-baseline.json')['records']),client_files=[dict(**x,unchanged=True) for x in client],first_pass_R05_snapshots=snapshots,fourteen_core_questions_unchanged=True,new_practitioner_observations=0,employer_forecasts=0,numerical_estimates=0,product_or_API_tests=0,external_actions=[],final_publication_approved=False,artifacts=[dict(path=f,sha256=sha(f)) for f in arts],next='R06 staying switching deferral rejection and abandonment; no external sending.')
write('08-qa/R05-second-check-completion.json',result)
print(json.dumps({k:v for k,v in result.items() if k not in ['client_files','first_pass_R05_snapshots','artifacts']},indent=2))
