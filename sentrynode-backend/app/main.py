from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db.database import engine, Base
import app.models  # Important: ensures models are registered

from app.routers import users, device, alerts, dashboard, logs

import subprocess

app = FastAPI(
    title="SentryNode Backend API",
    version="1.0.0"
)

@app.on_event("startup")
def run_migrations():
    subprocess.run(["alembic", "upgrade", "head"])

Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(
    users.router,
    prefix="/api/users",
    tags=["Users"]
)


app.include_router(
    device.router,
    prefix="/api/devices",
    tags=["Devices"]
)



app.include_router(
    alerts.protected_router,
    prefix="/api/alerts",
    tags=["Alerts"]
)

app.include_router(
    alerts.public_router,
    prefix="/api/alerts",
    tags=["Alerts"]
)


app.include_router(
    dashboard.router,
    prefix="/api/dashboard",
    tags=["Dashboard"]
)


app.include_router(
    logs.router,
    prefix="/api/logs",
    tags=["Logs"]
)