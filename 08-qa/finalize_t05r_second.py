"""Freeze the internal second-check record after independent review and validation."""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def read(path):
    return json.loads((ROOT / path).read_text())

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

review = read('08-qa/t05r-second-review/integration-checks.json')
assert review['status'] == 'passed_for_internal_T05R_second_challenge'
assert not review['open_substantive_issues']
assert all(item['passed'] for item in review['checks'])
for item in review['reviewed_artifacts']:
    assert digest(ROOT / item['path']) == item['sha256'], item['path']

baseline = read('08-qa/T05R-second-check-baseline.json')
for item in baseline['files']:
    target = Path(item['path'])
    target = target if target.is_absolute() else ROOT / target
    assert digest(target) == item['sha256'], item['path']

mapping = read('08-qa/T05R-second-check-record-map.json')
conditions = read('04-table/T05R-second-challenge-map.json')
captures = read('08-qa/T05R-second-check-captures.json')
sources = read('02-evidence/registers/sources.json')['records']
claims = read('02-evidence/registers/claims.json')['records']
lineage = read('04-table/research-notes/t05r-second-check/competitors/prior-study-bridge-check.json')
constructed = read('04-table/research-notes/t05r-second-check/root/constructed-cost-applications.json')

paths = set()
for folder in ['04-table/research-notes/t05r-second-check', '08-qa/t05r-second-review']:
    paths.update(x for x in (ROOT / folder).rglob('*') if x.is_file() and not x.name.startswith('.'))
for name in [
    '04-table/T05R-SECOND-CHECK-READOUT.md', '04-table/T05R-COST-AND-DELIVERY-REFINEMENTS.md',
    '04-table/T05R-second-challenge-map.json', '04-table/financial-inputs.json',
    '08-qa/T05R-second-check-baseline.json', '08-qa/T05R-second-check-record-map.json',
    '08-qa/T05R-second-check-captures.json', '08-qa/merge_t05r_second.py',
    '08-qa/validate_workspace.py', '08-qa/finalize_t05r_second.py',
    '00-control/CURRENT-STATUS.md', '00-control/work-packages.json', '00-control/changes.json',
    '00-control/decisions.json', 'README.md', '05-analysis/CONTRADICTIONS-AND-GAPS.md',
    '05-analysis/findings.json', '02-evidence/registers/sources.json',
    '02-evidence/registers/claims.json', '02-evidence/registers/searches.json',
    '02-evidence/registers/source-aliases.json',
]:
    paths.add(ROOT / name)
paths.add(Path(conditions['original_workbook_path']))
artifacts = []
for path in sorted(paths):
    assert path.is_file(), path
    try:
        label = str(path.relative_to(ROOT))
    except ValueError:
        label = str(path)
    artifacts.append({'path': label, 'sha256': digest(path)})

result = {
    'date': '2026-11-01',
    'source_collection_date': '2026-10-31',
    'status': 'verification_in_progress',
    'scope': 'Internal second challenge of the first T05 research/staffing component; remaining customer/service/sales, event and cash model still pending.',
    'new_source_routes': mapping['new_source_routes'],
    'new_claim_records': mapping['new_claim_records'],
    'canonical_sources': len(sources),
    'canonical_claims': len(claims),
    'source_records_with_primary_originals': sum(bool(x['capture_path']) for x in sources),
    'earlier_source_base_records_preserved': 235,
    'earlier_claims_preserved_exactly': 466,
    'internal_findings_preserved': len(read('05-analysis/findings.json')['records']),
    'protected_baseline_files': len(baseline['files']),
    'prechange_file_snapshots': len(read('04-table/research-notes/t05r-second-check/before-review/manifest.json')['records']),
    'original_financial_component_inputs': len(read('04-table/financial-inputs.json')['records']),
    'new_financial_inputs': 0,
    'financial_inputs_unchanged': True,
    'original_workbook_unchanged': True,
    'original_workbook_path': conditions['original_workbook_path'],
    'original_workbook_sha256': conditions['original_workbook_sha256'],
    'original_workbook_edit_needed': False,
    'original_workbook_or_native_Excel_rerun': False,
    'cost_delivery_conditions': len(conditions['conditions']),
    'constructed_applications': len(constructed['cases']),
    'constructed_examples_not_observations_or_adopted_inputs': True,
    'prior_study_questions': 3,
    'prior_study_saved_answers': 24,
    'prior_study_semantic_rereads': 3,
    'prior_study_strand_lineage_checks': len(lineage['checks']),
    'model_reruns': 0,
    'new_route_primary_originals': captures['new_route_primary_originals'],
    'reused_route_fresh_primary_originals': captures['reused_route_fresh_primary_originals'],
    'new_route_reader_extracts': captures['new_route_browser_reader_extracts'],
    'capture_inventory_artifacts': len(captures['records']),
    'capture_counts_by_kind': captures['counts_by_kind'],
    'prior_notes_distinguished_from_fresh_access': True,
    'independent_review_status': review['status'],
    'independent_grouped_checks': len(review['checks']),
    'independent_exact_artifact_hashes': len(review['reviewed_artifacts']),
    'open_substantive_issues': [],
    'actual_quotes': 0,
    'actual_suppliers_or_hires': 0,
    'actual_timesheets_or_savings': 0,
    'actual_practitioner_contributions': 0,
    'actual_buyer_member_validation': 0,
    'fieldwork_or_tool_activation': False,
    'external_messages_or_enquiries': 0,
    'spend_purchases_or_bookings': 0,
    'current_contract_fee_changed': False,
    'fourteen_core_questions_unchanged': True,
    'client_files_changed': False,
    'full_financial_model_complete': False,
    'final_client_delivery': False,
    'next_step': 'Customer/licence fulfilment, briefings, partner obligations and sales effort, then selected event/travel and dated cash before the complete matched A/B pilot/annual model.',
    'artifacts': artifacts,
}
completion = ROOT / '08-qa/T05R-second-check-completion.json'
completion.write_text(json.dumps(result, indent=2, ensure_ascii=False) + '\n')
run = subprocess.run([sys.executable, str(ROOT / '08-qa/validate_workspace.py')], cwd=ROOT, capture_output=True, text=True)
if run.returncode:
    result['status'] = 'validation_failed'
    completion.write_text(json.dumps(result, indent=2, ensure_ascii=False) + '\n')
    sys.stderr.write(run.stdout + run.stderr)
    raise SystemExit(run.returncode)
validation = json.loads(run.stdout)
assert validation['status'] == 'passed'
result['status'] = 'completed_internal_T05R_second_challenge_full_model_pending'
result['full_workspace_validation'] = validation
result['completion_artifact_hashes_verified'] = True
completion.write_text(json.dumps(result, indent=2, ensure_ascii=False) + '\n')
for item in artifacts:
    target = Path(item['path'])
    assert digest(target if target.is_absolute() else ROOT / target) == item['sha256'], item['path']
print(json.dumps({'status': result['status'], 'completion_artifacts': len(artifacts), 'independent_grouped_checks': len(review['checks']), 'validation': validation}, indent=2))
