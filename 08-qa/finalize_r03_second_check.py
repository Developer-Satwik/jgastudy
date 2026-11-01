from pathlib import Path
import hashlib,json

ROOT=Path(__file__).resolve().parents[1]
DATE='2026-10-29'
def read(p):return json.loads(p.read_text())
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
review=ROOT/'08-qa/R03-second-check-independent-review.md'
assert review.exists(),'Independent integrated review is required before completion.'

fp=ROOT/'05-analysis/findings.json';findings=read(fp)
rows=[
 ('FND-029','Continuing readiness is relevant to retained, configured, replaced and delegated arrangements as well as initial go-live.',
  ['CLM-0235','CLM-0236','CLM-0237','CLM-0238','CLM-0239','CLM-0249'],
  'Official operating guidance, supplier release conditions and historical context do not establish maintenance burden, realised forecasts or a universal release schedule.',
  'Separate transition, ordinary cycle, scheduled updates and exceptional changes; identify the applicable change, owner, relevant check, communication and exception route.'),
 ('FND-030','Self-service can change the distribution of work and benefits across employees, managers and operators.',
  ['CLM-0240','CLM-0243'],
  'Declared features support a work-journey question, not a measured net saving, increased burden or user-acceptance result.',
  'Examine who originates, approves, operates, benefits and obtains support, separating one-off preparation from recurring work and preserving outcome quality.'),
 ('FND-031','The actual product, package, country/entity, worker/service relationship and underlying parties define the useful comparison.',
  ['CLM-0241','CLM-0242','CLM-0243'],
  'Deliberately selected supplier examples are not a market census, service-equivalence test or jurisdictional employment advice.',
  'Distinguish software, HR records, payroll, payment, partner coordination and employment-provider roles; check the real case scope without adding an employment-model recommendation.'),
 ('FND-032','Individual capacity, enduring leadership, consulting-led outputs and ongoing payroll execution are distinct engagement questions.',
  ['CLM-0244','CLM-0245','CLM-0246','CLM-0247','CLM-0248'],
  'Editorial and cross-function service declarations sharpen analysis but do not establish payroll performance, staffing demand, availability or actual engagement terms.',
  'Broaden P08 beyond time-bound cover; establish duration, task, work product, completion/acceptance, retained business authority and knowledge handback. Keep operations and change capacity visible together.'),
 ('FND-033','Recoverability and useful delegated capability must be assessed alongside retained configuration and accepted technical dependence.',
  ['CLM-0249','CLM-0250','CLM-0251','CLM-0252'],
  'Guidance supplies conditional design checks, not product certification, a recovery test, a payroll switching cost or a zero-dependence mandate.',
  'Distinguish export, backup and a usable restored/receiving service. Preserve managed-service benefits while identifying relevant access, configuration, skills and recovery/handback conditions.')
]
for ident,statement,claims,limits,implication in rows:
    if any(r['finding_id']==ident for r in findings['records']):continue
    findings['records'].append({'finding_id':ident,'topic_ids':['R03'],'statement':statement,'supporting_claim_ids':claims,
      'contradicting_claim_ids':[],'participant_observation_ids':[],'interpretation':limits,'decision_implication':implication,
      'confidence_rationale':'Targeted second challenge from inspected primary context, bounded reuse and independent integration review; not original fieldwork or validated option scoring.',
      'outstanding_questions':['Actual context, retained work, user outcomes, engagement and continuing readiness in permissioned practitioner cases.'],
      'publication_status':'internal_research_design','reviewed_on':DATE})
findings['status']='R01_R02_R03_internal_synthesis_including_R03_second_challenge';write(fp,findings)

ch=ROOT/'00-control/changes.json';changes=read(ch)
if not any(r['change_id']=='CHG-009' for r in changes['records']):
    changes['records'].append({'change_id':'CHG-009','date':DATE,'type':'User-requested second challenge of R03',
      'description':'Historical/lifecycle, market, specific competitor/prior-study and dependency/recovery checks. Twelve new primary routes and eighteen contextual records, five internal findings; broadened P08 to enduring capability/leadership and added five cross-cutting conditions. First-pass snapshots, original constructed-prompt bridge limits and client/core files preserved. No product/API trial, new original fieldwork or external action.'})
write(ch,changes)
wp=ROOT/'00-control/work-packages.json';packages=read(wp)
packages['updated_on']=DATE;packages['active_work_package']='WP06'
packages['next_action']='R03 second challenge completed; begin R04 decision-authority research as the next substantive step. No external sending.'
for r in packages['records']:
    if r['work_package_id']=='WP05':
        r['second_challenge_completed_on']=DATE;r['second_challenge_readout']='03-report/R03-SECOND-CHECK-READOUT.md'
        if 'Second challenge applied:' not in r['evidence_of_completion']:
            r['evidence_of_completion']+=' Second challenge applied: continuing readiness, whole-work effects, exact service unit, engagement/output ownership and recovery/dependence; P08 includes enduring capability. Prior constructed scenarios checked with anti-anchoring rule. Practitioner/final-use work remains open.'
