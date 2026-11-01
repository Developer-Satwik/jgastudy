"""Same-agent preservation, source lineage and read-only application review."""
from pathlib import Path
from collections import Counter
import hashlib,json

ROOT=Path(__file__).resolve().parents[2]
B='04-table/research-notes/t05c-second-check'
def load(p):return json.loads((ROOT/p).read_text())
def path(p):return Path(p) if Path(p).is_absolute()else ROOT/p
def sha(p):return hashlib.sha256(path(p).read_bytes()).hexdigest()
checks=[]
def check(ok,msg):
    if not ok:raise AssertionError(msg)
    checks.append({'check':msg,'passed':True})
before={x['original_path']:x for x in load(B+'/before-review/manifest.json')['records']}
for x in before.values():check(sha(x['snapshot_path'])==x['sha256'],'Exact before snapshot '+x['original_path'])
baseline=load('08-qa/T05C-second-check-baseline.json')['files']
check(len(baseline)==1994 and len(before)==12,'Exact protected baseline and snapshot count')
for x in baseline:check(sha(x['path'])==x['sha256'],'Protected original '+x['path'])
for p in ['04-table/financial-inputs.json','05-analysis/findings.json']:
    check(load(p)==load(before[p]['snapshot_path']),'Unchanged register '+p)
sources=load('02-evidence/registers/sources.json')['records'];claims=load('02-evidence/registers/claims.json')['records']
oldsrc=load(before['02-evidence/registers/sources.json']['snapshot_path'])['records'];oldclm=load(before['02-evidence/registers/claims.json']['snapshot_path'])['records']
check((len(oldsrc),len(oldclm),len(sources),len(claims))==(266,545,273,563),'Exact before/current canonical totals')
check(claims[:545]==oldclm,'All545 prior claims unchanged')
by={s['source_id']:s for s in sources}
for x in oldsrc:
    y=by[x['source_id']]
    check({k:v for k,v in x.items()if k not in ['additional_reviews','related_topic_ids']}=={k:v for k,v in y.items()if k not in ['additional_reviews','related_topic_ids']},'Preserved source substance '+x['source_id'])
    check(y.get('additional_reviews',[])[:len(x.get('additional_reviews',[]))]==x.get('additional_reviews',[])and set(x.get('related_topic_ids',[]))<=set(y.get('related_topic_ids',[])),'Append-only source review history '+x['source_id'])
for p in ['00-control/changes.json','00-control/decisions.json','02-evidence/registers/searches.json']:
    old=load(before[p]['snapshot_path'])['records'];now=load(p)['records']
    check(len(now)==len(old)+1 and now[:-1]==old,'Append-only control history '+p)
m=load('08-qa/T05C-second-check-record-map.json');pack=load(B+'/evidence/source-candidates.json')['records']
check(len(pack)==len(m['source_map'])==18 and m['new_source_routes']==7 and m['reused_source_routes']==11,'Seven new and eleven reused source routes')
for x in pack:
    s=by[m['source_map'][x['candidate_id']]]
    check(s['url']==x['url'],'Candidate/canonical URL '+x['candidate_id'])
    if x.get('canonical_reuse'):
        check(s['additional_reviews'][-1]['detail']==x,'Exact reuse history '+x['candidate_id'])
    else:
        check(s['t05c_second_source_candidate_id']==x['candidate_id']and s['capture_path']==x.get('capture_path'),'New source provenance '+x['candidate_id'])
    if x.get('capture_path'):check(sha(x['capture_path'])==x['capture_sha256'],'Retained original hash '+x['candidate_id'])
    if x.get('reader_note_path'):check(sha(x['reader_note_path'])==x['reader_note_sha256']and x['capture_path']is None,'Reader paraphrase not an original '+x['candidate_id'])
check(sum(bool(s.get('capture_path'))for s in sources)==192,'192 sources with primary originals; reader notes excluded')
cap=load('08-qa/T05C-second-check-captures.json')
check(len(cap['records'])==24 and cap['counts_by_kind']=={'retained_original_html':8,'parsed_original_text':9,'retained_original_pdf':1,'browser_reader_paraphrase_not_original':2,'prior_source_context_reinspected':4},'Capture inventory exact kinds')
for x in cap['records']:check(sha(x['path'])==x['sha256'],'Capture inventory hash '+x['path'])
cc=load(B+'/evidence/claim-candidates.json')['records']
check(cc==claims[-18:] and len(m['claim_map'])==18,'Eighteen exact bounded claim records')
for x in cc:
    check(set(x['source_ids'])<=set(by)and x['support_checked']and x['value']is None,'Bounded non-input claim '+x['claim_id'])
