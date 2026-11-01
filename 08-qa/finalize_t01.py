from pathlib import Path
import json,hashlib,shutil
R=Path(__file__).resolve().parents[1];D='2026-10-29'
def read(p):return json.loads((R/p).read_text())
def write(p,d):(R/p).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
rev=read('08-qa/t01-review/integration-checks.json');assert not rev['open_substantive_issues'] and all(x['passed'] for x in rev['checks'])
reviewed=[];dest=R/'04-table/research-notes/t01/reviewed-before-status';dest.mkdir(exist_ok=True)
for r in rev['reviewed_artifacts']:
 p=R/r['path'];h=hashlib.sha256(p.read_bytes()).hexdigest();assert h==r['sha256'],r['path']
 if r['path'] in ['04-table/T01-model-map.json','04-table/T02-proposition-hypotheses.json']:
  out=dest/p.name;shutil.copy2(p,out);reviewed.append(dict(original_path=r['path'],snapshot_path=str(out.relative_to(R)),sha256=h))
write('04-table/research-notes/t01/reviewed-before-status/manifest.json',dict(date=D,records=reviewed))
for p,status in [('04-table/T01-model-map.json','desktop_comparison_reviewed_for_internal_use'),('04-table/T02-proposition-hypotheses.json','internally_reviewed_draft_not_buyer_validated')]:
 x=read(p);x['status']=status;x['review_basis']='08-qa/T01-independent-review.md and t01-review/integration-checks.json; original fieldwork, commercial validation and final-use review remain pending.';write(p,x)
x=read('00-control/work-packages.json');x['updated_on']=D;x['active_work_package']='WP12'
for p in x['records']:
 if p['work_package_id']=='WP12':p.update(status='T01_desktop_reviewed_T02_propositions_draft',working_file='04-table/T01-DESKTOP-READOUT.md',evidence_of_completion=['08-qa/T01-record-map.json','08-qa/T01-independent-review.md','04-table/T01-model-map.json','04-table/T02-proposition-hypotheses.json'],T01_desktop_reviewed=True,T02_buyer_validated=False,T03_conversations_complete=False)
