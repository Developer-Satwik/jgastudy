from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
def read(p):return json.loads((ROOT/p).read_text())
def write(p,d):(ROOT/p).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
m=read('08-qa/R06-second-check-record-map.json');cm=m['claim_map'];sm=m['source_map']
def C(*x):return [cm[v] for v in x]
conditions=[
 dict(condition_id='C01',name='Feasible options at the dated event',establish='Which alternatives were practically available then, what maintaining service required and which conditions would persist under another option.',inference_limit='A later option set or result does not establish earlier irrationality. A new supplier does not automatically remove upstream data or organisational conditions.',supporting_claim_ids=C('H6S-C01','H6S-C02','H6S-C03','H6S-C04','M6S-C07')),
 dict(condition_id='C02',name='Last evidenced state and observation boundary',establish='Last observed event/date, source publication/knowledge basis, forecast versus observed milestones and what later outcome remains unestablished.',inference_limit='An elapsed forecast date is not evidence of success, continued delay or abandonment. Repeated documents about one programme are not independent employers or a market trend.',supporting_claim_ids=C('H6S-C02','H6S-C05')),
 dict(condition_id='C03',name='Distinct lifecycle dates and usable receiving arrangement',establish='Product/service, processing/support eligibility, commitments, access/export, receiving setup and first live run, with the relevant owner/date only where material.',inference_limit='Same supplier is not necessarily same product; read-only access is not supported processing or a proven secure permanent archive; declared export is not verified receiving-service readiness.',supporting_claim_ids=C('M6S-C01','M6S-C02','M6S-C03','M6S-C04','M6S-C05','M6S-C06','M6S-C07')),
 dict(condition_id='C04',name='Other-party commitment and continuing knowledge',establish='For a relevant talent option: employer approval/offer, the candidate or other party’s actual agreement/start, handover and continuing receiving-team knowledge/ownership.',inference_limit='Approval to recruit, verbal acceptance, start and useful enduring capability are different events. No current candidate availability, universal interim duration or hiring necessity follows.',supporting_claim_ids=C('C6S-C01','C6S-C02','C6S-C03','C6S-C04')),
 dict(condition_id='C05',name='Completion for the affected user and task',establish='Relevant user/cohort, current task and needed historical evidence, supported channel and receiving service/help owner after change or retirement.',inference_limit='Contractual exit or a new portal alone does not establish usable access, harm-free transition or satisfied needs. No mandatory new user interviews, unlimited archive or legal retention rule introduced.',supporting_claim_ids=C('R6R-C01','R6R-C02','R6R-C03','M6S-C06'))]
