"""Append the event second-check evidence and write its separate review artefacts once."""
from pathlib import Path
import json,hashlib
ROOT=Path(__file__).resolve().parents[1]
B='04-table/research-notes/t05e-second-check'
def load(p):return json.loads((ROOT/p).read_text())
def save(p,x):
 q=ROOT/p;q.parent.mkdir(parents=True,exist_ok=True);q.write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def text(p,x):(ROOT/p).write_text(x.strip()+'\n')
pack=load(B+'/evidence/source-candidates.json');candidates=pack['records']
sources=load('02-evidence/registers/sources.json');claims=load('02-evidence/registers/claims.json')
assert len(sources['records'])==256 and len(claims['records'])==520,'Run this append once only'
source_map={};added=0
for x in candidates:
 ident=x['candidate_id'];sid=x.get('reuse_source_id')
 if sid:
  current=next(s for s in sources['records']if s['source_id']==sid)
  assert current['url']==x['url']
  current.setdefault('additional_reviews',[]).append({'date':'2026-11-01','module':'T05E-second','origin':B+'/evidence/source-candidates.json','detail':x})
  if 'T05E-second'not in current['related_topic_ids']:current['related_topic_ids'].append('T05E-second')
 else:
  sid=f'SRC-{289+added:04}';added+=1
  assert x['url']not in {s['url']for s in sources['records']}
  historical=ident=='E2-S07'
  sources['records'].append({'source_id':sid,'title':x['title'],'publisher':x['publisher'],'url':x['url'],
   'source_type':'historical_primary_venue_guide'if historical else'primary_publisher_event_context',
   'review_status':'selected_sections_reviewed_historical_context_only'if historical else'selected_primary_sections_reviewed',
   'notes':'Historical guide remains excluded as a current/future budget input. Prior original reused, not a fresh quote.'if historical else'Publisher-scoped format/context only. No demand, achieved benefit, actual cost or future attendance inferred.',
   'accessed_on':'2026-11-01','published_date':'2026-10-22'if ident=='E2-S03'else'2026-09-23'if ident=='E2-S04'else None,
   'fieldwork_period':None,'population':None,'geography':'Source-specific UK/global context','sample_size':None,'method_available':None,
   'funding_or_commercial_interest':'Publisher or named commercial partner interest',
   'capture_path':x.get('capture_path'),'capture_sha256':x.get('capture_sha256'),
   'reuse_status':'internal_selected_context','publication_eligibility':'historical_context_not_current_budget'if historical else'final_context_and_rights_check_required',
   'related_topic_ids':['T05E-second'],'t05e_second_source_candidate_id':ident,'candidate_detail':x})
 source_map[ident]=sid
