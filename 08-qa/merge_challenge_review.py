from pathlib import Path
import json, re, hashlib
from urllib.parse import urlsplit, urlunsplit

ROOT=Path(__file__).resolve().parents[1]
NOTES=ROOT/'03-report/research-notes'
DATE='2026-10-28'

root_records=[
 ('ROOT-C01','The Future of Payroll How AI is Revolutionising the Industry','JGA Recruitment Group','https://jgarecruitment.com/wp-content/uploads/2024/07/The-Future-of-Payroll-How-AI-is-Revolusionising-the-Industry.pdf',None,'JGA publication contents and introductory scope','Contents PDF pp2–4; July2024 URL path is not an independently verified printed publication date','JGA already publishes guidance on AI, governance, skills and readiness; this is positioning evidence, not independent verification of the numerical examples.'),
 ('ROOT-C02','What Are Payroll Leaders Saying About the Future','JGA Recruitment Group','https://jgarecruitment.com/blog/what-are-payroll-leaders-saying-about-the-future/','2026-03-04','JGA original editorial article','Strategy, technology, trust and skills sections','JGA editorial already addresses strategic payroll, technology, data and skills using its podcast lens; it is not a representative survey.'),
 ('ROOT-C03','The Payroll Podcast','JGA Recruitment Group','https://jgarecruitment.com/the-payroll-podcast/',None,'JGA resource description','Programme description','JGA has an established public expert-conversation resource. This does not supply new permissioned participants or establish research ownership.'),
 ('ROOT-C04','PayrollOrg Partners With JGA Ventures to Offer AI Program for Payroll Leaders','PayrollOrg','https://payroll.org/news-resources/news/news-detail/2026/10/20/payrollorg-partners-with-jga-ventures-to-offer-ai-program-for-payroll-leaders','2026-10-20','Primary programme announcement','Programme structure and partnership sections','The announced Nick/JGA Ventures programme includes readiness, governance and business cases. No course uptake, content access or efficacy was evaluated.'),
 ('ROOT-C05','Mandatory payrolling of benefits in kind and expenses interim guidance','HMRC','https://www.gov.uk/guidance/draft-guidance-and-legislation-to-aid-preparation-for-reporting-benefits-in-kind-in-real-time','2025-11-26','Official interim guidance index','Summary and update date 23 September 2026','The manual remains interim and distinguishes planned phased reporting from current practice; recheck before publication.'),
 ('ROOT-C06','The phased introduction of mandatory payrolling for benefits in kind','HMRC','https://www.gov.uk/guidance/draft-guidance-and-legislation-to-aid-preparation-for-reporting-benefits-in-kind-in-real-time/the-phased-introduction-of-mandatory-payrolling-for-benefits-in-kind','2025-11-26','Official interim guidance chapter','Phase 1 list and phase 2 paragraphs; updated23 September2026','The current interim chapter sets specified benefits for April2027 and most others for April2028. These are dated planned milestones, not observed employer readiness or expenditure.'),
 ('ROOT-C07','Getting ready for mandatory payrolling of benefits in kind','HMRC','https://www.gov.uk/guidance/draft-guidance-and-legislation-to-aid-preparation-for-reporting-benefits-in-kind-in-real-time/getting-ready-for-mandatory-payrolling-of-benefits-in-kind','2025-11-26','Official interim guidance chapter','Preparing for transition steps1–3; employee communication; cash flow paragraphs','Preparation involves data flow across providers and functions, software, training, employee communication and cash timing. The guidance does not establish prevalence or a need for replacement software.'),
 ('ROOT-C08','Implementing the Plan to Make Work Pay and Employment Rights Act','Department for Business and Trade','https://www.gov.uk/government/publications/implementing-the-plan-to-make-work-pay-and-employment-rights-act','2026-02-03','Official implementation collection','Update history22 October2026 and linked timeline','The implementation collection was updated22 October2026. Scheduled and consultation-dependent changes must be distinguished from in-force obligations; no payroll prevalence or legal advice inferred.')
]
rr=[]
for ident,title,publisher,url,date,kind,locator,point in root_records:
 rr.append({'candidate_id':ident,'title':title,'publisher':publisher,'url':url,'publication_date':date,
   'source_type':kind,'review_status':'relevant_original_sections_inspected','accessed_on':DATE,
   'locator':locator,'supported_point':point,'limitations':'Context and design use only. Final factual wording, date, rights and any numerical use require publication review.',
   'funding_or_commercial_interest':'JGA commissioning/commercial context' if ident in ['ROOT-C01','ROOT-C02','ROOT-C03','ROOT-C04'] else 'Government guidance',
   'capture_path':None,'capture_sha256':None})
rootfile=NOTES/'challenge-root/source-candidates.json'
rootfile.write_text(json.dumps({'schema_version':'1.0','date':DATE,'records':rr},indent=2,ensure_ascii=False)+'\n')

def read(p):return json.loads(p.read_text())
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
def norm(u):
 p=urlsplit(u);return urlunsplit((p.scheme,p.netloc.lower(),p.path.rstrip('/'),'',''))

