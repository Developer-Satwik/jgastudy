from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'03-report/research-notes/r07-second-check'
def read(p):return json.loads((ROOT/p).read_text())
def write(p,d):(ROOT/p).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n' if not isinstance(d,str) else d)
m=read('08-qa/R07-second-check-record-map.json');cs=m['claim_map']
def cc(*x):return [cs[k] for k in x]
bridge=read('03-report/research-notes/r07-second-check/competitors/prior-study-bridge.json')
conditions=[
 dict(condition_id='C01',title='Origin and material revision',selective_use='Where the history matters, establish whether the stated priority is new, continuing, re-scoped or re-timed, its last evidenced state and the actual reason for a material change.',boundary='Repeated themes are not matched employer histories; a passed target date does not establish later delivery, persistent delay or failure. Do not require a complete project archive.',claim_ids=cc('H7S-C01','H7S-C02','H7S-C04')),
 dict(condition_id='C02',title='Sequence beside ongoing work',selective_use='Where a milestone depends on other work or capacity, record the actual dependency, whose action matters and the next relevant review or decision.',boundary='Later order is not proof of lower importance, rejection or no funding. A government management framework is not an observed private-payroll rule; no forced portfolio rank or optimal sequence.',claim_ids=cc('H7S-C03','H7S-C04','R7R-C01','R7R-C03')),
 dict(condition_id='C03',title='Actual capability, account and service scope',selective_use='For a feature/update priority, establish relevant task, account/service scope, known inclusion/access, released versus future availability, configuration/use and who must act.',boundary='Supplier declarations, entitlement, release, installation and useful operation are separate facts that can coexist across tasks. No product trial, universal capability, zero total cost or inferred new purchase.',claim_ids=cc('M7S-C01','M7S-C02','M7S-C03','M7S-C04','M7S-C05')),
 dict(condition_id='C04',title='Needed work and capability before a chosen route',selective_use='Keep the actual work, role/remit, performing party and known resources separate from a proposed hire, learning, process, retention or tool response; distinguish employer/team and geography units.',boundary='Recruiter advice, hosted account, service promise and salary inputs are not funded employer demand, available candidates or validated remedies. Constructed prompts preselect routes and do not validate them.',claim_ids=cc('C7S-C01','C7S-C02','C7S-C03','C7S-C04','C7S-C05','C7S-C06')),
 dict(condition_id='C05',title='Whose outcome and whose next action',selective_use='Where another function, provider, client or affected user matters, distinguish the contributor’s stated value from evidence about that task/outcome and the condition another party actually controls.',boundary='Do not assume misalignment, user satisfaction, contractual responsibility or permission. No supplier/employee cohort expansion, additional interview obligation or full stakeholder census.',claim_ids=cc('M7S-C05','R7R-C02','R7R-C04')),
]
for c in conditions:c.update(mandatory=False,scored=False,validated=False)
model=read('03-report/R07-priority-map.json')
model.update(cross_cutting_conditions=conditions,second_challenge_status='integrated_desktop_draft_independent_review_pending',second_challenge_review_basis='Independent integrated review pending; root exact saved-data linkage verification retained separately.',second_challenge_supporting_claim_ids=list(cs.values()),additional_mandatory_questions_from_second_challenge=0,prior_prompt_scenarios_are_constructed=True,prior_recommendation_counts_reused=False,prior_model_reruns=False,unaided_participant_priorities_first=True,second_challenge_selected_question_ids=[q['question_id'] for q in bridge['questions']],second_challenge_selected_saved_answers=bridge['selected_total_answers'],second_challenge_new_public_employer_histories=0,second_challenge_blank_context_template={k:None for k in ['contribution_id','priority_origin_or_material_revision','last_evidenced_state','actual_dependency_and_sequence','account_task_access_and_availability','needed_work_and_chosen_route','affected_party_and_knowledge_basis','next_review_or_action','evidence_and_permission']})
write('03-report/R07-priority-map.json',model)

