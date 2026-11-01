from pathlib import Path
from urllib.parse import unquote
import json,re,hashlib
R=Path(__file__).resolve().parents[2];checks=[]
def rd(p):return json.loads((R/p).read_text())
def ck(t,n):checks.append({'name':n,'passed':bool(t)});assert t,n
def h(p):return hashlib.sha256((R/p).read_bytes()).hexdigest()
claims={r['claim_id']:r for r in rd('02-evidence/registers/claims.json')['records']}
source_ids={r['source_id']for r in rd('02-evidence/registers/sources.json')['records']}
p=rd('04-table/T02-proposition-map.json');d=rd('04-table/T02-delivery-map.json');u=rd('04-table/T02-use-and-entitlement-options.json');b=rd('04-table/T02-buyer-segments.json');v=rd('04-table/T02-validation-map.json')
ck(len(claims)==432 and len(source_ids)==223 and len(rd('05-analysis/findings.json')['records'])==81,'Canonical counts unchanged:223sources/432claims/81findings')
for x in rd('08-qa/T02-baseline-manifest.json')['files']:ck(h(x['path'])==x['sha256'],'146baseline preservation: '+x['path'])
ck(len(rd('08-qa/T02-baseline-manifest.json')['files'])==146,'146protected baseline artifacts retained')
ck([x['proposition_id']for x in p['propositions']]==['TP01','TP02','TP03'],'Exactly three coherent proposition drafts')
ck(p['original_hypotheses']==[f'T02-H{i:02}'for i in range(1,5)],'Four original hypotheses remain the design basis')
ck(p['selected_T01_models']==6 and p['secondary_model_assumptions_not_adopted'],'Six reviewed mechanisms preserved without adoption')
ck(p['report_free_to_practitioner_preserved']and p['JGA_commissioned_IP_not_restricted_by_drafts'],'Free benefit and JGA commissioned IP preserved')
ck(p['original_report_questions']==14 and p['extra_mandatory_questions']==0,'Fourteen report questions unchanged')
ck(not p['signed_project_scope_changed']and not p['fieldwork_activated']and not p['active_WP03_guide_changed'],'No scope expansion or active collection switch')
for k in ['actual_buyer_validation','actual_member_validation','actual_offer_exposures','actual_rights_grants','financial_inputs','external_actions','prices']:ck(p[k]==[],'No unperformed actuals or monetary values: '+k)
for x in p['propositions']:
 i=x['proposition_id'];ck(not x['adopted']and not x['validated']and x['price']is None and x['currency']is None,'Unadopted, unpriced draft: '+i)
 ck(x['actual_customers']==[]and x['actual_commitments']==[]and x['actual_participants']==[]and x['new_mandatory_report_questions']==0,'No invented customers, commitments or questions: '+i)
 ck(bool(x['minimum_payload'])and bool(x['optional_payload'])and bool(x['not_in_core'])and bool(x['free_paid_rule']),'Minimum, optional, boundary and free/paid rule explicit: '+i)
 ck(set(x['canonical_claim_ids'])<=set(claims),'Canonical proposition claim references: '+i)
 for c in x['canonical_claim_ids']:
  ck(bool(claims[c]['interpretation_limits']) and set(claims[c]['source_ids'])<=source_ids,'Bounded source-linked design support: '+i+'/'+c)
 raw=rd(x['raw_candidate_path']);records=raw.get('records',raw.get('buyers',[raw.get('primary_candidate',{})]));ck(any(z.get('candidate_id')==x['raw_candidate_id']for z in records),'Author candidate lineage: '+i)
textp=(R/'04-table/T02-PROPOSITION-PACK.md').read_text()
ck('complete commissioned report' in textp and 'not replaced with a smaller pack'in textp,'Draft future product does not shrink present commissioned report')
ck('No duration, turnaround, price or future-update promise'in textp,'No unproven service timing or recurring promise')
ck('equivalent access twice'in textp and 'free attendance and free research'in textp,'Free practitioner research and no duplicate licence sale')
ck('A separately defined event/access component remains possible'in textp and 'absent from the minimum draft'in textp,'Optional transparent research/access combination remains possible but not included')
funding='Name the actual edition and funding purpose. If research is already commissioned or complete, describe that accurately and distinguish any additional release, briefing or distribution work; do not present it as a newly commissioned study. Keep production costs and partner/licence revenues separately defined, counting each cost and bundled entitlement once.'
ck(funding in textp,'Funding purpose accurately distinguishes existing commission from additional work')
ck(p['propositions'][1]['funding_purpose_boundary']==funding,'Structured funding boundary exactly matches reviewed wording')

