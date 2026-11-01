# T04 input and model rules

31 October 2026. Preparation for T05, not a completed Excel model, priced budget or sales forecast.

## Three cost and funding views

1. **Current first-project investment.** The agreed commission is USD1,500, including USD1,000 for the report and USD500 for Table feasibility. The reported USD750 upfront and remaining USD750 concern JGA/Riseklix project payment, not Table sponsorship revenue. Retain what is already paid, what remains due and any allocation basis.
2. **Additional cash to proceed.** Show future cash receipts/payments, deposits, cancellation exposure and remaining obligations separately from amounts already spent. A paid deposit is a partpayment unless the actual terms establish a separate fee.
3. **Full repeatable programme resources.** Include future research production, JGA labour, sales, servicing, moderation and event operations as applicable. Current commission is not proof of future unit cost; salaried time may be realresourcecost without additional cash.

Use the same common research basis and time horizon to compare A and B. An initial feasibility investment can be shown separately or allocated explicitly; do not silently charge every research-only unit the full programme-development cost. Legitimate cost recovery and multiple licence/partner revenues remain possible.

## Input groups and unresolved values

| Group | What needs to be defined | Applicability |
| --- | --- | --- |
| IN01: Case, period and edition | Selected A/B route, horizon, edition/version, pilot city ifchosen, annual city list and event months. No calendar, annual refresh count or Texas city inferred. A can remain usable when event inputs are not selected. | All cases; selected event/city details only for B. |
| IN02: Research and free/paid units | Number of actual modelled editions, partner bundles, additional unbundled licences/use types, optional sold/scoped briefings and free contributor copies. Same edition can support legitimate multiple buyers. Remove equivalent/bundled double-counts; contributor benefit does not imply a second employer purchase. | All cases as applicable. |
| IN03: Price and volume assumptions | Test prices, customer/partner counts, service units, fulfilment conditions and assumption/source IDs. No sales or willingnesstopay observed. Conservative/base/optimistic are assumptions, not confidence intervals or forecasts. | Only revenue streams actually modelled. |
| IN04: Initial investment and remaining obligations | Existing USD1500commission with report1000/Table500 scope allocation; actual paid/upfront/balance state and dated FX if needed. Userreported USD750received byRiseklix is not sponsor income forJGA. Firstprojectfee is not recurringedition cost; do not silently load allTablefeasibility onto research-only unitcost. | Initial project/investment and later funding views. |
| IN05: Research production and servicing | Research/editorial/design/analysis/rights/admin/sales preparation and optional briefing/followthrough work, hours and actual rate/cash classification. JGAstafftime and alreadybudgeted salary/opportunity cost differ from new cash. Allocate sharedtime once; do not add an overhead-loaded rate and the same overhead again. | All cases that use the work; common costs occur only as specified. |
| IN06: Event costs and participant load | Practitioner seats, host/moderator/partner seats ifany, room capacity, quotedminimum/fee, menus, drinks, service, tax and cancellation conditions. Perpersonmenu is not roomminimum. Distinguish minimumspend eligibleitems, roomhire, deposits and separate event liability. If not known retainunknown; no named partner defaultseat. | Selected B event/city only. |
| IN07: Travel, accessibility and participation operations | Recruitment/scheduling/moderation/admin, accessible/privacy-fit room, necessary travel/accommodation and who bears it. Free attendance does not promise travel paid. Texas city not defined; do not fabricate route/time/cost or countcapacity asrecruitedpeople. | Selected event/city only, with staff/member roles distinct. |
| IN08: Cash timing and exposure | Invoice, expectedreceipt, supplierdeposit/balance/refund/cancellation dates; spend alreadycommitted/receivedfunding. Signed/invoiced/received/fulfilled differ. Deposits paid against invoice not addedagain as separate expense; recoveries and future obligations remain distinct. | Cash schedule for selectedstreams/costs. |
| IN09: Currency and tax basis | Originalcurrency, datedFX direction/source, net/gross tax/service basis and any actuallyconfirmed recovery/refund assumptions. Do not assume FX=1, missingtax=0, serviceoptional orVATrecoverable. No universal tax/legal treatment asserted. | Any nonreportingcurrency/tax-sensitive row. |
| IN10: Scenario and risk decisions | Sales, partnerfees, workhours, deliveryinflation/delay/cancellation assumptions; startingcash/riskappetite for decision. No arbitrarygo/no-go threshold. Receivedfunding versus nonrefundableexposure and deliveryreadiness must be visible; favourableassumptions do not validate demand. | Case-dependent parameters and tests. |

