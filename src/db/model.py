from __future__ import annotations

from datetime import datetime

import uuid
from sqlmodel import Field, SQLModel, Relationship


class TagInfoLink(SQLModel, table=True):
    __tablename__ = "tag_info_link"
    tag_id: int | None = Field(default=None, foreign_key="tag.id", primary_key=True)
    info_id: int | None = Field(default=None, foreign_key="info.id", primary_key=True)


class Tag(SQLModel, table=True):
    __tablename__ = "tag"

    id: int = Field(primary_key=True)
    name: str = Field(unique=True)
    description: str | None = None

    infos: list[LoadInfo] = Relationship(back_populates="tags", link_model=TagInfoLink)


class LoadInfo(SQLModel, table=True):
    __tablename__ = "info"

    id: int = Field(primary_key=True)
    uuid: uuid.UUID
    id_plan: int
    name: str
    created_at: datetime
    start_datetime: datetime
    end_datetime: datetime
    description: str | None = None

    tags: list[Tag] = Relationship(back_populates="infos", link_model=TagInfoLink)
