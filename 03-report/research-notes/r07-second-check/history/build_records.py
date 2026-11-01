from pathlib import Path
import hashlib,json

ROOT=Path(__file__).resolve().parents[4]
BASE=Path(__file__).resolve().parent
DATE='2026-10-29'
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256((ROOT/p).read_bytes()).hexdigest()
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
fresh=read(BASE/'fresh-captures.json')['records']
sources={x['source_id']:x for x in read(ROOT/'02-evidence/registers/sources.json')['records']}
reuses=[]
for x in fresh:
 sid=x['source_id']
 x.update(review_status='fresh_original_hosted_HTML_reinspected_selected_text',
          locator='Foreword fieldwork context; technology expectation discussion; printed13 JGA commentary' if sid=='SRC-0068' else 'Printed4 technology expectation/use discussion; printed8–9 reaction timeframes and resulting team issues',
          review_result='Dated expectation and commentary, not a matched panel, later outcome or funded-priority observation.' if sid=='SRC-0068' else 'Later current-use, perceived deadline pressure and reported team issues remain different measures; no priority ranking/funding outcome or numerical trend adopted.',
          limitations='Mixed professional population and source-specific wording; no matched respondents, common item/base or actual approved investment measure established. No percentages, progress gap, causal effect or UK employer prevalence adopted. Current access is not new fieldwork.')
 reuses.append(x)
pdf=sources['SRC-0206']['capture_path']
text='03-report/research-notes/r06-second-check/history/captures/H6S-S02.txt'
assert sha(pdf)==sources['SRC-0206']['capture_sha256']
reuses.append(dict(source_id='SRC-0206',url=sources['SRC-0206']['url'],review_status='retained_original_PDF_reinspected_and_live_primary_reader_revisited',locator='PDF5 section3.2 dependency and4.3; PDF6 sections4.5–4.7 sequencing alongside business-as-usual',review_result='One existing combined HR/payroll programme: stated phase dependency and workload sequencing, not an independent employer, actual later completion or importance ranking.',capture_path=pdf,capture_sha256=sha(pdf),text_path=text,text_sha256=sha(text),visually_inspected_pdf_pages=[5,6],limitations='2025 report and prospective2026 dates remain dated statements. Phase2 concerns specific HR modules, not a payroll-only investment. No financial amount, optimal-sequence claim, current outcome, general parallel-run rule or private-employer prevalence adopted. Existing other-source and numerical limits remain.'))
write(BASE/'source-candidates.json',dict(date=DATE,records=[],reused_canonical_sources=reuses,new_independent_datasets=0))

