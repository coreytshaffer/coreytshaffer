"""Validate the Philosophical Council planning artifacts.

This is validation tooling for a planning milestone. It checks documents and
data; it is not, and does not test, any council implementation.

It runs every structural and semantic rule that can be decided mechanically,
then applies each negative control in negative_controls.json to an in-memory
copy of the files and confirms that the rules still detect the fault that
control injects. No file on disk is modified.

Passing establishes only that the files satisfy these rules. It does not
establish that the answer keys are correct (that needs a human second reader),
that free text is free of overreach (that needs human scoring), or anything
about how critics would behave. See validation/README.md.

Usage:
    python3 research/philosophical-council/validation/validate.py [--root DIR]

Exit status: 0 when every rule passes and every negative control is detected;
1 on any rule failure, any rule that could not run, any missed or invalid
negative control, or any rule without a negative control; 2 on usage errors.
"""

import argparse
import hashlib
import importlib.metadata
import json
import posixpath
import re
import sys
from pathlib import Path

try:
    import jsonschema
except ImportError:  # schema rules are then reported as not run, and the run fails
    jsonschema = None

VALIDATOR_VERSION = "pc-validate 0.2"

RULES = {
    "F01": "Data files (JSON and SHA256SUMS) contain only ASCII bytes",
    "F02": "Files use LF line endings and end with a newline",
    "F03": "JSON files parse",
    "F04": "JSON objects have no duplicate keys",
    "SCH01": "Schema files are the expected set and are valid JSON Schema Draft 2020-12",
    "FX01": "Case packets conform to pc-case/0.1",
    "FX02": "Answer keys conform to pc-expectation/0.2",
    "FX03": "index.json lists exactly the case and answer-key files present, with matching categories, existing pinned documents and the canary",
    "FX04": "File names, case IDs and index entries agree",
    "FX05": "Case packets contain no answer-key fields and no canary text",
    "FX06": "Case titles contain no category words",
    "FX07": "Subject segments run A1..An without gaps",
    "FX08": "Evidence segments are numbered per source without gaps, and segment IDs are unique",
    "FX09": "Declared lineage names existing sources and is acyclic",
    "FX10": "assistant_had_access_to names existing sources",
    "FX11": "Transformation records name existing items, and each output declares its sources in derived_from",
    "FX12": "Every case has an answer key and every answer key a case",
    "FX13": "expected_support_assessment is among the acceptable assessments",
    "FX14": "Benign controls plant nothing and expect no material defect; every other case plants a primary item",
    "FX15": "Answer-key item IDs carry their case prefix and are unique",
    "FX16": "Every locus named in an answer key exists in its case",
    "FX17": "Every inferable_from quotation is an exact substring of its segment",
    "FX18": "Disagreement and transformation expectations appear exactly for their categories and name existing transformations",
    "FX19": "Each of the six categories appears exactly once",
    "FX20": "The fixtures README carries the canary",
    "EX01": "Example case packets conform to pc-case/0.1",
    "V0": "Records conform to pc-eer/0.2",
    "V1": "packet.sha256 equals the SHA-256 of the packet bytes, and case IDs agree",
    "V2": "packet_hash_consistent matches the reviewers' packet hashes",
    "V3": "Reviewer and finding IDs are unique and every reference resolves",
    "V4": "Each valid reviewer has exactly one assessment",
    "V5": "Quotation source_verification matches a byte-exact substring check, and integrity lists flagged findings truthfully",
    "V6": "Findings citing segments absent from the packet are listed in integrity.unknown_segment_finding_ids",
    "V7": "Positions plus dropped positions partition the reviewer assessments; none dropped by mechanical synthesis",
    "V8": "Disagreements reference listed positions, and differing positions are covered by an open disagreement",
    "V9": "segment_attention is the projection of the findings, with correct independence classes",
    "V10": "lineage.declared mirrors the packet's derived_from metadata and its roots",
    "V11": "lineage.transformations mirrors the packet's transformation records",
    "V12": "Every reviewer submitted before synthesis; single_reviewer has exactly one reviewer",
    "V13": "Study records: the condition matches the reviewers and the synthesis method",
    "PIN01": "Every SHA256SUMS entry is well formed, exists and matches the file bytes",
    "PIN02": "SHA256SUMS pins every case, answer key, the index and every pinned document, once each",
}

SCHEMA_FILES = {
    "case": "schemas/pc-case-0.1.schema.json",
    "expectation": "schemas/pc-expectation-0.2.schema.json",
    "eer": "schemas/pc-eer-0.2.schema.json",
}
SCHEMA_RULES = {"case": ["FX01", "EX01"], "expectation": ["FX02"], "eer": ["V0"]}

