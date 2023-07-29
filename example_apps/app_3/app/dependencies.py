from config import settings, api_settings, db_settings, ENV
from database import (
    create_base_metadata,
    saSQLiteConnection,
    get_engine,
    debug_metadata_obj,
    get_session,
    Base,
    scoped_session,
)


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
