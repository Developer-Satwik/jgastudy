"""Prepare explicit illustrative scenario inputs, preserving canonical financial records."""
from pathlib import Path
import json,hashlib
ROOT=Path(__file__).resolve().parents[1]
B='04-table/research-notes/t05-programme'
def load(p):return json.loads((ROOT/p).read_text())
groups=[]
def add(key,label,unit,pilot,annual=None,basis='Constructed planning assumption, not observed demand, a quote or an approved budget.',source=''):
    groups.append({'key':key,'label':label,'unit':unit,'pilot':pilot,'annual':pilot if annual is None else annual,'basis':basis,'source':source,'actual_observation':False})
add('months','Displayed months','months',[3,3,3],[12,12,12])
add('contributors','Usable contributors costed','people',[10,8,6],basis='Preserved effort-case contributor assumptions. Actual permissioned contributions remain zero.')
add('editions','Research editions','editions',[1,1,1],basis='One shared hypothetical edition in both routes. No automatic annual refresh.')
add('licences','Standalone licences','orders',[3,10,20],[6,20,40])
add('licence_price','Standalone licence fee','GBP/order',[250,500,750])
add('partners','Research partner bundles','orders',[0,1,2],[0,2,3])
add('partner_price','Partner bundle fee','GBP/order',[1500,2000,3000])
add('briefings','Additional paid briefings','sessions',[0,2,4],[1,4,6])
add('briefing_price','Additional briefing fee','GBP/session',[200,300,450])
for key,label,price in [('event_licences','Additional B-only licences',[250,500,750]),('event_partners','Additional B-only partners',[1500,2000,3000]),('event_briefings','Additional B-only paid briefings',[200,300,450])]:
    add(key,label,'orders',[0,0,0],basis='Explicit zero event revenue uplift in all illustrations. Change only as a stated hypothesis; no attribution or demand established.')
    add(key+'_price',label+' fee','GBP/order',price)
add('included_licences','Licence rights included per partner','rights/bundle',[1,1,1],basis='Bundle design illustration. These are benefits, never additional licence revenue.')
add('included_briefings','Briefings included per partner','sessions/bundle',[1,1,1],basis='Bundle design illustration. Included sessions generate work, not another sale.')
add('campaigns','Sales campaigns','campaigns',[1,1,1],[1,2,2])
add('contacts','Worked contact attempts','attempts',[40,60,80],[80,120,160],basis='Labour illustration includes unsuccessful attempts. Not an outreach instruction, funnel conversion or quota.')
add('discussions','Sales discussions','discussions',[6,8,12],[10,16,24])
add('proposals','Initial proposals','proposals',[4,6,8],[6,10,16])
add('rounds','Additional commercial rounds','rounds',[3,3,2],[5,6,4])
add('distribution','Shared distribution runs','runs',[1,1,1],[1,2,2],basis='One run can include free, bundled and paid recipients. Do not count each copy as a separate run.')
add('cases','Support cases','cases',[3,2,1],[5,4,2])
add('renewals','Renewal/expiry administration','actions',[0,0,0],[2,2,2],basis='Administration only. No renewal receipt or automatic subscription.')
add('cycle_notes','Optional cycle notes','notes',[0,0,0])
add('extra_assets','Additional use assets','packages',[0,0,0])
add('contingency','Cash-cost reserve','fraction',[.15,.10,.05],basis='Illustrative reserve on future operating cash-cost budget. Not a probability, actual expense or scheduled payment.')
add('receipt_delay','Expected receipt delay','days',[60,30,0],basis='Scenario timing only. Not calibrated from survey late-payment rates.')
add('receipt_deposit','Customer receipt first instalment','fraction',[.5,.5,1])
add('opening','Opening cash','GBP',[0,0,0],basis='Explicit zero funding illustration. No actual bank balance was supplied.')
add('usd_fx','Current investment comparison FX','GBP/USD',[.8,.8,.8],basis='Hypothetical comparison factor, not an actual Payoneer settlement or exchange-rate forecast.')
roles=[('Research',372/7.5,1,120,'Published research day-rate comparison /7.5 analyst hours; not a supplier quote.','FI-R01'),('Writing',440/7.5,1,120,'Published writing day-rate comparison /7.5 analyst hours; not a supplier quote.','FI-R02'),('Editing',37.11,1,100,'Published editing comparison; actual scope/minimum booking unconfirmed.','FI-R03'),('Design',348/7.5,1,100,'Published design day-rate comparison /7.5 analyst hours; not a supplier quote.','FI-R04'),('Coordination',46.19,1,100,'Published coordination comparison; actual suitable performer unconfirmed.','FI-R05'),('Commercial',45,0,60,'Analyst-assumed internal resource rate, not a published wage or extra cash salary.',''),('JGA',60,0,24,'Analyst-assumed retained review time valuation, not extra cash payroll or named availability.',''),('Moderation',65,1,40,'Explicit hypothetical moderator comparison. No capability, quote or staffing implied.',''),('Hosting',60,0,24,'Hypothetical internal host time, not cash pay.',''),('Travel',25,0,24,'Hypothetical staff travel-time resource value, separate from fare cash.','')]
fin={x['input_id']:x for x in load('04-table/financial-inputs.json')['records']};sources={x['source_id']:x for x in load('02-evidence/registers/sources.json')['records']}
for role,rate,cash,cap,basis,fid in roles:
    url='; '.join(sources[s]['url']for s in fin.get(fid,{}).get('source_ids',[])if s in sources)
    add('rate_'+role,role+' hourly valuation','GBP/hour',[rate,rate,rate],basis=basis,source=url)
    add('cash_'+role,role+' additional-cash share','fraction',[cash,cash,cash],basis='Hypothetical split between extra external cash and already-budgeted internal resource. No person hired.')
    add('capacity_'+role,role+' available hours/month','hours',[cap,cap,cap],basis='Unconfirmed hour-capacity illustration. Does not verify named people, skill or simultaneous duty coverage.')
