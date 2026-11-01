from pathlib import Path
import json,hashlib
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'01-method/collection-pack-v0.1'
def read(p):return json.loads((ROOT/p).read_text())
def write(p,d):(BASE/p).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n' if not isinstance(d,str) else d)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
q=read('01-method/question-map.json');assert q['version']=='0.2' and len(q['records'])==14
scope=read('00-control/scope-baseline.json')
agreement=Path(scope['documents']['agreement_text'])
assert agreement.is_file()
contract=dict(source_path=str(agreement),source_sha256=sha(agreement),executed_copy_retrieved=False,working_role='JGA controller and Riseklix processor for participant information processed on JGA’s behalf; each separately responsible for own business-contact/invoicing/legal records.',role_change_rule='Document a materially different research role before collection.',provider_location='India',tools_rule='No sub-processor or external recording/transcription/AI service receives identifiable or confidential research data without JGA prior written authorisation and appropriate contractual safeguards.',access_rule='Record approved tools, recipients, hosting and access locations before collection; establish any required international-transfer safeguards and assessment before JGA-controlled personal data is made accessible outside the UK. The agreement is not itself an IDTA.',fallback_rule='JGA may retain identifiable contacts/responses and supply genuinely anonymised material while required safeguards are not in place. Do not treat remote access or pseudonymous records as anonymisation.',return_or_delete_days=30,backup_deletion_days=90,closure_trigger='Completion or termination; at JGA choice, with technically necessary backups and protected legally required-record exceptions as stated in section12.',participant_notice_rule='JGA supplies appropriate notices and lawful collection instructions; actual permissions and attribution/quotation/sharing limits recorded.',sensitive_data_rule='Do not request employee payroll records, special-category data or unnecessary personal information.',legal_compliance_certified=False)
decisions=[
 ('READY01','Focus, guide and introduction route','Client confirmation of the proposed population/focus, current core guide and practical introduction route; actual working dates/burden agreed.','Nick/JGA with Satwik','DEC-002, DEC-004, DEC-006 and existing WP02 review remain open.'),
 ('READY02','Actual data flow and authorised access','Document the tools/storage, authorised people/recipients, hosting/access locations, security/retention implementation and any required transfer route/assessment.','JGA and Riseklix designated contacts','Contract section12 is the baseline; no account or tool has been approved through this pack.'),
 ('READY03','Participant information and collection instructions','JGA-approved privacy information, lawful collection instructions, actual contact/rights and incident-escalation route, purpose/recipient/retention details and correction/withdrawal handling.','JGA, supported by Riseklix','Voluntary research agreement is separate from selecting a data-protection lawful basis; no basis automatically chosen.'),
 ('READY04','Publication and optional uses','Define this edition/report/licensing scope, de-identification checks, quote/name/employer clearance and any future-use/recontact/Table choices separately.','JGA and participant through approved route','No assumed future-edition reuse, personal-data sale or sponsor access; contract rights remain subject to participant restrictions.'),
 ('READY05','Release and first collection','User permission for the exact external message/route, client/data arrangements confirmed, actual participant information/choices provided and recorded before collecting substantive input.','Satwik/user; JGA for its instructions','No sending or collection is authorised by an empty template or a synthetic check.'),
]
write('REVIEW-DECISIONS.json',dict(date='2026-10-29',version='0.1',status='prepared_for_user_client_review_not_activated',working_contract=contract,release_decisions=[dict(decision_id=i,title=t,needed_before_use=n,responsible_party=o,status='not_confirmed',resolution=None,confirmation_reference=None,basis=b) for i,t,n,o,b in decisions],additional_document_control=dict(executed_agreement_reconciliation='pending',not_a_reason_to_stop_public_research=True,does_not_silently_override_working_contract=True),actual_tool_selection=None,actual_restricted_storage=None,actual_authorised_access_list=[],actual_notice_version=None,actual_lawful_instructions_reference=None,actual_transfer_arrangement_reference=None,user_send_permission_reference=None,collection_ready=False,legal_compliance_certified=False,external_actions=[]))