ck('favourable findings, suppression, method/results control'in textp,'Partner does not buy favourable findings or editorial veto')
ck('Recognition does not by itself authorise attendance disclosure or attribution; contextual details can still identify someone.'in textp,'Recognition does not grant attribution and indirect identification remains possible')
ck('One possible extra is a short follow-up separating useful takeaways from questions that still need evidence.'in textp,'Member concept script matches optional follow-through status')
ck('One possible extra'in p['propositions'][2]['concept_after_discovery'],'Structured member script preserves optional follow-through')
ck(any('follow-through'in x for x in p['propositions'][2]['optional_payload']),'Follow-through not silently required core service')
ck('An event is a possible additional format, not a prerequisite for the first report.'in textp,'Report independent of event launch')
ck('all research sales depend on dinners' in textp and 'changing cohorts rather than a longitudinal panel'in textp,'Event increment and cohort boundaries preserved')
ck(p['contract_segment_ids']==[f'BS{i:02}'for i in range(1,6)]and p['employer_segment_is_additional_hypothesis'],'Five contractual buyer segments beside additional employer use')
ck(b['contract_segment_ids']==p['contract_segment_ids']and b['additional_segment_ids']==['BS06']and not b['ranked'],'Segment map consistent and not ranked')
for x in b['records']:
 ck(not x['actual_payer_identified']and not x['actual_purchase_observed']and not x['validated'],'Segment remains unvalidated: '+x['segment_id'])
ck(u['actual_rights_grants']==[]and u['actual_customer_contracts']==[]and not u['Riseklix_controls_JGA_commissioned_IP'],'Future use options not actual licences or Provider veto')
ck([x['option_id']for x in u['options']]==[f'RU{i:02}'for i in range(1,9)],'Eight distinct reuse/service options')
for x in u['options']:ck(not x['approved']and bool(x['boundary'])and bool(x['state']),'Each use option remains unagreed: '+x['option_id'])
ck('Do not downgrade this to a teaser'in u['options'][0]['boundary']and 'individual-only'in u['options'][0]['boundary'],'Original free research not weakened to manufacture a tier')
ck('do not declare it forbidden'in u['options'][3]['boundary'],'Adviser use is an open JGA decision, not automatically prohibited')
ck('not included'in u['options'][6]['state'],'Commercial access outside minimum core')
ck(set(u['canonical_support_ids'])<=set(claims)and set(b['canonical_claim_ids'])<=set(claims),'Use and segment map support links resolve')
ck([x['work_id']for x in d['items']]==[f'DW{i:02}'for i in range(1,9)],'Eight delivery work objects retained')
for x in d['items']:
 ck(not x['owner_assigned']and x['hours']is None and x['cash_cost']is None and not x['capacity_confirmed'],'Work requirement not a staff/cost commitment: '+x['work_id'])
 ck(bool(x['work'])and bool(x['owner_role_requirement'])and bool(x['completion_evidence']),'Work, role and fulfilment evidence explicit: '+x['work_id'])
for k in ['financial_inputs','actual_delivery_events','staff_hired','new_signed_project_deliverables']:ck(d[k]==[],'No unperformed operating inputs: '+k)
ck(not d['commercial_validation'],'Delivery map is not commercial validation')
ck(v['version']=='0.2'and not v['active_collection_guide_changed']and not v['fieldwork_activated'],'Versioned guide is proposed, inactive')
ck(v['report_core_questions']==14 and v['additional_mandatory_report_questions']==0,'Versioned guide does not expand report core')
ck([x['question_id']for x in v['records']]==[f'B{i:02}'for i in range(1,7)]+[f'M{i:02}'for i in range(1,7)],'Same six buyer/six member IDs')
for x in v['records']:
 ck(not x['all_probes_mandatory'],'Probes remain selective: '+x['question_id'])
 ck(set(x['hypothesis_ids'])<=set(p['original_hypotheses']),'Guide hypothesis links: '+x['question_id'])
 ck(set(x['condition_ids'])<={f'TC{i:02}'for i in range(1,7)},'Guide selective-condition links: '+x['question_id'])
