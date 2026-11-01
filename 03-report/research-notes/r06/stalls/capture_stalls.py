from pathlib import Path
from html.parser import HTMLParser
import urllib.request,json,hashlib,datetime
ROOT=Path(__file__).resolve().parents[4]
OUT=Path(__file__).resolve().parent
(OUT/'captures').mkdir(exist_ok=True)
class Text(HTMLParser):
 def __init__(self):super().__init__();self.skip=0;self.buf=[]
 def handle_starttag(self,t,a):
  if t in ('script','style','noscript'):self.skip+=1
  if t in ('div','p','li','br','h1','h2','h3','h4','tr'):self.buf.append('\n')
 def handle_endtag(self,t):
  if t in ('script','style','noscript') and self.skip:self.skip-=1
  if t in ('div','p','li','h1','h2','h3','h4','tr'):self.buf.append('\n')
 def handle_data(self,d):
  if not self.skip:self.buf.append(d)
urls=[('STL6-S01','https://schools.westsussex.gov.uk/Article/184856'),('STL6-S02','https://schools.westsussex.gov.uk/Article/194014'),('STL6-S03','https://www.niauditoffice.gov.uk/publications/civil-service-human-resource-management-system-cancellation-payroll-project'),('STL6-S04','https://www.gets.govt.nz/EPL/ExternalTenderDetails.htm?id=34909219')]
rows=[]
for ident,url in urls:
 req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'})
 with urllib.request.urlopen(req,timeout=40) as r:data=r.read();status=r.status;final=r.url
 raw=OUT/'captures'/f'{ident}.html';raw.write_bytes(data)
 p=Text();p.feed(data.decode('utf-8',errors='replace'));txt='\n'.join(' '.join(x.split()) for x in ''.join(p.buf).splitlines() if x.strip())
 text=OUT/'captures'/f'{ident}.txt';text.write_text(txt+'\n')
 rows.append(dict(candidate_id=ident,url=url,final_url=final,http_status=status,retrieved_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),capture_path=str(raw.relative_to(ROOT)),capture_sha256=hashlib.sha256(data).hexdigest(),text_path=str(text.relative_to(ROOT)),text_sha256=hashlib.sha256(text.read_bytes()).hexdigest(),capture_kind='retained_original_html'))
 print(ident,status,len(data))
(OUT/'capture-manifest.json').write_text(json.dumps({'date':'2026-10-29','records':rows},indent=2)+'\n')
