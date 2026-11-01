from pathlib import Path
import json
import re
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
checks = []

def require(test, message):
    if not test:
        raise ValueError(message)
    checks.append(message)

data = {}
for file in ROOT.rglob('*.json'):
    data[str(file.relative_to(ROOT))] = json.loads(file.read_text())
require(bool(data), 'Structured project records parse')
t02s_before={x['original_path']:x for x in data.get('04-table/research-notes/t02-second-check/before-review/manifest.json',{}).get('records',[])}
t02s_canonical_paths={f'02-evidence/registers/{n}.json'for n in ['sources','claims','searches','source-aliases']}|{'05-analysis/findings.json'}
def t02s_asof_canonical(path):
    return t02s_before[path]['snapshot_path'] if data.get('08-qa/T02-second-check-record-map.json') and path in t02s_canonical_paths else path


baseline = data['00-control/scope-baseline.json']
require(baseline['commercial']['total_fee'] == 1500, 'Total scope fee preserved')
require(baseline['commercial']['report_allocation'] == 1000 and baseline['commercial']['table_allocation'] == 500, 'Workstream allocations preserved')
require(baseline['commercial']['upfront'] + baseline['commercial']['balance'] == 1500, 'Payment split reconciles')
require(baseline['research']['practitioner_target_min'] == 6 and baseline['research']['practitioner_target_max'] == 10, 'Practitioner target preserved')
require(baseline['research']['table_conversations_max'] == 4 and baseline['research']['comparables'] == 6, 'Table scope preserved')
require(not baseline['research']['primary_population_approved'], 'Unapproved population remains proposed')
require(baseline['timing']['formal_kickoff_date'] is None, 'No kickoff date invented')

deliverables = data['00-control/deliverables.json']['records']
require(len(deliverables) == 22, 'All 22 scope records present')
require(all(d['status'] in ['planned','in_progress'] and not d['final_paths'] for d in deliverables), 'No final client deliverable falsely marked finished')
require(len({d['deliverable_id'] for d in deliverables}) == len(deliverables), 'Deliverable IDs unique')

packages = data['00-control/work-packages.json']['records']
package_ids = {p['work_package_id'] for p in packages}
require(len(package_ids) == len(packages), 'Work package IDs unique')
require(all(set(p['dependencies']) <= package_ids for p in packages), 'Work dependencies resolve')
for p in packages:
    if p['working_file']:
        require((ROOT / p['working_file']).is_file(), f"Working file exists for {p['work_package_id']}")

sources = data['02-evidence/registers/sources.json']['records']
require(len({s['source_id'] for s in sources}) == len(sources), 'Source IDs unique')
require(all(s['url'].startswith('https://') for s in sources), 'Sources retain original HTTPS routes')
require(all(s['review_status'] != 'publication_checked' for s in sources), 'Discovery not misreported as full publication review')
for s in sources:
    if s.get('capture_path'):
        capture=ROOT/s['capture_path']
        require(capture.is_file(), f"Source capture exists for {s['source_id']}")
        import hashlib
        require(hashlib.sha256(capture.read_bytes()).hexdigest()==s['capture_sha256'], f"Capture hash matches for {s['source_id']}")
    else:
        require(not s.get('capture_sha256'), f"No hash invented for {s['source_id']}")
source_ids = {s['source_id'] for s in sources}
for record in data['02-evidence/registers/searches.json']['records']:
    require(set(record.get('related_source_ids',[])) <= source_ids, f"Search references resolve for {record['search_id']}")

claims=data['02-evidence/registers/claims.json']['records']
claim_ids={c['claim_id'] for c in claims}
require(len(claim_ids)==len(claims), 'Claim IDs unique')
for c in claims:
    require(set(c['source_ids'])<=source_ids, f"Claim sources resolve for {c['claim_id']}")
for f in data['05-analysis/findings.json']['records']:
    require(set(f['supporting_claim_ids']+f['contradicting_claim_ids'])<=claim_ids, f"Finding evidence resolves for {f['finding_id']}")
    require(f['publication_status']=='internal_research_design', f"Finding not misreported as client-approved for {f['finding_id']}")

r02_map=data['08-qa/R02-deepening-record-map.json']
require(set(r02_map['source_map'].values())<=source_ids, 'R02 mapped sources resolve')
require(set(r02_map['claim_map'].values())<=claim_ids, 'R02 mapped claims resolve')
require(len(r02_map['claim_map'])==24, 'Twenty-four R02 deepening claim/guardrail records mapped')
require((ROOT/'08-qa/R02-independent-review.md').is_file(), 'R02 independent synthesis review retained')
require((ROOT/'03-report/research-notes/r02-operating-needs/MODULE-INITIAL.txt').is_file(), 'Initial R02 module preserved as a verbatim text snapshot')
for module_file in ['03-report/R02-DESKTOP-READOUT.md','03-report/R02-NEEDS-CONSEQUENCES-MATRIX.md']:
    require(set(re.findall(r'CLM-\d{4}',(ROOT/module_file).read_text()))<=claim_ids, f'R02 synthesis claim references resolve in {module_file}')

second_map=data.get('08-qa/R02-second-check-record-map.json')
if second_map:
    require(len(second_map['source_map'])==20 and set(second_map['source_map'].values())<=source_ids, 'Twenty second-challenge source routes resolve')
    require(len(second_map['claim_map'])==22 and set(second_map['claim_map'].values())<=claim_ids, 'Twenty-two second-challenge claim/guardrail references resolve')
    bridge=data['08-qa/R02-prior-study-bridge-check.json']
    require(bridge['status']=='passed' and all(c['passed'] for c in bridge['checks']), 'Independent prior-study bridge checks passed')
    for ident in ['CLM-0167','CLM-0168']:
        require(next(c for c in claims if c['claim_id']==ident)['status']=='hold_numeric_reuse', f'Existing numerical hold preserved for {ident}')
    for rel in ['03-report/R02-SECOND-CHECK-READOUT.md','03-report/R02-NEEDS-CONSEQUENCES-MATRIX.md']:
        text=(ROOT/rel).read_text()
        require(set(re.findall(r'CLM-\d{4}',text))<=claim_ids, f'Second-challenge individual claim references resolve in {rel}')
        for start,end in re.findall(r'CLM-(\d{4})[–-](\d{4})',text):
            require({f'CLM-{n:04}' for n in range(int(start),int(end)+1)}<=claim_ids, f'Second-challenge claim range resolves in {rel}')

r03_map=data.get('08-qa/R03-record-map.json')
if r03_map:
    require(len(r03_map['source_map'])==17 and set(r03_map['source_map'].values())<=source_ids, 'Seventeen R03 source routes resolve')
    require(len(r03_map['claim_map'])==29 and set(r03_map['claim_map'].values())<=claim_ids, 'Twenty-nine R03 claim/guardrail records resolve')
    require(next(c for c in claims if c['claim_id']==r03_map['claim_map']['DEL-C05'])['status']=='hold_universal_ui_behaviour', 'R03 current UI behaviour limitation preserved')
    options=data['03-report/R03-option-map.json']
    require([r['option_id'] for r in options['records']]==[f'P{i:02}' for i in range(1,9)], 'Eight ordered R03 options retained')
    require(options['ranking'] is False and options['tested_products'] is False and options['practitioner_observations']==0, 'R03 analytical map not misreported as product ranking or trial')
    for rel in ['03-report/R03-DESKTOP-READOUT.md','03-report/R03-OPTIONS-AND-TRADEOFFS.md']:
        text=(ROOT/rel).read_text()
        require(set(re.findall(r'CLM-\d{4}',text))<=claim_ids, f'R03 individual claim references resolve in {rel}')
        for start,end in re.findall(r'CLM-(\d{4})[–-](\d{4})',text):
            require({f'CLM-{n:04}' for n in range(int(start),int(end)+1)}<=claim_ids, f'R03 claim range resolves in {rel}')

r03_second=data.get('08-qa/R03-second-check-record-map.json')
if r03_second:
    require(len(r03_second['source_map'])==12 and set(r03_second['source_map'].values())<=source_ids, 'Twelve R03 second-challenge routes resolve')
    require(len(r03_second['claim_map'])==18 and set(r03_second['claim_map'].values())<=claim_ids, 'Eighteen R03 second-challenge claims resolve')
    bridge=data['08-qa/R03-prior-study-bridge-check.json']
    require(bridge['status']=='passed' and all(c['passed'] for c in bridge['checks']), 'Independent R03 prior-study bridge checks passed')
    option_map=data['03-report/R03-option-map.json']
    require(len(option_map['cross_cutting_conditions'])==5, 'Five selective R03 lifecycle/context conditions recorded')
    require(option_map['unaided_participant_priorities_first'] and option_map['prior_prompt_scenarios_are_constructed'], 'Constructed prior scenarios cannot replace unaided priorities')
    require('leadership' in option_map['records'][7]['response'].lower(), 'P08 accommodates leadership rather than only time-bound cover')
    for rel in ['03-report/R03-SECOND-CHECK-READOUT.md','03-report/R03-OPTIONS-AND-TRADEOFFS.md']:
        text=(ROOT/rel).read_text()
        require(set(re.findall(r'CLM-\d{4}',text))<=claim_ids, f'R03 second-check individual references resolve in {rel}')
        for start,end in re.findall(r'CLM-(\d{4})[–-](\d{4})',text):
            require({f'CLM-{n:04}' for n in range(int(start),int(end)+1)}<=claim_ids, f'R03 second-check claim range resolves in {rel}')

r04=data.get('08-qa/R04-record-map.json')
if r04:
    require(len(r04['source_map'])==13 and set(r04['source_map'].values())<=source_ids, 'R04 twelve new routes and one explicit reused candidate resolve')
    require(r04['source_map']['GOV4-REUSE01']=='SRC-0131', 'R04 operating documentation reuses its canonical route')
    require(len(r04['claim_map'])==26 and set(r04['claim_map'].values())<=claim_ids, 'Twenty-six bounded R04 claims and guardrails resolve')
    model=data['03-report/R04-decision-map.json']
    require([f['function_id'] for f in model['functions']]==[f'F{i:02}' for i in range(1,13)], 'Twelve R04 analytical functions retained')
    require(all(not f['mandatory'] and not f['distinct_person_required'] for f in model['functions']), 'R04 functions are optional and need not be distinct posts')
    require(not model['universal_workflow'] and not model['mandatory_sequence'] and not model['validated_framework'] and not model['ranking'], 'R04 map not misreported as a universal sequence or validated ranking')
    require(model['original_practitioner_observations']==0 and model['participant_observations']==[], 'R04 published examples not counted as original practitioner observations')
    require(len(model['published_case_examples'])==6 and all(not c['original_JGA_contribution'] for c in model['published_case_examples']), 'Six selected secondary cases remain distinct from JGA fieldwork')
    functions={f['function_id'] for f in model['functions']}
    for c in model['published_case_examples']:
        require(set(c['source_ids'])<=source_ids and set(c['claim_ids'])<=claim_ids, f"R04 case evidence resolves for {c['case_id']}")
        require(set(c['relevant_function_ids'])<=functions, f"R04 case functions resolve for {c['case_id']}")
    require(set(model['supporting_claim_ids'])<=claim_ids, 'R04 structured supporting evidence resolves')
    require(not model['full_committee_map_required'] and not model['confidential_documents_required'] and not model['personal_names_required'], 'R04 minimum case does not require confidential complete committee records')
    require(model['extra_mandatory_questions']==0 and model['fourteen_core_questions_unchanged'] and model['unaided_account_first'], 'R04 worksheet does not expand the core or lead with role examples')
    require(all(v is None for v in model['blank_event_template'].values()), 'R04 blank analytical template contains no invented participant data')
    for ident in ['SRC-0153','SRC-0157']:
        src=next(s for s in sources if s['source_id']==ident)
        require(not src['capture_path'] and bool(src['review_extracts']), f'Parsed extract not counted as raw original for {ident}')
    for ident in ['SRC-0160','SRC-0161','SRC-0162']:
        require(not next(s for s in sources if s['source_id']==ident)['capture_path'], f'Unavailable local original not invented for {ident}')
    captured={r['path']:r for r in data['08-qa/R04-captures.json']['files']}
    for ending in ['BUY-S01-purplebricks.html','BUY-S01-purplebricks.txt']:
        row=next(r for path,r in captured.items() if path.endswith('/'+ending))
        require(row['kind']=='excluded_access_response', f'Access-error payload excluded for {ending}')
    for c in claims:
        if c.get('r04_claim_candidate_id','').startswith('GOV4-') and c['r04_claim_candidate_id']!='GOV4-C06':
            require('rendered and visually checked' not in c['review_mode'], f'GovS006 visual review not misattributed in {c["claim_id"]}')
    for rel in ['03-report/R04-DESKTOP-READOUT.md','03-report/R04-DECISION-PATHWAY.md','03-report/modules/R04-decision-authority-and-pathways.md']:
        text=(ROOT/rel).read_text()
        require(set(re.findall(r'CLM-\d{4}',text))<=claim_ids, f'R04 individual claim references resolve in {rel}')
        for start,end in re.findall(r'CLM-(\d{4})[–-](\d{4})',text):
            require({f'CLM-{n:04}' for n in range(int(start),int(end)+1)}<=claim_ids, f'R04 claim range resolves in {rel}')