choice_names=['participation_and_notes_or_written_response','deidentified_report_publication_scope','recording_if_proposed','exact_quotation_specific_extract','name_and_role_specific_wording','employer_identification_specific_wording','council_recognition','contribution_clarification_recontact','future_research_invitation','future_edition_reuse_if_proposed','Table_exploratory_information']
choices={name:dict(answer=None,scope_or_exact_wording=None,information_version=None,choice_date=None,evidence_reference=None,restrictions=None) for name in choice_names}
templates=dict(version='0.1',date='2026-10-29',status='blank_design_only_do_not_populate_here',use_location='Only the agreed restricted collection environment, after readiness/release decisions. This ordinary workspace is not approved participant storage.',all_templates_are_blank=True,choice_values=['yes','no','not_asked','needs_clarification','withdrawn_or_changed'],blank_is_not_yes=True,participation_choice_is_not_automatically_GDPR_lawful_basis=True,restricted_identity_lookup={k:None for k in ['participant_id','minimal_identity_contact_reference','introduction_source','actual_professional_remit','report_eligibility_verification_basis','verification_date','permitted_workstream_roles','restricted_permission_reference']},restricted_permission_record=dict(participant_id=None,information_and_notice_version=None,purposes_explained=None,permission_evidence_date=None,choices=choices,change_or_withdrawal_reference=None,agreed_release_review_limits=None),contribution_note=dict(contribution_id=None,participant_id=None,purposes_actually_covered=None,collection_date=None,mode=None,guide_version=None,concept_version_if_applicable=None,selected_case_event_and_remit_if_known=None,permission_reference=None,questions_actually_covered=[],routed_wording_used=None,source_and_knowledge_basis=None,safe_context_limit=None,response_entries=[],note_review_status=None,followup_limits=None),response_entry={k:None for k in ['question_id','text','text_type_quote_paraphrase_or_analyst_interpretation','missingness','source_and_direct_knowledge','scope_event_time_account_time_if_known','relevant_code_or_module','qualification_or_contrary_evidence','permitted_use_reference']},publication_item={k:None for k in ['item_id','contribution_reference','exact_text_or_summary','intended_edition_output_audience','quote_paraphrase_or_aggregate','name_role_employer_display_if_any','permission_scope_reference','context_identification_review','factual_or_quote_check_if_agreed','release_decision_and_reference']},restricted_request_or_change_log={k:None for k in ['request_id','participant_reference','received_date','request_scope','forwarded_to_JGA_reference','instruction_or_resolution_reference','affected_material_references','action_and_date_if_authorised']},blank_analysis_transfer_check={k:None for k in ['material_reference','actual_data_form_and_identification_risk','purpose_and_recipient','approved_route_reference','minimum_context_needed','source_permission_limits','release_review_reference']},blank_count_record={k:None for k in ['participant_id','report_eligible_verified','actual_usable_report_input','analysis_use_permitted','report_count_once_decision','question_base_limits','Table_substantive_event_references','publication_items_cleared_separately']},actual_participants=[],actual_permissions=[],actual_contributions=[],actual_Table_events=[],actual_publication_items=[],actual_rights_or_change_requests=[],actual_transfer_events=[])
write('RECORD-TEMPLATES.json',templates)

routes=read('01-method/research-notes/wp03/routes/route-requirements.json')
policy=dict(version='0.1',status='prepared_policy_not_activated',report_target_min=6,report_target_max=10,report_unit='distinct_verified_eligible_person_with_actual_usable_permitted_report_input',table_event_cap=4,table_ideal_mix=dict(buyers=2,members=2),mix_is_not_a_fixed_quota=True,participant_id_prefix='P',contribution_id_prefix='INT',one_person_reference_across_modes_and_streams=True,report_count_rule='Count once only after relevant eligibility/verification, actual usable input and permitted analysis are established. No fixed number of answered questions; preserve no-case and written routes.',Table_count_rule='Count actual substantive exploratory conversation/contribution events, not role labels. One combined event is one event; repeated substantive sessions remain separate events within cap. Log factual clarifications honestly with scope, not a blanket exemption.',overlap_rule='A prospective member/buyer counts once toward report only if independently report-eligible and supplies actual relevant permitted report input; an RSVP or question suggestion alone does not establish that.',publication_base_rule='Analysis usability, named/quote release and question-specific reporting bases differ; publication permission is item/output-specific.',routes=routes['routes'],missingness_values=routes['missingness_values'],guide_references=dict(report='01-method/PRACTITIONER-GUIDE-v0.2.md',report_question_map='01-method/question-map.json',table='01-method/TABLE-VALIDATION-GUIDES-v0.1.md'),core_question_version='0.2',report_core_questions=14,new_core_questions=0,extra_optional_framework_fields_are_not_compulsory_probes=True,recording_default_enabled=False,external_AI_transcription_default_enabled=False,written_equivalent_allowed=True,duration_tested=False,fixed_duration_promised=False,actual_report_contributor_count=0,actual_Table_event_count=0,actual_records=[],external_actions=[])
write('COUNT-AND-ROUTING-POLICY.json',policy)

