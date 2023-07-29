from __future__ import annotations

from typing import Optional

import sqlalchemy as sa

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass
