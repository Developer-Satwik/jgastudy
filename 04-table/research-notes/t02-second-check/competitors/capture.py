from pathlib import Path
import json,hashlib,urllib.request,urllib.error,datetime,concurrent.futures
from html.parser import HTMLParser
B=Path(__file__).resolve().parent;R=B.parents[3]
class P(HTMLParser):
 def __init__(self):super().__init__();self.skip=0;self.out=[]
 def handle_starttag(self,t,a):
  if t in ['script','style','noscript']:self.skip+=1
  if t in ['p','div','li','h1','h2','h3','section','br']:self.out.append('\n')
 def handle_endtag(self,t):
  if t in ['script','style','noscript']:self.skip=max(0,self.skip-1)
  if t in ['p','div','li','h1','h2','h3','section']:self.out.append('\n')
 def handle_data(self,d):
  if not self.skip:self.out.append(d)
def cap(item):
 ident,url=item;x=dict(source_candidate_or_canonical_id=ident,url=url,retrieved_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
 try:
  req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'})
  with urllib.request.urlopen(req,timeout=30)as r:raw=r.read();x.update(http_status=r.status,final_url=r.url)
  p=B/'captures'/f'{ident}.html';p.write_bytes(raw);hp=P();hp.feed(raw.decode('utf-8',errors='replace'));lines=[' '.join(s.split())for s in ''.join(hp.out).splitlines()];lines=[s for s in lines if s];tp=p.with_suffix('.txt');tp.write_text('\n'.join(f'{i:04}: {s}'for i,s in enumerate(lines,1))+'\n')
  x.update(capture_path=str(p.relative_to(R)),capture_sha256=hashlib.sha256(raw).hexdigest(),text_path=str(tp.relative_to(R)),text_sha256=hashlib.sha256(tp.read_bytes()).hexdigest(),capture_kind='retained_original_html')
 except Exception as e:x.update(http_status=getattr(e,'code',None),error=str(e),capture_path=None,capture_sha256=None,capture_kind='raw_unavailable_not_evidence')
 return x
items=[('SRC-0193','https://www.roberthalf.com/gb/en/insights/salary-guide'),('SRC-0222','https://www.oakleafpartnership.com/news-views/market-insights-payroll-reward'),('SRC-0116','https://middlemore.co.uk/payroll-search/'),('TC2-S01','https://www.oakleafpartnership.com/news-views/pensions-reform-salary-sacrifice')]
with concurrent.futures.ThreadPoolExecutor(max_workers=4)as ex:rows=list(ex.map(cap,items))
(B/'capture-manifest.json').write_text(json.dumps(dict(date='2026-10-30',records=rows),indent=2)+'\n');print(json.dumps([(r['source_candidate_or_canonical_id'],r.get('http_status'))for r in rows]))
