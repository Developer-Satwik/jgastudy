"""One-time append of bounded second-challenge evidence and separate review outputs."""
from pathlib import Path
from collections import Counter
import hashlib
import json

ROOT=Path(__file__).resolve().parents[1]
B='04-table/research-notes/t05c-second-check'
def load(p): return json.loads((ROOT/p).read_text())
def save(p,x):
    q=ROOT/p;q.parent.mkdir(parents=True,exist_ok=True);q.write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def text(p,x): (ROOT/p).write_text(x.strip()+'\n')
pack=load(B+'/evidence/source-candidates.json')
sources=load('02-evidence/registers/sources.json');claims=load('02-evidence/registers/claims.json')
assert len(sources['records'])==266 and len(claims['records'])==545,'One-time append only'
source_map={};new=0
for x in pack['records']:
    sid=x.get('canonical_reuse')
    if sid:
        s=next(s for s in sources['records']if s['source_id']==sid)
        assert s['url']==x['url']
        s.setdefault('additional_reviews',[]).append({'date':'2026-11-01','module':'T05C-second','origin':B+'/evidence/source-candidates.json','detail':x})
        if 'T05C-second' not in s['related_topic_ids']:s['related_topic_ids'].append('T05C-second')
    else:
        sid=f'SRC-{299+new:04}';new+=1
        assert x['url']not in {s['url']for s in sources['records']}
        ident=x['candidate_id'];field='3–31 January 2024'if ident=='CS-S01'else'15 January–7 February 2025'if ident=='CS-S02'else None
        sources['records'].append({'source_id':sid,'title':x['title'],'publisher':x['publisher'],'url':x['url'],
          'source_type':'official_payment_research'if ident in ['CS-S01','CS-S02']else'primary_publisher_annual_report'if ident in ['CS-S03','CS-S04']else'official_tax_context_not_JGA_advice',
          'review_status':'selected_relevant_sections_reviewed','notes':'Context for distinctions between commercial commitment, cash, supply and performance. No JGA payment probability, market price, renewal rate, accounting policy or tax amount adopted.',
          'accessed_on':'2026-11-01','published_date':{'CS-S01':'2024-09-19','CS-S02':'2025-07','CS-S03':'2025-02-13','CS-S04':'2026-02-12','CS-S05':'2019-05-08'}.get(ident),
          'fieldwork_period':field,'population':'Surveyed UK businesses, not JGA prospects'if field else None,'geography':'UK'if ident not in ['CS-S03','CS-S04']else'Gartner global corporate reporting; US accounting context',
          'sample_size':300 if ident=='CS-S01' else 1455 if ident=='CS-S02' else None,'method_available':True if field else None,
          'funding_or_commercial_interest':'Government commissioned research'if field else'Company reporting'if ident in ['CS-S03','CS-S04']else'Official guidance',
          'capture_path':x.get('capture_path'),'capture_sha256':x.get('capture_sha256'),'reuse_status':'internal_selected_paraphrase',
          'publication_eligibility':'final_context_and_rights_check_required','related_topic_ids':['T05C-second'],'t05c_second_source_candidate_id':ident,'candidate_detail':x})
    source_map[x['candidate_id']]=sid
