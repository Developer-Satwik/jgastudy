from pathlib import Path
import json, hashlib, urllib.request
from concurrent.futures import ThreadPoolExecutor

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
items=[
 ('R02-ROOT-01','Fix problems with running payroll You made a mistake in your FPS or EPS','HMRC','https://www.gov.uk/payroll-errors/correcting-your-fps-or-eps','Opening correction list; payment-date, personal-information and EPS sections',
  'The guidance identifies reporting errors affecting a PAYE bill and distinct correction routes, including duplicate-record risks. Correct employee payment, correct statutory reporting and correction effort are different outcomes.'),
 ('R02-ROOT-02','PAYE and payroll for employers Keeping records','HMRC','https://www.gov.uk/paye-for-employers/keeping-records','Keeping records; lost stolen or destroyed records',
  'Payroll records include payments, deductions, reports, HMRC payments and relevant supporting information. Record evidence and recoverability are separate operating needs from paying employees correctly.'),
 ('R02-ROOT-03','Universal Credit and employers','Department for Work and Pensions','https://www.gov.uk/guidance/universal-credit-information-for-employers','Employers your responsibilities',
  'Incorrect or late earnings information can affect the Universal Credit a claimant expects. Employers do not need to know which employees receive it. The reporting consequence is relevant without collecting personal benefit status.'),
 ('R02-ROOT-04','Handling unpaid wages','Acas','https://www.acas.org.uk/if-your-wages-are-not-paid/handling-unpaid-wages','Keeping workers informed; Repaying workers',
  'Payroll delay or incorrect payment requires communication and correction; financial difficulty and charges are possible consequences. The guidance is not evidence of incidence, retention effects or a typical cost per error.')]

def fetch(item):
 ident,title,publisher,url,locator,point=item
 rec={'candidate_id':ident,'title':title,'publisher':publisher,'url':url,'locator':locator,
  'point':point,'accessed_on':'2026-10-28','source_type':'official_operational_guidance',
  'review_status':'relevant_original_sections_inspected_through_web',
  'published_date':'2022-09-30' if ident=='R02-ROOT-03' else None,
  'updated_date':'2025-10-01' if ident=='R02-ROOT-04' else None,
  'population':'Guidance for relevant UK employers or workers; not a survey',
  'sample_size':None,'fieldwork_period':None,
  'limitations':'Operational mechanism and consequence context only. No market prevalence, automatic penalty, causal ROI or organisation-specific tax/legal advice inferred. Recheck rules at final publication.',
  'capture_path':None,'capture_sha256':None}
 try:
  req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'})
  with urllib.request.urlopen(req,timeout=20) as response:
   data=response.read();mime=response.headers.get('Content-Type','')
  assert 'html' in mime.lower()
  target=HERE/(ident+'.html');target.write_bytes(data)
  rec['capture_path']=str(target.relative_to(ROOT));rec['capture_sha256']=hashlib.sha256(data).hexdigest()
  rec['capture_status']='retained_original_html'
 except Exception as e:
  rec['capture_status']='not_retained';rec['capture_error']=str(e)[:180]
 return rec

with ThreadPoolExecutor(max_workers=4) as pool:records=list(pool.map(fetch,items))
(HERE/'root-source-candidates.json').write_text(json.dumps({'schema_version':'1.0','date':'2026-10-28','records':records},indent=2,ensure_ascii=False)+'\n')
print(json.dumps([{'id':r['candidate_id'],'capture':r['capture_status']} for r in records],indent=2))
