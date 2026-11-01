from pathlib import Path
import json,hashlib,shutil
R=Path(__file__).resolve().parents[1];D='2026-10-30'
def rd(p):return json.loads((R/p).read_text())
def wr(p,d):(R/p).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
review=rd('08-qa/t02-review/integration-checks.json');assert review['status']=='passed_for_internal_T02_proposition_preparation' and not review['open_substantive_issues'] and all(x['passed']for x in review['checks'])
for x in review['reviewed_artifacts']:assert hashlib.sha256((R/x['path']).read_bytes()).hexdigest()==x['sha256'],x['path']
p=R/'04-table/T02-proposition-map.json';dest=R/'04-table/research-notes/t02/reviewed-before-status';dest.mkdir(exist_ok=True);out=dest/p.name;shutil.copy2(p,out)
wr('04-table/research-notes/t02/reviewed-before-status/manifest.json',dict(date=D,records=[dict(original_path=str(p.relative_to(R)),snapshot_path=str(out.relative_to(R)),sha256=hashlib.sha256(out.read_bytes()).hexdigest())]))
x=rd('04-table/T02-proposition-map.json');x['status']='internal_proposition_design_reviewed_validation_pending';x['review_basis']='08-qa/T02-independent-review.md and t02-review/integration-checks.json,331independent checks. Design review only; T03 actual input, collection arrangements, T04/T05 economics and final-use review remain open.';wr('04-table/T02-proposition-map.json',x)
x=rd('00-control/work-packages.json');x['updated_on']=D;x['active_work_package']='WP14'
for r in x['records']:
 if r['work_package_id']=='WP12':r.update(status='T01_T02_internal_design_reviewed_validation_pending',working_file='04-table/T02-PROPOSITION-PACK.md',T02_design_reviewed=True,T02_design_reviewed_on=D,T02_buyer_validated=False,T03_conversations_complete=False,evidence_of_completion=['08-qa/T01-second-check-completion.json','08-qa/T02-independent-review.md','08-qa/T02-completion-check.json','04-table/T02-proposition-map.json'])
 if r['work_package_id']=='WP14':r['next_design_input']='Reviewed T02 three-proposition design, eight work objects and open use/entitlement choices; not actual prices, demand or rights.'
