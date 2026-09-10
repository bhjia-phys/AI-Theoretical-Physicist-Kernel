# Research memory: read and write

Use this reference when recovering a research line, reconciling a handoff with
new evidence, or writing a synthesis. It is guidance for the existing AITP
records, not another protocol or a checklist to run at every Research action.
The parent Skill owns session maintenance and verification; `distilling-methods`
owns all Method-card rules. A native host, when present, owns scheduling.

## Keep three relationships distinct

| Relationship | Existing representation | What it does not establish |
|---|---|---|
| Belongs to this research direction | Topic plus explicit Entry/Note `workstreams` | A directory name, shared codebase, citation, or current session does not assign membership. |
| Depends on this evidence | Entry `refs`; Note `basis_refs`, with `target`, `at`, optional `locator` | A pin establishes an evidence reference, not whether it supports, contradicts, or proves a claim. Explain that in the body. |
| Replaces an earlier record | New Entry/Note `supersedes`; failure closure via an Entry's own evidence and `resolves` | Supersession does not refute every old claim. Newer timestamps, a successful build, or a Method card do not resolve scientific failures. |

Questions, competing explanations, applicability, and uncertainty belong in the
existing body sections. Do not invent `hypothesis_id`, `supports`, `used_by`,
lineage records, a card registry, or another mutable project-state file.
Ordinary derivations, code, figures, and manuscripts remain ordinary research
files. Pin and locate the parts used; do not copy whole artifacts into Entries.

For a disputed failure closure, use canonical `show` to check the resolver's
current `status`, not only its body or `resolves` field. The projection computes
relations globally, but only **active** Entries contribute `resolves`. A
superseded resolver is historical evidence; its active successor does not inherit
that edge. If the successor has no `resolves`, the failure can legitimately
reappear as unresolved, even across workstreams. Explain the historical repair
and current ledger relation separately; do not declare a projection bug or add a
closure merely to remove the discrepancy.

## Read enough to answer the current question

### Topic is a research map, not a second ledger

Use `.aitp/topic/TOPIC.md` for the project's durable question, established
directions and their explicit workstream slugs, shared conventions, and a few
useful reading locations. This is a human-readable map inside the existing
Topic sections, not a machine registry, exhaustive record index, or new schema.
Keep per-run status and detailed current conclusions in Entries and line Notes.

A direction's map entry should explain its question and boundary, not just its
material name. One workstream may contain several materials; still check the
system, approximation and run identity before using its evidence. Conversely,
similar slugs are not aliases unless the records explicitly establish that.
Map prose and hyperlinks never assign membership or close failures.

Prefer an established slug plus a useful Note/artifact entry point over a table
of every record. A dated Note link is an orientation hint: obtain the current
`latest_working_note.source` with scoped `enter` when resuming that direction.
The map need not change after each Note save. If a link is old or missing, use
the line's recorded evidence; do not silently switch to the global latest Note.

Maintain the map when directions, shared conventions or principal locations
actually change, or when explicitly asked to organize it. Do not replace a
human-established Research Goal with the current chat task. Preserve historical
wording and distinguish an observed navigation correction from a new decision.
The CLI currently has no Topic update command: the parent Skill's ordinary-file
edit path requires applicable user authorization. It is not Entry/Note save,
has no atomic compare-and-save receipt, and must not bypass a stricter workspace
write restriction. If editing is not authorized, propose the exact map change
outside canonical files; do not manufacture a CLI or duplicate the map elsewhere
as a competing source of truth. Old pinned Topic bytes remain historical evidence.

### Choose the depth of recovery

Use the already established Topic and explicit workstream. If scope is unknown,
recover it from authoritative records or ask; never borrow the global handoff
or the first matching Note as the current line's state. Missing scoped records
do not mean the whole Topic has no memory. Older unscoped material may be read
as explicitly identified background, but is not silently assigned a workstream.

