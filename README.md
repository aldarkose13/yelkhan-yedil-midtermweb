# Space Bounty Hunters API

REST API built with **FastAPI**, **SQLAlchemy** and **PostgreSQL**.

## Setup

Copy `.env.example` to `.env` (it holds the Postgres credentials and `DATABASE_URL`).
PostgreSQL is published on host port **5434** (container port 5432).

### Option A: everything in Docker (recommended)

```bash
docker compose up --build
```

This starts PostgreSQL and the API. On startup the API creates the tables and imports the seed data
(6 criminals, 12 hunt logs) if the database is empty. Nothing else to run.

- API: http://localhost:8000  - interactive docs: http://localhost:8000/docs
- Reset the data: `docker compose exec api python seed.py` (drops, recreates and reseeds the tables)
- Full reset including credentials/volume: `docker compose down -v`

### Option B: API on the host, only the database in Docker

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows  (Linux/macOS: source .venv/bin/activate)
pip install -r requirements.txt
docker compose up -d db         # or use your own Postgres and adjust DATABASE_URL in .env
python seed.py                  # create tables + import seed data (wipes existing data)
uvicorn main:app --reload
```

`DATABASE_URL` in `.env` points at `localhost:5434`. Inside Docker, compose overrides it to use the
`db` service on port 5432.

## Models

- **WantedCriminal** (`wanted_criminals`): id, name (nullable), nickname, reward, latitude/longitude (nullable),
  last_known_location_note, difficulty (1-10, DB check constraint), armed, has_crew, escape_master.
- **HuntLog** (`hunt_logs`): id, criminal_id (FK), success, notes, created_at (server-generated).
- One-to-many: `WantedCriminal.hunts` <-> `HuntLog.criminal`.

## Endpoints

| Method | Path | Description |
|---|---|---|
| GET | `/api/criminals/` | List. Query: `min_reward`, `max_reward`, `armed`, `has_crew`, `escape_master`, `sort` (`reward` / `-reward`). Filters combine. |
| GET | `/api/criminals/{id}/` | Details (404 if missing) |
| GET | `/api/hunts/` | List. Query: `criminal_id` |
| GET | `/api/hunts/{id}/` | Details |
| POST | `/api/hunts/` | Create (`criminal_id`, `success`, `notes`) -> 201 |
| PATCH | `/api/hunts/{id}/` | Update `success` / `notes` |
| DELETE | `/api/hunts/{id}/` | Delete -> 204 |

Example: `GET /api/criminals/?min_reward=5000&armed=true&sort=-reward`

### Status codes / validation

- `404` unknown criminal or hunt id (including `criminal_id` on POST)
- `422` malformed body or ids, missing required fields, unknown fields (e.g. client-sent `created_at` is rejected)
- `400` invalid `sort` value, or `min_reward > max_reward`

## Postman

Import `postman/SpaceBountyHunters.postman_collection.json` (variable `baseUrl` = `http://localhost:8000`).
Run the requests in order (or use the Collection Runner) after running `python seed.py`.
