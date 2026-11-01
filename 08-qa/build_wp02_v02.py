from pathlib import Path
import json
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / '06-client-checkpoints/week-one-v0.2'
OUT.mkdir(parents=True, exist_ok=True)
previous = ROOT/'01-method/question-map.json'
snapshot = ROOT/'01-method/question-map-v0.1.json'
if not snapshot.exists():
    old = json.loads(previous.read_text())
    assert old['version']=='0.1'
    snapshot.write_bytes(previous.read_bytes())

# Core wording is shared by the editable client pack and the analysis map.
Q = [
('Role in decisions', 'What is your role in decisions about payroll technology, providers or major process changes?', ['R04'], 'Establish actual decision involvement.', ['Distinguish recommending, evaluating, implementing and approving.'], 'all'),
('Operating context', 'How is payroll currently delivered in your area of responsibility?', ['R02','R03','R07'], 'Interpret the experience in its operating context.', ['In-house, outsourced or mixed; broad organisational scale; relevant countries and team responsibilities. Do not request employee records.', 'For outsourced or mixed delivery, clarify work retained by the employer, information supplied to providers and responsibility for handoffs.'], 'all'),
('Improvement priority', 'What, if anything, would you most like to improve about payroll in your organisation?', ['R02'], 'Identify the participant’s own priority before thematic prompts.', ['What consequence makes this important, and who is affected?', 'What currently works well and should be preserved?', 'Clarify whether the account is first-hand, based on internal reporting, or an interpretation.'], 'all'),
('Unmet needs', 'Where, if anywhere, do the payroll technology or services you use or have recently evaluated fall short of your needs?', ['R02','R03'], 'Identify a concrete capability or service gap without presuming dissatisfaction.', ['Ask for a specific example, workaround and where the problem begins.', 'Do you know of an option that would meet this need? If so, what explains why it is not being used?', 'Use the answer to distinguish perceived availability, suitability, affordability/value, readiness or ownership. Preserve not evaluated, not known and no significant shortfall; do not infer market absence.'], 'all'),
('Future priorities', 'Which payroll improvements, if any, do you expect your organisation to prioritise over the next 12–24 months?', ['R03','R07'], 'Separate ambition from organisational commitment.', ['For up to two priorities, establish whether each is an idea, under evaluation, in a plan, approved or being delivered. Clarify funding separately where relevant; preserve not known.', 'What would have to change for this priority to move forward or become less important?', 'Only after the unaided answer, use AI, automation, integration or outsourcing as optional prompts. Label prompted themes separately. If technology arises, clarify the task, pilot/live stage and oversight rather than assume a common definition.'], 'all'),
('Recent decision', 'Thinking about the past 24 months, what is the most recent payroll investment, provider renewal or proposed change in which you had direct involvement?', ['R04','R06'], 'Anchor the investigation in one recent real case.', ['Approximate timing, proposal type and direct involvement. Investment may include people, capability, training or controls as well as software and providers.', 'A substantive approval, renewal, re-scope or go-live decision in an older programme can qualify within the window. Record programme start and selected milestone dates separately; routine activity is not automatically a new decision.', 'If no recent case is recalled, and the participant is willing, ask: Has an improvement you mentioned been put forward internally? Choose the relevant follow-up: What happened next? Or: What has prevented it being raised?', 'Only never-raised needs are pre-proposal. If a qualifying recent case emerges, confirm it and resume Q007–Q013. Older-only or uncertain cases stay separately labelled context; otherwise continue to Q014. Do not repeat a declined request to share a case.'], 'all'),
('Decision reached', 'What decision had been reached on that proposal as of today?', ['R04','R06'], 'Establish the actual decision position independently of delivery.', ['Approved, declined, deferred, withdrawn/abandoned, pending, no formal approval required, not known or prefer not to disclose.', 'Separately ask what has been implemented, if applicable. Preserve chronology where an earlier approval was subsequently changed.'], 'recent_case'),
('Original trigger', 'What prompted this proposal or review?', ['R02','R04'], 'Connect the case with its initial need, intended outcome and opportunity.', ['What improvement was the proposal meant to deliver, and how would you know it had worked?', 'After the open answer, clarify any mandatory deadline, lifecycle/contract timing or discretionary opportunity. Do not presume failure or force a single trigger.'], 'recent_case'),
('Authority and influence', 'Who had the authority to approve or stop the proposal?', ['R04'], 'Identify decision power and conditions.', ['Sponsor, budget owner, final sign-off and veto or condition-setting roles.', 'Record functions rather than names. Separate known facts from the participant’s understanding.'], 'recent_case'),
('Evidence requested', 'What evidence, if any, was requested to assess the proposal?', ['R05'], 'Establish the business-case requirements and what value meant in this case.', ['After the unaided answer, select relevant probes: baseline/measure, cost scope, who expected to benefit, risk, compliance, continuity, capacity, references or a pilot.', 'Clarify implementation, ongoing support, training and transition costs if they mattered. Distinguish reduced spending from capacity at unchanged spending; do not monetise every benefit or double count.', 'Do not request confidential documents or exact budgets; not measured or not known are valid answers.'], 'recent_case'),
('Evidence that mattered', 'Which evidence, if any, appeared to influence the decision most?', ['R05','R08'], 'Distinguish evidence produced from evidence believed to affect a decision.', ['What makes you say it mattered?', 'Did the proposal or decision change after the evidence was supplied?', 'For a pending proposal ask: Which evidence, if any, has appeared to influence the assessment so far? For deferred cases retain the main question. For both pending and deferred cases also ask: What evidence, if any, is still needed before a decision can be made? Record routed wording.'], 'recent_case'),
('Alternatives and choice', 'What other options were considered?', ['R03','R06'], 'Understand the choice set and selected option.', ['Renewal, keeping the present arrangement, process change, another provider/platform, mixed solution or no change.', 'Which option, if any, was selected, and why? Retaining an incumbent is an option, not a decision disposition.', 'Where relevant, clarify whether staying was preferred on merit, constrained by transition or contract timing, or both. Do not assume lock-in.'], 'recent_case'),
('Conditions and constraints', 'What conditions or concerns, if any, most affected whether or when the proposal could proceed?', ['R05','R06','R08'], 'Explain conditions enabling progress, observed results and constraints.', ['After the unaided answer, select relevant probes: affordability, migration, integration, upstream data ownership, continuity, compliance, security, skills, training, adoption, capacity or competing priorities.', 'Ask what enabled progress as well as what constrained it. If useful, ask what supplier action could have reduced the barrier; label that as a proposed remedy rather than an observed effect.', 'If delivery permits: What has actually changed, and how is the result being assessed? Clarify the benefit owner, baseline/measure and assessment date where known. Where time or capacity was released, ask where it went.', 'Keep expected benefit, go-live, observed change and attribution separate. Not measured, not yet assessed, not applicable, not known and prefer not to disclose are distinct; none automatically means failure.'], 'recent_case'),
('Next research question', 'What is one question about payroll investment that you think the profession should answer next?', ['R08','T02'], 'Retain priorities beyond the researcher’s assumptions and inform future research.', ['Optional: advice to another payroll leader facing a comparable decision.', 'Answering does not imply council membership, recontact or attribution permission.'], 'all'),
]

