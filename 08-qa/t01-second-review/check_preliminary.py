from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parents[2];W=R.parents[1];B=R/'04-table/research-notes/t01-second-check';O=R/'08-qa/t01-second-review';checks=[];hashes={}
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def ck(v,n):checks.append({'name':n,'passed':bool(v)});assert v,n
def resolve(p):
 p=Path(p)
 for q in [p if p.is_absolute()else R/p,W/p]:
  if q.is_file():return q
 raise FileNotFoundError(p)
def checkpaths(x):
 if isinstance(x,list):
  for y in x:checkpaths(y)
 elif isinstance(x,dict):
  for k,v in x.items():
   if (k=='path'or k.endswith('_path'))and v:
    hk='sha256'if k=='path'else k[:-5]+'_sha256';h=x.get(hk)
    if h:
     p=resolve(v);ck(sha(p)==h,'retained hash '+v);hashes[v]=h
   checkpaths(v)
S={};C={};old=read(B/'before-review/sources.json')['records'];sid={s['source_id']for s in old}
for folder in ['history','market','competitors','root']:
 d=read(B/folder/'source-candidates.json');checkpaths(d);checkpaths(read(B/folder/'capture-manifest.json'))
 for s in d.get('records',[]):ck(s['candidate_id']not in S,'new source candidate unique '+s['candidate_id']);S[s['candidate_id']]=s
 for s in d.get('reused_canonical_sources',[]):ck(s['source_id']in sid,'explicit canonical reuse '+s['source_id'])
 for c in read(B/folder/'claim-candidates.json')['records']:
  ck(c['candidate_id']not in C,'claim candidate unique '+c['candidate_id']);C[c['candidate_id']]=c
ck(len(S)==6 and len(C)==25,'six new route candidates and25 bounded claim/condition candidates')
for c in C.values():
 ck(set(c.get('source_candidate_ids',[]))<=set(S),'candidate sources resolve '+c['candidate_id'])
 ck(set(c.get('canonical_source_ids',[]))<=sid,'canonical sources resolve '+c['candidate_id'])
 ck(bool(c.get('limitations')),'limits retained '+c['candidate_id'])
for x in read(R/'08-qa/T01-second-check-baseline.json')['files']:ck(sha(R/x['path'])==x['sha256'],'131 baseline file preserved '+x['path'])
bridge=read(B/'competitors/prior-study-bridge.json');A={a['id']:a for a in read(W/'sites/jga-discovery-report-2026-10-22/output/JGA-Research-Pack/data/all-answers.json')['answers']};I={a['id']:a for a in read(W/'sites/jgafinalcode/dist/data/answer-index.json')};previous=read(R/'03-report/research-notes/r08-second-check/competitors/prior-study-bridge.json');P={a['answer_id']:a for q in previous['questions']for a in q['answer_links']}
for x in bridge['provenance']:ck(sha(resolve(x['path']))==x['sha256'],'prior provenance exact '+x['role'])
ck(len(bridge['questions'])==3 and bridge['selected_saved_records']==24 and bridge['semantic_rereads']==3 and bridge['other_records_integrity_only']==21,'three constructed prompts24 saved records3semantic rereads scope explicit')
for q in bridge['questions']:
 ck(len(q['answer_links'])==8 and{a['product']for a in q['answer_links']}=={'ChatGPT','Claude','Gemini','Perplexity'},'four tools two repeats '+q['question_id'])
 ck(hashlib.sha256(q['prompt'].encode()).hexdigest()==q['prompt_sha256'],'question hash exact '+q['question_id'])
 for a in q['answer_links']:
  n=A[a['answer_id']];ck(n['prompt']==q['prompt']and n['promptHash']==a['prompt_sha256'],'saved prompt exact '+a['answer_id']);ck(hashlib.sha256(n['fullAnswer'].encode()).hexdigest()==a['full_answer_sha256'],'saved full answer hash '+a['answer_id']);ck(n['fullAnswer']==I[a['answer_id']]['fullAnswer'],'final index exact '+a['answer_id']);ck(P[a['answer_id']]['full_answer_sha256']==a['full_answer_sha256'],'earlier bridge exact '+a['answer_id']);ck(n['sourceStatus']==a['source_status'],'capture limitation retained '+a['answer_id'])
ck(bridge['no_model_reruns']and not bridge['recommendation_counts_reused']and not bridge['new_participant_evidence'],'prior bridge is not fresh model evidence or demand')
cm=read(B/'competitors/comparator-map.json');ck(len(cm['records'])==7 and cm['recruitment_comparator_count']==6 and cm['JGA_context_count']==1 and cm['not_the_T01_six_business_models'],'six recruitment firms plusJGA distinct from six business models')
ck(all(not x['actual_Table_buyer']and not x['actual_sponsor']and not x['actual_participant']for x in cm['records']),'comparator names not converted into qualified contacts')
ct=S['T1R2-S01'];ck(ct['capture_path']is None and ct['capture_kind']=='primary_reader_extract_only'and ct['review_extracts'][0]['kind']=='selected_reader_extract','Chatham reader note not raw original')
t=(B/'history/captures/T1H-S02.txt').read_text();ck('Nick Day, CEO of JGA Recruitment Group, moderated a panel'in t and'Hosted by PayrollOrg and sponsored by Strada'in t,'Nick public moderator role supported not formal partnership')
h=read(B/'history/screened-leads.json');ck(bool(h),'broader partnership lead retained as screened not claimed')
for p in ['05-analysis/observations.json','05-analysis/charts.json','04-table/financial-inputs.json']:ck(read(R/p)['records']==[],'actual array remains empty '+p)
result={'status':'passed_preliminary_T01_second_challenge_source_review_integration_pending','date':'2026-10-30','check_count':len(checks),'checks':checks,'retained_hashes':hashes,'new_routes':6,'claim_candidates':25,'open_substantive_issues':[],'manual_review':['Current Chatham primary FAQ reopened: Rule-specific no recording/AI/in-room imagery, not universal interview ban.','Nick moderator role verified in retrospective; no formal partnership inference.','Planning Inspectorate policy scoped to one employer.','Three original ChatGPT answers reread; other21records integrity only.','First-pass price/rights distinctions retained; no new price input.'],'capture_classification_followup':'Hays fresh raw is shell; substantive method only selected reader note. History Accomplishments shell excluded. Verify integrated inventory preserves this.','integration_complete':False,'fieldwork':False,'commercial_validation':False,'external_contact':False}
(O/'preliminary-checks.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n');print(json.dumps({k:v for k,v in result.items()if k not in ['checks','retained_hashes']},indent=2))
