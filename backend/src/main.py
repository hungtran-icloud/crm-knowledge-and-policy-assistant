"""
SongNhat CRM Knowledge & Policy Assistant — Backend entrypoint.
Architecture: Modular Monolith + RAG + Policy Control Layer
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.config import settings
from src.db import engine, Base
from src.logging_config import configure_logging

from src.modules.identity.router import router as identity_router
from src.modules.knowledge.router import router as knowledge_router
from src.modules.ingestion.router import router as ingestion_router
from src.modules.policy.router import router as policy_router
from src.modules.answer.router import router as answer_router
from src.modules.admin.router import router as admin_router
from src.modules.feedback.router import router as feedback_router
from src.modules.audit.router import router as audit_router
from src.modules.evaluation.router import router as evaluation_router

configure_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    yield
    # Shutdown


app = FastAPI(
    title="CKPA Backend",
    description="SongNhat CRM Knowledge & Policy Assistant API",
    version="0.1.0",
    lifespan=lifespan,
    docs_url="/docs" if settings.APP_ENV != "production" else None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routers ───────────────────────────────────────────────────────────────────
API = "/api/v1"
app.include_router(identity_router,   prefix=f"{API}/identity",   tags=["Identity"])
app.include_router(knowledge_router,  prefix=f"{API}/knowledge",  tags=["Knowledge"])
app.include_router(ingestion_router,  prefix=f"{API}/ingestion",  tags=["Ingestion"])
app.include_router(policy_router,     prefix=f"{API}/policy",     tags=["Policy"])
app.include_router(answer_router,     prefix=f"{API}/answer",     tags=["Answer"])
app.include_router(admin_router,      prefix=f"{API}/admin",      tags=["Admin"])
app.include_router(feedback_router,   prefix=f"{API}/feedback",   tags=["Feedback"])
app.include_router(audit_router,      prefix=f"{API}/audit",      tags=["Audit"])
app.include_router(evaluation_router, prefix=f"{API}/evaluation", tags=["Evaluation"])


@app.get("/health", tags=["Health"])
async def health():
    return {"status": "ok", "version": "0.1.0"}