check(by[m['source_map']['CS-S01']]['sample_size']==300 and by[m['source_map']['CS-S02']]['sample_size']==1455,'Distinct survey scopes and denominators retained')
c=load('04-table/T05C-second-challenge-map.json')
check(len(c['conditions'])==8 and c['programme_integration_still_required'],'Eight explicit integration requirements')
for x in c['conditions']:check(set(x['claim_ids'])<={z['claim_id']for z in claims},'Condition lineage '+x['condition_id'])
check(not c['arithmetic_error_identified_in_defined_cash_unit']and len(c['presentation_or_integration_limits_identified'])==3,'Defined arithmetic and identified scope limits distinguished')
check(not c['original_four_workbooks_changed']and not c['financial_inputs_changed']and not c['full_financial_model_complete']and not c['current_contract_fee_changed']and c['fourteen_core_questions_unchanged']and c['practitioner_free_full_research_preserved']and not c['independent_agent_review'],'Scope, workbooks, financial assumptions and review independence preserved')
check(c['actual_participants']==c['actual_quotes']==c['actual_bookings']==c['external_actions']==[],'No actual external fieldwork or action')
check(len(load(B+'/comparator-map.json')['records'])==7 and load(B+'/business-model-check.json')['model_count']==6,'Six recruiter comparisons plus JGA and six distinct commercial mechanisms')
app=load(c['cash_applications_path'])
check(app['case_count']==len(app['cases'])==18 and app['check_count']==len(app['checks'])==173 and all(x['passed']for x in app['checks']),'Eighteen read-only applications and173 checks passed')
check(app['formula_caches_reconciled']==150 and app['new_workbook_engine_tests']==0 and not app['original_workbook_edited']and not app['native_Excel_tested'],'150 cached defaults inspected; no new workbook-engine or native Excel test claimed')
check(sha(app['source_workbook'])==app['source_workbook_sha256']and sha('04-table/T05-cash-map.json')==app['source_component_sha256'],'Original cash component provenance')
for x in app['cases']:check(not x['actual_observation']and not x['new_financial_input']and not x['workbook_recalculated_for_this_case']and x['result']==x['expected'],'Constructed example limits '+x['case_id'])
caseby={x['case_id']:x for x in app['cases']}
check(caseby['CA04']['result']['excess_vs_bill']==500.0,'Duplicate transaction overstatement explicitly found')
check(caseby['CA11']['result']=={'opening_date_review_flag':False,'expiry_within_horizon':True},'Upcoming-expiry limitation explicitly found')
check(caseby['CA05']['result']=={'raw_A_closing':0.0,'raw_B_closing':-500.0},'Route filter is separate from incurred-cost baseline')
bridge=load(c['prior_study_bridge_path']);bqa=load(B+'/prior-study/bridge-checks.json')
check(len(bridge['questions'])==4 and bridge['linked_saved_answers']==32 and bridge['semantic_rereads']==4 and bridge['model_reruns']==0,'Four prior questions,32 linked answers and4 full rereads')
for x in bridge['provenance']:check(sha(ROOT.parent.parent/x['path'])==x['sha256'],'Exact saved-study original '+x['role'])
check(bqa['check_count']==len(bqa['checks'])==132 and all(x['passed']for x in bqa['checks']),'132 saved-study linkage checks passed')
prior=load('08-qa/T05C-completion-check.json')
check(len(prior['artifacts'])==54 and prior['canonical_sources']==266 and prior['canonical_claims']==545,'First cash completion retains historical checkpoint')
for x in prior['artifacts']:
    p=before.get(x['path'],{}).get('snapshot_path',x['path'])
    check(sha(p)==x['sha256'],'First cash completion as-of artifact '+x['path'])
firstqa=load('08-qa/t05c-workbook/verification.json')
check(firstqa['check_count']==len(firstqa['tests'])==65 and all(x['passed']for x in firstqa['tests'])and len(firstqa['renders'])==7,'Original65 engine tests/seven visual regions retained')
files=[p for p in (ROOT/B).rglob('*')if p.is_file()and 'before-review'not in str(p)]
files += [ROOT/p for p in ['04-table/T05C-SECOND-CHECK-READOUT.md','04-table/T05C-INTEGRATION-REFINEMENTS.md','04-table/T05C-second-challenge-map.json','08-qa/T05C-second-check-record-map.json','08-qa/T05C-second-check-captures.json','08-qa/build_t05c_second_support.py','08-qa/merge_t05c_second.py','08-qa/t05c-second-review/validate_second.py']]
reviewed=[{'path':str(p.relative_to(ROOT)),'sha256':sha(p)}for p in sorted(set(files))]
out={'date':'2026-11-01','status':'passed_same_agent_second_check','check_count':len(checks),'checks':checks,'reviewed_artifacts':reviewed,'independent_agent_review':False,'native_Excel_tested':False,'first_component_preserved':True,'programme_refinements_recorded':True,'full_programme_model_complete':False,'external_actions':0}
savepath=ROOT/'08-qa/t05c-second-review/verification.json';savepath.write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'status':out['status'],'checks':len(checks),'reviewed_artifacts':len(reviewed),'protected_files':len(baseline)}))
