from pathlib import Path
import json,hashlib
B=Path(__file__).resolve().parent;R=B.parents[3];D='2026-10-30'
def rd(p):return json.loads(p.read_text())
def wr(n,d):(B/n).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
cap=rd(B/'capture-manifest.json')['records'];by={x['source_id']:x for x in cap}
meta={
'T1M-S01':('IPASS Membership Options','IPASS','Ireland-facing payroll technical support membership with separate individual, corporate/bureau and overseas eligibility branches. Not a Table licence or event sponsorship.','Membership branches and respective billing/VAT descriptions; live original inspected. No private terms, purchase, quality, demand or retention verified. Search snippet tariffs differ from retained original, so no snippet price or price-change claim is adopted.'),
'T1M-S02':('Global Payroll Alliance: membership and resources','Global Payroll Alliance','Global/in-country payroll practitioner resources and network; not a senior-only council or research licence.','Public home/member benefits catalogue only. No achieved outcomes, readership, engagement, membership inclusion at a particular paid tier, independent quality or exact reuse licence assumed. Current page uses Global Payroll Alliance branding; no dated rebrand history inferred.')}
records=[]
for i,(title,pub,pop,lim) in meta.items():
 x=by[i]
 records.append(dict(candidate_id=i,title=title,publisher=pub,url=x['url'],source_type='professional_payroll_provider_public_offer',review_status='relevant_live_original_html_sections_inspected',accessed_on=D,published_date=None,last_updated=None,date_note='Review date, not publication, fieldwork or a proved price-change date.',population=pop,sample_size=None,fieldwork_period=None,method_available=False,funding_or_commercial_interest='Provider public catalogue describes its own membership/resources; no realised sales or benefits independently established.',capture_path=x['capture_path'],capture_sha256=x['capture_sha256'],capture_kind='retained_original_html',review_extracts=[dict(path=x['parsed_path'],sha256=x['parsed_sha256'],kind='parsed_original_text')],limitations=lim,reuse_status='Private verification only; no third-party republication rights obtained.'))
loc={
'SRC-0227':'SRC-0227.parsed.txt lines108–126: enterprise/service-provider assessment and annual research/inquiry service',
'SRC-0228':'SRC-0228.parsed.txt lines113–136: software-provider marketing purpose and licensed assets',
'SRC-0238':'SRC-0238.parsed.txt offer heading, organisation-team plan and annual support benefits',
'SRC-0239':'SRC-0239.parsed.txt lines99–119,141–145,167–176: users/benefit changes, auto-renewal and materials/service limits',
'SRC-0245':'SRC-0245.parsed.txt lines19,25,30,34–36: approved corporate executives, travel exclusion and possible partner meetings',
'SRC-0246':'SRC-0246.parsed.txt lines44–61: sponsor inventory and target-list invitations',
'SRC-0248':'SRC-0248.parsed.txt lines17–33: pre-event payment and generic cancellation/credit conditions with conflicting21/14-day wording'}
reuses=[]
for i,l in loc.items():
 x=by[i];reuses.append(dict(source_id=i,url=x['url'],locator=l,review_status='fresh_original_reinspection_for_segment_and_delivery_conditions',capture_path=x['capture_path'],capture_sha256=x['capture_sha256'],parsed_path=x['parsed_path'],parsed_sha256=x['parsed_sha256'],limitations='Source-specific public offer/terms only; no private JGA contract, current buyer behaviour or observed financial outcome. No existing base-source fields overwritten.',new_independent_dataset=False))
