from datetime import datetime
from sqlmodel import SQLModel, Field
from sqlalchemy import Column, DateTime as SaDateTime, func


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
    buildbot: str = Field(index=True)
    failure_reason: str | None = None


class Build(BuildBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class BuildCreate(BuildBase):
    pass


class BuildPublic(BuildBase):
    id: int
