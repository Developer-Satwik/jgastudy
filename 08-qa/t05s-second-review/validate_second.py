"""Same-agent second-check integrity and scope checks, with no workbook edits."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
checks = []

def read(path):
    return json.loads((ROOT / path).read_text())

def require(value, detail):
    assert value, detail
    checks.append({'passed': bool(value), 'detail': detail})

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

baseline = read('08-qa/T05S-second-check-baseline.json')
before = read('04-table/research-notes/t05s-second-check/before-review/manifest.json')
snapshots = {x['original_path']: x['snapshot_path'] for x in before['records']}
require(len(baseline['files']) == 401 and len(before['records']) == 13, 'Exactly401 protected files and13 snapshots')
for x in baseline['files']:
    path = Path(x['path'])
    path = path if path.is_absolute() else ROOT / path
    require(digest(path) == x['sha256'], 'Protected bytes: ' + x['path'])
for x in before['records']:
    require(digest(ROOT / x['snapshot_path']) == x['sha256'], 'Snapshot bytes: ' + x['original_path'])

sources = read('02-evidence/registers/sources.json')['records']
claims = read('02-evidence/registers/claims.json')['records']
old_sources = read(snapshots['02-evidence/registers/sources.json'])['records']
old_claims = read(snapshots['02-evidence/registers/claims.json'])['records']
mapping = read('08-qa/T05S-second-check-record-map.json')
require(len(old_sources) == 247 and len(old_claims) == 495, 'Exact prior evidence counts')
require(len(sources) == 249 and len(claims) == 508 and mapping['new_source_routes'] == 2 and mapping['new_claim_records'] == 13, 'Exact two-route/thirteen-record append')
require(claims[:495] == old_claims, 'All495 earlier claims preserved exactly')
by_source = {x['source_id']: x for x in sources}
for old in old_sources:
    new = by_source[old['source_id']]
    require({k:v for k,v in old.items() if k not in ['additional_reviews', 'related_topic_ids']} == {k:v for k,v in new.items() if k not in ['additional_reviews', 'related_topic_ids']}, 'Prior source substantive record: ' + old['source_id'])
    require(new.get('additional_reviews', [])[:len(old.get('additional_reviews', []))] == old.get('additional_reviews', []) and set(old.get('related_topic_ids', [])) <= set(new.get('related_topic_ids', [])), 'Prior source review/topic history: ' + old['source_id'])
require(sum(bool(x['capture_path']) for x in sources) == 173, 'Primary-original source count173')
require(read('04-table/financial-inputs.json') == read(snapshots['04-table/financial-inputs.json']) and len(read('04-table/financial-inputs.json')['records']) == 70, 'All70 financial records and classifications unchanged')
require(read('05-analysis/findings.json') == read(snapshots['05-analysis/findings.json']), 'All81 findings unchanged')
for path, key in [('02-evidence/registers/searches.json','records'), ('02-evidence/registers/source-aliases.json','url_aliases'), ('00-control/changes.json','records'), ('00-control/decisions.json','records')]:
    old = read(snapshots[path]).get(key, [])
    require(read(path).get(key, [])[:len(old)] == old, 'Append-only history: ' + path)

capture = read('08-qa/T05S-second-check-captures.json')
require(len(capture['records']) == 16 and capture['counts_by_kind'] == {'browser_reader_paraphrase_not_original':3, 'parsed_original_text':6, 'prior_selected_paraphrased_reader_notes_not_raw_original':1, 'retained_original_html':6}, 'Originals, readers and prior notes distinguished')
for x in capture['records']:
    require(digest(ROOT / x['path']) == x['sha256'] and x['source_id'] in by_source, 'Captured evidence: ' + x['path'])
require(by_source[mapping['source_map']['SS2-S02']]['capture_path'] is None and by_source[mapping['source_map']['SS2-S01']]['capture_path'].endswith('.html'), 'SEC reader note is not a raw original; timeline retains original HTML')
source_qa = read('04-table/research-notes/t05s-second-check/evidence/verification.json')
require(all(x['passed'] for x in source_qa['checks']) and len(source_qa['checks']) == 32 and source_qa['external_actions'] == [], 'Bounded source/capture checks passed')

component = read('04-table/T05S-second-challenge-map.json')
tasks = {x['workload_id'] for x in read(component['first_component_map_path'])['tasks']}
claim_ids = {x['claim_id'] for x in claims}
require(len(component['conditions']) == 6 and len({x['condition_id'] for x in component['conditions']}) == 6, 'Six distinct programme conditions')
for x in component['conditions']:
    require(set(x['workload_ids']) <= tasks and set(x['claim_ids']) <= claim_ids and x['programme_implication'], 'Condition task/evidence mapping: ' + x['condition_id'])
require(component['status'] == 'second_challenge_reviewed_required_programme_refinements_recorded' and component['programme_noncompletion_and_exception_work_still_required'], 'Required programme work is explicit, not falsely completed')
require(not any(component[k] for k in ['workbook_changed', 'financial_inputs_changed', 'first_component_arithmetic_error_identified', 'independent_agent_review', 'current_contract_fee_changed', 'new_case_or_geography_quota', 'full_financial_model_complete']), 'Preservation and bounded same-agent review status')
require(component['fourteen_core_questions_unchanged'] and component['practitioner_free_full_research_preserved'], 'Questions and full practitioner benefit preserved')
require(all(component[k] == [] for k in ['actual_quotes', 'actual_staffing', 'actual_customers', 'actual_participants', 'actual_savings', 'external_actions']), 'No actual commercial/fieldwork record fabricated')
cost = read(component['cost_applications_path'])
require(len(cost['cases']) == cost['case_count'] == 12 and len(cost['checks']) == cost['check_count'] == 22 and all(x['passed'] for x in cost['checks']), 'Twelve constructed cases and22 checks passed')
require(cost['source_workbook_sha256'] == component['first_component_workbook_sha256'] == digest(Path(component['first_component_workbook_path'])) and cost['source_financial_inputs_sha256'] == digest(ROOT / '04-table/financial-inputs.json'), 'Constructed applications use exact unchanged inputs and workbook')
require(not cost['workbook_changed'] and not cost['financial_inputs_changed'] and not cost['native_Excel_application_tested'] and not cost['independent_agent_review'], 'No original edits or new independent/native execution claim')
cancel = next(x for x in cost['cases'] if x['case_id'] == 'SA05')
require(cancel['result']['catalogue_delivered_unit_hours'] == 0 and cancel['result']['additional_noncompletion_work_hours'] == 3, 'Zero-completion gap is exposed rather than claimed covered')

bridge = read(component['prior_study_bridge_path'])
workspace = ROOT.parent.parent
for x in bridge['provenance']:
    require(digest(workspace / x['path']) == x['sha256'], 'Original study provenance: ' + x['role'])
answers = json.loads((workspace / bridge['provenance'][0]['path']).read_text())['answers']
answer_by = {x['id']: x for x in answers}
index = {x['id']: x for x in json.loads((workspace / bridge['provenance'][1]['path']).read_text())}
require(len(bridge['questions']) == 4 and bridge['linked_saved_answers'] == 32 and bridge['semantic_rereads'] == 4 and bridge['model_reruns'] == 0, 'Four exact questions,32 saved answers,four selected semantic rereads')
semantic_products = []
for q in bridge['questions']:
    require(len(q['answer_links']) == 8 and {(x['product'], x['repeat']) for x in q['answer_links']} == {(a,b) for a in ['ChatGPT','Claude','Gemini','Perplexity'] for b in [1,2]}, 'Four products/two repeats: ' + q['question_id'])
    for link in q['answer_links']:
        a = answer_by[link['answer_id']]
        require(hashlib.sha256(a['prompt'].encode()).hexdigest() == link['prompt_sha256'] == q['prompt_sha256'] and a['prompt'] == q['prompt'], 'Exact prompt: ' + a['id'])
        require(hashlib.sha256(a['fullAnswer'].encode()).hexdigest() == link['full_answer_sha256'] and a['fullAnswer'] == index[a['id']]['fullAnswer'], 'Exact saved answer/index: ' + a['id'])
        require(all(link[k] == a[j] for k,j in [('product','product'), ('repeat','repeat'), ('country','country'), ('observed_at_utc','dateUtc')]), 'Saved metadata: ' + a['id'])
        if link['semantic_reread_for_this_review']:
            semantic_products.append(link['product'])
require(set(semantic_products) == {'ChatGPT','Claude','Gemini','Perplexity'} and len(semantic_products) == 4, 'Selected semantic rereads span all four products')
bridge_qa = read('04-table/research-notes/t05s-second-check/prior-study/bridge-checks.json')
require(len(bridge_qa['checks']) == 136 and all(x['passed'] for x in bridge_qa['checks']), 'All136 bridge checks retained')
comparison = read('04-table/research-notes/t05s-second-check/comparator-map.json')
require(comparison['recruitment_comparators'] == 6 and comparison['JGA_contexts'] == 1 and len(comparison['records']) == 7, 'All six recruitment comparators plus JGA retained with scope boundaries')

paths = [ROOT / '04-table/T05S-SECOND-CHECK-READOUT.md', ROOT / '04-table/T05S-PROGRAMME-COST-REFINEMENTS.md', ROOT / '04-table/T05S-second-challenge-map.json', ROOT / '04-table/financial-inputs.json', ROOT / '08-qa/T05S-second-check-captures.json', ROOT / '08-qa/T05S-second-check-record-map.json', Path(component['first_component_workbook_path'])]
paths += [x for x in (ROOT / '04-table/research-notes/t05s-second-check').rglob('*') if x.is_file() and 'before-review' not in x.parts and not x.name.startswith('.')]
artifacts = [{'path':str(x.relative_to(ROOT)) if x.is_relative_to(ROOT) else str(x), 'sha256':digest(x)} for x in sorted(set(paths))]
output = {'date':'2026-11-01', 'status':'passed_same_agent_second_check', 'method':'Source-scoped desk review, exact preservation/lineage checks and read-only constructed applications. Previous independent review is retained; no new independent-agent audit.', 'independent_agent_review':False, 'native_Excel_application_tested':False, 'checks':checks, 'check_count':len(checks), 'reviewed_artifacts':artifacts, 'required_programme_refinements_recorded':True, 'programme_model_complete':False, 'arithmetic_error_identified':False, 'workbooks_changed':False, 'financial_inputs_changed':False, 'external_actions':[]}
(ROOT / '08-qa/t05s-second-review/review-checks.json').write_text(json.dumps(output, indent=2) + '\n')
print(json.dumps({'status':output['status'], 'checks':len(checks), 'reviewed_artifacts':len(artifacts), 'programme_refinements_still_required':True}))
