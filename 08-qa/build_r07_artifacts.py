from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
DATE = '2026-10-29'
mapping = json.loads((ROOT/'08-qa/R07-record-map.json').read_text())
C = mapping['claim_map']
def claims(*ids): return [C[x] for x in ids]
def write(path, data):
    (ROOT/path).write_text(json.dumps(data, indent=2, ensure_ascii=False)+'\n' if not isinstance(data, str) else data)

contexts = [
    ('C01', 'Population and unit', 'The payroll population actually within the contributor’s remit; one payroll, entity, country or group where known.', 'Do not substitute global workforce, headquarters, payroll-team size or an arbitrary size threshold.', ['CTX7-C03','CTX7-C05','METH7-C04']),
    ('C02', 'Working and pay arrangements', 'The relevant contractual pattern, variability and actual data/calculation task, if material.', 'A sector label cannot classify a worker, establish the applicable calculation or prove an investment need.', ['CTX7-C01','CTX7-C05']),
    ('C03', 'Jurisdiction and remit', 'The jurisdictions and responsibilities relevant to this work and the contributor’s knowledge.', 'Country count and headquarters do not define a common regime, tax outcome or priority ranking.', ['CTX7-C02','CTX7-C05']),
    ('C04', 'Delivery responsibilities and handoffs', 'The internal, provided and retained tasks affected by the priority.', 'In-house or outsourced alone does not establish responsibility, workload, dissatisfaction or the right response.', ['CTX7-C03','CTX7-C05','SIG7-C02']),
    ('C05', 'Decision and change context', 'Current service, proposed change and dated evaluation, authority, commitment, delivery and result.', 'Do not compare a wish with an implemented process as if they were the same outcome.', ['PRI7-C08','CTX7-C05','METH7-C03']),
    ('C06', 'Relevant timing', 'The actual horizon, applicable period, known deadline or operating calendar where it matters to the case.', 'One employer’s school-calendar account is not a universal sector migration rule or proof that delay was optimal.', ['CTX7-C04','SIG7-C03','SIG7-C07']),
]
comparisons = [
    ('observed_case_contrast', 'A contrast between actual collected cases', 'Describe the cases, relevant scope, their evidence and alternative explanations. No cases have yet been collected.'),
    ('source_supported_mechanism', 'A source-supported contextual mechanism', 'Explain why a condition can matter; do not infer how often employers prioritise or fund it.'),
    ('hypothesis_for_case_check', 'A hypothesis for later case checking', 'Label the proposed explanation and what would support or challenge it. It is not an observed result.'),
    ('unestablished_group_difference', 'A group difference not established', 'Preserve missing or non-comparable coverage; do not replace it with a stereotype, zero or assumption that groups are identical.'),
]
signals = [
    dict(signal_id='S01', title='SSP changes described as effective 6 April 2026', source_ids=['SRC-0215','SRC-0216'], claim_ids=claims('SIG7-C04','SIG7-C05'), external_status='current_official_guidance_context', organisation_status=None, application='Establish relevant workforce/task, actual changes, present evidence and any unresolved work.', boundary='Guidance only; no individual eligibility/rate determination, complete statute audit or observed employer compliance.'),
    dict(signal_id='S02', title='Phased benefits-in-kind preparation', source_ids=['SRC-0090','SRC-0091','SRC-0072','SRC-0092'], claim_ids=claims('SIG7-C01','SIG7-C02','SIG7-C03'), external_status='draft_interim_future_guidance', organisation_status=None, application='Establish relevant benefits/phase, data owners, provider handoffs, capability and next actual decision.', boundary='Specified April 2027 and April 2028 phases are future scope, not all benefits on one date, a launched November service or tested software capability. Recheck current detail before final use.'),
    dict(signal_id='S03', title='Synergy reported programme commitments', source_ids=['SRC-0075'], claim_ids=claims('SIG7-C06'), external_status='one_published_programme_account', organisation_status=None, application='Distinguish the reported approval/contract, funding envelope and departmental responsibilities from prospective gaps and benefits.', boundary='Reuse of one combined-function public programme. No monetary value, actual later spend, financial assurance or realised payroll benefit inferred.'),
]

