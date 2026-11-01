"""Read-only validation of preserved records and the artifact-authored XLSX export."""
from pathlib import Path
import hashlib
import json
import re
import zipfile
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
checks = []

def read(path):
    return json.loads((ROOT / path).read_text())

def resolve(path):
    p = Path(path)
    return p if p.is_absolute() else ROOT / p

def digest(path):
    return hashlib.sha256(resolve(path).read_bytes()).hexdigest()

def require(ok, message):
    checks.append({'check': message, 'passed': bool(ok)})
    if not ok:
        raise ValueError(message)

baseline = read('08-qa/T05C-baseline-manifest.json')['files']
before = read('04-table/research-notes/t05-cash/before-review/manifest.json')['records']
before_by = {x['original_path']: x for x in before}
require(len(baseline) == 1948, 'Exact 1948-file protected baseline')
for x in baseline:
    require(digest(x['path']) == x['sha256'], 'Protected original: ' + x['path'])
require(len(before) == 12, 'Twelve mutable-file before snapshots')
for x in before:
    require(digest(x['snapshot_path']) == x['sha256'], 'Exact snapshot: ' + x['original_path'])

sources = read('02-evidence/registers/sources.json')['records']
claims = read('02-evidence/registers/claims.json')['records']
mapping = read('08-qa/T05C-record-map.json')
require(len(sources) == 266 and len(claims) == 545, 'Current canonical record totals')
require(sources[:263] == read(before_by['02-evidence/registers/sources.json']['snapshot_path'])['records'], '263 prior source records preserved exactly')
require(claims[:537] == read(before_by['02-evidence/registers/claims.json']['snapshot_path'])['records'], '537 prior claims preserved exactly')
for path, count in [('04-table/financial-inputs.json', 70), ('05-analysis/findings.json', 81)]:
    require(read(path) == read(before_by[path]['snapshot_path']) and len(read(path)['records']) == count, 'Unchanged register: ' + path)
for path, added in [('00-control/changes.json', 'CHG-032'), ('00-control/decisions.json', 'DEC-014'), ('02-evidence/registers/searches.json', 'SCH-0031')]:
    old = read(before_by[path]['snapshot_path'])['records']
    now = read(path)['records']
    require(now[:-1] == old and added in now[-1].values(), 'Append-only history: ' + path)
require(len(mapping['source_map']) == 3 and len(mapping['claim_map']) == 8 and mapping['new_financial_inputs'] == 0, 'Only three source routes and eight claims added')
source_by = {x['source_id']: x for x in sources}
claim_by = {x['claim_id']: x for x in claims}
for candidate, source_id in mapping['source_map'].items():
    require(source_by[source_id]['t05c_source_candidate_id'] == candidate, 'Source route: ' + candidate)
for candidate, claim_id in mapping['claim_map'].items():
    x = claim_by[claim_id]
    require(x['t05c_claim_candidate_id'] == candidate and all(s in source_by for s in x['source_ids']), 'Claim lineage: ' + candidate)
require(sum(bool(x.get('capture_path')) for x in sources) == 187, '187 source records have retained primary originals')
require(source_by['SRC-0296']['capture_path'] is None and source_by['SRC-0296']['candidate_detail']['capture_kind'] == 'browser_reader_paraphrase_not_original', 'Reader paraphrase not misclassified as original')
captures = read('08-qa/T05C-captures.json')
require(len(captures['records']) == 5 and captures['counts_by_kind'] == {'browser_reader_paraphrase_not_original': 1, 'retained_original_html': 2, 'parsed_original_text': 2}, 'Five capture artefacts retain their distinct provenance')
for x in captures['records']:
    require(digest(x['path']) == x['sha256'], 'Capture hash: ' + x['path'])
prior = read('08-qa/T05E-second-check-completion.json')
require(len(prior['artifacts']) == 69 and prior['canonical_sources'] == 263 and prior['canonical_claims'] == 537, 'Prior event-second checkpoint preserved')
for x in prior['artifacts']:
    path = before_by.get(x['path'], {}).get('snapshot_path', x['path'])
    require(digest(path) == x['sha256'], 'Prior completion as of cash start: ' + x['path'])

