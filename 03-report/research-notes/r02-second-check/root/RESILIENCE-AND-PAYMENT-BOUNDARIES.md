# Resilience, authorisation and payment boundaries

28 October 2026. Targeted second challenge of R02. Public original sources; no participant input or external contact.

## What changes in the needs analysis

The four outcomes in the first R02 synthesis remain useful, but they are not exhaustive. Payment, reporting, records and explanation also depend on safe authorisation, appropriate access, continuity and recoverability. Apply these as cross-cutting conditions, rather than add an overlapping list of every possible risk.

The [government fraud guidance](https://stopthinkfraud.campaign.gov.uk/protecting-your-business/), Payment diversion fraud section, explicitly describes salary diversion through impersonated requests to change payroll bank details. This supports checking whether changes are authenticated and approved. It establishes a mechanism, not payroll-specific incidence, a vendor weakness or an amount lost. Do not import the page's general cyber statistic into a payroll risk rate or its supplier delay examples into a universal payroll policy.

The [Bacs glossary](https://www.bacs.co.uk/resources/glossary/), Bacs cycle entry, distinguishes submission, processing and account entry across three English bank working days. This reinforces the need to locate payment preparation, authorisation, transmission and receipt separately. It does not mean every employer uses Bacs or that a correction always takes three days. The organisation's actual route and cutoffs matter.

## A positive case that prevents a false inference

The British Library's 8 March 2024 incident review reports extensive organisational disruption and exfiltration of staff/user data, alongside continued normal operation of cloud-based finance/payroll. Pages 2 and 9 were read and visually checked. The case separates service continuity from wider information harm. It is not evidence that payroll data itself was exposed or that cloud delivery caused the continuity. It supplies no payroll-specific loss benchmark or comparative resilience result.

Original: [British Library review](https://www.bl.uk/files/v5dwkion/production/99206a2d1e9f07b35712b78f7d75fbb09560c08d.pdf/british-library-cyber-incident-review-8-march-2024.pdf?dl=). The dated account describes the position at publication, not the Library's current recovery status.

## Practical application to existing questions and matrix

- Inputs/approval: where relevant, distinguish authorised data from merely complete data, and a generated payroll file from an authorised and received payment.
- Records/reconciliation: investigate appropriate access, availability and recovery as well as accuracy. Do not ask for employee-level files, bank details or security configurations.
- Capacity/coverage: distinguish absence of a person, system outage, inaccessible information and missing authority. Each can impede continuation without proving the same remedy is needed.
- Service boundary: include the actual bank/payment interface, public reporting authority and other external dependencies where they arise in a case.
- Materiality: keep interruption, loss of confidentiality, erroneous reporting and financial loss distinct. A working payroll does not establish that every protective outcome was met.

These are conditional analysis prompts under existing Q002–Q004 and Q013, not new mandatory questions or a separate cyber audit. The interviewee should identify their own priority first. No technology, outsourcing or security product recommendation follows from these examples. R03 will consider options against the diagnosed need.

## Review record

`capture-log.json` records three successful original downloads with real hashes. Two PDF-page PNGs in `qa/` were visually inspected by the root researcher. A first rendering attempt failed because the optional fitz module was unavailable; Poppler then rendered the retained original successfully. No unread PDF numbers were extracted or used. Original captures are for private verification; reproduction rights have not been assumed.
