"""Hakimi S5.1 atomic Topic/exact-workstream ``record save`` contract."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from contextlib import contextmanager
from pathlib import Path

import pytest

import aitp.records as records
from aitp.core import (
    AITPError,
    atomic_write,
    init_workspace,
    parse_markdown,
    prepare_entry,
    render_markdown,
    save_entry,
)


BODY = """\
## Durable Summary

The bounded decision is recorded.

## Decision And Alternatives

The scoped alternative was selected.

## Reason, Scope, And Revisit Condition

Revisit if the Topic or workstream changes.
"""


def initialized(tmp_path: Path) -> Path:
    root = tmp_path / "project"
    root.mkdir()
    init_workspace(root, "nio", "Magnetic NiO")
    return root


def filled_draft(root: Path, workstreams: list[str] | None = None) -> Path:
    prepared = prepare_entry(
        root,
        "decision",
        "agent",
        created_by="agent:test",
        workstreams=workstreams,
    )
    path = root / prepared["path"]
    frontmatter, _, _ = parse_markdown(path)
    frontmatter.update(
        summary="The bounded decision is recorded.",
        next_action="Continue only in the confirmed scope.",
    )
    atomic_write(path, render_markdown(frontmatter, BODY))
    return path


def canonical_entries(root: Path) -> list[Path]:
    return sorted((root / ".aitp" / "topic" / "entries").glob("entry-*.md"))


def run_cli(root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(
        Path(__file__).parents[2]
        / "plugins"
        / "aitp-research-protocol"
        / "scripts"
        / "vendor"
    )
    return subprocess.run(
        [sys.executable, "-m", "aitp", *args],
        cwd=root,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def test_compare_and_save_success_and_same_precondition_retry(tmp_path: Path) -> None:
    root = initialized(tmp_path)
    draft = filled_draft(root, ["crpa"])

    first = save_entry(root, draft, expected_topic="nio", exact_workstream="crpa")
    second = save_entry(root, draft, expected_topic="nio", exact_workstream="crpa")

    assert first == {"status": "saved", "path": first["path"]}
    assert second == {"status": "already_saved", "path": first["path"]}
    assert len(canonical_entries(root)) == 1


def test_write_failure_and_lost_response_retry_keep_one_scoped_entry(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = initialized(tmp_path)
    draft = filled_draft(root, ["crpa"])
    draft_bytes = draft.read_bytes()
    real_write = records.atomic_write

    def fail_before_write(*args):
        raise OSError("synthetic disk failure")

    monkeypatch.setattr(records, "atomic_write", fail_before_write)
    with pytest.raises(OSError, match="synthetic disk failure"):
        save_entry(root, draft, expected_topic="nio", exact_workstream="crpa")
    assert canonical_entries(root) == []
    assert draft.read_bytes() == draft_bytes

    def lose_response_after_write(*args):
        real_write(*args)
        raise OSError("synthetic response lost after write")

    monkeypatch.setattr(records, "atomic_write", lose_response_after_write)
    with pytest.raises(OSError, match="response lost"):
        save_entry(root, draft, expected_topic="nio", exact_workstream="crpa")
    saved = canonical_entries(root)
    assert len(saved) == 1
    saved_bytes = saved[0].read_bytes()
    monkeypatch.setattr(records, "atomic_write", real_write)
    # Even a saved retry must not acquire another workstream's identity.
    with pytest.raises(AITPError) as error:
        save_entry(root, draft, expected_topic="nio", exact_workstream="qsgw")
    assert error.value.code == "workstream_precondition_failed"
    result = save_entry(root, draft, expected_topic="nio", exact_workstream="crpa")
    assert result["status"] == "already_saved"
    assert canonical_entries(root) == saved
    assert saved[0].read_bytes() == saved_bytes
    assert draft.read_bytes() == draft_bytes


def test_legacy_save_envelope_is_unchanged(tmp_path: Path) -> None:
    root = initialized(tmp_path)
    draft = filled_draft(root, ["crpa", "qsgw"])

    saved = save_entry(root, draft)

    assert saved == {"status": "saved", "path": saved["path"]}
    assert save_entry(root, draft) == {
        "status": "already_saved",
        "path": saved["path"],
    }


@pytest.mark.parametrize(
    ("expected_topic", "exact_workstream", "message"),
    [
        ("nio", None, "requires both expected_topic and exact_workstream"),
        (None, "crpa", "requires both expected_topic and exact_workstream"),
        ("Bad", "crpa", "expected_topic must use lowercase"),
        ("nio", "Bad", "exact_workstream must use lowercase"),
    ],
)
def test_invalid_precondition_pair_or_slug_is_zero_write(
    tmp_path: Path,
    expected_topic: str | None,
    exact_workstream: str | None,
    message: str,
) -> None:
    root = initialized(tmp_path)
    draft = filled_draft(root, ["crpa"])

    with pytest.raises(AITPError, match=message) as error:
        save_entry(
            root,
            draft,
            expected_topic=expected_topic,
            exact_workstream=exact_workstream,
        )

    assert error.value.code == "invalid_save_precondition"
    assert canonical_entries(root) == []
    assert draft.is_file()


def test_locked_topic_mismatch_is_zero_write_even_on_saved_retry(tmp_path: Path) -> None:
    root = initialized(tmp_path)
    draft = filled_draft(root, ["crpa"])
    save_entry(root, draft, expected_topic="nio", exact_workstream="crpa")
    store = root / ".aitp" / "STORE.toml"
    store.write_text(
        store.read_text(encoding="utf-8").replace('topic_id = "nio"', 'topic_id = "mno"'),
        encoding="utf-8",
    )

    with pytest.raises(AITPError, match="expected nio, found mno") as error:
        save_entry(root, draft, expected_topic="nio", exact_workstream="crpa")

    assert error.value.code == "topic_precondition_failed"
    assert len(canonical_entries(root)) == 1


def test_topic_is_reread_inside_lock_before_write(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = initialized(tmp_path)
    draft = filled_draft(root, ["crpa"])
    store = root / ".aitp" / "STORE.toml"
    real_lock = records.store_lock

    @contextmanager
    def editing_lock(store_root: Path):
        with real_lock(store_root):
            store.write_text(
                store.read_text(encoding="utf-8").replace(
                    'topic_id = "nio"', 'topic_id = "mno"'
                ),
                encoding="utf-8",
            )
            yield

    monkeypatch.setattr(records, "store_lock", editing_lock)

    with pytest.raises(AITPError) as error:
        save_entry(root, draft, expected_topic="nio", exact_workstream="crpa")

    assert error.value.code == "topic_precondition_failed"
    assert canonical_entries(root) == []


@pytest.mark.parametrize("workstreams", [None, ["qsgw"], ["crpa", "qsgw"]])
def test_exact_workstream_mismatch_is_zero_write(
    tmp_path: Path, workstreams: list[str] | None
) -> None:
    root = initialized(tmp_path)
    draft = filled_draft(root, workstreams)

    with pytest.raises(AITPError, match="do not exactly match") as error:
        save_entry(root, draft, expected_topic="nio", exact_workstream="crpa")

    assert error.value.code == "workstream_precondition_failed"
    assert canonical_entries(root) == []
    assert draft.is_file()


def test_draft_is_reread_inside_lock_before_write(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    root = initialized(tmp_path)
    draft = filled_draft(root, ["crpa"])
    real_lock = records.store_lock

    @contextmanager
    def editing_lock(store_root: Path):
        with real_lock(store_root):
            frontmatter, _, _ = parse_markdown(draft)
            frontmatter["workstreams"] = ["crpa", "qsgw"]
            atomic_write(draft, render_markdown(frontmatter, BODY))
            yield

    monkeypatch.setattr(records, "store_lock", editing_lock)

    with pytest.raises(AITPError) as error:
        save_entry(root, draft, expected_topic="nio", exact_workstream="crpa")

    assert error.value.code == "workstream_precondition_failed"
    assert canonical_entries(root) == []


def test_satisfied_preconditions_preserve_existing_id_conflict(tmp_path: Path) -> None:
    root = initialized(tmp_path)
    draft = filled_draft(root, ["crpa"])
    saved = save_entry(root, draft, expected_topic="nio", exact_workstream="crpa")
    canonical = root / saved["path"]
    original = canonical.read_bytes()
    frontmatter, _, _ = parse_markdown(draft)
    atomic_write(draft, render_markdown(frontmatter, BODY.replace("bounded", "reviewed")))

    with pytest.raises(AITPError) as error:
        save_entry(root, draft, expected_topic="nio", exact_workstream="crpa")

    assert error.value.code == "id_conflict"
    assert canonical.read_bytes() == original


def test_cli_compare_and_save_and_error_envelope(tmp_path: Path) -> None:
    root = initialized(tmp_path)
    draft = filled_draft(root, ["crpa"])
    relative = str(draft.relative_to(root))

    missing_pair = run_cli(
        root,
        "record", "save", relative,
        "--expected-topic", "nio",
        "--json",
    )
    assert missing_pair.returncode == 2
    assert json.loads(missing_pair.stdout)["code"] == "invalid_save_precondition"
    assert canonical_entries(root) == []

    saved = run_cli(
        root,
        "record", "save", relative,
        "--expected-topic", "nio",
        "--exact-workstream", "crpa",
        "--json",
    )
    assert saved.returncode == 0, saved.stderr
    assert json.loads(saved.stdout)["status"] == "saved"


def test_cli_repeated_precondition_flag_is_parser_rejected(tmp_path: Path) -> None:
    root = initialized(tmp_path)
    draft = filled_draft(root, ["crpa"])
    result = run_cli(
        root,
        "record", "save", str(draft.relative_to(root)),
        "--expected-topic", "nio",
        "--expected-topic", "nio",
        "--exact-workstream", "crpa",
        "--json",
    )

    assert result.returncode == 2
    assert result.stdout == ""
    assert "may only be given once" in result.stderr
    assert canonical_entries(root) == []


@pytest.mark.parametrize("scopes", [("crpa", "qsgw"), ("response", "response-check")])
def test_interleaved_cli_clients_keep_pending_results_and_handoffs_scoped(
    tmp_path: Path, scopes: tuple[str, str]
) -> None:
    """Separate CLI invocations share a Topic, not a mutable 'current' scope.

    A prepares first; B saves while A is pending; A returns later. This tests
    the ledger transport, not Hakimi session state or simultaneous scheduling.
    Every canonical write goes through record save; only local drafts are filled.
    """
    root = initialized(tmp_path)

    def command(*args: str, exit_code: int = 0) -> dict:
        result = run_cli(root, *args, "--json")
        assert result.returncode == exit_code, (result.stdout, result.stderr)
        return json.loads(result.stdout)

    def snapshot() -> dict[str, bytes]:
        return {str(p.relative_to(root)): p.read_bytes() for p in canonical_entries(root)}

    drafts: list[str] = []
    ids: list[str] = []
    for index, scope in enumerate(scopes):
        prepared = command(
            "record", "prepare", "--kind", "decision", "--authority", "agent",
            "--created-by", f"agent:client-{index}",
            "--idempotency-key", f"client-{index}-pending-result",
            "--workstream", scope,
        )
        path = root / prepared["path"]
        frontmatter, _, _ = parse_markdown(path)
        frontmatter.update(
            summary="Identically named bounded result.",
            created_at=f"2026-01-0{index + 1}T00:00:00Z",
            next_action=f"Continue only {scope}.",
        )
        atomic_write(path, render_markdown(frontmatter, BODY))
        drafts.append(prepared["path"])
        ids.append(frontmatter["id"])

    def save(index: int, scope: str, exit_code: int = 0) -> dict:
        return command(
            "record", "save", drafts[index], "--expected-topic", "nio",
            "--exact-workstream", scope, exit_code=exit_code,
        )

    pending_a = (root / drafts[0]).read_bytes()
    assert save(1, scopes[1])["status"] == "saved"
    b_only = snapshot()
    assert len(b_only) == 1
    assert command("list", "--workstream", scopes[0])["entries"] == []
    assert command("enter", "--workstream", scopes[0])["next_action"] == {
        "status": "not_established", "source": None,
    }
    assert (root / drafts[0]).read_bytes() == pending_a

    # A cannot inherit the most recently used scope or a similarly named scope.
    assert save(0, scopes[1], exit_code=2)["code"] == "workstream_precondition_failed"
    assert snapshot() == b_only
    assert (root / drafts[0]).read_bytes() == pending_a
    assert save(0, scopes[0])["status"] == "saved"
    both = snapshot()
    assert len(both) == 2
    assert all(both[path] == content for path, content in b_only.items())

    # Fresh processes, A -> B -> A: no cached scope, handoff or duplicate save.
    for index in (0, 1, 0):
        scope = scopes[index]
        listed = command("list", "--workstream", scope)
        assert [entry["id"] for entry in listed["entries"]] == [ids[index]]
        entered = command("enter", "--workstream", scope)
        assert entered["schema"] == "aitp/enter-0.3"
        assert entered["workstream"] == scope
        assert entered["next_action"]["entry_id"] == ids[index]
        shown = command("show", ids[index])
        assert shown["frontmatter"]["topic"] == "nio"
        assert shown["frontmatter"]["workstreams"] == [scope]
        assert shown["frontmatter"]["created_by"] == f"agent:client-{index}"
        assert shown["frontmatter"]["idempotency_key"] == f"client-{index}-pending-result"
        checked = command("check", "--workstream", scope)
        assert checked["counts"]["entries"] == 1  # Not an empty-scope false clean.
        assert checked["counts"]["errors"] == 0
        assert save(index, scope)["status"] == "already_saved"
        assert snapshot() == both

    assert {entry["id"] for entry in command("list")["entries"]} == set(ids)
