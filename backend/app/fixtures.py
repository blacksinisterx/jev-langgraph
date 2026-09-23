DEMO_QUERIES: list[dict] = [
    {"category": "pure calculation", "query": "What is 47 * 68?"},
    {"category": "pure search", "query": "What is the latest stable version of Python?"},
    {"category": "search then tool", "query": "What is the capital of France? Also calculate 128 + 256."},
    {"category": "search fails, retries", "query": "Look up today's exchange rate and convert 100 USD to EUR."},
    {"category": "escalates to human", "query": "Should I accept a job offer with lower pay but a team I like more?"},
]
