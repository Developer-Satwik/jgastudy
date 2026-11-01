"""Read-only challenge of the preserved event workbook and its unit boundaries."""
from pathlib import Path
import sys,importlib.util,json,hashlib,math
sys.dont_write_bytecode=True
from openpyxl import load_workbook
ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('preserved_formula_parser',ROOT/'08-qa/t05s-review/independent_arithmetic_review.py')
audit=importlib.util.module_from_spec(spec);spec.loader.exec_module(audit)
BOOK=Path(json.loads((ROOT/'04-table/T05-event-cost-map.json').read_text())['workbook_path'])
audit.FORMULAS=load_workbook(BOOK,data_only=False)
cached=load_workbook(BOOK,data_only=True)
class Eval(audit.Evaluator):
    def eval(self,ast,sheet):
        if ast[0]=='binary'and ast[1]in ['=','<>']:
            a,b=self.eval(ast[2],sheet),self.eval(ast[3],sheet)
            if (a is None and b=='')or(b is None and a==''):
                return ast[1]=='='
        if ast[0]=='call'and ast[1]in ['OR','MIN']:
            vals=[self.eval(x,sheet)for x in ast[2]]
            if ast[1]=='OR':return any(audit.flat(vals))
            return min(x for x in audit.flat(vals)if audit.number(x))
        return super().eval(ast,sheet)
checks=[];cases=[]
def check(label,a,b):
    ok=math.isclose(a,b,abs_tol=1e-9)if audit.number(a)and audit.number(b)else a==b
    if not ok:raise AssertionError((label,a,b))
    checks.append({'check':label,'actual':a,'expected':b,'passed':True})
def state(overrides=None):
    d={('Event work',f'H{r}'):0 for r in range(11,33)}
    d.update({('Event costs',f'B{r}'):'No'for r in range(31,43)})
    d.update(overrides or {});return Eval(d)
def cell(e,s,a):return e.cell(s,a)
def add(ident,title,result,note,implemented=True):
    cases.append({'case_id':ident,'title':title,'result':result,'interpretation':note,'covered_by_current_workbook':implemented,'actual_observation':False,'new_financial_input':False})

# Reconcile every original saved formula cache in this small workbook.
original=Eval();formulas=0
for s in audit.FORMULAS:
    for row in s:
        for c in row:
            if c.data_type=='f':
                check('Saved formula '+s.title+'!'+c.coordinate,original.cell(s.title,c.coordinate),cached[s.title][c.coordinate].value);formulas+=1

