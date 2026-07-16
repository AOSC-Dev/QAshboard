from collections.abc import Generator
from fastapi import Depends
from sqlmodel import Session
from typing import Annotated

from app.db import engine


def get_db() -> Generator[Session]:
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_db)]