LOAD_PATTERNS = (
    "schemas/*.json",
    "fixtures/cases/*.json",
    "fixtures/expectations/*.json",
    "fixtures/index.json",
    "fixtures/README.md",
    "fixtures/SHA256SUMS",
    "examples/*.json",
    "study-protocol.md",
    "epistemic-evaluation-record.md",
    "validation/validate.py",
    "validation/negative_controls.json",
)

CATEGORIES = (
    "conceptual_error",
    "false_corroboration",
    "missing_evidence",
    "legitimate_disagreement",
    "transformed_context",
    "benign_control",
)
CATEGORY_WORDS = re.compile(r"conceptual|corroborat|missing|disagree|transform|benign|control|error|false|fallac|planted|trap|expected", re.I)
ANSWER_KEY_FIELDS = {"expected", "planted", "traps", "category", "canary", "acceptable", "notes", "author_only_knowledge"}
CANARY = re.compile(r"canary GUID [0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}")
PIN_LINE = re.compile(r"([0-9a-f]{64}) [ *](\S.*)")
OPERATORS = {"O1", "O2", "O3", "O4", "O5", "O6"}


class Report:
    """Failures, rules that could not run, and rules that do not apply, per rule ID."""

    def __init__(self):
        self.failures = {}
        self.not_run = {}
        self.not_applicable = {}
        self.study_records = 0

    def fail(self, rule, path, message):
        self.failures.setdefault(rule, set()).add((path, message))

    def skip(self, rules, reason):
        for rule in rules:
            self.not_run.setdefault(rule, reason)

    def status(self, rule):
        if rule in self.failures:
            return "FAIL"
        if rule in self.not_run:
            return "NOT RUN"
        if rule in self.not_applicable:
            return "N/A"
        return "PASS"


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def load_tree(root):
    files = {}
    for pattern in LOAD_PATTERNS:
        for path in sorted(root.glob(pattern)):
            if path.is_file():
                files[path.relative_to(root).as_posix()] = path.read_bytes()
    return files


def parse_json_files(files, report):
    parsed = {}
    for path in sorted(p for p in files if p.endswith(".json")):
        dupes = []

        def keep_pairs(pairs, dupes=dupes):
            seen = set()
            for key, _ in pairs:
                if key in seen:
                    dupes.append(key)
                seen.add(key)
            return dict(pairs)

        try:
            doc = json.loads(files[path].decode("utf-8"), object_pairs_hook=keep_pairs)
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            report.fail("F03", path, f"does not parse: {exc}")
            continue
        if dupes:
            report.fail("F04", path, "duplicate keys: " + ", ".join(sorted(set(dupes))))
        parsed[path] = doc
    return parsed


def check_bytes(files, report):
    for path, raw in sorted(files.items()):
        if (path.endswith(".json") or path.endswith("SHA256SUMS")) and any(b > 0x7F for b in raw):
            report.fail("F01", path, "contains non-ASCII bytes")
        if b"\r" in raw:
            report.fail("F02", path, "contains CR bytes")
        if raw and not raw.endswith(b"\n"):
            report.fail("F02", path, "does not end with a newline")


def load_validators(files, parsed, report):
    if jsonschema is None:
        report.skip(["SCH01", "FX01", "FX02", "EX01", "V0"], "jsonschema is not installed")
        return {}
    for path in sorted(p for p in files if p.startswith("schemas/")):
        if path not in SCHEMA_FILES.values():
            report.fail("SCH01", path, "unexpected schema file; a superseded revision should not remain in schemas/")
    validators = {}
    for name, path in SCHEMA_FILES.items():
        doc = parsed.get(path)
        if doc is None:
            report.fail("SCH01", path, "missing or does not parse")
            report.skip(SCHEMA_RULES[name], f"{path} unavailable")
            continue
        try:
            jsonschema.Draft202012Validator.check_schema(doc)
        except jsonschema.exceptions.SchemaError as exc:
            report.fail("SCH01", path, f"not a valid Draft 2020-12 schema: {exc.message}")
            report.skip(SCHEMA_RULES[name], f"{path} is not a valid schema")
            continue
        validators[name] = jsonschema.Draft202012Validator(doc)
    return validators


def schema_check(validators, name, rule, path, doc, report):
    validator = validators.get(name)
    if validator is None:
        return
    errors = sorted(("/" + "/".join(str(p) for p in e.absolute_path), e.message) for e in validator.iter_errors(doc))
    for pointer, message in errors:
        report.fail(rule, path, f"at {pointer}: {message}")


