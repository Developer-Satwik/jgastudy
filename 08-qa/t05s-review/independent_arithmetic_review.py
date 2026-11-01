"""Independent audit of the delivered T05S OpenXML formulas and lineage.

Uses a small evaluator for the formula subset actually present. It does not use
the author's calculation code, mutate the workbook, or claim native Excel QA.
"""
from pathlib import Path
from collections import Counter
import hashlib
import json
import math
from openpyxl import load_workbook
from openpyxl.formula.tokenizer import Tokenizer

PROJECT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
MAP = json.loads((PROJECT / '04-table/T05-service-cost-map.json').read_text())
CELLS = json.loads((PROJECT / '08-qa/t05s-workbook/cell-map.json').read_text())
FIN = json.loads((PROJECT / '04-table/financial-inputs.json').read_text())
RATES = {x['input_id']: x for x in FIN['records']}
BOOK = Path(MAP['workbook_absolute_path'])
FORMULAS = load_workbook(BOOK, data_only=False)
CACHED = load_workbook(BOOK, data_only=True)
NA = 'n.a.'


class ExcelError(Exception):
    pass


def number(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def flat(values):
    for v in values:
        if isinstance(v, list):
            yield from flat(v)
        else:
            yield v


class Parser:
    def __init__(self, formula):
        self.tokens = [x for x in Tokenizer(formula).items if x.type != 'WHITE-SPACE']
        self.i = 0

    def parse(self, precedence=0):
        t = self.tokens[self.i]
        self.i += 1
        if t.type == 'FUNC' and t.subtype == 'OPEN':
            args = []
            while self.tokens[self.i].subtype != 'CLOSE':
                args.append(self.parse())
                if self.tokens[self.i].type == 'SEP':
                    self.i += 1
            self.i += 1
            left = ('call', t.value[:-1], args)
        elif t.type == 'OPERAND':
            if t.subtype == 'NUMBER':
                left = ('literal', float(t.value))
            elif t.subtype == 'TEXT':
                left = ('literal', t.value[1:-1].replace('""', '"'))
            elif t.subtype == 'RANGE':
                left = ('reference', t.value)
            else:
                raise ValueError((t.type, t.subtype, t.value))
        else:
            raise ValueError((t.type, t.subtype, t.value))
        prec = {'=': 1, '>=': 1, '<=': 1, '>': 1, '<': 1, '<>': 1,
                '+': 2, '-': 2, '*': 3, '/': 3}
        while self.i < len(self.tokens):
            op = self.tokens[self.i]
            if op.type != 'OPERATOR-INFIX' or prec[op.value] <= precedence:
                break
            self.i += 1
            left = ('binary', op.value, left, self.parse(prec[op.value]))
        return left


class Evaluator:
    def __init__(self, overrides=None):
        self.overrides = overrides or {}
        self.cache = {}

    def cell(self, sheet, address):
        address = address.replace('$', '')
        key = (sheet, address)
        if key in self.overrides:
            return self.overrides[key]
        if key in self.cache:
            return self.cache[key]
        v = FORMULAS[sheet][address].value
        if isinstance(v, str) and v.startswith('='):
            v = self.eval(Parser(v).parse(), sheet)
        self.cache[key] = v
        return v

    def eval(self, ast, sheet):
        kind = ast[0]
        if kind == 'literal':
            return ast[1]
        if kind == 'reference':
            ref = ast[1].replace('$', '')
            if '!' in ref:
                other, ref = ref.split('!', 1)
                other = other.strip("'")
            else:
                other = sheet
            if ':' in ref:
                return [self.cell(other, c.coordinate) for row in FORMULAS[other][ref] for c in row]
            return self.cell(other, ref)
        if kind == 'binary':
            a, b = self.eval(ast[2], sheet), self.eval(ast[3], sheet)
            op = ast[1]
            if op in ['+', '-', '*', '/']:
                a = 0 if a is None else a
                b = 0 if b is None else b
                if not number(a) or not number(b):
                    raise ExcelError('#VALUE!')
                if op == '/':
                    if b == 0:
                        raise ExcelError('#DIV/0!')
                    return a / b
                return {'+': lambda: a+b, '-': lambda: a-b, '*': lambda: a*b}[op]()
            a = 0 if a is None else a
            b = 0 if b is None else b
            if op == '=':
                return a == b
            if op == '<>':
                return a != b
            # Excel compares a text operand after all numeric operands.
            if type(a) != type(b) and isinstance(a, str) != isinstance(b, str):
                a, b = (1 if isinstance(a, str) else 0), (1 if isinstance(b, str) else 0)
            return {'>=': lambda: a >= b, '<=': lambda: a <= b,
                    '>': lambda: a > b, '<': lambda: a < b}[op]()
        name, args = ast[1], ast[2]
        if name == 'IF':
            return self.eval(args[1] if self.eval(args[0], sheet) else args[2], sheet)
        if name == 'CHOOSE':
            idx = self.eval(args[0], sheet)
            if not number(idx) or int(idx) < 1 or int(idx) >= len(args):
                raise ExcelError('#VALUE!')
            return self.eval(args[int(idx)], sheet)
        vals = [self.eval(x, sheet) for x in args]
        if name == 'ISNUMBER':
            return number(vals[0])
        if name == 'AND':
            return all(vals)
        if name == 'INT':
            v = 0 if vals[0] is None else vals[0]
            if isinstance(v, str):
                try:
                    v = float(v)
                except ValueError:
                    raise ExcelError('#VALUE!')
            return math.floor(v)
        if name == 'COUNT':
            return sum(number(x) for x in flat(vals))
        if name == 'COUNTBLANK':
            return sum(x is None or x == '' for x in flat(vals))
        if name == 'SUM':
            return sum(x for x in flat(vals) if number(x))
        raise ValueError(name)


CHECKS = []


def same(a, b):
    return math.isclose(a, b, rel_tol=1e-10, abs_tol=1e-9) if number(a) and number(b) else a == b


def check(name, passed, detail=None):
    CHECKS.append({'check_id': name, 'passed': bool(passed), 'detail': detail})


def result(ev, sheet, address):
    try:
        return ev.cell(sheet, address)
    except ExcelError as e:
        return str(e)


def oracle(case, unit):
    tasks = [t for t in MAP['tasks'] if t['unit_key'] == unit['unit_key']]
    h = sum(RATES[t['hours_input_id']]['value'][case] for t in tasks)
    ref = 0
    commercial_hours = 0
    for t in tasks:
        hours = RATES[t['hours_input_id']]['value'][case]
        if t['comparison_role'] == 'Commercial':
            commercial_hours += hours
        else:
            rate = RATES[t['rate_input_id']]['value']
            if RATES[t['rate_input_id']]['unit'] == 'day':
                rate /= RATES[MAP['day_normalisation_input_id']]['value']
            ref += hours * rate
    return [h, ref, NA if commercial_hours else 0, NA if commercial_hours else ref]


def run():
    case_results = []
    for i, case in enumerate(['low', 'working', 'high'], 1):
        ev = Evaluator({('Inputs', 'D4'): i})
        for unit in MAP['units']:
            row = CELLS['unit_output_rows'][unit['unit_key']]
            actual = [result(ev, 'Service cost', f'{c}{row}') for c in 'CDEF']
            expected = oracle(case, unit)
            passed = all(same(a, b) for a, b in zip(actual, expected))
            case_results.append({'case': case, 'unit_key': unit['unit_key'],
                                 'actual_hours_reference_commercial_combined': actual,
                                 'independent_expected': expected, 'passed': passed})
    check('45-per-unit-case-formula-results', len(case_results) == 45 and all(x['passed'] for x in case_results), case_results)

    ev = Evaluator()
    cached_mismatches = []
    formula_count = 0
    for sheet in FORMULAS:
        for row in sheet:
            for cell in row:
                if cell.data_type == 'f':
                    formula_count += 1
                    evaluated = result(ev, sheet.title, cell.coordinate)
                    saved = CACHED[sheet.title][cell.coordinate].value
                    if not same(evaluated, saved):
                        cached_mismatches.append({'cell': f'{sheet.title}!{cell.coordinate}', 'evaluated': evaluated, 'cached': saved})
    check('saved-working-formula-caches-match', not cached_mismatches, {'formula_count': formula_count, 'mismatches': cached_mismatches})

    base_zero = {('Inputs', f'D{i}'): 0 for i in range(19, 34)}
    scenarios = [
        ('blank-quantities-not-zero', {}, 'I26', NA),
        ('all-zero-activity-cost', base_zero, 'I26', 0),
        ('all-zero-activity-hours', base_zero, 'H26', 0),
        ('two-briefing-sessions', {**base_zero, ('Inputs', 'D29'): 2}, 'I26', 496),
        ('proposal-loss-retains-hours', {**base_zero, ('Inputs', 'D22'): 2}, 'H26', 6),
        ('proposal-loss-unpriced-cost', {**base_zero, ('Inputs', 'D22'): 2}, 'I26', NA),
        ('proposal-commercial-entered', {**base_zero, ('Inputs', 'D22'): 2, ('Inputs', 'E14'): 40}, 'I26', 240),
        ('explicit-zero-commercial-rate', {**base_zero, ('Inputs', 'D22'): 2, ('Inputs', 'E14'): 0}, 'I26', 0),
        ('one-unknown-quantity-blocks-total', {**base_zero, ('Inputs', 'D19'): None}, 'I26', NA),
        ('negative-activity-invalid', {**base_zero, ('Inputs', 'D29'): -1}, 'I26', NA),
        ('fractional-activity-invalid', {**base_zero, ('Inputs', 'D29'): .5}, 'I26', NA),
        ('text-activity-invalid', {**base_zero, ('Inputs', 'D29'): 'unknown'}, 'I26', NA),
        ('missing-selected-effort-blocks-unit', {('Inputs', 'H50'): None}, 'F20', NA),
        ('missing-unselected-effort-does-not-block', {('Inputs', 'G50'): None}, 'F20', 248),
        ('zero-shared-preparation-credit', {('Inputs', 'H50'): 0}, 'F20', 99.2),
        ('admin-independent-of-invalid-day-divisor', {('Inputs', 'F8'): 0}, 'F19', 46.19),
        ('specialist-blocked-by-invalid-day-divisor', {('Inputs', 'F8'): 0}, 'F20', NA),
        ('joint-session-two-partners-once', {**base_zero, ('Inputs', 'D27'): 2, ('Inputs', 'D29'): 1}, 'I26', 455.855),
        ('distinct-second-session-adds-delivery', {**base_zero, ('Inputs', 'D27'): 2, ('Inputs', 'D29'): 2}, 'I26', 703.855),
        ('out-of-range-selector-invalid', {('Inputs', 'D4'): 4}, 'F20', NA),
        ('pasted-text-selector-invalid', {('Inputs', 'D4'): 'invalid'}, 'F20', NA),
    ]
    for name, overrides, address, expected in scenarios:
        actual = result(Evaluator(overrides), 'Service cost', address)
        check(name, same(actual, expected), {'actual': actual, 'expected': expected, 'input_overrides': {f'{s}!{a}': v for (s, a), v in overrides.items()}})

    check('two-tabs-exact', FORMULAS.sheetnames == ['Service cost', 'Inputs'], FORMULAS.sheetnames)
    check('fifteen-saved-quantities-blank', all(FORMULAS['Inputs'][f'D{i}'].value is None for i in range(19, 34)))
    check('commercial-rate-saved-blank', FORMULAS['Inputs']['E14'].value is None)
    check('working-selector-and-divisor', FORMULAS['Inputs']['D4'].value == 2 and FORMULAS['Inputs']['F8'].value == 7.5)
    check('restored-rate-inputs', FORMULAS['Inputs']['E12'].value == 372 and FORMULAS['Inputs']['E13'].value == 46.19)
    check('partner-label-is-administration', FORMULAS['Service cost']['B18'].value == 'Partner administration')
    check('seven-role-tasks-each', Counter(x['comparison_role'] for x in MAP['tasks']) == {'Commercial': 7, 'Specialist': 7, 'Coordination': 7})
    check('unit-task-partition', sorted(t for u in MAP['units'] for t in u['task_ids']) == sorted(t['workload_id'] for t in MAP['tasks']))

    for t in MAP['tasks']:
        ir, br = CELLS['task_input_rows'][t['workload_id']], CELLS['task_build_rows'][t['workload_id']]
        expected = RATES[t['hours_input_id']]['value']
        good = all(FORMULAS['Inputs'][f'{col}{ir}'].value == expected[case] for col, case in zip('GHI', ['low', 'working', 'high']))
        good &= FORMULAS['Service cost'][f'E{br}'].value == f"='Inputs'!F{ir}"
        role_row = CELLS['rate_rows'][t['comparison_role']]
        good &= FORMULAS['Service cost'][f'F{br}'].value == f"='Inputs'!F{role_row}"
        check(f"task-lineage-{t['workload_id']}", good)

    baseline = json.loads((PROJECT / '08-qa/T05S-baseline-manifest.json').read_text())
    snapshots = json.loads((PROJECT / baseline['mutable_paths_snapshotted_in']).read_text())
    for label, records, key in [('baseline', baseline['files'], 'path'), ('snapshot', snapshots['records'], 'snapshot_path')]:
        failures = []
        for x in records:
            path = Path(x[key])
            path = path if path.is_absolute() else PROJECT / path
            if not path.exists() or hashlib.sha256(path.read_bytes()).hexdigest() != x['sha256']:
                failures.append(x[key])
        check(f'{label}-hashes-preserved', not failures, {'count': len(records), 'failures': failures})

    snapshot_dir = PROJECT / '04-table/research-notes/t05-service-costs/before-review'
    for path, expected_count in [('04-table/financial-inputs.json', 33), ('02-evidence/registers/sources.json', 242), ('02-evidence/registers/claims.json', 484), ('05-analysis/findings.json', 81)]:
        before = json.loads((snapshot_dir / path).read_text())['records']
        after = json.loads((PROJECT / path).read_text())['records']
        if Path(path).stem == 'sources':
            # Three reused sources append a new review and topic without
            # changing the original route, capture, facts, or prior reviews.
            changes = []
            good = len(before) == expected_count
            for old, new in zip(before, after):
                for key in set(old) | set(new):
                    if old.get(key) == new.get(key):
                        continue
                    allowed = key in ['related_topic_ids', 'additional_reviews'] and isinstance(old.get(key), list) and new[key][:len(old[key])] == old[key]
                    changes.append({'source_id': old['source_id'], 'field': key, 'append_only_metadata': allowed})
                    good &= allowed
            check('old-source-substance-and-prefix-order-preserved', good,
                  {'old_count': len(before), 'new_count': len(after), 'metadata_appends': changes})
        else:
            check(f'preserved-prefix-{Path(path).stem}', len(before) == expected_count and after[:len(before)] == before,
                  {'old_count': len(before), 'new_count': len(after)})
    sources = json.loads((PROJECT / '02-evidence/registers/sources.json').read_text())['records']
    claims = json.loads((PROJECT / '02-evidence/registers/claims.json').read_text())['records']
    check('five-new-primary-routes', len(sources) == 247 and [x['source_id'] for x in sources[-5:]] == [f'SRC-0{i}' for i in range(275, 280)])
    check('eleven-new-bounded-claims', len(claims) == 495 and [x['claim_id'] for x in claims[-11:]] == [f'CLM-0{i}' for i in range(575, 586)] and all(x.get('interpretation_limits') for x in claims[-11:]))
    capture_checks = []
    for source in sources[-5:]:
        for path, digest in [(source['capture_path'], source['capture_sha256'])] + [(x['path'], x['sha256']) for x in source['review_extracts']]:
            actual = hashlib.sha256((PROJECT / path).read_bytes()).hexdigest()
            capture_checks.append({'path': path, 'sha256': actual, 'passed': actual == digest})
    check('five-html-five-parsed-capture-hashes', len(capture_checks) == 10 and all(x['passed'] for x in capture_checks), capture_checks)
    check('exact-new-financial-records', len(FIN['records']) == 70 and [x['input_id'] for x in FIN['records'][33:]] == [f'FI-S{i:02}' for i in range(1, 38)])
    check('no-new-actual-cost-or-budget', all(not x['actual_cost'] and not x['actual_supplier_quote'] and not x['budget_authorised'] for x in FIN['records'][33:]))
    check('new-quantity-values-null', all(RATES[u['quantity_input_id']]['value'] is None and u['quantity'] is None for u in MAP['units']))
    check('unknown-commercial-record-null', RATES['FI-S01']['value'] is None)
    check('delivered-workbook-hash', hashlib.sha256(BOOK.read_bytes()).hexdigest() == MAP['workbook_sha256'])

    # The selector explicitly rejects pasted text before INT is evaluated.
    invalid_text = result(Evaluator({('Inputs', 'D4'): 'invalid'}), 'Service cost', 'F20')
    out = {'date': '2026-11-01', 'status': 'passed' if all(x['passed'] for x in CHECKS) else 'failed',
           'method': 'Independent Python evaluation of the actual saved OpenXML formula subset, direct register-based arithmetic oracle, cached-output comparison and in-memory input overrides. No workbook file mutation; no native Excel execution claim.',
           'checks': CHECKS, 'check_count': len(CHECKS), 'passed_count': sum(x['passed'] for x in CHECKS),
           'diagnostics': [{'case': 'Pasted nonnumeric selector outside validated input domain', 'result': invalid_text}]}
    (OUT / 'independent-arithmetic-checks.json').write_text(json.dumps(out, indent=2) + '\n')
    print(json.dumps({k: out[k] for k in ['status', 'check_count', 'passed_count', 'diagnostics']}))
    for x in CHECKS:
        if not x['passed']:
            print(json.dumps(x))


if __name__ == '__main__':
    run()
