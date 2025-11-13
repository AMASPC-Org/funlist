# funlist
The best place to find fun.

## Requirements
- Python 3.11 or newer
- A virtual environment tool (`uv`, `venv`, or `virtualenv`)
- A database reachable via SQLAlchemy (SQLite is preconfigured for local work)
- A Google Maps JavaScript API key

## Setup

### 1. Install dependencies
```bash
# Create and activate a virtual environment (choose one approach)
uv venv && source .venv/bin/activate
# or
python3 -m venv .venv && source .venv/bin/activate

# Sync Python packages (replace with `pip install -r` if you prefer pip)
uv pip sync pyproject.toml uv.lock
```

### 2. Configure environment variables
1. Edit `env.local.sh` and replace `REPLACE_WITH_REAL_KEY` with your Google Maps key.  
   You can also set a stronger `FLASK_SECRET_KEY` or point `DATABASE_URL` at Postgres.
2. Source the script so the variables apply to your current shell:
   ```bash
   source env.local.sh
   ```
3. (Optional) Add the `source env.local.sh` line to your shell profile for convenience.

### 3. Prepare the database
- The default `DATABASE_URL` uses `instance/funlist.db`. Ensure the directory exists:
  ```bash
  mkdir -p instance
  ```
- On first boot `create_app()` will run `db.create_all()` and `update_schema.py`, so no manual migrations are required for SQLite. If you point to Postgres, make sure the target database already exists (e.g., `createdb funlist`).

## Running the app
```bash
python main.py
```
`main.py` finds an open port (default 5000), applies schema updates, and serves Flask on `0.0.0.0`. You should see output similar to:
```
Starting Flask server on port 5000
🚀 Server running at: http://0.0.0.0:5000
```

Navigate to `http://localhost:5000/map` to verify that event markers load and the draw-to-filter control appears. Check `app.log` if the server exits or if the map fails to load (missing Google Maps key is a common culprit).

## Useful scripts
- `add_sample_events.py`, `create_admin.py`, etc. populate the database with seed data once the environment variables are set.
- `env.local.sh` manages the standard runtime configuration and can be sourced in any new shell session.

## Docker workflow
You can spin up both the Flask app and a local Postgres instance with Docker Compose:
```bash
docker compose up --build
```
Environment defaults live in `docker-compose.yml`. Override the Google Maps key by exporting `GOOGLE_MAPS_API_KEY` before running Compose (or by editing the file). The app will be available at `http://localhost:5000`, and Postgres data persists in the `pg_data` volume. Use `docker compose down -v` to tear everything down, including the database volume.
