from pathlib import Path
import json,hashlib,re
ROOT=Path(__file__).resolve().parents[2]
checks=[]
def read(p):return json.loads((ROOT/p).read_text())
def sha(p):return hashlib.sha256((ROOT/p).read_bytes()).hexdigest()
def check(x,label):
 checks.append({'check':label,'passed':bool(x)})
 if not x:raise AssertionError(label)
base=read('08-qa/R08-second-check-baseline.json')['records']
check(len(base)==85,'85 fixed prior/core/client/first-pass baseline records')
for x in base:check(sha(x['path'])==x['sha256'],'Preservation hash: '+x['path'])
snaps=read('03-report/research-notes/r08-second-check/before-review/manifest.json')['records']
check(len(snaps)==8,'Eight first-pass R08 synthesis/application/completion snapshots')
for x in snaps:check(sha(x['snapshot_path'])==x['sha256'],'First-pass snapshot: '+x['original_path'])
oldmap=read(next(x['snapshot_path'] for x in snaps if x['original_path']=='03-report/R08-framework-map.json'))
oldroutes=read(next(x['snapshot_path'] for x in snaps if x['original_path']=='03-report/R08-constructed-walkthroughs.json'))
oldreport=read(next(x['snapshot_path'] for x in snaps if x['original_path']=='03-report/R08-report-integration-map.json'))
raw=read('03-report/research-notes/r08-second-check/before-review/canonical-file-manifest.json')['records'];firstbase={x['path']:x['sha256'] for x in read('08-qa/R08-baseline-manifest.json')['files']}
check(len(raw)==5,'Five shared canonical byte snapshots retained')
for x in raw:
 check(sha(x['snapshot_path'])==x['sha256'],'Canonical snapshot bytes preserved: '+x['original_path'])
 check(x['sha256']==firstbase[x['original_path']],'Canonical first-pass hash reconciles: '+x['original_path'])
old=read('03-report/research-notes/r08-second-check/before-review/canonical-before.json')
ss=read('02-evidence/registers/sources.json')['records'];cc=read('02-evidence/registers/claims.json')['records'];ff=read('05-analysis/findings.json')['records'];sources={x['source_id']:x for x in ss};claims={x['claim_id']:x for x in cc};findings={x['finding_id']:x for x in ff}
check(len(ss)==191 and len(cc)==355 and sum(bool(x.get('capture_path')) for x in ss)==120,'191 canonical sources355 claims120 primary-original captures')
for x in old['sources']['records']:
 a={k:v for k,v in x.items() if k not in ['related_topic_ids','additional_reviews']};b={k:v for k,v in sources[x['source_id']].items() if k not in ['related_topic_ids','additional_reviews']}
 check(a==b,'Prior source identity/capture/method retained: '+x['source_id'])
check(all(claims[x['claim_id']]==x for x in old['claims']['records']),'All338 earlier claims preserved exactly')
check(all(findings[x['finding_id']]==x for x in old['findings']['records']),'All76 earlier findings preserved exactly')
held={'CLM-0051':'quarantined_conflicting','CLM-0052':'quarantined_conflicting','CLM-0167':'hold_numeric_reuse','CLM-0168':'hold_numeric_reuse','CLM-0218':'hold_universal_ui_behaviour','CLM-0392':'hold_numeric_reuse'}
for i,status in held.items():check(claims[i]['status']==status,'Held claim remains excluded: '+i)
q=read('01-method/question-map.json');check(q==read('01-method/question-map-v0.2.json') and len(q['records'])==14,'Exact14-question version0.2 unchanged')
for p in ['05-analysis/observations.json','05-analysis/charts.json','04-table/financial-inputs.json']:check(read(p)['records']==[],'No invented actual input: '+p)
mapping=read('08-qa/R08-second-check-record-map.json');check(mapping['source_map']=={} and mapping['new_source_routes']==0,'No new source route/dataset counted')
check(len(mapping['claim_map'])==17 and set(mapping['claim_map'].values())<=set(claims),'Seventeen bounded additional claim/application records resolve')
for d in ['history','market','competitors','root']:
 for c in read('03-report/research-notes/r08-second-check/'+d+'/claim-candidates.json')['records']:
  x=claims[mapping['claim_map'][c['candidate_id']]]
  check(x['claim_text']==c['claim_text'] and x['locator']==c['locator'],'Candidate exact text/locator mapped: '+c['candidate_id'])
  check(x['value'] is None and x['unit'] is None and x['denominator'] is None,'No numerical estimate adopted: '+c['candidate_id'])
  check(set(x['source_ids'])<=set(sources) and x['publication_status']=='working','Claim references bounded working evidence: '+c['candidate_id'])
