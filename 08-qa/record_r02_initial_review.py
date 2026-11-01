from pathlib import Path
import json, hashlib

ROOT=Path(__file__).resolve().parents[1]
folder=ROOT/'03-report/research-notes/r02-operating-needs'
def read(p):return json.loads(p.read_text())
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
claims_path=ROOT/'02-evidence/registers/claims.json';claims=read(claims_path)
sources=read(ROOT/'02-evidence/registers/sources.json')['records'];source_ids={r['source_id'] for r in sources}
next_id=max(int(r['claim_id'].split('-')[1]) for r in claims['records'])+1
mapping=[]
origin='03-report/research-notes/r02-operating-needs/claim-candidates.json'
for c in read(folder/'claim-candidates.json')['records']:
    assert set(c['source_ids'])<=source_ids
    found=next((r for r in claims['records'] if r.get('r02_candidate_id')==c['candidate_id']),None)
    if found:ident=found['claim_id']
    else:
        ident=f'CLM-{next_id:04}';next_id+=1
        claims['records'].append({'claim_id':ident,'source_ids':c['source_ids'],'locator':c['locator'],
          'claim_text':c['finding'],'evidence_class':c['evidence_class'],'metric':None,'value':c.get('value'),
          'selected_values':c.get('values'),'unit':c.get('unit'),'question_wording':c.get('question_wording'),
          'denominator':c.get('item_base'),'achieved_sample_context':c.get('achieved_sample'),
          'population':c['population'],'time_period':c.get('fieldwork_period'),'support_checked':True,
          'review_mode':c['review_mode']+'; parent inspected all four saved renders',
          'interpretation_limits':c['limitations'],'status':'extracted_context_only','publication_status':'working',
          'audit_record_origin':origin,'r02_candidate_id':c['candidate_id'],
          'extends_or_qualifies':c['extends_or_qualifies']})
    mapping.append({'candidate_id':c['candidate_id'],'claim_id':ident,'source_ids':c['source_ids']})
write(claims_path,claims)
log=read(folder/'review-log.json')
for image in log['page_renders']:
    p=ROOT/image['path'];assert p.is_file()
    assert hashlib.sha256(p.read_bytes()).hexdigest()==image['sha256']
wp=ROOT/'00-control/work-packages.json';w=read(wp)
w['active_work_package']='WP04';w['pending_review_work_packages']=['WP02']
for r in w['records']:
    if r['work_package_id']=='WP04':
        r.update(status='in_progress_initial_evidence_assessed',started_on='2026-10-28',
          working_file='03-report/modules/R02-operational-needs-and-service-gaps.md',
          evidence_of_completion='Initial scoped appraisal of three reused originals and three bounded claim records; four source renders inspected by researcher and parent. Practitioner integration and final publication checks outstanding.')
write(wp,w)
cp=ROOT/'00-control/changes.json';c=read(cp)
if not any(r.get('change_id')=='CHG-005' for r in c['records']):
    c['records'].append({'change_id':'CHG-005','date':'2026-10-28','type':'R02 initial desktop research',
      'description':'Assessed operational needs through three reused original sources, added three contextual claim extractions, and inspected four source renders. No new sources or participant observations; R02 remains in progress.'})
write(cp,c)
result={'date':'2026-10-28','status':'passed_for_initial_internal_assessment','claim_map':mapping,
        'new_sources':0,'source_renders_hash_checked_and_visually_inspected_by_parent':4,
        'participant_observations':0,'final_publication_approved':False,'external_actions':[]}
write(ROOT/'08-qa/R02-initial-review-check.json',result)
print(json.dumps(result,indent=2))