r04_second=data.get('08-qa/R04-second-check-record-map.json')
if r04_second:
    require(len(r04_second['source_map'])==9 and set(r04_second['source_map'].values())<=source_ids, 'Nine R04 second-check new routes resolve')
    require(len(r04_second['claim_map'])==16 and set(r04_second['claim_map'].values())<=claim_ids, 'Sixteen R04 second-check claim and method records resolve')
    model=data['03-report/R04-decision-map.json']
    require([c['condition_id'] for c in model['cross_cutting_conditions']]==[f'C{i:02}' for i in range(1,6)], 'Five selective R04 conditions recorded')
    require(all(not c['mandatory'] and set(c['supporting_claim_ids'])<=claim_ids for c in model['cross_cutting_conditions']), 'R04 conditions are optional and evidence-linked')
    require(len(model['secondary_challenge_examples'])==3 and all(not c['original_JGA_contribution'] for c in model['secondary_challenge_examples']), 'Second-check examples do not inflate original fieldwork')
    for c in model['secondary_challenge_examples']:
        require(set(c['source_ids'])<=source_ids and set(c['claim_ids'])<=claim_ids, f"R04 second-check example evidence resolves for {c['example_id']}")
    require(model['prior_prompt_scenarios_are_constructed'] and not model['prior_recommendation_counts_reused'] and model['unaided_participant_priorities_first'], 'Prior constructed prompts cannot become buyer authority or demand evidence')
    require(model['additional_mandatory_questions_from_second_challenge']==0, 'Second R04 review adds no compulsory questions')
    bridge=data['08-qa/R04-prior-study-bridge-check.json']
    require(bridge['status']=='passed' and len(bridge['checks'])==243 and all(c['passed'] for c in bridge['checks']), 'Independent R04 prior-study bridge passed243 checks')
    import hashlib
    require(hashlib.sha256((ROOT/bridge['bridge_path']).read_bytes()).hexdigest()==bridge['bridge_sha256'], 'Independently checked R04 bridge remains unchanged')
    snapshots=data['03-report/research-notes/r04-second-check/before-review/manifest.json']['files']
    original={r['path']:r['sha256'] for r in data['08-qa/R04-completion-check.json']['artifacts']}
    for s in snapshots:
        require(hashlib.sha256((ROOT/s['snapshot_path']).read_bytes()).hexdigest()==s['sha256']==original[s['original_path']], f"First-pass R04 snapshot preserved for {s['original_path']}")
    old_map=next(s for s in snapshots if s['original_path']=='03-report/R04-decision-map.json')
    old=json.loads((ROOT/old_map['snapshot_path']).read_text())
    require(model['functions']==old['functions'] and model['published_case_examples']==old['published_case_examples'], 'Twelve first-pass functions and six original secondary examples preserved')
    for ident in ['SRC-0165','SRC-0169']:
        src=next(s for s in sources if s['source_id']==ident)
        require(not src['capture_path'] and bool(src['review_extracts']), f'Second-check parsed extract not mislabelled raw original for {ident}')
    for rel in ['03-report/R04-SECOND-CHECK-READOUT.md','03-report/R04-DESKTOP-READOUT.md','03-report/R04-DECISION-PATHWAY.md']:
        text=(ROOT/rel).read_text()
        require(set(re.findall(r'CLM-\d{4}',text))<=claim_ids, f'R04 second-check individual claims resolve in {rel}')
        for start,end in re.findall(r'CLM-(\d{4})[–-](\d{4})',text):
            require({f'CLM-{n:04}' for n in range(int(start),int(end)+1)}<=claim_ids, f'R04 second-check claim range resolves in {rel}')

r05=data.get('08-qa/R05-record-map.json')
if r05:
    require(len(r05['source_map'])==10 and set(r05['source_map'].values())<=source_ids, 'R05 source candidates resolve with canonical reuse')
    require(r05['source_map']['ECO5-S01']=='SRC-0074', 'Efficiency Framework reinspection is not a new independent source')
    require(len(r05['claim_map'])==28 and set(r05['claim_map'].values())<=claim_ids, 'Twenty-eight R05 claim/method records resolve')
    model=data['03-report/R05-evidence-map.json']
    require([r['domain_id'] for r in model['domains']]==[f'E{i:02}' for i in range(1,10)], 'Nine R05 domains present')
    require(all(not r['mandatory'] and not r['scored'] and set(r['supporting_claim_ids'])<=claim_ids for r in model['domains']), 'R05 domains optional unscored and evidence-linked')
    require([v['view_id'] for v in model['financial_views']]==['V01','V02','V03'], 'Resource cash and funding views retained separately')
    require(not model['ranking'] and not model['mandatory_sequence'] and not model['validated_framework'] and not model['universal_rate_or_risk_threshold'], 'R05 map not a mandatory ranking or prescribed hurdle/risk score')
    require(model['participant_observations']==[] and model['employer_forecasts']==[] and model['calculations']==[] and not model['financial_inputs_populated'] and model['new_numeric_estimates']==0, 'R05 has no invented observations forecasts calculations or financial inputs')
    require(not model['evidence_state_labels_are_ordinal_score'] and model['extra_mandatory_questions']==0 and model['fourteen_core_questions_unchanged'] and model['unaided_case_first'], 'R05 state labels are not a score or new questionnaire')
    require(all(v is None for v in model['blank_evidence_template'].values()), 'R05 evidence template remains blank')
    for c in model['reference_contexts']:
        require(set(c['source_ids'])<=source_ids and set(c['claim_ids'])<=claim_ids and not c['original_JGA_contribution'], f"R05 published context bounded and linked for {c['context_id']}")
    require(set(model['supporting_claim_ids'])<=claim_ids, 'R05 structured claims resolve')
    original=next(s for s in sources if s['source_id']==r05['source_map']['R5COM-S01'])
    require(not original['capture_path'] and bool(original['review_extracts']), 'BrightPay billing reader extract not called a raw original')
    for rel in ['03-report/R05-DESKTOP-READOUT.md','03-report/R05-BUSINESS-CASE-CHECKLIST.md','03-report/modules/R05-business-case-evidence-and-risks.md']:
        text=(ROOT/rel).read_text()
        require(set(re.findall(r'CLM-\d{4}',text))<=claim_ids, f'R05 individual evidence references resolve in {rel}')
        for start,end in re.findall(r'CLM-(\d{4})[–-](\d{4})',text):
            require({f'CLM-{n:04}' for n in range(int(start),int(end)+1)}<=claim_ids, f'R05 claim range resolves in {rel}')
    import hashlib
    for r in data['08-qa/R05-baseline-manifest.json']['files']:
        require(hashlib.sha256((ROOT/r['path']).read_bytes()).hexdigest()==r['sha256'], f"Prior topic/core artifact unchanged during R05: {r['path']}")

r05_second=data.get('08-qa/R05-second-check-record-map.json')
if r05_second:
    require(len(r05_second['source_map'])==12 and set(r05_second['source_map'].values())<=source_ids, 'Twelve R05 second-challenge routes resolve')
    require(len(r05_second['claim_map'])==21 and set(r05_second['claim_map'].values())<=claim_ids, 'Twenty-one R05 second-challenge claim/method records resolve')
    model=data['03-report/R05-evidence-map.json']
    require([c['condition_id'] for c in model['cross_cutting_conditions']]==[f'C{i:02}' for i in range(1,6)], 'Five selective R05 second-challenge conditions present')
    domains={x['domain_id'] for x in model['domains']}
    for c in model['cross_cutting_conditions']:
        require(not c['mandatory'] and not c['scored'] and set(c['domain_ids'])<=domains and set(c['supporting_claim_ids'])<=claim_ids, f"R05 optional condition references resolve for {c['condition_id']}")
    require(model['additional_mandatory_questions_from_second_challenge']==0 and model['prior_prompt_scenarios_are_constructed'] and not model['prior_recommendation_counts_reused'] and model['unaided_participant_priorities_first'], 'R05 second challenge adds no compulsory questions or buyer-priority inference')
    require(all(v is None for v in model['second_challenge_blank_context_template'].values()), 'R05 second-challenge context template remains blank')
    bridge=data['08-qa/R05-prior-study-bridge-check.json']
    require(bridge['status']=='passed' and bridge['check_count']==327 and all(c['passed'] for c in bridge['checks']), 'Independent R05 bridge passes327 exact saved-data checks')
    require(bridge['selected_questions']==4 and bridge['selected_saved_answers']==32 and bridge['no_model_reruns'], 'R05 bridge scope is four constructed questions and32 saved texts without reruns')
    require(hashlib.sha256((ROOT/bridge['bridge_path']).read_bytes()).hexdigest()==bridge['bridge_sha256'], 'Checked R05 bridge remains unchanged')
    snapshots=data['03-report/research-notes/r05-second-check/before-review/manifest.json']['records']
    for x in snapshots:
        require(hashlib.sha256((ROOT/x['snapshot_path']).read_bytes()).hexdigest()==x['sha256'], f"First-pass R05 snapshot preserved for {x['original_path']}")
    first_completion=json.loads((ROOT/next(x['snapshot_path'] for x in snapshots if x['original_path']=='08-qa/R05-completion-check.json')).read_text())
    artifact_hashes={x['path']:x['sha256'] for x in first_completion['artifacts']}
    for x in snapshots:
        if x['original_path'] in artifact_hashes:require(x['sha256']==artifact_hashes[x['original_path']], f"R05 original completion reconciles to snapshot {x['original_path']}")
    original_map=json.loads((ROOT/next(x['snapshot_path'] for x in snapshots if x['original_path']=='03-report/R05-evidence-map.json')).read_text())
    for k in ['domains','financial_views','blank_evidence_template','template_fields','current_question_ids','reference_contexts']:
        require(model[k]==original_map[k], f'R05 first-pass {k} unchanged')
    for x in data['08-qa/R05-second-check-baseline.json']['records']:
        require(hashlib.sha256((ROOT/x['path']).read_bytes()).hexdigest()==x['sha256'], f"Earlier/client/core preservation for R05 second challenge: {x['path']}")
    for x in data['08-qa/R05-second-check-captures.json']['files']:
        require(hashlib.sha256((ROOT/x['path']).read_bytes()).hexdigest()==x['sha256'], f"Second-challenge capture hash matches {x['path']}")
    for ident in ['SRC-0190','SRC-0191']:
        s=next(s for s in sources if s['source_id']==ident)
        require(not s['capture_path'] and bool(s['review_extracts']), f'R05 second-challenge extract not mislabelled raw for {ident}')
    for c in model['second_challenge_reference_contexts']:
        require(not c['original_JGA_contribution'] and set(c['source_ids'])<=source_ids and set(c['claim_ids'])<=claim_ids, f"R05 historical context is not original fieldwork: {c['context_id']}")
    require((ROOT/'08-qa/R05-second-check-independent-review.md').is_file(), 'R05 second-challenge integrated review retained')
    for rel in ['03-report/R05-SECOND-CHECK-READOUT.md','03-report/R05-BUSINESS-CASE-CHECKLIST.md']:
        text=(ROOT/rel).read_text()
        require(set(re.findall(r'CLM-\d{4}',text))<=claim_ids, f'R05 second-challenge individual claims resolve in {rel}')
        for start,end in re.findall(r'CLM-(\d{4})[–-](\d{4})',text):
            require({f'CLM-{n:04}' for n in range(int(start),int(end)+1)}<=claim_ids, f'R05 second-challenge claim range resolves in {rel}')

r06=data.get('08-qa/R06-record-map.json')
if r06:
    require(len(r06['source_map'])==10 and set(r06['source_map'].values())<=source_ids, 'Ten R06 primary source routes resolve')
    require(len(r06['claim_map'])==23 and set(r06['claim_map'].values())<=claim_ids, 'Twenty-three R06 claim/method records resolve')
    model=data['03-report/R06-outcome-map.json']
    require(model['decision_dispositions']==['approved','declined','deferred','withdrawn_abandoned','pending','no_formal_approval_required','not_known','prefer_not_to_disclose'], 'R06 dispositions retain existing Q007 vocabulary')
    require(not model['validated_framework'] and not model['ranking'] and not model['mandatory_sequence'] and not model['universal_workflow'] and not model['fields_are_ordinal'], 'R06 map is not a validated ranked universal workflow')
    require(len(model['matrix_rows'])==9 and all(not x['mandatory'] and not x['scored'] and not x['remedy_validated'] for x in model['matrix_rows']), 'Nine optional R06 rows do not assert scored/validated remedies')
    for x in model['matrix_rows']:require(set(x['supporting_claim_ids'])<=claim_ids, f"R06 matrix claims resolve for {x['row_id']}")
    require(len(model['published_employer_contexts'])==6 and all(not x['original_JGA_contribution'] for x in model['published_employer_contexts']), 'Six R06 selected public employer contexts not counted as original contributions')
    for x in model['published_employer_contexts']:require(set(x['source_ids'])<=source_ids and set(x['claim_ids'])<=claim_ids, f"R06 public context evidence resolves for {x['case_id']}")
    cases={x['case_id']:x for x in model['published_employer_contexts']}
    require(cases['PC04']['normalised_proposal_disposition'] is None and len(cases['PC04']['events'])==2 and all(x['normalised_investment_disposition'] is None for x in cases['PC04']['events']), 'R06 West Sussex scoped delivery events do not invent investment disposition')
    require(cases['PC05']['historical_context_only'] and not cases['PC05']['eligible_for_recent_practitioner_window'] and cases['PC05']['event_date']=='2001-05', 'R06 historical component case cannot enter recent practitioner window')
    require(cases['PC06']['normalised_proposal_disposition'] is None and cases['PC06']['benefit_status']=='not_established', 'R06 OEP operational management account does not invent approval or benefit')
    require(all(not x['actual_signed_contract_verified'] for x in cases.values()), 'R06 selected public records not reported as inspected signed contracts')
    require(len(model['notice_status_contexts'])==1, 'R06 narrow notice context is separate from employer case count')
    x=model['notice_status_contexts'][0]
    require(x['normalised_proposal_disposition'] is None and x['underlying_upgrade_abandoned'] is None and x['cancellation_date'] is None and x['cancellation_reason'] is None and not x['commencement_of_procurement_established'] and not x['original_JGA_contribution'], 'R06 cancelled advance notice does not invent tender/upgrade abandonment')
    require(set(x['source_ids'])<=source_ids and set(x['claim_ids'])<=claim_ids, 'R06 notice context references resolve')
    require(model['option_is_not_decision_disposition'] and model['no_status_inferred_from_silence'] and model['preproposal_is_separate_route'] and model['rollout_delay_is_not_automatically_deferred_investment'] and model['reason_and_remedy_are_separate'], 'R06 object disposition timing and remedy boundaries retained')
    require(model['anticipated_trigger_is_not_completed_switch'] and model['stated_premium_is_not_funded_purchase'] and model['source_population_and_item_base_separate'], 'R06 buyer measures not converted into observed purchasing')
    require(model['participant_observations']==[] and model['forecast_calculations']==[] and model['causal_remedies_tested']==[] and model['original_practitioner_observations']==0 and model['product_trials']==0 and model['new_numeric_estimates']==0 and not model['financial_inputs_populated'], 'R06 has no invented fieldwork forecasts numeric outcome estimates or validated remedies')
    require(model['extra_mandatory_questions']==0 and model['fourteen_core_questions_unchanged'] and model['unaided_case_first'] and not model['confidential_documents_required'], 'R06 preserves fourteen core questions and proportional disclosure')
    require(all(v is None for v in model['blank_event_template'].values()), 'R06 event template remains blank')
    require(set(model['supporting_claim_ids'])<=claim_ids, 'R06 structured supporting claims resolve')
    for ident in ['SRC-0195','SRC-0196','SRC-0197']:
        x=next(x for x in sources if x['source_id']==ident)
        require(not x['capture_path'] and bool(x['review_extracts']), f'R06 selected reader note not promoted to original for {ident}')
    for ident in ['CLM-0051','CLM-0052']:require(next(c for c in claims if c['claim_id']==ident)['status']=='quarantined_conflicting', f'R06 preserves Moorepay numerical quarantine {ident}')
    for x in data['08-qa/R06-baseline-manifest.json']['files']:
        require(hashlib.sha256((ROOT/x['path']).read_bytes()).hexdigest()==x['sha256'], f"R06 earlier topic/client/core artifact preserved {x['path']}")
    for x in data['08-qa/R06-captures.json']['files']:
        require(hashlib.sha256((ROOT/x['path']).read_bytes()).hexdigest()==x['sha256'], f"R06 retained-file hash matches {x['path']}")
    review=data['08-qa/r06-review/integration-check.json']
    require(review['status']=='passed' and all(x['passed'] for x in review['checks']), 'R06 independent bounded integration checks pass')
    require((ROOT/'08-qa/R06-independent-review.md').is_file(), 'R06 independent integrated review retained')
    for rel in ['03-report/R06-DESKTOP-READOUT.md','03-report/R06-BARRIER-RESPONSE-MATRIX.md','03-report/modules/R06-staying-switching-delay-and-abandonment.md']:
        text=(ROOT/rel).read_text()
        require(set(re.findall(r'CLM-\d{4}',text))<=claim_ids, f'R06 individual claim references resolve in {rel}')
        for start,end in re.findall(r'CLM-(\d{4})[–-](\d{4})',text):
            require({f'CLM-{n:04}' for n in range(int(start),int(end)+1)}<=claim_ids, f'R06 claim range resolves in {rel}')

