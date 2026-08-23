from datetime import datetime
from pydantic import BaseModel
from sqlmodel import SQLModel, Field
from sqlalchemy import Column, DateTime as SaDateTime, func


class BuildBotBase(SQLModel):
    name: str = Field(primary_key=True)
    display_name: str | None = None
    enabled: bool = True


class BuildBot(BuildBotBase, table=True):
    token_hash: str = Field(index=True, unique=True)


class BuildBotCreate(BuildBotBase):
    pass


class BuildBase(SQLModel):
    package_name: str = Field(index=True)
    success: bool
    timestamp: datetime = Field(
        sa_column=Column(
            SaDateTime(timezone=True),
            nullable=False,
            server_default=func.now(),
        ),
    )
    architecture: str = Field(index=True)
    buildbot: str = Field(index=True, foreign_key="buildbot.name")
    failure_reason: str | None = None


class Build(BuildBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class BuildCreate(BuildBase):
    pass


class BuildPublic(BuildBase):
    id: int


class Builds(BaseModel):
    total: int
    items: list[BuildPublic]


class CoveragePoint(BaseModel):
    snapshot: datetime
    architecture: str
    coverage: float