assert new==7
specs=[
 ('CS-C01',['CS-S01'],'Introduction, payment drivers and conclusion','The 2024 DBT/IFF study used 300 January2024 telephone interviews and discusses invoice administration, payment processes, disputes and limited bargaining power. It does not establish definitive sector differences.','source_scoped_payment_research','Cross-sector self-report context, not a JGA collection-delay estimate, causal proof or trend against a differently designed study.'),
 ('CS-C02',['CS-S02'],'Executive summary, methodology and limitations, printed pp4,39,55','The July2025 DBT/London Economics study combines 1,455 January–February2025 survey responses with secondary-data/econometric and quantification work. It records staff effort and business consequences around late payment.','source_scoped_payment_research','No aggregate prevalence, hours, economy estimate or implied probability is entered into JGA costs or scenarios; its limitations and unlike definitions matter.'),
 ('CS-C03',['CS-S03'],'Revenue recognition policy, printed p22; Note9 contract balances','Gartner FY2024 distinguishes subscription service periods, completed conferences and consulting performance when describing revenue recognition. Billing, collection and performance remain different events.','publisher_accounting_context','One large publisher, not a JGA accounting policy, payroll-market rate or transferable margin, renewal or working-capital estimate.'),
 ('CS-C04',['CS-S04'],'Policy p23; Note9 contract balances p64 and footnote3','Gartner FY2025 describes deferred revenue arising from upfront payments or recognized receivables before performance. A deferred-revenue balance is not itself a cash-received measure.','publisher_accounting_context','Do not equate billed, deferred or contracted amounts with cleared cash; no reported dollar balance or margin is a JGA financial input.'),
 ('CS-C05',['CS-S05'],'Notice701/41 sections1.2,2.1,2.4,3.1,3.3','HMRC distinguishes sponsor benefits, money and support in goods/services. Actual supplies and circumstances can affect VAT treatment, including overseas publicity services.','official_tax_context','This establishes a scoping question only. No JGA VAT registration status, place of supply, rate, liability, recovery, valuation or tax payment date is determined.'),
 ('CS-C06',['CS-S06'],'VATTOS5120 deposits and pre-payments','HMRC describes part-payment deposits for identifiable supplies and says refundability or forfeiture depends on the contract; security deposits have separate treatment.','official_tax_context','No legal conclusion, generic refund assumption or automatic tax calculation for JGA. The cash object must identify what the payment actually is.'),
 ('CS-C07',['CS-S07'],'VATTOS5135 security-deposit treatment','HMRC describes security deposits distinct from initial consideration for a supply and discusses later offsets against hire charges.','official_tax_context','Do not reclassify every deposit as security, revenue, an expense or automatically refundable; determine the actual transaction and applicable treatment.'),
 ('CS-C08',['CS-R01'],'Payment, cancellation and substitution sections','The freshly inspected iVentiv page still gives differing generic invoice intervals and describes future-use credits, substitution, cancellation and exclusion of travel/accommodation responsibility.','publisher_terms_context','Those are not JGA terms. No single generic interval, refund right, credit expiry or travel recovery is adopted for the planned programme.'),
 ('CS-C09',['CS-R02'],'Membership sections5.1–5.5','The Payroll Centre terms distinguish membership package/user benefits, service periods and renewal or termination arrangements.','publisher_terms_context','Do not transfer auto-renewal, named-user rights, refund rules or price into The Table; existing promises can survive a displayed sales period.'),
 ('CS-C10',['CS-R03'],'Licensed report/graphic use and report types','ISG presents licensed marketing use and different provider-report, snapshot and insight assets. These are distinct scopes of rights/output.','publisher_offer_context','No public price, unlimited rights, licence duration or cash schedule is inferred. One funded bundle can contain several benefits without several receipts.'),
 ('CS-C11',['CS-R04'],'Membership benefits and Council membership sections','The Conference Board distinguishes organisational insight access and a vetted individual-executive Council offering.','publisher_offer_context','Different access and peer benefits are not interchangeable units. No audience size, JGA membership demand or payment/renewal pattern is adopted.'),
 ('CS-C12',['CS-R05','CS-R06','CS-R07','CS-R08','CS-R09','CS-R10'],'Preserved service/case descriptions and R02 competitor challenge','Six earlier recruiter comparisons distinguish permanent hiring, interim coverage, search and broader advisory/project services. Their public scope descriptions do not establish payment schedules or actual contracted payroll results.','researcher_comparator_application','Retained dated context was re-read, not a new live price audit. No placement fee, candidate pay cycle, conversion fee or sponsor value is a JGA input.'),
 ('CS-C13',['CS-R11','CS-R03','CS-R04'],'Preserved JGA podcast context and public research/community alternatives','JGA content and public research/community access can be relevant alternatives or useful inputs; visibility, guest participation and engagement do not establish a paid Table contract.','researcher_market_application','No permission, commercial conversion, audience availability, partner commitment or new outreach follows.'),
 ('CS-C14',['CS-S01','CS-S04','CS-R01'],'Researcher object/settlement application','Reconcile each real order, invoice, deposit, remaining balance, net settlement, fee and refund once. Distinct row IDs alone cannot prevent one transaction appearing under two IDs.','researcher_model_requirement','The cash component is a dated-leg calculator, not an automatic order or bank reconciliation. Original arithmetic is not thereby disproved.'),
 ('CS-C15',['CS-S01','CS-S04','CS-S05','CS-S06','CS-S07'],'Researcher evidence/state and noncash application','Track the meaning of observed evidence and the transaction stage. A signature, invoice or payment promise is not cleared available cash; noncash support is not bank funding.','researcher_model_requirement','No new legal restriction, account ownership rule, banking arrangement or sponsor contract is assumed. Record actual gross/net and cash/tax basis when applicable.'),
 ('CS-C16',['CS-S03','CS-S04','CS-R01'],'Researcher historical/counterfactual route application','Compare routes from the same decision date and scope. Already incurred or unavoidable obligations must not disappear solely because a prospective event route is deselected.','researcher_model_requirement','A research-only case chosen before commitment differs from a decision after an event deposit is paid. Preserve actual sunk cash and incremental future choices separately.'),
 ('CS-C17',['CS-R01','CS-R02','CS-R03','CS-R04'],'Researcher date/fulfilment application and preserved formula inspection','Carry remaining benefits/work across periods and test their actual due, use and expiry dates. Opening-date credit status is insufficient to detect all upcoming expiries inside the horizon.','researcher_model_requirement','No credit is converted to cash, automatically written off, renewed, fulfilled or valued. Add usable-date reminders and actual delivery/capacity linkage in the combined model.'),
 ('CS-C18',['CS-S01','CS-S02','CS-S03','CS-S04'],'Researcher scenario and delivery application','Test delayed or absent receipts and continuing fulfilment costs, including shared payer/approval dependencies. Keep cost, receipts, remaining units and available delivery capacity separate.','researcher_model_requirement','Illustrative scenarios are not projected probabilities, market forecasts or estimates calibrated from broad survey percentages or large-publisher accounts.')
]
claim_map={}
for i,(ident,ss,loc,body,kind,limit)in enumerate(specs):
    cid=f'CLM-{636+i:04}';claim_map[ident]=cid
    claims['records'].append({'claim_id':cid,'source_ids':[source_map[s]for s in ss],'locator':loc,'claim_text':body,'evidence_class':kind,'metric':None,'value':None,'unit':None,'denominator':None,'question_wording':None,'population':None,'time_period':None,'support_checked':True,'review_mode':'Selected official/publisher sections, retained comparator context and preserved formula/answer records inspected. Reader paraphrases remain separate from originals.','interpretation_limits':limit,'status':'T05C_second_desktop_context','publication_status':'working','audit_record_origin':B+'/evidence/claim-candidates.json','t05c_second_claim_candidate_id':ident})
