# CLI contracts and uncommon operations

Read this reference for bootstrap/backfill, transport compatibility, or a scoped
health/relationship ambiguity. Ordinary lookup does not require loading it.
Session maintenance belongs to ../SKILL.md; these command details do not add
another check cycle. Frozen-stage history below explains compatibility, not a
runtime workflow or new authorization.

## Current command map

Every command accepts `--cwd PATH` (default `.`) and `--json`. No `aitp
search` exists — `rg` over `.aitp/topic/` is the query path.

- `aitp init --topic <slug> --title "<title>"` — blank repository only;
  `--adopt` creates `.aitp/` inside an existing tree without touching
  content; `--dry-run` previews without writing.
- `aitp enter [--recent N] [--workstream <slug>]` — orientation at
  session start and before ending; `--recent` defaults to 20 and is a
  projection, not the whole ledger. The M1c `--workstream` flag (shipped;
  deterministic gate passed) takes a single slug and scopes the view to that
  research line (a repeated flag is parser-rejected misuse).
- `aitp check [--cwd PATH] [--json] [--workstream <slug>]` — read-only
  whole-store health validation; zero-write. No flag:
  `aitp/check-report-0.1` (byte-unchanged). The M1d single-occurrence
  `--workstream` flag emits the scoped `aitp/check-report-0.2`
  (shipped; deterministic gate passed) — see §M1d.
  Exit 0 clean / 1 findings / 2 cannot run or misuse, in both modes.
- `aitp inventory <path> --name <slug>` — operator-only M0.6 bootstrap tool
  (legacy scan + hash manifest); not part of routine session flow.
- `aitp backfill workstreams --mapping <path> --decision <entry-id> [--apply]`
  — M1e reviewed explicit workstream backfill for legacy records; dry-run by
  default, requires a human decision Entry that sha256-pins the mapping file
  (see §M1e).
- `aitp record prepare --kind <kind> --authority <level> --created-by <id>
  [--idempotency-key <key>] [--workstream <slug>]...` → `aitp record save
  <draft-path>`. When a host coordinator has already captured an explicit
  Topic plus singleton workstream binding for this Entry, it uses the 0.9.0
  compare-and-save variant `record save <draft-path> --expected-topic <topic>
  --exact-workstream <slug>`; both flags are required together and a failed
  precondition is a zero-canonical-write stop, never permission to retry
  unscoped or direct-write the ledger.
- `aitp note prepare --mode working|theory --title "<title>" --created-by
  <id> [--workstream <slug>]...` → `aitp note save <draft-path>`.

## M1a/M1b-R1 read commands — implemented (sync checklist)

The current CLI is `init`, `enter`, `inventory`, `backfill`, `record`,
`note`, `list`, `show`, and `check`. `check` is the read-only store-health command with two
read-only transports — `aitp/check-report-0.1` no-flag and
`aitp/check-report-0.2` scoped (M1d, §M1d) — while the **diagnosed file
schemas remain the shipped v0.1 ones** (`aitp/lite-entry-0.1`/
`aitp/lite-note-0.1`). The M1b-R1 baseline (no-flag `check`,
[`docs/archive/m1b-r1-spec.md`](../../../../../docs/archive/m1b-r1-spec.md))
shipped with its deterministic gate **passed** (evidence recorded in
`docs/archive/m1b-r1-stage-notes.md`). `lineage` is a deferred candidate — do not
invoke or teach it.
M1a is **done; deterministic gate passed**; the implementation evidence is in
[`docs/archive/m1a-stage-notes.md`](../../../../../docs/archive/m1a-stage-notes.md).

- `aitp list [--kind KIND] [--since DATE] [--workstream <slug>] [--json]`
  is the read-only retrieval
  projection. Use `--kind` for a kind filter and `--since` for an inclusive
  recorded-time filter; superseded Entries remain visible. Its JSON schema is
  `aitp/list-0.1`; with the M1c single-occurrence `--workstream` flag it is
  `aitp/list-0.2` (shipped; deterministic gate passed).
- `aitp show <entry-id> [--json]` opens one exact Entry. Its JSON schema is
  `aitp/show-0.1`. Do not emulate `show` with ad-hoc parsing.