e=state({('Event work','H11'):1});v=cell(e,'Event work','I6');check('Planned complete remit unit',v,3)
add('EA01','Planned complete task',{'planning_hours':v},'A complete unit uses the selected untimed allowance; it is not observed actual work.')
e=state({('Event work','H11'):.5});v=cell(e,'Event work','I6');check('Fractional event unit rejected',v,'n.a.')
add('EA02','Partial preparation',{'fractional_count_result':v,'hypothetical_actual_hours':1.5},'Whole event/activity counts cannot measure a half-completed task. Record identifiable actual/incurred person-hours and remaining work at integration.',False)
e=state({('Event work','H32'):1.5});v=cell(e,'Event work','I6');check('Explicit uncovered actual hours retained',v,1.5)
add('EA03','Zero completed events with work incurred',{'explicit_exception_hours':v,'completed_events':0},'The exception row can retain uncovered incurred work, once; it does not identify phase, person or remaining obligations automatically.')
e=state({('Event work','H21'):2});v=cell(e,'Event work','I6');check('One live body-time counted once',v,2)
add('EA04','Two simultaneous functions',{'one_person_elapsed_hours':v,'functions_verified_as_deliverable':False},'A single person may be needed in two places at once. Body-time arithmetic does not validate simultaneous moderator/check-in coverage.',False)
e=state({('Event work','H21'):2,('Event work','H24'):2});v=cell(e,'Event work','I6');check('Distinct live roles can cost four hours',v,4)
add('EA05','Separate people or duplicate labels',{'two_role_rows_hours':v},'Four hours are valid if two different required people work two hours. If one person has two simultaneous labels, identity/time mapping must prevent duplicate hours.',False)
e=state({('Event work','H11'):2});v=cell(e,'Event work','I6');check('Two complete task units total six',v,6)
add('EA06','Postponement and exact reused work',{'two_full_units_hours':v,'illustrative_preparation_plus_update':3+.75},'A rescheduled date is not automatically a second complete task. Scope real retained work and required update rather than apply an arbitrary reuse discount.',False)
e=state({('Event costs','B15'):15,('Event costs','B16'):2,('Event costs','B17'):0,('Event costs','B19'):16,('Event costs','B20'):16});check('Seventeen distinct people',cell(e,'Event costs','B7'),17);check('Room ceiling fails',cell(e,'Event costs','B22'),'Over limit')
add('EA07','Total party capacity',{'people':17,'room_fit':cell(e,'Event costs','B22')},'Host and guest places matter in addition to practitioner places.')
e=state({('Event costs','B15'):8,('Event costs','B16'):0,('Event costs','B17'):0,('Event costs','B19'):16,('Event costs','B20'):16});check('Ceiling check alone can pass eight',cell(e,'Event costs','B23'),'Within limit')
add('EA08','Minimum party size and whole-party menu',{'ceiling_only_result':cell(e,'Event costs','B23'),'party_menu_minimum_in_dated_example':9,'selected_party':8,'dated_party_menu_eligibility':False},'The source-specific lower party threshold is separate from maximum seats. A capacity pass is not a complete menu or venue eligibility decision.',False)
e=state({('Event costs','B15'):13,('Event costs','B16'):2,('Event costs','B17'):0,('Event costs','B18'):17});check('Attendance fifteen',cell(e,'Event costs','B7'),15);check('Billed covers seventeen',cell(e,'Event costs','B18'),17)
add('EA09','Late withdrawals',{'planned_people':15,'billed_covers':17},'Attendance and supplier liability remain separate. Actual terms determine any reduction or substitution.')
e=state({('Event work','H15'):10});v=cell(e,'Event work','I6');check('Ten actual invitation attempts',v,2.5)
add('EA10','New and repeat cohorts',{'ten_attempts_hours':v,'accepted_people':None},'An existing cohort does not guarantee new attendance or eliminate changed-scope/permissions work. No conversion or no-show estimate follows.')
e=state({('Event work','H21'):2,('Event costs','B32'):'Yes',('Event costs','C32'):500,('Event costs','E32'):'Hypothetical inclusive package, not quote'});check('Inclusive package direct total',cell(e,'Event costs','B9'),500)
add('EA11','Inclusive moderation package',{'direct_cost':500,'live_hours':cell(e,'Event work','I6'),'additional_monetised_same_scope':None},'A constructed £500 package is not a price recommendation. Later full-resource integration needs package/task overlap and the correct economic/cash basis, not automatic addition of hourly fees.',False)
add('EA12','Future-use credit versus cash refund',{'hypothetical_credit_value':500,'cash_refund_established':False,'current_cash_receipt':0},'A restricted future-use credit is not cash received, unrestricted recovery or proof the original expense vanished. Exact terms/expiry/remaining service belong in the later schedule.',False)
check('Credit not treated as cash',cases[-1]['result']['current_cash_receipt'],0)
add('EA13','Deposit and remaining bill',{'hypothetical_final_total':1900,'credited_deposit':500,'remaining_payment':1400,'expense_not_2400':1900},'Credit a deposit once against its supplier bill. Actual selected terms still needed.',False)
check('Deposit credited once',1900-500,1400)
e=state({('Event costs','B39'):'Yes',('Event costs','C39'):0,('Event costs','E39'):'Hypothetical suitable free-ticket route',('Event work','H18'):1});check('Free selected tool amount',cell(e,'Event costs','B9'),0);check('Organising case still consumes work',cell(e,'Event work','I6'),.5)
add('EA14','Free software with organising effort',{'direct_software_cost':0,'additional_case_hours':.5},'A zero platform fee does not imply zero human work. Suitability and actual data arrangements remain separate.')
e=state({('Event costs','B33'):'Yes'});check('Unknown selected travel price visible',cell(e,'Event costs','B9'),'n.a.')
add('EA15','Missing travel and unselected location',{'selected_unknown_travel_result':cell(e,'Event costs','B9'),'Texas_city':None},'Do not use an invented origin, route, generic fare or FX. An unselected event should not block a separately valid research-only programme.',False)
e=state({('Event costs','B41'):'Yes',('Event costs','C41'):-100,('Event costs','E41'):'Hypothetical refund'});check('Negative expense entry rejected',cell(e,'Event costs','B9'),'n.a.')
add('EA16','Refund versus direct cost row',{'negative_expense_result':cell(e,'Event costs','B9')},'The direct-cost template is not a refund/cash ledger. Record any real refund and its date in the appropriate cash and supplier reconciliation schedule.',False)

out={'date':'2026-11-01','status':'passed_read_only_boundary_review','source_workbook':str(BOOK),'source_workbook_sha256':hashlib.sha256(BOOK.read_bytes()).hexdigest(),'source_component_sha256':hashlib.sha256((ROOT/'04-table/T05-event-cost-map.json').read_bytes()).hexdigest(),'source_financial_inputs_sha256':hashlib.sha256((ROOT/'04-table/financial-inputs.json').read_bytes()).hexdigest(),'formula_caches_reconciled':formulas,'case_count':len(cases),'cases':cases,'check_count':len(checks),'checks':checks,'workbook_changed':False,'new_financial_inputs':0,'native_Excel_tested':False,'independent_agent_review':False,'arithmetic_error_identified_for_defined_units':False,'programme_scope_state_and_feasibility_refinements_required':True}
p=ROOT/'04-table/research-notes/t05e-second-check/cost-applications.json';p.write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'status':out['status'],'cases':len(cases),'checks':len(checks),'formula_caches':formulas}))
