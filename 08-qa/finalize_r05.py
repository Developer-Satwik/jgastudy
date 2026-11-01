from pathlib import Path
import hashlib, json

ROOT = Path(__file__).resolve().parents[1]
DATE = '2026-10-29'
def read(p): return json.loads(p.read_text())
def write(p,d): p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
assert (ROOT/'08-qa/R05-independent-review.md').exists(), 'Independent integrated review required.'
mapping=read(ROOT/'08-qa/R05-record-map.json')
assert len(mapping['source_map'])==10 and len(mapping['claim_map'])==28

fp=ROOT/'05-analysis/findings.json'; findings=read(fp)
rows=[
 ('FND-044','Whole-life resources, future incremental cash and funding affordability answer different questions.',
  ['CLM-0295','CLM-0296','CLM-0300','CLM-0302'],
  'Government social appraisal and educational financial principles are source-scoped; no private rate, horizon, tax treatment or employer forecast is prescribed.',
  'Define actual decision, perspective, realistic evolving counterfactual and feasible alternatives. Reconcile resource/cash/funding views; do not confuse historic accountability with forward cash.'),
 ('FND-045','Benefit type and realisation conditions matter as much as a headline saving.',
  ['CLM-0298','CLM-0299','CLM-0301','CLM-0302','CLM-0319','CLM-0320'],
  'Guidance is not an observed payroll saving. Time valued at salary is not automatic cash release; cost avoidance requires an evidenced counterfactual. No fabricated fines or causal attribution.',
  'Record baseline, benefit type/status, owner, dependencies, period and overlapping claims. Keep cash, capacity and nonmonetary outcomes distinct.'),
 ('FND-046','A public price structure does not establish a customer-specific quote or total relevant cost.',
  ['CLM-0303','CLM-0304','CLM-0305','CLM-0306','CLM-0307','CLM-0308'],
  'Selected supplier declarations, dated billing context and public sourcing design are not a negotiated rate, market average, guaranteed remedy, product trial or private procurement mandate.',
  'Establish service/unit/quantity and included or unknown work, promotion/renewal, transition/retained resources and exit obligations. Empty calculator zero and conditional credit are not free service or cash recovery.'),
 ('FND-047','Deliverability includes continuing payroll, usable skills and support as well as project milestones.',
  [f'CLM-{i:04}' for i in range(309,319)],
  'Supplier/government design and selected public cases do not prescribe universal gates, a parallel-run duration, staffing need or pay-error tolerance. Positive scoped evidence and dated limitations coexist.',
  'Link relevant scope, executed checks, practical learning, capacity, exceptions, ownership and support transition to the actual decision. Keep planned readiness, release and benefit separate.'),
 ('FND-048','Uncertainty and audit scope limit what a forecast or risk summary can establish.',
  ['CLM-0297','CLM-0300','CLM-0301','CLM-0302','CLM-0313','CLM-0314'],
  'A positive forecast metric is not funding or approval. NAO did not replicate or assure published business-case figures; its March report is not a later assessment of the April-published Synergy summary.',
  'Identify decision-changing assumptions, supported sensitivity, material unmonetised conditions and risk owners/mitigations/interactions. Preserve source assurance boundaries and unknowns.'),
 ('FND-049','Evidence should fit the benefit claim and operating context, with assessment planned before needed data disappears.',
  ['CLM-0299','CLM-0319','CLM-0320','CLM-0321','CLM-0322'],
  'Monitoring is not alone causal attribution; a selected pilot or demonstration is not generalised live performance or cash saving. Magenta/NIST guidance is not an employer impact evaluation or product certification.',
  'Track claim provenance/status, baseline/owner/period, deployment conditions and evidence actually requested/supplied/influential. For relevant AI tasks retain quality and review/correction work; no forced experiment or AI audit.')]
for ident,statement,claims,limits,implication in rows:
 if any(x['finding_id']==ident for x in findings['records']): continue
 findings['records'].append(dict(finding_id=ident,topic_ids=['R05'],statement=statement,supporting_claim_ids=claims,
  contradicting_claim_ids=[],participant_observation_ids=[],interpretation=limits,decision_implication=implication,
  confidence_rationale='Targeted primary guidance, supplier-declaration and bounded published-case review with independent integrated challenge. No original fieldwork, employer forecast or validated score.',
  outstanding_questions=['Actual requested/supplied evidence, costs, benefits, funding and delivery conditions in permissioned practitioner cases.'],publication_status='internal_research_design',reviewed_on=DATE))
findings['status']='R01_to_R05_internal_desktop_synthesis';write(fp,findings)

