from pathlib import Path
import json,hashlib,copy
R=Path(__file__).resolve().parents[4];B=Path(__file__).resolve().parent;W=R.parent.parent;D='2026-10-30'
def rd(p):return json.loads(p.read_text())
def wr(n,d):(B/n).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
S={x['source_id']:x for x in rd(R/'02-evidence/registers/sources.json')['records']};caps=rd(B/'capture-manifest.json')['records'];cap={x['source_candidate_or_canonical_id']:x for x in caps}
new=cap['TC2-S01'];source=dict(candidate_id='TC2-S01',title='Pension Reform 2026',publisher='Oakleaf Partnership',url=new['url'],source_type='provider_published_webinar_followthrough_format',review_status='selected_original_format_sections_inspected',accessed_on=D,published_date='2026-01-28',updated_date=None,date_note='Visible article date, not date of verified webinar attendance or outcomes.',population='Public employer-facing payroll content; no Table audience sample.',sample_size=None,fieldwork_period=None,method_available=False,funding_or_commercial_interest='Recruitment provider publishes its own expert content and event routes.',capture_path=new['capture_path'],capture_sha256=new['capture_sha256'],capture_kind='retained_original_html',review_extracts=[dict(path=new['text_path'],sha256=new['text_sha256'],kind='parsed_original_text')],locator='Retained parsed lines13–21,42–43,57–59; primary reader lines19–32,79–81,106–111',limitations='Used only for declared webinar-to-written-themes and recording/event-discovery format. Legal, tax, reform-date, savings and employer-behaviour assertions are excluded. Recording not watched, registration not submitted, no audience reach, fee, event value, permission or sales result established.',reuse_status='Private verification; no reproduction licence or commercial content reuse obtained.')
prior=rd(R/'04-table/research-notes/t01-second-check/competitors/source-candidates.json')['reused_canonical_sources'];re=[]
for old in prior:
 sid=old['source_id'];x=dict(source_id=sid,url=S[sid]['url'],accessed_on=D,new_independent_dataset=False,locator=old.get('locator'),limitations='Source-specific prior/current access boundary retained. No public statement becomes observed audience value, paid demand, outcome, reuse permission or original Table contribution.')
 if sid in cap:
  c=cap[sid];x.update(c);x.pop('source_candidate_or_canonical_id',None);x['review_status']='fresh_retained_original_sections_inspected'
  x['review_extracts']=[dict(path=c['text_path'],sha256=c['text_sha256'],kind='parsed_original_text')]
 else:
  # Reuse the exact previously reviewed primary reader context; no fresh body claimed.
  x['review_status']='prior_primary_context_rechecked_not_fresh_full_body';x['prior_review_record']='04-table/research-notes/t01-second-check/competitors/source-candidates.json'
  x['review_extracts']=copy.deepcopy(old.get('review_extracts',[]))
  x['prior_access_boundary']=old.get('review_status')
 re.append(x)
