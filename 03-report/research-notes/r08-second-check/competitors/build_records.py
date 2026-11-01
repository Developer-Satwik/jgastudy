from pathlib import Path
import json,hashlib,collections
ROOT=Path(__file__).resolve().parents[4];WORKSPACE=ROOT.parent.parent;BASE=Path(__file__).resolve().parent
DATE='2026-10-29'
def read(p):return json.loads(p.read_text())
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def textsha(s):return hashlib.sha256(s.encode()).hexdigest()
manifest=read(BASE/'capture-manifest.json');captures={x['source_id']:x for x in manifest['records']}
notes={
 'SRC-0210':'''Selected paraphrased reader notes, not retained original HTML. Original route read29October2026; raw retrieval403.
https://www.theportfoliogroup.com/payroll/why-use-us/
Relevant sections: roles/services and Our process, especially vacancy registration, assessment, offer, contact and aftercare. The provider describes reviewing the role and requirements, assessing relevant skills/culture, managing the offer process and keeping in touch through acceptance/starting and aftercare. These are the provider's process declarations, not a completed search/candidate check in our study. No database/fee/rating or outcome percentage is adopted.
''',
 'SRC-0113':'''Selected paraphrased reader notes, not retained original HTML. Original route read29October2026; raw retrieval403.
https://jgarecruitment.com/payroll-recruitment/
Relevant original body2–13: UK/global payroll talent acquisition, tailored service and continuing support; the firm publishes its own quality/retention claims. We use only the source identity and service/proof boundary, not the numerical quality claims or their validity. A sponsor's proposition does not establish a specific candidate's availability/fit, actual engagement or payroll result.
''',
 'SRC-0119':'''Selected evidence-review note, not raw original HTML or a new full live-original read. Direct and reader access to the canonical route returned403 on29October2026.
Canonical: https://www.frazerjones.com/case-studies/delivering-payroll-and-hr-operations-talent-during-organisational-change/
Previously retained original-reader extract:03-report/research-notes/r04-second-check/competitors/captures/SRC-0119-reader-extract.txt
Fresh indexed same-case body appeared through the publisher's/de/case-studies/delivering-payroll-and-hr-operations-talent-during-organisational-change/ alias and case index. It describes aosphere de-merger/reorganisation, CPO commissioning context, interim/permanent HR/payroll talent and a named client testimonial. This is one provider-reported case, not independently assured availability or performance for another search, actual payroll controls/benefit metrics, full approval chain or a new employer dataset. No numerical or causal effect adopted.
'''
}
for ident,text in notes.items():
 p=BASE/'captures'/f'{ident}-selected-reader-notes.txt';p.write_text(text)
 captures[ident]['review_extracts']=[dict(path=str(p.relative_to(ROOT)),sha256=sha(p),kind='selected_paraphrased_reader_notes_not_raw_original')]
 if ident=='SRC-0119':
  old=ROOT/'03-report/research-notes/r04-second-check/competitors/captures/SRC-0119-reader-extract.txt'
  captures[ident]['review_extracts'].append(dict(path=str(old.relative_to(ROOT)),sha256=sha(old),kind='prior_selected_reader_extract_not_raw_original'))
  captures[ident]['fresh_indexed_alias_url']='https://www.frazerjones.com/de/case-studies/delivering-payroll-and-hr-operations-talent-during-organisational-change/'
write(BASE/'capture-manifest.json',dict(date=DATE,records=list(captures.values())))
detail={
 'SRC-0210':('Roles/services and Ourprocess: registration/assessment/offer/contact/aftercare','fresh_original_reader_sections_inspected_raw_unavailable','Declared assessment and search events remain distinct from actual candidate fit, acceptance, start and later payroll result.'),
 'SRC-0119':('Retained prior-reader challenge/outcome/attribution plus fresh primary indexed same-case alias','prior_reader_extract_rechecked_with_fresh_indexed_same_case_only','Aosphere is one prior canonical provider case; fresh full canonical reader access failed. No independent current search capability or causal payroll effect.'),
 'SRC-0115':('Payroll capabilities/recentplacement list, originalreader22–38','relevant_live_original_html_and_reader_rechecked','Provider placement examples and level/remit coverage do not assure current candidate availability, this assignment or independent payroll improvement.'),
 'SRC-0116':('PayrollSearch25–39: assessment,beyondshortlist,PostProjectReport','relevant_live_original_html_and_reader_rechecked','Declared assessment of work/leadership and recruitment analytics are not independently assessed payroll task performance or a necessary hire.'),
 'SRC-0147':('Deliverymodels275–294; requirements/SOW/onboarding-offboarding/reviews345–382','relevant_live_original_html_and_reader_rechecked','Resource augmentation and PMO-owned defined deliverables are different service declarations; no actual statement of work, payroll accountability transfer or benefit tested.'),
 'SRC-0192':('2026heading and method107–109; retainedHTML/text','relevant_live_original_html_and_reader_rechecked','2025 salary inputs and employer/employee survey have different bases. Legacy URL is not current edition; no price, salary or funded payroll evidence adopted.'),
 'SRC-0193':('2027heading; FAQ84–110 and method','relevant_live_original_html_and_reader_rechecked','Projected starting-salary methodology and non-salary survey differ. No payroll subgroup, employer budget, current offer or forecast value transferred.'),
 'SRC-0113':('Originalreader2–13 UK/global talent and tailoredsupport/quality declaration','fresh_original_reader_sections_inspected_raw_unavailable','JGA commercial/sponsor proposition, not independent performance or a predetermined recommendation. Numerical quality/retention claims not adopted.'),
}
reuses=[]
for ident,(locator,status,limits) in detail.items():
 d=dict(captures[ident]);d.update(locator=locator,review_status=status,review_result=limits,limitations=limits+' No original JGA contributor, representative market demand, candidate availability, contract/legal assurance or validated remedy.',accessed_on=DATE)
 reuses.append(d)
