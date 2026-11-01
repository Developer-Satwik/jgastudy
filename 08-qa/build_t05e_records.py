from pathlib import Path
import json, hashlib

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / '04-table/research-notes/t05-event-costs'
def load(p): return json.loads((ROOT/p).read_text())
def save(p,d):
    q=ROOT/p; q.parent.mkdir(parents=True,exist_ok=True)
    q.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
def text(p,s):
    q=ROOT/p; q.parent.mkdir(parents=True,exist_ok=True);q.write_text(s.strip()+'\n')

attempts=load('04-table/research-notes/t05-event-costs/evidence/capture-attempts.json')['records']
adopted=[x for x in attempts if x.get('adopted') is not False]
assert len(adopted)==7
sources=load('02-evidence/registers/sources.json')
claims=load('02-evidence/registers/claims.json')
assert len(sources['records'])==249 and len(claims['records'])==508, 'Merge once only'
source_map={x['candidate_id']:f'SRC-{282+i:04}'for i,x in enumerate(adopted)}
for x in adopted:
    assert x['url']not in {s['url']for s in sources['records']}
    assert hashlib.sha256((ROOT/x['capture_path']).read_bytes()).hexdigest()==x['capture_sha256']
    sources['records'].append({
        'source_id':source_map[x['candidate_id']],'title':x['title'],'publisher':x['publisher'],
        'url':x['url'],'source_type':'professional_competency_framework'if x['candidate_id']=='E-S08'else'official_public_guidance_or_publisher_terms',
        'review_status':'selected_relevant_sections_inspected_original_retained','notes':'Source-scoped event design and cost treatment only. No supplier quote, booking, capability, legal determination or demand estimate.',
        'accessed_on':'2026-11-01','published_date':None,'fieldwork_period':None,'population':None,
        'geography':'UK'if x['candidate_id']not in ['E-S07','E-S08']else'publisher/global context; selected UK application only',
        'sample_size':None,'method_available':None,'funding_or_commercial_interest':'Publisher commercial interest'if x['candidate_id']=='E-S07'else None,
        'capture_path':x['capture_path'],'capture_sha256':x['capture_sha256'],
        'reuse_status':'internal_selected_paraphrase','publication_eligibility':'final_context_and_permissions_check_required',
        'related_topic_ids':['T05E'],'t05e_source_candidate_id':x['candidate_id'],
        'candidate_detail':x})
