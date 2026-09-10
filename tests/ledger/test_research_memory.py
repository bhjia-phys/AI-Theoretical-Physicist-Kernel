"""Small real-use-inspired memory journeys through the installable CLI.

Synthetic data, not scientific experiments or model-behavior acceptance. Only
drafts and ordinary evidence files are filled by this test; the bundled CLI is
the sole canonical writer. Read-side ordering remains the frozen contract.
"""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

import pytest

from aitp.core import parse_markdown, render_markdown

PLUGIN = Path(__file__).resolve().parents[2] / "plugins" / "aitp-research-protocol"


def cli(root: Path, *args: str, expected_exit: int = 0) -> dict:
    result = subprocess.run(
        [sys.executable, "-I", str(PLUGIN / "scripts/aitp.py"), *args, "--json"],
        cwd=root, capture_output=True, text=True, check=False, timeout=15,
    )
    assert result.returncode == expected_exit, (args, result.stdout, result.stderr)
    return json.loads(result.stdout)


@pytest.fixture
def project(tmp_path: Path) -> Path:
    cli(tmp_path, "init", "--topic", "memory-example", "--title", "Memory example")
    return tmp_path


def evidence(root: Path, name: str, text: str) -> str:
    path = root / "theory" / name
    assert not path.exists()
    path.write_text(text, encoding="utf-8")
    return str(path.relative_to(root))


def pin(root: Path, target: str) -> dict[str, str]:
    return {
        "target": target,
        "at": "sha256:" + hashlib.sha256((root / target).read_bytes()).hexdigest(),
        "locator": "whole synthetic example file",
    }


def save(
    root: Path, family: str, variant: str, scope: str, summary: str,
    paragraphs: list[str], targets: list[str], *, authority: str = "agent",
    supersedes: list[str] | None = None, resolves: list[str] | None = None,
    next_action: str = "", expected_check_exit: int = 0,
) -> dict:
    creator = "researcher" if authority == "human" else "agent:test"
    prepare = [family, "prepare", "--created-by", creator, "--workstream", scope]
    if family == "record":
        prepare += ["--kind", variant, "--authority", authority,
                    "--idempotency-key", summary]
    else:
        prepare += ["--mode", variant, "--title", summary]
    prepared = cli(root, *prepare)
    assert prepared["status"] == "prepared"
    draft = root / prepared["path"]
    assert draft.parent == root / ".aitp/local/drafts"
    fm, template, _ = parse_markdown(draft)
    fm["summary"] = summary
    fm["supersedes"] = supersedes or []
    fm["refs" if family == "record" else "basis_refs"] = [pin(root, t) for t in targets]
    if family == "record":
        fm["limitations"] = ["Synthetic memory fixture; not a physical result."]
        fm["resolves"] = resolves or []
        fm["next_action"] = next_action
    headings = re.findall(r"^## (.+)$", template, re.MULTILINE)
    body = "\n\n".join(
        f"## {heading}\n\n{paragraph}"
        for heading, paragraph in zip(headings, paragraphs, strict=True)
    ) + "\n"
    draft.write_text(render_markdown(fm, body), encoding="utf-8")
    save_args = [family, "save", prepared["path"]]
    if family == "record":
        save_args += ["--expected-topic", "memory-example", "--exact-workstream", scope]
    saved = cli(root, *save_args)
    assert saved["status"] == "saved"
    assert cli(root, *save_args)["status"] == "already_saved"
    cli(root, "check", "--workstream", scope, expected_exit=expected_check_exit)
    cli(root, "enter", "--workstream", scope)
    return {"id": fm["id"], "path": saved["path"], "created_at": fm["created_at"]}


def tree(root: Path) -> dict[str, bytes]:
    return {str(p.relative_to(root)): p.read_bytes() for p in root.rglob("*") if p.is_file()}


def working(summary: str, basis: str, synthesis: str, next_action: str) -> list[str]:
    return [summary, basis, synthesis, f"Evidence and limits: {basis}",
            "This synthesis does not establish general physical correctness.",
            "Which missing observation would distinguish the remaining explanations?",
            next_action]


