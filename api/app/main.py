import time

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import config
from .fixtures import DEMO_QUERIES
from .graph import NODE_NAMES, STATIC_EDGES, build_graph
from .providers import get_provider
from .schemas import RunRequest, RunResult, TraceStep
from .state import initial_state

app = FastAPI(title="JevLangGraph", description="A LangGraph agent where Jev, not an LLM, controls every branch point.")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

_runs: list[RunResult] = []
_MAX_LOG = 30


@app.post("/run", response_model=RunResult)
def run(req: RunRequest) -> RunResult:
    provider = get_provider(config.JEV_PROVIDER)
    graph = build_graph(provider)

    start = time.perf_counter()
    final_state = graph.invoke(initial_state(req.query))
    total_latency_ms = (time.perf_counter() - start) * 1000

    result = RunResult(
        query=req.query,
        steps=[TraceStep(**s) for s in final_state["steps"]],
        final_answer=final_state["final_answer"],
        escalation_reason=final_state["escalation_reason"],
        provider=config.JEV_PROVIDER,
        total_latency_ms=round(total_latency_ms, 3),
    )
    _runs.insert(0, result)
    del _runs[_MAX_LOG:]
    return result


@app.get("/runs", response_model=list[RunResult])
def runs() -> list[RunResult]:
    return _runs


@app.get("/examples")
def examples() -> list[dict]:
    return DEMO_QUERIES


@app.get("/graph-schema")
def graph_schema() -> dict:
    return {"nodes": NODE_NAMES, "edges": [{"from": a, "to": b} for a, b in STATIC_EDGES]}


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "provider": config.JEV_PROVIDER}
