from pathlib import Path
import hashlib,json,re
R=Path(__file__).resolve().parents[2]
P=R/'01-method/collection-pack-v0.1'
checks=[]
def read(p):return json.loads((R/p).read_text())
def check(value,label):
 checks.append({'check':label,'passed':bool(value)})
 if not value:raise AssertionError(label)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
for x in read('08-qa/WP03-baseline-manifest.json')['files']:
 check(sha(R/x['path'])==x['sha256'],'Preserved baseline '+x['path'])
q=read('01-method/question-map.json')
check(q==read('01-method/question-map-v0.2.json') and len(q['records'])==14,'Canonical14-question guide unchanged')
for f in ['05-analysis/observations.json','05-analysis/charts.json','04-table/financial-inputs.json']:
 check(read(f)['records']==[],'Unperformed actual research empty: '+f)
for f in ['START-HERE.md','OPERATOR-RUNBOOK.md','INTRODUCTION-DRAFTS.md','PARTICIPANT-INFORMATION-DRAFT.md','PERMISSION-CHOICES.md','COUNT-AND-ROUTING-POLICY.json','REVIEW-DECISIONS.json','RECORD-TEMPLATES.json']:
 check((P/f).is_file(),'Integrated pack file '+f)
policy=json.loads((P/'COUNT-AND-ROUTING-POLICY.json').read_text())
decisions=json.loads((P/'REVIEW-DECISIONS.json').read_text())
templates=json.loads((P/'RECORD-TEMPLATES.json').read_text())
check((policy['report_target_min'],policy['report_target_max'],policy['table_event_cap'])==(6,10,4),'Report target andTable cap preserved')
check(policy['table_ideal_mix']=={'buyers':2,'members':2} and policy['mix_is_not_a_fixed_quota'],'Tableideal2buyers2members without statistical quota')
check(policy['one_person_reference_across_modes_and_streams'] and policy['written_equivalent_allowed'],'Unique person across modes/streams andwrittenroute preserved')
check(policy['core_question_version']=='0.2' and policy['report_core_questions']==14 and policy['new_core_questions']==0,'No extra questionnaire introduced')
check(policy['extra_optional_framework_fields_are_not_compulsory_probes'],'Framework detail not cumulative required probes')
check(not policy['recording_default_enabled'] and not policy['external_AI_transcription_default_enabled'],'Proposed default no recording/externalAI')
check(not policy['duration_tested'] and not policy['fixed_duration_promised'],'Untestedduration not claimed validated or fixed')
check(policy['actual_report_contributor_count']==0 and policy['actual_Table_event_count']==0 and policy['actual_records']==[] and policy['external_actions']==[],'No actual counts/data/actions inpolicy')
routes={x['route_id']:x for x in policy['routes']}
check(set(routes)=={'recent_case','pre_proposal','no_recent_case','older_or_uncertain_context','declined_detail','written','table_buyer','table_member'},'All intended routes exist')
for key in ['pre_proposal','no_recent_case','older_or_uncertain_context']:
 check(not any(x in routes[key]['existing_question_ids'] for x in [f'Q{i:03}' for i in range(7,14)]),'No-case route doesnotforcecasequestions: '+key)
