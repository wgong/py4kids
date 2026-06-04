# Concept-based micro-textbook — linear algebra

A cookbook recipe sketch for SPL. The model proposes the conceptual structure
(probabilistic); a symbolic layer guarantees it is genuinely *generative* —
built from a minimal primitive basis, and aimed at a payoff — rather than a
flat list of topics.

`SOLVE`, `ASSERT`, `primitive`, `concept`, and `application` are the proposed
new constructs. Everything else (`GENERATE`, `CALL`, `EVALUATE`, `RETRY`,
`INTO`, `:=`, `COMMIT`) already exists in spl3.

The textbook is designed **backward from a target** — for linear algebra the
target is spectral analysis, the point where the two radicals meet and the
reductionist story closes.

---

## 1. The reductionist basis

Declare the floor explicitly, the way physics declares its base dimensions.
Below this floor we do not reduce.

**Primitives (irreducible "radicals"):**

| Primitive | Symbol | Note |
| --- | --- | --- |
| field of scalars | `F` | the floor for scalars; we do not reduce the field |
| carrier set | `V` | set theory is below the floor |
| vector addition | `⊕ : V×V→V` | first radical |
| scalar multiplication | `⊙ : F×V→V` | first radical |
| inner product | `⟨·,·⟩ : V×V→F` | **second radical** — introduced only in the geometry module; not reducible to ⊕, ⊙ |

The vector-space **axioms** (associativity, distributivity, identity, inverse)
are not new primitives — they are the *composition grammar*, the analog of
"only add quantities of the same dimension."

**The single most productive node** (highest out-degree in the graph):

```
linear_combination  =  Σ αᵢ ⊙ vᵢ           # composed only of ⊙ and ⊕
```

Almost the entire first half of the course is a statement *about* linear
combinations. It is the 木 of linear algebra.

---

## 2. The composition graph (composed-of, not just comes-before)

Each node names what it is *made of*. Reading downward = increasing composition,
not merely teaching order.

```
linear_combination     ← ⊕, ⊙
  subspace             ← closed under linear_combination
  span                 ← all linear_combinations of a set
  linear_independence  ← uniqueness of the trivial zero combination
    basis              ← linear_independence ∧ span
      dimension        ← | basis |               (well-defined: exchange lemma)
      coordinates      ← unique coefficients over a basis
  linear_map           ← function preserving linear_combination
    matrix             ← linear_map in coordinates (basis-dependent)
    matrix_mult        ← coordinate form of map composition  (DERIVED — definition is forced)
    image / col_space  ← span of columns
    kernel / null_space← { v : f(v)=0 }
      rank             ← dimension(image)
      nullity          ← dimension(kernel)
      rank_nullity     ← rank + nullity = dimension(domain)   (composite theorem)
    determinant        ← alternating multilinear form on a linear_map
    eigenpair          ← (λ, v≠0) with f(v) = λ ⊙ v           (a fixed linear_combination)
      diagonalization  ← basis of eigenpairs                  (operator → independent ⊙'s)

[second radical: ⟨·,·⟩]
  norm                 ← √⟨v,v⟩
  orthogonality        ← ⟨u,v⟩ = 0
  projection           ← orthogonality + span
  orthonormal_basis    ← basis + orthogonality
  gram_schmidt         ← projection + orthonormal_basis
  adjoint / transpose  ← ⟨·,·⟩ + linear_map
  spectral_theorem     ← adjoint + eigenpair + orthonormal_basis   ◀── TARGET
```

Headline property the verifier enforces: **every node above reduces, transitively,
to {F, V, ⊕, ⊙} or to ⟨·,·⟩.** Nothing else is allowed to be primitive.

**Application edges (external reach — the payoff, and the second edge type):**

```
normal_modes        ← eigenpair                 (mechanics)
stability_analysis  ← eigenpair                 (dynamical systems)
markov_stationary   ← eigenpair                 (probability)
pagerank            ← eigenpair                 (networks)
pca                 ← eigenpair + inner_product (statistics)
quantum_observable  ← spectral_theorem          (quantum mechanics)
fourier_modes       ← spectral_theorem          (signals / analysis)
```

These edges point *out* of linear algebra. They are what makes the eigen cluster
fundamental: its fan-out is mostly external, so it looks late in the composed-of
order but ranks high once reach counts the payoff (§5).

---

## 3. The verifier mapping

Three deterministic checks replace "trust the model":

