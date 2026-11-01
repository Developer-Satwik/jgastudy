from pathlib import Path
from urllib.parse import urlsplit,urlunsplit,parse_qsl,urlencode
import json,hashlib
R=Path(__file__).resolve().parents[1]; B=R/'04-table/research-notes/t05r-second-check'; DATE='2026-10-31'
def read(p):return json.loads(p.read_text())
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
if (R/'08-qa/T05R-second-check-record-map.json').exists():
 raise RuntimeError('T05R merge already recorded. Do not rerun: preserve the original append counts and reconcile any changes explicitly.')
def norm(u):
 p=urlsplit(u);return urlunsplit((p.scheme,p.netloc.lower(),p.path.rstrip('/'),urlencode(sorted((k,v) for k,v in parse_qsl(p.query) if not k.lower().startswith('utm_'))),''))
def resolve(v):
 p=Path(v)
 for q in [p if p.is_absolute() else R/p, R.parent.parent/p]:
  if q.is_file():return q
 raise FileNotFoundError(v)
def rel(v):return str(resolve(v).relative_to(R)) if v else None
def sha(v):return hashlib.sha256(resolve(v).read_bytes()).hexdigest()
def limits(c):return c.get('limitations',c.get('limits',c.get('interpretation_limits')))
def capture(c):
 x=c.get('capture',{})
 p=c.get('capture_path') or c.get('original_bytes_path') or x.get('html_path') or x.get('path')
 h=c.get('capture_sha256') or c.get('original_sha256') or x.get('html_sha256') or x.get('sha256')
 kind=c.get('capture_kind','');ext=list(c.get('review_extracts',[]))
 for pk,hk in [('parsed_extract_path','parsed_extract_sha256'),('parsed_path','parsed_sha256'),('parsed_text_path','parsed_sha256'),('text_path','text_sha256')]:
  if c.get(pk):ext.append(dict(path=c[pk],sha256=c[hk],kind='parsed_original_text'))
 if p and any(k in kind for k in ['parsed','extract','browser']):ext.append(dict(path=p,sha256=h,kind=kind));p=h=None
 if p: assert sha(p)==h,(p,h)
 for e in ext:e['path']=rel(e['path']);assert sha(e['path'])==e['sha256']
 return rel(p),h,ext