records = []
for i,(title,wording,topics,purpose,probes,route) in enumerate(Q,1):
    records.append({'question_id':f'Q{i:03}', 'number':i, 'title':title, 'wording':wording,
        'topic_ids':topics,'purpose':purpose,'optional_probes':probes,'route':route,
        'part':'context' if i<3 else ('needs_and_priorities' if i<6 else ('case_selection' if i==6 else ('decision_case' if i<14 else 'closing'))),
        'routed_wording':{'pending':'Which evidence, if any, has appeared to influence the assessment so far?', 'pending_or_deferred_follow_up':'What evidence, if any, is still needed before a decision can be made?', 'deferred':'Retain the main question to capture evidence behind the deferral, then ask the follow-up.'} if i==11 else {}})
question_map={'schema_version':'1.1','version':'0.2','date':'2026-10-28',
    'status':'draft_for_user_review','client_approved':False,'participant_tested':False,
    'instrument_type':'Semi-structured qualitative guide','core_question_count':14,
    'population':'Proposed senior employer-side payroll decision-makers with UK-relevant responsibilities; outsourced payroll users eligible.',
    'recall_window_months':24,'records':records,
    'routing':{'no_recent_case':'Ask Q001–Q006. If willing, clarify whether a need was raised. Never-raised needs are pre-proposal; older-only or uncertain cases remain contextual. If no eligible recent case emerges, continue to Q014 and exclude from the recent-decision-case base.',
      'recent_case':'Ask all core questions for a confirmed recent case or substantive recent decision milestone. Select relevant probes; record programme start and selected decision dates separately.',
      'recalled_recent_case':'If the no-case follow-up reveals an eligible recent case, confirm timing and direct involvement then resume Q007–Q013.',
      'case_not_shared':'Respect a decision not to share. Do not use the follow-up to repeat a declined request; continue to Q014.',
      'written_mode':'Same core wording and routing, selective follow-ups, distinguish written responses.'},
    'route_states':{'recent_case':['confirmed_initial','confirmed_after_probe','recent_substantive_milestone'],
      'no_recent_case':['never_raised','older_only','unknown_eligibility','no_improvement','no_case_shared']},
    'priority_probes':['No-case clarification where relevant and welcome','Intended outcome and baseline/measure where known','Observed result and benefit assessment where delivery permits'],
    'analysis_rules':['Separate future priorities from selected historical case.',
      'Code decision disposition, chosen option and implementation status separately.',
      'Code benefit assessment separately from delivery: measured or observed change is not implied by go-live.',
      'Never-raised needs, older context and confirmed recent cases use different bases; do not force uncertainty into a case category.',
      'Gap explanations are participant-attributed, may overlap and do not prove that a market capability is absent.',
      'Record unanswered, not asked, not applicable, not known and prefer not to disclose separately.',
      'Keep quotations separate from paraphrase; participant attribution does not prove causation.',
      'No automatic population percentages or saturation claim from 6–10 contributions.']}
