from pathlib import Path
from html.parser import HTMLParser
import urllib.request,urllib.error,json,hashlib,datetime,concurrent.futures
R=Path(__file__).resolve().parents[4];B=R/'04-table/research-notes/t02-second-check/market';D='2026-10-30'
# Root=project: file parent market0,t02-second-check1,research-notes2,04-table3,project4.
class P(HTMLParser):
 def __init__(self):super().__init__();self.skip=0;self.out=[]
 def handle_starttag(self,t,a):
  if t in ['script','style','noscript']:self.skip+=1
  if t in ['div','p','li','br','h1','h2','h3','tr','section']:self.out.append('\n')
 def handle_endtag(self,t):
  if t in ['script','style','noscript']:self.skip=max(0,self.skip-1)
  if t in ['div','p','li','h1','h2','h3','tr','section']:self.out.append('\n')
 def handle_data(self,d):
  if not self.skip:self.out.append(d)
def w(n,d):(B/n).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
urls=[('SRC-0003','https://www.gov.uk/government/publications/the-magenta-book/quality-in-qualitative-evaluation-qqe-html'),('SRC-0227','https://research.isg-one.com/research/buyers-guides/services/enterprise-and-service-providers'),('SRC-0229','https://research.isg-one.com/buyers-guide/business-technologies/employees-and-hcm/global-payroll/2025'),('SRC-0246','https://www.iventiv.com/sponsors')]
def fetch(item):
 sid,u=item;req=urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0 (research verification)'})
 try:
  with urllib.request.urlopen(req,timeout=35)as r:raw=r.read();status=r.status;final=r.url
  path=B/'captures'/f'{sid}.html';path.write_bytes(raw);parser=P();parser.feed(raw.decode('utf-8',errors='replace'));lines=[' '.join(s.split())for s in ''.join(parser.out).splitlines()];lines=[s for s in lines if s];tp=path.with_suffix('.parsed.txt');tp.write_text('\n'.join(f'{i:04}: {s}'for i,s in enumerate(lines,1))+'\n')
  return dict(source_id=sid,url=u,http_status=status,final_url=final,retrieved_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),capture_path=str(path.relative_to(R)),capture_sha256=hashlib.sha256(raw).hexdigest(),parsed_path=str(tp.relative_to(R)),parsed_sha256=hashlib.sha256(tp.read_bytes()).hexdigest(),capture_kind='retained_original_html')
 except urllib.error.HTTPError as e:return dict(source_id=sid,url=u,http_status=e.code,capture_path=None,capture_sha256=None,capture_kind='raw_unavailable_not_evidence',error=str(e))
with concurrent.futures.ThreadPoolExecutor(max_workers=4)as pool:rows=list(pool.map(fetch,urls))
w('capture-manifest.json',dict(date=D,records=rows))
print(R);print([(x['source_id'],x['http_status'])for x in rows])
