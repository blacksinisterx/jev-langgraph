from .base import Provider
from .mock import MockProvider
from .typesafe import TypeSafeProvider
from .jev_agent import JevAgentProvider


def get_provider(name: str) -> Provider:
    providers = {
        "mock": MockProvider,
        "typesafe": TypeSafeProvider,
        "jev_agent": JevAgentProvider,
    }
    try:
        return providers[name]()
    except KeyError:
        raise ValueError(f"Unknown JEV_PROVIDER '{name}', expected one of {list(providers)}")
