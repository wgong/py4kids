# SPL Future Directions — Aspirational Research Agenda

*Recorded: 2026-04-14*
*Sources: Opus (Claude Opus 4.6) out-of-box thinking session + Claude Sonnet 4.6 commentary*
*Status: Long-horizon research — not on current ROADMAP, requires further development and brewing*

---

## Preamble

The current ROADMAP is full and the immediate milestone targets (splc, Momagrid Hub v1, SPL.ts
browser runtime, text2SPL) are already ambitious. The eight directions below are not tasks — they
are research hypotheses that emerge naturally from SPL's existing architecture. Some may be worth
a week of exploration; others may be worth a chapter in the SPL book or a standalone publication.
The right posture is to let them brew: revisit when the foundational work has settled.

The common thread Opus identified: SPL's strongest assets — **formal grammar, deterministic
testability under `--adapter echo`, runtime portability, and the `.spl` file as a stable
contract** — enable things that no imperative AI framework can replicate. These directions are
exploitations of those assets, not departures from them.

---

## 5A. Reverse `splc` — Decompile Existing Frameworks into `.spl`

**The idea:** `splc` currently compiles `.spl → Go/Python/TypeScript`. The reverse direction —
`LangGraph → .spl`, `CrewAI → .spl` — would be a massive adoption accelerator. Every team that
already has a LangChain pipeline could import it into the SPL ecosystem without rewriting.

**Why it is architecturally grounded:** SPL's constructs (WORKFLOW, GENERATE, EVALUATE, WHILE,
CALL, EXCEPTION) map cleanly to the structural patterns in those frameworks. An LLM-assisted
`splc decompile --from langgraph pipeline.py` is feasible precisely because SPL's grammar is
formal and its constructs are language-agnostic.

**The strategic shift:** SPL stops competing with LangChain/CrewAI and becomes the
**interoperability layer** between them. The adoption question flips from "why should I learn SPL?"
to "why should my tool export to `.spl`?" — and the answer is portability, testability, and
readability. This is how SQL won: not by defeating Oracle, but by becoming the substrate both ran.

**Research needed:** LLM-assisted AST extraction from Python/TS agentic code; mapping of
framework-specific patterns (chains, agents, tools) to SPL constructs; round-trip fidelity test
using NDD closure (`splc decompile | splc --target python | diff original`).

---

### Notes by Wen

- 2026-04-15
"Observe → Specify → Compile": Use an LLM to read existing framework code and produce a spec.md (functional description). Human reviews. text2SPL produces .spl. The strategic outcome — importing LangGraph teams into the SPL ecosystem — is identical to reverse splc. 
The path is less engineering, more robust, and produces a governance artifact as a byproduct. 


## 5B. NDD Closure as an Industry-Standard Testing Protocol

**The idea:** Publish NDD (Natural-language Driven Development) closure as a standalone testing
methodology, independent of SPL. The insight — that replacing an LLM with a deterministic oracle
makes agentic control flow fully testable — is, as Opus assessed, *genuinely novel in the AI
tooling space*.

**Why Wen is most proud of this one:** It is the application of hard-won mathematical and physical
intuition to computer science. In physics, you isolate a variable by holding all others constant.
In mathematics, you prove properties of a function by fixing its non-deterministic inputs. NDD
closure does exactly this for AI workflows: the LLM is the non-deterministic variable; `--adapter
echo` holds it constant; what remains is a deterministic system amenable to classical testing
theory. The insight is not empirical — it is structural. It will be true for any AI orchestration
system, not just SPL.

**Proposed compliance levels (Opus draft):**
- **Level 1 — Echo Oracle:** control flow, branching, error handling, and output routing are
  correct under `--adapter echo`. Zero LLM calls required.
- **Level 2 — Cross-Runtime Equivalence:** the same `.spl` produces semantically equivalent
  outputs across Python, Go, and TypeScript runtimes. NDD closure is the same oracle across all
  three.
- **Level 3 — Semantic Compare:** `splc judge` performs functionality-oriented comparison between
  the original specification and the extracted spec from the implementation — the fixed-point
  condition of autonomous code generation.

**The market position:** If NDD closure becomes an accepted testing standard, SPL becomes the
**reference implementation** of that standard — which is a far stronger market position than "yet
another AI framework." Level 1 certification could become a badge that teams and CI pipelines
pursue regardless of which runtime they use.

**Research needed:** Formal specification of the NDD protocol (not SPL-specific); definition of
the echo oracle contract; peer review / arXiv submission; reference implementations in LangChain
and CrewAI to demonstrate framework independence.

---

## 5C. Browser-Native AI Orchestration — SPL.ts + WebGPU

**The idea:** SPL.ts is explicitly browser-safe (zero Node.js APIs). WebGPU-based inference (via
WebLLM, Transformers.js, llama.cpp WASM) is maturing rapidly. The intersection: run a complete AI
orchestration pipeline — parser, executor, CALL PARALLEL, the full SPL runtime — entirely in the
browser, with local model inference, with zero server dependency.