r06_second=data.get('08-qa/R06-second-check-record-map.json')
if r06_second:
    require(len(r06_second['source_map'])==8 and set(r06_second['source_map'].values())<=source_ids, 'Eight R06 second-challenge primary routes resolve')
    require(len(r06_second['claim_map'])==19 and set(r06_second['claim_map'].values())<=claim_ids, 'Nineteen R06 second-challenge claims resolve')
    model=data['03-report/R06-outcome-map.json']
    require([x['condition_id'] for x in model['cross_cutting_conditions']]==[f'C{i:02}' for i in range(1,6)], 'Five R06 selective second-challenge conditions present')
    for x in model['cross_cutting_conditions']:
        require(not x['mandatory'] and not x['scored'] and not x['remedy_validated'] and set(x['supporting_claim_ids'])<=claim_ids, f"R06 second-challenge condition bounded and linked: {x['condition_id']}")
    require(model['additional_mandatory_questions_from_second_challenge']==0 and model['prior_prompt_scenarios_are_constructed'] and not model['prior_recommendation_counts_reused'] and model['unaided_participant_priorities_first'], 'R06 prior constructed prompts do not add questions or infer demand')
    require(all(v is None for v in model['second_challenge_blank_context_template'].values()), 'R06 second-challenge context template remains blank')
    require(len(model['second_challenge_contexts'])==1, 'One additional LFB programme history, not one employer per document')
    x=model['second_challenge_contexts'][0]
    require(not x['original_JGA_contribution'] and x['independent_employer_histories']==1 and not x['later_go_live_observed'] and x['later_outcome'] is None and x['normalised_current_proposal_disposition'] is None and x['forecast_dates_are_not_observed_events'], 'R06 LFB history does not invent later outcomes/current status or fieldwork')
    require(set(x['source_ids'])<=source_ids and set(x['claim_ids'])<=claim_ids, 'R06 LFB history links resolve')
    snapshots=data['03-report/research-notes/r06-second-check/before-review/manifest.json']['records']
    for x in snapshots:require(hashlib.sha256((ROOT/x['snapshot_path']).read_bytes()).hexdigest()==x['sha256'], f"First-pass R06 snapshot preserved {x['original_path']}")
    first_completion=json.loads((ROOT/next(x['snapshot_path'] for x in snapshots if x['original_path']=='08-qa/R06-completion-check.json')).read_text())
    oldhash={x['path']:x['sha256'] for x in first_completion['artifacts']}
    for x in snapshots:
        if x['original_path'] in oldhash:require(x['sha256']==oldhash[x['original_path']], f"R06 first-pass completion reconciles to snapshot {x['original_path']}")
    old=json.loads((ROOT/next(x['snapshot_path'] for x in snapshots if x['original_path']=='03-report/R06-outcome-map.json')).read_text())
    for k in ['matrix_rows','published_employer_contexts','notice_status_contexts','blank_event_template','decision_dispositions','current_question_ids']:
        require(model[k]==old[k], f'R06 first-pass {k} unchanged after second challenge')
    for x in data['08-qa/R06-second-check-baseline.json']['records']:
        require(hashlib.sha256((ROOT/x['path']).read_bytes()).hexdigest()==x['sha256'], f"R06 second-challenge prior/client/core preservation {x['path']}")
    for x in data['08-qa/R06-second-check-captures.json']['files']:
        require(hashlib.sha256((ROOT/x['path']).read_bytes()).hexdigest()==x['sha256'], f"R06 second-challenge retained file hash {x['path']}")
    bridge=data['08-qa/R06-prior-study-bridge-check.json']
    require(bridge['status']=='passed' and bridge['check_count']==250 and all(x['passed'] for x in bridge['checks']), 'R06 saved-study bridge passes250 root exact-linkage checks')
    require(bridge['selected_questions']==3 and bridge['selected_saved_answers']==24 and bridge['no_model_reruns'], 'R06 bridge remains three constructed questions and24 saved texts without reruns')
    require(hashlib.sha256((ROOT/bridge['bridge_path']).read_bytes()).hexdigest()==bridge['bridge_sha256'], 'Verified R06 second-challenge bridge unchanged')
    peer=data['08-qa/R06-second-check-peer-checks.json'];rootcheck=data['08-qa/R06-second-check-root-verification.json']
    require(peer['status']=='passed' and peer['check_count']==25 and all(x['passed'] for x in peer['checks']), 'R06 scoped peer checks passed without own-strand independence claim')
    require(rootcheck['status']=='passed_targeted_root_verification' and all(x['passed'] for x in rootcheck['checks']), 'R06 separately authored competitor input root verification passed')
    require('not fully independent' in model['second_challenge_review_basis'], 'R06 partial-review independence is explicit')
    require((ROOT/'08-qa/R06-second-check-peer-review.md').is_file(), 'R06 scoped peer review retained')
    for ident in ['SRC-0205','SRC-0209','SRC-0210']:
        x=next(x for x in sources if x['source_id']==ident)
        require(not x['capture_path'] and bool(x['review_extracts']), f'R06 second-check reader notes not promoted to raw original: {ident}')
    for rel in ['03-report/R06-SECOND-CHECK-READOUT.md','03-report/R06-BARRIER-RESPONSE-MATRIX.md','03-report/modules/R06-staying-switching-delay-and-abandonment.md']:
        text=(ROOT/rel).read_text()
        require(set(re.findall(r'CLM-\d{4}',text))<=claim_ids, f'R06 second-challenge individual claims resolve in {rel}')
        for start,end in re.findall(r'CLM-(\d{4})[–-](\d{4})',text):
            require({f'CLM-{n:04}' for n in range(int(start),int(end)+1)}<=claim_ids, f'R06 second-challenge claim range resolves in {rel}')

r07=data.get('08-qa/R07-record-map.json')
if r07:
    require(len(r07['source_map'])==4 and set(r07['source_map'].values())<=source_ids, 'Four R07 new official routes resolve')
    require(len(r07['claim_map'])==24 and set(r07['claim_map'].values())<=claim_ids, 'Twenty-four R07 claim/method/hold records resolve')
    require(r07['original_JGA_participants']==0 and r07['employer_forecasts']==0 and r07['product_tests']==0, 'R07 mapping does not invent empirical collection or tests')
    for ident in r07['source_map'].values():
        x=next(x for x in sources if x['source_id']==ident)
        require(bool(x['capture_path']) and x['capture_path'].endswith('.html'), f'R07 official route retains original HTML: {ident}')
        require(x['publication_eligibility']=='R07_context_final_use_pending', f'R07 source final-use approval not inferred: {ident}')
    for ident in r07['claim_map'].values():
        x=next(x for x in claims if x['claim_id']==ident)
        require(x['value'] is None and x['metric'] is None, f'R07 does not adopt a new numeric estimate: {ident}')
    require(next(c for c in claims if c['claim_id']==r07['claim_map']['PRI7-C07'])['status']=='hold_numeric_reuse', 'R07 new Moorepay feature conflict remains held')
    for ident in ['CLM-0051','CLM-0052']:
        require(next(c for c in claims if c['claim_id']==ident)['status']=='quarantined_conflicting', f'R07 preserves prior Moorepay quarantine: {ident}')
    for ident in ['CLM-0167','CLM-0168']:
        require(next(c for c in claims if c['claim_id']==ident)['status']=='hold_numeric_reuse', f'R07 preserves prior Deloitte hold: {ident}')
    require(next(c for c in claims if c['claim_id']=='CLM-0218')['status']=='hold_universal_ui_behaviour', 'R07 preserves prior UI-behaviour boundary')
    model=data['03-report/R07-priority-map.json']
    require(model['status']=='completed_internal_desktop_synthesis_practitioner_integration_pending', 'R07 completed only for internal desktop synthesis')
    require(model['primary_priority_question_id']=='Q005' and model['maximum_selective_priorities']==2 and model['horizon_months']==[12,24], 'R07 uses existing Q005 two-priority horizon')
    require(model['fourteen_core_questions_unchanged'] and model['extra_mandatory_questions']==0 and model['unaided_priorities_first'] and model['prompted_themes_labelled'], 'R07 selective design preserves question and prompting boundaries')
    require(not model['ordinal_status_ladder'] and not model['mandatory_sequence'] and not model['validated_priority_score'], 'R07 facts are not a maturity or sequential status ladder')
    require(model['fields_are_selective_analyst_aids'] and not model['confidential_documents_required'] and not model['exact_private_amounts_required'], 'R07 does not demand confidential complete financial records')
    require(model['original_practitioner_observations']==0 and model['new_empirical_datasets']==0 and model['new_numeric_estimates']==0 and not model['financial_inputs_populated'], 'R07 sources do not become original observations forecasts or estimates')
    for k in ['participant_observations','completed_case_comparisons','forecast_calculations','subgroup_estimates','market_rankings']:
        require(model[k]==[], f'R07 unperformed empirical work remains empty: {k}')
    for k in ['blank_priority_template','blank_context_template','blank_comparison_template']:
        require(bool(model[k]) and all(v is None for v in model[k].values()), f'R07 template remains unpopulated: {k}')
    require(set(model['missingness_values'])=={'not_known','not_measured','not_applicable','not_disclosed'}, 'R07 missingness categories remain distinct')
    require(len(model['priority_dimensions'])==6 and len(model['context_dimensions'])==6 and len(model['comparison_claim_purposes'])==4 and len(model['planning_signals'])==3, 'R07 selective priority/context/comparison/planning dimensions retained')
    for x in model['priority_dimensions']:
        require(set(x['claim_ids'])<=claim_ids, f"R07 priority dimension evidence resolves: {x['dimension_id']}")
    for x in model['context_dimensions']:
        require(not x['mandatory'] and not x['scored'] and set(x['claim_ids'])<=claim_ids, f"R07 optional context evidence resolves: {x['context_id']}")
    for x in model['comparison_claim_purposes']:
        require(not x['ordinal'] and set(x['claim_ids'])<=claim_ids, f"R07 nonordinal comparison purpose resolves: {x['claim_type']}")
    for x in model['planning_signals']:
        require(x['organisation_status'] is None and set(x['source_ids'])<=source_ids and set(x['claim_ids'])<=claim_ids, f"R07 external signal does not invent employer commitment: {x['signal_id']}")
    require(model['planning_signals'][0]['external_status']=='current_official_guidance_context' and model['planning_signals'][1]['external_status']=='draft_interim_future_guidance', 'R07 current SSP guidance and interim future BiK context remain distinct')
    require(set(model['supporting_claim_ids'])<=claim_ids and model['no_external_sending_without_user_permission'], 'R07 supporting evidence and sending boundary resolve')
    for x in data['08-qa/R07-baseline-manifest.json']['files']:
        require(hashlib.sha256((ROOT/x['path']).read_bytes()).hexdigest()==x['sha256'], f"R07 prior/core/client file preserved: {x['path']}")
    for x in data['08-qa/R07-captures.json']['files']:
        require(hashlib.sha256((ROOT/x['path']).read_bytes()).hexdigest()==x['sha256'], f"R07 retained source/review file hash matches: {x['path']}")
        if x['path'].endswith('/MP-feature.png'):
            require(x['kind']=='published_chart_asset', 'R07 downloaded publisher chart distinguished from rendered PDF page')
        if x['path'].endswith('.txt'):
            require(x['kind']=='parsed_or_selected_extract', 'R07 text extract not promoted to retained original')
    failed=[x for x in data['03-report/research-notes/r07/signals/capture-manifest.json']['records'] if x.get('http_status') in [202,403]]
    require(len(failed)==2 and all(not x.get('path') and x['evidence_status'].startswith('excluded') for x in failed), 'R07 empty legislation and blocked Powys are excluded, not inspected originals')
    require(not any('legislation.gov.uk/uksi/2026/373' in x['url'] or 'powys.moderngov.co.uk/documents/g9862' in x['url'] for x in sources if x.get('r07_source_candidate_id')), 'R07 excludes unsupported screened routes from new source evidence')
    review=data['08-qa/r07-review/integrated-review-checks.json']
    require(review['status']=='passed_for_internal_R07_desktop_synthesis' and all(x['passed'] for x in review['checks']), 'R07 independent integrated review passed')
    require((ROOT/'08-qa/R07-independent-review.md').is_file(), 'R07 independent review preserved')
    for rel in ['03-report/R07-DESKTOP-READOUT.md','03-report/R07-CONTEXTUAL-PRIORITIES.md','03-report/modules/R07-priorities-and-contextual-differences.md']:
        text=(ROOT/rel).read_text()
        require(set(re.findall(r'CLM-\d{4}',text))<=claim_ids, f'R07 individual claim references resolve: {rel}')
        for start,end in re.findall(r'CLM-(\d{4})[–-](\d{4})',text):
            require({f'CLM-{n:04}' for n in range(int(start),int(end)+1)}<=claim_ids, f'R07 claim range resolves: {rel}')