rw=load('04-table/research-notes/t05-research-costs/workload/workload-candidates.json')
rm={x['workload_id']:x for x in load('04-table/T05-research-cost-map.json')['tasks']}
sw=load('04-table/research-notes/t05-service-costs/workload/workload-candidates.json');sm={x['workload_id']:x for x in load('04-table/T05-service-cost-map.json')['tasks']}
ew=load('04-table/T05-event-cost-map.json')
tasks=[]
for x in rw['report_provider_tasks']+rw['JGA_retained_tasks']:
    k=x['workload_id'];h=x['planning_hours'];add('hours_'+k,k+' '+x['task'],'hours/unit',[h['high'],h['base'],h['low']],basis='Preserved untimed task allowance. Conservative uses higher effort, optimistic lower effort. No measured time or AI saving.')
    tasks.append({'id':k,'label':x['task'],'role':rm[k]['role_group'],'scope':'Common','unit':'contributors'if x['unit']=='per_usable_contributor'else'editions','month':1 if int(k[-2:])<9 else 2,'basis':x['boundary']})
unit_map={'campaign_count':'campaigns','contact_attempt_count':'contacts','sales_discussion_count':'discussions','proposal_attempt_count':'proposals','extra_commercial_round_count':'rounds','won_order_count':'orders','reading_path_count':'licences_all','use_asset_package_count':'extra_assets','partner_bundle_count':'partners_all','distribution_run_count':'distribution','briefing_session_count':'briefings_all','service_case_count':'cases','invoice_cycle_count':'orders','renewal_action_count':'renewals','cycle_note_count':'cycle_notes'}
for x in sw['tasks']:
    k=x['workload_id'];h=x['planning_hours_per_unit'];add('hours_'+k,k+' '+sm[k]['task'],'hours/unit',[h['high'],h['working'],h['low']],basis='Preserved untimed service task allowance. Count real common work once; no automatic paid/free entitlement duplication.')
    role={'Specialist':'Research'}.get(sm[k]['comparison_role'],sm[k]['comparison_role'])
    tasks.append({'id':k,'label':sm[k]['task'],'role':role,'scope':'Common','unit':unit_map[x['unit_key']],'month':2 if int(k[-2:])>=7 else 1,'basis':x['boundary_and_exclusions']})
for key in ['campaigns','contacts','discussions','proposals','rounds','distribution','cases','renewals','cycle_notes','extra_assets']:
    add('extra_'+key,'B-only additional '+key,'activities',[0,0,0],basis='Explicit additional-work illustration. Keep genuine shared campaign/reuse once. If event-only sales require more work, enter it here; no automatic conversion or duplicated campaign.')
for x in sw['tasks']:
    k=x['workload_id'];role={'Specialist':'Research'}.get(sm[k]['comparison_role'],sm[k]['comparison_role'])
    tasks.append({'id':k+'-B','catalogue_id':k,'label':'B-only '+sm[k]['task'],'role':role,'scope':'Event','unit':'event_'+unit_map[x['unit_key']],'month':2 if int(k[-2:])>=7 else 1,'basis':'Additional B-only work, not a copy of the common task. '+x['boundary_and_exclusions']})