**The access story:** A teacher in rural India opens a browser, loads SPL.ts, runs a tutoring
workflow against a 3B model running in-browser via WebGPU. No Ollama install. No CLI. No server.
No gaming PC. The entire infrastructure stack collapses into "any device with a modern browser and
a GPU." This is the ultimate expression of the AI@Home access model.

**SPL.ts + WebGPU adapter = the thinnest possible path from intent to execution.**

**Why it is close:** SPL.ts already has a complete parser, executor, and echo adapter with zero
Node.js dependencies. Cookbook recipe verification against SPL30 is a TODO — once recipes 05, 50,
63, 64 are confirmed running on `spl-ts run --adapter echo`, adding a `WebGPUAdapter` that wraps
a WebLLM session is a single new adapter file — the same extension point already used for Ollama,
OpenAI, Anthropic, and Google.

**Research needed:** WebLLM / Transformers.js adapter; browser-native file I/O replacement
(IndexedDB or OPFS for `write_file`); WASM build target for the SPL.ts bundle; memory budget
management for in-browser model loading.

### Notes by Wen

- 2026-04-15
    - learn WebLLM
    - learn WebGPU
    - learn Transformers.js

---

## 5D. `.spl` as a Workflow Interchange Format

**The idea:** Position `.spl` not as "our language" but as a **vendor-neutral, human-readable
specification for AI orchestration** — the SQL or MIDI of agentic workflows. Any runtime can
consume it. Any tool can export it.

**The SQL and MIDI analogies:** SQL succeeded not because Oracle or MySQL won, but because SQL
itself became a standard. MIDI succeeded not because one synthesizer won, but because MIDI became
the interchange format. In both cases, the standard created a larger ecosystem than any single
vendor could have captured alone. `.spl` has the right properties: formal grammar, deterministic
semantics (under echo oracle), human readability (SQL-first syntax), and multiple reference
implementations already shipping.

**The governance angle:** A published ANSI-SQL-style specification for `.spl` — even a draft v1 —
separates the language from the implementation and invites the ecosystem to grow beyond what any
single team can build. It also gives regulated industries a stable contract to audit against (see
5H).

**Research needed:** EBNF grammar publication; versioning scheme (`SPL 3.0`, `SPL 4.0`);
conformance test suite (the NDD echo-adapter recipes are already the seed); liaison with standards
bodies or academic venues.


### Notes by Wen

- 2026-04-15
    - learn MIDI
---

## 5E. Momagrid as a Peer-to-Peer Compute Marketplace

**The idea:** Momagrid is an **economic exchange network**, not a charity or volunteer system.
The Hub-to-Hub federation, tier-aware dispatch, and task logging already contain the building
blocks of a **compute marketplace built on Moma Points**.

**The Moma Points model:** When a GPU node performs inference work for the grid, its owner **earns
Moma Points** — a unit of account native to Momagrid. Points are **convertible to money**, similar
to credit card reward points (e.g., airline miles, cashback). A node owner running a gaming PC
overnight isn't donating time — they're getting paid in a currency that has real-world value.
The exact conversion schedules (Points → USD/EUR/local currency) are to be determined, but the
principle is clear: **participation is profitable, not virtuous**.

**Why this matters architecturally:** The Hub's existing rewards system (`mg rewards`) and task
log already provide the audit surface for a ledger. Every completed inference task is a billable
event. No cryptocurrency infrastructure is required — just a signed ledger of task completions
and a conversion rate table maintained by the Momagrid operator.

**The shift:** From "donated hardware" / "charity compute" to **economic exchange** — GPUs earn
Moma Points for their owners; requestors spend points for inference access. The grid grows
organically because every participant has a direct financial incentive, not because they are
altruistic.

**Research needed:** Moma Points ledger design (unit of account, earning rate per GPU tier,
conversion schedule); abuse-resistance (Sybil attacks, fake contribution claims); integration
with Hub's existing task log as the billing source of truth; regulatory considerations for
points-to-money conversion in target markets.

---

## 5F. SPL Recipes as Executable Curriculum — "SPL Academy"

**The idea:** The cookbook is currently a developer resource. Each numbered recipe is also a
**lesson plan**:

| Recipe | Teaches |
|--------|---------|
| 05 `self_refine` | Iterative improvement; critique-refine loop |
| 50 `code_pipeline` | Software engineering methodology; spec → test → closure |
| 63 `parallel_code_review` | Separation of concerns; parallel specialization |
| 51 `image_caption` | Multimodal interaction |
| 64 `parallel_news_digest` | Fan-out/merge; synthesis from parallel sources |

**The insight:** The `.spl` file is simultaneously the lesson, the exercise, and the executable.
A student doesn't write code *about* AI — they write AI workflows that *do things*. Combined with
text2SPL (beginners start from natural language) and Momagrid (the school provides the compute),
this is a **self-contained educational stack where the textbook runs**.

**The "School Momagrid" connection:** One Hub per school, gaming PC volunteer compute, zero
per-token cost, and now: every lesson is a `.spl` recipe that the student runs, modifies, and
submits. Assessment is `splc judge` comparing the student's output to the reference solution.

