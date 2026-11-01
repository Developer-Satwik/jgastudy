from pathlib import Path
import json,hashlib
ROOT=Path(__file__).resolve().parents[1]
def read(p):return json.loads((ROOT/p).read_text())
def sha(p):return hashlib.sha256((ROOT/p).read_bytes()).hexdigest()
checks=[]
def check(value,label):
 checks.append(dict(check=label,passed=bool(value)))
 if not value:raise AssertionError(label)
framework=read('03-report/R08-framework-map.json')
applications=read('03-report/R08-constructed-walkthroughs.json')
design=read('03-report/research-notes/r08/route-challenge/constructed-routes.json')
claims={x['claim_id']:x for x in read('02-evidence/registers/claims.json')['records']}
findings={x['finding_id']:x for x in read('05-analysis/findings.json')['records']}
sources={x['source_id']:x for x in read('02-evidence/registers/sources.json')['records']}
questionids={x['question_id'] for x in read('01-method/question-map.json')['records']}
views={x['view_id']:x for x in framework['views']}
check(set(views)=={f'V{i:02}' for i in range(1,7)},'Six linked framework views present')
check(framework['views_are_linked_not_stages'] and not framework['mandatory_sequence'] and not framework['score'] and not framework['validated_predictor'] and not framework['approval_recipe'],'Framework is not an approval sequence score or predictive recipe')
check(framework['partial_brief_allowed'] and framework['no_case_allowed'] and framework['no_disclosure_allowed'] and not framework['all_views_required'],'Partial no-case and limited-disclosure routes allowed')
check(not framework['missing_owner_or_date_defaults_to_pending'] and not framework['exact_budget_required'] and not framework['personal_names_required'] and not framework['confidential_documents_required'],'Missing facts do not force status identity or confidential disclosure')
check(framework['requires_WP11_original_coding'] and not framework['complete_final_WP15'] and not framework['participant_validated'],'Final synthesis dependency and no practitioner-validation claim preserved')
check(framework['new_mandatory_questions']==0 and framework['core_question_version']=='0.2' and framework['core_question_count']==14,'Framework adds no questions')
held=set(framework['held_claim_ids_not_positive_support'])
for ident,v in views.items():
 check(not v['mandatory'] and not v['sequence_required'] and not v['scored'] and not v['validated'],f'{ident}: optional nonordinal view')
 check(set(v['claim_ids'])<=set(claims) and not set(v['claim_ids'])&held,f'{ident}: positive claim support resolves without held claims')
 check(set(v['finding_ids'])<=set(findings) and set(v['source_ids'])<=set(sources),f'{ident}: finding/source links resolve')
 check(set(v['existing_question_ids'])<=questionids,f'{ident}: mapped to existing questions')
 check(all(x is None for x in framework['blank_canvas'][ident].values()),f'{ident}: reusable canvas remains blank')
check(set(framework['states_are_separate'])=={'proposal_decision','commitment','implementation','benefit_assessment'},'Decision commitment delivery and benefit fields distinct')
check(len(framework['evidence_claims_are_separate'])==5 and {'evidence_acceptance_if_known','perceived_influence_and_basis'}<=set(views['V04']['selective_record_fields']),'Requested supplied accepted perceived influential and established effect remain distinct')
check(set(framework['missingness_values'])=={'not_known','not_measured','not_applicable','not_disclosed'},'Missingness categories remain distinct')
check(all(x is None for x in framework['blank_scope_template'].values()) and all(x is None for x in framework['blank_decision_brief'].values()),'Scope and decision-brief templates remain blank')
check(len(applications['routes'])==applications['route_count']==15 and design['route_count']==10,'Ten original route designs reapplied plus five additional constructed challenges')
check(not applications['practitioner_validation'] and applications['actual_case_records']==[] and applications['numerical_results']==[],'Constructed applications not counted as fieldwork or numerical results')
check(all(not r['executed_against_final_R08_framework'] for r in design['routes']),'Original design record not retroactively changed to an executed validation')
by={x['route_id']:x for x in applications['routes']}
for r in applications['routes']:
 ident=r['route_id'];d=next((x for x in design['routes'] if x['route_id']==ident),r)
 check(r['supplied_premises']==d['supplied_premises'],f'{ident}: exact supplied constructed premises retained')
 check(r['executed_against_preparatory_R08_framework'] and r['framework_version']==framework['framework_version'],f'{ident}: application is to current preparatory framework')
 check(r['evidence_type']=='constructed_internal_application' and not r['original_practitioner_observation'] and r['actual_employer'] is None and r['participant_id'] is None and r['actual_case_id'] is None,f'{ident}: constructed provenance explicit')
 check(r['numerical_result'] is None and r['as_of_date'] is None and r['event_date'] is None,f'{ident}: no invented real date or numerical result')
 check(set(r['view_ids'])<=set(views) and bool(r['view_ids']),f'{ident}: application uses actual framework views')
 check(r['supporting_claim_ids']==d['supporting_claim_ids'] and set(r['supporting_claim_ids'])<=set(claims),f'{ident}: source-design claim links preserved')
 check(bool(r['recorded_position']) and bool(r['unknowns']) and bool(r['boundary_preserved']),f'{ident}: usable partial record and explicit remaining gap')
 check(r['failed_boundary'] is None,f'{ident}: root manual application reports no violated boundary')
