from pathlib import Path
import json

root=Path(__file__).resolve().parents[1]
qmap=json.loads((root/'01-method/question-map.json').read_text())
cases=[
    {'case_id':'SYN-01','description':'Approved renewal with incumbent retained and operating service','has_recent_case':True,'disposition':'approved','option':'incumbent_retained','delivery':'operating'},
    {'case_id':'SYN-02','description':'Approved alternative platform not yet implemented','has_recent_case':True,'disposition':'approved','option':'alternative_platform','delivery':'not_started'},
    {'case_id':'SYN-03','description':'Deferred proposal awaiting evidence','has_recent_case':True,'disposition':'deferred','option':'none_selected','delivery':'not_started'},
    {'case_id':'SYN-04','description':'Proposal withdrawn after review','has_recent_case':True,'disposition':'withdrawn','option':'none_selected','delivery':'not_applicable'},
    {'case_id':'SYN-05','description':'Pending decision with no option selected','has_recent_case':True,'disposition':'pending','option':'none_selected','delivery':'not_started'},
    {'case_id':'SYN-06','description':'Senior practitioner with priorities but no recent case','has_recent_case':False,'disposition':None,'option':None,'delivery':None},
    {'case_id':'SYN-07','description':'Deliberate no change after a formal review','has_recent_case':True,'disposition':'approved','option':'deliberate_no_change','delivery':'not_applicable'},
    {'case_id':'SYN-08','description':'Internal process change requiring no formal approval','has_recent_case':True,'disposition':'no_formal_approval_required','option':'internal_process_change','delivery':'underway'},
]
for c in cases:
    c['asked_ids']=[q['question_id'] for q in qmap['records'] if q['route']=='all' or c['has_recent_case']]
    c['recent_case_base']=c['has_recent_case']
    assert len(c['asked_ids'])==(14 if c['has_recent_case'] else 7)
    assert ('Q007' in c['asked_ids'])==c['has_recent_case']
    c['q011_wording']=None if not c['has_recent_case'] else (
        qmap['records'][10]['routed_wording']['pending']
        if c['disposition']=='pending' else qmap['records'][10]['wording'])
    c['q011_follow_up']=qmap['records'][10]['routed_wording']['pending_or_deferred_follow_up'] if c['has_recent_case'] and c['disposition'] in ('pending','deferred') else None
    c['result']='passed'
assert cases[0]['disposition']==cases[1]['disposition'] and cases[0]['option']!=cases[1]['option']
assert cases[0]['delivery']!=cases[1]['delivery']
assert cases[2]['q011_wording']==qmap['records'][10]['wording'] and cases[2]['q011_follow_up']
assert cases[4]['q011_wording']==qmap['records'][10]['routed_wording']['pending'] and cases[4]['q011_follow_up']
result={'date':'2026-10-28','status':'passed','instrument_version':qmap['version'],
        'check_type':'Internal synthetic route walkthrough only',
        'limitations':'Not participant responses, cognitive testing, interview timing or evidence of actual outcomes. The scenarios validate structural routing only.',
        'cases':cases}
(root/'08-qa/WP02-routing-walkthrough.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({'status':'passed','synthetic_cases':len(cases),'human_participants':0}))
