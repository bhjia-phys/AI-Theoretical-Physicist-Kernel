# Atomic scoped Note save — implementation contract

2026-09-10. Authorized by the user's new finite Hakimi × AITP simplification
Goal. The AITP CLI implements the bounded behavior below. As of 2026-09-10
06:38 UTC, the matching 0.10.0/contract-0.3 bundle and Hakimi adapter are locally
installed and a new session reports ready. This is not a new roadmap stage;
the full integration Goal has a separate finite acceptance checklist.

## Existing gap and ownership

Before this change, `notes.save_note` read/validated before `store_lock`, then only checked
the final ID and writes inside the lock. `records.save_entry` already loads the
Topic, parses the exact draft and validates under the lock. Hakimi's old noteSave
passed only a draft path and cancellation signal. Pre/post reads cannot
substitute for comparing the captured scope at the canonical write boundary.

AITP owns this deterministic write primitive. Hakimi captures explicit Topic and
workstream before preparation and carries them through save/recovery; changing
Board focus is not permission to change the captured scope. No scientific
judgment, new record schema, automatic Note production or approval is added.

## Required CLI/API behavior

Add the optional paired, single-occurrence flags to existing `note save`:

```text
aitp note save <draft> --expected-topic <slug> --exact-workstream <slug>
```

The Python API takes equivalent optional keyword-only values. Reuse existing
slug grammar and deterministic error codes: invalid_save_precondition,
topic_precondition_failed, workstream_precondition_failed. Messages must name
Note where appropriate, not claim to be an Entry. Parser rejects repeated flags.
Both absent retains legacy unscoped/multi-workstream save, envelopes and file
format; one absent is invalid. These flags do not establish scientific membership
by inference, and a precondition failure never permits an unscoped fallback.

For a valid path under local drafts, the save critical section is:

1. Acquire the existing store lock; load the current STORE.toml Topic.
2. Compare expected Topic, when supplied, before accepting a retry.
3. Read/parse the exact draft text to be written; require raw workstreams to
   equal exactly [exact_workstream] when supplied.
4. Validate Note fields, evidence and relations against that locked Topic.
5. If canonical ID exists: identical bytes return already_saved; different
   bytes fail id_conflict. Otherwise atomically write the validated text.

No failure may modify canonical Note/Entry bytes or consume a draft. The lock
serializes cooperating writers, not arbitrary direct filesystem edits; this is
not OS isolation or a transaction over every referenced file. The legacy save
also moves its read/validation inside the lock, preserving ordinary behavior
while no longer using a stale pre-lock draft/Topic view.

## Retry and uncertainty

Notes retain their prepared ID; this does not add Entry-style idempotency keys.
If save may have succeeded, inspect that exact ID/path and compare the expected
content and scope before reporting success. Retrying the same retained draft
with satisfied preconditions returns already_saved, not another Note. Stale
preconditions still fail even for identical canonical bytes. Missing drafts or
unavailable evidence do not authorize generating a replacement Note silently.
Disk failures retain available draft/canonical evidence for explicit recovery;
do not promise exactly-once or discard unknown outcomes.

## Delivery and compatibility requirements

Source release is 0.10.0 / aitp/adapter-contract-0.3. Consumer inspection found
explicit schema allowlists and a version-equality check for atomic Entry saves;
0.3 must be added deliberately and Entry capability retained. Flags/descriptions,
version surfaces and CLI/help tests are synchronized on the AITP side. Do not
label old 0.2 consumers as supporting atomic Notes merely because they support
atomic Entries. Scoped
Hakimi Note saves must detect support and fail closed if absent, never silently
fall back. No breaking SDK deletion/major is authorized by this spec.

Frozen S5.1 remains historical: its exclusion of Note is unchanged there; this
new authorization extends Note independently. No M1b or M2/M3/M4 disposition
changes. Runtime remains within existing cumulative/module caps.

## Acceptance matrix

- working and theory Note success with exact bytes; identical retry one Note;
  changed same-ID draft fails without altering old bytes;
- legacy no-flag and multi-workstream success unchanged;
- incomplete/invalid pair; duplicate CLI flags; absent, multiple, malformed or
  wrong workstream; changed current Topic; draft Topic inconsistent with store;
- Topic/draft change before lock acquisition is checked after acquisition,
  including stale expectations on an already-saved retry;
- concurrent same-draft writers do not duplicate; distinct lines remain scoped;
- validation failure and injected atomic-write failure leave canonical state
  unchanged; simulated lost response can be recovered from same ID/draft;
- adapter captures scope before I/O, validates runtime capability, cancels safely,
  and never substitutes current browsing focus on retry;
- full ledger/contract/fixture tests and targeted Hakimi adapter/recovery tests;
  final installation and fresh-session proof separate from deterministic tests.

No real research store is changed by these tests. Prior passed tests may be
reused only for the exact unchanged requirement they demonstrate.

## Pre-implementation evidence

2026-09-10 isolated diagnostic:
`/tmp/aitp-note-lock-baseline-7ZmVO0/probe.py` invokes the current public
save_note implementation against a synthetic initialized store. An injected
lock wrapper changes STORE Topic and draft membership at lock entry. Save
returns saved with initial-topic/line-a while the current store/draft identify
changed-topic/line-b. This demonstrates stale pre-lock bytes being written,
not a measured incidence of corruption in a real project or an OS isolation
claim. This was the pre-implementation baseline; source-fix evidence follows.

## Source implementation evidence

Note save now reads/validates inside the existing lock and compares optional
Topic/exact singleton membership before validation and retry. Shared slug/pair
validation preserves the legacy Entry error wording. File/read schemas and
human review_state remain unchanged. The lock returns store_busy to overlapping
writers; it does not queue them. Retry after that rejection uses the same draft.

The initial new test failed because the API had no expected_topic parameter.
After implementation, a concurrency test incorrectly expected both callers to
succeed immediately; it now asserts the existing store_busy/no-duplicate
semantics, without changing the lock. A duplicate-flag wording assertion was
corrected to the existing parser message. The first targeted run passed 47
tests in 6.71 seconds. Further tests cover legacy locked reads, evidence/review
validation and distinct-line concurrent saves. Full ledger suite: 219 passed
in 44.76 seconds (single pytest worker; two tiny subprocesses only inside the
concurrency fixtures). Runtime 1,828 nonblank lines, largest module 396.
No scoped Hakimi Note-save or installed acceptance claim yet.
## 2026-09-10 consumer subprocess evidence

Current Hakimi launcher and node-local HostProcess invoked the real 0.10.0 CLI
in `/tmp/hakimi-note-cross-cli-IHbKNC/workspace-s7uJCE`: working/line-a and
theory/line-b prepare/save, exact retry, wrong Topic/workstream zero-addition,
same-ID changed-content rejection and scoped check (zero errors) passed.
Canonical Note IDs matched prepare IDs; save returns only status/path.
Probe: `/tmp/hakimi-note-cross-cli-IHbKNC/probe.mts`. Initial probe incorrectly
used save.id with Entry-only show; corrected evidence is the final run, not
that failed probe. Full model acceptance, unknown-response end-to-end recovery
and installation remain pending. See Hakimi's lean-harness-live-acceptance record.
