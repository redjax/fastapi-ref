from typing import Optional

from database import Base
import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship


class ItemModel(Base):
    __tablename__ = "items"

    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(sa.String, index=True)
    description: Mapped[str] = mapped_column(sa.String)
    quantity: Mapped[int] = mapped_column(sa.Integer)
