from pathlib import Path
from urllib.parse import unquote,urlsplit,urlunsplit,parse_qsl,urlencode
import json,hashlib,re
R=Path(__file__).resolve().parents[2];B=R/'04-table/research-notes/t02-second-check';O=R/'08-qa/t02-second-review';checks=[]
def rd(p):return json.loads(p.read_text())
def ck(v,n):checks.append(dict(name=n,passed=bool(v)));assert v,n
def hs(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def norm(u):
 p=urlsplit(u);return urlunsplit((p.scheme,p.netloc.lower(),p.path.rstrip('/'),urlencode(sorted((k,v)for k,v in parse_qsl(p.query)if not k.lower().startswith('utm_'))),''))
S=rd(R/'02-evidence/registers/sources.json')['records'];C=rd(R/'02-evidence/registers/claims.json')['records'];F=rd(R/'05-analysis/findings.json')['records'];sid={x['source_id']:x for x in S};cid={x['claim_id']:x for x in C}
oldS=rd(B/'before-review/02-evidence/registers/sources.json')['records'];oldC=rd(B/'before-review/02-evidence/registers/claims.json')['records'];oldF=rd(B/'before-review/05-analysis/findings.json')['records'];mp=rd(R/'08-qa/T02-second-check-record-map.json')
ck(len(oldS)==223 and len(oldC)==432 and len(oldF)==81,'correct pre-challenge canonical base223/432/81')
ck(len(S)==225 and len(C)==443 and F==oldF,'two source and11claim append with81findings unchanged')
ck(C[:432]==oldC,'all prior432claims exact preserved')
for old in oldS:
 new=sid[old['source_id']]
 ck({k:v for k,v in old.items()if k not in ['additional_reviews','related_topic_ids']}=={k:v for k,v in new.items()if k not in ['additional_reviews','related_topic_ids']},'prior source base unchanged '+old['source_id'])
 ck(all(x in new.get('additional_reviews',[])for x in old.get('additional_reviews',[])),'prior reviews preserved '+old['source_id'])
 ck(set(old.get('related_topic_ids',[]))<=set(new.get('related_topic_ids',[])),'prior topics preserved '+old['source_id'])
ck(len({norm(x['url'])for x in S})==len(S),'canonical URLs deduplicated preserving substantive query')
ck(mp['new_source_routes']==2 and len(mp['source_map'])==2 and mp['new_claim_records']==11 and len(mp['claim_map'])==11,'two new source/eleven record mapping')
for folder in ['history','market','competitors','root']:
 d=rd(B/folder/'source-candidates.json')
 for x in d.get('records',[]):
  n=sid[mp['source_map'][x['candidate_id']]]
  ck(n['candidate_detail']==x,'source detail exact '+x['candidate_id'])
  ck(n['capture_path']==x.get('capture_path')and n['capture_sha256']==x.get('capture_sha256'),'source original reference exact '+x['candidate_id'])
 for x in rd(B/folder/'claim-candidates.json')['records']:
  n=cid[mp['claim_map'][x['candidate_id']]]
  ck(n['candidate_detail']==x,'claim detail exact '+x['candidate_id'])
  expected=set(mp['source_map'].get(v,v)for v in x.get('canonical_source_ids',[])+x.get('source_candidate_ids',[])+x.get('source_ids',[]))
  ck(set(n['source_ids'])==expected and bool(expected),'exact canonical support '+x['candidate_id'])
  ck(n['claim_text']==x['claim_text']and n['interpretation_limits']==x['limitations'],'claim/limits retained '+x['candidate_id'])
  ck(n['value']is None and n['unit']is None,'no numerical outcome imported '+x['candidate_id'])
asof={x['original_path']:x for x in rd(B/'before-review/manifest.json')['records']}
base=rd(R/'08-qa/T02-second-check-baseline.json')['files'];ck(len(base)==158,'158 baseline records')
for x in base:
 target=R/asof[x['path']]['snapshot_path']if x['path']in asof else R/x['path']
 ck(hs(target)==x['sha256'],'prior/core/client/canonical asof preservation '+x['path'])
for x in asof.values():ck(hs(R/x['snapshot_path'])==x['sha256'],'exact prechallenge snapshot '+x['original_path'])
for x in rd(R/'08-qa/T02-second-check-captures.json')['files']:
 ck(hs(R/x['path'])==x['sha256'],'capture inventory hash '+x['path'])
 if x['path'].endswith('.html'):ck(x['kind']=='retained_original_html','rawHTML classification '+x['path'])
 elif x['path'].endswith('.txt'):ck(x['kind']=='parsed_original_text','parsed not original '+x['path'])
 elif 'reader'in x['path']:ck('reader'in x['kind'],'reader note classification '+x['path'])
sm=rd(R/'04-table/T02-second-challenge-map.json');aid=rd(R/'04-table/T02-offer-fit-aid.json')
ck(sm['original_proposition_ids']==['TP01','TP02','TP03']and sm['original_propositions_preserved'],'same original3propositions')
ck(sm['original_hypothesis_ids']==[f'T02-H{i:02}'for i in range(1,5)],'same original4hypotheses')
ck([x['condition_id']for x in sm['conditions']]==[f'OC{i:02}'for i in range(1,6)],'five ordered selective conditions')
for x in sm['conditions']:
 ck(not x['mandatory']and not x['scored']and not x['validated']and x['new_core_questions']==0,'optional unscored unvalidated condition '+x['condition_id'])
 ck(set(x['claim_ids'])<=set(cid)and bool(x['application'])and bool(x['boundary']),'condition evidence and application '+x['condition_id'])
ck([x['proposition_id']for x in sm['proposition_refinements']]==['TP01','TP02','TP03'],'all three refinement paths')
for x in sm['proposition_refinements']:ck(set(x['claim_ids'])<=set(cid)and set(x['condition_ids'])<={f'OC{i:02}'for i in range(1,6)},'refinement mappings '+x['proposition_id'])
ck(sm['contract_segments_unchanged']==5 and sm['employer_additional_hypothesis_unchanged']and sm['free_full_practitioner_research_preserved']and sm['commissioned_JGA_IP_unchanged'],'scope segments/freebenefit/IP preserved')
ck(sm['report_question_count']==14 and sm['Table_question_IDs_unchanged']and not sm['active_collection_guide_changed']and sm['new_mandatory_questions']==0,'report14/TableIDs/protocol not expanded or activated')
ck(not sm['new_case_quota']and not sm['requires_named_publishable_case']and not sm['scored']and not sm['validated'],'no named case/quota/validation gate invented')
for k in ['actual_offer_exposures','actual_buyer_member_input','actual_rights_grants','actual_commitments','financial_inputs','prices','external_actions']:ck(sm[k]==[],'no unperformed evidence/price '+k)
ck(not sm['prior_model_reruns']and not sm['prior_recommendation_counts_reused'],'no model reruns/counttodemand transfer')
ck(all(v is None for v in aid['blank_offer_fit'].values())and aid['actual_offer_fit_records']==[]and aid['actual_concept_exposures']==[]and aid['financial_inputs']==[]and aid['prices']==[],'optional aid blank')
ck(not aid['new_participant_form']and not aid['new_case_quota']and not aid['practitioner_count_rule_changed'],'fit aid not mandatory data collection or count change')
for p in ['05-analysis/observations.json','05-analysis/charts.json','04-table/financial-inputs.json']:ck(rd(R/p)['records']==[],'actual data remains empty '+p)
ck(not rd(R/'01-method/collection-pack-v0.1/REVIEW-DECISIONS.json')['collection_ready'],'collection not activated')
bridge=rd(B/'competitors/prior-study-bridge-check.json');ck(bridge['check_count']==126 and all(x['passed']for x in bridge['checks'])and bridge['selected_questions']==3 and bridge['selected_saved_records']==24 and bridge['semantic_rereads']==3,'priorbridge126lineagechecks+3semanticrereads boundaries')
ck(hs(R/bridge['bridge_path'])==bridge['bridge_sha256'],'exact checked bridge hash')
textpaths=['04-table/T02-SECOND-CHECK-READOUT.md','04-table/T02-OFFER-FIT-AND-WORDING.md']
for p in textpaths:
 t=(R/p).read_text();ck(set(re.findall(r'CLM-\d{4}',t))<=set(cid),'canonical prose claim links '+p)
 for u in re.findall(r'\]\(([^)]+)\)',t):
  if not u.startswith(('https://','http://','#')):ck(((R/p).parent/unquote(u.split('#',1)[0])).resolve().exists(),'local link '+u)
alltext='\n'.join((R/p).read_text()for p in textpaths)
ck('No named-case quota'in alltext and 'current contract defects and corrections remain covered'in alltext.lower(),'usable aggregate input and defect remedies preserved')
ck('An unshown variant is unknown'in alltext and 'not an ordered funnel'in alltext,'feedback contextual not ordinal/absence inference')
ck('edition already commissioned or complete'in alltext and 'exactly what that support funds'in alltext,'stage-appropriate partner wording')
ck('New evidence or client-specific research would need a separate scope'in alltext,'briefing boundary explicit')
ck('No need to be unique'in alltext and 'format alone'in alltext,'not a false novelty prerequisite')
for ident,status in [('CLM-0051','quarantined_conflicting'),('CLM-0052','quarantined_conflicting'),('CLM-0167','hold_numeric_reuse'),('CLM-0168','hold_numeric_reuse'),('CLM-0218','hold_universal_ui_behaviour'),('CLM-0392','hold_numeric_reuse')]:ck(cid[ident]['status']==status,'prior numerical/UI hold preserved '+ident)
routepath=R/'08-qa/T02-second-routing-walkthrough.json'
if routepath.exists():
 routes=rd(routepath);ck(all(x['passed']for x in routes['checks']),'root constructedroute checks pass')
 ck(not routes['practitioner_validation']and not routes['commercial_validation']and routes['actual_participant_cases']==0,'constructed routes not empirical validation')
 ck(routes['route_count']==8 and routes['check_count']==199 and [x['route_id']for x in routes['routes']]==[f'OR{i:02}'for i in range(1,9)],'eight constructed applications199rootchecks')
 ck(routes['model_sha256_at_walkthrough']==hs(R/'04-table/T02-second-challenge-map.json'),'constructed assessments exact draftmaphash')
 for x in routes['routes']:
  ck(x['assessment_completed']and not x['actual_participant_case']and not x['empirical_validation']and not x['financial_input_created'],'constructed assessment not actual evidence '+x['route_id'])
  ck(set(x['claim_ids'])<=set(cid)and set(x['condition_ids'])<={f'OC{i:02}'for i in range(1,6)},'constructed route links '+x['route_id'])
 reviewpaths=textpaths+['04-table/T02-second-challenge-map.json','04-table/T02-offer-fit-aid.json','08-qa/T02-second-check-record-map.json','08-qa/T02-second-check-captures.json','08-qa/T02-second-routing-walkthrough.json']
else:raise AssertionError('Awaiting root constructed route file for final independent application review')
result=dict(date='2026-10-30',status='passed_for_internal_T02_second_challenge',check_count=len(checks),checks=checks,open_substantive_issues=[],manual_review=['Source bodies and exact contextual claims checked:ONS analogy,ISG published-study inquiry and dated guide,iVentiv advertised inventory,Oakleaf follow-through format only.','Current working agreement section6 governs included defects/corrections and written changes; no new fee/SLA.','Three original ChatGPT-r1 texts independently reread; other21 lineage/integrity only.','Released-use fit does not require named/detailed case from every contributor or reduce contracted report/freebenefit.','Stage-appropriate scripts used only after unaided needs; feedback relates only to shown concept without funnel/demand inference.','All eight root analyst assessments independently read and checked: no empirical validation, pricing, new scope obligation or actual event.'],reviewed_artifacts=[dict(path=p,sha256=hs(R/p))for p in reviewpaths],allowed_following_status_only_changes=['status','review_basis'],actual_fieldwork=False,commercial_validation=False,publication_approval=False)
(O/'integration-checks.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n');print(json.dumps({k:v for k,v in result.items()if k not in ['checks','reviewed_artifacts']},indent=2))
