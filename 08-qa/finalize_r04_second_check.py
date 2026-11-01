from pathlib import Path
import hashlib, json

ROOT = Path(__file__).resolve().parents[1]
DATE = '2026-10-29'
def read(p): return json.loads(p.read_text())
def write(p, d): p.write_text(json.dumps(d, indent=2, ensure_ascii=False) + '\n')
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
review = ROOT / '08-qa/R04-second-check-independent-review.md'
assert review.exists(), 'Independent integrated second review is required before completion.'
mapping = read(ROOT / '08-qa/R04-second-check-record-map.json')
assert len(mapping['source_map']) == 9 and len(mapping['claim_map']) == 16

fp = ROOT / '05-analysis/findings.json'; findings = read(fp)
rows = [
    ('FND-039', 'The relevant authority is the remit effective for the selected event, including any known change.',
     ['CLM-0279','CLM-0280','CLM-0281','CLM-0282','CLM-0288','CLM-0289'],
     'Historical parliamentary and current government design are not a private-market trend. Prospective recruitment remit is not effective delegation or a completed appointment.',
     'Record requested scope, described delegation, effective period and actual exercise; preserve interim, succession or handover conditions where relevant.'),
    ('FND-040', 'Organisational, contractual and service scope matter alongside the authority holder.',
     ['CLM-0279','CLM-0283','CLM-0284','CLM-0286','CLM-0287'],
     'Selected founder-targeted and global-programme contexts do not establish a simple SME/large-employer hierarchy, verified headcount, sole purchasing power or cross-country rule.',
     'Identify employer/external party, broad group/local/entity/country level and relevant service/agreement. Keep operational software access and retained responsibility separate from buying authority.'),
    ('FND-041', 'The mandate described and practical decision-making reported may differ and should remain separate.',
     ['CLM-0285','CLM-0287','CLM-0288','CLM-0289'],
     'Adviser diagnosis and recruiter cases/briefs are bounded source accounts, not independent delegation records, legal judgments or causal verification. Missing powers remain unknown.',
     'Preserve what should happen as understood, what was directly done/observed, any reported difference and the knowledge basis; do not manufacture a complete chain or resolve by seniority.'),
    ('FND-042', 'Acceptance and approval require an explicit object.',
     ['CLM-0284','CLM-0290','CLM-0291'],
     'Supplier operational permissions and service declarations are not tested corporate controls, signed scopes or proof of authority to buy or accept another work product.',
     'Distinguish hours for payment/invoicing, deliverables, handover, payroll output, supplier selection and contractual commitment; establish each actual remit.'),
    ('FND-043', 'Relevant affected-party input or external conditions are distinct from internal investment approval.',
     ['CLM-0292','CLM-0293','CLM-0294'],
     'Employment-term and monitoring guidance are conditional contexts, not a universal worker veto or compulsory consultation route for software changes. ICO guidance is under review; no employer-specific legal advice inferred.',
     'Establish what actually changes, which relevant condition was identified, its basis, owner and state. Consultation, contract agreement and processing consent are not interchangeable.')
]
for ident, statement, claims, limits, implication in rows:
    if any(x['finding_id'] == ident for x in findings['records']): continue
    findings['records'].append(dict(finding_id=ident, topic_ids=['R04'], statement=statement, supporting_claim_ids=claims,
        contradicting_claim_ids=[], participant_observation_ids=[], interpretation=limits, decision_implication=implication,
        confidence_rationale='Targeted multi-perspective second challenge, source-specific original inspection and independent integrated review; no original fieldwork or validated authority model.',
        outstanding_questions=['Actual effective rights, actions, context and conditions in permissioned practitioner cases.'],
        publication_status='internal_research_design', reviewed_on=DATE))
findings['status'] = 'R01_R02_R03_R04_internal_synthesis_including_R04_second_challenge'; write(fp, findings)

chp = ROOT / '00-control/changes.json'; changes = read(chp)
if not any(x['change_id'] == 'CHG-011' for x in changes['records']):
    changes['records'].append(dict(change_id='CHG-011', date=DATE, type='User-requested R04 second challenge',
        description='Historical/effective-mandate, market/service-level, all-six-comparator/prior-study and affected-party checks. Nine new source routes, sixteen bounded claim/method records and five internal findings. Five optional conditions supplement unchanged twelve functions and fourteen core questions. Constructed CFO/leader premises explicitly cannot validate authority or demand; 243 independent bridge checks passed. First-pass snapshots, prior topics and client files preserved. No original fieldwork or external action.'))