assert added==7
specs=[
 ('E2-C01',['E2-S01'],'Opening, chair/support description and recap invitation','Portfolio describes a sector-specific education-payroll discussion with a practitioner chair, CIPP support and a written recap.','publisher_event_description','No date, admission price, turnout, cost, verified outcomes or rights adopted. No payroll-law or pay-growth assertions reused.'),
 ('E2-C02',['E2-S02'],'Events FAQ: formats, audience, price and recordings','Frazer Jones describes several HR event formats and career levels, with most events complimentary and registration usually required. Recordings/resources may be available.','publisher_offer','Not every event is free, a particular place is available or every participant receives a recording. No event cost or willingness to pay inferred.'),
 ('E2-C03',['E2-S03'],'22 October2026 article: 8 October breakfast and named facilitators/co-host','Oakleaf reports an HR-leader breakfast roundtable with external co-facilitators and a co-host, followed by a written recap.','publisher_event_account','Source declarations of format/roles only. Statistical, AI-investment and causal claims in the article were not adopted; no fee, staffing need or outcome verified.'),
 ('E2-C04',['E2-S04','E2-S05'],'Hays-attributed ICAS commercial article; Shared Services Forum notice/archive2020','A 2020 Hays payroll notice describes virtual activities; a September2026 Hays-authored partner article describes online and in-person formats across the UK.','dated_publisher_context','Two dated notices are not a measured market trend, delivered attendance record, price comparison or proof one mode replaces another. ICAS labels the2026 article commercial partner content.'),
 ('E2-C05',['E2-S06'],'UK event catalogue introduction and dated listings','Robert Half presents webinars, workshops, roundtables and networking alongside leadership/business content.','publisher_offer','Broad finance/HR/leadership context is not a payroll-only peer offer, current place entitlement, admission price or event-level cost.'),
 ('E2-C06',['E2-S09'],'Beyond the Shortlist; Post Project Report','Middlemore describes client advice, market context and post-search recruitment analytics.','publisher_service_context','These selected sections do not establish an event product, event cost, audience access or a commissioned payroll-investment evidence base. No sample form submitted.'),
 ('E2-C07',['E2-S10','E2-S14'],'Podcast description; CPO article12 January2026 referencing October2025 launch','JGA describes an expert payroll podcast, while CPO describes an invite-only online executive community launched in October2025.','publisher_format_context','Different publishers and mechanisms. No automatic guest/member access, sponsorship, partnership, event availability or permission follows. Audio and member area uninspected.'),
 ('E2-C08',['E2-S07','E2-S08'],'January and September guides, p6; September additional information p8','Benares guides for different2026 periods retain a £78 Bayleaf menu while showing different cover/service components; the later guide has a nine-person party-menu threshold and whole-party menu selection.','dated_primary_terms_context','Historical versus dated menu context only, not comparable inflation measurement, a2027 quote, selected meal or universal all-in uplift. Calculation bases, actual minimum/hire and selected event terms remain open.'),
 ('E2-C09',['E2-S11'],'FAQ: qualification, travel, pre-event input and substitutes','iVentiv separates approved senior-corporate places, participant input and eligible substitutes; free attendance does not include travel/accommodation.','publisher_offer','Adjacent L&D/executive mechanism, not JGA terms, a payroll event, achieved conversion or a fee/cost benchmark. Eligibility thresholds are not imported.'),
 ('E2-C10',['E2-S12'],'Payment, substitution, cancellation and postponement sections','iVentiv generic terms distinguish future-use credit and cancellation/postponement, while containing differing payment intervals.','publisher_terms_context','The public FAQ and generic terms need product-specific reconciliation. No JGA cancellation clause, payment deadline, refund right or price is adopted.'),
 ('E2-C11',['E2-S13'],'Current named Rule and recording/AI/photo/designated-parts FAQ','Chatham House distinguishes use of information from identity/affiliation disclosure and specifies no recording, AI notetaking/transcription or in-room photos/video for its named Rule.','primary_named_meeting_protocol','Applies if that named mode is selected. Not a blanket ban on every event, legal confidentiality guarantee, collection consent or JGA adoption; designated modes must be agreed and workable.'),
 ('E2-C12',['E2-S11','E2-S03'],'Researcher application to WE01-WE10 and remaining work','Whole activity counts and planning allowances do not by themselves measure partial actual preparation or specify a rescheduled task\'s remaining effort.','researcher_programme_cost_requirement','Use attributable actual/incurred hours and necessary remainder without duplicating full tasks or adding a generic cancellation/reuse percentage.'),
 ('E2-C13',['E2-S03'],'Researcher application to WE11-WE16 and onsite timeline','Unique person-hours and simultaneous role coverage are different checks. One person\'s elapsed time should not be counted twice, but overlapping required duties still need capable available coverage.','researcher_delivery_feasibility_requirement','No staffing ratio, mandatory second moderator, wage or verified JGA capability follows. Actual timed duties determine the need.'),
 ('E2-C14',['E2-S01','E2-S02','E2-S04','E2-S06','E2-S09','E2-S10','E2-S14'],'Researcher application to audience, alternative and event use','Select an actual decision/audience/mode contribution before assigning event effort or a paid gap. Public events, personalised advice and asynchronous communities are relevant alternatives.','researcher_market_design_requirement','No market size, willingness to attend/pay, demand forecast, membership plan or substitution of contracted practitioner research inferred.'),
 ('E2-C15',['E2-S04','E2-S11','E2-S12'],'Researcher application to cohort, format, city and travel','Reprice actual changed scope, cohort, format, locality and payer obligations rather than replicate one event cost across an international calendar.','researcher_cost_scope_requirement','No city, fare, FX, hotel, no-show estimate, annual cadence or delivery capacity is selected.'),
 ('E2-C16',['E2-S08'],'Researcher application to lower/upper meal and venue conditions','Maximum numerical seats are only one feasibility condition. Actual minimum party/menu rules, room/layout, privacy/access and billable-cover terms need their own applicable treatment.','researcher_event_feasibility_requirement','A capacity result is not a booking or complete venue/menu validation. Earlier workbook explicitly limits its test to numerical fit.'),
 ('E2-C17',['E2-S08','E2-S12'],'Researcher application to resources, liabilities, credit and receipts','Keep gross supplier bill, credited deposit, net cancellation loss, restricted future-use credit, actual refund and remaining service distinct across their periods.','researcher_cost_and_obligation_requirement','This review records the requirement; dated cash and full programme implementation remain open. No future-use credit is assumed convertible to cash.')]
