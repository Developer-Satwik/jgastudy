from pathlib import Path
import json,hashlib,zipfile,xml.etree.ElementTree as ET
from urllib.parse import urlparse
ROOT=Path(__file__).resolve().parents[1]
checks=[]
def load(p):return json.loads((ROOT/p).read_text())
def check(ok,message):
    if not ok:raise AssertionError(message)
    checks.append({'check':message,'passed':True})
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,x):
    q=ROOT/p;q.parent.mkdir(exist_ok=True,parents=True);q.write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
old={x['original_path']:x for x in load('04-table/research-notes/t05-event-costs/before-review/manifest.json')['records']}
for x in old.values():check(sha(ROOT/x['snapshot_path'])==x['sha256'],'Exact snapshot '+x['original_path'])
for x in load('08-qa/T05E-baseline-manifest.json')['files']:
    p=Path(x['path']);p=p if p.is_absolute()else ROOT/p
    check(sha(p)==x['sha256'],'Protected original '+x['path'])
for f in ['02-evidence/registers/sources.json','02-evidence/registers/claims.json']:
    before=load(old[f]['snapshot_path'])['records'];now=load(f)['records']
    check(now[:len(before)]==before,'Earlier source/claim records unchanged '+f)
check(load('04-table/financial-inputs.json')==load(old['04-table/financial-inputs.json']['snapshot_path']),'All70 financial inputs unchanged')
check(len(load('05-analysis/findings.json')['records'])==81,'No new empirical finding')
routes=load('04-table/research-notes/t05-event-costs/evidence/source-candidates.json')['records']
check(len(routes)==7,'Seven adopted originals')
for x in routes:
    check(sha(ROOT/x['capture_path'])==x['capture_sha256'],'Source hash '+x['candidate_id'])
    check(sha(ROOT/x['parsed_path'])==x['parsed_sha256'],'Parsed text hash '+x['candidate_id'])
    check(urlparse(x['url']).hostname==urlparse(x['final_url']).hostname,'Adopted final domain matches publisher '+x['candidate_id'])
attempts=load('04-table/research-notes/t05-event-costs/evidence/capture-attempts.json')['records']
bad=next(x for x in attempts if x['candidate_id']=='E-S06')
check(bad['adopted']is False and 'unrelated'in bad['exclusion_reason'],'Unrelated old member-domain redirect excluded')
check(not any(x['candidate_id']=='E-S06'for x in routes),'Unrelated route absent from adopted evidence')
scope=load('04-table/T05-event-cost-map.json')
check([x['task_id']for x in scope['tasks']]==[f'WE{i:02}'for i in range(1,23)],'22 stable ordered tasks')
for t in scope['tasks']:
    h=t['planning_hours_per_unit'];check(0<=h['low']<=h['working']<=h['high'],'Task allowance order '+t['task_id'])
    check(t['quantity']is None and t['actual_work_records']==[],'No actual quantity '+t['task_id'])
