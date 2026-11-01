from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parents[4];P=Path(__file__).resolve().parent;DATE='2026-10-29'
def read(p):return json.loads(p.read_text())
def write(n,d):(P/n).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
sources={x['source_id']:x for x in read(R/'02-evidence/registers/sources.json')['records']}
manifest=read(P/'capture-manifest.json');fresh={x['id']:x for x in manifest['records']}
reuses=[]
for ident,loc,result in [
('SRC-0202','PDF/printed11 B1 bundled strategic/review/investment status;12 E1 management OR investment influences;32 methodology','Bundled status and general influence items do not isolate an approved project, allocated resources, amount/period or delivered result. Commissioned pooled six-market survey, large-employer skew; item bases/routing/weights unknown. Country samples known; not UK item results.'),
('SRC-0033','PDF33 Table6 urgent HR challenges and Table7 separate AI employer agreement statements; methods re-read at PDF4/32','Different item frames and separate marginal agreement statements cannot create a respondent-level exploration-to-investment-to-outcome pipeline. HR/workplace AI is not necessarily payroll AI. No percentages or longitudinal transition adopted.'),
('SRC-0034','PDF2 scope/method;11 payroll-related priorities and separate recommendations','Pooled 16-country HR/employee study. Published payroll priority list lacks the exact underlying question/item valid base in the inspected page. Priorities/recommendations are not approved funding or completed delivery.'),
('SRC-0011','Methodology; Chapter2 finding8 exact feature-desire question; original published V2-01 chart','Current feature preferences, not confirmed willingness to pay/approved budgets. New branding/customisation figure discrepancy12chart/13prose held; prior switching/investment conflicts remain. Mixed payroll/HR/finance/bureau respondents and item-valid bases unknown.'),
('SRC-0070','Printed15 employer qualification offer/support;16 personal undertaken/current/planned qualifications; foreword/conclusion sample scope','Employer-reported qualification support and respondent personal qualification status have different units/routes. Personal plans are not employer-funded priorities or successful completion. Mixed in-house/provider professional sample, exact achieved/item bases/fieldwork unknown.')]:
 s=sources[ident];row=dict(source_id=ident,url=s['url'],locator=loc,review_status='selected_original_sections_reinspected_for_R07',review_result=result)
 if ident in fresh:
  row.update(capture_path=fresh[ident]['path'],capture_sha256=fresh[ident]['sha256'],text_path=fresh[ident]['text_path'],text_sha256=fresh[ident]['text_sha256'])
 else:
  row.update(capture_path=s['capture_path'],capture_sha256=s['capture_sha256'],text_path=str((P/'captures'/f'{ident}-fulltext.txt').relative_to(R)),text_sha256=sha(P/'captures'/f'{ident}-fulltext.txt'))
 row['visually_inspected_pdf_pages']={'SRC-0202':[11,12,32],'SRC-0033':[33],'SRC-0034':[2,11]}.get(ident,[])
 if ident=='SRC-0011':row['published_chart_review']=fresh['MP-feature']
 reuses.append(row)