wr('source-candidates.json',dict(date=D,records=records,reused_canonical_sources=reuses))
cs=[
('T1M-C01',[],['T1M-S01'],'IPASS publicly separates individual, employer/corporate, payroll-bureau and overseas membership branches, with differing qualification, billing and tax descriptions. This makes the member organisation, geography and benefit unit material when comparing support alternatives.','publisher_declared_segmented_offer','T1M-S01.parsed.txt lines51–185: individual/corporate/overseas/Section56 branches','No price benchmark, tax advice, full licence interpretation, actual buyer preference or quality outcome. These are Irish payroll-support offers, not evidence that an Irish employer would buy The Table.'),
('T1M-C02',[],['T1M-S02'],'GPA publicly offers a global/in-country payroll resource and network catalogue including training, events, country information, a forum and a helpdesk route. A global payroll audience therefore has additional visible alternatives beyond the UK support membership reviewed in the first pass.','publisher_declared_resource_catalogue','T1M-S02.parsed.txt lines65–67 and128–147','No paid-tier entitlement, price, actual usage or independent effectiveness verified. Catalogue breadth does not prove the alternative satisfies a particular investment decision.'),
('T1M-C03',['SRC-0227','SRC-0228','SRC-0239'],[],'Specify who pays, who can use the asset and the actual use: internal decision support, client advice, public marketing and resale can require different permissions and servicing. An adviser buying research for client work is not automatically covered by an employer/internal-use package.','researcher_buyer_user_end_use_condition','Analytical application: ISG enterprise/provider service distinction; TPC clauses5.1,6 and9','No assertion that every adviser is excluded or that exact ISG licence terms are known. No new JGA licence terms adopted. Seek the intended use selectively, not a mandatory procurement questionnaire.'),
('T1M-C04',['SRC-0238'],['T1M-S01','T1M-S02'],'Assess alternatives against the decision geography, country set, employer size and operating need, rather than the city of an event or a generic global-payroll label. A country compliance-support need and a cross-country investment decision may require different evidence and value.','researcher_context_and_substitution_condition','Analytical comparison of UK team support, Irish segmented membership and global/in-country resource catalogue','No country market size, willingness-to-pay, geographic exclusion or law equivalence inferred. Context is selective and case-specific; no new mandatory report question.'),
('T1M-C05',['SRC-0245','SRC-0246'],[],'Define the intended research/member eligibility and how invitations are selected before assigning funder benefits. A sponsor target-list invitation route can serve commercial access objectives, while a research cohort may need a different role, country or decision-case mix. Keep any partner nominations distinguishable from independently recruited participants.','researcher_recruitment_and_funder_fit_condition','Analytical application: iVentiv FAQ qualification/approval and live sponsor target-list inventory','iVentiv is an L&D mechanism comparator, not a payroll sample design. No assertion that nominations must be prohibited or that The Table has recruited anyone. No default sponsor contacts, guaranteed eligible attendees or representative claims.'),
('T1M-C06',['SRC-0245','SRC-0246','SRC-0248','SRC-0239'],[],'Match each proposed commercial benefit to its actual delivery conditions and timing before modelling funding. Interest, accepted order, cleared cash, deliverable-ready research or seats, permitted publication and benefit delivered are separate states; funding received alone does not make every promised benefit deliverable.','researcher_commercial_delivery_state_condition','Analytical application: iVentiv approval/meeting/package/payment conditions and TPC start/payment/benefit conditions','No JGA cash dates, accounting recognition rule, deposit amount or legal contract advice. Generic iVentiv21/14-day conflict remains unresolved; do not import either interval. Later financial model needs its own sourced or explicitly assumed inputs.'),
('T1M-C07',['SRC-0239'],[],'The Payroll Centre terms describe an automatic renewal mechanism with reminder, termination and renewal-price provisions. This is a published contract mechanism for subscribed membership, not evidence of an actual retained customer base or achieved recurring revenue.','publisher_declared_membership_lifecycle_terms','SRC-0239.parsed.txt lines114–119, clauses5.4.1–5.4.5','Do not adopt an automatic subscription for JGA or equate annual availability with contracted renewals. Actual customer contracts, opt-outs, renewal behaviour, receipts and margin are not inspected.')]
wr('claim-candidates.json',dict(date=D,records=[dict(candidate_id=i,canonical_source_ids=s,source_candidate_ids=ss,claim_text=t,evidence_class=e,locator=l,limitations=lim,value=None,unit=None,denominator=None,population='Published offer/terms or explicit researcher application, not original participant input.',time_period='Rechecked30October2026; no longitudinal outcome estimate.',status='T01_second_challenge_context')for i,s,ss,t,e,l,lim in cs]))
conditions=[
 dict(condition_id='MKT01',name='Payer, user and intended use',apply_when='A licence, partner deliverable or adviser/client use is being considered.',check='What asset will be used, by whom, for which internal/client/public purpose, with what permission and briefing/servicing?',counterexample='A consultant needs a client-facing slide pack but the available package only supports internal reading.',claim_ids=['T1M-C03']),
 dict(condition_id='MKT02',name='Decision-fit of substitutes',apply_when='A geography or audience is being compared.',check='Which free/paid/internal alternatives actually match the country set, role, employer context and immediate decision?',counterexample='Dublin dinner interest is treated as demand for research, while the person primarily needs Irish compliance support already available elsewhere.',claim_ids=['T1M-C01','T1M-C02','T1M-C04']),
 dict(condition_id='MKT03',name='Recruitment and funder fit',apply_when='Partners nominate people or expect commercial access.',check='Does that invitation route fit the defined member/research purpose, and are recruitment origin and any optional access benefits clear?',counterexample='A sponsor wants accounts from a target list, while the research requires decision cases across a different employer/country mix.',claim_ids=['T1M-C05']),
 dict(condition_id='MKT04',name='Deliverability alongside funding',apply_when='A commercial bundle or cash model is being defined.',check='Which commitments, rights, approvals, research assets, attendees and servicing resources are actually ready, at which dates?',counterexample='A partner pays, but permissioned findings or approved attendees are not ready to supply the contracted benefit.',claim_ids=['T1M-C06','T1M-C07'])]