r07_second=data.get('08-qa/R07-second-check-record-map.json')
if r07_second:
    require(len(r07_second['source_map'])==7 and set(r07_second['source_map'].values())<=source_ids, 'Seven R07 second-challenge primary routes resolve')
    require(len(r07_second['claim_map'])==19 and set(r07_second['claim_map'].values())<=claim_ids, 'Nineteen R07 second-challenge claim/design records resolve')
    require(r07_second['original_JGA_participants']==0 and r07_second['employer_forecasts']==0 and r07_second['product_tests']==0, 'R07 second challenge adds no invented original data or tests')
    model=data['03-report/R07-priority-map.json']
    require(model['second_challenge_status']=='completed_internal_desktop_review_practitioner_integration_pending', 'R07 second challenge completed only for internal desktop synthesis')
    require([x['condition_id'] for x in model['cross_cutting_conditions']]==[f'C{i:02}' for i in range(1,6)], 'Five R07 second-challenge conditions retained')
    for x in model['cross_cutting_conditions']:
        require(not x['mandatory'] and not x['scored'] and not x['validated'] and set(x['claim_ids'])<=claim_ids, f"R07 second-challenge condition selective and linked: {x['condition_id']}")
    require(model['additional_mandatory_questions_from_second_challenge']==0 and model['prior_prompt_scenarios_are_constructed'] and not model['prior_recommendation_counts_reused'] and not model['prior_model_reruns'] and model['unaided_participant_priorities_first'], 'R07 prior scenarios preserve unaided priorities without count or rerun transfer')
    require(model['second_challenge_selected_question_ids']==['S03-A','S07-A','S08-C','S11-A'] and model['second_challenge_selected_saved_answers']==32, 'R07 four constructed geography/team/role scenarios retain32 saved texts')
    require(model['second_challenge_new_public_employer_histories']==0 and all(v is None for v in model['second_challenge_blank_context_template'].values()), 'R07 reuses do not invent new histories or context observations')
    require(set(model['second_challenge_supporting_claim_ids'])<=claim_ids, 'R07 second-challenge supporting evidence resolves')
    snapshots=data['03-report/research-notes/r07-second-check/before-review/manifest.json']['records']
    require(len(snapshots)==7, 'Seven first-pass R07 artifacts snapshotted')
    for x in snapshots:
        require(hashlib.sha256((ROOT/x['snapshot_path']).read_bytes()).hexdigest()==x['sha256'], f"R07 first-pass snapshot preserved: {x['original_path']}")
    first_completion=json.loads((ROOT/next(x['snapshot_path'] for x in snapshots if x['original_path']=='08-qa/R07-completion-check.json')).read_text())
    oldhash={x['path']:x['sha256'] for x in first_completion['artifacts']}
    for x in snapshots:
        if x['original_path'] in oldhash:
            require(x['sha256']==oldhash[x['original_path']], f"R07 first-pass completion reconciles to snapshot: {x['original_path']}")
    old=json.loads((ROOT/next(x['snapshot_path'] for x in snapshots if x['original_path']=='03-report/R07-priority-map.json')).read_text())
    for k in ['priority_dimensions','context_dimensions','comparison_claim_purposes','planning_signals','blank_priority_template','blank_context_template','blank_comparison_template','current_question_ids']:
        require(model[k]==old[k], f'R07 first-pass structure preserved after second challenge: {k}')
    for x in data['08-qa/R07-second-check-baseline.json']['records']:
        require(hashlib.sha256((ROOT/x['path']).read_bytes()).hexdigest()==x['sha256'], f"R07 second-challenge prior/core/client preservation: {x['path']}")
    for x in data['08-qa/R07-second-check-captures.json']['files']:
        require(hashlib.sha256((ROOT/x['path']).read_bytes()).hexdigest()==x['sha256'], f"R07 second-challenge capture/extract hash: {x['path']}")
        if 'selected-reader-notes' in x['path']:
            require(x['kind']=='parsed_or_selected_extract', 'R07 selected reader note distinct from raw retrieval error and retained original')
    for ident in ['SRC-0218','SRC-0220','SRC-0221']:
        x=next(s for s in sources if s['source_id']==ident)
        require(not x['capture_path'] and bool(x['review_extracts']), f'R07 second-challenge reader-only source not promoted to raw original: {ident}')
    require(next(s for s in sources if s['source_id']=='SRC-0153')['capture_path'] is None, 'R07 GovS002 selected reinspection does not repair absent raw original')
    bridge=data['08-qa/R07-prior-study-bridge-check.json']
    require(bridge['status']=='passed' and bridge['check_count']==327 and all(x['passed'] for x in bridge['checks']), 'R07327 exact saved-study linkage checks passed')
    require(bridge['selected_questions']==4 and bridge['selected_saved_answers']==32 and bridge['no_model_reruns'], 'R07 prior bridge remains four constructed questions/32saved texts with no reruns')
    require(hashlib.sha256((ROOT/bridge['bridge_path']).read_bytes()).hexdigest()==bridge['bridge_sha256'], 'R07 verified bridge unchanged')
    review=data['08-qa/r07-second-review/integration-checks.json']
    require(review['status']=='passed_for_internal_R07_second_challenge' and all(x['passed'] for x in review['checks']), 'R07 second-challenge independent integration checks passed')
    require((ROOT/'08-qa/R07-second-check-independent-review.md').is_file(), 'R07 second-challenge independent review retained')
    for rel in ['03-report/R07-SECOND-CHECK-READOUT.md','03-report/R07-DESKTOP-READOUT.md','03-report/R07-CONTEXTUAL-PRIORITIES.md','03-report/modules/R07-priorities-and-contextual-differences.md']:
        text=(ROOT/rel).read_text()
        require(set(re.findall(r'CLM-\d{4}',text))<=claim_ids, f'R07 second-challenge individual references resolve: {rel}')
        for start,end in re.findall(r'CLM-(\d{4})[–-](\d{4})',text):
            require({f'CLM-{n:04}' for n in range(int(start),int(end)+1)}<=claim_ids, f'R07 second-challenge claim range resolves: {rel}')

r08=data.get('03-report/R08-framework-map.json')
r08_second=data.get('08-qa/R08-second-check-record-map.json')
if r08_second:
    r08_first_snapshots=data['03-report/research-notes/r08-second-check/before-review/manifest.json']['records']
    r08=json.loads((ROOT/next(x['snapshot_path'] for x in r08_first_snapshots if x['original_path']=='03-report/R08-framework-map.json')).read_text())
    r08_canonical_snapshots={x['original_path']:x for x in data['03-report/research-notes/r08-second-check/before-review/canonical-file-manifest.json']['records']}
if r08:
    require(r08['status']=='prepared_internal_desktop_framework_original_integration_pending', 'R08 prepared only for desktop framework pending original integration')
    require(r08['views_are_linked_not_stages'] and not r08['mandatory_sequence'] and not r08['score'] and not r08['validated_predictor'] and not r08['approval_recipe'], 'R08 linked views are not a sequence score predictor or approval recipe')
    require(r08['requires_WP11_original_coding'] and not r08['complete_final_WP15'] and not r08['participant_validated'], 'R08 final practitioner integration dependency remains open')
    require(r08['new_mandatory_questions']==0 and r08['core_question_count']==14 and r08['core_question_version']=='0.2', 'R08 preserves fourteen core questions')
    require(r08['partial_brief_allowed'] and r08['no_case_allowed'] and r08['no_disclosure_allowed'] and not r08['all_views_required'], 'R08 partial no-case and undisclosed accounts remain usable')
    require(not r08['confidential_documents_required'] and not r08['personal_names_required'] and not r08['exact_budget_required'] and not r08['missing_owner_or_date_defaults_to_pending'], 'R08 cannot force sensitive data or missingness-to-pending inference')
    require([x['view_id'] for x in r08['views']]==[f'V{i:02}' for i in range(1,7)], 'Six R08 framework views retained')
    held=set(r08['held_claim_ids_not_positive_support'])
    require(held=={'CLM-0051','CLM-0052','CLM-0167','CLM-0168','CLM-0218','CLM-0392'}, 'R08 all existing numerical/UI holds excluded from positive framework support')
    for x in r08['views']:
        require(not x['mandatory'] and not x['sequence_required'] and not x['scored'] and not x['validated'], f"R08 optional nonordinal view: {x['view_id']}")
        require(set(x['claim_ids'])<=claim_ids and not set(x['claim_ids'])&held and set(x['source_ids'])<=source_ids, f"R08 bounded positive source/claim links: {x['view_id']}")
        require(set(x['finding_ids'])<={f['finding_id'] for f in data['05-analysis/findings.json']['records']}, f"R08 finding links resolve: {x['view_id']}")
        require(set(x['existing_question_ids'])<={f'Q{i:03}' for i in range(1,15)}, f"R08 existing question links resolve: {x['view_id']}")
        require(set(x['selective_record_fields'])==set(r08['blank_canvas'][x['view_id']]) and all(v is None for v in r08['blank_canvas'][x['view_id']].values()), f"R08 blank selective canvas: {x['view_id']}")
    for k in ['blank_scope_template','blank_decision_brief']:
        require(all(v is None for v in r08[k].values()), f'R08 reusable template unpopulated: {k}')
    for k in ['participant_observations','actual_case_records','completed_framework_use_tests','causal_effect_estimates','employer_forecasts','chart_data','financial_inputs']:
        require(r08[k]==[], f'R08 unperformed actual work remains empty: {k}')
    require(r08['new_source_routes']==0 and r08['new_canonical_claims']==0 and r08['new_market_estimates']==0 and r08['new_numeric_scores']==0, 'R08 synthesis creates no new canonical evidence or market estimates')
    require(set(r08['evidence_claims_are_separate'])=={'requested','supplied','accepted_if_known','perceived_influence_and_basis','independently_established_effect_if_claimed'}, 'R08 evidence requested supplied accepted attributed influence and causal effect distinct')
    require({'evidence_acceptance_if_known','perceived_influence_and_basis'}<=set(r08['views'][3]['selective_record_fields']), 'R08 structured acceptance and perceived influence are separate fields')
    require(set(r08['states_are_separate'])=={'proposal_decision','commitment','implementation','benefit_assessment'}, 'R08 approval commitment delivery benefit remain separate states')
    for x in data['08-qa/R08-baseline-manifest.json']['files']:
        target=r08_canonical_snapshots[x['path']]['snapshot_path'] if r08_second and x['path'] in r08_canonical_snapshots else x['path']
        require(hashlib.sha256((ROOT/target).read_bytes()).hexdigest()==x['sha256'], f"R08 prior/client/core/canonical as-of file preserved: {x['path']}")
    r08_findings=json.loads((ROOT/r08_canonical_snapshots['05-analysis/findings.json']['snapshot_path']).read_text())['records'] if r08_second else data['05-analysis/findings.json']['records']
    require(r08_findings==data['08-qa/R08-existing-findings.json']['records'], 'R08 first-pass existing finding content preserved without synthetic results becoming original findings')
    report=data['03-report/R08-report-integration-map.json']
    require(report['chapter_count']==8 and report['two_parts_preserved'] and not report['outline_client_approved'] and report['finished_report_required'], 'R08 preserves proposed unapproved eight-chapter/two-part finished report')
    require(report['part_labels']=={'part_one':'What leaders want','part_two':'How investment decisions happen','conclusion':'From Ambition to Investment'}, 'R08 proposed part labels match client plan')
    require(not report['D01_complete'] and not report['D06_final_complete'] and not report['commercial_table_content_in_public_report'], 'R08 working Markdown/JSON not final report or confidential Table content')
    for x in report['chapter_map']:
        require(set(x['supporting_claim_ids'])<=claim_ids and not set(x['supporting_claim_ids'])&held, f"R08 chapter positive claim support resolves without held values: {x['chapter_number']}")
        require(set(x['guardrail_claim_ids'])<=held and bool(x['can_prepare_now']) and bool(x['requires_later_evidence']), f"R08 chapter guardrail and original-case dependency explicit: {x['chapter_number']}")
    require(report['chapter_map'][2]['guardrail_claim_ids']==['CLM-0392'], 'R08 held feature conflict is a guardrail only')
    qa=data['08-qa/R08-routing-walkthrough.json'];applications=data['03-report/R08-constructed-walkthroughs.json'];design=data['03-report/research-notes/r08/route-challenge/constructed-routes.json']
    if r08_second:
        applications=json.loads((ROOT/next(x['snapshot_path'] for x in r08_first_snapshots if x['original_path']=='03-report/R08-constructed-walkthroughs.json')).read_text())
    require(qa['status']=='passed_internal_constructed_walkthrough' and qa['route_count']==10 and qa['check_count']==133 and all(x['passed'] for x in qa['checks']), 'R08 ten root constructed routes pass133 analytical/linkage checks')
    require(not qa['practitioner_validation'] and qa['actual_participant_cases']==0 and qa['new_questions']==0, 'R08 route checks not practitioner validation fieldwork or extra questions')
    require(hashlib.sha256((ROOT/qa['source_design_path']).read_bytes()).hexdigest()==qa['source_design_sha256'], 'R08 original constructed design unchanged')
    require(all(not x['executed_against_final_R08_framework'] for x in design['routes']), 'R08 original design not retroactively marked as final framework validation')
    snaps=data['03-report/research-notes/r08/before-completion/manifest.json']['records']
    for x in snaps:
        require(hashlib.sha256((ROOT/x['snapshot_path']).read_bytes()).hexdigest()==x['sha256'], f"R08 exact reviewed structured draft snapshot retained: {x['original_path']}")
    for k,p in [('framework_sha256_at_walkthrough','03-report/R08-framework-map.json'),('application_sha256_at_walkthrough','03-report/R08-constructed-walkthroughs.json')]:
        require(next(x['sha256'] for x in snaps if x['original_path']==p)==qa[k], f'R08 routing hash reconciles to reviewed pre-status draft: {p}')
    oldframework=json.loads((ROOT/next(x['snapshot_path'] for x in snaps if x['original_path']=='03-report/R08-framework-map.json')).read_text())
    require({k:v for k,v in r08.items() if k not in ['status','review_basis']}=={k:v for k,v in oldframework.items() if k not in ['status','review_basis']}, 'R08 reviewed framework substance unchanged by status completion')
    oldapplications=json.loads((ROOT/next(x['snapshot_path'] for x in snaps if x['original_path']=='03-report/R08-constructed-walkthroughs.json')).read_text())
    require({k:v for k,v in applications.items() if k!='status'}=={k:v for k,v in oldapplications.items() if k!='status'}, 'R08 reviewed constructed application substance unchanged by status completion')
    for x in applications['routes']:
        require(x['executed_against_preparatory_R08_framework'] and x['evidence_type']=='constructed_internal_application' and not x['original_practitioner_observation'] and x['actual_employer'] is None and x['participant_id'] is None and x['actual_case_id'] is None and x['numerical_result'] is None, f"R08 synthetic application not original case: {x['route_id']}")
    review=data['08-qa/r08-review/integration-checks.json']
    require(review['status']=='passed_for_internal_R08_preparatory_synthesis' and all(x['passed'] for x in review['checks']), 'R08 independent integrated preparatory review passed')
    require((ROOT/'08-qa/R08-independent-review.md').is_file(), 'R08 independent review retained')
    p=next(p for p in packages if p['work_package_id']=='WP15')
    require(p['status']=='preparatory_desktop_synthesis_ready_original_integration_pending' and p['preparatory_work_only'] and 'WP11' in p['dependencies'], 'WP15 remains open for original coded contributions')
    for rel in ['03-report/R08-DECISION-FRAMEWORK.md','03-report/R08-DESKTOP-SYNTHESIS.md','03-report/R08-REPORT-INTEGRATION.md','03-report/modules/R08-decision-framework-and-synthesis.md']:
        text=(ROOT/rel).read_text()
        require(set(re.findall(r'CLM-\d{4}',text))<=claim_ids, f'R08 individual claim references resolve: {rel}')