wr('source-candidates.json',dict(date=D,records=[source],reused_canonical_sources=re,new_source_routes=1,new_independent_demand_datasets=0))
cs=[
('TC2-C01',['SRC-0222'],['TC2-S01'],'Oakleaf publishes a dated article that presents named-expert webinar themes, employer questions and a link to a recording/future-event route. This is a concrete existing follow-through format beside its payroll market commentary and event account.','provider_declared_content_followthrough_format','New article parsed13–21,42–43,57–59; existing payroll-event/market article body','Only the content/format and public route are observed. No legal/tax assertions, actual webinar viewing, participant benefit, publication reuse right, reach, fee or market demand is imported.'),
('TC2-C02',['SRC-0190','SRC-0221','SRC-0222','SRC-0116','SRC-0192','SRC-0193','SRC-0088'],['TC2-S01'],'For TP01 briefing and TP03 follow-through, define the additional task, evidence or practical interpretation beyond the actual alternatives the user already has. A summary, event, expert conversation or personalised explanation is not distinctive merely by its format; existing public recruiter/JGA formats supply counterexamples.','researcher_offer_incremental_value_vs_format_condition','All-seven context map plus Oakleaf webinar-follow-through and Robert Half personalised interpretation route','This does not prove those alternatives solve a specific user need, that a format must be unique, or that free content makes paid interpretation unviable. No market ranking, right to copy, price or guaranteed value is established. Selective design criterion, not a new mandatory question.'),
('TC2-C03',['SRC-0116','SRC-0192','SRC-0193','SRC-0088'],[],'Earlier constructed recruiting prompts distinguish US domestic remit, UK/European responsibility and Manchester provider-governance ownership. For T02, a tailored reading path or briefing must preserve the actual task, evidence object and geography of the underlying material; office presence or a broader label does not create relevant case evidence.','researcher_prior_study_task_remit_and_offer_boundary','Exact S03-C/S08-C/S09-C bridge and24saved-answer lineage; three ChatGPT repeat1 texts semantically reread','These prompts already assume recruiting and their stated situations. Generated firms, rankings, weights, capability assertions and recommendations are not revalidated or transferred as buyer demand, case coverage or permission. This is a constructed counterexample lens, not original market evidence.')]
wr('claim-candidates.json',dict(date=D,records=[dict(candidate_id=i,canonical_source_ids=s,source_candidate_ids=ss,claim_text=t,evidence_class=e,locator=l,limitations=lim,value=None,unit=None,denominator=None,population='Provider content or explicit researcher/constructed-prompt application; not original participant data',time_period='Article28January2026; other source-specific dates preserved; this review30October2026')for i,s,ss,t,e,l,lim in cs]))
prevmap=rd(R/'04-table/research-notes/t01-second-check/competitors/comparator-map.json');rows=copy.deepcopy(prevmap['records'])
for x in rows:
 x['T02_role']='Existing content/service/interpretation/convening context; actual buyer, funding or distribution role not established.'
 x['T02_selective_lesson']={
 'Portfolio Payroll':'Test what the user needs beyond salary/hiring resources; do not treat generic report access as automatically incremental.',
 'Frazer Jones':'A public leader interview is a prior peer-learning format; distinguish actual case analysis and usable interpretation from the label of expert access.',
 'Oakleaf Partnership':'A webinar-to-themes/article/recording format already exists. Follow-through must serve a specific task and actual evidence, not just be called a new benefit.',
 'Middlemore':'A client-specific post-search output is a distinct work/service object. Do not turn a short edition briefing into an uncosted client study.',
 'Hays':'Keep evidence period, country and intended compensation/hiring task; a research edition label does not make all use current or geographically suitable.',
 'Robert Half':'A public resource with personalised interpretation is an existing service architecture; define the additional task/service rather than assume a paywall or standalone sale.',
 'JGA':'Existing payroll expert conversations are context, not a guaranteed Table audience or permission to republish guest contributions.'}[x['firm']]
 x['T02_review_mode']='Fresh retained original body' if x['source_id']in cap else 'Previously inspected primary context retained; no fresh full body claimed'
wr('comparator-map.json',dict(date=D,records=rows,recruitment_comparator_count=6,JGA_context_count=1,not_the_T01_six_business_models=True,no_qualified_buyer_list=True,actual_fieldwork=False))
afile=W/'sites/jga-discovery-report-2026-10-22/output/JGA-Research-Pack/data/all-answers.json';ifile=W/'sites/jgafinalcode/dist/data/answer-index.json';answers=rd(afile)['answers'];index={x['id']:x for x in rd(ifile)}
qs=[];checks=[]
def ck(v,n):checks.append(dict(name=n,passed=bool(v)));assert v,n
qnotes={
'S03-C':('US-based director with US-only responsibility and public evidence request.','Keep domestic operating remit separate from global responsibility and public advertised-role evidence separate from a completed outcome.','The reread answer itself separates advertised searches from verified placements. Its named firms and assessment are not fact-validated here.'),
'S08-C':('US parent hiring a UK-based EMEA leader, explicitly contrasting UK/European hiring evidence with office/website presence.','A geographic footprint or general expertise label is not evidence that a report covers the relevant task/country set.','The generated weighted RFP and ranked firms are advice introduced by the model, not empirically validated purchasing criteria or participant preferences.'),
'S09-C':('Manchester-based head for UK/European provider transition, asking for vendor-governance hiring evidence.','Keep role location, operating-country scope and actual supplier-governance ownership distinct when stating the edition/briefing use.','The answer distinguishes general payroll recruitment from transition/governance proof; its recommendations and case assertions are not reverified.')}
for q in qnotes:
 ans=[a for a in answers if a['question']==q];ck(len(ans)==8 and {(a['product'],a['repeat'])for a in ans}=={(p,r)for p in ['ChatGPT','Claude','Gemini','Perplexity']for r in [1,2]},q+' fourproducts two repeats');ck({a['product']for a in ans}=={'ChatGPT','Claude','Gemini','Perplexity'},q+' four products')
 prompt=ans[0]['prompt'];psha=hashlib.sha256(prompt.encode()).hexdigest();links=[]
 for a in ans:
  ah=hashlib.sha256(a['fullAnswer'].encode()).hexdigest();ii=index[a['id']]
  ck(a['prompt']==prompt and hashlib.sha256(a['prompt'].encode()).hexdigest()==psha and a['promptHash']==psha,a['id']+' exact prompt/hash')
  ck(ah==a['answerHash'],a['id']+' original full answer hash')
  ck(ii['prompt']==a['prompt'] and ii['fullAnswer']==a['fullAnswer'],a['id']+' finalindex exact text')
  ck(all(ii[k]==a[k]for k in ['country','dateUtc','product','repeat','question']),a['id']+' original routing/time metadata')
  ck(ii['sourceStatus']==a['sourceStatus'],a['id']+' source status preserved')
  links.append(dict(answer_id=a['id'],product=a['product'],repeat=a['repeat'],observed_at_utc=a['dateUtc'],country=a['country'],prompt_sha256=psha,full_answer_sha256=ah,source_status=a['sourceStatus'],source_note=a['sourceNote'],semantic_reread_for_this_lens=a['product']=='ChatGPT'and a['repeat']==1))
 n=qnotes[q];qs.append(dict(question_id=q,prompt=prompt,prompt_sha256=psha,embedded_assumption=n[0],T02_selective_analyst_application=n[1],semantic_reread_note=n[2],answer_links=links))
