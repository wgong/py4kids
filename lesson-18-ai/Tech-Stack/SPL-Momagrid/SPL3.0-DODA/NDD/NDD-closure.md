# NDD: Natural-language Driven Development and the Closure Principle

**Author:** Wen G. Gong  
**Date:** April 10, 2026 (updated April 2026)
**Status:** Contribution note for SPL v3.0 arXiv paper  
**Reference implementation:** `cookbook/56_code_pipeline/` (SPL30 repository)
**Companion documents:**
- `MLAT-framework.md` — MLAT: the four-level measurement framework; NDD Closure as totality condition
- `NDD-position.md` — philosophical grounding; Noether analogy; agentic integrity lineage

---

## Overview

This note documents a sixth contribution to the SPL v3.0 paper, complementing
the five listed in §1.4 of the main draft. It introduces **Natural-language
Driven Development (NDD)** — a development paradigm conceived by the author in
early 2025, predating the public wave of "vibe coding" — and formalizes its
**closure property**, which SPL v3.0's workflow composition makes implementable
for the first time in a compact, declarative form.

---

## 1. NDD: The Concept

**Natural-language Driven Development (NDD)** is a software development
paradigm in which a natural-language specification is the primary and
authoritative artifact of the development process. Code, documentation, and
tests are derived from the specification — not the other way around.

NDD differs from related approaches in a precise way:

| Approach | Who holds the loop | Spec status |
|---|---|---|
| Traditional TDD | Human (writes tests first) | Implicit in test assertions |
| Prompt engineering | Human (iterates prompts manually) | Ephemeral, not persisted |
| "Vibe coding" | Human-in-the-loop (accepts/rejects suggestions) | Informal, conversational |
| **NDD** | **Autonomous system (closed loop)** | **First-class typed value (`@spec TEXT`)** |

The critical distinction: in NDD the natural-language specification is a
**typed, versioned, machine-readable input** that flows through an automated
pipeline. The system generates, tests, and verifies the implementation
autonomously — and checks its own work.

Importantly, S itself is not assumed to be perfect on first expression. The user
U is the first mover (U → S), and S evolves through iterations: each MLAT
divergence report is a clarification prompt back to U, whose refinement of S
drives the next cycle. NDD Closure is a convergence criterion, not a one-shot
test. See `MLAT-framework.md` §10 for the full iterative development cycle.

The concept was formulated in early 2025, before "vibe coding" entered the
mainstream lexicon. At the time, the missing piece was an expressive enough
declarative layer to implement the full NDD loop without custom orchestration
glue. SPL v3.0's `CALL`, `IMPORT`, `WHILE`, and `EVALUATE` constructs provide
exactly that layer.

---

## 2. The Closure Principle

### 2.1 Informal statement

> An autonomous code generation system achieves **closure** when the
> specification it can reconstruct from its own output matches the specification
> it was given as input.

This is a fixed-point condition: the system has correctly understood the intent
when `extract_spec(generate(spec)) ≈ spec`.

*Scope note:* NDD closure as defined here operates at the `.spl` specification
layer — it is **J₂ (Design-time Judge)** in the MLAT framework (`MLAT-framework.md`).
MLAT extends the same round-trip principle to three additional levels: J₁
(ideation), J₃ (compiler output), and J₄ (deployed behavior). NDD Closure in the
broader sense is the conjunction of all four MLAT levels passing.

### 2.2 Formal definition

Let:

- `S` — the original natural-language specification (the `@spec` input)
- `G(S)` — the code generated from `S` by the system
- `E(C)` — the specification extracted (reverse-engineered) from code `C`
- `J(S, S')` — a semantic similarity judgment between two specifications

**Definition (NDD Closure):** A code generation system achieves NDD closure on
specification `S` if and only if:

```
J(S, E(G(S))) = CLOSED
```

Where `CLOSED` denotes that the derived specification `E(G(S))` is semantically
equivalent to `S` — agreeing on purpose, input/output contract, behavioural
completeness, and introducing no unintended semantic drift.

### 2.3 Significance

The closure condition is a **falsifiable, automated correctness criterion** that
operates at the level of intent rather than implementation detail. It is
strictly stronger than passing unit tests:

| Criterion | What it verifies |
|---|---|
| Unit tests pass | Code behaves correctly on enumerated cases |
| Closure holds | Code captures the *intent* of the specification |

A system can pass all tests and still fail closure — if the tests themselves
were derived from a misinterpretation of the spec. Closure catches semantic
drift that test suites cannot.

This is analogous to a round-trip encoding test in distributed systems:
`decode(encode(x)) = x` is the correctness criterion for a serialisation
protocol. `E(G(S)) ≈ S` is the correctness criterion for an NDD system.

---

## 3. SPL Implementation

### 3.1 The code_pipeline recipe

The NDD closure loop is implemented in full in:

