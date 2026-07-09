from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.schemas.vehicle_log import (
    VehicleLogCreate,
    VehicleLogUpdate,
    VehicleLogResponse,
)
from app.services import vehicle_log_service

router = APIRouter(
    prefix="/vehicle-logs",
    tags=["Vehicle Logs"]
)


@router.post(
    "/",
    response_model=VehicleLogResponse,
    status_code=status.HTTP_201_CREATED
)
def create_vehicle_log(
    vehicle_log: VehicleLogCreate,
    db: Session = Depends(get_db)
):
    return vehicle_log_service.create_vehicle_log(db, vehicle_log)


@router.get(
    "/",
    response_model=list[VehicleLogResponse]
)
def get_vehicle_logs(
    db: Session = Depends(get_db)
):
    return vehicle_log_service.get_all_vehicle_logs(db)


@router.get(
    "/{vehicle_log_id}",
    response_model=VehicleLogResponse
)
def get_vehicle_log(
    vehicle_log_id: int,
    db: Session = Depends(get_db)
):
    return vehicle_log_service.get_vehicle_log(
        db,
        vehicle_log_id
    )


@router.put(
    "/{vehicle_log_id}",
    response_model=VehicleLogResponse
)
def update_vehicle_log(
    vehicle_log_id: int,
    vehicle_log: VehicleLogUpdate,
    db: Session = Depends(get_db)
):
    return vehicle_log_service.update_vehicle_log(
        db,
        vehicle_log_id,
        vehicle_log
    )


@router.delete(
    "/{vehicle_log_id}",
    status_code=status.HTTP_200_OK
)
def delete_vehicle_log(
    vehicle_log_id: int,
    db: Session = Depends(get_db)
):
    return vehicle_log_service.delete_vehicle_log(
        db,
        vehicle_log_id
    )