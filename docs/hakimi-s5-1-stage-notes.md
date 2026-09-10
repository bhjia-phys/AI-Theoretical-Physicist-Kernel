# Hakimi S5.1 atomic record-save gate notes

Date: 2026-09-01

This record closes only the reviewed S5.1 slice frozen in
[`docs/archive/hakimi-s5-1-atomic-record-save-spec.md`](archive/hakimi-s5-1-atomic-record-save-spec.md).
It is deterministic implementation evidence, not scientific validation, an
AITP roadmap-stage transition, or authorization for Hakimi S6.

## Frozen completion criterion

The slice passes when a checkpoint-bound Hakimi Entry save supplies the
captured Topic and exact singleton workstream through a versioned adapter
contract, and AITP compares both under the canonical write lock before any
Entry is persisted. A failed precondition must create no canonical Entry; an
identical retry with satisfied preconditions must retain the existing
`already_saved` result. CLI help, error codes, plugin/contract versions,
fixtures, tests, and both repositories' handoff documents must agree.

## Implemented boundary

- AITP 0.9.0 adds the optional paired, single-occurrence
  `record save --expected-topic <topic> --exact-workstream <workstream>`
  variant. The no-flag save path and success envelopes are unchanged.
- Inside the existing store lock, AITP reads the current Topic, reads and
  parses the exact draft bytes, enforces exact singleton workstream
  membership, performs the existing validation and idempotency decision, and
  then uses the existing atomic write.
- Deterministic failures are `invalid_save_precondition`,
  `topic_precondition_failed`, and `workstream_precondition_failed`. They
  preserve the draft and create no canonical Entry or side record.
- The adapter surface is `aitp/adapter-contract-0.2`. Hakimi may still consume
  0.1 for legacy non-checkpoint operations, but a checkpoint-bound save fails
  closed unless 0.2 is available.
- Hakimi derives both values from the immutable binding captured by its
  pending checkpoint. The model-facing tool does not accept caller-controlled
  Topic or workstream precondition fields.
- Canonical `show` and scoped `check` remain post-save defense in depth. The
  change adds no Entry/Note schema, read transport schema, registry, backfill,
  scientific judgment, or human-decision behavior.

## Deterministic evidence

### AITP

- Full unchanged-plus-S5.1 ledger suite:
  181 tests passed under Python 3.12 with bytecode and pytest cache
  disabled.
- Live source CLI help exposes the two paired flags on `record save`; repeated
  flags and an incomplete pair are rejected by tests.
- Adapter-contract tests bind schema `aitp/adapter-contract-0.2`, plugin
  version 0.9.0, current CLI help, unchanged live payload schema names, and the
  bundled Skill paths.
- Canonical runtime: 1,817 nonblank lines; largest module
  `records.py`: 396 nonblank lines. Both remain under the normative ceilings.
- All six official golden JSON fixtures are byte-identical in AITP and Hakimi.
- `git diff --check` passes.

### Hakimi

- S5.1 adapter, checkpoint, fixture, Research transition, and Goal integration
  selection: 6 files, 659 tests passed.
- Complete `@moonshot-ai/agent-core-v2` suite: 339 files, 5,823 tests passed,
  1 skipped. TypeScript typecheck and the 1,286-file import-boundary check pass.
- The formerly observed plugin temporary-directory cleanup flake passed alone:
  12 tests passed.
- Research-specific Node SDK and event-wiring selection: 16 passed; TUI
  Research selection: 459 passed; Web Research selection: 444 passed; Web
  typecheck passed.
- Web assets are reproducible: 521 files, source hash
  `112b5da0852fd0a20c313b39ea8a7e908322f36336ba2d8b61834ad6c2115427`.
- `git diff --check` passes.

One broader Node SDK file still has two non-Research failures in workspace
Skill discovery and gated MCP reporting. They reproduce when that file runs
alone, occur outside the S5.1 production/test hunks, and are not reclassified
as S5.1 evidence. The Research-specific SDK selection is green; the unrelated
defect remains a separately scoped repository gap.

## Plugin installation and fixture parity

The plugin manifest was refreshed with the repository helper, then both the
plugin and modified `using-aitp` Skill passed their validators. The installed
local plugin is
`aitp-research-protocol@aitp-protocol` version
`0.9.0+codex.20260901061711`. Source and installed-cache hashes match for the
plugin manifest, adapter contract, and `using-aitp` Skill.

The official fixture hashes match across repositories:

| Fixture | SHA-256 |
| --- | --- |
| `enter.json` | `173aa8f184381f9b6bb3697cbba7a1384c344f75f228f7f31044b7f49429d288` |
| `enter-after-save.json` | `5e124c56edccab7a3d29d23ceed6d1171fd63137e9b8d9b6b903fc38ccb3ce10` |
| `list.json` | `5f1cac638efc3dbb4b7e95e45a0cfa6fe099fcd1706e3ea99e40dc3418b8ea42` |
| `show.json` | `c670777653e6681e44d1cd05eb366a0af3e01501ecdf8770a6e143de106668fa` |
| `check.json` | `f055e846021cb82108023714894e4a9773ca4ff0a2d35d69adc496d85bd3086d` |
| `check-workstream.json` | `9b16f47c1833941c1103821b11863e21857084e0e2f084b9fc200cea32b00eb1` |

## Adjudication and limitations

The S5 strong canonical write-isolation gate passes. This claim covers
cooperating AITP writers using the canonical lock and checkpoint-bound Hakimi
saves using adapter-contract 0.2. Direct external edits are not an operating
system transaction, and reset/process-exit races can still require canonical
state inspection and same-identity recovery.

S6 remains unstarted. Native H6b method-distillation orchestration, external
dsh 0.9.0 consumption, M2 reviewed artifacts, M3 cross-Topic links/catalog,
and M4 collaborator protocol remain `planned / unavailable` under their own
review and natural-demand gates.