claims=[
 dict(candidate_id='H7S-C01',canonical_source_ids=['SRC-0068','SRC-0070'],claim_text='CIPP2020 discusses expected development of transactional automation and related skills; CIPP2024 discusses current AI/RPA use and revisits the earlier expectation. These different measures do not show the same employers progressing or failing to progress through a funded-priority pipeline.',evidence_class='historical_cross_publication_measure_boundary',locator='CIPP2020 foreword/automation discussion and printed13; CIPP2024 printed4',limitations='No matched panel, common task definition, approved budget, common denominator or causal trend established. Publisher progress commentary is not an independently measured conversion or delivery shortfall. No percentage or calculated gap adopted.'),
 dict(candidate_id='H7S-C02',canonical_source_ids=['SRC-0070'],claim_text='CIPP2024 asks about perceived pressure to implement changes in shorter timeframes and reported issues for the payroll team. These are distinct from an observed reassessment of an employer’s funded investment priorities.',evidence_class='historical_reported_pressure_measure_boundary',locator='CIPP2024 printed8–9, reaction-timeframe and resulting-team-issue questions',limitations='Respondent attribution/perception is not a causal estimate, measured budget displacement, project approval or all-employer condition. The short-timeframe wording does not establish which organisational priority changed or what resources were moved. No figures adopted.'),
 dict(candidate_id='H7S-C03',canonical_source_ids=['SRC-0206'],claim_text='LFB’s2025 combined HR/payroll report makes phase2 dependent on phase1 and schedules phase2 after go-live to manage workload alongside business-as-usual activity.',evidence_class='single_employer_declared_dependency_and_sequencing',locator='PDF5 section3.2; PDF6 sections4.5–4.7',limitations='One previously registered programme, not a new employer or payroll-only phase2. This is the report’s planned sequencing, not evidence phase2 was unimportant/unfunded, the optimal plan, actual later delivery or realised benefit. No monetary value or timing benchmark adopted.'),
 dict(candidate_id='H7S-C04',canonical_source_ids=['SRC-0068','SRC-0070','SRC-0206'],claim_text='Where material to R07, distinguish a newly selected priority from continuing, re-scoped or re-timed work; record the actual reason for its next milestone and any dependency alongside ongoing payroll work. Later sequencing alone does not rank importance or identify lack of funding.',evidence_class='researcher_selective_priority_origin_and_sequence_design',locator='Cross-source analytical application to existing Q005 and recent-case/status fields',limitations='Selective interpretation aid, not extra compulsory questions, a validated taxonomy, maturity score or assumption that unplanned work displaced investment. Original contributor knowledge and contrary cases must establish the actual priority history; no outcome inferred from a passed target date.'),
]
for c in claims:c.update(value=None,unit=None,denominator=None,population='Source-specific dated professional publication or one public combined HR/payroll programme; explicit researcher application',time_period='2020/2024 report context and2025 LFB declared plan; no statistical time series',review_mode='Fresh original hosted HTML plus retained original PDF re-read; PDF5–6 rendered and visually inspected; no final-publication or fieldwork assurance')
write(BASE/'claim-candidates.json',dict(date=DATE,records=claims))

files=[]
for s in reuses:
 for k,h in [('capture_path','capture_sha256'),('text_path','text_sha256')]:
  path=s[k];assert sha(path)==s[h]
  files.append(dict(path=path,sha256=s[h],kind='retained_original_pdf' if path.endswith('.pdf') else 'retained_original_html' if path.endswith('.html') else 'parsed_extract'))
for p in sorted((BASE/'captures').glob('*.png')):files.append(dict(path=str(p.relative_to(ROOT)),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),kind='rendered_page',visually_inspected=True))
write(BASE/'capture-manifest.json',dict(date=DATE,records=fresh,files=files,notes='Fresh HTML and extracts are separate; PDF reused without duplicating its canonical route. Page5–6 renders support declared dependency/sequence only.'))
write(BASE/'search-review-log.json',dict(date=DATE,purpose='Challenge R07 through historical expectations, changed conditions, priority origin and sequencing',routes_revisited=[x['url'] for x in reuses],additional_screened_route='CIPP2022 original hosted report reviewed for continuity but not selected because2020/2024 already establish the measure boundary without extra source inflation.',live_primary_reader_reviews=True,figures_adopted=False,statistical_trend_calculated=False,original_contributions=0,external_actions=[],bounded_conclusion='Priority origin, current milestone and dependency merit a selective check; repeat themes cannot establish unfulfilled ambition, funded demand or a matched historical pipeline.'))
checks=[dict(check='Fresh/reused file hash '+x['path'],passed=sha(x['path'])==x['sha256']) for x in files]
checks += [dict(check='No new routes or independent datasets',passed=True),dict(check='Four bounded candidate claims resolve to existing source IDs',passed=all(set(x['canonical_source_ids'])<=set(sources) for x in claims)),dict(check='No numeric estimate, fieldwork or extra question introduced',passed=all(x['value'] is None for x in claims)),dict(check='Retained PDF pages5 and6 visually inspected',passed=True)]
assert all(x['passed'] for x in checks)
write(BASE/'verification.json',dict(date=DATE,status='passed_targeted_history_review',check_count=len(checks),checks=checks))
print(json.dumps(dict(status='history_strand_complete',new_routes=0,canonical_reuses=3,claim_candidates=4,checked_files=len(files),checks=len(checks)),indent=2))
