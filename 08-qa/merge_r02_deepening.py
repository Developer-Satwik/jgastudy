from pathlib import Path
import json, hashlib
from urllib.parse import urlsplit, urlunsplit

ROOT=Path(__file__).resolve().parents[1]
FOLDER=ROOT/'03-report/research-notes/r02-deepening'
DATE='2026-10-28'
def read(p):return json.loads(p.read_text())
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
def norm(url):
    p=urlsplit(url);return urlunsplit((p.scheme,p.netloc.lower(),p.path.rstrip('/'),'',''))

sp=ROOT/'02-evidence/registers/sources.json';cp=ROOT/'02-evidence/registers/claims.json'
sources=read(sp);claims=read(cp)
source_by_url={norm(s['url']):s for s in sources['records']}
next_s=max(int(s['source_id'].split('-')[1]) for s in sources['records'])+1
next_c=max(int(s['claim_id'].split('-')[1]) for s in claims['records'])+1
source_map={};new_sources=0;new_claims=0
for folder,filename in [('service-boundaries','source-candidates.json'),('consequences','source-candidates.json'),('root','root-source-candidates.json')]:
    path=FOLDER/folder/filename
    for c in read(path)['records']:
        found=source_by_url.get(norm(c['url']))
        if found:
            sid=found['source_id']
            if not found.get('capture_path') and c.get('capture_path'):
                found['capture_path']=c['capture_path'];found['capture_sha256']=c['capture_sha256']
                found['capture_scope']='Original page retained during R02 deepening'
            found.setdefault('additional_reviews',[])
            review={'date':DATE,'module':'R02','origin':str(path.relative_to(ROOT)),'locator':c['locator']}
            if review not in found['additional_reviews']:found['additional_reviews'].append(review)
            if c['candidate_id']=='R02-ROOT-04':
                found['published_date']=None;found['last_updated']='2025-10-01'
                found['date_note']='Page displays last updated date; original publication date not established.'
        else:
            sid=f'SRC-{next_s:04}';next_s+=1;new_sources+=1
            found={'source_id':sid,'title':c['title'],'publisher':c['publisher'],'url':c['url'],
              'source_type':c['source_type'],'review_status':c['review_status'],'accessed_on':DATE,
              'published_date':c.get('published_date'),'fieldwork_period':c.get('fieldwork_period'),
              'population':c.get('population'),'sample_size':c.get('sample_size'),'method_available':None,
              'funding_or_commercial_interest':c.get('funding_or_commercial_interest'),
              'capture_path':c.get('capture_path'),'capture_sha256':c.get('capture_sha256'),
              'reuse_status':c.get('reuse_status','Reference and private verification only; reproduction rights not reviewed'),
              'publication_eligibility':'R02_context_final_wording_and_rights_pending','related_topic_ids':['R02'],
              'notes':c['limitations'],'date_note':c.get('date_note'),
              'audit_record_origin':str(path.relative_to(ROOT)),'r02_source_candidate_id':c['candidate_id'],
              'candidate_detail':c}
            if c['candidate_id'] in ['CON-S01','CON-S02']:
                found['document_date']=c['published_date'];found['published_date']=None
                found['date_note']='Report/final-issue date; exact public upload date not independently established.'
            sources['records'].append(found);source_by_url[norm(c['url'])]=found
        source_map[c['candidate_id']]=sid

# An additional summary route is a dataset alias, not another survey/source count.
ap=ROOT/'02-evidence/registers/source-aliases.json';aliases=read(ap)
aliases.setdefault('url_aliases',[])
for c in read(FOLDER/'capacity/source-candidates.json')['records']:
    if c.get('same_dataset_as'):
        record={'url':c['url'],'canonical_source_id':c['same_dataset_as'],'relationship':'Official summary of the same dataset','reviewed_on':DATE,'new_independent_dataset':False}
        if record not in aliases['url_aliases']:aliases['url_aliases'].append(record)
write(ap,aliases)

