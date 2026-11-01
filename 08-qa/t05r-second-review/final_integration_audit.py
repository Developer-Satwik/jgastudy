"""Independent, read-only T05R second-challenge verification.

Writes only the final review artifacts in this directory. Manual source and
semantic review is recorded explicitly rather than represented as a parser test.
"""
from pathlib import Path
import hashlib
import json
import math
import re
from collections import Counter

PROJECT = Path(__file__).resolve().parents[2]
WORKSPACE = PROJECT.parents[1]
OUT = Path(__file__).resolve().parent

def read(path):
    return json.loads((PROJECT / path).read_text())

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def text_sha(value):
    return hashlib.sha256(value.encode()).hexdigest()

checks = []
def passed(check_id, name, detail):
    checks.append({"check_id": check_id, "name": name, "passed": True, "detail": detail})

baseline_path = "08-qa/T05R-second-check-baseline.json"
baseline = read(baseline_path)
assert len(baseline["files"]) == 265
for entry in baseline["files"]:
    path = Path(entry["path"])
    if not path.is_absolute():
        path = PROJECT / path
    assert sha(path) == entry["sha256"], path
passed("IR01", "Protected first-component artifacts", "All 265 protected artifact hashes match the pre-second-check baseline, including the original workbook and its supporting files.")

snap_path = "04-table/research-notes/t05r-second-check/before-review/manifest.json"
snap = read(snap_path)
assert len(snap["records"]) == 13
for entry in snap["records"]:
    assert sha(PROJECT / entry["snapshot_path"]) == entry["sha256"], entry["snapshot_path"]
passed("IR02", "Pre-change snapshots", "All thirteen retained pre-change snapshots match their original manifest hashes. Mutable live controls are not final-hash dependencies.")

old_sources = read("04-table/research-notes/t05r-second-check/before-review/02-evidence/registers/sources.json")["records"]
sources = read("02-evidence/registers/sources.json")["records"]
old_claims = read("04-table/research-notes/t05r-second-check/before-review/02-evidence/registers/claims.json")["records"]
claims = read("02-evidence/registers/claims.json")["records"]
assert len(old_sources) == 235 and len(sources) == 242
assert len(old_claims) == 466 and len(claims) == 484
assert claims[:466] == old_claims
new_sources = {entry["source_id"]: entry for entry in sources}
for old in old_sources:
    new = new_sources[old["source_id"]]
    assert {k:v for k,v in old.items() if k not in {"additional_reviews", "related_topic_ids"}} == {k:v for k,v in new.items() if k not in {"additional_reviews", "related_topic_ids"}}
    for key in ("additional_reviews", "related_topic_ids"):
        assert new.get(key, [])[:len(old.get(key, []))] == old.get(key, [])
passed("IR03", "Canonical evidence lineage", "The 235 prior source bases and 466 prior claims are preserved. Reused-route context was appended separately; totals are 242 sources and 484 claims.")

record_map_path = "08-qa/T05R-second-check-record-map.json"
record_map = read(record_map_path)
assert len(record_map["source_map"]) == 7 and len(record_map["claim_map"]) == 18
assert set(record_map["source_map"].values()) == {f"SRC-{i:04}" for i in range(268, 275)}
assert set(record_map["claim_map"].values()) == {f"CLM-{i:04}" for i in range(557, 575)}
canonical_claims = {entry["claim_id"]: entry for entry in claims}
candidate_count = 0
for pack in ("history-market", "competitors", "root"):
    for candidate in read(f"04-table/research-notes/t05r-second-check/{pack}/claim-candidates.json")["records"]:
        canonical = canonical_claims[record_map["claim_map"][candidate["candidate_id"]]]
        assert canonical["claim_text"] == candidate["claim_text"]
        assert canonical["interpretation_limits"] == candidate["limitations"]
        candidate_count += 1
assert candidate_count == 18
passed("IR04", "Seven routes and eighteen bounded records", "The candidate-to-canonical map reconciles exactly. All eighteen claim texts and interpretation limits match the inspected candidate records; they are not eighteen new empirical datasets.")

financial_path = "04-table/financial-inputs.json"
financial = read(financial_path)
findings_path = "05-analysis/findings.json"
assert len(financial["records"]) == 33
assert sha(PROJECT / financial_path) == "acf688c2ac540f32ec63c06e15b7b4077159d89c3b94799b2fd95e8a7de43509"
assert (PROJECT / findings_path).read_bytes() == (PROJECT / "04-table/research-notes/t05r-second-check/before-review/05-analysis/findings.json").read_bytes()
assert len(read(findings_path)["records"]) == 81
passed("IR05", "Financial inputs and findings", "All 33 first-component financial inputs and all 81 findings are unchanged. No new price, workload input or saving was adopted.")