write(chp, changes)
wpp = ROOT / '00-control/work-packages.json'; wp = read(wpp)
wp['updated_on'] = DATE; wp['active_work_package'] = 'WP07'
wp['next_action'] = 'R04 second challenge completed. Next R05: business-case evidence, funding and implementation risks. Practitioner/final-use work remains open; no external sending without user permission.'
for x in wp['records']:
    if x['work_package_id'] == 'WP06':
        x['second_challenge_status'] = 'completed_for_internal_desktop_synthesis'
        x['second_challenge_completed_on'] = DATE
        x['second_challenge_readout'] = '03-report/R04-SECOND-CHECK-READOUT.md'
        if 'Second challenge applied:' not in x['evidence_of_completion']:
            x['evidence_of_completion'] += ' Second challenge applied: effective remit/change, organisation/contract level, mandate versus practice, acceptance object and relevant affected-party conditions. Twelve functions/core 14 unchanged. Prior prompt bridge passed 243 independent checks; no authority/demand inference.'
write(wpp, wp)
module = ROOT / '03-report/modules/R04-decision-authority-and-pathways.md'
t = module.read_text().replace('Second-challenge integrated review is pending.', 'Second-challenge [integrated review](../../08-qa/R04-second-check-independent-review.md) and preservation checks passed.')
module.write_text(t)

gaps = ROOT / '05-analysis/CONTRADICTIONS-AND-GAPS.md'; t = gaps.read_text()
if '## R04 second-challenge controls' not in t:
    t += '''
## R04 second-challenge controls

- Historical framework/customer powers and April 2026 reforms demonstrate the need to identify effective remit and scope, not a measured private-market shift or better outcome. CLM-0279–0282.
- Payfit selected involvement and software-admin rights do not establish headcount, sole authority or a complete buying chain. HMRC retained PAYE responsibility does not name the internal signatory. CLM-0283–0284/0286.
- Chazey's Herbalife diagnosis concerns reported practical implementation calls, not proven formal delegation, misconduct or independently verified causation. No universal provider behaviour. CLM-0285/0287.
- Frazer's CPO-tasked case and Oakleaf's prospective services brief do not establish funding/signature or actual appointment powers. Temporary/succession/handback conditions are analyst checks. CLM-0288–0289.
- Hays time approval is for its defined operational object; it is not automatically deliverable acceptance or investment authority. Other service declarations are not a signed client scope. CLM-0290–0291.
- Constructed S01/S05/S10 prompts, including specified CFO/permanent-leader premises, cannot validate market hierarchy, demand or a staffing solution. Twelve exact prompts and 96 saved answers remain internal analyst contrasts;243 independent provenance/link/text checks passed. No reruns or recommendation counts reused.
- Relevant terms-change/monitoring conditions must be established for the actual proposal. No universal consultation route, employee veto or processing-consent inference. ICO page is under review. CLM-0292–0294.
- Datasite's unrecovered rollout passage and redirected Portfolio job advert are not promoted as original-body evidence. Failed raw captures and selected reader extracts remain labelled; no fabricated originals/hashes.
- Five conditions are optional analysis, not additional mandatory interview questions, a new respondent cohort or extra required posts. First-pass artifacts and original-client/core files remain preserved.
'''
    gaps.write_text(t)

sources = read(ROOT / '02-evidence/registers/sources.json')['records']
claims = read(ROOT / '02-evidence/registers/claims.json')['records']
counts = f"The register contains {len(sources)} source routes and {len(claims)} claims or guardrails. These include guidance, product descriptions, cases and different report populations, not equivalent independent surveys. {sum(bool(x.get('capture_path')) for x in sources)} source records have actual retained originals with checked hashes; parsed extracts are recorded separately. {len(findings['records'])} internal findings are recorded across R01–R04 and completed reviews."
status = ROOT / '00-control/CURRENT-STATUS.md'; t = status.read_text()
a = t.index('For current substantive findings, start with'); b = t.index('\n\n## Main working conclusion', a)
t = t[:a] + 'For current substantive findings, start with the [R04 second-check readout](../03-report/R04-SECOND-CHECK-READOUT.md), [authority synthesis](../03-report/R04-DESKTOP-READOUT.md) and [decision pathway](../03-report/R04-DECISION-PATHWAY.md), building on completed R02/R03 work. ' + counts + ' R01 originally established 35 sources and 39 claims; later additions remain internal context, not publication approval. Current QA records include `08-qa/R02-second-check-completion.json`, `08-qa/R03-second-check-completion.json` and `08-qa/R04-second-check-completion.json`; first-pass checks are historical.' + t[b:]
bullet = '- User-requested R04 second challenge completed: historical/effective mandate, segmented market, all six comparators/prior-study and affected-party lenses. Five optional conditions applied; independent integrated review passed and the prompt bridge passed 243 checks. First-pass snapshots, earlier topics and all eight client files preserved.\n'
if bullet not in t: t = t.replace('\nFor current substantive findings', '\n' + bullet + '\nFor current substantive findings')
t = t.replace('The user-requested second challenge of R04 is in progress across historical, market, six-comparator/prior-study and affected-party lenses. Complete that review before R05: business-case evidence, funding and implementation risks.', 'R04\'s second challenge is complete, including effective remit, organisation/contract level, mandate versus practice, acceptance object and relevant affected-party conditions. Next is R05: business-case evidence, funding and implementation risks.')
status.write_text(t)
readme = ROOT / 'README.md'; t = readme.read_text(); a = t.index('R01–R04 desktop research is complete'); b = t.index('\n\n## Additional review', a)
t = t[:a] + '''R01–R04 desktop work is complete for the respective design/synthesis purposes. The [R04 second challenge](03-report/R04-SECOND-CHECK-READOUT.md), [synthesis](03-report/R04-DESKTOP-READOUT.md) and [decision pathway](03-report/R04-DECISION-PATHWAY.md) now include five selective conditions around effective remit, organisation/contract level, mandate versus practice, acceptance object and affected-party conditions. Twelve functions and the fourteen-question core remain unchanged. Prior constructed prompts supply analyst contrasts, not authority or demand evidence; 243 independent bridge checks passed. Next is R05: business-case evidence, funding and implementation risks. Original practitioner integration and final publication checks remain open.

WP02 version 0.2 remains prepared for user review: [checkpoint notes and files](06-client-checkpoints/week-one-v0.2/REVIEW-NOTES.md). All eight client files, completed R02/R03 artifacts and first-pass R04 snapshots are preserved. Collection arrangements and Nick's scope review remain open before fieldwork. ''' + counts + ' Current R04 QA is `08-qa/R04-second-check-completion.json`; earlier checks remain historical.' + t[b:]
readme.write_text(t)

