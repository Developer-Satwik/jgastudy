"""Build read-only cash challenge applications and exact saved-study links.

Does not open a workbook for authoring or change the source study.
"""
from pathlib import Path
from datetime import date
from decimal import Decimal
import hashlib
import json
import zipfile
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT.parent.parent
B = '04-table/research-notes/t05c-second-check'

def load(path): return json.loads((ROOT / path).read_text())
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def save(path, value):
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n')

answer_path = BASE / 'sites/jga-discovery-report-2026-10-22/output/JGA-Research-Pack/data/all-answers.json'
index_path = BASE / 'sites/jgafinalcode/dist/data/answer-index.json'
answers = json.loads(answer_path.read_text())['answers']
index = {x['id']: x for x in json.loads(index_path.read_text())}
notes = {
    'S02-D': ('S02-D-claude-r1', 'Our prompt already specifies retained confidential search. The selected generated answer suggests stages, expenses and guarantees, including an unverified guarantee range. Treat these as possible questions about an engagement, never evidence of contracted fees, cash dates, a guarantee or permission to approach people.'),
    'S03-C': ('S03-C-perplexity-r1', 'Our question concerns a US domestic payroll director. The answer distinguishes public vacancy evidence from completed placements. Preserve country, actual contracting entity and service scope; neither a UK service page nor a generated US recommendation establishes payment terms, currency, tax treatment, a sale or payroll performance.'),
    'S07-A': ('S07-A-chatgpt-r2', 'The ordinary UK replacement prompt generates suggestions to brief recruiters and verify payment schedules, fees and guarantees. This supports retaining ordinary buying contexts beside complex searches. It does not observe an employer, prove that JGA won a fee or establish a Table membership/sponsorship sale.'),
    'S10-C': ('S10-C-claude-r2', 'The answer explicitly cannot verify a current director bench and raises separate interim/permanent scope and handover. Its day-rate, conversion, extension and overlap suggestions remain unverified generated advice. Carry actual concurrent work and separate agreements, not generic rates, overlap weeks or assumed six-month billing.')
}
questions, checks = [], []
def check(ok, label):
    if not ok: raise AssertionError(label)
    checks.append({'check': label, 'passed': True})
for q, (selected, note) in notes.items():
    rows = [x for x in answers if x['question'] == q]
    check(len(rows) == 8 and {x['product'] for x in rows} == {'ChatGPT','Gemini','Claude','Perplexity'}, 'Eight tool/repeat records: ' + q)
    links = []
    for a in rows:
        check(sha_text := hashlib.sha256(a['fullAnswer'].encode()).hexdigest() == a['answerHash'], 'Saved full-answer hash: ' + a['id'])
        check(hashlib.sha256(a['prompt'].encode()).hexdigest() == a['promptHash'], 'Saved prompt hash: ' + a['id'])
        check(index[a['id']]['fullAnswer'] == a['fullAnswer'] and index[a['id']]['prompt'] == a['prompt'], 'Final handover text/prompt identity: ' + a['id'])
        check(index[a['id']]['sourceStatus'] == a['sourceStatus'] and index[a['id']]['country'] == a['country'] and index[a['id']]['repeat'] == a['repeat'], 'Final index metadata identity: ' + a['id'])
        links.append({'answer_id': a['id'], 'product': a['product'], 'repeat': a['repeat'], 'country': a['country'], 'observed_at_utc': a['dateUtc'], 'full_answer_sha256': a['answerHash'], 'prompt_sha256': a['promptHash'], 'source_status': a['sourceStatus'], 'semantic_reread_for_this_review': a['id'] == selected, 'adopted_as_observed_buyer_or_financial_evidence': False})
    questions.append({'question_id':q,'prompt':rows[0]['prompt'],'prompt_sha256':rows[0]['promptHash'],'semantic_reread_answer_id':selected,'semantic_note':note,'answer_links':links})
bridge = {'date':'2026-11-01','purpose':'Use the earlier constructed AI discovery study to challenge service, geography, engagement and timing premises, without treating generated advice as real demand or cash evidence.', 'provenance':[{'role':'all_answers','path':str(answer_path.relative_to(BASE)),'sha256':sha(answer_path)},{'role':'final_answer_index','path':str(index_path.relative_to(BASE)),'sha256':sha(index_path)}], 'questions':questions,'linked_saved_answers':32,'semantic_rereads':4,'model_reruns':0,'new_demand_or_cost_estimates':False}
save(B+'/prior-study/prior-study-bridge.json', bridge)
save(B+'/prior-study/bridge-checks.json', {'date':'2026-11-01','status':'passed_exact_saved_data_linkage','check_count':len(checks),'checks':checks,'semantic_rereads_by_same_agent':4,'independent_agent_review':False})

