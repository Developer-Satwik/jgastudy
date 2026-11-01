from pathlib import Path
import json,hashlib
ROOT=Path(__file__).resolve().parents[1];DATE='2026-10-29'
def read(p):return json.loads((ROOT/p).read_text())
def write(p,d):(ROOT/p).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
def sha(p):return hashlib.sha256((ROOT/p).read_bytes()).hexdigest()
review='08-qa/WP03-independent-review.md'
assert 'passed for internal collection-pack preparation' in (ROOT/review).read_text().lower()
r=read('08-qa/wp03-review/integration-checks.json');assert r['status']=='passed_for_internal_WP03_collection_pack_preparation' and all(x['passed'] for x in r['checks'])
base=read('08-qa/WP03-baseline-manifest.json')['files'];assert len(base)==111
for x in base:assert sha(x['path'])==x['sha256'],x['path']
qa=read('08-qa/WP03-routing-permission-checks.json');assert qa['status']=='passed_internal_WP03_pack_walkthrough_not_fieldwork' and qa['check_count']==199 and all(x['passed'] for x in qa['checks'])
for x in qa['pack_structured_hashes']:assert sha(x['path'])==x['sha256'],x['path']
assert sha(qa['source_design_path'])==qa['source_design_sha256']
pack=ROOT/'01-method/collection-pack-v0.1'
d=read('01-method/collection-pack-v0.1/REVIEW-DECISIONS.json');assert not d['collection_ready'] and all(x['status']=='not_confirmed' for x in d['release_decisions'])
assert d['working_contract']['return_or_delete_days']==30 and d['working_contract']['backup_deletion_days']==90
assert read('01-method/question-map.json')==read('01-method/question-map-v0.2.json')
for p in ['05-analysis/observations.json','05-analysis/charts.json','04-table/financial-inputs.json']:assert read(p)['records']==[]
for f in pack.glob('*.md'):
 t=f.read_text()
 if f.name=='START-HERE.md':
  assert '\n## Preparation review' not in t
  t+='\n## Preparation review\n\nIndependent integrated review and the internal count/permission walkthrough passed for this draft. The review does not activate collection, approve a tool/notice/transfer arrangement or provide a legal-compliance certification. The five release decisions remain open. See [preparation review](../../08-qa/WP03-independent-review.md) and [completion record](../../08-qa/WP03-completion-check.json). Nothing sent or collected.\n'
  f.write_text(t)
changes=read('00-control/changes.json')
if not any(x['change_id']=='CHG-020' for x in changes['records']):changes['records'].append(dict(change_id='CHG-020',date=DATE,type='WP03 collection/permission pack preparation',description='Eight-file local review pack: operatorrunbook, unsentintro/invitation, participantinfo/choice drafts, blankrecordschemas, counting/routingpolicy and5groupedrelease decisions. Workingagreementon-behalfroles/30-90closureterms preserved, actualtool/storage/notice/access/lawfulinstructions/requiredtransferroute unconfirmed. Eightconstructedcountapplications+3releasecases passed199rootchecks; independent integrated review and111preservationhashes passed. Employer-namingpermission clarified from indirectidentification. No14Q/core/client/sourceclaimfindings changes, actualparticipantdata, fieldworktoolactivation, contact or sending.'))
write('00-control/changes.json',changes)
wp=read('00-control/work-packages.json');wp['updated_on']=DATE;wp['active_work_package']='WP03';wp['next_action']='WP03 local collection pack independently reviewed, ready for user/client decisions. No collection activated: confirm focus/introduction/timing, actual dataflow/tools/access, JGA notice/lawfulinstructions/contact route, specific output/use permissions and exact message release. Public WP12 Table comparable research can proceed independently; no outreach or participant data in workspace.'
for x in wp['records']:
 if x['work_package_id']=='WP03':x.update(status='prepared_for_user_client_review_collection_not_activated',working_file='01-method/collection-pack-v0.1/START-HERE.md',prepared_on=DATE,collection_ready=False,evidence_of_completion='Eight-file blank/local review pack; actualgeneratedagreementsection12workingroles/closureterms and5focusedprimaryguidancepages reviewed. Eightconstructedcountscenarios+3permission/readinesscases/199rootchecks, independentintegratedreview and111prior/core/client/canonicalhashes. Allrealcounts/records0,14questions unchanged. Actualfocus/notice/instructions/tools/access/requiredtransferandrelease decisions remainopen; no fieldwork/outreach.')