c = read('04-table/T05-cash-map.json')
require(c['cash_legs'] == c['obligations'] == c['foreign_fx_inputs'] == [], 'No invented selected cash, obligation or FX inputs')
require(c['start_month'] is None and c['opening_cash_gbp'] is None and c['cash_coverage_confirmed'] is None and c['obligation_coverage_confirmed'] is None, 'Unconfigured cash scope explicitly retained')
require((c['cash_leg_capacity'], c['obligation_capacity'], c['monthly_capacity']) == (40, 24, 12) and c['row_capacities_are_not_activity_forecasts'], 'Storage capacities distinguished from activity forecast')
fee = c['current_commission_context']
require((fee['total_fee'], fee['report_allocation'], fee['table_allocation'], fee['upfront'], fee['balance']) == (1500, 1000, 500, 750, 750), 'Commission context matches agreed amounts')
require(fee['currency'] == 'USD' and fee['balance_trigger'] == 'Satisfactory completion and written acceptance under the agreement' and not fee['payment_system_independently_checked'], 'Conditional USD balance and reported-payment provenance retained')
for x in c['private_context_provenance']:
    require(digest(x['path']) == x['sha256'] and not x['independently_verified_executed_contract_or_bank_record'], 'Private context provenance: ' + x['role'])
require(c['commission_is_not_sponsorship_income'] and c['conditional_balance_not_scheduled_automatically'] and not c['actual_bank_reconciliation'], 'Commission not automatically converted into programme cash')
require(not c['shared_financial_register_extended'] and not c['prior_three_workbooks_changed'] and not c['current_contract_fee_changed'] and c['fourteen_core_questions_unchanged'] and c['practitioner_free_full_research_preserved'], 'Prior books, scope and practitioner benefit preserved')
require(c['external_actions'] == [] and not c['fieldwork_activated'] and not c['full_financial_model_complete'], 'No external action, fieldwork or premature full-model claim')
qa = read(c['workbook_qa_path'])
require(qa['status'] == 'passed_artifact_engine' and qa['check_count'] == len(qa['tests']) == 65 and all(x['passed'] for x in qa['tests']), '65 input-driven artifact-engine calculation tests passed')
require(qa['defaults_restored'] and not qa['native_Excel_tested'] and qa['actual_cash_legs'] == qa['actual_obligation_records'] == 0, 'Test inputs removed; no native Excel verification claimed')

