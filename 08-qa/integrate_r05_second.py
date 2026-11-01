from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
def read(p):return json.loads((ROOT/p).read_text())
def write(p,d):(ROOT/p).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
mp=read('08-qa/R05-second-check-record-map.json');cm=mp['claim_map']
def ids(*x):return [cm[v] for v in x]
conditions=[
 dict(condition_id='C01',name='Dated case and whole-decision boundary',domain_ids=['E01','E04','E05','E09'],establish='Appraisal version/date, actual option and payroll component/wider programme, material changes and next reconsideration point.',inference_limit='An old approval need not reflect current inputs; a later revision is not proof the earlier decision was irrational. No automatic expiry/full reapproval rule.',supporting_claim_ids=ids('R5H-C02','R5H-C03','R5H-C04','R5H-C05','R5C-C04')),
 dict(condition_id='C02',name='Who bears costs and who receives value',domain_ids=['E02','E03','E04','E06','E08'],establish='Relevant entity/team bearing money, work or risk; benefit recipient, timing, funding control and actual allocation/shortfall arrangement if material.',inference_limit='Aggregate net value does not establish each party affordability; do not infer conflict, prescribe equal sharing or invent funding transfers.',supporting_claim_ids=ids('R5H-C02','R5H-C04','R5H-C06')),
 dict(condition_id='C03',name='Actual unit, retained work and lifecycle cash',domain_ids=['E02','E04','E06','E08'],establish='Applicable service/contract version, licence/payroll/employee/payslip/payment unit, task split, commitment/access/handback timing and any changed wage-funding timing.',inference_limit='Headcount is not a universal billing unit; ceasing use is not necessarily ceasing payment. Ordinary wage principal is not automatically additional transformation cost. No tariff/notice/credit or legal rule generalised.',supporting_claim_ids=ids('R5M-C01','R5M-C02','R5M-C03','R5M-C04','R5M-C05','R5M-C06','R5M-C07','R5M-C08','R5C-C05')),
 dict(condition_id='C04',name='Usable skill, time window and displaced work',domain_ids=['E02','E04','E06','E07'],establish='Specific expertise and usable time at relevant change/payroll windows, existing paid availability, extra cover and work displaced.',inference_limit='Annual hours or unchanged salary do not establish critical-time capacity, zero resource cost or cash release. No wage/contribution formula, permanent hire or staffing ratio imposed.',supporting_claim_ids=ids('R5R-C01','R5R-C02','R5H-C01')),
 dict(condition_id='C05',name='Benchmark and evidence fit',domain_ids=['E02','E03','E04','E06','E09'],establish='Edition, underlying period, role/remit, geography, pay/engagement basis, contributing population and evidence actually available for this claim.',inference_limit='Starting salary, day rate, survey opinion, advertised capability and delivered output are different inputs; no standard staffing-cost loading, availability or employer benefit inferred. Constructed evidence-request prompts cannot independently corroborate buyer priorities.',supporting_claim_ids=ids('R5C-C01','R5C-C02','R5C-C03','R5C-C05'))]