write('START-HERE.md','''# JGA collection pack

Version 0.1 | 29 October 2026 | Local review draft

This pack prepares the practitioner and Table collection process. It contains no participant data, tool approval or authority to send. The existing 14-question guide and Table guides remain unchanged. Public research can continue while collection decisions are confirmed.

## What is ready to review

| File | Purpose |
| --- | --- |
| [Operator runbook](OPERATOR-RUNBOOK.md) | Introductions, collection routes, notes, counts, publication checks and closure. |
| [Introduction and invitation drafts](INTRODUCTION-DRAFTS.md) | A concise coordination email to Nick and later practitioner invitation. Both are unsent. |
| [Participant information draft](PARTICIPANT-INFORMATION-DRAFT.md) | Short purpose/choice information plus the privacy details JGA must settle before use. |
| [Permission choices](PERMISSION-CHOICES.md) | Separate relevant optional uses without a blanket agree-to-all form. |
| [Blank record templates](RECORD-TEMPLATES.json) | Identity, permissions, contribution notes and release records for use only in approved restricted storage. |
| [Count and routing policy](COUNT-AND-ROUTING-POLICY.json) | Six to ten distinct report contributors; up to four Table events, with legitimate overlap counted accurately. |
| [Decisions before use](REVIEW-DECISIONS.json) | Actual route, tools, instructions, notice, permissions and sending confirmation. |

## What the agreement already establishes

For information processed on JGA's behalf, the working section 12 identifies JGA as controller and Riseklix as processor; own business-contact/legal records are separate. A materially different role must be documented. JGA supplies appropriate notices and lawful instructions. Actual tools, authorised access, recipients and locations still need recording, with any required international-transfer safeguards before outside-UK access. The agreement itself is not a transfer mechanism.

At JGA's choice, participant personal data is returned or securely deleted within 30 days after completion or termination; remaining technically necessary backups within 90 days, subject to the agreement's protected legally required-record exceptions. These are working contractual terms, not newly invented participant-retention or withdrawal deadlines. The executed copy remains to be reconciled.

The proposed minimum route is manual notes or equivalent written input, without recording or external AI/transcription. It is a proposal until the actual storage/access and instructions are confirmed. No identifiable or confidential contribution belongs in this workspace.

## Before sending or receiving input

Resolve the five grouped decisions in the JSON: focus/introduction/timing; actual data flow/access; JGA notice and lawful instructions/contact route; publication/optional-use scope; and permission to release the exact message/collection route. Do not ask for contacts or response histories in an unapproved channel while waiting. This is a concrete collection arrangement to review, not a new contract or legal-compliance certification.

An appropriate alternative under the agreement is for JGA to retain identifiable records and supply genuinely anonymised material. That route still needs its actual purpose, permissions and identification-risk handling agreed; removing names or using participant IDs alone does not make material anonymous.

See the [supporting data decisions](../research-notes/wp03/data/DATA-ARRANGEMENT-DECISIONS.md), [route design](../research-notes/wp03/routes/COLLECTION-ROUTES.md) and [participant wording review](../research-notes/wp03/wording/PARTICIPANT-WORDING.md). Original participant contributions, fieldwork readiness and final deliverables remain open. Nothing sent or collected.
''')

