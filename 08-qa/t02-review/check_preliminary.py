from pathlib import Path
import json,re,hashlib
from urllib.parse import unquote
R=Path(__file__).resolve().parents[2];C=[]
def rd(p):return json.loads((R/p).read_text())
def ck(t,n):C.append({'name':n,'passed':bool(t)});assert t,n
claims={r['claim_id']for r in rd('02-evidence/registers/claims.json')['records']}
bs=rd('04-table/T02-buyer-segments.json');uses=rd('04-table/T02-use-and-entitlement-options.json');vm=rd('04-table/T02-validation-map.json')
ck([r['segment_id']for r in bs['records']]==[f'BS{i:02}'for i in range(1,7)],'Five contract segments and additional employer hypothesis')
ck(bs['contract_segment_ids']==[f'BS{i:02}'for i in range(1,6)]and bs['additional_segment_ids']==['BS06'],'Contract segment basis separate from new hypothesis')
for x in bs['records']:
 ck(not x['actual_payer_identified']and not x['actual_purchase_observed']and not x['validated'],'Segment not an actual buyer: '+x['segment_id'])
 ck(bool(x['possible_job'])and bool(x['possible_output_value'])and bool(x['limits']),'Segment job, value and limits: '+x['segment_id'])
ck(set(bs['canonical_claim_ids'])<=claims,'Buyer segment canonical claim references')
ck(uses['actual_rights_grants']==[]and uses['actual_customer_contracts']==[]and not uses['Riseklix_controls_JGA_commissioned_IP'],'Customer options grant no rights or new Riseklix veto')
ck([r['option_id']for r in uses['options']]==[f'RU{i:02}'for i in range(1,9)],'Eight distinct use options')
for x in uses['options']:ck(not x['approved']and bool(x['state'])and bool(x['boundary']),'Use option remains open with boundary: '+x['option_id'])
ck('teaser'in uses['options'][0]['boundary']and 'individual-only'in uses['options'][0]['boundary'],'Free benefit not downgraded or artificially restricted')
ck(set(uses['canonical_support_ids'])<=claims,'Use option canonical references')
ck(vm['version']=='0.2'and not vm['active_collection_guide_changed']and not vm['fieldwork_activated'],'Versioned validation draft not activated')
ck(vm['report_core_questions']==14 and vm['additional_mandatory_report_questions']==0,'Fourteen core questions not expanded')
ck([x['question_id']for x in vm['records']]==[f'B{i:02}'for i in range(1,7)]+[f'M{i:02}'for i in range(1,7)],'Six buyer and six member questions')
ck('B01/B02 before buyer concept; M01 before member benefits.'in vm['presentation_flow'],'Unaided discovery before concept')
for x in vm['records']:ck(not x['all_probes_mandatory'],'Selective probes: '+x['question_id'])
ck(vm['actual_concept_exposures']==[]and vm['actual_responses']==[]and vm['actual_Table_events']==0 and vm['actual_report_contributors']==0 and vm['price_anchors']==[],'No actual concept exposure, data or price')
for x in rd('08-qa/T02-baseline-manifest.json')['files']:ck(hashlib.sha256((R/x['path']).read_bytes()).hexdigest()==x['sha256'],'Prior artifact preservation: '+x['path'])
for p in ['04-table/T02-BUYER-USES-AND-RIGHTS.md','01-method/TABLE-VALIDATION-GUIDES-v0.2.md']:
 text=(R/p).read_text();ck(set(re.findall(r'CLM-\d{4}',text))<=claims,'Prose claim references: '+p)
 for u in re.findall(r'\]\(([^)]+)\)',text):
  if not u.startswith(('http://','https://','#')):ck((R/p).parent.joinpath(unquote(u.split('#')[0])).resolve().exists(),'Local link: '+u)
out={'date':'2026-10-30','status':'passed_preliminary_T02_scope_and_design_integration_pending','check_count':len(C),'checks':C,'actual_fieldwork':False,'publication_approval':False,'commercial_validation':False,'manual_review_basis':'Working agreement sections 4/5/7/8/9, original concept and user instruction; source claims are existing bounded design records, with no new research facts.','provisional_refinement':'Council recognition wording should say it does not by itself authorise attendance disclosure or attribution, because context can still identify someone.'}
(R/'08-qa/t02-review/preliminary-checks.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({k:v for k,v in out.items()if k!='checks'},indent=2))