(ROOT/'01-method/question-map.json').write_text(json.dumps(question_map,indent=2,ensure_ascii=False)+'\n')
(ROOT/'01-method/question-map-v0.2.json').write_text(json.dumps(question_map,indent=2,ensure_ascii=False)+'\n')

md=['# Practitioner discussion guide','', 'Version 0.2 • 28 October 2026 • Internal draft for user review', '',
    'Proposed audience and questions require review before use. No participant testing or interviews have occurred.', '',
    '## Before the conversation', '',
    'Confirm eligibility and collection permissions. Explain JGA commissioning, Riseklix research support and intended publication/commercial licensing. Agree note-taking, any recording and separate attribution choices. Do not collect employee records, exact confidential budgets or unnecessary identities in this workspace.', '',
    'Use open questions first. Probes are a menu, not a checklist. Prioritise a relevant no-case clarification, intended outcome/baseline and observed result where delivery permits. Accept successful arrangements, no unmet need, justified renewal and deliberate no change. The earlier internal 30–40 minute estimate remains untested and may change; confirm burden after a real timing check. Written contributions use the same core with selective follow-up.', '']
for r in records:
    md += [f"## {r['question_id']} {r['title']}",'',r['wording'],'',f"Purpose: {r['purpose']}",f"Maps to: {', '.join(r['topic_ids'])}. Route: {r['route']}.",'']
    md += ['Optional probes:']+[f'- {p}' for p in r['optional_probes']]+['']
md += ['## Analysis controls','']+[f'- {s}' for s in question_map['analysis_rules']]+['',
    'Decision disposition: approved; declined; deferred; withdrawn/abandoned; pending; no formal approval required; not known; prefer not to disclose.',
    'Chosen option: incumbent retained; alternative provider/platform; internal process change; deliberate no change; mixed; none selected; not known; prefer not to disclose.',
    'Delivery: not started; underway; live/stabilising; operating/completed; paused; stopped; not applicable; not known; prefer not to disclose.',
    'Benefit assessment: measured result; reported change without a measure; not yet assessed; not measured; not applicable; not known; prefer not to disclose. Separately record direction and source of the result, including mixed or adverse outcomes.',
    'Preserve dates, chronology, exact instrument version and routed wording. Eligibility for a case and permission to publish are separate.']
(ROOT/'01-method/PRACTITIONER-GUIDE-v0.2.md').write_text('\n'.join(md)+'\n')