def walk_keys(obj):
    if isinstance(obj, dict):
        for key, value in obj.items():
            yield key
            yield from walk_keys(value)
    elif isinstance(obj, list):
        for value in obj:
            yield from walk_keys(value)


def case_segments(case):
    segments = {}
    for seg in case.get("subject", {}).get("segments", []):
        segments[seg.get("segment_id")] = seg.get("text", "")
    for item in case.get("evidence", []):
        for seg in item.get("segments", []):
            segments[seg.get("segment_id")] = seg.get("text", "")
    return segments


def lineage_graph(case):
    return {item.get("source_id"): list(item.get("origin", {}).get("derived_from", [])) for item in case.get("evidence", [])}


def has_cycle(graph):
    state = {}

    def visit(node):
        if state.get(node) == "active":
            return True
        if state.get(node) == "done":
            return False
        state[node] = "active"
        cyclic = any(visit(parent) for parent in graph.get(node, []) if parent in graph)
        state[node] = "done"
        return cyclic

    return any(visit(node) for node in sorted(graph))


def check_case(path, case, report):
    stem = posixpath.basename(path).split(".")[0]
    if case.get("case_id") != stem:
        report.fail("FX04", path, f"case_id {case.get('case_id')!r} does not match file name {stem!r}")
    leaked = ANSWER_KEY_FIELDS & set(walk_keys(case))
    if leaked:
        report.fail("FX05", path, "answer-key fields present: " + ", ".join(sorted(leaked)))
    if CATEGORY_WORDS.search(str(case.get("title", ""))):
        report.fail("FX06", path, f"title may reveal the category: {case.get('title')!r}")
    subject_ids = [seg.get("segment_id") for seg in case.get("subject", {}).get("segments", [])]
    if subject_ids != [f"A{i}" for i in range(1, len(subject_ids) + 1)]:
        report.fail("FX07", path, f"subject segments are not A1..An: {subject_ids}")
    seen = set(subject_ids)
    source_ids = [item.get("source_id") for item in case.get("evidence", [])]
    if len(source_ids) != len(set(source_ids)):
        report.fail("FX08", path, "duplicate source IDs")
    for item in case.get("evidence", []):
        sid = item.get("source_id")
        seg_ids = [seg.get("segment_id") for seg in item.get("segments", [])]
        if seg_ids != [f"{sid}.{i}" for i in range(1, len(seg_ids) + 1)]:
            report.fail("FX08", path, f"segments of {sid} are not {sid}.1..{sid}.n: {seg_ids}")
        for seg_id in seg_ids:
            if seg_id in seen:
                report.fail("FX08", path, f"duplicate segment ID {seg_id}")
            seen.add(seg_id)
    graph = lineage_graph(case)
    for sid, parents in sorted(graph.items()):
        for parent in parents:
            if parent not in graph or parent == sid:
                report.fail("FX09", path, f"{sid} derived_from names {parent!r}, which is not another source in this case")
    if has_cycle(graph):
        report.fail("FX09", path, "declared lineage contains a cycle")
    for sid in case.get("assistant_had_access_to", []):
        if sid not in graph:
            report.fail("FX10", path, f"assistant_had_access_to names unknown source {sid!r}")
    for x in case.get("transformations", []):
        tid = x.get("transformation_id")
        for sid in list(x.get("source_ids", [])) + [x.get("output_id")]:
            if sid not in graph:
                report.fail("FX11", path, f"transformation {tid} names unknown item {sid!r}")
        output = x.get("output_id")
        if output in graph and not set(x.get("source_ids", [])) <= set(graph[output]):
            report.fail("FX11", path, f"transformation {tid}: output {output} does not declare its sources in derived_from")