x['next_action']='Refine T02 specific research-use, founding-partner and practitioner propositions against the six reviewed mechanisms and public alternatives; preserve separate rights/units. Actual T03 contributions await existing client/user/collection decisions. T04/T05 product economics and final report practitioner integration remain open; no external sending.'
write('00-control/work-packages.json',x)
x=read('00-control/changes.json');assert not any(r['change_id']=='CHG-021' for r in x['records'])
x['records'].append(dict(change_id='CHG-021',date=D,type='T01 six-model desktop comparison and T02 hypothesis preparation',description='Six distinct selected public business mechanisms;26 primary source routes and52 bounded claim/guardrail records appended,26 original HTML captures plus explicit prior-report/catalogue reuses. Detailed reviews, matrix, canonical model map, public-alternatives analysis and4untested propositions retained. Independent417preliminary/1110integrated checks passed;120baselinefiles, old355claims/191sourcebase/81findings preserved. Wording refined: public offer is not viable economics; research/access can be a separately defined combination without default data/meeting rights. No fieldwork, JGA pricing/financial inputs, new core questions, sponsor/venue enquiries, purchases, final publication or external sends.'))
write('00-control/changes.json',x)
x=read('00-control/decisions.json');x['records'].append(dict(decision_id='DEC-008',date=D,status='internal_design_method',decision='For Table feasibility, distinguish the research-use licence, funding-partner benefits and practitioner participation; assess event value incrementally and permit a separately defined transparent research/access combination without default private-data or meeting rights.',basis='T01 six public mechanisms and independent desktop review; four T02 hypotheses remain untested. No launch, price, partner or rights terms adopted.',requires_client_approval=False));write('00-control/decisions.json',x)
p=R/'00-control/CURRENT-STATUS.md';s=p.read_text()
s=s.replace('The register contains 191 source routes, 355 claims/guardrails and 81 internal findings. 120 source records retain originals in primary capture fields;', 'At the R08 checkpoint the register contained 191 source routes, 355 claims/guardrails and 81 internal findings. 120 source records retained originals in primary capture fields;')
s=s.replace('Next prepare collection/permission arrangements under WP03 and the Table comparison research under WP12. Public desktop work continues independently of introductions.', 'WP03 collection preparation is now reviewed and inactive. T01 public comparison research under WP12 is reviewed; next refine the T02 propositions while actual collection arrangements remain open.')
s=s.replace('Public Table comparable research under WP12 can continue while these decisions are settled;', 'T01 public Table comparisons are now reviewed and T02 propositions remain draft while these decisions are settled;')
s=s.replace("Table's six final model reviews and buyer/member conversations;", "Table buyer/member validation, final model-use checks and commercial definitions;")
s=s.replace('review the prepared WP03 collection pack, make necessary checkpoint revisions or begin WP12 public comparison research.', 'review the prepared WP03 collection pack and reviewed T01 comparisons, make necessary checkpoint revisions and refine T02 propositions. Do not repeat the six-model desk review unless new evidence or a targeted challenge warrants it.')
insert='''## Table comparison now reviewed

The [T01 readout](../04-table/T01-DESKTOP-READOUT.md) integrates six distinct mechanisms: sponsored research, licensed intelligence, payroll support membership, research community, senior payroll forum and sponsor-funded executive events. Direct payroll and adjacent HR/L&D offers are explicitly separated. Their commercial units, participant value, public rights, operating work and limits are retained in six detailed reviews and [the matrix](../04-table/T01-COMPARABLE-MATRIX.md).

The canonical register now contains **217 source routes, 407 claims/guardrails and 81 preserved internal findings**. 146 source records retain originals in primary capture fields. T01 appended26 routes/52 bounded records;26 new raw HTML pages, separate extracts,3 PDF page renders and explicit canonical/catalogue reuses are retained. No existing claim or finding was rewritten. Independent source and integrated review passed, with120baselinefiles preserved. Current QA is `08-qa/T01-completion-check.json`.

The [T02 propositions](../04-table/T02-PROPOSITION-WORKING-NOTE.md) are four untested hypotheses, not buyer/member validation or agreed product terms. Research use, partner funding and practitioner participation remain distinct; an event is a possible incremental mechanism. No comparator price is a JGA financial input. The UK pilot, annual programme, partner demand, final rights and cash/resource economics remain undecided. Next refine T02, then collect actual authorised input through the existing arrangements when ready. T03 and T04/T05 are not completed.

'''
s=s.replace('## Still open\n',insert+'## Still open\n');p.write_text(s)
p=R/'README.md';s=p.read_text();s=s.replace('Next prepare collection/permission arrangements under WP03 and public Table comparisons under WP12;', 'WP03 collection preparation and T01 public comparisons are now reviewed; next refine T02 propositions;')
s=s.replace('The register contains 191 source routes, 355 claims/guardrails and 81 internal findings. 120 source records retain originals in primary capture fields;', 'At R08 the register contained 191 source routes, 355 claims/guardrails and 81 internal findings. 120 source records retained originals in primary capture fields;')
s=s.replace('Next public work can be WP12 Table comparables while user/client collection arrangements are settled.', 'T01 public comparisons are now reviewed; T02 proposition refinement can continue while user/client collection arrangements are settled.')
s+='''
## Table comparisons reviewed

The [T01 readout](04-table/T01-DESKTOP-READOUT.md) and [comparison matrix](04-table/T01-COMPARABLE-MATRIX.md) cover six selected mechanisms, with source-linked detail and clear audience/price/rights limits. The register now has217sources/407claims/81preserved internal findings and146primary original captures. Independent integrated review passed;120earlier/core/client/collection files remain unchanged.

Four [T02 hypotheses](04-table/T02-PROPOSITION-WORKING-NOTE.md) specify possible research-use, partner and member value and the event's incremental role. They are untested, with no actual buyer conversations, JGA prices, financial inputs or launch decision. T03validation and T04/T05economics remain open. Nothing sent. Current QA: `08-qa/T01-completion-check.json`.
''';p.write_text(s)
p=R/'05-analysis/CONTRADICTIONS-AND-GAPS.md';s=p.read_text()+'''

## T01 comparable-model boundaries, 29 October 2026

- Six selected business mechanisms, not the earlier six recruitment firms, a competitor league table or exhaustive market census. Direct payroll and adjacent HR/L&D audiences are distinguished.
- HR.com's dated Custom Research help page and separate2025 sponsor-branded payroll output do not establish the exact sponsor contract. ISG2025 software comparisons do not validate a small council benchmark.
- The Payroll Centre Corporate list price is GBP1,122 per organisation/year with VAT excluded unless stated otherwise; support/training differs from a research licence. No JGA price input is inferred. CIPP current tariff remains unconfirmed; its tier footnotes explicitly date validity to14June2026.
- Conference Board Center research membership and vetted annual-fee individual Council seats are distinct; website submissions and confidential Council meetings have different terms. No automatic research/publication right follows.
- CPO free quarterly editorial subscription is distinct from forum access/fee; provider-side leaders appear, so employer-only/vendor-free status is not assumed. General platform rules are not confidential interview terms.
- iVentiv L&D London17–18November2026 is forthcoming in this review. Advertised contacts/meetings are explicit commercial-access inventory, not default research-partner rights. Research/access may be a separately defined combination. Conflicting generic invoice intervals cannot supply cash timing.
- Public offered architecture is not proved commercial viability.52 new bounded records do not add demand/retention/outcome estimates or original participant findings. T02hypotheses, actualT03input, final rights and T04/T05cash/resource model remain open. No external action occurred.
''';p.write_text(s)
print('T01 status, review snapshots and control updates saved')
