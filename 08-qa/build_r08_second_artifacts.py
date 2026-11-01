from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
def read(p):return json.loads((ROOT/p).read_text())
def write(p,d):(ROOT/p).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n' if not isinstance(d,str) else d)
mapping=read('08-qa/R08-second-check-record-map.json');cs=mapping['claim_map']
def cc(*ids):return [cs[i] for i in ids]
manifest=read('03-report/research-notes/r08-second-check/before-review/manifest.json')['records']
old=read(next(x['snapshot_path'] for x in manifest if x['original_path']=='03-report/R08-framework-map.json'))
model=json.loads(json.dumps(old));model['framework_version']='0.2'
model['second_challenge_status']='integrated_preparatory_draft_independent_review_pending'
model['new_canonical_claims_count_basis']='first_pass_preparatory_synthesis_only'
model['second_challenge_new_canonical_claims']=len(cs)
model['views'][1]['instruction']='Consider the relevant responses feasible at the specified decision/event date; distinguish knowledge available then from a later retrospective account. Include current capability, process/skills, retention or scoped change.'
model['views'][3]['boundary']='Requested, supplied, accepted, believed influential and independently corroborated evidence are different claims. Acceptance does not verify every assertion or establish causal influence. Existing resources can support work without a new budget.'
model['second_challenge_view_edits']=[dict(view_id='V02',field='instruction',before=old['views'][1]['instruction'],after=model['views'][1]['instruction'],reason='Resolve ambiguous at-this-time wording by separating event-time feasibility/knowledge and retrospective explanation.',claim_ids=cc('H8S-C03')),dict(view_id='V04',field='boundary',before=old['views'][3]['boundary'],after=model['views'][3]['boundary'],reason='Do not conflate decision-maker acceptance with case-specific verification or independent corroboration.',claim_ids=cc('R8R-C02','R8R-C03','C8S-C05'))]
conditions=[
 dict(condition_id='C01',title='Event-time basis and later interpretation',use='Where history changes the explanation, distinguish the selected event date and knowledge/options available then from the date, perspective and basis of a later account.',boundary='No hindsight optimality, reconstructed contemporaneous knowledge, universal release-risk threshold or observed later outcome from an old target.',claim_ids=cc('H8S-C01','H8S-C02','H8S-C03','H8S-C04')),
 dict(condition_id='C02',title='Approval object and recurring operating period',use='Where an approval or handoff matters, identify whether it concerns the investment/change, a release, one report/task/payroll run or payment authorisation; retain the actual period and continuing duties if known.',boundary='One accepted report does not prove payment, a completed investment, future-period readiness or transfer of every duty. No exact universal UI/workflow, legal determination or monitoring obligation.',claim_ids=cc('M8S-C01','M8S-C02','M8S-C04'),guardrail_claim_ids=cc('M8S-C03')),
 dict(condition_id='C03',title='Evidence object and case-specific match',use='For material evidence identify the claim about the work, provider/team/person, engagement, date and remit that it actually supports, and what remains unverified or introduced as an assumption.',boundary='A firm case, process description, placement list, salary guide or model recommendation is not current candidate fit/availability, acceptance/start, an executed engagement or the later payroll result.',claim_ids=cc('C8S-C01','C8S-C02','C8S-C03','C8S-C04','C8S-C05')),
 dict(condition_id='C04',title='Qualification beyond acceptance',use='Selectively retain source/status, task/object, date/version and knowledge basis, then describe what supports the material claim and the limits of any corroboration.',boundary='Accepted is not independently verified; repeated links or models may share a source. No automatic source-type ranking, confidence score, required document or assumption uncorroborated means false.',claim_ids=cc('R8R-C01','R8R-C02','R8R-C03')),
 dict(condition_id='C05',title='Divergent accounts and alternative explanations',use='When accounts materially differ, inspect whether object, time or assessment criterion differs. Preserve a remaining disagreement and plausible alternatives rather than force consensus.',boundary='Do not invent a dispute, average incompatible accounts or require recontact. Existing disclosure, permission, burden and actual knowledge limits apply.',claim_ids=cc('R8R-C02','R8R-C04')),
]
for c in conditions:c.update(mandatory=False,scored=False,validated=False)
model.update(cross_cutting_conditions=conditions,second_challenge_supporting_claim_ids=list(cs.values()),additional_mandatory_questions_from_second_challenge=0,second_challenge_blank_evidence_qualification={k:None for k in ['material_claim','work_person_service_object','event_time_and_account_time_if_known','source_status_and_knowledge_basis','accepted_by_if_known','what_the_evidence_supports','corroboration_basis_if_any','introduced_assumption_or_qualification','divergent_account_or_alternative_explanation','remaining_gap_or_supported_next_action']},prior_prompt_scenarios_are_constructed=True,prior_recommendation_counts_reused=False,prior_model_reruns=False,second_challenge_review_basis='Independent integrated preparatory review pending; root exact saved-study linkage checks separate.',second_challenge_new_employer_histories=0)
write('03-report/R08-framework-map.json',model)

