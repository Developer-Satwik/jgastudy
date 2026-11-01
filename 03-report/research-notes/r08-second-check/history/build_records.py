from pathlib import Path
import json,hashlib
from pypdf import PdfReader

ROOT=Path(__file__).resolve().parents[4]
BASE=Path(__file__).resolve().parent
DATE='2026-10-29'
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rel(p):return str(p.relative_to(ROOT))
captures=BASE/'captures';captures.mkdir(exist_ok=True)
lfb=ROOT/'03-report/research-notes/r06-second-check/history/captures/H6S-S02.pdf'
sg=ROOT/'03-report/research-notes/r03/cases/scottish-government-aar-2025.pdf'
oldnote=ROOT/'03-report/research-notes/r06-second-check/history/captures/H6S-S01-selected-reader-notes.txt'
extracts=[]
for ident,p,pages in [('SRC-0206',lfb,[2,3,4]),('SRC-0134',sg,[43,46])]:
 reader=PdfReader(p);out=captures/(ident+'-selected-text.txt')
 out.write_text('Selected text extracted from retained original PDF. Not a complete export.\n'+''.join(f'\nPDF PAGE {n}\n'+reader.pages[n-1].extract_text()+'\n' for n in pages))
 extracts.append(dict(source_id=ident,path=rel(out),sha256=sha(out),kind='selected_pdf_text_extract',pdf_pages=pages))
reuses=[
 dict(source_id='SRC-0205',url='https://www.london.gov.uk/decisions/dmfd106-replacement-human-resources-and-payroll-solution',locator='Retained selected original-reader notes: executive summary;1.3,1.5,1.7,2.3',review_status='prior_inspected_selected_reader_notes_reused_fresh_route_blocked',review_extracts=[dict(path=rel(oldnote),sha256=sha(oldnote),kind='prior_selected_reader_notes_not_raw_original')],review_result='Earlier authorisation/options account retained in its2021 scope; compared with2025event account without treating either as later outcome evidence.',limitations='Fresh primary reader returned403; not a fresh full-page reinspection or original capture. Existing selected notes are paraphrases. One LFBprogramme, not a new employer. No amounts, optimality, complete option audit, contract execution or2026outcome.'),
 dict(source_id='SRC-0206',url='https://www.london-fire.gov.uk/media/jrqngpy0/lfc-25-098-replacement-hr-and-payroll-system-novemberr-2025-update-signed.pdf',locator='PDF2–4, especially1.1–1.5,2.1–2.8',capture_path=rel(lfb),capture_sha256=sha(lfb),review_extracts=[dict(path=x['path'],sha256=x['sha256'],kind=x['kind']) for x in extracts if x['source_id']=='SRC-0206'],review_status='retained_original_PDF_reinspected_and_primary_reader_revisited',visually_inspected_pdf_pages=[3,4],review_result='Report narrates prior decisions, sponsor change, the assessed release alternatives and reset measures within one programme; later explanations and dates need their own scope.',limitations='Report itself is an employer account with retrospective narrative, not raw minutes or an independently tested option/risk audit. No go-live outcome after prospective dates, payroll-only cost, source-wide run-count rule, current2026status or supplier fault/ranking.'),
 dict(source_id='SRC-0134',url='https://audit.scot/uploads/2025-10/aar_2425_scottish_government.pdf',locator='PDF/printed43para125;46paras137–141',capture_path=rel(sg),capture_sha256=sha(sg),review_extracts=[dict(path=x['path'],sha256=x['sha256'],kind=x['kind']) for x in extracts if x['source_id']=='SRC-0134'],review_status='retained_original_PDF_reinspected_and_primary_reader_revisited',visually_inspected_pdf_pages=[46],review_result='Later external audit describes separate migration signoff, conditional committee recommendations, final go-live decision with known issues and audit appraisal of particular processes.',limitations='One2024/25combined HR/finance programme, linked to SRC0067, not a new employer or current2026assurance. Audit reporting of minutes/management reasoning is not full independent validation of all contemporary beliefs or universal payroll accuracy. No percentages, defect threshold, staffing size, cost or generic acceptable-risk standard adopted.')
]
write(BASE/'source-candidates.json',dict(date=DATE,records=[],reused_canonical_sources=reuses,new_independent_datasets=0))
rows=[
 ('H8S-C01',['SRC-0205','SRC-0206'],'LFB’s earlier authorisation/options account and2025reset report describe different dated events and option constraints within one continuing programme. The later report narrates sponsor/plan changes and a release decision; it does not replace the earlier event with a later outcome.', 'dated_employer_history_and_record_boundary','SRC0205retainedlocators; SRC0206PDF2–4,1.1–1.5,2.1–2.8','Earlier source is retained selected reader notes and fresh route403. Later account is not raw complete decisionminutes. No hindsight-optimality judgment, new employer, current/later delivery, programme success/failure or monetary trend.'),
 ('H8S-C02',['SRC-0134'],'The Scottish Government audit describes migration signoff, conditional backing and a later final go-live approval that recorded known issues and assurances. Its subsequent audit appraisal is a different claim from the managers’ reported judgement at that decision.', 'retrospective_external_audit_of_staged_decision_context','PDF/printed43para125;46paras137–141','One shared HR/finance programme. No imported readiness threshold, universal minimum runs, current2026outcome, all-payroll accuracy, causal benefit or claim that acceptance proved every underlying assertion true.'),
 ('H8S-C03',['SRC-0205','SRC-0206','SRC-0134'],'When explaining an earlier decision in R08, distinguish the event and evidence/knowledge available then from the date, perspective and basis of a later retrospective explanation. Present-day alternatives or a later outcome must not silently backfill the earlier option or authority record.', 'researcher_selective_event_time_knowledge_condition','Cross-source analytical application to existingV02–V05 and Q006–Q013','A selective clarification of already time/scoped fields, not another view or compulsory question. Actual contemporaneous knowledge is not presumed; unknown stays unknown. No inference about what an individual ought to have known, negligence or decision optimality.'),
 ('H8S-C04',['SRC-0206','SRC-0134'],'The selected accounts record different release decisions with outstanding issues. R08 should preserve each account’s specific judgement and conditions without treating a decision to proceed or postpone as a reusable risk threshold or a proven-quality score.', 'researcher_no_hindsight_or_universal_release_rule','SRC0206PDF3–4,2.1–2.8; SRC0134PDF46paras137–141; explicit analytical application','These are not matched or equivalent risks or comparable severity measures. No claim that either decision was right/wrong, a guaranteed remedy, private-employer rule or causal link from a framework view to outcome.')
]
claims=[]
for ident,ids,text,kind,locator,limits in rows:
 claims.append(dict(candidate_id=ident,canonical_source_ids=ids,source_candidate_ids=[],claim_text=text,evidence_class=kind,locator=locator,limitations=limits,value=None,unit=None,denominator=None,population='Selected dated public programme record/audit and explicit researcher application, not an original practitioner or market sample',time_period='2021 and2025LFB records; Scottish2024/25audit of2024events. No observed2026series.',review_mode='Retained original PDFs and selected reader notes, source-specific limits retained; relevant PDF3–4/46rendered and visually inspected.'))
