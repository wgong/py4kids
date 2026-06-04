# NDD Position Paper: Natural-language Driven Development as Rigorous Software Engineering

**Author:** Wen G. Gong  
**Date:** April 12, 2026 (updated April 2026)
**Status:** Position note for SPL v3.0 arXiv paper  
**Companion documents:**
- `NDD-closure.md` — formal definition of NDD closure; SPL implementation; real-world validation
- `MLAT-framework.md` — MLAT: four-level measurement framework; NDD as AI-assisted SDLC

---

## 0. A Philosophical Lens: Integrity as Closure

Before the formal machinery, there is a human-scale intuition.

A person forms an *intent* — an idea of what they want to do. They express it in *words* — a declaration, a promise, a specification. They take *action* — implementation, execution, behavior. Then they — or someone else — *check the outcome*: does what was done faithfully reflect what was said?

A person who does this consistently and truthfully, across many contexts and over time, is a person of high integrity. The word *integrity* comes from the Latin *integer* — whole, undivided. A person of integrity is one whose inner state, outer declaration, and action form a coherent whole. We trust such people because their word reliably predicts their deed.

This principle has been recognized independently across philosophical traditions:

- **Wang Yangming** (明, ~1500): 知行合一 — *"the unity of knowing and acting."* True understanding of something is expressed in action. If your behavior diverges from your stated understanding, you did not truly know it. Closure failure is an epistemological deficiency, not just a behavioral one.
- **Aristotle's phronesis**: practical wisdom — the virtue that bridges good intention and good action. Integrity requires not just good intent but the capacity to translate it faithfully into the world.
- **Kant's universalizability**: act only on maxims you could universalize — which presupposes consistency between stated principle and action across all instances. The closure check is the per-instance test of that consistency.

### Noether's Theorem for Intent

Emmy Noether proved that every continuous symmetry of a physical system corresponds to a conserved quantity. The symmetry of time-translation conserves energy; the symmetry of spatial rotation conserves angular momentum. The theorem unifies what had appeared to be separate conservation laws under a single structural principle.

NDD closure is the analogous claim for software intent: the round-trip symmetry `spec → code → spec` corresponds to a conserved semantic quantity — the *intent* of the specification. If the transformation `G` (code generation) and its inverse `E` (spec extraction) are mutually faithful, semantic intent is conserved across the boundary. If they are not, intent has been lost — and the system can measure exactly where.

This is not a metaphor. It is the same structural argument: a claimed symmetry (semantic preservation) implies a conserved quantity (intent), and the round-trip test is the empirical probe of whether the symmetry holds.

### The normalization that makes this a system design principle

Before large language models, human intent and machine behavior were incommensurable. Human intent lives in natural language; machine behavior lives in code, logs, binary output. No common language existed in which to apply the integrity test across the human-machine boundary.

LLMs changed this. Both human specifications and machine-extracted specifications can now be expressed in natural language. The interface is normalized. For the first time, the same closure test — `J(stated_intent, extract_intent(behavior)) = CLOSED?` — applies symmetrically to human agents and AI agents. The boundary between "human accountability" and "machine accountability" dissolves into a single, uniform criterion.

This is the philosophical generalization: **NDD closure is a formalization of integrity, applicable to any agent — human or artificial — whose interface is natural language.** A trustworthy agent is one with a consistently high closure rate. A trustworthy agentic system is one designed so that every transformation in the intent → spec → action chain is verifiable for closure.

The `splc` compiler, the `code_pipeline` recipe, and the `spec_judge` workflow are instantiations of this principle in one domain. The principle itself is domain-agnostic:

```
Intent (idea)
    │  express
    ▼
Spec (declared)
    │  implement
    ▼
Behavior (action)
    │  extract_intent
    ▼
Spec' (reconstructed)
    │  judge
    ▼
J(Spec, Spec') ∈ {CLOSED, DIVERGED}
```

Applied to a software agent: trustworthiness is a measurable closure rate over time.
Applied to a multi-agent system: coalition trust is grounded in each member's closure history.
Applied to a product organization: roadmap → engineering spec → shipped feature → [CLOSED]? Companies that consistently close this loop are trusted; those that diverge are not.

The SPL v3.0 contribution is to make this principle *executable* — not as philosophy, but as a 40-line declarative workflow that runs on commodity hardware and returns a machine-checkable verdict.

