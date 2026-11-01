from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parents[2]
checks=[]
def check(value,label):
 checks.append({'check':label,'passed':bool(value)})
 if not value:raise AssertionError(label)
b=json.loads((R/'08-qa/WP03-baseline-manifest.json').read_text())['files']
check(len(b)==111,'111 immutable preparation baseline records')
for x in b:
 check(hashlib.sha256((R/x['path']).read_bytes()).hexdigest()==x['sha256'],'Preserved '+x['path'])
q=json.loads((R/'01-method/question-map.json').read_text())
check(q==json.loads((R/'01-method/question-map-v0.2.json').read_text()) and len(q['records'])==14,'Canonical14core equalsv0.2')
for f in ['05-analysis/observations.json','05-analysis/charts.json','04-table/financial-inputs.json']:
 check(json.loads((R/f).read_text())['records']==[],f+' actualdata stays empty')
t=json.loads((R/'01-method/research-notes/wp03/routes/constructed-route-tests.json').read_text())
check(len(t['tests'])==8 and not t['practitioner_testing'],'Eight internal test designs, not practitioner tests')
check(all(not x['executed'] and x['actual_participant'] is None for x in t['tests']),'Designs remain unexecuted until root application')
for f in ['01-method/research-notes/wp03/wording/PARTICIPANT-WORDING.md','01-method/research-notes/wp03/routes/COLLECTION-ROUTES.md']:
 check((R/f).exists(),'Input exists '+f)
result={'date':'2026-10-29','status':'passed_preliminary_preservation_and_scope','checks':checks,'check_count':len(checks),'scope':'Independent preliminary review before integrated pack and applied route records. No legal certification, approved collection route or practitioner validation.'}
(R/'08-qa/wp03-review/preliminary-checks.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='checks'},indent=2))