write(BASE/'source-candidates.json',dict(date=DATE,records=[],reused_canonical_sources=reuses,new_independent_datasets=0))
rows=[
 ('C8S-C01',['SRC-0210','SRC-0116'],'Portfolio describes role assessment and search/offer/contact/aftercare events; Middlemore describes assessing actual work and a post-search report of recruitment analytics. These are different evidence objects from a particular candidate’s current capability, acceptance/start and later payroll outcome.','recruiter_declared_process_and_evidence_object_boundary','Portfolio Ourprocess/roles; MiddlemorePayrollSearch andPostProjectReport','Declared process/reporting, not an independently tested candidate assessment, actual case progression, availability or useful operating effect. No brand-performance rank, numerical recruitment metric or right-to-work conclusion adopted.'),
 ('C8S-C02',['SRC-0147'],'Hays distinguishes resource augmentation and defined managed-project delivery, with SOW requirements, deliverables, governance and transition knowledge transfer. The exact engagement object matters before treating delivery support as transferred payroll responsibility or achieved benefit.','recruiter_cross_function_service_declaration_and_scope_application','Deliverymodels275–294; requirements/SOW/transition/reviews345–382','Cross-function technology/project service declaration, not a payroll engagement trial, executed terms, blanket transfer of accountability, legal status or proven cost/result. Retained responsibilities remain case-specific.'),
 ('C8S-C03',['SRC-0119','SRC-0115','SRC-0113'],'Frazer’s one hosted reorganisation case, Oakleaf’s placement/capability list and JGA’s tailored talent proposition provide different kinds of public firm-level material. None alone establishes the proposed team or candidate will meet a new brief or deliver its intended payroll result.','supplier_reported_case_and_service_evidence_boundary','Frazerretainedchallenge/outcome/attribution; Oakleaf22–38; JGA2–13','One provider-reported case and commercial claims, not independent effect assurance, a representative talent market, actual current candidate or an original JGA contribution. Frazer current full access unavailable; indexed alias/prior-reader scope retained. Numeric quality claims excluded.'),
 ('C8S-C04',['SRC-0192','SRC-0193'],'Hays’s salary inputs and employer/employee survey, and Robert Half’s projected starting salaries and non-salary survey, have distinct methods and periods. They do not identify the evidence accepted for a specific payroll decision, its affordability or its approved resources.','recruiter_method_and_decision_specific_evidence_fit','Hays107–109; RobertHalfFAQ84–110/method','No numeric values, payroll subgroup estimate, salary quote, current vacancy/candidate availability, employer budget or forecast adopted. Method description is not an audit of underlying microdata.'),
 ('C8S-C05',['SRC-0210','SRC-0116','SRC-0147','SRC-0119'],'For R08, make the object and match of evidence explicit where material: what specific claim about the work, provider/team/person, time and remit it supports, who checked it if known, and what remains unverified or introduced as an assumption. Firm-level material or generated verification advice is not completed case-specific assurance.','researcher_selective_evidence_object_and_match_condition','Cross-source application toV02/V04/V05; local exact bridge S01-C/S02-D/S06-C/S11-C','Selective analyst aid, not an extra mandatory question or request to collect confidential candidate evidence. Actual relevance/acceptance/influence/effect remain separate. Earlier prompts are researcher-selected hiring routes and evidence requests, not actual demand or a validation of generated scorecards/rules.')
]
cc=[]
for ident,ids,text,kind,loc,limits in rows:cc.append(dict(candidate_id=ident,canonical_source_ids=ids,claim_text=text,evidence_class=kind,locator=loc,limitations=limits,value=None,unit=None,denominator=None,population='Specific recruiter declaration/case/method or explicit analyst application; no original payroll respondents',time_period='Source-specific current and historical context inspected29October2026; no trend or forecast',review_mode='Relevant fresh primary HTML/reader sections or explicitly labelled prior-reader plus fresh indexed same-case body; captures and limits retained.'))
write(BASE/'claim-candidates.json',dict(date=DATE,records=cc))

