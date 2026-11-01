from pathlib import Path
import json,hashlib,re
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'01-method/collection-pack-v0.1'
def read(p):return json.loads((ROOT/p).read_text())
def sha(p):return hashlib.sha256((ROOT/p).read_bytes()).hexdigest()
checks=[]
def check(v,label):
 checks.append(dict(check=label,passed=bool(v)))
 if not v:raise AssertionError(label)
policy=read('01-method/collection-pack-v0.1/COUNT-AND-ROUTING-POLICY.json')
templates=read('01-method/collection-pack-v0.1/RECORD-TEMPLATES.json')
decisions=read('01-method/collection-pack-v0.1/REVIEW-DECISIONS.json')
design=read('01-method/research-notes/wp03/routes/constructed-route-tests.json')
question=read('01-method/question-map.json')
check(question==read('01-method/question-map-v0.2.json') and len(question['records'])==14,'Existing fourteen core questions remain version0.2 unchanged')
check(policy['report_target_min']==6 and policy['report_target_max']==10 and policy['table_event_cap']==4,'Contract contribution and Table scope preserved')
check(policy['table_ideal_mix']=={'buyers':2,'members':2} and policy['mix_is_not_a_fixed_quota'],'Ideal Table mix not silently turned into fixed quota')
check(policy['one_person_reference_across_modes_and_streams'] and policy['new_core_questions']==0,'One stable person reference and no added research questions')
check(not policy['recording_default_enabled'] and not policy['external_AI_transcription_default_enabled'] and policy['written_equivalent_allowed'] and not policy['duration_tested'] and not policy['fixed_duration_promised'],'Notes-only proposal and flexible unvalidated duration/mode explicit')
check(policy['actual_report_contributor_count']==0 and policy['actual_Table_event_count']==0 and policy['actual_records']==[],'Real counters remain zero and records empty')
check(not decisions['collection_ready'] and not decisions['legal_compliance_certified'] and decisions['user_send_permission_reference'] is None,'Pack does not activate collection or certify compliance/sending')
check([x['decision_id'] for x in decisions['release_decisions']]==[f'READY{i:02}' for i in range(1,6)] and all(x['status']=='not_confirmed' and x['resolution'] is None and x['confirmation_reference'] is None for x in decisions['release_decisions']),'Five grouped release decisions remain unresolved rather than inferred approved')
for k in ['actual_tool_selection','actual_restricted_storage','actual_notice_version','actual_lawful_instructions_reference','actual_transfer_arrangement_reference']:
 check(decisions[k] is None,'Actual collection arrangement not invented: '+k)
check(decisions['actual_authorised_access_list']==[],'No authorised-person list invented')
contract=decisions['working_contract']
check(sha(contract['source_path'])==contract['source_sha256'],'Working agreement exact source hash matches')
check('JGA controller' in contract['working_role'] and 'Riseklix processor' in contract['working_role'] and not contract['executed_copy_retrieved'],'Working on-behalf roles retained without claiming executed-copy retrieval')
check(contract['return_or_delete_days']==30 and contract['backup_deletion_days']==90 and 'Completion or termination' in contract['closure_trigger'],'Contract closure trigger and30/90periods retained')
check('prior written authorisation' in contract['tools_rule'] and 'not itself an IDTA' in contract['access_rule'],'Subprocessor authorisation and transfer limits retained')
check(templates['blank_is_not_yes'] and templates['participation_choice_is_not_automatically_GDPR_lawful_basis'],'Participation and processing basis remain distinct; blank choice not yes')
def blank(x):
 if isinstance(x,dict):return all(blank(v) for v in x.values())
 if isinstance(x,list):return len(x)==0
 return x is None
for k in ['restricted_identity_lookup','restricted_permission_record','contribution_note','response_entry','publication_item','restricted_request_or_change_log','blank_analysis_transfer_check','blank_count_record']:
 check(blank(templates[k]),'Template is unpopulated: '+k)
for k in ['actual_participants','actual_permissions','actual_contributions','actual_Table_events','actual_publication_items','actual_rights_or_change_requests','actual_transfer_events']:
 check(templates[k]==[],'Actual collection array remains empty: '+k)
choice=templates['restricted_permission_record']['choices']
check(len(choice)==11 and all(x['answer'] is None for x in choice.values()),'Eleven selective use choices are blank, not preselected or compulsory')
for k in ['recording_if_proposed','exact_quotation_specific_extract','name_and_role_specific_wording','employer_identification_specific_wording','contribution_clarification_recontact','future_research_invitation','future_edition_reuse_if_proposed','Table_exploratory_information']:
 check(k in choice,'Separate relevant permission choice exists: '+k)
check(set(policy['missingness_values'])=={'not_asked','not_answered','not_known','not_applicable','not_measured','not_yet_assessed','prefer_not_to_disclose'},'Route-specific missingness remains distinct')
check(all(not x['executed'] and x['actual_result'] is None for x in design['tests']),'Original eight constructed test designs remain unexecuted design inputs')