write('OPERATOR-RUNBOOK.md','''# Collection operator runbook

Version 0.1 | 29 October 2026 | Prepared for review, not activated

## Start with the existing instrument

Use [the report guide version 0.2](../PRACTITIONER-GUIDE-v0.2.md), with its 14 unchanged core questions and selective probes. Use [the Table guides](../TABLE-VALIDATION-GUIDES-v0.1.md) for their separate purposes. R08's six views and evidence notes are analyst aids, not another questionnaire or a list to complete on every call.

1. Confirm the focus, actual introduction and collection/data route, applicable participant information and permission to send. Do not begin from an unfilled form or an assumed tool approval.
2. Use a minimal permission-first introduction. JGA can ask whether a person wishes to receive the information without passing a private case history to Riseklix. Do not request identity documents, employee records or exact private budgets.
3. In the approved environment, assign one stable P reference per person and a separate INT reference per contribution. Record actual remit and professional-profile or JGA verification basis; title/introduction alone does not complete eligibility or permission.
4. Explain the report purpose and defined publication/licensing uses. Explain any Table/commercial feasibility purpose separately before covering it. Agree notes/written response and relevant optional uses; unanswered choices are not yes.
5. Collect only the route the person is willing and able to discuss. A practical mode and time are agreed before scheduling. The earlier 30–40-minute estimate is untested, not a promised slot. Recording is off unless the actual tool, permissions, instructions and handling have been separately cleared.
6. Capture the actual questions, guide/version, date/mode, routed wording and knowledge basis. Label exact quotations, paraphrase and analyst interpretation distinctly. Keep relevant event/account times, scope, contrary evidence and unresolved gaps without demanding a full approval dossier.
7. Review usability and permissions separately. Code permitted observations; later public wording must fit the actual output/use permission and contextual identification review. Follow any agreed quote/factual-check process. A general statement of willingness to be quoted is not approval of an arbitrary later extract.
8. Reconcile people, report contributions, Table events and publication items. Report no-case and question-specific bases accurately. Do not replace missing originals with public cases or AI answers, or quietly reduce the target; flag access shortfalls and agree a route/timetable/sample change with JGA.

## Route without forcing a case

| Account | Use the existing guide this way |
| --- | --- |
| Qualifying event within the past 24 months | Confirm the event/direct involvement, including a substantive recent milestone in an older programme; use Q007–Q013 selectively. |
| No recent case | Useful operating/priorities input remains valid. Use the willing Q006 clarification, then Q014 unless a qualifying case emerges. |
| Need never raised internally | Label pre-proposal only if that fact is supplied. Do not infer pending, rejected or deferred. |
| Only older or uncertain context | Keep it separately labelled; no automatic recent-case classification. |
| Declined detail | Stop that request. Continue a permitted remaining route only if the person wishes. |
| Written response | Use the same version and relevant core. Do not require every probe or promise equivalent depth. |
| Adequate service, renewal or no change | Preserve it as useful evidence; no manufactured dissatisfaction, sale or hire. |

Preserve not asked, not answered, not known, not applicable, not measured, not yet assessed and prefer not to disclose where relevant. Decision, chosen option, commitment, delivery and benefit are not one progress score. Accepted evidence and a belief about its influence remain distinct from independent support and causality.

## Count the right unit

The report target is 6–10 distinct verified eligible people with actual usable permitted report input. One person can contribute in writing and by call and still counts once. A fixed number of answered questions is not required. A no-recent-case contribution can be useful; recent-case coverage is a separate base.

The Table includes up to four actual substantive exploratory contribution events, ideally two buyer and two member conversations. One combined session is one event, not two because roles differ. Repeat substantive Table sessions still consume events. Record short factual clarification and its treatment honestly rather than invent an automatic exemption.

A prospective member or commercial buyer overlaps with the report only if independently eligible and providing actual relevant permitted report input. An RSVP, introduction, question suggestion or commercial interest alone is insufficient. An eligible permissioned pilot can count only where actual input, version and comparability qualify; it is not a free extra collection exercise.

## Data flow, public release and closure

Store identity/contact, permissions and identifiable notes only in the agreed restricted environment. This repository contains blank designs and no participant data. A P reference is not anonymisation. Before any analysis transfer, verify the actual approved route, minimum context and permission/identification risks; do not upload raw material into an AI, recording or transcription tool simply because it is available.

If unsolicited identifiable/confidential material arrives through another channel, do not copy it into this workspace or unapproved tools. Flag the handling issue to the authorised project contact and follow documented instructions; do not claim remote copies were removed or that the incoming channel became approved.

For each proposed quotation, named contribution, employer reference or contextual summary, use a publication-item record with the exact intended wording/output and applicable permission. Do not promise anonymity merely because a name was removed. No sale of participant contact/identity records or automatic sponsor outreach is part of the report licence.

Forward permission changes/individual requests to JGA through the agreed route, preserve what was requested and follow authorised instructions. Explain correction/withdrawal and distributed-output limits accurately in the final information; no invented cutoff or blanket promise to recall all copies. Keep research-participation choices distinct from the project's selected lawful processing basis.

At closure, follow JGA's documented return/deletion choice under working section 12: 30 days after completion/termination and technically necessary backups within 90 days, with the agreement's legal-record exceptions. Record completion evidence in the approved environment. Do not start a new retention clock from each interview or silently extend the period for future editions.

No incentive, venue, subscription, recording service or other spending commitment is authorised. The report/Table scopes, guide approval, executed-copy reconciliation and data arrangements remain open. Nothing sent or collected by this runbook.
''')

