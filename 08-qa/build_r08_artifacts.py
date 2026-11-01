from pathlib import Path
import json,hashlib
ROOT=Path(__file__).resolve().parents[1];DATE='2026-10-29'
def read(p):return json.loads((ROOT/p).read_text())
def write(p,d):(ROOT/p).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n' if not isinstance(d,str) else d)
def sha(p):return hashlib.sha256((ROOT/p).read_bytes()).hexdigest()
e=read('03-report/research-notes/r08/evidence/synthesis-links.json')
content=read('03-report/research-notes/r08/reader-flow/content-map.json')
designed=read('03-report/research-notes/r08/route-challenge/constructed-routes.json')
claims={x['claim_id']:x for x in read('02-evidence/registers/claims.json')['records']}
held=set(e['held_claim_ids_not_used_as_positive_framework_support'])
for chapter in content['chapter_map']:
 chapter['guardrail_claim_ids']=[c for c in chapter['supporting_claim_ids'] if c in held]
 chapter['supporting_claim_ids']=[c for c in chapter['supporting_claim_ids'] if c not in held]
 chapter['guardrail_reference_rule']='Held claims explain an exclusion/conflict only, never a positive numerical priority or outcome.'
views=[]
wording=[
 ('What needs attention, if anything?','Describe the actual task, what works, who is affected and the intended outcome.','A need is not a chosen solution. Adequate service and no new priority are valid.',['task_and_scope','current_adequate_work','affected_outcome','intended_improvement']),
 ('Which responses are feasible?','Consider only relevant responses at this time: current capability, process/skills, retention or a change in tools, service or responsibility.','Options can combine; advertised availability does not prove usable access. Do not force a purchase or shortlist.',['current_arrangement','alternatives_considered','actual_feasibility_basis','selected_response_if_known']),
 ('Who can decide what?','Establish the authority, resource responsibility or external condition for this particular action, object and date, where known.','Seniority, sponsorship, funding, signature and release rights differ. No separate formal approval can be a valid scoped position.',['action_and_object','known_authority_function','funding_responsibility','condition_and_controlling_party']),
 ('What evidence and support are relevant?','Match the outcome to the evidence actually requested or supplied, known resources, affordability and practical delivery conditions.','Requested, supplied, accepted and believed influential evidence are not causal proof. Existing resources can support work without a new budget.',['evidence_requested','evidence_supplied','evidence_acceptance_if_known','perceived_influence_and_basis','resources_and_delivery_conditions']),
 ('What is the evidenced position?','Keep the proposal decision, commitment, implementation and intended/assessed benefit separate, with their own scope and dates where supplied.','Approval is not operation or benefit. Last evidenced state is not automatically the current or ultimate outcome.',['proposal_decision','commitment','implementation','benefit_assessment']),
 ('What next action or review is justified?','Identify a remaining evidence need, actual condition or relevant review only when supported by the account.','A proposed remedy is not a proven effect. Retention, a reasoned stop, no new action or an unresolved partial brief can be legitimate.',['remaining_evidence_or_condition','supported_next_action_if_any','relevant_owner_if_known','review_trigger_or_timing_if_known']),
]
for i,(link,(title,instruction,boundary,fields)) in enumerate(zip(e['records'],wording),1):
 views.append(dict(view_id=f'V{i:02}',title=title,instruction=instruction,boundary=boundary,selective_record_fields=fields,mandatory=False,sequence_required=False,scored=False,validated=False,synthesis_link_id=link['link_id'],topic_ids=link['topic_ids'],finding_ids=link['finding_ids'],claim_ids=link['claim_ids'],source_ids=link['source_ids'],existing_question_ids=link['existing_question_ids']))
