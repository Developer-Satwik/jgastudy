from pathlib import Path
from urllib.parse import urlsplit,urlunsplit,parse_qsl,urlencode,unquote
import json,hashlib,re
R=Path(__file__).resolve().parents[2];W=R.parents[1];B=R/'04-table/research-notes/t01-second-check';O=R/'08-qa/t01-second-review';checks=[]
def read(p):return json.loads(p.read_text())
def hash(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def ck(v,n):checks.append({'name':n,'passed':bool(v)});assert v,n
def norm(u):
 p=urlsplit(u);return urlunsplit((p.scheme,p.netloc.lower(),p.path.rstrip('/'),urlencode(sorted((k,v)for k,v in parse_qsl(p.query)if not k.lower().startswith('utm_'))),''))
S=read(R/'02-evidence/registers/sources.json')['records'];C=read(R/'02-evidence/registers/claims.json')['records'];F=read(R/'05-analysis/findings.json')['records'];sid={s['source_id']:s for s in S};cid={c['claim_id']:c for c in C};mp=read(R/'08-qa/T01-second-check-record-map.json');model=read(R/'04-table/T01-second-challenge-map.json')
oldS=read(B/'before-review/sources.json')['records'];oldC=read(B/'before-review/claims.json')['records'];oldF=read(B/'before-review/findings.json')['records']
ck(len(S)==223 and len(C)==432 and len(F)==81,'canonical223sources432claims81findings')
ck(len(oldS)==217 and len(oldC)==407 and len(oldF)==81,'before-review217sources407claims81findings')
ck(C[:407]==oldC,'old407claimrecords preserved exactly')
ck(F==oldF,'old81findings preserved exactly; no new synthetic/practitioner finding')
for x in oldS:
 n=sid[x['source_id']];ck({k:v for k,v in x.items()if k not in ['additional_reviews','related_topic_ids']}=={k:v for k,v in n.items()if k not in ['additional_reviews','related_topic_ids']},'sourcebase preserved '+x['source_id']);ck(all(y in n.get('additional_reviews',[])for y in x.get('additional_reviews',[])),'oldreview preserved '+x['source_id']);ck(set(x.get('related_topic_ids',[]))<=set(n.get('related_topic_ids',[])),'oldtopic preserved '+x['source_id'])
ck(len({norm(s['url'])for s in S})==len(S),'canonical normalized URLs unique')
ck(mp['new_source_routes']==6 and len(mp['source_map'])==6 and mp['new_claim_records']==25 and len(mp['claim_map'])==25,'sixroute25recordappend')
for f in ['history','market','competitors','root']:
 d=read(B/f/'source-candidates.json')
 for x in d.get('records',[]):
  n=sid[mp['source_map'][x['candidate_id']]];ck(n['candidate_detail']==x,'exactsourcecandidate '+x['candidate_id'])
  for pk,hk in [('capture_path','capture_sha256')]:
   if x.get(pk):ck(hash(R/x[pk])==x[hk],'rawcapturehash '+x['candidate_id'])
  for x2 in x.get('review_extracts',[]):ck(hash(R/x2['path'])==x2['sha256'],'reader/extracthash '+x['candidate_id'])
 for x in d.get('reused_canonical_sources',[]):ck(x['source_id']in sid,'canonicalreuse '+x['source_id'])
 for x in read(B/f/'claim-candidates.json')['records']:
  n=cid[mp['claim_map'][x['candidate_id']]];ck(n['candidate_detail']==x,'exactclaimcandidate '+x['candidate_id']);ck(n['claim_text']==x['claim_text']and n['interpretation_limits']==x['limitations'],'claimtext/limit '+x['candidate_id']);expected=set(mp['source_map'].get(s,s)for s in x.get('source_candidate_ids',[])+x.get('canonical_source_ids',[]));ck(set(n['source_ids'])==expected,'exactclaimsources '+x['candidate_id'])
for x in read(R/'08-qa/T01-second-check-baseline.json')['files']:ck(hash(R/x['path'])==x['sha256'],'131filepreservation '+x['path'])
ck(model['selected_model_ids']==[f'T01-M{i:02}'for i in range(1,7)]and len(model['model_changes'])==6,'sixmodelidentity preserved')
ck(model['original_T02_hypothesis_ids']==[f'T02-H{i:02}'for i in range(1,5)]and not model['hypotheses_replaced'],'fouroriginalhypotheses preserved')
ck(not model['commercial_validation']and not model['ranking']and not model['prior_model_reruns']and not model['prior_recommendation_counts_reused'],'secondchallenge not adoption/rank/demand/rerun')
ck(model['additional_mandatory_questions']==0 and all(model[k]==[] for k in ['participant_observations','actual_Table_conversations','financial_inputs','new_price_recommendations']),'no extramandatory/actual/financial records')
ck([c['condition_id']for c in model['conditions']]==[f'TC{i:02}'for i in range(1,7)],'sixselectiveconditions')
for c in model['conditions']:
 ck(not c['mandatory']and not c['scored']and not c['validated']and c['new_core_questions']==0,'conditionoptional/unvalidated '+c['condition_id']);ck(set(c['claim_ids'])<=set(cid)and bool(c['counterexample'])and bool(c['application']),'conditionevidence/counterexample '+c['condition_id'])
for m in model['model_changes']:ck(set(m['claim_ids'])<=set(cid)and bool(m['transfer_limit']),'modelrefinement scoped '+m['model_id'])
for x in read(R/'08-qa/T01-second-check-captures.json')['files']:
 ck(hash(R/x['path'])==x['sha256'],'captureinventory hash '+x['path'])
 if 'selected-reader' in x['path']:ck(x['kind']=='selected_reader_extract','selectedreader not original/parsed '+x['path'])
 if 'T1H-S03' in x['path']:ck('shell'in x['kind']and'discovery'in x['kind'],'accomplishments shell discoveryonly '+x['path'])
 if Path(x['path']).name=='SRC-0192.html':ck(x['kind']=='retained_application_shell_not_substantive_body','Haysrawshellclass')
 if Path(x['path']).name=='SRC-0192.txt':ck(x['kind']=='parsed_application_shell_not_substantive_body','Haysparsed shellclass')
ck(sid[mp['source_map']['T1R2-S01']]['capture_path']is None,'Chathamnoraworiginalinvented')
ck('T1H-S03'not in mp['source_map'],'Accomplishmentslead notnewsource')
ck('T1H-C04'not in mp['claim_map'],'duplicatehistoryrenewalclaim notmerged')
for ident,status in [('CLM-0051','quarantined_conflicting'),('CLM-0052','quarantined_conflicting'),('CLM-0167','hold_numeric_reuse'),('CLM-0168','hold_numeric_reuse'),('CLM-0218','hold_universal_ui_behaviour'),('CLM-0392','hold_numeric_reuse')]:ck(cid[ident]['status']==status,'previoushold '+ident)
bridge=read(B/'competitors/prior-study-bridge.json');A={x['id']:x for x in read(W/'sites/jga-discovery-report-2026-10-22/output/JGA-Research-Pack/data/all-answers.json')['answers']};I={x['id']:x for x in read(W/'sites/jgafinalcode/dist/data/answer-index.json')};P={x['answer_id']:x for q in read(R/'03-report/research-notes/r08-second-check/competitors/prior-study-bridge.json')['questions']for x in q['answer_links']}
ck(len(bridge['questions'])==3 and bridge['selected_saved_records']==24 and bridge['semantic_rereads']==3,'bridge3questions24saved3semantic')
for x in bridge['provenance']:
 p=Path(x['path']);p=p if p.is_absolute()else W/p;ck(hash(p)==x['sha256'],'bridgeprovenance '+x['role'])
for q in bridge['questions']:
 ck(hashlib.sha256(q['prompt'].encode()).hexdigest()==q['prompt_sha256'],'exactprompthash '+q['question_id']);ck(len(q['answer_links'])==8,'eightanswers '+q['question_id'])
 for x in q['answer_links']:
  n=A[x['answer_id']];ck(n['prompt']==q['prompt']and n['promptHash']==x['prompt_sha256'],'savedprompt '+x['answer_id']);ck(hashlib.sha256(n['fullAnswer'].encode()).hexdigest()==x['full_answer_sha256'],'savedanswerhash '+x['answer_id']);ck(n['fullAnswer']==I[x['answer_id']]['fullAnswer'],'finalindex '+x['answer_id']);ck(n['sourceStatus']==x['source_status'],'sourcestatus '+x['answer_id']);ck(P[x['answer_id']]['full_answer_sha256']==x['full_answer_sha256'],'previousbridge '+x['answer_id'])
ck('Assuming the role is London-based'in A['S11-C-chatgpt-r1']['fullAnswer']and'London'not in A['S11-C-chatgpt-r1']['prompt'],'S11Londonaddition semanticcheck')
ck('weighted scorecard'in A['S02-D-chatgpt-r1']['fullAnswer']and'confidential'in A['S02-D-chatgpt-r1']['prompt'],'S02generatedweights suppliedconfidentialpremise')
ck('named search leader'in A['S02-D-chatgpt-r1']['fullAnswer']and'public evidence'in A['S01-C-chatgpt-r1']['prompt'],'firm/person evidence distinction grounded in savedtext')
ck(bridge['no_model_reruns']and not bridge['recommendation_counts_reused']and not bridge['new_participant_evidence'],'bridge noactualdemandornewtest')
cm=read(B/'competitors/comparator-map.json');ck(len(cm['records'])==7 and cm['recruitment_comparator_count']==6 and cm['JGA_context_count']==1 and cm['not_the_T01_six_business_models'],'all6recruitersplusJGA distinctmodels')
ck(all(not x['actual_Table_buyer']and not x['actual_sponsor']and not x['actual_participant']for x in cm['records']),'noneofcomparators convertedprospect')
route=read(R/'08-qa/T01-second-routing-walkthrough.json')
ck(route['status']=='passed_internal_constructed_T01_second_challenge_walkthrough'and route['route_count']==9 and route['check_count']==173 and all(x['passed']for x in route['checks']),'root9constructed173checks passed')
ck(hash(R/route['model_path'])==route['model_sha256_at_walkthrough'],'constructedwalkthrough exactmaphash')
ck(not route['practitioner_validation']and not route['commercial_validation']and route['actual_participant_cases']==0 and route['new_mandatory_questions']==0 and route['financial_inputs_added']==0 and not route['external_contact'],'constructedroutes notempirical/finance/activation')
conditions={x['condition_id']for x in model['conditions']}
expected={
'TR01':['Preserve the free benefit','incremental'],
'TR02':['actual intended client use','neither internal access'],
'TR03':['Separate research/member eligibility','does not create'],
'TR04':['public dated role','do not infer'],
'TR05':['programme, cohort, person, role','Do not infer'],
'TR06':['checkbox does not silently override','Separately approved'],
'TR07':['separately from attendance','actual, verified, eligible, usable and permissioned'],
'TR08':['Separate received funds','does not prove'],
'TR09':['actual decision/country scope','does not establish demand']}
ck([x['route_id']for x in route['routes']]==[f'TR{i:02}'for i in range(1,10)],'nineorderedrouteapplications')
for x in route['routes']:
 ck(set(x['condition_ids'])<=conditions and set(x['claim_ids'])<=set(cid),'routeconditionclaimlinks '+x['route_id'])
 ck(x['assessment_completed']and not x['actual_participant_case']and not x['empirical_validation']and not x['financial_input_created'],'routeexplicitconstructed '+x['route_id'])
 ck(all(v in x['root_analyst_assessment']for v in expected[x['route_id']]),'independentlyreadrouteboundedinterpretation '+x['route_id'])
paths=['04-table/T01-SECOND-CHECK-READOUT.md','04-table/T01-SECOND-CHECK-MATRIX.md','04-table/T01-second-challenge-map.json','04-table/T02-SECOND-CHECK-REFINEMENTS.md','08-qa/T01-second-check-record-map.json','08-qa/T01-second-check-captures.json','08-qa/T01-second-routing-walkthrough.json']
for rel in paths:
 if rel.endswith('.md'):
  p=R/rel;t=p.read_text();ck(set(re.findall(r'CLM-\d{4}',t))<=set(cid),'proseclaims '+rel)
  for u in re.findall(r'\]\(([^)]+)\)',t):
   if not u.startswith(('https://','http://','#')):ck((p.parent/unquote(u.split('#',1)[0])).resolve().exists(),'localproselink '+rel+' '+u)
t='\n'.join((R/p).read_text()for p in paths if p.endswith('.md'))
for phrase in ['Preserve the free benefit','No audience access, permission, endorsement or Table partnership','This applies only if that mode is adopted','Planning Inspectorate','No gap or demand has been proven','not automatically a sponsor list','No models were rerun','not an additional questionnaire']:
 ck(phrase in t,'integrationguardrail '+phrase)
ck('Neither public offerings nor positive interest supply JGA prices'in t,'no publicoffer toJGAeconomics')
for p in ['05-analysis/observations.json','05-analysis/charts.json','04-table/financial-inputs.json']:ck(read(R/p)['records']==[],'unperformedarrayblank '+p)
ck(not read(R/'01-method/collection-pack-v0.1/REVIEW-DECISIONS.json')['collection_ready'],'WP03notactivated')
result={'status':'passed_for_internal_T01_second_challenge','date':'2026-10-30','check_count':len(checks),'checks':checks,'open_substantive_issues':[],'corrected_issues':['Capture inventory now distinguishes selected reader notes from parsed originals and the Accomplishments discovery shell from substantive original body.'],'manual_review':['Nick moderator role supported by original retrospective, not a formal partnership.','Current primary Chatham Rule FAQs independently reopened; meeting-mode scope preserved.','Planning Inspectorate policy independently opened; employer-specific boundary preserved.','Three original ChatGPT-r1 texts independently reread; other21answers integrity only.','Free practitioner research is retained as promised; additional paid value/rights remain hypotheses.','All nine root constructed applications read and checked: no actual participation, price, rights or commitment inferred.'],'reviewed_artifacts':[dict(path=p,sha256=hash(R/p))for p in paths],'allowed_following_status_only_changes':['status','review_basis'],'actual_fieldwork':False,'commercial_validation':False,'publication_approval':False}
(O/'integration-checks.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n');print(json.dumps({k:v for k,v in result.items()if k not in ['checks','reviewed_artifacts']},indent=2))
