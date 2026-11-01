from pathlib import Path
import hashlib, json

ROOT=Path(__file__).resolve().parents[1]
DATE='2026-10-29'
def read(p):return json.loads((ROOT/p).read_text())
def write(p,d):(ROOT/p).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
def sha(p):return hashlib.sha256((ROOT/p).read_bytes()).hexdigest()

review='08-qa/R07-independent-review.md'
assert (ROOT/review).is_file()
assert 'passed for internal desktop synthesis' in (ROOT/review).read_text().lower()
review_checks=read('08-qa/r07-review/integrated-review-checks.json')
assert review_checks['status']=='passed_for_internal_R07_desktop_synthesis'
assert all(x['passed'] for x in review_checks['checks'])
m=read('08-qa/R07-record-map.json');cs=m['claim_map']
assert len(m['source_map'])==4 and len(cs)==24
baseline=read('08-qa/R07-baseline-manifest.json')['files']
assert len(baseline)==54
for x in baseline:assert sha(x['path'])==x['sha256'],x['path']
captures=read('08-qa/R07-captures.json')['files']
for x in captures:assert sha(x['path'])==x['sha256'],x['path']
assert next(x for x in captures if x['path'].endswith('/MP-feature.png'))['kind']=='published_chart_asset'
q=read('01-method/question-map.json');assert len(q['records'])==14 and q==read('01-method/question-map-v0.2.json')
for p in ['05-analysis/observations.json','05-analysis/charts.json','04-table/financial-inputs.json']:assert read(p)['records']==[]
model=read('03-report/R07-priority-map.json')
for k in ['participant_observations','completed_case_comparisons','forecast_calculations','subgroup_estimates','market_rankings']:assert model[k]==[]
for k in ['blank_priority_template','blank_context_template','blank_comparison_template']:assert all(v is None for v in model[k].values())
assert model['maximum_selective_priorities']==2 and model['extra_mandatory_questions']==0
assert not model['ordinal_status_ladder'] and not model['mandatory_sequence']
model['status']='completed_internal_desktop_synthesis_practitioner_integration_pending'
model['review_basis']='Independent integrated desktop review, targeted original/visual source checks and preservation verification; no final publication or original fieldwork assurance.'
write('03-report/R07-priority-map.json',model)
for rel in ['03-report/R07-DESKTOP-READOUT.md','03-report/R07-CONTEXTUAL-PRIORITIES.md','03-report/modules/R07-priorities-and-contextual-differences.md']:
 p=ROOT/rel;t=p.read_text()
 t=t.replace('Internal desktop synthesis; independent integrated review pending.','Internal desktop research and independent integrated review completed.')
 t=t.replace('Internal analytical aid, pending independent integrated review.','Internal analytical aid; independent integrated review passed for desktop synthesis.')
 t=t.replace('Desktop synthesis prepared 29 October 2026. Independent integrated review and preservation gate pending.','Desktop research, independent integrated review and preservation checks completed 29 October 2026.')
 t=t.replace('Complete independent integrated review and preservation checks before closing desktop work.','Independent integrated review and preservation checks passed for desktop synthesis.')
 if rel.endswith('R07-DESKTOP-READOUT.md'):
  t+='\nVerification: [independent integrated review](../08-qa/R07-independent-review.md) and [completion record](../08-qa/R07-completion-check.json). Final-use checks and practitioner integration remain separate.\n'
 p.write_text(t)

