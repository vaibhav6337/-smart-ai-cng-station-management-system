from fastapi import FastAPI
from app.api.v1.vehicle_log import router as vehicle_log_router
from app.api.v1.station import router as station_router
from app.api.v1.camera import router as camera_router
from app.core.config import settings

app = FastAPI(
    title="Smart AI CNG Station Management System",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "message": "API is running",
        "database_connected_to": settings.DATABASE_URL.split("@")[-1]
    }


app.include_router(
    station_router,
    prefix="/api/v1"
)

app.include_router(
    camera_router,
    prefix="/api/v1"
)


app.include_router(
    vehicle_log_router,
    prefix="/api/v1"
)