"""
Import Service — FastAPI application entry point.
SongNhat CRM Knowledge & Policy Assistant (WP02)
Implements: WP02, DAT01-08, OPS01, OPS05, SEC05, VN01, VN03
Status: Bootstrap skeleton. Business logic pending migration of src/importer/ code.
"""
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import JSONResponse
import structlog

from shared.logging.config import configure_logging
from src.api.routers import batches, withdrawals, health

SERVICE_NAME = os.getenv("SERVICE_NAME", "import-service")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
VERSION = "0.1.0"

configure_logging(SERVICE_NAME, LOG_LEVEL)
logger = structlog.get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("service_startup", service=SERVICE_NAME, version=VERSION)
    yield
    logger.info("service_shutdown", service=SERVICE_NAME)


app = FastAPI(
    title="SongNhat Import Service",
    description=(
        "Data Import & Integration Engine (WP02). "
        "Handles CSV batch ingestion, validation, quarantine, reconciliation and withdrawal. "
        "Implements: WP02, DAT01–08, OPS01, OPS05, SEC05, VN01, VN03."
    ),
    version=VERSION,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

app.include_router(health.router, tags=["Health"])
app.include_router(batches.router, prefix="/api/import/batches", tags=["Batches"])
app.include_router(withdrawals.router, prefix="/api/import/withdrawals", tags=["Withdrawals"])


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error("unhandled_exception", error=str(exc), path=str(request.url))
    return JSONResponse(
        status_code=500,
        content={"error_code": "INTERNAL_ERROR", "message": "Internal server error"},
    )