bridge=dict(date=D,purpose='T02 narrow task/remit/reading-path challenge, not model rerun or demand evidence',provenance=[dict(role='all_answers',path=str(afile.relative_to(W)),sha256=h(afile)),dict(role='final_answer_index',path=str(ifile.relative_to(W)),sha256=h(ifile))],questions=qs,question_count=3,linked_saved_records=24,semantic_rereads=3,integrity_only_records=21,no_model_reruns=True,recommendation_counts_reused=False,generated_advice_fact_validated=False,actual_buyer_evidence=False)
wr('prior-study-bridge.json',bridge)
wr('prior-study-bridge-check.json',dict(date=D,status='passed_narrow_saved_data_integrity_not_fact_validation',check_count=len(checks),checks=checks,selected_questions=3,selected_saved_records=24,semantic_rereads=3,no_model_reruns=True,prior_recommendation_counts_reused=False,bridge_path=str((B/'prior-study-bridge.json').relative_to(R)),bridge_sha256=h(B/'prior-study-bridge.json')))
(B/'PRIOR-STUDY-BRIDGE.md').write_text('''# Earlier prompt study: T02 task/remit bridge

30 October2026. Three exact questions link24savedanswers across the four products and two repeats. Original prompt/text hashes, routing/time metadata and final-index source statuses were checked. Three ChatGPT repeat1 full texts were independently semantically reread for this lens; the other21received integrity checks only. No model was rerun, and generated advice was not fact-validated.

| Question | Supplied task | T02 implication |
| --- | --- | --- |
| S03-C | US-based Payroll Director responsible for US payroll | Domestic remit and advertised-role evidence do not establish global coverage or completed outcomes |
| S08-C | UK-based EMEA head for a US multinational; evidence beyond office presence | A location/brand label does not create relevant task/geography evidence; generated scoring weights are not validated buyer criteria |
| S09-C | Manchester head for a UK/European provider transition | Local role location, operating countries and governance ownership are distinct objects |

These are researcher-constructed recruiting questions, not spontaneous research-product needs. Their model rankings, named firms, weights and advice do not prove demand, permission or coverage. They expose a bounded offer-design counterexample: changing a reading path or briefing explanation cannot turn evidence about one context into a demonstrated case about another.

[Exact bridge](prior-study-bridge.json) preserves the wording and24links. [Verification](prior-study-bridge-check.json) reports126lineage checks, not126respondents or factual verifications.
''')
(B/'COMPETITOR-AND-TASK-CHECK.md').write_text('''# T02: specific competitors and task fit

30 October2026. Second challenge of the concrete offers, building on the earlier seven-context map without treating those firms as qualified buyers or replacing the six distinct business models.

## A useful format already exists

Oakleaf's28January2026article explicitly presents named-expert webinar themes, questions and a recording/future-event route. The retained original supports this format observation only. The legal, tax, reform-date and savings assertions are excluded, and the recording was not watched. A Table follow-through note therefore needs a specific useful task/evidence contribution rather than distinctiveness from the fact that it is a short written follow-up. TC2-C01.

## Define the incremental use, not a unique-looking format

The existing Portfolio resources, Frazer Jones interview, Oakleaf commentary/events, Middlemore client output, Hays guide, Robert Half personalised interpretation route and JGA podcast each address different jobs. Their existence does not prove they solve the proposed buyer's problem; equally a report, expert discussion or briefing is not new merely as a format. Assess what the actual user needs beyond the alternatives they use. Paid interpretation can be useful without being a unique format, if the added service/evidence is real and deliverable. TC2-C02.

Keep the user's actual intended task, market and evidence object visible. A client-specific post-search report is different from a short briefing on an existing edition. A general or international office footprint is different from relevant operating-country evidence. No fee, reach, paid uptake, outcome or licence right follows from any public route. The [seven-context map](comparator-map.json) states source-specific currentness/access boundaries.

## Earlier evidence tests a promise boundary

The [three-question bridge](PRIOR-STUDY-BRIDGE.md) compares US domestic remit, UK/European responsibility and Manchester/provider-governance hiring premises. It does not transfer recruiter rankings into research demand. A tailored explanation or reading path must retain the actual evidence scope rather than create missing geography/task coverage. This overlaps the market pack's releaseable-evidence condition as an independent constructed counterexample, not a second empirical dataset or a duplicated primary finding. TC2-C03.

## Two selective implications for the offers

1. For a briefing/follow-through benefit, identify the concrete use and additional evidence/interpretation relative to the user's actual alternatives. Do not require novelty of format, assume that free alternatives fail, or promise a new custom service by accident.
2. Keep the task/remit/evidence object on any reading path, excerpt or briefing. A product category or geographic label cannot substitute for actual suitable findings. Narrow or qualify the use if necessary; retain complete contracted report delivery.

These implications preserve the three propositions and existing questions. All prior evidence/rights/free-practitioner and JGA-IP conditions remain. No new country quota, mandatory case, price, survey, customer, event, private access or financial input is introduced. No external action occurred.

Records: [sources](source-candidates.json), [claims](claim-candidates.json), [captures](capture-manifest.json), [verification](verification.json).
''')
wr('search-log.json',dict(date=D,purpose='Specific competitor/offer-format and prior-task counterexample challenge',reviewed_new_route=new['url'],fresh_canonical_rechecks=['SRC-0193','SRC-0222','SRC-0116'],prior_context_reused=['SRC-0190','SRC-0221','SRC-0192','SRC-0088'],primary_web_reopen='Oakleaf new route reopened30October2026; relevantformat sections verified against retainedoriginal',excluded_assertions=['Pension/tax/legal reform details and savings','Webinar recording content or attendance','Reach, paid demand, conversion, partnership or licence rights'],model_reruns=0,external_actions=False))
vc=[]
def v(t,n):vc.append(dict(name=n,passed=bool(t)));assert t,n
v(len(re)==7 and len(rows)==7,'six recruiters plus JGA contexts retained');v(len(cs)==3,'three bounded records');v(len(checks)==126 and all(x['passed']for x in checks),'three questions24answers126exactchecks')
for x in caps:
 v(h(R/x['capture_path'])==x['capture_sha256'],'original capture hash '+x['source_candidate_or_canonical_id']);v(h(R/x['text_path'])==x['text_sha256'],'parsed capture hash '+x['source_candidate_or_canonical_id'])