if r08_second:
    require(r08_second['source_map']=={} and r08_second['new_source_routes']==0 and len(r08_second['claim_map'])==17, 'R08 second challenge reuses existing routes and adds seventeen bounded records')
    require(set(r08_second['claim_map'].values())<=claim_ids, 'R08 second-challenge claim links resolve')
    model=data['03-report/R08-framework-map.json']
    require(model['framework_version']=='0.2' and model['second_challenge_status']=='completed_internal_preparatory_second_challenge_original_integration_pending', 'R08 version0.2 reviewed only for preparatory second challenge')
    require(model['new_canonical_claims_count_basis']=='first_pass_preparatory_synthesis_only' and model['new_canonical_claims']==0 and model['second_challenge_new_canonical_claims']==17, 'R08 new-claim counts distinguish first pass from second challenge')
    require(model['requires_WP11_original_coding'] and not model['complete_final_WP15'] and not model['participant_validated'] and model['additional_mandatory_questions_from_second_challenge']==0, 'R08 second challenge preserves final practitioner dependency and questions')
    require(not model['prior_model_reruns'] and not model['prior_recommendation_counts_reused'] and model['prior_prompt_scenarios_are_constructed'], 'R08 earlier model results do not become demand counts or reruns')
    require([x['condition_id'] for x in model['cross_cutting_conditions']]==[f'C{i:02}' for i in range(1,6)], 'R08 five selective evidence/time/object conditions present')
    for x in model['cross_cutting_conditions']:
        require(not x['mandatory'] and not x['scored'] and not x['validated'] and set(x['claim_ids'])<=claim_ids and set(x.get('guardrail_claim_ids',[]))<=claim_ids, f"R08 selective second-challenge condition linked: {x['condition_id']}")
    require(all(v is None for v in model['second_challenge_blank_evidence_qualification'].values()), 'R08 optional qualification template remains blank')
    require(len(model['second_challenge_view_edits'])==2, 'R08 two view text refinements explicitly logged')
    import copy
    expected=copy.deepcopy(r08['views'])
    for edit in model['second_challenge_view_edits']:
        v=next(x for x in expected if x['view_id']==edit['view_id'])
        require(v[edit['field']]==edit['before'] and set(edit['claim_ids'])<=claim_ids, f"R08 exact view edit has before-value and support: {edit['view_id']}")
        v[edit['field']]=edit['after']
    require(model['views']==expected, 'R08 six views/fields/evidence unchanged except two logged text refinements')
    for k in ['blank_scope_template','blank_canvas','blank_decision_brief','evidence_claims_are_separate','states_are_separate','hypotheses','collision_controls']:
        require(model[k]==r08[k], f'R08 first-pass structure remains unchanged: {k}')
    for k in ['participant_observations','actual_case_records','completed_framework_use_tests','causal_effect_estimates','employer_forecasts','chart_data','financial_inputs']:
        require(model[k]==[], f'R08 second challenge does not populate unperformed work: {k}')
    for x in data['08-qa/R08-second-check-baseline.json']['records']:
        require(hashlib.sha256((ROOT/x['path']).read_bytes()).hexdigest()==x['sha256'], f"R08 second-challenge prior/core/client preservation: {x['path']}")
    for x in r08_first_snapshots:
        require(hashlib.sha256((ROOT/x['snapshot_path']).read_bytes()).hexdigest()==x['sha256'], f"R08 first-pass snapshot preserved: {x['original_path']}")
    old_completion=json.loads((ROOT/next(x['snapshot_path'] for x in r08_first_snapshots if x['original_path']=='08-qa/R08-completion-check.json')).read_text())
    oldhash={x['path']:x['sha256'] for x in old_completion['artifacts']}
    for x in r08_first_snapshots:
        if x['original_path'] in oldhash:
            require(x['sha256']==oldhash[x['original_path']], f"R08 first-pass completion reconciles to snapshot: {x['original_path']}")
    oldcanonical=data['03-report/research-notes/r08-second-check/before-review/canonical-before.json']
    require(claims[:len(oldcanonical['claims']['records'])]==oldcanonical['claims']['records'], 'R08 second challenge preserves every earlier claim record exactly')
    require(data['05-analysis/findings.json']['records'][:len(oldcanonical['findings']['records'])]==oldcanonical['findings']['records'], 'R08 second challenge preserves every earlier finding record exactly')
    oldsource={x['source_id']:x for x in oldcanonical['sources']['records']}
    r08_asof_sources = {x['source_id'] for x in data['04-table/research-notes/t01/root/sources-before.json']['records']} if data.get('08-qa/T01-record-map.json') else source_ids
    require(set(oldsource)==r08_asof_sources, 'R08 second challenge as-of source set adds no route or dataset')
    for x in sources:
        if x['source_id'] not in oldsource:
            require(bool(x.get('t01_source_candidate_id') or x.get('t01_second_source_candidate_id') or x.get('t02_second_source_candidate_id')), 'Later source addition is explicitly T01 first/second review, not retroactive R08 evidence')
            continue
        old=oldsource[x['source_id']]
        require({k:v for k,v in x.items() if k not in ['additional_reviews','related_topic_ids']}=={k:v for k,v in old.items() if k not in ['additional_reviews','related_topic_ids']}, f"R08 source base data unchanged apart from review/topic metadata: {x['source_id']}")
        require(all(v in x.get('additional_reviews',[]) for v in old.get('additional_reviews',[])), f"R08 preserves prior source reviews: {x['source_id']}")
    for x in data['08-qa/R08-second-check-captures.json']['files']:
        require(hashlib.sha256((ROOT/x['path']).read_bytes()).hexdigest()==x['sha256'], f"R08 second-challenge retained file hash: {x['path']}")
        if 'selected-reader' in x['path'] or 'prior-reader' in x['path']:
            require(x['kind']=='parsed_or_selected_extract', 'R08 selected reader note not promoted to raw original')
    bridge=data['08-qa/R08-prior-study-bridge-check.json']
    require(bridge['status']=='passed' and bridge['check_count']==327 and all(x['passed'] for x in bridge['checks']) and bridge['selected_questions']==4 and bridge['selected_saved_answers']==32 and bridge['no_model_reruns'], 'R08 four constructed questions/32saved texts pass327 exact checks without reruns')
    require(hashlib.sha256((ROOT/bridge['bridge_path']).read_bytes()).hexdigest()==bridge['bridge_sha256'], 'R08 exact-checked prior-study bridge unchanged')
    route=data['08-qa/R08-second-routing-walkthrough.json'];apps=data['03-report/R08-constructed-walkthroughs.json']
    require(route['status']=='passed_internal_second_constructed_walkthrough' and route['route_count']==15 and route['check_count']==197 and all(x['passed'] for x in route['checks']), 'R08 fifteen version0.2 constructed applications pass197 checks')
    require(not route['practitioner_validation'] and route['actual_participant_cases']==0 and route['new_questions']==0, 'R08 second route checks not human fieldwork or validation')
    reviewed=data['03-report/research-notes/r08-second-check/before-status/manifest.json']['records']
    for x in reviewed:
        require(hashlib.sha256((ROOT/x['snapshot_path']).read_bytes()).hexdigest()==x['sha256'], f"R08 exact reviewed v0.2 snapshot retained: {x['original_path']}")
    for key,p in [('framework_sha256_at_walkthrough','03-report/R08-framework-map.json'),('application_sha256_at_walkthrough','03-report/R08-constructed-walkthroughs.json')]:
        require(next(x['sha256'] for x in reviewed if x['original_path']==p)==route[key], f'R08 second routing hash reconciles to pre-status draft: {p}')
    reviewedmodel=json.loads((ROOT/next(x['snapshot_path'] for x in reviewed if x['original_path']=='03-report/R08-framework-map.json')).read_text())
    require({k:v for k,v in model.items() if k not in ['second_challenge_status','second_challenge_review_basis']}=={k:v for k,v in reviewedmodel.items() if k not in ['second_challenge_status','second_challenge_review_basis']}, 'R08 v0.2 reviewed substance unchanged by status edits')
    require(apps['route_count']==15 and apps['original_routes_reapplied']==10 and apps['new_constructed_routes']==5 and not apps['practitioner_validation'], 'R08 ten old plus five new constructed applications preserved')
    by={x['route_id']:x for x in apps['routes']}
    for x in applications['routes']:
        require({k:v for k,v in by[x['route_id']].items() if k not in ['framework_version','second_challenge_reassessment']}=={k:v for k,v in x.items() if k not in ['framework_version','second_challenge_reassessment']}, f"R08 original constructed interpretation unchanged on reapplication: {x['route_id']}")
    review=data['08-qa/r08-second-review/integration-checks.json']
    require(review['status']=='passed_for_internal_R08_second_challenge' and all(x['passed'] for x in review['checks']), 'R08 independent integrated second-challenge review passed')
    require((ROOT/'08-qa/R08-second-check-independent-review.md').is_file(), 'R08 independent second-challenge review retained')
    for rel in ['03-report/R08-SECOND-CHECK-READOUT.md','03-report/R08-DECISION-FRAMEWORK.md','03-report/R08-DESKTOP-SYNTHESIS.md','03-report/R08-REPORT-INTEGRATION.md','03-report/modules/R08-decision-framework-and-synthesis.md']:
        text=(ROOT/rel).read_text();require(set(re.findall(r'CLM-\d{4}',text))<=claim_ids, f'R08 second-challenge references resolve: {rel}')
        for start,end in re.findall(r'CLM-(\d{4})[–-](\d{4})',text):
            require({f'CLM-{n:04}' for n in range(int(start),int(end)+1)}<=claim_ids, f'R08 second-challenge claim range resolves: {rel}')