paths={
 'all_answers':WORKSPACE/'sites/jga-discovery-report-2026-10-22/output/JGA-Research-Pack/data/all-answers.json',
 'answer_index':WORKSPACE/'sites/jgafinalcode/dist/data/answer-index.json',
 'summary':WORKSPACE/'sites/jgafinalcode/dist/data/summary.json',
 'previous_R07_bridge':ROOT/'03-report/research-notes/r07-second-check/competitors/prior-study-bridge.json',
}
a=read(paths['all_answers'])['answers'];ix=read(paths['answer_index']);byindex={x['id']:x for x in ix}
qdetails={
 'S01-C':('Role definition and public experience evidence','The researcher already chooses a UK-based global head, Europe/NorthAmerica expansion and recruiting route. The request for public evidence elicits verification language; it is not spontaneous employer evidence demand.'),
 'S02-D':('Authorisation before confidential candidate approaches','Confidential retained search and replacement are preselected. Asking what to check before candidate approaches cannot establish actual client/candidate permissions, search contract terms, or validate generated confidentiality gates.'),
 'S06-C':('Assessment claims for control-recovery leadership','A permanent UK-based global director and a controls-rebuild narrative are researcher premises. Generated assessment questions, scenarios and weighted scorecards are not independently validated tests or proof that a hire solves the underlying work.'),
 'S11-C':('Hands-on capability evidence for a growing small team','Permanent hiring and small-team growth are preselected. Team size is not employer size; unprovided location/salary assumptions introduced in an answer are not case facts. Public vacancy/activity does not establish completed placement or candidate quality.'),
}
questions=[]
for qid,(contrast,assumption) in qdetails.items():
 selected=[x for x in a if x['question']==qid]
 p=selected[0]['prompt'];links=[]
 for r in selected:
  k=byindex[r['id']]
  links.append(dict(answer_id=r['id'],product=r['product'],repeat=r['repeat'],observed_at_utc=r['dateUtc'],full_answer_sha256=textsha(r['fullAnswer']),recorded_answer_hash=r['answerHash'],prompt_sha256=r['promptHash'],source_status=r['sourceStatus'],source_note=r.get('sourceNote'),index_text_match=r['fullAnswer']==k['fullAnswer']))
 questions.append(dict(question_id=qid,prompt=p,prompt_sha256=textsha(p),analyst_contrast=contrast,embedded_assumption_to_exclude=assumption,saved_answer_count=len(selected),capture_status_counts=dict(collections.Counter(x['sourceStatus'] for x in selected)),answer_links=links))
