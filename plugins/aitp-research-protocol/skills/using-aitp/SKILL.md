---
name: using-aitp
description: "Recover and maintain evidence-grounded research memory with AITP files and CLI. Use at project resumption, after durable research changes, and for evidence-based working/theory Notes. Keep session-boundary state current with zero writes for no durable delta; route recurring methods and card trials to distilling-methods. Best-effort guidance, not a runtime hook."
---

# Using AITP

AITP stores recorded understanding, not scientific truth. Use its public CLI
and ordinary files; the host owns orchestration and execution permissions.

## Entry point and on-demand detail

Resolve `../../scripts/aitp.py` relative to this file to an absolute path.
Before invoking the CLI, reuse a verified absolute path to Python 3.11 or newer,
or discover candidates with `command -v python3.13 python3.12 python3.11 python3`.
Check each available candidate with `-c 'import sys; print(sys.executable); raise SystemExit(sys.version_info < (3, 11))'`;
keep the first passing interpreter path. Do not test compatibility by failing an
AITP command through an unverified `python3`. No match: report the missing runtime;
do not replace system Python or install packages without permission.
Below, `aitp` abbreviates that interpreter plus bundled script.
A known installed path is sufficient; do not rediscover it on each call.
Host Skill visibility and tool permissions still apply; this guide does not
authorize changing Research Mode, bypassing a denied operation, or extra work.

Read only the reference that the task requires:

- [Research memory](references/research-memory.md): multi-line recovery,
  disputed handoffs, Topic maps, synthesis or detailed derivation/manuscript writing.
- [Recording](references/recording.md): before preparing/saving an Entry or Note,
  including evidence-lifecycle pins, immutable pointers and retry handling.
- [CLI contracts](references/cli-contracts.md): bootstrap/backfill, transport
  compatibility, or uncertainty about scoped health/relationship semantics.
- [Distilling methods](../distilling-methods/SKILL.md): when its stable-procedure
  trigger or existing-card trial review applies. It alone owns the card rules.

Do not load all references for each task. Already read, unchanged instructions
and evidence remain usable within the session.

## Start or resume work

At project entry/resumption obtain `enter` and `check`, or reuse an explicitly
fresh matching host report. Ordinary follow-up turns are not new resumptions.
For several lines in one Topic, use one global `check` plus each line's scoped
`enter`; read the complete global report as global, never relabel it scoped or
infer membership/cleanliness from omitted findings. Single-line work may use
scoped `check`. Never run one full check per line merely to navigate a project.
Explicit workstream membership is authoritative. Never infer it from a path,
shared code, citation, material name or similar slug. Unscoped old records are
background, not silently assigned members of a line.

Useful read operations (add `--cwd PATH` when needed):

```text
aitp enter --workstream <slug> --recent 3 --json
aitp check --workstream <slug> --json
aitp list --workstream <slug> --since <recorded-time> --json
aitp show <entry-id> --json
```

Use the global variant when scope is unknown or whole-project context is needed.
The positive `--recent` limit is an orientation window, not proof of absence;
choose it for the question and search beyond it when necessary.
`list/show` expose Entries only: read Notes at the exact file path, normally
`latest_working_note.source`. Use targeted `rg` over Markdown for discovery.
There is no search engine, Note-show, Topic-update, lineage or card registry.

For current progress or remaining gaps, keyword hits are locators, not a current
state summary. Use a matched record's explicit workstream to recover relevant
later Entries and the Working Note; do not stop at an old "not implemented" or
"next action". Distinguish implementation, synthetic tests, real runs and physical
validation. If later coverage is unknown, say "as of this record", not "still missing".
Read evidence behind relied-on claims and relevant objections/decisions. The newest
Note is not automatically complete; `--since` filters recorded time, not semantic
coverage. An unchanged job poll does not need this reconstruction again.
Report explicit metadata/body contradictions; do not explain away stale wording
merely because a charitable interpretation is possible.

### Health and interpretation