def test_scoped_resume_finds_new_failure_without_rewriting_old_handoff(project: Path):
    root = project
    report = evidence(root, "submission.txt", "Synthetic run receipt; no physical output yet.")
    old = save(root, "record", "closeout", "qsgw", "Waiting for the submitted run",
               ["Submitted run awaits output.", "No accepted band output yet.",
                "Read the submitted run's output."], [report], next_action="Wait for run")
    si = save(root, "note", "working", "qsgw", "Si working explanation",
              working("Si output question", report, "Output is still awaited.", "Read output"),
              [old["path"]])
    # Shared evidence does not import the other line's Note or establish its physics.
    nio = save(root, "note", "working", "crpa", "NiO working explanation",
               working("NiO interaction question", report, "No accepted interaction yet.",
                       "Check the interaction"), [report])
    err = evidence(root, "failure.txt", "Synthetic output: build target not found; no bands.")
    failed = save(root, "record", "failure", "qsgw", "Build failed before producing bands",
                  ["No bands were produced.", "Expected compilation; observed missing target.",
                   "Inspect the named target, not band physics."], [err],
                  next_action="Inspect the build target")
    before = tree(root)
    state = cli(root, "enter", "--workstream", "qsgw")
    assert state["schema"] == "aitp/enter-0.3"
    assert state["latest_working_note"]["source"] == si["path"]
    assert state["next_action"]["entry_id"] == old["id"]  # closeout-first, unchanged
    assert state["unresolved_failures"][0]["id"] == failed["id"]
    later = cli(root, "list", "--workstream", "qsgw", "--since", si["created_at"])
    assert [entry["id"] for entry in later["entries"]] == [failed["id"]]
    shown = cli(root, "show", failed["id"])
    assert "missing target" in shown["body"]
    assert shown["frontmatter"]["refs"] == [pin(root, err)]
    si_fm, _, _ = parse_markdown(root / state["latest_working_note"]["source"])
    assert si_fm["workstreams"] == ["qsgw"]
    assert cli(root, "enter", "--workstream", "crpa")["latest_working_note"]["source"] == nio["path"]
    assert cli(root, "enter", "--workstream", "unknown")["latest_working_note"] is None
    cli(root, "check", "--workstream", "qsgw")
    assert tree(root) == before  # the read journey creates no Entry, Note or repair


def test_derivation_revision_preserves_human_pause_and_exact_prior_evidence(project: Path):
    root = project
    pause = save(root, "record", "decision", "operator-search", "Pause autonomous exploration",
                 ["The researcher paused autonomous work.", "Discuss before a new campaign.",
                  "A bounded derivation review is not permission to resume."], [], authority="human")
    early = evidence(root, "argument-v1.txt", "Synthetic draft: replace XY + YX by 2XY unconditionally.")
    old = save(root, "record", "result", "operator-search", "Initial candidate simplification",
               ["Candidate simplification only.", "The argument is in argument-v1.txt.",
                "Operator ordering has not been checked."], [early])
    preserved = {p: (root / p).read_bytes() for p in (pause["path"], old["path"], early)}
    revised = evidence(root, "argument-v2.txt", "Synthetic correction: XY + YX = 2XY only if [X,Y]=0.")
    current = save(root, "record", "result", "operator-search", "Ordering assumption made explicit",
                   ["The simplification requires commutativity.", "argument-v2.txt states the condition.",
                    "No general integrability or new execution authority follows."],
                   [old["path"], revised], supersedes=[old["id"]])
    state = cli(root, "enter", "--workstream", "operator-search")
    assert state["latest_working_note"] is None  # no compulsory synthesis to enable reads
    assert cli(root, "show", old["id"])["status"] == "superseded"
    human = cli(root, "show", pause["id"])
    assert human["status"] == "active"
    assert human["frontmatter"]["authority"] == "human"
    assert "not permission to resume" in human["body"]
    note = save(root, "note", "theory", "operator-search", "Conditional operator argument",
                ["When is the ordered expression replaceable?", "Finite operators X and Y.",
                 "Retain XY + YX unless their commutator vanishes.", "A conditional identity only.",
                 "A small example is not a general many-body proof.",
                 "General symmetry and integrability remain open."], [current["path"], revised])
    note_fm, body, _ = parse_markdown(root / note["path"])
    assert note_fm["review_state"] == "agent_draft"
    assert note_fm["basis_refs"][-1] == pin(root, revised)
    assert "not a general many-body proof" in body
    assert {p: (root / p).read_bytes() for p in preserved} == preserved
    assert cli(root, "list", "--workstream", "operator-search")["count"] == 3


