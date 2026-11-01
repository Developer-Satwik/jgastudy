from pathlib import Path
from collections import Counter
import hashlib,json,re
ROOT=Path(__file__).resolve().parents[1]
WORKSPACE=ROOT.parent.parent
B=ROOT/'03-report/research-notes/r05-second-check/competitors/prior-study-bridge.json'
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def textsha(s):return hashlib.sha256(s.encode()).hexdigest()
checks=[]
def check(v,label):
 checks.append({'check':label,'passed':bool(v)})
 if not v:raise AssertionError(label)
b=read(B)
for p in b['provenance']:
 check((WORKSPACE/p['path']).is_file(),'Provenance file exists: '+p['role'])
 check(sha(WORKSPACE/p['path'])==p['sha256'],'Provenance hash matches: '+p['role'])
files={p['role']:WORKSPACE/p['path'] for p in b['provenance']}
a=read(files['all_answers'])['answers'];ix=read(files['answer_index']);s=read(files['summary'])
by={r['id']:r for r in a};ind={r['id']:r for r in ix}
check(len(by)==len(a)==352,'Original export has352 unique saved answer records')
check(len(ind)==len(ix)==352,'Answer index has352 unique records')
check(set(s['tools'])=={'ChatGPT','Claude','Gemini','Perplexity'},'Original summary identifies four tools')
check(len(b['questions'])==b['selected_questions']==4,'Four selected questions retained')
check({q['question_id'] for q in b['questions']}=={'S04-C','S05-C','S09-C','S10-C'},'Selected IDs match stated contrasts')
seen=set();tools={'ChatGPT','Claude','Gemini','Perplexity'}
for q in b['questions']:
 qid=q['question_id'];links=q['answer_links'];p=q['prompt']
 check(textsha(p)==q['prompt_sha256'],'Prompt SHA matches: '+qid)
 check(bool(re.search('evidence|demonstrate|verify',p,re.I)),'Evidence demand embedded in selected prompt: '+qid)
 check(len(links)==q['saved_answer_count']==8,'Eight saved answers: '+qid)
 check({(x['product'],x['repeat']) for x in links}=={(t,n) for t in tools for n in [1,2]},'Four-tool/two-repeat coverage: '+qid)
 check(Counter(x['source_status'] for x in links)==Counter(q['capture_status_counts']),'Selected capture status counts: '+qid)
 for x in links:
  ident=x['answer_id'];r=by[ident];k=ind[ident]
  check(ident not in seen,'Selected unique answer ID: '+ident);seen.add(ident)
  check(r['question']==k['question']==qid,'Question linkage: '+ident)
  check(r['prompt']==k['prompt']==p,'Exact prompt preserved in both exports: '+ident)
  check(textsha(r['prompt'])==r['promptHash']==x['prompt_sha256']==q['prompt_sha256'],'Prompt hash linkage: '+ident)
  check(r['fullAnswer']==k['fullAnswer'],'Exact full answer/index text: '+ident)
  check(textsha(r['fullAnswer'])==r['answerHash']==x['full_answer_sha256']==x['recorded_answer_hash'],'Full answer text/hash: '+ident)
  check(r['product']==k['product']==x['product'] and r['repeat']==k['repeat']==x['repeat'],'Tool/repeat linkage: '+ident)
  check(r['dateUtc']==k['dateUtc']==x['observed_at_utc'],'Observation date linkage: '+ident)
  check(r['sourceStatus']==k['sourceStatus']==x['source_status'],'Source status linkage: '+ident)
check(len(seen)==b['selected_total_answers']==32,'32 selected saved answers; no rerun counted')
check(dict(Counter(x['sourceStatus'] for x in a))==b['global_source_limitations_preserved'],'Original global source limits preserved independently of subset completeness')
check(b['recommendation_counts_reused'] is False,'No recommendation-count transfer')
check('prompted' in b['anti_anchoring_rule'] and 'unaided' in b['anti_anchoring_rule'],'Explicit anti-anchoring rule retained')
check('six months' in b['anti_anchoring_rule'],'S10 duration/hiring premise retained as constructed')
check(b['external_actions']==[],'No external action recorded in bridge')
result={'date':'2026-10-29','status':'passed','bridge_path':str(B.relative_to(ROOT)),'bridge_sha256':sha(B),'checks':checks,'check_count':len(checks),'selected_questions':4,'selected_saved_answers':32,'scope':'Independent exact text, hash, provenance, index/date/status and coverage checks. Not semantic validation of model advice, source capture completeness, buyer demand or cost/savings/authority proof.','no_model_reruns':True,'source_limitations_preserved':b['global_source_limitations_preserved']}
(ROOT/'08-qa/R05-prior-study-bridge-check.json').write_text(json.dumps(result,indent=2)+'\n')
(ROOT/'08-qa/R05-prior-study-bridge-check.md').write_text(f'''# Independent R05 prior-study bridge check

29 October 2026. Passed {len(checks)} explicit checks on four constructed questions and 32 saved full answer texts.

Verified the four provenance-file hashes, unique ID coverage in the original 352-answer export and index, exact prompts, text hashes, dates, source-status labels and all four tools/two repeats for each selected question. The original global source-capture limitations remain distinct from this complete selected subset. The exact checked bridge hash is in the JSON record.

The selected C prompts ask for evidence or verification, so repeated due-diligence wording cannot independently establish buyer priorities. They assume recruitment, and S10 assumes a six-month interim alongside a permanent search. None is employer fieldwork or a current statement of cost, tax status, candidate availability, capability or outcome. No recommendation counts or numerical model claims transferred. No model reruns performed.

This is linkage and integrity verification, not independent validation of every answer's advice, every underlying website or the old study's full capture conditions. It does not establish later commercial demand or payroll investment evidence.
''')
print(json.dumps({k:v for k,v in result.items() if k!='checks'},indent=2))
