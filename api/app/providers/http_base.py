import os
import time

import httpx

from ..schemas import Answer, JevRequest, JevResponse, Question
from .base import Provider


class HttpJevProvider(Provider):
    """Shared request/response handling for any host that speaks the real Jev
    HTTP schema (POST {base_url}, Bearer auth, JevRequest in / JevResponse out).
    Only the base URL, env var for the key, and per-token price differ."""

    base_url: str
    api_key_env: str
    input_price_per_million: float = 0.0
    timeout_s: float = 8.0

    def evaluate(self, state: str | dict, questions: dict[str, Question]) -> dict[str, Answer]:
        api_key = os.environ.get(self.api_key_env)
        if not api_key:
            raise RuntimeError(f"{self.api_key_env} is not set but JEV_PROVIDER='{self.name}' was requested")

        payload = JevRequest(state=state, questions=questions).model_dump(mode="json")
        start = time.perf_counter()
        resp = httpx.post(
            self.base_url,
            json=payload,
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            timeout=self.timeout_s,
        )
        resp.raise_for_status()
        self._last_latency_ms = (time.perf_counter() - start) * 1000
        parsed = JevResponse.model_validate(resp.json())
        self._last_usage = parsed.usage
        return parsed.answers

    def cost_estimate_usd(self, input_tokens: int) -> float:
        return round(input_tokens / 1_000_000 * self.input_price_per_million, 8)
