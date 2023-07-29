https://hackernoon.com/efficient-session-handling-using-the-repository-pattern-in-fastapi
https://praciano.com.br/fastapi-and-async-sqlalchemy-20-with-pytest-done-right.html

## Notes

### Running in Docker

* To get Dynaconf to load data from the environment, `environments=True` must be set on the Dyanconf `settings` object (in `app/config.py`)
  * When setting environment variables in the `docker-compose.yml` file, prepend `DYNACONF_` to any variable to load in the app
    * i.e. `APP_TITLE` env var should be declared in `docker-compose.yml` as `DYNACONF_APP_TITLE=${APP_TITLE:-Default title}`
* When using a Postgres database, the database must already exist
  * You can create a script to create the database in `db/postgres/pg_entrypoint/`, or use the attached PGAdmin container to open the web UI and create a database.
    * This database must match the ENV var `DYNACONF_DB_DATABASE` value
* On first clone:
  * Copy `.env.example` -> `.env`
  * Copy `env_files/app.env.example` -> `env_files/app.env`
  * Run `docker compose build && docker compose up -d`

### Alembic

**IMPORTANT**: After every model change (i.e. adding/removing fields, changing type, etc), you must run `alembic upgrade head` before running an `alembic revision`.

* Install with `pip install alembic`
* Initialize Alembic migrations
  * Ensure you are at the project root (i.e. the path with your `pyproject.toml` file)
  * Run `alembic init <alembic_dir_name>`
    * You can use any name you want, i.e. `alembic`, `migration`
  * Edit `alembic.ini`
    * `sqlalchemy.url = driver://user:pass@localhost/dbname`
      * Example: a database file located in `app/.db` named `demo.sqlite`:
        * `sqlalchemy.url = sqlite+pysqlite:///app/.db/demo.sqlite`
  * Edit `<alembic_dir_name>/env.py`
    * Find `target_metadata`
    * Above `target_metadata = None`, import your SQLAlchemy `Base` object
      * `from app.database import Base`
    * Set `target_metadata` to `Base.metadata`
      * target_metadata = Base.metadata
    * Example:
      * ```
        from app.database import Base

        target_metadata = Base.metadata
        ```
* Run first migration
  * `alembic revision --autogenerate -m "Some comment"`