wp03=data.get('01-method/collection-pack-v0.1/REVIEW-DECISIONS.json')
if wp03:
    require(not wp03['collection_ready'] and not wp03['legal_compliance_certified'] and wp03['user_send_permission_reference'] is None, 'WP03 draft does not activate collection or certify compliance/sending')
    require([x['decision_id'] for x in wp03['release_decisions']]==[f'READY{i:02}' for i in range(1,6)] and all(x['status']=='not_confirmed' and x['resolution'] is None and x['confirmation_reference'] is None for x in wp03['release_decisions']), 'WP03 five actual release decisions remain unconfirmed')
    contract=wp03['working_contract']
    require(hashlib.sha256(Path(contract['source_path']).read_bytes()).hexdigest()==contract['source_sha256'], 'WP03 working agreement reference hash verified')
    require(contract['return_or_delete_days']==30 and contract['backup_deletion_days']==90 and not contract['executed_copy_retrieved'], 'WP03 contract closure periods retained without executed-copy claim')
    require('JGA controller' in contract['working_role'] and 'Riseklix processor' in contract['working_role'] and 'own business-contact' in contract['working_role'], 'WP03 on-behalf roles and own-business-record distinction retained')
    require('prior written authorisation' in contract['tools_rule'] and 'not itself an IDTA' in contract['access_rule'], 'WP03 subprocessors/transfer arrangement not presumed approved')
    for k in ['actual_tool_selection','actual_restricted_storage','actual_notice_version','actual_lawful_instructions_reference','actual_transfer_arrangement_reference']:
        require(wp03[k] is None, 'WP03 actual arrangement not invented: '+k)
    require(wp03['actual_authorised_access_list']==[], 'WP03 no approved access list invented')
    policy=data['01-method/collection-pack-v0.1/COUNT-AND-ROUTING-POLICY.json']
    require(policy['report_target_min']==6 and policy['report_target_max']==10 and policy['table_event_cap']==4 and policy['table_ideal_mix']=={'buyers':2,'members':2} and policy['mix_is_not_a_fixed_quota'], 'WP03 scope and separate count units preserved')
    require(policy['one_person_reference_across_modes_and_streams'] and policy['report_core_questions']==14 and policy['new_core_questions']==0 and policy['core_question_version']=='0.2', 'WP03 one-person count and unchanged fourteen questions')
    require(not policy['recording_default_enabled'] and not policy['external_AI_transcription_default_enabled'] and policy['written_equivalent_allowed'] and not policy['duration_tested'] and not policy['fixed_duration_promised'], 'WP03 minimal mode is proposed without recording/tool/duration activation')
    require(policy['actual_report_contributor_count']==0 and policy['actual_Table_event_count']==0 and policy['actual_records']==[], 'WP03 real participant/contribution/event counts remain zero')
    templates=data['01-method/collection-pack-v0.1/RECORD-TEMPLATES.json']
    def template_blank(x):
        if isinstance(x,dict):return all(template_blank(v) for v in x.values())
        if isinstance(x,list):return len(x)==0
        return x is None
    for k in ['restricted_identity_lookup','restricted_permission_record','contribution_note','response_entry','publication_item','restricted_request_or_change_log','blank_analysis_transfer_check','blank_count_record']:
        require(template_blank(templates[k]), 'WP03 blank collection schema remains unpopulated: '+k)
    for k in ['actual_participants','actual_permissions','actual_contributions','actual_Table_events','actual_publication_items','actual_rights_or_change_requests','actual_transfer_events']:
        require(templates[k]==[], 'WP03 actual collection array empty: '+k)
    require(templates['blank_is_not_yes'] and templates['participation_choice_is_not_automatically_GDPR_lawful_basis'], 'WP03 blank choices not consent and participation not automatically processing basis')
    require(len(templates['restricted_permission_record']['choices'])==11, 'WP03 selective permissions separated rather than bundled')
    t01_canonical_before={f'02-evidence/registers/{n}.json':f'04-table/research-notes/t01/root/{n}-before.json' for n in ['sources','claims','searches','source-aliases']}
    t01_canonical_before['05-analysis/findings.json']='04-table/research-notes/t01/root/findings-before.json'
    for x in data['08-qa/WP03-baseline-manifest.json']['files']:
        target=t01_canonical_before.get(x['path'],x['path']) if data.get('08-qa/T01-record-map.json') else x['path']
        require(hashlib.sha256((ROOT/target).read_bytes()).hexdigest()==x['sha256'], f"WP03 prior/core/client/canonical as-of file preserved: {x['path']}")
    captures=data['01-method/research-notes/wp03/data/capture-manifest.json']['records']
    require(len(captures)==5, 'WP03 five focused operating-guidance HTML reviews recorded separately from payroll market findings')
    for x in captures:
        require(hashlib.sha256((ROOT/x['path']).read_bytes()).hexdigest()==x['sha256'] and hashlib.sha256((ROOT/x['text_path']).read_bytes()).hexdigest()==x['text_sha256'], f"WP03 original and parsed text hashes: {x['review_id']}")
    qa=data['08-qa/WP03-routing-permission-checks.json']
    require(qa['status']=='passed_internal_WP03_pack_walkthrough_not_fieldwork' and qa['check_count']==199 and all(x['passed'] for x in qa['checks']), 'WP03199 root constructed/contract/link/preservation checks passed')
    require(len(qa['constructed_count_route_applications'])==8 and len(qa['constructed_release_gate_applications'])==3 and qa['actual_participants']==0 and qa['actual_Table_events']==0 and not qa['collection_ready'] and not qa['practitioner_testing'], 'WP03 eight count/three permission cases not actual fieldwork or activation')
    require(hashlib.sha256((ROOT/qa['source_design_path']).read_bytes()).hexdigest()==qa['source_design_sha256'], 'WP03 original route-design input unchanged')
    for x in data['01-method/research-notes/wp03/routes/constructed-route-tests.json']['tests']:
        require(not x['executed'] and x['actual_result'] is None, 'WP03 original unexecuted design distinct from root application: '+x['test_id'])
    for x in qa['pack_structured_hashes']:
        require(hashlib.sha256((ROOT/x['path']).read_bytes()).hexdigest()==x['sha256'], 'WP03 reviewed structured pack unchanged: '+x['path'])
    review=data['08-qa/wp03-review/integration-checks.json']
    require(review['status']=='passed_for_internal_WP03_collection_pack_preparation' and all(x['passed'] for x in review['checks']), 'WP03 independent integrated preparation review passed')
    require((ROOT/'08-qa/WP03-independent-review.md').is_file(), 'WP03 independent review retained')
    p=next(x for x in packages if x['work_package_id']=='WP03')
    require(p['status']=='prepared_for_user_client_review_collection_not_activated' and not p['collection_ready'], 'WP03 preparation complete only for review; fieldwork not activated')

t01=data.get('08-qa/T01-record-map.json')
if t01:
    require(t01['new_source_routes']==26 and len(t01['source_map'])==26 and t01['new_claim_records']==52 and len(t01['claim_map'])==52, 'T01 twenty-six new routes and fifty-two bounded claim records mapped')
    require(set(t01['source_map'].values())<=source_ids and set(t01['claim_map'].values())<=claim_ids, 'T01 canonical source/claim maps resolve')
    model=data['04-table/T01-model-map.json'];hs=data['04-table/T02-proposition-hypotheses.json']
    require(model['model_count']==6 and len(model['models'])==6 and [x['model_id'] for x in model['models']]==[f'T01-M{i:02}' for i in range(1,7)], 'T01 exactly six ordered models')
    require(len({x['mechanism'] for x in model['models']})==6 and not model['ranking'] and not model['commercial_validation'], 'T01 six distinct mechanisms without ranking/demand validation')
    for x in model['models']:
        require(set(x['source_ids'])<=source_ids and set(x['claim_ids'])<=claim_ids and bool(x['source_ids']) and bool(x['claim_ids']), 'T01 model evidence resolves: '+x['model_id'])
        require(not x['actual_demand_validated'] and not x['adopted_jga_model'] and not x['jga_price_input'], 'T01 model not adopted, validated or price input: '+x['model_id'])
        require((ROOT/x['review_note']).is_file() and (ROOT/x['raw_model_candidate_path']).is_file(), 'T01 detailed/raw review files exist: '+x['model_id'])
    price=model['models'][2]['public_price']
    require(price['value']==1122 and price['currency']=='GBP' and price['period']=='year' and not price['jga_forecast_input'], 'T01 Payroll Centre fee original GBP annual support unit; not a JGA price')
    require(model['participant_observations']==[] and model['actual_Table_conversations']==[] and model['financial_inputs']==[] and model['new_mandatory_questions']==0 and model['original_fourteen_questions_unchanged'], 'T01 no invented fieldwork, finance inputs or extra core questions')
    require(hs['actual_interviews']==0 and hs['actual_commitments']==[] and hs['price_recommendations']==[] and not hs['fieldwork_activated'] and not hs['T03_validation_complete'], 'T02 draft hypotheses do not imply T03 validation or activation')
    require(len(hs['hypotheses'])==4 and all(x['status']=='untested_design_hypothesis' and not x['validated'] and x['actual_supporting_contributions']==[] and x['counter_signal'] for x in hs['hypotheses']), 'T02 four explicit untested hypotheses with disconfirming signals')
    old=data['04-table/research-notes/t01/root/claims-before.json']['records']
    require(len(old)==355 and claims[:len(old)]==old, 'T01 preserves every earlier canonical claim exactly')
    require(data['05-analysis/findings.json']==data['04-table/research-notes/t01/root/findings-before.json'] and len(data['05-analysis/findings.json']['records'])==81, 'T01 does not rewrite earlier findings or invent practitioner findings')
    oldsrc=data['04-table/research-notes/t01/root/sources-before.json']['records'];newsrc={x['source_id']:x for x in sources}
    t01_asof_sources=data['04-table/research-notes/t01-second-check/before-review/sources.json']['records'] if data.get('08-qa/T01-second-check-record-map.json') else sources
    require(len(oldsrc)==191 and len(t01_asof_sources)==217, 'T01 first-pass as-of old191 and appended26 routes reconcile')
    for x in oldsrc:
        y=newsrc[x['source_id']]
        require({k:v for k,v in x.items() if k not in ['additional_reviews','related_topic_ids']}=={k:v for k,v in y.items() if k not in ['additional_reviews','related_topic_ids']}, 'T01 preserves old source base data: '+x['source_id'])
        require(all(v in y.get('additional_reviews',[]) for v in x.get('additional_reviews',[])) and set(x.get('related_topic_ids',[]))<=set(y.get('related_topic_ids',[])), 'T01 retains old source reviews/topics: '+x['source_id'])
    oldsearch=data['04-table/research-notes/t01/root/searches-before.json']['records']
    require(data['02-evidence/registers/searches.json']['records'][:len(oldsearch)]==oldsearch, 'T01 preserves earlier search records')
    oldalias=data['04-table/research-notes/t01/root/source-aliases-before.json']
    for k in ['aliases','url_aliases']:
        require(all(x in data['02-evidence/registers/source-aliases.json'].get(k,[]) for x in oldalias.get(k,[])), 'T01 preserves earlier alias records: '+k)
    for x in data['08-qa/T01-baseline-manifest.json']['files']:
        require(hashlib.sha256((ROOT/x['path']).read_bytes()).hexdigest()==x['sha256'], 'T01 earlier/core/client/collection file preserved: '+x['path'])
    for x in data['08-qa/T01-captures.json']['files']:
        require(hashlib.sha256((ROOT/x['path']).read_bytes()).hexdigest()==x['sha256'], 'T01 retained file hash: '+x['path'])
        require(x['kind'] in ['retained_original_html','parsed_original_text','rendered_pdf_page'], 'T01 file type remains explicit: '+x['path'])
    for rel in ['04-table/T01-COMPARABLE-MODELS.md','04-table/T01-COMPARABLE-MATRIX.md','04-table/T01-DESKTOP-READOUT.md','04-table/T02-PROPOSITION-WORKING-NOTE.md']:
        require(set(re.findall(r'CLM-\d{4}',(ROOT/rel).read_text()))<=claim_ids, 'T01 prose claim references resolve: '+rel)
    review=data.get('08-qa/t01-review/integration-checks.json')
    if review:
        require(review['status']=='passed_for_internal_T01_desktop_comparison_and_T02_hypothesis_preparation' and all(x['passed'] for x in review['checks']), 'T01 independent integrated desktop comparison review passed')
        require((ROOT/'08-qa/T01-independent-review.md').is_file(), 'T01 independent review retained')
        snapshots={x['original_path']:x for x in data['04-table/research-notes/t01/reviewed-before-status/manifest.json']['records']}
        for x in review['reviewed_artifacts']:
            target=snapshots.get(x['path'],{}).get('snapshot_path',x['path'])
            require(hashlib.sha256((ROOT/target).read_bytes()).hexdigest()==x['sha256'], 'T01 independently reviewed content hash retained: '+x['path'])
            if x['path'] in snapshots:
                before=data[target];after=data[x['path']]
                require({k:v for k,v in before.items() if k not in ['status','review_basis']}=={k:v for k,v in after.items() if k not in ['status','review_basis']}, 'T01 post-review changes are only allowed status/basis: '+x['path'])
        require(model['status']=='desktop_comparison_reviewed_for_internal_use' and hs['status']=='internally_reviewed_draft_not_buyer_validated', 'T01 reviewed deskwork and T02 untested proposition status explicit')
        p=next(x for x in packages if x['work_package_id']=='WP12')
        require(p['status'] in ['T01_desktop_reviewed_T02_propositions_draft','T01_second_challenge_reviewed_T02_refinement_pending','T01_T02_internal_design_reviewed_validation_pending','T01_T02_second_design_reviewed_validation_pending'] and not p['T02_buyer_validated'] and not p['T03_conversations_complete'], 'WP12 desktop comparison does not complete T03 or demand validation')