write('source-candidates.json',dict(date=DATE,records=[],reused_canonical_sources=reuses,new_independent_datasets=0))
rows=[
('PRI7-C01',['SRC-0202'],'Azets B1 presents a response combining strategic priority, active review and investment. That composite status does not separately establish which specific proposal was approved or what funding, resource amount or delivery followed.','survey_item_definition_boundary','PDF/printed11 B1; methodology32','Pooled commissioned sample; country sample counts do not establish UK item results or item-valid bases. No composite percentage becomes a funded share.'),
('PRI7-C02',['SRC-0202'],'Azets E1 asks what factors influence how the organisation currently manages OR invests in payroll. It identifies reported influences on a broad activity, not a ranking of approved investment projects, budget allocation or causal purchase drivers.','survey_item_definition_boundary','PDF/printed12 E1; methodology32','Do not label all respondents as currently investing or all selected factors as actual deal triggers. No amount, project or funded decision is identified by the item.'),
('PRI7-C03',['SRC-0033'],'SD Worx reports exploring, investing, scaled deployment and significant HR-AI outcomes as separate employer-agreement statements. Their marginal percentages cannot reconstruct a respondent-level sequential investment pipeline or quantify conversion/loss between stages.','survey_measure_and_unit_boundary','PDF33 Table7; methods4/32','The broader workplace/HR AI wording is not a common payroll deployment definition. Respondent links, item-valid bases/weights and independently assessed outcomes not inspected. No numerical difference or causal conversion adopted.'),
('PRI7-C04',['SRC-0033','SRC-0034'],'SD Worx distinguishes urgent HR challenges from a separate payroll-priority list and from publisher recommendations. Those question frames cannot be combined into one funded payroll investment ranking.','survey_frame_and_prescription_boundary','FullreportPDF32–33 Table6; payrollthematicPDF10–11, method2','Pooled study contexts, not a UK approved-spend ranking. Exact underlying payroll-priority wording/item valid base not shown on inspected list. A narrative/category difference across different frames is not automatically a numeric inconsistency.'),
('PRI7-C05',['SRC-0011'],'Moorepay asks what respondents would most like to see from their payroll provider. Feature-desire responses can inform hypotheses for questions about automation, reporting and self-service, but do not establish a purchase, available budget or need to change provider.','survey_preference_not_commitment','AnnualsurveyChapter2 finding8; publishedV2-01chart and methodology','Mixed professional/buyer/provider roles, item base/routing unestablished. No feature percentages, change forecast or supplier-caused outcome adopted. Existing numerical quarantines remain.'),
('PRI7-C06',['SRC-0070'],'CIPP distinguishes organisations offering qualification-related support from respondents having undertaken, currently taking or planning qualifications. Employer support, personal career intent and completed training are different claims.','survey_unit_and_time_boundary','Originalhostedtext printed15–16; sample contextforeword/conclusion','Mixed professional sample and reported practices; no verified payment, amount, completion or usable capability. No planned qualification automatically becomes organisational approved training investment.'),
('PRI7-C07',['SRC-0011'],'The current Moorepay annual prose says branding/customisation13%, while the original V2-01 feature chart labels12%. The exact branding/customisation value should not be reused until reconciled.','source_conflict_numeric_hold','Annualfinding8 branding/customisationprose and V2-01chart','New targeted conflict; do not average, select a preferred value, or treat other known conflicts as resolved. This is not evidence the whole study is false or feature priorities are funded.',),
('PRI7-C08',['SRC-0202','SRC-0033','SRC-0034','SRC-0011','SRC-0070'],'For R07, preserve the priority’s actual unit, wording, timeframe and evidence status; separately establish organisational approval, funding/resources, delivery and observed result where known. A theme can be relevant without a funded project, and planned/approved/delivered statuses need not be a single linear ladder.','researcher_analytical_application','Cross-source application of item/actor/time boundaries; existingQ005 provides interview basis','No new compulsory questions or stage score. Up to two unaided priorities under unchangedQ005; preserve no priority, not known, not applicable and non-disclosure. No market-wide ranking or forecast populated.')]
claims=[]
for ident,ss,txt,cl,loc,lim in rows:
 claims.append(dict(candidate_id=ident,source_ids=ss,claim_text=txt,evidence_class=cl,locator=loc,limitations=lim,review_mode='Source-specific original item text inspected; Azets11/12/32, SDWorxfull33 and thematic2/11 visually checked; CIPP hosted HTML and Moorepay body/chart separately inspected. No funding document, employer interview or product trial.',value=None,unit=None,denominator=None,population='Source-specific reported measures; not a new JGA practitioner sample',time_period='Each original publication/fieldwork/item timeframe preserved; no 2027 forecast'))
# Avoid attributing PDF checks to HTML-only claims.
for x in claims:
 if x['candidate_id'] in ['PRI7-C01','PRI7-C02']:x['review_mode']='Original Azets PDF11/12/32 rendered and visually inspected; existing raw retained and hashes checked. No employer funding or budget document.'
 elif x['candidate_id']=='PRI7-C03':x['review_mode']='Original SDWorx full PDF33 rendered and visually inspected; methods4/32 text re-read. Separate marginal statements, no participant linkage.'
 elif x['candidate_id']=='PRI7-C04':x['review_mode']='Original SDWorx fullPDF33 and thematic2/11 rendered and visually inspected; full32 and thematic10 text re-read. No underlying questionnaire or microdata inspected.'
 elif x['candidate_id'] in ['PRI7-C05','PRI7-C07']:x['review_mode']='Fresh original annual HTML/body and published V2-01 chart captured; chart visually inspected. No actual buyer or funding verification.'
 elif x['candidate_id']=='PRI7-C06':x['review_mode']='Fresh original CIPP hosted HTML text inspected at printed15/16; no PDF visual-inspection claim or employer payment verification.'
 if x['candidate_id']=='PRI7-C07':x['recommended_canonical_status']='hold_numeric_reuse';x['status']='hold_numeric_reuse';x['numeric_reuse']='hold_until_source_reconciliation'
