from pathlib import Path
from urllib.parse import urlsplit, urlunsplit
import hashlib, json

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / '03-report/research-notes/r02-second-check'
DATE = '2026-10-28'
def read(path): return json.loads(path.read_text())
def write(path, obj): path.write_text(json.dumps(obj, indent=2, ensure_ascii=False)+'\n')
def norm(url):
    p=urlsplit(url)
    return urlunsplit((p.scheme,p.netloc.lower(),p.path.rstrip('/'),'',''))
def resolve(path):
    p=Path(path)
    if p.is_absolute(): return p
    for q in [ROOT/p, ROOT.parent.parent/p]:
        if q.exists(): return q
    raise FileNotFoundError(path)

sp=ROOT/'02-evidence/registers/sources.json'
cp=ROOT/'02-evidence/registers/claims.json'
sources=read(sp); claims=read(cp)
by_url={norm(s['url']):s for s in sources['records']}
source_map={}; claim_map={}; additions={'sources':0,'claims':0}
next_s=max(int(s['source_id'].split('-')[1]) for s in sources['records'])+1
next_c=max(int(c['claim_id'].split('-')[1]) for c in claims['records'])+1
aliases_path=ROOT/'02-evidence/registers/source-aliases.json'
aliases=read(aliases_path);aliases.setdefault('url_aliases',[])

for folder in ['history','market','competitors','root']:
    path=BASE/folder/'source-candidates.json'
    for candidate in read(path)['records']:
        sid=candidate['candidate_id']
        found=by_url.get(norm(candidate['url']))
        if found is None:
            canonical=f'SRC-{next_s:04}'; next_s+=1; additions['sources']+=1
            found={
                'source_id':canonical,'title':candidate['title'],'publisher':candidate['publisher'],
                'url':candidate['url'],'source_type':candidate['source_type'],
                'review_status':candidate['review_status'],'accessed_on':DATE,
                'published_date':candidate.get('published_date'),'last_updated':candidate.get('updated_date'),
                'date_note':candidate.get('date_note','Live source snapshot; publication date not established.'),
                'population':candidate.get('population'),'sample_size':candidate.get('sample_size'),
                'fieldwork_period':candidate.get('fieldwork_period'),'method_available':None,
                'funding_or_commercial_interest':candidate.get('funding_or_commercial_interest', 'Publisher describes its own recruitment offer/request; no independent outcome verification.' if folder=='competitors' else None),
                'capture_path':candidate.get('capture_path'),'capture_sha256':candidate.get('capture_sha256'),
                'reuse_status':candidate.get('reuse_status','Private verification; final-use rights outstanding'),
                'publication_eligibility':'R02_second_check_context_final_use_pending',
                'related_topic_ids':['R02'],'notes':candidate['limitations'],
                'audit_record_origin':str(path.relative_to(ROOT)),
                'r02_second_check_source_candidate_id':sid,'candidate_detail':candidate
            }
            if sid=='SC-ROOT-S03':
                found['document_date']=found['published_date'];found['published_date']=None
            sources['records'].append(found);by_url[norm(candidate['url'])]=found
        source_map[sid]=found['source_id']
        review={'date':DATE,'module':'R02-second-check','origin':str(path.relative_to(ROOT)),'locator':candidate['locator']}
        if review not in found.setdefault('additional_reviews',[]):found['additional_reviews'].append(review)
        for url in list(candidate.get('alias_urls',[]))+([candidate['landing_url']] if candidate.get('landing_url') else []):
            record={'url':url,'canonical_source_id':found['source_id'],'relationship':'Publisher landing or release route for the same report','reviewed_on':DATE,'new_independent_dataset':False}
            if record not in aliases['url_aliases']:aliases['url_aliases'].append(record)