write(wp,packages)
gaps=ROOT/'05-analysis/CONTRADICTIONS-AND-GAPS.md';text=gaps.read_text()
if '## R03 second-challenge controls' not in text:
    text+='''
## R03 second-challenge controls

- Historical expectations and release/update guidance: do not become observed adoption, fulfilled forecasts, maintenance cost or a universal payroll cadence. CLM-0235–0239.
- Self-service scope is not measured net saving or burden. Track work and outcomes across the actual stakeholders. CLM-0240/0243.
- Multicountry product/worker/service roles and partner coordination are not equivalent under one global brand; no employment-model recommendation or all-country guarantee. CLM-0241–0243.
- Recruitment, project/SOW delivery and ongoing operation declarations are not a signed payroll contract or achieved result. P08 now permits enduring leadership without presumed hiring demand. CLM-0244–0248.
- Constructed prior S04/S05/S09 scenarios remain analyst contrasts; unaided participant priorities come first. No ranking/demand inference. Independent bridge check preserves twelve prompt texts, ninety-six saved answers and global source limits.
- Oakleaf TCT live redirect: cached body excluded from current claims; redirected homepage retained only as access evidence. No capability-disappearance inference.
- Export/backup is not proof of recoverable service; technical dependence can bring useful managed capability. No recovery target, provider certification or payroll switching-cost estimate. CLM-0249–0252.
'''
    gaps.write_text(text)

# Preserve client work and the first-pass evidence trail while legitimately revising current R03 synthesis.
client=[]
for version in ['0.1','0.2']:
    for record in read(ROOT/f'06-client-checkpoints/week-one-v{version}/checkpoint-manifest.json')['files']:
        sha=hashlib.sha256((ROOT/record['path']).read_bytes()).hexdigest();assert sha==record['sha256']
        client.append({'path':record['path'],'sha256':sha,'unchanged':True})
for r in read(ROOT/'08-qa/R02-second-check-completion.json')['artifacts']:
    assert hashlib.sha256((ROOT/r['path']).read_bytes()).hexdigest()==r['sha256']
snapshots=read(ROOT/'03-report/research-notes/r03-second-check/before-review/manifest.json')['files']
first={r['path']:r['sha256'] for r in read(ROOT/'08-qa/R03-completion-check.json')['artifacts']}
for r in snapshots:
    assert hashlib.sha256((ROOT/r['snapshot_path']).read_bytes()).hexdigest()==r['sha256']==first[r['original_path']]
questions=read(ROOT/'01-method/question-map.json')
assert questions==read(ROOT/'01-method/question-map-v0.2.json') and len(questions['records'])==14
bridge=read(ROOT/'08-qa/R03-prior-study-bridge-check.json')
assert bridge['status']=='passed' and len(bridge['checks'])==148 and all(c['passed'] for c in bridge['checks'])
assert hashlib.sha256((ROOT/bridge['bridge_path']).read_bytes()).hexdigest()==bridge['bridge_sha256']
mapping=read(ROOT/'08-qa/R03-second-check-record-map.json')
assert len(mapping['source_map'])==12 and len(mapping['claim_map'])==18
sources=read(ROOT/'02-evidence/registers/sources.json')['records'];claims=read(ROOT/'02-evidence/registers/claims.json')['records']
captures=read(ROOT/'08-qa/R03-second-check-captures.json')['files']
files=['03-report/R03-SECOND-CHECK-READOUT.md','03-report/R03-DESKTOP-READOUT.md','03-report/R03-OPTIONS-AND-TRADEOFFS.md','03-report/R03-option-map.json','03-report/modules/R03-technology-and-operating-model-tradeoffs.md','08-qa/R03-second-check-independent-review.md','08-qa/R03-prior-study-bridge-check.json','08-qa/R03-second-check-record-map.json']
result={'date':DATE,'status':'passed_for_internal_R03_second_challenge','supersedes_for_current_synthesis':'08-qa/R03-completion-check.json',
 'new_source_routes':12,'new_claim_or_guardrail_records':18,'source_records':len(sources),'claim_records':len(claims),
 'source_records_with_retained_original':sum(bool(s.get('capture_path')) for s in sources),'internal_findings':len(findings['records']),
 'retained_original_files_hash_checked':sum(r['scope']=='retained_original' for r in captures),
 'excluded_redirect_response_hash_checked':sum(r['scope']=='excluded_redirect_response' for r in captures),
 'prior_bridge_checks_passed':len(bridge['checks']),'client_files':client,'prior_R02_artifacts_unchanged':True,'first_pass_R03_snapshots':snapshots,
 'fourteen_core_questions_unchanged':True,'option_paths':8,'cross_cutting_conditions':5,
 'artifacts':[{'path':f,'sha256':hashlib.sha256((ROOT/f).read_bytes()).hexdigest()} for f in files],
 'new_practitioner_observations':0,'product_or_API_tests':0,'final_publication_approved':False,'external_actions':[],
 'next':'R04 decision authority/pathways; no external sending.'}
write(ROOT/'08-qa/R03-second-check-completion.json',result)
print(json.dumps({k:v for k,v in result.items() if k not in ['artifacts','client_files','first_pass_R03_snapshots']},indent=2))
