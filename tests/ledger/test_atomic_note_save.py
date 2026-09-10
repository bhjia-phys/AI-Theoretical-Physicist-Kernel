"""Atomic Note scope and recovery fixtures; no real research records."""
from contextlib import contextmanager
from concurrent.futures import ThreadPoolExecutor
import json

import pytest

import aitp.notes as notes
from aitp.core import AITPError, parse_markdown, render_markdown
from test_research_memory import cli, evidence, pin, project, tree
from test_atomic_record_save import run_cli


def draft(root, mode="working", scopes=None):
    source = evidence(root, f"basis-{mode}.txt", "Synthetic evidence only.")
    result = notes.prepare_note(root, mode, "Scoped synthesis", created_by="agent:test",
                                workstreams=scopes or ["line-a"])
    path = root / result["path"]
    fm, _, _ = parse_markdown(path)
    fm.update(summary="Synthetic synthesis", basis_refs=[pin(root, source)])
    body = "\n\n".join(f"## {h}\n\nSynthetic bounded claim." for h in notes.NOTE_SECTIONS[mode])
    path.write_text(render_markdown(fm, body))
    return path


def atomic(root, path, topic="memory-example", scope="line-a"):
    return notes.save_note(root, path, expected_topic=topic, exact_workstream=scope)


@pytest.mark.parametrize("mode", ["working", "theory"])
def test_scoped_save_retry_and_conflict(project, mode):
    path = draft(project, mode)
    saved = atomic(project, path)
    assert saved["status"] == "saved"
    assert atomic(project, path) == dict(saved, status="already_saved")
    final = project / saved["path"]
    original = final.read_bytes()
    assert original == path.read_bytes()
    fm, body, _ = parse_markdown(path)
    path.write_text(render_markdown(dict(fm, summary="Different content"), body))
    with pytest.raises(AITPError, match="Note ID already exists"):
        atomic(project, path)
    assert final.read_bytes() == original


@pytest.mark.parametrize("topic,scope,code", [
    (None, "line-a", "invalid_save_precondition"),
    ("memory-example", None, "invalid_save_precondition"),
    ("Bad", "line-a", "invalid_save_precondition"),
    ("memory-example", "Bad", "invalid_save_precondition"),
    ("other-topic", "line-a", "topic_precondition_failed"),
    ("memory-example", "line-b", "workstream_precondition_failed"),
])
def test_bad_precondition_zero_write(project, topic, scope, code):
    path = draft(project)
    before = tree(project)
    with pytest.raises(AITPError) as error:
        atomic(project, path, topic, scope)
    assert error.value.code == code
    assert tree(project) == before


@pytest.mark.parametrize("scopes", [None, [], ["line-a", "line-b"], ["line-a", "line-a"], "line-a"])
def test_exact_membership_is_not_subset_or_coercion(project, scopes):
    path = draft(project)
    fm, body, _ = parse_markdown(path)
    fm.pop("workstreams")
    if scopes is not None:
        fm["workstreams"] = scopes
    path.write_text(render_markdown(fm, body))
    before = tree(project)
    with pytest.raises(AITPError) as error:
        atomic(project, path)
    assert error.value.code == "workstream_precondition_failed"
    assert tree(project) == before


@pytest.mark.parametrize("change", ["topic", "draft"])
def test_scope_rechecked_inside_lock_even_on_retry(project, monkeypatch, change):
    path = draft(project)
    saved = atomic(project, path)
    original = (project / saved["path"]).read_bytes()
    real_lock = notes.store_lock
    @contextmanager
    def changed_at_lock(root):
        with real_lock(root):
            if change == "topic":
                store = root / ".aitp/STORE.toml"
                store.write_text(store.read_text().replace("memory-example", "changed-topic"))
            else:
                fm, body, _ = parse_markdown(path)
                path.write_text(render_markdown(dict(fm, workstreams=["line-b"]), body))
            yield
    monkeypatch.setattr(notes, "store_lock", changed_at_lock)
    with pytest.raises(AITPError) as error:
        atomic(project, path)
    assert error.value.code == ("topic_precondition_failed" if change == "topic" else "workstream_precondition_failed")
    assert (project / saved["path"]).read_bytes() == original


