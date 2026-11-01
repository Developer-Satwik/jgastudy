from pathlib import Path
import hashlib, json

ROOT = Path(__file__).resolve().parents[1]
DATE = '2026-10-29'
def read(p): return json.loads(p.read_text())
def write(p, d): p.write_text(json.dumps(d, indent=2, ensure_ascii=False) + '\n')
review = ROOT / '08-qa/R04-independent-review.md'
assert review.exists(), 'Independent integrated review is required before desktop completion.'

findings_path = ROOT / '05-analysis/findings.json'
findings = read(findings_path)
rows = [
    ('FND-034', 'Decision authority is most usefully reconstructed for a specified action, object and date rather than inferred from title.',
     ['CLM-0253','CLM-0256','CLM-0258','CLM-0259','CLM-0261','CLM-0264','CLM-0265','CLM-0266'],
     'Analytical conclusion from source-scoped role guidance and selected published cases, not an observed universal hierarchy or authority-prevalence finding.',
     'Record the actual right, scope, knowledge basis and decision event. Allow shared, combined, absent and unknown functions.'),
    ('FND-035', 'The inspected public cases distinguish recommendations, conditional backing, funding, awards, functional signoff and final release.',
     ['CLM-0269','CLM-0270','CLM-0271','CLM-0272','CLM-0273','CLM-0274','CLM-0275','CLM-0276'],
     'Three deliberately selected public-employer programmes, with linked publications not independent cases. They do not establish private-employer process or benefits from an approval.',
     'Preserve dated decisions, conditions and later states separately. Do not turn an award or go-live into evidence of realised return.'),
    ('FND-036', 'The UK employer accounts report different relationships between operational input and particular decision stages.',
     ['CLM-0264','CLM-0265'],
     'Purplebricks is supplier-published named testimony; the construction case is an adviser-reported anonymous account. Undisclosed rights and dates remain unknown; no causal or prevalence inference.',
     'Establish actual participation and exclusion in each decision rather than assume payroll always leads or is always excluded. Later resource approval is not original selection authority.'),
    ('FND-037', 'Advice, assurance, delegated authority and organisational accountability require separate interpretation.',
     ['CLM-0254','CLM-0256','CLM-0258','CLM-0259','CLM-0260','CLM-0262','CLM-0277'],
     'Government, listed-company, privacy-role and supplier-operational sources retain their own scopes. ICO page is under review; no universal CFO or specialist veto is established.',
     'Record whether input was a concern, advice, prerequisite, binding condition or formal stop; identify the actual clearance/escalation right. Operational payment authority is not purchasing authority.'),
    ('FND-038', 'Evidence purpose and record regime determine what can be concluded about the decision route.',
     ['CLM-0263','CLM-0267','CLM-0268','CLM-0278'],
     'Evaluation perceptions, survey selection criteria and leadership recommendations do not reconstruct actual approvals. Notice labels depend on the applicable date/regime; no procurement advice or timetable inferred.',
     'Use source-specific locators and limits, distinguish perceived from observed/described authority, and retain missingness and record conflicts without manufacturing a complete chain.')
]
for ident, statement, claims, limits, implication in rows:
    if any(x['finding_id'] == ident for x in findings['records']): continue
    findings['records'].append(dict(finding_id=ident, topic_ids=['R04'], statement=statement,
        supporting_claim_ids=claims, contradicting_claim_ids=[], participant_observation_ids=[],
        interpretation=limits, decision_implication=implication,
        confidence_rationale='Inspected primary role/record context and selected published cases, with independent integrated review. No original fieldwork or validated framework implied.',
        outstanding_questions=['Actual rights, actions, conditions and pathways in permissioned practitioner cases.'],
        publication_status='internal_research_design', reviewed_on=DATE))
findings['status'] = 'R01_R02_R03_R04_internal_desktop_synthesis'
write(findings_path, findings)

changes_path = ROOT / '00-control/changes.json'
changes = read(changes_path)
if not any(x['change_id'] == 'CHG-010' for x in changes['records']):
    changes['records'].append(dict(change_id='CHG-010', date=DATE, type='R04 decision authority and pathways desktop research',
        description='Twelve new source routes, twenty-six bounded claim/method records and five internal findings. Twelve optional analytical functions, six secondary employer examples, scope/date/knowledge/conditions and separate decision/result states. Integrated review and preservation checks completed. No change to fourteen core questions, client files, scope or fieldwork status; no external action.'))
