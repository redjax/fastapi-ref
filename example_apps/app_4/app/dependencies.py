from __future__ import annotations

from config import ENV, api_settings, db_settings, settings
from database import (
    Base,
    create_base_metadata,
    debug_metadata_obj,
    get_engine,
    get_session,
    saSQLiteConnection,
    scoped_session,
)
import sqlalchemy as sa

from sqlalchemy.orm import Session, sessionmaker

db_config = saSQLiteConnection(database=db_settings.db_database)
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