applications=read(next(x['snapshot_path'] for x in manifest if x['original_path']=='03-report/R08-constructed-walkthroughs.json'))
for r in applications['routes']:
 r['framework_version']='0.2';r['second_challenge_reassessment']='Root reapplied the same supplied premises to version0.2; original bounded interpretation and unknowns remain appropriate.'
added=[
 dict(route_id='R08-T11',title='Earlier decision and later audit perspective',supplied_premises=['A constructed earlier decision account identifies an option and stated conditions at that event.','A later audit describes additional issues or appraises those conditions; the earlier decision-maker’s knowledge of the later information is not supplied.'],recorded_position='Keep the earlier event and later account as separate dated-perspective statements.',event_time_knowledge='Only the earlier supplied account; no reconstruction from the later audit.',later_interpretation='Retained separately with its own basis; no automatic attribution to the earlier decision-maker.',proposal_decision='Earlier scoped decision as supplied; no new later decision inferred.',supported_next_action=None,unknowns=['What was known then beyond supplied facts','Decision optimality','Later operational result'],view_ids=['V02','V03','V05','V06'],supporting_claim_ids=cc('H8S-C01','H8S-C02','H8S-C03','H8S-C04'),boundary_preserved='No hindsight blame, common risk threshold, later-knowledge backfill or elapsed-target outcome.'),
 dict(route_id='R08-T12',title='One accepted payroll report set within continuing service',supplied_premises=['A constructed service-change decision has been approved.','The contributor separately reports acceptance of one pay-period report set; payment authority/execution, retained tasks and the next period are not supplied.'],recorded_position='Investment/change approval and one recurring report acceptance have separate objects and periods.',proposal_decision='Service-change approval only.',operating_acceptance='One specified report set/period only.',payment_authority_and_execution=None,continuing_duties_performed=None,next_period_readiness=None,supported_next_action=None,unknowns=['Actual payment','Unreported continuing duties','Next-period readiness','Benefit'],view_ids=['V03','V04','V05','V06'],supporting_claim_ids=cc('M8S-C01','M8S-C02','M8S-C04'),boundary_preserved='No promotion of a report handoff to paid employees, completed benefit, future readiness or transferred accountability.'),
 dict(route_id='R08-T13',title='Firm evidence without a current candidate or executed engagement',supplied_premises=['A constructed contributor regards a recruiter as worth discussing on the basis of a firm case and a generic assessment description.','No specific candidate, current assessment, agreement/start, executed contract or payroll outcome is supplied.'],recorded_position='Retain source-scoped firm-level material while person/engagement/outcome remain unknown.',firm_level_material='Supplied case/process description, not independently assured performance.',candidate_specific_assessment=None,candidate_availability_and_start=None,executed_engagement=None,payroll_result=None,supported_next_action='A relevant case-specific evidence need may be proposed; it is not completed assurance or an obligatory hire.',unknowns=['Candidate fit/availability','Acceptance/start','Contract execution','Payroll result'],view_ids=['V02','V04','V05','V06'],supporting_claim_ids=cc('C8S-C01','C8S-C02','C8S-C03','C8S-C05'),boundary_preserved='No firm-to-person proof transfer, guaranteed remedy, availability, or candidate-data demand.'),
 dict(route_id='R08-T14',title='Accepted evidence with a scoped divergent account',supplied_premises=['A constructed contributor says a report was accepted for a decision.','A separate supplied account describes a different outcome criterion or time; whether they concern the same task and period is unestablished.'],recorded_position='Record acceptance separately from accuracy/applicability and retain both scoped accounts.',evidence_accepted='Reported as accepted; not automatically verified.',independent_verification=None,perceived_influence=None,accounts_reconciled=False,disagreement_status='Potential difference of scope/time/criterion; remaining disagreement not adjudicated.',supported_next_action='Clarify the material comparison only where supported and permitted; no mandatory recontact.',unknowns=['Common object/period/criterion','Accuracy','Causal influence'],view_ids=['V01','V04','V05','V06'],supporting_claim_ids=cc('R8R-C02','R8R-C03','R8R-C04'),boundary_preserved='No majority-vote truth, averaged consensus, false-by-default conclusion or assumed user conflict.'),
 dict(route_id='R08-T15',title='Repeated recommendations and an added model assumption',supplied_premises=['Constructed saved model answers repeatedly refer to firm/public material while answering a researcher question that explicitly asks for verification evidence.','One answer adds a location or selection weight absent from the supplied scenario; no actual buyer, candidate test or independent outcome evidence is provided.'],recorded_position='Keep researcher premises, public assertions and introduced assumptions separate.',evidence_request_origin='Researcher-elicited, not unaided buyer demand.',independent_corroboration=None,introduced_assumption='Added location/weight is not a supplied case fact or validated framework score.',actual_buyer_decision=None,supported_next_action=None,unknowns=['Truth/applicability of underlying assertions','Actual buyer criteria','Independent fit/result evidence'],view_ids=['V01','V02','V04','V06'],supporting_claim_ids=cc('C8S-C04','C8S-C05','R8R-C03'),boundary_preserved='No recommendation-count demand, independent-vote proof, model-added case fact or imported numerical score.'),
]
for a in added:
 a.update(evidence_type='constructed_internal_application',actual_employer=None,participant_id=None,actual_case_id=None,as_of_date=None,event_date=None,numerical_result=None,original_practitioner_observation=False,framework_version='0.2',framework_path='03-report/R08-framework-map.json',executed_against_preparatory_R08_framework=True,method='Root-authored manual analytical application to supplied constructed premises; no real employer observation, automatic decision engine or human-user test.',failed_boundary=None)
