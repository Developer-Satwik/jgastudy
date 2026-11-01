from pathlib import Path
import json
import hashlib

ROOT=Path(__file__).resolve().parents[1]
CWD=ROOT.parents[1]
NOTES=ROOT/'03-report/research-notes'

def load(path):
    return json.loads(path.read_text())

def save(path,data):
    path.write_text(json.dumps(data,indent=2)+'\n')

def normalise_capture(path):
    if not path:
        return None
    candidate=Path(path)
    if not candidate.is_absolute():
        candidate=(CWD/candidate) if (CWD/candidate).exists() else (ROOT/candidate)
    candidate=candidate.resolve()
    if not candidate.is_file():
        raise ValueError(f'Missing claimed capture {candidate}')
    return str(candidate.relative_to(ROOT))

aliases={'SRC-0030':'SRC-0011','SRC-0032':'SRC-0012'}
source_doc=load(ROOT/'02-evidence/registers/sources.json')
sources={s['source_id']:s for s in source_doc['records']}
claims={c['claim_id']:c for c in load(ROOT/'02-evidence/registers/claims.json')['records']}
search_doc=load(ROOT/'02-evidence/registers/searches.json')
new_searches=[]
root_captures=load(ROOT/'02-evidence/captures/root-r01/capture-manifest.json')
root_capture_map={Path(c['file']).name:c for c in root_captures if c.get('status')=='saved'}

for name in ['cipp-records.json','moorepay-sdworx-records.json','wider-records.json','root-landscape-records.json']:
    batch=load(NOTES/name)
    for item in batch['sources']:
        s=dict(item)
        original_id=s['source_id']
        canonical_id=aliases.get(original_id,original_id)
        if s.get('capture_filename'):
            capture=root_capture_map.get(s['capture_filename'])
            if capture:
                s['capture_path']=capture['file'];s['capture_sha256']=capture['sha256']
        s.pop('capture_filename',None)
        s['source_id']=canonical_id
        s['audit_record_origin']=f'03-report/research-notes/{name}'
        s['capture_path']=normalise_capture(s.get('capture_path'))
        if s['capture_path']:
            digest=hashlib.sha256((ROOT/s['capture_path']).read_bytes()).hexdigest()
            if s.get('capture_sha256') and s['capture_sha256']!=digest:
                raise ValueError(f'Hash mismatch {canonical_id}')
            s['capture_sha256']=digest
        else:
            s['capture_sha256']=None
        if canonical_id in sources:
            old=sources[canonical_id]
            combined={**old,**s}
            if original_id!=canonical_id:
                combined['alias_source_ids']=sorted(set(old.get('alias_source_ids',[])+[original_id]))
                combined['initial_discovery_notes']=old.get('initial_discovery_notes',old.get('notes'))
            sources[canonical_id]=combined
        else:
            sources[canonical_id]=s
    for c0 in batch['claims']:
        c=dict(c0)
        c['source_ids']=[aliases.get(s,s) for s in c['source_ids']]
        c['audit_record_origin']=f'03-report/research-notes/{name}'
        c.setdefault('publication_status','working')
        claims[c['claim_id']]=c
    logs=batch.get('search_log',batch.get('searches',[]))
    if logs:
        if isinstance(logs,list):
            for log in logs:
                new_searches.append({'audit_record_origin':f'03-report/research-notes/{name}',**(log if isinstance(log,dict) else {'query':log})})
    elif batch.get('search_queries'):
        new_searches.append({'audit_record_origin':f'03-report/research-notes/{name}','date':'2026-10-28','queries':batch['search_queries'],'purpose':'R01 source audit'})

for c in claims.values():
    if not set(c['source_ids'])<=set(sources):
        raise ValueError(f'Unresolved claim source {c["claim_id"]}')
source_doc['records']=sorted(sources.values(),key=lambda s:s['source_id'])
source_doc['updated_on']='2026-10-28'
source_doc['deduplication_note']='Alias SRC-0030 is canonical SRC-0011; alias SRC-0032 is canonical SRC-0012. Multiple pages from one study are not independent datasets.'
save(ROOT/'02-evidence/registers/sources.json',source_doc)
save(ROOT/'02-evidence/registers/claims.json',{'schema_version':'1.0','updated_on':'2026-10-28','records':sorted(claims.values(),key=lambda c:c['claim_id'])})

known_origins={(x.get('audit_record_origin'),json.dumps(x.get('queries',x.get('query',None)),sort_keys=True)) for x in search_doc['records']}
counter=max(int(x['search_id'].split('-')[1]) for x in search_doc['records'])
for record in new_searches:
    key=(record.get('audit_record_origin'),json.dumps(record.get('queries',record.get('query',None)),sort_keys=True))
    if key in known_origins:
        continue
    counter+=1;record['search_id']=f'SCH-{counter:04d}'
    record.setdefault('date','2026-10-28')
    search_doc['records'].append(record);known_origins.add(key)
save(ROOT/'02-evidence/registers/searches.json',search_doc)

save(ROOT/'02-evidence/registers/source-aliases.json',{'schema_version':'1.0','aliases':aliases,'note':'Preserve local audit IDs; use canonical IDs in master claims.'})
print(json.dumps({'sources':len(sources),'claims':len(claims),'source_files_with_checked_hashes':sum(bool(s.get('capture_path')) for s in sources.values()),'search_records':len(search_doc['records'])}))