for c in conditions:c.update(mandatory=False,scored=False,validated=False,actual_application=None)
wr('selective-conditions.json',dict(date=D,conditions=conditions,original_fourteen_questions_unchanged=True,extra_mandatory_questions=0,commercial_validation=False,actual_contributions=[],financial_inputs=[]))
wr('search-log.json',dict(date=D,purpose='Segmented market and purchaser-economics challenge of T01; direct country/global substitutes and actual use/rights/delivery.',queries=['Global payroll association current membership country resources','Irish payroll corporate overseas payroll bureau membership','Existing ISG enterprise vs software-provider research services and iVentiv sponsor/admission terms'],reviewed_urls=[x['url']for x in cap],screened_not_used=[dict(name='GPA become-a-member price grid',url='https://www.becomeagpamember.com/',reason='Search discovery only; not needed for the bounded global catalogue finding. Grid/price units not adopted.'),dict(name='IPASS search-result tariff',reason='Search snippet differed from opened page/live HTML. Do not treat snippet as current rate or dated historical change; no price entered.')],external_actions='Read-only public page retrieval only. No form, contact, registration, quote, purchase or terms acceptance.'))
(B/'MARKET-CHALLENGE.md').write_text('''# T01 second challenge: market segments and purchaser economics

30 October 2026. Bounded public desktop check. The six selected models remain unchanged; IPASS and GPA are additional substitutes for testing fit, not two more adopted models or validated demand.

## What changes the working design

The first pass separates buyer, partner and practitioner value. This check adds four selective conditions that make those exchanges more concrete. None is a new mandatory report question or a score.

| Condition | Why it changes an offer | Counterexample to catch |
| --- | --- | --- |
| Payer, user and intended use | A client-facing adviser pack needs different permissions and service from internal employer reading. | Adviser says “research access” but intends to put results into paid client deliverables. |
| Decision-fit of substitutes | Country compliance help, global resources and investment-case research answer different jobs. Compare against the buyer's actual job. | Irish event interest is treated as research demand despite an existing local support route. |
| Recruitment and funder fit | Sponsor target lists can serve access goals; research/member eligibility has a separate purpose. | Funding requires a prospect mix that does not fit the intended decision cases or peer group. |
| Deliverability alongside funding | Cash, permissioned assets, eligible attendees and completed benefits are different states. | Partner funding arrives but the promised asset or approved audience is not ready. |

See [structured conditions](selective-conditions.json), including specific candidate claim links and counterexamples. These are researcher applications, not observed failures or buyer behaviour.

## Direct alternatives sharpen the geography question

IPASS's Irish support offer distinguishes individual, corporate/bureau and overseas branches with different published eligibility/billing descriptions. GPA's public catalogue spans global and in-country resources, training, events and a forum/helpdesk route. These routes show additional alternatives relevant to Dublin or internationally responsible practitioners; they do not prove that any particular need is satisfied. An event city alone does not define the buyer's country set or decision need. T1M-C01–C02 and C04. [IPASS](https://ipass.ie/membership/) · [GPA](https://gpa.net/)

The live IPASS capture has different tariff figures from the search-result snippet. No snippet value, price-change history, price comparison or JGA fee was adopted. Exact plan rights and tax application require the provider's actual terms; this review does not provide tax advice. GPA page branding is Global Payroll Alliance; no transition date or historical rebrand is inferred.

## The intended use is more precise than the buyer's label

ISG separates enterprise/service-provider assessment access from software-provider promotional licences. TPC restricts named member/user access and third-party exploitation. This supports asking what a buyer will actually do with the material. It does not establish exact ISG sharing terms or exclude every adviser. A JGA internal-use licence, external citation permission, client deliverable and resale right should be defined separately when relevant. T1M-C03. [Enterprise research](https://research.isg-one.com/research/buyers-guides/services/enterprise-and-service-providers) · [Provider assets](https://research.isg-one.com/research/buyers-guides/services/software-providers)

TPC also specifies a renewal mechanism. A subscription contract can have renewal provisions; a public annual offer alone still says nothing about actual customers, renewals or recurring cash. Do not copy automatic renewal into JGA's product or infer a retention rate. T1M-C07. [TPC terms](https://thepayrollcentre.co.uk/terms-and-conditions-of-business/)

## Recruitment, benefits and funds must fit together

The iVentiv FAQ screens senior corporate delegates and the live sponsor inventory includes target-list invitations. These are explicit commercial mechanics, not a sample for JGA to copy. Record partner-nominated and independently recruited routes where relevant, preserve the research/member fit and disclose any separately agreed commercial access. An invitation, attendance, permissioned research contribution and sponsor benefit are different objects. T1M-C05. [FAQ](https://www.iventiv.com/how-can-we-help) · [Sponsor inventory](https://www.iventiv.com/sponsors)

Payment and cancellation terms show that a programme also has timing and delivery obligations. The retained iVentiv generic terms still give inconsistent invoice intervals; neither supplies JGA's cash timing. Model the actual bundle and prerequisites later, including permissions, research/briefing availability, participant approval and servicing resources. Funding does not resolve those automatically. T1M-C06. [Event terms](https://www.iventiv.com/terms-and-conditions)

## What this does not decide

No demand rate, viable price, revenue, saving, retention, market size or margin is estimated. The cohort and invitation rule are not adopted, no commercial term is signed and no financial input is populated. The original four T02 hypotheses remain hypotheses. These conditions can refine selective probes in existing Table guides; actual authorised T03 contributions and later T04/T05 costing remain necessary. Nothing was sent or purchased.
''')
checks=[]
def ck(v,n):checks.append(dict(name=n,passed=bool(v)));assert v,n
for x in cap:
 ck(x.get('http_status')==200,'HTTP200 original '+x['source_id'])
 for p,h in [('capture_path','capture_sha256'),('parsed_path','parsed_sha256')]:ck(hashlib.sha256((R/x[p]).read_bytes()).hexdigest()==x[h],'retained hash '+x[p])
ck(len(records)==2,'Only two new primary routes')
ck(len(reuses)==7,'Seven canonical reuses not independent datasets')
for c in cs:ck(c[3] and c[5] and c[6],'Claim text locator limits '+c[0])
for x in conditions:ck(not x['mandatory']and not x['scored']and not x['validated']and x['actual_application']is None,'Selective condition not applied/validated '+x['condition_id'])
ck(len({c[0]for c in cs})==7,'Seven bounded records')
wr('verification.json',dict(date=D,status='passed',checks=checks,check_count=len(checks),new_primary_routes=2,canonical_reuses=7,claim_candidates=7,conditions=4,actual_participants=0,actual_Table_conversations=0,financial_inputs_added=0,external_sends=0,commercial_validation=False))
print(json.dumps(dict(status='passed',checks=len(checks),new_primary_routes=2,claims=7,conditions=4)))