eventrole={'coordination':'Coordination','moderation':'Moderation','hosting':'Hosting','research support':'Research','travel time':'Travel','actual appropriate role':'Coordination'}
for x in ew['tasks']:
    k=x['task_id'];h=x['planning_hours_per_unit'];add('hours_'+k,k+' '+x['label'],'hours/unit',[h['high'],h['working'],h['low']],basis='Preserved untimed event task allowance. A role label does not verify availability or duty coverage.')
    for e in range(1,5):tasks.append({'id':k+f'-E{e}','catalogue_id':k,'label':x['label'],'role':eventrole[x['role_context']],'scope':f'E{e}','unit':x['quantity_unit'],'month':3*e,'basis':x['counting_note']})
events=[('E1','London','GBP',3,[125,100,80],[2000,1500,1000],300,[150,100,75],[4,3,2]),('E2','Manchester','GBP',6,[115,90,75],[1800,1400,1000],250,[300,250,200],[6,5,4]),('E3','Dublin','EUR',9,[140,110,90],[2200,1800,1400],350,[650,500,400],[10,8,6]),('E4',None,'USD',12,[None,None,None],[None,None,None],None,[None,None,None],[None,None,None])]
for eid,city,ccy,month,price,minimum,hire,travel,travelhours in events:
    add(eid+'_practitioners',eid+' practitioner places','places',[15,13,12],basis='Proposed capacity illustration only. Separate from the commissioned6–10 usable report contributions and up-to-four exploratory conversations.')
    add(eid+'_team',eid+' additional team places','places',[3,3,3])
    for key,label,unit,values in [('price','Catering per cover',ccy,price),('minimum','Eligible catering minimum',ccy,minimum),('hire','Separate room hire',ccy,[hire]*3),('travel','Fares/accommodation total',ccy,travel),('travelhours','Additional staff travel','hours',travelhours),('attempts','Worked invitation attempts','attempts',[50,40,30]),('coordcases','Access/dietary cases','cases',[3,2,1]),('changes','Material change cases','cases',[3,2,1])]:add(eid+'_'+key,eid+' '+label,unit,values,basis='City-specific constructed comparison, not a current menu, fare, quote, selected venue or attendance commitment. Texas values deliberately unresolved.'if eid=='E4'else'City-specific hypothetical planning value, not a supplier quote, current menu or fare.')
    add(eid+'_fx',eid+' original-currency conversion','GBP/'+ccy,[1,1,1]if ccy=='GBP'else[.85,.85,.85]if ccy=='EUR'else[.8,.8,.8],basis='GBP identity or hypothetical GBP per original currency unit. No actual foreign settlement or market forecast.')
    add(eid+'_service',eid+' additional service charge','fraction',[.125,.125,.125],basis='Hypothetical additional service charge. Other supplied figures treated as gross illustrative amounts; no VAT liability/recovery determined.')
    add(eid+'_deposit',eid+' supplier deposit share','fraction',[.5,.5,.5],basis='Hypothetical part-payment schedule, not refundability/cancellation terms.')
data={'date':'2026-11-01','status':'constructed_internal_planning_illustration_not_forecast','default_case':2,'default_scope':1,'start_date':'2027-01-01','start_date_basis':'Assumed illustration calendar, not project delivery date or agreed kickoff.','groups':groups,'tasks':tasks,'roles':[r[0]for r in roles],'events':[{'id':e[0],'city':e[1],'currency':e[2],'month':e[3]}for e in events],'actual_orders':[],'actual_participants':[],'actual_suppliers':[],'actual_bank_cash':[],'current_commission_usd':{'total':1500,'report':1000,'table':500,'upfront_reported_paid':750,'balance_conditional':750},'scope_guards':{'original_four_books_preserved':True,'financial_register_unchanged':True,'fourteen_questions_unchanged':True,'free_full_practitioner_research_preserved':True,'external_actions':[]},'source_provenance':[{'path':p,'sha256':hashlib.sha256((ROOT/p).read_bytes()).hexdigest()}for p in ['04-table/financial-inputs.json','04-table/T05-research-cost-map.json','04-table/T05-service-cost-map.json','04-table/T05-event-cost-map.json','04-table/T05-cash-map.json','04-table/T05C-second-challenge-map.json']]}
(ROOT/B/'scenario-inputs.json').write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({'drivers':len(groups),'work_rows':len(tasks),'roles':len(roles),'events':4,'shared_financial_register_modified':False}))