1. **Shape / type check — the dimensional-analysis analog.**
   Vector dimensions and matrix shapes must compose: `(m×n)·(n×p) → m×p`;
   `⊕` requires equal dimension. Adding a 3-vector to a 2-vector is a type error,
   exactly like adding metres to seconds. Checkable with NumPy/SymPy shapes.

2. **Symbolic recompute.** SymPy recomputes every worked example: RREF, rank,
   determinant, eigenvalues; confirms a claimed basis is independent *and*
   spanning (rank = count); verifies a solution to `Ax = b`. The example is
   verified, not plausible.

3. **Reducibility.** Graph reachability over `composed_of` must terminate only
   at declared primitives.

The eigen cluster is the cheapest of all to verify: "is `v` an eigenvector with
value `λ`?" is the one-line check `Av == λv`. A wrong eigen-example cannot
survive the loop.

---

## 4. Concept-graph schema

```
primitive vector_addition        { tier: 0 }
primitive scalar_multiplication  { tier: 0 }
primitive inner_product          { tier: 0, introduced_in: "geometry" }

concept span {
    composed_of: [linear_combination]
    defines:     "set of all linear combinations of a given set of vectors"
    verifier:    sympy        # how a worked example is checked
    shape_typed: true         # subject to the dimensional/shape check
}

concept eigenpair {
    composed_of: [linear_map, scalar_multiplication]
    defines:     "(λ, v≠0) with f(v) = λ ⊙ v — a direction the map acts on as pure ⊙"
    verifier:    sympy
    lab:         sympy        # the engine that powers the student's interactive cell
    play:        "build A; A.eigenvals(); perturb an entry; watch λ move"
}

# Application nodes carry the external (cross-domain) edges.
application quantum_observable {
    needs:  [spectral_theorem]
    domain: "quantum mechanics"
}
application normal_modes {
    needs:  [eigenpair]
    domain: "mechanics"
}
```

---

## 5. The symbolic rules

```
# (a) Reducibility — every concept bottoms out at the declared primitives
ASSERT reducible(@graph, @primitives)
    OTHERWISE RETRY GENERATE propose_concepts

# (b) New-primitive budget — at most k new radicals per section
#     (mirrors "introduce few new radicals at a time" in character pedagogy)
ASSERT new_primitives(@section) <= @primitive_budget
    OTHERWISE GENERATE refine_section(@section, "compose from prior primitives")

# (c) Reach-weighted productivity ordering, scoped to the target
#     reach(c) = (# concepts that depend on c)  +  w · (# applications that depend on c)
#     the analog of "characters unlocked", with downstream STEM payoff weighted by w
SOLVE @needed SET  := ancestors(@graph, @target)                       # composed-of closure feeding the target
SOLVE @order  LIST := productivity_order(restrict(@graph, @needed), weight = @payoff_weight)
```

`reducible`, `acyclic`, `minimal`, `new_primitives`, `ancestors`, `restrict`,
and `productivity_order` are deterministic verifiers (graph reachability +
SymPy), not generations — the symbolic half of the workflow.

---

## 6. Designing backward from the target

Spectral analysis is the endpoint, not a late afterthought. Two reasons it
belongs there:

- **It straddles both radicals.** `Av = λv` needs only ⊕ and ⊙; the spectral
  theorem's orthogonal diagonalization needs ⟨·,·⟩. Eigenvalues open the first
  half, the spectral theorem closes the second. The two radicals meet here.

- **It is the reductionist climax.** An eigenvector is a direction in which the
  map acts as pure ⊙. Diagonalization decouples the whole operator into
  independent one-dimensional ⊙'s along an eigenbasis — coupled oscillators
  resolved into normal modes. The atom you reduced everything to in §1 returns
  as the thing the hardest object decomposes into.

So the workflow takes the target as input, scopes the graph to
`ancestors(target)` — exactly the concepts the target reduces to, nothing
extra — and orders that subgraph by reach. The textbook becomes a minimal
generating path that culminates in the payoff.

---

## 7. The basis-first workflow

