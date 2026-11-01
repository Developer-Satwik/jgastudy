from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import urllib.request,json,hashlib,datetime
p=Path(__file__).resolve().parent
routes=[
('MKT-S01','hmrc-basic-tools.html','https://www.gov.uk/basic-paye-tools'),
('MKT-S02','hmrc-recognised-software.html','https://www.gov.uk/guidance/find-payroll-software-that-is-recognised-by-hmrc'),
('MKT-S03','xero-uk-pricing.html','https://www.xero.com/uk/pricing-plans/'),
('MKT-S04','xero-uk-payroll.html','https://www.xero.com/uk/accounting-software/payroll/'),
('MKT-S05','adp-uk-managed.html','https://uk.adp.com/what-we-offer/payroll/managed-payroll-services.aspx'),
('MKT-S06','adp-global-payroll.html','https://uk.adp.com/what-we-offer/products/adp-global-payroll.aspx')]
def get(row):
 ident,name,url=row
 try:
  req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'})
  with urllib.request.urlopen(req,timeout=45) as r:
   raw=r.read(); final=r.url; status=r.status
  (p/name).write_bytes(raw)
  return {'candidate_id':ident,'url':url,'final_url':final,'http_status':status,'status':'retained_original_html','path':str((p/name).relative_to(p.parents[3])),'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw),'retrieved_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 except Exception as e:return {'candidate_id':ident,'url':url,'status':'local_capture_unavailable','error':str(e),'path':None,'sha256':None,'web_reader':'Original relevant live sections inspected with web tool on 2026-10-28'}
with ThreadPoolExecutor(max_workers=4) as ex: out=list(ex.map(get,routes))
(p/'capture-log.json').write_text(json.dumps({'date':'2026-10-28','records':out},indent=2)+'\n')
print(json.dumps(out,indent=2))
