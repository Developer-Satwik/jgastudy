"""Read-only, same-agent applications of saved formulas to constructed cases."""
import hashlib
import importlib.util
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True
PROJECT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('preserved_service_formula_reader', PROJECT / '08-qa/t05s-review/independent_arithmetic_review.py')
reader = importlib.util.module_from_spec(spec)
spec.loader.exec_module(reader)
book_before = hashlib.sha256(reader.BOOK.read_bytes()).hexdigest()
financial_file = PROJECT / '04-table/financial-inputs.json'
finance_before = hashlib.sha256(financial_file.read_bytes()).hexdigest()
zero = {('Inputs', f'D{i}'): 0 for i in range(19, 34)}
cases = []
checks = []

def evaluate(overrides):
    engine = reader.Evaluator(overrides)
    return {k: reader.result(engine, 'Service cost', address) for k, address in [('hours', 'H26'), ('GBP_comparison', 'I26')]}

def add(ident, name, assumptions, result, implication, overrides=None):
    cases.append({'case_id': ident, 'name': name, 'constructed_assumptions': assumptions, 'result': result, 'programme_implication': implication, 'saved_formula_overrides_in_memory_only': {f'{s}!{c}': v for (s, c), v in (overrides or {}).items()}, 'actual_activity_or_terms': False})

def test(name, actual, expected):
    passed = actual == expected if isinstance(expected, str) else isinstance(actual, (int, float)) and abs(actual - expected) < 1e-7
    checks.append({'passed': passed, 'detail': name, 'actual': actual, 'expected': expected})
    assert passed, (name, actual, expected)

o = {**zero, ('Inputs', 'D29'): 1}
r = evaluate(o)
test('One complete working briefing has five hours', r['hours'], 5)
test('One complete working briefing comparison', r['GBP_comparison'], 248)
add('SA01', 'Complete briefing unit', {'completed_sessions': 1}, r, 'Reconciles the preserved catalogue only; not a quote or observed delivery.', o)

o = {**zero, ('Inputs', 'D27'): 2, ('Inputs', 'D29'): 1}
r = evaluate(o)
test('Joint session with two administration bundles', r['hours'], 9.5)
test('Joint-session comparison', r['GBP_comparison'], 455.855)
add('SA02', 'Joint audience if eligible', {'partner_administration_units': 2, 'shared_sessions': 1, 'audience_fit_and_permissions_confirmed': False}, r, 'Joint delivery is a conditional option. This calculation establishes no permission to combine buyers.', o)

o = {**zero, ('Inputs', 'D27'): 2, ('Inputs', 'D29'): 2}
r = evaluate(o)
test('Separate sessions require more work', r['hours'], 14.5)
test('Separate-session comparison', r['GBP_comparison'], 703.855)
add('SA03', 'Separate confidential or incompatible audiences', {'partner_administration_units': 2, 'sessions': 2, 'no_reuse_credit_in_this_case': True}, r, 'One contract or common report does not prove one joint session is appropriate.', o)

o = {**zero, ('Inputs', 'D29'): 2, ('Inputs', 'H50'): 1.5}
r = evaluate(o)
test('One reusable three-hour preparation block over two sessions', r['hours'], 7)
test('Specific reused-preparation comparison', r['GBP_comparison'], 347.2)
add('SA04', 'Exact preparation reused once', {'sessions': 2, 'common_preparation_hours_once': 3, 'live_hours_each': 1, 'separate_followthrough_hours_each': 1}, r, 'A conditional three-hour credit, not an automation or general reuse percentage. Necessary new preparation remains.', o)

r = evaluate(zero)
test('Zero delivered units produce zero catalogue labour', r['hours'], 0)
add('SA05', 'Cancelled after preparation, no delivered session', {'delivered_sessions': 0, 'preparation_already_incurred_hours': 3}, {'catalogue_delivered_unit_hours': r['hours'], 'additional_noncompletion_work_hours': 3, 'additional_reference_GBP': 3 * 49.6}, 'The zero delivered-session count cannot represent this incurred work. Before programme use, add a separate exception/state allowance or a supported allocation; no cancellation fee or actual cancellation is inferred.')

o = {**zero, ('Inputs', 'D29'): 2, ('Inputs', 'H50'): 4.5}
r = evaluate(o)
test('Two completed sessions plus three hours of cancelled preparation', r['hours'], 13)
test('Mixed completed and noncompleted preparation comparison', r['GBP_comparison'], 644.8)
add('SA06', 'Mixed states with a valid allocation denominator', {'completed_sessions': 2, 'completed_preparation_hours': 6, 'cancelled_preparation_hours': 3, 'allocated_preparation_hours_per_completed_unit': 4.5}, r, 'A documented average can reconcile a particular mixed period. It cannot allocate cancellation work when no completed units exist; keep states visible.', o)

