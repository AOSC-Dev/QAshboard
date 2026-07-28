from fastapi import APIRouter, HTTPException, Query
from datetime import datetime, timedelta, timezone
from sqlalchemy import func, text
from sqlmodel import col, select

from app.api.deps import SessionDep
from app.models import Build, BuildCreate, BuildPublic, Builds, CoveragePoint


router = APIRouter()


@router.get("/health-check")
def health_check() -> bool:
    return True


@router.get("/builds", response_model=Builds)
def get_builds(session: SessionDep, offset: int = 0, limit: int = 10):
    total = session.exec(select(func.count()).select_from(Build)).one()
    builds = session.exec(
        select(Build)
        .order_by(col(Build.id).desc())
        .offset(offset)
        .limit(limit if limit != -1 else None)
    ).all()
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
def add_build(build: BuildCreate, session: SessionDep):
    db_build = Build.model_validate(build)
    session.add(db_build)
    session.commit()
    session.refresh(db_build)
    return db_build


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