rows=[
 ('FND-066','Published priority measures do not supply one common ranking of funded payroll investment.',['PRI7-C01','PRI7-C02','PRI7-C03','PRI7-C04','PRI7-C05'],'Composite status, manages-or-invests framing, separate AI marginal statements and feature desire have different units and populations. No common funding denominator or sequential conversion is established.','Preserve the exact measure, unit, horizon and source. Establish the concrete priority and actual commitment separately; do not average lists or infer a buying pipeline.'),
 ('FND-067','Personal development, employer support and usable organisational resources are different claims.',['PRI7-C06','PRI7-C08','SIG7-C06','METH7-C03'],'A qualification plan or employer offer does not prove funding paid, completed learning, useful capacity or a successful programme. Undisclosed amounts are not evidence of no funding.','Under existing selective probes record whose priority and known recurring/new resources, protected time and dependencies, without requiring confidential documents or a separate project budget.'),
 ('FND-068','Context can explain relevant payroll work without establishing a size, sector or country priority ranking.',['CTX7-C01','CTX7-C02','CTX7-C03','CTX7-C04','CTX7-C05'],'Official conditional guidance and one employer timing account are mechanisms and scoped context, not measured subgroup investment differences, legal determinations or a complexity score.','Use six optional context dimensions only where material; preserve contributor remit, actual task and timing rather than infer need from employer labels.'),
 ('FND-069','External planning signals and internal organisational commitment require separate dated evidence.',['SIG7-C01','SIG7-C02','SIG7-C03','SIG7-C04','SIG7-C05','SIG7-C06','SIG7-C07'],'Current guidance, interim future phases, declared service dates and a published programme account do not establish actual employer readiness, resourcing, later spend or realised benefit. No rates, full statute assurance, forecasts or product tests are supplied.','Record applicability and operative/interim/future status, then the actual known employer decision/resources/delivery. Recheck current detail before final use and do not sell a mandatory platform/provider/hire from a headline.'),
 ('FND-070','A case contrast, contextual mechanism, later hypothesis and unestablished group difference are different analytical claims.',['METH7-C01','METH7-C02','METH7-C03','METH7-C04'],'A small purposive cohort is not a representative subgroup survey; absent coverage is neither zero need nor equality. Mechanisms do not by themselves prove a causal explanation.','Compare work, scope, horizon and measure; retain alternative explanations and contrary cases. Preserve empty observation templates until permissioned original contributions exist.'),
 ('FND-071','A newly identified feature-chart conflict can be excluded numerically while preserving the question’s qualitative meaning.',['PRI7-C05','PRI7-C07'],'Moorepay branding/customisation has prose13 versus chart12; neither is reconciled or selected. The narrow conflict does not establish that every other value is incorrect.','Keep CLM-0392 on hold_numeric_reuse, use no feature percentages here, and preserve all earlier holds.'),
]
findings=read('05-analysis/findings.json')
for ident,statement,keys,limits,implication in rows:
 if not any(x['finding_id']==ident for x in findings['records']):
  findings['records'].append(dict(finding_id=ident,topic_ids=['R07'],statement=statement,supporting_claim_ids=[cs[x] for x in keys],contradicting_claim_ids=[],participant_observation_ids=[],interpretation=limits,decision_implication=implication,confidence_rationale='Targeted original/item/guidance review, explicit source reuses and independent integrated desktop challenge. No original fieldwork, representative funded-priority ranking, forecast or validated priority score.',outstanding_questions=['Actual permissioned priorities, known authority/resources, context and outcomes; achieved and missing case coverage.'],publication_status='internal_research_design',reviewed_on=DATE))
findings['status']='R01_to_R07_internal_desktop_synthesis';write('05-analysis/findings.json',findings)
changes=read('00-control/changes.json')
if not any(x['change_id']=='CHG-016' for x in changes['records']):
 changes['records'].append(dict(change_id='CHG-016',date=DATE,type='R07 priorities and contextual differences desktop research',description='Four new official routes,24 bounded claim/method/hold records and6 internal findings; survey item/status audit, six optional context dimensions, four nonordinal comparison claim purposes and dated planning contexts. Existing Q005/fourteen questions unchanged, blank templates and empty fieldwork/financial arrays. Moorepay branding/customisation numeric conflict held. Independent integrated review corrected chart-asset provenance;54 prior/client/core preservation hashes checked. No original fieldwork, estimates, legal calculation, product test or sending.'))
write('00-control/changes.json',changes)
wp=read('00-control/work-packages.json');wp['updated_on']=DATE;wp['active_work_package']='WP15'
wp['next_action']='R07 desktop synthesis complete. Next R08 preparatory synthesis across R01–R07; final WP15 framework/report requires WP11 coded original practitioner contributions. Do not mark dependencies completed or start final publication; no external sending without user permission.'
for x in wp['records']:
 if x['work_package_id']=='WP09':x.update(status='completed_desktop_research_practitioner_integration_pending',desktop_completed_on=DATE,evidence_of_completion='Four official routes,24 claim/method/hold records, six internal findings, six optional context dimensions and four nonordinal comparison purposes. Independent integrated review and54 preservation hashes passed. Fourteen questions/eight client files/prior modules unchanged; no fieldwork, ranking, forecast or final-use approval.')