for x in read('08-qa/R08-second-check-captures.json')['files']:
 check(sha(x['path'])==x['sha256'],'Source/review capture hash: '+x['path'])
 if 'selected-reader' in x['path'] or x['path'].endswith('.txt'):check(x['kind']=='parsed_or_selected_extract','Text/note is an extract, not original or raw error: '+x['path'])
fw=read('03-report/R08-framework-map.json');v={x['view_id']:x for x in fw['views']};ov={x['view_id']:x for x in oldmap['views']}
check(fw['framework_version']=='0.2' and set(v)=={f'V{i:02}' for i in range(1,7)},'Version0.2 preserves six linked views')
check(not fw['mandatory_sequence'] and not fw['score'] and not fw['validated_predictor'] and not fw['approval_recipe'],'No sequence score validated prediction or approval recipe')
check(fw['partial_brief_allowed'] and fw['no_case_allowed'] and fw['no_disclosure_allowed'] and not fw['all_views_required'],'Partial/no-case/non-disclosure route retained')
check(not fw['confidential_documents_required'] and not fw['personal_names_required'] and not fw['exact_budget_required'] and not fw['missing_owner_or_date_defaults_to_pending'],'No compulsory sensitive data or pending-by-default')
check(fw['requires_WP11_original_coding'] and not fw['complete_final_WP15'] and not fw['participant_validated'],'Original-input/final-use dependency retained')
check(fw['new_mandatory_questions']==0 and fw['core_question_count']==14 and fw['core_question_version']=='0.2','No additional mandatory questions')
check(fw.get('new_canonical_claims_count_basis')=='first_pass_preparatory_synthesis_only' and fw.get('second_challenge_new_canonical_claims')==17,'Zero first-pass canonical count distinguished from17 second-challenge records')
edits={(x['view_id'],x['field']):x for x in fw['second_challenge_view_edits']}
check(set(edits)=={('V02','instruction'),('V04','boundary')},'Only two view-text refinements declared')
for i,x in v.items():
 check(not x['mandatory'] and not x['sequence_required'] and not x['scored'] and not x['validated'],'Optional nonordinal view: '+i)
 for k,a in ov[i].items():
  if (i,k) in edits:
   ed=edits[(i,k)];check(ed['before']==a and ed['after']==x[k] and set(ed['claim_ids'])<=set(claims),'Exact justified view edit: '+i+'/'+k)
  else:check(x[k]==a,'First-pass view field preserved: '+i+'/'+k)
 check(not set(x['claim_ids'])&set(held),'No held value used as positive view support: '+i)
for k in ['blank_scope_template','blank_canvas','blank_decision_brief','states_are_separate','evidence_claims_are_separate','missingness_values','held_claim_ids_not_positive_support']:
 check(fw[k]==oldmap[k],'First-pass reusable structure retained: '+k)
check(all(x is None for x in fw['second_challenge_blank_evidence_qualification'].values()),'New evidence-qualification note remains blank')
check([x['condition_id'] for x in fw['cross_cutting_conditions']]==[f'C{i:02}' for i in range(1,6)],'Five selective conditions retained')
for x in fw['cross_cutting_conditions']:
 check(not x['mandatory'] and not x['scored'] and not x['validated'] and set(x['claim_ids']+x.get('guardrail_claim_ids',[]))<=set(claims),'Bounded optional condition: '+x['condition_id'])
