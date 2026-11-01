from pathlib import Path
from urllib.parse import urlsplit,urlunsplit,parse_qsl,urlencode,unquote
import json,hashlib,re
R=Path(__file__).resolve().parents[2];B=R/'04-table/research-notes/t01';O=R/'08-qa/t01-review';checks=[]
def read(p):return json.loads(p.read_text())
def ck(v,n):checks.append({'name':n,'passed':bool(v)});assert v,n
def hash(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def norm(u):
 p=urlsplit(u);return urlunsplit((p.scheme,p.netloc.lower(),p.path.rstrip('/'),urlencode(sorted((k,v)for k,v in parse_qsl(p.query)if not k.lower().startswith('utm_'))),''))
S=read(R/'02-evidence/registers/sources.json')['records'];C=read(R/'02-evidence/registers/claims.json')['records'];F=read(R/'05-analysis/findings.json')['records'];sid={s['source_id']:s for s in S};cid={c['claim_id']:c for c in C};mp=read(R/'08-qa/T01-record-map.json');model=read(R/'04-table/T01-model-map.json');hyp=read(R/'04-table/T02-proposition-hypotheses.json')
ck(len(S)==217 and len(C)==407 and len(F)==81,'canonical counts 217 sources 407 claims 81 preserved findings')
oldS=read(B/'root/sources-before.json')['records'];oldC=read(B/'root/claims-before.json')['records'];oldF=read(B/'root/findings-before.json')['records']
ck(len(oldS)==191 and len(oldC)==355 and len(oldF)==81,'correct before-work canonical snapshot counts')
ck(C[:355]==oldC,'all prior 355 claims preserved exactly')
ck(F==oldF,'all prior 81 findings preserved exactly with no Table demand findings invented')
for old in oldS:
 new=sid[old['source_id']]
 ck({k:v for k,v in old.items()if k not in ['additional_reviews','related_topic_ids']}=={k:v for k,v in new.items()if k not in ['additional_reviews','related_topic_ids']},'source base unchanged '+old['source_id'])
 ck(all(x in new.get('additional_reviews',[])for x in old.get('additional_reviews',[])),'earlier source reviews preserved '+old['source_id'])
 ck(set(old.get('related_topic_ids',[]))<=set(new.get('related_topic_ids',[])),'earlier topics preserved '+old['source_id'])
ck(len(mp['source_map'])==26 and len(mp['claim_map'])==52 and mp['new_source_routes']==26 and mp['new_claim_records']==52,'bounded canonical append exactly 26 routes and52 records')
ck(len({norm(s['url'])for s in S})==len(S),'canonical source URLs deduplicated without stripping substantive query')
for folder in ['research-products','membership-community','forums-events','root']:
 sources=read(B/folder/'source-candidates.json')
 for s in sources.get('records',[]):
  n=sid[mp['source_map'][s['candidate_id']]]
  ck(n['candidate_detail']==s,'source candidate retained exactly '+s['candidate_id'])
  ck(n['capture_path']==s.get('capture_path') and n['capture_sha256']==s.get('capture_sha256'),'source raw capture preserved '+s['candidate_id'])
 for c in read(B/folder/'claim-candidates.json')['records']:
  n=cid[mp['claim_map'][c['candidate_id']]]
  ck(n['candidate_detail']==c,'claim candidate retained exactly '+c['candidate_id'])
  expected=set(mp['source_map'].get(x,x)for x in c.get('canonical_source_ids',[])+c.get('source_candidate_ids',[])+c.get('source_ids',[]))
  ck(set(n['source_ids'])==expected,'claim exact canonical support '+c['candidate_id'])
  ck(n['claim_text']==c.get('claim_text',c.get('claim')) and n['interpretation_limits']==c['limitations'],'claim wording and limits preserved '+c['candidate_id'])
for x in read(R/'08-qa/T01-baseline-manifest.json')['files']:
 ck(hash(R/x['path'])==x['sha256'],'120-file preservation '+x['path'])
for x in read(R/'08-qa/T01-captures.json')['files']:
 ck(hash(R/x['path'])==x['sha256'],'T01 capture inventory hash '+x['path'])
 if x['path'].endswith('.parsed.txt')or'/parsed/'in x['path']:ck(x['kind']=='parsed_original_text','derived text not promoted to original '+x['path'])
 if x['path'].endswith('.html'):ck(x['kind']=='retained_original_html','HTML provenance classification '+x['path'])
 if x['path'].endswith('.png'):ck(x['kind']=='rendered_pdf_page','PDF render not promoted to raw original '+x['path'])
ck([m['model_id']for m in model['models']]==[f'T01-M{i:02}'for i in range(1,7)]and model['model_count']==6,'exact six ordered normalized models')
ck(len({m['mechanism']for m in model['models']})==6,'six distinct named mechanisms not six undifferentiated suppliers')
ck(not model['ranking'] and not model['commercial_validation'],'comparison is not ranking or validated business demand')
for m in model['models']:
 i=m['model_id'];ck(set(m['source_ids'])<=set(sid)and set(m['claim_ids'])<=set(cid),'canonical model references resolve '+i)
 expected=set(v for c in m['claim_ids']for v in cid[c]['source_ids']);ck(set(m['source_ids'])==expected,'model source coverage exact claim union '+i)
 d=read(R/m['raw_model_candidate_path']);raw=next(v for v in d.get('models',d.get('records',[]))if v.get('candidate_id',v.get('candidate_model_id',v.get('model_id')))==m['raw_model_candidate_id'])
 rawclaims=raw.get('claim_candidate_ids',raw.get('claim_candidates',[]));ck(set(m['claim_ids'])=={mp['claim_map'][x]for x in rawclaims},'normalized model claims match author pack '+i)
 ck((R/m['review_note']).is_file(),'underlying model review retained '+i)
 ck(not m['actual_demand_validated']and not m['adopted_jga_model']and not m['jga_price_input'],'conditional transfer not adopted or price input '+i)
 ck(bool(m['comparability'])and bool(m['critical_transfer_limit']),'fit and transfer boundary stated '+i)
ck(model['participant_observations']==[]and model['actual_Table_conversations']==[]and model['financial_inputs']==[],'T01 actual evidence and money arrays blank')
ck(model['new_mandatory_questions']==0 and model['original_fourteen_questions_unchanged'],'no core question expansion')
ck([x['hypothesis_id']for x in hyp['hypotheses']]==[f'T02-H{i:02}'for i in range(1,5)],'four distinct proposition hypotheses')
for x in hyp['hypotheses']:
 ck(not x['validated']and x['status']=='untested_design_hypothesis'and x['actual_supporting_contributions']==[],'hypothesis remains untested '+x['hypothesis_id'])
 ck(bool(x['test'])and bool(x['counter_signal'])and bool(x['not_established']),'hypothesis has disconfirmation and limits '+x['hypothesis_id'])
ck(not hyp['fieldwork_activated']and not hyp['T03_validation_complete']and hyp['actual_interviews']==0 and hyp['actual_commitments']==[]and hyp['price_recommendations']==[],'T02 does not claim collection or demand')
for p in ['05-analysis/observations.json','05-analysis/charts.json','04-table/financial-inputs.json']:ck(read(R/p)['records']==[],'unperformed actual array stays empty '+p)
ck(not read(R/'01-method/collection-pack-v0.1/REVIEW-DECISIONS.json')['collection_ready'],'collection review gates not bypassed')
textpaths=['04-table/T01-COMPARABLE-MODELS.md','04-table/T01-COMPARABLE-MATRIX.md','04-table/T01-DESKTOP-READOUT.md','04-table/T02-PROPOSITION-WORKING-NOTE.md']
for rel in textpaths:
 p=R/rel;text=p.read_text();ck(set(re.findall(r'CLM-\d{4}',text))<=set(cid),'synthesis claim references resolve '+rel)
 for u in re.findall(r'\]\(([^)]+)\)',text):
  if not u.startswith(('https://','http://','#')):ck((p.parent/unquote(u.split('#',1)[0])).resolve().exists(),'synthesis local link '+u)
alltext='\n'.join((R/p).read_text()for p in textpaths)
ck('publicly offered product architectures'in alltext and 'workable product architectures'not in alltext,'public offer not promoted to demonstrated viable economics')
ck('separately defined combination' in alltext and 'Choose explicitly between an access event and a research partnership'not in alltext,'commercial/research combination possible with separate explicit rights')
ck('provider-side leaders also appear'in alltext,'CPO not made employer-only or vendor-free')
ck('2021'in alltext and '2025'in alltext and 'forthcoming'in alltext,'dated help/editions and announced future event transparent')
price=model['models'][2]['public_price'];ck(price['value']==1122 and price['currency']=='GBP'and price['period']=='year'and 'unless otherwise stated'in price['vat']and not price['jga_forecast_input'],'published organisation-year price has unit tax qualifier and no forecast use')
ck(model['models'][4]['public_price']['forum_fee']is None and model['models'][4]['public_price']['editorial_subscription_price']==0,'CPO free editorial vs unknown forum fee separated')
ck('Adjacent L&D'in model['models'][5]['comparability'],'iVentiv not falsely presented as payroll-specific product')
for ident,status in [('CLM-0051','quarantined_conflicting'),('CLM-0052','quarantined_conflicting'),('CLM-0167','hold_numeric_reuse'),('CLM-0168','hold_numeric_reuse'),('CLM-0218','hold_universal_ui_behaviour'),('CLM-0392','hold_numeric_reuse')]:ck(cid[ident]['status']==status,'prior hold remains '+ident)
reviewpaths=textpaths+['04-table/T01-model-map.json','04-table/T02-proposition-hypotheses.json','08-qa/T01-record-map.json','08-qa/T01-captures.json']
result={'status':'passed_for_internal_T01_desktop_comparison_and_T02_hypothesis_preparation','date':'2026-10-29','check_count':len(checks),'checks':checks,'six_models_reviewed':True,'actual_fieldwork':False,'commercial_validation':False,'publication_approval':False,'open_substantive_issues':[],'wording_refinements_applied':['Publicly offered architecture is not proved commercial viability.','Research and access can be a separately defined transparent combination; neither has default private-data/meeting rights.'],'provisional_issue_closed':'CIPP 2026 tier-footnote expiry verified; missing-year concern disproved.','reviewed_artifacts':[{'path':p,'sha256':hash(R/p)}for p in reviewpaths],'allowed_following_status_only_changes':['status','review_basis']}
(O/'integration-checks.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n');print(json.dumps({k:v for k,v in result.items()if k not in ['checks','reviewed_artifacts']},indent=2))