applications['routes']+=added
applications.update(status='second_challenge_constructed_applications_independent_review_pending',framework_version='0.2',route_count=15,original_routes_reapplied=10,new_constructed_routes=5,practitioner_validation=False)
write('03-report/R08-constructed-walkthroughs.json',applications)

fp=ROOT/'03-report/R08-DECISION-FRAMEWORK.md';t=fp.read_text().replace('working version0.1','working version0.2')
t=t.replace(old['views'][1]['instruction'],model['views'][1]['instruction']).replace(old['views'][3]['boundary'],model['views'][3]['boundary'])
t=t.replace('the account establishes [known facts]','the account reports [scoped facts] / the available evidence supports [specific claim]')
t=t.replace('Ten expressly constructed walkthroughs apply this canvas','Fifteen expressly constructed walkthroughs apply this canvas')
table='| Selective condition | When it changes the explanation | Boundary |\n| --- | --- | --- |\n'
for c in conditions:table+=f"| {c['title']} | {c['use']} | {c['boundary']} {', '.join(c['claim_ids'])}. |\n"
t+='''
## Second challenge: qualify the claim, not just the decision status

The five conditions below add depth only where material. They introduce no new view, question, score or documentary requirement. Existing blank canvas fields remain unchanged; an optional blank evidence-qualification note is available in the structured map. A direct account can remain useful without independent corroboration, provided the basis and limits are clear.

'''+table+'''
In particular, separate the decision date from the later account date; change approval from a recurring run/report/payment action; and evidence about a firm from evidence about a particular person, engagement or outcome. Keep any introduced assumption identifiable. Acceptance of a report is not automatic verification or causal proof. If accounts differ, inspect their scope/time/criterion and retain unresolved differences rather than manufacture consensus.

[Second-challenge findings](R08-SECOND-CHECK-READOUT.md) give the original-source checks, six-comparator/JGA distinctions, earlier-study premises and additional constructed routes. Independent integrated second-challenge review pending. The first-pass review remains an as-of record for version0.1, preserved in snapshots. Nothing sent.
''';fp.write_text(t)

