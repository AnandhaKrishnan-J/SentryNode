from fastapi import FastAPI
from app.routers import dashboard, alerts, auth

from app.db.database import Base, engine
import app.models

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SentryNode Backend API",
    version="1.0.0"
)

app.include_router(
    dashboard.router,
    prefix="/api/dashboard",
    tags=["Dashboard"]
)

app.include_router(
    alerts.router,
    prefix="/api/alerts",
    tags=["Alerts"]
)

app.include_router(
    auth.router,
    prefix="/api/auth",
    tags=["Auth"]
)