for folder in ['history','market','competitors','root']:
    path=BASE/folder/'claim-candidates.json'
    for candidate in read(path)['records']:
        cid=candidate['candidate_id']
        sids=[source_map.get(x,x) for x in candidate.get('source_candidate_ids',candidate.get('source_ids',[]))]
        assert sids and set(sids)<={s['source_id'] for s in sources['records']}
        found=next((c for c in claims['records'] if c.get('r02_second_check_claim_candidate_id')==cid),None)
        if found is None:
            canonical=f'CLM-{next_c:04}';next_c+=1; additions['claims']+=1
            period=candidate.get('time_period')
            if cid=='HIS-C01':period='Historical programme review published December 2017; implementation and 2016–2017 evidence.'
            elif cid in ['HIS-C02','HIS-C03']:period='Selected case accounts spanning November 2020–January 2025; published February 2025.'
            elif cid=='HIS-C04':period='Statistical methodology published January 2025.'
            elif cid=='HIS-C05':period='Interpretive comparison of 2017 review and 2025 selected cases; no common series.'
            elif cid=='SC-ROOT-C03':period='Incident October 2023; account dated March 2024.'
            found={
                'claim_id':canonical,'source_ids':sids,'locator':candidate['locator'],
                'claim_text':candidate['claim_text'],'evidence_class':candidate['evidence_class'],
                'metric':None,'value':candidate.get('value'),'unit':candidate.get('unit'),
                'denominator':candidate.get('denominator'),'question_wording':candidate.get('question_wording'),
                'population':candidate.get('population'),'time_period':period,
                'support_checked':True,'review_mode':candidate.get('review_mode','Relevant original sections inspected by assigned researcher; context and limits reviewed by root.'),
                'interpretation_limits':candidate.get('limitations',candidate.get('interpretation_limits')),
                'status':'R02_second_check_context','publication_status':'working',
                'audit_record_origin':str(path.relative_to(ROOT)),
                'r02_second_check_claim_candidate_id':cid,'candidate_detail':candidate
            }
            if cid=='HIS-C05':found['evidence_class']='historical_interpretation_not_a_measured_trend'
            claims['records'].append(found)
        claim_map[cid]=found['claim_id']

# Verify bytes rather than assuming every web inspection produced a file.
checked={}
for s in sources['records']:
    if s.get('capture_path'):
        q=resolve(s['capture_path']);assert hashlib.sha256(q.read_bytes()).hexdigest()==s['capture_sha256']
    else:assert not s.get('capture_sha256')
for folder in ['history','market','competitors','root']:
    log=read(BASE/folder/'capture-log.json')
    records=log if isinstance(log,list) else log.get('records',[])
    for record in records:
        sha=record.get('sha256',record.get('capture_sha256'))
        rel=record.get('path',record.get('capture_path'))
        if not sha:continue
        q=resolve(rel);assert hashlib.sha256(q.read_bytes()).hexdigest()==sha
        checked[str(q.relative_to(ROOT))]=sha
bridge=read(BASE/'competitors/prior-study-bridge.json')
for record in bridge['provenance']:
    assert hashlib.sha256(resolve(record['path']).read_bytes()).hexdigest()==record['sha256']

for path,obj in [(sp,sources),(cp,claims),(aliases_path,aliases)]:
    obj['updated_on']=DATE;write(path,obj)
search_path=ROOT/'02-evidence/registers/searches.json'; searches=read(search_path)
purpose='R02 second challenge: history, market, recruitment comparators, prior-study bridge and resilience'
if not any(r.get('purpose')==purpose for r in searches['records']):
    num=max(int(r['search_id'].split('-')[1]) for r in searches['records'])+1
    searches['records'].append({'search_id':f'SCH-{num:04}','date':DATE,'purpose':purpose,
      'queries':['HMRC RTI historical review; CIPP reported RTI exception cases; ONS RTI statistical QA',
       'HMRC basic tools and recognised software; Xero software/price scope; ADP managed/global responsibilities',
       'JGA and six earlier recruitment comparators current primary service scope; interim payroll vacancy and organisational change case',
       'Government salary-diversion guidance; Bacs payment cycle; British Library incident review and payroll continuity'],
      'action':'Primary public originals inspected with bounded scope; local capture limits recorded. Earlier AI study used as discovery leads only; no prompts rerun or external contacts.',
      'related_source_ids':sorted(set(source_map.values()))})
write(search_path,searches)
write(ROOT/'08-qa/R02-second-check-record-map.json',{'date':DATE,'source_map':source_map,'claim_map':claim_map})
write(ROOT/'08-qa/R02-second-check-captures.json',{'date':DATE,'files':[{'path':p,'sha256':h} for p,h in checked.items()]})
print(json.dumps({'status':'merged_for_internal_review','added':additions,'total_sources':len(sources['records']),'total_claims':len(claims['records']),'capture_log_originals_checked':len(checked),'prior_study_provenance_files_hash_checked':len(bridge['provenance'])},indent=2))
