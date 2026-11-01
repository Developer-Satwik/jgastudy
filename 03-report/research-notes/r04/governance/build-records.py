from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json

folder = Path(__file__).resolve().parent
project = folder.parents[3]
date = '2026-10-29'

def rel(path):
    return str(path.relative_to(project))

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def artifact(name):
    path = folder / name
    return {'capture_path': rel(path), 'capture_sha256': sha(path), 'bytes': path.stat().st_size}

def save(name, data):
    (folder / name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')

common = dict(accessed_on=date, sample_size=None, fieldwork_period=None,
              review_status='relevant_original_sections_reviewed',
              reuse_status='Private verification; paraphrase and rights review required before final client reuse',
              publication_eligibility='internal_R04_context_final_use_pending')

sources = [
    dict(candidate_id='GOV4-S01', title='Government Functional Standard GovS 002: Project delivery, version 2.1',
         publisher='Government Project Delivery / Cabinet Office',
         url='https://projectdelivery.gov.uk/library-products/government-functional-standard-govs-002-project-delivery/',
         alias_urls=['https://www.gov.uk/government/publications/project-delivery-functional-standard',
                     'https://projectdelivery.gov.uk/library-product/government-functional-standard-govs-002-project-delivery/',
                     'https://projectdelivery.gov.uk/download/66847/?tmstv=1756584452'],
         published_date='2025-09-01', last_updated='2025-09-17',
         date_note='PDF cover and library metadata issue date 1 September 2025; GOV.UK landing release/update entry 17 September 2025. Distinguish document issue from landing release date.',
         document_version='2.1', source_type='official_government_functional_standard',
         locator='HTML 1.2; 4.1.3; 4.2.3; 4.3; 4.4.7-4.4.9; 6.2-6.3; 6.4.4. Browser tool line ranges 130-138, 231-240, 269-308, 358-374, 486-525, 564-570.',
         population='Projects, programmes and portfolios in or across government departments and arm\u2019s-length bodies; other public organisations may find it useful.',
         geography='UK central-government framework; not a sample of UK employers',
         funding_or_commercial_interest='Government standard setter, not a supplier outcome case',
         limitations='Normative government framework, not observed private-employer payroll practice or prevalence. Direct HTML and PDF download returned Cloudflare interstitials. Browser parsed extracts of original sections are retained and hashed; the original HTML/PDF is NOT retained.',
         capture_kind='browser_tool_parsed_extract_not_original', original_capture_status='blocked_direct_capture',
         additional_captures=[artifact('govs-002-browser-lifecycle-extract.txt')],
         **artifact('govs-002-browser-text-extract.txt'), **common),
    dict(candidate_id='GOV4-S02', title='Government Functional Standard GovS 008: Commercial, version 2.2',
         publisher='Government Commercial Function',
         url='https://www.gov.uk/government/publications/government-functional-standard-govs-008-commercial-and-commercial-continuous-improvement-assessment-framework/government-functional-standard-govs-008-commercial-html',
         published_date=None, last_updated='2026-05-14', document_version='2.2',
         date_note='HTML states Updated 14 May 2026 and describes v2.2 replacing v2.1 after spending-control reforms.',
         source_type='official_government_functional_standard',
         locator='1.2 scope; 4.4.3; 4.5.1-4.5.2; 4.6.4-4.6.7; 5.4.2-5.4.5. Browser tool lines 296-405 and 642-697.',
         population='Government commercial activity within the standard\u2019s specified public-sector scope; not payroll-only or private-employer data.',
         geography='UK government commercial framework',
         funding_or_commercial_interest='Government standard setter',
         limitations='Normative public-sector standard. Internal schemes of delegation still matter. Do not apply central-government approvals, public procurement rules or mandatory roles to private employers; do not treat expert advice as final approval.',
         capture_kind='retained_original_html', original_capture_status='retained',
         **artifact('govs-008-commercial.html'), **common),
    dict(candidate_id='GOV4-S03', title='Government Functional Standard GovS 006: Finance, version 3.1',
         publisher='Government Finance Function / HM Treasury',
         url='https://assets.publishing.service.gov.uk/media/66d5c8c4701781e1b341db29/Government_Functional_Standard_006.pdf',
         alias_urls=['https://www.gov.uk/government/publications/government-finance-standards-page'],
         published_date='2024-07-31', last_updated=None, document_version='3.1',
         date_note='PDF cover says Date issued 31 July 2024. Landing page says Version 3.1 July 2024 but still carries 11 May 2023 last-update stamp; do not misdate the document to that stamp.',
         source_type='official_government_functional_standard',
         locator='PDF cover p1; scope section 1.2 printed p2/PDF p6; 4.4.4-4.4.7 printed pp15-16/PDF pp19-20 (one-based).',
         population='Government departments, arm\u2019s-length bodies, some public corporations and other entities as specified in section 1.2; no empirical sample.',
         geography='UK public-funds management framework',
         funding_or_commercial_interest='Government standard setter',
         limitations='Specific public-sector finance roles; not evidence of private-employer practice, a universal CFO veto or current policy for every public body. PDF issue date is 2024; its relationship to newer spending-control reforms must remain scoped, with GovS 008 v2.2 used for the current commercial distinctions reviewed.',
         capture_kind='retained_original_pdf', original_capture_status='retained',
         additional_captures=[artifact('govs-006-finance-landing.html')],
         **artifact('govs-006-finance.pdf'), **common),
    dict(candidate_id='GOV4-S04', title='Corporate Governance Code Guidance',
         publisher='Financial Reporting Council',
         url='https://www.frc.org.uk/library/standards-codes-policy/corporate-governance/corporate-governance-code-guidance/',
         published_date='2024-01-29', last_updated='2026-06-03',
         date_note='Live guidance, explicit update log. Paragraph locators refer to the 29 October 2026 capture.',
         source_type='professional_regulatory_guidance',
         locator='Opening scope; Executive Summary paragraphs 1-3 and 6; committee paragraph 99; risk governance paragraphs 221-228.',
         population='Guidance supporting the Code applied by companies in commercial-company and closed-ended investment-fund listed categories; not a survey or all-private-company code.',
         geography='UK Corporate Governance Code context, including in-scope listed issuers',
         funding_or_commercial_interest='Governance regulator/standard setter',
         limitations='Guidance is non-mandatory and non-prescriptive; underlying Code principles/provisions and listing scope differ. Retained board framework responsibility does not prove board approval of every payroll contract or universal committee/CFO power.',
         capture_kind='retained_original_html', original_capture_status='retained',
         **artifact('frc-corporate-governance-guidance.html'), **common),
]

reused_path = project / '03-report/research-notes/r03/delivery/DEL-S01.html'
sources.append(dict(candidate_id='GOV4-REUSE01', canonical_source_id='SRC-0131',
    title='In-house vs outsourced payroll', publisher='Cintra',
    url='https://help.cintra.co.uk/docs/in-house-vs-outsourced-payroll',
    published_date='2026-07-07', last_updated='2026-09-24',
    source_type='supplier_operational_documentation',
    locator='SaaS customers / Authorise payments; Source customers / Authorise payments',
    population='Specific Cintra service/payment-route documentation; not a payroll market sample',
    geography='Supplier documentation relevant to UK payroll/BACS workflows',
    funding_or_commercial_interest='Supplier describing its own workflows',
    limitations='Operational submission/approval/payment workflow does not establish authority to buy or replace the service. Absence of an in-product authorisation banner is not absence of employer controls. Actual package and contract require checking.',
    capture_path=rel(reused_path), capture_sha256=sha(reused_path), bytes=reused_path.stat().st_size,
    capture_kind='reused_retained_original_html', original_capture_status='existing_original_rechecked',
    **common))

save('source-candidates.json', dict(date=date, module='R04', status='internal_candidates_not_canonical',
     new_source_count=4, reused_source_count=1, records=sources,
     existing_register_context=['SRC-0005 Green Book: retained as R05 method context, not reanalysed here',
        'SRC-0077 Sourcing Playbook: existing R03 delivery-model context; 2023 edition is not used for current approval mechanics',
        'SRC-0136 Scottish Government closure report: actual case chronology belongs to the concurrent case strand'],
     screened_not_added=[dict(url='https://projectdelivery.gov.uk/library-product/the-role-of-the-senior-responsible-owner/',
        reason='GovS 002 approved standard already supplies the necessary role distinctions. Separate SRO portal metadata shows v2.1 trial/consultation status and dates that differ from GOV.UK update entry; no unsupported equivalence assumed and no source added.')]))

def claim(i, ids, locator, text, evidence, limits, pop):
    return dict(candidate_id=f'GOV4-C{i:02d}', source_ids=ids, locator=locator, claim_text=text,
       evidence_class=evidence, limitations=limits, value=None, unit=None, denominator=None,
       population=pop, fieldwork_period=None, accessed_on=date,
       review_mode='Relevant original online sections read; PDF pp19-20 rendered and visually checked; capture type explicit per source',
       status='internal_R04_context_candidate')

public='Source-scoped government framework, not an observed employer sample'
claims=[
 claim(1,['GOV4-S01'],'4.4.7-4.4.9; 6.4.4',
   'GovS 002 distinguishes higher sponsoring authority, the accountable SRO owning the business case, and day-to-day programme/project management; the SRO escalates decisions outside delegated authority.',
   'official_public_sector_role_framework','Do not substitute public SRO titles for private employer roles or infer a universal approval chain.',public),
 claim(2,['GOV4-S01'],'4.2.3; 6.3',
   'GovS 002 places assurance assessment before significant decisions and requires decision-makers, consultation and review type to be defined for each gate.',
   'official_public_sector_role_framework','Review recommendations are inputs; this wording alone does not assign reviewers authority to approve funds or go-live.',public),
 claim(3,['GOV4-S01'],'4.1.3; 4.3; 6.2-6.3',
   'GovS 002 allows proportionate governance, conditional or phased decisions, and outcomes including revision, deferral or termination.',
   'official_public_sector_governance_framework','Government project provisions do not impose the same stages, gates or thresholds on private routine renewals.',public),
 claim(4,['GOV4-S02'],'4.6.4-4.6.7',
   'GovS 008 separates contract justification/business ownership, commercial leadership, signature under delegation and day-to-day contract management; specialist commercial roles can be advisory or executive.',
   'official_public_sector_commercial_framework','Government standard; these rights may be combined or distributed in an actual case. Title does not establish authority.',public),
 claim(5,['GOV4-S02'],'4.5.1-4.5.2; 4.4.3',
   'GovS 008 identifies offer invitation, award recommendation, payment, extension/change and termination as distinct decisions within the organisation\u2019s controls, with commercial and project decisions aligned.',
   'official_public_sector_commercial_framework','Do not read these as a universal fixed sequence or import public-spending controls into private payroll procurement.',public),
 claim(6,['GOV4-S03'],'4.4.5-4.4.7, printed pp15-16/PDF pp19-20',
   'GovS 006 describes delegated budget holders separately from finance business partners who support and challenge them; specialist finance roles can be advisory or executive according to assignment.',
   'official_public_sector_finance_framework','Not proof that finance advice is a binding veto, or that every CFO personally approves every payroll change.',public),
 claim(7,['GOV4-S04'],'Opening scope; paragraphs 1-3, 6, 221-228',
   'FRC guidance distinguishes board delegation and committee advice from retained board responsibility for the risk/control framework and management\u2019s day-to-day implementation; delegations should be explicit.',
   'listed_company_governance_guidance','Non-mandatory guidance supporting the Code for specified listed categories, not all private employers or individual payroll approvals.','In-scope listed-company governance guidance, not observed payroll decisions'),
 claim(8,['SRC-0131'],'SaaS customers / Authorise payments; Source customers / Authorise payments',
   'Cintra distinguishes approval/submission of payroll from BACS payment authorisation according to service/payment route.',
   'supplier_operational_documentation','Does not show who can purchase the platform, approve investment, sign contracts or release funds outside that supplier workflow.','Specific supplier workflows'),
 claim(9,['GOV4-S01','GOV4-S02','GOV4-S03','GOV4-S04','SRC-0131'],'Cross-source analytical distinction; see GOV4-C01-C08',
   'R04 should code the right exercised at a dated decision separately from job title, sponsorship, influence, assurance, signature and operational approval.',
   'researcher_method_recommendation','An analytical recommendation, not an empirical finding that all organisations use these roles or a proposal to change the 14-question core.','Proposed qualitative case analysis'),
 claim(10,['GOV4-S01','GOV4-S02'],'4.3/6.3 and 4.5.1; methodological application to Q007/Q009/Q013',
   'Case coding should distinguish a concern or recommendation from a binding condition, establish who can clear or escalate it, and preserve decision disposition separately from implementation.',
   'researcher_method_recommendation','Actual conditions and decision rights remain to be established from original practitioner cases; do not impose a mandatory private workflow.','Proposed qualitative case analysis')
]
save('claim-candidates.json', dict(date=date, module='R04', status='internal_candidates_not_canonical', records=claims))

log = json.loads((folder/'capture-log.json').read_text())
for filename,sid,kind,url in [
  ('govs-006-finance.pdf','GOV4-S03','retained_original_pdf',sources[2]['url']),
  ('govs-002-browser-text-extract.txt','GOV4-S01','browser_tool_parsed_extract_not_original',sources[0]['url']),
  ('govs-002-browser-lifecycle-extract.txt','GOV4-S01','browser_tool_parsed_extract_not_original',sources[0]['url'])]:
    path=folder/filename
    log['records'].append(dict(source_candidate_id=sid,url=url,
      captured_at_utc=datetime.fromtimestamp(path.stat().st_mtime,timezone.utc).isoformat(),
      http_status=None, capture_kind=kind, status='retained', **artifact(filename)))
log['records'].append(dict(source_candidate_id='GOV4-S01',
   status='direct_curl_returned_cloudflare_interstitial_not_original',
   urls=[sources[0]['url'],sources[0]['alias_urls'][2]],
   note='Shell exits were zero but payload signatures were HTML Just a moment challenge pages. These are not retained or counted as originals. No challenge bypass attempted.'))
for path in folder.glob('*.blocked-response.html'):
    path.unlink()
log['summary']={'new_sources_reviewed':4,'new_sources_with_retained_originals':3,
    'new_sources_browser_parsed_only':1,'new_metadata_originals_retained':1,
    'existing_originals_rechecked':1,'mislabelled_originals':0}
save('capture-log.json',log)

review=dict(date=date,module='R04',scope='Own-folder research candidates only',
    inputs_read=['00-control/CURRENT-STATUS.md','01-method/WORK-PACKAGE-ORDER.md',
      '01-method/question-map.json v0.2','03-report/R03-DESKTOP-READOUT.md',
      '02-evidence/registers/sources.json; R03 delivery candidates and retained Cintra HTML'],
    sources_reviewed=[dict(candidate_id=s['candidate_id'],locator=s['locator'],
      review_status=s['review_status'],capture_kind=s['capture_kind']) for s in sources],
    pdf_review=dict(skill_read=True,source='GOV4-S03',pdf_page_count=59,
      text_extracted_pages_one_based=[1,6,19,20],
      rendered_and_visually_checked_pages_one_based=[19,20],
      printed_page_numbers_for_visuals=[15,16],
      notes='Two-column layout, section headings and continuation checked; no new PDF authored.'),
    scope_checks=dict(public_private_scope_explicit=True,no_prevalence_inference=True,
      title_not_authority=True,assurance_not_automatic_approval=True,
      supplier_operations_not_investment_authority=True,
      formal_advice_and_actual_case_evidence_distinct=True,
      core_questions_unchanged=True,canonical_files_changed=False,
      client_contact=False,spending=False,practitioner_cases_collected=0),
    retained_manifest=[])
for path in sorted(folder.iterdir()):
    if path.is_file() and path.name not in ['review-check.json','build-records.py']:
        review['retained_manifest'].append(dict(path=rel(path),sha256=sha(path),bytes=path.stat().st_size))
save('review-check.json',review)
print(json.dumps({'new_sources':4,'reused_sources':1,'claims':len(claims),
                  'manifest_files':len(review['retained_manifest'])},indent=2))