At the existing session boundary, consume the host's fresh, matching maintenance
receipt if supplied; otherwise follow the parent Skill's `enter`/`check` path.
Do not repeat that maintenance merely because this reference was opened. For a
needed Note locator or further recorded evidence, these are read operations,
not a new health cycle (`aitp` abbreviates the parent Skill's resolved launcher):

```text
aitp enter --workstream <confirmed-slug> --json
aitp list --workstream <confirmed-slug> --since <note-created-at> --json
aitp show <entry-id> --json
```

Choose a reading depth that matches the question. A status lookup needs the
relevant synthesis and changed evidence, not every old derivation. A requested
whole-project recovery needs a short map of the explicit directions and their
important conclusions, failures and artifacts, then deeper reads only where
coverage or evidence is missing. Reuse already inspected Entries instead of
issuing another `show` solely for a different paragraph of the same answer.
Do not mistake an empty Entry list for absent Notes or an absent research line.

Keep the actual `check` report and its exit code available during the session;
inspect relevant findings from it rather than repeating the same check for
counts, text rendering and detail. A scoped check still scans the whole store;
looping it over all lines is not a faster inventory. When whole-store findings
need inspection, use the no-flag report (reuse it if already current), not guessed
scoped membership. This does not skip the parent's session/save boundary
verification, manufacture a host receipt, or treat scoped clean as global clean.

1. Read the exact `latest_working_note.source` file when useful; inspect its
   Topic, workstreams, `supersedes`, scope, basis, and omissions. `list`/`show`
   expose Entries only, so use a file read for Notes. A newest Note can be
   irrelevant to this question or omit important evidence.
2. Read the relevant Entries not covered by that synthesis. The `--since`
   window is inclusive and uses recorded time, not execution time or semantic
   coverage. Older decisions, failures, sources, or excluded records can still
   matter. Use targeted `rg` discovery followed by canonical `show` as needed;
   do not rebuild the entire Topic's history for an ordinary question.
3. Inspect the actual pinned sources behind claims you rely on, including
   assumptions and counterevidence. Reuse already read, unchanged evidence;
   pointer/report files describe what was observed then, not a fresh remote
   query. Retrieve applicable Method cards through the parent Skill's existing
   marker route, not an additional scan on each action.

`enter.next_action` is a recorded handoff, **not an execution instruction**.
The frozen CLI prefers active closeouts; a newer failure/result can coexist
with an older closeout's next action. Explain the discrepancy and use the
evidence to propose a current next step. A later result does not cancel an
older human decision or resume a paused host Goal. Do not rewrite records or
invent a new closeout merely to make a read view look consistent. Distinguish
the standing scientific direction from present execution permission: a proof
programme can remain valid while its Goal is paused. When asked about current
constraints, read the newest relevant record's limitations/body, not just its
summary or an older human programme; report both, without inferring resumption.

Present a short, evidence-backed answer: **which question; what is established
and under which conditions; what changed; what is still unknown; what next**.
This is a reading view in the response, not a new canonical object. Link to the
record and relevant equation/output so the researcher can inspect the argument.
Lead with the physics, not revision IDs, full hashes, or counts of warnings.
Disclose a finding that affects the evidence being used; do not equate unrelated
store findings with this claim's validity, hide relevant errors, or downgrade
pins to obtain a clean report. Exit 2 means unknown store state: stop relying on
that projection and report the access problem.

## Write at a change of understanding, not every tool boundary

| What actually happened | Smallest useful durable representation |
|---|---|
| Asked progress; re-read known output; unchanged queue; conversational exploration | Answer using the existing identity/evidence. No new Entry, Note, or Method review just for this. |
| New observation/result, decisive failure, source assessment, verified code/run event, or direction decision | One appropriate Entry with the evidence, conditions, limitations, and next implication. Several jobs serving one campaign moment can share one report and Entry. |
| A chain of results now changes the working explanation, or the researcher requests a current synthesis | A working Note referencing the actual basis. No duplicate result Entry merely to announce the Note. |
| A derivation is worth retaining, including an incomplete argument with a precise gap | A theory Note, or an ordinary derivation/manuscript pinned by a Note/Entry. Mark assumptions, checked steps, and unproved steps separately. |
| Recorded execution suggests a reusable non-trivial method | Assess only the touched evidence first; consult `distilling-methods` if eligible. No automatic card from a phase change, Note revision, marker count, or elapsed time. |

Human suggestions may start as attributed hypotheses in a discussion or Note.
A consequential human direction/decision remains attributable to the human;
verification is a separate agent/tool/source claim with its own basis. Do not
turn “the researcher said so” into a tested result. Do not require a human
decision Entry for every conversational suggestion.

A working Note's seven existing sections already fit a useful research map:

- **Purpose / Scope And Basis:** the question, line, coverage and exclusions.
- **Synthesis:** current explanation, alternatives, and what changed since the
  previous synthesis; distinguish observation from interpretation.
- **Evidence Map:** for each consequential statement, locate supporting or
  contradicting evidence and explain the relation and its limits.
- **Uncertainty And Omissions / Open Questions:** missing inputs and unresolved
  alternatives, including evidence this Note deliberately did not assess.
- **Next Actions:** the smallest discriminating next step, or an explicit wait
  or need for researcher judgment. Do not invent a test just to fill the section.

Use as much detail as the question needs, not an event timeline of every tool.
`basis_refs` may directly pin a derivation or report: an otherwise redundant
Entry is not required between an artifact and a Note. A Note is synthesis, not
independent verification of the result it discusses. If there is a genuinely
new result to record, retain that event and its direct evidence as an Entry.

## Detailed scientific writing without duplicate records

Use the existing sections at the depth the argument needs, not a mandatory
length or one record per algebraic step. For a derivation, identify the object,
conventions and assumptions at their first consequential use; explain the
non-obvious steps in dependency order. Label an exact identity, controlled
approximation, numerical observation and conjecture differently. A failed or
incomplete derivation is useful when the failed step and missing input are
precise; do not fill that gap with polished prose.

A long TeX/Markdown derivation, lecture or paper can remain an ordinary research
file. Its Note should recover the question, main claim, assumptions, changed
understanding and exact equation/section locations, not copy the entire file.
Choose version/snapshot pins by the parent Skill's evidence-lifecycle rules.
Revising the manuscript does not update an old Note's evidence automatically.
For a paper, trace consequential claims and figures to their basis and disclose
unresolved qualifications; a compiled PDF is not scientific acceptance.

### Theory and numerics: examples, not separate lifecycles

Both can occur in one workstream. Preserve the conditions behind a claim:
definitions, conventions and missing proof steps for an argument; model,
approximation, parameters and error/convergence limits for a numerical result.
These are writing cues, not extra fields or a checklist before using tools.

| Situation | Useful response or record | Avoid |
|---|---|---|
| Recheck known algebra or poll an unchanged job | Answer from existing evidence; zero new records. | A new hypothesis, Entry or Note just for the query. |
| Derive data within a candidate wall theory, but its physical attachment map is missing | Locate the derivation; a short result Entry distinguishes the calculation from the unestablished physical identification. | Declaring the whole wall/junction problem solved. |
| A counterexample narrows an earlier interpretation | Record the counterexample, the assumption it defeats, what still holds and when retrying could help. Update synthesis only if genuinely affected. | Treating all earlier mathematics as false, or disguising a negative result as progress. |
| A GW run produces bands, but only one grid/frequency setting was tested | Record the output and tested conditions; convergence remains unestablished. | Equating successful execution with convergence or physical accuracy. |
| Several findings change the working explanation | One synthesis referencing the original arguments/results, explaining why the route changed. | Another result Entry merely announcing that Note. |

The wall/GW examples are illustrative, not independent validation of a real run
or derivation. For a changed interpretation, explain “previous understanding →
new evidence → revised scope”, including what remains valid. If the old reason
for choosing a route was never recorded, mark it unknown; dates do not establish
causality. A useful failure records the excluded possibility and precise missing
step, not just “failed”. Human guidance can motivate work without validating it.

When reconsidering a route, recover the current claim, relevant earlier attempts
and objections, then the specific original argument needed. Do not execute an
old next action merely because it exists, or repeat this historical review on
each turn. Keep the current answer short with deeper evidence locations.

A retained conjecture, theorem or counterexample belongs in research records;
it is not automatically a Method card. Only a reusable procedure is a candidate
for the existing distillation rules. No extra card review follows from finishing
a derivation or revising a Note.

## Preserve history without multiplying it

For a consequential older claim, distinguish finding its record, retrieving
the cited version, and independently checking the science. When a relied-on
file has drifted or disappeared, look first at the recorded commit, snapshot
or archive location; compare retrieved bytes with the original pin before
calling that version recovered. A current manuscript with the same title is
not the old argument. Report an unavailable version as a specific evidence
gap, not as proof that the result never existed or that its physics is false.
A newly established recovery link can be recorded with its observation and
limits; update a genuinely affected synthesis without rewriting the old pin.
Do not turn this into a full-archive audit on every query. Pins do not retain
bytes: long-term access still needs the underlying repository or evidence
backup. Local `git:` pins resolve in the Topic workspace repository; a nested
checkout's commit/path is not automatically a valid root-repository pin.
An explicit retrieval locator must not be advertised as runtime verification.

Use the existing `record/note prepare → fill returned draft → save` path. Never
edit `.aitp/topic/entries/` or `.aitp/topic/notes/` directly. Keep the generated
headings and fields; choose pins by evidence lifecycle as the parent Skill
specifies. A revised agent working Note can supersede its genuinely stale
predecessor; leave the old Note and its evidence bytes intact. State what changed
and what remains valid. Do not silently amend a human decision/result.

For an explicitly captured singleton Entry scope, use `record save <draft-path>
--expected-topic <topic> --exact-workstream <slug>`. A mismatch is not permission
to retry unscoped. Since 0.10.0 / contract-0.3, use the same paired flags on
`note save` for a captured singleton scope. Older adapters must detect unsupported
capability and stop scoped saves, not silently downgrade to legacy unscoped writes.

Reuse the same idempotency key for an Entry retry; if prepare returns an existing
canonical path, read it instead of treating it as an editable draft. Check
whether a requested synthesis already exists before preparing another Note;
Notes do not acquire an Entry-style idempotency key. Keep required save and
post-save verification under the existing owner; neither “lightweight” nor a
successful tool return means the claims have been scientifically validated.

An ordinary query with no durable delta stays zero-write, even if a Note is
missing or old. Automatic current-state maintenance additionally requires the
parent Skill's genuinely-behind test; an explicitly requested synthesis is a
different task from a query. A UI warning alone is not a compulsory record,
repair, or interruption of research.

Review draft claims, explicit scope and references, then let the public save
command perform authoritative validation. Do not install a YAML dependency or
write a substitute regex/parser/validator just to preflight a Note. An ordinary
file read and exact evidence-pin calculation do not need another validation
framework. Draft review is not scientific approval, and a saved agent Note
remains `agent_draft`; do not leave temporary “waiting for this draft's save”
instructions as its durable research next action.