model=dict(schema_version='1.0',framework_version='0.1',date=DATE,module_id='R08',title='Payroll Investment Decision Framework',status='preparatory_desktop_draft_independent_review_pending',purpose='Help explain the current decision and next supported action for a scoped payroll need, without prescribing investment.',views=views,views_are_linked_not_stages=True,mandatory_sequence=False,score=False,validated_predictor=False,approval_recipe=False,participant_validated=False,complete_final_WP15=False,requires_WP11_original_coding=True,new_mandatory_questions=0,core_question_version='0.2',core_question_count=14,all_views_required=False,partial_brief_allowed=True,no_case_allowed=True,no_disclosure_allowed=True,confidential_documents_required=False,personal_names_required=False,exact_budget_required=False,missing_owner_or_date_defaults_to_pending=False,missingness_values=['not_known','not_measured','not_applicable','not_disclosed'],case_route_not_a_decision_disposition=True,no_material_gap_is_valid=True,no_action_or_retention_or_stop_can_be_appropriate=True,states_are_separate=['proposal_decision','commitment','implementation','benefit_assessment'],evidence_claims_are_separate=['requested','supplied','accepted_if_known','perceived_influence_and_basis','independently_established_effect_if_claimed'],blank_scope_template={k:None for k in ['record_id','as_of_date_if_known','event_date_if_known','work_object_and_scope','remit_and_direct_knowledge','source_and_permission']},blank_canvas={v['view_id']:{k:None for k in v['selective_record_fields']} for v in views},blank_decision_brief={k:None for k in ['scope_and_date_if_known','what_is_known','source_and_knowledge_basis','what_is_not_established','next_action_or_review_if_supported']},participant_observations=[],actual_case_records=[],completed_framework_use_tests=[],causal_effect_estimates=[],employer_forecasts=[],chart_data=[],financial_inputs=[],new_source_routes=0,new_canonical_claims=0,new_market_estimates=0,new_numeric_scores=0,held_claim_ids_not_positive_support=e['held_claim_ids_not_used_as_positive_framework_support'],hypotheses=e['hypotheses'],collision_controls=e['collisions'],source_register_path='02-evidence/registers/sources.json',questionnaire_path='01-method/question-map.json',report_map_path='03-report/R08-report-integration-map.json',report_table_boundary=e['report_table_boundary'],no_external_sending_without_user_permission=True)
write('03-report/R08-framework-map.json',model)
integration=dict(date=DATE,status='preparatory_report_integration_not_client_approved',outline_origin=content['outline_origin'],outline_client_approved=False,finished_report_required=True,chapter_count=8,two_parts_preserved=True,part_labels={'part_one':'What leaders want','part_two':'How investment decisions happen','conclusion':'From Ambition to Investment'},concluding_chapter=content['concluding_chapter'],chapter_map=content['chapter_map'],held_claim_ids_not_positive_support=sorted(held),proposed_graphics=content['proposed_graphics'],report_deliverable_ids=content['report_deliverable_ids'],D01_complete=False,D06_final_complete=False,commercial_table_content_in_public_report=False,table_boundary=content['table_boundary'],practitioner_observations=[],priority_rankings=[],forecast_values=[],chart_data=[],new_mandatory_questions=0,core_questions_changed=False,external_actions=[])
write('03-report/R08-report-integration-map.json',integration)

