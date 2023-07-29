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
