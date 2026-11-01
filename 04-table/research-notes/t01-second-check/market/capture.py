from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from urllib.request import Request,urlopen
from html.parser import HTMLParser
import hashlib,json,datetime
R=Path(__file__).resolve().parents[4]
B=Path(__file__).resolve().parent
routes=[('SRC-0227','https://research.isg-one.com/research/buyers-guides/services/enterprise-and-service-providers'),('SRC-0228','https://research.isg-one.com/research/buyers-guides/services/software-providers'),('SRC-0238','https://thepayrollcentre.co.uk/membership/'),('SRC-0239','https://thepayrollcentre.co.uk/terms-and-conditions-of-business/'),('SRC-0245','https://www.iventiv.com/how-can-we-help'),('SRC-0246','https://www.iventiv.com/sponsors'),('SRC-0248','https://www.iventiv.com/terms-and-conditions'),('T1M-S01','https://ipass.ie/membership/'),('T1M-S02','https://gpa.net/')]
class Parser(HTMLParser):
 def __init__(self): super().__init__();self.skip=0;self.parts=[]
 def handle_starttag(self,t,a):
  if t in ['script','style','noscript']:self.skip+=1
  if not self.skip and t in ['p','div','section','li','h1','h2','h3','h4','br','tr']:self.parts.append('\n')
 def handle_endtag(self,t):
  if t in ['script','style','noscript']:self.skip=max(0,self.skip-1)
  if not self.skip and t in ['p','div','section','li','h1','h2','h3','h4','tr']:self.parts.append('\n')
 def handle_data(self,x):
  if not self.skip:self.parts.append(x)
def run(x):
 i,u=x
 try:
  req=Request(u,headers={'User-Agent':'Mozilla/5.0 ResearchReadOnly/1.0'})
  with urlopen(req,timeout=35) as r: data=r.read();url=r.url;status=r.status;ct=r.headers.get('Content-Type')
  p=B/'captures'/f'{i}.html';p.write_bytes(data);z=Parser();z.feed(data.decode('utf-8',errors='replace'));lines=[' '.join(s.split())for s in ''.join(z.parts).splitlines()];lines=[s for s in lines if s]
  t=B/'captures'/f'{i}.parsed.txt';t.write_text('\n'.join(f'{n:04}: {v}' for n,v in enumerate(lines,1))+'\n')
  return dict(source_id=i,url=u,final_url=url,http_status=status,content_type=ct,retrieved_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),capture_path=str(p.relative_to(R)),capture_sha256=hashlib.sha256(data).hexdigest(),parsed_path=str(t.relative_to(R)),parsed_sha256=hashlib.sha256(t.read_bytes()).hexdigest(),kind='retained_original_html')
 except Exception as e:return dict(source_id=i,url=u,error=str(e),http_status=getattr(e,'code',None),kind='excluded_failed_retrieval')
with ThreadPoolExecutor(max_workers=5) as ex:records=list(ex.map(run,routes))
(B/'capture-manifest.json').write_text(json.dumps(dict(date='2026-10-30',records=records),indent=2)+'\n')
print(json.dumps([dict(source_id=x['source_id'],http_status=x.get('http_status'),kind=x['kind'])for x in records],indent=2))
