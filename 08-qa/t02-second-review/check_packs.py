from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parents[2];W=R.parent.parent;B=R/'04-table/research-notes/t02-second-check';O=R/'08-qa/t02-second-review';checks=[]
def rd(p):return json.loads(p.read_text())
def ck(v,n):checks.append(dict(name=n,passed=bool(v)));assert v,n
def hs(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def sh(t):return hashlib.sha256(t.encode()).hexdigest()
sids={x['source_id']for x in rd(B/'before-review/02-evidence/registers/sources.json')['records']};ids=set()
for folder in ['history','market','competitors']:
 d=rd(B/folder/'source-candidates.json')
 for x in d.get('records',[]):
  ck(x['candidate_id']not in ids,'unique new source '+x['candidate_id']);ids.add(x['candidate_id'])
  ck(hs(R/x['capture_path'])==x['capture_sha256'],'new retained original '+x['candidate_id'])
  for e in x.get('review_extracts',[]):ck(hs(R/e['path'])==e['sha256'],'new parsed file '+x['candidate_id'])
 for x in d.get('reused_canonical_sources',[]):
  ck(x['source_id']in sids,'reuse known canonical '+x['source_id'])
  for pk,hk in [('capture_path','capture_sha256'),('parsed_path','parsed_sha256'),('text_path','text_sha256')]:
   if x.get(pk):ck(hs(R/x[pk])==x[hk],'reuse retained hash '+x['source_id']+pk)
  for e in x.get('review_extracts',[]):ck(hs(R/e['path'])==e['sha256'],'reuse selected/parsed hash '+x['source_id'])
claims=[]
for folder in ['history','market','competitors']:
 for x in rd(B/folder/'claim-candidates.json')['records']:
  claims.append(x);ck(bool(x['locator'])and bool(x['limitations']),'claim support/boundary '+x['candidate_id'])
  ck(set(x.get('canonical_source_ids',[]))<=sids and set(x.get('source_candidate_ids',[]))<=ids,'claim candidate references '+x['candidate_id'])
  ck(x['value']is None and x['unit']is None and x['denominator']is None,'no numerical market result '+x['candidate_id'])
ck(len(claims)==9 and len({x['candidate_id']for x in claims})==9,'nine distinct author claims before root additions')
bridge=rd(B/'competitors/prior-study-bridge.json');ck([x['question_id']for x in bridge['questions']]==['S03-C','S08-C','S09-C'],'three selected exact questions')
for x in bridge['provenance']:ck(hs(W/x['path'])==x['sha256'],'original provenance '+x['role'])
a={x['id']:x for x in rd(W/'sites/jga-discovery-report-2026-10-22/output/JGA-Research-Pack/data/all-answers.json')['answers']};i={x['id']:x for x in rd(W/'sites/jgafinalcode/dist/data/answer-index.json')}
for q in bridge['questions']:
 ck(sh(q['prompt'])==q['prompt_sha256'],'prompt hash '+q['question_id'])
 ck(len(q['answer_links'])==8 and {x['product']for x in q['answer_links']}=={'ChatGPT','Claude','Gemini','Perplexity'}and {x['repeat']for x in q['answer_links']}=={1,2},'four products two repeats '+q['question_id'])
 for x in q['answer_links']:
  y=a[x['answer_id']];z=i[x['answer_id']]
  ck(y['prompt']==q['prompt']and y['promptHash']==x['prompt_sha256']==q['prompt_sha256'],'exact saved prompt '+x['answer_id'])
  ck(sh(y['fullAnswer'])==x['full_answer_sha256']==y['answerHash'],'exact saved answer hash '+x['answer_id'])
  ck(y['fullAnswer']==z['fullAnswer']and y['prompt']==z['prompt'],'final-index exact text '+x['answer_id'])
  ck(y['country']==x['country']and y['dateUtc']==x['observed_at_utc']and y['product']==x['product']and y['repeat']==x['repeat'],'routing metadata '+x['answer_id'])
  ck(y['sourceStatus']==x['source_status']and y['sourceNote']==x['source_note'],'source-status context '+x['answer_id'])
  ck(x['semantic_reread_for_this_lens']==(x['product']=='ChatGPT'and x['repeat']==1),'three semantic rereads distinct '+x['answer_id'])
cm=rd(B/'competitors/comparator-map.json');rows=cm['records'];ck(len(rows)==7 and {x['firm']for x in rows}=={'Portfolio Payroll','Frazer Jones','Oakleaf Partnership','Middlemore','Hays','Robert Half','JGA'},'all six recruiters plus JGA')
res=dict(date='2026-10-30',status='passed_author_pack_independent_review_integration_pending',check_count=len(checks),checks=checks,new_author_sources=2,author_claims=9,prior_questions=3,prior_saved_answers=24,semantic_rereads=3,manual_semantic_scope='Read original ChatGPT-r1 full texts for task/remit/evidence assumptions; no generated facts verified or Table demand inferred.',open_substantive_issues=[])
(O/'source-review-checks.json').write_text(json.dumps(res,indent=2,ensure_ascii=False)+'\n');print(json.dumps({k:v for k,v in res.items()if k!='checks'},indent=2))