for x in [sources,claims]:x['updated_on']='2026-11-01'
save('02-evidence/registers/sources.json',sources);save('02-evidence/registers/claims.json',claims)
save(B+'/evidence/claim-candidates.json',{'records':claims['records'][-18:]})
save('08-qa/T05C-second-check-record-map.json',{'date':'2026-11-01','source_map':source_map,'claim_map':claim_map,'new_source_routes':7,'reused_source_routes':11,'new_claim_records':18,'canonical_sources':273,'canonical_claims':563,'new_financial_inputs':0})
captures=[]
for x in pack['records']:
    for pathkey,hashkey,kind in [('capture_path','capture_sha256',x['capture_kind']),('parsed_path','parsed_sha256','parsed_original_text'),('reader_note_path','reader_note_sha256','browser_reader_paraphrase_not_original')]:
        if x.get(pathkey):captures.append({'candidate_id':x['candidate_id'],'source_id':source_map[x['candidate_id']],'path':x[pathkey],'sha256':x[hashkey],'kind':kind})
save('08-qa/T05C-second-check-captures.json',{'date':'2026-11-01','records':captures,'counts_by_kind':dict(Counter(x['kind']for x in captures))})

firms=[
 ('Portfolio Payroll','CS-R05','Permanent, temporary/contract and executive recruitment are separate service contexts.','An employer may need a simple replacement or temporary continuity rather than paid research/community access. No recruiter fee or invoice trigger is supplied.'),
 ('Frazer Jones','CS-R06','Publisher case combines interim and permanent HR/payroll rebuilding after organisational change.','Concurrent services and handover can require separate scope/work; public case wording does not supply payment milestones or completed payroll results.'),
 ('Oakleaf Partnership','CS-R07','Retained capabilities cover operational, implementation and leadership roles with interim/permanent routes.','A job or role category does not establish actual availability, who contracts/pays the worker or a sponsor budget.'),
 ('Middlemore','CS-R08','Retained live payroll-search body distinguishes permanent, interim leadership and transformation contexts.','Use the dated live body instead of older indexed wording. Declared expertise does not establish a fixed retainer structure or specific commercial terms.'),
 ('Hays','CS-R09','Payroll is included in a broader UK finance recruitment and workforce context.','Different project/staffing obligations need their own evidence; do not assign agency payroll funding, public fee rates or finance-wide outcomes to JGA.'),
 ('Robert Half','CS-R10','UK finance staffing and broader consulting support are distinct public contexts.','A UK Payroll Manager page is not evidence of a US Payroll Director engagement or its currency, billing, tax or payment schedule.'),
 ('JGA','CS-R11','Existing payroll content and expert discussions are preserved context.','Podcast participation is not a Table order or sponsor pipeline. The current commission remains separate project investment and reported-payment context.')]