```
cookbook/56_code_pipeline/
├── code_pipeline.spl     ← orchestrator (the NDD engine)
├── generate_code.spl     ← G(S): spec → code
├── review_code.spl       ← internal quality check
├── improve_code.spl      ← iterative refinement
├── test_code.spl         ← functional test gate
├── document_code.spl     ← human-readable documentation
├── extract_spec.spl      ← E(C): code → derived spec
└── spec_judge.spl        ← J(S, S'): closure verdict
```

Each component is a self-contained `WORKFLOW`, independently testable and
replaceable — a direct consequence of SPL v3.0's native workflow composition.

### 3.2 The lifecycle in SPL

```sql
WORKFLOW code_pipeline
    INPUT:
        @spec          TEXT,
        @check_closure BOOL DEFAULT TRUE,
        ...
    OUTPUT: @docs TEXT
DO
    -- Step 1+2: Generate → Review → Improve → Test (retry loop)
    WHILE NOT @test_passed AND @cycle < @max_cycles DO
        CALL generate_code(@spec, ...) INTO @code       -- G(S)
        CALL review_code(@code, ...)   INTO @feedback
        CALL improve_code(@code, ...)  INTO @code
        CALL test_code(@code, @spec, ...) INTO @test_result
        EVALUATE @test_result
            WHEN contains('[PASSED]') THEN @test_passed := TRUE
            ELSE LOGGING 'tests failed | retrying ...' LEVEL WARN
        END
    END

    -- Step 3: Document + Closure check
    CALL document_code(@code, @spec, ...) INTO @docs    -- human docs
    CALL extract_spec(@code, ...)         INTO @out_spec -- E(G(S))
    EVALUATE @check_closure
        WHEN = TRUE THEN
            CALL spec_judge(@spec, @out_spec, ...) INTO @closure_report
            -- J(S, E(G(S))) ∈ {[CLOSED], [DIVERGED]}
    END
    RETURN @docs
END
```

The entire NDD loop — generation, testing, documentation, and closure
verification — is expressed in **under 40 lines of SPL**. The equivalent in
LangGraph or AutoGen would require 150–200 lines of Python plus a custom state
machine schema.

### 3.3 What each workflow contributes to closure

| Workflow | Role in closure | SPL construct |
|---|---|---|
| `generate_code` | Produces `G(S)` | `GENERATE coder(@spec)` |
| `test_code` | Validates functional correctness of `G(S)` | `GENERATE run_tests(@code, @spec)` |
| `extract_spec` | Computes `E(G(S))` | `GENERATE reverse_spec(@code)` |
| `spec_judge` | Evaluates `J(S, E(G(S)))` | `GENERATE judge_closure(@spec, @out_spec)` |

All four use `GENERATE` — the single SPL primitive for LLM interaction — with
different prompt functions. The orchestration logic contains no LLM calls
directly; it only composes sub-workflows via `CALL`.

---

## 4. Positioning as a Paper Contribution

### 4.1 Proposed contribution statement

> **6. NDD Closure (§X):** We introduce Natural-language Driven Development
> (NDD) as a formal development paradigm and define the NDD closure property
> `J(S, E(G(S))) = CLOSED` as an automated, intent-level correctness criterion
> for autonomous code generation. We demonstrate that SPL v3.0's workflow
> composition makes the full NDD loop — generation, test-gated iteration,
> documentation, spec extraction, and closure verification — expressible in
> under 40 lines of declarative SPL, without external orchestration frameworks.
> The `code_pipeline` recipe (cookbook/56) is the reference implementation.

### 4.2 Relation to existing contributions

NDD Closure builds directly on three of the five existing contributions:

- **Contribution 3 (workflow composition):** `CALL` is what makes each NDD
  stage a composable, independently-testable unit rather than a monolithic
  prompt chain.
- **Contribution 1 (DODA):** The `.spl` script is the NDD specification's
  runtime representation — hardware-agnostic, version-controlled, executable.
- **Contribution 4 (`splc` compiler):** The same `code_pipeline.spl` runs on a
  laptop, a LAN grid, or a Momagrid peer Hub without modification.

### 4.3 Differentiation from "vibe coding"

The term "vibe coding" (popularised in early 2025) describes a practice:
iterative, conversational, human-in-the-loop code generation. NDD is an
architecture: closed-loop, autonomous, specification-first. The table below
clarifies the distinction for readers likely to conflate the two:

| Property | Vibe coding | NDD |
|---|---|---|
| Specification | Informal prompt | Typed `@spec TEXT` value |
| Loop control | Human (accept / reject) | Automated (`WHILE`, `EVALUATE`) |
| Correctness criterion | Human judgment | `J(S, E(G(S))) = CLOSED` |
| Reproducibility | Session-dependent | Deterministic given `@spec` |
| Composability | Tool-dependent | `CALL` sub-workflow |
| Documentation | Manual or ad hoc | `document_code` sub-workflow |

NDD does not replace human judgment — the human writes `@spec`. But it
automates everything downstream of the specification, and it verifies its own
output against the specification it was given. That is the closure property.

---

