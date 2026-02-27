# Show HN: MoMa Hub — distributed AI inference network as a solution to the 2028 Intelligence Crisis

*HackerNews draft v1.2 — publish after momahub 2-node demo is working*
*Cites: Medium blog (01-moma-medium.md) | Responds to: Citrini Research "2028 Global Intelligence Crisis"*

---

## Submission Title (choose one before posting)

**Option A** (crisis-response framing):
> Show HN: We built the open distributed inference layer that prevents AI from becoming a single point of failure

**Option B** (demo-led, cites Citrini):
> Show HN: MoMa Hub — SETI@home for AI inference, Apache 2.0, a working answer to AI centralization risk

**Option C** (contrarian, direct):
> Show HN: spl-llm + momahub — declarative LLM orchestration across community GPUs (not a manifesto, working code)

---

## Body Text

A few days ago Citrini Research published
[*THE 2028 GLOBAL INTELLIGENCE CRISIS*](https://www.citriniresearch.com/p/2028gic).
It is speculative macro analysis, not a prediction — but the feedback loop
they identify is worth taking seriously:

> *AI capability improves → payroll shrinks → spending softens → margins
> tighten → companies buy more AI → capability improves.*

Machines don't consume discretionary goods. The cycle has no natural
stabilizer. Their proposed solutions — an AI compute tax, a sovereign
wealth fund redistributing AI returns — face political gridlock.

We have been building the market-mechanism alternative.

---

**MoMa Hub is a distributed AI inference network modelled on SETI@home.**

Consumer GPUs and phone NPUs register as contributing nodes. SPL CTEs
(Common Table Expressions — independently executable work units) are
dispatched across them. The same `.spl` script runs locally, on cloud
APIs, or across the community network without modification. Contributing
nodes earn MoMa Points for every CTE they process. Points are redeemable
for inference time on the network.

That is not a roadmap item. `contribution_tokens` tracking is already in
`momahub v0.2.0`. MoMa Points is its user-facing formalization.

---

**This is not a thought experiment. Here is what exists today:**

```bash
pip install spl-llm    # SPL engine, 58/58 tests, Apache 2.0
pip install momahub    # v0.2.0 — node registry, circuit breaker, SQLite-persistent
pip install spl-flow   # Text2SPL + PocketFlow orchestration + Streamlit UI
```

The SPL engine runs parallel CTE dispatch — three specialist models
(Qwen, Mistral, Llama) executing simultaneously via `asyncio.gather`,
synthesized by Claude into a single composed output. Tested on Ollama
(local/free), OpenRouter (cloud), and Claude CLI.

```sql
-- Route each sub-task to its specialist. Budgets declared, not guessed.
PROMPT radical_family USING MODEL "claude-sonnet"

WITH chars    AS (PROMPT extract_chars  USING MODEL "qwen2.5")   -- CJK specialist
WITH german   AS (PROMPT translate_de   USING MODEL "mistral")   -- EU language
WITH insights AS (PROMPT cultural_note  USING MODEL "llama3.1")  -- cultural reasoning

SELECT compose_table(chars, german, insights)
WITH OUTPUT FORMAT markdown;
```

The provider is a runtime detail. The `.spl` script never changes.

The full specification is on arXiv: [2602.21257](https://arxiv.org/abs/2602.21257).
A longer write-up of the architecture and the SETI@home parallel is on
Medium: [*The Moment of AI: From SETI@home to MoMa Hub*](#).

---

**Why this addresses the Citrini scenario — mechanically, not rhetorically:**

Citrini's crisis is a distribution problem: AI productivity accrues to a
small number of labs and their largest customers, while the workers
displaced by AI have no stake in the infrastructure that displaced them.
Their policy proposals try to redirect that value after the fact through
taxation and sovereign funds.

MoMa Hub redirects value at the point of production.

A contributing node owner — running a GTX 1080 Ti overnight, or leaving
a phone plugged in — processes real inference work and earns real MoMa
Points. When enterprises route overflow capacity through the network, the
compute revenue flows to the contributing nodes directly. No government
intermediary. No regulatory timeline. The redistribution is in the
architecture.

The Citrini feedback loop breaks when people who own inference hardware
have a stake in running it. We are 50–100 million consumer GPUs away from
meaningful scale. The hardware already exists, already purchased, already
drawing power. The coordination layer was missing.

---

**Why Apache 2.0, not a platform play:**

The honest moat here is not lock-in. It is the SQL abstraction applied to
LLM orchestration — a new level in the stack that makes the level below
(which backend runs the inference) a commodity. SQL did not extract rent
from databases. It made databases accessible to everyone, which made the
entire ecosystem larger.

SPL must do the same. Apache 2.0 is a structural commitment, not a
marketing choice.

---

**What SETI@home proved:**

In 1999, SETI@home demonstrated that idle consumer compute — coordinated
by an open protocol — could rival supercomputer-class infrastructure at
near-zero marginal cost. The project processed more floating-point
operations than any supercomputer then in existence.

SETI@home was a voluntary coordination network for a single scientific
problem. MoMa Hub is a market-coordination network for general AI
inference. The coordination problem is harder. The stakes are larger. The
hardware pool — including ~6 billion smartphones with dedicated NPUs — is
orders of magnitude bigger.

One of us was a physics post-doc at Lawrence Berkeley National Laboratory
when SETI@home launched. We recognised the pattern. We are building the
next iteration.

---

**What's missing (honest status):**

- Multi-node demo: requires the 2nd GPU (in transit). Will post "Show HN"
  once a 2-node dispatch is reproducible in under 10 minutes on consumer
  hardware.
- MoMa Points valuation: the Points-to-Cycles exchange rate is not
  finalised. The tracking infrastructure exists; the market mechanism
  needs calibration.
- Mobile node tier: architectural decisions are being kept hardware-agnostic
  from the start; mobile is a v0.5+ milestone.
- Anti-gaming: Sybil node detection for Points farming is an open research
  question. Reliability weighting (uptime-weighted Point rates) is the
  current partial answer.

---

**Links:**
- arXiv (SPL spec): https://arxiv.org/abs/2602.21257
- SPL engine: https://github.com/digital-duck/SPL
- MoMa Hub: https://github.com/digital-duck/momahub
- SPL-Flow: https://github.com/digital-duck/SPL-Flow
- PyPI: `pip install spl-llm` / `pip install momahub` / `pip install spl-flow`

---

> *We are not building an alternative to frontier AI labs —
> we are building the resilience layer that makes AI infrastructure
> as robust as nature, and as open as the Internet.*

---

## HN Submission Checklist

**Version history:**
- `02-moma-hackernews-v1.0.md` — original "Show HN: I built a tool" framing,
  written before the Citrini Research report was read. Clean technical launch
  post; still valid if the crisis framing feels too heavy for the moment.
- `02-moma-hackernews-v1.2.md` — this file. Reframed around the Citrini
  "2028 Global Intelligence Crisis" scenario. MoMa Hub as working
  infrastructure, not thought experiment. Written after the Citrini piece
  gave the project its larger context and motivation.

- [ ] momahub 2-node demo working and reproducible in <10 min
- [ ] Medium blog published (cite with live URL in body)
- [ ] Citrini Research blog URL confirmed live (use in opening paragraph)
- [ ] Clean `spl execute examples/parallel_cte.spl` terminal recording
- [ ] momahub "register your node in 5 minutes" quick-start in README
- [ ] Benchmark table: MoMa Hub community node vs. frontier API cost/1K tokens
- [ ] MoMa Points economy explained in momahub README (not just in the HN post)
- [ ] Review HN guidelines: no marketing language, answer every comment promptly
- [ ] Post on weekday, 8–10am US Eastern
- [ ] GitHub READMEs polished before posting

---

## Post-submission Response Notes

*"How is this different from LangChain / LlamaIndex?"*
> Those are imperative Python libraries — you write loops and callbacks.
> SPL is declarative — you describe what you want, the engine decides execution.
> Same difference as a stored procedure vs. writing SQL. The 8 million SQL
> developers worldwide can read an `.spl` file immediately.

*"Why SQL syntax? LLMs understand natural language."*
> Natural language is ambiguous. SQL is precise, composable, and learnable
> in one afternoon by anyone with a data background. NL→SPL translation
> (Text2SPL) is a planned feature; SPL is the target representation, not
> the input constraint.

*"MoMa Points sounds like crypto."*
> No blockchain, no token speculation. MoMa Points is an internal accounting
> unit — closer to frequent flier miles or AWS Credits than to a tradeable
> token. Contributing nodes earn Points for compute contributed; Points
> are redeemed for inference time. Real money enters when enterprises buy
> bulk capacity; it distributes as Points to contributing nodes. The
> infrastructure is SQLite, not a chain.

*"What prevents contributing nodes from being slow or unreliable?"*
> Circuit breaker per node (already in momahub v0.2.0), hedged requests
> (duplicate dispatch, take first result), SWIM gossip for health (v0.3.0).
> Reliability weighting: nodes with higher uptime earn more per CTE.

*"This is just Ollama with extra steps."*
> Ollama is one supported backend. SPL also runs on OpenRouter, Claude,
> and will support llama.cpp, llamafile, and vLLM. The point isn't the
> runtime — it's the declarative abstraction above it, and the coordination
> layer that dispatches across community hardware. The same way SQL's value
> wasn't tied to Oracle.

*"How is this not a repeat of the Citrini intermediary problem — MoMa Hub
as a new centralized coordinator?"*
> Fair. The answer is in the architecture: Apache 2.0 means anyone can run
> a Hub instance. Multiple Hub instances operate in a spoke-and-hub
> topology — regional hubs with cross-hub SPL routing — so no single
> instance is a single point of failure. This is how the Internet works:
> BGP routing between autonomous systems, regional Internet Exchange Points
> as hubs, ISPs as spokes. ARPANET was designed to survive nuclear attack
> by eliminating central routing nodes. MoMa Hub applies the same principle.