capture_path = "08-qa/T05R-second-check-captures.json"
captures = read(capture_path)
assert len(captures["records"]) == 22
for entry in captures["records"]:
    assert sha(PROJECT / entry["path"]) == entry["sha256"], entry["path"]
assert dict(Counter(entry["kind"] for entry in captures["records"])) == captures["counts_by_kind"]
assert sum(entry["kind"] == "retained_original_html" and entry["scope"] == "new_route" for entry in captures["records"]) == 4
assert sum(entry["kind"] == "retained_original_html" and entry["scope"] == "reused_canonical_route" for entry in captures["records"]) == 3
assert sum(entry["kind"] == "browser_reader_extract" for entry in captures["records"]) == 3
for source_id in ("SRC-0269", "SRC-0271", "SRC-0272"):
    assert new_sources[source_id]["capture_path"] is None
hays = next(entry for entry in captures["records"] if entry["source_id"] == "SRC-0192")
assert hays["access_for_this_review"] == "prior_context_reused"
assert "inherited" in captures["note"]
passed("IR06", "Capture integrity and access classifications", "All 22 indexed hashes match. Four new-route originals, three fresh originals on reused routes and three new browser reader extracts remain distinct. Failed HTTP bodies are not originals. Hays is expressly prior context for this review.")

passed("IR07", "Historical source interpretation", "Independently reread the retained CIEP archive rows, ProCopywriters retrospective extract and YunoJuno release sections. The readout preserves minimum/mean/median and role/discipline distinctions; it infers neither a like-for-like decline nor automatic 2027 inflation.")
passed("IR08", "Other-market and fee interpretation", "Independently reread the two retained Upwork extracts. The worldwide USD range is not an Indian quote or GBP budget. Conditional client fees are not adopted as universal charges or actual account terms.")
passed("IR09", "Method and assisted-process interpretation", "Independently reread the retained Camden and QUADRA-AI primary sections. Public-health planning is a scoped analogy; the planned July 2026 to March 2027 project is not measured JGA productivity, available tooling or a permitted data-processing instruction.")

first_map_path = "04-table/T05-research-cost-map.json"
first_map = read(first_map_path)
inputs = {entry["input_id"]: entry for entry in financial["records"]}
assert len(first_map["tasks"]) == 21
task_ids = {entry["workload_id"] for entry in first_map["tasks"]}
assert len([t for t in first_map["tasks"] if t["workload_id"].startswith("WR")]) == 16
assert len([t for t in first_map["tasks"] if t["workload_id"].startswith("JG")]) == 5
role_hours = Counter()
jga_hours = 0
for task in first_map["tasks"]:
    value = inputs[task["hours_input_id"]]["value"]
    multiplier = inputs[first_map["contributor_scenarios_input_id"]]["value"]["base"] if task["unit_basis"] == "per_usable_contributor" else 1
    hours = value["base"] * multiplier
    if task["workload_id"].startswith("WR"):
        role_hours[task["role_group"]] += hours
    else:
        jga_hours += hours
cases_path = "04-table/research-notes/t05r-second-check/root/constructed-cost-applications.json"
constructed = read(cases_path)
case = {entry["test_id"]: entry for entry in constructed["cases"]}
assert len(case) == 10
assert dict(role_hours) == constructed["role_hours"] and sum(role_hours.values()) == 174 and jga_hours == 23
day_rates = {"Research": 372, "Writing": 440, "Design": 348}
hour_rates = {"Editing": 37.11, "Coordination": 46.19}
def reference(day_hours):
    return sum(role_hours[role] * rate / day_hours for role,rate in day_rates.items()) + sum(role_hours[role] * rate for role,rate in hour_rates.items())
assert math.isclose(reference(7.5), 8726.14, abs_tol=1e-8)
for test_id, day in (("SC02", 7), ("SC03", 8)):
    assert math.isclose(reference(day), case[test_id]["result"]["provider_reference_value_GBP"], abs_tol=1e-8)
passed("IR10", "Role totals and day normalisation", "Independent reconstruction from the preserved inputs gives 174 provider hours, 23 JGA hours and GBP 8,726.14. Seven- and eight-hour day normalisations give GBP 9,270.14 and GBP 8,250.14; they change valuation, not required work or observed supplier terms.")

