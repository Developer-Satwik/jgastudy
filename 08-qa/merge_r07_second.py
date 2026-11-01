from pathlib import Path
from urllib.parse import urlsplit, urlunsplit, parse_qsl, urlencode
import hashlib, json

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / '03-report/research-notes/r07-second-check'
DATE = '2026-10-29'

def read(p): return json.loads(p.read_text())
def write(p, d):
    tmp = p.with_suffix(p.suffix + '.tmp')
    tmp.write_text(json.dumps(d, indent=2, ensure_ascii=False) + '\n')
    tmp.replace(p)
def norm(url):
    p = urlsplit(url)
    # Modern.gov document and meeting IDs are substantive, not tracking parameters.
    query = urlencode(sorted((k, v) for k, v in parse_qsl(p.query) if not k.lower().startswith('utm_')))
    return urlunsplit((p.scheme, p.netloc.lower(), p.path.rstrip('/'), query, ''))
def resolve(rel):
    p = Path(rel)
    for q in [p if p.is_absolute() else ROOT / p, ROOT.parent.parent / p]:
        if q.is_file(): return q
    raise FileNotFoundError(rel)
def local(rel): return str(resolve(rel).relative_to(ROOT)) if rel else None
def limits(c): return c.get('limitations', c.get('limits', c.get('interpretation_limits')))
def capture(c):
    x = c.get('capture', {})
    path = c.get('capture_path') or x.get('html_path') or x.get('path')
    sha = c.get('capture_sha256') or x.get('html_sha256') or x.get('sha256')
    kind = c.get('capture_kind', '')
    extracts = list(c.get('review_extracts', []))
    if c.get('parsed_extract_path'):
        extracts.append(dict(path=c['parsed_extract_path'], sha256=c['parsed_extract_sha256'], kind='selected_reader_extract'))
    if path and any(v in kind for v in ['parsed', 'extract', 'browser']):
        extracts.append(dict(path=path, sha256=sha, kind=kind)); path=sha=None
    for e in extracts:
        e['path'] = local(e['path'])
        assert hashlib.sha256(resolve(e['path']).read_bytes()).hexdigest() == e['sha256']
    return local(path), sha, extracts

sp = ROOT / '02-evidence/registers/sources.json'
cp = ROOT / '02-evidence/registers/claims.json'
ap = ROOT / '02-evidence/registers/source-aliases.json'
sources, claims, aliases = read(sp), read(cp), read(ap)
by_url = {norm(s['url']): s for s in sources['records']}
by_id = {s['source_id']: s for s in sources['records']}
next_s = max(int(s['source_id'].split('-')[1]) for s in sources['records']) + 1
next_c = max(int(c['claim_id'].split('-')[1]) for c in claims['records']) + 1
source_map, claim_map = {}, {}
added_s = added_c = 0
folders = ['history', 'market', 'competitors', 'root']

