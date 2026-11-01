from pathlib import Path
import json, hashlib, shutil
from docx import Document
from pypdf import PdfReader

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'06-client-checkpoints/week-one-v0.2'
def read(p):return json.loads(p.read_text())
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
old=read(ROOT/'06-client-checkpoints/week-one-v0.1/checkpoint-manifest.json')
for entry in old['files']:
    assert hashlib.sha256((ROOT/entry['path']).read_bytes()).hexdigest()==entry['sha256']
questions=read(ROOT/'01-method/question-map.json')
assert questions==read(ROOT/'01-method/question-map-v0.2.json')
assert questions['version']=='0.2'
routes=read(ROOT/'08-qa/WP02-v0.2-routing-walkthrough.json')
assert routes['status']=='passed' and routes['test_count']==19
assert (ROOT/'08-qa/v02-independent-review/EXACT-V02-REVIEW.md').is_file()
files=[]
for sub,name,pages in [('plan','JGA Research Plan and Practitioner Questions',5),('prospectus','JGA Payroll Research Prospectus',2)]:
    rendered=OUT/'qa'/sub/(name+'.pdf')
    assert len(PdfReader(rendered).pages)==pages
    assert len(list((OUT/'qa'/sub).glob('page-*.png')))==pages
    doc=Document(OUT/(name+'.docx'))
    text='\n'.join(p.text for p in doc.paragraphs)
    assert '\u2014' not in text and '*' not in text
    if sub=='plan':assert all(q['wording'] in text for q in questions['records'])
    shutil.copy2(rendered,OUT/(name+'.pdf'))
    for ext in ['.pdf','.docx']:
        p=OUT/(name+ext)
        files.append({'path':str(p.relative_to(ROOT)),'pages':pages,'bytes':p.stat().st_size,
                      'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'status':'draft_for_user_review'})
write(OUT/'checkpoint-manifest.json',{'schema_version':'1.0','version':'0.2','date':'2026-10-28',
    'status':'draft_for_user_review','sharing_status':'Not authorised for external sending',
    'external_sent':False,'client_approved':False,'participant_tested':False,'files':files,'not_final_delivery':True})

wp=ROOT/'00-control/work-packages.json';w=read(wp)
for p in w['records']:
    if p['work_package_id']=='WP02':
        p.update(status='v02_prepared_for_user_review',working_file='06-client-checkpoints/week-one-v0.2/REVIEW-NOTES.md',
          sharing_status='Local only; user permission required before sending.',
          evidence_of_completion='Revised five-page plan and two-page prospectus; fourteen unchanged core questions, refined probes/routes, nineteen synthetic checks, independent exact-content review and seven rendered pages checked. Client review and human timing/testing outstanding.')
write(wp,w)
dp=ROOT/'00-control/deliverables.json';d=read(dp)
for p in d['records']:
    if p['deliverable_id'] in ['D03','D07','D20']:
        p['current_draft_note']='WP02 version 0.2 locally prepared after second review; no client approval, participant collection or final handover. Final files depend on later work.'
write(dp,d)
cp=ROOT/'00-control/changes.json';c=read(cp)
if not any(p.get('change_id')=='CHG-004' for p in c['records']):
    c['records'].append({'change_id':'CHG-004','date':'2026-10-28','type':'Checkpoint refinement within existing scope',
        'description':'Applied second-review refinements into version0.2, preserving version0.1 client-file hashes and core wording. Revised routes/probes, guide and clientpack; structural and rendered checks passed; nothing sent.'})
write(cp,c)
qa={'date':'2026-10-28','status':'passed_for_local_v02_draft','client_files':4,'rendered_pages':7,
    'independent_review':'08-qa/v02-independent-review/EXACT-V02-REVIEW.md','synthetic_cases':19,
    'old_client_file_hashes_preserved':True,'core_wording_preserved':True,'human_testing':False,
    'external_sent':False,'client_approved':False,
    'visual_review':'All five plan pages and both prospectus pages inspected after rendering; no spill, clipping, missing glyphs or broken hierarchy observed.'}
write(ROOT/'08-qa/WP02-v0.2-completion-check.json',qa)
print(json.dumps(qa,indent=2))
