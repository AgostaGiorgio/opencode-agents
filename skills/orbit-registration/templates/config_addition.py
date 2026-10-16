"""Additions to the project's AppConfig (pydantic-settings, see app_config.py).

Only add these fields; keep the existing CORS and DB fields.
"""

# Public URL of this service. Orbit validates it as an absolute http(s) URL,
# so the default "localhost" only works when Orbit is disabled. Set APP_URL in
# the environment to a real URL.
app_url: str = "localhost"

# Full Orbit registration endpoint (NOT the API root).
# Example: https://api.<orbit-host>/api/v1/register
# When empty/None, Orbit integration is disabled and the app runs normally.
orbit_api_url: str | None = None
