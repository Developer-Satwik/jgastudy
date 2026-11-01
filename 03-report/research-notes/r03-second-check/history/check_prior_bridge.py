from pathlib import Path
from collections import Counter
import hashlib,json

PROJECT=Path(__file__).resolve().parents[4]
WORKSPACE=PROJECT.parent.parent
BRIDGE=PROJECT/'03-report/research-notes/r03-second-check/competitors/prior-study-bridge.json'
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def digest(text):return hashlib.sha256(text.encode('utf-8')).hexdigest()
checks=[]
def check(name,actual,expected):
    checks.append({'check':name,'actual':actual,'expected':expected,'passed':actual==expected})

initial_hash=sha(BRIDGE)
bridge=read(BRIDGE)
provenance={r['role']:r for r in bridge['provenance']}
for role,r in provenance.items():check('provenance hash '+role,sha(WORKSPACE/r['path']),r['sha256'])
answers=read(WORKSPACE/provenance['all_answers']['path'])['answers']
index=read(WORKSPACE/provenance['answer_index']['path'])
summary=read(WORKSPACE/provenance['summary']['path'])
previous_check=read(WORKSPACE/provenance['previous_independent_check']['path'])
check('previous independent status',previous_check['status'],'passed')
check('previous independent checks remain passed',all(r['passed'] for r in previous_check['checks']),True)
check('bridge previous hashes claim',bridge['previous_bridge_hashes_match'],True)
check('bridge previous status claim',bridge['previous_independent_check_status'],previous_check['status'])

description=bridge['study_description']
check('saved answer count',len(answers),description['saved_answers'])
check('unique answer IDs',len({r['id'] for r in answers}),352)
check('unique question count',len({r['question'] for r in answers}),description['unique_questions'])
check('situation count',len({r['situation'] for r in answers}),description['situations'])
check('tools',sorted({r['product'] for r in answers}),sorted(description['tools']))
check('recorded date range',[min(r['dateUtc'] for r in answers),max(r['dateUtc'] for r in answers)],description['date_range_utc'])
check('comparators',summary['comparators'],description['comparators'])
check('raw/index exact record IDs',sorted(r['id'] for r in answers)==sorted(r['id'] for r in index),True)
check('source capture status limits',dict(Counter(r['sourceStatus'] for r in answers)),bridge['global_source_limitations_preserved'])
check('six partial and one pending retained',sum(r['sourceStatus'] in ['partial','pending'] for r in answers),7)

check('selected situation IDs',[r['situation_id'] for r in bridge['selected_situations']],['S04','S05','S09'])
selected=[];question_ids=[]
for situation in bridge['selected_situations']:
    sid=situation['situation_id'];rows=[r for r in answers if r['situation']==sid];selected.extend(rows)
    check(sid+' answer count',len(rows),situation['saved_answers'])
    check(sid+' four questions',len({r['question'] for r in rows}),4)
    check(sid+' source status limits',dict(Counter(r['sourceStatus'] for r in rows)),situation['capture_status_counts'])
    check(sid+' constructed question labels',[q['question_id'] for q in situation['questions']],[sid+'-'+q for q in 'ABCD'])
    check(sid+' unit excludes employer cases','not employer cases' in situation['unit'],True)
    for q in situation['questions']:
        qid=q['question_id'];question_ids.append(qid);qrows=[r for r in rows if r['question']==qid]
        check(qid+' saved answers',len(qrows),q['saved_answers'])
        check(qid+' exact constructed text',sorted({r['prompt'] for r in qrows}),[q['prompt']])
        check(qid+' prompt text digest',digest(q['prompt']),q['prompt_text_sha256'])
        check(qid+' raw stored prompt hashes',sorted({r['promptHash'] for r in qrows}),[q['prompt_text_sha256']])
        check(qid+' products',sorted({r['product'] for r in qrows}),sorted(description['tools']))
        check(qid+' two observations each',dict(Counter(r['product'] for r in qrows)),{k:2 for k in description['tools']})
check('selected total answers',len(selected),bridge['selected_total_answers'])
check('selected unique questions',len(set(question_ids)),12)
check('selected raw unique answer IDs',len({r['id'] for r in selected}),96)

lookup={r['id']:r for r in answers}
check('three raw examples',len(bridge['raw_examples']),3)
for example in bridge['raw_examples']:
    ident=example['answer_id'];r=lookup[ident]
    check(ident+' computed full-answer hash',digest(r['fullAnswer']),example['exported_full_answer_sha256'])
    check(ident+' stored answer hash',r['answerHash'],example['recorded_answer_hash'])
    check(ident+' computed/stored hash agreement',digest(r['fullAnswer']),r['answerHash'])
    check(ident+' question',r['question'],example['question_id'])
    check(ident+' product',r['product'],example['product'])
    check(ident+' observation date',r['dateUtc'],example['observed_at_utc'])
    check(ident+' generated-fact restriction',all(word in example['use'] for word in ['generated','rankings','performance','not adopted']),True)

check('no recommendation counts reused',bridge['recommendation_counts_reused'],False)
check('prior-study files unchanged claim',bridge['files_changed'],[])
anti=bridge['anti_anchoring_rule']
check('researcher-constructed scenarios acknowledged','researcher-written constructed scenarios' in anti,True)
check('not real buyer questions acknowledged','not observed real buyer questions' in anti,True)
check('unaided priorities protected','unaided priority/need questions first' in anti,True)
check('selective use protected','relevant later selective follow-up' in anti,True)
check('does not establish priorities or engagement terms','cannot establish participant priorities or engagement terms' in anti,True)
check('capture incompleteness preserved',any('missing source records remain missing' in r for r in bridge['cannot_transfer']),True)
check('ranks not market demand/quality',any('market share, demand, shortage, supplier quality' in r for r in bridge['cannot_transfer']),True)
check('generated old capability not external facts',any('Old generated capability/affiliation/fee claims' in r for r in bridge['cannot_transfer']),True)
check('no new prompt rerun','No prompt reruns' in bridge['purpose'],True)
check('bridge stable during check',sha(BRIDGE),initial_hash)

question_map=PROJECT/'01-method/question-map.json'
q=read(question_map)
check('fourteen unchanged core map records',len(q['records']),14)
check('current map matches v0.2 snapshot',q==read(PROJECT/'01-method/question-map-v0.2.json'),True)
check('unaided improvement priority before unmet service follow-up',[r['question_id'] for r in q['records']][:5],['Q001','Q002','Q003','Q004','Q005'])

failed=[r['check'] for r in checks if not r['passed']]
result={'date':'2026-10-29','status':'passed' if not failed else 'failed','reviewer':'r03_second_history independent follow-up',
 'bridge_path':str(BRIDGE.relative_to(PROJECT)),'bridge_sha256':initial_hash,
 'method':'Exact local provenance hashes and stored prompt/answer text checks. Recomputed selected coverage and source-status counts; no semantic recommendation recoding or validation of generated external claims.',
 'additional_check_input':{'path':str(question_map.relative_to(PROJECT)),'sha256':sha(question_map)},
 'checks':checks,'check_count':len(checks),'failed_checks':failed,
 'scope_limit':'Verifies faithfully constructed bridge and anti-anchoring limits, not historical external facts, market demand, recruitment performance or a new fieldwork result.',
 'external_actions':[],'prior_study_or_client_files_changed':False}
(PROJECT/'08-qa/R03-prior-study-bridge-check.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({'status':result['status'],'checks':len(checks),'failed':failed,'selected_answers':len(selected),'selected_questions':len(set(question_ids))},indent=2))
