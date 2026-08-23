from fastapi import APIRouter, HTTPException, Query, Response, status, UploadFile
from fastapi.responses import FileResponse
from datetime import datetime, timedelta, timezone
from os import replace
from pathlib import Path
from sqlalchemy import func, text
from sqlmodel import col, select
from tempfile import NamedTemporaryFile

from app.api.deps import SessionDep, BuildBotDep, auth_exception
from app.config import settings
from app.models import Build, BuildCreate, BuildPublic, Builds, CoveragePoint


router = APIRouter()


@router.get("/health-check")
def health_check() -> bool:
    return True


@router.get("/builds", response_model=Builds)
def get_builds(
    session: SessionDep,
    offset: int = 0,
    limit: int = 10,
    success: bool | None = None,
):
    total_stmt = select(func.count()).select_from(Build)
    build_stmt = (
        select(Build)
        .order_by(col(Build.id).desc())
        .offset(offset)
        .limit(limit if limit != -1 else None)
    )
    if success is not None:
        total_stmt = total_stmt.where(Build.success == success)
        build_stmt = build_stmt.where(Build.success == success)

    total = session.exec(total_stmt).one()
    builds = session.exec(build_stmt).all()

    return Builds(
        total=total, items=[BuildPublic.model_validate(build) for build in builds]
    )


@router.get("/builds/{id}", response_model=BuildPublic)
def get_build(id: int, session: SessionDep):
    build = session.get(Build, id)
    if not build:
        raise HTTPException(status_code=404, detail="Build not found")
    return build


@router.post("/builds", response_model=BuildPublic)
def add_build(build: BuildCreate, session: SessionDep, buildbot: BuildBotDep):
    db_build = Build.model_validate(build)
    if build.buildbot != buildbot.name:
        raise auth_exception()

    session.add(db_build)
    session.commit()
    session.refresh(db_build)
    return db_build


@router.put(
    "/builds/{id}/logs",
    status_code=status.HTTP_201_CREATED,
    responses={status.HTTP_204_NO_CONTENT: {"description": "Build log replaced"}},
)
def upload_build_logs(
    id: int,
    file: UploadFile,
    session: SessionDep,
    response: Response,
    builtbot: BuildBotDep,
):
    build = session.get(Build, id)
    if build is None:
        raise HTTPException(404, "Build not found")
    if build.buildbot != builtbot.name:
        raise auth_exception()

    file_path = settings.BUILD_LOGS_PATH / str(id)
    if file_path.exists():
        response.status_code = status.HTTP_204_NO_CONTENT

    temp_file_path: str | None = None
    try:
        with NamedTemporaryFile(
            delete=False, dir=settings.BUILD_LOGS_TEMP_PATH
        ) as temp_file:
            temp_file_path = temp_file.name
            while chunk := file.file.read(1024**2):
                temp_file.write(chunk)
        replace(temp_file_path, file_path)
    finally:
        if temp_file_path is not None:
            Path(temp_file_path).unlink(missing_ok=True)

    return {"id": id}


@router.get(
    "/builds/{id}/logs",
    response_class=FileResponse,
    responses={200: {"content": {"text/plain": {"schema": {"type": "string"}}}}},
)
def get_build_logs(id: int, session: SessionDep):
    if session.get(Build, id) is None:
        raise HTTPException(404, "Build not found")

    file_path = settings.BUILD_LOGS_PATH / str(id)
    if not file_path.exists():
        raise HTTPException(404, "Build log not found")

    return FileResponse(settings.BUILD_LOGS_PATH / str(id), media_type="text/plain")


@router.get("/stats/coverage", response_model=list[CoveragePoint])
def get_coverage(
    session: SessionDep,
    start: datetime = Query(datetime(2020, 1, 1, tzinfo=timezone.utc)),
    end: datetime = Query(datetime.now(timezone.utc)),
    interval: timedelta = Query(timedelta(weeks=1)),
):
    """
    `interval` is an ISO 8601 duration, e.g. P1W or P1D.
    """
    start, end = start.astimezone(timezone.utc), end.astimezone(timezone.utc)
    if end is not None and end < start:
        raise HTTPException(
            status_code=422,
            detail="end must be on or after start",
        )
    if interval <= timedelta(0):
        raise HTTPException(status_code=422, detail="interval must be positive")

    query = text("""
        WITH
        snapshots AS (
            SELECT generate_series(
                CAST(:start_date AS timestamptz),
                COALESCE(CAST(:end_date AS timestamptz), CURRENT_DATE),
                CAST(:interval AS interval)
            ) AS snapshot
        ),

        intervals AS (
            SELECT
                package_name,
                architecture,
                success,
                tstzrange(
                    timestamp,
                    lead(timestamp) OVER (
                        PARTITION BY package_name, architecture
                        ORDER BY timestamp, id
                    )
                ) AS validity
            FROM build
        )

        SELECT
            s.snapshot,
            i.architecture,
            COUNT(*) FILTER (WHERE i.success) * 100.0 / COUNT(*) AS coverage
        FROM snapshots s
        JOIN intervals i
            ON i.validity @> s.snapshot
        GROUP BY
            s.snapshot,
            i.architecture
        ORDER BY
            s.snapshot,
            i.architecture;
    """)

    coverage = (
        session.execute(
            query,
            {
                "start_date": start,
                "end_date": end,
                "interval": interval,
            },
        )
        .mappings()
        .all()
    )
    return [CoveragePoint.model_validate(row) for row in coverage]