write(changes_path, changes)
wp_path = ROOT / '00-control/work-packages.json'
wp = read(wp_path); wp['updated_on'] = DATE; wp['active_work_package'] = 'WP07'
wp['next_action'] = 'R04 desktop work completed. Next substantive step R05: business-case evidence, funding and implementation risks. Original practitioner integration and user permission before external sending remain open.'
for x in wp['records']:
    if x['work_package_id'] == 'WP06':
        x.update(status='completed_desktop_research_practitioner_integration_pending', desktop_completed_on=DATE,
            evidence_of_completion='Source-scoped governance, mixed-role buyer-method recheck and six selected secondary employer cases; twelve optional function map, decision/event/condition design, twenty-six claim/guardrail records and independent integrated review. Core/client and prior R02/R03 artifacts preserved. Practitioner integration and final-use checks remain open.')
write(wp_path, wp)

module = ROOT / '03-report/modules/R04-decision-authority-and-pathways.md'
t = module.read_text().replace('Desktop synthesis prepared 29 October 2026. Integrated review pending; original practitioner integration and final-use checks remain open.',
    'Desktop research and integrated review completed 29 October 2026. Original practitioner integration and final-use checks remain open.')
t = t.replace('Complete independent integrated review and preservation checks, then move to R05:', 'Independent integrated review and preservation checks are complete. Next is R05:')
module.write_text(t)
gaps = ROOT / '05-analysis/CONTRADICTIONS-AND-GAPS.md'
t = gaps.read_text()
if '## R04 authority and pathway controls' not in t:
    t += '''
## R04 authority and pathway controls

- Title, meeting attendance, familiarity, evaluation involvement and practical dependency do not independently establish decision rights. CLM-0253–0266.
- G2 evaluation perceptions, HR.com selection criteria and KPMG/UKG leadership recommendations are not an authority-prevalence dataset. CLM-0263/0267/0268.
- Purplebricks CFO agreement on change is not final funding/contract approval; the CIPP case's later CEO resourcing is not original selection authority. Attributed cases remain distinct from new JGA contributors. CLM-0264–0266.
- Scottish recommendation, conditional backing, formal go-live and functional migration signoff retain separate dates/scopes. Positive governance assessment retained; no benefit inference. CLM-0269–0273.
- Rotherham continuity award uses the stated delegation; decision body says 2024 but signature line says 2023. Do not silently repair it, infer reviewer vetoes or equate award with execution. CLM-0274.
- Argyll minutes/report concern one employer and decision; additional-budget approval is not actual spend or successful remediation. Final go-live approver is unestablished. CLM-0275–0276.
- GovS definitions and listed-company guidance retain their populations. Advice/assurance and accountable organisational ownership do not establish a universal payroll veto; ICO page is under review. CLM-0253–0262/0277.
- Procurement notice labels require the applicable regime/date and actual wording; do not apply current Act sequence to older/differently governed or ordinary private cases. CLM-0278.
- GovS 002 and Purplebricks retain parsed reader extracts rather than raw originals. Three new council source bodies were inspected but local raw captures remain unavailable. No missing file/hash is fabricated.
- Twelve functions are an analytical vocabulary, not twelve required posts or extra mandatory questions. Original observation arrays remain empty. No validated approval funnel or authority score.
'''
    gaps.write_text(t)

