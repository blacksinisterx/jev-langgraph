from .http_base import HttpJevProvider


class JevAgentProvider(HttpJevProvider):
    """Free unofficial relay at jev-agent.com (not affiliated with TypeSafe AI,
    no uptime SLA, ~5k input tokens/month). Handy for capturing real screenshots
    locally; not meant to back a public deployment. Needs JEV_AGENT_KEY."""

    name = "jev_agent"
    base_url = "https://jev-agent.com/api/v1/systemone"
    api_key_env = "JEV_AGENT_KEY"
    input_price_per_million = 0.0  # free tier
