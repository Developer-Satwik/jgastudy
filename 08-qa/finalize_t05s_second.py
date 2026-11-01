"""Record completion of the bounded service/sales second challenge."""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def read(name):
    return json.loads((ROOT / name).read_text())

def file(name):
    path = Path(name)
    return path if path.is_absolute() else ROOT / path

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

review = read('08-qa/t05s-second-review/review-checks.json')
assert review['status'] == 'passed_same_agent_second_check' and not review['independent_agent_review']
assert all(x['passed'] for x in review['checks'])
for x in review['reviewed_artifacts']:
    assert sha(file(x['path'])) == x['sha256'], x['path']
baseline = read('08-qa/T05S-second-check-baseline.json')
for x in baseline['files']:
    assert sha(file(x['path'])) == x['sha256'], x['path']
component = read('04-table/T05S-second-challenge-map.json')
applications = read(component['cost_applications_path'])
sources = read('02-evidence/registers/sources.json')['records']
claims = read('02-evidence/registers/claims.json')['records']
paths = set()
for folder in ['04-table/research-notes/t05s-second-check', '08-qa/t05s-second-review']:
    paths.update(x for x in (ROOT / folder).rglob('*') if x.is_file() and '__pycache__' not in x.parts and not x.name.startswith('.'))
for name in [
    '04-table/T05S-SECOND-CHECK-READOUT.md', '04-table/T05S-PROGRAMME-COST-REFINEMENTS.md',
    '04-table/T05S-second-challenge-map.json', '04-table/financial-inputs.json',
    '08-qa/T05S-second-check-baseline.json', '08-qa/T05S-second-check-record-map.json',
    '08-qa/T05S-second-check-captures.json', '08-qa/merge_t05s_second.py',
    '08-qa/validate_workspace.py', '08-qa/finalize_t05s_second.py',
    '00-control/CURRENT-STATUS.md', '00-control/work-packages.json', '00-control/changes.json',
    '00-control/decisions.json', 'README.md', '05-analysis/CONTRADICTIONS-AND-GAPS.md',
    '05-analysis/findings.json', '02-evidence/registers/sources.json', '02-evidence/registers/claims.json',
    '02-evidence/registers/searches.json', '02-evidence/registers/source-aliases.json',
]:
    paths.add(ROOT / name)
paths.add(Path(component['first_component_workbook_path']))
artifacts = [{'path': str(x.relative_to(ROOT)) if x.is_relative_to(ROOT) else str(x), 'sha256': sha(x)} for x in sorted(paths)]
result = {
    'date': '2026-11-01',
    'status': 'verification_in_progress',
    'scope': 'Same-agent second challenge of per-unit service/sales costs, with required incurred-work and remaining-obligation programme refinements recorded. No full-model completion or new independent-agent audit.',
    'new_source_routes': 2, 'new_claim_records': 13,
    'canonical_sources': len(sources), 'canonical_claims': len(claims),
    'source_records_with_primary_originals': sum(bool(x['capture_path']) for x in sources),
    'earlier_source_records_preserved': 247, 'earlier_claim_records_preserved': 495,
    'internal_findings_preserved': 81, 'protected_baseline_files': len(baseline['files']),
    'prechange_file_snapshots': 13,
    'new_route_originals': 1, 'new_route_selected_reader_notes': 1,
    'reused_route_fresh_originals': 5, 'reused_route_current_reader_notes': 2,
    'prior_context_reused': 1, 'unadopted_discovery_routes': 1,
    'capture_inventory_artifacts': 16, 'all_financial_inputs_preserved': 70,
    'new_financial_inputs': 0, 'original_workbooks_changed': False,
    'original_catalogue_tasks_preserved': 21, 'original_catalogue_units_preserved': 15,
    'programme_refinement_conditions': len(component['conditions']),
    'programme_noncompletion_and_exception_work_still_required': True,
    'constructed_applications': len(applications['cases']),
    'constructed_application_checks': len(applications['checks']),
    'prior_questions': 4, 'saved_answers_linked': 32,
    'semantic_rereads': 4, 'prior_study_exact_checks': 136, 'model_reruns': 0,
    'same_agent_review_checks': len(review['checks']),
    'reviewed_artifact_hashes': len(review['reviewed_artifacts']),
    'new_independent_agent_review': False, 'native_Excel_application_tested': False,
    'arithmetic_error_identified_in_original_defined_units': False,
    'fourteen_core_questions_unchanged': True, 'current_contract_fee_changed': False,
    'practitioner_free_full_research_preserved': True,
    'actual_quotes_customers_or_staffing': 0, 'actual_savings_or_timesheets': 0,
    'actual_practitioner_or_buyer_contributions': 0,
    'external_messages_or_enquiries': 0, 'purchases_hires_or_bookings': 0,
    'fieldwork_or_campaign_activated': False, 'full_financial_model_complete': False,
    'final_client_delivery': False,
    'next_step': 'Event/participant operations, hosting/moderation and travel, then dated cash and complete matched programme integration. The latter must incorporate the recorded incurred-work and remaining-obligation requirements.',
    'artifacts': artifacts,
}
completion = ROOT / '08-qa/T05S-second-check-completion.json'
completion.write_text(json.dumps(result, indent=2) + '\n')
run = subprocess.run([sys.executable, str(ROOT / '08-qa/validate_workspace.py')], cwd=ROOT, capture_output=True, text=True)
if run.returncode:
    result['status'] = 'validation_failed'
    completion.write_text(json.dumps(result, indent=2) + '\n')
    sys.stderr.write(run.stdout + run.stderr)
    raise SystemExit(run.returncode)
result['full_workspace_validation'] = json.loads(run.stdout)
assert result['full_workspace_validation']['status'] == 'passed'
result['status'] = 'completed_internal_T05S_second_challenge_required_programme_refinements_recorded'
result['completion_artifact_hashes_verified'] = True
completion.write_text(json.dumps(result, indent=2) + '\n')
for x in artifacts:
    assert sha(file(x['path'])) == x['sha256'], x['path']
print(json.dumps({'status': result['status'], 'completion_artifacts': len(artifacts), 'validation': result['full_workspace_validation']}, indent=2))