sp=ROOT/'02-evidence/registers/sources.json';cp=ROOT/'02-evidence/registers/claims.json'
sources=read(sp);claims=read(cp)
source_by_url={norm(s['url']):s for s in sources['records']}
nexts=max(int(s['source_id'].split('-')[1]) for s in sources['records'])+1
nextc=max(int(c['claim_id'].split('-')[1]) for c in claims['records'])+1
mapping=[]
for folder in ['challenge-history','challenge-economics','challenge-method','challenge-root']:
 f=NOTES/folder/'source-candidates.json'
 for c in read(f)['records']:
  ident=c.get('candidate_id',c.get('source_id'))
  url=c['url'];found=source_by_url.get(norm(url))
  if found:
   sid=found['source_id']
  else:
   sid=f'SRC-{nexts:04}';nexts+=1
   capture=c.get('capture_path')
   if capture:
    assert (ROOT/capture).is_file()
    assert hashlib.sha256((ROOT/capture).read_bytes()).hexdigest()==c['capture_sha256']
   found={'source_id':sid,'title':c['title'],'publisher':c['publisher'],'url':url,
    'source_type':c.get('source_type',c.get('evidence_type','original_source')),
    'review_status':c.get('review_status','original_sections_inspected'),
    'notes':c.get('limitations',c.get('use','Retain original population and dates; context only pending final review.')),
    'accessed_on':DATE,'published_date':c.get('publication_date',c.get('publication_or_update_date')),
    'fieldwork_period':c.get('fieldwork_period'),'population':c.get('population',c.get('population_or_base',c.get('population_and_base'))),
    'geography':None,'sample_size':c.get('sample_size'),'method_available':None,
    'funding_or_commercial_interest':c.get('funding',c.get('funding_or_commercial_interest')),
    'capture_path':capture,'capture_sha256':c.get('capture_sha256'),
    'reuse_status':c.get('reuse_status','Reproduction and redistribution rights not reviewed'),
    'publication_eligibility':'internal_challenge_context_not_final_publication_checked',
    'related_topic_ids':['R01','method'] if folder=='challenge-method' else ['R01','R02','R03','R05','R08'],
    'audit_record_origin':str(f.relative_to(ROOT)), 'challenge_candidate_id':ident,
    'candidate_detail':c}
   sources['records'].append(found);source_by_url[norm(url)]=found
  origin=str(f.relative_to(ROOT))
  old=next((r for r in claims['records'] if r.get('challenge_candidate_id')==ident and r.get('audit_record_origin')==origin),None)
  if old:cid=old['claim_id']
  else:
   cid=f'CLM-{nextc:04}';nextc+=1
   selected=c.get('supported_point',c.get('usable_point'))
   locator=c.get('locator',c.get('locators'))
   if not selected:
    selected=' '.join(item['finding'] for item in c.get('claims',[]));locator='; '.join(item['locator'] for item in c.get('claims',[]))
   # Do not promote context-only numerical findings into publication headlines.
   limits=c.get('limitations') or '; '.join(item.get('use','') for item in c.get('claims',[]))
   claims['records'].append({'claim_id':cid,'source_ids':[sid],'locator':locator,'claim_text':selected,
    'evidence_class':'published_source_context','metric':None,'value':None,'unit':None,'question_wording':None,'denominator':None,
    'population':c.get('population',c.get('population_or_base',c.get('population_and_base'))),'time_period':c.get('fieldwork_period'),
    'support_checked':True,'review_mode':c.get('review_status'),'interpretation_limits':limits,
    'status':'internal_design_context_only','publication_status':'working','audit_record_origin':origin,'challenge_candidate_id':ident})
  mapping.append({'candidate_id':ident,'source_id':sid,'claim_id':cid,'origin':origin})
sources['updated_on']=DATE;claims['updated_on']=DATE
write(sp,sources);write(cp,claims)
write(ROOT/'08-qa/challenge-record-map.json',{'schema_version':'1.0','date':DATE,'records':mapping})

searchpath=ROOT/'02-evidence/registers/searches.json';searches=read(searchpath)
ident='SCH-0007'
if not any(r['search_id']==ident for r in searches['records']):
 searches['records'].append({'search_id':ident,'date':DATE,'purpose':'Second challenge through historical, economic, method, JGA positioning and future-readiness lenses',
  'queries':['CIPP Future of Payroll2020 2022 2024 originals JGA forewords','PayrollOrg2025 Getting the World Paid original','HMRC mandatory benefits payrolling phased2027 2028 interim','JGA own payroll AI ebook and PayrollOrg JGA Ventures announcement','Government Efficiency Framework2025 and Green Book2026','Synergy2026 business case and NAO shared-services audit','Magenta Book case studies and Futures Toolkit2024','MHR payroll paradox and CIPP2024 roundtable'],
  'action':'Inspected original guidance, reports and product descriptions with access limits preserved; no new participants or commercial validation.',
  'related_source_ids':sorted(set(m['source_id'] for m in mapping))})
write(searchpath,searches)

qa={'status':'merged_for_internal_challenge','date':DATE,'candidate_records':len(mapping),'source_records':len(sources['records']),
    'claim_records':len(claims['records']),'new_human_observations':0,'client_drafts_changed':False,'external_actions':[],
    'note':'Context, guidance, case and product records are not interchangeable independent surveys. All require claim-specific final publication checks.'}
write(ROOT/'08-qa/challenge-merge-check.json',qa)
print(json.dumps(qa,indent=2))