table='| Selective refinement | Why it matters | Boundary |\n| --- | --- | --- |\n'
for c in conditions:table+=f"| {c['title']} | {c['selective_use']} | {c['boundary']} {', '.join(c['claim_ids'])}. |\n"
readout='''# R07 second challenge: what changes a priority into the next action

29 October 2026. Internal integrated desktop challenge; independent integrated review pending. Requested after the first R07 pass. No original practitioner evidence or external contact.

## Result of the challenge

The first-pass distinction between stated priority, commitment, resources and result still holds. The additional lenses sharpen five conditions: the origin of a priority, its sequence alongside ongoing work, actual usable capability, the underlying work before choosing a response, and whose outcome/action is involved.

This makes the report more practical. A useful explanation is not merely “integration was a priority but was delayed.” It should identify the concrete task, what was already known or available, the actual dependency and next decision. This example describes the analytical approach, not a collected case or evidence that all delays are justified.

## Historical lens: recurring themes do not measure the same employer's progress

CIPP2020 expectations about transactional work and skills differ from CIPP2024 current AI/RPA use and perceived pressure. The populations, task definitions, measures and linked respondents do not establish a matched ambition-to-investment history. No subtraction, progress gap, causal story or funded share is adopted. Reappearing “automation” could refer to different work or an ongoing priority; the actual explanation must be established. @H1@, @H2@.

LFB's existing2025 programme report provides a narrower concrete contrast: phase2 depends on phase1 and is scheduled alongside ordinary work. It concerns specific HR modules in one combined HR/payroll programme. This is declared sequencing, not proof of low importance, no funding, an optimal plan or later completion. A passed prospective2026 date is not a new observed outcome. No new employer history is added. @H3@, @H4@.

## Market lens: an included feature is not an implemented improvement

FreeAgent's feature declaration and setup route illustrate that advertised inclusion and the relevant account/access/configuration conditions are different facts. No actual account, filing, quote or total-cost claim is tested. A next action could be establishing existing capability rather than assuming replacement; that remains a case hypothesis, not a finding of unused features. @M1@, @M4@.

Moneysoft separates update prompts/checks from a June2026 statement about a future BiK update. A roadmap does not prove shipment, local installation, useful operation, employer resources or legal readiness. BrightPay's own-employer and multiple-client routes also show why the provider's work and a client's priority can have different owners and beneficiaries. Neither route is evidence of observed misalignment or market prevalence. @M2@, @M3@, @M5@.

## Specific competitor and JGA check

The following are source-scoped views that challenge a hiring-only interpretation. They are not a supplier ranking or six independently measured markets.

| Firm/source | Relevant observation | Use in R07 |
| --- | --- | --- |
| Portfolio Payroll / The Portfolio Group | Advice includes mentoring, communication and process work without necessarily introducing technology; Canadian author context retained. | Consider needed work and existing capability, without treating indexed advice as UK funded demand. @C1@. |
| Frazer Jones | Written summary of a named leader's interview describes rotation, shared learning, communication and review. Audio uninspected. | An illustrative secondary account, not a proven retention intervention or original JGA contribution. @C2@. |
| Oakleaf Partnership | March2026 commentary describes blended payroll/benefits/reward/HR roles, without an inspected prevalence method. | Establish actual remit; reward spending and payroll-function investment are different. @C3@. |
| Middlemore | Declares assessment of work, technical capability, judgement and influence beyond title. | Role title alone cannot define the capability needed or prove a necessary hire. @C5@. |
| Hays | Salary inputs differ from its employer/employee survey and underlying period. | Do not convert broad salary/hiring context into an approved payroll priority. @C4@. |
| Robert Half | Projected starting salaries differ from its non-salary survey. | No source figure, employer budget, staffing availability or payroll subgroup forecast transferred. @C4@. |
| JGA | Tailored UK/global talent acquisition is its declared proposition. | A possible response after defining the need, rather than the report's predetermined answer. @C5@–@C6@. |

Preserve the actual service/task/geography and commercial interests. Portfolio's indexed body and Frazer's reader notes are not fresh retained raw originals; JGA's reused reader notes likewise remain labelled. The market declarations do not independently validate any supplier effect.

## Earlier prompt study: use its scenarios to challenge our assumptions

The bridge uses four exact constructed questions, each with eight saved answers from four tools/two repeats, giving32selected texts. No model was rerun. Source-capture limits from the complete earlier dataset remain separate from this subset.

| Question | What the researcher already specified | What cannot be inferred |
| --- | --- | --- |
| S03-A | US employer, US-based Payroll Director and recruitment. | Real expansion, employer priority or a need to hire. |
| S07-A | Medium-sized UK employer, resignation and permanent replacement. | Representative UK replacement demand or that retention/revised work was evaluated. |
| S08-C | US parent, UK work base and Head of EMEA Payroll; explicit evidence request. | Headquarters equals payroll jurisdiction, or verification language arose unaided. |
| S11-A | Growing business, small UK payroll team, workload and permanent extra specialist. | Small team means SME employer, or a hire is the only feasible response. |

These are useful contrasting frames, not original buyer observations. No recommendation counts, generated salary/rules/candidate assertions or visibility rankings become evidence of demand, funded priority, supplier quality or remedy effectiveness. The independently authored bridge is root-checked against original text/hash/index/date/status records; that is integrity verification, not validation of every model answer or citation. @C6@. See the [bridge verification](../08-qa/R07-prior-study-bridge-check.md).

## Portfolio, affected-user and alternative-response lenses

Government project-delivery guidance considers existing work, capacity, dependencies and review. Government digital guidance uses performance/user evidence and connected service responsibilities for improvement. Both are normative contexts, not private-employer payroll requirements or observed results. The useful adaptation is selective: clarify what must happen first, what is known about the affected task and whose action controls the next step. No full portfolio, rigid review timetable, stakeholder census or additional interviews are required. @R1@–@R4@.

## Changes applied under the unchanged instrument

'''+table+'''
The five conditions supplement, rather than replace, the first-pass six priority dimensions, six context dimensions, four comparison claim purposes and blank templates. Existing Q005 still asks for up to two organisational priorities over12–24months, unaided first. There is no extra compulsory question, ordinal status ladder or score. Actual practices and source expectations are kept separate; not known, not measured, not applicable and not disclosed remain different.

## What remains unestablished

We do not have permissioned original cases showing the actual relative priority, access/configuration, changed resources, alternative response, affected-user outcome or next-decision reason. Six to ten purposive contributions will support careful case explanations, not representative sector/size/country percentages. Published advice and service declarations cannot fill those arrays or expand the unapproved proposed cohort.

No future policy statement, supplier promise, old target date or source silence is promoted into a delivered outcome. Existing Moorepay/Deloitte/UI holds remain, including the new first-pass branding/customisation conflict. No prices, statutory rates, salary values, numerical forecasts or Table inputs are added.

## Evidence and verification

- [Historical challenge](research-notes/r07-second-check/history/HISTORY-CHALLENGE.md)
- [Market challenge](research-notes/r07-second-check/market/MARKET-CHALLENGE.md)
- [All-six-comparator/JGA challenge](research-notes/r07-second-check/competitors/COMPETITOR-CHALLENGE.md)
- [Prioritisation and user challenge](research-notes/r07-second-check/root/PRIORITISATION-AND-USER-CHALLENGE.md)
- [First-pass snapshots](research-notes/r07-second-check/before-review/manifest.json)
- [Canonical second-challenge map](../08-qa/R07-second-check-record-map.json) and [retained-file hashes](../08-qa/R07-second-check-captures.json)

Original captures, reader notes, parsed text and PDF renders retain their distinct provenance. Reuses do not create new studies or employers. Independent integrated review and final preservation checks are required before closing this challenge. Then R08 can begin preparatory synthesis; final conclusions still require practitioner integration and final-use review. Nothing sent.
'''
replacements={'@H1@':cs['H7S-C01'],'@H2@':cs['H7S-C02'],'@H3@':cs['H7S-C03'],'@H4@':cs['H7S-C04'],'@M1@':cs['M7S-C01'],'@M2@':cs['M7S-C02'],'@M3@':cs['M7S-C03'],'@M4@':cs['M7S-C04'],'@M5@':cs['M7S-C05'],'@C1@':cs['C7S-C01'],'@C2@':cs['C7S-C02'],'@C3@':cs['C7S-C03'],'@C4@':cs['C7S-C04'],'@C5@':cs['C7S-C05'],'@C6@':cs['C7S-C06'],'@R1@':cs['R7R-C01'],'@R2@':cs['R7R-C02'],'@R3@':cs['R7R-C03'],'@R4@':cs['R7R-C04']}
for k,v in replacements.items():readout=readout.replace(k,v)
write('03-report/R07-SECOND-CHECK-READOUT.md',readout)
for rel in ['03-report/R07-DESKTOP-READOUT.md','03-report/R07-CONTEXTUAL-PRIORITIES.md','03-report/modules/R07-priorities-and-contextual-differences.md']:
 p=ROOT/rel;t=p.read_text();marker='\n## User-requested second challenge'
 assert marker not in t, 'Do not rebuild after second-challenge integration has been reviewed'
 prefix='R07-SECOND-CHECK-READOUT.md' if '/modules/' not in rel else '../R07-SECOND-CHECK-READOUT.md'
 t+='\n## User-requested second challenge\n\nHistorical, segmented-market, all-six-comparator/JGA, prior-prompt and affected-user checks add five selective conditions: priority origin/revision, sequence beside ongoing work, actual usable capability/access, needed work before a chosen response, and whose outcome/action matters. First-pass dimensions, blank templates and fourteen questions remain unchanged. No original observations, market estimates or model reruns. Independent second-challenge review pending.\n\n'
 t+=f'[Second-challenge findings]({prefix}) give the evidence, specific competitor distinctions and saved-study boundaries.\n'
 if rel.endswith('R07-CONTEXTUAL-PRIORITIES.md'):t+='\n'+table
 p.write_text(t)
print(json.dumps({'status':'R07_second_integrated_draft_ready','source_candidates':len(m['source_map']),'claims':len(cs),'selective_conditions':len(conditions),'selected_prompts':len(bridge['questions']),'saved_texts':bridge['selected_total_answers']},indent=2))
