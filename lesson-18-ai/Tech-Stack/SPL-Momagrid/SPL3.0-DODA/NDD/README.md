# NDD Research Folder — Reviewer Briefing

**Prepared by:** Wen G. Gong
**Date:** April 2026
**Requesting review from:** Gemini, Z.ai

---

## What This Folder Contains

Three documents that together form the NDD (Natural-language Driven Development)
theoretical contribution to the SPL v3.0 arXiv paper:

| File | Role | Read when |
|------|------|-----------|
| `MLAT-framework.md` | **MLAT: the four-level measurement framework** — operational, engineering-focused | Start here for the full picture |
| `NDD-closure.md` | **NDD Closure: formal definition** — single-level (J₂) closure property, SPL implementation, real-world validation | Start here for the formal/technical core |
| `NDD-position.md` | **Position paper** — philosophical grounding, Noether analogy, agentic integrity, AI safety implications | Start here for the "why it matters" argument |

The three documents have a deliberate division of labor:
- `NDD-position.md` answers: **why does this matter?**
- `NDD-closure.md` answers: **what is it and how is it implemented?** (at the `.spl` layer)
- `MLAT-framework.md` answers: **how do we measure it across the full pipeline?**

They are designed to be readable in any order. Each has companion document pointers
to the others.

---

## Key Terminology

| Term | Definition |
|------|-----------|
| **S** | Original human intent, expressed in natural language |
| **U** | The user — first mover; produces S; S evolves through iteration |
| **NDD Closure** | The totality condition: all four MLAT levels pass |
| **MLAT** | Multi-Level Alignment Test — the four-level measurement instrument |
| **J₁ Ideation Judge** | Did authoring/text2SPL preserve U's intent in S? |
| **J₂ Design-time Judge** | Does the `.spl` faithfully encode S? (`[CLOSED]`/`[DIVERGED]`) |
| **J₃ Runtime Judge** | Did `splc` preserve semantics in the compiled target? (deterministic — echo oracle) |
| **J₄ Behavior Judge** | Does deployed behavior match S? (statistical — trace sampling) |
| **Agentic integrity** | Philosophical framing (NDD-position.md) — the degree to which an agent consistently satisfies J(S, Sᵢ) = CLOSED over time |
| **Alignment score** | Engineering framing (MLAT) — measurable, no philosophical claims required |

**Terminology note:** "Agentic integrity" is the philosophical framing used in
`NDD-position.md`. For the arXiv paper and engineering contexts, the preferred
term is **alignment** (MLAT measures alignment, not integrity). This avoids
philosophical objections while preserving the full depth of the idea in the
position paper for those who want it.

---

## The Core Argument in One Paragraph

NDD extends TDD into the AI-assisted SDLC era. TDD made tests the first-class
specification artifact at the implementation layer. NDD extends this one layer
up — to the requirements layer — using natural language as the specification
medium. MLAT is the test harness: four judges, one per transformation boundary
in the intent-to-deployment pipeline, grounded in round-trip fidelity (the same
principle that makes codecs, compilers, and LLM training work). NDD Closure is
reached when all four pass. SPL is the reference test-bed — the full NDD loop
is implementable in under 40 lines of declarative SPL.

---

## What We Are Asking Reviewers to Evaluate

### 1. Clarity and coherence across the three documents
- Does the division of labor (why / what / how-to-measure) come through clearly?
- Can each document stand alone, or do critical concepts require reading all three?
- Is the terminology consistent? (Check especially: "closure" vs. "alignment",
  U → S iteration, J₁–J₄ judge names)

### 2. MLAT-framework.md — engineering soundness
- Is the four-level framework well-motivated? Does each level genuinely isolate
  a different class of failure?
- Section 2 (physical grounding): does the physics analogy add or distract?
- Section 10 (NDD as AI-assisted SDLC): does the TDD/SDLC extension feel like a
  natural evolution or a stretch?
- Is the "U as first mover, S evolves" framing (§10.1–10.3) coherent and novel?

### 3. NDD-closure.md — formal correctness
- Is the single-level closure definition (§2) rigorous enough for an arXiv paper?
- Section 6 (SPL v2.0 real-world validation): is this the right level of detail,
  or does it need tightening?
- Does the J₂ scope note (§2.1) clarify or add noise?

### 4. NDD-position.md — philosophical and safety arguments
- Section 0 (integrity as closure, Noether, Wang Yangming, Buddha): does this
  grounding strengthen or weaken the paper's credibility? (Note: this section is
  explicitly flagged as *not* for the arXiv paper — it is for the authors.)
- The AI safety argument (§0, "Agentic Integrity as AI Safety Mechanism"):
  is the detection-vs-prevention framing compelling?
- §7.5 literature search results: do the "agentic integrity" and
  "closure-based AI safety" verdicts hold up? Are there prior works we missed?

### 5. Overall positioning
- The paper introduction strategy is: "NDD extends TDD in AI-assisted SDLC,
  SPL is the test-bed." Does this framing minimize friction while making a
  strong claim?
- Is there a risk that MLAT (four levels) is seen as overreach vs. NDD-closure
  alone (single level, already implemented)? Should the paper lead with the
  implemented J₂ and introduce MLAT as future work?

---

## Notes from Wen

```User
Dear XYZ, 
I am developing a test framework as part of SPL (Structured Prompt Language) research project, please review the attached 3 files, Thank you!

| File | Role | Read when |
|------|------|-----------|
| `MLAT-framework.md` | **MLAT: the four-level measurement framework** — operational, engineering-focused | Start here for the full picture |
| `NDD-closure.md` | **NDD Closure: formal definition** — single-level (J₂) closure property, SPL implementation, real-world validation | Start here for the formal/technical core |
| `NDD-position.md` | **Position paper** — philosophical grounding, Noether analogy, agentic integrity, AI safety implications | Start here for the "why it matters" argument |

```

---

*The backup originals (`NDD-closure-orig.md`, `NDD-position-orig.md`) are
preserved in this folder to document the thought process.*
