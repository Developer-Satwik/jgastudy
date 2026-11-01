from pathlib import Path
import json, hashlib, shutil
from docx import Document
from pypdf import PdfReader

root=Path(__file__).resolve().parents[1]
out=root/'06-client-checkpoints/week-one-v0.1'
qmap=json.loads((root/'01-method/question-map.json').read_text())
files=[]
for sub,name,count in [('plan','JGA Research Plan and Practitioner Questions',5),('prospectus','JGA Payroll Research Prospectus',2)]:
    rendered=out/'qa'/sub/(name+'.pdf')
    assert len(PdfReader(rendered).pages)==count
    assert len(list((out/'qa'/sub).glob('page-*.png')))==count
    shutil.copy2(rendered,out/(name+'.pdf'))
    doc=Document(out/(name+'.docx'))
    text='\n'.join(p.text for p in doc.paragraphs)
    assert '\u2014' not in text and '*' not in text
    if sub=='plan':
        assert all(r['wording'] in text for r in qmap['records'])
        assert 'report contribution' in text
    for suffix in ['.docx','.pdf']:
        f=out/(name+suffix)
        files.append({'path':str(f.relative_to(root)),'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),
                      'bytes':f.stat().st_size,'pages':count,'status':'draft_for_user_review'})

manifest={'schema_version':'1.0','version':'0.1','date':'2026-10-28',
          'status':'draft_for_user_review','external_sent':False,'client_approved':False,
          'files':files,'not_final_delivery':True}
(out/'checkpoint-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')

packages_path=root/'00-control/work-packages.json'
packages=json.loads(packages_path.read_text())
for r in packages['records']:
    if r['work_package_id']=='WP02':
        r.update(status='draft_ready_for_user_review',working_file='06-client-checkpoints/week-one-v0.1/REVIEW-NOTES.md',
          evidence_of_completion='Draft 5-page research plan, 2-page prospectus, 14-question map, internal routed guides, eight synthetic route checks, independent scope review and seven-page visual QA. User/client review and participant testing outstanding.',
          draft_prepared_on='2026-10-28')
packages_path.write_text(json.dumps(packages,indent=2)+'\n')

deliverable_path=root/'00-control/deliverables.json'
deliverables=json.loads(deliverable_path.read_text())
for r in deliverables['records']:
    if r['deliverable_id'] in ['D03','D07','D20']:
        r['status']='in_progress'
        r['current_draft_note']='WP02 version 0.1 is local for user review; no client approval or final handover. Final publication/templates depend on later work.'
deliverable_path.write_text(json.dumps(deliverables,indent=2)+'\n')

decisions_path=root/'00-control/decisions.json'
decisions=json.loads(decisions_path.read_text())
new={'decision_id':'DEC-006','date':'2026-10-28','status':'proposed_for_client_review',
     'decision':'Propose an eight-chapter report and fourteen core practitioner questions, including a no-case route and separate decision, option and delivery fields.',
     'basis':'R01 design findings, question review and eight internal synthetic routing checks; no participant validation yet.',
     'requires_client_approval':True}
if not any(r['decision_id']==new['decision_id'] for r in decisions['records']):decisions['records'].append(new)
decisions_path.write_text(json.dumps(decisions,indent=2)+'\n')

changes_path=root/'00-control/changes.json'
changes=json.loads(changes_path.read_text())
new={'change_id':'CHG-002','date':'2026-10-28','description':'Prepared WP02 review draft and editable client files; mapped fourteen core questions and separate Table guides; recorded synthetic routing and rendered-file checks. No external sending, client approval or fieldwork.'}
if not any(r.get('change_id')==new['change_id'] for r in changes['records']):changes['records'].append(new)
changes_path.write_text(json.dumps(changes,indent=2)+'\n')

qa={'date':'2026-10-28','status':'passed_for_local_draft','files':len(files),'rendered_pages':7,
    'visual_review':'All five plan pages and both prospectus pages inspected after final rendering. No clipping, spill, blank page or broken glyph observed.',
    'content_checks':['14 ordered core questions present in editable plan','Five-page plan and two-page prospectus',
      'No em dashes or literal asterisks in client document text','No invented findings, approvals, participant responses or calendar dates',
      'Separate six-to-ten practitioner target and up-to-four Table scope preserved','Independent review corrections incorporated'],
    'independent_review':'wp02_fieldwork_and_table_review; corrections to deferred evidence routing and usable report contribution for overlap incorporated.',
    'route_walkthrough':'08-qa/WP02-routing-walkthrough.json','participant_testing':False,'external_sent':False,'client_approved':False}
(root/'08-qa/WP02-completion-check.json').write_text(json.dumps(qa,indent=2)+'\n')
print(json.dumps({'status':'draft_ready_for_user_review','files':len(files),'pages':7},indent=2))