for folder in folders:
    path = BASE / folder / 'source-candidates.json'
    d = read(path)
    for c in d.get('records', d.get('new_route_candidates', [])):
        found = by_id.get(c.get('canonical_source_id')) or by_url.get(norm(c['url']))
        if found is None:
            ident = f'SRC-{next_s:04}'; next_s += 1; added_s += 1
            cap, sha, extracts = capture(c)
            found = dict(source_id=ident, title=c['title'], publisher=c['publisher'], url=c['url'],
                source_type=c['source_type'], review_status=c.get('review_status', 'relevant_original_sections_inspected'),
                accessed_on=DATE, published_date=c.get('published_date'),
                last_updated=c.get('updated_date', c.get('last_updated')), date_note=c.get('date_note'),
                document_version=c.get('document_version'), population=c.get('population'), sample_size=c.get('sample_size'),
                fieldwork_period=c.get('fieldwork_period'), method_available=c.get('method_available'),
                funding_or_commercial_interest=c.get('funding_or_commercial_interest'), capture_path=cap, capture_sha256=sha,
                review_extracts=extracts, reuse_status=c.get('reuse_status', 'Private verification; final rights and wording checks pending'),
                publication_eligibility='R07_context_final_use_pending', related_topic_ids=['R07'], notes=limits(c),
                audit_record_origin=str(path.relative_to(ROOT)), r07_second_source_candidate_id=c['candidate_id'], candidate_detail=c)
            sources['records'].append(found); by_url[norm(c['url'])] = found; by_id[ident] = found
        source_map[c['candidate_id']] = found['source_id']
        if found.get('r07_second_source_candidate_id') != c['candidate_id']:
            review = dict(date=DATE, module='R07_second_challenge', origin=str(path.relative_to(ROOT)), source_candidate_detail=c)
            if review not in found.setdefault('additional_reviews', []): found['additional_reviews'].append(review)
        for url in c.get('alias_urls', []):
            a = dict(url=url, canonical_source_id=found['source_id'], relationship='Same publication or decision context; not an independent study', reviewed_on=DATE, new_independent_dataset=False)
            if a not in aliases.setdefault('url_aliases', []): aliases['url_aliases'].append(a)
    for c in d.get('reused_canonical_sources', []):
        src = by_id[c['source_id']]
        review = dict(date=DATE, module='R07_second_challenge', origin=str(path.relative_to(ROOT)), detail=c)
        if review not in src.setdefault('additional_reviews', []): src['additional_reviews'].append(review)
        if 'R07' not in src.setdefault('related_topic_ids', []): src['related_topic_ids'].append('R07')
        if c.get('additional_alias_url'):
            a = dict(url=c['additional_alias_url'], canonical_source_id=src['source_id'], relationship='Section of the same closure report; not a new programme', reviewed_on=DATE, new_independent_dataset=False)
            if a not in aliases.setdefault('url_aliases', []): aliases['url_aliases'].append(a)

for folder in folders:
    path = BASE / folder / 'claim-candidates.json'
    for c in read(path)['records']:
        ids = list(dict.fromkeys(source_map.get(s, s) for s in c.get('canonical_source_ids', []) + c.get('source_candidate_ids', []) + c.get('source_ids', [])))
        assert ids and set(ids) <= set(by_id), (c['candidate_id'], ids)
        found = next((x for x in claims['records'] if x.get('r07_second_claim_candidate_id') == c['candidate_id']), None)
        if found is None:
            ident = f'CLM-{next_c:04}'; next_c += 1; added_c += 1
            found = dict(claim_id=ident, source_ids=ids, locator=c['locator'], claim_text=c.get('claim_text', c.get('claim')),
                evidence_class=c['evidence_class'], metric=None, value=c.get('value'), unit=c.get('unit'),
                denominator=c.get('denominator'), question_wording=c.get('question_wording'), population=c.get('population', c.get('base')),
                time_period=c.get('time_period'), support_checked=True,
                review_mode=c.get('review_mode', 'Relevant original sections inspected; source-specific capture and scope limits retained.'),
                interpretation_limits=limits(c), status=c.get('status', 'R07_second_challenge_context'), publication_status='working',
                audit_record_origin=str(path.relative_to(ROOT)), r07_second_claim_candidate_id=c['candidate_id'], candidate_detail=c)
            claims['records'].append(found)
        found['review_mode'] = c.get('review_mode', found['review_mode'])
        found['candidate_detail'] = c
        claim_map[c['candidate_id']] = found['claim_id']
        for sid in ids:
            src = by_id[sid]
            if 'R07' not in src.setdefault('related_topic_ids', []): src['related_topic_ids'].append('R07')
            review = dict(date=DATE, module='R07_second_challenge', origin=str(path.relative_to(ROOT)), locator=c['locator'])
            if review not in src.setdefault('additional_reviews', []): src['additional_reviews'].append(review)

