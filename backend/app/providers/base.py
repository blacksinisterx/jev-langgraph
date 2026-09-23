from abc import ABC, abstractmethod

from ..schemas import Answer, Question


class Provider(ABC):
    """Anything that can answer typed questions about a state. Swapping the
    implementation (mock / typesafe / jev_agent) never changes a call site."""

    name: str

    @abstractmethod
    def evaluate(self, state: str | dict, questions: dict[str, Question]) -> dict[str, Answer]:
        ...

    def cost_estimate_usd(self, input_tokens: int) -> float:
        return 0.0
