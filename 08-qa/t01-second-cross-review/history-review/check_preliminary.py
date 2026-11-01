from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parents[3];W=R.parent.parent;B=R/'04-table/research-notes/t01-second-check';O=R/'08-qa/t01-second-cross-review/history-review';checks=[]
def rd(p):return json.loads(p.read_text())
def ck(v,n):checks.append(dict(name=n,passed=bool(v)));assert v,n
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
S=rd(R/'02-evidence/registers/sources.json')['records'];C=rd(R/'02-evidence/registers/claims.json')['records'];sid={x['source_id']:x for x in S};cid={x['claim_id']:x for x in C};mp=rd(R/'08-qa/T01-second-check-record-map.json')
for f in ['market','competitors','root']:
 d=rd(B/f/'source-candidates.json')
 for x in d.get('records',[])+d.get('reused_canonical_sources',[]):
  for pk,hk in [('capture_path','capture_sha256'),('text_path','text_sha256'),('parsed_path','parsed_sha256'),('parsed_extract_path','parsed_extract_sha256')]:
   if x.get(pk):ck((R/x[pk]).is_file() and h(R/x[pk])==x[hk],f+' source path/hash '+x.get('candidate_id',x.get('source_id'))+' '+pk)
  for e in x.get('review_extracts',[]):ck(h(R/e['path'])==e['sha256'],f+' explicit selected/parsed extract hash '+x.get('candidate_id',x.get('source_id')))
  if x.get('source_id'):ck(x['source_id'] in sid,f+' canonical reuse resolves '+x['source_id'])
 for x in rd(B/f/'claim-candidates.json')['records']:
  ck(x['value'] is None and x['unit'] is None and x['denominator'] is None,'no numerical demand/finance estimate '+x['candidate_id'])
  ck(bool(x['locator']) and bool(x['limitations']),'claim locator/limits present '+x['candidate_id'])
  y=cid[mp['claim_map'][x['candidate_id']]]
  ck(y['candidate_detail']==x,'candidate preserved exactly '+x['candidate_id'])
  expected={mp['source_map'].get(s,s) for s in x.get('canonical_source_ids',[])+x.get('source_candidate_ids',[])}
  ck(set(y['source_ids'])==expected,'canonical support exact '+x['candidate_id'])
  ck(y['claim_text']==x['claim_text'],'canonical wording exact '+x['candidate_id'])
roots=rd(B/'root/source-candidates.json')['records'];ch=next(x for x in roots if x['candidate_id']=='T1R2-S01')
ck(ch['capture_path'] is None and ch['capture_kind']=='primary_reader_extract_only','Chatham House selected reader not raw capture')
rt={x['candidate_id']:x for x in rd(B/'root/claim-candidates.json')['records']}
ck('meeting adopting' in rt['T1R2-C01']['limitations'] and 'not a universal interview' in rt['T1R2-C01']['limitations'],'Rule scope conditional on adopted meeting mode')
ck('No new restriction' in rt['T1R2-C05']['limitations'] and 'has or lacks' in rt['T1R2-C05']['limitations'],'free/paid overlap does not impose new employer rights')
ck('promises research free' in rt['T1R2-C05']['claim_text'] and rt['T1R2-C05']['evidence_class'].startswith('researcher_'),'free practitioner benefit preserved as analytic design issue')
cc=rd(B/'competitors/comparator-map.json')
ck(cc['recruitment_comparator_count']==6 and cc['JGA_context_count']==1 and cc['not_the_T01_six_business_models'],'six recruiter contexts plus JGA distinct from six mechanisms')
for x in cc['records']:ck(not x['actual_Table_buyer'] and not x['actual_sponsor'] and not x['actual_participant'],'no invented role '+x['firm'])
hays=next(x for x in rd(B/'competitors/source-candidates.json')['reused_canonical_sources'] if x['source_id']=='SRC-0192')
ck('shell' in hays['limitations'] and bool(hays['review_extracts']),'Hays substantive reader vs original application shell explicit')
ck('No source or' not in '', 'source review uses bounded observations rather than absence claims')
bridge=rd(B/'competitors/prior-study-bridge.json')
for x in bridge['provenance']:ck(h(W/x['path'])==x['sha256'],'prior bridge retained provenance '+x['role'])
answers=rd(W/'sites/jga-discovery-report-2026-10-22/output/JGA-Research-Pack/data/all-answers.json')['answers'];by={x['id']:x for x in answers};idx={x['id']:x for x in rd(W/'sites/jgafinalcode/dist/data/answer-index.json')}
ck(bridge['selected_questions']==3 and bridge['selected_saved_records']==24 and bridge['semantic_rereads']==3,'prior bridge three selected questions and24records with3semantic rereads')
ck(bridge['no_model_reruns'] and not bridge['recommendation_counts_reused'] and not bridge['new_participant_evidence'],'prior bridge not demand, model rerun or fieldwork')
for q in bridge['questions']:
 ck(hashlib.sha256(q['prompt'].encode()).hexdigest()==q['prompt_sha256'],'exact selected prompt hash '+q['question_id'])
 ck(len(q['answer_links'])==8 and {x['product'] for x in q['answer_links']}=={'ChatGPT','Claude','Gemini','Perplexity'},'four models two repeats '+q['question_id'])
 for x in q['answer_links']:
  a=by[x['answer_id']];z=idx[x['answer_id']]
  ck(a['prompt']==q['prompt'] and a['fullAnswer']==z['fullAnswer'],'original/full index exact '+x['answer_id'])
  ck(hashlib.sha256(a['fullAnswer'].encode()).hexdigest()==x['full_answer_sha256'],'independent answer text hash '+x['answer_id'])
  ck(a['dateUtc']==x['observed_at_utc'] and a['sourceStatus']==x['source_status'],'original date/source record status preserved '+x['answer_id'])
for x in rd(R/'08-qa/T01-second-check-baseline.json')['files']:ck(h(R/x['path'])==x['sha256'],'prior/core/first-pass file preserved '+x['path'])
for p in ['05-analysis/observations.json','05-analysis/charts.json','04-table/financial-inputs.json']:ck(rd(R/p)['records']==[],'unperformed array blank '+p)
q=rd(R/'01-method/question-map.json');ck(len(q['records'])==14 and q==rd(R/'01-method/question-map-v0.2.json'),'fourteen core questions unchanged')
for ident,status in [('CLM-0051','quarantined_conflicting'),('CLM-0052','quarantined_conflicting'),('CLM-0167','hold_numeric_reuse'),('CLM-0168','hold_numeric_reuse'),('CLM-0218','hold_universal_ui_behaviour'),('CLM-0392','hold_numeric_reuse')]:ck(cid[ident]['status']==status,'existing hold preserved '+ident)
result=dict(date='2026-10-30',status='passed_preliminary_cross_review_integration_pending',scope='Independent review of market, competitors and root authored packs only. History author pack excluded from substantive self-review.',check_count=len(checks),checks=checks,open_substantive_issues=[],followup_integration_focus=['Preserve promised free practitioner research; do not manufacture paid use rights.','Meeting mode condition applies only where named Rule adopted.','Hays shell is not substantive raw method evidence.'],direct_primary_recheck='Chatham House official explanation and current FAQ independently reopened; recording/AI/in-room image restrictions and own-attendance disclosure verified. Selected source remains reader-only, not raw.',fieldwork=False,commercial_validation=False)
(O/'preliminary-checks.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n');print(json.dumps({k:v for k,v in result.items() if k not in ['checks']},indent=2))
