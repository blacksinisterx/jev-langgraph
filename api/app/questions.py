from .schemas import ChoiceQuestion, Question

QUESTIONS: dict[str, Question] = {
    "next_action": ChoiceQuestion(
        instructions="Given the agent's progress so far on this query, decide what to do next.",
        criteria={
            "continue": "Think one more step before taking any external action",
            "search": "Look up external information the agent doesn't have yet",
            "use_tool": "Perform a computation or structured operation (e.g. arithmetic)",
            "retry": "The last action failed and should be attempted again",
            "finish": "Enough information has been gathered to answer the query",
            "escalate": "This is stuck, ambiguous, or outside what the agent can resolve -- a human should take over",
        },
    ),
}