def check_expectation(path, exp, case, report):
    cid = exp.get("case_id")
    stem = posixpath.basename(path).split(".")[0]
    if cid != stem:
        report.fail("FX04", path, f"case_id {cid!r} does not match file name {stem!r}")
    acceptable = exp.get("acceptable_support_assessments", [])
    if exp.get("expected_support_assessment") not in acceptable:
        report.fail("FX13", path, "expected_support_assessment is not in acceptable_support_assessments")
    planted = exp.get("planted", [])
    if exp.get("category") == "benign_control":
        if planted or exp.get("expect_no_material_defect") is not True:
            report.fail("FX14", path, "a benign control must plant nothing and set expect_no_material_defect to true")
    elif exp.get("expect_no_material_defect") is not False or not any(p.get("role") == "primary" for p in planted):
        report.fail("FX14", path, "a defect case must plant a primary item and set expect_no_material_defect to false")
    if case is None:
        return
    segments = case_segments(case)
    ids = []
    for group, key in (("planted", "planted_id"), ("acceptable", "acceptable_id"), ("traps", "trap_id")):
        for item in exp.get(group, []):
            item_id = item.get(key, "")
            ids.append(item_id)
            if not str(item_id).startswith(f"{cid}-"):
                report.fail("FX15", path, f"{item_id} does not carry the prefix {cid}-")
            for locus in item.get("loci", []):
                if locus not in segments:
                    report.fail("FX16", path, f"{item_id} names locus {locus}, which is not in the case")
    if len(ids) != len(set(ids)):
        report.fail("FX15", path, "duplicate item IDs")
    for item in planted:
        for q in item.get("inferable_from", []):
            text = segments.get(q.get("segment_id"))
            if text is None:
                report.fail("FX17", path, f"{item.get('planted_id')} quotes unknown segment {q.get('segment_id')}")
            elif q.get("quote", "") not in text:
                report.fail("FX17", path, f"{item.get('planted_id')} quotation is not an exact substring of {q.get('segment_id')}")
    category = exp.get("category")
    disagreement = exp.get("disagreement_expectations")
    transformation = exp.get("transformation_expectations")
    if (category == "legitimate_disagreement") != isinstance(disagreement, dict):
        report.fail("FX18", path, "disagreement expectations must be present exactly for legitimate_disagreement")
    if (category == "transformed_context") != isinstance(transformation, dict):
        report.fail("FX18", path, "transformation expectations must be present exactly for transformed_context")
    if (category == "transformed_context") != bool(case.get("transformations")):
        report.fail("FX18", path, "a case has transformation records exactly when its category is transformed_context")
    if isinstance(transformation, dict):
        known = {x.get("transformation_id") for x in case.get("transformations", [])}
        if transformation.get("transformation_id") not in known:
            report.fail("FX18", path, f"transformation expectation names unknown transformation {transformation.get('transformation_id')!r}")


def check_fixtures(files, parsed, validators, report):
    cases, exps = {}, {}
    for path, doc in parsed.items():
        if path.startswith(("fixtures/cases/", "fixtures/expectations/")):
            if not isinstance(doc, dict):
                report.fail("FX01" if path.startswith("fixtures/cases/") else "FX02", path, "not a JSON object")
            elif path.startswith("fixtures/cases/") and path.endswith(".case.json"):
                cases[path] = doc
            elif path.endswith(".expected.json"):
                exps[path] = doc
    for path, case in sorted(cases.items()):
        schema_check(validators, "case", "FX01", path, case, report)
        if b"canary" in files[path].lower():
            report.fail("FX05", path, "canary text present in a critic-visible case")
        check_case(path, case, report)
    case_by_id = {posixpath.basename(p).split(".")[0]: d for p, d in cases.items()}
    exp_ids = {posixpath.basename(p).split(".")[0] for p in exps}
    present_case_files = {p for p in files if p.startswith("fixtures/cases/") and p.endswith(".case.json")}
    present_exp_files = {p for p in files if p.startswith("fixtures/expectations/") and p.endswith(".expected.json")}
    for cid in sorted(set(posixpath.basename(p).split(".")[0] for p in present_case_files) - exp_ids):
        report.fail("FX12", f"fixtures/cases/{cid}.case.json", "no answer key for this case")
    for cid in sorted(exp_ids - set(posixpath.basename(p).split(".")[0] for p in present_case_files)):
        report.fail("FX12", f"fixtures/expectations/{cid}.expected.json", "answer key without a case")
    categories = []
    for path, exp in sorted(exps.items()):
        schema_check(validators, "expectation", "FX02", path, exp, report)
        check_expectation(path, exp, case_by_id.get(posixpath.basename(path).split(".")[0]), report)
        categories.append(exp.get("category"))
    if sorted(categories) != sorted(CATEGORIES):
        report.fail("FX19", "fixtures/expectations", f"categories are {sorted(categories)}, expected one of each of {sorted(CATEGORIES)}")
    index = parsed.get("fixtures/index.json")
    if not isinstance(index, dict):
        report.fail("FX03", "fixtures/index.json", "missing, unparsable or not a JSON object")
    else:
        if not CANARY.search(str(index.get("canary", ""))):
            report.fail("FX03", "fixtures/index.json", "canary missing")
        entries = index.get("cases", [])
        listed_cases = {posixpath.join("fixtures", e.get("case_file", "")) for e in entries}
        listed_exps = {posixpath.join("fixtures", e.get("expectation_file", "")) for e in entries}
        if listed_cases != present_case_files:
            report.fail("FX03", "fixtures/index.json", "listed case files differ from the case files present")
        if listed_exps != present_exp_files:
            report.fail("FX03", "fixtures/index.json", "listed answer-key files differ from the answer-key files present")
        for e in entries:
            exp = parsed.get(posixpath.join("fixtures", e.get("expectation_file", "")))
            if exp is not None and exp.get("category") != e.get("category"):
                report.fail("FX03", "fixtures/index.json", f"{e.get('case_id')}: category {e.get('category')!r} differs from its answer key")
            for key in ("case_file", "expectation_file"):
                stem = posixpath.basename(e.get(key, "")).split(".")[0]
                if stem != e.get("case_id"):
                    report.fail("FX04", "fixtures/index.json", f"{e.get('case_id')}: {key} {e.get(key)!r} does not match the case ID")
        for doc in index.get("pinned_documents", []):
            if posixpath.normpath(posixpath.join("fixtures", doc)) not in files:
                report.fail("FX03", "fixtures/index.json", f"pinned document {doc} does not exist")
    readme = files.get("fixtures/README.md")
    if readme is None or not CANARY.search(readme.decode("utf-8", "replace")):
        report.fail("FX20", "fixtures/README.md", "canary missing")