- `check`: exit0 clean; exit1 findings (inspect them, not a failed invocation);
  exit2 cannot run/misuse: fail closed on exit 2 and stop relying on that projection. Unexpected exits also
  leave state unknown. Capture exit status explicitly; a pipe or `set -e` must
  not hide it or prevent required handling.
- A scoped check still scans the entire store. It attributes findings only to
  valid, unique records explicitly in that workstream. Empty scope can be clean
  because nothing is attributable. `outside_scope` is the global remainder,
  not another finding or a scientific failure of this line. Inspect/reuse the
  global report when that remainder needs investigation; do not loop checks
  over every line as a cheap inventory.
- `enter/list` warnings remain global even when scoped. `memory_status` and
  Goal/handoff/Note-age hints are structural, not health or scientific judgment.
  Field warnings are not necessarily `malformed` parse failures.
- `next_action` is a recorded closeout-first handoff, not an instruction to
  execute. Compare newer relevant evidence before following it; a newer result
  does not resume a paused Goal or cancel a human decision.
- Relations are computed globally before scoped projection. Only active Entries
  contribute `resolves`; a superseded resolver's successor does not inherit its
  edge. Confirm disputed closure through canonical `show`, not old prose.
- Explain relevant pin errors without relabeling old evidence or hiding damage.
  A historical mismatch does not itself refute a physical claim; it does limit
  which source version was verified. Do not edit old pins to obtain clean output.

### Keep the interaction small

Execute independent reads in one tool batch when the host supports it: for
example initial enter/check, or already identified Note/Entry/source reads.
A dependent lookup waits for its locator; prepare must finish before draft
editing, and save before post-save verification. Do not mix dependent writes
into a batch or bypass host ordering/permissions.

Keep a complete check report and its exit code accessible, but avoid feeding
hundreds of unrelated findings into every model round. With ordinary host
output capture or a temporary noncanonical report, inspect the public JSON:
start with schema/status/counts and exact findings affecting the relied-on
records. Retain the full report location and disclose omissions/outside scope.
This is an on-demand view, not a replacement validator or semantic classifier.
Never truncate first and then treat missing errors as absent. If complete
capture is unavailable, use the complete CLI result rather than hiding errors.
Reuse that report for details; do not rerun check merely to obtain another format.
Reuse current enter/check across preparation, ordinary follow-ups and closeout
only within the same known-unchanged work interval. Record the root, Topic,
scope, exit status and report location in context, not a new ledger or cache.
Ledger/Topic/policy/referenced-file changes, a different root, resumed work,
concurrent writers, failed reads or uncertain freshness require refreshing the
affected view. Draft-only preparation/edits do not invalidate it. A scoped report
does not cover another scope. Save validation and post-save checks are never skipped.

For ordinary recall, read the located record; do not add a standalone hash check
to every Entry, Note or artifact read. Existence is enough for locating a file,
not for asserting its version or scientific validity. Compute a digest only to
construct a required new pin, verify a claimed historical version, or investigate
a relevant integrity finding; reuse an already verified digest for the same
unchanged target. Let save/check perform their mandatory validation rather than
duplicating it with shell audits. See Recording for safe pin reuse.

Answer with the question, supported conclusion and limits, what changed, and
the smallest useful next step. Include exact evidence locations. Operational
metadata belongs in supporting detail unless it changes the current judgment.

## Choose whether to write

An unchanged query or re-read is zero-write, even if a Note is absent or old.
Record a real new observation/result/failure/source/code/run event or decision
as an Entry. Several jobs serving one campaign moment can share a report/Entry.
A requested or genuinely changed synthesis belongs in a working Note; a retained
argument in a theory Note or a pinned ordinary manuscript. Record changes of
understanding, not tool counts: a calculation may remain valid while its physical
interpretation narrows. Keep the full argument in one primary location; do not
automatically produce report + Entry + Note + card. Theory/numerics examples are
in Research memory; they are writing choices, not additional required steps.