def base(label):
    d=Document(); s=d.sections[0]
    s.page_width=Inches(8.5);s.page_height=Inches(11)
    s.top_margin=Inches(.65);s.bottom_margin=Inches(.65)
    s.left_margin=Inches(.75);s.right_margin=Inches(.75)
    s.header_distance=Inches(.25);s.footer_distance=Inches(.25)
    for sty in d.styles:
        if sty.type==1:
            sty.font.name='Arial';sty.font.color.rgb=RGBColor(0,0,0)
            if sty.element.pPr is not None:
                for b in list(sty.element.pPr.findall(qn('w:pBdr'))):sty.element.pPr.remove(b)
    normal=d.styles['Normal']; normal.font.size=Pt(11)
    normal.paragraph_format.space_after=Pt(7);normal.paragraph_format.line_spacing=1.08
    caption=d.styles['Caption'];caption.font.size=Pt(10);caption.font.bold=False;caption.font.italic=False
    for name,size in [('Title',26),('Subtitle',11),('Heading 1',18),('Heading 2',12),('Heading 3',11)]:
        st=d.styles[name];st.font.size=Pt(size);st.font.color.rgb=RGBColor(0,0,0)
        st.paragraph_format.space_before=Pt(10 if name.startswith('Heading') else 0)
        st.paragraph_format.space_after=Pt(6)
    h=s.header.paragraphs[0];h.text='JGA RECRUITMENT GROUP  /  RESEARCH 2027';h.style='Caption'
    h.runs[0].font.size=Pt(8);h.runs[0].font.color.rgb=RGBColor(0,0,0)
    f=s.footer.paragraphs[0];f.paragraph_format.space_before=Pt(0)
    f.add_run(label+'  |  28 October 2026  |  ')
    field=OxmlElement('w:fldSimple');field.set(qn('w:instr'),'PAGE');f._p.append(field)
    for r in f.runs:r.font.size=Pt(8)
    return d

def p(d,text,style=None):
    pp=d.add_paragraph(text,style);return pp
def h(d,text,l=2):return d.add_heading(text,l)
def lead(d,label,text):
    pp=d.add_paragraph();pp.add_run(label+(' ' if label.endswith('?') else '. ')).bold=True;pp.add_run(text);return pp
def page(d,title):
    d.add_page_break();h(d,title,1)
def bullet(d,text):return p(d,text,'List Bullet')

d=base('Research plan for review')
d.add_heading('JGA Payroll Research Plan',0)
p(d,'Proposed scope and practitioner questions', 'Subtitle')
p(d,'Prepared for Nick Day and Mark • Version 0.2 for review')
p(d,'We propose a report that connects what payroll leaders want to improve with the decisions that fund, delay or stop change. This pack sets out the readership, chapter structure and questions for review before practitioner collection begins.')
h(d,'The central research question')
p(d,'What do payroll leaders need, and what determines whether those needs become approved and delivered investment?')
h(d,'Who the report is for')
p(d,'Proposed primary readers are senior employer-side payroll leaders and the finance, HR and technology decision-makers who assess payroll investment. Start with UK-relevant responsibilities, including international remits. Employer-side users of outsourced payroll are included.')
h(d,'How the evidence will be built')
bullet(d,'Review and reference existing industry research, then investigate specific decision cases rather than repeat a broad trends survey.')
bullet(d,'Target 6–10 distinct verified senior payroll practitioner contributions through JGA introductions, subject to availability and permission.')
bullet(d,'Explore unresolved needs, including those never proposed internally. Where available, examine one recent decision or substantive milestone, including success, renewal, delay, rejection and abandonment.')
bullet(d,'Synthesize the evidence into a Payroll Investment Decision Framework. Qualitative contributions explain experiences; they do not establish representative market percentages.')
h(d,'What we need you to review')
p(d,'Please confirm the proposed audience and geography, chapter coverage and core questions. On page 5, we set out the introduction route, materials and dates to agree. The separate two-page prospectus can then support feedback from selected contacts.')

page(d,'Proposed report structure')
p(d,'Working title: The Payroll Investment and Transformation Report 2027. The edition year describes its planning focus; source and fieldwork dates will be recorded accurately.')
p(d,'The design target is approximately 20–24 pages including methods and references, adjusted to the evidence rather than used as a fixed limit. An executive summary opens the publication.')
h(d,'Part One  What leaders want')
lead(d,'1  Operating reality','What works, where friction occurs and who is affected, with brief historical context on recurring ambitions and changed conditions.')
lead(d,'2  Technology and service needs','Capability, fit, affordability and readiness gaps, including needs never proposed. Examine workarounds across people, systems, services and data handoffs.')
lead(d,'3  Priorities and commitment','The next 12–24 months: desired, evaluated, planned and funded work, plus dated signals and conditions that could change priorities.')
h(d,'Part Two  How investment decisions happen')
lead(d,'4  The decision pathway','Who recommends, sponsors, funds, approves or can stop a proposal, and where conditions enter the process.')
lead(d,'5  The business case','Intended value, baseline, affordability, cost scope and who benefits; which evidence decision-makers request and what appears to influence the decision.')
lead(d,'6  Progress and constraints','What enables or blocks progress, and how go-live differs from observed improvement. Explain delay, decline or abandonment and any result assessment.')
lead(d,'7  Staying or switching','When renewal, an alternative supplier, a process change or deliberate no change is the chosen option.')
h(d,'Conclusion  From Ambition to Investment')
lead(d,'8  The practical framework','A repeatable route from an operational need to a credible case, decision and delivery review, grounded in the research.')
p(d,'Methods, references and evidence notes will make source populations, dates and permissions clear. Proposed case summaries and original graphics will be built from the collected evidence. No validated confidence index is assumed for this first edition.')

