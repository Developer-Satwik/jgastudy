from pathlib import Path
from urllib.parse import urlparse
import json,hashlib
ROOT=Path(__file__).resolve().parents[2]
B='04-table/research-notes/t05e-second-check'
def load(p):return json.loads((ROOT/p).read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
checks=[]
def check(ok,msg):
 if not ok:raise AssertionError(msg)
 checks.append({'check':msg,'passed':True})
before={x['original_path']:x for x in load(B+'/before-review/manifest.json')['records']}
for x in before.values():check(sha(ROOT/x['snapshot_path'])==x['sha256'],'Exact before snapshot '+x['original_path'])
protected=load('08-qa/T05E-second-check-baseline.json')['files']
for x in protected:
 p=Path(x['path']);p=p if p.is_absolute()else ROOT/p
 check(sha(p)==x['sha256'],'Protected original '+x['path'])
for f in ['04-table/financial-inputs.json','05-analysis/findings.json']:check(load(f)==load(before[f]['snapshot_path']),'Exact financial/findings preservation '+f)
sources=load('02-evidence/registers/sources.json')['records'];claims=load('02-evidence/registers/claims.json')['records']
oldsrc=load(before['02-evidence/registers/sources.json']['snapshot_path'])['records'];oldclm=load(before['02-evidence/registers/claims.json']['snapshot_path'])['records']
check(len(sources)==263 and len(claims)==537 and len(oldsrc)==256 and len(oldclm)==520,'Exact prior/current source and claim totals')
check(claims[:520]==oldclm,'All520 earlier claims unchanged')
by={x['source_id']:x for x in sources}
for x in oldsrc:
 y=by[x['source_id']]
 check({k:v for k,v in x.items()if k not in ['additional_reviews','related_topic_ids']}=={k:v for k,v in y.items()if k not in ['additional_reviews','related_topic_ids']},'Prior source substance '+x['source_id'])
 check(y.get('additional_reviews',[])[:len(x.get('additional_reviews',[]))]==x.get('additional_reviews',[])and set(x.get('related_topic_ids',[]))<=set(y.get('related_topic_ids',[])),'Prior source append-only review history '+x['source_id'])
for f in ['00-control/changes.json','00-control/decisions.json','02-evidence/registers/searches.json']:
 old=load(before[f]['snapshot_path'])['records'];check(load(f)['records'][:len(old)]==old,'Append-only control history '+f)
m=load('08-qa/T05E-second-check-record-map.json');pack=load(B+'/evidence/source-candidates.json')
check(len(pack['records'])==len(m['source_map'])==14 and len(pack['unadopted'])==1,'Fourteen mapped routes and one discovery-only route')
for c in pack['records']:
 sid=m['source_map'][c['candidate_id']];s=by[sid];check(s['url']==c['url'],'Candidate/canonical URL '+c['candidate_id'])
 if c.get('capture_path'):
  check(sha(ROOT/c['capture_path'])==c['capture_sha256'],'Original retained bytes '+c['candidate_id'])
  if c.get('fresh_network_retrieval')is not False:check(urlparse(c['url']).hostname==urlparse(c['final_url']).hostname,'Publisher final domain '+c['candidate_id'])
 else:check(c['capture_kind']=='browser_reader_paraphrase_not_original'and c['reader_note_path'],'Reader distinguished from original '+c['candidate_id'])
 if not c.get('reuse_source_id'):check(s['t05e_second_source_candidate_id']==c['candidate_id']and s['capture_path']==c.get('capture_path'),'New source provenance '+sid)
 else:check(s['additional_reviews'][-1]['detail']==c,'Canonical reuse metadata '+sid)
check(sum(bool(x.get('capture_path'))for x in sources)==185,'Reader notes not promoted to primary originals')
hist=by[m['source_map']['E2-S07']]
check(hist['source_type']=='historical_primary_venue_guide'and hist['publication_eligibility']=='historical_context_not_current_budget'and hist['candidate_detail']['current_budget_eligible']is False,'Prior excluded menu adopted for history only, not current budget')
claimids={x['claim_id']for x in claims};candidate_claims=load(B+'/evidence/claim-candidates.json')['records']
check(candidate_claims==claims[-17:]and len(m['claim_map'])==17,'Seventeen exact adopted bounded records')
for c in candidate_claims:check(set(c['source_ids'])<=set(by)and c['value']is None and c['support_checked'],'Source scoped non-input claim '+c['claim_id'])
cap=load('08-qa/T05E-second-check-captures.json')
check(len(cap['records'])==29,'Capture inventory scope')
for x in cap['records']:check(sha(ROOT/x['path'])==x['sha256'],'Capture inventory bytes '+x['path'])
check(cap['counts_by_kind']=={'browser_reader_paraphrase_not_original':4,'retained_original_html':8,'parsed_original_text':10,'prior_primary_original_reused':2,'prior_pdf_page_render_reviewed':3,'discovery_shell_not_substantive_evidence':2},'Original/reader/history/discovery kinds reconcile')
component=load('04-table/T05E-second-challenge-map.json');tasks={x['task_id']for x in load(component['first_component_path'])['tasks']}
check(len(component['conditions'])==7 and component['programme_state_coverage_and_obligation_implementation_still_required'],'Seven required programme refinements are recorded')
for c in component['conditions']:check(set(c['workload_ids'])<=tasks and set(c['claim_ids'])<=claimids,'Condition lineage '+c['condition_id'])
check(not component['workbooks_changed']and not component['financial_inputs_changed']and not component['independent_agent_review']and not component['full_financial_model_complete']and not component['current_contract_fee_changed']and component['fourteen_core_questions_unchanged']and component['practitioner_free_full_research_preserved'],'Scope and implementation limits preserved')
check(component['actual_participants']==component['actual_quotes']==component['actual_bookings']==component['external_actions']==[],'No actual fieldwork, quotes, bookings or external action')
app=load(component['cost_applications_path'])
check(app['case_count']==len(app['cases'])==16 and app['formula_caches_reconciled']==64 and app['check_count']==len(app['checks'])==83 and all(x['passed']for x in app['checks']),'Read-only cases and formula cache checks passed')
check(sha(Path(app['source_workbook']))==app['source_workbook_sha256']and sha(ROOT/'04-table/T05-event-cost-map.json')==app['source_component_sha256']and sha(ROOT/'04-table/financial-inputs.json')==app['source_financial_inputs_sha256'],'Application original provenance')
check(all(not x['actual_observation']and not x['new_financial_input']for x in app['cases']),'Constructed examples are not empirical or adopted financial inputs')
caseby={x['case_id']:x for x in app['cases']}
check(caseby['EA02']['result']['fractional_count_result']=='n.a.'and not caseby['EA02']['covered_by_current_workbook'],'Partial actual-work gap explicit')
check(not caseby['EA04']['covered_by_current_workbook']and not caseby['EA08']['covered_by_current_workbook']and not caseby['EA12']['covered_by_current_workbook'],'Coverage, lower menu eligibility and credit/cash implementation gaps explicit')
bridge=load(component['prior_study_bridge_path']);qa=load(B+'/prior-study/bridge-checks.json')
check(len(bridge['questions'])==4 and bridge['linked_saved_answers']==32 and bridge['semantic_rereads']==4 and bridge['model_reruns']==0,'Prior study scope preserved')
for x in bridge['provenance']:check(sha(ROOT.parent.parent/x['path'])==x['sha256'],'Saved study original '+x['role'])
check(qa['check_count']==len(qa['checks'])==132 and all(x['passed']for x in qa['checks']),'132 exact prior-study checks passed')
check(len(load(B+'/comparator-map.json')['records'])==7,'Six comparators and JGA considered separately')
completion=load('08-qa/T05E-completion-check.json')
check(len(completion['artifacts'])==64 and completion['canonical_sources']==256 and completion['canonical_claims']==520,'First event completion remains historical')
for x in completion['artifacts']:
 p=Path(x['path']);p=p if p.is_absolute()else ROOT/before.get(x['path'],{}).get('snapshot_path',x['path'])
 check(sha(p)==x['sha256'],'First event as-of completed artefact '+x['path'])

paths=[p for p in(ROOT/B).rglob('*')if p.is_file()and'before-review'not in str(p)]
paths += [ROOT/p for p in ['04-table/T05E-SECOND-CHECK-READOUT.md','04-table/T05E-PROGRAMME-REFINEMENTS.md','04-table/T05E-second-challenge-map.json','08-qa/T05E-second-check-record-map.json','08-qa/T05E-second-check-captures.json','08-qa/t05e-second-review/cost_applications.py','08-qa/t05e-second-review/validate_second.py']]
reviewed=[{'path':str(p.relative_to(ROOT)),'sha256':sha(p)}for p in sorted(set(paths))]
out={'date':'2026-11-01','status':'passed_same_agent_second_check','check_count':len(checks),'checks':checks,'reviewed_artifacts':reviewed,'independent_agent_review':False,'native_Excel_tested':False,'first_component_preserved':True,'programme_refinements_recorded':True,'full_programme_model_complete':False,'external_actions':0}
p=ROOT/'08-qa/t05e-second-review/verification.json';p.write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'status':out['status'],'checks':len(checks),'reviewed_artifacts':len(reviewed),'protected_files':len(protected)}))