Before writing, read [Recording](references/recording.md), inspect whether the
same event/synthesis already exists, and use current pre-write enter/check:
reuse the known-unchanged start or previous post-save report; otherwise refresh.
Fill only the returned draft; preserve template sections, explicit scope, and
`target`/`at` evidence refs (never `pin`). Notes use `created_by` and
`basis_refs`, not `authority`. Save with the public validator; never write
canonical Entry/Note files directly or add an ad hoc parser/validation layer.

For a captured Topic plus singleton Entry scope, use both
`record save <draft> --expected-topic <topic> --exact-workstream <slug>`.
A precondition failure is zero-write, not permission to retry unscoped.
Since 0.10.0 / contract-0.3, the same paired flags also apply to `note save`;
older adapters must not claim atomic Note scope or silently retry unscoped.
Reuse the Entry idempotency key for the
same logical write; an existing canonical path returned on retry is read-only.
Notes have no Entry-style idempotency key. After save, re-run check/enter to
verify the saved state and report any new findings; receipt alone is not enough.

Topic maps use existing sections, not a second status ledger. Update only for
real direction/convention/location changes or an explicit request, preserving
identity and human Research Goal. The ordinary-file path needs applicable
authorization and cannot override stricter canonical-write restrictions.
Never import the current chat/host Goal as a confirmed Topic Goal.

## Before ending

Compare the current enter view with this session's evidence; reuse the final
post-save or known-unchanged read-only view instead of another closing scan.
Refresh when freshness is uncertain. Only if this session produced a durable delta and recorded state is
genuinely behind, append the missing agent closeout and/or working Note yourself.
Supersede only a genuinely stale agent closeout/agent working Note; preserve old
bytes. Never automatically supersede human records, decisions or results.
Agent closeout provenance: `--kind closeout --authority agent --created-by agent:<name>`.
No delta means no maintenance write; an old timestamp or UI warning is not a
reason to manufacture one. Four or more related Entries, a missing synthesis
and a real durable change can justify synthesis judgment, never a runtime rule.

Reuse fresh matching host scheduling to avoid duplicate boundary checks or
questions. Without such a coordinator this is best-effort Skill behavior, not a
runtime hook or exactly-once guarantee. Save verification remains mandatory.
If handoff_status is review, this session produced a durable delta, and no
working Note exists, make closeout/current-state upkeep an explicit end task;
with no durable delta it remains zero-write.

At session start, retrieve applicable Method cards through `rg "^> method-card:" .aitp/topic/`
and read matching Notes. Retrieve candidate observations with
`rg "^> method-observation:" .aitp/topic/entries/`; candidates are low-trust.
Discovery is not a distillation trigger. Ordinary read-only recall does not load
distilling-methods merely because historical markers exist. First use the current
task and touched evidence to judge relevance; do not expand into unrelated
candidate review or infer workstream membership from a slug. For an explicit
card/review request, relevant recurring execution evidence, or new evidence for
an existing card's trial/revision, read distilling-methods for its bounded review.
These are loading cues, not proof that a drafting or publication trigger holds.
At closeout review this session's new observations/cards/
post-card trials under that Skill; no per-action scans or new phase triggers.
Never infer independent trials from marker counts, auto-approve/publish,
propagate across Topics, or resolve a failure on a card's authority.

## Work with the researcher

Before consequential, costly or convention-ambiguous compute, state the physical
setup and get confirm-or-correct where needed; routine cheap steps do not need
repeated questioning. Reconsider objections honestly rather than capitulating
or defending automatically. Record a consequential direction change as such;
a human suggestion is not a verified scientific result. Verification supporting
the claim is required; extra checks beyond it are proposed with costs and need
the researcher's confirmation. Runtime never supplies scientific judgment.

Optional natural-use feedback belongs in the protocol checkout's feedback/
using [the existing template](natural-use-session-template.md). Skip it when it
has no research substance or would delay the researcher; it never blocks work.
