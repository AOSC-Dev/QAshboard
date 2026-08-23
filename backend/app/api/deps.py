from collections.abc import Generator
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel import Session, select
from typing import Annotated

from app.db import engine
from app.services.buildbots import hash_token
from app.models import BuildBot


def get_db() -> Generator[Session]:
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_db)]


security = HTTPBearer()


def auth_exception(detail: str | None = None):
    return HTTPException(
        status.HTTP_401_UNAUTHORIZED, detail, {"WWW-Authenticate": "Bearer"}
    )


def get_current_bot(
    session: SessionDep,
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
) -> BuildBot:
    if credentials.scheme.lower() != "bearer":
        raise auth_exception("Incorrect auth scheme")

    token_hash = hash_token(credentials.credentials)

    bot = session.exec(
        select(BuildBot).where(BuildBot.token_hash == token_hash)
    ).first()

    if not bot or not bot.enabled:
        raise auth_exception()

    return bot


BuildBotDep = Annotated[BuildBot, Depends(get_current_bot)]