## Unknown, zero and not applicable

A missing required cost, price, city or FX rate is not a zero. Use an explicit unknown/unconfigured result for the affected selected case; unselected event inputs should not block a valid research-only case. An explicit zero needs a source/assumption basis, such as a cost genuinely borne elsewhere, not a shortcut that hides work. No current values are populated in the shared financial register by this design.

## Revenue, cost and fulfilment units

The edition, licence/use, briefing, partner bundle, free contributor copy, practitioner, attendee seat, event, programme and staff hour are different units. A single report can be legitimately sold through multiple licences. The same free or bundled entitlement is not counted again as another sale. A planned programme is not a contracted subscription, and a signed order/invoice is not received cash or fulfilled benefit.

## Core model calculations

| Calculation | Logic | Boundary |
| --- | --- | --- |
| FM01: Unbundledlicencerevenue | sum(modelled unbundled licence units by type × their scenario price) | Counts exclude copies/entitlements already included in partner or free access. Customer counts and prices remain assumptions. |
| FM02: Partnershiprevenue | sum(modelled partner bundles × their scenario price) | Define actual edition/work/use and includedbenefits. Do not separately resell/count bundled entitlement by assumption. |
| FM03: Incremental event cash | sum(additional event-related cash costs not in common research-only case) | Includes actual selected room/minimum/menu mechanics and timing. Do not add an entire menu total plus the same minimum spend when one offsets the other. |
| FM04: Operating contribution on cash-cost basis | modelled revenue less defined attributable external cash costs | Managerial operating measure, not bank cash or formal accounting recognition. Fulfilment and invoicing are separate from actual receipts/payments in FM08. |
| FM05: Full resource result | modelled revenue less complete external cost and JGA/internal resource allocation, without duplicates | Separate a stafftime allocation from extra cash. Explicit sharedresearch allocation and initialinvestment recovery view. |
| FM06: Remaining funding gap | relevant fixed cost less net contribution of partner/other streams already included | Do not add partner revenue or included licence contribution a second time. Positive gap/negativeunitcontribution handled explicitly. |
| FM07: Break-even additional licences | if remaining funding gap <= 0: 0 additional licences; otherwise if unit contribution > 0: ceiling(gap / unit contribution); otherwise: no finite break-even | First test whether the remaining gap is already covered. For a positive gap, a zero/negative unit contribution has no finite break-even. Use the selected licence type/mix and servicing cost; capacity can still make a numerical result infeasible. |
| FM08: Closing cash by month | opening cash + actual-modelled receipts − cash payments | Invoicevalue and revenuefulfilment are not cash receipts. Carry deposits/refunds/remaining obligations correctly, no doubleexpense. |
| FM09: Peak extra funding | maximum positive cumulative cash deficit under the chosen startingcash/timing definition | Initialinvestment already paid, remaining balance and future event exposures need separate views; no assumed sponsorreceipt. |
| FM10: Event increment versus research-only | B result minus comparable A result over same horizon/common research basis | Revenue uplift is a separate explicit scenario hypothesis. Do not ascribe all research sales to the dinner or force A to pay B-only feasibility/hospitality costs. |

## Scenario tests before any recommendation

Test zero sales, one fewer/no partner, lower partner/licence prices, greater staffing/servicing hours, higher venue/travel cost, delayed receipts, cancellation exposure and a delayed launch. Test missing versus explicit-zero inputs and all route/currency selections. A favourable scenario is not buyer validation. Mathematical break-even also requires enough delivery capacity, rights and practical time; it is not a go decision by itself.

This is a managerial planning model, not statutory revenue recognition, tax advice or an authorisation to incur costs. Reporting GBP remains a proposal; retain original currencies and dated FX direction. The annual Texas location remains unconfirmed. The [structured inputs](T04-input-requirements.json) and [formula specification](T04-formula-design.json) keep actual values/results blank until the separate model build.