claim_specs=[
 ('E-C01',['E-S01'],'Planning; safety plan; selecting contractors','Event planning should fit the scale and risks, clarify responsibility, and consider audience, place, duration, facilities and suitable contractors.','official_guidance','HSE guidance is used for proportionate organising work, not a bespoke legal opinion or a requirement to reproduce festival staffing.'),
 ('E-C02',['E-S02'],'Management; competence; monitoring; after an event','Organising includes coordination and competent oversight during relevant phases and a post-event review. The guidance allows a simple checklist for small-scale events.','official_guidance','Venue staff do not automatically own all organiser tasks. Actual responsibilities and competent available people must be established.'),
 ('E-C03',['E-S03'],'About Advance tickets; changing/refunding','Advance rail tickets are restricted to the specified date/train and limited availability. Changes can incur a fee and fare difference; ordinary refunds are restricted, with disruption exceptions.','official_ticket_terms','No route fare, universal cheapest option or blanket no-refund rule adopted. Check the actual ticket and travel dates.'),
 ('E-C04',['E-S04'],'Passenger Assist; assistance requests','Rail assistance offers a route to arrange travel support, including multi-service journeys; actual requirements and station/train arrangements need checking.','official_service_description','No personal disability data, support booking, universal accessibility guarantee or cost saving inferred.'),
 ('E-C05',['E-S05'],'Mileage allowance payments; approved amount','HMRC mileage guidance concerns tax treatment of employee business-vehicle payments. It does not establish JGA reimbursement policy, a fare quote or a complete journey cost.','official_guidance_researcher_scope_application','No numeric tax rate adopted as an event input. Actual payer, eligibility, date, policy and reimbursement amount remain unknown.'),
 ('E-C06',['E-S07'],'Eventbrite Pricing; free tickets','Eventbrite states that free-ticket events have no ticketing-platform fee, while paid-ticket handling and optional tools can involve charges.','publisher_offer','No platform is selected. Free software does not remove invitation, privacy, moderation or support work; no paid-fee percentage adopted.'),
 ('E-C07',['E-S08'],'PDF pp2-4 and p6: relationships, process and outcomes','The IAF framework separates agreed roles and deliverables, process design, participation and useful outcomes. This supports treating moderator preparation and follow-through as work alongside live facilitation.','professional_framework_researcher_application','No certification, JGA capability, freelance fee, universal staff ratio or fixed preparation multiple is implied. Only the cited competency sections were visually checked.'),
 ('E-C08',[],'Researcher application to T04 venue evidence and T05S refinements','Practitioner seats, additional distinct team/guest seats, confirmed attendance, attendance on the day and billed covers require separate counts. A person with two roles occupies one place.','researcher_cost_design','Constructed count examples are not recruited participants or evidence of actual attendance.', ['SRC-0258','SRC-0260','SRC-0261','SRC-0262']),
 ('E-C09',[],'Researcher application to minimum, charges and deposit mechanics','Use the actual minimum-spend offset, eligible consumption and charge bases. A credited deposit changes cash and balance, rather than adding a second expense.','researcher_cost_design','Venue-specific rules remain unquoted. No blanket tax recovery, charge base or future rate is adopted.', ['SRC-0258','SRC-0261','SRC-0262']),
 ('E-C10',['E-S01','E-S03','E-S08'],'Researcher application to activity/state/time','Invitation and change work can occur without a completed event. Track incurred work, remaining work and supplier liabilities separately from completed-session counts.','researcher_cost_design','No no-show probability, cancellation rate, guaranteed turnout or loss provision is estimated.'),
 ('E-C11',['E-S08'],'Researcher application to role/package overlap','Count each person\'s required task time once. A moderator package may include preparation, travel or notes; avoid adding the same cash or resource cost again when integrating a quote.','researcher_cost_design','This component does not value labour or combine a staffing package with its included hourly resources.'),
 ('E-C12',['E-S03','E-S04','E-S05'],'Researcher application to journey and currency scope','Travel is scoped by traveller, route, date, mode, payer, flexibility and necessary accommodation. Keep staff travel time separate from fares and avoid duplicating work done during travel.','researcher_cost_design','No origin, Texas city, fare, hotel, per diem, foreign exchange rate or reimbursement promise is assumed.')]
claim_map={}
for i,spec in enumerate(claim_specs):
    ident,sids,locator,body,kind,limits,*old=spec
    cid=f'CLM-{599+i:04}';claim_map[ident]=cid
    row={'claim_id':cid,'source_ids':[source_map[v]for v in sids]+(old[0]if old else[]),
        'locator':locator,'claim_text':body,'evidence_class':kind,'metric':None,'value':None,'unit':None,
        'denominator':None,'question_wording':None,'population':None,'time_period':None,'support_checked':True,
        'review_mode':'Selected primary sections inspected; researcher applications distinguished from publisher statements.',
        'interpretation_limits':limits,'status':'T05E_desktop_design_context','publication_status':'working',
        'audit_record_origin':'04-table/research-notes/t05-event-costs/evidence/claim-candidates.json','t05e_claim_candidate_id':ident}
    claims['records'].append(row)
for doc in [sources,claims]:doc['updated_on']='2026-11-01'
save('02-evidence/registers/sources.json',sources);save('02-evidence/registers/claims.json',claims)
save('04-table/research-notes/t05-event-costs/evidence/source-candidates.json',{'records':adopted})
save('04-table/research-notes/t05-event-costs/evidence/claim-candidates.json',{'records':claims['records'][-12:]})
save('08-qa/T05E-record-map.json',{'date':'2026-11-01','source_map':source_map,'claim_map':claim_map,'new_source_routes':7,'new_claim_records':12,'canonical_sources':256,'canonical_claims':520,'financial_inputs_added':0})

