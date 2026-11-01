from pathlib import Path
import json,hashlib,re,zipfile,xml.etree.ElementTree as ET
from urllib.parse import unquote
ROOT=Path(__file__).resolve().parents[2]
def read(p):return json.loads((ROOT/p).read_text())
def sha(p):return hashlib.sha256((ROOT/p).read_bytes()).hexdigest()
checks=[]
def ck(v,label):
 checks.append(dict(check=label,passed=bool(v)))
 if not v:raise AssertionError(label)
baseline=read('08-qa/R08-baseline-manifest.json')['files']
ck(len(baseline)==76,'76 preserved prior/core/client/register artifacts')
for x in baseline:ck(sha(x['path'])==x['sha256'],'Preserved baseline '+x['path'])
findings=read('05-analysis/findings.json')['records'];prior=read('08-qa/R08-existing-findings.json')['records']
ck(findings==prior and len(findings)==76,'All76 prior internal findings unchanged')
sources=read('02-evidence/registers/sources.json')['records'];claims=read('02-evidence/registers/claims.json')['records']
ck(len(sources)==191 and len(claims)==338 and sum(bool(x.get('capture_path')) for x in sources)==120,'Existing191source338claim120primarycapture totals preserved')
claim={x['claim_id']:x for x in claims};sourceids={x['source_id'] for x in sources};findingids={x['finding_id'] for x in findings}
holds={'CLM-0051':'quarantined_conflicting','CLM-0052':'quarantined_conflicting','CLM-0167':'hold_numeric_reuse','CLM-0168':'hold_numeric_reuse','CLM-0218':'hold_universal_ui_behaviour','CLM-0392':'hold_numeric_reuse'}
for i,status in holds.items():ck(claim[i]['status']==status,'Hold remains '+i)
q=read('01-method/question-map.json');ck(q==read('01-method/question-map-v0.2.json') and len(q['records'])==14,'Fourteen core questions remain v0.2 exact')
qids={x['question_id'] for x in q['records']}
for p in ['05-analysis/observations.json','05-analysis/charts.json','04-table/financial-inputs.json']:ck(read(p)['records']==[],'Unperformed records empty '+p)
model=read('03-report/R08-framework-map.json');views=model['views'];vids={x['view_id'] for x in views}
ck([x['view_id'] for x in views]==[f'V{i:02}' for i in range(1,7)],'Six ordered identifiers for linked optional views')
ck(model['views_are_linked_not_stages'] and not any(model[k] for k in ['mandatory_sequence','score','validated_predictor','approval_recipe','participant_validated','complete_final_WP15','all_views_required']),'No forced stages score approval recipe or final completion')
ck(model['requires_WP11_original_coding'] and model['new_mandatory_questions']==0 and model['core_question_count']==14 and model['core_question_version']=='0.2','Final dependency and unchanged core explicit')
ck(all(model[k] for k in ['partial_brief_allowed','no_case_allowed','no_disclosure_allowed','case_route_not_a_decision_disposition','no_material_gap_is_valid','no_action_or_retention_or_stop_can_be_appropriate']),'Partial no-case adequate-current and no-action routes valid')
ck(not any(model[k] for k in ['confidential_documents_required','personal_names_required','exact_budget_required','missing_owner_or_date_defaults_to_pending']),'No forced private record or pending default')
ck(set(model['missingness_values'])=={'not_known','not_measured','not_applicable','not_disclosed'},'Four missingness categories distinct')
ck(set(model['states_are_separate'])=={'proposal_decision','commitment','implementation','benefit_assessment'},'Decision commitment delivery and benefit distinct')
ck(set(model['evidence_claims_are_separate'])=={'requested','supplied','accepted_if_known','perceived_influence_and_basis','independently_established_effect_if_claimed'},'Evidence acceptance and perceived influence explicitly separated after review')
ck('evidence_acceptance_if_known' in model['blank_canvas']['V04'] and 'perceived_influence_and_basis' in model['blank_canvas']['V04'],'V04 distinct optional acceptance and perceived influence fields')
ck(set(model['held_claim_ids_not_positive_support'])==set(holds),'All held claims excluded from positive framework support')
links=read('03-report/research-notes/r08/evidence/synthesis-links.json')['records'];link={x['link_id']:x for x in links}
for x in views:
 i=x['view_id'];basis=link[x['synthesis_link_id']]
 ck(not any(x[k] for k in ['mandatory','sequence_required','scored','validated']),'Optional nonordinal view '+i)
 ck(set(x['claim_ids'])<=set(claim) and not(set(x['claim_ids'])&set(holds)),'Bounded positive claim links '+i)
 ck(set(x['source_ids'])=={s for k in x['claim_ids'] for s in claim[k]['source_ids']},'Exact source/claim union '+i)
 ck(set(x['finding_ids'])<=findingids and set(x['existing_question_ids'])<=qids,'Finding/question linkage '+i)
 ck(x['claim_ids']==basis['claim_ids'] and x['finding_ids']==basis['finding_ids'],'Separately authored evidence linkage preserved '+i)
 ck(set(x['selective_record_fields'])==set(model['blank_canvas'][i]) and all(v is None for v in model['blank_canvas'][i].values()),'Selective blank view template '+i)