```
IMPORT linalg_verifiers     # reducible, acyclic, minimal, ancestors, restrict,
                            # productivity_order, verify_math, shape_check

WORKFLOW build_micro_textbook
    INPUT:  @domain TEXT, @target CONCEPT, @primitive_budget INT, @payoff_weight FLOAT
    OUTPUT: @textbook TEXT
DO
    # 1. Propose the primitive basis  (probabilistic)
    GENERATE propose_basis(@domain) INTO @primitives

    # 2. The basis must be minimal and non-redundant  (deterministic)
    ASSERT minimal(@primitives)
        OTHERWISE RETRY GENERATE propose_basis

    # 3. Propose every concept and application as explicit compositions  (probabilistic)
    GENERATE propose_concepts(@domain, @primitives, @target) INTO @graph

    # 4. No circular definitions; everything reduces to primitives
    ASSERT acyclic(@graph)
        OTHERWISE RETRY GENERATE propose_concepts
    ASSERT reducible(@graph, @primitives)
        OTHERWISE RETRY GENERATE propose_concepts

    # 5. Scope to the target, then order by reach (payoff-weighted)  (deterministic)
    SOLVE @needed SET  := ancestors(@graph, @target)
    SOLVE @order  LIST := productivity_order(restrict(@graph, @needed), weight = @payoff_weight)

    # 6. Write and verify each section in dependency order
    FOR @concept IN @order DO
        GENERATE write_section(@concept, @graph) INTO @section

        # budget: don't smuggle in undeclared primitives
        ASSERT new_primitives(@section) <= @primitive_budget
            OTHERWISE GENERATE refine_section(@section, "compose from prior primitives") INTO @section

        # recompute the math; repair on mismatch
        CALL verify_math(@section) INTO @check
        EVALUATE @check:
            WHEN fail:
                GENERATE refine_section(@section, @check) INTO @section
                CALL verify_math(@section) INTO @check

        # dimensional-analysis analog: shapes must compose
        CALL shape_check(@section) INTO @shapes
        EVALUATE @shapes:
            WHEN fail:
                GENERATE refine_section(@section, @shapes) INTO @section

        APPEND @section TO @textbook
    END

    # 7. Close on the payoff: tie the target to its applications
    GENERATE write_payoff(@target, applications_of(@graph, @target)) INTO @capstone
    APPEND @capstone TO @textbook

    COMMIT @textbook
END
```

`FOR … IN … DO … END` lowers to your existing iteration / map-reduce facility;
independent sections (no path between them in the composed-of graph) are the
natural candidates for `CALL PARALLEL`. The per-concept loop also emits one more
artifact per section — the lab cell (§8) — powered by the concept's declared
`lab` engine.

---

## 8. Learning by playing — the executable textbook

The same engine that verifies the author's example *is* the student's playground.
Verifier and lab are one tool seen from two sides: author-side, SymPy checks the
worked example is correct; student-side, SymPy gives instant, exact feedback on
the student's own manipulations. Building the verifier (§3) buys the playground
for free.

This fits the reductionist spine exactly: **to play is to compose.** The student
doesn't merely read that diagonalization decomposes an operator into independent
⊙'s — they build a matrix, diagonalise it, perturb an entry, and watch the
eigenvalues move. Applying the composition operation yourself, with the engine
confirming closure, *is* the learning.

**Each concept node carries a `lab`** — a runnable, parameterised cell alongside
its definition and verified example (see the `lab` / `play` fields in §4).

**Two game modes — the two directions of the neurosymbolic axis:**

- *Deductive puzzle* (Z3 / a solver): "find values satisfying these constraints."
  The student proposes; the solver answers SAT/UNSAT. E.g. "find coefficients
  making these vectors dependent" — UNSAT means independent.
- *Inductive discovery* (PySR / gplearn): "here is data from a hidden law —
  recover the equation." The student (or the SR engine) induces the symbolic
  form: sample points from a relationship and have them find it. The deductive
  solvers *check*; the inductive ones *discover*.

**Self-check.** The student's answer is judged by the same verifier — `Av == λv`
returns instantly and exactly. Immediate, exact, non-judgmental feedback is the
strongest reinforcement loop available.

**Delivery: emit runnable cells, not static prose.** Target Jupyter notebooks,
or — for zero-install reach — run entirely in the browser via Pyodide /
JupyterLite, where SymPy and Z3 execute client-side with no server. Tiering:
SymPy, SymEngine, and Z3 run in-browser; PySR's Julia backend needs a server, so
use **gplearn** for the in-browser discovery game and PySR for heavier
server-side discovery.

**Package → play-mode map:**

| Package | Play mode |
| --- | --- |
| SymPy / SymEngine | the universal manipulator — every concept |
| Z3 / solvers | constraint puzzles (deductive) |
| PySR / gplearn | law discovery (inductive) |
| CasADi | optimisation / dynamics sandboxes |
| SageManifolds · EinsteinPy · Cadabra2 · galgebra | physics-module labs |

---

## 9. On-demand generation — natural language → SPL → content