cp=ROOT/'00-control/changes.json'; changes=read(cp)
if not any(x['change_id']=='CHG-012' for x in changes['records']):
 changes['records'].append(dict(change_id='CHG-012',date=DATE,type='R05 business-case evidence and implementation-risk desktop research',description='Nine new canonical routes plus explicit reuses, twenty-eight bounded claim/method records and six internal findings. Nine optional evidence domains and three financial views, with no values/forecasts populated. Independent integrated review and preservation checks completed. Fourteen core questions, client files and earlier topic artifacts preserved. No external action, original fieldwork, financial workbook or product trial.'))
write(cp,changes)
wp_path=ROOT/'00-control/work-packages.json';wp=read(wp_path);wp['updated_on']=DATE;wp['active_work_package']='WP08'
wp['next_action']='R05 desktop work completed. Next R06: actual staying, switching, deferral, rejection and abandonment. Practitioner/final-use work remains open; no sending without user permission.'
for x in wp['records']:
 if x['work_package_id']=='WP07':
  x.update(status='completed_desktop_research_practitioner_integration_pending',desktop_completed_on=DATE,evidence_of_completion='Economics/benefit, commercial-cost, delivery/readiness and evidence-quality originals reconciled into nine-domain checklist and three-view structured map. Twenty-eight claim/method records, independent integrated review and prior-topic/client/core preservation. No employer forecast, populated financial inputs or fieldwork; practitioner integration/final-use checks remain open.')
write(wp_path,wp)
module=ROOT/'03-report/modules/R05-business-case-evidence-and-risks.md';t=module.read_text()
t=t.replace('Desktop synthesis prepared 29 October 2026. Independent integrated review and preservation gate pending.', 'Desktop research and independent integrated review completed 29 October 2026.')
t=t.replace('Complete independent integrated review and preservation checks before closing desktop work.', 'The [independent integrated review](../../08-qa/R05-independent-review.md) and preservation checks passed.')
module.write_text(t)
gaps=ROOT/'05-analysis/CONTRADICTIONS-AND-GAPS.md';t=gaps.read_text()
if '## R05 business-case controls' not in t:
 t+='''
## R05 business-case controls

- Resource/TCO, future incremental cash and funding profiles stay separate. Realistic BAU may evolve; comparison baseline is not automatically a feasible recommendation. No social/public rate, classroom hurdle or client tax treatment imported. CLM-0295–0302.
- Cash release, capacity and cost avoidance need different evidence. Valued time is not automatic budget reduction, overlapping claims are not additive and unknown cost is not zero. No invented fine probability or reputational amount. CLM-0298–0302.
- Supplier price declarations are not quotes, whole-life cost or market averages. Empty BrightPay zero is not free service; conflicting billing-period descriptions require actual plan confirmation. Moorepay credit is not assumed cash reimbursement and promotional saving is not accepted. CLM-0303–0308.
- Payfit pricing redirect/inaccessible managed-route material is not scope or price evidence. AQA worked-example arithmetic is excluded; definitions only. No numerical rates, prices or savings adopted.
- Plans, available training, executed results, accepted exceptions, usable live service and benefits are different. No compulsory parallel-run duration, pay-error threshold, full project team or automatic hire. CLM-0309–0318.
- NAO did not replicate/assure business-case figures; March2026 audit is not a later assessment of April-published Synergy summary. Scottish positives and practical limitations retain audited dates/scopes; SPCB underlying test work uninspected. CLM-0312–0317.
- Early measurement supports later assessment; monitoring alone does not isolate attribution. NIST context/limits/update notice retained; no AI certification, financial saving or forced experiment. CLM-0319–0322.
- Nine optional domains do not add required questions or a validated score. Original observation, chart and financial-input arrays remain empty; The Table workbook is a separate later package.
''';gaps.write_text(t)

