# funlist
The best place to find fun

## Running ensure_single_admin.py with Docker Compose

1. Build the containers (first run only): `docker compose build`
2. Start Postgres in the background: `docker compose up -d db`
3. Run the admin-enforcement script inside the app container: `docker compose run --rm app python ensure_single_admin.py`
4. Shut everything down when finished: `docker compose down`

The compose file provisions a local Postgres instance (`postgres://funlist:funlist@localhost:5432/funlist`) and sets the `DATABASE_URL` inside the app service. The script runs inside the same container image that is used for the rest of the project, so it has access to the same dependencies and source tree. By default your local `.env` values are loaded, and the compose file overrides `DATABASE_URL` so the script connects to the Dockerized database instead of SQLite.