for k in ['blank_scope_template','blank_decision_brief']:ck(all(v is None for v in model[k].values()),'Blank reusable template '+k)
for k in ['participant_observations','actual_case_records','completed_framework_use_tests','causal_effect_estimates','employer_forecasts','chart_data','financial_inputs']:ck(model[k]==[],'No invented empirical result '+k)
for k in ['new_source_routes','new_canonical_claims','new_market_estimates','new_numeric_scores']:ck(model[k]==0,'No inflated evidence or score '+k)
ck(model['no_external_sending_without_user_permission'],'Sending boundary preserved')
report=read('03-report/R08-report-integration-map.json')
ck(report['chapter_count']==8 and report['two_parts_preserved'] and report['finished_report_required'] and not report['outline_client_approved'],'Unapproved two-part eight-chapter finished report retained')
ck(not report['D01_complete'] and not report['D06_final_complete'] and not report['commercial_table_content_in_public_report'],'Working files do not complete final formats or expose Table economics')
ck(report['part_labels']=={'part_one':'What leaders want','part_two':'How investment decisions happen','conclusion':'From Ambition to Investment'},'Exact proposed part labels preserved')
with zipfile.ZipFile(ROOT/report['outline_origin']) as z:doc=ET.fromstring(z.read('word/document.xml'))
ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
text=' '.join(x.text or '' for x in doc.findall('.//w:t',ns))
for label in ['What leaders want','How investment decisions happen','From Ambition to Investment','Operating reality','Technology and service needs','Priorities and commitment','The decision pathway','The business case','Progress and constraints','Staying or switching','The practical framework']:ck(label in text,'SourceDOCX outline contains '+label)
for x in report['chapter_map']:
 i=str(x['chapter_number'])
 ck(set(x['supporting_claim_ids'])<=set(claim) and not(set(x['supporting_claim_ids'])&set(holds)),'Chapter positive claims avoid holds '+i)
 ck(set(x['guardrail_claim_ids'])<=set(holds),'Chapter holds only as guardrail '+i)
 ck(set(x['relevant_finding_ids'])<=findingids and set(x['current_question_ids'])<=qids,'Chapter finding/question linkage '+i)
 ck(bool(x['can_prepare_now']) and bool(x['requires_later_evidence']),'Chapter now versus later evidence separated '+i)
ck(next(x for x in report['chapter_map'] if x['chapter_number']==3)['guardrail_claim_ids']==['CLM-0392'],'Chapter3 new numeric hold separated from positive support')
for k in ['practitioner_observations','priority_rankings','forecast_values','chart_data']:ck(report[k]==[],'Report original data absent '+k)
ck(report['new_mandatory_questions']==0 and not report['core_questions_changed'] and report['external_actions']==[],'Report no new core/contact')
design=read('03-report/research-notes/r08/route-challenge/constructed-routes.json');bydesign={x['route_id']:x for x in design['routes']}
applications=read('03-report/R08-constructed-walkthroughs.json');apps={x['route_id']:x for x in applications['routes']}
ck(applications['route_count']==len(apps)==10 and set(apps)==set(bydesign),'Ten actual root applications correspond to designs')
ck(not applications['practitioner_validation'] and applications['actual_case_records']==[] and applications['numerical_results']==[],'Constructed applications outside fieldwork and numeric data')
for ident,x in apps.items():
 d=bydesign[ident]
 ck(x['supplied_premises']==d['supplied_premises'],'Supplied premises exact '+ident)
 ck(x['supporting_claim_ids']==d['supporting_claim_ids'] and set(x['supporting_claim_ids'])<=set(claim),'Route support linkage '+ident)
 ck(x['evidence_type']=='constructed_internal_application' and x['executed_against_preparatory_R08_framework'] and x['framework_version']==model['framework_version'],'Actual preparatory application '+ident)
 ck(not x['original_practitioner_observation'] and all(x[k] is None for k in ['actual_employer','participant_id','actual_case_id','as_of_date','event_date','numerical_result']),'No invented employer identity/time/result '+ident)
 ck(set(x['view_ids'])<=vids and x['framework_path']=='03-report/R08-framework-map.json' and bool(x['method']),'Application references actual views/method '+ident)
 ck(bool(x['unknowns']) and x['failed_boundary'] is None,'Unknowns retained/no recorded violation '+ident)
 ck(not d['executed_against_final_R08_framework'] and not d['validated_predictive_result'],'Source design not retrospectively validated '+ident)