sources=read(ROOT/'02-evidence/registers/sources.json')['records'];claims=read(ROOT/'02-evidence/registers/claims.json')['records']
counts=f"The register contains {len(sources)} source routes and {len(claims)} claims or guardrails. They include different guidance, product declarations, cases and research populations, not equivalent independent surveys. {sum(bool(x.get('capture_path')) for x in sources)} source records have retained originals in their primary capture fields with checked hashes; additional reviewed captures/extracts are recorded separately. {len(findings['records'])} internal findings are recorded across R01–R05 and completed reviews."
status=ROOT/'00-control/CURRENT-STATUS.md';t=status.read_text();a=t.index('For current substantive findings, start with');b=t.index('\n\n## Main working conclusion',a)
t=t[:a]+'For current substantive findings, start with the [R05 evidence readout](../03-report/R05-DESKTOP-READOUT.md) and [business-case checklist](../03-report/R05-BUSINESS-CASE-CHECKLIST.md), building on the [R04 second challenge](../03-report/R04-SECOND-CHECK-READOUT.md) and completed R02/R03 work. '+counts+' Current topic QA includes `08-qa/R05-completion-check.json` and the latest second-check completion records for R02–R04. Earlier checks remain historical; no source has final publication approval.'+t[b:]
bullet='- R05 desktop research completed on 29 October: economics/benefit, commercial cost, delivery/readiness and measurement evidence. Nine optional domains and three financial views passed integrated review; no prices, savings, forecasts, risk scores or financial inputs populated. Earlier topic artifacts, fourteen core questions and all eight client files preserved.\n'
if bullet not in t:t=t.replace('\nFor current substantive findings','\n'+bullet+'\nFor current substantive findings')
t=t.replace('Next is R05: business-case evidence, funding and implementation risks.', 'R05 now separates cost/resource, incremental cash, affordability, benefit realisation, commercial scope and delivery evidence. Next is R06: staying, switching, deferral, rejection and abandonment.')
t=t.replace('R02–R04 practitioner integration and final-use checks; R05–R08 report-topic research;', 'R02–R05 practitioner integration and final-use checks; R06–R08 report-topic research;')
t=t.replace('and begin R05 desktop research or necessary checkpoint revisions.', 'and begin R06 desktop research or necessary checkpoint revisions.')
status.write_text(t)
readme=ROOT/'README.md';t=readme.read_text();a=t.index('R01–R04 desktop work is complete');b=t.index('\n\n## Additional review',a)
t=t[:a]+'''R01–R05 desktop work is complete for the respective design/synthesis purposes. The [R05 evidence readout](03-report/R05-DESKTOP-READOUT.md) and [business-case checklist](03-report/R05-BUSINESS-CASE-CHECKLIST.md) separate whole-life resources, incremental cash and funding, then link benefits and delivery conditions to actual evidence. Nine optional domains and a blank evidence template add no compulsory questions, company forecast or validated score. The [R04 authority pathway](03-report/R04-DECISION-PATHWAY.md) and its completed second challenge remain unchanged. Next is R06: staying, switching, deferral, rejection and abandonment. Original practitioner integration and final publication checks remain open.

WP02 version 0.2 remains prepared for user review: [checkpoint notes and files](06-client-checkpoints/week-one-v0.2/REVIEW-NOTES.md). All eight client files, fourteen core questions and earlier topic artifacts are preserved. Collection arrangements and Nick's scope review remain open before fieldwork. '''+counts+' Current R05 QA is `08-qa/R05-completion-check.json`; no material has been sent.'+t[b:];readme.write_text(t)

baseline=read(ROOT/'08-qa/R05-baseline-manifest.json')['files']
for x in baseline:assert sha(ROOT/x['path'])==x['sha256']
client=[]
for v in ['0.1','0.2']:
 for x in read(ROOT/f'06-client-checkpoints/week-one-v{v}/checkpoint-manifest.json')['files']:
  assert sha(ROOT/x['path'])==x['sha256'];client.append(dict(path=x['path'],sha256=x['sha256'],unchanged=True))
q=read(ROOT/'01-method/question-map.json');assert q==read(ROOT/'01-method/question-map-v0.2.json') and len(q['records'])==14
model=read(ROOT/'03-report/R05-evidence-map.json');assert len(model['domains'])==9 and len(model['financial_views'])==3 and not model['employer_forecasts'] and not model['calculations'] and not model['participant_observations']
captures=read(ROOT/'08-qa/R05-captures.json')['files']
for x in captures:assert sha(ROOT/x['path'])==x['sha256']
for f in ['05-analysis/observations.json','05-analysis/charts.json','04-table/financial-inputs.json']:assert read(ROOT/f)['records']==[]
files=['03-report/R05-DESKTOP-READOUT.md','03-report/R05-BUSINESS-CASE-CHECKLIST.md','03-report/R05-evidence-map.json','03-report/modules/R05-business-case-evidence-and-risks.md','08-qa/R05-independent-review.md','08-qa/R05-record-map.json']
result=dict(date=DATE,status='passed_for_internal_R05_desktop_synthesis',new_source_routes=9,source_candidate_routes_including_reuse=10,new_claim_or_guardrail_records=28,source_records=len(sources),claim_records=len(claims),source_records_with_primary_retained_original=sum(bool(x.get('capture_path')) for x in sources),internal_findings=len(findings['records']),evidence_domains=9,financial_views=3,checked_capture_files=len(captures),prior_topic_and_core_hashes_preserved=len(baseline),client_files=client,fourteen_core_questions_unchanged=True,new_practitioner_observations=0,employer_forecasts=0,numerical_estimates=0,product_or_API_tests=0,external_actions=[],final_publication_approved=False,artifacts=[dict(path=f,sha256=sha(ROOT/f)) for f in files],next='R06 actual staying switching deferral rejection and abandonment; no sending without user permission.')
write(ROOT/'08-qa/R05-completion-check.json',result)
print(json.dumps({k:v for k,v in result.items() if k not in ['client_files','artifacts']},indent=2))
