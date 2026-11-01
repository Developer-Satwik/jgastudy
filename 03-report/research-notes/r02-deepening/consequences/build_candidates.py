from pathlib import Path
import json, hashlib

folder = Path(__file__).resolve().parent
root = folder.parents[3]
base = str(folder.relative_to(root)) + '/'

def capture(name):
    file = folder / 'captures' / name
    return {'capture_path': base + 'captures/' + name,
            'capture_sha256': hashlib.sha256(file.read_bytes()).hexdigest()} if file.exists() else {'capture_path': None, 'capture_sha256': None}

sources = [
    dict(candidate_id='CON-S01', title='Payroll Audit Progress', publisher='Oldham Council',
         url='https://committees.oldham.gov.uk/documents/s155079/Payroll%20Audit%20Progress.pdf',
         published_date='2025-10-22', source_type='Primary employer management report to Audit Committee',
         review_status='original_relevant_sections_reviewed_via_web',
         locator='Printed pp1–5; sections2.3–2.6,3.3–3.10,4.6,5',
         population='One local-authority payroll service across council, schools and partner employers; current report context27 monthly payrolls, almost8,500 staff',
         sample_size=None, fieldwork_period='Records2024/25 and partial2025/26; report22 October2025',
         funding_or_commercial_interest='Employer management reporting, not independent causal evaluation',
         limitations='Error classification was incomplete. Incident counts are not unique employees or a valid error rate. Launched actions and hoped-for future benefits remain separate. No measured administrative rework cost.',
         reuse_status='Reproduction and redistribution rights not reviewed', **capture('oldham-payroll-audit-progress-2025.pdf')),
    dict(candidate_id='CON-S02', title='Payroll and Expenses Internal Audit Review2024/25-02', publisher='Comhairle nan Eilean Siar Internal Audit',
         url='https://www.cne-siar.gov.uk/sites/default/files/imce/Committees/Audit%20and%20Scrutiny%20Committee/2025/June/O-15A-Final-Report-Payroll-and-Expenses.pdf',
         published_date='2025-05-23', source_type='Primary internal audit case',
         review_status='original_relevant_sections_reviewed_and_selected_pages_rendered',
         locator='Printed pp2–3; findings M2–M6 pp7–10; cover and issue log',
         population='One Scottish local-authority payroll and expenses function administering seven payrolls, including one external payroll',
         sample_size=None, fieldwork_period='Visits February/March2025; management response22 May2025; selected records December2023–December2024 and since January2024',
         funding_or_commercial_interest='Public employer internal audit',
         limitations='Cover and issue log identify final issue23 May2025 while body headers retain draft. Advances are cash movements, not administrative cost or loss. Gross overpayments are not write-offs. Assurance is scoped and timebound, not an audited error rate.',
         reuse_status='Reproduction and redistribution rights not reviewed', **capture('comhairle-payroll-expenses-2025.pdf')),
    dict(candidate_id='CON-S03', title='April2026 issue of the Employer Bulletin', publisher='HM Revenue and Customs',
         url='https://www.gov.uk/government/publications/employer-bulletin-april-2026/april-2026-issue-of-the-employer-bulletin',
         published_date='2026-04-15', source_type='Primary regulator operational bulletin',
         review_status='original_relevant_section_reviewed',
         locator='RTI submission problems and incorrect handling of payroll ID; original HTML lines332–364',
         population=None, sample_size=None, fieldwork_period=None,
         funding_or_commercial_interest='Government guidance',
         limitations='Regulator-described mechanism, not prevalence, measured administrative cost or a sample of employer outcomes. Current detailed correction instructions remain with official guidance.',
         reuse_status='Page states Open Government Licence v3.0 except third-party content', **capture('hmrc-employer-bulletin-april-2026.html'))
]