t01_second=data.get('08-qa/T01-second-check-record-map.json')
if t01_second:
    require(t01_second['new_source_routes']==6 and len(t01_second['source_map'])==6 and t01_second['new_claim_records']==25 and len(t01_second['claim_map'])==25, 'T01 second challenge six new routes and twenty-five bounded records')
    require(set(t01_second['source_map'].values())<=source_ids and set(t01_second['claim_map'].values())<=claim_ids, 'T01 second source/claim mapping resolves')
    before=data['04-table/research-notes/t01-second-check/before-review/claims.json']['records']
    require(len(before)==407 and claims[:len(before)]==before, 'T01 second preserves all prior407 claim records exactly')
    before_s=data['04-table/research-notes/t01-second-check/before-review/sources.json']['records']
    t02s_source_asof=data[t02s_asof_canonical('02-evidence/registers/sources.json')]['records']
    t02s_claim_asof=data[t02s_asof_canonical('02-evidence/registers/claims.json')]['records']
    require(len(before_s)==217 and len(t02s_source_asof)==223 and len(t02s_claim_asof)==432, 'T01 second as-of canonical append reconciles223sources432claims')
    current_s={x['source_id']:x for x in sources}
    for x in before_s:
        y=current_s[x['source_id']]
        require({k:v for k,v in x.items() if k not in ['additional_reviews','related_topic_ids']}=={k:v for k,v in y.items() if k not in ['additional_reviews','related_topic_ids']}, 'T01 second preserves prior source base: '+x['source_id'])
        require(all(v in y.get('additional_reviews',[]) for v in x.get('additional_reviews',[])) and set(x.get('related_topic_ids',[]))<=set(y.get('related_topic_ids',[])), 'T01 second preserves prior reviews/topics: '+x['source_id'])
    require(data['05-analysis/findings.json']==data['04-table/research-notes/t01-second-check/before-review/findings.json'], 'T01 second preserves earlier81findings without invented buyer evidence')
    old_search=data['04-table/research-notes/t01-second-check/before-review/searches.json']['records']
    require(data['02-evidence/registers/searches.json']['records'][:len(old_search)]==old_search, 'T01 second preserves previous search records')
    for x in data['08-qa/T01-second-check-baseline.json']['files']:
        require(hashlib.sha256((ROOT/x['path']).read_bytes()).hexdigest()==x['sha256'], 'T01 second131earlier/core/client/first-pass artifacts preserved: '+x['path'])
    asof={x['original_path']:x for x in data['04-table/research-notes/t01-second-check/before-review/before-file-manifest.json']['records']}
    for x in asof.values():
        require(hashlib.sha256((ROOT/x['snapshot_path']).read_bytes()).hexdigest()==x['sha256'], 'T01 second exact canonical/control before snapshot: '+x['original_path'])
    for x in data['08-qa/T01-completion-check.json']['artifacts']:
        target=asof.get(x['path'],{}).get('snapshot_path',x['path'])
        require(hashlib.sha256((ROOT/target).read_bytes()).hexdigest()==x['sha256'], 'T01 first completion reconciles to preserved as-of artifact: '+x['path'])
    sm=data['04-table/T01-second-challenge-map.json']
    require(sm['selected_model_ids']==[f'T01-M{i:02}'for i in range(1,7)] and len(sm['model_changes'])==6 and sm['first_pass_preserved'], 'T01 second supplements same six models')
    require(sm['original_T02_hypothesis_ids']==[f'T02-H{i:02}'for i in range(1,5)] and not sm['hypotheses_replaced'], 'T01 second preserves four T02hypotheses')
    require([x['condition_id']for x in sm['conditions']]==[f'TC{i:02}'for i in range(1,7)], 'T01 second six ordered selective conditions')
    for x in sm['conditions']:
        require(not x['mandatory'] and not x['scored'] and not x['validated'] and x['new_core_questions']==0 and set(x['claim_ids'])<=claim_ids and bool(x['counterexample']), 'T01 second linked optional condition: '+x['condition_id'])
    for x in sm['model_changes']:
        require(set(x['claim_ids'])<=claim_ids, 'T01 second model refinement evidence resolves: '+x['model_id'])
    require(sm['additional_mandatory_questions']==0 and not sm['ranking'] and not sm['commercial_validation'] and not sm['prior_model_reruns'] and not sm['prior_recommendation_counts_reused'], 'T01 second no added core/ranking/validation/rerun/demand-count transfer')
    for k in ['participant_observations','actual_Table_conversations','financial_inputs','new_price_recommendations']:
        require(sm[k]==[], 'T01 second unperformed data/pricing empty: '+k)
    inventory=data['08-qa/T01-second-check-captures.json']['files']
    for x in inventory:
        require(hashlib.sha256((ROOT/x['path']).read_bytes()).hexdigest()==x['sha256'], 'T01 second retained capture hash: '+x['path'])
        name=Path(x['path']).name
        if name=='SRC-0192.html':require(x['kind']=='retained_application_shell_not_substantive_body','T01 second Hays raw shell not promoted to substantive original')
        if name=='SRC-0192.txt':require(x['kind']=='parsed_application_shell_not_substantive_body','T01 second Hays parsed shell explicit')
        if name=='T1H-S03.html':require(x['kind']=='discovery_only_application_shell','T01 second Accomplishments rawshell discovery only')
        if name=='T1H-S03.txt':require(x['kind']=='parsed_discovery_only_application_shell','T01 second Accomplishments parsed shell discovery only')
        if 'selected-reader' in name:require(x['kind']=='selected_reader_extract','T01 second selected reader notes not promoted to original: '+name)
    root=current_s[t01_second['source_map']['T1R2-S01']]
    require(root['capture_path'] is None and bool(root['review_extracts']), 'T01 second Chatham primary reader extract not raw HTML')
    require('T1H-S03' not in t01_second['source_map'], 'T01 second excluded collaboration shell not canonical substantive source')
    bridge=data['04-table/research-notes/t01-second-check/competitors/prior-study-bridge-check.json']
    require(bridge['status']=='passed_narrow_saved_data_integrity_not_fact_validation' and bridge['check_count']==126 and all(x['passed']for x in bridge['checks']), 'T01 second threequestion24savedrecords126exactchecks retained')
    routes=data.get('08-qa/T01-second-routing-walkthrough.json')
    if routes:
        require(routes['status']=='passed_internal_constructed_T01_second_challenge_walkthrough' and routes['route_count']==9 and routes['check_count']==173 and all(x['passed']for x in routes['checks']), 'T01 second nine root constructed applications173checks')
        require(not routes['practitioner_validation'] and not routes['commercial_validation'] and routes['actual_participant_cases']==0 and routes['new_mandatory_questions']==0 and routes['financial_inputs_added']==0, 'T01 second constructed applications not fieldwork/validation')
    for rel in ['04-table/T01-SECOND-CHECK-READOUT.md','04-table/T01-SECOND-CHECK-MATRIX.md','04-table/T02-SECOND-CHECK-REFINEMENTS.md']:
        require(set(re.findall(r'CLM-\d{4}',(ROOT/rel).read_text()))<=claim_ids, 'T01 second prose canonical references resolve: '+rel)
    review=data.get('08-qa/t01-second-review/integration-checks.json')
    if review:
        require(review['status']=='passed_for_internal_T01_second_challenge' and review['check_count']==1168 and all(x['passed']for x in review['checks']) and not review.get('open_substantive_issues',[]), 'T01 second independent integrated review passed')
        require((ROOT/'08-qa/T01-second-check-independent-review.md').is_file(), 'T01 second independent review retained')
        snapshots={x['original_path']:x for x in data['04-table/research-notes/t01-second-check/reviewed-before-status/manifest.json']['records']}
        for x in review['reviewed_artifacts']:
            target=snapshots.get(x['path'],{}).get('snapshot_path',x['path'])
            require(hashlib.sha256((ROOT/target).read_bytes()).hexdigest()==x['sha256'], 'T01 second exact independently reviewed artifact retained: '+x['path'])
            if x['path'] in snapshots:
                b=data[target];a=data[x['path']]
                require({k:v for k,v in b.items()if k not in ['status','review_basis']}=={k:v for k,v in a.items()if k not in ['status','review_basis']}, 'T01 second post-review status/basis-only changes: '+x['path'])
        require(sm['status']=='second_challenge_reviewed_for_internal_design', 'T01 second reviewed status remains internal design')
        require(routes['model_sha256_at_walkthrough']==snapshots['04-table/T01-second-challenge-map.json']['sha256'], 'T01 second constructed assessments reconcile to reviewed pre-status map')
        p=next(x for x in packages if x['work_package_id']=='WP12')
        require(p['status'] in ['T01_second_challenge_reviewed_T02_refinement_pending','T01_T02_internal_design_reviewed_validation_pending','T01_T02_second_design_reviewed_validation_pending'] and p['T01_second_challenge_reviewed'] and not p['T02_buyer_validated'] and not p['T03_conversations_complete'], 'T01 second WP12 completion does not imply T02/T03 validation')


t02=data.get('04-table/T02-proposition-map.json')
if t02:
    require([x['proposition_id']for x in t02['propositions']]==['TP01','TP02','TP03'] and len(t02['propositions'])==3, 'T02 three distinct research/partner/practitioner concepts')
    require(t02['original_hypotheses']==[f'T02-H{i:02}'for i in range(1,5)] and t02['selected_T01_models']==6, 'T02 four hypotheses and six reviewed comparables preserved')
    require(t02['report_free_to_practitioner_preserved'] and t02['JGA_commissioned_IP_not_restricted_by_drafts'] and not t02['signed_project_scope_changed'], 'T02 preserves free research, JGA commissioned IP and signed scope')
    require(t02['original_report_questions']==14 and t02['extra_mandatory_questions']==0 and not t02['fieldwork_activated'] and not t02['active_WP03_guide_changed'], 'T02 no core expansion or fieldwork/protocol activation')
    for k in ['actual_buyer_validation','actual_member_validation','actual_offer_exposures','actual_rights_grants','financial_inputs','external_actions','prices']:
        require(t02[k]==[], 'T02 design does not populate actual data: '+k)
    for x in t02['propositions']:
        require(not x['adopted'] and not x['validated'] and x['price'] is None and x['currency'] is None, 'T02 no adoption/price/demand validation: '+x['proposition_id'])
        require(x['actual_customers']==[] and x['actual_commitments']==[] and x['actual_participants']==[] and x['new_mandatory_report_questions']==0, 'T02 no invented customers/contributions/newcore: '+x['proposition_id'])
        require(set(x['canonical_claim_ids'])<=claim_ids and bool(x['minimum_payload']) and bool(x['concept_after_discovery']), 'T02 concept evidence and concrete payload: '+x['proposition_id'])
        require((ROOT/x['raw_candidate_path']).is_file(), 'T02 author candidate retained: '+x['proposition_id'])
    require('already commissioned or complete' in t02['propositions'][1]['funding_purpose_boundary'] and 'counting each cost and bundled entitlement once' in t02['propositions'][1]['funding_purpose_boundary'], 'T02 partner funding accurately identifies edition/purpose without banning legitimate multiple revenues')
    seg=data['04-table/T02-buyer-segments.json']
    require(seg['contract_segment_ids']==[f'BS{i:02}'for i in range(1,6)] and seg['additional_segment_ids']==['BS06'] and len(seg['records'])==6 and not seg['ranked'], 'T02 five contract segments and additional employer hypothesis distinct')
    require([x['segment']for x in seg['records'][:5]]==['Payroll technology','Payroll outsourcing/services','HCM organisations','Consulting/advisory','Investment organisations'], 'T02 all five contract named market categories retained')
    require(all(not x['actual_payer_identified'] and not x['actual_purchase_observed'] and not x['validated']for x in seg['records']), 'T02 segment map is use hypothesis not qualified pipeline')
    require(seg['actual_buyers']==[] and seg['price_estimates']==[] and set(seg['canonical_claim_ids'])<=claim_ids, 'T02 no segment demand/price estimates and evidence resolves')
    rights=data['04-table/T02-use-and-entitlement-options.json']
    require(len(rights['options'])==8 and [x['option_id']for x in rights['options']]==[f'RU{i:02}'for i in range(1,9)], 'T02 eight distinct customer use/entitlement options')
    require(not rights['Riseklix_controls_JGA_commissioned_IP'] and rights['actual_rights_grants']==[] and rights['actual_customer_contracts']==[] and all(not x['approved']for x in rights['options']), 'T02 future customer choices neither rights grants nor Riseklix IP veto')
    require(set(rights['canonical_support_ids'])<=claim_ids, 'T02 use-option support references resolve')
    delivery=data['04-table/T02-delivery-map.json']
    require([x['work_id']for x in delivery['items']]==[f'DW{i:02}'for i in range(1,9)], 'T02 eight scoped delivery work objects')
    require(all(not x['owner_assigned'] and not x['capacity_confirmed'] and x['hours'] is None and x['cash_cost'] is None for x in delivery['items']), 'T02 delivery roles/work are requirements not staff or cost quotes')
    require(delivery['financial_inputs']==[] and delivery['actual_delivery_events']==[] and delivery['staff_hired']==[] and delivery['new_signed_project_deliverables']==[] and not delivery['commercial_validation'], 'T02 no delivery/finance/scope commitments invented')
    guide=data['04-table/T02-validation-map.json']
    require(guide['version']=='0.2' and guide['status']=='draft_for_user_client_review_not_activated' and not guide['active_collection_guide_changed'] and not guide['fieldwork_activated'], 'T02 proposed guide0.2 not active collection protocol')
    require([x['question_id']for x in guide['records']]==[f'B{i:02}'for i in range(1,7)]+[f'M{i:02}'for i in range(1,7)], 'T02 same six buyer/six member question IDs')
    require(all(not x['all_probes_mandatory'] for x in guide['records']) and guide['report_core_questions']==14 and guide['additional_mandatory_report_questions']==0, 'T02 selective probes not new mandatory report questions')
    require(guide['actual_concept_exposures']==[] and guide['actual_responses']==[] and guide['actual_Table_events']==0 and guide['actual_report_contributors']==0 and guide['price_anchors']==[], 'T02 no concept exposure/response/price anchors invented')
    conds={x['condition_id']for x in data['04-table/T01-second-challenge-map.json']['conditions']}
    for x in guide['records']:
        require(set(x['condition_ids'])<=conds and set(x['hypothesis_ids'])<=set(t02['original_hypotheses']), 'T02 guide linked to existing hypotheses/conditions: '+x['question_id'])
    require(data['01-method/collection-pack-v0.1/COUNT-AND-ROUTING-POLICY.json']['guide_references']['table']=='01-method/TABLE-VALIDATION-GUIDES-v0.1.md', 'T02 original active-policy reference not silently switched')
    for x in data['08-qa/T02-baseline-manifest.json']['files']:
        require(hashlib.sha256((ROOT/t02s_asof_canonical(x['path'])).read_bytes()).hexdigest()==x['sha256'], 'T02 earlier/core/client/canonical as-of146file preservation: '+x['path'])
    for rel in ['04-table/T02-PROPOSITION-PACK.md','04-table/T02-BUYER-USES-AND-RIGHTS.md','04-table/T02-DELIVERY-AND-VALIDATION.md','01-method/TABLE-VALIDATION-GUIDES-v0.2.md']:
        require(set(re.findall(r'CLM-\d{4}',(ROOT/rel).read_text()))<=claim_ids, 'T02 narrative evidence resolves: '+rel)
    oldfiles={x['original_path']:x for x in data['04-table/research-notes/t02/before-review/manifest.json']['records']}
    for x in oldfiles.values():
        require(hashlib.sha256((ROOT/x['snapshot_path']).read_bytes()).hexdigest()==x['sha256'], 'T02 before-control raw snapshot preserved: '+x['original_path'])
    for x in data['08-qa/T01-second-check-completion.json']['artifacts']:
        target=oldfiles.get(x['path'],{}).get('snapshot_path',t02s_asof_canonical(x['path']))
        require(hashlib.sha256((ROOT/target).read_bytes()).hexdigest()==x['sha256'], 'T01 second completion reconciles to T02 before snapshot: '+x['path'])
    review=data.get('08-qa/t02-review/integration-checks.json')
    if review:
        require(all(x['passed']for x in review['checks']) and not review.get('open_substantive_issues',[]), 'T02 independent integrated design review passed')
        require((ROOT/'08-qa/T02-independent-review.md').is_file(), 'T02 independent review retained')
        require(review['status']=='passed_for_internal_T02_proposition_preparation' and review['check_count']==331, 'T02 independently reviewed design status and bounded funding clarification')
        snaps={x['original_path']:x for x in data['04-table/research-notes/t02/reviewed-before-status/manifest.json']['records']}
        for x in review['reviewed_artifacts']:
            target=snaps.get(x['path'],{}).get('snapshot_path',x['path'])
            require(hashlib.sha256((ROOT/target).read_bytes()).hexdigest()==x['sha256'], 'T02 exact independently reviewed artifact retained: '+x['path'])
            if x['path'] in snaps:
                b=data[target];a=data[x['path']]
                require({k:v for k,v in b.items()if k not in ['status','review_basis']}=={k:v for k,v in a.items()if k not in ['status','review_basis']}, 'T02 only reviewed status/basis keys changed: '+x['path'])
        require(t02['status']=='internal_proposition_design_reviewed_validation_pending', 'T02 design reviewed without market validation')
        p=next(x for x in packages if x['work_package_id']=='WP12')
        require(p['status'] in ['T01_T02_internal_design_reviewed_validation_pending','T01_T02_second_design_reviewed_validation_pending'] and p['T02_design_reviewed'] and not p['T02_buyer_validated'] and not p['T03_conversations_complete'], 'WP12 design complete only; T03 validation remains open')


