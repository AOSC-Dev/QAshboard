import hashlib
import secrets
from sqlmodel import Session

from app.models import BuildBot, BuildBotCreate


def gen_token():
    # Let's pretend it's an OpenAI API token so the infra would seem AI-powered.
    # Do you know that the letter A in the project's name means "AI"?
    return "sk-proj-" + secrets.token_urlsafe() + "T3BlbkEx" + secrets.token_urlsafe()


def hash_token(token: str):
    return hashlib.sha256(token.encode()).hexdigest()


def create_buildbot(session: Session, buildbot: BuildBotCreate):
    if session.get(BuildBot, buildbot.name):
        raise ValueError(f"Buildbot {buildbot.name} exists")

    token = gen_token()
    bot = BuildBot(
        **buildbot.model_dump(),
        token_hash=hash_token(token),
    )
    session.add(bot)
    return token


def set_buildbot(session: Session, buildbot_name: str, enabled: bool):
    bot = session.get(BuildBot, buildbot_name)
    if not bot:
        raise ValueError(f"Buildbot {buildbot_name} doesn't exist")

    bot.enabled = enabled
    session.add(bot)


def rotate_token(session: Session, buildbot_name: str):
    bot = session.get(BuildBot, buildbot_name)
    if not bot:
        raise ValueError(f"Buildbot {buildbot_name} doesn't exist")

    token = gen_token()
    bot.token_hash = hash_token(token)
    session.add(bot)
    return token