### Coining the term: Agentic Integrity

We propose the term **agentic integrity** to name this property precisely: the
degree to which an agent — human or artificial — consistently satisfies
`J(stated_intent, extract_intent(behavior)) = CLOSED` over time.

*Note on terminology:* "Agentic integrity" is the philosophical and ethical framing
developed in this document. The engineering measurement instrument is the
**Multi-Level Alignment Test (MLAT)**, defined in `MLAT-framework.md`. MLAT operationalizes
agentic integrity as a measurable, four-level alignment score across the full
intent-to-deployment pipeline — without requiring any philosophical claims about the
nature of the system being measured. The two framings are complementary: this document
establishes *why* the criterion matters; MLAT establishes *how* to measure it.

Agentic integrity is not a new idea. It is one of the oldest ideas in human civilization. What is new is:

1. **The interface normalization.** AI agents now operate in natural language — the same medium in which human intentions are formed and stated. This makes the closure test applicable across the human-machine boundary for the first time.
2. **The executable formalization.** NDD closure gives agentic integrity a machine-checkable definition. It moves the concept from an ethical aspiration to a measurable engineering property.
3. **The system design implication.** An AI system designed for agentic integrity is one in which every transformation in the intent → spec → action chain is instrumented for closure verification. This is a design principle, not a post-hoc audit.

### Buddha: the strongest proof-by-existence

If Wang Yangming codified agentic integrity as philosophy, the Buddha instantiated it as a living system — and used his life as the proof.

After enlightenment under the Bodhi tree, the Buddha faced a choice: remain in silent liberation, or teach. The choice he made — to teach — was itself the statement of intent: *liberate all beings who seek liberation.* What followed was a 45-year implementation:

- **Intent:** liberation of all who seek it
- **Spec (Dharma):** systematically versioned teachings — Four Noble Truths, Eightfold Path, Prajnaparamita — adapted to different audiences, different runtimes
- **Implementation:** he walked. Village to village, teacher to student, for four decades. The action matched the word without deviation.
- **Closure condition:** the Bodhisattva vow — *"I will continue until all beings are liberated"* — is literally a `WHILE NOT closed` loop: the loop runs as long as the closure criterion is not globally satisfied.
- **Closure check:** the Sangha carried the Dharma forward. Successive traditions — Theravada, Mahayana, Vajrayana — are compilation targets of the same source, each adapting the intent to a different execution environment, each checkable for semantic fidelity to the original.

What makes Buddha the supreme exemplar of agentic integrity is not the enlightenment — it is the **choice not to stop there.** Liberation without teaching would be intent without implementation: `G(S)` without `E(G(S))`. The Buddha completed the loop. He submitted to the closure check by making his understanding observable, transmissible, and verifiable across centuries. The Dharma is the spec that survived round-trip fidelity across 2,500 years of compilation targets.

The lineage of this principle through human thought:

```
Buddha         (~500 BCE)  — lived agentic integrity as proof-of-concept
Confucius      (~500 BCE)  — 信 (xìn): trustworthiness as a cardinal virtue;
                             the person whose word and deed align
Wang Yangming  (1472 CE)   — 知行合一: formalized intent-action unity as epistemology
NDD closure    (2025 CE)   — J(S, E(G(S))) = CLOSED: formalized as a machine-checkable
                             criterion applicable to any natural-language-interfaced agent
```

The through-line is unbroken. What changes across these 2,500 years is not the principle but the substrate: from human conduct, to philosophical doctrine, to executable system design. SPL v3.0 is the latest compilation target of the same ancient intent.

---

> **Note:** The philosophical content above — Buddhism, Wang Yangming, the integrity lineage — is grounding for the authors, not content for the arXiv paper. It is preserved here because it establishes *why* the formal criterion matters at the deepest level. The arXiv paper argues from engineering and mathematics; this document argues from first principles. Both are necessary; they belong in different places.

---

### Agentic Integrity as an AI Safety Mechanism

The philosophical grounding has a direct, practical implication for AI safety that *does* belong in the paper's discussion section — framed in engineering terms, not philosophical ones.