whole_days = sum(math.ceil(role_hours[role] / 7.5) * rate for role,rate in day_rates.items()) + sum(role_hours[role] * rate for role,rate in hour_rates.items())
assert math.isclose(whole_days, case["SC04"]["result"]["illustrative_value_GBP"], abs_tol=1e-8)
assert math.isclose(whole_days - reference(7.5), 464, abs_tol=1e-8)
passed("IR11", "Whole-role booking illustration", "The role-pooled whole-day illustration correctly gives GBP 9,190.14, GBP 464 above the normalised reference. It is explicitly hypothetical, is not task-by-task rounding, and is not an adopted supplier policy.")

extra = 5 * .5 * 46.19
reuse = -4 * 440 / 7.5 + 3 * 372 / 7.5
assert math.isclose(extra, case["SC05"]["result"]["extra_reference_value_GBP"], abs_tol=1e-8)
assert math.isclose(reference(7.5) + extra, case["SC05"]["result"]["illustrative_provider_total_GBP"], abs_tol=1e-8)
assert math.isclose(reuse, case["SC06"]["result"]["net_reference_value_change_GBP"], abs_tol=1e-8)
assert math.isclose(reference(7.5) + reuse, case["SC06"]["result"]["illustrative_provider_total_GBP"], abs_tol=1e-8)
passed("IR12", "Additional-work and reuse illustrations", "The two constructed incremental examples recalculate correctly. Extra unsuccessful contacts are work events, not a conversion rate. Reuse exchanges writing for receiving review; no verified saving or contributor-count change is claimed.")

assert case["SC07"]["result"]["JGA_value"] is None and case["SC07"]["result"]["combined_value"] is None
assert case["SC08"]["result"]["adopted_Indian_hourly_rate"] is None
assert case["SC08"]["result"]["GBP_replacement_cost"] is None
assert case["SC09"]["result"]["adopted_automation_saving_percent"] is None
assert case["SC09"]["result"]["hours_removed"] == 0
assert case["SC10"]["result"]["converted_fee_GBP"] is None
assert case["SC10"]["result"]["added_to_future_labour_value"] is False
assert constructed["actual_workbook_edits"] == constructed["new_financial_inputs"] == constructed["actual_quote_or_hire"] == 0
passed("IR13", "Remaining constructed-case boundaries", "Cases SC07 to SC10 preserve unknown JGA resource costs, no geographic price substitution, no unverified AI saving and no implicit conversion or addition of the current report fee to future labour. All ten cases remain read-only analyst applications.")

comparator_path = "04-table/research-notes/t05r-second-check/competitors/comparator-map.json"
comparator = read(comparator_path)
assert comparator["recruitment_comparators"] == 6 and comparator["JGA_contexts"] == 1
assert len(comparator["records"]) == 7
assert comparator["no_competitor_cost_comparison"] and comparator["no_demand_or_capacity_validation"]
for entry in comparator["records"]:
    assert not entry["actual_supplier_quote"] and not entry["actual_participant"] and not entry["labour_saving_quantified"]
passed("IR14", "Recruiter and JGA comparisons", "All six specified recruiters and JGA have source-specific formats and access boundaries. Their public assets do not establish equivalent study costs, capacity, permissioned new contributions or automatic production savings.")

bridge_path = "04-table/research-notes/t05r-second-check/competitors/prior-study-bridge.json"
bridge = read(bridge_path)
original_indices = []
for entry in bridge["provenance"]:
    path = WORKSPACE / entry["path"]
    assert sha(path) == entry["sha256"]
    data = json.loads(path.read_text())
    rows = data["answers"] if isinstance(data, dict) else data
    original_indices.append({row["id"]: row for row in rows})
count = 0
for question in bridge["questions"]:
    assert text_sha(question["prompt"]) == question["prompt_sha256"]
    for entry in question["answer_links"]:
        for index in original_indices:
            row = index[entry["answer_id"]]
            assert row["prompt"] == question["prompt"]
            assert text_sha(row["prompt"]) == entry["prompt_sha256"]
            assert text_sha(row["fullAnswer"]) == entry["full_answer_sha256"]
        count += 1