write('00-control/work-packages.json',wp)
sources=read('02-evidence/registers/sources.json')['records'];claimrecords=read('02-evidence/registers/claims.json')['records']
counts=f"The register contains {len(sources)} source routes and {len(claimrecords)} claims or guardrails. They include different guidance, product declarations, cases and research populations, not equivalent independent surveys. {sum(bool(x.get('capture_path')) for x in sources)} source records have retained originals in their primary capture fields with checked hashes; additional reviewed captures/extracts are recorded separately. {len(findings['records'])} internal findings are recorded across R01–R07 and completed reviews."
p=ROOT/'00-control/CURRENT-STATUS.md';t=p.read_text();a=t.index('For current substantive findings, start with');b=t.index('\n\n## Main working conclusion',a)
t=t[:a]+'For current substantive findings, start with the [R07 desktop readout](../03-report/R07-DESKTOP-READOUT.md) and [priority/context guide](../03-report/R07-CONTEXTUAL-PRIORITIES.md), building on completed R01–R06. '+counts+' Current topic QA is `08-qa/R07-completion-check.json`; earlier checks/snapshots remain preserved. R07 passed independent integrated desktop review. R06 second challenge retains its recorded partial-review independence limits. No source has final publication approval.'+t[b:]
bullet='- R07 desktop research completed: exact priority measures, personal versus organisational support, six optional context dimensions and four nonordinal comparison claim purposes. Dated signals remain separate from actual commitment. Four new routes/24 bounded claims/six internal findings; one new numeric hold. Independent integrated review and54 preservation hashes passed. Original practitioner evidence and final-use checks remain open.\n'
if bullet not in t:t=t.replace('\nFor current substantive findings','\n'+bullet+'\nFor current substantive findings')
t=t.replace('Next is R07: priorities and defensible contextual differences.','R07 now separates priority meaning, actual commitment/resources, contextual mechanism and demonstrated case contrast. Next is R08 preparatory synthesis across the completed desktop modules; final WP15 remains dependent on WP11 coded original practitioner contributions.')
t=t.replace('R02–R06 practitioner integration and final-use checks; R07–R08 report-topic research;','R02–R07 practitioner integration and final-use checks; R08 preparatory/final synthesis;')
t=t.replace('and begin R07 desktop research or necessary checkpoint revisions.','and begin R08 preparatory synthesis or necessary checkpoint revisions. Final synthesis requires actual coded practitioner contributions; do not infer dependencies complete.')
p.write_text(t)
p=ROOT/'README.md';t=p.read_text();a=t.index('R01–R06 desktop work');b=t.index('\n\n## Additional review',a)
t=t[:a]+'''R01–R07 desktop work and their targeted reviews are complete for the respective internal design/synthesis purposes. The [R07 readout](03-report/R07-DESKTOP-READOUT.md) and [priority/context guide](03-report/R07-CONTEXTUAL-PRIORITIES.md) distinguish preference, organisational commitment, resources, delivery and relevant context. Six optional context dimensions and four comparison claim purposes add no questions, scores or market estimates. R07 passed independent integrated review; prior reviews retain their own stated limits. Next is R08 preparatory synthesis. Final WP15 depends on WP11 coded original practitioner contributions, so final framework/publication is not complete.

WP02 version 0.2 remains prepared for user review: [checkpoint notes](06-client-checkpoints/week-one-v0.2/REVIEW-NOTES.md). Earlier topic artifacts, eight client files, fourteen core questions and scope are preserved. '''+counts+' Current R07 QA is `08-qa/R07-completion-check.json`; nothing was sent.'+t[b:];p.write_text(t)
p=ROOT/'05-analysis/CONTRADICTIONS-AND-GAPS.md';t=p.read_text();marker='\n## R07 priority and contextual-comparison controls'
assert marker not in t, 'Do not re-run completion after it is recorded'
t+='''
## R07 priority and contextual-comparison controls

- Azets B1 composite status and E1 manages-or-invests framing do not establish a separately approved/funded project. SD Worx separate AI agreement marginals do not form a respondent pipeline; urgent HR/payroll/publisher-advice frames are not one ranking. CLM-0386–0389.
- Moorepay feature desire is not a purchase, willingness to pay or switching need. Branding/customisation prose13 versus original chart12 is held in CLM-0392; no feature percentage is used. Earlier Moorepay/Deloitte/UI holds remain. CLM-0390–0393.
- CIPP personal training status and employer support differ; neither alone establishes paid resources, completed learning or usable capability. Priority, authority, funding/resources, delivery and assessed result are separate, potentially concurrent facts. No mandatory ladder, score, budget document or extra core question. CLM-0391, CLM-0393, CLM-0408.
- Working-pattern, jurisdiction and tool/task boundaries plus one employer timing account support conditional mechanisms, not funded group rankings. Six optional context dimensions do not classify workers, supply tax advice or justify an SME/sector/country stereotype. CLM-0394–0398.
- HMRC BiK manual remains draft/interim future scope; specified phases/benefits, exclusions and dependencies matter. November2026 services/April2027 tools availability are future declarations as of29October, not observed launches or product tests. Recheck applicable current detail before final use. CLM-0399–0401.
- HMRC/Acas SSP guidance describes effective6April2026 changes with remaining eligibility/transitional conditions. Guidance instructions are not actual employer compliance, resources or benefit. Empty HTTP202 legislation and blocked Powys retrieval are excluded, not legal originals or budget case evidence. CLM-0402–0403.
- Synergy is one reused combined-function published programme: reported approval/contract/funding responsibilities differ from prospective gaps/benefits. No amount, spend assurance, payroll-only cost or new employer case. CLM-0404.
- Distinguish actual case contrast, source-supported mechanism, later hypothesis and unestablished group difference; these are not ordinal evidence scores. Achieved/missing coverage, alternative explanations and contrary cases remain visible. No participant observation, subgroup estimate, national priority ranking or forecast exists. CLM-0405–0409.
- R07 passed an independent integrated desktop review. The reviewer’s chart-asset provenance correction is applied; retained publisher chart is not labelled as our PDF render. Fourteen questions, eight client files and54 prior/core/client hashes remain unchanged. Final practitioner integration, proposed cohort confirmation and final-use review are open; nothing sent.
''';p.write_text(t)

