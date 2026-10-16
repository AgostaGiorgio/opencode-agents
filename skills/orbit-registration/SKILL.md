---
name: Orbit Registration
description: Use when adding or maintaining the Orbit umbrella integration in a FastAPI service (self-registration with a central Orbit registry). Covers the shared OrbitClient heartbeat, the FastAPI lifespan start/stop wiring in main.py, app_url/orbit_api_url config, and the registration contract of the Orbit registry API. Trigger on requests like "orbit", "aggiungi orbit", "registra il servizio su orbit", "umbrella", "OrbitClient", "heartbeat orbit", "ORBIT_API_URL", "platform registration", "iscrivi il servizio a orbit".
---

# Orbit service registration

Orbit is the umbrella that groups all the user's services under one dashboard.
Each service self-registers with the Orbit registry on startup and then sends a
heartbeat every hour. Orbit shows each platform as `online` / `warning` /
`offline` based on the last heartbeat.

Same implementation in every project:

```
src/clients/orbit_client.py   # OrbitClient: background heartbeat thread (identical everywhere)
src/config/app_config.py      # app_url + orbit_api_url fields
src/main.py                   # instantiate OrbitClient and start/stop it in lifespan
.env                          # ORBIT_API_URL (full register endpoint) + APP_URL
pyproject.toml                # requests, tomli
```

The Orbit registry (server side) is a FastAPI app exposing:
`POST /api/v1/register` and `GET /api/v1/platforms`.

## When to use

Use this skill to add Orbit registration to a new project, to update the
heartbeat/wiring, to change the service metadata, or to debug "the service does
not appear in Orbit".

## Workflow (add Orbit to a project)

1. **Client**: copy `templates/orbit_client.py` to `src/clients/orbit_client.py`.
   Keep it byte-identical across projects; do not customize it per service.
2. **Config**: add the `app_url` and `orbit_api_url` fields to `AppConfig`
   (see `templates/config_addition.py`).
3. **Dependencies**: ensure `requests` and `tomli` are in `pyproject.toml`
   (see `templates/pyproject_additions.toml`).
4. **Env**: add the two variables to `.env` and `.env.example`
   (see `templates/env_additions.env`). `ORBIT_API_URL` must be the **full**
   register endpoint, `APP_URL` must be a **full http(s) URL**.
5. **main.py**: add the version read + client instantiation + lifespan wiring
   exactly as in `templates/main_wiring.py`.
6. **Verify**: start the app and check the platform shows up (see
   `references/orbit-contract.md`).

## Non-negotiable rules

- **lifespan must always `yield`.** The `if orbit_api_url:` branch yields and
  stops the client; the `else` branch must also `yield`. A lifespan that returns
  without yielding makes FastAPI fail to start.
- **Keep the guard consistent.** `orbit_client` is defined only inside
  `if app_config.orbit_api_url:`. Reference it only under the same condition.
- **`ORBIT_API_URL` is the full registration URL**, including path
  (e.g. `https://api.<orbit-host>/api/v1/register`), not the API root.
- **`APP_URL` must be a valid absolute http(s) URL** (the registry validates it
  as `HttpUrl`; `localhost` without scheme is rejected with 422).
- **`name`/`description` are this service's identity** in Orbit; choose them once
  and keep them stable (e.g. a short product name and a one-line description).
- **Version comes from `pyproject.toml`** `[tool.poetry].version` via `tomli`.
  Keep that field present.
- **Registration is best-effort.** Network errors only log a warning; the app
  must start normally even if Orbit is unreachable or disabled.

## Pitfalls seen in the wild

- Missing `else: yield` in lifespan -> app crashes when `ORBIT_API_URL` is unset.
- `ORBIT_API_URL` pointing at the root (`http://localhost:8000`) instead of the
  endpoint -> heartbeat POSTs to `/` and gets 404; the service never registers.
- `APP_URL=localhost` (default) while `ORBIT_API_URL` is set -> registry returns
  422 and logs a warning; the platform never appears.
- `icon` set to a non-URL string -> registry 422. Leave it `None` or a real URL.
- Registry stores platforms **in memory**: restarting the Orbit backend clears
  the list until services heartbeat again (within `ping_interval_seconds`).

## Reference

- `references/orbit-contract.md` — endpoint contract, payload/status semantics,
  verification commands, security notes.
- `templates/orbit_client.py`, `templates/main_wiring.py`,
  `templates/config_addition.py`, `templates/env_additions.env`,
  `templates/pyproject_additions.toml`.
