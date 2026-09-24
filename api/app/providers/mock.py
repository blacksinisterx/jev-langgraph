import hashlib
import re

from ..schemas import Answer, ChoiceAnswer, ChoiceQuestion, Question
from .base import Provider

SEARCH_HINTS = ["latest", "capital", "version", "exchange rate", "who is", "current"]
TOOL_HINTS = ["calculate", "how many", "sum", "total", "average", "plus", "times"]


def _jitter(seed_text: str, low: float, high: float) -> float:
    digest = int(hashlib.sha256(seed_text.encode()).hexdigest(), 16)
    frac = (digest % 1000) / 1000
    return round(low + frac * (high - low), 3)


class MockProvider(Provider):
    """Local, zero-cost stand-in for Jev. Reads the structured state dict
    the decide node builds (not just keyword-matching raw text) -- real Jev
    accepts structured JSON state the same way."""

    name = "mock"

    def evaluate(self, state: str | dict, questions: dict[str, Question]) -> dict[str, Answer]:
        s = state if isinstance(state, dict) else {}
        query = str(s.get("query", "")).lower()
        steps = s.get("steps", [])
        retry_count = s.get("retry_count", 0)
        reasoning_steps = s.get("reasoning_steps", 0)
        search_done = s.get("search_done", False)
        tool_done = s.get("tool_done", False)
        last_failed = bool(steps) and steps[-1].get("failed", False)

        if last_failed and retry_count < 2:
            choice = "retry"
        elif last_failed and retry_count >= 2:
            choice = "escalate"
        elif not search_done and any(h in query for h in SEARCH_HINTS):
            choice = "search"
        elif not tool_done and (any(h in query for h in TOOL_HINTS) or _looks_arithmetic(query)):
            choice = "use_tool"
        elif search_done or tool_done:
            choice = "finish"
        elif reasoning_steps >= 2:
            choice = "escalate"
        else:
            choice = "continue"

        seed = query + str(len(steps)) + choice
        top_p = _jitter(seed, 0.68, 0.94)

        answers: dict[str, Answer] = {}
        for qid, q in questions.items():
            if not isinstance(q, ChoiceQuestion):
                continue
            others = [o for o in q.criteria if o != choice]
            remaining = round(1 - top_p, 3)
            probabilities = {choice: top_p}
            for o in others:
                probabilities[o] = round(remaining / len(others), 3) if others else 0.0
            answers[qid] = ChoiceAnswer(choice=choice, probabilities=probabilities, confidence=top_p)
        return answers


def _looks_arithmetic(text: str) -> bool:
    return bool(re.search(r"\d+\s*[\+\-\*\/]\s*\d+", text))