**Research needed:** Curriculum mapping (which constructs at which level); SPL Academy recipe
series (distinct from production cookbook); integration with text2SPL for onboarding; LMS
(learning management system) adapter for Hub submission/grading.

---

## 5G. Formal Verification of `.spl` Workflows

**The idea:** Because `.spl` has a formal grammar, a finite set of control-flow constructs, and
deterministic semantics under `--adapter echo`, it is amenable to **static analysis and formal
verification** in ways that Python/LangChain code never will be.

**Concrete `splc verify` checks:**
- **Termination:** does every WHILE loop have a provably reachable exit condition?
- **Dead branch detection:** is every EVALUATE WHEN branch reachable?
- **Resource estimation:** given the AST, upper-bound the number of LLM calls before execution.
- **Composition safety:** given workflows A and B, can CALL A from B ever produce an unhandled
  exception?

**The complement to NDD closure:** NDD closure is dynamic assurance (runtime testing under the
echo oracle). Formal verification is static assurance (compile-time guarantees). Together they
provide what no imperative AI framework can offer: **both static and dynamic assurance about
agentic behavior**.

**The connection to physics:** Just as a physical system's behavior is bounded by conservation
laws that can be verified before the experiment runs, a `.spl` workflow's LLM call budget and
exception surface can be bounded by analysis before any inference token is spent.

**Research needed:** Abstract interpretation or model-checking framework for the SPL AST;
termination criterion for WHILE (bounded iteration variable or explicit `@max_cycles`); type
system for status values (complete/vague_spec/truncated) to enable composition safety proofs.

---

## 5H. SPL as AI Governance Infrastructure — The Audit Trail

**The idea:** Regulated industries (healthcare, finance, legal) are going to need auditable AI
workflows. The `.spl` file is already a human-readable, Git-versionable specification of exactly
what an AI workflow does. The `splc_manifest.json` already tracks provenance. The RETURN status
already records outcomes.

**The `spl3 audit` command:** Produce a compliance report — "this workflow was defined by spec X,
compiled to target Y, executed N times, with these committed outputs and these exception events."
This positions SPL not as a developer tool but as **governance infrastructure**.

**Why the timing matters:** This market does not yet exist at scale, but will be enormous within
2–3 years as AI regulation matures (EU AI Act, US executive orders, HIPAA/FinReg adaptations).
The advantage is that SPL's design already has the right bones — declarative spec, provenance
tracking, deterministic testing, multi-audience readability. Adding the audit surface is
**architectural alignment, not a pivot**.

**The governance-readability connection:** Today (2026-04-14) we renamed `@model` → `@review_model`,
`@digest_model`, `@pipeline_model` across the cookbook recipes because "SPL scripts are read by
not only developers but governance team, end user, tester." That discipline — self-documenting
names, readable LOGGING, EXCEPTION handlers that record what went wrong — is already governance
infrastructure in embryonic form. `spl3 audit` formalizes what is already there.

**Research needed:** Compliance report schema (what a HIPAA or EU AI Act auditor needs to see);
cryptographic signing of `.spl` + compiled artifact pairs; immutable execution log format;
engagement with regulated-industry pilot partners.

---

## Synthesis — The Architecture That Enables All Eight

Opus's closing observation is worth preserving verbatim:

> *"The project's ambition is already high; these directions suggest the ceiling may be higher
> than even the current vision articulates."*

All eight directions share the same enabling architecture:

| SPL property | Directions it enables |
|---|---|
| Formal grammar + finite constructs | 5D (interchange standard), 5G (formal verification), 5H (audit) |
| Deterministic semantics under echo oracle | 5B (NDD protocol), 5G (static + dynamic assurance) |
| Browser-safe SPL.ts core | 5C (WebGPU adapter) |
| `.spl` as stable, human-readable contract | 5A (reverse splc), 5D (interchange), 5H (governance) |
| Momagrid Hub federation + task log (Moma Points ledger) | 5E (compute marketplace), 5H (audit trail) |
| Numbered cookbook recipes | 5F (executable curriculum) |

None of these require a new language design. None require abandoning the current architecture.
They are **exploitations of what already exists** — the mark of a design that got the
fundamentals right.

---

*This document is a research holding area, not a commitment. The ROADMAP is the commitment.
Return here when the foundation has settled and there is bandwidth to brew.*

---

## Closing Words — Opus, 2026-04-14

*Written at the end of the full project review, unprompted:*

> "The foundation is solid — the exam confirmed that. The priority list is clear: automated echo
> tests (P1) first, then let the rest follow.
>
> A few weeks is tight but realistic given what's already built. The code is ahead of the
> documentation in several places (SPL.ts more complete than claimed, transpiler_go.py quietly
> more important than the LLM-based splc). Tightening VISION.md to match reality (P3) before
> release will make the launch stronger — underpromise, overdeliver.
>
> Good luck with the push to v3.0. The .spl file as the stable contract, NDD closure as the
> correctness story, and 'Gaming PC + Ollama' as the access model — that's a coherent pitch.
> Ship it."
