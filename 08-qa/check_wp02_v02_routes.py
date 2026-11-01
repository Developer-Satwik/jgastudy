from pathlib import Path
from datetime import date
import calendar, json

ROOT=Path(__file__).resolve().parents[1]
qmap=json.loads((ROOT/'01-method/question-map.json').read_text())
old=json.loads((ROOT/'01-method/question-map-v0.1.json').read_text())
assert qmap['version']=='0.2'
assert [q['question_id'] for q in qmap['records']]==[f'Q{i:03}' for i in range(1,15)]
assert [q['wording'] for q in qmap['records']]==[q['wording'] for q in old['records']]
assert qmap['client_approved'] is False and qmap['participant_tested'] is False

def cutoff(collection):
    year=collection.year-2
    return date(year,collection.month,min(collection.day,calendar.monthrange(year,collection.month)[1]))

def route(case):
    collection=date.fromisoformat(case.get('collection_date','2026-10-28'))
    if case.get('declined_to_share'):
        state='no_case_shared'
    elif case.get('never_raised'):
        state='never_raised'
    elif case.get('no_improvement'):
        state='no_improvement'
    elif not case.get('decision_date') or case.get('direct_involvement') is None:
        state='unknown_eligibility'
    else:
        decision=date.fromisoformat(case['decision_date'])
        if decision>collection:
            state='unknown_eligibility'
        elif decision<cutoff(collection) or not case.get('direct_involvement'):
            state='older_only' if decision<cutoff(collection) else 'unknown_eligibility'
        elif case.get('old_programme'):
            state='recent_substantive_milestone' if case.get('substantive_decision') else 'older_only'
        else:
            state='confirmed_after_probe' if case.get('recalled_after_probe') else 'confirmed_initial'
    recent=state in qmap['route_states']['recent_case']
    asked=[q['question_id'] for q in qmap['records'] if q['route']=='all' or recent]
    return {'route_state':state,'asked_ids':asked,'recent_case_base':recent,
      'pre_proposal_need':state=='never_raised',
      'no_case_follow_up_allowed':not recent and state not in ['no_case_shared','no_improvement'],
      'cutoff_date':cutoff(collection).isoformat()}