def test_interpretation_narrows_without_losing_valid_argument_or_inventing_route_reason(project: Path):
    root = project
    argument = evidence(root, "conditional-identity.txt",
                        "Synthetic: under assumption A, identity B holds. No physical map supplied.")
    old = save(root, "record", "result", "wall-theory", "Candidate interpretation",
               ["Identity B holds under A; a physical interpretation is proposed.",
                "See conditional-identity.txt; the original route reason was not recorded.",
                "The physical map remains unproved."], [argument])
    preserved = {p: (root / p).read_bytes() for p in (argument, old["path"])}
    objection = evidence(root, "map-objection.txt",
                         "Synthetic objection: B alone does not identify the physical object.")
    revised = save(root, "record", "result", "wall-theory", "Interpretation narrowed",
                   ["Identity B under A remains valid; physical identification is withdrawn.",
                    "The map objection explains the restriction; original route reason is unknown.",
                    "Retry identification only with an independent physical map."],
                   [old["path"], argument, objection], supersedes=[old["id"]])
    before = tree(root)
    state = cli(root, "enter", "--workstream", "wall-theory")
    assert state["latest_working_note"] is None  # result does not require a duplicate synthesis
    current = cli(root, "show", revised["id"])
    prior = cli(root, "show", old["id"])
    assert prior["status"] == "superseded"
    assert "remains valid" in current["body"]
    assert "original route reason is unknown" in current["body"]
    assert current["frontmatter"]["refs"] == [pin(root, old["path"]), pin(root, argument), pin(root, objection)]
    assert prior["frontmatter"]["refs"] == [pin(root, argument)]
    assert cli(root, "list", "--workstream", "wall-theory")["count"] == 2
    assert cli(root, "list", "--workstream", "crpa")["count"] == 0
    assert {p: (root / p).read_bytes() for p in preserved} == preserved
    assert tree(root) == before


def test_working_synthesis_revision_can_pin_manuscript_without_duplicate_result(project: Path):
    root = project
    argument = evidence(root, "wall-argument-v1.txt", "Synthetic candidate construction; uniqueness not proved.")
    first = save(root, "note", "working", "wall-theory", "Candidate wall construction",
                 working("Which wall construction?", argument, "A candidate, not a uniqueness theorem.",
                         "Find a discriminating physical input"), [argument])
    original = (root / first["path"]).read_bytes()
    audit = evidence(root, "wall-audit.txt", "Synthetic audit: a noncircular probe-to-wall map is missing.")
    result = save(root, "record", "result", "wall-theory", "Missing map identified",
                  ["The argument needs an independent map.", "See the pinned wall audit.",
                   "Candidate construction remains; uniqueness does not follow."], [audit])
    count_before_note = cli(root, "list", "--workstream", "wall-theory")["count"]
    second = save(root, "note", "working", "wall-theory", "Candidate with explicit missing map",
                  working("What prevents a uniqueness claim?", f"{result['path']}; {argument}",
                          "New audit isolates the missing map; the candidate remains conditional.",
                          "Derive the independent probe-to-wall map"),
                  [result["path"], argument], supersedes=[first["id"]])
    state = cli(root, "enter", "--workstream", "wall-theory")
    assert state["latest_working_note"]["source"] == second["path"]
    fm, body, _ = parse_markdown(root / second["path"])
    assert fm["supersedes"] == [first["id"]]
    assert fm["basis_refs"][1] == pin(root, argument)  # no intermediate duplicate Entry
    assert "candidate remains conditional" in body
    assert (root / first["path"]).read_bytes() == original
    assert cli(root, "list", "--workstream", "wall-theory")["count"] == count_before_note == 1
    before = tree(root)
    cli(root, "enter", "--workstream", "wall-theory")
    report = cli(root, "check", expected_exit=1)
    assert report["status"] == "findings"
    assert [finding["message"] for finding in report["findings"]] == [
        "Research Goal is not established"
    ]  # scoped clean never implies the placeholder Topic has a confirmed Goal
    assert tree(root) == before
    assert all("method-card:" not in p.read_text(encoding="utf-8")
               for p in (root / ".aitp/topic/notes").glob("*.md"))