def roots_of(graph, node, trail=()):
    parents = [p for p in graph.get(node, []) if p in graph and p not in trail]
    if not parents:
        return {node}
    return set().union(*(roots_of(graph, p, trail + (node,)) for p in parents))


def check_record(path, rec, files, parsed, validators, report):
    schema_check(validators, "eer", "V0", path, rec, report)
    packet_ref = rec.get("packet", {})
    packet_path = packet_ref.get("path", "")
    raw = files.get(packet_path)
    packet = parsed.get(packet_path)
    if raw is None or packet is None:
        report.fail("V1", path, f"packet {packet_path!r} is missing or does not parse")
        return
    if sha256(raw) != packet_ref.get("sha256"):
        report.fail("V1", path, "packet.sha256 does not match the packet bytes")
    if packet.get("case_id") != packet_ref.get("case_id"):
        report.fail("V1", path, "packet case_id does not match")
    reviewers = rec.get("reviewers", [])
    findings = rec.get("findings", [])
    assessments = rec.get("reviewer_assessments", [])
    synthesis = rec.get("synthesis", {})
    integrity = rec.get("integrity", {})
    segments = case_segments(packet)

    consistent = all(r.get("packet_sha256") == packet_ref.get("sha256") for r in reviewers)
    if consistent != integrity.get("packet_hash_consistent"):
        report.fail("V2", path, "integrity.packet_hash_consistent does not match the reviewers' packet hashes")

    reviewer_ids = [r.get("reviewer_id") for r in reviewers]
    by_id = {r.get("reviewer_id"): r for r in reviewers}
    finding_ids = [f.get("finding_id") for f in findings]
    if len(reviewer_ids) != len(set(reviewer_ids)):
        report.fail("V3", path, "duplicate reviewer IDs")
    if len(finding_ids) != len(set(finding_ids)):
        report.fail("V3", path, "duplicate finding IDs")
    for f in findings:
        if f.get("reviewer_id") not in by_id:
            report.fail("V3", path, f"finding {f.get('finding_id')} names unknown reviewer {f.get('reviewer_id')!r}")
    for a in assessments:
        if a.get("reviewer_id") not in by_id:
            report.fail("V3", path, f"assessment names unknown reviewer {a.get('reviewer_id')!r}")

    invalid = {x.get("reviewer_id") for x in integrity.get("invalid_reviewer_outputs", [])}
    assessed = sorted(a.get("reviewer_id") for a in assessments)
    if assessed != sorted(set(reviewer_ids) - invalid):
        report.fail("V4", path, "reviewer_assessments must cover each valid reviewer exactly once")

    mismatched, unverified, unknown = set(), set(), set()
    for f in findings:
        fid = f.get("finding_id")
        if any(s not in segments for s in f.get("segments", [])):
            unknown.add(fid)
        for q in f.get("quotations", []):
            text = segments.get(q.get("segment_id"))
            if text is None:
                unknown.add(fid)
            matches = text is not None and q.get("quote", "") in text
            state = q.get("source_verification")
            if state == "unverified":
                unverified.add(fid)
                continue
            if state == "source_linked" and not matches:
                report.fail("V5", path, f"finding {fid}: quotation marked source_linked is not in {q.get('segment_id')}")
            if state == "source_mismatch" and matches:
                report.fail("V5", path, f"finding {fid}: quotation marked source_mismatch is present in {q.get('segment_id')}")
            if not matches:
                mismatched.add(fid)
    if mismatched != set(integrity.get("quotation_mismatch_finding_ids", [])):
        report.fail("V5", path, "integrity.quotation_mismatch_finding_ids does not list exactly the findings with mismatched quotations")
    if unverified != set(integrity.get("unverified_quotation_finding_ids", [])):
        report.fail("V5", path, "integrity.unverified_quotation_finding_ids does not list exactly the findings with unverified quotations")
    if unknown != set(integrity.get("unknown_segment_finding_ids", [])):
        report.fail("V6", path, "integrity.unknown_segment_finding_ids does not list exactly the findings citing absent segments")

    by_value = {}
    for a in assessments:
        by_value.setdefault(a.get("support_assessment"), set()).add(a.get("reviewer_id"))
    listed = {}
    for p in synthesis.get("positions", []) + synthesis.get("dropped_positions", []):
        listed.setdefault(p.get("support_assessment"), set()).update(p.get("held_by", []))
    if listed != by_value:
        report.fail("V7", path, "positions plus dropped_positions must exactly partition the reviewer assessments")
    if synthesis.get("method") in ("single_reviewer", "mechanical_union") and synthesis.get("dropped_positions"):
        report.fail("V7", path, f"dropped_positions must be empty for {synthesis.get('method')}")

    position_ids = {p.get("position_id") for p in synthesis.get("positions", [])}
    covered = set()
    for d in synthesis.get("unresolved_disagreements", []):
        if not set(d.get("position_ids", [])) <= position_ids:
            report.fail("V8", path, f"disagreement {d.get('disagreement_id')} references a position that is not listed")
        covered |= set(d.get("position_ids", []))
    if len(position_ids) > 1 and covered != position_ids:
        report.fail("V8", path, "positions differ but no open disagreement covers all of them")

    attention = {}
    for f in findings:
        for s in f.get("segments", []):
            attention.setdefault(s, set()).add(f.get("reviewer_id"))
    recorded = {a.get("segment_id"): set(a.get("reviewer_ids", [])) for a in synthesis.get("segment_attention", [])}
    if recorded != attention:
        report.fail("V9", path, "segment_attention is not the projection of the findings' segments")
    for a in synthesis.get("segment_attention", []):
        classes = {by_id[r].get("independence_class") for r in a.get("reviewer_ids", []) if r in by_id}
        if classes != set(a.get("independence_classes", [])):
            report.fail("V9", path, f"independence_classes for {a.get('segment_id')} do not match its reviewers")

    graph = lineage_graph(packet)
    declared = {d.get("source_id"): d for d in rec.get("lineage", {}).get("declared", [])}
    if set(declared) != set(graph):
        report.fail("V10", path, "lineage.declared must list every evidence item exactly once")
    for sid, d in sorted(declared.items()):
        if sid in graph and (d.get("derived_from") != graph[sid] or set(d.get("declared_roots", [])) != roots_of(graph, sid)):
            report.fail("V10", path, f"declared lineage for {sid} does not mirror the packet")

    in_packet = {x.get("transformation_id"): x for x in packet.get("transformations", [])}
    in_record = {x.get("transformation_id"): x for x in rec.get("lineage", {}).get("transformations", [])}
    if set(in_packet) != set(in_record):
        report.fail("V11", path, "lineage.transformations must mirror the packet's transformation records")
    for tid, x in sorted(in_record.items()):
        p = in_packet.get(tid)
        if p and (set(x.get("standing_ceiling_source_ids", [])) != set(p.get("source_ids", []))
                  or x.get("fidelity_check") != p.get("fidelity_check") or x.get("output_id") != p.get("output_id")):
            report.fail("V11", path, f"transformation {tid} does not mirror the packet")
        for effect in x.get("standing_effects_reported", []):
            if not set(effect.get("finding_ids", [])) <= set(finding_ids):
                report.fail("V11", path, f"transformation {tid} cites an unknown finding")

    method = synthesis.get("method")
    if method in ("mechanical_union", "model_synthesis") and not all(r.get("submitted_before_synthesis") is True for r in reviewers):
        report.fail("V12", path, "every reviewer must submit before synthesis")
    if method == "single_reviewer" and len(reviewers) != 1:
        report.fail("V12", path, "single_reviewer requires exactly one reviewer")

    if rec.get("record_status") == "study_record":
        check_condition(path, rec, report)
        report.study_records += 1


