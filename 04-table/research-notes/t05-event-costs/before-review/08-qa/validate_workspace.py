from pathlib import Path
import json
import re
import math
import zipfile
import xml.etree.ElementTree as ET
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
t04_before={x['original_path']:x for x in data.get('04-table/research-notes/t04/before-review/manifest.json',{}).get('records',[])}
t04_record_map=data.get('08-qa/T04-record-map.json')
t05r_before={x['original_path']:x for x in data.get('04-table/research-notes/t05-research-costs/before-review/manifest.json',{}).get('records',[])}
t05r_record_map=data.get('08-qa/T05R-record-map.json')
t05rs_before={x['original_path']:x for x in data.get('04-table/research-notes/t05r-second-check/before-review/manifest.json',{}).get('records',[])}
t05rs_record_map=data.get('08-qa/T05R-second-check-record-map.json')
t05s_before={x['original_path']:x for x in data.get('04-table/research-notes/t05-service-costs/before-review/manifest.json',{}).get('records',[])}
t05s_record_map=data.get('08-qa/T05S-record-map.json')
t05ss_before={x['original_path']:x for x in data.get('04-table/research-notes/t05s-second-check/before-review/manifest.json',{}).get('records',[])}
t05ss_record_map=data.get('08-qa/T05S-second-check-record-map.json')
def t05ss_asof(path):
    return t05ss_before.get(path,{}).get('snapshot_path',path) if t05ss_record_map else path
def t05s_asof(path):
    return t05s_before.get(path,{}).get('snapshot_path',path) if t05s_record_map else path
def t05rs_asof(path):
    return t05rs_before.get(path,{}).get('snapshot_path',t05s_asof(path)) if t05rs_record_map else t05s_asof(path)
def t05r_asof(path):
    return t05r_before.get(path,{}).get('snapshot_path',path) if t05r_record_map else path
def t04_asof(path):
    return t04_before.get(path,{}).get('snapshot_path',path) if t04_record_map else path
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
            require(bool(x.get('t01_source_candidate_id') or x.get('t01_second_source_candidate_id') or x.get('t02_second_source_candidate_id') or x.get('t04_source_candidate_id') or x.get('t05r_source_candidate_id') or x.get('t05r_second_source_candidate_id') or x.get('t05s_source_candidate_id') or x.get('t05s_second_source_candidate_id')), 'Later source addition explicitly belongs to subsequent T01/T02/T04/T05 research, not retroactive R08 evidence')
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
    require(len(oldsrc)==223 and len(data[t04_asof('02-evidence/registers/sources.json')]['records'])==225 and len(data[t04_asof('02-evidence/registers/claims.json')]['records'])==443, 'T02 second as-of225sources443claims reconcile')
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


if t04_record_map:
    require(set(t04_record_map['source_map'].values())<=source_ids and set(t04_record_map['claim_map'].values())<=claim_ids, 'T04 canonical mapping resolves')
    before_sources=data[t04_before['02-evidence/registers/sources.json']['snapshot_path']]['records']
    before_claims=data[t04_before['02-evidence/registers/claims.json']['snapshot_path']]['records']
    require(len(before_sources)==225 and len(before_claims)==443, 'T04 begins from preserved225source443claim checkpoint')
    require(len(data[t05r_asof('02-evidence/registers/sources.json')]['records'])==225+t04_record_map['new_source_routes']==t04_record_map['canonical_sources'] and len(data[t05r_asof('02-evidence/registers/claims.json')]['records'])==443+t04_record_map['new_claim_records']==t04_record_map['canonical_claims'], 'T04 as-of canonical append reconciles')
    require(claims[:len(before_claims)]==before_claims, 'T04 preserves every prior claim record exactly')
    current_by={x['source_id']:x for x in sources}
    for old in before_sources:
        current=current_by[old['source_id']]
        require({k:v for k,v in old.items()if k not in ['additional_reviews','related_topic_ids']}=={k:v for k,v in current.items()if k not in ['additional_reviews','related_topic_ids']}, 'T04 prior source base preserved: '+old['source_id'])
        require(all(v in current.get('additional_reviews',[])for v in old.get('additional_reviews',[])) and set(old.get('related_topic_ids',[]))<=set(current.get('related_topic_ids',[])), 'T04 prior source reviews/topics preserved: '+old['source_id'])
    require(data['05-analysis/findings.json']==data[t04_before['05-analysis/findings.json']['snapshot_path']], 'T04 preserves findings without invented empirical results')
    for path,key in [('02-evidence/registers/searches.json','records'),('02-evidence/registers/source-aliases.json','url_aliases')]:
        old=data[t04_before[path]['snapshot_path']].get(key,[])
        require(data[path].get(key,[])[:len(old)]==old, 'T04 preserves prior canonical history: '+path)
    for x in t04_before.values():
        require(hashlib.sha256((ROOT/x['snapshot_path']).read_bytes()).hexdigest()==x['sha256'], 'T04 exact before-file snapshot preserved: '+x['original_path'])
    for x in data['08-qa/T04-baseline-manifest.json']['files']:
        require(hashlib.sha256((ROOT/x['path']).read_bytes()).hexdigest()==x['sha256'], 'T04 prior/core/client baseline file preserved: '+x['path'])
    for x in data['08-qa/T02-second-check-completion.json']['artifacts']:
        require(hashlib.sha256((ROOT/t04_asof(x['path'])).read_bytes()).hexdigest()==x['sha256'], 'T02 second completion reconciles to T04 as-of artifact: '+x['path'])
    require(not t04_record_map['commercial_validation'] and t04_record_map['participant_observations']==0 and t04_record_map['financial_inputs_added']==0, 'T04 append is public desktop evidence only')
    inputs=data['04-table/T04-input-requirements.json'];formulas=data['04-table/T04-formula-design.json']
    require(len(inputs['requirements'])==10 and [x['input_group_id']for x in inputs['requirements']]==[f'IN{i:02}'for i in range(1,11)] and all(x['actual_values']is None for x in inputs['requirements']), 'T04 ten input groups retain unpopulated actual values')
    require(inputs['blank_is_not_zero'] and inputs['explicit_zero_requires_basis'] and inputs['unselected_route_missing_inputs_do_not_block_selected_route'] and inputs['selected_missing_critical_input_must_remain_visible'], 'T04 missing explicit-zero and selected-route rules retained')
    require(all(inputs[k]==[]for k in ['actual_financial_inputs','actual_quotes','actual_partner_orders','actual_customers']) and not inputs['workbook_created'] and not inputs['Texas_city_confirmed'], 'T04 input design creates no quotes sales workbook or Texas-city selection')
    require([x['formula_id']for x in formulas['records']]==[f'FM{i:02}'for i in range(1,11)] and formulas['actual_calculated_results']==[] and not formulas['workbook_created'], 'T04 ten algebraic concepts contain no calculated workbook results')
    break_even=next(x for x in formulas['records']if x['formula_id']=='FM07')
    require(break_even['decision_branches']==[{'condition':'gap_lte_zero','result':'zero_additional_units'},{'condition':'gap_positive_and_margin_positive','result':'ceiling_gap_over_margin'},{'condition':'gap_positive_and_margin_nonpositive','result':'no_finite_break_even'}], 'T04 break-even tests covered gap before positive-gap margin feasibility')
    routes=data['04-table/research-notes/t04/routes/route-candidates.json'];units=data['04-table/research-notes/t04/routes/model-unit-spec.json'];assumptions=data['04-table/research-notes/t04/routes/assumptions-and-validation.json']
    byroute={x['route_id']:x for x in routes['routes']}
    require(list(byroute)==['A-PILOT','B-PILOT','A-ANNUAL','B-ANNUAL'] and [x['event_count']for x in routes['routes']]==[0,1,0,4], 'T04 four matched research-only/event route definitions retained')
    require(all(byroute[x['comparison_pair']]['comparison_pair']==x['route_id'] and x['core_edition_count']is None and x['horizon_start']is None and x['horizon_end']is None for x in routes['routes']), 'T04 paired route references reconcile without invented horizon/edition values')
    require([x['revenue_id']for x in routes['revenue_lines']]==[f'RV{i:02}'for i in range(1,5)] and all(x['price']is None and x['quantity']is None for x in routes['revenue_lines']), 'T04 four revenue units remain unpriced and unvalidated')
    require([x['cost_id']for x in routes['cost_objects']]==[f'CO{i:02}'for i in range(1,8)] and all(x['amount']is None for x in routes['cost_objects']), 'T04 seven cost objects remain uncosted')
    require(all(routes[k]==[]for k in ['actual_orders','actual_events','actual_receipts','actual_customers','actual_rights','financial_inputs','price_recommendations','external_actions']) and routes['adopted_model']is None, 'T04 route design does not invent transactions events or adoption')
    require([x['unit_id']for x in units['units']]==[f'U{i:02}'for i in range(1,16)] and not units['workbook_created'] and units['actual_model_outputs']==[] and units['financial_inputs']==[], 'T04 fifteen model units retain blank outputs')
    investment=units['initial_contract_investment']
    require(investment['currency']=='USD' and investment['total']==1500 and investment['report_allocation']==1000 and investment['Table_allocation']==500 and investment['not_automatically_sunk_or_paid'], 'T04 current contract investment and payment boundary preserved')
    require(len(assumptions['records'])==10 and all(x['value']is None and not x['validated']for x in assumptions['records']) and assumptions['no_actual_validation'] and assumptions['no_financial_assumptions_populated'], 'T04 ten unresolved dependencies remain unpopulated assumptions')
    for rel in ['04-table/T04-COMMERCIAL-ROUTES-READOUT.md','04-table/T04-PUBLIC-COST-SCREEN.md','04-table/T04-INPUT-AND-MODEL-RULES.md']:
        require((ROOT/rel).is_file() and set(re.findall(r'CLM-\d{4}',(ROOT/rel).read_text()))<=claim_ids, 'T04 readout exists with resolving bounded claims: '+rel)
    model=data['04-table/T04-model-design.json']
    require(model['route_ids']==list(byroute) and model['comparison_pairs']==[['A-PILOT','B-PILOT'],['A-ANNUAL','B-ANNUAL']], 'T04 integrated route pairs match detailed case definitions')
    require(model['views']==['additional_cash_operating','full_repeatable_resources','initial_investment_recovery'] and set(model['required_common_basis'])=={'horizon','selected_editions_and_evidence','common_research_work','free_and_bundled_entitlements','revenue_cost_and_currency_definitions'}, 'T04 three financial views use an explicit matched comparison basis')
    for key,path in [('route_design_path','04-table/research-notes/t04/routes/route-candidates.json'),('unit_spec_path','04-table/research-notes/t04/routes/model-unit-spec.json'),('input_requirements_path','04-table/T04-input-requirements.json'),('formula_design_path','04-table/T04-formula-design.json'),('open_assumptions_path','04-table/research-notes/t04/routes/assumptions-and-validation.json'),('cost_evidence_map_path','04-table/T04-cost-evidence-map.json')]:
        require(model[key]==path and path in data, 'T04 integrated model design resolves its component: '+key)
    require(model['no_automatic_event_sales_attribution'] and model['practitioner_free_full_research_preserved'] and model['current_commission_not_repeated_unit_cost'] and model['cost_screen_is_not_selected_budget'], 'T04 integrated design preserves event-attribution free-benefit and cost boundaries')
    require(all(model[k]==[]for k in ['selected_budget_inputs','actual_quotes','actual_orders','actual_receipts','actual_participants','financial_inputs','external_actions']) and model['selected_venue']is None and not model['workbook_created'] and not model['commercial_validation'] and not model['fieldwork_activated'], 'T04 integrated design remains unpopulated and inactive')
    require(model['remaining_T05_work'] and model['not_completed'], 'T04 keeps T05 build and unresolved delivery work visible')
    acceptance=data['08-qa/T04-to-T05-acceptance-cases.json']
    require(acceptance['status']=='acceptance_test_design_for_T05_not_workbook_results' and acceptance['actual_workbook_results']==[] and all(not x['workbook_test_executed']for x in acceptance['cases']), 'T04 proposed T05 acceptance cases are unexecuted test design')
    require(len({x['test_id']for x in acceptance['cases']})==len(acceptance['cases']) and all(x['purpose'] and x['constructed_inputs'] and x['expected_behaviour']for x in acceptance['cases']), 'T04 constructed acceptance cases retain unique IDs inputs and expected behaviour')
    costmap=data['04-table/T04-cost-evidence-map.json'];rawcost=data['04-table/research-notes/t04/uk-costs/cost-candidates.json']
    require(costmap['source_routes']==len(t04_record_map['source_map']) and set(costmap['all_source_ids'])==set(t04_record_map['source_map'].values()) and set(costmap['all_claim_ids'])==set(t04_record_map['claim_map'].values()), 'T04 public cost map reconciles canonical source/claim mapping')
    require(len(costmap['records'])==costmap['distinct_venue_examples']==len(rawcost['records']) and set(costmap['synthesis_claim_ids'])<=claim_ids, 'T04 distinct venue examples and synthesis references reconcile')
    rawby={x['cost_candidate_id']:x for x in rawcost['records']}
    for x in costmap['records']:
        require({k:x[k]for k in rawby[x['cost_candidate_id']]}==rawby[x['cost_candidate_id']], 'T04 integrated cost context preserves inspected candidate facts: '+x['cost_candidate_id'])
        require(x['source_ids']==[t04_record_map['source_map'][v]for v in x['source_candidate_ids']] and x['claim_ids']==[t04_record_map['claim_map'][v]for v in x['claim_candidate_ids']], 'T04 venue-specific source and claim mapping reconciles: '+x['cost_candidate_id'])
        require(not x['selected_budget_input'] and not x['selected_for_pilot'] and not x['quote_received'] and x['quote_total']is None and x['budget_amount']is None and not x['financial_input_eligible'] and not x['future_2027_budget_eligible'], 'T04 published venue facts not represented as selected quoted or future budget: '+x['cost_candidate_id'])
        require(x['actual_participant_count']==0 and x['contact_attempts']==0 and bool(x['unknown_inputs']), 'T04 venue screen retains unresolved terms without invented attendance/contact: '+x['cost_candidate_id'])
    require(costmap['selected_venue']is None and all(costmap[k]==[]for k in ['actual_quotes','selected_budget_inputs','financial_inputs','external_actions']) and costmap['source_currentness_not_future_price_applicability'], 'T04 currentness and future-budget boundaries preserved')
    require(costmap['historical_exclusion_path']in data and not rawcost['historical_exclusion']['financial_input_eligible'], 'T04 historical Benares evidence preserved and excluded from financial selection')
    captures=data['08-qa/T04-captures.json']
    core_originals=[];parsed=[];renders=[];historical=[]
    for x in captures['records']:
        require(hashlib.sha256((ROOT/x['path']).read_bytes()).hexdigest()==x['sha256'], 'T04 retained evidence hash: '+x['path'])
        if x['core_evidence']:
            if x['kind']in ['retained_original_html','retained_original_pdf']:core_originals.append(x)
            elif x['kind']=='parsed_original_text':parsed.append(x)
            else:
                require(x['kind']=='rendered_source_page_not_new_original', 'T04 core rendered aid not promoted to original: '+x['path'])
                renders.append(x)
            require(x['source_id']in set(t04_record_map['source_map'].values()) and ('source_candidate_id'not in x or x['source_id']==t04_record_map['source_map'][x['source_candidate_id']]), 'T04 core capture canonical mapping resolves: '+x['path'])
        else:
            require(x['kind'].startswith('excluded_historical_') and 'excluded-historical/'in x['path'], 'T04 excluded historical aid retains explicit classification: '+x['path'])
            historical.append(x)
    require(len(core_originals)==captures['core_primary_originals']==len(t04_record_map['source_map']) and len(parsed)==captures['core_parsed_extracts'] and len(renders)==captures['core_page_renders'] and len(historical)==captures['excluded_historical_artifacts'], 'T04 original extract render and historical counts reconcile without extra source inflation')
    require({x['source_id']for x in core_originals}==set(t04_record_map['source_map'].values()) and captures['new_independent_datasets']==0, 'T04 originals cover mapped routes without claiming independent datasets')
    review=data['08-qa/t04-review/integration-checks.json']
    require(review['status']=='passed_for_internal_T04_design_and_public_cost_screen' and review['checks'] and all(x['passed']for x in review['checks']) and review['open_substantive_issues']==[], 'T04 independent integrated design/public-cost review passed without open substantive issues')
    require(not review['workbook_audited'] and not review['commercial_validation'], 'T04 independent review does not imply workbook or commercial validation')
    require((ROOT/'08-qa/t04-review/INTEGRATED-REVIEW.md').is_file(), 'T04 independent review readout retained')
    for x in review['reviewed_artifacts']:
        require(hashlib.sha256((ROOT/t05r_asof(x['path'])).read_bytes()).hexdigest()==x['sha256'], 'T04 exact independently reviewed as-of artifact retained: '+x['path'])
    require({x['source_id']for x in review['public_cost_sources_reviewed']}==set(t04_record_map['source_map'].values()), 'T04 independent source review covers all mapped public-cost routes')
    for x in review['public_cost_sources_reviewed']:
        original=current_by[x['source_id']]
        require(x['url']==original['url'] and x['original_sha256']==original['capture_sha256'] and t04_record_map['source_map'][x['candidate_id']]==x['source_id'], 'T04 independent source URL/hash matches canonical original: '+x['source_id'])