save(B+'/comparator-map.json',{'date':'2026-11-01','recruitment_comparators':6,'JGA_contexts':1,'records':[{'firm':name,'source_ids':[source_map[s]],'retained_context':ctx,'cash_and_obligation_implication':use,'fresh_live_service_verification':False,'actual_buyer_or_partner':False,'measured_cost_or_demand':False}for name,s,ctx,use in firms],'scope_note':'Six recruitment comparisons plus JGA, distinct from the six T01 commercial mechanisms. No fee, cash term or empirical demand extrapolation.'})
models=load('04-table/T01-model-map.json')['models']
model_notes={
 'T01-M01':'A sponsored report order can combine outputs and rights; recognition is neither payment nor editorial control. No public fee/receipt schedule was established.',
 'T01-M02':'Licensed access and provider marketing assets need exact term, asset, user and use rights. One package receipt must not be counted again for included rights.',
 'T01-M03':'Annual service access can leave work and named-user obligations beyond the cash window. Comparator auto-renewal is not adopted for JGA.',
 'T01-M04':'Organisational access and a vetted peer seat are different benefits. Payment for one does not satisfy or sell the other by assumption.',
 'T01-M05':'A senior-payroll forum or public research is an alternative; public access does not establish Table admission price or paid conversion.',
 'T01-M06':'Approved attendee and sponsor benefits have different payers/obligations. Actual booking terms govern credits, cancellation and excluded travel.'}
save(B+'/business-model-check.json',{'date':'2026-11-01','model_count':6,'original_model_map_preserved':True,'records':[{'model_id':m['model_id'],'mechanism':m['mechanism'],'source_ids':m['source_ids'],'cash_obligation_implication':model_notes[m['model_id']],'jga_financial_input':False,'actual_demand_validated':False}for m in models]})
conditions=[
 ('C201','Evidence and transaction state',['CS-C01','CS-C04','CS-C15'],'Name the order/invoice/acceptance/settlement stage and actual evidence. Forecast cash dates remain assumptions until actual receipts/payments are supported.'),
 ('C202','Object and settlement reconciliation',['CS-C06','CS-C07','CS-C08','CS-C14'],'Reconcile real deposit, final bill, unpaid balance, fees, net cash, refund and credit by object and transaction identity. Row-ID uniqueness alone is insufficient.'),
 ('C203','Matched decision date and unavoidable costs',['CS-C03','CS-C04','CS-C16'],'Show the same decision/horizon and baseline in A/B. Preserve incurred or unavoidable cost/cash when future event activity is deselected; isolate genuinely avoidable future work.'),
 ('C204','Within-horizon expiry and remaining work',['CS-C09','CS-C10','CS-C11','CS-C17'],'Add due/use/expiry reminders and link continuing benefits to actual delivery dates, skill and capacity. Opening-date status alone misses upcoming expiry.'),
 ('C205','Gross/net, noncash and applicable tax basis',['CS-C05','CS-C06','CS-C07','CS-C15'],'Separate noncash support and displaced work from money; reconcile settlement fees and applicable taxes without automatically assigning a VAT rate or recovery.'),
 ('C206','Term, bundle, right and payer',['CS-C09','CS-C10','CS-C11','CS-C12','CS-C13'],'Specify contract term, asset/use/user rights, included benefits, responsible payer and country. Do not duplicate bundled sales or assume renewal.'),
 ('C207','Receipt and delivery stress together',['CS-C01','CS-C02','CS-C18'],'Stress delayed/no renewal and jointly dependent receipts against supplier dates and continuing fulfilment work. Do not assign a probability from aggregate survey or comparator data.'),
 ('C208','Proportionate implementation and current commission',['CS-C12','CS-C13','CS-C14','CS-C17','CS-C18'],'Use linked existing schedules, not a new research system or questionnaire. Keep the USD1500 commission, reported USD750 upfront and conditional USD750 balance distinct from future sponsor receipts; no scope, fee or participation change.')]
