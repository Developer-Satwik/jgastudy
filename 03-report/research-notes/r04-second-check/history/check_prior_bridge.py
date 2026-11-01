from pathlib import Path
from collections import Counter
import hashlib, json

PROJECT = Path(__file__).resolve().parents[4]
WORKSPACE = PROJECT.parent.parent
BRIDGE = PROJECT / '03-report/research-notes/r04-second-check/competitors/prior-study-bridge.json'

def read(p): return json.loads(p.read_text())
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def digest(t): return hashlib.sha256(t.encode('utf-8')).hexdigest()
checks = []
def check(name, actual, expected):
    checks.append(dict(check=name, actual=actual, expected=expected, passed=actual == expected))

initial_hash = sha(BRIDGE)
bridge = read(BRIDGE)
provenance = {r['role']:r for r in bridge['provenance']}
for role, r in provenance.items():
    check('current provenance hash: ' + role, sha(WORKSPACE / r['path']), r['sha256'])
answers = read(WORKSPACE / provenance['all_answers']['path'])['answers']
index = read(WORKSPACE / provenance['answer_index']['path'])
summary = read(WORKSPACE / provenance['summary']['path'])
prior = read(WORKSPACE / provenance['previous_bridge']['path'])
prior_check = read(WORKSPACE / provenance['previous_independent_check']['path'])
check('previous independent check status', prior_check['status'], 'passed')
check('previous independent checks passed', all(r['passed'] for r in prior_check['checks']), True)
check('prior checker targets current prior bridge', prior_check['bridge_sha256'], sha(WORKSPACE / provenance['previous_bridge']['path']))
for r in prior['provenance']:
    check('independently rechecked earlier provenance: ' + r['role'], sha(WORKSPACE / r['path']), r['sha256'])
check('bridge prior provenance summary', bridge['previous_bridge_hashes_match'], True)
check('bridge prior provenance items', all(r['passed'] for r in bridge['previous_bridge_provenance_checks']), True)

desc = bridge['study_description']
check('all-answer count', len(answers), desc['saved_answers'])
check('unique answer IDs', len({r['id'] for r in answers}), 352)
check('unique questions', len({r['question'] for r in answers}), desc['unique_questions'])
check('unique situations', len({r['situation'] for r in answers}), desc['situations'])
check('product names', sorted({r['product'] for r in answers}), sorted(desc['tools']))
check('observed date range', [min(r['dateUtc'] for r in answers), max(r['dateUtc'] for r in answers)], desc['date_range_utc'])
check('six comparator names', summary['comparators'], desc['comparators'])
check('raw/index all ID membership', sorted(r['id'] for r in answers), sorted(r['id'] for r in index))
check('global source-status counts', dict(Counter(r['sourceStatus'] for r in answers)), bridge['global_source_limitations_preserved'])
check('partial/pending records not erased', sum(r['sourceStatus'] in ['partial','pending'] for r in answers), 7)

selected = []; linked_ids = []; question_ids = []
raw = {r['id']:r for r in answers}; indexed = {r['id']:r for r in index}
check('selected situation IDs', [s['situation_id'] for s in bridge['selected_situations']], ['S01','S05','S10'])
for situation in bridge['selected_situations']:
    sid = situation['situation_id']
    rows = [r for r in answers if r['situation'] == sid]
    selected.extend(rows)
    check(sid + ' answer count', len(rows), situation['saved_answer_count'])
    check(sid + ' four question labels', [q['question_id'] for q in situation['questions']], [sid + '-' + x for x in 'ABCD'])
    check(sid + ' source-status counts', dict(Counter(r['sourceStatus'] for r in rows)), situation['capture_status_counts'])
    for q in situation['questions']:
        qid = q['question_id']; question_ids.append(qid)
        qr = [r for r in rows if r['question'] == qid]
        check(qid + ' exact prompt text', sorted({r['prompt'] for r in qr}), [q['prompt']])
        check(qid + ' computed prompt hash', digest(q['prompt']), q['prompt_text_sha256'])
        check(qid + ' raw prompt hashes', sorted({r['promptHash'] for r in qr}), [q['prompt_text_sha256']])
        check(qid + ' raw answer count', len(qr), q['saved_answer_count'])
        check(qid + ' answer links exact membership', sorted(l['answer_id'] for l in q['answer_links']), sorted(r['id'] for r in qr))
        check(qid + ' products with two saved observations each', dict(Counter(r['product'] for r in qr)), {p:2 for p in desc['tools']})
        check(qid + ' product/repeat coverage', sorted((r['product'],r['repeat']) for r in qr), sorted((p,n) for p in desc['tools'] for n in [1,2]))
        for link in q['answer_links']:
            ident = link['answer_id']; linked_ids.append(ident)
            r = raw[ident]; ix = indexed[ident]
            comparisons = {
                'situation': r['situation'] == sid,
                'question': r['question'] == qid,
                'product': r['product'] == link['product'],
                'repeat': r['repeat'] == link['repeat'],
                'timestamp': r['dateUtc'] == link['observed_at_utc'],
                'source_status': r['sourceStatus'] == link['source_status'],
                'full_answer_digest': digest(r['fullAnswer']) == link['exported_full_answer_sha256'],
                'stored_answer_hash': r['answerHash'] == link['recorded_answer_hash'],
                'computed_stored_answer_agreement': digest(r['fullAnswer']) == r['answerHash'],
                'index_full_answer_text': ix['fullAnswer'] == r['fullAnswer'],
                'index_prompt_text': ix['prompt'] == q['prompt'] == r['prompt'],
                'index_metadata': all(ix[k] == r[k] for k in ['id','question','situation','product','country','repeat','dateUtc','sourceStatus'])
            }
            check(ident + ' raw/link/index agreement', comparisons, {k:True for k in comparisons})

