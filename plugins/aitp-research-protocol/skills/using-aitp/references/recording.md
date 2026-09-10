# Recording and evidence pins

Read before preparing a durable Entry or Note, not for ordinary queries.
Follow ../SKILL.md for scope, authorization and pre/post save verification.
Use the generated template and public save validator, not a copied parser.
Detailed M1e pin/backfill semantics live in cli-contracts.md; research-memory.md
explains synthesis and manuscript structure when needed.

## Record a durable moment

Record only information that should survive the current conversation:

```text
aitp record prepare --kind <kind> --authority <level> \
  --created-by agent:<name> --idempotency-key <stable-key>
```

Choose one kind: `observation`, `result`, `failure`, `decision`, `source`, `code-change`, `run`, or `closeout`. Set `authority` to the source of the event: `human` (`--created-by researcher`) when the researcher asserts it, `agent` when you act or observe.

Open the returned draft, replace every inline prompt, add precise relations and pinned references, then run:

```text
aitp record save <draft-path>
```

The CLI template is the schema. Keep claims small, state limitations, and distinguish evidence from interpretation. The generated frontmatter starts with `refs: []` (Notes: `basis_refs: []`) — that is a schema placeholder, not a valid evidence list. The draft prompts show the required shape; replace the list with maps containing `target` and `at`. The pin key is `at`, never `pin:`.

- Before preparing a record, check that the ledger does not already contain the same logical event. A restatement, confirmation, or re-verification of an already-recorded convention, decision, or claim is not a durable event: cite the existing record and write nothing new. Never re-issue with `agent` authority a decision the ledger already records as `human`.
- When the Entry directly records one actual execution of a non-trivial,
  reusable procedure (preferred kinds `run`, `result`, `observation`;
  `code_change` only with its own execution evidence; `failure` only when it
  records a workaround execution), and no existing card covers it, consider
  adding a `> method-observation: <slug>` marker as the Entry body's first
  line. This is a low-noise, low-trust candidate tag — not a trial, not
  proof of repetition, and not a workstream assignment. The detailed
  eligibility rules and the full distillation chain live in
  [`../../distilling-methods/SKILL.md`](../../distilling-methods/SKILL.md); do not
  duplicate them here. If an applicable card already exists, create the
  Entry as a post-card trial that exact-`sha256:` pins that card instead of
  writing an observation marker.
- Record a verification only when it changes a live claim or surfaces auditable evidence the ledger lacks; do not wrap an ordinary re-read or an un-triggered check as a durable event.
- Use `resolves` only when this Entry's own evidence directly closes an active failure — first check the failure's state and its `supersedes`/`resolves` chain, and confirm no existing record already settles the failure's subject. A projected counter (such as `unresolved_failures`) is ledger state, not an instruction: do not change a failure's status unless the records support the change.
- Use `supersedes` only when replacing an older Entry; never silently rewrite history.
- When the researcher challenges an existing result/closeout: first write a narrowly scoped `failure`; after the fix, resolve it with direct evidence and write a new closeout; never rewrite the old result to manufacture a clean history. If the main claim stands and only a local statement is corrected, state that distinction in the failure/resolver `limitations`.
- Use `git`, `sha256`, `run`, `version`, or `retrieved` pins for evidence that may change.

### Pinned references — exact YAML and lifecycle

Keep manual hashing proportional to the write. A new `sha256:` pin needs the
digest of its exact target, computed once or reused from a verified same-target
result in this known-unchanged work interval. Do not copy an Entry's evidence
digest as the digest of the Entry itself. A historical pin alone does not prove
current bytes match. Changed targets, concurrent writers or uncertain freshness
invalidate reuse; do not fabricate digests or substitute file-existence checks.
When several new pins are needed, compute their digests in one ordinary tool
call where supported, not one model round trip per file. Save and required
post-save check remain authoritative; no additional before/after `sha256sum`
audit is needed merely to duplicate them. Reading a record without creating a
pin is not a reason to hash it.

