from sqlalchemy import create_engine


def get_engine(conn_str: str = "sqlite://", echo: bool = True):
    try:
        engine = create_engine(conn_str, echo=echo)
    except Exception as exc:
        raise Exception(f"Unhandled exception creating database engine. Details: {exc}")

    return engine
