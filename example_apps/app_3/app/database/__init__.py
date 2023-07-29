"""SQLAlchemy common database code.

Contains SQLAlchemy setup code, engine, and session(s). Uses dataclasses to define
database connection, and builds a default engine & session. The use of dataclasses is
to minimize depdencies for this common SQLAlchemy code so it can be easily re-used in
other projects utilizing SQLAlchemy for database operations.

The default engine and session are customizable using the get_engine() and get_session()
functions. These functions can be imported & called from another app, with customized
values to control engine & session behavior.

Currently supported databases:
    - [x] SQLite
    - [x] Postgres
    - [ ] MySQL
    - [x] MSSQL
    - [ ] Azure Cosmos
    
Be sure to import the Base object from this script and run Base.metadata.create_all(bind=engine)
as early as possible. For example, import the Base object from this script into main.py,
create/import an engine, and immediately run the metadata create function.
"""
import sqlalchemy as sa
from sqlalchemy import create_engine, orm as sa_orm
from sqlalchemy.orm import Session, sessionmaker, scoped_session

from .constants import valid_db_types
from .base import Base
from .connection_models import (
    saConnectionGeneric,
    saMSSQLConnection,
    saPGConnection,
    saSQLiteConnection,
)

from .utils import (
    generate_metadata,
    create_base_metadata,
    debug_metadata_obj,
    validate_db_type,
    get_engine,
    get_session,
)
