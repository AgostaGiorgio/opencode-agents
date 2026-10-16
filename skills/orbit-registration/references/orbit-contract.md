# Orbit registry contract & operations

## Server side (the Orbit registry)

FastAPI app, all routes under `/api/v1`:

| Method | Path | Body | Response |
| --- | --- | --- | --- |
| POST | `/register` | `Registration` | 200 (empty) |
| GET | `/platforms` | — | `list[dict]` with `status` |

`Registration` (Pydantic):

| Field | Type | Notes |
| --- | --- | --- |
| `name` | `str` | required; id = `name.lower().strip().replace(" ", "_")` |
| `version` | `str` | required; service version |
| `description` | `str` | required |
| `icon` | `HttpUrl \| None` | optional; must be a URL if present |
| `url` | `HttpUrl` | required; public URL of the service |

`GET /platforms` adds a `status` computed from the last heartbeat:

| Age of last heartbeat | status |
| --- | --- |
| < 2 hours | `online` |
| 2–5 hours | `warning` |
| > 5 hours | `offline` |

Storage is an in-memory dict keyed by the normalized name: it is **not** persisted,
so restarting the Orbit backend clears the list until services heartbeat again
(at most one `ping_interval_seconds` later).

## Client side (each service)

- File: `src/clients/orbit_client.py`, class `OrbitClient`. Identical everywhere.
- On `start()`: spawns a daemon thread, POSTs immediately, then every
  `ping_interval_seconds` (default 3600 = 1h).
- On `stop()`: sets the stop event and joins the thread.
- `verify=False` on the POST (TLS verification disabled). Note: traffic to the
  registry is unauthenticated and TLS is not verified — treat as internal/
  best-effort telemetry, not a security boundary. Don't send secrets.
- Errors from `requests` are logged as warnings only.

## Field mapping: service -> registry payload

| OrbitClient arg | Registry field | Source in a service |
| --- | --- | --- |
| `orbit_api_url` | (POST target) | `app_config.orbit_api_url` (`ORBIT_API_URL`) |
| `name` | `name` | hardcoded service name |
| `version` | `version` | `APP_VERSION` from pyproject |
| `description` | `description` | hardcoded short description |
| `app_url` | `url` | `app_config.app_url` (`APP_URL`) |
| `icon` | `icon` | optional, default `None` |

## Verify

1. Start the service with `ORBIT_API_URL` and `APP_URL` set.
2. Confirm the first POST in the logs (no warning) or with curl:

   ```sh
   curl -s -X POST "$ORBIT_API_URL" \
     -H 'Content-Type: application/json' \
     -d '{"name":"Probe","version":"0","description":"probe","icon":null,"url":"https://example.dev"}'
   ```

3. List platforms:

   ```sh
   curl -s "$ORBIT_BASE/api/v1/platforms"
   ```

4. The service should appear with `status: "online"` (heartbeat < 2h).

## Disable

Leave `ORBIT_API_URL` unset/empty. The `if app_config.orbit_api_url` guard in
`main.py` keeps `orbit_client` undefined and the `else: yield` branch keeps the
app running normally.