claim_map={}
for i,(ident,ss,loc,body,kind,limit)in enumerate(specs):
 cid=f'CLM-{611+i:04}';claim_map[ident]=cid
 claims['records'].append({'claim_id':cid,'source_ids':[source_map[s]for s in ss],'locator':loc,'claim_text':body,'evidence_class':kind,
  'metric':None,'value':None,'unit':None,'denominator':None,'question_wording':None,'population':None,'time_period':None,
  'support_checked':True,'review_mode':'Selected primary sections and retained dated guides inspected; publisher descriptions separated from researcher applications.',
  'interpretation_limits':limit,'status':'T05E_second_desktop_context','publication_status':'working',
  'audit_record_origin':B+'/evidence/claim-candidates.json','t05e_second_claim_candidate_id':ident})
for d in [sources,claims]:d['updated_on']='2026-11-01'
save('02-evidence/registers/sources.json',sources);save('02-evidence/registers/claims.json',claims)
save(B+'/evidence/claim-candidates.json',{'records':claims['records'][-17:]})
save('08-qa/T05E-second-check-record-map.json',{'date':'2026-11-01','source_map':source_map,'claim_map':claim_map,'new_source_routes':7,'reused_source_routes':7,'new_claim_records':17,'canonical_sources':263,'canonical_claims':537,'financial_inputs_added':0})

comparators=[
 ('Portfolio Payroll',['E2-S01'],'Education-payroll cohort, practitioner chair and CIPP-supported discussion.','A specific sector context is a stronger comparison than a generic senior-title list. No fee or observed attendance adopted.'),
 ('Frazer Jones',['E2-S02'],'Multiple HR formats and levels; most events described as complimentary.','An alternative to compete with on usefulness and fit, not evidence that all events or personalised work must be free.'),
 ('Oakleaf Partnership',['E2-S03'],'8 October2026 HR breakfast with named co-facilitators/co-host and22 October recap.','Role/partner/output scope matters. Their setup is not a required JGA headcount or price template.'),
 ('Middlemore',['E2-S09'],'Client market advice and post-search report in selected payroll service sections.','Actual engagement-specific evidence and relationships may already satisfy some needs. No event product asserted from these sections.'),
 ('Hays',['E2-S04','E2-S05'],'2020 payroll virtual notice and September2026 mixed-mode commercial partner article.','Delivery mode and audience varied by purpose/period. No linear return-to-dinner trend or transfer of costs inferred.'),
 ('Robert Half',['E2-S06'],'UK event catalogue across leadership, finance/HR and networking formats.','A wider leadership alternative, not an exact payroll peer product or a verified commercial conversion model.'),
 ('JGA',['E2-S10'],'Nick Day-hosted UK/global payroll expert podcast and archive routes.','Existing content could inform a discussion, subject to scope/rights. Guest access, new permission, availability and Table demand remain unknown.')]