artifacts=['03-report/R07-DESKTOP-READOUT.md','03-report/R07-CONTEXTUAL-PRIORITIES.md','03-report/R07-priority-map.json','03-report/modules/R07-priorities-and-contextual-differences.md',review,'08-qa/R07-record-map.json','08-qa/R07-captures.json','08-qa/r07-review/integrated-review-checks.json']
result=dict(date=DATE,status='passed_for_internal_R07_desktop_synthesis',review_basis='Independent integrated desktop review with bounded original/visual source sample, record/hash/core/blank-data checks; final use and fieldwork remain separate.',new_source_routes=4,new_claim_or_guardrail_records=24,source_records=len(sources),claim_records=len(claimrecords),source_records_with_primary_retained_original=sum(bool(x.get('capture_path')) for x in sources),internal_findings=len(findings['records']),context_dimensions=6,comparison_claim_purposes=4,planning_contexts=3,checked_capture_files=len(captures),preserved_baseline_records=len(baseline),client_files=[dict(**x,unchanged=True) for x in baseline if x['path'].startswith('06-client-checkpoints/')],fourteen_core_questions_unchanged=True,new_practitioner_observations=0,numerical_estimates=0,product_trials=0,extra_mandatory_questions=0,external_actions=[],final_publication_approved=False,artifacts=[dict(path=p,sha256=sha(p)) for p in artifacts])
write('08-qa/R07-completion-check.json',result)
print(json.dumps({k:v for k,v in result.items() if k not in ['artifacts','client_files']},indent=2))