**The deception constraint.** A malicious or deceptive AI system faces a structural problem: it cannot sustain high agentic integrity while pursuing a divergent intent. To deceive, it must state one intent and act on another. This is exactly the closure failure `J(stated_intent, extract_intent(behavior)) = DIVERGED`. The deception is detectable by the same mechanism used to evaluate any agent.

This reframes AI safety from a *prevention problem* to a *detection and containment problem*:

| Framing | Question | Tractability |
|---------|----------|-------------|
| Alignment (prevention) | How do we instill correct values before deployment? | Hard — unobservable internal states |
| Agentic integrity (detection) | Does the agent's behavior match its stated intent over time? | Tractable — observable, measurable, continuous |

The detection framing mirrors how human societies actually manage bad actors. We do not prevent crime by perfecting human nature before birth. We detect it through observable behavior, adjudicate it against stated norms, and isolate persistent violators. The existence of criminals does not make society impossible — it makes accountability systems necessary.

Applied to AI: the existence of potentially deceptive or misaligned agents does not make agentic systems dangerous by default. It makes **agentic integrity monitoring** necessary. An agent that consistently achieves `[CLOSED]` is trustworthy. An agent that persistently returns `[DIVERGED]` — whose stated purposes do not match its reconstructed behavior — is a candidate for quarantine, retraining, or shutdown.

**The audit trail.** Because NDD closure operates on natural-language artifacts (spec in, spec extracted out), the entire chain is human-readable and auditable:

```
stated_intent.txt  →  behavior log  →  extracted_intent.txt  →  [CLOSED | DIVERGED]
```

This is not a black-box safety check. It is a transparent, versioned record of whether an agent kept its word — inspectable by humans, regulators, or other agents in a multi-agent system.

**Scaling to multi-agent trust.** In a network of agents, each agent's closure history becomes its *trust score*. Coalition formation, task delegation, and resource allocation can all be conditioned on closure history. An agent that has never diverged is a reliable collaborator. An agent with a pattern of divergence is isolated — not by a central authority deciding values in advance, but by the emergent behavior of agents who have learned to recognize closure failure.

This is not a utopian claim. Human societies have bad actors despite millennia of moral philosophy. Agentic systems will have bad actors too. The claim is narrower and more useful: **agentic integrity monitoring provides a principled, automatable, continuously-operating detection mechanism** — the same mechanism used to verify code generation quality, compiler faithfulness, and organizational accountability, now applied to AI agent behavior.

---

## 1. The Problem with Vibe-Coding

When "vibe coding" entered the mainstream lexicon in early 2025, it described something real: developers using LLM-generated code by feel, iterating conversationally, accepting outputs that "look right." The practice spread rapidly because the productivity gains are genuine. But the engineering rigor is absent.

The core failure mode is not that LLMs produce bad code — they often produce good code. The failure mode is that there is no *accountability chain*. The specification lives in a chat window, gets consumed by the model, and disappears. The developer accepts the output based on subjective judgment. There is no machine-checkable criterion that links the final artifact back to the original intent.

This is not a new problem. It is the same problem that motivated Test-Driven Development (TDD) in the late 1990s: code that "looks correct" is not the same as code that *is* correct. TDD's answer was to make the correctness criterion explicit — written before the code, executable, non-negotiable. NDD applies the same discipline one layer up: to the specification itself.

---

## 2. NDD Builds on TDD — It Does Not Replace It

TDD operates at the implementation layer:

```
[failing test] → [minimal code] → [passing test] → [refactor]
```

The test is the correctness criterion. It is written in code and is deterministically executable.

NDD operates at the requirements layer:

```
[natural-language spec] → [generate code + tests] → [closure check]
```

The two compose vertically:

```
Intent (natural-language spec)
        │
        ▼  NDD: verifies that code faithfully encodes intent
   Code + Tests
        │
        ▼  TDD: verifies that code behaves correctly on enumerated cases
   Verified behavior
```

TDD cannot verify that the tests themselves correctly capture the intent — tests are written by humans who may have misread the spec. NDD closes this gap by checking the relationship between spec and code *independently* of the test suite, using the closure property.

The full engineering chain is:

| Layer | Discipline | Correctness criterion |
|-------|-----------|----------------------|
| Intent | NDD | `J(S, E(G(S))) = CLOSED` |
| Implementation | TDD | all tests pass |
| Deployment | DODA | same `.spl` runs on all targets |

