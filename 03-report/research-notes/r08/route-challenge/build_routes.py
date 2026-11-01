from pathlib import Path
import json, hashlib

BASE=Path(__file__).resolve().parent
ROOT=BASE.parents[3]
BASE.mkdir(parents=True,exist_ok=True)
claims={x['claim_id'] for x in json.loads((ROOT/'02-evidence/registers/claims.json').read_text())['records']}

rows=[
 dict(route_id='R08-T01',title='Adequate current arrangement without a new change',
  supplied_premises=['The constructed contributor reports that the current scoped payroll task is adequate and identifies no material improvement they expect the organisation to prioritise.','No separate renewal, replacement or new investment decision is supplied.'],
  permissible_interpretation=['Retain an adequate-current-position route without manufacturing a gap or transaction.','Current service continuation and an explicit renewal decision remain different facts.'],
  forbidden_inferences=['No material priority means payroll has no value or no resource use.','A deliberate renewal, permanent satisfaction, absence of every unmet need or immunity from future change has been established.'],
  expected_analyst_output='A constructed brief records adequate current scoped service, no new priority supplied and the observation/knowledge boundary. It does not invent an approval or vendor opportunity.',
  remaining_gap='Any later change in conditions or review trigger is unknown unless supplied; no compulsory monitoring programme or new question is imposed.',
  views_stressed=['need','current_basis','options','states','next_action'],
  supporting_claim_ids=['CLM-0347','CLM-0348','CLM-0365','CLM-0366','CLM-0408'],
  failure_signal='The canvas forces a problem, a purchase or an approval status for this route.'),
 dict(route_id='R08-T02',title='Need exists but no proposal has been raised',
  supplied_premises=['The constructed contributor identifies a concrete handoff or control problem within their remit.','They state that it has not been raised as a proposal and provide no organisational approval, funding or selected response.'],
  permissible_interpretation=['Record a pre-proposal need and the contributor’s knowledge, preserving the distinction between problem and chosen solution.','A possible next clarification is proportionate to the task; it is not evidence that a particular remedy has worked.'],
  forbidden_inferences=['The organisation declined, deferred or is pending approval.','The problem requires a new platform or hire, or a lack of supplied budget proves unwillingness to fund.'],
  expected_analyst_output='A constructed need statement, affected work and known consequence are separated from unestablished proposal/authority/resources. A relevant existing guide route can be used without creating a recent approved case.',
  remaining_gap='The organisation’s awareness, alternatives and authorised next step remain unestablished.',
  views_stressed=['need','current_basis','options','authority','states','next_action'],
  supporting_claim_ids=['CLM-0362','CLM-0365','CLM-0366','CLM-0393','CLM-0408'],
  failure_signal='Not-yet-raised is coded as pending, declined or an unsuccessful purchase.'),
 dict(route_id='R08-T03',title='Scoped operating improvement with no formal approval required',
  supplied_premises=['The constructed contributor describes a small process/control change within their existing remit and resources.','They explicitly state that no separate formal approval was required for that particular action.','No wider purchasing authority, full implementation assurance or assessed benefit is supplied.'],
  permissible_interpretation=['Use the existing no-formal-approval-required disposition only for the supplied task and authority scope.','Separate the stated action from evidence about its result and any wider decision.'],
  forbidden_inferences=['Every improvement requires a business case, committee, new funding or contract.','No formal approval required means no authority/control, or that the improvement succeeded.'],
  expected_analyst_output='A constructed dated/scoped operating-action record retains its authority basis, known action and unknown result without forcing procurement or a new budget.',
  remaining_gap='Actual operation and outcome would need their own evidence; no confidential threshold or full delegation document is demanded.',
  views_stressed=['authority','support','states','next_action'],
  supporting_claim_ids=['CLM-0255','CLM-0261','CLM-0262','CLM-0287','CLM-0365','CLM-0408'],
  failure_signal='The canvas treats missing purchase approval as failure or infers unrestricted authority from one delegated action.'),
 dict(route_id='R08-T04',title='Conditional phase approval and resources do not prove delivery',
  supplied_premises=['The constructed account supplies approval and resources for an initial scoped phase.','A separate clearance condition precedes operational release; a later phase is described but its resources are not supplied.','No executed release, later-phase approval or assessed benefit is supplied.'],
  permissible_interpretation=['Record the approved object/phase, known resource basis and separate binding condition with its owner if known.','Keep later-phase support unknown and distinguish commitments, release and realised outcome.'],
  forbidden_inferences=['All phases are approved/funded, or later phases are unfunded.','Initial approval, available funds or a clearance plan establishes live service, current compliance or realised benefit.'],
  expected_analyst_output='A constructed brief keeps phase-specific approval/resources, the release condition and later unknowns in parallel. It identifies the next decision/clearance rather than a success score.',
  remaining_gap='Evidence of condition clearance, actual execution, later resources and intended-result assessment remains absent.',
  views_stressed=['authority','support','states','next_action'],
  supporting_claim_ids=['CLM-0255','CLM-0262','CLM-0299','CLM-0302','CLM-0318','CLM-0404','CLM-0408'],
  failure_signal='Approved/funded becomes a single completed or ready status for the whole programme.'),
 dict(route_id='R08-T05',title='Time-bounded renewal for continuity rather than pure satisfaction',
  supplied_premises=['The constructed decision explicitly renews a scoped current arrangement for a limited period.','The supplied reason combines service continuity and the practical time needed to prepare a feasible alternative.','No permanent replacement commitment, optimality proof or subsequent outcome is supplied.'],
  permissible_interpretation=['Record the actual renewal, the alternatives feasible at that event and the stated mixed rationale.','A next review or preparation condition may be relevant if known; it is not a guaranteed future switch.'],
  forbidden_inferences=['Renewal proves complete satisfaction, irrational inertia, permanent lock-in or absence of investment.','The eventual alternative is guaranteed, or a later option shows the earlier decision was irrational.'],
  expected_analyst_output='A constructed renewal record explains the dated continuity constraint and known scope, with later choices and results left open.',
  remaining_gap='Later review, readiness and actual choice/outcome remain unknown; no universal renewal duration is introduced.',
  views_stressed=['current_basis','options','support','states','next_action'],
  supporting_claim_ids=['CLM-0345','CLM-0346','CLM-0348','CLM-0367','CLM-0370','CLM-0371','CLM-0427'],
  failure_signal='The canvas places all retained arrangements in a satisfaction or unsuccessful-change bucket.'),
 dict(route_id='R08-T06',title='Retained platform with a changed service or commercial route',
  supplied_premises=['The constructed account retains the payroll platform and supplies approval for a specific change to the commercial/service route.','The specific authority event is supplied, while contract execution, recurring-service operation and benefit are not.'],
  permissible_interpretation=['Represent retained and changed components together, attaching status to the actual route/object.','Retained responsibilities, handoffs and the receiving arrangement need their own scope.'],
  forbidden_inferences=['A binary supplier-stay/switch label captures the whole choice.','Agreement to recommendations proves signed terms, full migration, operational readiness or realised savings.'],
  expected_analyst_output='A constructed component-level brief states what remains and what changes, the actual known decision and the separate implementation/result gaps.',
  remaining_gap='Contract scope, operational acceptance and observed results are unknown unless supplied.',
  views_stressed=['current_basis','options','authority','states'],
  supporting_claim_ids=['CLM-0215','CLM-0344','CLM-0347','CLM-0365','CLM-0377','CLM-0378'],
  failure_signal='The framework requires a whole-programme stay/switch answer or treats one approval as an executed migration.'),
 dict(route_id='R08-T07',title='Postponed rollout without evidence of deferred investment',
  supplied_premises=['The constructed record supplies a previously authorised change and a later declared postponement of a rollout milestone.','It gives a sequencing or continuity reason but no new investment-decision event.','The target milestone has since passed, with no later observed event supplied.'],
  permissible_interpretation=['Keep the supplied proposal decision and implementation schedule separate.','Record the last evidenced statement, declared reason, target and present observation boundary.'],
  forbidden_inferences=['The investment was deferred, rejected or abandoned solely because rollout moved.','The elapsed target establishes completion, continued delay, success or failure.','The supplied reason proves risk was reduced or the sequence was optimal.'],
  expected_analyst_output='A constructed brief preserves the prior authorisation and declared rollout revision while marking later operation and benefit as unestablished.',
  remaining_gap='A later authoritative event or original directly known update is needed to change the observation boundary.',
  views_stressed=['authority','support','states','next_action'],
  supporting_claim_ids=['CLM-0349','CLM-0354','CLM-0365','CLM-0371','CLM-0412','CLM-0413','CLM-0427'],
  failure_signal='The canvas auto-updates a decision or outcome from the schedule or elapsed time.'),
 dict(route_id='R08-T08',title='Stopped component while the wider need continues',
  supplied_premises=['The constructed account supplies an explicit stop of one scoped project/component at a known stage.','Other operations/components continue and the underlying payroll need is still described.','No completed replacement, comparative outcome or alternative remedy effect is supplied.'],
  permissible_interpretation=['Attach the stop to its actual component, decision and knowledge basis.','Separate continuing service/obligations and the unresolved need from the ceased option.'],
  forbidden_inferences=['Stopping one component means the entire need or programme was abandoned.','Benefits elsewhere prove payroll benefit, or stopping proves an earlier alternative would have worked.','A cancellation label alone supplies the reason, authority or executed contract history.'],
  expected_analyst_output='A constructed object-specific stop record states what ceased, what continues, the known reason and any handback/dependency gap without prescribing a restart.',
  remaining_gap='Remaining obligations, later alternatives and actual effects need separate evidence; a reasoned stop may remain legitimate.',
  views_stressed=['need','options','authority','states','next_action'],
  supporting_claim_ids=['CLM-0351','CLM-0352','CLM-0353','CLM-0354','CLM-0362','CLM-0366'],
  failure_signal='The framework treats every stop as whole-project failure or automatically offers a remedy to reverse it.'),
 dict(route_id='R08-T09',title='Existing feature may need access or setup rather than purchase',
  supplied_premises=['The constructed contributor wants a defined task to improve and cites advertised inclusion in a current offer.','Actual account entitlement, permissions, configuration and use are unknown; a supplier also describes a future update.','No product test, firm quote, employer purchase decision or observed effect is supplied.'],
  permissible_interpretation=['Separate task need, advertised offer, actual access/setup/use and future roadmap.','Existing-capability clarification, a process change or a new option remain possibilities until the case establishes fit.'],
  forbidden_inferences=['Advertised inclusion proves current usable functionality, zero total cost, an unused feature or successful task operation.','A future supplier statement establishes release, legal readiness or employer commitment.','The task necessarily requires replacement or recruitment.'],
  expected_analyst_output='A constructed brief identifies the specific capability/access uncertainty and a proportionate verification need before any purchase conclusion.',
  remaining_gap='Current applicable entitlement/release, actual setup/use, responsible party and desired/observed result remain unestablished.',
  views_stressed=['need','current_basis','options','support','states','next_action'],
  supporting_claim_ids=['CLM-0414','CLM-0415','CLM-0417','CLM-0418','CLM-0424'],
  failure_signal='The canvas converts feature interest into a new sale or maps a supplier roadmap onto employer delivery.'),
 dict(route_id='R08-T10',title='Limited knowledge, withheld details and a future external signal',
  supplied_premises=['The constructed contributor identifies a potentially relevant dated external planning signal but cannot establish its detailed applicability to their actual payroll task.','They do not know the relevant approval/delivery position and prefer not to disclose resource information.','No original user outcome or later event is supplied.'],
  permissible_interpretation=['Keep the external signal, applicability uncertainty, not-known authority/delivery and not-disclosed resources distinct.','A bounded account can remain useful without filling every view or requiring confidential proof.'],
  forbidden_inferences=['Unknown approval means pending, no approval required or concealed refusal.','Withheld resources mean no funding or zero cost; no measured result means no benefit.','A future or interim external statement makes a new project, hire or platform mandatory, or extends the proposed cohort.'],
  expected_analyst_output='A constructed partial brief records exactly what is known, the distinct missingness and any permissioned existing route, leaving applicability and employer action unresolved.',
  remaining_gap='Only suitable later evidence can establish applicability or the missing facts; refusal is honoured and no further disclosure demand is imposed.',
  views_stressed=['need','authority','support','states','next_action'],
  supporting_claim_ids=['CLM-0365','CLM-0366','CLM-0401','CLM-0405','CLM-0408','CLM-0409','CLM-0428'],
  failure_signal='The framework requires every field, imputes a status/value or treats an external signal as observed internal commitment.'),
]
for x in rows:
    x.update(evidence_type='constructed_internal_route',original_practitioner_observation=False,
             actual_employer=None,participant_id=None,actual_case_id=None,
             numerical_result=None,executed_against_final_R08_framework=False,
             new_mandatory_questions=0,validated_predictive_result=False)
    assert set(x['supporting_claim_ids'])<=claims,x['route_id']