model = dict(
    schema_version='1.0', module_id='R07', date=DATE,
    status='internal_desktop_synthesis_independent_integrated_review_pending',
    purpose='Distinguish what a payroll priority means, its organisational commitment and the defensible context of any comparison.',
    current_question_ids=['Q002','Q003','Q005','Q007','Q008','Q009','Q010','Q011','Q012','Q013'],
    primary_priority_question_id='Q005', maximum_selective_priorities=2, horizon_months=[12,24],
    fourteen_core_questions_unchanged=True, extra_mandatory_questions=0,
    unaided_priorities_first=True, prompted_themes_labelled=True,
    ordinal_status_ladder=False, mandatory_sequence=False, validated_priority_score=False,
    fields_are_selective_analyst_aids=True, confidential_documents_required=False,
    exact_private_amounts_required=False, original_practitioner_observations=0,
    participant_observations=[], completed_case_comparisons=[], forecast_calculations=[],
    financial_inputs_populated=False, subgroup_estimates=[], market_rankings=[],
    new_empirical_datasets=0, new_numeric_estimates=0,
    priority_dimensions=[
        dict(dimension_id='P01',title='Whose priority and what work',record='Person/team/employer/programme or published respondent population; specific task/outcome and decision unit.',claim_ids=claims('PRI7-C08','METH7-C03')),
        dict(dimension_id='P02',title='Time and provenance',record='Horizon, as-of date, actual source, direct knowledge, and unaided or prompted origin.',claim_ids=claims('PRI7-C08','METH7-C01','METH7-C03')),
        dict(dimension_id='P03',title='Evaluation, plan and authority',record='Known evaluation/plan/approval facts, their exact scope and date. Several can coexist or change; source silence remains unknown.',claim_ids=claims('PRI7-C01','PRI7-C08','METH7-C03')),
        dict(dimension_id='P04',title='Funding and practical resources',record='Known recurring operating resources, new allocation or proposal, protected time/capacity, owner and any unmet dependency; disclose only what is appropriate.',claim_ids=claims('PRI7-C06','SIG7-C06','METH7-C03')),
        dict(dimension_id='P05',title='Commitment, delivery and result',record='Actual procurement/other commitment, work delivered, affected users/task and intended versus assessed result, each with its own basis/date.',claim_ids=claims('PRI7-C03','SIG7-C05','SIG7-C06','METH7-C03')),
        dict(dimension_id='P06',title='What could change the priority',record='Contributor’s stated enabling condition, constraint, alternative or next decision; do not infer a remedy works.',claim_ids=claims('SIG7-C07','METH7-C03','METH7-C04')),
    ],
    context_dimensions=[dict(context_id=i,title=t,record=r,boundary=b,mandatory=False,scored=False,claim_ids=claims(*cs)) for i,t,r,b,cs in contexts],
    comparison_claim_purposes=[dict(claim_type=i,title=t,rule=r,ordinal=False,claim_ids=claims('METH7-C01','METH7-C02','METH7-C04')) for i,t,r in comparisons],
    planning_signals=signals,
    blank_priority_template={k:None for k in ['record_id','contribution_id','whose_priority','decision_unit','specific_task_or_outcome','horizon','as_of_date','source_and_direct_knowledge','unaided_or_prompted','evaluation_facts','plan_facts','authority_facts','funding_and_resource_basis','commitment_facts','delivery_facts','intended_result','assessed_result_and_basis','next_condition_or_decision','disclosure_permission']},
    blank_context_template={k:None for k in ['record_id','contribution_id','population_and_unit','working_pay_arrangements','jurisdiction_and_remit','retained_delivery_and_handoffs','decision_change_context','relevant_timing','missingness','publication_detail_permission']},
    blank_comparison_template={k:None for k in ['comparison_id','claim_purpose','cases_or_sources','comparable_work_scope_horizon_measure','observed_contrast','alternative_explanations','contrary_case','missing_coverage','permissible_inference','supporting_evidence']},
    missingness_values=['not_known','not_measured','not_applicable','not_disclosed'],
    numerical_holds=[dict(claim_id=C['PRI7-C07'],status='hold_numeric_reuse',subject='Moorepay branding/customisation prose13 versus chart12',client_numeric_reuse=False)],
    existing_holds_preserved=['CLM-0051','CLM-0052','CLM-0167','CLM-0168','CLM-0218'],
    supporting_claim_ids=list(C.values()),
    final_use_requires=['Eligible permissioned practitioner evidence','Client confirmation of proposed population and scope','Factual/currentness, attribution and rights checks','Disclosure and re-identification review','Integration and final report review'],
    no_external_sending_without_user_permission=True,
)
write('03-report/R07-priority-map.json',model)