- `aitp check [--cwd PATH] [--json] [--workstream <slug>]` validates the
  store read-only with two transports: no-flag `aitp/check-report-0.1`
  (byte-unchanged; whole store) and the M1d scoped flag variant
  `aitp/check-report-0.2` (§M1d; shipped; deterministic gate passed).
  Both: exit 0 clean, 1 findings, 2 cannot run (not a
  workspace, unreadable store metadata, or CLI misuse); zero-write (no lock,
  cache, index, repair, or migration); findings deterministic, sorted by
  `(path, code, message)`. The diagnosed file schemas stay the shipped v0.1
  ones (`aitp/lite-entry-0.1`/`aitp/lite-note-0.1`) in both transports. Run
  it before resuming a dense store; parse the report on exits 0 and 1;
  warnings are non-blocking.
- `aitp enter --json` uses `aitp/enter-0.2`: the latest active closeout with a
  non-empty `next_action` is the handoff; only without such a closeout does it
  fall back to another active Entry. Notes sort by recorded time. With the M1c
  single-occurrence `--workstream <slug>` flag the payload is `aitp/enter-0.3`
  (shipped; deterministic gate passed).
- `enter`'s text rendering is compact: two frozen M1a safety lines
  (`recent_entries: <shown> of <active> active (<omitted> omitted)`;
  `recent_notes: <shown>; latest_working_note: <id @ time|(none)>;
  active_newer: <n|unknown>`), a `goal_status: not_established`/`goal:` hint,
  an optional `handoff_status: review` hint, and a `warnings:` count pointing
  at `aitp check`. The goal and handoff hints are **structural**, not
  semantic — `goal_status` mirrors the normalized Research Goal placeholder
  and `handoff_status: review` only means a newer unresolved failure exists
  than the handoff; never read scientific staleness or quality into them.
  Machine output is the versioned JSON; never parse the text.
- A Note or Entry is `legacy_derived` only when its body first line is exactly:
  `> legacy-derived: recovery orientation only — not re-validated`
- `counts.malformed` counts records that could not be parsed or structurally
  validated at all. A record that parses but carries an invalid field value
  (for example an unparseable `created_at`) is reported as a separate
  field-level warning (`invalid_timestamp`) and is **not** counted in
  `counts.malformed`; the two can therefore differ, and `memory_status:
  available` can appear beside a non-empty `warnings:` count. Check the
  `warnings` detail (`aitp check`) instead of reading `malformed` as a
  total health count.
- `latest_working_note` and `active_newer_than_latest_working_note` are
  structural Note-age signals only, not semantic coverage or credibility.
- When four or more related durable Entries form a conclusion chain a returning
  session would otherwise reconstruct, consider a working Note. This is a Skill
  judgment, never a runtime rule.
- Also consider a working Note when `enter` reports `latest_working_note =
  None` while several recently recorded Entries depend on each other, or when
  the researcher asks what the actual current conclusion is. These are
  natural-use checks applied by Skill judgment, never by the runtime or by
  semantic rules.
- Keep `rg` over `.aitp/topic/` for full-text search. There is no
  `aitp search`; `list`/`show` are projections, not a semantic search engine.