c={'date':'2026-11-01','status':'second_challenge_reviewed_required_integration_refinements_recorded','reviewer':'same_agent_second_check','independent_agent_review':False,
 'first_component_path':'04-table/T05-cash-map.json','source_ids':list(dict.fromkeys(source_map.values())),'claim_ids':list(claim_map.values()),'conditions':[{'condition_id':i,'label':l,'claim_ids':[claim_map[k]for k in ks],'required_treatment':t}for i,l,ks,t in conditions],
 'evidence_candidate_path':B+'/evidence/source-candidates.json','comparator_map_path':B+'/comparator-map.json','business_model_check_path':B+'/business-model-check.json','prior_study_bridge_path':B+'/prior-study/prior-study-bridge.json','cash_applications_path':B+'/cash-applications.json','review_checks_path':'08-qa/t05c-second-review/verification.json',
 'arithmetic_error_identified_in_defined_cash_unit':False,'presentation_or_integration_limits_identified':['Distinct IDs do not detect duplicated real transaction','Opening-date credit status does not flag all within-horizon expiries','Counterfactual route filter needs a matched incurred/unavoidable baseline'],
 'original_four_workbooks_changed':False,'financial_inputs_changed':False,'original_shared_financial_inputs':70,'programme_integration_still_required':True,'full_financial_model_complete':False,
 'current_contract_fee_changed':False,'fourteen_core_questions_unchanged':True,'practitioner_free_full_research_preserved':True,'actual_participants':[],'actual_quotes':[],'actual_bookings':[],'external_actions':[]}
save('04-table/T05C-second-challenge-map.json',c)
text('04-table/T05C-INTEGRATION-REFINEMENTS.md','''# Cash and remaining-obligation integration requirements

1 November 2026. Internal requirements before completing the matched programme model. Preserve the original four workbooks and seventy shared financial inputs.

| Requirement | Minimal practical implementation |
| --- | --- |
| Evidence and payment stage | Link the real order, invoice, acceptance condition and settlement evidence. An observed signature or invoice is not an observed cash receipt. Keep expected dates explicitly assumed. |
| One real transaction once | Reconcile credited deposit, remaining balance, gross bill, fee, net settlement, refund and credit by object and transaction identity. Different ledger IDs can still duplicate the same deposit. |
| Same decision date in A/B | Keep already incurred/unavoidable amounts in both relevant decision cases. Selecting research-only after a deposit was paid does not undo it. Before-commitment and after-commitment comparisons differ. |
| Expiry within the horizon | Show approaching credit use/expiry and delivery deadlines. The original opening-date status is not a rolling expiry alert. Review actual terms without automatic write-off or refund. |
| Fulfilment and usable capacity | Carry remaining units into actual dates, tasks and capable available people, including outside the displayed year. Cash received does not complete work or establish free capacity. |
| Gross, net, noncash and tax | Reconcile actual bank settlement to the selected gross/net basis. In-kind support is no cash receipt. Resolve applicable supply, tax and charge treatment for the actual entity and scope; do not hard-code generic VAT or tax recovery. |
| Term, rights, payer and bundle | Identify the exact asset, period, users/use and responsible payer. Count included rights once within the paid bundle. No automatic licence renewal, market price or cross-border terms. |
| Receipt and work stresses | Test delayed/absent receipts alongside fixed supplier dates and continuing fulfilment. Link same-payer or shared-approval delays when appropriate; no unsupported probability or collection-average assumption. |

Use existing records and a few linked fields, not extra compulsory interview questions or another software system. Keep the current USD1,500 commission separate from future partner revenue. Its reported USD750 upfront is not independently bank-reconciled, and its USD750 balance is conditional on satisfactory completion and written acceptance.

The [eighteen read-only applications](research-notes/t05c-second-check/cash-applications.json) show the required behaviour. They use constructed examples and independent arithmetic; they are not eighteen new workbook-engine tests or adopted forecasts. The first workbook's 65 engine tests and seven visual regions remain preserved.

Return to the [second-check findings](T05C-SECOND-CHECK-READOUT.md). Full-model implementation and authorised buyer/member/practitioner work remain open.
''')