readout='''# R08 second challenge: a decision brief must keep its evidence basis visible

29October2026. Internal preparatory desktop second challenge; independent integrated review pending. No new source route, original participant or market estimate. Seventeen bounded guidance/application records extend canonical reuses; they do not create seventeen new studies.

## Result

The six-view framework remains useful as an evidence-informed working structure. The challenge narrows two ambiguous points: “at this time” now identifies the selected decision/event time rather than silently importing later knowledge, and accepted evidence is explicitly different from verified or independently corroborated claims. The brief-writing pattern now says “the account reports” or “the available evidence supports,” according to its actual basis.

Five optional conditions add precision without expanding the questionnaire: event-time knowledge, the object/period of approval, evidence fit to the person/service/outcome, qualification beyond acceptance, and divergent accounts. Practitioner usefulness, causal influence on approval and commercial value remain untested.

## Historical and counterfactual lenses

LFB's earlier account and2025reset concern different events in one continuing programme. The later account cannot replace what was known or feasible at the earlier event. A Scottish Government audit separately reports migration signoff, conditional backing and final go-live with known issues and assurances, followed by audit appraisal. These scoped judgments do not yield a universal risk threshold, an optimal release decision or a current2026operational result. @H1@–@H4@.

The framework now makes this timing distinction explicit. A later source may legitimately change today's interpretation, but it does not prove an earlier decision-maker knew the same facts. Neither decision is scored as right/wrong from hindsight. Existing target-date and programme/component controls remain.

## Market and operating-service lens

Cintra's documentation describes recurring submission/report/payment actions according to its declared route. These are not the same as the investment/change decision. Its cycle page now carries an October2026update label, but cross-article visibility/payment-stage wording remains inconsistent; CLM-0218 stays held. No UI, customer account, payment or automatic sequence was tested. @M1@, @M3@.

HMRC's source-scoped provider guidance distinguishes purchased support from retained employer inputs/records and responsibilities. This is not a full legal audit or a determination about an actual contract/employer. The analytical implication is selective: identify which task/run/period an approval or accepted handoff concerns, then preserve unknown payment, ongoing work and next-period readiness. One accepted report set cannot settle all those facts. @M2@, @M4@.

## Specific competitor and JGA checks

| Firm/source | Source-scoped check | What it cannot prove |
| --- | --- | --- |
| Portfolio | Declared assessment/search/offer/contact/aftercare process. | Current candidate fit, availability, agreement/start or payroll effect. @C1@. |
| Middlemore | Actual-work assessment and post-search recruitment analytics. | That analytics measure an employer's payroll outcome or validate the next proposed person. @C1@. |
| Hays Project Services | Resource augmentation versus defined managed-project deliverables, governance and transition knowledge. | The actual executed scope, full transfer of payroll responsibility or realised benefit. @C2@. |
| Frazer Jones | One reused provider-hosted reorganisation case, with full-current-access and independent-assurance limits. | A new employer dataset, causal effect or readiness for another brief. @C3@. |
| Oakleaf | Published capabilities and placement examples with level/remit context. | Case-specific capability and result of a proposed individual. @C3@. |
| JGA | Its tailored UK/global talent proposition and own proof claims. | Independent validation, a necessary hire or automatic future performance. No numerical claim adopted. @C3@. |
| Hays / Robert Half guides | Distinct salary-input, employer/employee and non-salary survey frames/periods. | A particular employer's accepted evidence, budget, offer or causal decision influence. No figures transferred. @C4@. |

The useful added condition is evidence-object matching: provider material can support a question worth examining without proving a particular person, engagement or outcome. No named-candidate data, full contract or extra interview question is demanded. @C5@.

## Earlier prompt-study lens

Four exact constructed questions, S01-C,S02-D,S06-C,S11-C, link32saved answers across four tools and two repeats. Root exact text/hash/index/date/status checks passed327checks. Existing global source-capture limits remain separate; no model reruns or recommendation-count transfer.

The researcher already asks for public experience evidence, confidentiality checks or hands-on assessment. Generated verification language is therefore not an unaided employer priority. Four saved ChatGPT repeat1answers were semantically reviewed in the strand; the other28were checked for integrity, not validated as advice. One answer adds London to a prompt that did not supply it, and others generate numerical selection weights. Those are introduced assumptions, not case facts or framework scores.

This makes R08's wording more disciplined: supplied premise, source assertion, observed event and researcher/model addition need distinct treatment. Repeated recommendations do not demonstrate independent corroboration. The [bridge verification](../08-qa/R08-prior-study-bridge-check.md) is integrity assurance, not proof of all generated advice or underlying citations. @C5@, @R3@.

## Method, affected-party and disagreement lenses

QQE supports purpose-fit judgement, source provenance, whose appraisal is reported, divergent criteria and traceable interpretation. It is not certification of this framework or a mandatory indicator list. A contributor's report need not be dismissed merely because no other source corroborates it; equally, acceptance cannot stand in for independent verification. @R1@–@R3@.

Where accounts differ, first inspect object, time and criterion. A platform owner and an affected user could describe different tasks or outcomes. If a material disagreement remains, preserve it with alternative explanations rather than average it away. This is an analytical possibility, not a claim that participants disagree. No recontact, stakeholder census or numerical confidence rating is required. @R4@.

## Applied refinements

'''+table+'''
Version0.2 preserves the six views, their selective fields and blank scope/canvas/brief, all14corequestions and the two-part/eight-chapter proposed report structure. Two exact view-text edits are logged, with source links. The added qualification template remains blank. Accepted evidence and perceived influence remain separate existing fields.

## Constructed challenge and remaining gap

Root reapplied the original ten supplied scenarios to version0.2 and added five constructed challenges: event-time versus later audit perspective; one accepted report set; firm material without a candidate; accepted evidence with divergent criteria; and repeated recommendations plus introduced assumptions. Fifteen applications remain synthetic and separate from actual fieldwork/data arrays. They test internal analytical handling, not user comprehension, decision effect or predictor accuracy.

Original permissioned/coded contributions must still shape the final findings and framework. WP11 remains open; finalWP15 and final Word/PDF/editable package are not complete. No source's rights/currentness or commercial value is assumed. No prices, salary values, statutory calculations, forecasts, confidence score or Table financial input is added. Existing holds remain.

## Evidence trail

- [Historical challenge](research-notes/r08-second-check/history/HISTORY-CHALLENGE.md)
- [Market/service challenge](research-notes/r08-second-check/market/MARKET-CHALLENGE.md)
- [All-six-comparator/JGA and prior study](research-notes/r08-second-check/competitors/COMPETITOR-CHALLENGE.md)
- [Evidence and divergence challenge](research-notes/r08-second-check/root/EVIDENCE-AND-DIVERGENCE-CHALLENGE.md)
- [First-pass snapshots](research-notes/r08-second-check/before-review/manifest.json)
- [Canonical mapping](../08-qa/R08-second-check-record-map.json) and [retained-file hashes](../08-qa/R08-second-check-captures.json)

Raw originals, PDF renders, selected reader notes and parsed text remain distinct. Source failures and same-case aliases are not new independent evidence. Independent integrated second-challenge review and final preservation checks remain before this review is closed. Nothing sent.
'''
for prefix,ids in [('H',['H8S-C01','H8S-C02','H8S-C03','H8S-C04']),('M',['M8S-C01','M8S-C02','M8S-C03','M8S-C04']),('C',[f'C8S-C{i:02}' for i in range(1,6)]),('R',[f'R8R-C{i:02}' for i in range(1,5)])]:
 for i,key in enumerate(ids,1):readout=readout.replace(f'@{prefix}{i}@',cs[key])
write('03-report/R08-SECOND-CHECK-READOUT.md',readout)
for rel in ['03-report/R08-DESKTOP-SYNTHESIS.md','03-report/R08-REPORT-INTEGRATION.md','03-report/modules/R08-decision-framework-and-synthesis.md']:
 p=ROOT/rel;t=p.read_text();marker='\n## User-requested second challenge';assert marker not in t
 link='../R08-SECOND-CHECK-READOUT.md' if '/modules/' in rel else 'R08-SECOND-CHECK-READOUT.md'
 t+='\n## User-requested second challenge\n\nVersion0.2 retains six linked views and adds selective event-time, operating-period, evidence-object, claim-qualification and divergent-account conditions. It narrows two view-text ambiguities and keeps introduced assumptions distinct. Fifteen constructed applications remain separate from practitioner validation; core questions, outline and finalWP11dependency are unchanged. Independent integrated second-challenge review pending.\n\n'+f'[Second-challenge findings]({link}) contain the evidence, exact changes and remaining gaps. Nothing sent.\n'
 p.write_text(t)
print(json.dumps({'status':'integrated_second_draft_ready','framework_version':'0.2','views':6,'conditions':5,'constructed_applications':15,'new_routes':0,'new_claims':len(cs)},indent=2))