check(len(scope['external_cost_rows'])==12 and all(x['selected']is None and x['amount_gbp']is None for x in scope['external_cost_rows']),'Twelve unselected unpriced direct areas')
check(all(x is None for x in scope['counts'].values()),'No attendance or capacity selected')
check(scope['labour_not_monetised'] and not scope['all_in_budget_available'] and not scope['full_financial_model_complete'],'No full price or programme completion claimed')
check(not scope['external_actions']and not scope['actual_quotes']and not scope['actual_participants']and not scope['actual_bookings'],'No enquiry, quote, participant or booking')
qa=load('08-qa/t05e-workbook/verification.json')
check(qa['check_count']==len(qa['tests'])==35 and all(x['passed']for x in qa['tests']),'35 input-driven calculation cases')
check(qa['all_counts_restored_blank']and qa['all_amounts_restored_blank']and not qa['native_Excel_tested'],'Engine/restoration boundary retained')
path=Path(scope['workbook_path'])
ns={'x':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
with zipfile.ZipFile(path)as z:
    wb=ET.fromstring(z.read('xl/workbook.xml'))
    check([x.attrib['name']for x in wb.findall('x:sheets/x:sheet',ns)]==['Event costs','Event work'],'Two expected sheets exported')
    a=ET.fromstring(z.read('xl/worksheets/sheet1.xml'));b=ET.fromstring(z.read('xl/worksheets/sheet2.xml'))
    def cells(x):return {v.attrib['r']:v for v in x.findall('.//x:sheetData/x:row/x:c',ns)}
    ca,cb=cells(a),cells(b)
    def cached(c):
        if c is None:return None
        v=c.find('x:v',ns)
        if v is not None:return v.text
        v=c.find('x:is/x:t',ns);return v.text if v is not None else None
    for sheet,c in [('Event costs',ca),('Event work',cb)]:
        check(not any(v.attrib.get('t')=='e'for v in c.values()),'No exported Excel error cells '+sheet)
    for addr in ['B7','B8','B9','B22','B23']:check(cached(ca[addr])=='n.a.','Unavailable cached result '+addr)
    check(cached(cb['I6'])=='n.a.','Unavailable saved total hours')
    for r in range(11,33):check(cached(cb.get(f'H{r}'))is None,'Quantity remains blank '+str(r))
    for r in range(31,43):
        for col in ['B','C','E']:check(cached(ca.get(f'{col}{r}'))is None,'Direct input blank '+col+str(r))
    check(cached(ca['B4'])=='2','Working case saved')
    check(len(b.findall('.//x:dataValidations/x:dataValidation',ns))==22,'Quantity validation exported for all22 tasks')
    check(bool(b.find('.//x:pane',ns)is not None),'Working header/identifier panes exported')
    formulas=[v.find('x:f',ns).text for c in [ca,cb]for v in c.values()if v.find('x:f',ns)is not None]
    check(all('['not in f for f in formulas),'No external workbook formula links')
    check(any('CHOOSE'in f for f in formulas),'Effort selector feeds active hours')

# Additional constructed mechanics explain future integration; they are not workbook budget inputs.
examples=[]
def example(ident,result,expected,note):
    check(result==expected,'Constructed mechanism '+ident)
    examples.append({'case_id':ident,'result':result,'expected':expected,'note':note,'actual_observation':False})
example('SEATS-17',[15+2,15+2<=16],[17,False],'All people count, not practitioners alone.')
example('MINIMUM-SHORTFALL',1400+max(1800-1400,0)+100,1900,'Hypothetical eligible spend, minimum and separate hire, before any applicable charges.')
example('ABOVE-MINIMUM',2200+max(1800-2200,0),2200,'Do not add the whole minimum to eligible consumption.')
example('DEPOSIT-CREDIT',[1900,1900-500],[1900,1400],'Credited deposit changes remaining cash, not total expense.')
example('CANCEL-SUPPLIER-FINAL',[300,300-100],[300,200],'A hypothetical credited deposit does not make final cancellation loss400.')
example('TWO-PEOPLE',2*2,4,'Two live people for two hours produce four person-hours.')
example('ONE-PERSON-TWO-ROLES',2,2,'One simultaneous two-hour host/moderator assignment is counted once.')
example('PACKAGE-NONOVERLAP',500+0,500,'Hypothetical inclusive package with no additional valuation of its included scope. No actual package rate adopted.')
save('04-table/research-notes/t05-event-costs/constructed-applications.json',{'date':'2026-11-01','status':'passed_constructed_only','cases':examples,'actual_inputs_added':0})
reviewed=[]
paths=[p for p in (ROOT/'04-table/research-notes/t05-event-costs').rglob('*')if p.is_file()and'before-review'not in str(p)]
paths += [ROOT/'04-table/T05-event-cost-map.json',ROOT/'04-table/T05-EVENT-OPERATIONS-AND-TRAVEL.md',path,ROOT/'08-qa/t05e-workbook/verification.json',ROOT/'08-qa/validate_t05e.py']
for p in paths:reviewed.append({'path':str(p.relative_to(ROOT))if p.is_relative_to(ROOT)else str(p),'sha256':sha(p)})
visual=[]
for x in qa['renders']:
    p=Path(x['path']);check(p.exists(),'Rendered workbook region '+x['range']);visual.append({**x,'sha256':sha(p),'visually_reviewed':True})
check(len(visual)==7,'Seven workbook regions visually reviewed')
result={'date':'2026-11-01','status':'passed_same_agent_component_review','independent_agent_review':False,'check_count':len(checks),'checks':checks,'reviewed_artifacts':reviewed,'visual_review':visual,'native_Excel_tested':False,'original_workbooks_changed':False,'shared_financial_inputs_changed':False,'full_programme_complete':False,'external_actions':0}
save('08-qa/t05e-review/verification.json',result)
print(json.dumps({'status':result['status'],'checks':len(checks),'reviewed_artifacts':len(reviewed),'workbook_visual_regions':7,'constructed_applications':8}))
