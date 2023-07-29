# FastAPI Reference Repo

A repository with multiple FastAPI demos, ranging from a simple app with a couple endpoints to a full app with `APIRouter` routes and `SQLAlchemy` database demos.

## Example Apps

### [App 1](example_apps/app_1/)

**Description**: `app_1` is a simple demo of FastAPI. The app is configured with `Dynaconf`, does not have a database or `APIRouter`, and only has a few simple endpoints. Demonstrates features like Python's `Annotated` syntax, FastAPI's `Depends()`, `CORSMiddleware`, `status.HTTP_XXX` responses, `jsonable_encoder`, & features to interact with OpenAPI documentation.

### [App 2](example_apps/app_2/)

*WIP*

### [App 3](example_apps/app_3/)

API with a database and CRUD endpoints. This is a simple SQLite database, which stores `Item`s, which have a `name`, `description`, and `quantity`.

Alembic is configured on this project for database migrations. Check the [App 3 README](example_apps/app_3/README.md) for notes on Alembic.

### [App 4](example_apps/app_4/)

This app runs in Docker. The `docker-compose.yml` file defines the stack for this API, with an NGINX reverse proxy, Postgres database, and PGAdmin for a web UI to manage the database.

Note the layout of the app, where `.env` files are in relation to the `docker-compose.yml` file. The settings for the FastAPI app are in `env_files/app.env`, but the rest of the configurations for the proxy, db, etc are in `.env` alongside the `docker-compose.yml` file.

**NOTE**: Dynaconf & environment variables described below

Also note the environment variables for the `api` service in `docker-compose.yml`. All ENV variables are prepended with `DYNACONF_APP`. When this app is run outside of Docker, i.e. with `pdm run start-server`, settings are loaded from `app/conf/{*.toml, *.local.toml}`. To override those settings with environment variables, i.e. when running in Docker, env variables must be defined as `DYANCONF_`.

For example, `APP_TITLE` as an env variable in the `api` Docker Compose service would be `DYNACONF_APP_TITLE: ${APP_TITLE:-Example Title}`.
