from fastapi import APIRouter, HTTPException
from sqlmodel import select

from app.api.deps import SessionDep
from app.models import Build, BuildCreate, BuildPublic


router = APIRouter()


@router.get("/health-check")
async def health_check() -> bool:
    return True


@router.get("/builds", response_model=list[BuildPublic])
async def get_builds(session: SessionDep, offset: int = 0, limit: int = 10):
    builds = session.exec(select(Build).offset(offset).limit(limit)).all()
    return builds


@router.get("/builds/{id}", response_model=BuildPublic)
async def get_build(id: int, session: SessionDep):
    build = session.get(Build, id)
    if not build:
        raise HTTPException(status_code=404, detail="Build not found")
    return build


@router.post("/builds", response_model=BuildPublic)
async def add_build(build: BuildCreate, session: SessionDep):
    db_build = Build.model_validate(build)
    session.add(db_build)
    session.commit()
    session.refresh(db_build)
    return db_build
