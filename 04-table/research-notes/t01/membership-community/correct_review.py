from pathlib import Path
import json,hashlib,datetime
b=Path('04-table/research-notes/t01/membership-community')
def read(n):return json.loads((b/n).read_text())
def save(n,d):(b/n).write_text(json.dumps(d,indent=2)+'\n')
d=read('source-candidates.json');d['records']=[x for x in d['records'] if x['candidate_id']!='T1MC-S07']
for x in d['records']:
 if x['candidate_id']=='T1MC-S02':x['limitations']='Current tariff and VAT basis are unconfirmed. Retained parsed lines 113,154,203,247,326,374 explicitly say prices valid until 14 June 2026; this source may differ from another capture. Magazine frequency conflicts with the landing page. Not a current price input.'
save('source-candidates.json',d)
d=read('claim-candidates.json')
for x in d['records']:
 if x['candidate_id']=='T1MC-C09':
  x['claim_text']='CIPP Full membership is an individual professional grade with qualification or payroll-management experience eligibility; the current tariff is unconfirmed.'
  x['limitations']='Alternative screened only. Do not equate a personal grade with an organisational licence. The retained source at parsed line247 explicitly states price validity until 14 June 2026, so its displayed price is not promoted as a current price; another capture may differ.'
save('claim-candidates.json',d)
d=read('model-candidates.json')
for m in d['records']:
 for a in m['screened_alternatives']:
  if a['name']=='CIPP professional membership':a['why_not_primary']='Real technical-advice and professional-recognition bundle, but individual grade rather than corporate support unit. Current tariff is unconfirmed and benefit-frequency wording differs across captured pages. No CIPP price is a current financial input.'
  if a['name']=='Fosway Corporate Research Network':a.update(source_candidates=[],screened_lead_id='T1MC-L01',why_not_primary='Plausible analyst-network lead only. Public reader screening did not establish a concrete fee/admission/entitlement schedule; original retrieval returned HTTP403. Excluded from substantive source candidates and canonical evidence.')
save('model-candidates.json',d)
d=read('capture-manifest.json')
for x in d['records']:
 if x.get('source_candidate_id')=='T1MC-S07':x.pop('source_candidate_id');x.update(screened_lead_id='T1MC-L01',evidence_eligibility='excluded_access_failure_not_public_evidence')
save('capture-manifest.json',d)
save('screened-leads.json',{'date':'2026-10-29','records':[{'screened_lead_id':'T1MC-L01','name':'Fosway Corporate Research Network','url':'https://www.fosway.com/hrd/','status':'screened_lead_only_excluded_from_source_register','access_result':'HTTP403 original fetch; public reader result used only for lead screening','limitation':'No original bytes, verified fee/admission/entitlement schedule or substantive claim candidates. Not a selected comparable.'}]})
p=b/'MODEL-03-payroll-decision-support.md';s=p.read_text().replace('Published prices explicitly end 14 June 2026 and frequency wording conflicts across pages; current tariff unknown.','Current tariff is unconfirmed and benefit-frequency wording differs across captured pages. No CIPP price is a current financial input.');p.write_text(s)
p=b/'MODEL-04-practitioner-research-community.md';s=p.read_text().replace('Relevant buyer insight and analyst model, but primary reader screening did not establish a concrete public member fee/admission/entitlement schedule; original-byte retrieval returned HTTP403. Retained as a future route, not a second validated comparator.','Plausible analyst-network lead only. Original retrieval returned HTTP403 and is excluded from substantive source candidates. No verified fee/admission/entitlement schedule. Retained as a screened lead, not a second validated comparator.');p.write_text(s)
p=b/'review.md';s=p.read_text().replace('Its grades page explicitly ends price validity on 14 June 2026.','The current tariff is unconfirmed; captured price text is not used as a current price.').replace('source-candidates.json contains local T1MC source candidates, including clearly marked screened routes, and a canonical SRC-0010 reuse reference without changing its discovery-only status.','source-candidates.json contains ten retained public-page source candidates and a canonical SRC-0010 reuse reference without changing its discovery-only status. Fosway is held only in screened-leads.json.').replace('The Fosway failure is explicit.','The Fosway failure is explicit and excluded from substantive source candidates.');p.write_text(s)
(b/'write_outputs.py').unlink(missing_ok=True)
manifest=read('capture-manifest.json');sources=read('source-candidates.json')['records'];claims=read('claim-candidates.json')['records'];models=read('model-candidates.json')['records'];errors=[];hashes=[]
for r in manifest['records']:
 for pf,hf in [('original_bytes_path','original_sha256'),('parsed_text_path','parsed_sha256')]:
  if r.get(pf):
   p=Path(r[pf]);actual=hashlib.sha256(p.read_bytes()).hexdigest() if p.exists() else None;ok=actual==r[hf];hashes.append({'source_candidate_id':r.get('source_candidate_id'),'path':str(p),'sha256_matches':ok})
   if not ok:errors.append('hash '+str(p))
sids={x['candidate_id'] for x in sources};mids={x['candidate_id'] for x in models}
for cl in claims:
 if not set(cl['source_candidate_ids']).issubset(sids):errors.append('source '+cl['candidate_id'])
 if cl['model_candidate_id'] not in mids:errors.append('model '+cl['candidate_id'])
 p=Path(cl['locator']['file']);n=len(p.read_text().splitlines()) if p.exists() else 0
 if any(i<1 or i>n for i in cl['locator']['lines']):errors.append('locator '+cl['candidate_id'])
v={'checked_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'passed' if not errors else 'errors','selected_model_count':len(models),'source_candidate_count':len(sources),'claim_candidate_count':len(claims),'original_capture_count':sum(bool(r.get('original_bytes_path')) for r in manifest['records']),'excluded_access_failure_count':1,'checks':['Exactly two selected models','Ten substantive source candidates retain original and parsed hashes','Fosway403 excluded from source candidates and held only as lead','Claim references and line bounds valid','No financial-input array created','CIPP current tariff unconfirmed; no expired rate promoted','TPC graphical tier entitlement ambiguity explicit','TCB website and Council confidentiality conditions distinguished','No PDF source used','No shared canonical/core/client edits'],'hash_checks':hashes,'errors':errors}
save('verification.json',v);print(json.dumps({k:v[k] for k in ['status','selected_model_count','source_candidate_count','claim_candidate_count','errors']}))
