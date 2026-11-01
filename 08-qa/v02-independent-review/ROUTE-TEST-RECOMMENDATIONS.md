# Independent route tests for version 0 2

28 October 2026. Internal structural QA recommendations. These are synthetic scenarios, not participant responses, cognitive testing, timing checks or findings.

## Route contract

Keep Q001–Q014 as the fourteen core items. The normal no-case path is Q001–Q006, relevant optional follow-up, then Q014. An eligible recent case uses Q007–Q013 before Q014. The follow-up must first establish whether the need was raised, then select the applicable follow-up; do not read all branches as a compound question.

A case requires direct involvement and a relevant proposal or substantive decision milestone inside the agreed 24-month window. An older programme can qualify through a recent milestone, with original programme start and selected milestone dates separate. Do not treat an old programme's mere continued existence as a recent milestone. Unclear dates or involvement remain unresolved rather than forced into eligibility.

## Deterministic synthetic cases

| Test | Input | Expected route and classification |
| --- | --- | --- |
| RT01 Never raised need | No recent case; an important improvement has never been put forward. | Ask relevant no-case follow-up, then Q014. Record a pre-proposal need. Exclude from recent-case base. Do not invent a declined, deferred or abandoned decision. |
| RT02 Older proposal | No recent case; follow-up reveals a proposal outside 24 months, with no recent substantive milestone. | Retain separately labelled historical context, then Q014. No recent-case inclusion. It is not a never-raised need. |
| RT03 Newly recalled recent case | Initial Q006 response is no case; follow-up recalls a directly involved proposal within 24 months. | Confirm eligibility and select that case; resume Q007–Q013, then Q014. Include once in recent-case base. Do not retain the initial no-case status as the final route. |
| RT04 Recent milestone in older programme | Programme began earlier; a directly involved renewal, approval, re-scope or go-live decision occurred inside 24 months. | Full case route. Keep both dates and identify the selected milestone. Status describes the selected decision as of collection, not the entire programme compressed into one label. |
| RT05 Old programme still operating | Programme began earlier and is still operating; no recent decision or substantive milestone is identified. | Continued operation alone does not create eligibility. Use historical context/no-case path. |
| RT06 Pending proposal | Recent eligible proposal remains under assessment. | Full case route. Q011 uses evidence influencing the assessment so far, followed by what is still needed. Pending decision does not imply no selected option or no implementation unless stated. |
| RT07 Deferred proposal | Recent eligible proposal was deliberately deferred. | Full case route. Retain Q011's main question about evidence influencing that decision; also ask what is still needed. Do not replace the history of the deferral with future requirements only. |
| RT08 No relevant need or case | No material shortfall and no recent eligible case. | Accept the account; skip inapplicable need follow-ups, then Q014. No invented barrier or pressure to supply a negative example. |
| RT09 Eligibility unclear | Approximate date straddles the recall boundary, or direct involvement cannot be established. | Record eligibility as unresolved. Clarify if feasible; do not silently include in confirmed recent-case counts. Context can still inform relevant themes with its status visible. |
| RT10 Approved renewal | Renewal approved; incumbent retained; current service operating. | Three independent fields: approved, incumbent retained, operating. Renewal is not the opposite of approval, and operation does not establish benefit achievement. |
| RT11 Approved but not started | Alternative approved but delivery has not begun. | Approved, alternative selected, not started. Benefit assessment may be not yet assessable; do not call the approved forecast a realised result. |
| RT12 Live but unmeasured | Change is live; the participant reports no agreed baseline or result assessment. | Preserve live delivery plus not measured/not yet assessed benefit status as appropriate. Do not infer success, failure, savings or zero benefit. |
| RT13 Capacity rather than cash | Participant reports hours released; payroll spending unchanged. | Record released capacity and its stated use. Do not automatically convert it into cash saved or double-count time, productivity and staffing reductions. |
| RT14 Future priority only | Q005 mentions a desired investment; it has not been evaluated or funded. | Retain future-priority stage. Do not make it the selected historical case or an approved expenditure without separate evidence. |

## Assertions for the test harness

- The unique ordered core IDs equal Q001–Q014. Optional branch prompts do not create Q015 or inflate the core count.
- Every routed path reaches Q014 exactly once. Q007–Q013 occur only when an eligible case has been confirmed, or are explicitly labelled contextual exploration outside the recent-case base.
- The initial route may change after a newly recalled eligible case; final route, evidence basis and selected case are recorded without duplicating the contributor.
- Never-raised needs, older proposals, confirmed recent cases and unresolved eligibility have distinct codes. None is inferred merely from an initial no-case answer.
- Decision disposition, selected option, delivery state and benefit evidence are separate dimensions. Missing/not known, not asked, not applicable, prefer not to disclose, not measured and not yet assessed retain distinct meanings.
- Q011 pending and deferred wording matches the source guide, question map and client summary. Deferred cases preserve past decision evidence.
- Recall-window boundary handling uses the actual collection date and an explicit convention. Test an exact cutoff date, the day before, and unknown dates; do not substitute an undocumented fixed-day window.
- A second contextual example or Table conversation does not create an additional distinct practitioner. A council prospect counts toward the report target only after an eligible, permissioned usable report contribution.
- Case counts and contributor counts remain separate. No synthetic response enters observations, findings or chart data as human evidence; no market percentage or saturation claim follows from the 6–10 target.

## Review gate

Once the authored version is available, compare exact route language across the client plan, internal guide, question map, response/coding template and test harness. A passing structural test cannot establish comprehension, burden, participant consent or factual accuracy of future accounts.