write('claim-candidates.json',dict(date=DATE,records=claims))
# All current/reused capture paths are explicit, with raw originals distinct from parsed text and page renders.
files={}
for row in manifest['records']:
 for key,sha_key,kind in [('path','sha256',row['kind']),('text_path','text_sha256','parsed_text')]:
  if row.get(key):files[row[key]]=dict(path=row[key],sha256=row[sha_key],kind=kind)
for row in reuses:
 for key,sha_key,kind in [('capture_path','capture_sha256','retained_original_pdf' if row['capture_path'].endswith('.pdf') else 'retained_original_html'),('text_path','text_sha256','parsed_text')]:
  files[row[key]]=dict(path=row[key],sha256=row[sha_key],kind=kind)
for f in (P/'captures').glob('*.png'):
 rel=str(f.relative_to(R));files[rel]=dict(path=rel,sha256=sha(f),kind='published_chart_asset' if f.name=='MP-feature.png' else 'rendered_pdf_page',visually_inspected=True)
# Screened Deloitte text is not a priority claim source and is clearly excluded.
f=P/'captures/SRC-0040-fulltext.txt';files[str(f.relative_to(R))]=dict(path=str(f.relative_to(R)),sha256=sha(f),kind='screened_parsed_text_not_relied_on')
write('capture-manifest.json',dict(date=DATE,records=manifest['records'],files=list(files.values()),raw_originals_and_parsed_text_distinct=True))
write('search-review-log.json',dict(date=DATE,queries=['site.sdworx.co.uk payroll2026 priorities investment','site.cipp.org.uk futurepayroll2026 priority investment research','site.brightsg.com payroll ai report2026 study priorities'],selected_canonical_routes=['SRC-0202','SRC-0033','SRC-0034','SRC-0011','SRC-0070'],new_routes_required=False,screened_not_adopted=[dict(source_id='SRC-0040',reason='Operational mega-enterprise benchmark not selected as future-priority/funded-spend evidence in this strand; existing numeric holds unchanged.'),dict(source_id='SRC-0041',reason='Landing advertises AI interest/use/trust; full report/method not obtained. No gated form submitted or AI interest converted into funded priorities.'),'Secondary AI-payroll priority article and compensation/HR studies outside the specific selected population were not used to add a link quota.'],pdf_skill_read=True,visually_inspected_pdf_pages={'SRC-0202':[11,12,32],'SRC-0033':[33],'SRC-0034':[2,11]},published_chart_visually_inspected='MoorepayV2-01',no_item_percentages_adopted=True,external_actions=[]))
checks=[]
for x in files.values():checks.append(dict(check='Filehash '+x['path'],passed=(R/x['path']).is_file() and sha(R/x['path'])==x['sha256']))
checks.append(dict(check='No new source routes/datasets claimed',passed=len(reuses)==5))
checks.append(dict(check='Eight bounded claim/design/hold records',passed=len(claims)==8))
checks.append(dict(check='No item percentage adopted as investment/funded share',passed=all(x['value'] is None for x in claims)))
checks.append(dict(check='New branding value conflict explicitly held',passed=claims[6]['recommended_canonical_status']=='hold_numeric_reuse'))
checks.append(dict(check='Claim-specific PDF versus HTML review modes',passed=all('visually' not in x['review_mode'] for x in [claims[5]]) and 'V2-01' in claims[6]['review_mode']))
assert all(x['passed'] for x in checks)
write('verification.json',dict(date=DATE,status='passed',check_count=len(checks),checks=checks,new_canonical_sources=0,reused_canonical_sources=5,claim_candidates=8,original_practitioner_observations=0,external_actions=[]))
print('Priority records complete:',len(reuses),'reuses,',len(claims),'claims,',len(files),'retained files,',len(checks),'checks')