def check_condition(path, rec, report):
    context = rec.get("study_context")
    if not isinstance(context, dict):
        report.fail("V13", path, "a study record needs a study_context")
        return
    condition = context.get("condition")
    procedures = [r.get("procedure") for r in rec.get("reviewers", [])]
    method = rec.get("synthesis", {}).get("method")
    single = {"C0": "naive", "C1": "generic", "C2": "O1-O6_sequential"}
    if condition in single:
        ok = procedures == [single[condition]] and method == "single_reviewer"
    elif condition == "C3":
        ok = len(procedures) >= 2 and set(procedures) == {"generic"} and method in ("mechanical_union", "model_synthesis")
    elif condition == "C4":
        ok = sorted(procedures) == sorted(OPERATORS) and method in ("mechanical_union", "model_synthesis")
    else:
        ok = False
    if not ok:
        report.fail("V13", path, f"condition {condition!r} does not match reviewers {procedures} with method {method!r}")


def check_examples(files, parsed, validators, report):
    for path, doc in sorted(parsed.items()):
        if not path.startswith("examples/"):
            continue
        if not isinstance(doc, dict):
            report.fail("V0", path, "not a JSON object")
        elif "case_format" in doc:
            schema_check(validators, "case", "EX01", path, doc, report)
        elif "record_format" in doc:
            check_record(path, doc, files, parsed, validators, report)
        else:
            report.fail("V0", path, "neither a case packet nor a record")
    if report.study_records == 0:
        report.not_applicable["V13"] = "no study records present"