client = []
for v in ['0.1','0.2']:
    for x in read(ROOT / f'06-client-checkpoints/week-one-v{v}/checkpoint-manifest.json')['files']:
        assert sha(ROOT / x['path']) == x['sha256']; client.append(dict(path=x['path'], sha256=x['sha256'], unchanged=True))
prior = []
for f in ['R02-second-check-completion.json','R03-second-check-completion.json']:
    for x in read(ROOT / '08-qa' / f)['artifacts']: assert sha(ROOT / x['path']) == x['sha256']
    prior.append(dict(check=f, all_artifacts_unchanged=True))
snapshots = read(ROOT / '03-report/research-notes/r04-second-check/before-review/manifest.json')['files']
first = {x['path']:x['sha256'] for x in read(ROOT / '08-qa/R04-completion-check.json')['artifacts']}
for x in snapshots: assert sha(ROOT / x['snapshot_path']) == x['sha256'] == first[x['original_path']]
q = read(ROOT / '01-method/question-map.json')
assert q == read(ROOT / '01-method/question-map-v0.2.json') and len(q['records']) == 14
model = read(ROOT / '03-report/R04-decision-map.json')
assert len(model['functions']) == 12 and len(model['cross_cutting_conditions']) == 5 and model['participant_observations'] == []
bridge = read(ROOT / '08-qa/R04-prior-study-bridge-check.json')
assert bridge['status'] == 'passed' and len(bridge['checks']) == 243 and all(x['passed'] for x in bridge['checks'])
assert sha(ROOT / bridge['bridge_path']) == bridge['bridge_sha256']
captures = read(ROOT / '08-qa/R04-second-check-captures.json')['files']
for x in captures: assert sha(ROOT / x['path']) == x['sha256']
for f in ['05-analysis/observations.json','05-analysis/charts.json','04-table/financial-inputs.json']: assert read(ROOT / f)['records'] == []
files = ['03-report/R04-SECOND-CHECK-READOUT.md','03-report/R04-DESKTOP-READOUT.md','03-report/R04-DECISION-PATHWAY.md','03-report/R04-decision-map.json',
         '03-report/modules/R04-decision-authority-and-pathways.md','08-qa/R04-second-check-record-map.json','08-qa/R04-second-check-independent-review.md','08-qa/R04-prior-study-bridge-check.json']
result = dict(date=DATE, status='passed_for_internal_R04_second_challenge', supersedes_for_current_synthesis='08-qa/R04-completion-check.json',
    new_source_routes=9, new_claim_or_guardrail_records=16, source_records=len(sources), claim_records=len(claims),
    source_records_with_retained_original=sum(bool(x.get('capture_path')) for x in sources), internal_findings=len(findings['records']),
    optional_functions=12, selective_conditions=5, prior_bridge_checks_passed=243, capture_files_hash_checked=len(captures),
    client_files=client, prior_topic_artifacts=prior, first_pass_R04_snapshots=snapshots, fourteen_core_questions_unchanged=True,
    new_practitioner_observations=0, product_or_API_tests=0, external_actions=[], final_publication_approved=False,
    artifacts=[dict(path=f, sha256=sha(ROOT / f)) for f in files], next='R05 business-case evidence, funding and implementation risks. No external sending.')
write(ROOT / '08-qa/R04-second-check-completion.json', result)
print(json.dumps({k:v for k,v in result.items() if k not in ['client_files','prior_topic_artifacts','first_pass_R04_snapshots','artifacts']}, indent=2))
