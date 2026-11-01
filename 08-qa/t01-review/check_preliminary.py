from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parents[2];B=R/'04-table/research-notes/t01';O=R/'08-qa/t01-review'
checks=[]
def ck(v,n):checks.append({'name':n,'passed':bool(v)});assert v,n
def read(p):return json.loads(p.read_text())
S={};C={};M=[];hashes={}
for f in ['research-products','membership-community','forums-events','root']:
 d=read(B/f/'source-candidates.json')
 for s in d.get('records',[]):
  i=s.get('candidate_id',s.get('source_candidate_id'));ck(i not in S,'unique source candidate '+i);S[i]=s
  if s.get('capture_path'):
   p=R/s['capture_path'];ck(p.is_file(),'capture exists '+i);ck(hashlib.sha256(p.read_bytes()).hexdigest()==s['capture_sha256'],'raw hash '+i);hashes[str(p.relative_to(R))]=s['capture_sha256']
  for e in s.get('review_extracts',[]):
   p=R/e['path'];ck(p.is_file() and hashlib.sha256(p.read_bytes()).hexdigest()==e['sha256'],'extract hash '+i);hashes[str(p.relative_to(R))]=e['sha256']
 for c in read(B/f/'claim-candidates.json')['records']:
  ck(c['candidate_id'] not in C,'unique claim candidate '+c['candidate_id']);C[c['candidate_id']]=c
 if f!='root':
  d=read(B/f/'model-candidates.json');models=d.get('models',d.get('records',[]));ck(len(models)==2,f+' has exactly two models');M+=models
ck(len(M)==6,'exactly six comparable model records')
canonical={s['source_id'] for s in read(B/'root/sources-before.json')['records']}
for c in C.values():
 ck(set(c.get('source_candidate_ids',[]))<=set(S),'candidate sources resolve '+c['candidate_id'])
 ck(set(c.get('canonical_source_ids',[]))<=canonical,'canonical sources resolve '+c['candidate_id'])
 ck(bool(c.get('source_candidate_ids') or c.get('canonical_source_ids')),'claim support route supplied '+c['candidate_id'])
 ck(bool(c.get('limitations')),'claim limits supplied '+c['candidate_id'])
for m in M:
 i=m.get('candidate_id',m.get('candidate_model_id',m.get('model_id')))
 refs=[]
 for k in ['claim_candidate_ids','claim_candidates']:refs+=m.get(k,[])
 ck(bool(refs) and set(refs)<=set(C),'model claims resolve '+i)
 for k in ['source_candidate_ids','offer_source_candidates','core_source_candidate_ids','verification_source_candidate_ids','supplemental_terms_source_candidate_ids']:
  ck(set(m.get(k,[]))<=set(S),'model sources resolve '+i+'/'+k)
ck(read(R/'04-table/financial-inputs.json')['records']==[],'no public list price imported into financial inputs')
ck(read(R/'05-analysis/observations.json')['records']==[],'no participant observations invented')
t=(B/'membership-community/captures/tpc-membership.parsed.txt').read_text();terms=(B/'membership-community/captures/tpc-terms.parsed.txt').read_text()
ck('£1,122' in t and 'Corporate' in t and '/year' in t,'Corporate published annual GBP unit inspected')
ck('exclusive of any VAT payable unless otherwise stated' in terms,'generic VAT qualifier inspected')
ct=(B/'membership-community/captures/cipp-grades.parsed.txt').read_text();ck('Prices valid until 14 June 2026' in ct,'CIPP explicit tier-date footnote found; provisional missing-year issue disproved')
tcb=(B/'membership-community/captures/tcb-councils.parsed.txt').read_text();ck('Seats are available for individuals through an annual fee' in tcb and 'Chatham House Rule' in tcb,'TCB Council distinct annual individual seat and rule inspected')
iv=(B/'forums-events/captures/iventiv-sponsors.parsed.txt').read_text();ck(all(x in iv for x in ['Two Delegate Passes','9 x Pre-selected','Contact details of all Delegates','Choose your subject and format']),'iVentiv sponsor access inventory inspected; not research licence')
faq=(B/'forums-events/captures/iventiv-faq.parsed.txt').read_text();ck('10,000 or more' in faq and 'more than 10,000' in faq,'iVentiv company-size wording discrepancy preserved')
ck('maximum of two or three' in faq and 'maximum of 40' in faq,'iVentiv advertised limits inspected; not achieved counts')
isg=(B/'research-products/parsed/T1RP-S04.txt').read_text();ck('annual subscription' in isg and 'A 30-minute inquiry is included with each Buyers Guide' in isg,'ISG declared annual access and bounded inquiry inspected')
provider=(B/'research-products/parsed/T1RP-S05.txt').read_text();ck('Licensed use of the reports and graphics' in provider,'ISG external use licence category inspected')
cpo=(B/'forums-events/captures/cpo-forum-review.parsed.txt').read_text();ck('invite-only online community, launched in October 2025' in cpo,'CPO historical launch and invitation inspected')
ck('Product Director' in cpo and 'Alithya' in cpo,'CPO not assumed employer-only or vendor-free')
result={'status':'passed_preliminary_source_and_scope_review_integration_pending','date':'2026-10-29','checks':checks,'check_count':len(checks),'model_count':len(M),'source_candidates':len(S),'claim_candidates':len(C),'reviewed_hashes':hashes,'provisional_issue_closed':'CIPP missing-year concern disproved by explicit tier footnotes; retained year supported.','integration_review_complete':False,'external_contact':False,'commercial_validation':False}
(O/'preliminary-checks.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k not in ['checks','reviewed_hashes']},indent=2))