Each layer has a machine-checkable criterion. None relies on subjective judgment alone.

---

## 3. Round-Trip Fidelity: The Mathematical Foundation

The NDD closure property is an instance of a general principle in mathematics and physics: **to validate that a mapping and its inverse are correct, apply both in sequence and verify you return to the starting point.**

This principle appears throughout the sciences:

- **Algebra:** `f` and `g` are mutual inverses iff `g(f(a)) = a` for all `a ∈ A` and `f(g(b)) = b` for all `b ∈ B`. No weaker test suffices to establish the bijection.
- **Information theory / serialization:** `decode(encode(x)) = x` is the canonical correctness criterion for a codec. If this does not hold, the codec is lossy at the semantic level.
- **Physics:** A physical theory that claims a reversible transformation must demonstrate time-reversal symmetry experimentally — forward evolution followed by reverse evolution returns to the initial state.
- **Compiler verification:** A compiler is semantics-preserving iff the behavior of the compiled program equals the behavior of the source program on all inputs. Round-trip decompilation is one empirical probe of this property.

In NDD, the two mappings are:

```
G : Spec → Code          (code generation)
E : Code → Spec          (spec extraction / reverse-engineering)
```

The closure test is:

```
E(G(S)) ≈ S
```

If this holds, `G` is a faithful encoding of intent and `E` is its left-inverse — the system has demonstrated that it can correctly traverse the intent ↔ artifact boundary in both directions. If it does not hold, semantic drift has occurred: the generated code encodes something other than what the specification said.

This is not a heuristic. It is the same logical structure that physicists use to validate symmetries and that protocol designers use to validate codecs. Applying it to LLM-mediated code generation gives NDD its mathematical grounding.

---

## 4. The `splc` Compiler: A Second Domain for the Same Closure Test

The NDD closure property was first conceived as a correctness criterion for *LLM-generated code*. But the April 2026 insight is that the same criterion applies directly to the **`splc` compiler**.

`splc` compiles a `.spl` source file to a target runtime:

```
.spl source  ──splc──►  Go binary
                    ──►  Python / LangGraph
                    ──►  TypeScript / edge
```

The claim `splc` must satisfy is: **the compiled target implements the same workflow semantics as the `.spl` source.** This is a semantic preservation claim — exactly the kind of claim that round-trip fidelity is designed to test.

### 4.1 The deep connection: LLMs already embody round-trip fidelity

There is a non-obvious reason why NDD closure works in practice: the LLMs that power `G` (code generation) and `E` (spec extraction) were themselves trained under round-trip fidelity objectives. Auto-encoders, seq2seq models, and transformers all learn by reconstructing their input through a latent representation — `decode(encode(x)) ≈ x` is the training signal. The model's internal representations are shaped by round-trip fidelity at the token level.

NDD closure applies the same principle one level up — at the *semantic intent* level rather than the token embedding level. The LLMs are not being asked to do something foreign to their training; they are being asked to demonstrate, in the development workflow, the same fidelity they learned during pretraining. This alignment between training objective and evaluation criterion is why the `spec_judge` workflow can reliably discriminate `[CLOSED]` from `[DIVERGED]` — the model has been optimized for exactly this kind of reconstruction judgment.

### 4.2 NDD-closure as a `splc` validation suite

Given a `.spl` workflow `W` and a natural-language description `S` of what `W` does:

1. Run `W` interpreted (SPL runtime) on inputs derived from `S` → observe outputs.
2. Run `splc(W)` (compiled target) on the same inputs → observe outputs.
3. Apply spec extraction to both outputs → compare derived specs.
4. If `J(S, E(output_interpreted)) = CLOSED` **and** `J(S, E(output_compiled)) = CLOSED`, the compiled target is semantically faithful.

More directly: the `code_pipeline.spl` recipe itself can be used as the validation harness for any `splc` compilation target. Feed the same spec in; run both the interpreted and compiled versions; check that both achieve closure. If only the interpreted version closes, `splc` has introduced semantic drift.

### 4.3 Human governance at every level; hard stop at J₂

Human judgment governs the full MLAT pipeline at every level — J₁ through J₄.
At each boundary, the divergence report is shown to U, who determines whether
the cause is system drift, specification ambiguity, or both. See `MLAT-framework.md`
§10 for the complete iterative governance model (U as first mover, S evolving
through cycles).