specs=[
 ('Event remit and responsibilities','event','coordination',1.5,3,5,'Agree purpose, actual organiser/venue responsibilities and intended output.'),
 ('Venue, privacy and access assessment','event','coordination',1.5,3,5,'Review feasible capacity, access, conversation privacy, layout and proportionate arrangements.'),
 ('Supplier scope and terms coordination','event','coordination',1,2,4,'Review actual availability, charge bases, guaranteed covers, payment and cancellation terms.'),
 ('Participant pool and suitability map','event','coordination',1.5,3,5,'Identify a relevant pool. Public contacts are not recruited or permissioned participants.'),
 ('Individual invitation attempt','attempt','coordination',.1,.25,.5,'One actual individual approach or follow-up, including an unsuccessful attempt. No conversion assumed.'),
 ('Participant suitability and permissions','confirmed person','coordination',.25,.5,1,'Relevant fit, employer hospitality acceptability and participation/use choices. Not consent to unrelated marketing.'),
 ('Confirmed-person logistics','confirmed person','coordination',.15,.25,.5,'One ordinary scheduling and practical-information cycle, not every message.'),
 ('Access or dietary coordination case','case','coordination',.25,.5,1,'Only necessary additional handling beyond ordinary logistics. Keep sensitive detail out of this model.'),
 ('Material attendance or date change','change case','coordination',.1,.25,.75,'Actual extra handling, including withdrawals/replacements; do not derive from a guessed no-show rate.'),
 ('Moderator topic and process preparation','session','moderation',1.5,3,5,'Use existing permitted research; agree neutral process, boundaries and participation. New research belongs in its production task.'),
 ('Moderator live delivery','person-hour','moderation',1,1,1,'Actual required live person-hours, including each genuine co-moderator. Do not multiply every preparation task by every role.'),
 ('Moderator debrief and necessary actions','session','moderation',.5,1,2,'Bounded agreed actions and handover, excluding separate research writing or supplier reconciliation.'),
 ('Host preparation and guest liaison','host assignment','hosting',.5,1,2,'Actual host tasks not already performed in coordination or moderator preparation.'),
 ('Host live work','person-hour','hosting',1,1,1,'Actual hosting person-hours; if the same person moderates, do not count simultaneous elapsed work twice.'),
 ('Onsite setup, liaison and close','event','coordination',1,2,4,'Total additional person-hours across actual workers. Includes proportionate venue/emergency liaison, not duplicate live role hours.'),
 ('Permitted live note-taking','person-hour','research support',1,1,1,'Optional and permission-dependent. No recording or transcription service is assumed.'),
 ('Agreed event synthesis and review','output','research support',1.5,3,5,'Only a selected separate output. Map to existing report/cycle-note work when the same output serves both.'),
 ('Release and participant follow-through','batch','coordination',.5,1,2,'One actual permitted batch and ordinary follow-through. Do not duplicate WS12 distribution or WS20 cycle-note work.'),
 ('Supplier reconciliation and closure','event','coordination',.5,1,2,'Check final supplier bill, credits and open actions. Distinct from customer invoice/receipt work.'),
 ('Travel arrangements','booking case','coordination',.25,.5,1,'One actual journey/accommodation arrangement; shared booking only once, genuine extra handling separately.'),
 ('Additional staff travel time','person-hour','travel time',1,1,1,'Only time not already counted as productive work or included elsewhere. Actual paid/cash/resource treatment remains to be chosen.'),
 ('Unallocated incurred or exception work','person-hour','actual appropriate role',1,1,1,'Use only for identifiable necessary work not already in the rows above. Cancellation does not erase incurred work. Never add the same preparation twice.')]
tasks=[]
for i,(name,unit,role,low,working,high,note)in enumerate(specs,1):
    tasks.append({'task_id':f'WE{i:02}','label':name,'quantity_unit':unit,'role_context':role,
        'planning_hours_per_unit':{'low':low,'working':working,'high':high},'quantity':None,
        'basis':'Untimed researcher planning allowance, not a supplier quote, staffing promise, rate or time observation.',
        'counting_note':note,'source_claim_ids':[claim_map['E-C10'],claim_map['E-C11']],
        'actual_work_records':[]})