claims = [
    dict(candidate_id='CON-C01', source_candidate_ids=['CON-S01'], locator='Printed pp2–3, sections3.3–3.10',
         claim_text='Oldham records153 underpayments in2024/25 and says recorded underpayments were rectified through supplementary payment routes; it separately records overpayments requiring recovery action. Error classification was not systematically captured.',
         value=153, unit='recorded underpayments, not unique employees', time_period='2024/25',
         evidence_class='published_employer_case', denominator=None,
         limitations='No rate or per-head cost. Do not divide by an illustrative transaction count from another period. Management report, not an independent causal evaluation.'),
    dict(candidate_id='CON-C02', source_candidate_ids=['CON-S01'], locator='Printed pp3–5, sections4.6 and5',
         claim_text='Oldham reports launching a cross-functional payroll reconciliation group and tighter payment approvals; optimisation, training and intended capacity gains remain partly prospective.',
         value=None, unit=None, time_period='Report22 October2025', evidence_class='published_employer_case', denominator=None,
         limitations='Reported actions and plans do not demonstrate net benefit, completed turnaround or reduced errors.'),
    dict(candidate_id='CON-C03', source_candidate_ids=['CON-S02'], locator='Printed p8, finding M4; PDF p10 visually inspected',
         claim_text='The audit records advances of GBP106,529.57 affecting142 employees during December2023–December2024, linked in the audit to late or incomplete forms and payroll uploads.',
         value=106529.57, unit='GBP remedial advances, not administrative cost or loss', affected_employees=142,
         time_period='December2023–December2024', evidence_class='published_internal_audit_case', denominator=None,
         limitations='Do not sum advances with separate gross overpayments or label either an irrecoverable loss. The GBP50 charging policy was not being applied and is not an observed unit cost.'),
    dict(candidate_id='CON-C04', source_candidate_ids=['CON-S02'], locator='Printed pp2–3, sections1.3 and2.2; PDF p5 assurance visually inspected; p10 M6 for selected uploads',
         claim_text='The audit gave Reasonable Assurance and praised maintained payroll service after a cyberattack while recording control and capacity issues; selected upload samples had no issues.',
         value=None, unit=None, time_period='Audit February/March2025; final23 May2025', evidence_class='published_internal_audit_case', denominator=None,
         limitations='Scoped assurance and selected tests do not establish perfect service, uniform accuracy or absence of risk. Positive and adverse findings coexist.'),
    dict(candidate_id='CON-C05', source_candidate_ids=['CON-S02'], locator='Printed pp7–9, M2,M4,M5',
         claim_text='The audit describes additional authority checking, advances and debtor recovery work around incomplete or late departmental inputs; responsibility for the authorised signatory list does not sit within payroll.',
         value=None, unit=None, time_period='Final report23 May2025', evidence_class='published_internal_audit_case', denominator=None,
         limitations='Qualitative rework mechanism. Actual hours and payroll-only administrative cost were not measured here; reported causes do not establish general causality.'),
    dict(candidate_id='CON-C06', source_candidate_ids=['CON-S03'], locator='RTI submission problems and incorrect handling of payroll ID; HTML lines332–364',
         claim_text='HMRC describes incorrectly handled payroll IDs creating duplicate or wrong employment records, wrong year-to-date information, repeated employer contact, disputed charges and additional manual correction work.',
         value=None, unit=None, time_period='Published15 April2026', evidence_class='regulator_reported_mechanism', denominator=None,
         limitations='Primary mechanism and guidance, not prevalence or a quantified loss study. Correct payment and correct statutory records are separate outcomes.')
]

import re
for obj in sources + claims:
    obj['accessed_on'] = '2026-10-28'
    obj['status'] = 'candidate_for_parent_review_not_publication_approved'
    for key, value in list(obj.items()):
        if isinstance(value, str) and not key.endswith(('path','url','sha256','_id')):
            value = re.sub(r'([A-Za-z])(\d)', r'\1 \2', value)
            value = re.sub(r'(\d)([A-Za-z])', r'\1 \2', value)
            obj[key] = value

(folder/'source-candidates.json').write_text(json.dumps({'schema_version':'1.0','date':'2026-10-28','records':sources}, indent=2,ensure_ascii=False)+'\n')
(folder/'claim-candidates.json').write_text(json.dumps({'schema_version':'1.0','date':'2026-10-28','records':claims}, indent=2,ensure_ascii=False)+'\n')
qa=[]
for name in ['comhairle-page5.png','comhairle-page10.png']:
    file=folder/name
    qa.append({'path':base+name,'sha256':hashlib.sha256(file.read_bytes()).hexdigest(),'visually_inspected':True,'purpose':'Selected source verification, not an original research graphic'})
review={'date':'2026-10-28','sources_reviewed':3,'claim_candidates':6,'source_renders':qa,
    'excluded':[{'url':'https://democracy.edinburgh.gov.uk/documents/s103508/8.1%20-%20Internal%20Audit%20Outcomes%20June%20to%20August%202026%20-%20Appendix%201%20Payroll%20Oracle%20HR%20Key%20Controls.html?CT=2','reason':'Original returned403; search discovery only; no substantive claim'}],
    'new_participants':0,'canonical_files_modified':False,'external_contact':False}
(folder/'review-log.json').write_text(json.dumps(review,indent=2)+'\n')
print('Saved three source candidates, six claims and two inspected source renders.')