cases=[
 ('RT01','Never raised need',{'never_raised':True},'never_raised'),
 ('RT02','Older proposal without recent milestone',{'decision_date':'2023-08-04','direct_involvement':True},'older_only'),
 ('RT03','Recent case recalled after follow-up',{'decision_date':'2026-04-01','direct_involvement':True,'recalled_after_probe':True},'confirmed_after_probe'),
 ('RT04','Old programme with recent substantive decision',{'programme_start':'2021-03-01','decision_date':'2026-03-02','direct_involvement':True,'old_programme':True,'substantive_decision':True},'recent_substantive_milestone'),
 ('RT05','Old programme still operating only',{'programme_start':'2021-03-01','decision_date':'2026-03-02','direct_involvement':True,'old_programme':True,'substantive_decision':False},'older_only'),
 ('RT06','Pending proposal',{'decision_date':'2026-07-01','direct_involvement':True,'disposition':'pending'},'confirmed_initial'),
 ('RT07','Deferred proposal',{'decision_date':'2026-07-01','direct_involvement':True,'disposition':'deferred'},'confirmed_initial'),
 ('RT08','No relevant need or case',{'no_improvement':True},'no_improvement'),
 ('RT09','Uncertain involvement',{'decision_date':'2026-07-01','direct_involvement':None},'unknown_eligibility'),
 ('RT10','Approved renewal',{'decision_date':'2026-07-01','direct_involvement':True,'disposition':'approved','option':'incumbent_retained','delivery':'operating','benefit_assessment':'not_measured'},'confirmed_initial'),
 ('RT11','Approved alternative not started',{'decision_date':'2026-07-01','direct_involvement':True,'disposition':'approved','option':'alternative','delivery':'not_started','benefit_assessment':'not_yet_assessed'},'confirmed_initial'),
 ('RT12','Live but benefits unmeasured',{'decision_date':'2026-07-01','direct_involvement':True,'delivery':'live','benefit_assessment':'not_measured'},'confirmed_initial'),
 ('RT13','Capacity released with no spending reduction',{'decision_date':'2026-07-01','direct_involvement':True,'benefit_assessment':'reported_change','capacity_released':True,'spending_reduced':False},'confirmed_initial'),
 ('RT14','Future priority only',{'future_priority_stage':'idea'},'unknown_eligibility'),
 ('RT15','Exact calendar cutoff',{'decision_date':'2024-10-28','direct_involvement':True},'confirmed_initial'),
 ('RT16','Day before calendar cutoff',{'decision_date':'2024-10-27','direct_involvement':True},'older_only'),
 ('RT17','Unknown date',{'direct_involvement':True},'unknown_eligibility'),
 ('RT18','Choice not to share a case',{'declined_to_share':True},'no_case_shared'),
 ('RT19','Future planned event is not a recorded past decision',{'decision_date':'2027-04-01','direct_involvement':True},'unknown_eligibility'),
]
results=[]
for ident,label,inputs,expected in cases:
    actual=route(inputs)
    assert actual['route_state']==expected,ident
    assert len(actual['asked_ids'])==(14 if actual['recent_case_base'] else 7),ident
    assert actual['asked_ids'].count('Q014')==1
    assert ('Q007' in actual['asked_ids'])==actual['recent_case_base']
    q11=qmap['records'][10]
    disposition=inputs.get('disposition')
    actual['q011_wording']=(q11['routed_wording']['pending'] if disposition=='pending' else q11['wording']) if actual['recent_case_base'] else None
    actual['q011_follow_up']=q11['routed_wording']['pending_or_deferred_follow_up'] if disposition in ['pending','deferred'] and actual['recent_case_base'] else None
    # Preserve independent supplied fields without inventing a result from another field.
    actual['analytical_fields']={k:inputs[k] for k in ['disposition','option','delivery','benefit_assessment','capacity_released','spending_reduced','future_priority_stage'] if k in inputs}
    results.append({'test_id':ident,'description':label,'synthetic_inputs':inputs,'expected_route':expected,'actual':actual,'status':'passed'})
by={r['test_id']:r['actual'] for r in results}
assert by['RT02']['pre_proposal_need'] is False and by['RT01']['pre_proposal_need'] is True
assert by['RT03']['recent_case_base'] is True
assert by['RT04']['recent_case_base'] is True and by['RT05']['recent_case_base'] is False
assert by['RT07']['q011_wording']==qmap['records'][10]['wording'] and by['RT07']['q011_follow_up']
assert by['RT06']['q011_wording']==qmap['records'][10]['routed_wording']['pending'] and by['RT06']['q011_follow_up']
assert by['RT12']['analytical_fields']=={'delivery':'live','benefit_assessment':'not_measured'}
assert by['RT13']['analytical_fields']['spending_reduced'] is False
assert 'delivery' not in by['RT14']['analytical_fields'] and by['RT14']['recent_case_base'] is False
assert by['RT18']['no_case_follow_up_allowed'] is False
assert cutoff(date(2024,2,29))==date(2022,2,28)

out={'date':'2026-10-28','instrument_version':'0.2','status':'passed','test_count':len(results),
 'check_type':'Internal synthetic structural and analytical-state walkthrough only',
 'recall_boundary':'Inclusive calendar date two years before collection; leap-day cutoff clamps to last valid February day. Approximate participant dates remain uncertain rather than assumed exact.',
 'limitations':'Not participant answers, cognition, timing, real benefits or commercial validation. No synthetic input is added to observations or findings as human evidence.',
 'core_wording_unchanged_from_v01':True,'results':results}
(ROOT/'08-qa/WP02-v0.2-routing-walkthrough.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({'status':'passed','synthetic_checks':len(results),'human_participants':0,'core_wording_unchanged':True}))
