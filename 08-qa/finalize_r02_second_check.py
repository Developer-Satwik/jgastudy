from pathlib import Path
import hashlib,json,re,subprocess,sys

ROOT=Path(__file__).resolve().parents[1]
DATE='2026-10-28'
def read(path):return json.loads(path.read_text())
def write(path,data):path.write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')

fp=ROOT/'05-analysis/findings.json';findings=read(fp)
rows=[
 ('FND-019','Resolution may depend on external institutions, and prevention, legacy correction and consequence closure are distinct stages.',
  ['CLM-0184','CLM-0185','CLM-0186'],
  'Historical self-review and selected reported cases establish mechanisms, not present prevalence or deterioration.',
  'Map detection, authority, amendment and closure across the relevant parties; distinguish new cases from residual work.'),
 ('FND-020','Market scope and retained work can explain an unmet outcome even where a named capability is publicly offered.',
  [f'CLM-{n:04}' for n in range(189,195)],
  'Deliberately selected live guidance/product/service pages establish boundaries only; no market census, procurement score or achieved-result inference.',
  'Use complexity, footprint, entitlement, readiness and execution/retained duties as context. Keep licence/add-on/transaction/service fees and internal effort separate.'),
 ('FND-021','Capacity can concern ongoing operations, temporary continuity, specialist change expertise or accountable leadership and oversight.',
  [f'CLM-{n:04}' for n in range(195,203)],
  'Recruitment offers, a publisher-reported case and a vacancy inform case contrasts; they do not establish shortage, demand or the need to hire.',
  'Establish tasks, specialist context, authority, cover and knowledge handback where relevant. Keep recruitment, consultancy and payroll execution distinct.'),
 ('FND-022','Safe authorisation, appropriate access, continuity and recoverability qualify the operating outcomes across the needs map.',
  ['CLM-0203','CLM-0204','CLM-0205'],
  'Guidance, a payment definition and one dated incident account are distinct evidence; none estimates payroll risk or proves cloud resilience.',
  'Distinguish approved calculation, actual payment, information protection and continuity. Investigate only the relevant dependency without collecting sensitive records.'),
 ('FND-023','The appropriate information-quality test depends on its use, and recurrence of historical themes is not a measured trend.',
  ['CLM-0187','CLM-0188'],
  'Statistical methodology and unlike historical/selected-case sources cannot supply employer error rates or a comparable time series.',
  'State intended user, decision, transformations and timeliness. Present dated context without manufacturing a progress or deterioration curve.')
]
for ident,statement,support,limits,implication in rows:
    if any(r['finding_id']==ident for r in findings['records']):continue
    findings['records'].append({'finding_id':ident,'topic_ids':['R02'],'statement':statement,
     'supporting_claim_ids':support,'contradicting_claim_ids':[],'participant_observation_ids':[],
     'interpretation':limits,'decision_implication':implication,
     'confidence_rationale':'Source-specific primary context and bounded analytical challenge; not new practitioner evidence or population inference.',
     'outstanding_questions':['Actual materiality, context, ownership and observed outcomes in permissioned practitioner cases.'],
     'publication_status':'internal_research_design','reviewed_on':DATE})
findings['status']='R01_and_R02_internal_synthesis_including_R02_second_challenge';write(fp,findings)

ch=ROOT/'00-control/changes.json';changes=read(ch)
if not any(r['change_id']=='CHG-007' for r in changes['records']):
    changes['records'].append({'change_id':'CHG-007','date':DATE,'type':'User-requested second challenge of R02',
      'description':'Tested R02 through historical, market, recruitment-competitor, employee, institutional, payment, resilience and evidence-quality lenses. Twenty new primary routes and twenty-two contextual claim records; five internal findings. Updated needs map/readout, preserved first-pass snapshots and unchanged client/core-question files. Prior AI-study bridge independently checked; no new prompts or external actions.'})
write(ch,changes)

wp=ROOT/'00-control/work-packages.json';packages=read(wp)
packages['next_action']='R02 second challenge complete; R03 ready for the next substantive desktop step. No external sending.'
for r in packages['records']:
    if r['work_package_id']=='WP04':
        r['second_challenge_completed_on']=DATE
        r['second_challenge_readout']='03-report/R02-SECOND-CHECK-READOUT.md'
        r['evidence_of_completion']+=' Second challenge applied: historical/external resolution, market scope/complexity, all six prior recruitment comparators and prior-study bridge, payment and resilience conditions. Original inputs and final-use checks still open.' if 'Second challenge applied:' not in r['evidence_of_completion'] else ''
