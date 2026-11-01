from pathlib import Path
import json,hashlib
ROOT=Path(__file__).resolve().parents[1]
B='04-table/research-notes/t05-cash'
def load(p):return json.loads((ROOT/p).read_text())
def save(p,d):
 q=ROOT/p;q.parent.mkdir(parents=True,exist_ok=True);q.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
def text(p,s):(ROOT/p).write_text(s.strip()+'\n')
pack=load(B+'/evidence/source-candidates.json')
reader=ROOT/B/'evidence/C-S01-selected-reader-paraphrase.txt'
reader.write_text('Selected primary British Business Bank web-reader sections inspected 1 November 2026. Cash receipts/payments over a period differ from profit. A profitable business can face a short-term shortage when supplier/service outgoings precede customer payment. Future projections help identify such timing risks. No business-specific forecast, buffer rule, credit product, borrowing recommendation, receipt date or current macroeconomic assertion is adopted. The article includes historical pandemic context. This is a researcher paraphrase, not retained original HTML.\n')
x=pack['records'][0];x.update(reader_note_path=str(reader.relative_to(ROOT)),reader_note_sha256=hashlib.sha256(reader.read_bytes()).hexdigest(),capture_kind='browser_reader_paraphrase_not_original')
save(B+'/evidence/source-candidates.json',pack)
s=load('02-evidence/registers/sources.json');c=load('02-evidence/registers/claims.json')
assert len(s['records'])==263 and len(c['records'])==537,'Append once only'
sm={}
for i,x in enumerate(pack['records'],296):
 assert x['url']not in {v['url']for v in s['records']}
 sid=f'SRC-{i:04}';sm[x['candidate_id']]=sid
 s['records'].append({'source_id':sid,'title':x['title'],'publisher':x['publisher'],'url':x['url'],'source_type':'official_cashflow_or_currency_guidance','review_status':'selected_relevant_sections_inspected','notes':'Managerial model context only. No statutory reporting/tax compliance, borrowing recommendation, current FX number or JGA cash estimate adopted.','accessed_on':'2026-11-01','published_date':None,'fieldwork_period':None,'population':None,'geography':'Publisher-scoped guidance; no foreign tax rule imported','sample_size':None,'method_available':None,'funding_or_commercial_interest':None,'capture_path':x.get('capture_path'),'capture_sha256':x.get('capture_sha256'),'reuse_status':'internal_selected_paraphrase','publication_eligibility':'final_context_check_required','related_topic_ids':['T05C'],'t05c_source_candidate_id':x['candidate_id'],'candidate_detail':x})
specs=[
 ('C-C01',['C-S01'],'Cash flow and profit sections','The British Business Bank distinguishes cash timing from profitability and describes shortfalls when outgoings precede customer payment.','official_guidance','No specific funding buffer, debt product, JGA forecast or current economic conclusion adopted.'),
 ('C-C02',['C-S02'],'Exchange-rates introduction and qualification','The Bank of England publishes daily spot reference rates and qualifies their authority; a published reference is not automatically a business transaction execution rate.','official_publication_context','No spot value retrieved or loaded. Foreign conversion direction, date, basis and actual fees must be explicit.'),
 ('C-C03',['C-S03'],'Opening balance, receipts, outgoings and closing balance','The Australian government guide rolls opening cash plus incoming less outgoing cash into closing cash and asks estimates to be labelled.','official_method_guidance','General cash arithmetic only. Australian tax treatment, GST rate, business pattern or statement certification not imported.'),
 ('C-C04',['C-S01','C-S03'],'Researcher application to invoice, receipt and assumption state','An expected receipt is a scenario input until cash occurs. A signed order, invoice, payment request or conditional acceptance balance does not establish a bank receipt date.','researcher_model_requirement','No new current-contract payment term or actual bank reconciliation. Source/assumption and timing must be supplied for selected cash legs.'),
 ('C-C05',[],'Researcher application to deposit, credit and refund objects','A credited deposit and remaining balance are cash legs against the same supplier object; a future-use credit is not a cash refund.','researcher_cash_and_obligation_requirement','Actual terms and payer/currency remain necessary. Economic expense, noncash entitlement and cash payment are not interchangeable.',['SRC-0248']),
 ('C-C06',['C-S01'],'Researcher application to daily timing','Monthly net cash can conceal earlier dated deficits. Date-end balances and a separately labelled same-day payments-first stress test are useful distinct views.','researcher_model_design','The payments-first calculation is a constructed sequencing stress, not observed intraday settlement or a universal required reserve.'),
 ('C-C07',['C-S02','C-S03'],'Researcher application to route, window and currency','Missing selected-scope dates, amounts or foreign FX basis should keep affected outputs unavailable; unselected event-only rows need not block a research-only case.','researcher_model_design','No automatic FX=1 for foreign currency, missing amount=0, future date, event frequency or funding receipt is adopted.'),
 ('C-C08',[],'Researcher application to promised, satisfied and remaining units','Payment and fulfilled benefit are different states. Remaining work, customer benefits, supplier payment and future-use credits require distinct typed units and timing.','researcher_model_design','Do not sum unlike units or treat positive projected cash as profit or discharge of unpaid/unfulfilled obligations. No remaining work cost is invented.',['SRC-0248'])]
