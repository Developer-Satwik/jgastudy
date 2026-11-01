from pathlib import Path
import json, hashlib

ROOT=Path(__file__).resolve().parents[1]
DATE='2026-10-28'
if (ROOT/'03-report/R02-SECOND-CHECK-READOUT.md').exists():
    raise SystemExit('Historical first-pass helper: R02 second challenge is now applied. Use current records; do not overwrite the revised synthesis.')
def read(p):return json.loads(p.read_text())
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')

module=ROOT/'03-report/modules/R02-operational-needs-and-service-gaps.md'
snapshot=ROOT/'03-report/research-notes/r02-operating-needs/MODULE-INITIAL.txt'
old_snapshot=snapshot.with_suffix('.md')
if old_snapshot.exists() and not snapshot.exists():old_snapshot.rename(snapshot)
if not snapshot.exists():snapshot.write_bytes(module.read_bytes())
module.write_text('''# R02 Operational needs and service gaps

Desktop evidence assessment completed • 28 October 2026

Original practitioner integration and final publication checks remain open. This is not a completed client chapter or a representative study of unmet needs.

## Decision this informs

Determine which operating needs and service gaps have meaningful consequences, what evidence supports them, and what desired outcome should guide the later assessment of a response.

## Questions covered

1. Which tasks, handoffs, service expectations and consequences appear in the inspected evidence?
2. What do query, accuracy, clarity, staffing and service measures actually measure?
3. When might a gap concern capability, fit, affordability/value, data, capacity, ownership or service scope?
4. What functioning arrangements and contrary evidence challenge a universal failure or replacement narrative?
5. What can desk evidence establish, and what must permissioned practitioner cases still supply?

## Boundaries and definitions

The proposed original cohort remains UK-relevant senior employer-side professionals, pending Nick's review. Existing in-house/provider studies, multinational peer samples, employee panels, official guidance, supplier scope documents and local-authority cases have different units. They are not pooled or presented as JGA's cohort. No participant data was collected.

Unmet need means an outcome inadequately served in a stated context. A perceived need does not prove absence of a market capability. A service exclusion is not automatically non-performance, and correct bank payment does not establish correct reporting, reconciled records or understandable service.

## Evidence and appraisal

The [desktop readout](../R02-DESKTOP-READOUT.md) explains conclusions and reader implications. The [needs and consequences matrix](../R02-NEEDS-CONSEQUENCES-MATRIX.md) links nine areas to canonical claim IDs and proposed case indicators.

The initial CIPP, PayrollOrg and SD Worx review was deepened through capacity/control, service-boundary and concrete-consequence assessments:

- CIPP originals, SRC-0020–0022: task mixes, complexity caveat, KPI definitions and included/excluded tasks. Report-specific bases remain unestablished.
- PayrollOrg and SD Worx, SRC-0071 and SRC-0033: input/performance measures and positive employee agreement, preserving distinct populations and bases.
- Deloitte/ADP, SRC-0040 and SRC-0064: peer-group task/support/target definitions and large-employer priorities. No universal staffing or service benchmark.
- Public service documents, SRC-0094–0097: declared scope, employer duties, escalation, data/reporting access and dated assurance tiers. No achieved-performance inference.
- Oldham/Comhairle, SRC-0098–0099: correction/recovery, handoff/control issues and response/continuity evidence. Bounded public-sector examples.
- Official guidance/bulletin, SRC-0100–0103 and SRC-0083: reporting identity, correction, records, employee consequences and communication. Mechanisms and responsibilities, not prevalence.

Extraction provenance is indexed in `08-qa/R02-deepening-record-map.json`. Existing originals were not counted as new independent surveys. The ADP summary is a same-dataset alias.

## Synthesis and practical implications

The evidence supports examining information intake/approval, correction/recovery, statutory reporting, employee explanation/resolution, records/reconciliation, sustainable capacity, service boundaries and useful reporting. It does not rank these for the intended cohort or assign typical financial magnitudes.

For payroll leaders, define the outcome, handoff, owner and actual evidence before choosing a response. For suppliers, distinguish absent capability from package scope, readiness, ownership and delivery. For JGA, explain the chain from need to consequence and desired result, allowing different responses. R03 will assess technology and operating-model trade-offs.

## Counterevidence and alternatives

Positive employee agreement, maintained service and scoped Reasonable Assurance coexist with improvement needs. Supplier documents show some assurance/control capability is already offered. Staffing ratio is not adjusted workload, SLA is not achieved resolution, and KPI selection is not incident rate.

Two additional Deloitte numerical presentations are held. Existing Moorepay, Finity and HR.com holds remain. No figure was corrected or pooled to support a preferred conclusion. Administrative cost, lost productivity and retention ROI cannot be inferred from payment principal or an unused internal charging policy.

## Original input still needed

Use the proposed core and selective probes to establish task/recurrence, consequence, workaround, evidence, responsible boundary and desired improvement. Keep never-raised needs, older context and eligible recent cases distinct. Seek adequate arrangements and contrasting outcomes. No additional survey or mandatory question bank is introduced.

## Completion check and handoff

The desktop questions have contextual support, explicit gaps and material counterevidence. Independent synthesis review found no substantive correction needed. The module can inform R03 without another broad discovery round. This closes desktop research, not practitioner collection, publication approval or every market hypothesis.

Next: R03 technology, integration and operating-model trade-offs. No client sending or collection is authorised by completing this module.
''')