frame='''# Payroll Investment Decision Framework

R08 working version0.1,29October2026. Preparatory desktop draft; independent integrated review pending. An original arrangement of this project's evidence, not a validated predictor, fixed workflow or recipe for approval. Final practitioner integration and client review remain open.

## Use one concrete decision, not a general technology theme

Start wherever the account begins: an operating need, a renewal, an approved phase, a stalled change or a reason to retain what works. Specify the relevant work and the date/remit only where known. Keep the contributor's unaided account before examples. This canvas helps organise that account; it is not six extra compulsory interview questions.

The aim is a clearer decision brief: what is known, what it is based on, what remains unestablished and any next action or review the account supports. All views are optional. A useful partial brief can leave an owner, date, approval position or next action unknown. Do not demand a confidential business case to fill a box.

## Six linked views

| View | Use it to establish | Keep separate |
| --- | --- | --- |
'''
for v in views:frame+=f"| {v['view_id']}: {v['title']} | {v['instruction']} | {v['boundary']} |\n"
frame+='''
The numbers identify views, not steps or a maturity score. Use only the parts relevant to the actual task. New evidence can lead back to an earlier view or change the explanation. The same arrangement can retain one component, change another and stop a third.

```mermaid
flowchart TB
  D[The scoped payroll decision or need]
  V1[Need and current basis] --- D
  V2[Feasible responses] --- D
  V3[Authority and conditions] --- D
  D --- V4[Evidence and support]
  D --- V5[Separate dated states]
  D --- V6[Supported next action or review]
```

The table is the complete text equivalent of this editable diagram. Connections show related views; they do not prescribe a progression.

## Make a useful brief with the facts available

Use this sentence structure only as a writing aid, leaving out unsupported parts:

“For [specific work/remit], the account establishes [known facts] on [source/date if known]. It does not yet establish [material gap]. [Supported action or review, if any] concerns [relevant function or condition, if known].”

This is a blank writing pattern, not a quotation or an employer observation. A next step is not required where none is known or appropriate. An adequate current arrangement, continuing work, a legitimate renewal or stop and a pre-proposal need all fit without inventing a purchase. Never-raised need is not automatically pending/declined; continuing operation is not automatically a deliberate renewal.

## Use evidence for the claim it can support

Ask what was requested, what was actually supplied, what the contributor believes influenced assessment and the basis for that belief. Those are different claims. A change after evidence was supplied is not, by itself, a causal demonstration. Independently established effects should be claimed only if their evidence exists; this project does not require a causal experiment or confidential approval records.

For resources and value, distinguish whole-life work/resources, future incremental cash and funding affordability. Preserve non-cash outcomes such as continuity or usable capacity without converting every benefit into money. Planned, approved and spent are different; paid hours are not necessarily available expertise. A tariff, salary guide or supplier promise is not a customer-specific total cost or benefit.

For position, keep decision, commitment, implementation and benefit in separate fields. A release condition can remain after funding; a rollout postponement does not itself change an earlier investment decision. Attach each statement to the component/task it describes. A future policy phase, software roadmap or passed target date does not establish delivery.

## Select detail only when it changes the explanation

The existing R02–R07 maps provide depth behind the canvas: need/consequence, eight combinable response paths, action-specific decision rights, three financial views and nine evidence domains, outcome-specific events, and priority/context conditions. They are analytical aids, not cumulative checklists to read to every contributor.

Relevant context can include retained work, actual account/access, worker/service arrangements, jurisdiction, available skill/time, a dependency beside business-as-usual or whose task improves. Do not infer it from company size, a role title, headquarters, a public feature list or the fact that a scenario asked for a hire. Preserve not known, not measured, not applicable and not disclosed separately; do not score missingness or infer failure.

## How the draft was challenged

Ten expressly constructed walkthroughs apply this canvas to adequate service, pre-proposal need, scoped action without separate formal approval, conditional phases, rational renewal, a changed route on a retained platform, delayed rollout, component stop, uncertain capability access and limited knowledge/disclosure. They demonstrate how the design handles supplied premises. They are not real practitioner cases, user testing, market validation or proof that the framework improves decisions.

## Evidence and next integration

Each view links to existing findings, source-specific claims and unchanged question IDs in the [structured framework](R08-framework-map.json). The [evidence synthesis](research-notes/r08/evidence/EVIDENCE-SYNTHESIS.md) preserves collisions, hypotheses and held claims. The [report integration plan](R08-REPORT-INTEGRATION.md) maps the two proposed parts and conclusion.

No numeric score, adoption/priority ranking, employer forecast or new interview question is created. Source, client, rights and practitioner gates remain. Final Word/PDF, editable graphic and chart/data deliverables are not replaced by these working files. Nothing sent.
'''
write('03-report/R08-DECISION-FRAMEWORK.md',frame)

report='''# R08 report integration and evidence gaps

29October2026. Preparatory synthesis, not a new approved outline or finished publication. The proposed structure is taken from the existing version0.2 client plan. Its two parts, eight chapters and concluding “From Ambition to Investment” chapter remain unchanged and unapproved.

## Narrative flow

The existing labels are Part One: “What leaders want”; Part Two: “How investment decisions happen”; and conclusion: “From Ambition to Investment.” The table uses readable working headings for the same proposed chapters; no client outline is replaced or silently approved.

Begin with the payroll work and consequences readers recognise, including what functions well. Explain capabilities and service boundaries before discussing priorities. The second part examines action-specific authority, evidence/resources and actual decisions/results. The conclusion uses the six-view canvas to make the next supported decision easier to explain, without treating every case as a purchase opportunity.

| Part / chapter | Reader purpose | Prepare now | Evidence still needed |
| --- | --- | --- | --- |
'''
for x in content['chapter_map']:
 report+=f"| {x['proposed_part'].replace('_',' ')} / {x['chapter_number']}. {x['proposed_reader_heading']} | {x['purpose']} | {' '.join(x['can_prepare_now'])} | {' '.join(x['requires_later_evidence'])} |\n"