check('selected total saved answers', len(selected), bridge['selected_total_answers'])
check('selected answer total is96', len(selected), 96)
check('selected twelve exact questions', len(set(question_ids)), 12)
check('unique linked answer IDs', len(set(linked_ids)), 96)
check('all selected IDs linked', sorted(linked_ids), sorted(r['id'] for r in selected))
check('bridge selected text-hash summary', bridge['all_selected_answer_text_hashes_match'], True)
check('bridge selected index-text summary', bridge['all_selected_index_texts_match'], True)

prompts = {q['question_id']:q['prompt'] for s in bridge['selected_situations'] for q in s['questions']}
for qid in ['S01-D','S05-D','S10-D']:
    check(qid + ' CFO assumption is in researcher-written input', 'CFO' in prompts[qid], True)
check('S05-D already assumes permanent leader', 'one permanent Group Payroll Director' in prompts['S05-D'], True)
check('S10-D already assumes permanent-head recruitment', 'permanent head' in prompts['S10-D'], True)
check('no recommendation-count transfer', bridge['recommendation_counts_reused'], False)
check('no external actions in bridge', bridge['external_actions'], [])
check('no historical files edited claim', bridge['files_changed_outside_own_folder'], [])
check('no model reruns claimed', 'No model reruns' in bridge['purpose'], True)
anti = bridge['anti_anchoring_rule']
check('constructed assumptions explicitly not corroboration', 'assumptions' in anti and 'not corroboration' in anti, True)
check('unaided needs/events first', 'unaided participant needs and actual events first' in anti, True)
check('no mandatory hierarchy', 'presumed hierarchy as mandatory questions' in anti, True)
check('actual authority not transferred', any('approval rights' in t and 'Actual employer demand' in t for t in bridge['cannot_transfer']), True)
check('model counts not decision evidence', any('Model recommendations/counts' in t and 'organisational decisions' in t for t in bridge['cannot_transfer']), True)
check('source-record limits remain', any('partial and missing source records remain limited' in t for t in bridge['cannot_transfer']), True)
qmap = read(PROJECT / '01-method/question-map.json')
check('fourteen current core questions', len(qmap['records']), 14)
check('canonical instrument matches frozen v0.2', qmap, read(PROJECT / '01-method/question-map-v0.2.json'))
check('unaided need precedes later case probes', [r['question_id'] for r in qmap['records']][:5], ['Q001','Q002','Q003','Q004','Q005'])
check('bridge unchanged during independent verification', sha(BRIDGE), initial_hash)

failed = [r['check'] for r in checks if not r['passed']]
result = dict(date='2026-10-29',status='passed' if not failed else 'failed',reviewer='r04_second_history independent follow-up; not author of competitor bridge',
    bridge_path=str(BRIDGE.relative_to(PROJECT)),bridge_sha256=initial_hash,
    method='Fresh exact local reads: provenance hashes, selected prompt bytes/hashes, all96 linked raw answer hashes and index text/metadata, coverage and source statuses. No recommendation recoding or new model run.',
    selected_situations=['S01','S05','S10'],selected_questions=12,selected_saved_answers=96,
    checks=checks,check_count=len(checks),failed_checks=failed,
    critical_anti_anchoring='CFO language is already in S01-D/S05-D/S10-D; S05-D and S10-D already presuppose permanent-leader recruitment. Repetition of these premises in answers cannot establish actual market authority or required solution.',
    scope_limit='Verifies fidelity and boundaries of the bridge, not historical external facts, actual employer behaviour, recruitment capability or an empirical payroll authority map.',
    external_actions=[],prior_study_files_changed=False,bridge_changed=False)
(PROJECT / '08-qa/R04-prior-study-bridge-check.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
print(json.dumps(dict(status=result['status'],checks=len(checks),failed=failed,selected_answers=len(selected),selected_questions=len(set(question_ids)),bridge_sha256=initial_hash),indent=2))