for rel in ['03-report/R02-DESKTOP-READOUT.md']:
    p=ROOT/rel;t=p.read_text()
    for a,b in [('May2025','May 2025'),('October2025','October 2025'),('original6–10','original 6–10'),('sections3–5','sections 3–5')]:t=t.replace(a,b)
    p.write_text(t)
initial=ROOT/'03-report/research-notes/r02-operating-needs/R02-OPERATING-NEEDS.md'
initial.write_text(initial.read_text().replace('Within the approved core and selective probes','Within the proposed core and selective probes'))

findings_path=ROOT/'05-analysis/findings.json';findings=read(findings_path)
rows=[
 ('FND-012','Information handoffs and approval can create consequential rework before or around processing.',
  ['CLM-0178','CLM-0164','CLM-0158'],'Source attribution and bounded audits support investigating the mechanism; no national causal rate is estimated.',
  'Locate task, input, owner, cutoff and known downstream consequence before diagnosing a product gap.'),
 ('FND-013','Service response targets, full resolution and corrected employee outcome are different measures.',
  ['CLM-0170','CLM-0165'],'Declared scope and self-reported target evidence do not demonstrate achieved service performance.',
  'Separate acknowledgement, updates, resolution and the affected outcome in case analysis.'),
 ('FND-014','A payroll service gap may concern scope or retained duties rather than an absent market capability.',
  ['CLM-0169','CLM-0171','CLM-0172','CLM-0173'],'Supplier examples establish published scope only; the older Phase3 definition is dated explicitly.',
  'Establish entitlement, ownership and actual case performance; do not claim all providers lack a capability.'),
 ('FND-015','Payroll capacity needs a task, complexity and support boundary rather than a headcount ratio alone.',
  ['CLM-0160','CLM-0162','CLM-0163'],'Different populations and task definitions prevent a universal staffing norm or inferred understaffing.',
  'Include queries, controls, projects and technical/retained work when examining capacity and desired improvement.'),
 ('FND-016','Payment, statutory reporting, records and employee explanation are separate protected outcomes.',
  ['CLM-0180','CLM-0181','CLM-0182','CLM-0183'],'Official guidance identifies responsibilities and possible consequences, not their market incidence.',
  'Investigate each outcome explicitly where relevant and avoid turning payslip confusion into an error rate.'),
 ('FND-017','Operating continuity and improvement needs can coexist.',
  ['CLM-0177','CLM-0159'],'A bounded audit and unrelated employee agreement data support balanced inquiry, not a pooled performance claim.',
  'Preserve functioning controls and positive cases while checking the effort, cover and unresolved conditions behind continuity.'),
 ('FND-018','Remedial payment principal and gross recoverable overpayments are not measured administrative cost or written-off loss.',
  ['CLM-0176','CLM-0174'],'The cases do not establish a transferable payroll correction cost, retention effect or cash ROI.',
  'Keep principal, recovery, outstanding amounts, write-offs, staff effort and actual spending separate.')]
