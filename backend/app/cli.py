from sqlmodel import Session, select
from typer import Typer

from app.db import engine
from app.models import BuildBot, BuildBotCreate
from app.services.buildbots import create_buildbot, set_buildbot, rotate_token

cli = Typer()

buildbot_cli = Typer(help="Manage contracts with magical buildbots")
cli.add_typer(buildbot_cli, name="buildbot")


@buildbot_cli.command()
def create(name: str, display_name: str | None = None):
    """Make a contract with QB and become a magical builtbot."""
    with Session(engine) as session:
        token = create_buildbot(
            session, BuildBotCreate(name=name, display_name=display_name)
        )
        session.commit()
    print(name, token)


@buildbot_cli.command()
def set(buildbot_name: str, enabled: bool):
    """Awaken a magical buildbot or send it into an enchanted slumber."""
    with Session(engine) as session:
        set_buildbot(session, buildbot_name, enabled)
        session.commit()


@buildbot_cli.command()
def rotate(buildbot_name: str):
    """Bestow a new secret token upon a magical buildbot."""
    with Session(engine) as session:
        token = rotate_token(session, buildbot_name)
        session.commit()
    print(buildbot_name, token)


@buildbot_cli.command(name="list")
def ls():
    """Reveal every magical buildbot under contract with QB."""
    with Session(engine) as session:
        buildbots = session.exec(select(BuildBot.name).distinct()).all()
        session.commit()
    print("\n".join(sorted(buildbots)))


if __name__ == "__main__":
    cli()