page(d,'Practitioner questions one to seven')
p(d,'Two context questions precede the guide. Ask open questions first; follow-ups are selective. Contributors may skip questions or avoid confidential details.')
short = {
1:'Follow-up: recommending, evaluating, implementing or approving.',
2:'Clarify broad scale, countries and delivery model. For outsourced/mixed delivery, ask what work remains internal.',
3:'Follow-up: why it matters, who is affected and what already works well.',
4:'Ask for an example and workaround. Clarify fit, cost or readiness where relevant; no significant shortfall is a valid answer.',
5:'For up to two priorities, clarify stage and funding. Ask what could change the priority. If technology arises, clarify its actual task and stage of use.',
6:'Record dates and involvement; people/capability changes and recent decision milestones in older programmes can qualify. If no case is recalled, ask whether a need was raised, then what happened or what prevented it. Resume 7–13 if an eligible recent case emerges; otherwise go to 14. Keep never-raised needs and older cases separate. Respect a choice not to share.',
7:'Record approval, decline, deferral, withdrawal, pending or no formal approval required. Separately record delivery status and any change in the decision.'}
for i in range(1,8):
    title,wording,*_=Q[i-1];h(d,f'{i}  {title}');p(d,wording);p(d,short[i],'Caption')

page(d,'Practitioner questions eight to fourteen')
p(d,'Questions 8–13 refer to the same recent case. The final question is open to every eligible contributor.')
short.update({
8:'Ask what improvement was intended and how success would be recognised. Clarify any deadline, lifecycle or discretionary trigger.',
9:'Follow-up: sponsor, budget owner, sign-off and veto roles. Record roles rather than names.',
10:'Select relevant follow-ups: baseline/measure, cost scope, who benefits, risk and capacity. Distinguish released time from reduced spending.',
11:'If pending, ask what evidence has influenced the assessment so far. If deferred, retain the main question. For both, also ask what evidence is still needed.',
12:'Ask which option was selected and why. Clarify preferred retention versus transition or contract constraints where relevant.',
13:'Ask what enabled progress too. Where delivery permits, ask what changed, who assesses it and where any released capacity went. Keep expectations, go-live and observed results separate; not yet assessed is valid.',
14:'Optional follow-up: advice for another payroll leader facing a similar decision.'})
for i in range(8,15):
    title,wording,*_=Q[i-1];h(d,f'{i}  {title}');p(d,wording);p(d,short[i],'Caption')

page(d,'Introductions and next decisions')
h(d,'Who would be useful to involve')
p(d,'Please forward the brief below to senior employer-side payroll leaders with direct involvement in technology, provider or major process decisions. We will seek varied operating models and outcomes, including successful change and sensible renewal. People without a recent case can contribute on needs and priorities.')
h(d,'Suggested introduction brief')
p(d,'JGA is commissioning The Payroll Investment and Transformation Report 2027, with research support from Riseklix. We are exploring what payroll leaders want to improve and what makes payroll investment get approved, delayed or abandoned.')
p(d,'We would value your perspective through a structured conversation or an equivalent written response, ideally drawing on a decision or substantive milestone from the past 24 months. We also welcome needs that have not become proposals. Participation is voluntary; you can skip questions or avoid confidential details.')
p(d,'The findings are intended for a JGA publication that may also be commercially licensed. Any named quotation or identification of your employer would require separate permission. Would you be open to contributing? We can share the questions and practical arrangements before you decide.')
h(d,'The Table is a separate feasibility question')
p(d,'Alongside the report, we will assess research-only licensing and an event-supported research model. Up to four exploratory conversations are planned, ideally two potential commercial buyers and two prospective council members. Council members count toward the 6–10 only where they also provide an eligible, permissioned report contribution; each person is counted once.')
h(d,'Inputs and timing to agree')
bullet(d,'Confirm the readership, geography, outline and questions, plus any essential topic we have missed.')
bullet(d,'Nominate an introduction coordinator and supply JGA brand assets or publication examples.')
bullet(d,'Agree collection tools, permissions and access arrangements before participant data is collected. Confirm the conversation length after a timing check.')
bullet(d,'Confirm the kickoff, first-week checkpoint and review date. The working plan remains approximately three working weeks from the agreed kickoff, subject to timely access and feedback.')
p(d,'Once the focus and collection arrangements are agreed, we will retain the approved version and begin introductions and practitioner collection.')
d.save(OUT/'JGA Research Plan and Practitioner Questions.docx')

