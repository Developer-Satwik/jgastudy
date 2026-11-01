from pathlib import Path
from urllib.parse import urlsplit,urlunsplit
import hashlib,json

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'03-report/research-notes/r03'
DATE='2026-10-29'
def read(p):return json.loads(p.read_text())
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
def norm(url):
    u=urlsplit(url);return urlunsplit((u.scheme,u.netloc.lower(),u.path.rstrip('/'),'',''))
def resolve(rel):
    p=Path(rel)
    for candidate in [p if p.is_absolute() else ROOT/p,ROOT.parent.parent/p]:
        if candidate.exists():return candidate
    raise FileNotFoundError(rel)

sp=ROOT/'02-evidence/registers/sources.json';cp=ROOT/'02-evidence/registers/claims.json'
sources=read(sp);claims=read(cp);by_url={norm(s['url']):s for s in sources['records']}
next_s=max(int(r['source_id'].split('-')[1]) for r in sources['records'])+1
next_c=max(int(r['claim_id'].split('-')[1]) for r in claims['records'])+1
source_map={};claim_map={};new_s=0;new_c=0
ap=ROOT/'02-evidence/registers/source-aliases.json';aliases=read(ap);aliases.setdefault('url_aliases',[])

for folder in ['integration','delivery','cases','root']:
    path=BASE/folder/'source-candidates.json'
    for c in read(path)['records']:
        sid=c['candidate_id'];found=by_url.get(norm(c['url']))
        if found is None:
            canonical=f'SRC-{next_s:04}';next_s+=1;new_s+=1
            found={'source_id':canonical,'title':c['title'],'publisher':c['publisher'],'url':c['url'],
             'source_type':c['source_type'],'review_status':c['review_status'],'accessed_on':DATE,
             'published_date':c.get('published_date'),'document_date':c.get('document_date'),
             'last_updated':c.get('updated_date',c.get('last_updated')),'date_note':c.get('date_note'),
             'fieldwork_period':c.get('fieldwork_period'),'population':c.get('population'),'sample_size':c.get('sample_size'),
             'method_available':None,'funding_or_commercial_interest':c.get('funding_or_commercial_interest'),
             'capture_path':c.get('capture_path'),'capture_sha256':c.get('capture_sha256'),
             'reuse_status':c.get('reuse_status'),'publication_eligibility':'R03_context_final_use_pending',
             'related_topic_ids':['R03'],'related_canonical_source_ids':c.get('related_canonical_source_ids',[]),
             'notes':c['limitations'],'audit_record_origin':str(path.relative_to(ROOT)),
             'r03_source_candidate_id':sid,'candidate_detail':c}
            sources['records'].append(found);by_url[norm(c['url'])]=found
        source_map[sid]=found['source_id']
        for url in c.get('alias_urls',[]):
            record={'url':url,'canonical_source_id':found['source_id'],'relationship':'Same publication section; not independent case evidence','reviewed_on':DATE,'new_independent_dataset':False}
            if record not in aliases['url_aliases']:aliases['url_aliases'].append(record)

source_by_id={s['source_id']:s for s in sources['records']}
for folder in ['integration','delivery','cases','root']:
    path=BASE/folder/'claim-candidates.json'
    for c in read(path)['records']:
        cid=c['candidate_id'];ids=[source_map.get(s,s) for s in c.get('source_candidate_ids',c.get('source_ids',[]))]
        assert ids and set(ids)<=set(source_by_id)
        found=next((r for r in claims['records'] if r.get('r03_claim_candidate_id')==cid),None)
        if found is None:
            canonical=f'CLM-{next_c:04}';next_c+=1;new_c+=1
            found={'claim_id':canonical,'source_ids':ids,'locator':c['locator'],'claim_text':c['claim_text'],
              'evidence_class':c['evidence_class'],'metric':None,'value':c.get('value'),'unit':c.get('unit'),
              'denominator':c.get('denominator'),'question_wording':c.get('question_wording'),
              'population':c.get('population'),'time_period':c.get('time_period'),
              'support_checked':True,'review_mode':c.get('review_mode','Relevant original sections inspected by assigned researcher; selected integration reviewed by root.'),
              'interpretation_limits':c.get('limitations',c.get('interpretation_limits')),
              'status':c['status'] if c['status'].startswith('hold_') else 'R03_extracted_context',
              'publication_status':'working','audit_record_origin':str(path.relative_to(ROOT)),
              'r03_claim_candidate_id':cid,'candidate_detail':c}
            claims['records'].append(found)
        claim_map[cid]=found['claim_id']
        for ident in ids:
            src=source_by_id[ident]
            if 'R03' not in src.setdefault('related_topic_ids',[]):src['related_topic_ids'].append('R03')
            review={'date':DATE,'module':'R03','origin':str(path.relative_to(ROOT)),'locator':c['locator']}
            if review not in src.setdefault('additional_reviews',[]):src['additional_reviews'].append(review)

checked={}
for folder in ['integration','delivery','cases','root']:
    log=read(BASE/folder/'capture-log.json')
    records=log if isinstance(log,list) else log.get('records',log.get('captures',[]))
    for r in records:
        sha=r.get('sha256',r.get('capture_sha256'));rel=r.get('path',r.get('capture_path'))
        if not sha:continue
        q=resolve(rel);assert hashlib.sha256(q.read_bytes()).hexdigest()==sha
        checked[str(q.relative_to(ROOT))]=sha
for s in sources['records']:
    if s.get('capture_path'):assert hashlib.sha256(resolve(s['capture_path']).read_bytes()).hexdigest()==s['capture_sha256']
    else:assert not s.get('capture_sha256')

for p,d in [(sp,sources),(cp,claims),(ap,aliases)]:d['updated_on']=DATE;write(p,d)
search_path=ROOT/'02-evidence/registers/searches.json';searches=read(search_path)
purpose='R03 task-level technology, integration, delivery and implementation trade-offs'
if not any(r.get('purpose')==purpose for r in searches['records']):
    n=max(int(r['search_id'].split('-')[1]) for r in searches['records'])+1
    searches['records'].append({'search_id':f'SCH-{n:04}','date':DATE,'purpose':purpose,
      'queries':['Primary Staffology sync/locks/async/import/webhook docs; Xero permissions; HMRC GfC22',
       'Cintra processing/payment workflow; Fourth retained scope; Phase3 managed components; official sourcing/choose-payroll guidance',
       'Audit Scotland SG annual audit; Scottish Parliament HR/payroll assurance; SG dated closure report',
       'Government AI Playbook; SAP configurable payroll controls; dated ADP variance-agent release and live overview'],
      'action':'Relevant primary originals inspected; version, beta, historical and case-selection limits preserved. No API/product trial, client-system access, new prompt test or contact.',
      'related_source_ids':sorted({s for c in claims['records'] if c.get('r03_claim_candidate_id') for s in c['source_ids']})})
write(search_path,searches)
write(ROOT/'08-qa/R03-record-map.json',{'date':DATE,'source_map':source_map,'claim_map':claim_map})
write(ROOT/'08-qa/R03-captures.json',{'date':DATE,'files':[{'path':p,'sha256':h} for p,h in checked.items()]})
print(json.dumps({'status':'R03_records_reconciled','added_sources':new_s,'added_claims':new_c,'total_sources':len(sources['records']),'total_claims':len(claims['records']),'capture_log_files_hash_checked':len(checked)},indent=2))