# Independent arithmetic illustrations, not execution of new XLSX input scenarios.
checks = []
cases = []
def d(s): return date.fromisoformat(s)
def cash(opening, legs, start='2026-11-01', end='2026-12-01', route='B'):
    opening = Decimal(str(opening))
    selected = [x for x in legs if (x.get('scope','Common') == 'Common' or route == 'B') and d(start) <= d(x['date']) < d(end)]
    def amount(x): return Decimal(str(x['amount'])) * (1 if x['direction']=='Receipt' else -1)
    days = sorted({x['date'] for x in selected})
    ends = [opening + sum((amount(x) for x in selected if x['date'] <= day), Decimal(0)) for day in days]
    stress = [opening + sum((amount(x) for x in selected if x['date'] < day), Decimal(0)) - sum((Decimal(str(x['amount'])) for x in selected if x['date']==day and x['direction']=='Payment'), Decimal(0)) for day in days]
    return {'closing':float(opening + sum((amount(x) for x in selected),Decimal(0))), 'daily_end_funding':float(max(Decimal(0),-min([opening]+ends))), 'payments_first_stress':float(max(Decimal(0),-min([opening]+stress)))}
def leg(day, direction, amount, scope='Common'):
    return {'date':day,'direction':direction,'amount':amount,'scope':scope}
def add(ident, title, inputs, result, expected, treatment, coverage):
    check(result == expected, 'Constructed application reconciles: ' + ident)
    cases.append({'case_id':ident,'title':title,'constructed_inputs':inputs,'result':result,'expected':expected,'required_treatment':treatment,'current_component_coverage':coverage,'actual_observation':False,'new_financial_input':False,'workbook_recalculated_for_this_case':False})