@pytest.mark.parametrize("replacement_scope", ["spectral", "other-line"])
def test_superseded_resolver_does_not_pass_closure_to_successor(project: Path, replacement_scope: str):
    """A historical repair statement is not an active resolves edge.

    Inspired by a cold-recall misreading, not a request to change the frozen
    projection or automatically close a real scientific failure.
    """
    root = project
    fault = evidence(root, "fault.txt", "Synthetic output failed a consistency check.")
    failed = save(root, "record", "failure", "spectral", "Consistency failure",
                  ["Observed inconsistency.", "Expected consistency, observed a mismatch.",
                   "Find the cause before accepting this output."], [fault])
    repair = evidence(root, "repair.txt", "Synthetic narrow repair passed its own test.")
    resolver = save(root, "record", "closeout", "spectral", "Narrow repair recorded",
                    ["The named inconsistency was repaired.", "Only this synthetic check passed.",
                     "Other scientific questions remain open."], [repair], resolves=[failed["id"]])
    assert cli(root, "enter", "--workstream", "spectral")["unresolved_failures"] == []
    original = (root / resolver["path"]).read_bytes()
    successor = save(root, "record", "closeout", replacement_scope, "Replacement without closure edge",
                     ["Historical repair was discussed previously.", "This record claims no new repair.",
                      "Do not infer a resolves edge from body text or supersedes."],
                     [resolver["path"]], supersedes=[resolver["id"]])
    before = tree(root)
    old = cli(root, "show", resolver["id"])
    current = cli(root, "show", successor["id"])
    assert old["status"] == "superseded"
    assert old["frontmatter"]["resolves"] == [failed["id"]]
    assert current["status"] == "active"
    assert current["frontmatter"]["resolves"] == []
    state = cli(root, "enter", "--workstream", "spectral")
    assert [entry["id"] for entry in state["unresolved_failures"]] == [failed["id"]]
    assert (root / resolver["path"]).read_bytes() == original
    assert tree(root) == before


def test_old_topic_navigation_does_not_override_scoped_note_or_membership(project: Path):
    """A prose map is orientation, not a registry or implicit scope assignment."""
    root = project
    report = evidence(root, "candidate.txt", "Synthetic candidate; numerical acceptance unknown.")
    old = save(root, "note", "working", "response", "Earlier response understanding",
               working("Response question", report, "Candidate only.", "Inspect the evidence"),
               [report])
    topic = root / ".aitp/topic/TOPIC.md"
    original = topic.read_text(encoding="utf-8")
    # Synthetic fixture only. Real Topic edits require the user's file authority.
    topic.write_text(original + f"\nHistorical response entry: {old['path']}\n"
                     "Navigation label: apparent-alias (not recorded membership).\n",
                     encoding="utf-8")
    current = save(root, "note", "working", "response", "Response with explicit missing input",
                   working("Response question", report, "A controlled comparison is missing.",
                           "Identify one discriminating comparison"),
                   [report], supersedes=[old["id"]])
    before = tree(root)
    state = cli(root, "enter", "--workstream", "response")
    assert state["latest_working_note"]["source"] == current["path"]
    fm, body, _ = parse_markdown(root / state["latest_working_note"]["source"])
    assert fm["workstreams"] == ["response"]
    assert fm["basis_refs"] == [pin(root, report)]
    assert "controlled comparison is missing" in body
    assert cli(root, "list", "--workstream", "response")["count"] == 0
    alias = cli(root, "enter", "--workstream", "apparent-alias")
    assert alias["latest_working_note"] is None
    assert alias["recent_entries"] == []
    assert old["path"] in topic.read_text(encoding="utf-8")
    assert tree(root) == before


def test_recovered_version_keeps_original_pin_finding_and_scientific_failure(project: Path):
    """Finding old bytes improves retrieval without rewriting or certifying science."""
    root = project
    original_text = "Synthetic v1 argument; numerical cause remains unknown.\n"
    source = evidence(root, "evolving-argument.txt", original_text)
    snapshot = evidence(root, "argument-v1-snapshot.txt", original_text)
    old = save(root, "record", "failure", "phase-bound", "Unexplained numerical discrepancy",
               ["Observed discrepancy.", "The recorded argument does not determine the cause.",
                "A same-run discriminating observation is missing."], [source])
    original_record = (root / old["path"]).read_bytes()
    original_pin = cli(root, "show", old["id"])["frontmatter"]["refs"][0]["at"]
    (root / source).write_text("Synthetic v2: later diagnostics, not the earlier argument.\n", encoding="utf-8")
    before = cli(root, "check", "--workstream", "phase-bound", expected_exit=1)
    assert [f["code"] for f in before["findings"]] == ["hash_mismatch"]
    assert pin(root, snapshot)["at"] == original_pin
    recovered = save(root, "record", "observation", "phase-bound", "Original argument version recovered",
                     ["The stored v1 snapshot matches the original digest.",
                      "The original working file has since changed; the snapshot is separate.",
                      "Availability is restored, not numerical correctness."],
                     [old["path"], snapshot], expected_check_exit=1)
    after = cli(root, "check", "--workstream", "phase-bound", expected_exit=1)
    assert after["findings"] == before["findings"]
    state = cli(root, "enter", "--workstream", "phase-bound")
    assert [f["id"] for f in state["unresolved_failures"]] == [old["id"]]
    shown = cli(root, "show", recovered["id"])
    assert shown["frontmatter"]["resolves"] == []
    assert shown["frontmatter"]["supersedes"] == []
    assert shown["frontmatter"]["refs"][1] == pin(root, snapshot)
    assert (root / old["path"]).read_bytes() == original_record
    assert cli(root, "show", old["id"])["frontmatter"]["refs"][0]["at"] == original_pin
    assert cli(root, "list", "--workstream", "different-physics")["entries"] == []