check(routes['declined_detail']['existing_question_ids']==[],'Declineddetail stopsroute request')
check(routes['table_buyer']['existing_question_ids']==[f'B{i:02}' for i in range(1,7)] and routes['table_member']['existing_question_ids']==[f'M{i:02}' for i in range(1,7)],'SeparateTableguidesnot practitioner replacement')
contract=decisions['working_contract'];agreement=Path(contract['source_path']).read_text()
check(sha(Path(contract['source_path']))==contract['source_sha256'],'Working agreement exactsourcehash')
check('JGA is controller and the Provider is processor' in agreement and 'JGA controller and Riseklix processor' in contract['working_role'],'Onbehalfcontrollerprocessorcontract baseline accurate')
check(contract['return_or_delete_days']==30 and contract['backup_deletion_days']==90 and 'At JGA' in agreement and 'completion or termination' in contract['closure_trigger'].lower(),'Contract30/90trigger/choice not invented')
check('own business-contact' in contract['working_role'] and 'materially different' in contract['role_change_rule'],'Ownbusinessrecords andmateriallydifferentrole distinction')
check('prior written authorisation' in contract['tools_rule'] and 'not itself an IDTA' in contract['access_rule'],'Tools andrequiredtransfer route not autoapproved')
check(not contract['executed_copy_retrieved'] and not contract['legal_compliance_certified'],'Executedcopy andlegalapproval not inferred')
check(len(decisions['release_decisions'])==5 and all(x['status']=='not_confirmed' and x['resolution'] is None and x['confirmation_reference'] is None for x in decisions['release_decisions']),'Five actualreleasereviewdecisions remain unresolved')
check(decisions['collection_ready'] is False and decisions['actual_tool_selection'] is None and decisions['actual_restricted_storage'] is None and decisions['actual_notice_version'] is None and decisions['actual_lawful_instructions_reference'] is None and decisions['actual_transfer_arrangement_reference'] is None and decisions['user_send_permission_reference'] is None,'No activated tool notice transfer basis orsend permission')
check(decisions['actual_authorised_access_list']==[] and decisions['external_actions']==[],'No actual accesslist/actions')
check('incident' in decisions['release_decisions'][2]['needed_before_use'].lower(),'Actual request/incident escalationroute explicit')
check(templates['all_templates_are_blank'] and templates['blank_is_not_yes'] and templates['participation_choice_is_not_automatically_GDPR_lawful_basis'],'Blankpermissiontemplates notyes or automaticlawfulbasis')
def leaves(obj):
 if isinstance(obj,dict):
  for v in obj.values():yield from leaves(v)
 elif isinstance(obj,list):
  for v in obj:yield from leaves(v)
 else:yield obj
for k in ['restricted_identity_lookup','restricted_permission_record','contribution_note','response_entry','publication_item','restricted_request_or_change_log','blank_analysis_transfer_check','blank_count_record']:
 check(all(v is None for v in leaves(templates[k])),'Blanktemplatevalues only: '+k)
choices=templates['restricted_permission_record']['choices']
check(len(choices)==11 and all(v['answer'] is None for v in choices.values()),'Elevenseparate optional choices withno answers preselected')
check({'participation_and_notes_or_written_response','deidentified_report_publication_scope','recording_if_proposed','exact_quotation_specific_extract','name_and_role_specific_wording','employer_identification_specific_wording','council_recognition','contribution_clarification_recontact','future_research_invitation','future_edition_reuse_if_proposed','Table_exploratory_information'}==set(choices),'Participation/recording/quote/person/employer/future/Table choices distinct')
for k,v in templates.items():
 if k.startswith('actual_'):check(v==[],'No actualtemplate records: '+k)
runbook=(P/'OPERATOR-RUNBOOK.md').read_text();info=(P/'PARTICIPANT-INFORMATION-DRAFT.md').read_text();intro=(P/'INTRODUCTION-DRAFTS.md').read_text();permissions=(P/'PERMISSION-CHOICES.md').read_text();start=(P/'START-HERE.md').read_text()
for label,value in [
 ('No-case andwrittenusablewithoutallprobes','Useful operating/priorities input remains valid' in runbook and 'Do not require every probe' in runbook),
 ('Counts reflect actual input, nottitle orintroduction','title/introduction alone' in runbook and 'actual usable permitted report input' in runbook),
 ('Repeat substantiveTableevents nothidden','Repeat substantive Table sessions still consume events' in runbook),
 ('Declinedrecordingnotblocknotesroute','It is optional; we can use notes instead' in permissions),
 ('No absoluteanonymity or automaticidentitylicence','removing a name does not always prevent recognition' in info and 'No sale of participant contact/identity records' in runbook),
 ('Employerpermission correction resolved','does not automatically authorise naming their employer; linked context may still identify it' in permissions),
 ('No new retentionclock or unlimitedrecall','Do not start a new retention clock' in runbook and 'no invented cutoff or blanket promise' in runbook),
 ('Separateactualnotice notfalsefinal','Incomplete notice, for review only' in info and 'must not be sent alone' in info),
 ('Commercialpublication scope explained','commercial licensing' in info and 'specific research uses explained to you' in info),
 ('Tableandpurchasecommitmentnotimplied','does not enrol you in The Table' in info and 'give sponsors access to you' in info),
 ('Introductionsdo not request data now','please keep identifiable contact details and responses with JGA' in intro),
 ('No transferworkaroundbyname removal','removing names or using participant IDs alone does not make material anonymous' in start),
 ('Ordinaryworkspace notapprovedstorage','No identifiable or confidential contribution belongs in this workspace' in start),
 ('Unexpecteddata notcopied or falselydeleted','do not copy it into this workspace' in runbook and 'do not claim remote copies were removed' in runbook),
 ('No incentives or spendingcreated','No incentive, venue, subscription' in runbook),
]:check(value,label)
core=info.split('## Short purpose and choice information',1)[1].split('## Information to complete',1)[0].strip()
check(150<=len(core.split())<=230,'Participantcore remains concise')
check('—' not in intro and '*' not in intro,'Externalmessage drafts avoidemdash/asterisks')
for x in read('01-method/research-notes/wp03/data/capture-manifest.json')['records']:
 check(sha(R/x['path'])==x['sha256'],'Data source original hash: '+x['review_id'])
 check(sha(R/x['text_path'])==x['text_sha256'],'Data source parsed-text hash: '+x['review_id'])