text('04-table/T05C-SECOND-CHECK-READOUT.md','''# Cash and remaining obligations: second-check findings

1 November 2026. Internal same-agent review before full programme integration. No original workbook, price, forecast, commercial term or fourteen-question research scope was changed.

## What the second look changes

Keep the dated cash component, but add transaction reconciliation, a matched decision baseline and forward-looking deadline handling when combining it with the programme. Its defined cash arithmetic did not reveal an error in this review. Three practical limits matter: distinct ledger IDs do not prevent the same deposit being entered twice; credit status compares expiry with the opening month rather than flagging every upcoming expiry; and selecting a research-only route cannot itself undo an event cost already incurred.

Those distinctions make the eventual recommendation more useful. Nick needs to know what has to be funded, when cash is available and what work remains, rather than see a positive closing balance which quietly depends on a duplicate receipt, vanished obligation or unusable credit. No new forecast values were selected here.

## Historical payment evidence and newer research

The [2024 DBT/IFF executive summary](https://www.gov.uk/government/publications/late-payments-research-performance-and-practices-across-business/late-payments-research-understanding-variations-in-payment-performance-and-practices-across-business-sectors-and-sizes-html-executive-summary) is based on 300 January2024 telephone interviews. It discusses payment administration, invoice disputes, customer cash flow and negotiating power, while declining definitive sector conclusions. This supports testing actual invoice/approval dependencies rather than assuming a signed deal pays on the proposed date.

The [July2025 DBT/London Economics report](https://assets.publishing.service.gov.uk/media/688a089a6478525675738ff9/late_payments_research_impact_on_uk_economy.pdf) combines 1,455 January–February2025 survey responses with secondary-data/econometric and quantification work. It reinforces the relevance of collection effort and cash consequences. It is not a repeat of the same sample/method. We do not construct a rising/falling trend from the two publications, or turn their aggregate figures into JGA collection delays, hours, failure probabilities or cash buffers.

The useful forward view is therefore a transparent set of scenarios: a customer pays after a supplier is due; two instalments controlled by the same approval are both delayed; no renewal arrives while existing benefits remain owed. These are constructed decision tests, not probabilistic projections. Any actual driver needs its own evidence or an explicit assumption.

## Publisher and commercial-model comparison

Gartner's [FY2024 report](https://investor.gartner.com/static-files/ce1f14c0-f496-4672-85d0-c663ed815341) and [FY2025 report](https://investor.gartner.com/static-files/ba7bf87c-2680-4780-a345-8679d232b8a6) describe different timing for subscription service, conferences and consulting. The newer Note9 also distinguishes fees receivable, contract assets and deferred revenues. Deferred revenue can include recognized receivables before performance, not only collected money. A public balance-sheet label cannot therefore substitute for a cash receipt.

This is a useful historical mechanism check, not a scale model for The Table. Gartner's margins, renewal economics, bill-on-signing practices, accounting policy and global collection patterns are not JGA inputs. Direct retrieval of these PDFs returned HTTP403; selected primary web-reader paraphrases and locators are retained, not invented original files.

All six earlier T01 mechanisms were reconsidered in the [business-model check](research-notes/t05c-second-check/business-model-check.json): sponsored research, licensed intelligence, payroll support membership, research/practitioner community, senior payroll forum and sponsor-funded executive events. A sponsor package can bundle several outputs or rights while providing one payment. Annual access can leave service work after receipt. Organisation access and an individual peer seat can be different benefits. Public participation does not establish paid conversion.

Fresh inspection of ISG's provider services, The Payroll Centre's terms and The Conference Board's membership offerings supports these distinctions. Their actual rights, user limits, renewal conditions and prices remain their own. No Table auto-renewal, licence duration, membership price, payer or sales volume was inferred. iVentiv's freshly inspected terms still contain differing generic invoice intervals and distinct credit/cancellation/travel treatment; they cannot supply one JGA due date or a cash-refund promise.

## Six recruiter comparisons and JGA's position

The [comparator map](research-notes/t05c-second-check/comparator-map.json) revisits the preserved service/case evidence for Portfolio Payroll, Frazer Jones, Oakleaf Partnership, Middlemore, Hays and Robert Half, plus JGA context. These are separate from the six commercial mechanisms above.

Portfolio's permanent/temporary/executive routes, Frazer Jones's combined interim/permanent change case, Oakleaf's varied role needs and Middlemore's scoped search work show why a generic commercial unit is inadequate. Hays and Robert Half also cover broader staffing/advisory contexts; their UK finance descriptions are not US director-level assignments or payroll-specific outcomes. The dated public context was re-read rather than represented as a fresh live fee audit.

No inspected comparator context gives a reliable JGA placement fee, retainer stage, worker payment cycle, candidate conversion fee or sponsor budget. JGA's podcast and existing client relationships may inform useful content or introductions, but a guest, recommendation, free resource or visible recruiter is not a paid Table order. Ordinary replacement/growth needs remain relevant alongside complex international roles.

## What the earlier prompt study contributes

The [saved-study bridge](research-notes/t05c-second-check/prior-study/prior-study-bridge.json) links four deliberately different questions to32 preserved answers: confidential retained search, a US domestic director hire, ordinary UK replacement and interim cover alongside permanent search. Four selected answers were re-read in full, and132 exact text/hash/index checks passed. No models were rerun.

Our prompts supplied those hiring situations; tools and repeats are not independent employers. Generated suggestions about fees, guarantees, notice periods, day rates or handover weeks are questions to verify, not contractual terms or observed demand. In particular, a public vacancy is not a successful placement; an interim plus permanent brief is not automatically one bill; and a UK service declaration cannot supply US payer/currency/tax facts. The original source-status limitations remain unchanged.

## Cash, supply and noncash support

The selected [HMRC sponsorship notice](https://www.gov.uk/guidance/sponsorship-and-vat-notice-70141) distinguishes cash and goods/services given for benefits. The [deposit](https://www.gov.uk/hmrc-internal-manuals/vat-time-of-supply/vattos5120) and [security-deposit](https://www.gov.uk/hmrc-internal-manuals/vat-time-of-supply/vattos5135) sections show why the word deposit alone is insufficient. A part-payment, security amount and restricted future-use credit have different meanings.

For the model, record what is exchanged, the actual supplier/customer, benefit and settlement. A venue supplied in kind does not fund another invoice. It may displace only the specific cash/resource work it actually replaces, while a sponsor benefit remains to be delivered. A net bank settlement should reconcile to gross receipt, conversion and fees; do not enter net receipt and deduct the same fee again. Applicable tax and charge treatment needs actual scope/entity facts. This review calculates no JGA tax, determines no legal status and presumes no VAT rate or recovery.

## Read-only applications and identified limits

Eighteen [constructed applications](research-notes/t05c-second-check/cash-applications.json) cover delayed cash, same-day sequencing, deposit/balance conservation, duplicate transaction identity, route switching after commitment, opening balances, annual service carryover, in-kind support, net settlement, foreign conversion, within-year expiry, credits, partial fulfilment, bundled rights, correlated delay, nonrenewal, negative opening cash and leap-day boundaries.

The review independently reconciled150 saved formula caches and inspected governing formulas. It did not insert these examples into the workbook engine or claim new native Excel verification. The original65 artifact-engine tests and seven reviewed rendered regions remain intact.

The duplicate-deposit case demonstrates a real reconciliation requirement: two distinct valid row IDs can sum the same £500 deposit twice, overstating a £1,900 bill's cash by £500. This does not contradict the calculator's entered-leg sum; it shows why correct arithmetic requires correct transaction identity. The expiry example likewise shows a £500 credit expiring in February remains Open at a November start, even in a twelve-month view. An upcoming-use reminder is needed before treating that credit as a future resource.

The route-switch case is a decision-scope issue: before commitment an event can be avoidable; after a nonrefundable deposit is paid the historic cash cannot disappear. Assign incurred/unavoidable amounts to the relevant common baseline, carry them into opening cash when already paid and compare only actual avoidable future choices. Do not replay the earlier payment or claim the same deposit as a second economic cost.

## The next step, without expanding the project

Use the [integration requirements](T05C-INTEGRATION-REFINEMENTS.md) when joining research, service/sales, event, cash and remaining work into matched pilot/annual A/B cases. Keep the same edition, decision date, benefit and horizon basis. Link remaining units to actual dates, task rates and capable available people; price and capacity remain unresolved until supported or explicitly assumed.

The current USD1,500 commission remains separate initial project investment: USD1,000 report, USD500 Table; USD750 upfront is user-reported received and supported by the supplied acknowledgement, not independently bank-reconciled. USD750 remains conditional on satisfactory completion and written acceptance. No new due date, revenue label, fee or settlement date was inferred.

All four original workbooks,70 financial inputs,81 findings,14 core questions and free full practitioner research are preserved. The complete programme model, actual buyer/member/practitioner collection and final publication remain open. No messages, enquiries, bookings, hiring, spending or payment actions occurred.
''')