assert count == 24 and bridge["question_count"] == 3
assert bridge["no_model_reruns"] and not bridge["actual_buyer_evidence"]
passed("IR15", "Earlier-study exact lineage", "The two original provenance hashes and all 24 linked prompt/full-answer texts reconcile for the three authored questions. These are saved model answers, with no rerun or transfer of recommendation counts into demand evidence.")
passed("IR16", "Selected semantic rereads", "The three ChatGPT first-run texts were independently reread during this review sequence. S04 generated scorecard weights are not observed buyer criteria; S07 public specialism is not delivery proof; S11 London was added by the answer rather than the prompt. The integrated readout preserves these distinctions.")

map_path = "04-table/T05R-second-challenge-map.json"
integrated_map = read(map_path)
assert integrated_map["date"] == "2026-11-01" and integrated_map["source_collection_date"] == "2026-10-31"
assert integrated_map["status"] == "second_challenge_reviewed_internal_design"
assert len(integrated_map["conditions"]) == 5
assert set(integrated_map["source_ids"]) == set(record_map["source_map"].values())
assert set(integrated_map["claim_ids"]) == set(record_map["claim_map"].values())
for condition in integrated_map["conditions"]:
    assert set(condition["source_ids"]).issubset(new_sources)
    assert set(condition["claim_ids"]).issubset(canonical_claims)
    assert set(condition["related_workload_ids"]).issubset(task_ids)
assert not integrated_map["financial_inputs_changed"] and not integrated_map["workbook_changed"]
assert integrated_map["new_financial_inputs"] == 0
assert integrated_map["fourteen_core_questions_unchanged"]
assert integrated_map["practitioner_free_full_research_preserved"]
assert not integrated_map["new_case_or_geography_quota"]
assert not integrated_map["current_contract_fee_changed"]
for key in ("actual_quotes", "actual_suppliers", "actual_staffing", "actual_participants", "actual_buyer_member_validation", "external_actions"):
    assert integrated_map[key] == []
assert not integrated_map["full_financial_model_complete"]
assert sha(Path(integrated_map["original_workbook_path"])) == integrated_map["original_workbook_sha256"]
passed("IR17", "Five conditions and canonical task map", "The final map has valid canonical source, claim and preserved task references. Its five conditions are selective costing refinements, not new mandatory participant questions, case/geography quotas, contract terms or a completed programme budget.")

readout_path = "04-table/T05R-SECOND-CHECK-READOUT.md"
refinements_path = "04-table/T05R-COST-AND-DELIVERY-REFINEMENTS.md"
readout = (PROJECT / readout_path).read_text()
refinements = (PROJECT / refinements_path).read_text()
assert "1 November 2026" in readout and "31 October" in readout
assert "fourteen core research questions remain unchanged" in readout
assert "full financial model and final report integration remain open" in readout
assert "No route is selected" in refinements and "USD1,500 agreement" in refinements
for file_path, value in ((readout_path, readout), (refinements_path, refinements)):
    for target in re.findall(r"\]\(([^)]+)\)", value):
        if re.match(r"[a-z]+://", target):
            continue
        assert ((PROJECT / file_path).parent / target.split("#")[0]).exists(), target
passed("IR18", "Integrated readout and implementation note", "Both final texts were read in full and their local links resolve. They lead with useful findings, distinguish source facts from applications and constructed arithmetic, preserve the first component, and identify the next incomplete cost work without claiming field validation.")

passed("IR19", "Contract and collection boundaries", "The integrated materials preserve the 14-question guide, six-to-ten usable practitioner target, distinct-person versus up-to-four Table contribution-event counting, free practitioner full research and existing ordinary delivery/correction duties. No external message, quote, hire, booking, participant data processing or client-file change is reported or performed by this review.")