for x in conditions:x.update(mandatory=False,scored=False,remedy_validated=False)
f='03-report/R06-outcome-map.json';d=read(f)
d['second_challenge_date']='2026-10-29';d['second_challenge_status']='integration_pending_scoped_peer_review';d['cross_cutting_conditions']=conditions
d['second_challenge_contexts']=[dict(context_id='SC01',name='London Fire Brigade dated authorisation/reset history',source_ids=[sm['H6S-S01'],sm['H6S-S02']],claim_ids=C('H6S-C01','H6S-C02','H6S-C03'),independent_employer_histories=1,original_JGA_contribution=False,initial_authorisation_signed_on='2021-03-02',initial_page_published_on='2021-07-06',reset_report_remote_signature_on='2025-12-18',later_go_live_observed=False,later_outcome=None,normalised_current_proposal_disposition=None,forecast_dates_are_not_observed_events=True)]
d['second_challenge_blank_context_template']={k:None for k in ['case_event_id','feasible_options_as_of','conditions_persisting_across_options','last_evidenced_event_and_date','source_publication_and_knowledge_date','forecast_and_observation_boundary','processing_support_commitment_access_dates','receiving_setup_and_first_run','other_party_agreement_and_start','handover_knowledge_and_owner','affected_user_task_channel_historical_need','remaining_unknowns']}
d['additional_mandatory_questions_from_second_challenge']=0;d['prior_prompt_scenarios_are_constructed']=True;d['prior_recommendation_counts_reused']=False;d['unaided_participant_priorities_first']=True;d['prior_study_bridge']='03-report/research-notes/r06-second-check/competitors/prior-study-bridge.json'
d['second_challenge_specific_exclusions']=['No expired target treated as actual later success, delay or abandonment','No public programme history or supplier declaration as market prevalence','No supplier retirement implies mandatory purchase of that supplier replacement','No read-only/export guarantee as tested secure usable handback','No candidate offer/acceptance/start or knowledge-transfer advice as observed capability','No recruitment premise from constructed prompts as actual demand or barrier evidence','No government retirement/redirect timings or legal archive/retention obligation transferred','Screened Cambridge general payslip declaration excluded from claims; no old tax/security advice adopted']
d['supporting_claim_ids']=list(dict.fromkeys(d['supporting_claim_ids']+list(cm.values())));write(f,d)
readout='''# R06 second challenge: what makes a choice possible, and when is change complete?

29 October 2026. Internal desktop challenge. Scoped peer review and root verification pending. No new practitioner, product trial, forecast, client approval or external contact.

## What changed

The first pass correctly separated option, dated disposition, implementation and benefit. The second check adds five selective conditions: feasible alternatives at the time; the last evidenced state; distinct lifecycle dates and usable receiving arrangements; other-party commitment and knowledge continuity; and completion for affected users. These sit across the existing nine [matrix rows](R06-BARRIER-RESPONSE-MATRIX.md), not another questionnaire or score.

## Historical and later-state lens

London Fire Brigade's 2021 authorisation describes earlier continuation/workarounds and assesses unchanged, upgrade and shared-service routes in its then context. A signed December 2025 report then records postponed rollout, a reset, additional oversight and delivery support, and continued legacy maintenance while retaining iTrent as the intended solution. This is one programme across dates, not two independent employers. CLM-0367–0368.

The later report describes a narrowing support horizon and the effort of alternative procurement/transition. It also expects the same legacy-data issues to affect another replacement system. That is the employer's stated assessment, not independently proven inevitability. It challenges a simple “switch supplier to remove the barrier” response. Establish which condition belongs to the incumbent, the proposed option or the employer's own upstream work. CLM-0369–0370.

The report's future milestones remain forecasts. A target date having passed does not independently establish go-live, continued delay or abandonment. Record the last evidenced position and what later evidence is absent. No deadline is converted into an actual event, no hindsight judgement is made and no fixed parallel-run rule is imported. The 2021 signed date, later publication and 2025 remote signature remain separate. CLM-0371.

## Current market and lifecycle lens

Three supplier declarations add different boundaries:

| Inspected offer or guidance | Useful distinction | Limit |
| --- | --- | --- |
| BrightPay UK Desktop-to-Cloud migration hub | Retaining a supplier can still require a different product/subscription and migration. Own-employer and bureau routes differ; assistance can depend on receiving setup. | The declared retirement/migration offer does not prove every customer's successful move, feature parity or that its replacement is the best/legally required option. CLM-0372–0373. |
| IRIS Earnie end-of-life guide | Ending supported processing differs from declared read-only/report export. The guide also warns about security monitoring ceasing and recommends external preservation. | A January 2026 cover and relevant pages govern this reading, not a date inferred from the filename. No permanent secure archive, actual defect or completed receiving-system import is established. CLM-0374. |
| Sage UK cancellation page | Subscription activity/expiry and data access through the solution are distinct; product-specific routes matter. | The named context is not all Sage products, regions or customer contracts; no numerical notice or tested UI adopted. CLM-0375. |

Re-read Payfit terms likewise distinguish cessation, retrieval, client retention and filing-agent access tasks. The previously retained version/reader discrepancy and executed-contract uncertainty remain. CLM-0376.

The analytical refinement is to separate live payroll operation, access to needed historical evidence and usable receiving arrangements. Processing/support eligibility, commitment, export/access, setup and first live run need not share one date. An export alone proves neither the right data nor permissions, reconciliation or usable service. Equally, a new system need not ingest every historical record if another appropriate arrangement meets the actual need. No blanket lock-in, unlimited archive, legal opinion or cost estimate follows. CLM-0377–0378.

## All six competitors and JGA: broaden beyond software

The talent/service check keeps payroll investment wider than a platform purchase:

- Portfolio's declared recruitment process separates employer offer, candidate verbal acceptance, contract/start, onboarding and aftercare. Approval to recruit is not agreement by the other party or a person doing useful work. Its counteroffer discussion is process advice, not an observed reason a hire stalled. CLM-0379.
- Robert Half's June 2026 finance advice addresses knowledge transfer before an interim leaves through review, mentoring/shadowing and debrief. It is not a demonstrated payroll result, required duration or guarantee of continuing knowledge. CLM-0380.
- Frazer Jones's named change case combines interim/permanent talent; Oakleaf, Middlemore and Hays describe different assignment or delivery routes. JGA's payroll proposition is another possible response. These are not proof of current candidate availability, funded demand or hiring necessity. CLM-0381.

The Frazer Jones case uses the prior original review plus a fresh indexed same-case body; a fresh full live reinspection was unavailable. Other source records similarly distinguish reader notes from retained originals. This is not a newly verified set of completed client engagements.

For a relevant talent option, distinguish employer commitment, candidate/other-party agreement and start, then the receiving team's knowledge and ownership after handover. Temporary support can bridge change or provide a defined service, but a departure or recruitment approval alone does not establish the lasting capability. No automatic permanent replacement, standard team size or six-month engagement follows. CLM-0382.

## Earlier prompt study: useful contrasts and built-in assumptions

The [limited saved-data bridge](research-notes/r06-second-check/competitors/prior-study-bridge.json) selects S07-D, S09-A and S10-C: three exact prompts, 24 saved answer texts across four tools/two repeats. They assume a resignation/permanent replacement, a provider transition/head appointment, or six-month interim cover alongside a permanent search.

These constructed premises cannot establish actual demand, why an employer retained or rejected a route, a feasible start/handover or necessary duration. Recurring advice or firm recommendations in the answers partly reflects what we asked. No recommendation counts, generated candidate/cost/tax claims or supplier outcome is transferred. The original study's source-capture limitations remain separate from full text availability. No question was rerun.

## Service-user lens: completion for whom?

GDS retirement guidance distinguishes a user need ending from a replacement service meeting it, and considers communication, API adjustment, assisted channels and information protection. It is public-service guidance, not a mandatory private-employer retirement process. Its displayed 2025 update changes a contact email; it does not establish a new substantive policy. CLM-0383.

The reused West Sussex notice offers specified new self-service access while stating that older payslips are not available in Oracle and providing support routes. It does not establish that every worker retained copies, could access the service, had another archive or suffered harm. CLM-0384.

Where material, identify the affected user/task, needed historical evidence, channel and receiving help owner. Contractual exit, record availability and practical access are different completion claims. This is a selective clarification under the existing questions, not a demand to interview every employee or retain everything indefinitely. CLM-0385.

## What to apply, and what remains open

Five optional conditions C01–C05 are now in the [structured map](R06-outcome-map.json) and practical matrix. The original nine rows, six first-pass employer contexts, notice context, fourteen core questions and client files are preserved. No original observations or Table financial inputs have been added.

For practitioners, assess the next specific choice using feasible alternatives, the actual lifecycle and whose work/access remains. For suppliers, distinguish customer-owned conditions and other-party commitments from issues your offer can address, then show evidence rather than promise a universal easy switch. For JGA, include talent and service continuity without steering every case toward a hire.

Actual recent private-employer declines/withdrawals, current later outcomes and demonstrated remedy effects still require permissioned original cases. Nothing in this check establishes market prevalence, a causal response, a supplier ranking or that every pause should be overcome. R07 follows this review: priorities and defensible contextual differences. Nothing has been sent to Nick.

Detailed strands: [history](research-notes/r06-second-check/history/HISTORY-CHALLENGE.md), [market](research-notes/r06-second-check/market/MARKET-CHALLENGE.md), [competitors/prior study](research-notes/r06-second-check/competitors/COMPETITOR-CHALLENGE.md), [user continuity](research-notes/r06-second-check/root/USER-CONTINUITY-CHALLENGE.md). Canonical mapping: `08-qa/R06-second-check-record-map.json`.
'''
(ROOT/'03-report/R06-SECOND-CHECK-READOUT.md').write_text(readout)
p=ROOT/'03-report/R06-BARRIER-RESPONSE-MATRIX.md';t=p.read_text().split('\n## Selective conditions from the second challenge')[0]
t+='\n## Selective conditions from the second challenge\n\nApply within relevant existing rows, after the unaided account. No new required questions, stages or score. See the [second-challenge findings](R06-SECOND-CHECK-READOUT.md).\n\n| Condition | Establish | Avoid inferring |\n| --- | --- | --- |\n'
for c in conditions:t+=f"| {c['condition_id']} {c['name']} | {c['establish']} | {c['inference_limit']} {'; '.join(c['supporting_claim_ids'])}. |\n"
t+='\nA last evidenced state is not automatically the current state. A proposed action is not an adopted remedy; a declared export or handover is not practical continuity for every user. Support, commitment, access, start and usefulness need source-specific evidence. The first-pass rows and blank event template remain unchanged.\n';p.write_text(t)
for rel,link in [('03-report/R06-DESKTOP-READOUT.md','R06-SECOND-CHECK-READOUT.md'),('03-report/modules/R06-staying-switching-delay-and-abandonment.md','../R06-SECOND-CHECK-READOUT.md')]:
 p=ROOT/rel;t=p.read_text().split('\n## User-requested second challenge')[0];t+=f'''\n## User-requested second challenge\n\nThe [second challenge]({link}) adds five selective conditions: feasible alternatives at each date; last evidenced state; distinct lifecycle dates and usable receiving arrangement; other-party commitment and knowledge continuity; and affected-user/task completion. Existing nine rows, first-pass contexts and fourteen core questions are unchanged. Scoped peer review and root verification are pending; no new fieldwork or external sending.\n''';p.write_text(t)
print('R06 second-challenge integrated draft ready; 5 optional conditions, first-pass rows and contexts unchanged')