searches=load('02-evidence/registers/searches.json');searches['records'].append({'search_id':'SCH-0032','date':'2026-11-01','purpose':'T05C second challenge: historical/newer payment evidence, publisher performance/cash, rights/terms, tax-context distinctions, six recruiter comparisons and saved-study premises','queries':['site.gov.uk late payments research2024 and2025 methods','Gartner FY2024 FY2025 contract liabilities revenue recognition','HMRC sponsorship VAT deposits security deposits'],'related_source_ids':list(dict.fromkeys(source_map.values())),'outcome':'Seven new routes, eleven canonical reuses, eighteen bounded records. Five new originals, two primary-reader paraphrases. No aggregate collection rate, competitor price, VAT amount, renewal or new forecast adopted.'});searches['updated_on']='2026-11-01';save('02-evidence/registers/searches.json',searches)
changes=load('00-control/changes.json');changes['records'].append({'change_id':'CHG-033','date':'2026-11-01','type':'T05C cash component second challenge','description':'Historical/newer payment research, publisher timing, six recruiter contexts and six commercial mechanisms,32 earlier saved answers and18 read-only applications challenge cash and remaining work. Eight integration conditions record transaction identity, matched incurred baseline, within-horizon expiry, gross/net/noncash, terms and delivery stresses.273 sources/563 bounded records;81 findings and70 inputs unchanged. All four workbooks preserved; full programme integration remains open. No external action.'});changes['updated_on']='2026-11-01';save('00-control/changes.json',changes)
decisions=load('00-control/decisions.json');decisions['records'].append({'decision_id':'DEC-015','date':'2026-11-01','status':'internal_cash_second_challenge','decision':'Preserve the defined cash calculator and require object/settlement reconciliation, matched incurred/unavoidable decision baselines and within-horizon expiry/fulfilment handling in the combined model. Separate payment stage, noncash support, rights and actual available capacity.','basis':'Source-scoped historical/current evidence, retained prior-study contexts and read-only constructed applications. No arithmetic defect identified within defined entered-leg scope; integration/presentation limits explicitly recorded.','requires_client_approval':False});decisions['updated_on']='2026-11-01';save('00-control/decisions.json',decisions)
wp=load('00-control/work-packages.json')
for x in wp['records']:
    if x['work_package_id']=='WP14':
        x['status']='T05_cash_second_challenge_reviewed_full_model_in_progress';x['working_file']='04-table/T05C-SECOND-CHECK-READOUT.md';x['T05_cash_component_second_check_reviewed_on']='2026-11-01'
        x['evidence_of_completion']+=['04-table/T05C-second-challenge-map.json','08-qa/T05C-second-check-completion.json']
        x['next_design_input']='Integrate four preserved components into matched pilot/annual A/B cases. Apply eight cash-stage/object/decision-date/expiry/term/noncash/stress requirements and earlier work/capacity/package refinements. Dates, prices, rates, opening cash and activity remain sourced assumptions or unresolved; no external actions.'