write('00-control/work-packages.json',wp)
p=ROOT/'00-control/CURRENT-STATUS.md';t=p.read_text();bullet='- WP03 collection pack prepared and independently reviewed: operator process, unsent introduction/invitation, participant information/choice drafts, blank restricted-record templates, count/routing policy and five grouped release decisions. Working contract roles and30/90-dayclosureterms preserved. Eight constructed count applications plus three permission/readiness cases passed199rootchecks;111prior/core/client/canonicalhashes preserved. No actual participant data, collection activation or sending.\n'
if bullet not in t:t=t.replace('\nFor the current synthesis','\n'+bullet+'\nFor the current synthesis')
marker='\n## Still open';idx=t.index(marker)
t=t[:idx]+'''\n## Collection preparation now available

Use the [WP03 collection pack](../01-method/collection-pack-v0.1/START-HERE.md) for review. Its [review decisions](../01-method/collection-pack-v0.1/REVIEW-DECISIONS.json) preserve the agreement’s working JGA-controller/Riseklix-processor on-behalf arrangement and return/delete30days/backups90days terms, while distinguishing actual instructions and implementation still needed. The executed copy remains unretrieved. No new lawful basis, secure store, tool, transfer mechanism, notice or participant permission is presumed.

The proposed low-burden route uses manual notes or written input, without recording or external AI/transcription by default, only after actual arrangements are approved. Six to ten distinct verified eligible report contributors and up to four substantive Table events remain separate units; permissioned substantive overlap counts each report person once. No-case input can be useful, all probes remain selective and publication clearance is separate from analysis usability.

The five grouped release decisions concern focus/introduction/timing, actual dataflow/access, JGA notice/instructions/contact route, publication/optional uses, and user permission for the exact message/route. The pack is prepared, not fieldwork-ready. Current QA is `08-qa/WP03-completion-check.json`. Public Table comparable research under WP12 can continue while these decisions are settled; finalWP15 still requires actual coded original contributions.
'''+t[idx:]
t=t.replace('and prepare WP03 collection/permission arrangements, necessary checkpoint revisions or WP12 public comparison research.','and review the prepared WP03 collection pack, make necessary checkpoint revisions or begin WP12 public comparison research.')
p.write_text(t)
p=ROOT/'README.md';t=p.read_text();marker='\n## Additional review';idx=t.index(marker)
t=t[:idx]+'''\n## Collection pack prepared

The [WP03 collection pack](01-method/collection-pack-v0.1/START-HERE.md) contains the operating process, unsent message drafts, participant information and separate-use choices, blank record templates and counting policy. Independent integrated review and199root constructed count/permission checks passed;111prior/client/core/canonical files remain preserved. No actual participants, permissions or contribution records were collected.

Actual collection stays inactive pending the five [release decisions](01-method/collection-pack-v0.1/REVIEW-DECISIONS.json). Working contract roles and30/90-dayclosureterms are carried through, not replaced; specific tools/access/instructions/notice/requiredtransferroute are not approved by the pack. Next public work can be WP12 Table comparables while user/client collection arrangements are settled. Current QA is `08-qa/WP03-completion-check.json`; nothing sent.
'''+t[idx:];p.write_text(t)
p=ROOT/'05-analysis/CONTRADICTIONS-AND-GAPS.md';t=p.read_text();marker='\n## WP03 collection preparation controls';assert marker not in t
t+='''
## WP03 collection preparation controls

- Working agreementsection12already assignsJGAcontroller/Riseklixprocessor foron-behalfprocessing, ownbusinessrecordsseparate, materialrolechangesdocumented; return/delete30days/backups90days withtrigger/exceptions. Actual notice/instructions/tools/access/requiredtransferroute are separate pending decisions; executedcopyunretrieved.
- Five focused operatingguidance HTMLpages are recorded inWP03data source-review/capturemanifest, not newpayrollmarketdatasets/findings. ICO23Oct2026consentupdate noted; roleguideunderreview and privacyinformationpagelegacyEUtransferrow not copied ascurrentUKmechanism; MRSlandingonlynotfullPDF.
- Voluntaryparticipation/notes versus recording, exactquotes, person/employeridentification, councilrecognition, limitedclarification, futurecontact/reuse andTableinterest are distinct; blankisnotyes. Namingpermission doesnotpreventindirectidentification or authorise employer naming.
- OnePpersonreference acrossmodes/streams; actualeligibleusablepermittedreportinput counts once; no recentcaseorall14answerthresholdrequired. Up4substantiveTableevents count events, notroles; combined/repeatedsessions explicit. Publicationitemclearance andquestionspecificbases separate.
- Blanktemplates are forapprovedrestrictedstorage only, notpersonaldata entry inthisworkspace. Pseudonymisation/UKhosting/toolavailability are notautomaticanonymisation or approval. No rightswithdrawalcutoff/incentive/duration/recallpromise invented.
- Root8constructedcountapplications+3releasecases passed199checks; originaldesignsremainunexecuted asdesignrecords. Independent integrated preparationreview and111preservationhashes passed; actualrecords/counters0. Notfieldwork/usertesting/legalcertification or activatedcollection.
- Fivegroupedrelease decisions remainopen. Core14Q/clientfiles/sourceclaimfindingregisters unchanged; finalWP15/practitionerinputs andTablevalidation remainopen. Nothing sent/collected/uploaded.
''';p.write_text(t)
sources=read('02-evidence/registers/sources.json')['records'];claims=read('02-evidence/registers/claims.json')['records'];findings=read('05-analysis/findings.json')['records']
artifacts=[str(p.relative_to(ROOT)) for p in sorted(pack.glob('*')) if p.is_file()]+[review,'08-qa/wp03-review/integration-checks.json','08-qa/WP03-routing-permission-checks.json','01-method/research-notes/wp03/data/DATA-ARRANGEMENT-DECISIONS.md','01-method/research-notes/wp03/data/source-review.json','01-method/research-notes/wp03/data/capture-manifest.json','01-method/research-notes/wp03/routes/COLLECTION-ROUTES.md','01-method/research-notes/wp03/routes/route-requirements.json','01-method/research-notes/wp03/routes/constructed-route-tests.json','01-method/research-notes/wp03/wording/PARTICIPANT-WORDING.md','01-method/research-notes/wp03/wording/wording-requirements.json']
result=dict(date=DATE,status='passed_for_internal_WP03_collection_pack_preparation_only',pack_version='0.1',review_basis='Independent integrated operational-draft review and root constructed count/permission applications. Not legal/tool-security certification, participant testing or collection activation.',pack_files=8,review_decisions=5,contract_role_terms_preserved=True,contract_return_delete_days=30,contract_backup_days=90,executed_copy_retrieved=False,source_records=len(sources),claim_records=len(claims),internal_findings=len(findings),new_canonical_sources_or_claims=0,core_questions=14,core_questions_unchanged=True,constructed_count_cases=8,constructed_release_cases=3,root_checks_passed=199,independent_integration_checks_passed=len(r['checks']),preserved_baseline_records=111,actual_participants=0,actual_completed_contributions=0,actual_Table_events=0,actual_permissions_obtained=0,collection_ready=False,tools_or_recording_activated=False,external_actions=[],artifacts=[dict(path=p,sha256=sha(p)) for p in artifacts])
write('08-qa/WP03-completion-check.json',result)
print(json.dumps({k:v for k,v in result.items() if k!='artifacts'},indent=2))