l=[leg('2026-11-20','Payment',800),leg('2026-12-10','Receipt',1000)]
add('CA01','Late customer cash crosses the horizon',{'opening':0,'legs':l},cash(0,l),{'closing':-800.0,'daily_end_funding':800.0,'payments_first_stress':800.0},'Show the supplier requirement now and the later receipt in its actual/scenario period. Do not count an invoice as received.','Date arithmetic supported; invoice/settlement stages require the integrated object record.')
l=[leg('2026-11-20','Receipt',1000),leg('2026-11-20','Payment',800)]
add('CA02','Same-day positive end balance still has sequencing exposure',{'opening':0,'legs':l},cash(0,l),{'closing':200.0,'daily_end_funding':0.0,'payments_first_stress':800.0},'Retain the separate adverse sequencing stress; actual settlement order is unknown.','Supported dated-leg calculation.')
l=[leg('2026-11-05','Payment',500),leg('2026-11-25','Payment',1400)]
add('CA03','Deposit plus remaining balance',{'gross_bill':1900,'legs':l},{'payments':-cash(0,l)['closing'],'residual_bill':1900-500-1400},{'payments':1900.0,'residual_bill':0},'Reconcile the economic bill to credited deposit and unpaid balance; do not add the full bill as a third payment.','Cash arithmetic supported; object-level bill reconciliation remains manual.')
l=[leg('2026-11-05','Payment',500),leg('2026-11-05','Payment',500),leg('2026-11-25','Payment',1400)]
add('CA04','Different row IDs can duplicate the same deposit',{'gross_bill':1900,'same_deposit_in_two_distinct_rows':True,'legs':l},{'ledger_payment':-cash(0,l)['closing'],'excess_vs_bill':-cash(0,l)['closing']-1900},{'ledger_payment':2400.0,'excess_vs_bill':500.0},'Reconcile object and settlement identity, not only unique ledger-row IDs.','Unique IDs are checked; duplicate real-world transaction identity is not automatically checked.')
l=[leg('2026-11-04','Payment',500,'Event')]
add('CA05','Route switching must not erase an already incurred deposit',{'legs':l},{'raw_A_closing':cash(0,l,route='A')['closing'],'raw_B_closing':cash(0,l,route='B')['closing']},{'raw_A_closing':0.0,'raw_B_closing':-500.0},'For a decision after commitment, retain unavoidable paid/nonrefundable amounts in the common historical/investment basis. Distinguish that from choosing an event-free route before commitment.','Route filter is correct; counterfactual scope/state must be assigned correctly.')
l=[leg('2026-10-28','Payment',500),leg('2026-11-20','Payment',1400)]
add('CA06','Opening balance already includes the earlier deposit',{'opening':1500,'legs':l},cash(1500,l),{'closing':100.0,'daily_end_funding':0.0,'payments_first_stress':0.0},'Do not replay prior-period payments. Carry any unpaid balance and delivery obligation separately.','Supported horizon arithmetic; actual opening balance/source still required.')
l=[leg('2026-11-02','Receipt',1200)]
add('CA07','Annual receipt leaves future benefits',{'legs':l,'agreed_months':12,'satisfied_months':1},{'cash':cash(0,l)['closing'],'remaining_service_months':12-1},{'cash':1200.0,'remaining_service_months':11},'Keep 11 service months and their cost/capacity after receipt, including periods outside the cash display. Do not call gross receipt profit.','Cash and typed remaining units supported; work/calendar valuation pending.')
add('CA08','Noncash support is not spending money',{'meeting_room_support_face_value':500,'cash_received':0,'sponsor_briefings_owed':1},{'cash_receipt':0,'briefings_still_owed':1},{'cash_receipt':0,'briefings_still_owed':1},'Record the actual in-kind service and sponsor obligation. Reduce only cash/resource work genuinely displaced; determine applicable tax separately.','No dedicated in-kind linkage or avoided-cost check in cash component.')
add('CA09','Net payment settlement and fees',{'customer_gross':1000,'processor_fee':30},{'net_bank':1000-30,'gross_less_fee':1000-30},{'net_bank':970,'gross_less_fee':970},'Either reconcile gross receipt plus fee to net settlement, or use a documented net-cash basis. Do not combine a net970 receipt with the same30 fee again.','Separate legs possible; settlement reconciliation remains manual.')
add('CA10','Foreign currency amount is not GBP amount',{'usd_amount':750,'assumed_gbp_per_usd':0.8,'separate_assumed_fee_gbp':10},{'gross_gbp':float(Decimal(750)*Decimal('0.8')),'net_gbp':float(Decimal(750)*Decimal('0.8')-10)},{'gross_gbp':600.0,'net_gbp':590.0},'Illustrative factor only. Actual paid currency/rate/date and fee basis must be sourced; no change to the USD commission record.','Explicit factor supported; actual conversion/fee unknown.')
start=d('2026-11-01');expiry=d('2027-02-01');end=d('2027-11-01')
add('CA11','Credit expires inside the displayed year',{'start':str(start),'expiry':str(expiry),'horizon_end':str(end),'remaining_credit_units':500},{'opening_date_review_flag':expiry<start,'expiry_within_horizon':start<=expiry<end},{'opening_date_review_flag':False,'expiry_within_horizon':True},'The original status compares expiry with start month. Add a dated expiry/use reminder in the integrated schedule; Open is not a guarantee it remains usable throughout the year.','Opening-date status only; upcoming expiry inside horizon is not separately flagged.')
add('CA12','Expired credit is not a refund',{'credit_units':500,'cash_refund_received':0},{'cash_refund':0,'unapplied_credit_units_pending_term_review':500},{'cash_refund':0,'unapplied_credit_units_pending_term_review':500},'Retain the record and review actual terms; no automatic cash receipt, legal discharge or write-off.','Original units/status separation supported.')
add('CA13','Cash settlement does not complete the promised output',{'supplier_bill_paid':500,'promised_sessions':2,'delivered_sessions':1},{'remaining_sessions':2-1,'cash_payment':500},{'remaining_sessions':1,'cash_payment':500},'Join settlement and fulfilment through the same object while keeping their states distinct.','Typed remaining units supported; owner/capacity scheduling pending.')
add('CA14','Several rights in a single paid bundle',{'bundle_cash':1200,'licence_benefit':1,'briefing_benefit':1},{'cash_counted_once':1200,'benefit_records':2},{'cash_counted_once':1200,'benefit_records':2},'Allocate rights/work under one order if appropriate. A licence included in sponsorship is not a second sale.','Separate objects can be recorded; integrated bundle conservation needed.')
add('CA15','Illustrative correlated sponsor delay',{'two_assumed_receipts_same_payer':[600,400],'cash_delay_of_both':True},{'receipts_in_delayed_period':0,'total_shifted_to_later_period':600+400},{'receipts_in_delayed_period':0,'total_shifted_to_later_period':1000},'Test payment timing together when the same buyer/approval dependency controls both. No inferred probability or expected-conversion weighting.','Dated changes representable; scenario linkage is full-model work.')
add('CA16','Nonrenewal preserves only existing promises',{'current_paid_term_months_remaining':2,'uncontracted_future_annual_price':1200},{'remaining_current_service_months':2,'renewal_receipt':0},{'remaining_current_service_months':2,'renewal_receipt':0},'Serve the existing term without automatically creating another receipt; comparator renewal clauses are not JGA terms.','Existing obligations representable; contract-term and renewal controls pending.')
add('CA17','Retain opening cash shortfall',{'opening':-250,'legs':[]},cash(-250,[]),{'closing':-250.0,'daily_end_funding':250.0,'payments_first_stress':250.0},'A negative supported opening balance remains a funding gap, not an invented zero or financing plug.','Arithmetic supports negative opening cash.')
l=[leg('2028-02-29','Payment',100),leg('2028-03-01','Receipt',100)]
add('CA18','Leap-day month boundary',{'legs':l,'start':'2028-02-01','end':'2028-03-01'},cash(0,l,start='2028-02-01',end='2028-03-01'),{'closing':-100.0,'daily_end_funding':100.0,'payments_first_stress':100.0},'Include the final day once and exclude the next month from this displayed period.','Supported inclusive-start/exclusive-end date basis.')