wp['updated_on']='2026-11-01';save('00-control/work-packages.json',wp)
for file in ['00-control/CURRENT-STATUS.md','README.md']:
    p=ROOT/file;t=p.read_text();heading='## Latest checkpoint'if file.startswith('00')else'## Current work';start=t.index(heading);end=t.index('\n## ',start+len(heading))
    block=heading+'''

The [cash and remaining-obligations second check]('''+('../'if file.startswith('00')else'')+'''04-table/T05C-SECOND-CHECK-READOUT.md) is the current entry point. Historical/newer payment research, publisher timing, six recruiter comparisons, six commercial mechanisms and32 preserved prompt-study answers informed eight requirements for the combined programme model. Eighteen read-only applications distinguish transaction duplication, incurred-cost route scope and upcoming expiry from the original defined cash arithmetic.

Current totals: **273 source routes,563 bounded records,81 preserved findings and192 sources with primary originals**. All four workbooks and70 shared financial inputs remain unchanged. Start/opening cash, selected transactions and obligations remain unconfigured. This review adds no new price, forecast, fee, payment term or empirical buyer evidence.

Next: complete matched pilot/annual A/B programme integration with the recorded cost, work, capacity, package/reuse, cash and fulfilment requirements, then scenarios, break-even and sensitivities. Full model, actual collection and final client production remain open. Nothing sent, bought, booked, hired or activated.
'''
    p.write_text(t[:start]+block+t[end:])
p=ROOT/'05-analysis/CONTRADICTIONS-AND-GAPS.md';p.write_text(p.read_text()+'''

## Cash component second challenge,1 November2026

The [cash second-check readout](../04-table/T05C-SECOND-CHECK-READOUT.md) records object-level transaction reconciliation, a matched decision-date/incurred baseline and within-horizon credit expiry as required full-model refinements. Distinct row IDs can duplicate a real deposit; opening-date credit status is not an upcoming-expiry monitor; deselecting prospective events cannot undo actual paid/unavoidable costs. These are explicit scope/integration limits, not an identified arithmetic defect in the entered-leg calculator.

Payment stage, gross/net fees, noncash support, applicable tax scope, term/rights/bundle and continuing fulfilment require actual evidence or clearly labelled assumptions. Historical/newer surveys are not a trend or JGA collection-rate forecast; large-publisher contract liabilities are not necessarily cash. All four workbooks and70 inputs remain unchanged. Original fieldwork, bank reconciliation, executed-document retrieval and full programme integration remain open.
''')
print(json.dumps({'sources':len(sources['records']),'claims':len(claims['records']),'primary_original_records':sum(bool(s.get('capture_path'))for s in sources['records']),'capture_artifacts':len(captures),'conditions':len(conditions)}))