data_note=(R/'01-method/research-notes/wp03/data/DATA-ARRANGEMENT-DECISIONS.md').read_text()
check('legacy EU/European-Commission wording' in data_note and 'landing page' in data_note and 'linked full PDF was not inspected' in data_note,'Sourceversion andMRSlandingonlylimits retained')
qa=read('08-qa/WP03-routing-permission-checks.json');design=read(qa['source_design_path'])
check(qa['status']=='passed_internal_WP03_pack_walkthrough_not_fieldwork' and qa['check_count']==199 and all(x['passed'] for x in qa['checks']),'Root199packchecks passed withboundedmethod')
check(sha(R/qa['source_design_path'])==qa['source_design_sha256'],'Rootapplied exactunchangedtestdesign')
for x in qa['pack_structured_hashes']:check(sha(R/x['path'])==x['sha256'],'Actualstructuredpack matchesrootapplications: '+x['path'])
check(len(qa['constructed_count_route_applications'])==8 and len(qa['constructed_release_gate_applications'])==3,'Eight count/routes andthree releasecases actuallyapplied')
expected=[(0,0),(1,0),(1,0),(1,1),(0,1),(1,0),(1,0),(1,2)]
for a,d,(rp,tp) in zip(qa['constructed_count_route_applications'],design['tests'],expected):
 check(a['test_id']==d['test_id'] and a['supplied_premises']==d['supplied_premises'],'Exactsuppliedpremises: '+a['test_id'])
 check((a['report_delta'],a['Table_delta'])==(rp,tp),'Independentmanualcount interpretation: '+a['test_id'])
 check(a['evidence_type']=='root_manual_constructed_application' and a['count_deltas_are_synthetic'] and a['actual_participant'] is None and a['actual_permission'] is None and a['actual_result'] is None and not a['practitioner_testing'],'Constructedcountnot actualinput: '+a['test_id'])
check(all(not x['executed'] for x in design['tests']),'Originaldesign notretroactively markedexecuted')
check(qa['actual_participants']==0 and qa['actual_Table_events']==0 and not qa['collection_ready'] and not qa['practitioner_testing'] and qa['external_actions']==[],'AppliedQA doesnotactivatecollection or inventrealcounts')
check(all(not x['actual_gate_open'] for x in qa['constructed_release_gate_applications']),'Actualreleasegatesremainclosedinallsyntheticexamples')
for f in P.glob('*.md'):
 for target in re.findall(r'\]\(([^)]+)\)',f.read_text()):
  if not target.startswith(('https://','http://','#')):check((f.parent/target).resolve().exists(),'Packlocallink resolves: '+f.name+' '+target)
result={'date':'2026-10-29','status':'passed_for_internal_WP03_collection_pack_preparation','check_count':len(checks),'checks':checks,'scope':'Independent integrated operational/contract/source-scope review and preservation checks. Reviewer did not author the pack or root count applications. Not legal certification, tool-security audit, approved storage/access/transfer, actual participant testing or activated fieldwork.','correction_resolved':'Employer identification wording now distinguishes permission to name an employer from possible indirect identification through naming/context.','external_actions':[]}
(R/'08-qa/wp03-review/integration-checks.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='checks'},indent=2))