o = {**zero, ('Inputs', 'D29'): 1, ('Inputs', 'H51'): 2}
r = evaluate(o)
test('Two presenters add person-time', r['hours'], 6)
test('Two-presenter comparison using the same illustrative proxy', r['GBP_comparison'], 297.6)
add('SA07', 'One elapsed hour with two presenters', {'sessions': 1, 'presenters_for_one_live_hour': 2}, r, 'Count actual people-time. Different actual performer rates and availability remain unknown.', o)

o = {**zero, ('Inputs', 'D19'): 2, ('Inputs', 'H58'): 1}
r = evaluate(o)
test('Shared two-hour route setup allocated once across two campaigns', r['hours'], 22)
test('Unknown commercial rate remains unavailable after reuse', r['GBP_comparison'], 'n.a.')
add('SA08', 'Shared route configuration', {'campaigns': 2, 'common_route_setup_hours_once': 2, 'other_task_hours_unchanged': True}, r, 'Reuse must identify the exact configuration and remaining checks. A shared asset does not make commercial work or the unknown rate disappear.', o)

o = {**zero, ('Inputs', 'D28'): 1}
r = evaluate(o)
test('One common distribution run', r['hours'], 1)
test('One distribution-run comparison', r['GBP_comparison'], 46.19)
add('SA09', 'One eligible batch for paid and free recipients', {'paid_or_partner_recipients': 5, 'free_practitioner_recipients': 10, 'actual_eligible_delivery_runs': 1}, r, 'Fifteen recipients do not automatically mean fifteen runs. Individual handling or different rights can require more work; free access remains intact.', o)

o = {**zero, ('Inputs', 'D22'): 5}
r = evaluate(o)
test('Five unsuccessful proposals retain commercial hours', r['hours'], 15)
test('Lost-sales effort does not invent a wage', r['GBP_comparison'], 'n.a.')
add('SA10', 'No sales with real proposal work', {'initial_proposals': 5, 'won_orders': 0}, r, 'Do not erase failed commercial effort or divide by zero customers to fabricate an acquisition cost.', o)

o = {**zero, ('Inputs', 'D24'): 1}
r = evaluate(o)
test('Order setup is not future delivery', r['hours'], 1.5)
add('SA11', 'Order now, briefing owed later', {'current_order_setups': 1, 'current_delivered_briefings': 0, 'future_committed_briefing_hours_illustration': 5}, {**r, 'separate_future_obligation_hours': 5, 'future_reference_GBP': 248}, 'Use the actual fulfilment and payment periods. Ending a campaign or ceasing new sales does not discharge existing obligations.', o)

o = {**zero, ('Inputs', 'D27'): 1, ('Inputs', 'H48'): 2.25}
r = evaluate(o)
test('Three explicitly assumed benefit checks change bundle effort', r['hours'], 3.75)
test('Longer scoped administration comparison', r['GBP_comparison'], 173.2125)
add('SA12', 'Partner administration over a different scoped term', {'recognition_setup_hours': 1.5, 'separately_required_checks': 3, 'constructed_hours_each': 0.75}, r, 'The original per-bundle allowance is not a promised unlimited term. Reforecast actual included duties; do not add a new compulsory service.', o)

assert book_before == hashlib.sha256(reader.BOOK.read_bytes()).hexdigest()
assert finance_before == hashlib.sha256(financial_file.read_bytes()).hexdigest()
result = {'date': '2026-11-01', 'status': 'passed_read_only_constructed_applications', 'reviewer': 'same_agent_second_check', 'independent_agent_review': False, 'source_workbook_sha256': book_before, 'source_financial_inputs_sha256': finance_before, 'cases': cases, 'checks': checks, 'case_count': len(cases), 'check_count': len(checks), 'workbook_changed': False, 'financial_inputs_changed': False, 'native_Excel_application_tested': False, 'new_observations_or_adopted_inputs': 0, 'programme_noncompletion_state_work_still_required': True}
(PROJECT / '04-table/research-notes/t05s-second-check/cost-applications.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({'cases': len(cases), 'checks': len(checks), 'workbook_unchanged': True, 'financial_inputs_unchanged': True}))