t02second=data.get('08-qa/T02-second-check-record-map.json')
if t02second:
    require(t02second['new_source_routes']==2 and len(t02second['source_map'])==2 and t02second['new_claim_records']==11 and len(t02second['claim_map'])==11, 'T02 second two routes eleven bounded source/application records')
    require(set(t02second['source_map'].values())<=source_ids and set(t02second['claim_map'].values())<=claim_ids, 'T02 second canonical append links resolve')
    before=data[t02s_before['02-evidence/registers/claims.json']['snapshot_path']]['records']
    require(len(before)==432 and claims[:len(before)]==before, 'T02 second preserves every prior432claim exactly')
    oldsrc=data[t02s_before['02-evidence/registers/sources.json']['snapshot_path']]['records'];by={x['source_id']:x for x in sources}
    require(len(oldsrc)==223 and len(sources)==225 and len(claims)==443, 'T02 second225sources443claims reconcile')
    for x in oldsrc:
        y=by[x['source_id']]
        require({k:v for k,v in x.items()if k not in ['additional_reviews','related_topic_ids']}=={k:v for k,v in y.items()if k not in ['additional_reviews','related_topic_ids']}, 'T02 second source base preserved: '+x['source_id'])
        require(all(v in y.get('additional_reviews',[])for v in x.get('additional_reviews',[])) and set(x.get('related_topic_ids',[]))<=set(y.get('related_topic_ids',[])), 'T02 second old source reviews/topics preserved: '+x['source_id'])
    require(data['05-analysis/findings.json']==data[t02s_before['05-analysis/findings.json']['snapshot_path']], 'T02 second81findings remain unchanged without invented empirical findings')
    oldsearch=data[t02s_before['02-evidence/registers/searches.json']['snapshot_path']]['records']
    require(data['02-evidence/registers/searches.json']['records'][:len(oldsearch)]==oldsearch, 'T02 second search history preserved')
    for x in data['08-qa/T02-second-check-baseline.json']['files']:
        require(hashlib.sha256((ROOT/t02s_asof_canonical(x['path'])).read_bytes()).hexdigest()==x['sha256'], 'T02 second158protected files/canonical asof: '+x['path'])
    for x in t02s_before.values():
        require(hashlib.sha256((ROOT/x['snapshot_path']).read_bytes()).hexdigest()==x['sha256'], 'T02 second exact before-file snapshot: '+x['original_path'])
    for x in data['08-qa/T02-completion-check.json']['artifacts']:
        target=t02s_before.get(x['path'],{}).get('snapshot_path',x['path'])
        require(hashlib.sha256((ROOT/target).read_bytes()).hexdigest()==x['sha256'], 'T02 first completion reconciles to second-check before snapshot: '+x['path'])
    sm=data['04-table/T02-second-challenge-map.json']
    require(sm['original_proposition_ids']==['TP01','TP02','TP03'] and sm['original_propositions_preserved'] and sm['original_hypothesis_ids']==[f'T02-H{i:02}'for i in range(1,5)], 'T02 second preserves three offers/four hypotheses')
    require([x['condition_id']for x in sm['conditions']]==[f'OC{i:02}'for i in range(1,6)] and len(sm['proposition_refinements'])==3, 'T02 second five selective conditions and three offer refinements')
    for x in sm['conditions']:
        require(not x['mandatory'] and not x['scored'] and not x['validated'] and x['new_core_questions']==0 and set(x['claim_ids'])<=claim_ids, 'T02 second optional bounded condition: '+x['condition_id'])
    for x in sm['proposition_refinements']:
        require(set(x['claim_ids'])<=claim_ids and set(x['condition_ids'])<={f'OC{i:02}'for i in range(1,6)}, 'T02 second offer refinement links: '+x['proposition_id'])
    require(sm['contract_segments_unchanged']==5 and sm['employer_additional_hypothesis_unchanged'] and sm['free_full_practitioner_research_preserved'] and sm['commissioned_JGA_IP_unchanged'], 'T02 second contract market/free benefit/IP unchanged')
    require(sm['report_question_count']==14 and sm['Table_question_IDs_unchanged'] and not sm['active_collection_guide_changed'] and sm['new_mandatory_questions']==0 and not sm['new_case_quota'] and not sm['requires_named_publishable_case'], 'T02 second no question/guide/casequota or eligibility expansion')
    require(not sm['scored'] and not sm['validated'] and not sm['prior_model_reruns'] and not sm['prior_recommendation_counts_reused'], 'T02 second not a score, market validation, model rerun or demand transfer')
    for k in ['actual_offer_exposures','actual_buyer_member_input','actual_rights_grants','actual_commitments','financial_inputs','prices','external_actions']:
        require(sm[k]==[], 'T02 second actual/financial/action array blank: '+k)
    fit=data['04-table/T02-offer-fit-aid.json']
    require(all(v is None for v in fit['blank_offer_fit'].values()) and not fit['new_participant_form'] and not fit['new_case_quota'] and not fit['practitioner_count_rule_changed'] and fit['actual_offer_fit_records']==[], 'T02 second optional aid blank/no new form or count condition')
    for x in data['08-qa/T02-second-check-captures.json']['files']:
        require(hashlib.sha256((ROOT/x['path']).read_bytes()).hexdigest()==x['sha256'], 'T02 second retained capture hash: '+x['path'])
        if 'reader' in Path(x['path']).name.lower():require(x['kind']=='selected_reader_extract', 'T02 second selectedreader not original: '+x['path'])
    bridge=data['04-table/research-notes/t02-second-check/competitors/prior-study-bridge-check.json']
    require(bridge['check_count']==126 and bridge['selected_saved_records']==24 and bridge['semantic_rereads']==3 and bridge['no_model_reruns'] and not bridge['prior_recommendation_counts_reused'] and all(x['passed']for x in bridge['checks']), 'T02 second threequestion24answers126lineagechecks with3semanticrereads only')
    require(hashlib.sha256((ROOT/bridge['bridge_path']).read_bytes()).hexdigest()==bridge['bridge_sha256'], 'T02 second exact prior bridge unchanged')
    route=data['08-qa/T02-second-routing-walkthrough.json']
    require(route['status']=='passed_internal_T02_second_constructed_applications' and route['route_count']==8 and route['check_count']==199 and all(x['passed']for x in route['checks']), 'T02 second eightconstructedapplications199rootchecks')
    require(not route['practitioner_validation'] and not route['commercial_validation'] and route['actual_participant_cases']==0 and route['new_mandatory_questions']==0 and route['financial_inputs_added']==0, 'T02 second constructed applications not fieldwork or empirical validation')
    for rel in ['04-table/T02-SECOND-CHECK-READOUT.md','04-table/T02-OFFER-FIT-AND-WORDING.md']:
        require(set(re.findall(r'CLM-\d{4}',(ROOT/rel).read_text()))<=claim_ids, 'T02 second prose claim references resolve: '+rel)
    review=data.get('08-qa/t02-second-review/integration-checks.json')
    if review:
        require(all(x['passed']for x in review['checks']) and not review.get('open_substantive_issues',[]), 'T02 second independent integrated review passed')
        require((ROOT/'08-qa/T02-second-check-independent-review.md').is_file(), 'T02 second independent review retained')
        require(review['status']=='passed_for_internal_T02_second_challenge' and review['check_count']==1011, 'T02 second independent integrated review status and current count')
        snaps={x['original_path']:x for x in data['04-table/research-notes/t02-second-check/reviewed-before-status/manifest.json']['records']}
        for x in review['reviewed_artifacts']:
            target=snaps.get(x['path'],{}).get('snapshot_path',x['path'])
            require(hashlib.sha256((ROOT/target).read_bytes()).hexdigest()==x['sha256'], 'T02 second exact independently reviewed content preserved: '+x['path'])
            if x['path'] in snaps:
                b=data[target];a=data[x['path']]
                require({k:v for k,v in b.items()if k not in ['status','review_basis']}=={k:v for k,v in a.items()if k not in ['status','review_basis']}, 'T02 second post-review status/basis-only keys: '+x['path'])
        require(sm['status']=='second_challenge_reviewed_internal_design', 'T02 second internal design status not commercial validation')
        require(route['model_sha256_at_walkthrough']==snaps['04-table/T02-second-challenge-map.json']['sha256'], 'T02 second analyst applications reconcile to reviewed pre-status map')
        p=next(x for x in packages if x['work_package_id']=='WP12')
        require(p['status']=='T01_T02_second_design_reviewed_validation_pending' and p['T02_second_challenge_reviewed'] and not p['T02_buyer_validated'] and not p['T03_conversations_complete'], 'T02 second WP12 design reviewed, actual validation pending')


questions=data['01-method/question-map.json']
require(questions['status']=='draft_for_user_review' and not questions['client_approved'] and not questions['participant_tested'], 'Question draft not misreported as approved or participant tested')
require([q['question_id'] for q in questions['records']]==[f'Q{i:03}' for i in range(1,15)], 'Fourteen ordered core questions present')
require([q['number'] for q in questions['records'] if q['route']=='recent_case']==list(range(7,14)), 'Recent case routing matches questions seven to thirteen')
require(all(q['purpose'] and q['topic_ids'] and q['wording'] for q in questions['records']), 'Every question has wording purpose and module mapping')
require(questions['version']=='0.2' and questions==data['01-method/question-map-v0.2.json'], 'Canonical map matches version zero two snapshot')
require([q['wording'] for q in questions['records']]==[q['wording'] for q in data['01-method/question-map-v0.1.json']['records']], 'Core wording preserved across checkpoint versions')
require(data['08-qa/WP02-v0.2-routing-walkthrough.json']['status']=='passed' and data['08-qa/WP02-v0.2-routing-walkthrough.json']['test_count']==19, 'Version zero two routing has nineteen passed synthetic cases')
for path in ['05-analysis/observations.json', '05-analysis/charts.json', '04-table/financial-inputs.json']:
    require(data[path]['records'] == [], f'Unperformed research stays empty in {path}')

link_count = 0
for file in ROOT.rglob('*.md'):
    for target in re.findall(r'\]\(([^)]+)\)', file.read_text()):
        if target.startswith(('https://', 'http://', '#')):
            continue
        target = unquote(target.split('#', 1)[0])
        if target:
            require((file.parent / target).resolve().exists(), f'Local link resolves in {file.relative_to(ROOT)}')
            link_count += 1

result = {'status': 'passed', 'date': data['00-control/work-packages.json']['updated_on'], 'checks': len(checks), 'json_files': len(data), 'source_records': len(sources), 'claim_records': len(claims), 'question_records':len(questions['records']), 'internal_design_findings':len(data['05-analysis/findings.json']['records']), 'deliverable_records': len(deliverables), 'work_packages': len(packages), 'local_markdown_links_checked': link_count, 'scope': 'T02 second challenge evidence/use/time/work/fulfilment/concept-state conditions; T02 three concrete internal propositions, use/rights/delivery and inactive draft guide; T01 second challenge historical/market/comparator/prior-study/participation lenses and selective conditions; T01 six distinct public comparable mechanisms and T02 untested propositions; WP03 prepared inactive collection pack; R01–R07 evidence/capture and synthesis consistency; R08 preparatory linked views, report integration, first-pass and version0.2 fifteen constructed applications, second-challenge evidence/time/object conditions, held claims and original-input dependency; prior/client/core/canonical preservation, WP02 question mapping and blank unperformed research. No final publication, participant testing, commercial validation, product trial, employer forecast or human fieldwork implied.'}
print(json.dumps(result, indent=2))