def check_pins(files, parsed, report):
    raw = files.get("fixtures/SHA256SUMS")
    if raw is None:
        report.fail("PIN01", "fixtures/SHA256SUMS", "missing")
        return
    entries = {}
    for number, line in enumerate(raw.decode("ascii", "replace").splitlines(), 1):
        match = PIN_LINE.fullmatch(line)
        if not match:
            report.fail("PIN01", "fixtures/SHA256SUMS", f"line {number} is not '<sha256>  <path>'")
            continue
        target = posixpath.normpath(posixpath.join("fixtures", match.group(2)))
        if target in entries:
            report.fail("PIN02", "fixtures/SHA256SUMS", f"{match.group(2)} is pinned more than once")
        entries[target] = match.group(1)
        data = files.get(target)
        if data is None:
            report.fail("PIN01", "fixtures/SHA256SUMS", f"{match.group(2)} is pinned but missing")
        elif sha256(data) != match.group(1):
            report.fail("PIN01", "fixtures/SHA256SUMS", f"{match.group(2)} does not match its pin")
    required = {p for p in files if p.startswith(("fixtures/cases/", "fixtures/expectations/")) and p.endswith(".json")}
    required.add("fixtures/index.json")
    index = parsed.get("fixtures/index.json")
    pinned = index.get("pinned_documents", []) if isinstance(index, dict) else []
    required |= {posixpath.normpath(posixpath.join("fixtures", doc)) for doc in pinned}
    for target in sorted(required - set(entries)):
        report.fail("PIN02", "fixtures/SHA256SUMS", f"{target} is not pinned")


def run_rules(files):
    report = Report()
    check_bytes(files, report)
    parsed = parse_json_files(files, report)
    validators = load_validators(files, parsed, report)
    check_fixtures(files, parsed, validators, report)
    check_examples(files, parsed, validators, report)
    check_pins(files, parsed, report)
    return report


class ControlError(Exception):
    pass


def _pointer_parent(doc, pointer):
    if not pointer.startswith("/"):
        raise ControlError(f"bad JSON pointer {pointer!r}")
    parts = [p.replace("~1", "/").replace("~0", "~") for p in pointer[1:].split("/")]
    node = doc
    try:
        for part in parts[:-1]:
            node = node[int(part)] if isinstance(node, list) else node[part]
    except (KeyError, IndexError, ValueError) as exc:
        raise ControlError(f"pointer {pointer!r} does not resolve") from exc
    return node, parts[-1]


def apply_control(files, control):
    mutated = dict(files)
    for op in control["ops"]:
        kind, path = op.get("op"), op.get("path")
        if kind == "file_add":
            if path in mutated:
                raise ControlError(f"{path} already exists")
            mutated[path] = op["text"].encode("utf-8")
            continue
        if path not in mutated:
            raise ControlError(f"{path} is not among the loaded files")
        if kind in ("json_set", "json_remove"):
            doc = json.loads(mutated[path].decode("utf-8"))
            parent, last = _pointer_parent(doc, op["pointer"])
            try:
                key = int(last) if isinstance(parent, list) else last
                if kind == "json_set":
                    parent[key] = op["value"]
                else:
                    del parent[key]
            except (KeyError, IndexError, ValueError) as exc:
                raise ControlError(f"pointer {op['pointer']!r} does not resolve") from exc
            mutated[path] = (json.dumps(doc, indent=2) + "\n").encode("ascii")
        elif kind == "text_replace":
            text = mutated[path].decode("utf-8")
            if op["old"] not in text:
                raise ControlError(f"text to replace not found in {path}")
            mutated[path] = text.replace(op["old"], op["new"], 1).encode("utf-8")
        elif kind == "remove_line_containing":
            lines = mutated[path].decode("utf-8").splitlines(keepends=True)
            hits = [i for i, line in enumerate(lines) if op["text"] in line]
            if not hits:
                raise ControlError(f"no line in {path} contains {op['text']!r}")
            del lines[hits[0]]
            mutated[path] = "".join(lines).encode("utf-8")
        elif kind == "file_remove":
            del mutated[path]
        else:
            raise ControlError(f"unknown operation {kind!r}")
    return mutated