sp=R/'02-evidence/registers/sources.json';cp=R/'02-evidence/registers/claims.json';ap=R/'02-evidence/registers/source-aliases.json'
s,c,a=read(sp),read(cp),read(ap); byid={x['source_id']:x for x in s['records']};byurl={norm(x['url']):x for x in s['records']}
ns=max(int(x['source_id'].split('-')[1]) for x in s['records'])+1;nc=max(int(x['claim_id'].split('-')[1]) for x in c['records'])+1
sm={};cm={};new_s=0;new_c=0
folders=['history-market','competitors','root']
for f in folders:
 p=B/f/'source-candidates.json';d=read(p)
 for x in d.get('records',d.get('new_route_candidates',[])):
  ident=x.get('candidate_id',x.get('source_candidate_id'));assert ident
  found=byid.get(x.get('canonical_source_id')) or byurl.get(norm(x['url']))
  if found is None:
   sid=f'SRC-{ns:04}';ns+=1;new_s+=1;cap,h,ex=capture(x)
   found=dict(source_id=sid,title=x['title'],publisher=x['publisher'],url=x['url'],source_type=x.get('source_type','publisher_public_offer_or_terms'),review_status=x.get('review_status','relevant_original_public_offer_sections_inspected'),accessed_on=DATE,published_date=x.get('published_date'),last_updated=x.get('updated_date',x.get('last_updated')),date_note=x.get('date_note'),document_version=x.get('document_version'),population=x.get('population'),sample_size=x.get('sample_size'),fieldwork_period=x.get('fieldwork_period'),method_available=x.get('method_available'),funding_or_commercial_interest=x.get('funding_or_commercial_interest','Publisher describes its own offer; not observed sales or outcomes'),capture_path=cap,capture_sha256=h,review_extracts=ex,reuse_status=x.get('reuse_status','Private verification only; third-party reuse rights not granted'),publication_eligibility='T05R_second_context_final_use_pending',related_topic_ids=['T05R_second'],notes=limits(x),audit_record_origin=str(p.relative_to(R)),t05r_second_source_candidate_id=ident,candidate_detail=x)
   s['records'].append(found);byid[sid]=found;byurl[norm(x['url'])]=found
  else:
   review=dict(date=DATE,module='T05R_second_history_market_task_delivery',origin=str(p.relative_to(R)),source_candidate_detail=x)
   if review not in found.setdefault('additional_reviews',[]):found['additional_reviews'].append(review)
  sm[ident]=found['source_id']
  if 'T05R_second' not in found.setdefault('related_topic_ids',[]):found['related_topic_ids'].append('T05R_second')
  for u in x.get('alias_urls',[]):
   v=dict(url=u,canonical_source_id=found['source_id'],relationship='Same publisher offer or document route; not an independent dataset',reviewed_on=DATE,new_independent_dataset=False)
   if v not in a.setdefault('url_aliases',[]):a['url_aliases'].append(v)
 for x in d.get('reused_canonical_sources',[]):
  sid=x.get('source_id',x.get('canonical_source_id'));found=byid[sid]
  if x.get('candidate_id'):sm[x['candidate_id']]=sid
  review=dict(date=DATE,module='T05R_second_history_market_task_delivery',origin=str(p.relative_to(R)),detail=x)
  if review not in found.setdefault('additional_reviews',[]):found['additional_reviews'].append(review)
  if 'T05R_second' not in found.setdefault('related_topic_ids',[]):found['related_topic_ids'].append('T05R_second')
for f in folders:
 p=B/f/'claim-candidates.json'
 for x in read(p)['records']:
  ident=x.get('candidate_id',x.get('claim_candidate_id'));assert ident
  ids=list(dict.fromkeys(sm.get(v,v) for v in x.get('canonical_source_ids',[])+x.get('source_candidate_ids',[])+x.get('source_ids',[])))
  assert ids and set(ids)<=set(byid),(ident,ids)
  found=next((v for v in c['records'] if v.get('t05r_second_claim_candidate_id')==ident),None)
  if found is None:
   cid=f'CLM-{nc:04}';nc+=1;new_c+=1
   found=dict(claim_id=cid,source_ids=ids,locator=x['locator'],claim_text=x.get('claim_text',x.get('claim')),evidence_class=x['evidence_class'],metric=x.get('metric'),value=x.get('value'),unit=x.get('unit'),denominator=x.get('denominator'),question_wording=x.get('question_wording'),population=x.get('population',x.get('base')),time_period=x.get('time_period'),support_checked=True,review_mode=x.get('review_mode','Relevant public primary offer/terms sections inspected; publisher declarations and researcher interpretation separated.'),interpretation_limits=limits(x),status=x.get('status','T05R_desktop_context'),publication_status='working',audit_record_origin=str(p.relative_to(R)),t05r_second_claim_candidate_id=ident,candidate_detail=x)
   c['records'].append(found)
  cm[ident]=found['claim_id']
for d in [s,c,a]:d['updated_on']=DATE
write(sp,s);write(cp,c);write(ap,a)
write(R/'08-qa/T05R-second-check-record-map.json',dict(date=DATE,source_map=sm,claim_map=cm,new_source_routes=new_s,new_claim_records=new_c,canonical_sources=len(s['records']),canonical_claims=len(c['records']),folders=folders,commercial_validation=False,participant_observations=0,financial_inputs_added=0))
print(json.dumps(dict(new_source_routes=new_s,new_claim_records=new_c,canonical_sources=len(s['records']),canonical_claims=len(c['records']))))
