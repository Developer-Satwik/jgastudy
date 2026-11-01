from pathlib import Path
import json,hashlib,re
from collections import Counter
R=Path.cwd();W=R.parent.parent;P=R/'03-report/research-notes/r07-second-check/competitors';checks=[]
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def test(ok,msg):
 assert ok,msg
 checks.append(dict(check=msg,passed=True))
a=read(P/'source-candidates.json');c=read(P/'claim-candidates.json');b=read(P/'prior-study-bridge.json');cap=read(P/'capture-manifest.json')
test(len(a['records'])==3 and len(a['reused_canonical_sources'])==4,'Three new routes and four canonical reuses')
test(len(c['records'])==6,'Six bounded claims/design records')
canon={s['source_id'] for s in read(R/'02-evidence/registers/sources.json')['records']};new={x['candidate_id'] for x in a['records']}
for x in c['records']:
 test(set(x['source_candidate_ids'])<=new and set(x['canonical_source_ids'])<=canon,'Claim refs '+x['candidate_id'])
 test(x['value'] is None and x['unit'] is None and x['denominator'] is None,'No adopted numeric estimate '+x['candidate_id'])
for x in cap['files']:test(sha(R/x['path'])==x['sha256'],'Retained filehash '+x['path'])
for x in a['records']+a['reused_canonical_sources']:
 if x.get('capture_path'):test(x['http_status']==200 and x['capture_path'].endswith('.html'),'Raw original valid '+x.get('candidate_id',x.get('source_id')))
 else:test(x['http_status']==403 and x['capture_sha256'] is None and bool(x['review_extracts']),'No error promoted to original '+x.get('candidate_id',x.get('source_id')))
for x in b['provenance']:test(sha(W/x['path'])==x['sha256'],'Bridge provenance '+x['role'])
answers=read(W/b['provenance'][0]['path'])['answers'];idx={x['id']:x for x in read(W/b['provenance'][1]['path'])};byid={x['id']:x for x in answers}
test(b['selected_questions']==4 and b['selected_total_answers']==32 and not b['recommendation_counts_reused'],'Four constructed prompts32texts no counts transferred')
for q in b['questions']:
 test(len(q['answer_links'])==8 and q['saved_answer_count']==8,'Coverage '+q['question_id'])
 test(hashlib.sha256(q['prompt'].encode()).hexdigest()==q['prompt_sha256'],'Prompt hash '+q['question_id'])
 for x in q['answer_links']:
  v=byid[x['answer_id']];i=idx[x['answer_id']]
  test(v['prompt']==q['prompt'] and i['prompt']==q['prompt'],'Exact prompt '+x['answer_id'])
  test(sha(W/b['provenance'][0]['path'])==b['provenance'][0]['sha256'],'Stable sourcefile '+x['answer_id'])
  test(hashlib.sha256(v['fullAnswer'].encode()).hexdigest()==x['full_answer_sha256']==v['answerHash'],'Text hash '+x['answer_id'])
  test(v['fullAnswer']==i['fullAnswer'],'Exact index text '+x['answer_id'])
  test(v['dateUtc']==x['observed_at_utc'] and v['product']==x['product'] and v['repeat']==x['repeat'],'Date/tool/repeat '+x['answer_id'])
  test(v['sourceStatus']==x['source_status'] and v.get('sourceNote')==x['source_note'],'Source limits '+x['answer_id'])
test(dict(Counter(x['sourceStatus'] for x in answers))==b['global_source_limitations_preserved'],'Full-study source statuses retained')
for target in re.findall(r'\]\(([^)]+)\)',(P/'COMPETITOR-CHALLENGE.md').read_text()):
 if not target.startswith('http'):test((P/target).exists(),'Local note link '+target)
test(read(P/'search-review-log.json')['external_actions']==[] and b['external_actions']==[],'No external actions')
out=dict(date='2026-10-29',status='passed',check_count=len(checks),checks=checks,scope='Own-strand parse/hash/link/exact saved-data checks; not independent integrated review or validation of generated advice',source_routes=3,canonical_reuses=4,claims=6,selected_questions=4,selected_saved_answer_texts=32)
(P/'verification.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='checks'},indent=2))