x['next_action']='T04–T05: define commercial routes and model units/assumptions from reviewed T02 product/use/delivery design, then build source-labelled costs, cash timing and Model A/B cases. Actual T03 buyer/member input stays pending existing user/client/collection decisions. No external sending, quotes, booking or spending.';wr('00-control/work-packages.json',x)
x=rd('00-control/changes.json');assert not any(v['change_id']=='CHG-023'for v in x['records']);x['records'].append(dict(change_id='CHG-023',date=D,type='T02 concrete internal proposition and discovery-design preparation',description='Three draftfutureproducts:research-usepack,foundingpartnerandpractitionercycle;fivecontractsegments+employeradditionalhypothesis,eightopenuseoptions,eightuncosted/unassignedworkobjects. ProposedTableguidev0.2retains6B/6MwithneutralB01/unaideddiscoveryfirst, inactiveoriginalWP03guide unchanged. Fullcontractreport/JGAIP/practitionerfreeresearchpreserved;optionalbriefing/followthrough/eventaccess separatelyscoped. Accurateedition/fundingpurposeclarifiesalreadycommissionedresearchandseparatecost/revenueaccounting. Independent331checks,146protectedfiles;zero newcanonicalrecords,prices,financialinputs,fieldworkorcontact. Currentstepdesignreviewednotbuyer/membervalidated.'));wr('00-control/changes.json',x)
p=R/'00-control/CURRENT-STATUS.md';s=p.read_text()
s=s.replace('Next refine T02 using these selective conditions before later actual T03 input and T04/T05 cost/cash modelling.','The reviewed T02 design below now implements these selective conditions; actual T03 input and T04/T05 cost/cash work remain open.')
s=s.replace('review the prepared WP03 collection pack, T01 second-check readout and T02 refinement brief; make necessary checkpoint revisions and refine propositions.', 'read the reviewed T02 proposition pack and delivery map, retain the prepared inactive WP03 pack, and continue T04/T05 commercial route/model design while actual T03 input remains pending.')
insert='''## T02 concrete proposition design reviewed, 30 October 2026

Use the [proposition pack](../04-table/T02-PROPOSITION-PACK.md) as the current working start. Three draft products define research use, founding research funding and practitioner research/peer value. Five contract-named buyer categories remain visible; employer-side paid use is an additional hypothesis. [Buyer/use choices](../04-table/T02-BUYER-USES-AND-RIGHTS.md) preserve the free practitioner benefit and JGA commissioned-IP arrangement. No equivalent access is forecast as a second sale.

The [delivery/validation map](../04-table/T02-DELIVERY-AND-VALIDATION.md) identifies eight work objects without invented owners, hours, costs or capacity. Briefings, follow-through notes and event/commercial-access components are bounded options to test and cost, not new signed-project obligations. Funding purpose must identify the actual edition/work, including if already commissioned or complete; costs and partner/licence revenues remain separately defined.

The proposed [Table guide version0.2](../01-method/TABLE-VALIDATION-GUIDES-v0.2.md) keeps six buyer/six member IDs, adapts buyer discovery to actual use, and places unaided needs/alternatives before concepts. It is inactive: original guide, WP03 policy, fourteen report questions and collection decisions remain unchanged. No participant, price, permission, concept exposure, order or actual contribution exists.

Independent integrated design review passed331checks with146baselinefiles preserved. Canonical sources223/claims432/findings81 remain unchanged. Current QA: `08-qa/T02-completion-check.json`. WP12 is reviewed for internal design, not market validation. Next T04/T05 can define commercial routes and ModelA/ModelB units, full work/cost and cash assumptions; actual T03 input still awaits existing arrangements. Nothing sent, purchased, booked or collected.

'''
s=s.replace('## Still open\n',insert+'## Still open\n');p.write_text(s)
p=R/'README.md';s=p.read_text()+'''
## T02 propositions ready for review

The [proposition pack](04-table/T02-PROPOSITION-PACK.md) is the current working entry point. Three draft products separate research use, funding partner and practitioner benefits. [Use/rights choices](04-table/T02-BUYER-USES-AND-RIGHTS.md) and [delivery/validation work](04-table/T02-DELIVERY-AND-VALIDATION.md) make the product and burden explicit without pricing or new scope commitments.

Independent integrated review passed331checks;146protectedfiles and all223source/432claim/81findingrecords remain unchanged. The proposed Table guide is inactive and the fourteen report questions remain unchanged. T03 actual input and collection arrangements remain open. Next: T04/T05 commercial route and cost/cash model design. Current QA: `08-qa/T02-completion-check.json`. Nothing sent.
''';p.write_text(s)
p=R/'05-analysis/CONTRADICTIONS-AND-GAPS.md';p.write_text(p.read_text()+'''

## T02 proposition-design review, 30 October 2026

- Three concrete future-product drafts do not replace the current complete commissioned report or add production, advice, event or recurring-service obligations. Five contract-named commercial segments remain hypotheses, with employer paid use additional rather than primary by assumption.
- Full free practitioner research, JGA commissioned IP and underlying rights are preserved. Customer use choices are ungranted, not a new Riseklix licence/veto. Equivalent free/bundled access is not counted twice.
- Partner support must identify actual edition/funding purpose, including existing commissioned/completed work. Distinguish legitimate multiple revenues from double-counted costs or entitlements. No newly commissioned study is implied where none exists.
- Optional briefing/follow-through/commercial access require scope, evidence, permissions, actual owners/capacity and costs. Recognition does not by itself authorise attendance disclosure or attribution; contextual identification remains possible.
- Proposed guide0.2 has6B/6M, neutralbuyerwording andunaideddiscoverybeforeconcept. It is not active; originalguide/WP03/14core unchanged. Actualevent/person counting and collectionrelease decisions remain.
- Independent331checks and146baselinefiles passed;223sources432claims81findings unchanged. Design reviewed, actualbuyer/member demand, prices, rights, usableevidence and T04/T05economics not established. No contact, contribution, quote, booking or spend.
''')
print('T02 reviewed design status and next-stage records saved')
