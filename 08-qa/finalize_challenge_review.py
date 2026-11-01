from pathlib import Path
import json, re, hashlib

ROOT=Path(__file__).resolve().parents[1]
DATE='2026-10-28'
def read(p):return json.loads(p.read_text())
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')

# Wording cleanup only in the newly authored prose, without changing linked URLs.
for rel in ['03-report/SECOND-REVIEW-READOUT.md','06-client-checkpoints/week-one-v0.1/SECOND-REVIEW-CHANGESET.md']:
 p=ROOT/rel;t=p.read_text()
 t=re.sub(r'\b([A-Za-z]+)(20\d{2})\b',r'\1 \2',t)
 t=re.sub(r'\b(version|within|remains)(?=\d)',r'\1 ',t)
 t=re.sub(r'(\d)(?=(?:October|April|March|June|July|November|September|December|core|months|questions)\b)',r'\1 ',t)
 t=t.replace('versions0.1','versions 0.1')
 p.write_text(t)

mapping=read(ROOT/'08-qa/challenge-record-map.json')['records']
by_id={r['candidate_id']:r for r in mapping}
def evidence(ids):return [by_id[i]['claim_id'] for i in ids]
fp=ROOT/'05-analysis/findings.json';f=read(fp)
new=[
 ('FND-007',['R01','R08'],'JGA has a documented public research and guidance lineage relevant to this report.',
  ['HIS-S01','HIS-S02','ROOT-C01','ROOT-C04'],
  'Sponsorship, forewords and announced education are positioning context, not proof of market demand or programme results.',
  'Investigate changed conditions and actual decisions rather than duplicate broad AI/strategy guidance.'),
 ('FND-008',['R01','R02','R04'],'The current guide needs to capture needs that have not become proposals and distinguish different gap mechanisms.',
  ['METHOD-C01','HIS-S04','ROOT-C07'],
  'This is an instrument-design inference, not evidence of how often pre-proposal barriers occur.',
  'Add a selective no-case probe and classify supported explanations without treating perceived gaps as verified absence of supply.'),
 ('FND-009',['R05','R06','R08'],'Intended value, affordability, implementation and realised benefits need separate treatment.',
  ['EC01','EC02','EC03','EC04'],
  'Public guidance and a large shared-services case inform analytical distinctions; they are not ordinary private-employer payroll benchmarks.',
  'Add selective intended-outcome, baseline, cost-scope, benefit-owner and observed-result probes.'),
 ('FND-010',['R03','R07','R08'],'A dated conditional outlook is more defensible than extrapolating unlike surveys into a numerical adoption forecast.',
  ['HIS-S03','METHOD-C02','ROOT-C06'],
  'Historical themes, current interim policy milestones and possible futures are different evidence classes; no probabilities are estimated.',
  'Use a short history element and a signal-condition-decision table within existing chapters, with final date checks.'),
 ('FND-011',['R01','T01','T02'],'The Table must demonstrate a defined decision use and distinct licensed value against existing research alternatives.',
  ['EC07','EC08','METHOD-C01'],
  'Product descriptions establish alternatives, not JGA willingness to pay, price or conversion.',
  'Keep buyer, member, event and practitioner evidence separate; preserve the existing financial specification and test actual rights/use cases.')]
for ident,topics,statement,ids,limits,action in new:
 if any(r['finding_id']==ident for r in f['records']):continue
 f['records'].append({'finding_id':ident,'topic_ids':topics,'statement':statement,'supporting_claim_ids':evidence(ids),
  'contradicting_claim_ids':[],'participant_observation_ids':[],'interpretation':limits,'decision_implication':action,
  'confidence_rationale':'Second independent design challenge against original public sources and the actual instrument; not practitioner or buyer validation.',
  'outstanding_questions':['Actual practitioner evidence and/or commercial usefulness remain to be tested where relevant.'],
  'publication_status':'internal_research_design','reviewed_on':DATE})
f['status']='R01_and_second_review_internal_design_findings';write(fp,f)

wp=ROOT/'00-control/work-packages.json';w=read(wp)
for r in w['records']:
 if r['work_package_id']=='WP02':
  r['status']='additional_review_complete_refinements_proposed'
  r['latest_review']='03-report/SECOND-REVIEW-READOUT.md'
  r['sharing_status']='Do not send version0.1; assess and apply proposed targeted refinements into a preserved new version first.'
write(wp,w)