Within the J₂ level specifically — NDD closure on the `.spl` artifact — a
deliberate design decision applies: `[DIVERGED]` triggers a **hard stop**, not
an automatic refinement loop.

The reasoning is architectural. Code-level failures (`[FAILED]` in `test_code`) are within the agent's competence boundary — the agent knows the spec, knows the test results, and can regenerate or improve the code autonomously. This is the inner `WHILE` loop.

Spec-level failures (`[DIVERGED]` in `spec_judge`) are at the boundary of the agent's mandate. A divergence means the generated code does not faithfully encode the original specification — and the correct fix may require *changing the spec*, which is the human's artifact. An agent that silently rewrites the spec to match the code has not fixed the problem; it has destroyed the accountability chain.

The design principle:

> **The agent executes autonomously within its competence boundary. When it cannot resolve a condition — particularly one that requires modifying the authoritative specification — it escalates to the human.**

SPL v3.0 implements this via the `EXCEPTION` channel and hard-stop semantics on `[DIVERGED]`. A human-in-the-loop approval step can be inserted at this boundary — the agent surfaces the divergence report, the human reviews and either revises the spec or accepts a controlled drift, and the pipeline resumes. The agent never makes that decision unilaterally.

This mirrors sound organizational design: autonomous execution within delegated scope, mandatory escalation when the decision exceeds the delegate's authority. A hard stop is not a failure — it is the agent correctly recognizing the limit of its mandate.

### 4.4 Why this matters for DODA

The DODA (Design Once, Deploy Anywhere) paradigm promises that the `.spl` script is the invariant across deployment targets. That promise is vacuous without a way to verify it. NDD-closure provides exactly that verification: a falsifiable, automated test that the compiled binary/module implements the original intent — not just the same control flow, but the same *meaning*.

```
.spl spec  ──splc──►  compiled target
    │                        │
    └─────── NDD-closure ────┘
             J(S, E(G(S))) = CLOSED?
```

This convergence — NDD-closure as the `splc` correctness criterion — was not anticipated when either concept was initially formulated. It emerged from the observation that both code generation and compiler output are *transformations that claim to preserve semantics*, and that round-trip fidelity is the canonical test for exactly that class of claim.

---

## 5. NDD vs. Vibe-Coding: The Engineering Comparison

The following table positions NDD against vibe-coding across the dimensions that matter for production software engineering:

| Property | Vibe coding | NDD |
|----------|------------|-----|
| Specification | Informal prompt, ephemeral | Typed `@spec TEXT`, versioned artifact |
| Loop control | Human (accept / reject) | Automated (`WHILE`, `EVALUATE`, sentinel tokens) |
| Correctness criterion | Human judgment ("looks right") | `J(S, E(G(S))) = CLOSED` (machine-checkable) |
| Reproducibility | Session-dependent | Deterministic given `@spec` |
| Testability | Ad hoc | Each sub-workflow independently testable (INPUT/OUTPUT contracts) |
| Accountability chain | Broken at spec → code boundary | Continuous: spec → code → test → extract → judge |
| Composability | Tool-dependent | `CALL` sub-workflow (SPL native) |
| Compiler validation | N/A | NDD-closure applies to `splc` targets |
| Grounding | Cultural practice | TDD + round-trip fidelity (mathematics) |

The gap is not about LLM quality. A vibe-coder using the best available model and a disciplined NDD practitioner using the same model will produce different outcomes — not because the code differs in the first iteration, but because NDD has a closed-loop verification step that catches semantic drift before it propagates into production.

---

## 6. Practical Evidence: The `code_pipeline` Unit Tests

The testability claim is not theoretical. The `cookbook/56_code_pipeline/tests/` directory demonstrates it concretely:

```
tests/
├── mock/                     # first-class spec artifacts
│   ├── spec_clear.txt        # the @spec input
│   ├── spec_vague.txt        # negative case: [VAGUE] sentinel
│   ├── code_good.py          # correct G(S)
│   ├── code_buggy.py         # incorrect G(S) — known defects
│   ├── feedback.txt          # reviewer output
│   └── spec_extracted.txt    # E(G(S)) — close paraphrase of spec_clear.txt
├── 00_analyze_spec_test.sh   # test: [READY] / [VAGUE]
├── 04_test_code_test.sh      # test: [PASSED] / [FAILED]
├── 07_spec_judge_test.sh     # test: [CLOSED] / [DIVERGED]
└── run_all_tests.sh
```