if t05r_record_map:
    require(bool(t05r_before), 'T05 research-cost inputs have an exact prechange snapshot manifest')
    for x in t05r_before.values():
        require(hashlib.sha256((ROOT/x['snapshot_path']).read_bytes()).hexdigest()==x['sha256'], 'T05 exact prechange artifact preserved: '+x['original_path'])
    oldsrc=data[t05r_before['02-evidence/registers/sources.json']['snapshot_path']]['records']
    oldclm=data[t05r_before['02-evidence/registers/claims.json']['snapshot_path']]['records']
    require(len(oldsrc)==230 and len(oldclm)==459, 'T05 research-cost work begins from 230 sources and 459 claims')
    require(len(data[t05rs_asof('02-evidence/registers/sources.json')]['records'])==len(oldsrc)+t05r_record_map['new_source_routes']==t05r_record_map['canonical_sources'] and len(data[t05rs_asof('02-evidence/registers/claims.json')]['records'])==len(oldclm)+t05r_record_map['new_claim_records']==t05r_record_map['canonical_claims'], 'T05 first-component as-of source and claim additions reconcile dynamically')
    require(set(t05r_record_map['source_map'].values())<=source_ids and set(t05r_record_map['claim_map'].values())<=claim_ids, 'T05 source and claim candidate mapping resolves')
    require(claims[:len(oldclm)]==oldclm, 'T05 preserves earlier claims exactly')
    current_by={x['source_id']:x for x in sources}
    for old in oldsrc:
        current=current_by[old['source_id']]
        require({k:v for k,v in old.items()if k not in ['additional_reviews','related_topic_ids']}=={k:v for k,v in current.items()if k not in ['additional_reviews','related_topic_ids']}, 'T05 prior source base preserved: '+old['source_id'])
        require(all(v in current.get('additional_reviews',[])for v in old.get('additional_reviews',[])) and set(old.get('related_topic_ids',[]))<=set(current.get('related_topic_ids',[])), 'T05 prior source reviews/topics preserved: '+old['source_id'])
    require(data['05-analysis/findings.json']==data[t05r_before['05-analysis/findings.json']['snapshot_path']], 'T05 cost planning creates no empirical research findings')
    for path,key in [('02-evidence/registers/searches.json','records'),('02-evidence/registers/source-aliases.json','url_aliases')]:
        old=data[t05r_before[path]['snapshot_path']].get(key,[])
        require(data[path].get(key,[])[:len(old)]==old, 'T05 preserves canonical history: '+path)
    for x in data['08-qa/T05R-baseline-manifest.json']['files']:
        require(hashlib.sha256((ROOT/x['path']).read_bytes()).hexdigest()==x['sha256'], 'T05 earlier/core/client baseline artifact preserved: '+x['path'])
    for x in data['08-qa/T04-completion-check.json']['artifacts']:
        require(hashlib.sha256((ROOT/t05r_asof(x['path'])).read_bytes()).hexdigest()==x['sha256'], 'T04 completion reconciles to exact pre-T05 artifact: '+x['path'])


    component=data['04-table/T05-research-cost-map.json']
    finance=data[t05s_asof('04-table/financial-inputs.json')];inputs=finance['records']
    input_by={x['input_id']:x for x in inputs}
    require(len(input_by)==len(inputs) and set(component['financial_input_ids'])==set(input_by), 'T05 component input IDs are unique and fully mapped')
    require(len(inputs)==t05r_record_map['financial_inputs_added'] and t05r_record_map['component_only'] and not t05r_record_map['commercial_validation'] and t05r_record_map['participant_observations']==0, 'T05 appended financial inputs are limited to the stated component')
    require(finance['actual_quotes']==[] and finance['actual_spend_records']==[] and not finance['full_model_complete'], 'T05 component has no quotes actual spend or completed full model')
    require(not component['full_financial_model_complete'] and not component['current_commission_added_to_future_task_valuation'] and not component['current_contract_fee_changed'] and component['practitioner_free_full_research_preserved'], 'T05 component preserves contract/free benefit and avoids duplicate current-fee valuation')
    require(all(component[k]==[]for k in ['actual_supplier_quotes','actual_staffing','actual_timesheets','actual_practitioner_contributions','external_actions']) and component['additional_unpriced_costs'], 'T05 component retains unpriced additional work without actual activity')
    require(component['unpriced_JGA_rates_must_keep_combined_labour_value_unavailable'], 'T05 unknown retained JGA rates cannot disappear into a full labour total')
    require(set(component['source_ids'])==set(t05r_record_map['source_map'].values()) and set(component['claim_ids'])==set(t05r_record_map['claim_map'].values()), 'T05 component evidence map reconciles to canonical additions')
    for x in inputs:
        require(x['component_id']==component['component_id'] and x['model_usage']=='future_edition_labour_comparison_only', 'T05 financial input has bounded component use: '+x['input_id'])
        require(not x['actual_supplier_quote'] and not x['actual_cost'] and not x['budget_authorised'] and x['cash_classification']is None, 'T05 scenario input is not an actual quoted authorised or cash cost: '+x['input_id'])
        require(set(x['source_ids'])<=source_ids and set(x['claim_ids'])<=claim_ids and bool(x['basis']), 'T05 input source/claim references and interpretation are retained: '+x['input_id'])
    benchmarks={x['benchmark_id']:x for x in data['04-table/research-notes/t05-research-costs/benchmarks/labour-benchmark-options.json']['records']}
    for ident in component['role_rate_input_ids'].values():
        x=input_by[ident];b=benchmarks[x['benchmark_id']]
        require(x['value']==b['value'] and x['unit']==b['unit'] and x['currency']==b['currency'] and x['evidence_class']==b['statistic'], 'T05 published role rate keeps original value unit currency and statistic: '+ident)
        require(set(x['source_ids'])=={t05r_record_map['source_map'][v]for v in b['source_candidate_ids']} and set(x['claim_ids'])=={t05r_record_map['claim_map'][v]for v in b['claim_candidate_ids']}, 'T05 selected role benchmark lineage reconciles: '+ident)
    day=input_by[component['day_normalisation_input_id']]
    require(day['evidence_class']=='analyst_conversion_assumption' and isinstance(day['value'],(int,float)) and day['value']>0 and day['source_ids']==[] and day['claim_ids']==[], 'T05 day-rate hourly divisor is a positive explicit analyst assumption')
    contributors=input_by[component['contributor_scenarios_input_id']]
    require(contributors['evidence_class']=='analyst_volume_scenarios' and set(contributors['value'])=={'low','base','high'} and all(6<=v<=10 for v in contributors['value'].values()), 'T05 contributor scenarios stay within the research target without claiming recruitment')
    workload=data[component['workload_source_path']]
    proposed={x['workload_id']:x for x in workload['report_provider_tasks']+workload['JGA_retained_tasks']}
    tasks={x['workload_id']:x for x in component['tasks']}
    require(len(tasks)==len(component['tasks']) and set(tasks)==set(proposed), 'T05 task map covers provider and retained JGA work once')
    work_ids={x['work_id']for x in data['04-table/T02-delivery-map.json']['items']}
    for ident,t in tasks.items():
        x=input_by[t['hours_input_id']];w=proposed[ident]
        require(t['rate_input_id']in input_by and set(t['T02_work_ids'])<=work_ids and t['T02_work_ids']==w['T02_work_ids'], 'T05 task resolves rate and T02 work-object mapping: '+ident)
        require(x['workload_id']==ident and x['value']==w['planning_hours'] and x['unit_basis']==t['unit_basis']==w['unit'] and x['actual_hours']is None, 'T05 task hours retain explicit original planning basis: '+ident)
        require(x['evidence_class']=='analyst_effort_assumption' and set(x['value'])=={'low','base','high'} and all(isinstance(v,(int,float)) and v>=0 for v in x['value'].values()), 'T05 task effort is nonnegative scenario data rather than observed work: '+ident)
        if t['role_group']=='JGA':
            rate=input_by[t['rate_input_id']]
            require(rate['evidence_class']=='unresolved_internal_resource_rate' and rate['value']is None and rate['workload_id']==ident and rate['source_ids']==[] and rate['claim_ids']==[], 'T05 retained JGA rate remains unknown rather than a freelancer substitution: '+ident)
        else:
            require(t['rate_input_id']==component['role_rate_input_ids'][t['role_group']], 'T05 provider task uses the mapped role comparison rate: '+ident)
    require(t05r_record_map['workbook_created']==component['workbook_created'], 'T05 workbook creation status is consistent across component records')
    captures=data['08-qa/T05R-captures.json']
    originals=[x for x in captures['records']if x['kind']=='retained_original_html']
    extracts=[x for x in captures['records']if x['kind']=='parsed_original_text']
    require(len(originals)==captures['primary_originals']==len(t05r_record_map['source_map']) and len(extracts)==captures['parsed_extracts'] and len(originals)+len(extracts)==len(captures['records']), 'T05 source inventory distinguishes retained originals from extracted review aids')
    require({x['source_id']for x in originals}=={x['source_id']for x in extracts}==set(t05r_record_map['source_map'].values()) and captures['new_independent_datasets']==0, 'T05 labour references cover mapped routes without dataset inflation')
    for x in captures['records']:
        require(hashlib.sha256((ROOT/x['path']).read_bytes()).hexdigest()==x['sha256'], 'T05 retained labour evidence hash: '+x['path'])
    if component['workbook_created']:
        output=Path(component['workbook_absolute_path'])
        require(output.is_absolute() and output.is_file() and output.suffix.lower()=='.xlsx', 'T05 partial research/staff workbook exists at its recorded output path')
        qa=data[component['workbook_qa_path']];cellmap=data['08-qa/t05r-workbook/cell-map.json']
        require(Path(qa['workbook_path'])==output==Path(cellmap['workbook_path']) and hashlib.sha256(output.read_bytes()).hexdigest()==qa['workbook_sha256']==component['workbook_sha256'], 'T05 workbook and QA/cell-map paths resolve to the exact exported bytes')
        require(component['workbook_cell_map_path']=='08-qa/t05r-workbook/cell-map.json' and component['independent_review_path']=='08-qa/t05r-review/integration-checks.json', 'T05 component points to its exact cell map and independent review')
        require(qa['status']=='passed' and qa['visual_review_complete'] and qa['all_temporary_input_changes_restored'], 'T05 workbook calculation and visual checks passed with test inputs restored')
        require(qa['authoring_engine']=='@oai/artifact-tool' and not qa['native_Excel_application_tested'], 'T05 workbook evidence states artifact-engine scope without claiming native Excel application testing')
        cases={x['test_id']:x for x in qa['tests']}
        required_cases={'CASE-low','CASE-base','CASE-high','EDIT-HOURS','MISSING-UNSELECTED','MISSING-SELECTED','ZERO-HOURS','ZERO-JGA-RATE','COMPLETE-JGA-RATES','BLANK-JGA-RATES','DAY-LENGTH-BLANK','DAY-LENGTH-ZERO','MISSING-RATE','INVALID-CASE','RESTORED-BASE'}
        require(len(cases)==len(qa['tests']) and required_cases<=set(cases) and all(x['passed']for x in qa['tests']), 'T05 workbook exercised active cases edits missing inputs valid zeros invalid selection and restoration')
        require(qa['final_saved_case']=='Working' and qa['final_saved_outputs']['JGA_value_GBP']=='n.a.' and qa['final_saved_outputs']['combined_labour_GBP']=='n.a.', 'T05 saved case preserves unavailable retained and combined labour values while JGA rates are missing')
        expected={}
        for scenario in ['low','base','high']:
            ph=0;pv=0;jh=0
            for t in component['tasks']:
                task=input_by[t['hours_input_id']];hours=task['value'][scenario]*(contributors['value'][scenario]if t['unit_basis']=='per_usable_contributor'else 1)
                if t['role_group']=='JGA':jh+=hours
                else:
                    rate=input_by[t['rate_input_id']];ph+=hours;pv+=hours*rate['value']/(day['value']if rate['unit']=='day'else 1)
            expected[scenario]=(ph,pv,jh)
            actual=cases['CASE-'+scenario]['detail']['actual']
            require(len(actual)==3 and all(abs(a-b)<0.000001 for a,b in zip(actual,expected[scenario])), 'T05 recalculated effort case reconciles independently to mapped task and rate inputs: '+scenario)
        final=qa['final_saved_outputs']
        require(abs(final['provider_hours']-expected['base'][0])<0.000001 and abs(final['provider_labour_GBP']-expected['base'][1])<0.000001 and abs(final['JGA_hours']-expected['base'][2])<0.000001, 'T05 saved working outputs reconcile to independent input arithmetic')
        require(cellmap['sheets']==['Research cost','Inputs'] and cellmap['case_selector']=='Inputs!D4' and cellmap['provider_hours']=='Research cost!E6' and cellmap['provider_labour_GBP']=='Research cost!E7' and cellmap['JGA_hours']=='Research cost!E8', 'T05 compact worksheet structure and principal result cells are recorded consistently')
        require(set(cellmap['task_input_rows'])==set(tasks) and len(set(cellmap['task_input_rows'].values()))==len(tasks), 'T05 workbook records one distinct input row per research/JGA task')
        require(set(x['sheet']for x in qa['renders'])==set(cellmap['sheets']) and all(Path(x['path']).is_file() and x['range']for x in qa['renders']), 'T05 visual evidence covers both sheets with saved rendered ranges')
        require({x['path']for x in qa['renders']}=={x['path']for x in qa['visual_reviewed_artifacts']} and all(hashlib.sha256(Path(x['path']).read_bytes()).hexdigest()==x['sha256']for x in qa['visual_reviewed_artifacts']), 'T05 visual review hashes identify the exact final rendered sections')
        exportpath=Path(qa['saved_export_checks_path'])
        require(exportpath.is_file(), 'T05 saved-export inspection record is retained')
        exported=json.loads(exportpath.read_text())
        require(exported['workbook_sha256']==qa['workbook_sha256'] and exported['restored_working_case'] and exported['saved_JGA_rates_blank'] and exported['formula_error_cells']==[] and not exported['native_Excel_application_tested'], 'T05 saved XLSX inspection confirms restored values and blank JGA rates without native-app claim')
        require(exported['saved_outputs']=={'E6':'174','E7':'8726.14','E8':'23','E9':'n.a.','E10':'n.a.'} and exported['chart_formula_bindings']==["'Research cost'!$K$7:$K$11","'Research cost'!$M$7:$M$11"], 'T05 saved XLSX result cells and chart source bindings agree with the verified component')
        scan=Path(qa['formula_error_scan_path'])
        require(scan.is_file() and all(x.get('kind')=='notice' and '0 entries' in x.get('message','')for x in [json.loads(v)for v in scan.read_text().splitlines()if v.strip()]), 'T05 final formula-error scan records no matches')
    review=data.get('08-qa/t05r-review/integration-checks.json')
    require(not component['component_review_complete'] or (component['workbook_created'] and bool(review)), 'T05 component review-complete status requires a workbook and independent integrated review')
    if review:
        require(review['status']=='passed_for_internal_T05R_component' and review['checks'] and all(x['passed']for x in review['checks']) and review['open_substantive_issues']==[], 'T05 independent research/staffing component review passed without substantive open issues')
        require(review['workbook_audited'] and not review['full_financial_model_audited'], 'T05 independent audit covers the component without claiming full programme financial-model completion')
        for x in review['reviewed_artifacts']:
            target=Path(x['path'])if Path(x['path']).is_absolute()else ROOT/t05rs_asof(x['path'])
            require(hashlib.sha256(target.read_bytes()).hexdigest()==x['sha256'], 'T05 independently reviewed as-of artifact bytes preserved: '+x['path'])


