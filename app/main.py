"""
AgriPredictAI Backend - FastAPI Entry Point
"""
import logging
from sqlalchemy import inspect, text

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import (
    auth_api, profile_api, data_api, prediction_api,
    feasibility_api, profit_api, risk_api,
    recommendation_api, simulation_api, alert_api, dashboard_api,
    chatbot_api, voice_api, debug_api, rotation_api, climate_routes,
    chatbot_routes,
)
from app.api import test_api
from app.core.config import settings
from app.db import engine
from app.models import Base

_startup_logger = logging.getLogger("api")

app = FastAPI(
    title="AgriPredictAI",
    description="AI-powered agricultural prediction and decision support system",
    version="1.0.0"
)


def _run_migrations() -> None:
    """Apply incremental schema migrations that create_all cannot handle.

    Runs on every startup and performs idempotent checks before applying
    migrations. Each migration is a no-op if the change is already present,
    so it is safe to run on every startup and across multiple instances.
    """
    inspector = inspect(engine)
    # Add 'username' column to 'users' table if it was created before this field was added
    if "users" in inspector.get_table_names():
        existing_cols = {col["name"] for col in inspector.get_columns("users")}
        if "username" not in existing_cols:
            try:
                with engine.connect() as conn:
                    conn.execute(text("ALTER TABLE users ADD COLUMN username VARCHAR(120)"))
                    conn.commit()
                _startup_logger.info("Migration applied: added 'username' column to 'users' table")
            except Exception as exc:  # noqa: BLE001
                # Column may have been added by a concurrent instance; log and continue
                _startup_logger.warning("Migration 'add username column' skipped (may already exist): %s", exc)


@app.on_event("startup")
def on_startup() -> None:
    """Create database tables on startup if they do not exist."""
    Base.metadata.create_all(bind=engine)
    _run_migrations()
    _startup_logger.info(
        "AgriPredictAI backend started | CORS origins: %s",
        settings.CORS_ORIGINS,
    )

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(auth_api.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(profile_api.router, prefix="/api/profile", tags=["Profile"])
app.include_router(data_api.router, prefix="/api/data", tags=["Data"])
app.include_router(prediction_api.router, prefix="/api/prediction", tags=["Prediction"])
app.include_router(feasibility_api.router, prefix="/api/feasibility", tags=["Feasibility"])
app.include_router(profit_api.router, prefix="/api/profit", tags=["Profit"])
app.include_router(risk_api.router, prefix="/api/risk", tags=["Risk"])
app.include_router(recommendation_api.router, prefix="/api/recommendation", tags=["Recommendation"])
app.include_router(simulation_api.router, prefix="/api/simulation", tags=["Simulation"])
app.include_router(alert_api.router, prefix="/api/alert", tags=["Alert"])
app.include_router(dashboard_api.router, prefix="/api/dashboard", tags=["Dashboard"])
app.include_router(chatbot_api.router, prefix="/api/chat", tags=["Chatbot"])
app.include_router(voice_api.router, prefix="/api/chat", tags=["Voice"])
app.include_router(test_api.router, prefix="/api/chat", tags=["Chatbot"])
app.include_router(debug_api.router, tags=["Debug"])
app.include_router(rotation_api.router, prefix="/api/rotation", tags=["Rotation"])
app.include_router(climate_routes.router, prefix="/api/climate", tags=["Climate"])
app.include_router(chatbot_routes.router, prefix="/api/chatbot", tags=["Farmer Assistant"])

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