ck(apps['R08-T01']['proposal_decision'] is None and apps['R08-T01']['supported_next_action'] is None,'Adequate current route no invented case/action')
ck(apps['R08-T02']['proposal_decision'] is None and apps['R08-T02']['selected_response'] is None,'Preproposal route no invented pending/solution')
ck(apps['R08-T03']['broader_authority'] is None and apps['R08-T03']['implementation'] is None and apps['R08-T03']['benefit_assessment'] is None,'Noformalapproval limited to scoped action')
ck(apps['R08-T04']['later_phase_resources'] is None and apps['R08-T04']['release_condition_clearance'] is None,'Initialphase approval does not fill later phases/release')
ck(apps['R08-T05']['commitment'] is None and apps['R08-T05']['implementation'] is None and apps['R08-T05']['benefit_assessment'] is None,'Limited renewal leaves execution/outcome open')
ck(apps['R08-T06']['commitment'] is None and apps['R08-T06']['implementation'] is None,'Retained platform/changed route keeps approval separate')
ck('authorisation' in apps['R08-T07']['proposal_decision'] and 'unknown' in apps['R08-T07']['implementation'],'Elapsed rollout preserves known state versus current unknown')
ck(apps['R08-T08']['selected_response'] is None and apps['R08-T08']['benefit_assessment'] is None,'Componentstop does not invent replacement/benefit')
ck(apps['R08-T09']['proposal_decision'] is None and apps['R08-T09']['implementation'] is None,'Feature/roadmap not purchase/usable release')
ck(apps['R08-T10']['resource_missingness']=='not_disclosed' and apps['R08-T10']['applicability_missingness']=='not_known' and apps['R08-T10']['owner'] is None and apps['R08-T10']['supported_next_action'] is None,'Limitedknowledge/disclosure distinct no forcedowner/action')
routing=read('08-qa/R08-routing-walkthrough.json')
ck(routing['status']=='passed_internal_constructed_walkthrough' and all(x['passed'] for x in routing['checks']) and routing['route_count']==10,'Root structured routing checks pass')
ck(sha(routing['framework_path'])==routing['framework_sha256_at_walkthrough'],'Routing exact reviewed framework hash')
ck(sha(routing['application_path'])==routing['application_sha256_at_walkthrough'],'Routing exact application hash')
ck(sha(routing['source_design_path'])==routing['source_design_sha256'],'Routing exact source design hash')
for rel in ['03-report/R08-DECISION-FRAMEWORK.md','03-report/R08-DESKTOP-SYNTHESIS.md','03-report/R08-REPORT-INTEGRATION.md','03-report/modules/R08-decision-framework-and-synthesis.md']:
 t=(ROOT/rel).read_text()
 ck('Nothing sent' in t,'No sending statement '+rel)
 for target in re.findall(r'\]\(([^)]+)\)',t):
  if target.startswith(('http://','https://','#')):continue
  target=unquote(target.split('#',1)[0]);ck((ROOT/rel).parent.joinpath(target).resolve().exists(),'Local draft link '+rel+' '+target)
wp=read('00-control/work-packages.json')['records'];p=next(x for x in wp if x['work_package_id']=='WP15')
ck('WP11' in p['dependencies'] and p['status']!='completed','WP15 retains original coding dependency and not finalcomplete')
deliverables=read('00-control/deliverables.json')['records']
ck(all(x['status'] in ['planned','in_progress'] and not x['final_paths'] for x in deliverables),'No finished client deliverable falsely marked complete')
result=dict(date='2026-10-29',status='passed_for_internal_R08_preparatory_synthesis',check_count=len(checks),checks=checks,scope='Independent review of separately authored evidence/reader/route inputs and root integrated preparatory canvas, ten manual constructed applications, report map and prior/core/client/register preservation. Internal coherence and traceability only; no original practitioner validation, causal approval effect, legal/vendor test, commercial demand or final publication assurance.',source_counts=dict(sources=191,claims=338,primary_captures=120,internal_findings=76),external_actions=[])
(ROOT/'08-qa/r08-review/integration-checks.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='checks'},indent=2))