def test_multiline_reads_reuse_global_health_but_evidence_change_requires_refresh(project: Path):
    """A report is a reusable observation, not an automatically fresh cache."""
    root = project
    source = evidence(root, "shared-input.txt", "Synthetic original input.\n")
    records = [save(root, "record", "observation", scope, f"Observed {scope}",
                    ["An observation.", "Synthetic conditions.", "No scientific inference."],
                    [source]) for scope in ("line-a", "line-b")]
    before = tree(root)
    report = cli(root, "check", expected_exit=1)  # Topic Goal placeholder warning.
    assert report["schema"] == "aitp/check-report-0.1"
    assert report["counts"]["errors"] == 0
    for scope, record in zip(("line-a", "line-b"), records, strict=True):
        state = cli(root, "enter", "--workstream", scope)
        assert state["workstream"] == scope
        listed = cli(root, "list", "--workstream", scope)
        assert [entry["id"] for entry in listed["entries"]] == [record["id"]]
        assert cli(root, "show", record["id"])["frontmatter"]["workstreams"] == [scope]
    assert tree(root) == before
    (root / source).write_text("Synthetic changed input.\n", encoding="utf-8")
    refreshed = cli(root, "check", expected_exit=1)
    assert report["counts"]["errors"] == 0  # Old observation has not refreshed itself.
    assert refreshed["counts"]["errors"] == 2
    assert {f["path"] for f in refreshed["findings"] if f["code"] == "hash_mismatch"} == {
        record["path"] for record in records
    }
    scoped = cli(root, "check", "--workstream", "line-a", expected_exit=1)
    assert scoped["counts"]["errors"] == 1
    assert scoped["counts"]["outside_scope"]["errors"] == 1


def test_reused_exact_pin_is_validated_by_save_not_file_existence(project: Path):
    """No repeated client hash is required; save still rejects changed bytes."""
    root = project
    target = evidence(root, "pin-reuse.txt", "Original synthetic evidence.\n")
    known_pin = pin(root, target)
    for changed in (False, True):
        prepared = cli(root, "record", "prepare", "--kind", "observation",
                       "--authority", "agent", "--created-by", "agent:test",
                       "--workstream", "line-a", "--idempotency-key", f"pin-reuse-{changed}")
        draft = root / prepared["path"]
        fm, template, _ = parse_markdown(draft)
        fm["summary"] = "Synthetic pin reuse"
        fm["refs"] = [known_pin]
        fm["limitations"] = ["Not a scientific result."]
        headings = re.findall(r"^## (.+)$", template, re.MULTILINE)
        draft.write_text(render_markdown(fm, "\n\n".join(
            f"## {heading}\n\nSynthetic recorded observation." for heading in headings
        )), encoding="utf-8")
        if changed:
            (root / target).write_text("Changed synthetic evidence.\n", encoding="utf-8")
        assert (root / target).is_file()
        canonical_before = tree(root / ".aitp/topic")
        result = subprocess.run(
            [sys.executable, "-I", str(PLUGIN / "scripts/aitp.py"), "record", "save",
             prepared["path"], "--expected-topic", "memory-example",
             "--exact-workstream", "line-a", "--json"],
            cwd=root, capture_output=True, text=True, timeout=15,
        )
        if changed:
            assert result.returncode != 0
            assert "hash_mismatch" in result.stdout + result.stderr
            assert tree(root / ".aitp/topic") == canonical_before
        else:
            assert result.returncode == 0, result.stdout + result.stderr
            assert json.loads(result.stdout)["status"] == "saved"
            cli(root, "check", "--workstream", "line-a")
            cli(root, "enter", "--workstream", "line-a")