cp=ROOT/'00-control/changes.json';c=read(cp)
if not any(r.get('change_id')=='CHG-003' for r in c['records']):
 c['records'].append({'change_id':'CHG-003','date':DATE,'type':'Additional internal research challenge; no commercial scope change',
  'description':'Reviewed history, economic value, method and JGA/policy context; reconciled27 candidate records, adding26 source routes. Prepared second readout and proposed refinements. Client Word/PDF files unchanged; nothing sent.'})
write(cp,c)
dp=ROOT/'00-control/decisions.json';d=read(dp)
if not any(r['decision_id']=='DEC-007' for r in d['records']):
 d['records'].append({'decision_id':'DEC-007','date':DATE,'status':'working_design_recommendation',
  'decision':'Preserve the14core and8chapters; add pre-proposal and benefit-realisation probes, careful gap classification and a bounded historical/conditional outlook before external sharing.',
  'basis':'Second challenge readout and FND-007 to FND-011; no participant evidence or client approval implied.',
  'requires_client_approval':True})
write(dp,d)

# Preserve the existing client-file bytes and verify their previous hashes.
mp=ROOT/'06-client-checkpoints/week-one-v0.1/checkpoint-manifest.json';m=read(mp)
for entry in m['files']:
 assert hashlib.sha256((ROOT/entry['path']).read_bytes()).hexdigest()==entry['sha256']
m['sharing_status']='held_pending_second_review_refinements'
m['second_review']='03-report/SECOND-REVIEW-READOUT.md';write(mp,m)

sources=read(ROOT/'02-evidence/registers/sources.json')['records']
claims=read(ROOT/'02-evidence/registers/claims.json')['records']
captures=sum(bool(s.get('capture_path')) for s in sources)
sp=ROOT/'00-control/CURRENT-STATUS.md';status=sp.read_text()
status=status.replace('The register contains 35 sources including guidance/discovery material and 39 claims or guardrails. These are not 35 independent surveys or publication-approved findings. Fourteen source records have actual retained files with checked hashes.',
 f'After the second challenge the register contains {len(sources)} source routes and {len(claims)} claims or guardrails. These include guidance, product descriptions, cases and different report populations, not equivalent independent surveys. {captures} source records have actual retained files with checked hashes. R01 originally established35sources and39claims; the later additions are internal context, not publication approval.')
status=status.replace('WP02 / F01 is drafted for user review.', 'WP02 / F01 version0.1 is preserved and held pending targeted refinements from the second review.')
status=status.replace('After user review, present the scope, outline, questions and prospectus to Nick.',
 'Read the [second review](../03-report/SECOND-REVIEW-READOUT.md) and [proposed changes](../06-client-checkpoints/week-one-v0.1/SECOND-REVIEW-CHANGESET.md) first. Assess and apply targeted changes into a new preserved version before any sharing. The user explicitly requires no external sending yet. After user review, present the scope, outline, questions and prospectus to Nick only when authorised.')
status += '\n## Second review on28October2026\n\nHistorical, economic, methodological and JGA/policy lenses support the direction and identify refinements: pre-proposal needs, intended/measured benefits, service boundaries and conditional future signals. Eleven internal design findings are recorded. No new interview, commercial validation or client-file change occurred. Existing figure conflicts remain held.\n'
status=status.replace('version0.1','version 0.1').replace('established35sources and39claims','established 35 sources and 39 claims').replace('on28October2026','on 28 October 2026')
sp.write_text(status)

rp=ROOT/'README.md';t=rp.read_text()
t += '\n## Additional review before sharing\n\nThe user requested a further challenge before anything is sent. Read the [second review findings](03-report/SECOND-REVIEW-READOUT.md) and proposed changes. Version0.1 client files remain preserved; a new revision is needed before external sharing. No messages have been sent.\n'
rp.write_text(t.replace('Version0.1','Version 0.1'))

qa={'status':'passed_for_internal_second_review','date':DATE,'source_records':len(sources),'claim_records':len(claims),
 'retained_source_files':captures,'internal_design_findings':len(f['records']),'candidate_records_reconciled':len(mapping),
 'client_file_hashes_unchanged':True,'question_core_unchanged':True,'external_actions':[],
 'next':'Assess and apply targeted changes to version0.2; no sharing without user permission.'}
write(ROOT/'08-qa/SECOND-REVIEW-completion-check.json',qa)
print(json.dumps(qa,indent=2))