Each `.spl` sub-workflow is unit-tested in isolation — not because SPL has special testing machinery, but because the `INPUT` / `OUTPUT` contracts define clean boundaries. This is the direct engineering consequence of specification-first design: testable interfaces emerge naturally from explicit contracts.

The sentinel tokens (`[READY]`, `[PASSED]`, `[CLOSED]`, `[DIVERGED]`) are machine-checkable exit criteria. They are the NDD equivalent of TDD's `PASS` / `FAIL` — unambiguous, greppable, automatable.

---

## 7. Related Work and Prior Art

### 7.1 Where the principle already appears

The round-trip fidelity principle is not new. It appears in several established bodies of work, each applying the same structure `f⁻¹(f(x)) ≈ x` in a different domain:

| Domain | Forward mapping `G` | Reverse mapping `E` | Closure criterion |
|--------|--------------------|--------------------|-------------------|
| Auto-encoder (ML) | `encode(x) → z` | `decode(z) → x̂` | minimize `‖x − x̂‖` |
| Seq2seq / transformer | `encode(source) → context` | `decode(context) → target` | cross-entropy loss on reconstruction |
| Back-translation (NLP) | `translate(EN → FR)` | `translate(FR → EN)` | surface similarity to original |
| Round-trip engineering (MDE) | `model → code` | `code → model` | structural equivalence of models |
| Translation validation (compilers) | `compile(source) → binary` | semantic equivalence proof | bisimulation / behavioral equivalence |
| **NDD closure** | `generate_code(spec) → code` | `extract_spec(code) → spec'` | `J(spec, spec') = CLOSED` |

The insight worth stating precisely: **the same round-trip fidelity principle that governs how LLMs are trained is what NDD applies at the level of software development methodology.**

Auto-encoders and seq2seq models learn round-trip fidelity at the *token embedding* level — the training objective is reconstruction of the input distribution. NDD closure enforces round-trip fidelity at the *semantic intent* level — the correctness criterion is reconstruction of the specification's meaning. The principle is the same; the granularity has moved from tokens to intent.

### 7.2 What is genuinely new

The prior art establishes the mathematical substrate. What NDD contributes that is not present in any of the above:

1. **Named development methodology.** Round-trip fidelity in ML training is an optimization objective, not a development practice. NDD formalizes it as a named, repeatable workflow with explicit roles for `G`, `E`, and `J`.

2. **Correctness criterion at the intent level.** Existing tools (unit tests, static analysis, formal verification) operate at the implementation level. NDD closure operates at the *intent* level — it checks whether the code means what the specification said, independently of whether the code passes its tests. A system can pass all unit tests and fail closure; this is the case NDD uniquely catches.

3. **Practical implementability at 40 lines.** The round-trip engineering literature requires formal metamodels and bidirectional transformation languages (QVT, ATL). NDD closure is implemented in 40 lines of declarative SPL using `CALL` composition — accessible to any practitioner with a text editor and an Ollama instance.

4. **Generalization to compiler validation (`splc`).** No prior work applies round-trip fidelity as the correctness criterion for a *compiler* that targets natural-language-specified workflows. This is the `splc` contribution: DODA's promise ("same `.spl` on all targets") is made falsifiable by NDD closure.

### 7.3 LLM errors as epistemological failures

Wang Yangming's formulation — "if your behavior diverges from your stated understanding, you did not truly know it" — has a practical engineering implication that goes beyond philosophy.

When a closure check returns `[DIVERGED]`, the conventional response is to patch the code. NDD reframes the diagnosis: the system did not truly *understand* the specification. The correct response is to improve the spec — clarify ambiguity, tighten the contract, resolve the vagueness that allowed semantic drift. This redirects engineering effort toward requirements quality rather than bug-fixing — which is where the root cause lives.

This reframing also changes how we think about LLM capability limits. A model that consistently fails closure on a given spec class is not "bad at coding" — it is epistemically limited with respect to that spec class. The closure score is a diagnostic of understanding depth, not just output quality.