for c in conditions:c.update(mandatory=False,scored=False)
f='03-report/R05-evidence-map.json';d=read(f)
d['second_challenge_date']='2026-10-29';d['second_challenge_status']='internal_integration_pending_independent_review';d['cross_cutting_conditions']=conditions
d['second_challenge_reference_contexts']=[dict(context_id='SC01',name='NAO2012 selected centres, mixed outcomes',source_ids=[mp['source_map']['R5H-S01']],claim_ids=ids('R5H-C01'),original_JGA_contribution=False),dict(context_id='SC02',name='NAO 2016 transfer versus transformation and customer/centre business case',source_ids=[mp['source_map']['R5H-S02']],claim_ids=ids('R5H-C02'),original_JGA_contribution=False),dict(context_id='SC03',name='NAO 2022 avoided-cost comparison and cluster basis',source_ids=[mp['source_map']['R5H-S03']],claim_ids=ids('R5H-C03'),original_JGA_contribution=False)]
d['additional_mandatory_questions_from_second_challenge']=0;d['prior_prompt_scenarios_are_constructed']=True;d['prior_recommendation_counts_reused']=False;d['unaided_participant_priorities_first']=True
d['prior_study_bridge']='03-report/research-notes/r05-second-check/competitors/prior-study-bridge.json'
d['second_challenge_blank_context_template']={k:None for k in ['case_version_and_date','payroll_component_and_wider_programme','material_change_and_reconsideration_point','cost_work_risk_bearer','benefit_recipient_and_period','funding_remit_and_actual_allocation','billable_population_or_transaction','retained_work_and_acceptance','use_commitment_and_handback_dates','wage_principal_fee_and_funding_timing','required_skill_and_usable_window','existing_capacity_extra_cover_displaced_work','benchmark_edition_period_role_location_basis_population']}
d['second_challenge_specific_exclusions']=['No cross-programme public-audit sequence called a longitudinal employer or payroll-market trend','No Synergy numeric reconciliation or historical monetary total adopted','Payfit retained27October2026label versus older reader label: no inferred policy-change chronology or executed-contract applicability','Modulr repeated bundle quantity conflicts: no tariff or funding/interest estimate','Hays live 2026edition and RobertHalf live 2027edition retain own periods and populations; no standard loading or salary quote','Portfolio/FrazerJones reader extracts are not local raw originals; blocked fetch payloads excluded','Prior C prompts explicitly request evidence, so repeated verification advice is elicited, not independent demand evidence','No educational numerical examples or lost-contribution formula applied to payroll control work']
d['supporting_claim_ids']=list(dict.fromkeys(d['supporting_claim_ids']+list(cm.values())))
write(f,d)
readout='''# R05 second challenge: making the business case fit the actual decision

29 October 2026. User-requested internal desktop challenge. Historical, market, competitor/prior-study and usable-capacity lenses. Independent integrated review pending. No original practitioners, forecasts, prices, new questionnaire or external contact.

## What survived, and what changed

The first pass correctly separated whole-life resources, incremental cash and funding. It also separated cash savings from capacity and delivery from benefit. The second check strengthens its application: **a case must identify whose value, which dated choice, which actual service and what usable capacity its evidence supports**. A convincing aggregate forecast can still leave an unfunded transition, displaced operating work or an incomplete comparison.

Five selective conditions now sit across the existing nine domains in the [business-case checklist](R05-BUSINESS-CASE-CHECKLIST.md) and [structured map](R05-evidence-map.json). They are not new approval stages, required questions or a score.

## 1. Keep the version and comparison boundary visible

The historical checks distinguish a function transferred, a platform transformed, an operating service and an observed benefit. Those are different objects. NAO 2016 reports delayed transformation and legacy-maintenance costs alongside transferred functions. NAO 2022 challenges an avoided standalone-replacement comparison that omitted cluster costs and induced replacement of some already-cloud services; calculations also differed in basis. The lesson is a like-for-like net comparison, not a historical number to reuse. CLM-0324–0325.

Synergy's approved FBC2 summary records revised inputs after sequential procurement and prospective financial arrangements. A dated approval can be legitimate without proving that later assumptions are unchanged or benefits achieved. Record the version, option/scope, material changes and next relevant reconsideration point. Do not invent an expiry or require full reapproval for every change. CLM-0326–0327.

Frazer Jones's 2017 new-market/acquisition advice adds a commercial boundary: payroll readiness can be part of a wider acquisition or market-entry decision. Keep the payroll component's cost, readiness and outcome visible without presuming which function controls the date. CLM-0340.

The 2012, 2016, 2022 and Synergy materials concern different public strategies/programmes and combined back-office functions. They are not a repeated employer cohort, payroll-only failure rate or evidence that the market is improving/worsening. The 2012 summary also preserves a break-even exception; favourable and adverse evidence both matter. CLM-0323.

## 2. Identify who funds the work and who receives the benefit

The2016 integrated customer/centre business-case gap and Synergy's lead-department/departmental financial arrangements sharpen a missing analytical distinction. Total net value does not establish each team's affordability or access to funds. Identify the entity/team carrying money, work and risk, the recipient and timing of benefits, actual allocation/shortfall arrangements and the relevant funding authority. CLM-0324, CLM-0326, CLM-0328.

This is a selective analytical application, not proof of conflict or a mandatory internal transfer. In a small delegated choice one person or budget may cover everything; do not create an artificial committee. In a multi-entity change, a positive whole-programme figure must not obscure a department's unfunded implementation or retained work.

## 3. Match the economics to the service and commitment

Current public declarations illustrate materially different units and responsibilities:

| Context inspected | What the evidence can add | What cannot be inferred |
| --- | --- | --- |
| HMRC Basic PAYE Tools | A bounded no-licence-fee alternative still needs registration, installation, updating and operation. | Free complete payroll operation or suitability for every employer/bureau. CLM-0335. |
| Moneysoft named annual licence | Multiple-payroll entitlement differs from each payroll's staff limit, which includes leavers. | Current active headcount as a universal charging proxy, or an employer-specific quote. CLM-0329. |
| Payfit retained terms | Task/support allocation can retain client input, checks and approval; commencement, notice, access and handback conditions differ. | Support removes all work, delayed/no use cancels commitments, or these public terms establish a particular customer's legal position. CLM-0330–0331. |
| Modulr payroll payments | Payment-product units, funding and approval differ from payroll calculation and employee count. | A full payroll service, credit facility or additional investment equal to the wage bill. CLM-0333–0334. |

Separate fees, ordinary wage principal and any change in when/where funds must be available. Unchanged wages are not an incremental transformation expense, but a changed funding window can matter. No float period, interest, credit availability or cost estimate has been assumed. CLM-0336.

Payfit's inspected AI terms illustrate retained human verification and distinct administrator/employee controls. This is declared wording, not a UI/product trial, certification or wider market rule. The earlier Cintra universal-UI hold remains intact. CLM-0332.

The retained Payfit original displays 27 October 2026 while the reader initially returned an older label. No policy-change chronology is inferred. Modulr's repeated bundle quantities conflict, so no exact tariff is adopted. The prior BrightPay billing-period conflict and Moorepay saving/credit boundaries remain unchanged.

## 4. Test usable capacity, not just annual hours

ACCA's educational relevant-cost material distinguishes existing paid availability, additional labour and displaced work. It supports separating resource use, changed cash and opportunity. Its classroom assumptions and amounts are not payroll evidence. CLM-0342.

Our application is to identify the actual skill and usable time window, extra cover and displaced work. Hours released across a year do not alone establish that the relevant people can cover a migration or a critical payroll/payment deadline. An unchanged salary does not make capacity freely available; a booked salary allocation does not automatically become extra cash. Do not monetise missed controls using product-contribution examples or assume a hire is necessary. CLM-0343.

## 5. Match the benchmark to the claim

All six recruitment comparators and JGA were checked for the kind of evidence their public materials actually offer:

- Portfolio Payroll publishes salary/hiring resource routes; a catalogue does not establish the underlying method or a usable cost input.
- Frazer Jones supplies scoped payroll implementation advice; its historical article is not an observed 2026 employer outcome.
- Oakleaf and Middlemore describe talent/remit/assessment routes; declarations do not establish available people, assignment-specific cost or realised value.
- Hays separates salary intelligence from its employer/employee survey and describes defined project-service commitments.
- Robert Half's current guide is the 2027 edition with projected starting salaries; its separate survey and consulting/staffing propositions have different evidential roles.
- JGA's payroll recruitment proposition supplies a possible response, not a predetermined need to hire.

CLM-0337–0341. Record benchmark edition, underlying period, role/remit, geography, pay basis and population. Starting salary, day rate and an accepted managed output are different cost inputs. None alone is loaded employer cost, funding or achieved benefit. No generic loading factor, pay figure or supplier ranking is supplied. Hays's inspected live 2026 edition/2025 data and Robert Half's live 2027 edition are not combined into a single current market estimate.

## Earlier prompt study: a sharper challenge to our own assumptions

The [saved-data bridge](research-notes/r05-second-check/competitors/prior-study-bridge.json) uses four exact C questions, S04-C, S05-C, S09-C and S10-C, covering 32 saved full texts across four tools/two repeats. All four questions explicitly request evidence or verification. Repeated due-diligence advice in the answers is therefore elicited by the question design and cannot independently corroborate real buyer priorities.

The prompts also assume particular director/head roles, transformation/transition and, in S10, a six-month interim/permanent-search route. These assumptions must not lead the new interviews. The previous study can supply coverage checks and source leads, while actual practitioner needs and events come first. No recommendation count, tax-status instruction, salary, candidate availability or employer-demand conclusion is transferred. Existing partial/pending source-list limits remain attached; saved full text is not equivalent to complete source capture.

## What is applied and what stays open

The five conditions C01–C05 supplement E01–E09. Three financial views, fourteen core questions, optional clarification under Q008–Q013 and the blank observation/forecast/calculation arrays are preserved. The first-pass R05 files are retained as verbatim snapshots; earlier modules and eight client Word/PDF files remain unchanged. No Table financial inputs have been populated.

**For payroll leaders:** identify the current decision, net comparison, parties, usable capacity and evidence that could change it. **For suppliers:** explain actual service/unit/retained work and supply relevant comparable evidence instead of a headline promise. **For JGA:** connect needs, capability, evidence and decision conditions while leaving adequate-incumbent, process and alternative delivery routes open.

Primary guidance, public audit summaries/full report, supplier terms/declarations and education remain distinct. This review improves the research design; it does not replace original practitioner contributions, client scope review or final publication/rights checks. R06 is next: staying, switching, deferral, rejection and abandonment. Nothing has been sent to Nick.

Detailed strands: [history](research-notes/r05-second-check/history/HISTORY-CHALLENGE.md), [market](research-notes/r05-second-check/market/MARKET-CHALLENGE.md), [competitors/prior study](research-notes/r05-second-check/competitors/COMPETITOR-CHALLENGE.md), [capacity/cost](research-notes/r05-second-check/root/CAPACITY-AND-RELEVANT-COST-CHALLENGE.md). Canonical mapping: `08-qa/R05-second-check-record-map.json`.
'''
(ROOT/'03-report/R05-SECOND-CHECK-READOUT.md').write_text(readout)
append='''
## Selective conditions from the second challenge

Apply these within the existing nine domains, only where relevant. They are not new required questions, mandatory gates or scores. The [second-challenge readout](R05-SECOND-CHECK-READOUT.md) carries the evidence and source-specific limits.

| Condition | Clarify for the actual case | Avoid inferring |
| --- | --- | --- |
| C01 Dated case and boundary | Current version, payroll component/wider programme, changed inputs and next reconsideration point. | A historical approval proves current readiness/value, or every change requires full reapproval. CLM-0324–0327, CLM-0340. |
| C02 Distribution and funding | Who bears money/work/risk, who benefits and when, actual allocation/shortfall and funding remit. | Aggregate value establishes every party's affordability, or a conflict/transfer must exist. CLM-0324, CLM-0326, CLM-0328. |
| C03 Service unit and lifecycle cash | Actual contract/version and licence/payroll/payslip/employee/payment unit, retained work, use/commitment/access/handback dates and funding changes. | Active headcount is universal, stopping use ends charging, or ordinary wage principal equals additional transformation cost. CLM-0329–0336, CLM-0341. |
| C04 Usable capacity | Required skill and time window, existing paid availability, extra cover and displaced work. | Annual hours are interchangeable, salary allocation means extra cash, or released time requires a new hire or staffing cut. CLM-0323, CLM-0342–0343. |
| C05 Evidence and benchmark fit | Edition, underlying period, role/remit, geography, pay/engagement basis, contributing population and actual assignment evidence. | Salary guide is loaded employer cost, service marketing proves availability/benefit, or prompted verification advice establishes buyer demand. CLM-0337–0341; prior-study bridge. |

Keep ordinary wages, supplier fees and changed timing of funding distinct; unknown is not zero. No public tariff, salary, standard loading, tax-status rule, financial forecast or compulsory review method has been adopted. Payfit/Modulr version/quantity limits and earlier holds remain explicit. The core instrument and client files are unchanged.
'''
f=ROOT/'03-report/R05-BUSINESS-CASE-CHECKLIST.md';t=f.read_text();marker='\n## Selective conditions from the second challenge';t=t.split(marker)[0]+append;f.write_text(t)
f=ROOT/'03-report/R05-DESKTOP-READOUT.md';t=f.read_text();marker='\n## Second challenge applied';t=t.split(marker)[0]+'''
## Second challenge applied

The user-requested [second challenge](R05-SECOND-CHECK-READOUT.md) adds five selective conditions: dated whole-decision boundary; cost/work/risk bearer versus benefit recipient/funder; actual service unit/retained work/commitment cash; usable skill/time and displaced work; and benchmark/evidence fit. These supplement the existing nine optional domains and three financial views. No numerical forecast, salary/rate, employer observation or new core question was added. Earlier full text and client files are preserved; original practitioner/final-use work remains open.
''';f.write_text(t)
f=ROOT/'03-report/modules/R05-business-case-evidence-and-risks.md';t=f.read_text();marker='\n## User-requested second challenge';t=t.split(marker)[0]+'''
## User-requested second challenge

The [second-challenge readout](../R05-SECOND-CHECK-READOUT.md) applies historical, current segmented service-market, all-six-comparator/JGA, prior-study and usable-capacity checks. Five optional conditions now accompany the unchanged nine-domain/three-view design. No historical total, quoted price, salary, standard loading, savings formula or UI rule was generalised. Constructed C-question evidence requests cannot independently validate buyer priorities. Prior modules, fourteen core questions and client Word/PDF files are preserved. Integrated review is pending; no external sending.
''';f.write_text(t)
print('Integrated draft: five selective conditions; firstpass domains/views/template unchanged; pending review')
