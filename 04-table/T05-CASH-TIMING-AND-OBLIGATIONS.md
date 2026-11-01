# Cash timing and remaining obligations

1 November 2026. Internal working component. This prepares cash and fulfilment logic; the complete programme budget and commercial recommendation remain open.

## What is now modelled

The workbook separates dated cash from remaining promises. Its three sheets are Cash plan, Cash legs and Obligations. The cash plan supports a selected research-only route or a route including event rows. Monthly results, daily-end funding need and a separate same-day payments-first stress all use the same selected dated legs. The obligation view keeps customer benefits, supplier payments, work and future-use credits as different objects with their own units.

Start month, opening cash, coverage confirmations and selected transactions remain unresolved. Reserved rows are storage capacity, not projected customers, events or contracts. No supplier term, price, receipt date, credit, booking or sales forecast has been entered as an actual observation.

## Research and source choices

The [British Business Bank cash-flow guide](https://www.british-business-bank.co.uk/business-guidance/guidance-articles/finance/what-is-cash-flow-how-do-you-manage-it) explains why a profitable business can still face a cash gap when service/supplier outgoings precede customer receipts. We use that timing distinction, without adopting its examples, a minimum cash buffer or financing advice.

The [Australian government guide](https://business.gov.au/finance/cash-flow/set-up-a-cash-flow-statement) provides the opening-plus-receipts-minus-payments roll-forward and asks estimates to be labelled. Its local tax rules and template figures are not imported into JGA's model. This is a managerial planning component rather than a statutory cash-flow statement.

The [Bank of England exchange-rate page](https://www.bankofengland.co.uk/statistics/exchange-rates) qualifies its published reference rates. No rate was taken from it. The workbook requires an explicit positive GBP-per-original-unit factor, dated basis and source for a selected EUR/USD leg. GBP-to-GBP needs no foreign conversion. Actual transaction spread/fees need their own applicable treatment; the calculator does not infer VAT recovery or other tax cash flows.

Earlier [iVentiv terms](https://www.iventiv.com/terms-and-conditions) distinguish future-use credits and postponement. This supports keeping a restricted credit separate from cash refunded. Those clauses and their differing payment intervals are not JGA terms.

## JGA's existing commission is a separate object

The agreed current project is US$1,500: US$1,000 report and US$500 Table feasibility. The user reported US$750 upfront received; the supplied acknowledgement replies to that payment request. The remaining US$750 depends on satisfactory completion and written acceptance under the preserved baseline. No fixed remaining-payment date is inferred from an old request due date or a working delivery target.

The generated working agreement and supplied acknowledgement are retained with hashes. They are not an independently retrieved executed copy or a bank reconciliation. An acknowledgement time is not automatically a bank settlement date.

For JGA this fee is an initial project investment. It is not partner revenue, a recurring edition cost or an automatically repeated event charge. The workbook shows the original-currency commission context separately; it does not load the US$750 as GBP opening cash, sponsorship income or a new future payment. If the selected cash period includes relevant payments, enter their actual or explicitly assumed dates and conversion once. If paid before the period, they are already reflected in the chosen opening-cash basis.

## Dated cash legs

Each used leg needs its scope, receipt/payment direction, linked object, date, original currency and amount, reported-observation or assumption class, and source/basis. EUR/USD conversion additionally needs a factor and date. The amounts are actual gross cash or clearly labelled scenario cash, with any applicable included charges described. A refund is a separate opposite-direction cash leg linked to the same supplier/customer object, not an invented negative expense or cancellation discount.

Unused rows are excluded. A used Event row is excluded from the research-only route; selecting the event route exposes its missing data. A used row with missing fields is unavailable, including outside-window selected legs. This deliberately requires a complete selected leg before it can be treated as known. Rows before the start month or after the displayed horizon remain visible but do not replay into current-period cash. Unpriced future work belongs in Obligations until its cash timing and amount are scoped.

The coverage confirmation means the model operator has included the cash legs relevant to this selected scope. It is not permission to spend, approval of a forecast or an independent assertion that the schedule is complete. Missing confirmation prevents a blank ledger appearing as a funded programme. Observed rows cannot be dated after the chosen evidence date. Assumed rows remain scenarios even when their expected payment falls before that date.

## Monthly cash and shorter funding gaps

Monthly opening cash rolls from the previous closing balance. Receipts and payments use inclusive month start and exclusive next-month start, so the last day is included and the next month is not counted twice. No forecast receipt is treated as received merely because an invoice or contract exists.

Daily-end balances are calculated from dates, so the cash legs do not need to be entered in chronological row order. The lowest date-end balance, including opening cash, determines additional funding needed on that basis. This does not insert a loan or financing plug.

Same-day netting can still hide a payment made before a receipt. The separate payments-first stress deducts all payments on a date before counting that date's receipts. It is a deliberately adverse sequencing illustration, not a statement about actual intraday settlement, a funding commitment or a required reserve. Actual settlement order and ability to fund a commitment still need checking.

## Deposits, balances, credits and refunds

A hypothetical supplier bill of £1,900 with a £500 credited deposit leaves £1,400 to pay. The two cash payments total £1,900. The deposit does not turn the economic bill into £2,400. Link all legs to the same booking/invoice object and reconcile the agreed total before integration.

A £500 future-use credit is different: it may carry an expiry, permitted use and replacement-service obligation while delivering no cash today. Record its units and terms in Obligations. Only an actual or explicitly assumed cash refund belongs in the cash schedule. A credit expiry is flagged for review; the model does not automatically forgive a debt, turn a credit into cash or assert a right has legally expired.

Refunds and replacement spending are separate dated legs when actually applicable. Do not add both a gross final supplier bill and the same deposit as another expense, or count a refund twice through a reduced payment and a separate receipt. No refundability, cancellation probability or recovery percentage has been invented.

## Remaining units and work still owed

Each selected obligation identifies its object, kind, description, unit, agreed units, satisfied/applied units and date, trigger or unknown timing. Remaining units are calculated only when valid. Unlike units are never added into a combined total. Paid money does not satisfy a customer benefit or complete remaining work; their own delivered units are needed.

The categories serve different directions: Customer benefit and Work describe output/effort still owed; Supplier payment describes a payment commitment in its stated units; Future-use credit describes a held noncash entitlement. Supplier delivery or an owed replacement service can have a separate appropriate benefit/work row. A cash payment can settle the payment object while leaving a delivery object open.

The cash view and obligation view have separate coverage/readiness. Cash can be calculated while unpriced or untimed obligations remain prominently unresolved. That prevents a positive cash balance from being presented as profit, spare distributable money or a completed programme. Future delivery beyond the horizon stays on the obligation list. Scope, capability, actual hours, rates and package/reuse overlap still need linking during full integration.

## Verification

The artifact-engine workbook passed 65 input-driven calculation tests. Export checks confirmed the three sheets, saved formulas and cached values, input validation, restored blank assumptions, unused reserved rows and absence of spreadsheet error cells or external workbook links. Seven rendered regions were visually reviewed. Same-agent checks verified the retained source captures, append-only evidence/history and preserved earlier workbooks and inputs. Native Microsoft Excel was not tested; no independent review is claimed for this component.

## What remains for the complete programme model

Join this cash component to research production, service/sales and event work using the same period, edition, original currencies and allocation basis. Reconcile all future payment legs with their economic costs, initial investment, actual reported payments and remaining commitments. A free or bundled copy remains a fulfilment benefit rather than an extra licence sale.

Then calculate the matched pilot/annual A/B results, conservative/base/optimistic scenarios, break-even, practical capacity and the agreed sensitivities. Do not assume event revenue uplift, use a generic licence price, multiply a UK event across four locations or select an unspecified Texas city. Actual buyer/member/practitioner work remains inactive and separate from this constructed planning component.

The earlier three workbooks, all seventy shared financial inputs, fourteen core questions, practitioner targets, free full practitioner research and agreed fee remain unchanged. No message, payment request, bank action, booking, hiring or spending occurred.