if t05rs_record_map:
    require(len(t05rs_before)==13, 'T05 research-cost second challenge has thirteen exact prechange snapshots')
    require(t05rs_record_map['new_source_routes']==len(t05rs_record_map['source_map'])==7 and t05rs_record_map['new_claim_records']==len(t05rs_record_map['claim_map'])==18, 'T05 second adds exactly seven source routes and eighteen bounded claim records')
    for x in t05rs_before.values():
        require(hashlib.sha256((ROOT/x['snapshot_path']).read_bytes()).hexdigest()==x['sha256'], 'T05 second exact prechange file preserved: '+x['original_path'])
    oldsrc=data[t05rs_before['02-evidence/registers/sources.json']['snapshot_path']]['records']
    oldclm=data[t05rs_before['02-evidence/registers/claims.json']['snapshot_path']]['records']
    require(len(oldsrc)==235 and len(oldclm)==466, 'T05 second challenge begins from the reviewed235source466claim component')
    t05rs_sources=data[t05s_asof('02-evidence/registers/sources.json')]['records'];t05rs_claims=data[t05s_asof('02-evidence/registers/claims.json')]['records']
    require(len(t05rs_sources)==len(oldsrc)+t05rs_record_map['new_source_routes']==t05rs_record_map['canonical_sources'] and len(t05rs_claims)==len(oldclm)+t05rs_record_map['new_claim_records']==t05rs_record_map['canonical_claims'], 'T05 second as-of evidence additions reconcile dynamically')
    require(set(t05rs_record_map['source_map'].values())<=source_ids and set(t05rs_record_map['claim_map'].values())<=claim_ids, 'T05 second candidate mappings resolve')
    require(claims[:len(oldclm)]==oldclm, 'T05 second preserves every earlier claim exactly')
    current_by={x['source_id']:x for x in sources}
    for old in oldsrc:
        current=current_by[old['source_id']]
        require({k:v for k,v in old.items()if k not in ['additional_reviews','related_topic_ids']}=={k:v for k,v in current.items()if k not in ['additional_reviews','related_topic_ids']}, 'T05 second prior source base preserved: '+old['source_id'])
        require(all(v in current.get('additional_reviews',[])for v in old.get('additional_reviews',[])) and set(old.get('related_topic_ids',[]))<=set(current.get('related_topic_ids',[])), 'T05 second appends only source reviews/topics: '+old['source_id'])
    require(len(data['05-analysis/findings.json']['records'])==81 and data['05-analysis/findings.json']==data[t05rs_before['05-analysis/findings.json']['snapshot_path']], 'T05 second preserves all81 internal findings and creates no invented empirical findings')
    require(len(data[t05s_asof('04-table/financial-inputs.json')]['records'])==33 and data[t05s_asof('04-table/financial-inputs.json')]==data[t05rs_before['04-table/financial-inputs.json']['snapshot_path']], 'T05 second preserves all33 first-component financial inputs and their classifications in its exact as-of checkpoint')
    for path,key in [('02-evidence/registers/searches.json','records'),('02-evidence/registers/source-aliases.json','url_aliases')]:
        old=data[t05rs_before[path]['snapshot_path']].get(key,[])
        require(data[path].get(key,[])[:len(old)]==old, 'T05 second preserves canonical history: '+path)
    require(len(data['08-qa/T05R-second-check-baseline.json']['files'])==265, 'T05 second protected baseline retains265 artifact records')
    for x in data['08-qa/T05R-second-check-baseline.json']['files']:
        target=Path(x['path'])if Path(x['path']).is_absolute()else ROOT/t05s_asof(x['path'])
        require(hashlib.sha256(target.read_bytes()).hexdigest()==x['sha256'], 'T05 second protected baseline artifact preserved: '+x['path'])
    require(len(data['08-qa/T05R-completion-check.json']['artifacts'])==53, 'T05 first-component completion retains all53 reviewed artifact hashes')
    for x in data['08-qa/T05R-completion-check.json']['artifacts']:
        target=Path(x['path'])if Path(x['path']).is_absolute()else ROOT/t05rs_asof(x['path'])
        require(hashlib.sha256(target.read_bytes()).hexdigest()==x['sha256'], 'T05 first-component completion reconciles to exact pre-second artifact: '+x['path'])
    require(not t05rs_record_map['commercial_validation'] and t05rs_record_map['participant_observations']==0 and t05rs_record_map['financial_inputs_added']==0, 'T05 second evidence append adds no fieldwork or financial assumptions')
    original=data['08-qa/T05R-completion-check.json']
    require(hashlib.sha256(Path(original['workbook_path']).read_bytes()).hexdigest()==original['workbook_sha256'], 'T05 second leaves original workbook bytes unchanged')
    applications=data['04-table/research-notes/t05r-second-check/root/constructed-cost-applications.json']
    require(applications['status']=='passed_constructed_readonly_cost_applications' and applications['actual_workbook_edits']==0 and applications['new_financial_inputs']==0 and applications['actual_quote_or_hire']==0, 'T05 second constructed cost applications are read-only illustrations')
    require(applications['source_financial_inputs_sha256']==hashlib.sha256((ROOT/t05s_asof('04-table/financial-inputs.json')).read_bytes()).hexdigest() and applications['source_workbook_sha256']==original['workbook_sha256'], 'T05 second constructed applications resolve the unchanged as-of input/workbook versions')
    ib={x['input_id']:x for x in data[t05s_asof('04-table/financial-inputs.json')]['records']}
    cm=data['04-table/T05-research-cost-map.json'];roleids=cm['role_rate_input_ids'];day=ib[cm['day_normalisation_input_id']]['value'];n=ib[cm['contributor_scenarios_input_id']]['value']['base']
    rolehours={k:0 for k in roleids};jg=0
    for task in cm['tasks']:
        hours=ib[task['hours_input_id']]['value']['base']*(n if task['unit_basis']=='per_usable_contributor'else 1)
        if task['role_group']=='JGA':jg+=hours
        else:rolehours[task['role_group']]+=hours
    hourly={k:ib[v]['value']/(day if ib[v]['unit']=='day'else 1)for k,v in roleids.items()}
    def refvalue(div):
        return sum(rolehours[k]*ib[v]['value']/(div if ib[v]['unit']=='day'else 1)for k,v in roleids.items())
    basevalue=refvalue(day)
    require(applications['role_hours']==rolehours and all(abs(applications['role_hourly_reference'][k]-hourly[k])<0.000001 for k in hourly), 'T05 second arithmetic starts from the exact task/role basis')
    cases={x['test_id']:x for x in applications['cases']}
    require(len(cases)==len(applications['cases']) and {'SC01','SC02','SC03','SC04','SC05','SC06','SC07','SC08','SC09','SC10'}<=set(cases) and all(x['lens'] and x['meaning']for x in applications['cases']), 'T05 second constructed cases have unique IDs and explicit interpretation')
    c=cases['SC01']['result']
    require(c['provider_hours']==sum(rolehours.values()) and abs(c['provider_reference_value_GBP']-basevalue)<0.000001 and c['JGA_hours']==jg and c['combined_value']is None, 'T05 second baseline arithmetic reconciles without valuing missing JGA rates')
    for ident in ['SC02','SC03']:
        case=cases[ident]
        require(abs(case['result']['provider_reference_value_GBP']-refvalue(case['constructed_assumptions']['hours_per_day']))<0.000001, 'T05 second day-normalisation illustration reconciles: '+ident)
    whole=sum(math.ceil(rolehours[k]/day)*ib[v]['value']if ib[v]['unit']=='day'else rolehours[k]*ib[v]['value']for k,v in roleids.items())
    require(cases['SC04']['constructed_assumptions']=={'day_denominated_roles_booked_in_whole_days':True,'one_pool_per_role':True} and abs(cases['SC04']['result']['illustrative_value_GBP']-whole)<0.000001 and abs(cases['SC04']['result']['difference_from_hour_normalisation_GBP']-(whole-basevalue))<0.000001, 'T05 second booking illustration rounds role pools without altering adopted supplier terms')
    a=cases['SC05']['constructed_assumptions'];h=a['additional_unsuccessful_contact_events']*a['additional_coordination_hours_each'];r=cases['SC05']['result']
    require(abs(r['extra_hours']-h)<0.000001 and abs(r['extra_reference_value_GBP']-h*hourly['Coordination'])<0.000001 and abs(r['illustrative_provider_total_GBP']-(basevalue+h*hourly['Coordination']))<0.000001, 'T05 second unsuccessful-work illustration preserves the stated workload and rate units')
    a=cases['SC06']['constructed_assumptions'];delta=-a['writing_hours_removed_after_verified_reuse']*hourly['Writing']+a['additional_research_review_hours']*hourly['Research'];r=cases['SC06']['result']
    require(abs(r['net_reference_value_change_GBP']-delta)<0.000001 and abs(r['illustrative_provider_total_GBP']-(basevalue+delta))<0.000001, 'T05 second hypothetical reuse credit includes receiving review work')
    require(cases['SC07']['result']=={'JGA_hours':jg,'JGA_value':None,'combined_value':None} and cases['SC08']['result']=={'adopted_Indian_hourly_rate':None,'GBP_replacement_cost':None} and cases['SC09']['result']=={'adopted_automation_saving_percent':None,'hours_removed':0} and cases['SC10']['result']=={'converted_fee_GBP':None,'added_to_future_labour_value':False}, 'T05 second preserves unknown rates/geography/automation and the current-fee boundary')
    challenge=data.get('04-table/T05R-second-challenge-map.json')
    require(challenge is not None, 'T05 second integrated challenge map is retained')
    if challenge:
        require(challenge['status']=='second_challenge_reviewed_internal_design', 'T05 second integrated status denotes internal design review only')
        require([x['condition_id']for x in challenge['conditions']]==[f'RC{i:02}'for i in range(1,6)] and all(x['name'] and x['applies_when'] and x['check'] and x['model_implication']for x in challenge['conditions']), 'T05 second five selective conditions retain their meaning and use')
        require(challenge['first_component_map_path']=='04-table/T05-research-cost-map.json' and challenge['constructed_applications_path']=='04-table/research-notes/t05r-second-check/root/constructed-cost-applications.json' and challenge['prior_study_bridge_path']in data, 'T05 second challenge resolves first component applications and saved-study context')
        require(set(challenge['source_ids'])==set(t05rs_record_map['source_map'].values()) and set(challenge['claim_ids'])==set(t05rs_record_map['claim_map'].values()), 'T05 second integrated map reconciles evidence additions')
        for condition in challenge['conditions']:
            require(set(condition['source_ids'])<=source_ids and set(condition['claim_ids'])<=claim_ids and set(condition['related_workload_ids'])<=set(x['workload_id']for x in cm['tasks']), 'T05 second selective condition resolves evidence and actual workload IDs: '+condition['condition_id'])
        require(challenge['original_workbook_path']==original['workbook_path'] and challenge['original_workbook_sha256']==original['workbook_sha256'] and challenge['original_financial_inputs_sha256']==applications['source_financial_inputs_sha256'], 'T05 second map preserves exact reviewed workbook and financial-input versions')
        require(not challenge['financial_inputs_changed'] and not challenge['workbook_changed'] and challenge['new_financial_inputs']==0 and challenge['first_component_workload_tasks']==len(cm['tasks'])==21 and challenge['first_component_input_records']==len(ib)==33, 'T05 second conditions do not alter original task/input counts or adopt a new cost')
        require(challenge['fourteen_core_questions_unchanged'] and not challenge['current_contract_fee_changed'] and challenge['practitioner_free_full_research_preserved'] and not challenge['new_case_or_geography_quota'], 'T05 second leaves core questions current fee free research and participant scope intact')
        require(all(challenge[k]==[]for k in ['actual_quotes','actual_suppliers','actual_staffing','actual_participants','actual_buyer_member_validation','external_actions']) and not challenge['full_financial_model_complete'], 'T05 second map creates no actual contact procurement fieldwork or full-model completion')
        bridge=data[challenge['prior_study_bridge_path']]
        require([q['question_id']for q in bridge['questions']]==['S04-C','S07-C','S11-C'] and bridge['question_count']==len(bridge['questions']) and bridge['no_model_reruns'] and not bridge['recommendation_counts_reused'] and not bridge['generated_advice_fact_validated'] and not bridge['actual_buyer_evidence'], 'T05 second prior-study bridge uses explicit task contexts without new demand or factual validation')
        for q in bridge['questions']:
            require(hashlib.sha256(q['prompt'].encode()).hexdigest()==q['prompt_sha256'] and len(q['answer_links'])==8 and {(x['product'],x['repeat'])for x in q['answer_links']}=={(product,repeat)for product in ['ChatGPT','Gemini','Claude','Perplexity']for repeat in [1,2]}, 'T05 second exact prompt and four-tool/two-repeat linkage: '+q['question_id'])
        require(sum(len(q['answer_links'])for q in bridge['questions'])==bridge['linked_saved_records'] and sum(x['semantic_reread_for_this_lens']for q in bridge['questions']for x in q['answer_links'])==bridge['semantic_rereads'], 'T05 second saved-record linkage and semantic-reading counts are distinct')
        for x in bridge['provenance']:
            target=Path(x['path'])if Path(x['path']).is_absolute()else ROOT.parent.parent/x['path']
            require(hashlib.sha256(target.read_bytes()).hexdigest()==x['sha256'], 'T05 second saved-study provenance unchanged: '+x['role'])
        lineage=data['04-table/research-notes/t05r-second-check/competitors/prior-study-bridge-check.json']
        require(lineage['status']=='passed' and lineage['checks'] and all(x['passed']for x in lineage['checks']), 'T05 second exact saved-answer lineage checks passed within their declared scope')
    captures=data.get('08-qa/T05R-second-check-captures.json')
    require(captures is not None, 'T05 second original and reader capture inventory is retained')
    if captures:
        counts={kind:sum(x['kind']==kind for x in captures['records'])for kind in {x['kind']for x in captures['records']}}
        expected_kinds={'browser_reader_extract':3,'fresh_selected_paraphrased_reader_notes_not_raw_original':2,'parsed_original_text':8,'prior_selected_original_reader_notes_not_raw_original':1,'prior_selected_paraphrased_reader_notes_not_raw_original':1,'retained_original_html':7}
        require(counts==captures['counts_by_kind']==expected_kinds and len({x['path']for x in captures['records']})==len(captures['records'])==22, 'T05 second22 capture types and unique artifact paths reconcile')
        for x in captures['records']:
            require(hashlib.sha256((ROOT/x['path']).read_bytes()).hexdigest()==x['sha256'] and x['source_id']in source_ids, 'T05 second retained original or reader evidence resolves: '+x['path'])
            if x['kind']=='retained_original_html':
                require(Path(x['path']).suffix=='.html', 'T05 second original HTML classification matches retained file: '+x['path'])
            elif x['kind']=='browser_reader_extract':
                require(Path(x['path']).suffix=='.txt', 'T05 second browser reader extraction is not promoted to original HTML: '+x['path'])
        nr=[x for x in captures['records']if x['scope']=='new_route'];rr=[x for x in captures['records']if x['scope']=='reused_canonical_route']
        require(sum(x['kind']=='retained_original_html'for x in nr)==captures['new_route_primary_originals']==4 and sum(x['kind']=='retained_original_html'for x in rr)==captures['reused_route_fresh_primary_originals']==3 and sum(x['kind']=='browser_reader_extract'for x in nr)==captures['new_route_browser_reader_extracts']==3, 'T05 second fresh new-route and recaptured reuse originals remain separate from reader extracts')
        require(captures['new_source_routes']==t05rs_record_map['new_source_routes'] and captures['reused_canonical_routes']==12 and captures['new_JGA_empirical_datasets']==0 and captures['no_failed_HTTP_body_promoted_to_original'] and captures['no_bypass'], 'T05 second capture inventory preserves source-count and access boundaries')
        require(all(x.get('access_for_this_review')=='prior_context_reused'for x in captures['records']if x['source_id']=='SRC-0192'), 'T05 second Hays inherited capture kind is not presented as a fresh read')
        for folder in ['history-market','root']:
            candidates=data[f'04-table/research-notes/t05r-second-check/{folder}/source-candidates.json']['records']
            for candidate in candidates:
                sid=t05rs_record_map['source_map'][candidate['candidate_id']];source=current_by[sid]
                require(source['url']==candidate['url'], 'T05 second candidate URL and canonical route match: '+sid)
                if candidate['capture_kind']=='retained_original_html':
                    require(source['capture_path']==candidate['capture_path'] and source['capture_sha256']==candidate['capture_sha256'], 'T05 second new original retains canonical capture fields: '+sid)
                else:
                    require(source['capture_path']is None and source['capture_sha256']is None and any(x['path']==candidate['capture_path'] and x['sha256']==candidate['capture_sha256'] and x['kind']=='browser_reader_extract'for x in source['review_extracts']), 'T05 second reader-only source retains extract classification rather than original fields: '+sid)
    review=data.get('08-qa/t05r-second-review/integration-checks.json')
    require(review is not None, 'T05 second final independent integration checks are retained')
    require(review['status']=='passed_for_internal_T05R_second_challenge' and review['checks'] and all(x['passed']for x in review['checks']) and not review['open_substantive_issues'], 'T05 second final independent integration review passed without open substantive issues')
    require(review['external_actions']==[] and review['original_workbook_preserved'] and review['financial_inputs_unchanged'] and review['findings_preserved'], 'T05 second independent review confirms original artifacts and no external actions')
    require(not review['original_workbook_edit_needed'] and not review['actual_validation'] and not review['actual_fieldwork'] and not review['full_financial_model_complete'] and review['mutable_live_controls_and_validator_excluded_from_hashes'], 'T05 second independent review preserves internal design scope and excludes mutable control artifacts')
    require(review['canonical_source_records']==len(t05rs_sources) and review['canonical_claim_records']==len(t05rs_claims) and review['new_source_routes']==7 and review['new_bounded_claim_records']==18 and review['findings']==81 and review['financial_inputs']==len(ib) and review['protected_files_checked']==265 and review['pre_change_snapshots_checked']==13 and review['constructed_cases_checked']==len(cases) and review['saved_answer_lineage_checked']==bridge['linked_saved_records'], 'T05 second independent review counts reconcile to exact as-of integrated evidence preservation and constructed checks')
    require(review['fourteen_core_questions_unchanged'] and not review['current_contract_fee_changed'] and review['practitioner_free_full_research_preserved'], 'T05 second independent review confirms original questions fee and practitioner benefit')
    require(review['reviewed_artifacts'] and len({x['path']for x in review['reviewed_artifacts']})==len(review['reviewed_artifacts']), 'T05 second independent reviewed artifact manifest is nonempty and unique')
    for x in review['reviewed_artifacts']:
        target=Path(x['path'])if Path(x['path']).is_absolute()else ROOT/t05s_asof(x['path'])
        require(hashlib.sha256(target.read_bytes()).hexdigest()==x['sha256'], 'T05 second independent reviewed artifact hash preserved: '+x['path'])
    require((ROOT/'08-qa/t05r-second-review/INTEGRATED-REVIEW.md').is_file(), 'T05 second final independent review readout is retained')
    for rel in ['04-table/T05R-SECOND-CHECK-READOUT.md','04-table/T05R-COST-AND-DELIVERY-REFINEMENTS.md']:
        text=(ROOT/rel).read_text()
        require(set(re.findall(r'CLM-\d{4}',text))<=claim_ids and set(re.findall(r'SRC-\d{4}',text))<=source_ids, 'T05 second integrated source and claim references resolve: '+rel)
        for start,end in re.findall(r'CLM-(\d{4})\s*[–-]\s*CLM-(\d{4})',text):
            require({f'CLM-{n:04}'for n in range(int(start),int(end)+1)}<=claim_ids, 'T05 second integrated claim range resolves: '+rel)

