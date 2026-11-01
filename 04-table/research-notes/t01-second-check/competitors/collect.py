from pathlib import Path
from urllib.request import Request,urlopen
from concurrent.futures import ThreadPoolExecutor
from html.parser import HTMLParser
from datetime import datetime,timezone
import json,hashlib
R=Path(__file__).resolve().parents[4];B=Path(__file__).resolve().parent
S={s['source_id']:s for s in json.loads((R/'02-evidence/registers/sources.json').read_text())['records']}
ids=['SRC-0190','SRC-0221','SRC-0222','SRC-0116','SRC-0192','SRC-0193','SRC-0088']
class T(HTMLParser):
 def __init__(self):super().__init__();self.a=[];self.skip=0
 def handle_starttag(self,t,a):
  if t in ['script','style','noscript']:self.skip+=1
  if t in ['p','li','div','h1','h2','h3','h4','br','tr']:self.a.append('\n')
 def handle_endtag(self,t):
  if t in ['script','style','noscript']:self.skip=max(0,self.skip-1)
  if t in ['p','li','div','h1','h2','h3','h4','tr']:self.a.append('\n')
 def handle_data(self,d):
  if not self.skip:self.a.append(d)
def get(i):
 u=S[i]['url'];r=dict(source_id=i,url=u,retrieved_at_utc=datetime.now(timezone.utc).isoformat())
 try:
  with urlopen(Request(u,headers={'User-Agent':'Mozilla/5.0'}),timeout=25) as a:b=a.read();r.update(http_status=a.status,final_url=a.url)
  p=B/'captures'/f'{i}.html';p.write_bytes(b);h=T();h.feed(b.decode('utf-8','replace'));lines=[' '.join(x.split()) for x in ''.join(h.a).splitlines() if x.strip()];t=B/'captures'/f'{i}.txt';t.write_text('\n'.join(f'{k:04}: {l}' for k,l in enumerate(lines,1))+'\n');r.update(capture_path=str(p.relative_to(R)),capture_sha256=hashlib.sha256(b).hexdigest(),text_path=str(t.relative_to(R)),text_sha256=hashlib.sha256(t.read_bytes()).hexdigest(),capture_kind='retained_original_html')
 except Exception as e:r.update(http_status=getattr(e,'code',None),error=str(e),capture_path=None,capture_sha256=None,capture_kind='raw_unavailable_not_source_evidence')
 return r
rows=list(ThreadPoolExecutor(max_workers=7).map(get,ids));(B/'capture-manifest.json').write_text(json.dumps(dict(date='2026-10-30',records=rows),indent=2)+'\n');print(json.dumps(rows,indent=2))
