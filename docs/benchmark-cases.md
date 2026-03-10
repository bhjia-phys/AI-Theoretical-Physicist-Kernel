# Benchmark Cases

This document lists candidate benchmark-style research cases for the project.

The purpose of these cases is not to prove that the system is already a fully capable AI researcher. The purpose is to create concrete tests for whether the architecture supports structured, epistemically disciplined research work.

---

## Case 1 — Literature-to-knowledge

### Purpose
Test whether the system can move from source intake to reusable knowledge rather than stopping at summary.

### Desired flow
1. register sources,
2. extract claims,
3. separate provisional from canonical material,
4. promote a small number of reusable notes,
5. preserve unresolved ambiguity explicitly.

### Minimum pass condition
- multiple sources registered,
- provisional claims recorded,
- at least one canonical note produced,
- provenance remains visible.

---

## Case 2 — Idea evaluation

### Purpose
Test whether the system can evaluate a proposed mechanism or conjectural connection without collapsing evidence and speculation together.

### Desired flow
1. state the idea,
2. identify nearest literature neighbors,
3. separate sourced claims from new conjectures,
4. identify likely failure modes,
5. propose validation routes.

### Minimum pass condition
- sourced background separated from new conjecture,
- explicit assumptions listed,
- at least one validation route proposed,
- uncertainty not hidden.

---

## Case 3 — Theory-to-numerics

### Purpose
Test whether the system can move from conceptual framing to a concrete numerical validation lane.

### Desired flow
1. define observables,
2. define model or toy system,
3. specify parameter points,
4. define expected signals,
5. record result interpretation rules.

### Minimum pass condition
- a numerical checklist exists,
- expected success/failure signals are explicit,
- results can be written back into the research record.

---

## Case 4 — Theory-to-formalization

### Purpose
Test whether the system can move from an informal argument to a scaffold suitable for proof-assistant or formal reasoning work.

### Desired flow
1. define notation,
2. isolate assumptions,
3. split the argument into local steps,
4. mark gaps and placeholders,
5. record what still requires human judgment.

### Minimum pass condition
- a scaffold exists,
- assumptions are explicit,
- unresolved gaps are not hidden,
- a formalization-ready surface is produced.

---

## Case 5 — Closed-loop research record

### Purpose
Test whether the system can write research outputs back into stable structure rather than leaving them as chat residue.

### Desired flow
1. active investigation produces intermediate output,
2. result evaluation distinguishes keep / revise / discard / defer,
3. reusable outcomes are promoted,
4. unresolved outputs stay marked as uncertain.

### Minimum pass condition
- result evaluation is explicit,
- reusable findings can enter the canonical layer,
- unresolved findings remain visible in an exploratory layer.

---

## Why benchmark cases matter

Without concrete benchmark-style cases, the project risks remaining a purely conceptual architecture. These cases are meant to anchor development in research behaviors that are inspectable, revisable, and progressively testable.