if t05s_record_map:
    t05s_current_sources=data[t05ss_asof('02-evidence/registers/sources.json')]['records']
    t05s_current_claims=data[t05ss_asof('02-evidence/registers/claims.json')]['records']
    require(len(t05s_before)==13, 'T05 service-cost component retains thirteen exact prechange snapshots')
    for x in t05s_before.values():
        require(hashlib.sha256((ROOT/x['snapshot_path']).read_bytes()).hexdigest()==x['sha256'], 'T05 service component exact prechange artifact preserved: '+x['original_path'])
    oldsrc=data[t05s_before['02-evidence/registers/sources.json']['snapshot_path']]['records']
    oldclm=data[t05s_before['02-evidence/registers/claims.json']['snapshot_path']]['records']
    oldfin=data[t05s_before['04-table/financial-inputs.json']['snapshot_path']]['records']
    require(len(oldsrc)==242 and len(oldclm)==484 and len(oldfin)==33, 'T05 service component begins from the reviewed242source484claim33input checkpoint')
    require(t05s_record_map['new_source_routes']==len(t05s_record_map['source_map'])==5 and t05s_record_map['new_claim_records']==len(t05s_record_map['claim_map'])==11, 'T05 service component appends five source routes and eleven bounded claim records')
    require(len(t05s_current_sources)==len(oldsrc)+t05s_record_map['new_source_routes']==t05s_record_map['canonical_sources'] and len(t05s_current_claims)==len(oldclm)+t05s_record_map['new_claim_records']==t05s_record_map['canonical_claims'], 'T05 service component evidence totals reconcile to the exact prior checkpoint')
    require(t05s_current_claims[:len(oldclm)]==oldclm, 'T05 service component preserves all484 earlier claims exactly')
    current_by={x['source_id']:x for x in t05s_current_sources};claim_by={x['claim_id']:x for x in t05s_current_claims}
    for old in oldsrc:
        current=current_by[old['source_id']]
        require({k:v for k,v in old.items()if k not in ['additional_reviews','related_topic_ids']}=={k:v for k,v in current.items()if k not in ['additional_reviews','related_topic_ids']}, 'T05 service component preserves earlier source base: '+old['source_id'])
        require(all(v in current.get('additional_reviews',[])for v in old.get('additional_reviews',[])) and set(old.get('related_topic_ids',[]))<=set(current.get('related_topic_ids',[])), 'T05 service component retains earlier source reviews/topics: '+old['source_id'])
    for candidate,sid in t05s_record_map['source_map'].items():
        require(sid in source_ids and current_by[sid].get('t05s_source_candidate_id')==candidate and 'T05S'in current_by[sid]['related_topic_ids'], 'T05 service source origin and topic mapping resolves: '+sid)
    for candidate,cid in t05s_record_map['claim_map'].items():
        require(cid in claim_ids and claim_by[cid].get('t05s_claim_candidate_id')==candidate, 'T05 service claim origin mapping resolves: '+cid)
    candidate_sources=[]
    for folder in ['benchmarks','root']:
        candidates=data[f'04-table/research-notes/t05-service-costs/{folder}/source-candidates.json']['records'];candidate_sources+=candidates
        qa=data[f'04-table/research-notes/t05-service-costs/{folder}/verification.json']
        require(qa['checks'] and all(x['passed']for x in qa['checks']) and qa['external_actions']==[], 'T05 service source-pack bounded verification passed: '+folder)
        for candidate in candidates:
            sid=t05s_record_map['source_map'][candidate['candidate_id']];source=current_by[sid]
            require(candidate['http_status']==200 and candidate['capture_kind']=='retained_original_html' and Path(candidate['capture_path']).suffix=='.html', 'T05 service source has retained successful original HTML: '+sid)
            require(source['url']==candidate['url'] and source['capture_path']==candidate['capture_path'] and source['capture_sha256']==candidate['capture_sha256'], 'T05 service canonical route resolves exact candidate original: '+sid)
            for path_key,hash_key in [('capture_path','capture_sha256'),('parsed_path','parsed_sha256')]:
                require(hashlib.sha256((ROOT/candidate[path_key]).read_bytes()).hexdigest()==candidate[hash_key], 'T05 service original or parsed evidence hash preserved: '+candidate[path_key])
    require(len(candidate_sources)==5 and {x['candidate_id']for x in candidate_sources}==set(t05s_record_map['source_map']), 'T05 service evidence pack covers the five mapped routes exactly')
    qa=data['04-table/research-notes/t05-service-costs/benchmarks/verification.json']
    require(qa['new_monetary_benchmarks']==0 and qa['actual_quotes']==[] and qa['actual_customer_or_sales_records']==[], 'T05 service public service-unit evidence creates no monetary benchmark quote or customer record')
    require(data['05-analysis/findings.json']==data[t05s_before['05-analysis/findings.json']['snapshot_path']] and len(data['05-analysis/findings.json']['records'])==81, 'T05 service cost planning preserves all81 internal findings without invented observations')
    finance=data['04-table/financial-inputs.json'];inputs=finance['records']
    require(inputs[:len(oldfin)]==oldfin and len(inputs)==len(oldfin)+t05s_record_map['financial_inputs_added'], 'T05 service finance register preserves all33 research-component records as an exact prefix')
    require(len({x['input_id']for x in inputs})==len(inputs) and finance['actual_quotes']==[] and finance['actual_spend_records']==[] and not finance['full_model_complete'], 'T05 service input IDs remain unique with no actual quote spend or completed full model')
    for path,key in [('02-evidence/registers/searches.json','records'),('02-evidence/registers/source-aliases.json','url_aliases')]:
        old=data[t05s_before[path]['snapshot_path']].get(key,[])
        require(data[path].get(key,[])[:len(old)]==old, 'T05 service component preserves canonical history: '+path)
    require(len(data['08-qa/T05S-baseline-manifest.json']['files'])==333, 'T05 service component protects333 earlier artifacts')
    for x in data['08-qa/T05S-baseline-manifest.json']['files']:
        target=Path(x['path'])if Path(x['path']).is_absolute()else ROOT/t05ss_asof(x['path'])
        require(hashlib.sha256(target.read_bytes()).hexdigest()==x['sha256'], 'T05 service component protected earlier artifact retained: '+x['path'])
    completion=data['08-qa/T05R-second-check-completion.json']
    require(len(completion['artifacts'])==82 and completion['canonical_sources']==242 and completion['canonical_claims']==484 and completion['original_financial_component_inputs']==33 and completion['new_financial_inputs']==0, 'T05 research second completion retains its exact82artifact242source484claim33input scope')
    for x in completion['artifacts']:
        target=Path(x['path'])if Path(x['path']).is_absolute()else ROOT/t05s_asof(x['path'])
        require(hashlib.sha256(target.read_bytes()).hexdigest()==x['sha256'], 'T05 research second completion reconciles to exact pre-service artifact: '+x['path'])
    require(not t05s_record_map['commercial_validation'] and t05s_record_map['participant_observations']==0, 'T05 service component adds no commercial validation or participant observation')
    workload=data['04-table/research-notes/t05-service-costs/workload/workload-candidates.json']
    tasks=workload['tasks'];task_by={x['workload_id']:x for x in tasks};families={x['family_id']for x in workload['families']}
    quantities={x['unit_key']:x for x in workload['quantity_inventory']}
    require([x['workload_id']for x in tasks]==[f'WS{i:02}'for i in range(1,22)] and len(task_by)==workload['task_count']==21 and len(families)==workload['family_count']==9, 'T05 service workload retains21 distinct task units across nine families')
    require(len(quantities)==len(workload['quantity_inventory'])==workload['distinct_quantity_driver_count']==15 and {x['unit_key']for x in tasks}==set(quantities), 'T05 service workload fifteen quantity drivers resolve every task exactly')
    require(all(x['quantity']is None and x['status']=='not_selected_not_zero'for x in quantities.values()) and workload['selected_effort_case']is None, 'T05 service candidate quantities and selected effort remain blank rather than zero or a forecast')
    require(all(workload[k]==[]for k in ['actual_customers','actual_partner_orders','actual_proposals','actual_contacts','actual_briefings','actual_service_cases','actual_staffing','actual_timesheets','actual_conversion_rates','external_actions']), 'T05 service workload contains no actual customer sales delivery staffing or conversion record')
    require(workload['financial_register_rows_added']==0 and not workload['canonical_files_modified'] and not workload['first_workbook_modified'], 'T05 service workload subtask made no canonical financial or original-workbook edits')
    contract=workload['current_contract']
    require(contract['complete_report_preserved'] and contract['practitioner_free_full_research_preserved'] and contract['existing_USD_1500_fee_unchanged'] and contract['new_compulsory_scope']==[] and contract['actual_new_fees']==[] and contract['no_current_contract_surcharge'], 'T05 service candidate preserves the complete current contract and free practitioner benefit')
    work_ids={x['work_id']for x in data['04-table/T02-delivery-map.json']['items']};prior_tasks={x['workload_id']for x in data['04-table/T05-research-cost-map.json']['tasks']}
    for task in tasks:
        hours=task['planning_hours_per_unit']
        require(task['family_id']in families and task['unit_key']in quantities and set(task['T02_work_ids'])<=work_ids and set(task['existing_report_boundary_ids'])<=prior_tasks, 'T05 service candidate task resolves family unit work object and prior research boundary: '+task['workload_id'])
        require(set(hours)=={'low','working','high'} and all(isinstance(v,(int,float))and v>=0 for v in hours.values()) and hours['low']<=hours['working']<=hours['high'] and task['hours_evidence_status']=='untimed_analyst_effort_assumption_not_measured_or_empirically_validated', 'T05 service per-unit effort cases remain ordered analyst assumptions: '+task['workload_id'])
        require(all(task[k]is None for k in ['selected_scope','unit_quantity','selected_effort_case','selected_hours_per_unit','shared_work_adjustment','role_split','rate_and_cash_basis','actual_hours']) and not task['staff_assigned'] and not task['capacity_confirmed'], 'T05 service candidate leaves quantity rate scope reuse staffing and actual hours unselected: '+task['workload_id'])
    component=data['04-table/T05-service-cost-map.json'];input_by={x['input_id']:x for x in inputs};newinputs=inputs[len(oldfin):]
    require(component['financial_input_ids']==[f'FI-S{i:02}'for i in range(1,38)] and {x['input_id']for x in newinputs}==set(component['financial_input_ids']) and component['first_financial_records_preserved']==33 and component['new_financial_records']==t05s_record_map['financial_inputs_added']==37 and component['shared_financial_records']==len(inputs)==70, 'T05 service component maps all37 new inputs alongside33 preserved research inputs')
    require(component['reused_financial_input_ids']==['FI-R01','FI-R05','FI-R06'] and component['role_rate_input_ids']=={'Specialist':'FI-R01','Coordination':'FI-R05','Commercial':'FI-S01'} and component['day_normalisation_input_id']=='FI-R06', 'T05 service labour comparison reuses exact research rates and a separately unresolved commercial rate')
    require(component['workload_source_path']=='04-table/research-notes/t05-service-costs/workload/workload-candidates.json' and {x['workload_id']for x in component['tasks']}==set(task_by) and len(component['tasks'])==21, 'T05 service component maps every candidate task once')
    require(component['comparison_role_mapping_is_analyst_assumption'] and component['commercial_rate_is_unknown'] and component['all_programme_quantities_start_blank'] and component['no_volume_or_conversion_forecast'] and component['programme_totals_require_explicit_quantities'] and component['per_unit_values_must_not_be_summed_without_quantities'] and component['no_complete_cash_cost_claim'], 'T05 service comparison preserves role assumptions unknown rates and unavailable programme totals')
    require(component['effort_cases']==['low','working','high'] and component['default_effort_case']=='working', 'T05 service effort controls retain three cases and one working default')
    require(component['practitioner_free_full_research_preserved'] and component['bundled_fulfilment_counted_once'] and component['session_count_distinct_from_audience_entitlements'] and not component['current_contract_fee_changed'] and component['within_scope_corrections_not_extra_charged'] and component['fourteen_core_questions_unchanged'] and not component['first_research_workbook_changed'] and not component['full_financial_model_complete'], 'T05 service map retains contract free benefit bundle/session counting and original research workbook')
    require(all(component[k]==[]for k in ['actual_orders','actual_quotes','actual_staffing','actual_timesheets','actual_briefings','actual_customer_validation','external_actions']), 'T05 service map records no actual order hire delivery validation or external action')
    require(set(component['source_ids'])==set(t05s_record_map['source_map'].values())|{sid for ident in component['reused_financial_input_ids']for sid in input_by[ident]['source_ids']} and set(component['claim_ids'])==set(t05s_record_map['claim_map'].values()), 'T05 service integrated evidence map reconciles new context and reused rate provenance')
    for item in newinputs:
        require(item['component_id']==component['component_id'] and item['model_usage']=='future_service_sales_labour_comparison_only' and not item['actual_supplier_quote'] and not item['actual_cost'] and not item['budget_authorised'] and item['cash_classification']is None and item['basis'], 'T05 service input preserves bounded assumption use rather than authorised cash cost: '+item['input_id'])
        require(set(item['source_ids'])<=source_ids and set(item['claim_ids'])<=claim_ids, 'T05 service input source and claim lineage resolves: '+item['input_id'])
    commercial=input_by['FI-S01']
    require(commercial['value']is None and commercial['evidence_class']=='unresolved_commercial_resource_rate' and commercial['currency']=='GBP' and commercial['unit']=='GBP per hour' and commercial['source_ids']==[] and commercial['claim_ids']==[], 'T05 service commercial resource rate remains unknown without a substituted benchmark')
    for task in component['tasks']:
        candidate=task_by[task['workload_id']];hours=input_by[task['hours_input_id']]
        require(hours['value']==candidate['planning_hours_per_unit'] and hours['evidence_class']=='analyst_effort_assumption' and hours['workload_id']==task['workload_id'] and hours['unit_key']==task['unit_key']==candidate['unit_key'] and hours['unit']=='hours '+task['unit_basis'] and task['unit_basis']==candidate['unit_basis'] and hours['actual_hours']is None, 'T05 service adopted hours preserve the exact original per-unit planning basis: '+task['workload_id'])
        require(task['T02_work_ids']==candidate['T02_work_ids'] and task['existing_report_boundary_ids']==candidate['existing_report_boundary_ids'] and task['overlap_rule']==candidate['boundary_and_exclusions'] and task['rate_input_id']==component['role_rate_input_ids'][task['comparison_role']], 'T05 service task preserves work-object overlap and selected comparison role mapping: '+task['workload_id'])
    units={x['unit_key']:x for x in component['units']}
    require(len(units)==len(component['units'])==15 and set(units)==set(quantities), 'T05 service integrated unit catalogue retains all fifteen distinct quantity drivers')
    for key,unit in units.items():
        quantity=input_by[unit['quantity_input_id']]
        require(quantity['value']is None and quantity['unit_key']==key and quantity['evidence_class']=='unresolved_activity_quantity' and quantity['currency']is None and unit['quantity']is None and unit['counting_note'], 'T05 service programme quantity remains explicitly unresolved: '+key)
        require(set(unit['task_ids'])=={x['workload_id']for x in component['tasks']if x['unit_key']==key}, 'T05 service unit aggregates its own task units once: '+key)
    require({x['hours_input_id']for x in component['tasks']}|{x['quantity_input_id']for x in component['units']}|{'FI-S01'}==set(component['financial_input_ids']), 'T05 service hours quantity and unresolved rate records exhaust the37 new inputs exactly')
    require(component['workbook_created'] and component['workbook_qa_path']=='08-qa/t05s-workbook/verification.json' and component['workbook_cell_map_path']=='08-qa/t05s-workbook/cell-map.json' and component['workbook_export_check_path']=='08-qa/t05s-workbook/export-check.json' and component['independent_review_path']=='08-qa/t05s-review/integration-checks.json', 'T05 service component resolves its complete workbook QA and independent-review paths')
    qa=data[component['workbook_qa_path']];cellmap=data[component['workbook_cell_map_path']];exported=data[component['workbook_export_check_path']]
    output=Path(component['workbook_absolute_path'])
    require(output.is_absolute() and output.is_file() and output.suffix.lower()=='.xlsx' and output==Path(qa['workbook_path'])==Path(cellmap['workbook_path'])==Path(exported['workbook_path']) and hashlib.sha256(output.read_bytes()).hexdigest()==component['workbook_sha256']==qa['workbook_sha256']==exported['workbook_sha256'], 'T05 service workbook and all QA records identify exact exported bytes')
    require(qa['status']=='passed_calculation_and_visual_review' and qa['authoring_engine']=='@oai/artifact-tool' and not qa['native_Excel_application_tested'] and qa['visual_review_complete'] and qa['all_temporary_input_changes_restored'], 'T05 service artifact-engine calculation and visual checks passed without a native Excel claim')
    require(qa['final_saved_effort_case']=='working' and qa['all_activity_quantities_blank'] and qa['commercial_rate_blank'] and qa['final_programme_hours']==qa['final_programme_labour_GBP']=='n.a.', 'T05 service delivered defaults retain blank quantities and unavailable programme hours and value')
    cases={x['test_id']:x for x in qa['tests']}
    required_cases={'DEFAULT-QUANTITIES-BLANK','EXPLICIT-ZERO-ACTIVITY','TWO-BRIEFINGS','UNKNOWN-COMMERCIAL-RATE','ENTERED-COMMERCIAL-RATE','EXPLICIT-ZERO-RATE','BLANK-IS-NOT-ZERO','MISSING-UNSELECTED-EFFORT','MISSING-SELECTED-EFFORT','ZERO-INCREMENTAL-PREP','INVALID-ACTIVITY--1','INVALID-ACTIVITY-0.5','MISSING-SPECIALIST-RATE','INVALID-DAY-NOT-APPLICABLE-TO-ADMIN','JOINT-SESSION-COUNTED-ONCE','DISTINCT-SECOND-SESSION','INVALID-EFFORT-CASE','PASTED-TEXT-EFFORT-CASE','RESTORED-DELIVERY-DEFAULTS'}
    require(len(cases)==len(qa['tests'])==component['workbook_calculation_tests']==64 and required_cases<=set(cases) and all(x['passed']for x in qa['tests']), 'T05 service workbook checks cover active cases edits blanks valid zeros missing selected inputs invalid activities joint sessions pasted-text selectors and restoration')
    divisor=input_by[component['day_normalisation_input_id']]['value'];expected={}
    for effort in component['effort_cases']:
        expected[effort]={}
        require(set(qa['expected_per_unit'][effort])==set(units), 'T05 service QA expected unit set is complete: '+effort)
        for key,unit in units.items():
            selected=[x for x in component['tasks']if x['workload_id']in unit['task_ids']]
            hours=sum(input_by[t['hours_input_id']]['value'][effort]for t in selected);ref=0;missing=False
            for task in selected:
                rate=input_by[task['rate_input_id']];h=input_by[task['hours_input_id']]['value'][effort]
                if rate['value']is None: missing=missing or h!=0
                else: ref+=h*rate['value']/(divisor if rate['unit']=='day'else 1)
            e={'hours':hours,'reference':ref,'commercial':'n.a.'if missing else 0,'combined':'n.a.'if missing else ref};expected[effort][key]=e
            recorded=qa['expected_per_unit'][effort][key]
            require(set(recorded)==set(e) and all(recorded[k]==v if isinstance(v,str)else isinstance(recorded[k],(int,float))and abs(recorded[k]-v)<0.000001 for k,v in e.items()), 'T05 service independently computed per-unit case reconciles to QA: '+effort+' '+key)
            actual=cases['CASE-'+effort+'-'+key]['detail']['actual'];values=[e['hours'],e['reference'],e['combined']]
            require(len(actual)==3 and all(a==v if isinstance(v,str)else isinstance(a,(int,float))and abs(a-v)<0.000001 for a,v in zip(actual,values)), 'T05 service recalculated unit outputs reconcile to the exact task and rate arithmetic: '+effort+' '+key)
    require(expected['working']['briefing_session_count']=={'hours':5,'reference':248,'commercial':0,'combined':248} and abs(expected['working']['partner_bundle_count']['hours']-2.25)<0.000001 and abs(expected['working']['partner_bundle_count']['combined']-103.9275)<0.000001, 'T05 service working briefing and partner administration examples retain their distinct limited scope')
    require(cases['TWO-BRIEFINGS']['detail']==[10,496] and cases['EXPLICIT-ZERO-ACTIVITY']['detail']==[0,0] and cases['UNKNOWN-COMMERCIAL-RATE']['detail']==[3,'n.a.'] and cases['MISSING-SELECTED-EFFORT']['detail']=='n.a.' and cases['MISSING-UNSELECTED-EFFORT']['detail']==248, 'T05 service tests preserve quantity scaling and selected versus unselected missing-input behaviour')
    require(cases['ENTERED-COMMERCIAL-RATE']['detail']==120 and cases['EXPLICIT-ZERO-RATE']['detail']==0 and cases['BLANK-IS-NOT-ZERO']['detail']==['n.a.','n.a.'] and cases['ZERO-INCREMENTAL-PREP']['detail']==[2,99.2], 'T05 service tests distinguish valid rate/hour zeros from blank unknowns')
    require(cases['JOINT-SESSION-COUNTED-ONCE']['detail']==[9.5,455.855] and cases['DISTINCT-SECOND-SESSION']['detail']==[14.5,703.855] and cases['INVALID-EFFORT-CASE']['detail']==['n.a.','n.a.'], 'T05 service tests count shared and distinct sessions without conflating audience entitlements')
    require(cases['PASTED-TEXT-EFFORT-CASE']['detail']==['n.a.','n.a.','n.a.'], 'T05 service pasted-text case selector returns unavailable label hours and value without an Excel error')
    require(cases['DEFAULT-QUANTITIES-BLANK']['detail']==['n.a.','n.a.',15] and cases['INVALID-ACTIVITY--1']['detail']==cases['INVALID-ACTIVITY-0.5']['detail']==['n.a.','n.a.'] and cases['MISSING-SPECIALIST-RATE']['detail']=='n.a.' and cases['INVALID-DAY-NOT-APPLICABLE-TO-ADMIN']['detail']==input_by['FI-R05']['value'] and cases['RESTORED-DELIVERY-DEFAULTS']['detail']=={'programme_hours':'n.a.','programme_value':'n.a.','blank_quantities':15}, 'T05 service boundary tests preserve unavailable invalid inputs independent hourly rates and final blank defaults')
    require(cellmap['sheets']==['Service cost','Inputs'] and cellmap['case_selector']=='Inputs!D4' and cellmap['case_label']=='Inputs!F4' and cellmap['day_normalisation']=='Inputs!F8' and cellmap['rate_rows']=={'Specialist':12,'Coordination':13,'Commercial':14} and cellmap['rate_input_column']=='E' and cellmap['normalised_rate_column']=='F', 'T05 service workbook has one case selector and distinct rate inputs with a shared normalisation basis')
    require(cellmap['task_input_rows']=={f'WS{i:02}':37+i for i in range(1,22)} and cellmap['task_build_rows']=={f'WS{i:02}':32+i for i in range(1,22)} and cellmap['task_active_column']=='F' and cellmap['task_case_columns']=={'low':'G','working':'H','high':'I'}, 'T05 service workbook maps every task active assumption and case inputs to its single build')
    require(set(cellmap['quantity_input_rows'])==set(cellmap['unit_output_rows'])==set(units) and list(cellmap['quantity_input_rows'].values())==list(range(19,34)) and cellmap['quantity_input_column']=='D' and cellmap['programme_hours']=='Service cost!E6' and cellmap['programme_labour_GBP']=='Service cost!E7', 'T05 service quantity and programme output locations are distinct and complete')
    require(len(qa['renders'])==qa['visual_regions_reviewed']==component['workbook_visual_regions']==6 and {(x['path'],x['sheet'],x['range'])for x in qa['renders']}=={(x['path'],x['sheet'],x['range'])for x in cellmap['renders']} and {x['sheet']for x in qa['renders']}==set(cellmap['sheets']), 'T05 service visual review covers exact six final ranges across both worksheets')
    for render in qa['renders']:
        require(hashlib.sha256(Path(render['path']).read_bytes()).hexdigest()==render['sha256'], 'T05 service final visual evidence hash preserved: '+render['range'])
    scan=Path(qa['formula_error_scan_path'])
    require(scan.is_file() and all(x.get('kind')=='notice' and '0 entries'in x.get('message','')for x in [json.loads(v)for v in scan.read_text().splitlines()if v.strip()]), 'T05 service final formula-error scan records no matches')
    require(exported['status']=='passed' and len(exported['checks'])==12 and all(x['passed']for x in exported['checks']) and not exported['native_Excel_application_tested'], 'T05 service saved export checks passed within the stated OpenXML scope')
    with zipfile.ZipFile(output)as archive:
        ns={'s':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
        require([x.attrib['name']for x in ET.fromstring(archive.read('xl/workbook.xml')).findall('s:sheets/s:sheet',ns)]==cellmap['sheets'] and not any(x.startswith('xl/externalLinks/')for x in archive.namelist()), 'T05 service saved workbook retains two named sheets without an external workbook dependency')
        sheets={name:{x.attrib['r']:x for x in ET.fromstring(archive.read(f'xl/worksheets/sheet{i}.xml')).findall('.//s:c',ns)}for i,name in enumerate(cellmap['sheets'],1)}
        require(not any(cell.attrib.get('t')=='e'for cells in sheets.values()for cell in cells.values()), 'T05 service saved workbook contains no cached Excel error cell')
        def saved_value(sheet,address):
            cell=sheets[sheet].get(address)
            if cell is None:return None
            value=cell.find('s:v',ns)
            if value is None:return None
            return float(value.text)if cell.attrib.get('t')in [None,'n']else value.text
        def saved_formula(sheet,address):
            cell=sheets[sheet].get(address)
            return cell.find('s:f',ns).text if cell is not None and cell.find('s:f',ns)is not None else None
        require(saved_value('Inputs','D4')==2 and saved_value('Inputs','F4')=='Working' and saved_value('Inputs','F8')==divisor and saved_value('Inputs','E14')is None and saved_value('Inputs','F14')=='n.a.', 'T05 service exported workbook restores the working case divisor and unresolved commercial rate')
        require(saved_formula('Inputs','F4').startswith('IF(ISNUMBER(D4),IF('), 'T05 service saved selector guards text before applying numeric range and integer checks')
        require(all(saved_value('Inputs','D'+str(row))is None for row in cellmap['quantity_input_rows'].values()) and all(saved_value('Service cost',address)=='n.a.'and saved_formula('Service cost',address)for address in ['E6','E7','H26','I26']), 'T05 service exported programme quantities remain blank and summary results unavailable formulas')
        for role,ident in component['role_rate_input_ids'].items():
            row=cellmap['rate_rows'][role];rate=input_by[ident]
            require(saved_value('Inputs','E'+str(row))==rate['value'] and saved_value('Inputs','F'+str(row))==('n.a.'if rate['value']is None else rate['value']/(divisor if rate['unit']=='day'else 1)), 'T05 service exported rate input and active normalisation match canonical meaning: '+role)
        for task in component['tasks']:
            ident=task['workload_id'];row=cellmap['task_input_rows'][ident];build=cellmap['task_build_rows'][ident];values=input_by[task['hours_input_id']]['value']
            require(all(saved_value('Inputs',column+str(row))==values[effort]for effort,column in cellmap['task_case_columns'].items()) and saved_value('Inputs','F'+str(row))==values['working'] and saved_formula('Inputs','F'+str(row)), 'T05 service exported task cases and active values preserve source assumptions: '+ident)
            require(saved_formula('Service cost','E'+str(build))=="'Inputs'!F"+str(row) and saved_formula('Service cost','F'+str(build))=="'Inputs'!F"+str(cellmap['rate_rows'][task['comparison_role']]), 'T05 service exported build links active task hours and corresponding active rate: '+ident)
        for key,row in cellmap['unit_output_rows'].items():
            e=expected['working'][key]
            require(all(saved_value('Service cost',column+str(row))==v if isinstance(v,str)else abs(saved_value('Service cost',column+str(row))-v)<0.000001 for column,v in [('C',e['hours']),('D',e['reference']),('E',e['commercial']),('F',e['combined'])]), 'T05 service exported working unit values match independent arithmetic: '+key)
        validations=ET.fromstring(archive.read('xl/worksheets/sheet2.xml')).findall('s:dataValidations/s:dataValidation',ns)
        require(any('D4'in x.attrib.get('sqref','')for x in validations) and any('D19:D33'in x.attrib.get('sqref','')for x in validations), 'T05 service saved case and activity input validations are retained')
    review=data.get(component['independent_review_path'])
    require(review is not None, 'T05 service final independent integration review is retained')
    require(review['status']=='passed_for_internal_T05S_component' and review['checks'] and all(x['passed']for x in review['checks']) and review['open_substantive_issues']==[], 'T05 service independent component review passed without open substantive issues')
    require(component['status']=='reviewed_service_sales_component_full_model_pending' and component['component_review_complete'] and not component['full_financial_model_complete'], 'T05 service reviewed component does not complete the full programme model')
    require(review['workbook_audited'] and review['workbook_sha256']==component['workbook_sha256'] and not review['full_financial_model_audited'] and not review['native_Excel_application_tested'], 'T05 service independent workbook audit retains exact bytes and bounded engine scope')
    require(all(review[k]==[]for k in ['actual_orders','actual_quotes','actual_staffing','actual_timesheets','actual_briefings','actual_customer_validation','actual_spend_records','external_actions']), 'T05 service independent review confirms no actual sale quote hire delivery validation or spend')
    arithmetic=review['independent_scenario_arithmetic']
    require(len(arithmetic)==review['independent_per_unit_case_results']==45 and {(x['case'],x['unit_key'])for x in arithmetic}=={(effort,key)for effort in component['effort_cases']for key in units} and all(x['passed']for x in arithmetic), 'T05 service independent review covers all45 unique unit and effort combinations')
    for item in arithmetic:
        e=expected[item['case']][item['unit_key']];values=[e[k]for k in ['hours','reference','commercial','combined']]
        for field in ['actual_hours_reference_commercial_combined','independent_expected']:
            require(len(item[field])==4 and all(a==v if isinstance(v,str)else isinstance(a,(int,float))and abs(a-v)<0.000001 for a,v in zip(item[field],values)), 'T05 service independent scenario result reconciles to canonical task arithmetic: '+item['case']+' '+item['unit_key']+' '+field)
    require(review['visual_regions_independently_viewed']==6, 'T05 service independent visual review covers all six final regions')
    require(review['reviewed_artifacts'] and len({x['path']for x in review['reviewed_artifacts']})==len(review['reviewed_artifacts']), 'T05 service independent reviewed artifact manifest is nonempty and unique')
    for x in review['reviewed_artifacts']:
        target=Path(x['path'])if Path(x['path']).is_absolute()else ROOT/t05ss_asof(x['path'])
        require(hashlib.sha256(target.read_bytes()).hexdigest()==x['sha256'], 'T05 service independent reviewed artifact bytes preserved: '+x['path'])
    text=(ROOT/'04-table/T05-SERVICE-AND-SALES-COSTS.md').read_text()
    require(set(re.findall(r'CLM-\d{4}',text))<=claim_ids and set(re.findall(r'SRC-\d{4}',text))<=source_ids, 'T05 service integrated readout source and claim references resolve')





if t05ss_record_map:
    require(len(t05ss_before)==13, 'T05 service second challenge retains thirteen exact prechange snapshots')
    for x in t05ss_before.values():
        require(hashlib.sha256((ROOT/x['snapshot_path']).read_bytes()).hexdigest()==x['sha256'], 'T05 service second exact snapshot: '+x['original_path'])
    oldsrc=data[t05ss_before['02-evidence/registers/sources.json']['snapshot_path']]['records']
    oldclm=data[t05ss_before['02-evidence/registers/claims.json']['snapshot_path']]['records']
    require(len(oldsrc)==247 and len(oldclm)==495 and len(sources)==249 and len(claims)==508, 'T05 service second exact prior/current evidence counts')
    require(t05ss_record_map['new_source_routes']==2 and t05ss_record_map['new_claim_records']==len(t05ss_record_map['claim_map'])==13 and t05ss_record_map['financial_inputs_added']==0, 'T05 service second appends two routes/thirteen bounded records and no financial input')
    require(claims[:495]==oldclm, 'T05 service second preserves all495 earlier claims exactly')
    bysource={x['source_id']:x for x in sources}
    for old in oldsrc:
        new=bysource[old['source_id']]
        require({k:v for k,v in old.items()if k not in ['additional_reviews','related_topic_ids']}=={k:v for k,v in new.items()if k not in ['additional_reviews','related_topic_ids']}, 'T05 service second prior source substance: '+old['source_id'])
        require(new.get('additional_reviews',[])[:len(old.get('additional_reviews',[]))]==old.get('additional_reviews',[]) and set(old.get('related_topic_ids',[]))<=set(new.get('related_topic_ids',[])), 'T05 service second source review history: '+old['source_id'])
    require(data['04-table/financial-inputs.json']==data[t05ss_before['04-table/financial-inputs.json']['snapshot_path']] and len(data['04-table/financial-inputs.json']['records'])==70, 'T05 service second preserves all70 financial inputs unchanged')
    require(data['05-analysis/findings.json']==data[t05ss_before['05-analysis/findings.json']['snapshot_path']], 'T05 service second creates no empirical finding')
    require(len(data['08-qa/T05S-second-check-baseline.json']['files'])==401, 'T05 service second protects401 prior artifacts')
    for x in data['08-qa/T05S-second-check-baseline.json']['files']:
        target=Path(x['path'])if Path(x['path']).is_absolute()else ROOT/x['path']
        require(hashlib.sha256(target.read_bytes()).hexdigest()==x['sha256'], 'T05 service second protected artifact: '+x['path'])
    completed=data['08-qa/T05S-completion-check.json']
    require(completed['canonical_sources']==247 and completed['canonical_claims']==495 and completed['shared_financial_inputs']==70 and len(completed['artifacts'])==79, 'T05 service first completion retains exact historical scope')
    for x in completed['artifacts']:
        target=Path(x['path'])if Path(x['path']).is_absolute()else ROOT/t05ss_asof(x['path'])
        require(hashlib.sha256(target.read_bytes()).hexdigest()==x['sha256'], 'T05 service first completion as-of artifact: '+x['path'])
    capture=data['08-qa/T05S-second-check-captures.json']
    require(len(capture['records'])==16 and capture['counts_by_kind']=={'browser_reader_paraphrase_not_original':3,'parsed_original_text':6,'prior_selected_paraphrased_reader_notes_not_raw_original':1,'retained_original_html':6}, 'T05 service second originals/readers/prior-context classifications reconcile')
    for x in capture['records']:
        require(x['source_id']in source_ids and hashlib.sha256((ROOT/x['path']).read_bytes()).hexdigest()==x['sha256'], 'T05 service second retained capture: '+x['path'])
    require(bysource[t05ss_record_map['source_map']['SS2-S02']]['capture_path']is None and bysource[t05ss_record_map['source_map']['SS2-S01']]['capture_path'].endswith('.html') and sum(bool(x['capture_path'])for x in sources)==173, 'T05 service second reader note not promoted to a primary original')
    component=data['04-table/T05S-second-challenge-map.json']
    require(component['status']=='second_challenge_reviewed_required_programme_refinements_recorded' and len(component['conditions'])==6 and component['programme_noncompletion_and_exception_work_still_required'], 'T05 service second records six required programme refinements without claiming implementation complete')
    require(not component['workbook_changed'] and not component['financial_inputs_changed'] and not component['independent_agent_review'] and not component['full_financial_model_complete'] and component['fourteen_core_questions_unchanged'] and component['practitioner_free_full_research_preserved'] and not component['current_contract_fee_changed'], 'T05 service second preserves scope inputs and same-agent review limits')
    tasks={x['workload_id']for x in data['04-table/T05-service-cost-map.json']['tasks']}
    for condition in component['conditions']:
        require(set(condition['workload_ids'])<=tasks and set(condition['claim_ids'])<=claim_ids, 'T05 service second condition lineage: '+condition['condition_id'])
    application=data[component['cost_applications_path']]
    require(application['case_count']==len(application['cases'])==12 and application['check_count']==len(application['checks'])==22 and all(x['passed']for x in application['checks']), 'T05 service second twelve constructed applications pass22 scoped checks')
    require(application['source_workbook_sha256']==component['first_component_workbook_sha256']==hashlib.sha256(Path(component['first_component_workbook_path']).read_bytes()).hexdigest() and application['source_financial_inputs_sha256']==hashlib.sha256((ROOT/'04-table/financial-inputs.json').read_bytes()).hexdigest(), 'T05 service second constructed applications retain exact workbook/input provenance')
    cancellation=next(x for x in application['cases']if x['case_id']=='SA05')
    require(cancellation['result']['catalogue_delivered_unit_hours']==0 and cancellation['result']['additional_noncompletion_work_hours']==3 and application['programme_noncompletion_state_work_still_required'], 'T05 service second zero-completion work gap remains visible')
    bridge=data[component['prior_study_bridge_path']]
    require(len(bridge['questions'])==4 and bridge['linked_saved_answers']==32 and bridge['semantic_rereads']==4 and bridge['model_reruns']==0, 'T05 service second exact prior-study scope')
    for x in bridge['provenance']:
        require(hashlib.sha256((ROOT.parent.parent/x['path']).read_bytes()).hexdigest()==x['sha256'], 'T05 service second original study provenance: '+x['role'])
    qa=data['04-table/research-notes/t05s-second-check/prior-study/bridge-checks.json']
    require(qa['check_count']==len(qa['checks'])==136 and all(x['passed']for x in qa['checks']), 'T05 service second136 exact text/hash/metadata checks passed')
    review=data[component['review_checks_path']]
    require(review['status']=='passed_same_agent_second_check' and review['check_count']==len(review['checks']) and review['checks'] and all(x['passed']for x in review['checks']) and not review['independent_agent_review'] and review['required_programme_refinements_recorded'] and not review['programme_model_complete'], 'T05 service second same-agent review passed with required implementation work explicit')
    for x in review['reviewed_artifacts']:
        target=Path(x['path'])if Path(x['path']).is_absolute()else ROOT/x['path']
        require(hashlib.sha256(target.read_bytes()).hexdigest()==x['sha256'], 'T05 service second reviewed artifact bytes: '+x['path'])

questions=data['01-method/question-map.json']
require(questions['status']=='draft_for_user_review' and not questions['client_approved'] and not questions['participant_tested'], 'Question draft not misreported as approved or participant tested')
require([q['question_id'] for q in questions['records']]==[f'Q{i:03}' for i in range(1,15)], 'Fourteen ordered core questions present')
require([q['number'] for q in questions['records'] if q['route']=='recent_case']==list(range(7,14)), 'Recent case routing matches questions seven to thirteen')
require(all(q['purpose'] and q['topic_ids'] and q['wording'] for q in questions['records']), 'Every question has wording purpose and module mapping')
require(questions['version']=='0.2' and questions==data['01-method/question-map-v0.2.json'], 'Canonical map matches version zero two snapshot')
require([q['wording'] for q in questions['records']]==[q['wording'] for q in data['01-method/question-map-v0.1.json']['records']], 'Core wording preserved across checkpoint versions')
require(data['08-qa/WP02-v0.2-routing-walkthrough.json']['status']=='passed' and data['08-qa/WP02-v0.2-routing-walkthrough.json']['test_count']==19, 'Version zero two routing has nineteen passed synthetic cases')
for path in ['05-analysis/observations.json', '05-analysis/charts.json']:
    require(data[path]['records'] == [], f'Unperformed research stays empty in {path}')
require(data[t05r_asof('04-table/financial-inputs.json')]['records']==[], 'Pre-T05 financial input register remains empty in its preserved checkpoint')

link_count = 0
for file in ROOT.rglob('*.md'):
    for target in re.findall(r'\]\(([^)]+)\)', file.read_text()):
        if target.startswith(('https://', 'http://', '#')):
            continue
        target = unquote(target.split('#', 1)[0])
        if target:
            require((file.parent / target).resolve().exists(), f'Local link resolves in {file.relative_to(ROOT)}')
            link_count += 1

result = {'status': 'passed', 'date': data['00-control/work-packages.json']['updated_on'], 'checks': len(checks), 'json_files': len(data), 'source_records': len(sources), 'claim_records': len(claims), 'question_records':len(questions['records']), 'internal_design_findings':len(data['05-analysis/findings.json']['records']), 'deliverable_records': len(deliverables), 'work_packages': len(packages), 'local_markdown_links_checked': link_count, 'scope': ('T05 service/sales second challenge with required incurred-work/remaining-obligation programme refinements and original catalogue preserved; 'if t05ss_record_map else '')+('T05 per-unit service/sales labour catalogue with blank programme quantities and commercial rate, full event/revenue/cash model pending; 'if t05s_record_map else '')+('T05 research/staffing second challenge across historical/market/competitor/task/delivery perspectives with original component preserved; ' if t05rs_record_map else '')+('T05 research/staffing cost component with full event/revenue/cash model pending; ' if t05r_record_map else '')+'T04 commercial route, model-unit/input/formula design and public venue-cost evidence with actual financial model and validation pending; T02 second challenge evidence/use/time/work/fulfilment/concept-state conditions; T02 three concrete internal propositions, use/rights/delivery and inactive draft guide; T01 second challenge historical/market/comparator/prior-study/participation lenses and selective conditions; T01 six distinct public comparable mechanisms and T02 untested propositions; WP03 prepared inactive collection pack; R01–R07 evidence/capture and synthesis consistency; R08 preparatory linked views, report integration, first-pass and version0.2 fifteen constructed applications, second-challenge evidence/time/object conditions, held claims and original-input dependency; prior/client/core/canonical preservation, WP02 question mapping and blank unperformed research. No final publication, participant testing, commercial validation, product trial, employer forecast or human fieldwork implied.'}
print(json.dumps(result, indent=2))