checked = {}
def check_paths(obj):
    if isinstance(obj, list):
        for x in obj: check_paths(x)
    elif isinstance(obj, dict):
        for k, v in obj.items():
            if k == 'path' or k.endswith('_path'):
                sha = obj.get('sha256' if k == 'path' else k[:-5] + '_sha256')
                if not v or not sha: continue
                p = resolve(v)
                assert hashlib.sha256(p.read_bytes()).hexdigest() == sha, str(p)
                # Prior-study files are independently verified provenance, not
                # new payroll-market originals in this module's capture pack.
                if not p.is_relative_to(ROOT):
                    continue
                rel = str(p.relative_to(ROOT))
                kind = 'retained_original'
                # A failed raw retrieval can share metadata with a separately
                # retained, valid selected reader note. Its extract is not an
                # access-error payload and must remain an extract, never raw HTML.
                explicit_kind = obj.get('kind', obj.get('capture_kind', ''))
                if ('extract' in k or any(v in explicit_kind for v in ['reader', 'extract', 'paraphrase'])):
                    kind = 'parsed_or_selected_extract'
                elif obj.get('http_status', 200) is not None and obj.get('http_status', 200) >= 400 or 'failed' in p.name or 'blocked' in p.name:
                    kind = 'excluded_access_response'
                elif obj.get('kind') == 'published_chart_asset' or checked.get(rel, {}).get('kind') == 'published_chart_asset':
                    kind = 'published_chart_asset'
                elif p.suffix == '.png': kind = 'rendered_page'
                elif p.suffix == '.json': kind = 'internal_record'
                elif p.suffix == '.py': kind = 'internal_check_code'
                elif p.suffix == '.md': kind = 'parsed_or_selected_extract' if 'extract' in p.name else 'internal_research_note'
                elif p.suffix == '.txt': kind = 'parsed_or_selected_extract'
                # Later manifests repeat paths without HTTP metadata. They cannot
                # promote an access-error payload into substantive source evidence.
                if checked.get(rel, {}).get('kind') == 'excluded_access_response':
                    kind = 'excluded_access_response'
                checked[rel] = dict(path=rel, sha256=sha, kind=kind)
            check_paths(v)
for folder in folders:
    for path in (BASE / folder).glob('*.json'): check_paths(read(path))
for s in sources['records']:
    if s.get('capture_path'):
        assert hashlib.sha256(resolve(s['capture_path']).read_bytes()).hexdigest() == s['capture_sha256']
    else: assert not s.get('capture_sha256')
assert claim_map and source_map
for p, d in [(sp, sources), (cp, claims), (ap, aliases)]:
    d['updated_on'] = DATE; write(p, d)

searchpath = ROOT / '02-evidence/registers/searches.json'
searches = read(searchpath)
purpose = 'R07 second challenge: priority history sequencing market access skill remit prior-study and affected-user context'
if not any(x.get('purpose') == purpose for x in searches['records']):
    n = max(int(x['search_id'].split('-')[1]) for x in searches['records']) + 1
    searches['records'].append(dict(search_id=f'SCH-{n:04}', date=DATE, purpose=purpose,
        queries=['Historical priority measures and programme sequences versus repeated cross-sections or unobserved later outcomes',
                 'Actual included/configured/delivered service versus supplier future roadmap; employer/agent/client unit',
                 'All six recruitment comparator and JGA task/skills/remit context; exact prior constructed prompt and saved-text linkage',
                 'Priority beside ongoing work, dependencies, capacity, affected-user evidence and review'],
        action='Targeted second challenge of R07 with primary material and explicit canonical reuses; conditions remain selective under14core. No original fieldwork, market estimate, salary/pricing arithmetic, model rerun or external contact. Holds retained.',
        related_source_ids=sorted({s for c in claims['records'] if c.get('r07_second_claim_candidate_id') for s in c['source_ids']})))
write(searchpath, searches)
write(ROOT / '08-qa/R07-second-check-record-map.json', dict(date=DATE, source_map=source_map, claim_map=claim_map,
    new_source_routes=len({v for v in source_map.values() if by_id[v].get('r07_second_source_candidate_id')}), new_claim_records=len(claim_map), new_source_candidates=len(source_map), reused_candidate_routes=sum(not by_id[v].get('r07_second_source_candidate_id') for v in source_map.values()),
    original_JGA_participants=0, employer_forecasts=0, product_tests=0))
write(ROOT / '08-qa/R07-second-check-captures.json', dict(date=DATE, files=list(checked.values())))
print(json.dumps(dict(status='merged_for_internal_review', new_sources=added_s, new_claims=added_c,
    sources=len(sources['records']), claims=len(claims['records']), originals=sum(bool(s.get('capture_path')) for s in sources['records']),
    files_hash_checked=len(checked), source_map=source_map, claim_map=claim_map), indent=2))
