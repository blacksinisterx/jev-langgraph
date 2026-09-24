"""Simulated tools -- no external calls, no LLM. `calculate` is a genuine
safe arithmetic evaluator (not canned); `search` is a small keyword lookup
table standing in for a real retrieval system."""

import ast
import operator
import re

_OPS = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul,
        ast.Div: operator.truediv, ast.USub: operator.neg}


def _eval_node(node: ast.AST) -> float:
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in _OPS:
        return _OPS[type(node.op)](_eval_node(node.left), _eval_node(node.right))
    if isinstance(node, ast.UnaryOp) and type(node.op) in _OPS:
        return _OPS[type(node.op)](_eval_node(node.operand))
    raise ValueError("unsupported expression")


def calculate(query: str) -> tuple[str, bool]:
    """Extracts the first arithmetic-looking substring and safely evaluates it."""
    match = re.search(r"[\d\.\s]+(?:[\+\-\*\/][\d\.\s]+)+", query)
    if not match:
        return "no arithmetic expression found in the query", True
    expr = match.group(0).strip().rstrip(".")
    try:
        tree = ast.parse(expr, mode="eval")
        result = _eval_node(tree.body)
        return f"{expr.strip()} = {result:g}", False
    except (ValueError, SyntaxError, ZeroDivisionError):
        return f"could not evaluate '{expr}'", True


_SEARCH_TABLE = [
    (["python", "version"], "Python 3.13 is the latest stable release, published in 2024."),
    (["exchange rate", "usd", "eur"], "Illustrative rate: 1 USD = 0.92 EUR."),
    (["capital of france"], "Paris is the capital of France."),
]


def search(query: str, attempt: int) -> tuple[str, bool]:
    """Deterministic simulated search. The 'exchange rate' demo query fails
    on its first attempt specifically, to exercise the retry path -- not
    random, so the demo is reproducible."""
    blob = query.lower()
    if "exchange rate" in blob and attempt == 0:
        return "search timed out reaching the rates provider", True
    for keywords, answer in _SEARCH_TABLE:
        if all(kw in blob for kw in keywords):
            return answer, False
    return "no specific information found for that query", False