write('INTRODUCTION-DRAFTS.md','''# Introduction and invitation drafts

Version 0.1 | 29 October 2026 | Unsent, not authorised for release

These drafts use no actual recipient list. The first coordinates focus and arrangements; it does not request transfer of identifiable records now. The later invitation is for a practitioner after the agreed route is ready. A buyer feasibility conversation requires its own honest commercial-purpose introduction.

## Coordination email to Nick

Subject: Practitioner contributions for the JGA report

Hi Nick,

The research design and draft framework are ready for practitioner input.

For the proposed UK-relevant focus, we are looking for 6–10 senior payroll professionals with direct involvement in payroll decisions. A useful mix would include changes that progressed, sensible renewals, and proposals that were delayed or stopped. Written responses or a short structured conversation can both work.

Could you confirm that focus and the best introduction route? We can then settle the participant information and practical collection arrangements before introductions begin. For now, please keep identifiable contact details and responses with JGA rather than forwarding them.

The Table discussions will be separate. Eligible council-member input can also contribute to the report with permission, counting each person once.

Best,
Satwik

## Later practitioner invitation

Subject: Your perspective for JGA’s payroll research

Hi,

Nick suggested your experience could be relevant to JGA’s Payroll Investment and Transformation Report 2027.

We are exploring what payroll leaders want to improve and how actual decisions progress, including renewals, delayed proposals and decisions not to change. A short conversation or written contribution would both be welcome, whichever is more practical.

The participant information explains the purpose, handling and your choices. There is no need to share employee information or confidential documents, and taking part does not commit you to The Table or an event.

If this is of interest, we can agree a suitable format.

Best,
Satwik

## Release notes for the operator

Do not send until the review decisions and exact message/route have user permission. Do not claim Nick suggested someone unless true. Supply the completed participant/privacy information through the agreed route before substantive input; never send a placeholder link. Agree timing without presenting the old untested estimate as validated. No automatic future-edition reuse, marketing or sponsor access is conveyed by either draft.
''')