def run_controls(files, controls):
    results = []
    for control in controls:
        cid = control.get("id", "?")
        expect = control.get("expect", [])
        if not expect or not control.get("ops") or any(rule not in RULES for rule in expect):
            results.append((cid, "INVALID", "control needs ops and known expected rules", []))
            continue
        try:
            report = run_rules(apply_control(files, control))
        except ControlError as exc:
            results.append((cid, "INVALID", str(exc), []))
            continue
        also = [rule for rule in RULES if rule in report.failures and rule not in expect]
        missing = [rule for rule in expect if rule not in report.failures]
        if missing:
            results.append((cid, "MISSED", "expected " + ", ".join(missing) + " did not fire", also))
        else:
            results.append((cid, "DETECTED", "expected " + ", ".join(expect), also))
    return results


def jsonschema_version():
    if jsonschema is None:
        return "not installed"
    try:
        return importlib.metadata.version("jsonschema")
    except importlib.metadata.PackageNotFoundError:
        return "installed (version unknown)"


def main(argv=None):
    parser = argparse.ArgumentParser(description="Validate the Philosophical Council planning artifacts.")
    parser.add_argument("--root", help="research/philosophical-council directory (default: parent of this script's directory)")
    args = parser.parse_args(argv)
    root = Path(args.root) if args.root else Path(__file__).resolve().parent.parent
    if not root.is_dir():
        parser.error(f"{root} is not a directory")

    files = load_tree(root)
    report = run_rules(files)
    controls_doc = {}
    try:
        controls_doc = json.loads(files.get("validation/negative_controls.json", b"{}").decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        pass  # reported as F03 by the positive run
    controls = controls_doc.get("controls", []) if isinstance(controls_doc, dict) else []
    results = run_controls(files, controls)

    print(f"{VALIDATOR_VERSION} (proposed planning tooling)")
    print(f"root: {args.root if args.root else 'default (parent of validation/)'}")
    print(f"python {sys.version.split()[0]}; jsonschema {jsonschema_version()}")
    print(f"validator sha256 {sha256(files.get('validation/validate.py', b''))}")
    print(f"negative controls sha256 {sha256(files.get('validation/negative_controls.json', b''))}")
    print(f"files read: {len(files)}")
    print()
    print("Rules")
    for rule, title in RULES.items():
        status = report.status(rule)
        print(f"  {status:<8} {rule:<6} {title}")
        for where, message in sorted(report.failures.get(rule, ())):
            print(f"           - {where}: {message}")
        if status == "NOT RUN":
            print(f"           - {report.not_run[rule]}")
        if status == "N/A":
            print(f"           - {report.not_applicable[rule]}")
    print()
    print("Negative controls")
    for cid, state, detail, also in results:
        print(f"  {state:<8} {cid}: {detail}" + (f"; also fired {', '.join(also)}" if also else ""))
    covered = {rule for control in controls for rule in control.get("expect", [])}
    uncovered = [rule for rule in RULES if rule not in covered]
    print()
    print("Coverage: " + ("every rule has a negative control" if not uncovered else "rules without a negative control: " + ", ".join(uncovered)))

    failed = [rule for rule in RULES if report.status(rule) in ("FAIL", "NOT RUN")]
    bad_controls = [cid for cid, state, _, _ in results if state != "DETECTED"]
    passed = not failed and not bad_controls and not uncovered and bool(controls)
    counts = {s: sum(1 for rule in RULES if report.status(rule) == s) for s in ("PASS", "FAIL", "NOT RUN", "N/A")}
    print(f"Result: {'PASS' if passed else 'FAIL'} "
          f"({counts['PASS']} rules passed, {counts['FAIL']} failed, {counts['NOT RUN']} not run, {counts['N/A']} not applicable; "
          f"{len(results) - len(bad_controls)}/{len(results)} negative controls detected)")
    print("Not established by a pass: correctness of the answer keys (needs a human second reader), absence of "
          "overreach in free text (needs human scoring), or anything about critic behaviour.")
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
