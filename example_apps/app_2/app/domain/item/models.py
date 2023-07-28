from typing import Optional

from database import Base
import sqlalchemy as sa

from sqlalchemy.orm import Mapped, mapped_column, relationship


class ItemModel(Base):
    __tablename__ = "items"

    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(sa.String(32), index=True)
    description: Mapped[str] = mapped_column(sa.String(260))

    def __repr__(self):
        return f"Item(id={self.id!r}, title={self.title!r}, description={self.description!r})"
