# Neurosymbolic SPL — landscape, design, and implementation

Combining rule-based symbolic AI with generative AI, grounded in the SPL stack.
The goal is to break a workflow into steps that call an LLM for its probabilistic
nature and call deterministic libraries for their exact nature, constraining LLM
usage to where it earns its place.

---

## 0. Two senses of "symbolic"

The word hides two very different ambitions, and the grand vision straddles both.

- **Weak sense — symbolic as deterministic control.** Imperative code, tool
  calls, typed state, branching. This is the MRKL / tool-router lineage.
  **SPL lives here today:** `GENERATE` is the probabilistic primitive; `CALL`,
  `@spl_tool`, the stdlib, and typed `INTO` are the deterministic envelope;
  `EVALUATE` is semantic branching.

- **Strong sense — symbolic as formal reasoning.** Logic solvers, knowledge
  graphs, constraint satisfaction, planners, theorem provers — engines with
  their own inference semantics that the LLM *feeds* and is *checked by*. This is
  VERUS-LM, LINC (LLM + first-order-logic prover), knowledge-graph + Prolog
  stacks, and the planning results where a neuro-symbolic model generalises while
  an end-to-end neural model collapses as the problem scales.

The grand vision is the move from weak to strong. Everything below is organised
around that transition. A useful mental anchor is the dual-process framing: the
neural component as **System 1** (fast, intuitive — recognition, translation,
drafting) and the symbolic component as **System 2** (slow, exact — proofs,
constraints, planning).

---

## 1. The current landscape

Three families. SPL touches all three but anchors in the middle one.

### 1a. Declarative LLM-programming frameworks (SPL's siblings)

- **DSPy** is the closest relative by philosophy — also pitched as "a higher-level
  language for AI, like SQL for data." The crucial difference: DSPy *compiles*
  signatures and modules into optimised prompts (and can tune weights) against
  your evaluation data. SPL is declarative **orchestration**; DSPy is declarative
  **optimisation**. They are orthogonal — which matters for implementation (§3).
- **LangGraph** is the standard for stateful, persistent orchestration; SPL
  already transpiles to it.
- **LangChain / LlamaIndex** for general orchestration and retrieval;
  **CrewAI / AutoGen** for multi-agent coordination; **TextGrad** for
  gradient-style prompt optimisation.

### 1b. Constrained decoding (the literal "constrain the LLM" mechanism)

This is the piece SPL does not yet expose and the most direct answer to
"constrain LLM usage." These libraries enforce a grammar at the **token** level,
masking any token that cannot lead to a valid output — guaranteeing syntactic
validity rather than hoping for it.