save(B+'/comparator-map.json',{'date':'2026-11-01','recruitment_comparators':6,'JGA_contexts':1,'records':[{'firm':name,'source_ids':[source_map[s]for s in ss],'observed_context':ctx,'event_implication':use,'actual_buyer_or_partner':False,'measured_cost_or_demand':False}for name,ss,ctx,use in comparators],'not_T01_six_business_models':True})
conditions=[
 ('E201','Actual contribution, audience and alternatives',['WE01','WE04','WE05','WE06','WE10'],['E2-C01','E2-C02','E2-C06','E2-C07','E2-C14'],'Name the useful decision/use, eligible audience and closest existing alternative before selecting scope. Do not infer a paid gap or participation from provider visibility.'),
 ('E202','Partial work, rescheduling and exact reuse',['WE01','WE03','WE09','WE10','WE17','WE22'],['E2-C12'],'Preserve attributable incurred hours and required remaining work by task/state. Reuse only genuinely retained work and do not treat changed dates as full duplicate tasks.'),
 ('E203','Concurrent roles and capable coverage',['WE11','WE12','WE13','WE14','WE15','WE16'],['E2-C03','E2-C13'],'Map necessary overlapping duties to actual people/time. Count body-time once and separately test coverage; check package inclusions before later labour valuation.'),
 ('E204','Chosen participation and output mode',['WE01','WE06','WE10','WE16','WE17','WE18'],['E2-C07','E2-C11'],'Agree actual audience, confidentiality and usable output. If adopting the named Chatham House Rule, respect its recording/AI/photo restrictions. Recording permission is not a default route around that mode.'),
 ('E205','Menu/venue eligibility and charge basis',['WE02','WE03','WE07','WE08','WE09','WE19'],['E2-C08','E2-C16'],'Test applicable lower/upper menu/room conditions and actual billed covers, charges and inclusions. Neither a seat ceiling nor a dated menu establishes future suitability/price.'),
 ('E206','Cohort, format, locality and travel',['WE04','WE05','WE07','WE09','WE15','WE20','WE21'],['E2-C04','E2-C09','E2-C15'],'Scope genuine cohort/mode/location changes, travel origins/payers and local resources. Shared research does not make international event operations identical.'),
 ('E207','Supplier liability, credit, cash and remaining service',['WE03','WE09','WE19','WE20','WE22'],['E2-C10','E2-C17'],'Carry supplier liability, deposits, restricted future credits, actual refunds and unfulfilled benefits separately into dated cash and resource schedules.')]
component={'date':'2026-11-01','status':'second_challenge_reviewed_required_programme_refinements_recorded','reviewer':'same_agent_second_check','independent_agent_review':False,
 'first_component_path':'04-table/T05-event-cost-map.json','conditions':[{'condition_id':i,'label':label,'workload_ids':work,'claim_ids':[claim_map[c]for c in cl],'required_treatment':treatment}for i,label,work,cl,treatment in conditions],
 'evidence_candidate_path':B+'/evidence/source-candidates.json','comparator_map_path':B+'/comparator-map.json','prior_study_bridge_path':B+'/prior-study/prior-study-bridge.json','cost_applications_path':B+'/cost-applications.json',
 'review_checks_path':'08-qa/t05e-second-review/verification.json','source_ids':list(source_map.values()),'claim_ids':list(claim_map.values()),
 'workbooks_changed':False,'financial_inputs_changed':False,'original_shared_financial_inputs':70,'first_component_arithmetic_error_identified':False,
 'programme_state_coverage_and_obligation_implementation_still_required':True,'full_financial_model_complete':False,
 'current_contract_fee_changed':False,'fourteen_core_questions_unchanged':True,'practitioner_free_full_research_preserved':True,'actual_participants':[],'actual_quotes':[],'actual_bookings':[],'external_actions':[]}