# Check exported cached defaults and governing formula references without modifying XLSX.
component = load('04-table/T05-cash-map.json')
wp = Path(component['workbook_path'])
ns={'m':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
cache_count=0
with zipfile.ZipFile(wp) as z:
    def cells(i): return {x.get('r'):x for x in ET.fromstring(z.read(f'xl/worksheets/sheet{i}.xml')).findall('.//m:c',ns)}
    cs=[cells(i) for i in [1,2,3]]
    def cache(i,ref):
        node=cs[i][ref].find('m:v',ns)
        return node.text if node is not None else None
    def formula(i,ref): return cs[i][ref].find('m:f',ns).text
    for row in range(11,51):
        for col in ['K','N','O']:
            check(cache(1,f'{col}{row}')=='0',f'Unconfigured cash cache {col}{row}')
            cache_count+=1
    for row in range(11,35):
        check(cache(2,f'M{row}')=='0',f'Unconfigured remaining-unit cache M{row}')
        cache_count+=1
    for ref in ['I5','I6','I7','I9','I10','I11']:
        check(cache(0,ref)=='n.a.','Unavailable unconfigured output '+ref)
        cache_count+=1
    check("COUNTIFS($A$11:$A$50,A11)=1" in formula(1,'N11') and 'E11<>""' in formula(1,'N11'), 'Row-ID uniqueness checked, object ID merely required')
    check("H11<'Cash plan'!$B$6" in formula(2,'N11') and '$B$12' not in formula(2,'N11'), 'Obligation timing review compares start month, not evidence date')
    check('"Future-use credit"' in formula(0,'I10') and '"Review timing"' in formula(0,'I10'), 'Credit review count depends on opening-date statuses')
    check('"Event"' in formula(1,'N11') and '"A"' in formula(1,'N11'), 'Event route exclusion formula retained')
    check("$F$11:$F$50,\"<\"&F11" in formula(1,'Q11'), 'Payments-first stress excludes same-day receipts')
save(B+'/cash-applications.json', {'date':'2026-11-01','status':'passed_read_only_constructed_review','method':'Independent Decimal/date arithmetic illustrations and inspection of preserved exported formula text/cached defaults. New example inputs were not run inside the workbook engine. Original 65 artifact-engine tests remain preserved.', 'source_workbook':str(wp),'source_workbook_sha256':sha(wp),'source_component_sha256':sha(ROOT/'04-table/T05-cash-map.json'),'case_count':len(cases),'cases':cases,'formula_caches_reconciled':cache_count,'check_count':len(checks),'checks':checks,'original_workbook_edited':False,'native_Excel_tested':False,'new_workbook_engine_tests':0,'new_financial_inputs':0})
print(json.dumps({'bridge_answers':32,'semantic_rereads':4,'bridge_checks':132,'cash_applications':len(cases),'cash_checks':len(checks),'formula_caches_reconciled':cache_count}))