M1b's exhaustive A–H + Followup roster, dispositions, and freeze rule remain
normative in [`docs/m1b-spec.md` §0.1](../../../../../docs/m1b-spec.md#01-authoritative-candidate-roster-and-current-dispositions).
The natural-use pause is complete and the 2026-08-12 reviewed freeze revision
([`docs/archive/m1b-adjudication.md`](../../../../../docs/archive/m1b-adjudication.md)) selected
the read-side slice **M1b-R1** — `aitp check` (no-flag
`aitp/check-report-0.1`) and a compact
`enter` text renderer — implemented per its
implementation-level spec
[`docs/archive/m1b-r1-spec.md`](../../../../../docs/archive/m1b-r1-spec.md); the deterministic
gate **passed** (evidence recorded in
`docs/archive/m1b-r1-stage-notes.md`). Do not teach or invoke the deferred candidates
(`based_on`/`used_by`, typed open items, pointer bundles, quick-run,
structured prepare, `lineage`) — they stay out of this Skill.

When a selected slice lands, sync the roadmap, README, Hakimi handoff, and
this command map in the same change; historical specs, adjudications, and
stage notes live frozen in `docs/archive/` and are not updated. A
selected capability that changes an unversioned success envelope must first use
a versioned envelope (preferred) or an explicit same-change Hakimi adapter
revision; never add a response key silently.

## M1c — Topic workstreams (shipped; deterministic gate passed)

The frozen implementation spec is
[`docs/archive/m1c-workstreams-spec.md`](../../../../../docs/archive/m1c-workstreams-spec.md)
(2026-08-13). Status: **done; deterministic gate passed** — the auditable
gate evidence is in
[`docs/m1c-stage-notes.md`](../../../../../docs/m1c-stage-notes.md).
M1c is independent of the frozen M1b roster
(`docs/m1b-spec.md` §0.1 dispositions unchanged) and of M3.

- `workstreams` is an **optional frontmatter list** on Entries and Notes
  (e.g. `workstreams: [crpa, magnetic-symmetry]`). A record without it is
  **unscoped legacy**: it appears only in the unfiltered global view and is
  excluded from every scoped view. A present field must be a non-empty,
  no-duplicate slug list (an empty list is invalid). Membership is explicit
  and multi-valued — never infer it from summary text, paths, kinds, or
  relations; a cross-line record lists all its workstreams.
- `record prepare`/`note prepare` accept a **repeatable** `--workstream
  <slug>` flag that seeds the draft's list in flag order; a repeated
  identical slug is rejected as a duplicate (no silent dedup); the
  prepare/save envelopes are unchanged. Slugs reuse the Topic slug rule
  `[a-z0-9][a-z0-9-]{0,62}`.
- `enter --workstream <slug>` and `list --workstream <slug>` emit the
  scoped schemas `aitp/enter-0.3`/`aitp/list-0.2`: the old payload plus one
  additive top-level singular `workstream` key, with entries/notes/counts
  filtered to strict exact membership (unscoped records are not in scope).
  The flag is single-occurrence on both read commands. **Relations run on
  the whole store first** — the superseded set and the resolved set are
  global, so a cross-line resolver/superseder still closes/replaces its
  target; then the projections, including the handoff (`next_action`), are
  strictly scoped — an out-of-scope handoff is never shown.
  `warnings`, `counts.malformed`,
  and `memory_status` stay global in scoped `enter`/`list`. **Without the
  flag the old schemas are byte-unchanged** (`aitp/enter-0.2`,
  `aitp/list-0.1`). The M1c "`check` has no scope flag" rule is superseded
  **for the flag variant only** (frozen M1c clause replaced per
  `docs/archive/m1d-workstream-health-spec.md` §Supersession); every other
  M1c clause stays in force and no-flag `check` is byte-unchanged. Note the
  frozen asymmetry: scoped `enter` `warnings` are **global**, while scoped
  `check` `counts.warnings` is **scoped**, with `outside_scope` carrying the
  global−scoped remainder (§M1d).
- No registry: there is no workstream file or command; enumerate slugs with
  `rg` over frontmatter when needed.
- In a dense multi-line store (e.g. GW_librpa running crpa,
  magnetic-symmetry, and qsgw-semiconductor lines sharing one
  source/build/provenance), scope `enter`/`list` to the line you are working
  on; unscoped legacy records stay global-only — they do not appear in a
  scoped view. When a record genuinely belongs to several lines, list all of
  them explicitly in `workstreams`.

## M1d — scoped `check` (shipped; deterministic gate passed)

The frozen implementation spec is
[`docs/archive/m1d-workstream-health-spec.md`](../../../../../docs/archive/m1d-workstream-health-spec.md)
(2026-08-14). Status: **done; deterministic gate passed** — the auditable
gate evidence is in
[`docs/m1d-stage-notes.md`](../../../../../docs/m1d-stage-notes.md)
(2026-08-14). M1d selects no M1b candidate; M1b/M1c frozen dispositions are
unchanged; the M1c "`check` has no scope flag" clause is superseded for the
flag variant only (§M1c; §Supersession in the spec).

- `check --workstream <slug>` takes **exactly one slug** (not a repeatable
  union): a repeated `--workstream` is parser-rejected misuse (exit 2,
  "may only be given once"); an invalid slug (or `""`) raises
  `invalid_workstreams` (exit 2 with the standard JSON error envelope under
  `--json`), same validation as the M1c read commands. The frozen help
  string is `only findings on records that explicitly list this workstream
  (single slug)`.
- Every run, scoped or not, scans the **whole store once** and computes the
  global report exactly as a no-flag run; the flag restricts only the
  report, never the scan. Relations are validated on the **global**
  `entry_map` first — an in-scope resolver/superseder whose target exists
  out-of-scope or unscoped validates cleanly (a cross-workstream resolver
  still closes its target); `missing_relation` fires only against the whole
  store.
- **Attribution (frozen)**: a finding is in the scoped view iff its path is
  an **admitted** record (parse and structure passed **and** the ID is
  unique — malformed and duplicate-ID files are never attributable) whose
  frontmatter `workstreams` **explicitly** contains the slug (strict exact
  membership, never inferred). Findings on out-of-scope, unscoped,
  malformed, duplicate-ID, and `TOPIC.md` records are excluded from every
  scoped view; they stay in the no-flag report and in `counts.outside_scope`.
  The scoped `findings` list is the globally sorted list restricted to
  attributable in-scope paths — same levels, codes, messages, `(path, code,
  message)` order; nothing is re-sorted, re-graded, or re-worded.
- Scoped `--json` is `aitp/check-report-0.2`: the complete 0.1 payload plus
  exactly three additive changes — one top-level **singular** `workstream:
  "<slug>"` key (appended last; there is no `workstreams` key anywhere),
  `counts.by_code`, and `counts.outside_scope`. Frozen key order: top level
  `schema, status, root, counts, findings, workstream`; inside `counts`:
  `entries, notes, errors, warnings, by_code, outside_scope` (no `malformed`
  key).
- Scoped `counts.entries`/`counts.notes` are the **admitted in-scope**
  canonical files (deliberately different from the global "count every
  canonical file" rule, because malformed files cannot be attributed to any
  scope). `counts.errors`/`counts.warnings` are the scoped findings by
  level; `status` is `"findings"` iff the scoped `findings` list is
  non-empty, else `"clean"`.
- **`by_code`** is a map `code → {"errors": n, "warnings": m}` over the
  scoped findings, keys sorted lexicographically by code, **always present**
  (`{}` on a clean scope). Buckets are per-level, so a code that grades as
  an error on one finding and a warning on another (e.g. `invalid_git_ref`)
  is tallied separately; the buckets sum exactly to `counts.errors`/
  `counts.warnings`/`len(findings)`. **`by_code` is a tally, not a
  diagnosis**: it never classifies a `hash_mismatch` as "expected historical
  pin drift" vs. "current evidence damage" — that is a human judgment
  informed by the tally, never a runtime call.
- **`counts.outside_scope`** is the derived level-delta
  `{"errors": n, "warnings": m}` = **global totals minus scoped totals**,
  per level, always present. It is not a finding: no paths, no codes, no
  `by_code` contribution, never in `findings`, never affects `status` or the
  exit code. It exists so a scoped report can never silently mask global
  findings — it names no workstream and labels nothing as "debt" or
  "damage". When `outside_scope` is large, run `aitp check` (no flag) for
  the whole store.
- Scoped text prints **exactly four stdout lines, always — including a
  clean scope** (stderr is empty on exits 0/1); details live in `--json`
  only, so scoped text never truncates:

  ```text
  workstream: <slug>
  check: <e> error(s), <w> warning(s)
  by_code: <compact JSON>
  outside_scope: <e> error(s), <w> warning(s) (run "aitp check" for the whole store)
  ```

  `by_code:` is the compact JSON serialization of `counts["by_code"]`
  (no indent), e.g. `by_code: {"hash_mismatch": {"errors": 2, "warnings":
  0}}`, and `by_code: {}` on a clean scope. No per-finding lines. The text
  is human-facing only — machine output is the versioned JSON; never parse
  the text.
- Exit codes, evaluated on the scoped report: `0` = zero scoped findings
  (the store may still have global findings — see `outside_scope`); `1` =
  at least one attributable in-scope error or warning; `2` = could not run
  (not a workspace, unreadable/invalid store metadata) or CLI misuse
  (repeated `--workstream`, invalid slug). Payload and exit are mutually
  consistent: non-empty scoped `findings` ⇒ exit 1, empty ⇒ exit 0.
  `outside_scope` never affects `status` or the exit code.
- **An empty scope is a valid result, not an error**: a well-formed slug
  with no admitted in-scope records yields counts 0, `findings` `[]`,
  `by_code` `{}`, `outside_scope` = the global totals, status `clean`,
  exit 0. **Unscoped legacy records are in no scope**: on a store whose
  records carry no `workstreams` (e.g. the GW_librpa legacy store), every
  scoped view is empty — a scoped `clean`/exit 0 may simply mean **nothing
  is attributable, not health**. Scoped health is meaningful only once
  records explicitly carry `workstreams` — new scoped records or a
  **reviewed manual backfill** (the runtime never backfills; a backfill
  only adds the explicit membership list, never content, and is a human
  decision, never automatic).
- **A scoped `clean`/exit 0 is not a whole-store health certificate**: it
  claims only "no attributable findings for this workstream". The no-flag
  run remains the whole-store instrument.
- **Deterministic baseline/delta is manual, not runtime**: `check` reports
  are deterministic in both modes (same store ⇒ byte-identical JSON/text;
  findings sorted by `(path, code, message)`; no wall-clock fields), so a
  baseline/delta reading is saving `check --json` outputs over time and
  `diff`/`rg`-ing them. There is **no report-comparison runtime** (deferred
  by the spec) — do not teach one.
- **Claims and boundaries**: M1d claims only deterministic implementation
  and read-only compatibility. It does **not** fix handoff staleness
  (closeout-first handoff is unchanged; roster H stays dropped), does not
  change exit-1 semantics (exit codes are byte-identical; the flag only
  gives recovery scripts a per-workstream signal), does not reduce write
  friction (structured prepare is Followup 6, deferred), and claims no
  behavioral, causal, or treatment-advantage evidence. `by_code` is never a
  drift-vs-damage classification and a scoped clean is never a health
  certificate.

## M1e — evidence lifecycle + reviewed backfill (shipped)

The frozen implementation spec is
[`docs/archive/m1e-evidence-lifecycle-backfill-spec.md`](../../../../../docs/archive/m1e-evidence-lifecycle-backfill-spec.md)
(2026-08-15). It changes no M1b/M1c/M1d disposition.

- **`sha256-once:`** is the mutable-target observation pin. Save verifies
  exactly like `sha256:`; later check drift is `historical_pin_drift`
  warning and a missing target is `historical_ref_missing` warning. Use it
  for live canonical files (`PROJECT_MEMORY.md`, execution-note pdf/zip,
  live status JSON) only when the historical record intentionally observes
  that mutable path. Immutable evidence and manifests stay `sha256:`; tracked
  source stays `git:`.
- **`check-policy`** is the optional reviewed store-local file
  `.aitp/local/check-policy.json` (schema `aitp/check-policy-0.1`) with
  `mutable` and `immutable` path-pattern lists. On legacy records that still
  use strict `sha256:`, a mutable match downgrades `hash_mismatch` to
  `historical_pin_drift` warning and `missing_ref` to
  `historical_ref_missing` warning; immutable matches and unmatched paths
  stay errors. No policy file ⇒ check output is byte-unchanged. The policy
  is explicit reviewed configuration, never runtime drift/damage inference.
- **`aitp backfill workstreams`** performs reviewed, explicit, idempotent
  backfill. The mapping file (schema `aitp/backfill-workstreams-0.1`) lists
  slugs and record IDs; `--decision` must be a human decision Entry whose
  `refs` sha256-pin the mapping file. The command only adds/merges the
  `workstreams` frontmatter block and preserves body and all other fields;
  it is dry-run by default and writes only with `--apply`. Never infer
  workstreams from paths or summaries — backfill only what the human-anchored
  mapping explicitly says.

### `check` exit codes in scripts — capture explicitly, fail closed on 2

Under `set -e`, a bare `aitp check` aborts the script on exit 1 before
`enter` can run; capture the exit code explicitly and branch. Exit 2
(cannot run: not a workspace, unreadable store metadata, misuse) means the
health state is unknown — **fail closed** on it, never treat it as clean:

```sh
set -e
code=0
report="$(aitp check --json 2>&1)" || code=$?
case "$code" in
  0) : ;;                                          # clean — proceed
  1) echo "check found findings; inspect the report" ;;  # non-blocking
  2) echo "check could not run; state unknown" >&2; exit 2 ;;  # fail closed
  *) echo "check exited with unexpected status $code; state unknown" >&2; exit 2 ;;  # fail closed (126/127 etc.)
esac
```

On exits 0 and 1 the check ran and the report is parseable; on exit 2 the
store state is unverified — do not proceed on unverified state. Scoped runs
behave the same, with the exit evaluated on the scoped report. `check`
never writes, so it is safe anywhere in a script.