for ident,statement,claim_ids,limits,action in rows:
    if any(f['finding_id']==ident for f in findings['records']):continue
    findings['records'].append({'finding_id':ident,'topic_ids':['R02'],'statement':statement,'supporting_claim_ids':claim_ids,
      'contradicting_claim_ids':[],'participant_observation_ids':[],'interpretation':limits,'decision_implication':action,
      'confidence_rationale':'Desktop synthesis of inspected originals with source-specific limits and contrary/positive evidence; not original fieldwork or population estimation.',
      'outstanding_questions':['Actual priorities, recurrence, materiality and observed results in permissioned practitioner cases.'],
      'publication_status':'internal_research_design','reviewed_on':DATE})
findings['status']='R01_second_review_and_R02_internal_synthesis';write(findings_path,findings)

assert (ROOT/'08-qa/R02-independent-review.md').is_file()
for version in ['0.1','0.2']:
    manifest=read(ROOT/f'06-client-checkpoints/week-one-v{version}/checkpoint-manifest.json')
    for f in manifest['files']:
        assert hashlib.sha256((ROOT/f['path']).read_bytes()).hexdigest()==f['sha256']

wp=ROOT/'00-control/work-packages.json';w=read(wp)
w['active_work_package']='WP05';w['pending_review_work_packages']=['WP02'];w['next_action']='Begin R03 desktop research; no external sending.'
for p in w['records']:
    if p['work_package_id']=='WP04':
        p.update(status='completed_desktop_research_practitioner_integration_pending',desktop_completed_on=DATE,
          evidence_of_completion='Capacity/control, service boundaries, two employer cases and official consequence mechanisms; nine-area matrix, evidence/holds, independent synthesis review and file-integrity checks. Practitioner integration and final publication approval remain open.')
    elif p['work_package_id']=='WP05':p['status']='ready_for_desktop_research'
write(wp,w)
cp=ROOT/'00-control/changes.json';c=read(cp)
if not any(r.get('change_id')=='CHG-006' for r in c['records']):
    c['records'].append({'change_id':'CHG-006','date':DATE,'type':'R02 desktop research completion',
      'description':'Deepened capacity/control, service boundary and business consequences. Reconciled ten new source routes and twenty-four additional claim/guardrail records; retained numeric holds, wrote nine-area matrix/readout, and preserved client-file hashes. No participant data or external sending.'})
write(cp,c)

gaps=ROOT/'05-analysis/CONTRADICTIONS-AND-GAPS.md';t=gaps.read_text()
if 'Deloitte support-query and technical-support presentations' not in t:
    t+='\n## Additional R02 numerical holds\n\n- Deloitte support-query and technical-support presentations: CLM-0167 and CLM-0168. Displayed query counts/footnoted base and combined/subgroup figures do not reconcile transparently. Preserve the source; do not renormalise, infer a missing category or use disputed numbers in a headline. Qualitative scope distinctions remain useful.\n- Public employer advances and overpayments: principal, recoverable balances and an unused internal charging policy are not an administrative cost or loss benchmark.\n- Service response/SLA targets, survey KPI adoption and employee agreement remain distinct from achieved resolution, incident rates and audited outcomes.\n'
    gaps.write_text(t)
print(json.dumps({'R02_desktop':'complete_pending_original_input_and_publication_checks','internal_findings':len(findings['records']),'client_file_hashes':'unchanged','next_module':'R03'},indent=2))
