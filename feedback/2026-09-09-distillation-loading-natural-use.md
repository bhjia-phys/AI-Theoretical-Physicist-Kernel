# Read-only recall unnecessarily loaded distillation

## Follow-up: unnecessary manual hash checks

The researcher reported a standalone `sha256sum` on an existing Entry during
AITP use. Its surrounding write/read context was not supplied, so this is not
proof that that particular command was redundant. The authorized refinement
distinguishes ordinary recall (no extra per-file hash audit), constructing a
required pin (compute once or reuse a verified digest of the same unchanged
target), and relevant integrity/historical-version verification. An Entry's
outgoing evidence pin is not the Entry's own digest. Save/check validation is
unchanged; mere existence is not accepted as evidence of unchanged content.
A synthetic public-CLI test exercises reusable pins and zero-canonical-write
rejection after target bytes change while the file still exists. No live model
speedup, new hash service or runtime change is claimed. Not reinstalled.

Follow-up validation: full ledger suite 194 passed in 42.39 s, including the
new unchanged-pin/changed-existing-file save test; using-aitp Skill validation
and both repository diff checks passed. These are deterministic contract tests,
not evidence of fewer hash calls in a fresh model session.

Status: active — user-authorized Skill-routing refinement implemented; behavioral retest pending.

Observed in one fresh Hakimi mode-off NiO cRPA recall session on 2026-09-09
Asia/Shanghai: three questions asked current understanding, earlier understanding
and why it changed. The model discovered one historical method-observation and
loaded the full distilling-methods Skill despite no requested distillation or
new method execution. The final answer recovered the main distinctions and
made zero canonical writes. The raw prompt, rubric, report and native trace
locator are retained in `/tmp/aitp-three-question-Aal6NMIJ/`; that temporary
directory is not a permanent archive guarantee.

Wall time 172.023 s, including 89.710 s supervised approval wait; 7 model
requests, 17 tools, one check. These measurements do not isolate the loading
cost and do not establish a causal speedup opportunity of any specific size.

Minimal change: separate cheap marker discovery from loading full candidate
review. Use current task and touched evidence for relevance; ordinary read-only
recall alone does not turn unrelated history into a review assignment. Explicit
review/card requests, relevant recurring execution and new trial/revision
evidence still route to the detailed Skill. Loading is not a drafting trigger;
eligibility, independent execution judgment, exact pins, no auto-draft by count,
and both human decisions remain unchanged. No registry, runtime classifier,
new command or relaxed canonical-write rule.

Verification covers the packaged guidance and existing ledger/card contracts;
it is not proof that every model will follow the guidance. Source change only,
not installed or live-retested in this slice.

Validation: `.venv/bin/python -m pytest -q` — 193 passed in 43.07 s;
both edited Skills pass skill-creator's quick validator; both repository diffs
pass `git diff --check`. Existing routing-text assertions now cover the negative
recall case and the retained positive review/trial cues; these are static
packaging checks, not a model-behavior test. No runtime or fixture semantics changed.
