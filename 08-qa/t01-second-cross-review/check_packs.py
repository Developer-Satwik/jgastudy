from pathlib import Path
from urllib.parse import unquote
import json,hashlib,re
R=Path(__file__).resolve().parents[2];B=R/'04-table/research-notes/t01-second-check';O=R/'08-qa/t01-second-cross-review';checks=[]
def rd(p):return json.loads(p.read_text())
def ck(v,n):checks.append(dict(name=n,passed=bool(v)));assert v,n
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
sources={x['source_id']:x for x in rd(B/'before-review/sources.json')['records']};new={};cs=[]
for folder in ['history','market','root']:
 d=rd(B/folder/'source-candidates.json')
 for s in d['records']:
  ck(s['candidate_id'] not in new,'new candidate unique '+s['candidate_id']);new[s['candidate_id']]=s
  if s.get('capture_path'):
   ck((R/s['capture_path']).is_file(),'raw retained '+s['candidate_id']);ck(h(R/s['capture_path'])==s['capture_sha256'],'raw hash '+s['candidate_id'])
  else:ck(not s.get('capture_sha256') and bool(s.get('review_extracts')),'extract-only provenance '+s['candidate_id'])
  for e in s.get('review_extracts',[]):ck(h(R/e['path'])==e['sha256'],'separate extract hash '+s['candidate_id'])
  if s.get('parsed_extract_path'):ck(h(R/s['parsed_extract_path'])==s['parsed_extract_sha256'],'root separate parsed hash '+s['candidate_id'])
 for s in d.get('reused_canonical_sources',[]):
  ck(s['source_id'] in sources,'canonical reuse resolves '+folder+' '+s['source_id'])
  if s.get('capture_path'):ck(h(R/s['capture_path'])==s['capture_sha256'],'reinspected raw hash '+s['source_id'])
  if s.get('parsed_path'):ck(h(R/s['parsed_path'])==s['parsed_sha256'],'reinspected parsed hash '+s['source_id'])
 cs+=rd(B/folder/'claim-candidates.json')['records']
ck(len(new)==6,'six new primary routes across other-author packs')
ck(len({x['candidate_id'] for x in cs})==len(cs),'other-author claim IDs unique')
for c in cs:
 ck(set(c.get('canonical_source_ids',[]))<=set(sources),'claim canonical sources '+c['candidate_id'])
 ck(set(c.get('source_candidate_ids',[]))<=set(new),'claim new sources '+c['candidate_id'])
 ck(bool(c['locator']) and bool(c['limitations']),'claim scoped locator and limits '+c['candidate_id'])
 ck(c.get('value') is None and c.get('unit') is None and c.get('denominator') is None,'no numerical outcome/forecast '+c['candidate_id'])
by={x['candidate_id']:x for x in cs}
ch=(B/'root/captures/T1R2-S01-selected-reader.md').read_text()
ck('not original HTML' in ch and 'selected paraphrase' in ch,'Chatham notes not promoted to raw export')
ck('current FAQ' in ch and 'AI note-taking/transcription' in ch and 'Parts may be designated' in ch,'named-Rule meeting-mode scope retained')
ck('meeting adopting' in by['T1R2-C01']['limitations'] and 'not a universal interview restriction' in by['T1R2-C01']['limitations'],'named Rule not every interview or universal law')
ck('employer-specific' in by['T1R2-C03']['evidence_class'] or 'employer' in by['T1R2-C03']['evidence_class'],'hospitality example bounded to employer')
ck('not a rule for all' in by['T1R2-C03']['limitations'],'hospitality policy not generalised')
his=(B/'history/HISTORICAL-AND-MEMBER-LIFECYCLE-CHECK.md').read_text()
ck('not proof of a present formal agreement' in his and 'moderator role' in his,'Nick public role not formal partnership/access')
ck('not a measured event-to-community conversion' in by['T1H-C01']['claim_text'],'format history not causal conversion')
ck('No evidence' in by['T1H-C01']['limitations'],'same-person participation/retention not inferred')
ck('withdrawn' in rd(B/'history/claim-candidates.json')['deduplication_note'],'duplicate history renewal claim withdrawn')
# Exact factual source-support segment checks complement direct reading.
ht=(B/'history/captures/T1H-S02.txt').read_text()
for term in ['October 9, 2026','in May','sponsored by Strada','Nick Day','moderated a panel']:ck(term in ht,'Summit retained original segment '+term)
arc=(B/'history/captures/T1H-S01.txt').read_text()
for term in ['October 2026','July 2025','Recent Issues']:ck(term in arc,'CPO archive listed output '+term)
tpc=(B/'market/captures/SRC-0239.parsed.txt').read_text()
for term in ['automatically renew','reminder approximately','9.3.3','9.5.1']:ck(term in tpc,'TPC renewal and access lifecycle '+term)
ip=(B/'market/captures/T1M-S01.parsed.txt').read_text()
for term in ['Individual membership','Corporate membership','Corporate Overseas (EU)','Corporate Overseas (Non-EU)','billed annually']:ck(term in ip,'IPASS segmented offer '+term)
ck('price benchmark' in by['T1M-C01']['limitations'],'IPASS no unlike price anchor')
gpa=(B/'market/captures/T1M-S02.parsed.txt').read_text()
for term in ['global and in-country','Forum','Help Desk (annual service)']:ck(term in gpa,'GPA alternative catalogue '+term)
market=rd(B/'market/selective-conditions.json')
ck(len(market['conditions'])==4 and market['extra_mandatory_questions']==0 and not market['commercial_validation'],'four selective market conditions no new questions')
for c in market['conditions']:ck(not c['mandatory'] and not c['scored'] and not c['validated'] and c['actual_application'] is None,'market condition not fieldwork '+c['condition_id'])
for n in ['05-analysis/observations.json','05-analysis/charts.json','04-table/financial-inputs.json']:ck(rd(R/n)['records']==[],'actual array remains empty '+n)
# Only the three other-author memos, not my own competitor synthesis.
for f,n in [('history','HISTORICAL-AND-MEMBER-LIFECYCLE-CHECK.md'),('market','MARKET-CHALLENGE.md'),('root','PARTICIPATION-AND-OUTPUT-MODES.md')]:
 p=B/f/n
 for u in re.findall(r'\]\(([^)]+)\)',p.read_text()):
  if not u.startswith(('http://','https://','#')):ck((p.parent/unquote(u.split('#',1)[0])).resolve().exists(),'other-author memo link '+f+' '+u)
result=dict(status='passed_other_author_packs_integration_pending',date='2026-10-30',scope='History, market and root packs only; competitor pack is reviewer-authored and excluded from this independent claim.',checks=checks,check_count=len(checks),manual_primary_support_review=['CPO origin/archive/forum and Summit retrospective paragraphs','TPC renewal, benefit, member organisation and materials clauses','IPASS segment and country/VAT branch descriptions; no values adopted','GPA resource catalogue','ISG enterprise/provider public offer purpose distinction','iVentiv FAQ/package/payment scope','Chatham House originator definition and current FAQ freshly reopened independently','Planning Inspectorate specific hospitality policy freshly reopened independently'],open_substantive_source_issues=[],integration_design_item='Preserve original free-practitioner research benefit; do not model equivalent employer access as an automatic additional paid licence. Test incremental service/use/entitlement; no new restriction is adopted.',raw_and_reader_distinction_preserved=True,fieldwork=False,commercial_validation=False)
(O/'checks.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n');print(json.dumps({k:v for k,v in result.items() if k not in ['checks','manual_primary_support_review']},indent=2))