write('03-report/R07-DESKTOP-READOUT.md', '''# R07: from stated priority to a practical decision

29 October 2026. Internal desktop synthesis; independent integrated review pending. This is the report module's evidence and analysis design, not completed practitioner research.

## What this step adds

The useful question is not simply which payroll themes sound important. It is what an organisation expects to do, what supports that expectation, and which conditions affect the next decision. A desired feature, a personal training plan, approved resources and an operating improvement can all be relevant, but they describe different things.

The inspected public evidence does not supply a common ranking of funded UK payroll priorities. The report can instead connect priority, operating context, authority, resources and result. This gives practitioners a clearer way to explain a need and suppliers a more accurate basis for understanding it. It does not assume that every priority needs a new system, provider or hire. CLM-0393, CLM-0398, CLM-0405, CLM-0408–0409.

## Findings that change how we use the evidence

| Evidence | What the original item supports | Consequence for this report |
| --- | --- | --- |
| Azets B1 and E1, original pages 11–12 | B1 bundles strategic importance, active review and investment; E1 asks about managing **or** investing in payroll. | Retain the exact frame. Neither identifies a separately approved project, allocation or purchase driver. CLM-0386–0387. |
| SD Worx full report, page 33 | Separate employer agreement statements concern exploring, investing, scaling and significant HR-AI outcomes. | No subtraction into a conversion funnel or assumption that the same organisations passed through stages. CLM-0388. |
| SD Worx payroll thematic report, page 11 | A payroll-priority list differs from broad urgent HR challenges and publisher advice. | Do not merge the lists into one ranking or call different question frames a numeric contradiction. CLM-0389. |
| Moorepay feature question | Respondents describe what they would most like from a provider. | Use as a hypothesis after unaided priorities, not a purchase, price acceptance or provider-change plan. CLM-0390. |
| CIPP qualification items, printed pages 15–16 | Employer support and personal undertaken/current/planned qualifications are separate measures. | Separate resources, personal intent, completed learning and usable capability. CLM-0391. |
| Published Synergy account | Reported approval/contract and funding responsibilities coexist with prospective gaps and benefits. | Funding, spend, delivery and realised benefit require their own scope and evidence. One programme remains one context. CLM-0404. |

No item percentages, cross-study averages, funded-market shares or forecasts are adopted. Published populations, fieldwork, interests and item/base limits remain in the linked strand notes and canonical records.

## A simpler analytical approach

Under the unchanged Q005, obtain up to two expected organisational priorities over 12–24 months before offering examples. For each, establish the specific task/outcome and whose priority it is. Then clarify only what is relevant and known: evaluation/plan/authority, money and practical capacity, actual commitment/delivery, intended and assessed result, and what might move the priority forward or reduce its importance.

These are parallel facts, not a mandatory ladder or a maturity score. Approved and being delivered can coexist; a useful improvement can use existing operating resources; an undisclosed amount is not proof of no funding. Unknown, not measured, not applicable and not disclosed remain distinct. No confidential budget document, precise headcount or complete committee map is required. CLM-0393, CLM-0408.

The [priority and context guide](R07-CONTEXTUAL-PRIORITIES.md) explains the selective record, comparison rules and reader use. The [structured map](R07-priority-map.json) keeps templates blank until original evidence exists.

## Context worth understanding

The actual payroll population, work/pay arrangements, relevant jurisdictions, retained service tasks, change stage and timing can make an issue relevant. A simple employer-size, sector or country label cannot establish what is funded or which response is suitable.

Official holiday-pay guidance illustrates dependence on the actual contractual pattern and applicable period. Cross-border guidance distinguishes territory, duration and coverage circumstances. Basic PAYE Tools has a bounded own-employer task scope. West Sussex's dated communication illustrates one employer's scale, reliable-payroll and school-calendar considerations. These support conditional explanations, not demonstrated sector/size investment differences or a universal complexity score. No calculation, individual classification or legal advice is adopted. CLM-0394–0398.

## Planning needs a date and an applicability check

HMRC and Acas guidance describe SSP changes effective on 6 April 2026. In this October review they are current operating context, not a new 2027 ambition. Eligibility and transitional conditions remain; guidance does not show what an employer implemented. CLM-0402–0403.

The inspected HMRC benefits-in-kind manual is draft/interim. It describes specified first-phase benefits from April 2027, most others from April 2028, with loans/accommodation voluntary. Data ownership, software, provider handoffs, training, communication and transition cash timing can matter. Its November 2026 service and April 2027 tools statements describe future availability as of this review; no launch or product test is assumed. This is conditional planning context, not full enacted-law assurance, a budget estimate or a mandate for a new hire/provider. Recheck applicable current detail before publication or action. CLM-0399–0401, CLM-0405.

## One additional number held back

Moorepay's annual prose and original feature chart disagree on branding/customisation: 13% versus 12%. CLM-0392 is held from numerical reuse; neither value is selected or averaged. The question's qualitative meaning remains usable. Existing Moorepay, Deloitte and UI-behaviour holds remain unchanged. This narrow conflict is not a claim that every value in the source is wrong.

## How this becomes valuable to JGA

The report can help a practitioner explain a concrete priority in organisational terms: what needs to improve, for whom, what is already supported, the remaining dependency and evidence needed for a decision. Suppliers can distinguish a general preference from a defined opportunity and show which actual work their offer addresses. JGA can connect capability and leadership to a specific evidenced gap without treating recruitment as the default answer.

Six to ten purposive contributions can support careful case explanations and contrasts, including contrary cases. They cannot supply representative UK sector rankings or national percentages of approved investment. No original contributions have yet been collected. The proposed cohort remains subject to client confirmation; public international examples do not expand it. CLM-0406–0409.

## Evidence trail and completion boundary

This pass adds four official source routes and 24 bounded claim/method/hold records, alongside explicit canonical reuses. Reused studies and programmes do not become new independent datasets. Original captures, selected extracts, PDF page renders and review logs remain distinct. Empty/blocked legislation and Powys attempts are excluded, not inspected source evidence.

- [Survey/item review](research-notes/r07/priorities/PRIORITY-EVIDENCE.md)
- [Context mechanisms](research-notes/r07/context/CONTEXT-EVIDENCE.md)
- [Dated planning signals](research-notes/r07/signals/PLANNING-SIGNALS.md)
- [Comparison method](research-notes/r07/root/PRIORITY-AND-COMPARISON-METHOD.md)
- [Canonical mapping](../08-qa/R07-record-map.json) and [capture hashes](../08-qa/R07-captures.json)

Next is R08 preparatory synthesis of the completed desktop modules. Final findings/framework still require permissioned practitioner integration and final-use checks. Fourteen core questions, eight client checkpoint files, scope and prior modules remain unchanged. Nothing has been sent.
''')

