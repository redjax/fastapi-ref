# Domain

Create new domain objects, each with a `models.py` and `schemas.py`, at minimum. Convert between schemas & models for communicating with the API (schemas) and database (models).

## Creating a new domain

To create a new domain, i.e. `book`, make a directory, add an `__init__.py` file, and create a `models.py` and `schemas.py` file. Define database models (`SQLAlchemy`) in `models.py`, and API schemas (`Pydantic`) in `schemas.py`
