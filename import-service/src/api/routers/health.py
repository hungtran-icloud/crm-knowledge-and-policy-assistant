"""Health check endpoints — liveness, readiness, metrics."""
import os
from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict

router = APIRouter()


class HealthResponse(BaseModel):
    status: str
    service: str
    version: str
    checks: Dict[str, bool]


@router.get("/health/live", response_model=HealthResponse, summary="Liveness probe")
async def liveness():
    """Returns 200 if the service process is alive."""
    return HealthResponse(
        status="ok",
        service=os.getenv("SERVICE_NAME", "import-service"),
        version="0.1.0",
        checks={"process": True},
    )


@router.get("/health/ready", response_model=HealthResponse, summary="Readiness probe")
async def readiness():
    """Returns 200 if DB and Redis are reachable. TODO: implement real checks."""
    checks = {"process": True, "database": True, "redis": True}
    status = "ok" if all(checks.values()) else "degraded"
    return HealthResponse(
        status=status,
        service=os.getenv("SERVICE_NAME", "import-service"),
        version="0.1.0",
        checks=checks,
    )


@router.get("/metrics", summary="Prometheus metrics (placeholder)")
async def metrics():
    """Prometheus metrics — wire to prometheus_client in next phase."""
    return {"message": "metrics placeholder — not yet implemented"}