guide = '''# R07: priority and context guide

29 October 2026. Internal analytical aid, pending independent integrated review. The fields below are selective aids under the existing questionnaire, not extra compulsory questions or a validated scoring system.

## Start with the work and the decision

Keep the contributor's own wording first. Record whose priority is described, the specific improvement, the actual organisational/service unit and the relevant horizon. A public survey theme, a payroll leader's preference and their employer's committed work are different sources of knowledge.

The unchanged Q005 asks which improvements, if any, the organisation expects to prioritise in the next 12–24 months. Its existing probes allow up to two priorities and clarify status/funding separately. Preserve “no material improvement needed,” not known and rational retention; do not force a technology theme. Label examples or themes offered after the unaided answer as prompted. CLM-0393, CLM-0408.

| Selective analytical dimension | Useful record | Do not assume |
| --- | --- | --- |
| Whose priority / task | Person, team, employer or programme; specific task, users and intended improvement. | A personal interest is an employer commitment; similar theme labels mean the same work. |
| Horizon / provenance | As-of date, period, source/direct knowledge and unaided or prompted origin. | A survey access date is new fieldwork; a forecast date is an observed event. |
| Evaluation / plan / authority | The actual action, scope, known authority and date; preserve concurrent states. | A bundled strategic-status answer establishes an approved proposal. |
| Funding / resources | Known recurring/new resources, protected time, owner and remaining dependencies. | Every improvement needs a separate budget; amount withheld means unfunded. |
| Commitment / delivery / result | Each actual event and intended versus assessed result, with its own basis and scope. | Approval guarantees delivery, or operation guarantees the intended benefit. |
| What could change it | Actual enabling condition, constraint, alternative or next decision. | A suggested response is proven to remove the barrier. |

CLM-0386–0391, CLM-0393, CLM-0403–0405, CLM-0408 support these distinctions. They do not create a linear pipeline: evaluation, approval and delivery may concern different tasks or overlap. Existing R04–R06 maps supply decision rights, financial views and event/object distinctions; do not duplicate them as new questions.

## Use context only where it explains the case

'''
guide += '| Dimension | Establish if material | Boundary |\n| --- | --- | --- |\n'
for _,title,record,boundary,cs in contexts:
    guide += f'| {title} | {record} | {boundary} {", ".join(claims(*cs))}. |\n'
