# Hakimi S5.1: atomic scoped `record save` (frozen 2026-09-01)

Status: **reviewed and authorized for implementation** by the human request
"继续当前 goal，按 S5.1 实现". This is a narrow, integration-driven AITP
0.9.0 change, not an M2/M3/M4 stage and not authorization for Hakimi S6.

## Objective and completion criterion

Close the one write-isolation gap that blocks the Hakimi Unified Research Mode
S5 strong gate: a checkpoint-bound Entry must not become canonical unless the
current AITP Topic and the exact singleton workstream membership still match
the binding captured by Hakimi.

Completion requires the CLI, error and retry semantics, adapter contract,
Hakimi adapter, fixtures/provenance, tests, README/current-state text, and both
cross-repository handoffs to agree. The unchanged AITP suite and targeted
Hakimi Research tests must pass, followed by the normal cross-repository S5
verification gate.

## Scope and non-goals

In scope:

- one optional compare-and-save variant of `aitp record save`;
- atomic Topic and exact singleton-workstream preconditions;
- deterministic errors and retry behavior;
- adapter-contract `0.2`, AITP plugin `0.9.0`, and the thin Hakimi adapter use;
- defense-in-depth post-save `show`/`check`, unchanged from S5.

Out of scope:

- `note save`, prepare semantics, Entry/Note file schemas, Topic mutation,
  backfill, lineage, structured prepare, method-card rules, human decisions,
  scheduler/artifact services, M2/M3/M4, H6b, and Hakimi S6;
- a new success envelope, warning field, registry, daemon, lock service, or
  direct Hakimi write to `.aitp` canonical files.

Allowed implementation files are the AITP runtime/CLI, adapter contract,
version surfaces, tests and current-state/handoff documentation, plus the
Hakimi AITP adapter/checkpoint path, its tests/fixture provenance, and its
current-state/handoff documentation. Existing dirty changes must be preserved.

## Frozen CLI and API contract

The additive CLI form is:

```text
aitp record save <draft> \
  --expected-topic <topic-slug> \
  --exact-workstream <workstream-slug>
```

The Python API adds keyword-only `expected_topic` and `exact_workstream`
arguments. Both are optional, but they must be supplied together. Omitting both
selects the legacy save path. Each CLI flag is single-occurrence. Both values
use the existing lowercase slug grammar.

The compare-and-save variant executes these steps under the existing AITP
store write lock, in this order:

1. load the current `STORE.toml` Topic identity;
2. reject a current Topic different from `expected_topic`;
3. read and parse the exact draft bytes that may be written;
4. require raw `workstreams` to equal exactly `[exact_workstream]`;
5. run the existing complete Entry and evidence validation against the locked
   Topic identity;
6. apply the existing ID-conflict / byte-identical retry decision;
7. atomically write those validated bytes when no canonical Entry exists.

The lock only serializes cooperating AITP writers; it does not claim an OS
transaction against arbitrary direct edits. Hakimi and other adapters remain
forbidden from direct canonical writes.

## Frozen errors, compatibility, and idempotency

All failures use the existing exit-2 `AITPError` JSON/text envelope. New codes:

- `invalid_save_precondition`: the pair is incomplete or a value is not a
  valid slug;
- `topic_precondition_failed`: the locked current Topic differs from the
  caller's expected Topic;
- `workstream_precondition_failed`: the draft has no `workstreams`, more than
  one, a different slug, or any other value not exactly equal to the singleton
  expectation.

Failure creates no canonical Entry and no idempotency side record. The draft is
preserved. A retry of the same draft with the same satisfied preconditions
returns the existing exact success envelope
`{"status":"already_saved","path":...}`. Preconditions are checked before
that retry short-circuit, so stale expectations never obtain a false success.
The legacy no-precondition success envelopes and `note save` are unchanged.

The machine adapter surface becomes `aitp/adapter-contract-0.2`; unknown
contract schemas still fail closed. Hakimi may continue read/general-write
compatibility with `0.1`, but a checkpoint-bound save requires `0.2` and passes
both preconditions from the captured confirmed binding. Model input does not
gain caller-controlled Topic/workstream precondition fields.

## Verification and stop conditions

Required AITP verification:

- legacy save and full ledger suite;
- CLI help/contract/version synchronization;
- pair, slug, Topic mismatch, exact-membership mismatch, zero-canonical-write,
  same-draft retry, stale retry, ID conflict, and lock-bound re-read tests;
- module `< 400` nonblank lines and cumulative runtime `< 2,000` nonblank
  lines; `git diff --check`.

Required Hakimi verification:

- adapter `0.1` compatibility and `0.2` capability detection;
- exact argv for checkpoint-bound versus ordinary saves;
- precondition failures preserve the pending checkpoint and do not invent a
  save receipt;
- canonical retry/recovery and post-save defense barriers;
- targeted Agent Core tests/typecheck and the established S5 public-surface
  gate, without entering S6.

Stop immediately on any need for a new file/transport schema, changed success
envelope, changed human-decision semantics, direct canonical write, ambiguous
dirty overlap, or expansion beyond this slice.