claim_map={}
for folder in ['capacity','service-boundaries','consequences','root']:
    path=FOLDER/folder/('root-source-candidates.json' if folder=='root' else 'claim-candidates.json')
    for c in read(path)['records']:
        if folder=='root':
            c={**c,'source_ids':[source_map[c['candidate_id']]],'claim_text':c['point'],
              'evidence_class':'official_guidance_mechanism','value':None,'unit':None,
              'review_mode':'Relevant live original sections inspected; original HTML retained'}
        ids=c.get('source_ids',c.get('source_candidate_ids',[]))
        ids=[source_map.get(s,s) for s in ids]
        assert all(s in {r['source_id'] for r in sources['records']} for s in ids)
        origin=str(path.relative_to(ROOT));candidate=c['candidate_id']
        existing=next((r for r in claims['records'] if r.get('r02_deepening_candidate_id')==candidate),None)
        if existing:cid=existing['claim_id']
        else:
            cid=f'CLM-{next_c:04}';next_c+=1;new_claims+=1
            claims['records'].append({'claim_id':cid,'source_ids':ids,'locator':c['locator'],
              'claim_text':c.get('claim_text',c.get('finding')),'evidence_class':c['evidence_class'],
              'metric':None,'value':c.get('value'),'selected_values':c.get('values'),'unit':c.get('unit'),
              'question_wording':c.get('question_wording',c.get('question_scope')),
              'denominator':c.get('denominator',c.get('item_base')),'achieved_sample_context':c.get('achieved_sample'),
              'population':c.get('population'),'time_period':c.get('time_period',c.get('fieldwork_period')),
              'support_checked':True,'review_mode':c.get('review_mode','Original relevant sections inspected'),
              'interpretation_limits':c['limitations'],
              'status':'hold_numeric_reuse' if c.get('status')=='hold_numeric_reuse' else 'R02_extracted_context',
              'publication_status':'working','audit_record_origin':origin,'r02_deepening_candidate_id':candidate,
              'extends_or_qualifies':c.get('extends_or_qualifies',[]),
              'candidate_detail':c})
        claim_map[candidate]=cid
sources['updated_on']=DATE;claims['updated_on']=DATE;write(sp,sources);write(cp,claims)

search_path=ROOT/'02-evidence/registers/searches.json';searches=read(search_path)
if not any(s['search_id']=='SCH-0008' for s in searches['records']):
    searches['records'].append({'search_id':'SCH-0008','date':DATE,'purpose':'R02 targeted needs, service boundary and consequence deepening',
      'queries':['CIPP original workload tasks KPIs and complexity; Deloitte original operations support and targets',
       'Payroll service definition customer approval escalation response resolution reconciliation support',
       'Primary council payroll audit late inputs overpayment recovery reasonable assurance',
       'HMRC FPS EPS payroll-ID corrections; employer records; DWP employer Universal Credit reporting'],
      'action':'Reused originals and inspected public primary service definitions, employer/audit cases and guidance. Restricted/unavailable routes excluded; no forms or contacts.',
      'related_source_ids':sorted(set(source_map.values())|{'SRC-0020','SRC-0021','SRC-0022','SRC-0040','SRC-0064'})})
write(search_path,searches)

# Check actual retained files in both primary records and page-capture logs.
checked={}
for s in sources['records']:
    if s.get('capture_path'):
        path=ROOT/s['capture_path'];assert path.is_file()
        assert hashlib.sha256(path.read_bytes()).hexdigest()==s['capture_sha256']
for folder in ['capacity','service-boundaries','consequences']:
    path=FOLDER/folder/'capture-log.json';log=read(path)
    records=log.get('records',log.get('captures',[]))
    for rec in records:
        if not rec.get('sha256'):continue
        rel=rec.get('path') or rec.get('capture_path')
        capture=ROOT/rel if rel else FOLDER/folder/rec['file']
        if not capture.exists() and rel:capture=Path.cwd()/rel
        if not capture.exists() and rec.get('file'):capture=FOLDER/folder/'captures'/rec['file']
        assert capture.is_file(),str(capture)
        assert hashlib.sha256(capture.read_bytes()).hexdigest()==rec['sha256']
        checked[str(capture.relative_to(ROOT))]=rec['sha256']

write(ROOT/'08-qa/R02-deepening-record-map.json',{'date':DATE,'source_map':source_map,'claim_map':claim_map})
write(ROOT/'08-qa/R02-deepening-captures.json',{'date':DATE,'files':[{'path':p,'sha256':h} for p,h in checked.items()]})
print(json.dumps({'status':'merged_for_R02_desktop_synthesis','new_source_routes':new_sources,'new_claim_records':new_claims,
  'total_source_records':len(sources['records']),'total_claim_records':len(claims['records']),
  'capture_log_files_checked':len(checked),'observations_added':0},indent=2))