external=[
 ('Venue and catering','Actual eligible consumption, minimum shortfall, hire and applicable charges, after a venue-specific reconciliation.'),
 ('External facilitation or hosting','Only an actually selected package. Record prep, live work, notes, travel and tax inclusions before combining with labour costs.'),
 ('Rail, air or other fares','Route/date/traveller-specific booking amount, restrictions and payer. Do not infer a fare from a promotional minimum.'),
 ('Accommodation','Necessary rooms/nights, actual rate and cancellation terms. No city or overnight stay is assumed.'),
 ('Local transfers or mileage reimbursement','Actual approved basis and eligible journeys; no automatic HMRC-rate reimbursement.'),
 ('Access or support provision','Only actual necessary provision, after clarifying responsibilities and arrangements.'),
 ('Participant expenses or honoraria','Only if actually agreed and permitted. Free attendance creates no reimbursement or incentive promise.'),
 ('Materials or equipment','Necessary items not supplied by the venue or included in an existing package.'),
 ('Platform or registration tools','Select only needed functionality. A free-ticket platform option does not price internal handling.'),
 ('Insurance or specialist advice','Only where applicable to the actual organiser/venue arrangements. No invented compulsory premium.'),
 ('Change or cancellation loss','Net nonrecoverable cost under actual terms, excluding deposits already included in the supplier final total.'),
 ('Other scoped direct cost','Identify the item, period, payer and nonoverlap basis before using.')]
data={'date':'2026-11-01','component_id':'T05E-event-operations','status':'prepared_internal_unpriced_event_component',
      'task_count':len(tasks),'tasks':tasks,'external_cost_rows':[{'cost_id':f'EC{i:02}','label':name,'scope_note':note,'selected':None,'amount_gbp':None,'basis':None}for i,(name,note)in enumerate(external,1)],
      'counts':{'practitioners':None,'additional_team':None,'additional_guests':None,'billed_covers':None,'room_capacity':None,'menu_capacity':None},
      'all_counts_and_amounts_start_blank':True,'effort_case_default':'working','effort_cases_are_not_empirical_bounds':True,
      'financial_register_extended':False,'shared_financial_inputs_preserved':70,
      'workload_assumptions_not_adopted_programme_quantities':True,'labour_not_monetised':True,
      'all_in_budget_available':False,'full_financial_model_complete':False,'selected_event_date':None,'selected_city':None,
      'selected_venue':None,'actual_quotes':[],'actual_participants':[],'actual_timesheets':[],'actual_bookings':[],
      'source_ids':list(source_map.values()),'claim_ids':list(claim_map.values()),
      'prior_venue_source_ids':['SRC-0258','SRC-0259','SRC-0260','SRC-0261','SRC-0262'],
      'scope_fee_changed':False,'fourteen_core_questions_unchanged':True,'practitioner_free_full_research_preserved':True,
      'collection_activated':False,'external_actions':[],
      'workbook_path':'/Users/satwikkumar/Documents/Codex/2026-10-09/oka/outputs/jga-t05-event-costs-2026-11-01/Event planning and direct costs.xlsx',
      'integration_requirements':['Match event to selected programme, city, date and edition; do not infer recurring cadence.',
       'Carry incurred work and future obligations across the correct periods.',
       'Reconcile package scope and hours to avoid double cash/resource valuation.',
       'Keep cash payment, resource use, full supplier bill and refundable/credited deposit distinct.',
       'Use original currencies and dated FX before combining cross-country amounts.',
       'Use actual applicable task skill/rate; do not copy a research or sales proxy to moderation.',
       'Show staff travel time separately from fare cash and productive work.',
       'Preserve report-free practitioner benefits, permissions and no implied guaranteed attendance.']}