### 7.4 The closure metric: boolean vs. continuous

"Vibe coding" (Karpathy, February 2025) describes a *practice*, not a methodology. It offers no correctness criterion and makes no claim about round-trip fidelity. NDD is its methodological counterpart: it takes the same LLM capability and wraps it in the accountability structure that engineering requires. The comparison is not adversarial — vibe coding demonstrates that LLMs are capable enough to make NDD tractable.

The current SPL implementation uses a boolean gate: the `spec_judge` workflow returns `[CLOSED]` or `[DIVERGED]` via sentinel tokens — a hard threshold set by the judge prompt. This is sufficient for the reference implementation and for unit tests.

A continuous `alignment_score ∈ [0, 1]` based on embedding cosine similarity between `spec` and `spec'` would enable gradient-based monitoring (trending toward divergence before the hard threshold is crossed) and is proposed as near-term future work. Both modes — boolean sentinel for decisions, continuous score for monitoring — are architecturally compatible with the same `spec_judge.spl` sub-workflow.

### 7.5 Literature search results (Gemini deep research, 2026-04-12)

A systematic literature search was conducted by Gemini across arXiv preprints and major 2025–2026 conference proceedings (ICML, NeurIPS, FAccT).

**"Agentic integrity"** — found in three clusters: (1) operational security (Statnikov, Medium Feb 2026: "provenance of instruction" against hallucinated commands), (2) corporate finance ("Agentic Revenue Integrity" in AI-native audit tools), (3) hardware/system risk ("Agentic Integrity Risk" following LLM-based OS agent incidents). None provides a formal mathematical definition. **Verdict: we are the first to define this as a closure property — `J(S, E(G(S))) = CLOSED`.**

**"Closure-based AI safety"** — no exact phrase match in any arXiv preprint or conference proceedings. Closest parallel: *Adversarial Intent is a Latent Variable* (arXiv:2602.21447, Feb 2026), which uses POMDPs for stateful trust inference in agentic RAG — no round-trip or closure terminology. "Constitutional Closure" has appeared in small circles but refers to action-space constraints, not semantic round-trip fidelity. **Verdict: novel phrase. Claim it.**

The substrate (round-trip fidelity) is well-attested across many domains. The specific application to NDD as a software engineering methodology, and to agentic integrity as a behavioral AI safety mechanism, is novel.

---

## 8. Summary: Why NDD Is a Rigorous Engineering Foundation

NDD is not a reaction to vibe-coding. It was formulated independently, before "vibe coding" entered common usage, as a principled answer to the question: *how do you apply the rigor of software engineering to a development process mediated by natural language?*

The answer has three parts:

1. **Make the spec a typed artifact.** Natural language treated as ephemeral prompt is not engineering. Natural language as a versioned, typed `@spec TEXT` value that flows through an automated pipeline *is* engineering.

2. **Close the loop with round-trip fidelity.** The mathematical foundation is not new — it is the same bijection test that validates codecs, compilers, physical symmetries, and the training objectives of the very LLMs that power NDD. Applying it to the spec ↔ code boundary gives NDD a falsifiable correctness criterion that neither TDD nor vibe-coding provides. The principle is borrowed from the LLMs' own learning structure and elevated one level: from token reconstruction to intent reconstruction.

3. **Compose with existing engineering practice.** NDD does not replace TDD. It extends the accountability chain upward into the requirements layer. The two disciplines compose: TDD verifies behavior, NDD verifies intent. Together they cover the full chain from natural-language specification to verified, deployed software.

The `splc` convergence — NDD-closure as the semantic preservation test for compiled SPL targets — is the key architectural insight: DODA's promise ("same `.spl` on all targets") is only meaningful if there exists a machine-checkable criterion that the compiled target preserves the original intent. NDD-closure *is* that criterion. It transforms DODA from a design aspiration into a verifiable engineering guarantee.

Wherever a transformation claims to preserve semantics, round-trip fidelity is the test. NDD makes that test explicit, automated, and part of the standard development loop — grounded in the same principle that makes neural networks learn, codecs compress, and compilers preserve meaning.



---

> **Literature search note:** When Gemini does the deep literature search,
> "agentic integrity" and "closure-based AI safety" are worth searching as
> exact phrases.