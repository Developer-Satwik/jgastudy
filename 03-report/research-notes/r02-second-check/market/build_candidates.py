from pathlib import Path
import json,hashlib
p=Path(__file__).resolve().parent
logs=json.loads((p/'capture-log.json').read_text())
for r in logs['records']:
 if r.get('path') and r['path'].startswith('JGA-Payroll-Research-2027/'):r['path']=r['path'].split('/',1)[1]
(p/'capture-log.json').write_text(json.dumps(logs,indent=2)+'\n')
cap={r['candidate_id']:r for r in logs['records']}
rows=[
('MKT-S01','Download HMRC Basic PAYE Tools','HM Revenue and Customs','official_product_guidance',None,None,'What it does; Before you start','Free core payroll tool for fewer than ten employees, with prerequisites and stated agent/bookkeeper limitation.','Official feature boundary; not a complete fit recommendation, market need estimate or measurement of operating effort.'),
('MKT-S02','Find payroll software that is recognised by HMRC','HM Revenue and Customs','official_software_recognition_guidance','2022-02-23','2026-10-16','Choosing software; Free payroll software','Recognition supports PAYE online reporting; buyers should check needed features and HMRC does not recommend a product.','Reporting recognition is not comparative quality or end-to-end outcome assurance; listed suppliers can change.'),
('MKT-S03','Pricing Plans Xero UK','Xero','public_supplier_pricing',None,None,'Compare features across plans; Pricing plan details and offer terms','Payroll is bundled or charged per additional person within accounting plans, with separately described payment charges.','Dynamic live supplier list; not a managed payroll quote or total cost of ownership. No exact price is used in the synthesis.'),
('MKT-S04','Payroll Software for Small Business Xero UK','Xero','public_supplier_product_description',None,None,'Automatic RTI submissions; 24/7 online support; Spend less time on payroll','Supplier advertises calculation, reporting, employee/payroll payment functions and online support.','Advertised functions/support do not establish supplier-operated payroll, universal case fit, achieved resolution or independently measured accuracy. Customer agreement statistic and testimonials not adopted.'),
('MKT-S05','Managed Payroll Services for UK Businesses','ADP UK','public_supplier_service_description',None,None,'What managed payroll services actually mean; You provide the information; ADP manages the payroll process','Supplier specifies employer changes/inputs and approval alongside provider processing/checks/reporting/support.','Published offer rather than a signed contract or independently audited delivery. Promotional testimonial/accuracy and savings claims not adopted. Web inspection succeeded; local capture returned403.'),
('MKT-S06','ADP Global Payroll for Multinational Businesses','ADP UK','public_supplier_product_description',None,None,'A unified platform; Global governance; Strategic decision; User experience','Supplier advertises multicountry governance/local expertise, consolidated data/reporting and employee self-service.','No uniform jurisdiction coverage, entitlement or achieved result inferred; country fit and actual contract would require checking. Web inspection succeeded; local capture returned403.')]
sources=[]
for ident,title,publisher,typ,pub,upd,loc,point,limits in rows:
 l=cap[ident]
 sources.append({'candidate_id':ident,'title':title,'publisher':publisher,'url':l['url'],'source_type':typ,'accessed_on':'2026-10-28','published_date':pub,'updated_date':upd,'date_note':'Live original inspected 28 October 2026; precise revision date unknown unless stated.','fieldwork_period':None,'population':None,'sample_size':None,'review_status':'original_relevant_live_sections_inspected_through_web','locator':loc,'supported_point':point,'limitations':limits,'funding_or_commercial_interest':('Official guidance; not a market survey' if publisher=='HM Revenue and Customs' else 'Supplier-authored commercial offer; no independent delivery verification'),'capture_path':l.get('path'),'capture_sha256':l.get('sha256'),'capture_status':l['status'],'reuse_status':'Private verification only; commercial reproduction rights not cleared'})
(p/'source-candidates.json').write_text(json.dumps({'schema_version':'1.0','date':'2026-10-28','status':'candidates_for_parent_review_only','records':sources},indent=2)+'\n')
claims=[]
for i,s in enumerate(sources,1):
 claims.append({'candidate_id':f'MKT-C{i:02}','source_ids':[s['candidate_id']],'locator':s['locator'],'claim_text':s['supported_point'],'evidence_class':('official_guidance_feature_boundary' if i<=2 else 'published_service_or_product_scope'),'population':None,'denominator':None,'question_wording':None,'limitations':s['limitations'],'date':'2026-10-28','value':None,'unit':None,'review_mode':'Relevant original live sections inspected through web; capture status recorded separately','status':'candidate_for_parent_review_not_publication_approved','r02_implication':'Use for contextual gap diagnosis and counterevidence to blanket capability absence, not ranking or achieved-performance claims.'})
(p/'claim-candidates.json').write_text(json.dumps({'schema_version':'1.0','date':'2026-10-28','records':claims},indent=2)+'\n')
root=p.parents[3]
for r in logs['records']:
 if r.get('path'):assert hashlib.sha256((root/r['path']).read_bytes()).hexdigest()==r['sha256']
assert len(sources)==len(claims)==6
assert {x for c in claims for x in c['source_ids']}<=set(s['candidate_id'] for s in sources)
(p/'review-check.json').write_text(json.dumps({'date':'2026-10-28','status':'passed_for_parent_review','source_candidates':6,'claim_candidates':6,'retained_original_html':4,'web_inspected_local_capture_unavailable':2,'hashes_checked':4,'canonical_files_changed':False,'external_actions':[],'review_scope':'Six bounded live primary offers/guidance; context only, no achieved service or procurement scoring.'},indent=2)+'\n')
print('6 source candidates, 6 claim candidates, 4 original HTML hashes checked, 2 web-inspected ADP pages without local capture.')