write('PARTICIPANT-INFORMATION-DRAFT.md','''# Participant information: working text

Version 0.1 | 29 October 2026 | Incomplete notice, for review only

## Short purpose and choice information

JGA Recruitment is commissioning The Payroll Investment and Transformation Report 2027, with research support from Riseklix. We would value your perspective on payroll needs and a decision you were involved in, including improvements that progressed, sensible renewals or changes that did not go ahead.

You can contribute through a short structured conversation or written responses. We will agree a practical format with you. Participation is voluntary: you can skip questions, decline case detail or stop the discussion. Please avoid employee payroll records, confidential documents, exact private budgets and information you are not authorised to share.

Your input will inform this JGA report and the specific research uses explained to you, which may include publication and commercial licensing. Identifiable responses will be handled confidentially. We will review context before using a de-identified summary, since removing a name does not always prevent recognition.

Recording, exact quotations, naming you or your employer, and later contact are separate choices. Taking part does not enrol you in The Table, commit you to an event or purchase, or give sponsors access to you. The agreed privacy information, contact route and correction/withdrawal process will be provided before you decide.

## Information to complete before this is used

This short block is not a complete privacy notice and must not be sent alone. JGA must confirm the actual controller/contact details and lawful collection instructions, purposes and specific output/reuse scope, relevant recipients, tools and access/hosting locations, retention/rights and any applicable access/transfer information. The working contract already sets on-behalf roles and provider return/deletion terms; those do not by themselves complete the participant notice or establish a lawful basis.

Agree the actual correction/withdrawal route and practical publication/distribution limits. Do not invent a deadline, promise unlimited recall, imply that all future research is covered or preselect every optional use. Clarify any restricted context before it is collected or released. The no-recording proposal does not approve any particular note-taking or email platform.

For operator decisions see [review decisions](REVIEW-DECISIONS.json) and [permission choices](PERMISSION-CHOICES.md). The information version actually used and actual choice evidence belong in the approved restricted register. Nothing has been sent or accepted.
''')

write('PERMISSION-CHOICES.md','''# Separate participation and use choices

Version 0.1 | 29 October 2026 | Draft prompts, not permissions already obtained

Use only the choices relevant to the actual mode and proposed use, after supplying the completed information. These are not new research questions or a compulsory agree-to-all form. Participation agreement is distinct from the project's data-protection lawful basis. Missing/unclear choices are not yes; a participant may decline an optional use without pressure to accept it.

| Choice | Draft wording | What to record |
| --- | --- | --- |
| Participation and notes/written response | Are you happy to take part on the basis of the information provided, with written notes or the written response you choose to supply? | Information/notice version, mode, actual answer, date and evidence. |
| De-identified report use | May we use a de-identified summary in this report and the specific publication/licensing uses described? Are there details to omit or review? | Exact output/edition scope, contextual restrictions and identification check. |
| Recording, only if proposed | Would you be comfortable with a recording for the agreed purpose? It is optional; we can use notes instead. | Actual approved tool/access/purpose/handling and separate permission before activation. No automatic transcription or AI permission. |
| Exact quotation | May we use this exact passage for the described report use? | Exact extract/context and permission scope; follow any agreed wording check. Do not convert paraphrase into a quotation. |
| Name and role | Should this approved item carry the name and role wording shown to you, or keep identifying details out? | Exact display wording and item/use. No answer means no named release. |
| Employer identification | May this approved contribution identify your employer in the wording shown, and are there restrictions we should respect? | Separate permission and any employer restriction; Permission to name a person does not automatically authorise naming their employer; linked context may still identify it. |
| Council recognition | Separately, would you want the specified council recognition if that proposed model proceeds? | Only the actual recognition wording/use. Interest is not membership or permission to identify a research account. |
| Contribution clarification | May we contact you about factual clarification or the proposed wording of this contribution? | Limited research purpose; not a marketing list or broad future-use permission. |
| Future research invitation | Would you like a separate invitation if a later research opportunity is relevant? | Distinct scope; no automatic reuse of the existing contribution. |
| Future-edition reuse, only if proposed | May this specified contribution also be used in the particular later output described? | Precisely defined use/version and restrictions, separately from invitation or this edition. No blanket future authorisation. |
| Table information | Separately, would you be interested in information about an exploratory discussion on the proposed Table council? | Interest only; no event, hospitality, sponsor access, purchase or recurring commitment. |

The operator records actual wording, scope, date/evidence and restrictions in the blank schema only after the approved environment is in place. If permission changes, preserve the request and follow JGA's documented instructions; do not assume all previous uses become allowed or that distributed copies can necessarily be recalled.
''')
print(json.dumps({'status':'collection_pack_integrated_draft_ready','files':8,'core_questions':14,'actual_records':0,'collection_ready':False,'working_contract_roles_and_closure_preserved':True},indent=2))