collisions=[
 dict(collision='Need versus chosen response',revision='Keep a neutral task/outcome statement distinct from current arrangement, feasible alternatives and selected route. No-change and pre-proposal routes must remain usable.'),
 dict(collision='Authority versus resources versus readiness',revision='Give approval/authority, funding/resources and release/delivery their own scope/date/knowledge basis. No single progress status or compulsory approval ladder.'),
 dict(collision='Whole programme versus component',revision='Attach status to its exact object. Retained and changed elements, or stopped and continuing components, can coexist.'),
 dict(collision='Importance versus sequence',revision='A later milestone can reflect dependency or BAU capacity. Record the actual reason without inferring importance, funding or optimality.'),
 dict(collision='Next action versus proven remedy',revision='Offer an evidence/decision need conditional on scope and permission. Keep proposed response, actual action and assessed effect separate; a legitimate stop or retention needs no conversion.'),
 dict(collision='Completeness versus knowledge/disclosure',revision='A useful partial brief must be possible. Preserve not known, not measured, not applicable and not disclosed without demanding confidential amounts or identifying data.'),
]
out=dict(schema_version='1.0',date='2026-10-29',module_id='R08',status='constructed_route_design_ready_for_parent_framework_walkthrough',
 scope='Internal constructed counterexamples for a compact non-linear decision canvas. Neither collected cases nor practitioner validation.',
 route_count=len(rows),framework_view_labels_are_provisional=True,
 provisional_view_labels=['need','current_basis','options','authority','support','states','next_action'],
 no_mandatory_sequence=True,no_scores_or_market_estimates=True,no_extra_mandatory_questions=True,
 original_participant_observations=0,actual_case_records=[],forecast_calculations=[],financial_inputs=[],external_actions=[],
 routes=rows,framework_collisions_and_revisions=collisions,
 next_gate='Parent maps these expected invariants to the actual R08 draft, records route-by-route results/corrections and obtains independent review. Internal walkthroughs do not replace eligible permissioned practitioner integration or final client/rights review.')