`refs` (and a Note's `basis_refs`) is a YAML list of maps. Every mutable
reference uses this exact shape:

```yaml
- target: relative/path-or-url
  at: sha256:<digest> | sha256-once:<digest> | git:<revision> | run:<id> | version:<id> | retrieved:<time>
  locator: exact section, equation, line, or object   # optional
```

Pin lifecycle (frozen in `docs/archive/m1b-r1-spec.md`; unchanged by M1d):
a pin is verified at **save** — a failing pin makes the record invalid as
written, and save errors with the same code/message the `check` path reports
— and re-verified read-only at every `check`. A `sha256:` pin records the
file's digest at save time; if the target file later changes, `check`
reports `hash_mismatch` (error). A `sha256-once:` pin also verifies at save
but later drift is `historical_pin_drift` warning (see cli-contracts.md, M1e). Whether that mismatch is the expected
drift of a historical pin (e.g. a legitimately regenerated inputs manifest)
or current evidence damage is a **human judgment** — the runtime never
classifies it. When evidence legitimately changes, update the pin
deliberately in a new record; never silently edit the old record's pin.

Choose the pin by evidence lifecycle:

- **immutable evidence** (one-time snapshot, provenance report, local
  manifest, PDF/archive copy): pin the file directly with `sha256:`.
- **tracked evolving source** (code, TeX, audit scripts): prefer
  `git:<revision>` over a working-tree `sha256:` so later edits do not turn
  a historical record into a `hash_mismatch`.
- **mutable canonical working files** (`PROJECT_MEMORY.md`, a live
  note/report, a regenerated `MANIFEST.sha256`): do not make a historical
  Entry or Note depend on the file staying unchanged. Copy the point-in-time
  state to an immutable snapshot and pin that, or pin a `git:` revision; a
  body citation by path is not an evidence pin.
- **remote run**: pin the local immutable pointer manifest (below), never a
  bare `host:path`.

A pointer manifest is itself evidence. Once a saved Entry pins a local
pointer file, never edit that pointer file in place. If a legitimate
r3→r4 revision changes it, write a new versioned pointer file (e.g.
`data/run-<job-id>-r4.pointer.json`) and record the new state in a new
Entry; leave the old pointer and old Entry as history. The same rule
applies to Note `basis_refs`: do not edit an old Note to chase a changed
hash — leave it as historical evidence and record the new state in a new
Note/Entry. The resulting old-pin `hash_mismatch` findings are expected
historical drift, not current damage; interpret `check`/`by_code` with
that distinction and prevent future noise by pinning snapshots from the
start.
Scheme notes: `git:` local pins verify `git cat-file -e <revision>:<target>`
(an external http/https/arxiv/doi target is an error; when no Git
environment exists the pin grades as a warning, cannot verify); `run:`
requires a directory whose name is the value; `version:` requires an
external persistent identifier; `retrieved:` requires an HTTP(S) target and
an ISO-8601 retrieval time.

- Reuse the same idempotency key when retrying the same logical write.

For a dense campaign — many jobs serving one purpose — first write one local
immutable submission/result report (job IDs, binary/build/input identity,
boundaries and status), then index that durable campaign moment with a single
`run` or `result` Entry. One Entry per job is not expected; transient queue
snapshots and preflight churn are not separately recorded.

### Remote evidence — pointer manifest (non-normative example)

A naked remote path is location metadata, not locally verifiable evidence.
When a durable result depends on remote immutable runs, first write a local
pointer manifest (e.g. `data/run-<job-id>-r4.pointer.json`) carrying the host,
remote path, scheduler job ID, binary/input SHAs, a local hash manifest, the
verification time, and a `boundary` line stating that the remote bytes were
checked then and not re-verified since; then pin that local file with
`sha256:` in the Entry's `refs`. Make each pointer file an immutable
per-event object: include job/date/revision in its filename, and never edit
in place a pointer file already pinned by a saved Entry — write a new file
and a new Entry for the next event. Never record a bare `host:path` as a pin.
This is a Skill convention with no runtime support (roster D is deferred).

## Write a note from recorded evidence

Use a Note for synthesis, not as the only evidence for a result:

```text
aitp note prepare --mode working --title "<title>" --created-by agent:<name>
aitp note prepare --mode theory --title "<title>" --created-by agent:<name>
```

Fill the generated template, cite supporting pinned sources in `basis_refs`, and save with:

```text
aitp note save <draft-path>
```

A working Note explains the current line of attack. A theory Note gives a derivation or formal argument with assumptions, conventions, checks, and open gaps.

A provisional plan can cite the researcher's proposal, not yet a result. Reuse
an existing proposal/transcript; if none is addressable and retaining it is in
scope, save the supplied text as a clearly attributed, unverified ordinary
source and pin it. Do not invent data or a decision Entry to satisfy basis_refs.
When fixing a draft, update its summary and affected prose together with refs:
“no scientific results” is different from “no source references.” Read the
affected sections once before save; this is a content review, not another hash
or whole-store check. Correct an already saved Note by supersession, not editing.
