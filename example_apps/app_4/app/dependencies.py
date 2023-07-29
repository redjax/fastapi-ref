from __future__ import annotations

from config import ENV, api_settings, db_settings, settings
from database import (
    Base,
    create_base_metadata,
    debug_metadata_obj,
    get_engine,
    get_session,
    saSQLiteConnection,
    saPGConnection,
    scoped_session,
)
import sqlalchemy as sa

from sqlalchemy.orm import Session, sessionmaker

match db_settings.db_type:
    case "sqlite":
        db_config = saSQLiteConnection(database=db_settings.db_database)
    case "postgres":
        db_config = saPGConnection(
            host=db_settings.db_host,
            username=db_settings.db_username,
            password=db_settings.db_password,
            database=db_settings.db_database,
        )
    case _:
        raise Exception(f"Unknown DB_TYPE: {db_settings.db_type}")

print(
    f"<< DATABASE CONNECTION STRING >>: (USER: {db_config.username}) {db_config.connection_string}"
)
engine = get_engine(connection=db_config, db_type=db_settings.db_type, echo=True)
SessionLocal = get_session(engine=engine)


def get_db():
    db = SessionLocal()

    try:
        yield db
    except Exception as exc:
        raise Exception(f"Unhandled exception getting database session. Details: {exc}")

    finally:
        db.close()