save('04-table/T05E-second-challenge-map.json',component)
text('04-table/T05E-PROGRAMME-REFINEMENTS.md','''# Event programme refinements after the second check

1 November2026. Requirements for later full-model integration. Preserve the original event workbook and its stated numerical-fit/unpriced-workload limits.

| Requirement | Implementation in the complete model |
| --- | --- |
| Decision, audience and alternatives | Identify the contribution and actual scope, rather than assume a generic forum or provider recommendation establishes demand. Keep report/practitioner benefits unchanged. |
| Actual, incurred and remaining work | Record attributable task/state/person-hours. Whole activity quantities and untimed allowances do not measure partially completed work. Preserve necessary work when completion is zero. |
| Rescheduling and reuse | Carry actual retained preparation plus necessary update, recruiting/handling and remaining obligations. Do not automatically count a second full task or adopt a reuse percentage. |
| Simultaneous coverage | Count each person's elapsed work once, then separately check whether actual critical duties overlap. A single person's two labels do not prove two functions were covered. |
| Chosen meeting/output mode | Select a workable confidentiality, recording and output approach. Apply the named Rule only if chosen; do not promise incompatible recordings, photos or identity-revealing outputs. No new tools/permissions assumed. |
| Venue and meal conditions | Check lower/upper party rules, seated layout, whole-party menu, actual guarantees and charge bases. A maximum-seat pass is a narrow result. Dated guide components are not a future quote. |
| Cohort, format, city and payer | Scope changed people, local delivery, travel, currency and responsibility. Reuse common research once; price real event changes separately. |
| Credit, refunds and remaining service | Keep gross bill, deposit credit, net loss, restricted future-use credit, cash refund and future benefit distinct. Resolve conflicting generic terms for the actual chosen transaction. |

These can be a few explicit fields and notes in existing schedules. They do not require another practitioner form, new question quota, mandatory second moderator, new software or an expanded contract. Actual task skill/rate and package overlap remain prerequisites to full resource valuation.

Before the full model passes, test partial preparation, a postponed event with retained work, simultaneous duties, a group below a chosen menu threshold, late withdrawals with unchanged billed covers, a restricted credit without cash, a refund and a selected event with unknown travel. Match the research-only/event cases on the same edition, horizon and existing benefits. No favourable scenario substitutes for authorised buyer/member validation.

See the [review findings](T05E-SECOND-CHECK-READOUT.md) and [sixteen constructed applications](research-notes/t05e-second-check/cost-applications.json). Dated cash and the full programme model remain unbuilt.
''')
text('04-table/T05E-SECOND-CHECK-READOUT.md','''# Event component: second-check findings

1 November2026. Internal review across historical, market, competitor, participation and delivery/cost perspectives. This is a same-agent challenge with read-only formula checks, not new independent validation or practitioner fieldwork.

## The decision this review changes

Keep the event workload template, but strengthen how the eventual programme model handles actual work, peak role coverage and commitments. Its defined-unit arithmetic did not reveal an error. Its numerical capacity result is deliberately narrower than a complete venue decision, and its planned task allowances do not measure actual partial preparation.

The strongest market implication is to test a specific useful payroll decision with a well-matched group before choosing hospitality. Existing recruiter events and online communities already offer learning and connections. A premium dinner, a senior title or a free report alone does not establish incremental paid value. The Table's proposed distinctive contribution remains a hypothesis for authorised buyer/member discussions.

## Historical and lifecycle checks

| Dated context | What it supports | What it cannot establish |
| --- | --- | --- |
| Hays payroll notice in the2020 archive | Virtual activities were already a route to payroll professionals during the pandemic. | Delivered turnout, cost savings or a permanent preference for that mode. |
| Hays-authored ICAS partner article,23 September2026 | The described programme includes online and in-person expert/peer formats. | A universal return to dinners or an actual JGA audience. |
| CPO article,12 January2026, describing an October2025 launch | An invite-only online senior-payroll community is a relevant alternative to a physical meal. | A JGA partnership, member access, price, new permission or verified engagement. |
| Two Benares2026 guide editions | A headline menu can retain its price while service/cover components, menu content and applicable dates differ. | A comparable inflation series or an all-in2027 quote. |

Sources: [Hays2020 notice](https://www.sharedservicesforumuk.com/news/celebrate-national-payroll-week-with-hays), [Hays/ICAS2026 article](https://www.icas.com/news-insights-events/news/member-rewards/turn-insight-into-action-join-hays-expert-events-and-webinars-partner-hays), [CPO account](https://cpo.org/forum-helps-communicate-payrolls-value-at-executive-level/).

In the retained [January Benares guide](https://benaresrestaurant.com/wp-content/uploads/2026/01/Benares-Events-Guide-2026-WEB.pdf), Bayleaf is £78 and the stated cover/service components are5%/10%. In the [September guide](https://benaresrestaurant.com/wp-content/uploads/2026/09/Benares-Events-Guide-2026-WEB-3-SEP-Onwards.pdf), Bayleaf remains £78 while those components are2%/13%. We have not treated the sums as a universal uplift: applicable bases, discretionary service, minimum spend and hire need actual terms. The menus differ and have bounded validity periods. The earlier guide remains excluded from current/future budget inputs, while being useful historical evidence.

## Specific competitor and JGA checks

| Firm | Relevant observed context | Implication for this event |
| --- | --- | --- |
| Portfolio Payroll | Education-payroll cohort with a practitioner chair, CIPP support and discussion-led recap. | A recognisable shared problem can define the group more usefully than title alone. No admission fee verified. |
| Frazer Jones | HR webinars, networking, roundtables and panels; most events described as complimentary. | Compete on decision usefulness and fit. Do not assume all formats or every place are free/available. |
| Oakleaf Partnership |8 October2026 HR breakfast with co-facilitators and a co-host, followed by a recap. | Define actual roles, inclusions and output. Their setup does not establish a required JGA staffing ratio or fee. |
| Middlemore | Advice and post-search recruitment analytics in the selected payroll service sections. | A specific engagement may already supply relevant evidence. Those sections do not establish an event product. |
| Hays | Dated payroll virtual notice plus2026 mixed-mode commercial partner description. | Match audience, purpose and period; mode is a design choice, not a market forecast. |
| Robert Half | UK leadership/business event catalogue with multiple formats. | A wider alternative for busy finance/HR leaders; not an exact payroll peer product or cost benchmark. |
| JGA | Payroll expert podcast and archive routes hosted by Nick Day. | Existing content might inform a briefing, subject to its actual scope/rights. Guest access, staff availability and event demand remain unknown. |

Primary context: [Portfolio](https://www.theportfoliogroup.com/education-payroll-roundtable-navigating-change-together/), [Frazer Jones](https://www.frazerjones.com/events/), [Oakleaf](https://www.oakleafpartnership.com/news-views/navigating-change-in-the-ai-era-what-hr-leaders-told-us), [Middlemore](https://middlemore.co.uk/payroll-search/), [Robert Half](https://www.roberthalf.com/gb/en/insights/tags/event), [JGA](https://jgarecruitment.com/the-payroll-podcast/). These are selected public offers/accounts, not a representative market sample or verified service outcomes. The [comparator map](research-notes/t05e-second-check/comparator-map.json) records scope. No forms, recordings, member area or contact route was used.

## Attendance, trust and the promised output

The [iVentiv FAQ](https://www.iventiv.com/how-can-we-help) makes admission approval, travel exclusion, participant topic input and substitutes visible. This is an adjacent executive/L&D mechanism, not JGA's policy. Its seniority/company thresholds do not become Table eligibility rules. The lesson is to define who the actual place and benefit are for, and handle replacements against that fit instead of treating any occupied chair as equivalent.

If the named [Chatham House Rule](https://www.chathamhouse.org/about-us/chatham-house-rule) is chosen, its current FAQ prohibits recording, AI notetaking/transcription and in-room photos/video. Information use and participant identification are different matters. Plan a compatible output and clearly designated meeting mode. The named Rule cannot simply coexist with a promised recording or identity-revealing recap. No new confidentiality mode, consent, data tool or publication right has been adopted by this review.

The [generic iVentiv terms](https://www.iventiv.com/terms-and-conditions) also distinguish credit, cancellation and postponement, and contain differing payment intervals. Their exact product applicability needs reconciliation. This reinforces a model requirement: a future-use credit is not the same thing as cash refunded, and a moved date can leave useful work and obligations outstanding. No comparator clause or date has been copied into JGA terms.

## What the read-only workbook challenge found

The [sixteen constructed applications](research-notes/t05e-second-check/cost-applications.json) reconcile all64 original saved formula caches and exercise defined-unit arithmetic and its boundaries. They preserve the workbook bytes. Monetary examples below are constructed mechanics, not recommended prices or new financial inputs.

| Challenge | Result and necessary treatment |
| --- | --- |
| One complete preparation unit versus partial work | The working allowance is3 hours; a half event count is rejected. An attributable1.5 hours can be retained in the uncovered-work row. The complete model still needs actual/incurred and remaining work, with the source task identified. |
| One person hosting and moderating | Counting elapsed time once prevents duplicate hours. It does not establish that simultaneous check-in and moderation duties can both be covered. Test the actual timeline and available capability. |
| A moved date | Two full task quantities produce6 hours for that task. An exact retained preparation plus an actual update can be different. Do not automatically book two complete tasks or invent a reuse discount. |
| Fifteen practitioners and two additional people | Seventeen places exceed a sixteen-person limit. Extra roles still occupy seats only once per distinct person. |
| Eight people below the chosen party-menu threshold | A maximum-seat check can pass while the later Benares guide's nine-person party-menu rule is not met. Capacity remains only a numerical ceiling result. |
| Two withdrawals after a cover guarantee | Fifteen people can remain alongside seventeen billed covers. Check actual permitted reductions/substitutions instead of tying the bill to attendance on the day. |
| Inclusive external package | Carry its actual inclusions once. Person-hours can remain visible without adding a duplicate hourly cash fee for the same scope. |
| Restricted credit or refund | A hypothetical £500 future-use credit produces no established £500 cash receipt. A real cash refund belongs in dated cash/supplier reconciliation; the direct-cost entry grid rejects a negative expense. |
| Free platform and unknown travel | A zero platform amount does not remove handling effort. A selected journey with no price stays unavailable. No assumed origin, Texas city, fare or exchange rate has been inserted. |

The first component remains a planning template, not a timesheet, role calendar, complete package valuation, booking validator or cash ledger. The [programme refinements](T05E-PROGRAMME-REFINEMENTS.md) record the missing integration requirements rather than disguise them as implemented features. No native Excel check or new independent-agent audit was performed.

## What the earlier prompt study contributes

Four exact questions were linked to32 saved answers across the four products/two repeats; one answer per product was semantically reread. The [bridge](research-notes/t05e-second-check/prior-study/prior-study-bridge.json) preserves exact prompts, dates and text hashes. These are researcher-authored buyer contexts and model responses, not actual respondents.

The confidentiality question helps challenge discussion boundaries. The transformation question helps separate operations, systems and change capabilities. The Manchester question makes locality relevant without supplying anyone's travel origin. The ordinary growth-hire question challenges the assumption that every useful payroll context is an executive-forum audience. Generated score weights, fees, credentials and performance assertions were excluded as market/cost evidence. No model reruns or refreshed recruiter rankings were made.

## Conditional implications for the next stage

Keep the same common research basis when comparing a research-only route and an event increment. A physical event should be tested around a concrete decision/use and matched people. An asynchronous or remote mechanism is an alternative to assess, not an automatic replacement for contracted research or a guaranteed cheaper/equivalent experience. A new cohort or international city can require fresh handling, different skills, travel and terms even when the research is reused.

Seven conditions are now recorded for full integration: contribution/audience; partial work and reuse; concurrent coverage; chosen participation/output mode; venue/menu/charges; cohort/mode/locality; and liability/credit/cash/remaining service. They are selective design requirements, not extra mandatory practitioner questions or a new paid scope.

All three workbooks, all70 shared financial inputs, the first event catalogue/QA and prior client/research artefacts are preserved. The agreed fee, fourteen core questions,6–10 distinct usable report contributors, up-to-four T03 exploratory contributions and free full practitioner research remain unchanged. No actual buyer/member validation, attendee recruitment, quote, booking, sending or spending occurred. Next is dated cash and remaining-obligation implementation, followed by the complete matched programme model. Those stages have not been executed here.
''')
search=load('02-evidence/registers/searches.json');search['records'].append({'search_id':'SCH-0030','date':'2026-11-01','purpose':'Second event-component challenge: dated alternatives, six comparators/JGA, participation/roles, venue history and read-only workbook boundaries','queries':['site.theportfoliogroup.com payroll events roundtable webinar','site.frazerjones.com payroll roundtable event','site.oakleafpartnership.com payroll roundtable breakfast','site.middlemore.co.uk payroll event roundtable','site.hays.co.uk payroll webinar events roundtable','site.roberthalf.com gb events webinars roundtable'],'related_source_ids':list(source_map.values()),'outcome':'Seven new routes and seven canonical reuses;17 bounded records. Four current selected-reader notes, current raw captures and two prior original guides distinguished. Hays direct events shell is discovery only; Hays-attributed commercial partner article and dated notice used for context. No fieldwork, rates, forecasts, sending, booking or spend.'});search['updated_on']='2026-11-01';save('02-evidence/registers/searches.json',search)
print(json.dumps({'source_routes':len(sources['records']),'claims':len(claims['records']),'new_sources':added,'source_map':source_map,'primary_originals':sum(bool(x.get('capture_path'))for x in sources['records'])},indent=2))
