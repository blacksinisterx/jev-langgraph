from app.tools import calculate, search


def test_calculate_evaluates_simple_arithmetic():
    result, failed = calculate("What is 47 * 68?")
    assert not failed
    assert "3196" in result


def test_calculate_strips_trailing_sentence_period():
    result, failed = calculate("Also calculate 128 + 256.")
    assert not failed
    assert result == "128 + 256 = 384"


def test_calculate_fails_with_no_expression():
    result, failed = calculate("What is the capital of France?")
    assert failed


def test_search_finds_known_topic():
    result, failed = search("What is the latest Python version?", attempt=0)
    assert not failed
    assert "Python" in result


def test_search_fails_first_attempt_for_flaky_demo_query():
    result, failed = search("Look up today's exchange rate", attempt=0)
    assert failed


def test_search_succeeds_on_retry_for_flaky_demo_query():
    result, failed = search("Look up today's exchange rate", attempt=1)
    assert not failed
