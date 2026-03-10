# Architecture

## Core objective

Build a human-in-the-loop research kernel for theoretical physics that can evolve toward a human-AI collaborative theoretical physicist.

The project is not trying to imitate a finished autonomous researcher. Instead, it aims to provide the core research structure needed for serious human-AI collaboration in theoretical physics.

---

## Three-layer knowledge architecture

### Layer 1 — Intake / Staging
Purpose:
- store source-bound, not-yet-canonical material,
- preserve provenance before abstraction,
- allow provisional extraction and ambiguity.

Typical contents:
- source registrations,
- raw notes,
- provisional claims,
- transcript fragments,
- intake maps.

### Layer 2 — Canonical Reusable Knowledge Base
Purpose:
- store reusable research memory,
- accumulate atomic notes, workflows, methods, concepts, and validation patterns,
- support cross-topic reuse.

This is the center of gravity of the system.

Typical contents:
- atomic notes,
- workflows,
- concept notes,
- method notes,
- claim cards,
- bridge notes,
- warning notes,
- validation patterns.

### Layer 3 — Research Feedback / Exploratory Log
Purpose:
- store active research outputs that are still uncertain or too local to canonicalize,
- support exploratory work without polluting the canonical layer too early.

Typical contents:
- conjectures,
- failed attempts,
- partial derivations,
- anomalies,
- negative results,
- run-local interpretations,
- open technical questions.

---

## Flow logic

The intended movement between layers is:

- **Layer 1 -> Layer 2** when extracted material becomes reusable and sufficiently source-anchored.
- **Layer 1 -> Layer 3** when intake directly triggers an active research question.
- **Layer 2 -> Layer 3** when canonical knowledge seeds a new investigation.
- **Layer 3 -> Layer 2** when a run-local result becomes portable and stable enough to reuse.

This separation is essential. The system should not collapse raw intake, canonical knowledge, and uncertain research output into one undifferentiated notebook.

---

## Research loop

The long-term research loop is:

1. source intake,
2. claim extraction and structuring,
3. knowledge promotion,
4. derivation or argument scaffolding,
5. validation design,
6. execution or handoff,
7. result evaluation,
8. writeback.

A complete version of the system should support explicit keep / revise / discard / defer decisions for nontrivial research outputs.

---

## Human checkpoints

The project is explicitly human-in-the-loop.
Important checkpoints include:

- framing the research question,
- accepting high-impact claims,
- correcting scaffold structure,
- choosing a validation route,
- deciding how to treat results.

This is a deliberate design choice. The aim is not fake autonomy, but disciplined research collaboration.

---

## Current implementation posture

At the current stage, the architecture is more mature than the public implementation.

What exists conceptually:
- three-layer separation,
- artifact-first workflow,
- validation-aware research loop,
- canonical promotion logic.

What still needs stronger public implementation:
- stable schemas,
- cleaned helper scripts,
- worked examples,
- clearer adapter surfaces,
- result-writeback discipline.

---

## Design principles

1. **Evidence before speculation**
2. **Durable artifacts over chat-only output**
3. **Reusable knowledge over local residue**
4. **Uncertainty should be preserved, not hidden**
5. **Human judgment remains central at high-impact points**
6. **The system should improve by compounding reusable research structure over time**