check(fw['additional_mandatory_questions_from_second_challenge']==0 and fw['prior_prompt_scenarios_are_constructed'] and not fw['prior_recommendation_counts_reused'] and not fw['prior_model_reruns'],'Prior-study reuse does not alter questionnaire or demand evidence')
for k in ['participant_observations','actual_case_records','completed_framework_use_tests','causal_effect_estimates','employer_forecasts','chart_data','financial_inputs']:check(fw[k]==[],'No invented empirical output: '+k)
report=read('03-report/R08-report-integration-map.json');check(report==oldreport,'Unapproved report structure/map preserved exactly')
check(report['chapter_count']==8 and report['two_parts_preserved'] and not report['outline_client_approved'] and not report['D01_complete'] and not report['D06_final_complete'],'Two parts/eight chapters remain proposed; finaldeliverables not complete')
qa=read('08-qa/R08-second-routing-walkthrough.json');app=read('03-report/R08-constructed-walkthroughs.json');design=read('03-report/research-notes/r08/route-challenge/constructed-routes.json')
check(qa['status']=='passed_internal_second_constructed_walkthrough' and qa['route_count']==15 and qa['check_count']==197 and all(x['passed'] for x in qa['checks']),'Root197 checks pass15 constructed applications')
check(sha(qa['framework_path'])==qa['framework_sha256_at_walkthrough'] and sha(qa['application_path'])==qa['application_sha256_at_walkthrough'],'Rootwalkthrough hashes match reviewed draft/application')
check(sha(qa['source_design_path'])==qa['source_design_sha256'],'Original ten-route design unchanged')
check(not qa['practitioner_validation'] and qa['actual_participant_cases']==0 and qa['new_questions']==0,'Rootwalkthrough is not practitioner validation')
check(len(app['routes'])==15 and app['route_count']==15 and app['framework_version']=='0.2' and not app['practitioner_validation'],'Fifteen applications all belong to preparatoryv0.2')
by={x['route_id']:x for x in app['routes']}
for original in oldroutes['routes']:
 x=by[original['route_id']]
 check({k:v for k,v in x.items() if k not in ['framework_version','second_challenge_reassessment']}=={k:v for k,v in original.items() if k!='framework_version'},'Original bounded application preserved/reapplied: '+x['route_id'])
 check(x['framework_version']=='0.2' and bool(x['second_challenge_reassessment']),'Reassessment explicitly attributed: '+x['route_id'])
for x in app['routes']:
 i=x['route_id'];check(x['evidence_type']=='constructed_internal_application' and not x['original_practitioner_observation'] and x['actual_employer'] is None and x['participant_id'] is None and x['actual_case_id'] is None,'Constructed not actual employer/case: '+i)
 check(x['as_of_date'] is None and x['event_date'] is None and x['numerical_result'] is None,'No invented real date or numeric output: '+i)
 check(x['executed_against_preparatory_R08_framework'] and x['framework_version']=='0.2' and set(x['view_ids'])<=set(v),'Applied to actual six-viewv0.2: '+i)
 check(set(x['supporting_claim_ids'])<=set(claims) and bool(x['unknowns']) and bool(x['boundary_preserved']) and x['failed_boundary'] is None,'Traceable bounded partial output: '+i)