report+='''
## What can be drafted from the desktop work

Definitions, source-scoped context, selected published cases with their dates/limits, an explanation of the distinctions and the blank analytical structures can be prepared. Reuse one source/programme identity across modules rather than count repeated documents as independent corroboration. Historical expectations and current measures do not become a matched trend; unlike populations do not create a market average. Numerical/UI holds remain excluded from positive support.

The report can offer questions worth considering, but cannot yet say which barriers/priorities were strongest among this commission's practitioners, what they most often bought, what changed approvals or how widely a contextual pattern occurs. No source or supplier advice can stand in for those original accounts.

## Practitioner integration before final synthesis

Before collection, reconcile client focus, proposed population, timing and collection/permission arrangements through the existing review process. User permission is required before anything is sent. Use the unchanged guide with proportionate routes; do not add a framework questionnaire or a new cohort.

For the agreed6–10distinct verified permissioned contributors, retain stable participant IDs, guide version, case/remit/event context, source of knowledge, missingness and permissions. Keep identifying/restricted material outside the public/source repository in the approved arrangement. Eligible overlap with Table membership input is counted once; commercial buyers are not automatically practitioners.

Code actual observations to the existing modules/views, including adequate service, useful retention, enabling conditions and contrary cases. Distinguish participant quotation/paraphrase, published material and researcher interpretation. Review the claims, alternative explanations, permissions and achieved/missing coverage before final synthesis. This is planned integration, not a record of interviews conducted or a requirement for extra tests beyond scope.

## Graphics and contracted formats

Four provisional structures are useful: need/consequence/outcome matrix, option trade-off map, component-level decision/delivery/benefit illustration and the linked-view canvas. Only analytical/blank structures are prepared now. Quantitative graphics need comparable values, units, bases and rights before any data are populated. Colour/hover must not carry the sole meaning; use readable text/source tables and editable assets.

D01 remains a finished JGA-branded PDF/editable Word publication. D02 remains the executive summary. D06 remains a framework included in the report and editable Word/PowerPoint or equivalent final source. D08 still needs reviewed editable graphics and underlying Excel data where charts use data. These Markdown/JSON preparations do not complete or substitute for those handover formats.

## Public report versus The Table

The public report can contain cleared research findings, bounded source context, method and the final framework. The Table's buyer/member conversations, pricing, licences, willingness to fund, sponsor terms, costs, cash flows and commercial recommendation belong in the confidential feasibility work. Participant identity/permission details remain restricted. Neither a useful framework nor payroll need establishes demand for paid research, membership or events.

T01–T07 and WP11 remain open. R08 can be prepared independently, but final WP15 depends on coded original practitioner contributions. No numerical Confidence Index, commercial launch verdict, approved venue/spend or original observation is created here.

The [structured report map](R08-report-integration-map.json) retains chapter-level evidence and source-plan provenance. See the [reader-flow analysis](research-notes/r08/reader-flow/READER-FLOW.md) and [framework](R08-DECISION-FRAMEWORK.md). Nothing sent.
'''
write('03-report/R08-REPORT-INTEGRATION.md',report)

