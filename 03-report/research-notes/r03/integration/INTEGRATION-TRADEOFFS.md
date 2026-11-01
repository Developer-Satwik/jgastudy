# Integration is an operating change, not a connection label

29 October 2026. R03 internal desktop research. Bounded primary technical and official examples; no API calls, customer-system tests, participant input or procurement ranking.

## Conclusion for the capability map

Integration can reduce a specific transfer or duplication task, but a connection is not evidence that information is complete, authorised, included in the right run, reconciled or corrected. The useful unit is the actual handoff: source, destination, fields, identity, date, owner, authority, confirmation and recovery route. File/API/event choices alter that handoff rather than remove responsibility for it.

Keep documented capability, available access, configured connection, completed processing and verified operating result separate. The sources demonstrate declared behaviour and constraints, not measured success rates or comparative benefits. R03 should preserve process/configuration improvement and adequate existing arrangements alongside replacement.

## Seven deliberate primary examples

| Evidence | What it establishes | Practical R03 implication | Limit |
| --- | --- | --- | --- |
| INT-S01, Staffology HR-to-payroll data sync | HR is the stated source; blank values can overwrite payroll fields, with tax-code handling separate. | Agree field ownership and blank/overwrite semantics before automating a transfer. Correct data in the system that controls it, then verify the relevant destination. | One documented product integration, not a universal data model or incident frequency. |
| INT-S02, integration management help | Logs identify failed syncs; payroll lock dates and catch-up of some variable elements are documented. Cost-centre/department mapping can affect third-party-controlled data. | Align timing and mapping with the actual payroll period, identify who reviews errors and clarify which system owns shared codes. | Declared configuration/operating options, not proof a customer has enabled them or meets a cutoff. |
| INT-S03, asynchronous jobs guide | The returned job reference precedes completion and result/error retrieval; the guide labels the described async access beta. | A request acknowledgement is not a completed batch. Check entitlement, terminal state and relevant results. | Do not treat beta documentation as general availability, a throughput promise or guaranteed runtime. |
| INT-S04, import-result model | The schema distinguishes queue/execution, completion, failure and completion with errors, including row-level information. | Partial acceptance needs a reconciliation and exception owner rather than a single green connection indicator. | A public schema does not establish how often partial import occurs or that its endpoint is generally enabled. |
| INT-S05, webhook guide | Specific change/job/payrun events and payload/response inspection are documented. | A notification can start a downstream check; its event meaning must match the task. A finalised-payrun event does not itself prove bank receipt or external-record correction. | No tested delivery, latency, replay or end-to-end outcome guarantee inferred. |
| INT-S06, Xero permissions FAQ | Payroll access requires the relevant authorising-user role; the documentation advises testing before connecting a live organisation. | Integration availability depends on authorised access and a tested arrangement, alongside feature coverage. | This generic permissions source does not establish current UK endpoint coverage, customer entitlement or a broad least-privilege assurance. |
| INT-S07, HMRC GfC22 | Current guidance describes employment-ID matching at software/provider changes and particular discrepancies requiring external correction. | Preserve identity/mapping and distinguish technical submission from account-level resolution. Migration is more than copying a roster. | Official operational guidance, not legal advice, a market error rate or a complete migration checklist. |

Original routes are retained in `source-candidates.json`. Specific field names and product behaviour belong in internal due diligence, not necessarily in the report's client-facing narrative.

## Trade-offs to carry into R03

| Possible approach | Task it might change | Dependencies and retained work | Evidence to seek before calling it successful |
| --- | --- | --- | --- |
| Governed file/batch transfer | Repeated data entry between defined systems at a known point. | Agreed format, field semantics, IDs, period, approved source, safe transfer, accepted/rejected-row reconciliation and timely owner action. | Expected rows/totals against actual imported results; exceptions resolved; relevant outcomes checked. A file arriving is insufficient. |
| API integration | Application-level reading/writing with less repeated manual transfer. | Documented required endpoints, access, mappings, available feature/version, scheduling, monitoring and recovery. Users still own source correctness and approval. | Correct population/period, completed jobs and row outcomes, reconciled downstream result and controlled exception handling. |
| Event notification plus workflow | Detecting a particular change or completed stage without repeatedly asking for it. | Supported event and its semantics, subscription/access, receiver, observable payload/result and recovery appropriate to the actual system. | A trace from meaningful event to the intended action/result; notification delivery alone is not payroll completion. |
| Reporting/consolidation | Making distributed information usable for a defined decision. | Definitions, scope, freshness, transformations, access and reconciliation with the relevant operating records. | A responsible user can answer the stated question and act; a dashboard alone is not a performed control. |
| Existing configuration/process correction | A wrong source, missing catch-up step, uncontrolled code ownership or unclear error responsibility. | Clear ownership, usable controls, appropriate training and a documented actual arrangement. | The diagnosed condition changes and the relevant outcome is checked. Software replacement is not implied by the need. |

This table is an analytical map, not a list of claimed benefits. A controlled batch may be appropriate in one context; a different arrangement may warrant APIs or events. The actual evidence must establish task frequency, complexity, materiality, current effort and operating constraints. No universal hierarchy or cost advantage is established here.

## Three distinctions that make the evidence useful

### Source correctness versus transfer fidelity

The Staffology source-of-truth example shows why copying accurately can still produce an unwanted result. Relevant field ownership, empty-value behaviour and separate tax-code handling matter. A faster transfer cannot establish that an upstream fact was complete or authorised. These are preconditions to investigate rather than a claim that automation makes data worse. INT-C01–C03.

### Processing state versus the protected outcome

The asynchronous and import-model examples expose separate stages and partial errors. Product state definitions can support monitoring, but payroll correctness still needs the relevant reconciliation and downstream result. Do not reinterpret an import success, a payslip, a finalised run, statutory acknowledgement and employee receipt as synonyms. Existing R02 HMRC correction and Bacs sources (SRC-0101 and SRC-0122) preserve the wider reporting/payment boundary. INT-C04–C06.

### Prevention versus residual correction

HMRC's GfC22, published 22 October 2026, links changed payroll IDs with duplicate-employment risk and specifies an external route for certain already-created discrepancies. It reinforces the R02 distinction between preventing recurrence, clearing old records and closing consequences. It does not justify an undifferentiated rule to resend data. Use current guidance for a specific operational case rather than republish technical instructions as the report's advice. INT-C08.

## A compact evidence request within the existing guide

Where integration arises naturally in Q004, Q012 or Q013, establish the actual transfer/task; the system and party that controls each important field; identity and period mapping; access and approval; exception detection; authority to correct; and a known result. Use only relevant selective follow-ups. Do not request employee files, credentials, security configuration or confidential vendor documents.

For an observed benefit, distinguish transfer effort avoided, new monitoring/correction work, elapsed time, released capacity and a change in spending. This strand estimates none of these. Full business-case valuation belongs to later R05 work; actual practitioner input is still required. A supplier can help by explaining scope and demonstrating the relevant states/exception path, rather than offering an unqualified seamless-integration claim.

## Access, freshness and exclusions

Seven original HTML files were retained, and actual hashes were checked. Retained Staffology help bodies display updates of 21 April and 13 October 2026. The web reader returned older cached date headers for the same substantive pages. The retained live originals control the metadata here; no capability-change trend is inferred.

Xero UK overview/employee routes returned JavaScript-only bodies through the reader. Their unseen details were not used. Australian documentation was excluded from UK technical claims. The Xero webhook search extract was not adopted as current UK payroll coverage. Staffology's beta notices are retained. No technical endpoint was exercised, account connected, terms accepted, product installed or data uploaded. No PDF source was required for this strand.