guide += '''
Do not infer private context from a public company profile or force exact sensitive figures. The contributor's remit can be narrower than the employer's full business. Detailed combinations of broad descriptors can identify a person in a small cohort; retain only what is permissioned and necessary to interpret the published case.

## Four kinds of comparison claim

'''
for _,title,rule in comparisons: guide += f'- **{title}:** {rule}\n'
guide += '''
These are different claim purposes, not an evidence-strength ladder. Check comparable work, service boundary, horizon, actual question/measure and knowledge basis before attributing a contrast to size, sector or geography. Explore alternative explanations and contrary cases. Sparse or absent groups remain gaps. No arbitrary minimum qualitative base, national percentage, country ranking, causal decomposition or saturation claim is introduced. CLM-0406–0409.

For a published numeric subgroup comparison, the relevant item, definition, period, group and valid bases/recruitment/weighting would need inspection. Overall country counts cannot stand in for an item's valid subgroup bases. We make no funded-priority subgroup estimates from the current material.

## Keep an external signal separate from employer commitment

| Source context | Dated external status | Case-level question it informs |
| --- | --- | --- |
| SSP | HMRC/Acas guidance describes changes effective 6 April 2026, retaining eligibility and transition conditions. | What relevant operating work actually changed, and what evidence supports present completion or remaining need? CLM-0402–0403. |
| Benefits in kind | Draft/interim phased future guidance; specified 2027/2028 scope, exclusions and dependencies. November 2026 services and April 2027 tools availability remain future statements at 29 October. | Which benefits/employees/phase and data handoffs apply; what task, capability, resources or next decision is actually known? CLM-0399–0401, CLM-0405. |
| Synergy | One published programme account separates approval/contract/funding responsibilities from prospective gaps and benefits. | Which commitment, resource and result does a given statement actually establish? No new case or monetary estimate. CLM-0404. |

A deadline or a published preparation instruction does not establish a new funded purchase, actual noncompliance or a mandatory technology/staffing solution. The SSP rows use official guidance, not a full primary-law audit; the BiK material remains interim. No rates, worker-specific determinations, tax advice, current software test or employer forecast is provided.

## Worked use without fabricated cases

If a future contributor says “integration is a priority,” keep the wording and establish the actual task and affected handoff. If they know it is in a plan but not how it is resourced, record both facts. Ask a relevant existing probe about what would move it forward; do not label it an active purchase or conclude budget is absent. This is an illustrative route, not a collected employer observation.

If two actual cases later differ, inspect their work and evidence before saying the difference is caused by sector. A school calendar can matter in one dated rollout account without proving a sector-wide priority or the best month for every migration. Conversely, no observed contrast does not establish that context never matters.

## Blank records and publication use

The [structured priority map](R07-priority-map.json) contains blank priority, context and comparison templates. All participant observations, completed case comparisons, forecasts, subgroup estimates and market rankings remain empty. Record not known, not measured, not applicable and not disclosed separately rather than impute a value.

Use later permissioned accounts to produce concise case explanations: priority, why it mattered in that context, what was known about support/resources, what happened, and the remaining decision. Cite the actual case or source beside the claim. A recurring theme may inform the discussion without becoming a national investment ranking. Public-source context and original contributions remain visibly different.

No publisher statistic, employment rule or service declaration is automatically approved for final use. The new Moorepay branding/customisation number remains held (CLM-0392), alongside existing holds. Original practitioner integration, factual/currentness and rights checks, confidentiality and client review are still required. Nothing has been sent.
'''
write('03-report/R07-CONTEXTUAL-PRIORITIES.md',guide)