The delivery model: the learner asks in plain language, `text2spl` (your existing
NL→SPL transpiler) translates the question into a scoped call to
`build_micro_textbook`, and the workflow generates and verifies just the requested
slice. The textbook is authored *by demand*, not upfront.

- **NL → target.** "Why does diagonalisation work?" → `text2spl` emits
  `build_micro_textbook(target = diagonalization, …)`. This resolution is itself a
  generate-then-verify step: the model maps the question to a node; a deterministic
  check confirms the node exists (else it proposes extending the graph).
- **Scope = ancestors minus mastered.** The slice to build is
  `ancestors(graph, target)` (already computed in §7) intersected with the *gap* —
  concepts not yet in the learner's mastery set. Each bite is therefore minimal and
  personalised: a learner who already holds `span` and `basis` and asks about
  `diagonalization` gets only `eigenpair` + `diagonalization`, not the whole chain.
- **Cache + verify = a lazy textbook.** Each generated-and-verified micro-section is
  cached by concept + params. Because the verifier guarantees correctness, cached
  sections are safe to reuse; the full textbook is the union of on-demand slices,
  warming toward completeness as learners explore.
- **Why verification is now non-negotiable.** On-demand means no human author or
  editor in the loop. The symbolic verifiers (§3) and the structural diff against an
  authoritative reference (§10) are the *only* quality gate — so the strong-symbolic
  layer is what makes live, learner-driven generation safe to put in front of a
  student.

```
WORKFLOW answer_on_demand
    INPUT:  @question TEXT, @learner_state SET
    OUTPUT: @lesson TEXT
DO
    GENERATE resolve_target(@question, @graph) INTO @target      # NL → concept
    ASSERT in_graph(@graph, @target)
        OTHERWISE GENERATE extend_graph(@question, @graph) INTO @graph

    SOLVE @needed LIST := minus(ancestors(@graph, @target), @learner_state)

    FOR @concept IN productivity_order(restrict(@graph, @needed)) DO
        CALL cache_get(@concept) INTO @section
        EVALUATE @section:
            WHEN miss:
                CALL build_micro_textbook(@concept) INTO @section   # generate + verify
                CALL cache_put(@concept, @section)
        APPEND @section TO @lesson
    END
    COMMIT @lesson
END
```

---

## 10. Validation sources

A reference set for checking on-demand content — chosen for authority, a
structured / named-theorem layout that maps onto concept nodes, and an open
license. Use them to diff *structure*, not to reproduce prose.

| Text | License | Role in validation |
| --- | --- | --- |
| Axler, *Linear Algebra Done Right* 4e — https://linear.axler.net/ | CC BY-NC | The philosophical twin: determinant-free, vector-space/linear-map-first, spectral-theorem as target. Use as the reference DAG. |
| Beezer, *A First Course in Linear Algebra* — http://linear.pugetsound.edu | GNU FDL | Best structural source of truth: every theorem named, numbered, fully proved → one result per concept node. PreTeXt source reusable. |
| Hefferon, *Linear Algebra* — https://hefferon.net/linearalgebra/ | CC BY-SA | Worked answers to all exercises → validate generated *exercises*, not just statements. |
| Treil, *Linear Algebra Done Wrong* — Treil's page at Brown | Free | Proof-level rigor for the harder claims. |
| Boyd & Vandenberghe, *Applied Linear Algebra (VMLS)* — https://web.stanford.edu/~boyd/vmls/ | Free | The application / payoff edges (least squares, etc.). |
| Margalit & Rabinoff, *Interactive Linear Algebra* — https://textbooks.math.gatech.edu/ila/ | Free | Reference *and* a working model of the executable-cell delivery (§8). |
| Strang, *Introduction to Linear Algebra* + MIT OCW 18.06 — https://ocw.mit.edu | Book paid; OCW free | Concrete intuition (column space, four fundamental subspaces) to cross-check Axler's abstract view. |

**How to use as ground truth.** Extract each reference's definitions, theorem
statements, and dependency order; diff that against the generated concept graph —
do the `composed_of` edges match the reference's logical order, do definitions
agree, does each generated claim correspond to a named result. That is validating
claims and structure, which your reducibility / concept-graph machinery already
produces; the reference simply supplies the comparison DAG.

**License note.** Parse and redistribute only the open-licensed texts (Beezer FDL,
Hefferon BY-SA, VMLS). Axler's BY-NC is fine to *validate against* for a
non-commercial project, but the NC term constrains redistribution of its content.

---