write(BASE/'claim-candidates.json',dict(date=DATE,records=claims))
files=[]
for p,kind in [(lfb,'retained_original_pdf'),(sg,'retained_original_pdf'),(oldnote,'selected_reader_notes')]:files.append(dict(path=rel(p),sha256=sha(p),kind=kind))
files+=extracts
for p in sorted(captures.glob('*.png')):files.append(dict(path=rel(p),sha256=sha(p),kind='rendered_pdf_page',visually_inspected=True))
write(BASE/'capture-manifest.json',dict(date=DATE,files=files,failed_rechecks=[dict(source_id='SRC-0205',url=reuses[0]['url'],http_status=403,path=None,sha256=None,evidence_status='fresh_access_failure_not_new_original_or_live_full_inspection')]))
write(BASE/'search-review-log.json',dict(date=DATE,purpose='R08historical/counterfactual challenge of event-time knowledge and retrospective explanation',queries=['Exact canonical LFB2021 authorisation route re-open','Exact canonical LFB2025reset PDF primaryreader and local original sections','Exact canonical Scottish2024/25annual audit primaryreader and local original sections'],source_ids=['SRC-0205','SRC-0206','SRC-0134'],read_pdf_pages={'SRC-0206':[2,3,4],'SRC-0134':[43,46]},visually_inspected_pdf_pages={'SRC-0206':[3,4],'SRC-0134':[46]},new_routes=0,scope_decision='Existing source set provides the needed contrast; no route added simply to repeat chronology or increase evidence count.',external_actions=[]))
checks=[]
def ck(v,label):checks.append(dict(check=label,passed=bool(v)));assert v,label
sources={x['source_id'] for x in json.loads((ROOT/'02-evidence/registers/sources.json').read_text())['records']}
for f in files:ck(sha(ROOT/f['path'])==f['sha256'],'Retained source/extract/render hash '+f['path'])
for c in claims:
 ck(set(c['canonical_source_ids'])<=sources,'Canonical source links '+c['candidate_id'])
 ck(c['value'] is None and c['unit'] is None and c['denominator'] is None,'No numerical estimate '+c['candidate_id'])
ck(len(reuses)==3 and not json.loads((BASE/'source-candidates.json').read_text())['records'],'Three explicit canonical reuses and zero new routes')
ck(len(claims)==4,'Four bounded history/design claims')
write(BASE/'verification.json',dict(date=DATE,status='passed_strand_scope_and_integrity',checks=checks,check_count=len(checks),original_practitioner_observations=0,numerical_estimates=0,external_actions=[]))
print(json.dumps({'status':'history_strand_complete','new_routes':0,'canonical_reuses':3,'claims':4,'hash_checked_files':len(files),'checks':len(checks)},indent=2))
