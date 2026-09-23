from .http_base import HttpJevProvider


class TypeSafeProvider(HttpJevProvider):
    """Official Jev API. Needs a real TYPESAFE_API_KEY from console.typesafe.ai."""

    name = "typesafe"
    base_url = "https://api.typesafe.ai/v1/systemone"
    api_key_env = "TYPESAFE_API_KEY"
    input_price_per_million = 0.042
