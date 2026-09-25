# LinkedIn post draft — JevLangGraph

**Attach:** `calculation-scenario-live.png` — the one genuinely live shot (real Jev, not mocked: 97% then 100% confidence, real latency). `dashboard.png` (the retry scenario, mock) or `escalate-scenario.png` (mock, shows the self-loop clearly) work as richer fallbacks if you'd rather show more of the graph.

---

Fourth in this series, and the one closest to what "agent framework" usually means: a real [LangGraph](https://github.com/langchain-ai/langgraph) `StateGraph`, where every branch point is decided by Jev instead of an LLM call.

Most agent loops put a prompt at every fork: "should I search, use a tool, retry, or answer now?" That's a bounded choice over ~6 options — not open-ended reasoning — which is exactly the shape Jev is built for. So the graph's single `decide` node asks Jev a typed `Choice` question instead of prompting a model, and everything else is real work: a genuine safe arithmetic evaluator for the calculator tool (Python's `ast`, not `eval`), a small lookup table standing in for search. No LLM calls anywhere in the project — it runs at $0 like the rest of this series.

Five demo queries hit every one of Jev's 6 possible decisions:
→ pure calculation → straight to the tool
→ pure lookup → search only
→ both → search, then tool
→ a lookup that fails on its first attempt (deterministically, not randomly — the demo is reproducible) → real retry logic kicks in
→ a genuinely ambiguous, subjective query → Jev picks "continue" twice (thinking, no clear action available), then escalates to a human

The dashboard shows both a static diagram of the whole graph — with the path this specific run actually took highlighted in color, everything unused fading to gray — and a numbered trace of Jev's exact decision, confidence, and latency at each step. A loopy graph can't show visit order on its own, so both views matter together.

Bug I want to flag because it's a good example of what "test the graph" actually needs to cover: the retry node's log message originally read "retrying after failed 'decide'" — it grabbed the wrong array index and named the decide step itself, not the search call that actually failed. The final answer was still correct every time; only the human-readable explanation was wrong. Caught it by actually reading the trace in the browser, not just checking the graph reached the right end node. There's a regression test for it now.

Ran the calculation path against the real Jev API too (not the $0 mock default) to sanity-check it end to end: same two-step trace, 97% then 100% confidence, real network latency — screenshot attached.

Repo + write-up: [link]

#AI #LangGraph #AgentArchitecture #BuildInPublic

---

**Notes for posting:**
- Swap `[link]` once the repo is pushed.
- The bug paragraph is the most "credible engineer" part of this post — keep it if trimming for length, cut something else first.