for x in re:
 for e in x.get('review_extracts',[]):v(h(R/e['path'])==e['sha256'],'retained context/extract hash '+x['source_id'])
for x in bridge['provenance']:v(h(W/x['path'])==x['sha256'],'original data provenance '+x['role'])
v(not bridge['actual_buyer_evidence']and not bridge['recommendation_counts_reused']and bridge['no_model_reruns'],'no demand/count transfer or reruns')
for p in B.glob('*.json'):rd(p)
v(True,'local JSON parse')
wr('verification.json',dict(date=D,status='passed_for_parent_integration_only',checks=vc,check_count=len(vc),new_source_routes=1,canonical_reuses=7,claim_candidates=3,prior_bridge_checks=126,selected_saved_records=24,semantic_rereads=3,actual_buyer_evidence=False,shared_edits=False,financial_inputs_added=0,external_actions=False))
for p in B.glob('*.md'):
 text=p.read_text()
 for a,b in [('October2026','October 2026'),('link24savedanswers','link 24 saved answers'),('repeat1','repeat 1'),('other21received','other 21 received'),('and24links','and 24 links'),('reports126lineage','reports 126 lineage'),('not126respondents','not 126 respondents'),("Oakleaf's28January2026article", "Oakleaf's 28 January 2026 article")]:text=text.replace(a,b)
 p.write_text(text)
print(json.dumps(dict(status='passed',local_checks=len(vc),bridge_checks=126,new_routes=1,reuses=7,claims=3)))
