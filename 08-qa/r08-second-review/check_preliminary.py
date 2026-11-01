from pathlib import Path
import json,hashlib
ROOT=Path(__file__).resolve().parents[2]
checks=[]
def read(p):return json.loads((ROOT/p).read_text())
def sha(p):return hashlib.sha256((ROOT/p).read_bytes()).hexdigest()
def check(x,label):
 checks.append({'check':label,'passed':bool(x)})
 if not x:raise AssertionError(label)
base=read('08-qa/R08-second-check-baseline.json')['records']
check(len(base)==85,'85 fixed prior/core/client/first-pass records present')
for x in base:check(sha(x['path'])==x['sha256'],'Preservation hash: '+x['path'])
snaps=read('03-report/research-notes/r08-second-check/before-review/manifest.json')['records']
check(len(snaps)==8,'Eight first-pass R08 mutable outputs snapshotted')
for x in snaps:check(sha(x['snapshot_path'])==x['sha256'],'First-pass snapshot: '+x['original_path'])
check(read('01-method/question-map.json')==read('01-method/question-map-v0.2.json'),'Fourteen-question version0.2 exactly preserved')
check(len(read('01-method/question-map.json')['records'])==14,'Fourteen core questions retained')
for p in ['05-analysis/observations.json','05-analysis/charts.json','04-table/financial-inputs.json']:
 check(read(p)['records']==[],'No unperformed research populated: '+p)
old=read('03-report/research-notes/r08-second-check/before-review/canonical-before.json')
nowclaims={x['claim_id']:x for x in read('02-evidence/registers/claims.json')['records']}
nowfindings={x['finding_id']:x for x in read('05-analysis/findings.json')['records']}
check(all(nowclaims[x['claim_id']]==x for x in old['claims']['records']),'All338 prior canonical claims unchanged')
check(all(nowfindings[x['finding_id']]==x for x in old['findings']['records']),'All76 prior internal findings unchanged')
for ident,status in [('CLM-0051','quarantined_conflicting'),('CLM-0052','quarantined_conflicting'),('CLM-0167','hold_numeric_reuse'),('CLM-0168','hold_numeric_reuse'),('CLM-0218','hold_universal_ui_behaviour'),('CLM-0392','hold_numeric_reuse')]:check(nowclaims[ident]['status']==status,'Existing hold preserved: '+ident)
checked=set()
def filehashes(o):
 if isinstance(o,list):
  for x in o:filehashes(x)
 elif isinstance(o,dict):
  for k,v in o.items():
   if (k=='path' or k.endswith('_path')) and isinstance(v,str):
    h=o.get('sha256' if k=='path' else k[:-5]+'_sha256')
    p=ROOT/v
    if h and p.is_file() and v not in checked:
     check(sha(v)==h,'Strand retained original/extract/render hash: '+v);checked.add(v)
   filehashes(v)
claims=0
for d in ['history','market','root']:
 p='03-report/research-notes/r08-second-check/'+d
 for f in ['capture-manifest.json','source-candidates.json']:
  filehashes(read(p+'/'+f))
 for x in read(p+'/claim-candidates.json')['records']:
  check(x['value'] is None and x['unit'] is None and x['denominator'] is None,'Bounded claim adds no numeric metric: '+x['candidate_id']);claims+=1
result={'date':'2026-10-29','status':'preliminary_source_and_preservation_review_passed','check_count':len(checks),'checks':checks,'strands_claims_reviewed':claims,'retained_files_checked':len(checked),'reviewer_source_sample':['LFB2025 renderedPDF3–4 visually inspected','Scottish2024/25audit renderedPDF46 visually inspected','CintraSRC0131/0132 retained current text and metadata','HMRCchoosepayrollSRC0078 retained relevant text','QQESRC0003 retained exact relevant sections'],'scope':'Independent pre-integration source/preservation review only. Competitor and final framework/application integration pending; no final pass implied.'}
(ROOT/'08-qa/r08-second-review/source-review-checks.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='checks'},indent=2))