check(by['R08-T11']['supported_next_action'] is None and 'no reconstruction' in by['R08-T11']['event_time_knowledge'],'T11 no later-knowledge backfill or forcedaction')
check(by['R08-T12']['payment_authority_and_execution'] is None and by['R08-T12']['continuing_duties_performed'] is None and by['R08-T12']['next_period_readiness'] is None,'T12 one report acceptance does not establish payment/continuingrun readiness')
check(all(by['R08-T13'][k] is None for k in ['candidate_specific_assessment','candidate_availability_and_start','executed_engagement','payroll_result']),'T13 firm material not candidate/engagement/outcome proof')
check(by['R08-T14']['independent_verification'] is None and by['R08-T14']['perceived_influence'] is None and by['R08-T14']['accounts_reconciled'] is False,'T14 acceptance remains separate from verification/influence/unresolved accounts')
check(by['R08-T15']['independent_corroboration'] is None and by['R08-T15']['actual_buyer_decision'] is None and by['R08-T15']['supported_next_action'] is None,'T15 repeatedrecommendations and addedassumptions do not establish demand/independentproof')
bridge=read('08-qa/R08-prior-study-bridge-check.json');b=read(bridge['bridge_path'])
check(bridge['status']=='passed' and bridge['check_count']==327 and all(x['passed'] for x in bridge['checks']),'Root327 exact prior-study checks passed')
check(bridge['selected_questions']==4 and bridge['selected_saved_answers']==32 and bridge['no_model_reruns'],'Four constructed prompts32savedtexts with no reruns')
check(sha(bridge['bridge_path'])==bridge['bridge_sha256'],'Rootverified bridge hash unchanged')
check({x['question_id'] for x in b['questions']}=={'S01-C','S02-D','S06-C','S11-C'} and not b['recommendation_counts_reused'] and b['external_actions']==[],'Priorbridge selection/premises/demand boundaries preserved')
check(b['global_source_limitations_preserved']=={'complete':339,'partial':6,'pending':1,'none_present':6},'Original global source-capture limits preserved')
check(b['semantic_review_answer_count']==4 and len(b['semantic_review'])==4,'Four semantic samples distinguished from other integrity-only checks')
for rel in ['03-report/R08-SECOND-CHECK-READOUT.md','03-report/R08-DECISION-FRAMEWORK.md','03-report/R08-DESKTOP-SYNTHESIS.md','03-report/R08-REPORT-INTEGRATION.md','03-report/modules/R08-decision-framework-and-synthesis.md']:
 text=(ROOT/rel).read_text();check(set(re.findall(r'CLM-\d{4}',text))<=set(claims),'Canonicalclaimrefsresolve: '+rel)
check('Final' in (ROOT/'03-report/R08-SECOND-CHECK-READOUT.md').read_text() or 'finalWP15' in (ROOT/'03-report/R08-SECOND-CHECK-READOUT.md').read_text(),'Readout keeps final practitioner dependency explicit')
result={'date':'2026-10-29','status':'passed_for_internal_R08_second_challenge','check_count':len(checks),'checks':checks,'reviewer_authored_no_strands':True,'review_scope':'Independent integrated preparatory desktop/source/preservation review; root327exact saved-study checks and197constructed-route checks are separately attributed. Not original fieldwork, user comprehension, model-advice validation, causality, commercial demand or final publication assurance.','source_sample':['LFB2025 renderedPDF3–4 and Scottish2024/25auditPDF46 visually inspected','Retained fresh CintraSRC0131/0132 currenttext and HMRCchoosepayrollSRC0078','QQEsource0003 original relevant sections; independently reopened primary route','Portfolio0210 and Middlemore0116 primary original web reader independently reopened','Retained HaysProjectServices/Oakleaf/guide methods; Portfolio/JGA/Frazer source-specific reader notes/alias limits','Four exact prompt premises and selected savedChatGPTr1sections inspected; generatedscores/assumptions not adopted'],'framework_version':'0.2','source_records':len(ss),'claim_records':len(cc),'source_records_with_primary_original':sum(bool(x.get('capture_path')) for x in ss),'prior_findings_preserved':76,'final_WP15_complete':False,'new_practitioner_observations':0,'external_actions':[]}
(ROOT/'08-qa/r08-second-review/integration-checks.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='checks'},indent=2))