check(by['R08-T01']['case_route']=='adequate_current_no_new_case' and by['R08-T01']['proposal_decision'] is None and by['R08-T01']['supported_next_action'] is None,'Adequate-current route does not manufacture proposal or next action')
check(by['R08-T02']['case_route']=='pre_proposal_need' and by['R08-T02']['proposal_decision'] is None and by['R08-T02']['selected_response'] is None,'Never-raised need is not pending declined deferred or preselected solution')
check(by['R08-T03']['broader_authority'] is None and by['R08-T03']['implementation'] is None and by['R08-T03']['benefit_assessment'] is None,'Scoped no-formal-approval route does not imply wider authority operation or benefit')
check(by['R08-T04']['later_phase_resources'] is None and by['R08-T04']['release_condition_clearance'] is None and by['R08-T04']['implementation'] is None,'Initial phase approval/resources do not complete release or later-phase support')
check(by['R08-T05']['case_route']=='explicit_limited_renewal' and by['R08-T05']['benefit_assessment'] is None,'Limited renewal retains actual rationale without satisfaction or outcome inference')
check(by['R08-T06']['case_route']=='retained_platform_changed_route' and by['R08-T06']['commitment'] is None and by['R08-T06']['implementation'] is None,'Retained platform and changed route coexist without contract/service inference')
check('no new decision event' in by['R08-T07']['proposal_decision'] and 'later operation unknown' in by['R08-T07']['implementation'],'Postponed rollout preserves earlier authorisation without inferred investment deferral or elapsed-date outcome')
check(by['R08-T08']['proposal_decision']=='Explicit stop of this component only.' and by['R08-T08']['selected_response'] is None,'Component stop does not abandon whole need or select a replacement')
check(by['R08-T09']['proposal_decision'] is None and by['R08-T09']['implementation'] is None and by['R08-T09']['resource_basis'] is None,'Feature interest and future promise do not establish purchase configuration or funding')
check(by['R08-T10']['resource_missingness']=='not_disclosed' and by['R08-T10']['applicability_missingness']=='not_known' and by['R08-T10']['supported_next_action'] is None and by['R08-T10']['owner'] is None,'Limited-disclosure route preserves distinct missingness without forced action or owner')
check(framework['framework_version']=='0.2','Second challenge uses framework version0.2')
check([x['condition_id'] for x in framework['cross_cutting_conditions']]==[f'C{i:02}' for i in range(1,6)],'Five optional second-challenge conditions present')
for c in framework['cross_cutting_conditions']:
 check(not c['mandatory'] and not c['scored'] and not c['validated'] and set(c['claim_ids'])<=set(claims),'Selective linked condition: '+c['condition_id'])
check(all(x is None for x in framework['second_challenge_blank_evidence_qualification'].values()),'Evidence qualification note remains blank/selective')
check(framework['additional_mandatory_questions_from_second_challenge']==0 and not framework['prior_model_reruns'] and not framework['prior_recommendation_counts_reused'],'Second challenge adds no questions or recommendation/rerun transfer')
check(by['R08-T11']['event_time_knowledge'].startswith('Only the earlier') and by['R08-T11']['supported_next_action'] is None,'Historical route does not backfill later knowledge or force a next action')
check(by['R08-T12']['payment_authority_and_execution'] is None and by['R08-T12']['next_period_readiness'] is None and by['R08-T12']['continuing_duties_performed'] is None,'Recurring report acceptance does not complete payment/continuity')
check(by['R08-T13']['candidate_specific_assessment'] is None and by['R08-T13']['candidate_availability_and_start'] is None and by['R08-T13']['executed_engagement'] is None and by['R08-T13']['payroll_result'] is None,'Firm material not promoted to candidate/engagement/payroll proof')
check(by['R08-T14']['independent_verification'] is None and by['R08-T14']['perceived_influence'] is None and not by['R08-T14']['accounts_reconciled'],'Accepted evidence and divergent accounts retain unresolved qualification')
check(by['R08-T15']['independent_corroboration'] is None and by['R08-T15']['actual_buyer_decision'] is None and by['R08-T15']['supported_next_action'] is None,'Repeated recommendations and added assumptions not independent proof or buyer facts')
snap=read('03-report/research-notes/r08-second-check/before-review/manifest.json')['records']
old=read(next(x['snapshot_path'] for x in snap if x['original_path']=='03-report/R08-constructed-walkthroughs.json'))
for r in old['routes']:
 now=by[r['route_id']]
 check({k:v for k,v in now.items() if k not in ['framework_version','second_challenge_reassessment']}=={k:v for k,v in r.items() if k not in ['framework_version','second_challenge_reassessment']},'Original bounded application preserved on reapplication: '+r['route_id'])
result=dict(date='2026-10-29',status='passed_internal_second_constructed_walkthrough',framework_version=framework['framework_version'],route_count=15,check_count=len(checks),checks=checks,method='Root-authored manual analytical application to supplied constructed premises, checked for linkage and explicit boundary preservation. Reapplied to version0.2 with five added challenges; no executable decision engine, human-user test, predictive validation or empirical effect is claimed.',practitioner_validation=False,actual_participant_cases=0,new_questions=0,source_design_path='03-report/research-notes/r08/route-challenge/constructed-routes.json',source_design_sha256=sha('03-report/research-notes/r08/route-challenge/constructed-routes.json'),framework_path='03-report/R08-framework-map.json',framework_sha256_at_walkthrough=sha('03-report/R08-framework-map.json'),application_path='03-report/R08-constructed-walkthroughs.json',application_sha256_at_walkthrough=sha('03-report/R08-constructed-walkthroughs.json'),external_actions=[])
(ROOT/'08-qa/R08-second-routing-walkthrough.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='checks'},indent=2))