semantic=[
 dict(answer_id='S01-C-chatgpt-r1',reviewed_scope='Full saved text',observation='The answer itself distinguishes public specialism/case material from independent validation and asks for role-definition evidence. This supports checking evidence kind rather than promoting every citation into verified fit.',excluded='Listed firms, named cases, numerical claims and recommended actions are not independently validated by this bridge.'),
 dict(answer_id='S02-D-chatgpt-r1',reviewed_scope='Full saved text',observation='The prompt explicitly requests verification before approaches; the answer supplies confidentiality/permission gates and a weighted pitch scorecard. These are generated proposed controls, not observed authorisation or a validated selection instrument.',excluded='Do not import generated pass/fail approvals, contracts, disclosure requirements, weights, candidate names or legal advice as mandatory research rules.'),
 dict(answer_id='S06-C-chatgpt-r1',reviewed_scope='Full saved text',observation='The answer proposes assessment scenarios and numerical weights. Neither the prompt nor this archive validates the measures or establishes causal payroll recovery from hiring.',excluded='No generated score weights, timed scenarios, staffing need or treatment effect becomes this framework’s evidence.'),
 dict(answer_id='S11-C-chatgpt-r1',reviewed_scope='Full saved text',observation='The answer adds an assumed London focus that the prompt did not supply, then distinguishes job adverts from completed-placement/candidate-quality proof. This is an explicit illustration of introduced assumptions versus source-supported case facts.',excluded='No location, wage, claimed role/candidate availability, agency ranking or job advertisement outcome is transferred as fact.'),
]
bridge=dict(date=DATE,purpose='R08 second challenge: match evidence object to actual decision and expose researcher/model-added premises; no reruns',provenance=[dict(role=k,path=str(p.relative_to(WORKSPACE)),sha256=sha(p)) for k,p in paths.items()],questions=questions,selected_questions=4,selected_total_answers=32,global_source_limitations_preserved=dict(collections.Counter(x['sourceStatus'] for x in a)),recommendation_counts_reused=False,model_reruns=False,anti_anchoring_rule='The researcher preselects hiring routes, role/remit and evidence questions. Obtain the actual unaided account first; do not convert generated verification lists or added assumptions into case facts. Team size differs from employer size, and headquarters, country remit and work location require their actual basis.',semantic_review=semantic,semantic_review_answer_count=4,remaining_selected_answers_review_mode='Exact full-text/index/hash/date/status integrity, not fresh semantic validation of every recommendation or citation.',external_actions=[])
write(BASE/'prior-study-bridge.json',bridge)
write(BASE/'search-review-log.json',dict(date=DATE,purpose='R08 evidence object and decision-specific match across all six recruitment comparators and JGA',original_routes_rechecked=list(captures),queries=['site:frazerjones.com/case-studies/delivering-payroll-and-hr-operations-talent-during-organisational-change aosphere interim permanent payroll'],fresh_indexed_alias_not_independent_source='https://www.frazerjones.com/de/case-studies/delivering-payroll-and-hr-operations-talent-during-organisational-change/',no_new_route_needed=True,no_figures_adopted=True,no_forms_submitted=True,external_actions=[]))
checks=[]
def check(v,label):
 checks.append(dict(check=label,passed=bool(v)))
 if not v:raise AssertionError(label)
for d in reuses:
 if d.get('capture_path'):check(sha(ROOT/d['capture_path'])==d['capture_sha256'],'Raw original hash '+d['source_id'])
 else:check(not d.get('capture_sha256'),'No raw hash invented '+d['source_id'])
 if d.get('text_path'):check(sha(ROOT/d['text_path'])==d['text_sha256'],'Parsed extract hash '+d['source_id'])
 for x in d.get('review_extracts',[]):check(sha(ROOT/x['path'])==x['sha256'],'Selected note hash '+x['path'])
sourceids={x['source_id'] for x in read(ROOT/'02-evidence/registers/sources.json')['records']}
for c in cc:check(set(c['canonical_source_ids'])<=sourceids,'Claim canonical links '+c['candidate_id'])
for p in bridge['provenance']:check(sha(WORKSPACE/p['path'])==p['sha256'],'Bridge provenance '+p['role'])
for q in questions:
 check(len(q['answer_links'])==8,'Eight saved records '+q['question_id'])
 check({(x['product'],x['repeat']) for x in q['answer_links']}=={(t,n) for t in ['ChatGPT','Claude','Gemini','Perplexity'] for n in [1,2]},'Fourtool/tworepeat coverage '+q['question_id'])
 for x in q['answer_links']:
  r=next(r for r in a if r['id']==x['answer_id']);k=byindex[x['answer_id']]
  check(r['fullAnswer']==k['fullAnswer'] and textsha(r['fullAnswer'])==x['full_answer_sha256']==r['answerHash'],'Exact saved-text/index/hash '+x['answer_id'])
  check(r['prompt']==q['prompt'] and textsha(r['prompt'])==q['prompt_sha256']==r['promptHash'],'Exact prompt/hash '+x['answer_id'])
  check(r['dateUtc']==k['dateUtc']==x['observed_at_utc'] and r['sourceStatus']==k['sourceStatus']==x['source_status'],'Date/source status '+x['answer_id'])
check(all(c['value'] is None for c in cc),'No new numerical claim adopted')
check(len(reuses)==8 and not read(BASE/'source-candidates.json')['records'],'All-six/JGA canonical reuses, no new route')
check(bridge['selected_total_answers']==sum(q['saved_answer_count'] for q in questions),'32selected saved records')
check(len(semantic)==4,'Four saved answers semantically reviewed; other texts integrity-only')
write(BASE/'verification.json',dict(date=DATE,status='passed',check_count=len(checks),checks=checks,scope='Targeted source/reuse hashes, claim links and saved-study integrity; not independent validation of advice, candidate capability, market effects or final integration.',new_source_routes=0,new_claim_candidates=len(cc),canonical_reuses=len(reuses),selected_questions=4,saved_answer_texts=32,external_actions=[]))
print(json.dumps({'status':'stable_for_parent_integration','canonical_reuses':len(reuses),'new_routes':0,'claims':len(cc),'selected_prompts':4,'saved_answers':32,'semantic_answers_reviewed':4,'local_checks':len(checks)},indent=2))
