from pathlib import Path
from html.parser import HTMLParser
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime,timezone
import urllib.request,json,hashlib
R=Path.cwd();P=R/'03-report/research-notes/r07-second-check/competitors'
rows=[('C7S-S01','https://www.theportfoliogroup.com/how-payroll-skills-are-changing-in-2026/'),('C7S-S02','https://www.frazerjones.com/market-insight/payroll/how-to-build-and-retain-a-high-performing-payroll-team-leadership-insights-from-andrea-wraight-head-of-pay-benefits/'),('C7S-S03','https://www.oakleafpartnership.com/news-views/market-insights-payroll-reward'),('SRC-0116','https://middlemore.co.uk/payroll-search/'),('SRC-0192','https://salary-guide.hays.co.uk/salary-guide-2025'),('SRC-0193','https://www.roberthalf.com/gb/en/insights/salary-guide'),('SRC-0113','https://jgarecruitment.com/payroll-recruitment/')]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
class Text(HTMLParser):
 def __init__(self):super().__init__();self.skip=0;self.out=[]
 def handle_starttag(self,t,a):
  if t in ['script','style']:self.skip+=1
  if t in ['h1','h2','h3','p','li','br','div']:self.out.append('\n')
 def handle_endtag(self,t):
  if t in ['script','style']:self.skip=max(0,self.skip-1)
 def handle_data(self,d):
  if not self.skip:self.out.append(d)
def fetch(row):
 ident,url=row;x=dict(id=ident,url=url,retrieved_at_utc=datetime.now(timezone.utc).isoformat(),capture_path=None,capture_sha256=None)
 try:
  res=urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=35);b=res.read();x.update(http_status=res.status,final_url=res.url)
  p=P/'captures'/f'{ident}.html';p.write_bytes(b);x.update(capture_path=str(p.relative_to(R)),capture_sha256=sha(p),capture_kind='retained_original_html')
  h=Text();h.feed(b.decode('utf-8',errors='replace'));s='\n'.join(' '.join(z.split()) for z in ''.join(h.out).split('\n') if z.strip());p=P/'captures'/f'{ident}.txt';p.write_text(s+'\n');x.update(text_path=str(p.relative_to(R)),text_sha256=sha(p))
 except Exception as e:x.update(http_status=getattr(e,'code',None),error=str(e),capture_kind='raw_unavailable')
 return x
with ThreadPoolExecutor(max_workers=7) as e:out=list(e.map(fetch,rows))
(P/'capture-manifest.json').write_text(json.dumps({'date':'2026-10-29','records':out},indent=2)+'\n')
for r in out:print(r['id'],r.get('http_status'),r.get('error',''),r.get('capture_path'))