write('03-report/modules/R07-priorities-and-contextual-differences.md','''# R07 Priorities and contextual differences

Desktop synthesis prepared 29 October 2026. Independent integrated review and preservation gate pending.

## Decision and contribution

What does a stated payroll priority mean, what organisational commitment supports it, and which contextual comparisons are justified?

Published importance, feature desire, employer support, personal intent, plan, approval, funding, delivery and assessed benefit remain separate claims. The useful report contribution is a traceable explanation of the concrete work, its context and the next decision, rather than a synthetic ranking of funded UK priorities. CLM-0386–0393, CLM-0408–0409.

The existing Q005 allows up to two unaided organisational priorities over 12–24 months, clarifying status and funding separately where relevant. Six selective analytical dimensions capture whose priority/task, time/provenance, evaluation/plan/authority, resources, commitment/delivery/result and changing conditions. They can overlap; there is no status ladder, score or compulsory new questionnaire.

Six optional context dimensions cover population/unit, working/pay arrangements, jurisdiction/remit, retained delivery/handoffs, decision/change context and relevant timing. Mechanisms in official guidance and one employer's timing account are not proven differences in sector, size or country priorities. Actual case contrast, contextual mechanism, later hypothesis and unestablished group difference are different claim purposes. CLM-0394–0398, CLM-0406–0409.

## Evidence and boundary

Four new official HTML routes and explicit canonical reuses support 24 bounded claim/method/hold records. The inspected BiK material remains draft/interim future planning context, while SSP guidance describes April 2026 changes as already effective. Neither establishes an employer's actual resources, implementation or need for a supplier/hire. No rates, individual legal determination, numerical forecast, funded share or product trial is adopted. CLM-0399–0405.

The Moorepay branding/customisation prose/chart conflict is held from numeric reuse (CLM-0392). Existing holds remain. Published studies/programmes are not original JGA contributions, and reused routes do not add independent datasets. All original observations, financial inputs and completed case comparisons remain empty. Fourteen core questions, prior modules, scope and eight checkpoint files are preserved.

## Outputs and next gate

- [Desktop readout](../R07-DESKTOP-READOUT.md)
- [Priority/context guide](../R07-CONTEXTUAL-PRIORITIES.md)
- [Structured map and blank records](../R07-priority-map.json)
- [Evidence mapping](../../08-qa/R07-record-map.json)

Complete independent integrated review and preservation checks before closing desktop work. R08 can next prepare synthesis across the desktop modules; final framework/findings require actual permissioned practitioner evidence, client confirmation and final-use review. Nothing is sent without user permission.
''')
print(json.dumps({'status':'integrated_draft_ready_for_independent_review','files':4,'claims':len(C),'context_dimensions':len(contexts),'planning_contexts':len(signals)},indent=2))