cm={}
for i,(ident,ss,loc,body,kind,limits,*extra)in enumerate(specs,628):
 cid=f'CLM-{i:04}';cm[ident]=cid
 c['records'].append({'claim_id':cid,'source_ids':[sm[v]for v in ss]+(extra[0]if extra else[]),'locator':loc,'claim_text':body,'evidence_class':kind,'metric':None,'value':None,'unit':None,'denominator':None,'question_wording':None,'population':None,'time_period':None,'support_checked':True,'review_mode':'Selected official sections inspected; original/reader distinction retained; researcher application separately labelled.','interpretation_limits':limits,'status':'T05C_cash_design_context','publication_status':'working','audit_record_origin':B+'/evidence/claim-candidates.json','t05c_claim_candidate_id':ident})
for d in [s,c]:d['updated_on']='2026-11-01'
save('02-evidence/registers/sources.json',s);save('02-evidence/registers/claims.json',c);save(B+'/evidence/claim-candidates.json',{'records':c['records'][-8:]})
save('08-qa/T05C-record-map.json',{'date':'2026-11-01','source_map':sm,'claim_map':cm,'new_source_routes':3,'new_claim_records':8,'canonical_sources':266,'canonical_claims':545,'new_financial_inputs':0})
commission=load('00-control/scope-baseline.json')['commercial']
private=[]
for role,p in [('working_agreement_text',Path('/Users/satwikkumar/Documents/Codex/2026-10-09/oka/outputs/jga-agreement-2026-10-27/agreement-text.txt')),('supplied_payment_acknowledgement',Path('/Users/satwikkumar/.codex/attachments/733ae05b-08c5-41f6-a5f3-3ce9a9d1a435/Pasted text.txt'))]:private.append({'role':role,'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'independently_verified_executed_contract_or_bank_record':False})
model={'date':'2026-11-01','status':'prepared_cash_timing_and_remaining_unit_component_full_programme_pending','component_id':'T05C-cash-and-obligations','perspective':'JGA future research/event programme; current Riseklix commission is separate investment context','route_options':['A research only','B with events'],'default_route':'A','monthly_capacity':12,'default_display_months':12,'cash_leg_capacity':40,'obligation_capacity':24,'row_capacities_are_not_activity_forecasts':True,
 'start_month':None,'opening_cash_gbp':None,'cash_coverage_confirmed':None,'obligation_coverage_confirmed':None,'cash_legs':[],'obligations':[],'foreign_fx_inputs':[],'actual_bank_reconciliation':False,'current_commission_context':commission,'private_context_provenance':private,'commission_is_not_sponsorship_income':True,'conditional_balance_not_scheduled_automatically':True,
 'views':['monthly opening, receipts, payments, net and closing cash','peak additional funding on daily-end basis','separate same-day payments-first funding stress','typed remaining units, timing and expiry review','separate original-currency current commission context'],
 'integration_requirements':['Link each receipt/payment to its order/booking/source without counting deposits twice.','Keep forecast or reported cash status and source separate; no probability assigned.','Opening cash includes prior-period legs; do not replay them in the selected horizon.','Reconcile applicable gross cash, charges, refund and credit terms separately from economic cost.','Use explicit GBP per original-currency-unit factor/date/basis; fees are additional legs if not included.','Carry timed/triggered/unknown unfulfilled benefits and work beyond the horizon.','Join remaining work to actual skill/rate/capacity and avoid package/reuse duplication.','Check intraday payment ability and readiness before any commitment, not only positive period-end cash.','The full matched A/B pilot/annual cost/revenue/scenario model is still a separate build.'],
 'source_ids':list(sm.values())+['SRC-0248'],'claim_ids':list(cm.values()),'shared_financial_register_extended':False,'shared_financial_inputs_preserved':70,'prior_three_workbooks_changed':False,'new_actual_orders_or_quotes':[],'external_actions':[],'fieldwork_activated':False,'current_contract_fee_changed':False,'fourteen_core_questions_unchanged':True,'practitioner_free_full_research_preserved':True,'full_financial_model_complete':False,
 'workbook_path':'/Users/satwikkumar/Documents/Codex/2026-10-09/oka/outputs/jga-t05-cash-2026-11-01/Cash timing and obligations.xlsx','workbook_qa_path':'08-qa/t05c-workbook/verification.json','component_review_path':'08-qa/t05c-review/verification.json'}
save('04-table/T05-cash-map.json',model)
text('04-table/T05-CASH-TIMING-AND-OBLIGATIONS.md','''# Cash timing and remaining obligations

1 November 2026. Internal working component. This prepares cash and fulfilment logic; the complete programme budget and commercial recommendation remain open.

## What is now modelled

The workbook separates dated cash from remaining promises. Its three sheets are Cash plan, Cash legs and Obligations. The cash plan supports a selected research-only route or a route including event rows. Monthly results, daily-end funding need and a separate same-day payments-first stress all use the same selected dated legs. The obligation view keeps customer benefits, supplier payments, work and future-use credits as different objects with their own units.

Start month, opening cash, coverage confirmations and selected transactions remain unresolved. Reserved rows are storage capacity, not projected customers, events or contracts. No supplier term, price, receipt date, credit, booking or sales forecast has been entered as an actual observation.

## Research and source choices

The [British Business Bank cash-flow guide](https://www.british-business-bank.co.uk/business-guidance/guidance-articles/finance/what-is-cash-flow-how-do-you-manage-it) explains why a profitable business can still face a cash gap when service/supplier outgoings precede customer receipts. We use that timing distinction, without adopting its examples, a minimum cash buffer or financing advice.

The [Australian government guide](https://business.gov.au/finance/cash-flow/set-up-a-cash-flow-statement) provides the opening-plus-receipts-minus-payments roll-forward and asks estimates to be labelled. Its local tax rules and template figures are not imported into JGA's model. This is a managerial planning component rather than a statutory cash-flow statement.

The [Bank of England exchange-rate page](https://www.bankofengland.co.uk/statistics/exchange-rates) qualifies its published reference rates. No rate was taken from it. The workbook requires an explicit positive GBP-per-original-unit factor, dated basis and source for a selected EUR/USD leg. GBP-to-GBP needs no foreign conversion. Actual transaction spread/fees need their own applicable treatment; the calculator does not infer VAT recovery or other tax cash flows.

Earlier [iVentiv terms](https://www.iventiv.com/terms-and-conditions) distinguish future-use credits and postponement. This supports keeping a restricted credit separate from cash refunded. Those clauses and their differing payment intervals are not JGA terms.

## JGA's existing commission is a separate object

The agreed current project is US$1,500: US$1,000 report and US$500 Table feasibility. The user reported US$750 upfront received; the supplied acknowledgement replies to that payment request. The remaining US$750 depends on satisfactory completion and written acceptance under the preserved baseline. No fixed remaining-payment date is inferred from an old request due date or a working delivery target.

The generated working agreement and supplied acknowledgement are retained with hashes. They are not an independently retrieved executed copy or a bank reconciliation. An acknowledgement time is not automatically a bank settlement date.

For JGA this fee is an initial project investment. It is not partner revenue, a recurring edition cost or an automatically repeated event charge. The workbook shows the original-currency commission context separately; it does not load the US$750 as GBP opening cash, sponsorship income or a new future payment. If the selected cash period includes relevant payments, enter their actual or explicitly assumed dates and conversion once. If paid before the period, they are already reflected in the chosen opening-cash basis.

## Dated cash legs

Each used leg needs its scope, receipt/payment direction, linked object, date, original currency and amount, reported-observation or assumption class, and source/basis. EUR/USD conversion additionally needs a factor and date. The amounts are actual gross cash or clearly labelled scenario cash, with any applicable included charges described. A refund is a separate opposite-direction cash leg linked to the same supplier/customer object, not an invented negative expense or cancellation discount.

Unused rows are excluded. A used Event row is excluded from the research-only route; selecting the event route exposes its missing data. A used row with missing fields is unavailable, including outside-window selected legs. This deliberately requires a complete selected leg before it can be treated as known. Rows before the start month or after the displayed horizon remain visible but do not replay into current-period cash. Unpriced future work belongs in Obligations until its cash timing and amount are scoped.

The coverage confirmation means the model operator has included the cash legs relevant to this selected scope. It is not permission to spend, approval of a forecast or an independent assertion that the schedule is complete. Missing confirmation prevents a blank ledger appearing as a funded programme. Observed rows cannot be dated after the chosen evidence date. Assumed rows remain scenarios even when their expected payment falls before that date.

## Monthly cash and shorter funding gaps

Monthly opening cash rolls from the previous closing balance. Receipts and payments use inclusive month start and exclusive next-month start, so the last day is included and the next month is not counted twice. No forecast receipt is treated as received merely because an invoice or contract exists.

Daily-end balances are calculated from dates, so the cash legs do not need to be entered in chronological row order. The lowest date-end balance, including opening cash, determines additional funding needed on that basis. This does not insert a loan or financing plug.

Same-day netting can still hide a payment made before a receipt. The separate payments-first stress deducts all payments on a date before counting that date's receipts. It is a deliberately adverse sequencing illustration, not a statement about actual intraday settlement, a funding commitment or a required reserve. Actual settlement order and ability to fund a commitment still need checking.

## Deposits, balances, credits and refunds

A hypothetical supplier bill of £1,900 with a £500 credited deposit leaves £1,400 to pay. The two cash payments total £1,900. The deposit does not turn the economic bill into £2,400. Link all legs to the same booking/invoice object and reconcile the agreed total before integration.

A £500 future-use credit is different: it may carry an expiry, permitted use and replacement-service obligation while delivering no cash today. Record its units and terms in Obligations. Only an actual or explicitly assumed cash refund belongs in the cash schedule. A credit expiry is flagged for review; the model does not automatically forgive a debt, turn a credit into cash or assert a right has legally expired.

Refunds and replacement spending are separate dated legs when actually applicable. Do not add both a gross final supplier bill and the same deposit as another expense, or count a refund twice through a reduced payment and a separate receipt. No refundability, cancellation probability or recovery percentage has been invented.

## Remaining units and work still owed

Each selected obligation identifies its object, kind, description, unit, agreed units, satisfied/applied units and date, trigger or unknown timing. Remaining units are calculated only when valid. Unlike units are never added into a combined total. Paid money does not satisfy a customer benefit or complete remaining work; their own delivered units are needed.

The categories serve different directions: Customer benefit and Work describe output/effort still owed; Supplier payment describes a payment commitment in its stated units; Future-use credit describes a held noncash entitlement. Supplier delivery or an owed replacement service can have a separate appropriate benefit/work row. A cash payment can settle the payment object while leaving a delivery object open.

The cash view and obligation view have separate coverage/readiness. Cash can be calculated while unpriced or untimed obligations remain prominently unresolved. That prevents a positive cash balance from being presented as profit, spare distributable money or a completed programme. Future delivery beyond the horizon stays on the obligation list. Scope, capability, actual hours, rates and package/reuse overlap still need linking during full integration.

## What remains for the complete programme model

Join this cash component to research production, service/sales and event work using the same period, edition, original currencies and allocation basis. Reconcile all future payment legs with their economic costs, initial investment, actual reported payments and remaining commitments. A free or bundled copy remains a fulfilment benefit rather than an extra licence sale.

Then calculate the matched pilot/annual A/B results, conservative/base/optimistic scenarios, break-even, practical capacity and the agreed sensitivities. Do not assume event revenue uplift, use a generic licence price, multiply a UK event across four locations or select an unspecified Texas city. Actual buyer/member/practitioner work remains inactive and separate from this constructed planning component.

The earlier three workbooks, all seventy shared financial inputs, fourteen core questions, practitioner targets, free full practitioner research and agreed fee remain unchanged. No message, payment request, bank action, booking, hiring or spending occurred.
''')
search=load('02-evidence/registers/searches.json');search['records'].append({'search_id':'SCH-0031','date':'2026-11-01','purpose':'T05C cash timing and obligations method, currency direction and prior commission context','queries':['site.british-business-bank.co.uk cash flow forecast cash income payments','site.bankofengland.co.uk statistics exchange rates','site.business.gov.au cash flow statement forecast opening closing'],'related_source_ids':list(sm.values())+['SRC-0248'],'outcome':'Three official routes; two originals and one selected primary reader paraphrase. No FX value, tax treatment, borrowing recommendation, forecast or actual bank payment inferred. Current commission and private-source hashes are separate from programme receipts.'});search['updated_on']='2026-11-01';save('02-evidence/registers/searches.json',search)
print(json.dumps({'sources':len(s['records']),'claims':len(c['records']),'primary_originals':sum(bool(x.get('capture_path'))for x in s['records'])}))