guide=(R/'01-method/TABLE-VALIDATION-GUIDES-v0.2.md').read_text()
for x in v['records']:ck(x['wording']in guide and x['optional_probes']in guide,'Exact proposed wording/probes match structured map: '+x['question_id'])
ck('B01/B02 or M01 before listing benefits'in guide and 'Begin with research alone'in guide,'Unaided discovery and research-only assessment before event')
ck('Record the actual concept version/order'in guide,'Actual concept exposure/order would be recorded')
ck('up to four substantive exploratory contribution events'in guide and 'Report contributors count each eligible person once only with actual usable permitted input'in guide,'Separate Table event cap and eligible person count preserved')
ck('A combined event counts once; repeated substantive events count separately.'in guide,'Combined/repeated event counting follows WP03')
ck('An introduction, RSVP, reaction or research-question suggestion alone does not establish an eligible report contribution.'in guide,'Interest/question alone not report overlap')
ck('Do not show a price anchor while the product/use/rights are undefined.'in guide,'No premature price anchoring')
for k in ['actual_concept_exposures','actual_responses','price_anchors']:ck(v[k]==[],'No actual validation evidence: '+k)
ck(v['actual_Table_events']==0 and v['actual_report_contributors']==0,'No collected contributions or events')
for path in ['05-analysis/observations.json','05-analysis/charts.json','04-table/financial-inputs.json']:ck(rd(path)['records']==[],'Actual observations/charts/financial inputs remain empty: '+path)
ck(not rd('01-method/collection-pack-v0.1/REVIEW-DECISIONS.json')['collection_ready'],'Existing collection decisions remain unconfirmed')
reviewpaths=['04-table/T02-PROPOSITION-PACK.md','04-table/T02-proposition-map.json','04-table/T02-BUYER-USES-AND-RIGHTS.md','04-table/T02-buyer-segments.json','04-table/T02-use-and-entitlement-options.json','04-table/T02-DELIVERY-AND-VALIDATION.md','04-table/T02-delivery-map.json','04-table/T02-validation-map.json','01-method/TABLE-VALIDATION-GUIDES-v0.2.md']
for path in reviewpaths:
 if path.endswith('.md'):
  text=(R/path).read_text();ck(set(re.findall(r'CLM-\d{4}',text))<=set(claims),'Canonical prose references: '+path)
  for link in re.findall(r'\]\(([^)]+)\)',text):
   if not link.startswith(('https://','http://','#')):ck((R/path).parent.joinpath(unquote(link.split('#')[0])).resolve().exists(),'Local link resolves: '+link)
out={'date':'2026-10-30','status':'passed_for_internal_T02_proposition_preparation','check_count':len(checks),'checks':checks,'open_substantive_issues':[],'wording_refinements_applied':['Neutral B01 now covers actual supplier, adviser, investment and employer use with the old guide preserved.','Recognition does not by itself authorise attendance disclosure/attribution; context can still identify someone.','Member follow-through is explicitly optional in the concept script and payload.','Funding purpose accurately names already commissioned/completed work and distinguishes costs from multiple legitimate revenue sources.'],'manual_review':['All three minimum payloads are concrete and conditional on actual evidence, permissions, delivery and capacity; this design is not commercial validation.','Five contractual market segments remain visible, employer-side use is additional rather than a silent change to primary buyer.','Full commissioned report and project IP rights are preserved; proposed future customer licences do not reserve a Riseklix veto.','Free practitioner research is intact; no teaser downgrade, artificial individual-only restriction or equivalent-copy second sale.','Partner recognition/briefing differs from optional separately scoped access; no default identities, private answers, guaranteed meetings or editorial control.','The peer-cycle value is more than hospitality, but no advice desk, unlimited support, fixed cadence or staffed bench is promised.','Research-only versus remote/written versus event-supported comparison remains open; no four-city launch, price, conversion or recurring revenue asserted.','The final funding-purpose clarification does not prohibit licensing an existing edition or cost recovery/profit; it prevents presenting existing work as a new study and separates costs, revenues and bundled entitlements.','Discovery sequence and counting policy remain coherent; all actual exposure/contribution arrays are empty.'],'reviewed_artifacts':[{'path':p,'sha256':h(p)}for p in reviewpaths],'allowed_following_status_only_changes':['status','review_basis'],'actual_fieldwork':False,'commercial_validation':False,'publication_approval':False,'source_or_claim_additions':False}
(R/'08-qa/t02-review/integration-checks.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({k:v for k,v in out.items()if k not in ['checks','reviewed_artifacts','manual_review']},indent=2))