# Independent scenarios, not rows in actual participant/contribution registers.
# These manual root applications exercise count/permission interpretation only.
applied=[
 dict(test_id='WP03-T01',report_delta=0,Table_delta=0,route='eligibility_clarification_only',record_note='An introduction/title supplies no verified remit or completed input.',recent_case_established=False,recording_or_named_release_permitted=None),
 dict(test_id='WP03-T02',report_delta=1,Table_delta=0,route='no_recent_case',record_note='Actual permitted usable general input can count for an eligible person; Q007caseposition remains unestablished.',recent_case_established=False,recording_or_named_release_permitted=None),
 dict(test_id='WP03-T03',report_delta=1,Table_delta=0,route='written_plus_interview_same_person',record_note='Separate contribution events/version/mode, one distinct person; no fixed answered-question threshold.',recent_case_established=None,recording_or_named_release_permitted=None),
 dict(test_id='WP03-T04',report_delta=1,Table_delta=1,route='eligible_permitted_report_and_member_overlap',record_note='Actual relevant report input and eligibility/permission present; combined session one Tableevent.',recent_case_established=None,recording_or_named_release_permitted=None),
 dict(test_id='WP03-T05',report_delta=0,Table_delta=1,route='buyer_only',record_note='Commercial buyer conversation not practitioner eligibility, and interest not commitment.',recent_case_established=False,recording_or_named_release_permitted=None),
 dict(test_id='WP03-T06',report_delta=1,Table_delta=0,route='older_context_declined_case_detail',record_note='Permitted general input can count, older context separate and declined detail not pursued.',recent_case_established=False,recording_or_named_release_permitted=None),
 dict(test_id='WP03-T07',report_delta=1,Table_delta=0,route='permitted_analysis_notes_only',record_note='Eligible usable analysis input; recording, named/employer release and recontact declined.',recent_case_established=None,recording_or_named_release_permitted=False),
 dict(test_id='WP03-T08',report_delta=1,Table_delta=2,route='qualifying_pilot_and_two_Table_events',record_note='Actual usable permissioned comparable pilot can count once; two substantive Table events remain two.',recent_case_established=None,recording_or_named_release_permitted=None),
]
for a in applied:
 d=next(x for x in design['tests'] if x['test_id']==a['test_id'])
 a.update(evidence_type='root_manual_constructed_application',supplied_premises=d['supplied_premises'],actual_participant=None,actual_contribution=None,actual_permission=None,actual_result=None,count_deltas_are_synthetic=True,applied_to_pack_version='0.1',practitioner_testing=False)
 check(a['report_delta']==d['expected_report_people_count_delta'] and a['Table_delta']==d['expected_Table_event_count_delta'],a['test_id']+': report-person and Table-event deltas match supplied scenario')
 check(bool(a['record_note']) and a['actual_participant'] is None and a['actual_result'] is None and a['count_deltas_are_synthetic'],a['test_id']+': bounded manual application not actual collection')
check(applied[0]['report_delta']==0 and applied[4]['report_delta']==0,'Introductions and buyer titles not counted as practitioners')
check(applied[1]['recent_case_established'] is False and applied[5]['recent_case_established'] is False,'No-case/older route does not invent a recent-case decision')
check(applied[2]['report_delta']==1 and applied[3]['Table_delta']==1 and applied[7]['Table_delta']==2,'Cross-mode/role person and Table-event units remain separate')
check(applied[6]['recording_or_named_release_permitted'] is False and applied[6]['report_delta']==1,'Declined recording/naming does not erase valid permitted analysis contribution')
gate_cases=[dict(test_id='WP03-G01',premise='Tools/access/notice not confirmed in actual pack.',permitted_result='Preparation only; do not activate collection or transmit participant data.',actual_gate_open=False),dict(test_id='WP03-G02',premise='Analysis permission is supplied in a hypothetical account; named quotation/future reuse is not.',permitted_result='Keep unapproved output uses unreleased; no blanket permission.',actual_gate_open=False),dict(test_id='WP03-G03',premise='A hypothetical account removes a name but retains recognisable contextual details.',permitted_result='Do not call it anonymous or automatically approve transfer/publication; assess actual approved route/context.',actual_gate_open=False)]
for x in gate_cases:check(not x['actual_gate_open'] and bool(x['permitted_result']),x['test_id']+': preparation/permission/identification boundary retained')
messages=(BASE/'INTRODUCTION-DRAFTS.md').read_text()
for part in ['## Coordination email to Nick','## Later practitioner invitation']:
 body=messages.split(part,1)[1].split('\n## ',1)[0]
 check('—' not in body and '*' not in body,'External draft has no emdash/asterisk: '+part)
check('linked context may still identify it' in (BASE/'PERMISSION-CHOICES.md').read_text(),'Naming permission and indirect employer identification not conflated')
for f in BASE.glob('*.md'):
 for target in re.findall(r'\]\(([^)]+)\)',f.read_text()):
  if target.startswith(('http://','https://','#')):continue
  check((f.parent/target.split('#')[0]).resolve().exists(),'Local pack link resolves: '+target)
for x in read('08-qa/WP03-baseline-manifest.json')['files']:
 check(sha(x['path'])==x['sha256'],'Prior/core/client/canonical preservation: '+x['path'])
for p in ['05-analysis/observations.json','05-analysis/charts.json','04-table/financial-inputs.json']:
 check(read(p)['records']==[],'No unperformed fieldwork/data input: '+p)
result=dict(date='2026-10-29',status='passed_internal_WP03_pack_walkthrough_not_fieldwork',check_count=len(checks),checks=checks,constructed_count_route_applications=applied,constructed_release_gate_applications=gate_cases,source_design_path='01-method/research-notes/wp03/routes/constructed-route-tests.json',source_design_sha256=sha('01-method/research-notes/wp03/routes/constructed-route-tests.json'),pack_version='0.1',pack_structured_hashes=[dict(path=str(p.relative_to(ROOT)),sha256=sha(p)) for p in BASE.glob('*.json')],method='Root manual operational applications to eight supplied constructed scenarios plus three release/permission cases, with structural/contract/preservation checks. Not participant testing, real counts, actual permissions or legal/tool-security certification.',actual_participants=0,actual_Table_events=0,collection_ready=False,practitioner_testing=False,external_actions=[])
(ROOT/'08-qa/WP03-routing-permission-checks.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ['checks','constructed_count_route_applications','constructed_release_gate_applications','pack_structured_hashes']},indent=2))
