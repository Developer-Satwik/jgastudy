from pathlib import Path
import json,hashlib,re

ROOT=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent
def read(p):return json.loads((ROOT/p).read_text())
def sha(p):return hashlib.sha256((ROOT/p).read_bytes()).hexdigest()
checks=[]
def check(v,label):
    checks.append(dict(check=label,passed=bool(v)))
    if not v:raise AssertionError(label)

pre=read('08-qa/r07-second-review/source-review-checks.json')
for x in pre['checks']:check(x['passed'],'Preliminary independent check: '+x['check'])
for x in read('08-qa/R07-second-check-baseline.json')['records']:
    check(sha(x['path'])==x['sha256'],'Final baseline preserved: '+x['path'])
snaps=read('03-report/research-notes/r07-second-check/before-review/manifest.json')['records']
for x in snaps:check(sha(x['snapshot_path'])==x['sha256'],'Final snapshot preserved: '+x['original_path'])
first=read(next(x['snapshot_path'] for x in snaps if x['original_path']=='03-report/R07-priority-map.json'))
model=read('03-report/R07-priority-map.json')
for k in ['priority_dimensions','context_dimensions','comparison_claim_purposes','planning_signals','blank_priority_template','blank_context_template','blank_comparison_template','current_question_ids']:
    check(model[k]==first[k],'First-pass R07 field retained exactly: '+k)
mapping=read('08-qa/R07-second-check-record-map.json')
sources={x['source_id']:x for x in read('02-evidence/registers/sources.json')['records']}
claims={x['claim_id']:x for x in read('02-evidence/registers/claims.json')['records']}
check(len(mapping['source_map'])==7 and len(mapping['claim_map'])==19,'Seven routes and19 bounded second-challenge claims mapped')
check(set(mapping['source_map'].values())<=set(sources),'Mapped sources resolve')
check(set(mapping['claim_map'].values())<=set(claims),'Mapped claims resolve')
for d in ['history','market','competitors','root']:
    records=read('03-report/research-notes/r07-second-check/'+d+'/claim-candidates.json')['records']
    for c in records:
        x=claims[mapping['claim_map'][c['candidate_id']]]
        check(x['claim_text']==c['claim_text'],'Exact candidate/canonical claim text: '+c['candidate_id'])
        check(x['value'] is None and x['metric'] is None,'No numeric promotion: '+c['candidate_id'])
        check(set(x['source_ids'])<=set(sources),'Source references resolve: '+c['candidate_id'])
        check(bool(x['interpretation_limits']),'Interpretation boundary retained: '+c['candidate_id'])
for ident in ['M7S-S02','C7S-S01','C7S-S02']:
    s=sources[mapping['source_map'][ident]]
    check(not s['capture_path'] and bool(s['review_extracts']),'Reader notes not promoted to raw original: '+ident)
check(not sources['SRC-0153']['capture_path'],'GovS002 existing missing raw capture not silently repaired')
check(sources[mapping['source_map']['R7R-S01']]['capture_path'].endswith('.html'),'GovS005 retains actual raw HTML')
for x in read('08-qa/R07-second-check-captures.json')['files']:
    check(sha(x['path'])==x['sha256'],'Second-challenge retained file hash: '+x['path'])
    if x['path'].endswith('M7S-S02-selected-reader-notes.txt'):
        check(x['kind']=='parsed_or_selected_extract','Raw403 not incorrectly applied to valid FreeAgent reader note')
for ident,status in [('CLM-0051','quarantined_conflicting'),('CLM-0052','quarantined_conflicting'),('CLM-0167','hold_numeric_reuse'),('CLM-0168','hold_numeric_reuse'),('CLM-0218','hold_universal_ui_behaviour'),('CLM-0392','hold_numeric_reuse')]:
    check(claims[ident]['status']==status,'Final hold retained: '+ident)
check(model['maximum_selective_priorities']==2 and model['extra_mandatory_questions']==0 and model['fourteen_core_questions_unchanged'],'Existing two-priority/14question route preserved')
check(not model['ordinal_status_ladder'] and not model['validated_priority_score'] and not model['mandatory_sequence'],'No score or mandatory ladder introduced')
for k in ['participant_observations','completed_case_comparisons','forecast_calculations','subgroup_estimates','market_rankings']:
    check(model[k]==[],'Unperformed evidence remains empty: '+k)
for p in ['05-analysis/observations.json','05-analysis/charts.json','04-table/financial-inputs.json']:
    check(read(p)['records']==[],'Shared unperformed records remain empty: '+p)
check(read('01-method/question-map.json')==read('01-method/question-map-v0.2.json'),'Final question map remains exact version0.2')
for rel in ['03-report/R07-SECOND-CHECK-READOUT.md','03-report/R07-DESKTOP-READOUT.md','03-report/R07-CONTEXTUAL-PRIORITIES.md','03-report/modules/R07-priorities-and-contextual-differences.md']:
    t=(ROOT/rel).read_text()
    check(set(re.findall(r'CLM-\d{4}',t))<=set(claims),'Integrated claim references resolve: '+rel)
    for a,b in re.findall(r'CLM-(\d{4})[–-](\d{4})',t):
        check({f'CLM-{n:04}' for n in range(int(a),int(b)+1)}<=set(claims),'Integrated claim range resolves: '+rel)
result=dict(date='2026-10-29',status='structural_checks_passed_semantic_review_pending',check_count=len(checks),checks=checks,independence='Reviewer did not author any research strand or integration.',scope='Bounded second-challenge desktop integration and preservation checks; not original fieldwork, numerical trend, vendor validation, final legal/currentness assurance or final publication approval.')
(OUT/'integrated-review-checks.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='checks'},indent=2))