def test_lost_response_retry_and_write_failure(project, monkeypatch):
    path = draft(project)
    before = tree(project)
    real_write = notes.atomic_write
    def fail(*args):
        raise OSError("synthetic disk failure")
    monkeypatch.setattr(notes, "atomic_write", fail)
    with pytest.raises(OSError, match="synthetic disk failure"):
        atomic(project, path)
    assert tree(project) == before
    def response_lost(*args):
        real_write(*args)
        raise OSError("synthetic response lost after write")
    monkeypatch.setattr(notes, "atomic_write", response_lost)
    with pytest.raises(OSError, match="response lost"):
        atomic(project, path)
    monkeypatch.setattr(notes, "atomic_write", real_write)
    assert atomic(project, path)["status"] == "already_saved"
    assert len(list((project / ".aitp/topic/notes").glob("note-*.md"))) == 1


def test_legacy_save_reads_draft_and_topic_after_lock(project, monkeypatch):
    path = draft(project)
    real_lock = notes.store_lock
    @contextmanager
    def changed_at_lock(root):
        with real_lock(root):
            store = root / ".aitp/STORE.toml"
            store.write_text(store.read_text().replace("memory-example", "changed-topic"))
            fm, body, _ = parse_markdown(path)
            path.write_text(render_markdown(dict(fm, topic="changed-topic", workstreams=["line-b"]), body))
            yield
    monkeypatch.setattr(notes, "store_lock", changed_at_lock)
    saved = notes.save_note(project, path)
    final = project / saved["path"]
    fm, _, _ = parse_markdown(final)
    assert fm["topic"] == "changed-topic"
    assert fm["workstreams"] == ["line-b"]
    assert final.read_bytes() == path.read_bytes()


@pytest.mark.parametrize("failure", ["topic", "evidence", "review"])
def test_scoped_save_retains_full_note_validation(project, failure):
    path = draft(project)
    fm, body, _ = parse_markdown(path)
    if failure == "topic":
        fm["topic"] = "wrong-topic"
    elif failure == "review":
        fm["review_state"] = "approved"
    else:
        (project / fm["basis_refs"][0]["target"]).write_text("Changed evidence")
    path.write_text(render_markdown(fm, body))
    before = tree(project)
    with pytest.raises(AITPError) as error:
        atomic(project, path)
    assert error.value.code == {"topic": "topic_mismatch", "review": "review_required", "evidence": "hash_mismatch"}[failure]
    assert tree(project) == before


def test_different_line_writers_do_not_exchange_membership(project):
    paths = [draft(project), draft(project, "theory", ["line-b"])]
    scopes = ["line-a", "line-b"]
    def invoke(i):
        return run_cli(project, "note", "save", str(paths[i]), "--expected-topic", "memory-example",
                       "--exact-workstream", scopes[i], "--json")
    with ThreadPoolExecutor(max_workers=2) as pool:
        responses = list(pool.map(invoke, range(2)))
    for i, response in enumerate(responses):
        result = json.loads(response.stdout)
        if response.returncode == 2:
            assert result["code"] == "store_busy"
            result = json.loads(invoke(i).stdout)
        assert result["status"] == "saved"
        fm, _, _ = parse_markdown(project / result["path"])
        assert fm["workstreams"] == [scopes[i]]
    assert len(list((project / ".aitp/topic/notes").glob("note-*.md"))) == 2


def test_cli_pair_duplicates_legacy_and_concurrent_retry(project):
    path = draft(project)
    # The existing lock rejects overlapping writers with store_busy, not a wait.
    args = ("note", "save", str(path), "--expected-topic", "memory-example", "--exact-workstream", "line-a")
    with ThreadPoolExecutor(max_workers=2) as pool:
        responses = list(pool.map(lambda _: run_cli(project, *args, "--json"), range(2)))
    results = [json.loads(r.stdout) for r in responses]
    assert sum(r["status"] == "saved" for r in results) == 1
    for response, result in zip(responses, results):
        if response.returncode == 2:
            assert result["code"] == "store_busy"
        else:
            assert response.returncode == 0
            assert result["status"] in {"saved", "already_saved"}
    assert cli(project, *args)["status"] == "already_saved"
    for flag, value in [("--exact-workstream", "line-a"), ("--expected-topic", "memory-example")]:
        duplicate = run_cli(project, *args, flag, value, "--json")
        assert duplicate.returncode == 2
        assert "may only be given once" in duplicate.stderr
    multi = draft(project, "theory", ["line-a", "line-b"])
    assert cli(project, "note", "save", str(multi))["status"] == "saved"