sources = read(ROOT / '02-evidence/registers/sources.json')['records']
claims = read(ROOT / '02-evidence/registers/claims.json')['records']
count_text = f"The register contains {len(sources)} source routes and {len(claims)} claims or guardrails. These include guidance, product descriptions, cases and different report populations, not equivalent independent surveys. {sum(bool(x.get('capture_path')) for x in sources)} source records have actual retained originals with checked hashes; parsed extracts are recorded separately. {len(findings['records'])} internal findings are recorded across R01–R04 and completed reviews."
status_path = ROOT / '00-control/CURRENT-STATUS.md'
t = status_path.read_text()
old_start = 'For current substantive findings, start with'
start = t.index(old_start); end = t.index('\n\n## Main working conclusion', start)
t = t[:start] + 'For current substantive findings, start with the [R04 authority readout](../03-report/R04-DESKTOP-READOUT.md) and [decision pathway](../03-report/R04-DECISION-PATHWAY.md), building on the [R03 second-check readout](../03-report/R03-SECOND-CHECK-READOUT.md), [response options](../03-report/R03-OPTIONS-AND-TRADEOFFS.md) and [R02 needs/consequences matrix](../03-report/R02-NEEDS-CONSEQUENCES-MATRIX.md). ' + count_text + ' R01 originally established 35 sources and 39 claims; later records remain internal context, not publication approval. Current QA records are `08-qa/R02-second-check-completion.json`, `08-qa/R03-second-check-completion.json` and `08-qa/R04-completion-check.json`; earlier checks are historical.' + t[end:]
bullet = '- R04 desktop research completed on 29 October: source-scoped roles/delegation, rechecked buyer-method limits, six selected secondary cases and twelve optional analytical functions. Independent integrated review and preservation checks passed. Funding, selection, signature, conditional backing, functional signoff, final release and result remain distinct; original practitioner integration and final-use checks remain open.\n'
if bullet not in t: t = t.replace('\nFor current substantive findings', '\n' + bullet + '\nFor current substantive findings')
t = t.replace('Next is R04: decision authority and pathways.', 'R04 now maps the actual dated decision, rights, knowledge basis and conditions. Next is R05: business-case evidence, funding and implementation risks.')
t = t.replace("R02/R03 practitioner integration and final-use checks; R04–R08 report-topic research;", "R02–R04 practitioner integration and final-use checks; R05–R08 report-topic research;")
t = t.replace('and begin R04 desktop research or necessary checkpoint revisions.', 'and begin R05 desktop research or necessary checkpoint revisions.')
status_path.write_text(t)
readme = ROOT / 'README.md'; t = readme.read_text()
start = t.index('R01–R03 desktop research is complete'); end = t.index('\n\n## Additional review', start)
t = t[:start] + '''R01–R04 desktop research is complete for the respective design/synthesis purposes. The [R04 readout](03-report/R04-DESKTOP-READOUT.md) and [decision pathway](03-report/R04-DECISION-PATHWAY.md) distinguish actual decision rights from titles, influence and advice, with six selected secondary employer cases and twelve optional analytical functions. Funding, selection, signature, release and realised result remain distinct. The [R03 second challenge](03-report/R03-SECOND-CHECK-READOUT.md) and [option map](03-report/R03-OPTIONS-AND-TRADEOFFS.md) remain unchanged. Next is R05: business-case evidence, funding and implementation risks. No original practitioner integration, final publication approval or product trial is implied.

WP02 version 0.2 remains prepared for user review: [checkpoint notes and files](06-client-checkpoints/week-one-v0.2/REVIEW-NOTES.md). Fourteen core questions and all eight client files remain unchanged. Collection arrangements and Nick's scope review remain open before fieldwork. ''' + count_text + ' Current R04 QA is `08-qa/R04-completion-check.json`; earlier topic artifacts and their hashes remain preserved.' + t[end:]
readme.write_text(t)

client = []
for version in ['0.1', '0.2']:
    for x in read(ROOT / f'06-client-checkpoints/week-one-v{version}/checkpoint-manifest.json')['files']:
        sha = hashlib.sha256((ROOT / x['path']).read_bytes()).hexdigest()
        assert sha == x['sha256']; client.append(dict(path=x['path'], sha256=sha, unchanged=True))
prior = []
for file in ['R02-second-check-completion.json','R03-second-check-completion.json']:
    for x in read(ROOT / '08-qa' / file)['artifacts']:
        assert hashlib.sha256((ROOT / x['path']).read_bytes()).hexdigest() == x['sha256']
    prior.append(dict(check=file, all_artifacts_unchanged=True))
questions = read(ROOT / '01-method/question-map.json')
assert questions == read(ROOT / '01-method/question-map-v0.2.json') and len(questions['records']) == 14
model = read(ROOT / '03-report/R04-decision-map.json')
assert not model['mandatory_sequence'] and model['participant_observations'] == []
capture_log = read(ROOT / '08-qa/R04-captures.json')
for x in capture_log['files']:
    assert hashlib.sha256((ROOT / x['path']).read_bytes()).hexdigest() == x['sha256']
for rel in ['05-analysis/observations.json','05-analysis/charts.json','04-table/financial-inputs.json']:
    assert read(ROOT / rel)['records'] == []
artifacts = ['03-report/R04-DESKTOP-READOUT.md','03-report/R04-DECISION-PATHWAY.md','03-report/R04-decision-map.json',
             '03-report/modules/R04-decision-authority-and-pathways.md','08-qa/R04-independent-review.md','08-qa/R04-record-map.json']
result = dict(date=DATE, status='passed_for_internal_R04_desktop_synthesis', new_source_routes=12, new_claim_or_guardrail_records=26,
    source_records=len(sources), claim_records=len(claims), source_records_with_retained_original=sum(bool(x.get('capture_path')) for x in sources),
    internal_findings=len(findings['records']), analytical_functions=12, selected_published_employer_cases=6,
    new_practitioner_observations=0, fourteen_core_questions_unchanged=True, client_files=client, prior_topic_artifacts=prior,
    capture_files_hash_checked=len(capture_log['files']), final_publication_approved=False, product_or_API_tests=0,
    external_actions=[], artifacts=[dict(path=f, sha256=hashlib.sha256((ROOT / f).read_bytes()).hexdigest()) for f in artifacts],
    next='R05 business-case evidence, funding and implementation risks. No sending without user permission.')
write(ROOT / '08-qa/R04-completion-check.json', result)
print(json.dumps({k:v for k,v in result.items() if k not in ['client_files','artifacts','prior_topic_artifacts']}, indent=2))