# Root-authored application to the final six-view draft. These are deliberately
# not written into the unperformed original-observation or source-data arrays.
applications=[
 dict(route_id='R08-T01',case_route='adequate_current_no_new_case',recorded_position='Adequate scoped current service; no new material priority supplied.',proposal_decision=None,selected_response=None,resource_basis=None,commitment=None,implementation=None,benefit_assessment=None,unknowns=['Any separate renewal','Later conditions/review'],supported_next_action=None,owner=None,view_ids=['V01','V02','V05','V06'],boundary_preserved='No manufactured gap, approval, transaction or compulsory monitoring.'),
 dict(route_id='R08-T02',case_route='pre_proposal_need',recorded_position='A stated task/control need has never been raised as a proposal.',proposal_decision=None,selected_response=None,resource_basis=None,commitment=None,implementation=None,benefit_assessment=None,unknowns=['Organisational awareness','Feasible alternatives','Authority/resources'],supported_next_action='A proportionate clarification can be proposed; it is not an actual authorised action or remedy effect.',owner=None,view_ids=['V01','V02','V03','V05','V06'],boundary_preserved='Not pending, declined or deferred; no new platform/hire inferred.'),
 dict(route_id='R08-T03',case_route='scoped_operating_action',recorded_position='Contributor explicitly supplies no separate formal approval requirement for this scoped action.',proposal_decision='No formal approval required for this action, per constructed premise.',selected_response='Small process/control change',resource_basis='Existing scoped resources, per premise.',broader_authority=None,commitment=None,implementation=None,benefit_assessment=None,unknowns=['Wider authority','Actual operation/result'],supported_next_action=None,owner=None,view_ids=['V03','V04','V05','V06'],boundary_preserved='No committee, new budget, unrestricted authority or success is invented.'),
 dict(route_id='R08-T04',case_route='conditional_scoped_phase',recorded_position='Initial phase approval/resources supplied; separate release condition and later-phase unknowns.',proposal_decision='Initial phase approved only.',selected_response=None,resource_basis='Initial phase only.',later_phase_resources=None,release_condition_clearance=None,commitment=None,implementation=None,benefit_assessment=None,unknowns=['Clearance/execution','Later phases','Assessed result'],supported_next_action='The condition/clearance and relevant next decision are the evidence gap, not a claimed completed step.',owner=None,view_ids=['V03','V04','V05','V06'],boundary_preserved='Approval/resources do not become live operation; later scope is neither funded nor unfunded by inference.'),
 dict(route_id='R08-T05',case_route='explicit_limited_renewal',recorded_position='A limited renewal is explicitly selected for continuity and time to prepare an alternative.',proposal_decision='Renewal decision supplied.',selected_response='Retain scoped arrangement for limited period.',resource_basis=None,commitment=None,implementation=None,benefit_assessment=None,unknowns=['Later choice','Subsequent outcome','Optimality'],supported_next_action='A relevant later preparation/review condition only if the account supplies it.',owner=None,view_ids=['V01','V02','V04','V05','V06'],boundary_preserved='No permanent satisfaction, irrational inertia, guaranteed switch or standard duration.'),
 dict(route_id='R08-T06',case_route='retained_platform_changed_route',recorded_position='Platform retained; one commercial/service route change approved.',proposal_decision='Approved scoped route change.',selected_response='Retain platform, change specified route.',resource_basis=None,commitment=None,implementation=None,benefit_assessment=None,unknowns=['Contract execution','Operational service','Benefit'],supported_next_action='Confirm the relevant execution/operation evidence if needed; no full replacement conclusion.',owner=None,view_ids=['V02','V03','V04','V05','V06'],boundary_preserved='Retention and change coexist; approval does not imply executed contract or service.'),
 dict(route_id='R08-T07',case_route='postponed_rollout',recorded_position='Earlier authorisation and later declared rollout postponement; target elapsed without a later observation.',proposal_decision='Earlier authorisation retained; no new decision event supplied.',selected_response=None,resource_basis=None,commitment=None,implementation='Postponed milestone declared in supplied account; later operation unknown.',benefit_assessment=None,unknowns=['Latest operational state','Realised result'],supported_next_action='A later dated observation would be needed for a current-outcome claim; no automatic nudge/action required.',owner=None,view_ids=['V03','V04','V05','V06'],boundary_preserved='No inferred deferred investment, current failure or completion from elapsed target.'),
 dict(route_id='R08-T08',case_route='scoped_component_stop',recorded_position='One component explicitly stops while other work and the underlying need continue.',proposal_decision='Explicit stop of this component only.',selected_response=None,resource_basis=None,commitment=None,implementation='Other operations/components continue per premise; replacement not supplied.',benefit_assessment=None,unknowns=['Replacement','Comparative outcome','Remedy effect','Handback/dependency detail'],supported_next_action='Describe any actual supported remaining need/handback condition; do not prescribe restart.',owner=None,view_ids=['V01','V02','V03','V05','V06'],boundary_preserved='No whole-need abandonment, failed supplier conclusion or guaranteed alternative.'),
 dict(route_id='R08-T09',case_route='capability_access_uncertainty',recorded_position='Defined task interest and advertised inclusion; actual entitlement/access/setup/use unknown, plus supplier future statement.',proposal_decision=None,selected_response=None,resource_basis=None,commitment=None,implementation=None,benefit_assessment=None,unknowns=['Actual account entitlement','Access/setup/use','Future release'],supported_next_action='A relevant capability/access clarification is a proposed evidence step, not proof a product purchase is needed.',owner=None,view_ids=['V01','V02','V04','V05','V06'],boundary_preserved='No free total cost, tested capability, roadmap shipment, customer funding or success.'),
 dict(route_id='R08-T10',case_route='limited_knowledge_and_disclosure',recorded_position='Potential dated external signal; actual applicability and employer states unknown, resources withheld.',proposal_decision=None,selected_response=None,resource_basis=None,resource_missingness='not_disclosed',commitment=None,implementation=None,benefit_assessment=None,applicability_missingness='not_known',unknowns=['Applicability','Authority','Operation','User result'],supported_next_action=None,owner=None,view_ids=['V01','V03','V04','V05','V06'],boundary_preserved='No forced owner/date/approval/action, pending default, compulsory disclosure or funded need from external signal.'),
]
for a in applications:
 design=next(x for x in designed['routes'] if x['route_id']==a['route_id'])
 a.update(evidence_type='constructed_internal_application',actual_employer=None,participant_id=None,actual_case_id=None,as_of_date=None,event_date=None,numerical_result=None,original_practitioner_observation=False,framework_version='0.1',framework_path='03-report/R08-framework-map.json',supplied_premises=design['supplied_premises'],supporting_claim_ids=design['supporting_claim_ids'],executed_against_preparatory_R08_framework=True,method='Root-authored manual analytical application to supplied constructed premises; no automatic decision engine or human user test.',failed_boundary=None)