- **Outlines**, **XGrammar**, **llguidance** (guidance's fast CFG engine), and
  **LMQL**. `llama.cpp`/Ollama support **GBNF** grammars natively.
- Caveat: naive constraint can hurt task accuracy if vocabularies are misaligned,
  and over-constraining can push the model toward locally-valid-but-wrong
  trajectories. The current best practice decouples planning from enforcement:
  draft relatively freely, then constrain/repair.

### 1c. Strong-symbolic reasoning

- **VERUS-LM** — separates domain knowledge from queries, supports optimisation
  and constraint satisfaction, and markedly outperforms raw LLMs on logical
  reasoning.
- **LINC** — the LLM translates natural language into first-order logic and an
  external prover does the inference.
- **Knowledge-graph platforms** (e.g. AllegroGraph) integrating a graph store, a
  vector store, and an LLM — "neuro-symbolic" in one package.
- Enterprise pattern: LLM agents + logic-based program synthesis +
  KG-grounded semantics, giving workflows with enforceable pre/post-conditions
  and deterministic, human-auditable execution.

---

## 2. How to design such a solution — the four-layer model

Determinism/constraint can be injected at four distinct layers; a mature hybrid
uses all four rather than treating "symbolic" as one thing. The unifying pattern
across every successful system is **generate-then-verify**: the LLM proposes, a
deterministic engine disposes.

```
                GENERATE  (the one probabilistic step)
                    │
   ┌────────────────┼─────────────────────────────────────────┐
   │  L1  Token layer      constrained decoding · GBNF/XGrammar │  ← gap in SPL today
   │  L2  Call layer       CALL · @spl_tool · typed INTO        │  ← SPL has this
   │  L3  Workflow layer   EVALUATE · RETRY · CALL PARALLEL     │  ← SPL's core strength
   │  L4  Knowledge layer  SOLVE · ASSERT · KG / solver query   │  ← the frontier
   └────────────────┬─────────────────────────────────────────┘
                    │   verify; on failure, repair and loop back to GENERATE
                  COMMIT
```

Three design principles follow.

1. **A symbolic verifier should be a first-class construct, not a generic `CALL`.**
   A Z3 check or a Datalog query is unlike `http_get`: it returns SAT/UNSAT, a
   model, or a proof, and that result should *drive control flow* the way
   `EVALUATE` does for semantics. A dedicated `SOLVE … INTO @model` /
   `ASSERT … OTHERWISE …` family — the symbolic analog of `EVALUATE` — is the
   single change that moves SPL from weak to strong.

2. **Generate-then-verify is the spine, and your `self_refine` recipe is already
   90% of it** — it just uses an LLM critic. Swap the critic for a deterministic
   verifier wherever the domain admits one: a type checker for codegen, `EXPLAIN`
   for SQL, unit tests for functions, a solver for constraint problems, a CAS for
   math, a KG consistency check for extracted facts.

3. **Constrained generation must be adapter-tiered.** True token masking needs
   logit access — available only on open/local backends (Ollama, vLLM). Frontier
   API adapters (Anthropic, OpenAI, Google) expose only coarser JSON-schema
   structured output. So a `GENERATE … CONFORMING TO <grammar>` modifier should
   compile to real grammar masking on the local tier and degrade to
   schema-prompt + validate + `RETRY` on the API tier. Honest tiering beats
   pretending the guarantee is uniform.

**Knowledge: split symbolic memory from associative memory.** The vector store is
associative recall; add a triple/graph or Datalog store so facts and rules are
*queryable symbolically* and consistency is *checkable*, not merely retrieved by
similarity.

---

## 3. Implementation recommendations

In rough priority order:

1. **Start with a CAS + an SMT solver** as the first deterministic backends —
   SymPy and Z3. Both are pip-installable, pure-Python to drive, and cover the
   majority of "recompute/verify" and "find/check under constraints" needs. (See
   §4 for how to learn them.)
2. **Add a logic/rule layer** — ASP via `clingo`, or Datalog via `pyDatalog` /
   Soufflé — for graph rules like reducibility and ordering, and for KG queries.
3. **Add a knowledge store** — `rdflib` + `oxigraph` (embedded SPARQL) for a
   light start, or Neo4j / AllegroGraph for an integrated reasoner.
4. **Borrow DSPy as an optimiser backend rather than competing with it.** Your
   cookbook is already an eval harness. A `spl3 optimize <file.spl>` that lifts
   each `GENERATE` prompt into a DSPy module, tunes it against the recipe's
   metric, and writes the optimised prompt back would make SPL self-improving in
   DSPy's sense while keeping your declarative surface — something pure
   orchestration frameworks (LangGraph included) do not offer at the language
   level.
5. **For constrained decoding**, lead with GBNF on the Ollama tier (zero extra
   deps), and use XGrammar / Outlines / llguidance for the broader open-model
   tier. Validate on your evals that constraint does not degrade quality.

**Honest limit.** The empirical neurosymbolic wins are concentrated in domains
with crisp formal structure — logic, planning, constraints, code, math. Manual
symbolic-interface design is still a bottleneck, and symbolic engines hit
combinatorial limits on large problems. So make the symbolic layer **optional and
per-workflow**: `SOLVE`/`ASSERT` available when the domain is formalisable, plain
`GENERATE`/`CALL` when it is not.

---

## 4. Learning CAS and the solver families

This is the deterministic backbone. Below is a map of the families, what each is
for, the Python entry point, and what to learn first — then a recommended order
and exercises grounded in the SPL textbook use case.

### 4a. The map

| Family | Solves / returns | Python entry | Learn first |
| --- | --- | --- | --- |
| **CAS** (computer algebra) | exact symbolic math: differentiate, integrate, simplify, solve, symbolic linear algebra | **SymPy** (also SageMath, Maxima; Mathematica/Maple commercial) | symbols, `diff`, `integrate`, `solve`, `Eq`, `Matrix.eigenvals()`, exact vs float |
| **SMT** (satisfiability modulo theories) | SAT + a model, or UNSAT (+ unsat core), over ints/reals/bitvecs/arrays | **Z3** (`z3-solver`); CVC5; PySMT frontend | `Int/Real/Bool` vars, add constraints, `Solver().check()`, `model()`, the SAT/UNSAT/model trichotomy |
| **SAT** (Boolean satisfiability) | satisfiability of CNF — the substrate under SMT/CP | python-sat (`pysat`) | conceptual only; use SMT/CP in practice |
| **CP / CP-SAT** (constraint programming) | discrete combinatorial search + optimisation (scheduling, assignment, puzzles) | **OR-Tools CP-SAT**; python-constraint | variables over finite domains, `AddAllDifferent`, objective, `Solve()` |
| **LP / MILP** (linear / mixed-integer programming) | optimise a linear objective under linear constraints | PuLP, Pyomo, OR-Tools, `scipy.optimize.linprog`; solvers CBC/HiGHS/GLPK/Gurobi | decision vars, objective, constraints, the LP relaxation idea |
| **ASP** (answer set programming) | answer sets (stable models); great for rules + defaults / nonmonotonic reasoning | **clingo** (Potassco) Python API | facts, rules `head :- body.`, choice rules, `#minimize` |
| **Logic programming / Prolog** | relational reasoning via Horn clauses, unification, backtracking | SWI-Prolog via `pyswip`; `kanren`; `pyDatalog` | facts, rules, queries, unification, backtracking |
| **Datalog** | deductive queries over a knowledge base; guaranteed to terminate | `pyDatalog`; Soufflé (compiled, fast) | facts, recursive rules, reachability queries |
| **Theorem provers** | machine-checked proofs (interactive) or automated refutation | Lean 4, Coq, Isabelle; Vampire/E (automated) | the proof-state model; Lean's `mathlib` for math |
| **Planners** (PDDL) | a sequence of actions reaching a goal state | unified-planning, pyperplan, Fast Downward | states, actions with pre/post-conditions, goals |
| **KG / semantic reasoner** | query + infer over RDF/OWL or property graphs | `rdflib`, `oxigraph`, `owlready2`; Neo4j | triples, SPARQL, RDFS/OWL entailment |

The dividing question is always *what does it return, and does that result drive a
branch?* CAS returns a value to compare against (verify); SMT/CP/LP return
SAT+model or UNSAT (decide + extract); ASP/Datalog/Prolog return derived facts or
answer sets (query the knowledge base); planners return a plan; provers return a
checked proof.

### 4b. A learning order for the SPL goal

1. **SymPy (CAS) — start here.** Immediately useful as `verify_math`, gentle,
   pure Python, directly serves the textbook. It teaches the exact-vs-numeric
   distinction that underlies all symbolic work.
2. **Z3 (SMT) — next.** The universal "find or check values under constraints"
   tool, and the cleanest way to internalise the SAT / UNSAT / model mental model
   that everything else inherits. This is the natural engine behind `SOLVE` /
   `ASSERT`.
3. **Datalog (`pyDatalog`) or ASP (`clingo`) — the graph/rule layer.** Concept
   reducibility is *literally* a reachability query; ordering and KG consistency
   are rule queries. Datalog is the gentlest entry; clingo adds optimisation and
   defaults.
4. **Then breadth as needed:** OR-Tools CP-SAT for combinatorial ordering/
   scheduling, a PDDL planner for the curriculum-as-planning and generalisation
   story, and — if you want proof-grade math verification — Lean 4 with `mathlib`
   (a larger lift, and an active LLM-autoformalisation research direction).

### 4c. Exercises grounded in the textbook recipe

Each maps a solver family onto a concrete SPL verifier role.

- **CAS / SymPy → `verify_math`.** Given a matrix `A` and a claimed eigenpair
  `(λ, v)`, check `A*v == λ*v`; independently recompute `A.eigenvals()` and
  compare. Extend to RREF, rank, determinant, and "is this set a basis?"
  (independent ⇔ rank == count).
- **CAS / SymPy → `shape_check`.** Verify matrix/vector shape compatibility
  (`(m×n)·(n×p) → m×p`; `⊕` needs equal dimension) and raise on mismatch. This is
  the dimensional-analysis analog (the same construct as `pint` for mechanics).
- **SMT / Z3 → an LA concept as constraints.** Encode "are these vectors linearly
  independent?" as: does there exist a *nonzero* coefficient vector with
  `Σ αᵢ vᵢ = 0`? UNSAT ⇒ independent. A neat way to feel how a definition becomes
  a satisfiability query.
- **Datalog / clingo → reducibility.** Encode `composed_of` as facts and the
  reachability rule:
  ```
  reaches(X, P) :- composed_of(X, P).
  reaches(X, P) :- composed_of(X, Y), reaches(Y, P).
  ```
  Then assert that every concept reaches *only* declared primitives.
- **CP-SAT / OR-Tools → `productivity_order`.** Topological order respecting
  `composed_of`, maximising early placement of high-reach nodes — a constrained
  optimisation rather than a plain sort.
- **Planner / PDDL → curriculum as planning.** Actions = "teach concept X",
  preconditions = "prerequisites taught", goal = "target taught". The plan *is*
  the teaching order, and the planner generalises to new target sets.

### 4d. Resources and links

Grouped by family — tool docs first, then learning texts.

**CAS**
- SymPy docs + tutorial: https://docs.sympy.org/latest/tutorials/intro-tutorial/index.html
- SageMath: https://www.sagemath.org/ · Maxima: https://maxima.sourceforge.io/
- *Doing Math with Python* (Saha): https://nostarch.com/doingmathwithpython

**SMT**
- Z3 repo: https://github.com/Z3Prover/z3
- Interactive Z3 Guide (runs in the browser, Python + SMT-LIB): https://microsoft.github.io/z3guide/
- CVC5: https://cvc5.github.io/ · PySMT (multi-backend frontend): https://github.com/pysmt/pysmt
- Theory: *The Calculus of Computation* (Bradley & Manna)

**SAT**
- PySAT: https://pysathq.github.io/

**CP / CP-SAT**
- Google OR-Tools, CP-SAT primer: https://developers.google.com/optimization/cp
- python-constraint: https://github.com/python-constraint/python-constraint

**LP / MILP**
- PuLP: https://coin-or.github.io/pulp/ · Pyomo: https://www.pyomo.org/ · HiGHS: https://highs.dev/
- SciPy `linprog`: https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.linprog.html

**ASP**
- clingo / Potassco: https://potassco.org/clingo/
- *Answer Set Solving in Practice* (Gebser et al.), via Potassco: https://potassco.org/book/

**Prolog**
- SWI-Prolog: https://www.swi-prolog.org/ · pyswip (Python bridge): https://github.com/yuce/pyswip
- *Learn Prolog Now!* (free, with runnable SWISH): https://www.learnprolognow.org/
- *The Art of Prolog* (Sterling & Shapiro), MIT Press

**Datalog**
- pyDatalog: https://github.com/pcarbonn/pyDatalog · Soufflé (compiled, fast): https://souffle-lang.github.io/
- *Foundations of Databases* — the "Alice book", free PDF from the authors: http://webdam.inria.fr/Alice/

**Theorem provers**
- Lean: https://lean-lang.org/ · *Theorem Proving in Lean 4* (free): https://leanprover.github.io/theorem_proving_in_lean4/ · *Mathematics in Lean* (free): https://leanprover-community.github.io/mathematics_in_lean/
- Isabelle: https://isabelle.in.tum.de/ · Coq/Rocq: https://rocq-prover.org/

**Planners (PDDL)**
- unified-planning (docs: https://unified-planning.readthedocs.io/): https://github.com/aiplan4eu/unified-planning
- pyperplan: https://github.com/aibasel/pyperplan · Fast Downward: https://www.fast-downward.org/
- *Automated Planning and Acting* (Ghallab, Nau, Traverso), Cambridge 2016

**Knowledge graphs / semantic reasoners**
- rdflib: https://rdflib.readthedocs.io/ · oxigraph (embedded SPARQL): https://github.com/oxigraph/oxigraph
- owlready2 (OWL reasoning): https://owlready2.readthedocs.io/ · Neo4j: https://neo4j.com/

**Neurosymbolic context**
- LINC (LLM + first-order-logic prover) and VERUS-LM — search arXiv: https://arxiv.org/ — plus recent neurosymbolic surveys, for how these engines wire to LLMs in practice.

### 4e. Symbolic analysis beyond SymPy

SymPy is the general-purpose CAS; these specialise. Grouped by the job they do best:

**Faster / larger general CAS**
- SymEngine — fast C++ core with SymPy-compatible Python bindings; can back SymPy for speed: https://github.com/symengine/symengine.py
- SageMath — comprehensive umbrella wrapping Maxima, GAP, FLINT, Singular, PARI (and includes SymPy): https://www.sagemath.org/

**Symbolic bridged to numerics (autodiff + optimisation)**
- CasADi — symbolic framework for automatic differentiation and optimal control / nonlinear optimisation: https://web.casadi.org/
- PyTensor — symbolic tensor graphs with autodiff and compilation; the maintained Theano/Aesara successor, and the engine under PyMC: https://pytensor.readthedocs.io/

**Symbolic regression — induce the equation *from data* (the discover-the-law direction)**
- PySR — scikit-learn-compatible symbolic regression on a Julia backend; recovers governing equations from data, with an LLM-guided variant (LaSR): https://github.com/MilesCranmer/PySR (docs: https://astroautomata.com/PySR/)
- gplearn — lighter pure-Python genetic-programming SR in the scikit-learn idiom (and browser-friendly, unlike PySR's Julia backend): https://gplearn.readthedocs.io/

**Physics / tensor algebra**
- Cadabra2 — tensor field-theory CAS: https://cadabra.science/
- SageManifolds — differential geometry & tensor calculus on manifolds (inside Sage): https://sagemanifolds.obspm.fr/
- EinsteinPy — general relativity, symbolic + numeric: https://einsteinpy.org/
- galgebra — geometric (Clifford) algebra on top of SymPy: https://github.com/pygae/galgebra

For the SPL stack specifically: **SymEngine** for speed behind `verify_math`, and **PySR / gplearn** as a new *inductive* primitive (law discovery) to sit alongside the *deductive* `SOLVE` / `ASSERT`.

---

## 5. First steps

1. Implement `verify_math` and `shape_check` in SymPy — these alone upgrade your
   `self_refine` loop from an LLM critic to a deterministic one on math content.
2. Prototype `SOLVE` / `ASSERT` against Z3 — start with a single LA predicate
   (linear independence) so the SAT/UNSAT/model flow is concrete.
3. Encode the concept graph as Datalog facts and write the reducibility query —
   the smallest possible "strong-symbolic" win, and the foundation of the
   knowledge layer.

From there, the textbook recipe (separate file) becomes the first end-to-end
demonstration: the model proposes the basis and the compositions; the symbolic
layer guarantees the result is generative, reducible, and correct.