## 11. Trust tiers and human-in-the-loop

Not all content carries the same warrant, and the system should say so. Every
section gets a `provenance` field:

```
section {
    concept:    eigenpair
    provenance: machine_verified        # canonical | machine_verified | machine_generated
    backed_by:  [sympy, "Av == λv"]     # what warrants it
    disclaimer: shown_unless(canonical)
}
```

- **Canonical** — traceable to an authoritative reference (§10). Target: 100%
  accuracy, validated by structural diff. Ground truth.
- **Machine-verified** — LLM-composed but passed symbolic verification: the example
  recomputed in SymPy, the constraint checked in Z3, the shapes confirmed. High
  confidence on the checkable claims.
- **Machine-generated** — LLM-composed prose that isn't mechanically checkable
  (intuition, motivation, analogy). Carries a disclaimer and is flagged for review.

**Calibrated disclaimers, not a blanket warning.** The disclaimer attaches to the
*unverifiable* layer only — "the worked example was verified symbolically; the
intuition was AI-generated and not independently checked" beats a flat "AI may be
wrong." Consequence: the better the verifiers, the smaller the disclaimer surface,
shrinking it to the genuine pedagogy and framing where human judgment belongs.

**Human-in-the-loop as engagement, not just QA.** Verification doubles as
participation:
- *Learners* verify by doing — the §8 lab self-check is exactly a learner
  confirming a claim; "find the error" becomes an exercise, and checking the
  machine is active learning.
- *Researchers* verify by reviewing — a flagged correction is a contribution that
  feeds back into the corpus.

**The promotion pipeline.** Content climbs the tiers as warrant accrues:

```
machine_generated --(symbolic verify)--> machine_verified
                  --(human review)------> human_verified
                  --(cross-check vs reference)--> canonical
```

So the verified cache (§9) is not static: today's disclaimered material, once
human-verified, becomes tomorrow's canonical reference. The system improves with
use, and the disclaimer surface contracts as the corpus matures. Make the
provenance badge visible per section — transparency about *what was checked* is
how a learner calibrates trust, and a "verified in SymPy" badge is itself
reassurance that the math was actually run.

---

## 12. What is new vs. what you already have

Already in spl3: `GENERATE`, `CALL`, `EVALUATE`, `RETRY`, typed `INTO`, the
self-refine repair loop, `CALL PARALLEL`, `run_python` (the executor behind
`verify_math` and the lab cells).

Genuinely new:

- the `SOLVE` / `ASSERT` constructs (deterministic branch points);
- the `primitive` / `concept` / `application` graph declarations, including the
  second, outward-pointing application edge type;
- the `lab` / `play` schema fields, and the insight that the verifier is
  **dual-use** — the same engine that checks the author also gives the student
  exact feedback;
- the reach metric and `ancestors` / `restrict` graph ops (pure graph work —
  topological sort biased by payoff-weighted out-degree);
- two thin verifier tools — `verify_math` (SymPy) and `shape_check` (NumPy
  shapes). The shape checker is the same construct you'd use for `pint` in the
  mechanics version; only the algebra of "what composes with what" changes;
- executable-cell output via Pyodide / JupyterLite, and an *inductive* game tier
  (PySR / gplearn) alongside the deductive solvers;
- the on-demand entry point — `text2spl` resolves a natural-language question to a
  `@target`, scoped against a per-learner mastery set, with a verified content
  cache so the textbook assembles lazily from demand;
- a validation layer — diffing generated structure against an authoritative
  open-licensed reference, which becomes the quality gate once there is no human
  author in the loop;
- a `provenance` field and trust tiers (canonical / machine-verified /
  machine-generated) with calibrated disclaimers, plus a promotion pipeline that
  lets human-verified content climb toward canonical over time.

---

## First build target

Stage it in two passes, one per radical, each culminating in a payoff:

1. **First radical only** (`primitive_budget = 1`, ⊕/⊙), `target = diagonalization`.
   Eigenpairs and diagonalization are reachable without the inner product, so the
   reducibility check is maximally strict — exactly one radical means any concept
   claiming to be primitive is provably wrong. Close on normal modes / stability
   as the payoff.

2. **Add the second radical** ⟨·,·⟩, `target = spectral_theorem`. Orthogonality,
   Gram–Schmidt, and the spectral theorem come online; close on the quantum
   observable / PCA payoff.

The smallest first deliverable is the `productivity_order` solver alone: a
topological sort biased by payoff-weighted out-degree. Implement and test it
against this exact graph before wiring up the generation side.