(BASE/'constructed-routes.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n')
md='''# R08 constructed counterexample plan

29 October 2026. Internal design input for the draft Payroll Investment Decision Framework. These ten scenarios are deliberately constructed. They are not actual employers, interviews, quotations, observed outcomes, financial inputs or evidence that the framework works for practitioners.

## Purpose and use

The compact canvas should help explain a specific need or decision without forcing every account through purchase approval, new funding and a successful implementation. It should permit entry at any relevant view and leave information unknown or undisclosed. The provisional views are need, current basis, options, authority, support, states and next action; the parent may combine labels as long as their distinctions survive.

Each route in the [structured plan](constructed-routes.json) supplies only its stated premises. The expected output is a permissible analytical brief, not a fabricated company finding. A failed invariant should lead to a revision of the canvas. None of these walkthroughs has yet been executed against the final R08 draft.

| Constructed route | What it challenges | Minimum permissible result |
| --- | --- | --- |
'''
for x in rows:md+=f"| {x['route_id']}: {x['title']} | {x['failure_signal']} | {x['expected_analyst_output']} |\n"
md+='''
## Cross-route design refinements

'''
for x in collisions:md+=f"- **{x['collision']}:** {x['revision']}\n"
md+='''
## Evidence fit and boundaries

The claim links explain which earlier safeguards the constructed tests challenge. They do not turn the hypothetical premises into evidence. In particular, public programmes, supplier declarations, government management guidance and researcher design applications have different purposes. Existing numeric holds are not used as supporting numeric inputs. No source rate, threshold, forecast, score or benefit calculation is introduced.

The output should allow a concise account of what is known, which actual work or component it concerns, what is unestablished and the next relevant evidence or decision. It must not require all optional subfields, a complete budget/committee history, exact personal/company details or a new compulsory question. Existing Q005 still covers up to two unaided organisational priorities, and the fourteen core questions remain unchanged.

The parent should record actual walkthrough results only after applying these premises to the draft framework. Those are internal consistency demonstrations, not validation of effectiveness, causation, completeness, practitioner comprehension or commercial value. The agreed original contributor work and final client/factual/rights review remain separate gates. No external action occurred.
'''
(BASE/'COUNTEREXAMPLE-PLAN.md').write_text(md)
print(json.dumps({'status':'constructed_design_saved','routes':len(rows),'all_claim_references_resolve':True,'original_observations':0,'external_actions':[]},indent=2))
