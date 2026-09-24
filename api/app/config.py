import os


def _env(key: str, default: str) -> str:
    """Treats a present-but-blank env var the same as an absent one.
    os.environ.get(key, default) only falls back when the key is missing
    entirely -- a blank value (e.g. from a dashboard env var accidentally
    set with no value) passes straight through and breaks whatever parses
    it. Confirmed this actually happens, not just theoretical."""
    val = os.environ.get(key, "").strip()
    return val or default


JEV_PROVIDER = _env("JEV_PROVIDER", "mock")
JEV_MODEL = _env("JEV_MODEL", "jev-latest")