write(wp,packages)

gaps=ROOT/'05-analysis/CONTRADICTIONS-AND-GAPS.md';text=gaps.read_text()
if '## R02 second-challenge interpretation controls' not in text:
    text+='''
## R02 second-challenge interpretation controls

- Historical RTI review versus selected 2025 cases: recurring mechanisms, no comparable incidence series or deterioration conclusion. CLM-0184–0188.
- Payroll supplier and recruitment firm declarations: inspectable scope, not actual demand, shortages, availability, achieved service or relative quality. CLM-0189–0202.
- Software/payroll add-ons, transaction charges, managed-service fees and retained effort: unlike price units; no total-cost ranking from live pages.
- Earlier 352-answer AI study: discovery bridge only; exact hashes and selected counts checked. Seven incomplete source records remain six partial and one pending. No conversion to employer observations or market share.
- British Library incident account: wider staff/user information harm and payroll continuity are distinct; payroll-data exposure or causal cloud advantage not established. CLM-0205.
- Middlemore live body differs from indexed/earlier text. Current retained original supports current scope only; no inferred date or capability trend.
'''
    gaps.write_text(text)

# Verify review drafts, original prompt-study exports and first-pass snapshots remain intact.
client=[]
for version in ['0.1','0.2']:
    for f in read(ROOT/f'06-client-checkpoints/week-one-v{version}/checkpoint-manifest.json')['files']:
        sha=hashlib.sha256((ROOT/f['path']).read_bytes()).hexdigest();assert sha==f['sha256']
        client.append({'path':f['path'],'sha256':sha,'unchanged':True})
snapshots=read(ROOT/'03-report/research-notes/r02-second-check/before-review/manifest.json')['files']
for record in snapshots:
    assert hashlib.sha256((ROOT/record['snapshot_path']).read_bytes()).hexdigest()==record['sha256']
bridge=read(ROOT/'08-qa/R02-prior-study-bridge-check.json')
assert bridge['status']=='passed' and all(c['passed'] for c in bridge['checks'])
mapping=read(ROOT/'08-qa/R02-second-check-record-map.json')
sources=read(ROOT/'02-evidence/registers/sources.json')['records']
claims=read(ROOT/'02-evidence/registers/claims.json')['records']
assert len(mapping['source_map'])==20 and len(mapping['claim_map'])==22
assert len({c['claim_id'] for c in claims})==len(claims)
ids={c['claim_id'] for c in claims}
for rel in ['03-report/R02-SECOND-CHECK-READOUT.md','03-report/R02-NEEDS-CONSEQUENCES-MATRIX.md']:
    txt=(ROOT/rel).read_text()
    for start,end in re.findall(r'CLM-(\d{4})[–-](\d{4})',txt):assert {f'CLM-{n:04}' for n in range(int(start),int(end)+1)}<=ids
    assert set(re.findall(r'CLM-\d{4}',txt))<=ids

review=ROOT/'08-qa/R02-second-check-independent-review.md'
assert review.exists(),'Independent integrated review is required before completion.'
files=['03-report/R02-SECOND-CHECK-READOUT.md','03-report/R02-DESKTOP-READOUT.md','03-report/R02-NEEDS-CONSEQUENCES-MATRIX.md','03-report/modules/R02-operational-needs-and-service-gaps.md','08-qa/R02-second-check-independent-review.md','08-qa/R02-prior-study-bridge-check.json']
result={'date':DATE,'status':'passed_for_internal_R02_second_challenge','supersedes_for_current_synthesis':'08-qa/R02-DESKTOP-completion-check.json',
 'new_source_routes':20,'new_claim_or_guardrail_records':22,'source_records':len(sources),'claim_records':len(claims),
 'source_records_with_retained_original':sum(bool(s.get('capture_path')) for s in sources),'internal_findings':len(findings['records']),
 'new_original_files_hash_checked':len(read(ROOT/'08-qa/R02-second-check-captures.json')['files']),
 'prior_study_bridge_checks_passed':len(bridge['checks']),
 'client_files':client,'first_pass_snapshots':snapshots,
 'artifacts':[{'path':f,'sha256':hashlib.sha256((ROOT/f).read_bytes()).hexdigest()} for f in files],
 'fourteen_core_questions_unchanged':True,'new_practitioner_observations':0,'final_publication_approved':False,
 'external_actions':[],'next':'R03 technology, integration and operating-model trade-offs; no external sending.'}
write(ROOT/'08-qa/R02-second-check-completion.json',result)
print(json.dumps(result,indent=2))