review_md = """# Independent integrated review: T05R second challenge

1 November 2026. Internal review of the frozen research/staffing second-check materials.

The integrated review passes for its stated design scope. No substantive issue requiring a change to the original research/staffing workbook was found. The original workbook, its 33 financial inputs and 81 findings remain preserved.

The readout, refinement note and structured map correctly develop five practical conditions for later costing: matching rate definitions; specifying scope and billing units; counting additional work once; identifying exact reusable assets and remaining work; and verifying assisted processes before crediting savings.

The review rechecked the seven added source routes and eighteen bounded records, all indexed capture hashes, the preserved evidence prefix and ten constructed applications. Four new-route original HTML captures, three browser reader extracts and three fresh originals from reused routes remain separately classified. Prior notes are not promoted to fresh original sources. Hays is explicitly prior context in this pass.

Independent arithmetic confirms GBP 8,726.14 for the original working reference, GBP 9,270.14 at a seven-hour normalised day, GBP 8,250.14 at eight hours, and GBP 9,190.14 for the hypothetical whole-role-day booking case. The last is GBP 464 above the reference. These are explanatory cases, not supplier offers, price forecasts or adopted new inputs. Unknown JGA resource rates remain unknown.

The six recruiter comparisons and JGA context concern public assets and distinct delivery units. Their existence does not establish reuse rights, new permissioned contributors, available capacity or savings. Exact lineage was rechecked for three earlier-study questions and 24 saved answers against both original indices. The three selected semantic rereads preserve the distinction between authored questions, generated advice and real buyer evidence.

The current contract fee, 14 core questions, six-to-ten usable contributor target, up-to-four Table contribution-event boundary and free full research benefit are unchanged. No quote, participant, market validation, production saving, hire or external action was established. This passes an internal desktop design challenge only; it does not complete the full T05 financial model or final report integration.

The machine-readable review contains the exact hashes of the reviewed frozen artifacts. Mutable live controls and the validator are intentionally excluded from that final hash list. The earlier retained pre-change snapshots remain checked against their own manifest.
"""
(OUT / "INTEGRATED-REVIEW.md").write_text(review_md)

artifact_paths = {
    baseline_path, snap_path, financial_path, findings_path, first_map_path,
    record_map_path, capture_path, map_path, readout_path, refinements_path,
    cases_path, comparator_path, bridge_path,
    "08-qa/t05r-second-review/nov01-independent-checks.json",
    "08-qa/t05r-second-review/prior-bridge-lineage-checks.json",
    "08-qa/t05r-second-review/preliminary-source-and-model-review.json",
    "08-qa/t05r-second-review/INTEGRATED-REVIEW.md",
    "08-qa/t05r-second-review/final_integration_audit.py",
}
for pack in ("history-market", "competitors", "root"):
    pack_dir = PROJECT / "04-table/research-notes/t05r-second-check" / pack
    for path in pack_dir.rglob("*"):
        if path.is_file():
            artifact_paths.add(path.relative_to(PROJECT).as_posix())
for entry in captures["records"]:
    artifact_paths.add(entry["path"])
artifact_paths.add(integrated_map["original_workbook_path"])
for entry in bridge["provenance"]:
    artifact_paths.add(str(WORKSPACE / entry["path"]))
reviewed = []
for path_str in sorted(artifact_paths):
    path = Path(path_str)
    resolved = path if path.is_absolute() else PROJECT / path
    reviewed.append({"path": path_str, "sha256": sha(resolved)})

result = {
    "date": "2026-11-01",
    "source_collection_date": "2026-10-31",
    "status": "passed_for_internal_T05R_second_challenge",
    "review_scope": "Independent review of the frozen second desktop challenge to the first T05 research/staffing component. Not completion of T05 or actual supplier, workload, participant, customer or market validation.",
    "checks": checks,
    "reviewed_artifacts": reviewed,
    "open_substantive_issues": [],
    "original_workbook_edit_needed": False,
    "original_workbook_preserved": True,
    "financial_inputs_unchanged": True,
    "findings_preserved": True,
    "canonical_source_records": 242,
    "canonical_claim_records": 484,
    "new_source_routes": 7,
    "new_bounded_claim_records": 18,
    "findings": 81,
    "financial_inputs": 33,
    "protected_files_checked": 265,
    "pre_change_snapshots_checked": 13,
    "constructed_cases_checked": 10,
    "saved_answer_lineage_checked": 24,
    "selected_semantic_rereads": ["S04-C-chatgpt-r1", "S07-C-chatgpt-r1", "S11-C-chatgpt-r1"],
    "fourteen_core_questions_unchanged": True,
    "current_contract_fee_changed": False,
    "practitioner_free_full_research_preserved": True,
    "actual_validation": False,
    "actual_fieldwork": False,
    "full_financial_model_complete": False,
    "external_actions": [],
    "mutable_live_controls_and_validator_excluded_from_hashes": True,
    "conclusion": "The original named UK-contractor reference remains intact. Five bounded refinements improve the next cost step. No new rate, cost input, geographic discount, automation saving or procurement decision is adopted."
}
(OUT / "integration-checks.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps({"status": result["status"], "checks": len(checks), "reviewed_artifacts": len(reviewed), "open_substantive_issues": [], "write_scope": str(OUT)}, indent=2))
