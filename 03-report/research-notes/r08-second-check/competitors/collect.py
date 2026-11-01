from pathlib import Path
import json,hashlib,datetime,concurrent.futures
from urllib.request import Request,urlopen
from html.parser import HTMLParser
ROOT=Path(__file__).resolve().parents[4];BASE=Path(__file__).resolve().parent
ids=['SRC-0210','SRC-0119','SRC-0115','SRC-0116','SRC-0147','SRC-0192','SRC-0193','SRC-0113']
sources=json.loads((ROOT/'02-evidence/registers/sources.json').read_text())['records']
class Parser(HTMLParser):
 def __init__(self):super().__init__();self.parts=[];self.skip=0
 def handle_starttag(self,t,a):
  if t in ['script','style']:self.skip+=1
  if t in ['p','h1','h2','h3','h4','li','div','br']:self.parts.append('\n')
 def handle_endtag(self,t):
  if t in ['script','style']:self.skip=max(0,self.skip-1)
 def handle_data(self,d):
  if not self.skip:self.parts.append(d)
def collect(i):
 s=next(x for x in sources if x['source_id']==i);url=s['url'];d=dict(source_id=i,url=url,retrieved_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
 try:
  res=urlopen(Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=40);b=res.read();t=b.decode(errors='replace');d.update(http_status=res.status,final_url=res.url)
  if res.status==200 and not any(x in t.lower()[:10000] for x in ['just a moment...','cf-chl-','attention required!']):
   p=BASE/'captures'/f'{i}.html';p.write_bytes(b);q=Parser();q.feed(t);txt='\n'.join(x.strip() for x in ''.join(q.parts).splitlines() if x.strip());o=BASE/'captures'/f'{i}.txt';o.write_text(txt)
   d.update(capture_path=str(p.relative_to(ROOT)),capture_sha256=hashlib.sha256(b).hexdigest(),capture_kind='retained_original_html',text_path=str(o.relative_to(ROOT)),text_sha256=hashlib.sha256(o.read_bytes()).hexdigest())
  else:d.update(capture_path=None,capture_sha256=None,capture_kind='raw_unavailable',evidence_status='excluded_interstitial')
 except Exception as e:d.update(error=str(e),http_status=getattr(e,'code',None),capture_path=None,capture_sha256=None,capture_kind='raw_unavailable',evidence_status='raw_access_failed_not_source_evidence')
 return d
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:records=list(ex.map(collect,ids))
(BASE/'capture-manifest.json').write_text(json.dumps({'date':'2026-10-29','records':records},indent=2)+'\n')
print(json.dumps(records,indent=2))