d=base('Research prospectus')
d.add_heading('The Payroll Investment and Transformation Report 2027',0)
p(d,'Research prospectus • Proposed first edition', 'Subtitle')
p(d,'Commissioned by JGA Recruitment Group with research support from Riseklix')
h(d,'What turns a payroll need into an investment decision',1)
p(d,'Payroll leaders may know what they want to improve. Getting a proposal evaluated, approved and delivered involves another set of decisions: who owns it, what evidence is needed, which alternatives are credible and what the organisation can implement.')
p(d,'This proposed report connects decisions with operational needs, including improvements that never become proposals. It builds on existing research and recent practitioner experience to examine the path from ambition to investment.')
h(d,'Two questions shape the research')
lead(d,'What do leaders want but struggle to obtain?','The capabilities, service expectations and improvements that matter, alongside what already works and should be preserved.')
lead(d,'What determines whether change proceeds?','The approval process, business case and delivery conditions behind investment, renewal, delay, rejection or abandonment.')
h(d,'The planned publication')
lead(d,'Part One','Operating needs, technology and service gaps, and future priorities distinguished from approved commitments.')
lead(d,'Part Two','Decision ownership, credible evidence, constraints and choices about staying, switching or changing a process. Approval and go-live will be distinguished from observed benefits.')
lead(d,'From Ambition to Investment','A practical Payroll Investment Decision Framework that brings the findings together for leaders assessing their next proposal.')
h(d,'Intended readers')
p(d,'Senior employer-side payroll leaders and the finance, HR and technology stakeholders who assess payroll investment. The proposed initial focus is UK-relevant responsibilities, including international remits and employer-side users of outsourced payroll.')

page(d,'How the research will be useful')
h(d,'Evidence and practitioner experience')
p(d,'The research will combine referenced industry sources, original analysis and a target of 6–10 distinct verified senior payroll practitioner contributions through JGA introductions, subject to availability and permission.')
p(d,'Conversations or structured written contributions will examine a recent real decision where available. Successful projects, sensible renewals and deliberate no-change decisions are relevant alongside delayed or abandoned proposals. These contributions provide explanation and context rather than representative market estimates.')
h(d,'What readers will be able to use')
bullet(d,'A clear account of priorities, gaps and purchasing realities, with the evidence behind each finding.')
bullet(d,'Decision-case insights that connect the initial need with the evidence, people and conditions affecting the outcome.')
bullet(d,'A reusable framework to help structure a proposal, assess alternatives and identify what is needed before proceeding.')
bullet(d,'A concise executive summary, original graphics and transparent source and method notes.')
h(d,'Help shape the first edition')
p(d,'We would welcome feedback on three points:')
lead(d,'1','Which specific business decision, if any, could this research help you make?')
lead(d,'2','What evidence, context or unanswered question would determine whether it is useful? What would duplicate material you already have?')
lead(d,'3','For commercial research buyers: how do you currently obtain this insight, and who evaluates a purchase? For practitioners: would contributing be worthwhile, and what would make participation practical?')
h(d,'Publication and participation')
p(d,'This is an early prospectus, not completed findings or a final commercial offer. Publication and potential licensing arrangements will be defined separately. Participation is voluntary; named quotations and employer identification require separate permission.')
p(d,'The report will also inform a separate assessment of The Table, a proposed research council and possible event-supported model. No event programme or partner commitments are being announced through this prospectus.')
p(d,'For feedback and contribution enquiries, contact Nick Day at JGA Recruitment Group or Satwik Kumar at satwik@riseklix.com.')
d.save(OUT/'JGA Payroll Research Prospectus.docx')
print(json.dumps({'question_records':len(records),'created':[str(p) for p in OUT.glob('*.docx')]},indent=2))
