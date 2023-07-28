from typing import Annotated

from fastapi import Header, HTTPException

from database import Base, get_engine

sqla_base = Base()
sqla_engine = get_engine()
# sqla_engine = get_engine(connection=default_sqlite_conn, echo=True)


async def get_token_header(x_token: Annotated[str, Header()]):
    if x_token != "fake-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")


async def get_query_token(token: str):
    if token != "jack":
        raise HTTPException(status_code=400, detail="No Jack token provided")


# def get_db(engine=sqla_engine):
#     db = get_session(engine=engine)

#     try:
#         yield db
#     except Exception as exc:
#         raise Exception(f"Error returning database. Details: {exc}")
