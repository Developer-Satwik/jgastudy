# Cash and remaining-obligation integration requirements

1 November 2026. Internal requirements before completing the matched programme model. Preserve the original four workbooks and seventy shared financial inputs.

| Requirement | Minimal practical implementation |
| --- | --- |
| Evidence and payment stage | Link the real order, invoice, acceptance condition and settlement evidence. An observed signature or invoice is not an observed cash receipt. Keep expected dates explicitly assumed. |
| One real transaction once | Reconcile credited deposit, remaining balance, gross bill, fee, net settlement, refund and credit by object and transaction identity. Different ledger IDs can still duplicate the same deposit. |
| Same decision date in A/B | Keep already incurred/unavoidable amounts in both relevant decision cases. Selecting research-only after a deposit was paid does not undo it. Before-commitment and after-commitment comparisons differ. |
| Expiry within the horizon | Show approaching credit use/expiry and delivery deadlines. The original opening-date status is not a rolling expiry alert. Review actual terms without automatic write-off or refund. |
| Fulfilment and usable capacity | Carry remaining units into actual dates, tasks and capable available people, including outside the displayed year. Cash received does not complete work or establish free capacity. |
| Gross, net, noncash and tax | Reconcile actual bank settlement to the selected gross/net basis. In-kind support is no cash receipt. Resolve applicable supply, tax and charge treatment for the actual entity and scope; do not hard-code generic VAT or tax recovery. |
| Term, rights, payer and bundle | Identify the exact asset, period, users/use and responsible payer. Count included rights once within the paid bundle. No automatic licence renewal, market price or cross-border terms. |
| Receipt and work stresses | Test delayed/absent receipts alongside fixed supplier dates and continuing fulfilment. Link same-payer or shared-approval delays when appropriate; no unsupported probability or collection-average assumption. |

Use existing records and a few linked fields, not extra compulsory interview questions or another software system. Keep the current USD1,500 commission separate from future partner revenue. Its reported USD750 upfront is not independently bank-reconciled, and its USD750 balance is conditional on satisfactory completion and written acceptance.

The [eighteen read-only applications](research-notes/t05c-second-check/cash-applications.json) show the required behaviour. They use constructed examples and independent arithmetic; they are not eighteen new workbook-engine tests or adopted forecasts. The first workbook's 65 engine tests and seven visual regions remain preserved.

Return to the [second-check findings](T05C-SECOND-CHECK-READOUT.md). Full-model implementation and authorised buyer/member/practitioner work remain open.
