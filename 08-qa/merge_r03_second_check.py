from pathlib import Path
from urllib.parse import urlsplit,urlunsplit
import hashlib,json

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'03-report/research-notes/r03-second-check'
DATE='2026-10-29'
def read(p):return json.loads(p.read_text())
def write(p,d):
    temp=p.with_suffix(p.suffix+'.tmp');temp.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n');temp.replace(p)
def norm(url):
    p=urlsplit(url);return urlunsplit((p.scheme,p.netloc.lower(),p.path.rstrip('/'),'',''))
def resolve(rel):
    p=Path(rel)
    for q in [p if p.is_absolute() else ROOT/p,ROOT.parent.parent/p]:
        if q.exists():return q
    raise FileNotFoundError(rel)

sp=ROOT/'02-evidence/registers/sources.json';cp=ROOT/'02-evidence/registers/claims.json'
sources=read(sp);claims=read(cp);by_url={norm(s['url']):s for s in sources['records']}
next_s=max(int(r['source_id'].split('-')[1]) for r in sources['records'])+1
next_c=max(int(r['claim_id'].split('-')[1]) for r in claims['records'])+1
source_map={};claim_map={};added_s=0;added_c=0
ap=ROOT/'02-evidence/registers/source-aliases.json';aliases=read(ap);aliases.setdefault('url_aliases',[])
for folder in ['history','market','competitors','root']:
    path=BASE/folder/'source-candidates.json'
    for c in read(path)['records']:
        found=by_url.get(norm(c['url']))
        if found is None:
            canonical=f'SRC-{next_s:04}';next_s+=1;added_s+=1
            found={'source_id':canonical,'title':c['title'],'publisher':c['publisher'],'url':c['url'],
              'source_type':c['source_type'],'review_status':c['review_status'],'accessed_on':DATE,
              'published_date':c.get('published_date'),'last_updated':c.get('updated_date',c.get('last_updated')),
              'date_note':c.get('date_note'),'document_version':c.get('document_version'),
              'population':c.get('population'),'sample_size':c.get('sample_size'),'fieldwork_period':c.get('fieldwork_period'),
              'method_available':None,'funding_or_commercial_interest':c.get('funding_or_commercial_interest'),
              'capture_path':c.get('capture_path'),'capture_sha256':c.get('capture_sha256'),
              'reuse_status':c.get('reuse_status'),'publication_eligibility':'R03_second_check_context_final_use_pending',
              'related_topic_ids':['R03'],'notes':c['limitations'],'audit_record_origin':str(path.relative_to(ROOT)),
              'r03_second_check_source_candidate_id':c['candidate_id'],'candidate_detail':c}
            sources['records'].append(found);by_url[norm(c['url'])]=found
        source_map[c['candidate_id']]=found['source_id']
        for url in c.get('alias_urls',[]):
            record={'url':url,'canonical_source_id':found['source_id'],'relationship':'Same guide/publication context route; not an independent study','reviewed_on':DATE,'new_independent_dataset':False}
            if record not in aliases['url_aliases']:aliases['url_aliases'].append(record)
source_by_id={s['source_id']:s for s in sources['records']}
for folder in ['history','market','competitors','root']:
    path=BASE/folder/'claim-candidates.json'
    for c in read(path)['records']:
        ids=[source_map.get(s,s) for s in c.get('source_candidate_ids',c.get('source_ids',[]))]
        assert ids and set(ids)<=set(source_by_id)
        found=next((r for r in claims['records'] if r.get('r03_second_check_claim_candidate_id')==c['candidate_id']),None)
        if found is None:
            canonical=f'CLM-{next_c:04}';next_c+=1;added_c+=1
            found={'claim_id':canonical,'source_ids':ids,'locator':c['locator'],'claim_text':c['claim_text'],
              'evidence_class':c['evidence_class'],'metric':None,'value':c.get('value'),'unit':c.get('unit'),
              'denominator':c.get('denominator'),'question_wording':c.get('question_wording'),
              'population':c.get('population'),'time_period':c.get('time_period'),
              'support_checked':True,'review_mode':c.get('review_mode','Relevant original sections inspected; synthesis checked with source-specific limits.'),
              'interpretation_limits':c.get('limitations',c.get('interpretation_limits')),
              'status':'R03_second_check_context','publication_status':'working',
              'audit_record_origin':str(path.relative_to(ROOT)),
              'r03_second_check_claim_candidate_id':c['candidate_id'],'candidate_detail':c}
            claims['records'].append(found)
        claim_map[c['candidate_id']]=found['claim_id']
        for sid in ids:
            src=source_by_id[sid]
            if 'R03' not in src.setdefault('related_topic_ids',[]):src['related_topic_ids'].append('R03')
            review={'date':DATE,'module':'R03-second-check','origin':str(path.relative_to(ROOT)),'locator':c['locator']}
            if review not in src.setdefault('additional_reviews',[]):src['additional_reviews'].append(review)