write('03-report/R08-constructed-walkthroughs.json',dict(date=DATE,status='root_constructed_applications_ready_for_independent_review',framework_version='0.1',route_count=len(applications),practitioner_validation=False,actual_case_records=[],numerical_results=[],routes=applications))

write('03-report/R08-DESKTOP-SYNTHESIS.md','''# R08: from the research modules to a usable decision framework

29October2026. Preparatory desktop synthesis; independent integrated review pending. The draft is ready for analytical review, not final publication or a claim of practitioner validation.

## Main synthesis

The value of this report is a concrete explanation of a payroll decision: the work and outcome, feasible responses, relevant authority, evidence/resources, the actual position and any justified next action. An organisation can legitimately retain a functioning arrangement, change only one component or stop a proposal. A need is not automatically a sale, and approval is not the sole measure of a sound decision.

Six linked views bring R02–R07 together without copying every analytical checklist into a new questionnaire. The [draft framework](R08-DECISION-FRAMEWORK.md) puts current adequate work inside the need view, keeps funding and delivery apart, and permits partial/no-case accounts. It does not supply a score, stage funnel or predictive approval recipe. The [structured map](R08-framework-map.json) connects each view to existing findings, claims, sources and questions.

## What the evidence supports now

- Define the actual task/remit, consequence and desired outcome before picking a technology/service or hiring response.
- Compare only relevant feasible options, including retained capability, process/skills, smaller change, combined options and retention.
- Establish action-specific decision rights rather than infer authority from title, sponsor status or contract signature.
- Keep value, whole-life resources, incremental cash, funding affordability and practical deliverability distinct.
- Record decision, commitment, implementation and assessed benefit as separate dated/scoped claims; preserve the last evidenced state.
- Identify the next evidence need or condition where the account supports it, without assuming a proposed remedy works or that further action is required.

These are evidence-informed analytical distinctions. They are not a finding that a particular view causes approval, that one barrier dominates the market or that every employer follows this pattern. Source-scoped cases, official management principles, supplier declarations, surveys and earlier constructed prompt results retain their different purposes and limits. Repeated programmes/sources are not counted as independent corroboration.

## Counterexamples applied to this draft

Ten expressly constructed routes challenge adequate-current/no-case, pre-proposal, no separate formal approval, conditional phases, limited renewal, retained platform/changed route, postponed rollout, stopped component, capability-access uncertainty and limited knowledge/disclosure. Root applied each route to the actual six-view version0.1 draft and recorded the permitted interpretation and unknowns. The [applications](R08-constructed-walkthroughs.json) and routing QA retain that trail.

The walkthroughs demonstrate internal coherence with supplied premises. They do not establish comprehension, practitioner usefulness, realised effects, commercial demand or a validated framework. No synthetic case is written into original-observation, chart/data or financial-input arrays.

## What changed during synthesis

The front view explicitly allows “if anything” and adequate service. Authority wording is neutral about whether an item needs unblocking. A useful brief may remain incomplete without a named owner, date, approval code or next step. Requested, supplied, accepted or believed influential evidence are separated from causal proof. The compact canvas points to optional depth rather than imposing the accumulated R02–R07 fields on every contributor.

## Report integration and remaining work

The existing proposed two parts, eight chapters and “From Ambition to Investment” conclusion are preserved in the [report integration plan](R08-REPORT-INTEGRATION.md). The plan distinguishes source-supported drafting from the original cases still needed. It retains the contracted finished Word/PDF, summary, editable framework and graphic/data package; these working files do not replace them.

WP11 coded eligible, permissioned practitioner contributions remain a dependency for final WP15. Actual context, approval/resource explanations, contrary cases and appropriate permission must shape the final framework and findings. Usefulness and approval influence remain hypotheses. The public narrative must also stay separate from The Table's confidential buyer/sponsor economics and launch assessment.

The [evidence synthesis](research-notes/r08/evidence/EVIDENCE-SYNTHESIS.md), [reader-flow review](research-notes/r08/reader-flow/READER-FLOW.md) and [constructed challenge design](research-notes/r08/route-challenge/COUNTEREXAMPLE-PLAN.md) explain the inputs. No new source, canonical claim, market estimate, question or original participant record is added. Existing holds and prior/client files are preserved. Nothing sent.
''')
write('03-report/modules/R08-decision-framework-and-synthesis.md','''# R08 Decision Framework and report synthesis

Preparatory desktop synthesis drafted29October2026; independent integrated review pending. FinalWP15 remains dependent on WP11 coded original practitioner contributions and final-use review.

## Contribution

A six-view Payroll Investment Decision Framework connects the scoped need/current basis, feasible responses, action-specific authority, relevant evidence/support, separate actual states and supported next action/review. Views are linked, optional and nonordinal. It is not a required purchase path, score, predictive model or recipe for approval.

The map reuses existing findings/claims/sources and unchanged question IDs. It adds no canonical evidence or practitioner result. Ten constructed applications test internal handling of difficult routes; they are not actual cases or user validation. Missing owner/date/status/action is permitted and does not default to pending. Evidence requested/supplied/perceived influential and causal effect remain different claims.

## Working outputs

- [Framework and blank writing pattern](../R08-DECISION-FRAMEWORK.md)
- [Desktop synthesis](../R08-DESKTOP-SYNTHESIS.md)
- [Structured framework](../R08-framework-map.json)
- [Report integration plan](../R08-REPORT-INTEGRATION.md)
- [Constructed applications](../R08-constructed-walkthroughs.json)

The proposed two parts/eight chapters/conclusion and14corequestions remain unchanged and unapproved. All76existing findings,191sources338claims and held claims remain distinct from this analyst synthesis. D01/D02/D06/D08 final formats, practitioner integration, collection/client/rights permissions and TheTable work remain open. Nothing sent.
''')
print(json.dumps({'status':'R08_integrated_draft_created','linked_views':6,'proposed_chapters':8,'root_constructed_applications':len(applications),'new_sources':0,'new_claims':0,'original_participants':0},indent=2))