## 5. Historical Note

The NDD concept and the term were formulated by the author in early 2025,
prior to the mainstream emergence of "vibe coding" as a cultural phenomenon.
The core intuition was that natural language, made sufficiently precise and
treated as a first-class typed artifact, could serve the same role in
AI-driven development that a formal specification serves in model-checked
systems — with the difference that the "model checker" is a large language
model operating under a declarative orchestration layer.

SPL v2.0 provided the workflow primitives (`WORKFLOW`, `GENERATE`, `WHILE`,
`EXCEPTION`). SPL v3.0's `CALL` and `IMPORT` provided the composability that
makes each stage independently verifiable. Together they reduced the
implementation of the full NDD loop from a research prototype requiring
hundreds of lines of orchestration glue to a 40-line declarative script —
demonstrating that the paradigm is not merely theoretically sound but
practically lightweight.

The `code_pipeline` recipe in the SPL30 cookbook is the first concrete,
runnable embodiment of NDD closure. It is offered both as a research artifact
and as a reusable component for any SPL user who wants autonomous,
self-verifying code generation as a building block in a larger workflow.

---

## 6. Real-World Validation: SPL v2.0 as Its Own Test Subject

### 6.1 Beyond Toy Examples

The initial NDD closure demonstration used binary search as the target program:
a small, self-contained function with a clear spec. This validated the mechanics
of the pipeline but raised an obvious question: does closure analysis scale to
a real language runtime with a rich design document, multiple source files, and
inevitable drift between original intent and shipped behaviour?

On 2026-04-12 we applied NDD closure to SPL v2.0 itself. The result was the
first real-world NDD closure run where the system being tested is the same
runtime family that implements the closure loop.

### 6.2 The Run

```
S  = SPL-design-v1.1.md           (original design doc written by Wen, March 2026)
G  = spl/ codebase                 (the implementation, ~3,000 lines Python)
E  = SPL20-user-guide.md          (spec extracted from code by human review)
J  = structured diff (manual)
```

The extraction step (`E`) was performed as a user-guide-style document derived
entirely from reading the implementation — not from the design doc. The judge
(`J`) then diffed `S` against `E` using the structured checklist method
developed in Step 7 of the `code_pipeline` recipe.

**Verdict: [DIVERGED]** — four functional gaps found.

### 6.3 The Four Gaps

| # | Gap | User impact |
|---|-----|------------|
| 1 | `WHILE @item IN @items` — item variable never bound in executor | Collection iteration silently broken; body runs without `@item` |
| 2 | `ToolFailed` not registered in `EXCEPTION_CLASSES` | CALL errors bypass the SPL exception system; `WHEN ToolFailed` unreachable |
| 3 | `HallucinationDetected` described as auto-detecting (confidence threshold) but only raised via explicit `RAISE` | Developers expecting runtime detection are surprised; wrong mental model |
| 4 | `COMMIT` described as primary finalisation keyword; `RETURN` is primary in code | Spec teaches the wrong keyword |

All four were closed on the same day: executor and parser patched for gaps 1–2,
design doc updated to v1.2 for gaps 3–4.

### 6.4 The Methodological Insight: Top-Down, User Perspective First

The most important outcome of this run was not the four fixes — it was the
clarification of the right methodology for applying NDD closure to real systems:

**Wrong approach:** start from file-level code details (class names, AST nodes,
function signatures). This produces a technical spec that is accurate but not
what users care about, and not what the original design doc promises.

**Right approach:**

```
Step 1: Write E(G(S)) as a user guide
        What can a user do? What syntax works? What are the gotchas?
        Written at the same level of abstraction as the original spec.

Step 2: Diff S against E(G(S)) at the user-functionality level
        What did the spec promise that the user guide cannot deliver?
        What does the user guide describe that the spec never mentioned?

Step 3: Drill down technically only where gaps appear
        A user-guide gap ("@item not bound") points to a specific
        code location. Investigation is targeted, not exhaustive.
```

This ordering matters because specs are written from the user's perspective.
The closure check must operate at the same level of abstraction as the promise.

### 6.5 Source of Truth Clarification

> The design doc captures *original intent and rationale*. The codebase
> captures *current reality*. The user guide bridges them: it is the spec
> that users actually need.

NDD closure measures three distances simultaneously:
- **Original intent → current reality** — what changed during development
- **Current reality → user guide** — what is real but undocumented
- **User guide → original intent** — what was promised but not yet delivered

Each distance is a different kind of work to resolve. When gaps are fixed
and the closure judge returns `[CLOSED]`, the fixed point is reached.

### 6.6 Artefacts

All artefacts are in `SPL20/docs/NDD-closure/`:

| File | Role |
|------|------|
| `SPL20-user-guide.md` | `E(G(S))` — extracted user guide |
| `SPL20-ndd-closure-report.md` | `J(S, E(G(S)))` — structured diff, [DIVERGED] → [CLOSED] |
| `ndd-is-working.md` | Methodology notes and findings |