checked={}
for folder in ['history','market','competitors','root']:
    log=read(BASE/folder/'capture-log.json')
    records=log if isinstance(log,list) else log.get('records',log.get('captures',[]))
    for r in records:
        sha=r.get('sha256',r.get('capture_sha256'));rel=r.get('path',r.get('capture_path'))
        if not sha:continue
        q=resolve(rel);assert hashlib.sha256(q.read_bytes()).hexdigest()==sha
        excluded=r.get('capture_status')=='redirected_homepage_not_requested_document'
        checked[str(q.relative_to(ROOT))]={'sha256':sha,'scope':'excluded_redirect_response' if excluded else 'retained_original'}
for s in sources['records']:
    if s.get('capture_path'):assert hashlib.sha256(resolve(s['capture_path']).read_bytes()).hexdigest()==s['capture_sha256']
    else:assert not s.get('capture_sha256')
bridge=read(BASE/'competitors/prior-study-bridge.json')
for r in bridge['provenance']:assert hashlib.sha256(resolve(r['path']).read_bytes()).hexdigest()==r['sha256']
assert norm('https://oakleaftct.com/digital-transformation/') not in {norm(s['url']) for s in sources['records']}
assert len(source_map)==12 and len(claim_map)==18
for p,d in [(sp,sources),(cp,claims),(ap,aliases)]:d['updated_on']=DATE;write(p,d)
search_path=ROOT/'02-evidence/registers/searches.json';searches=read(search_path)
purpose='R03 second challenge: historical/lifecycle, segmented market, recruitment/project engagement, prior-study contrasts and recoverability'
if not any(r.get('purpose')==purpose for r in searches['records']):
    n=max(int(r['search_id'].split('-')[1]) for r in searches['records'])+1
    searches['records'].append({'search_id':f'SCH-{n:04}','date':DATE,'purpose':purpose,
      'queries':['HMRC annual payroll software updates; SAP HCM release cycle and reused CIPP historical originals',
       'Xero UK self-service; CloudPay partner coordination; Deel worker/service distinctions; reused provider definitions',
       'JGA editorial; Hays project/SOW models; Robert Half/Protiviti blended consulting and staffing; six-firm prior scope',
       'GDS integration/adaptation and technical lock-in; NCSC shared responsibility and SaaS recovery'],
      'action':'Bounded current primary inspection and explicit historical reuse; selected prior constructed prompts independently verified, not rerun. Redirected TCT body excluded. No contact or product/API trial.',
      'related_source_ids':sorted({s for c in claims['records'] if c.get('r03_second_check_claim_candidate_id') for s in c['source_ids']})})
write(search_path,searches)
write(ROOT/'08-qa/R03-second-check-record-map.json',{'date':DATE,'source_map':source_map,'claim_map':claim_map})
write(ROOT/'08-qa/R03-second-check-captures.json',{'date':DATE,'files':[{'path':p,**r} for p,r in checked.items()]})
print(json.dumps({'status':'merged_for_internal_review','added_sources':added_s,'added_claims':added_c,'total_sources':len(sources['records']),'total_claims':len(claims['records']),'retained_original_files_checked':sum(r['scope']=='retained_original' for r in checked.values()),'excluded_redirect_response_checked':sum(r['scope']=='excluded_redirect_response' for r in checked.values()),'prior_provenance_hashes_checked':len(bridge['provenance'])},indent=2))