ns = {'m': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
with zipfile.ZipFile(c['workbook_path']) as z:
    require(z.testzip() is None, 'Exported XLSX ZIP integrity')
    book = ET.fromstring(z.read('xl/workbook.xml'))
    names = [x.get('name') for x in book.findall('m:sheets/m:sheet', ns)]
    require(names == ['Cash plan', 'Cash legs', 'Obligations'], 'Exactly three intended exported sheets')
    require(not any('externalLink' in n for n in z.namelist()), 'No external workbook link parts')
    for name in z.namelist():
        if name.endswith('.rels'):
            rels = ET.fromstring(z.read(name))
            require(all(x.get('TargetMode') != 'External' for x in rels), 'No external package relationship: ' + name)
    shared = []
    if 'xl/sharedStrings.xml' in z.namelist():
        shared = [''.join(i.itertext()) for i in ET.fromstring(z.read('xl/sharedStrings.xml')).findall('m:si', ns)]
    trees = [ET.fromstring(z.read(f'xl/worksheets/sheet{i}.xml')) for i in range(1, 4)]
    cells = [{x.get('r'): x for x in t.findall('.//m:c', ns)} for t in trees]
    def val(sheet, ref):
        node = cells[sheet].get(ref)
        if node is None:
            return None
        v = node.find('m:v', ns)
        if v is not None:
            return shared[int(v.text)] if node.get('t') == 's' else v.text
        inline = node.find('m:is', ns)
        return ''.join(inline.itertext()) if inline is not None else None
    def formula(sheet, ref):
        node = cells[sheet].get(ref)
        f = node.find('m:f', ns) if node is not None else None
        return f.text if f is not None else None
    for i, t in enumerate(trees):
        require(not any(x.get('t') == 'e' for x in cells[i].values()), 'No exported error cells: ' + names[i])
        require(all('Audit!' not in (x.text or '') and '[' not in (x.text or '') for x in t.findall('.//m:f', ns)), 'No audit or external-file formula dependencies: ' + names[i])
    for ref in ['B6', 'B8', 'B9', 'B11']:
        require(val(0, ref) in (None, ''), 'Blank configuration: ' + ref)
    require(val(0, 'B5') == 'A' and val(0, 'B7') == '12' and val(0, 'B12') == '46327', 'Default route, capacity and evidence date exported')
    require(val(0, 'B10') == 'Needs input', 'Unconfigured plan not labelled ready')
    for ref in ['I5', 'I6', 'I7', 'I9', 'I10', 'I11']:
        require(val(0, ref) == 'n.a.', 'Unavailable default output: ' + ref)
    for ref, amount in [('B40', '1500'), ('B41', '750'), ('B42', '750'), ('B44', '1000'), ('B45', '500')]:
        require(val(0, ref) == amount, 'Separate commission cached amount: ' + ref)
    require(formula(0, 'B42') == 'B40-B41', 'Conditional balance formula preserved')
    entry_formulas = [x.text or '' for i in [1, 2] for x in trees[i].findall('.//m:f', ns)]
    plan_formulas = [formula(0, r) or '' for r in ['B10', 'I5', 'I6', 'I7', 'I8', 'I9', 'I10', 'I11']]
    require(all(not re.search(r"'Cash plan'!\$?B\$?4[0-5](?!\d)", f) for f in entry_formulas) and all(not re.search(r'(?<![A-Z])\$?B\$?4[0-5](?!\d)', f) for f in plan_formulas), 'Commission context does not feed cash or obligation calculations')
    for row in range(11, 51):
        require(val(1, f'A{row}') == f'L{row-10:02}' and val(1, f'B{row}') == 'No', f'Cash row {row} unused and identified')
        require(all(val(1, f'{col}{row}') in (None, '') for col in ['C','D','E','F','G','H','I','J','L','M']), f'Cash row {row} has no retained scenario inputs')
        require(all(formula(1, f'{col}{row}') for col in ['K','N','O','P','Q']), f'Cash row {row} calculated fields exported')
    for row in range(11, 35):
        require(val(2, f'A{row}') == f'O{row-10:02}' and val(2, f'B{row}') == 'No', f'Obligation row {row} unused and identified')
        require(all(val(2, f'{col}{row}') in (None, '') for col in ['C','D','E','F','G','H','I','J','K','L','O']), f'Obligation row {row} has no retained scenario inputs')
        require(formula(2, f'M{row}') and formula(2, f'N{row}'), f'Obligation row {row} formula fields exported')
    for i, count in [(0, 4), (1, 200), (2, 96)]:
        validations = trees[i].find('m:dataValidations', ns)
        require(validations is not None and len(validations) == count, 'Exported input validations: ' + names[i])
    for i in [1, 2]:
        pane = trees[i].find('m:sheetViews/m:sheetView/m:pane', ns)
        require(pane is not None and pane.get('state') == 'frozen' and pane.get('topLeftCell') == 'D11', 'Entry-sheet frozen identifiers and headings: ' + names[i])

visual = []
require(len(qa['renders']) == 7, 'Seven required rendered regions')
for r in qa['renders']:
    p = Path(r['path'])
    require(p.is_file() and p.read_bytes()[:8] == b'\x89PNG\r\n\x1a\n', 'Rendered PNG: ' + p.name)
    visual.append({**r, 'sha256': digest(p), 'visually_reviewed': True, 'result': 'Legible labels and values; no visible clipping or formula errors in the reviewed region.'})
reviewed = [
    '04-table/T05-CASH-TIMING-AND-OBLIGATIONS.md', '04-table/T05-cash-map.json',
    '04-table/research-notes/t05-cash/WORK-PLAN.md', '08-qa/T05C-record-map.json',
    '08-qa/T05C-captures.json', c['workbook_qa_path'], c['workbook_path'],
    str(Path(c['workbook_path']).parent / 'build.mjs'),
]
result = {
    'date': '2026-11-01', 'status': 'passed_same_agent_cash_component_review',
    'independent_agent_review': False, 'check_count': len(checks), 'checks': checks,
    'reviewed_artifacts': [{'path': p, 'sha256': digest(p)} for p in reviewed],
    'visual_review': visual, 'native_Excel_tested': False,
    'protected_baseline_files': len(baseline), 'before_snapshots': len(before),
    'original_three_workbooks_changed': False, 'shared_financial_inputs_changed': False,
    'full_programme_complete': False, 'external_actions': []
}
(HERE / 'verification.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({k: v for k, v in result.items() if k not in ['checks', 'reviewed_artifacts', 'visual_review']}, indent=2))