save('04-table/T05-event-cost-map.json',data)
text('04-table/research-notes/t05-event-costs/WORK-PLAN.md','''# Event operations component

1 November 2026. Internal work only.

Review proportionate official event-planning guidance, facilitation work, travel restrictions and support, and optional registration tools. Preserve prior venue evidence and the seventy shared financial inputs. Prepare a task catalogue with explicit untimed effort assumptions, blank activity counts and unpriced selected direct costs. Test distinct seats, billable covers, missing versus zero values, cancellation work and nonoverlap. Keep original workbooks unchanged. Only after this component and its review should dated cash and the complete matched programme model be integrated.

The workbook serves the user and later JGA feasibility review. It is a GBP entry template for one explicitly scoped event/workload, not a confirmed UK or international programme budget. Labour is measured in person-hours, not monetised here. New planning allowances remain in the separate component until programme integration; no financial-register amount or forecast is added.
''')
text('04-table/T05-EVENT-OPERATIONS-AND-TRAVEL.md','''# Event operations, moderation and travel

1 November 2026. Prepared for internal review. No event is selected, quoted, recruited or booked.

## What this component establishes

The event increment needs organising work as well as hospitality spending. The [structured component](T05-event-cost-map.json) separates 22 work tasks, twelve possible direct-cost areas and six attendance/capacity inputs. The accompanying workbook is an entry and calculation tool. Its activity counts and monetary amounts start blank; it does not produce an invented all-in price.

The strongest practical conclusion is that attendee fit and usable discussion are the product. A room and meal alone do not establish that value. Protect participant suitability, a useful neutral process and the agreed output before optimising the dinner bill. A small event can use modest arrangements; this is not a conference production plan.

## Organising effort

[HSE planning guidance](https://www.hse.gov.uk/event-safety/getting-started.htm) links organising arrangements to event scale, audience, location, duration and suitable resources. [Its delivery guidance](https://www.hse.gov.uk/event-safety/managing-an-event.htm) includes coordination, competent oversight and review, and allows a simple checklist for small events. We apply these principles proportionately to a private discussion. No special staffing ratio, formal event certification or universal extra contractor is prescribed by this research.

The catalogue covers remit/roles, venue assessment, supplier terms, a relevant participant pool, individual invitations, suitability and permission handling, practical arrangements, material changes, moderation, hosting, onsite coordination, optional notes/output, release, supplier reconciliation and travel handling. Low/working/high hours are researcher planning allowances. They are not observed timesheets, minimum service promises or confidence intervals. Choose actual activities and refine them after delivery experience.

Attempts remain separate from accepted people. Two invitations and three follow-ups can create five genuine attempts; they do not establish five prospects willing to attend. Invitation work may remain valuable or incurred even when no event happens. No attendance conversion or no-show percentage has been inserted.

## Moderator and host work

The [IAF competency framework](https://iaf-world.org/iaf-core-competencies/) describes role/deliverable agreement, process design, participation and useful outcomes. It supports costing preparation and follow-through beside live facilitation. It does not quote a fee or demonstrate that any named person is available or qualified for this specific discussion.

For live work, enter actual person-hours. Two required moderators for a two-hour discussion create four live person-hours. If one person hosts and moderates during the same two-hour period, count their elapsed work once, with any genuinely additional preparation separately. A note-taker is optional and permission-dependent. No audio recording, transcription or automatic AI processing is assumed.

A supplier may quote a package covering design, live moderation, notes, travel or tax. Inspect those inclusions before adding individual labour values or reimbursements. This component keeps labour unpriced, so it does not silently treat a research or administrative benchmark as a moderator rate. Full resource integration still needs the appropriate actual rate and package treatment.

## Seats, attendance and the venue bill

Count practitioners, additional distinct team members and additional guests once each. A practitioner who also moderates occupies one place. Sponsors have no automatic seat entitlement. Planned attendees, confirmations, people present on the day and billed covers are different measures.

The [earlier venue screen](T04-PUBLIC-COST-SCREEN.md) remains intact. Its current published examples show why total-party capacity matters: the Hawksmoor private room has a 14-person ceiling, so fifteen practitioners cannot fit before adding anyone else. Benares' Berkeley room and tasting-menu limits are sixteen, while the larger Dover room has a different range. Corrigan's boardroom and reception capacities represent different layouts. None is selected or quoted for 2027.

An illustration with fifteen practitioners and two additional people needs seventeen places. If two people withdraw after a nonreducible cover deadline, actual attendance can fall without the bill falling. Do not automatically calculate catering from attendance on the day. Confirm actual guarantees, substitutions and chargeable covers.

Calculate eligible consumption, any applicable minimum shortfall, hire and each charge on its actual base. VAT-inclusive figures must not receive VAT a second time. Preserve discretionary service descriptions. A deposit credited against the final bill belongs in payment timing and the outstanding balance; it is not another expense. Unknown minimums, cancellation terms and charge bases remain unknown. Prior menus are historical/current published context, not future quotations.

## Travel and participation support

Use a named traveller/party, purpose, origin, destination, date, mode, payer, change terms and any necessary overnight stay. The [National Rail Advance-ticket terms](https://www.nationalrail.co.uk/tickets-railcards-and-offers/ticket-types/advance-tickets/) show that date/train restrictions and change/refund conditions matter alongside price. A promotional fare is not a dependable route-specific return cost. No fare or hotel rate has been adopted without a route and date.

[Passenger Assist](https://www.nationalrail.co.uk/help-and-assistance/passenger-assist/) provides a route to arrange relevant rail assistance. Actual station, train and venue arrangements still need checking. Ask only for necessary arrangements through the approved process; do not put personal medical detail in a cost workbook.

[HMRC's mileage page](https://www.gov.uk/expenses-and-benefits-business-travel-mileage/rules-for-tax) addresses employee payment tax treatment. It does not set JGA's reimbursement promise or price every journey. No numeric mileage rate is loaded into this component. Free attendance does not imply paid travel, accommodation or honoraria. Staff time spent travelling is separate from fares; exclude hours already counted as productive work.

The annual Texas city remains undecided. UK costs cannot be multiplied across international events. Before integration, define each event's route, original currency, applicable taxes, actual payer and dated FX basis. No international flight, city, hotel or overnight requirement is invented here.

## Tools and output choices

[Eventbrite's published pricing](https://www.eventbrite.com/organizer/pricing/) offers free-ticket publication without ticketing-platform fees. This is an optional route, not a selected system or an assumption that organising is free. Manual invitations may be sufficient for a small private group once the approved data arrangements exist. Do not buy software or add a public registration page by default.

An event summary is optional. If the same permitted synthesis also serves the report or an existing cycle note, cost the actual shared work once. Keep participant publication permissions and indirect-identification review. Attendance is not automatic permission to publish a quote, use a logo or approach someone for sales.

## How to use the workbook

On Event costs, choose an effort case, enter actual or deliberately assumed counts, and identify the selected direct costs. Use GBP amounts only after a documented currency/basis reconciliation. Explicitly unselected rows return zero; selected rows with missing amounts keep the direct-cost subtotal unavailable. Zero cost must have a valid stated basis. On Event work, select only genuinely required activities and enter their quantities. An explicit zero differs from an unknown blank. All required quantities must be resolved before the workload total is available.

For a cancellation, enter the incurred quantity on the relevant task, not a completed-event count of zero. Use the exception row only for extra work not already represented. Track money recoverable and liabilities separately in the later cash schedule. The workbook's direct-cost subtotal excludes monetised labour and is not the full programme cost.

## Checks and next step

The component is checked using constructed cases, not actual attendees or operations. Preservation checks cover the original workbooks, seventy shared financial inputs, prior research and client drafts. The original fourteen questions, 6–10 distinct report-contributor target, up-to-four T03 exploratory events, agreed fee and free practitioner research remain unchanged. A future dinner is not automatically one of those exploratory events or an original research contribution.

Next: review this component, then construct the dated receipt/payment and remaining-obligation schedule. Integrate common research, service/sales and event work into matched A/B cases on the same horizon. Full cash/resource results, scenario sensitivities and a final feasibility recommendation remain open. Nothing has been sent and no spend is authorised.
''')

search=load('02-evidence/registers/searches.json');search['records'].append({'search_id':'SCH-0029','date':'2026-11-01','purpose':'T05E proportionate event operations, moderation, travel and optional tools','queries':['site.hse.gov.uk event safety planning managing event organiser responsibilities','site.nationalrail.co.uk advance tickets specific train non refundable','site.gov.uk expenses benefits business travel mileage approved rates','site.iaf-world.org facilitator competencies prepare appropriate group processes','site.eventbrite.com organizer pricing free events'],'related_source_ids':list(source_map.values()),'outcome':'Seven official originals retained and twelve bounded statements/applications appended. Old IAF member-domain route redirected to unrelated content and was excluded; the current official framework route was used. No enquiry, booking, account action or spend.'});search['updated_on']='2026-11-01';save('02-evidence/registers/searches.json',search)
print(json.dumps({'sources':len(sources['records']),'claims':len(claims['records']),'tasks':len(tasks),'source_map':source_map},indent=2))
