"""Freeze the reviewed T05 service/sales component and its preservation record."""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def read(name):
    return json.loads((ROOT / name).read_text())

def target(name):
    path = Path(name)
    return path if path.is_absolute() else ROOT / path

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

review = read('08-qa/t05s-review/integration-checks.json')
assert review['status'] == 'passed_for_internal_T05S_component'
assert not review['open_substantive_issues']
assert all(x['passed'] for x in review['checks'])
for x in review['reviewed_artifacts']:
    assert digest(target(x['path'])) == x['sha256'], x['path']
baseline = read('08-qa/T05S-baseline-manifest.json')
for x in baseline['files']:
    assert digest(target(x['path'])) == x['sha256'], x['path']
old_inputs = read('04-table/research-notes/t05-service-costs/before-review/04-table/financial-inputs.json')['records']
inputs = read('04-table/financial-inputs.json')['records']
assert len(old_inputs) == 33 and old_inputs == inputs[:33]
component = read('04-table/T05-service-cost-map.json')
assert component['component_review_complete']
qa = read('08-qa/t05s-workbook/verification.json')
export = read('08-qa/t05s-workbook/export-check.json')
sources = read('02-evidence/registers/sources.json')['records']
claims = read('02-evidence/registers/claims.json')['records']

paths = set()
for folder in ['04-table/research-notes/t05-service-costs', '08-qa/t05s-workbook', '08-qa/t05s-review']:
    paths.update(x for x in (ROOT / folder).rglob('*') if x.is_file() and '__pycache__' not in x.parts and not x.name.startswith('.'))
for name in [
    '04-table/T05-SERVICE-AND-SALES-COSTS.md', '04-table/T05-service-cost-map.json',
    '04-table/financial-inputs.json', '08-qa/T05S-baseline-manifest.json',
    '08-qa/T05S-record-map.json', '08-qa/T05S-captures.json',
    '08-qa/merge_t05s.py', '08-qa/finalize_t05s.py', '08-qa/validate_workspace.py',
    '00-control/CURRENT-STATUS.md', '00-control/work-packages.json', '00-control/changes.json',
    '00-control/decisions.json', 'README.md', '05-analysis/CONTRADICTIONS-AND-GAPS.md',
    '05-analysis/findings.json', '02-evidence/registers/sources.json',
    '02-evidence/registers/claims.json', '02-evidence/registers/searches.json',
    '02-evidence/registers/source-aliases.json',
]:
    paths.add(ROOT / name)
output_dir = Path(component['workbook_absolute_path']).parent
paths.add(Path(component['workbook_absolute_path']))
paths.add(output_dir / 'build.mjs')
paths.update(output_dir.glob('*.png'))
artifacts = []
for path in sorted(paths):
    assert path.is_file(), path
    label = str(path.relative_to(ROOT)) if path.is_relative_to(ROOT) else str(path)
    artifacts.append({'path': label, 'sha256': digest(path)})

result = {
    'date': '2026-11-01',
    'status': 'verification_in_progress',
    'scope': 'Reviewed per-unit future service/sales labour component only. Event operations, travel, non-labour costs, dated cash, matched programme scenarios and commercial validation remain open.',
    'new_source_routes': 5,
    'new_claim_records': 11,
    'canonical_sources': len(sources),
    'canonical_claims': len(claims),
    'source_records_with_primary_originals': sum(bool(x['capture_path']) for x in sources),
    'earlier_source_base_records_preserved': 242,
    'earlier_claim_records_preserved': 484,
    'internal_findings_preserved': len(read('05-analysis/findings.json')['records']),
    'protected_baseline_files': len(baseline['files']),
    'prechange_file_snapshots': len(read('04-table/research-notes/t05-service-costs/before-review/manifest.json')['records']),
    'new_primary_originals': 5,
    'parsed_extracts': 5,
    'workload_tasks': len(component['tasks']),
    'distinct_activity_units': len(component['units']),
    'effort_cases': len(component['effort_cases']),
    'original_financial_inputs_preserved': len(old_inputs),
    'new_component_inputs': len(inputs) - len(old_inputs),
    'shared_financial_inputs': len(inputs),
    'actual_new_monetary_rates': 0,
    'all_programme_activity_quantities_blank': True,
    'commercial_owner_resource_rate_unknown': True,
    'volume_or_conversion_forecast': False,
    'workbook_path': component['workbook_absolute_path'],
    'workbook_sha256': component['workbook_sha256'],
    'workbook_calculation_tests': len(qa['tests']),
    'workbook_visual_regions': len(qa['renders']),
    'saved_file_checks': len(export['checks']),
    'authoring_engine': qa['authoring_engine'],
    'native_Excel_application_tested': False,
    'all_temporary_input_changes_restored': qa['all_temporary_input_changes_restored'],
    'final_saved_effort_case': qa['final_saved_effort_case'],
    'final_programme_hours': qa['final_programme_hours'],
    'final_programme_labour_GBP': qa['final_programme_labour_GBP'],
    'independent_review_status': review['status'],
    'independent_summary_gates': len(review['checks']),
    'independent_reviewed_artifact_hashes': len(review['reviewed_artifacts']),
    'open_substantive_issues': [],
    'first_research_workbook_changed': False,
    'current_contract_fee_changed': False,
    'practitioner_free_full_research_preserved': True,
    'fourteen_core_questions_unchanged': True,
    'actual_customers_or_orders': 0,
    'actual_supplier_quotes_or_hires': 0,
    'actual_timesheets_or_spend': 0,
    'actual_briefings_or_campaigns': 0,
    'actual_practitioner_contributions': 0,
    'actual_buyer_member_validation': 0,
    'fieldwork_or_tool_activation': False,
    'external_messages_or_enquiries': 0,
    'purchases_or_bookings': 0,
    'full_financial_model_complete': False,
    'final_client_delivery': False,
    'next_step': component['next_step'],
    'artifacts': artifacts,
}
completion = ROOT / '08-qa/T05S-completion-check.json'
completion.write_text(json.dumps(result, indent=2, ensure_ascii=False) + '\n')
run = subprocess.run([sys.executable, str(ROOT / '08-qa/validate_workspace.py')], cwd=ROOT, capture_output=True, text=True)
if run.returncode:
    result['status'] = 'validation_failed'
    completion.write_text(json.dumps(result, indent=2, ensure_ascii=False) + '\n')
    sys.stderr.write(run.stdout + run.stderr)
    raise SystemExit(run.returncode)
validation = json.loads(run.stdout)
assert validation['status'] == 'passed'
result['status'] = 'completed_internal_T05S_service_sales_component_full_model_pending'
result['full_workspace_validation'] = validation
result['completion_artifact_hashes_verified'] = True
completion.write_text(json.dumps(result, indent=2, ensure_ascii=False) + '\n')
for x in artifacts:
    assert digest(target(x['path'])) == x['sha256'], x['path']
print(json.dumps({'status': result['status'], 'completion_artifacts': len(artifacts), 'workbook_tests': len(qa['tests']), 'validation': validation}, indent=2))
