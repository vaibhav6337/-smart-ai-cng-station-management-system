from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.camera import Camera
from app.models.vehicle_log import VehicleLog
from app.schemas.vehicle_log import (
    VehicleLogCreate,
    VehicleLogUpdate,
)


def create_vehicle_log(db: Session, vehicle_log: VehicleLogCreate):
    camera = db.query(Camera).filter(
        Camera.id == vehicle_log.camera_id
    ).first()

    if camera is None:
        raise HTTPException(
            status_code=404,
            detail="Camera not found"
        )

    db_vehicle_log = VehicleLog(**vehicle_log.model_dump())

    db.add(db_vehicle_log)
    db.commit()
    db.refresh(db_vehicle_log)

    return db_vehicle_log


def get_all_vehicle_logs(db: Session):
    return db.query(VehicleLog).all()


def get_vehicle_log(db: Session, vehicle_log_id: int):
    vehicle_log = db.query(VehicleLog).filter(
        VehicleLog.id == vehicle_log_id
    ).first()

    if vehicle_log is None:
        raise HTTPException(
            status_code=404,
            detail="Vehicle log not found"
        )

    return vehicle_log


def update_vehicle_log(
    db: Session,
    vehicle_log_id: int,
    vehicle_log_data: VehicleLogUpdate,
):
    vehicle_log = db.query(VehicleLog).filter(
        VehicleLog.id == vehicle_log_id
    ).first()

    if vehicle_log is None:
        raise HTTPException(
            status_code=404,
            detail="Vehicle log not found"
        )

    update_data = vehicle_log_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(vehicle_log, field, value)

    db.commit()
    db.refresh(vehicle_log)

    return vehicle_log


def delete_vehicle_log(db: Session, vehicle_log_id: int):
    vehicle_log = db.query(VehicleLog).filter(
        VehicleLog.id == vehicle_log_id
    ).first()

    if vehicle_log is None:
        raise HTTPException(
            status_code=404,
            detail="Vehicle log not found"
        )

    db.delete(vehicle_log)
    db.commit()

    return {
        "success": True,
        "message": "Vehicle log deleted successfully",
    }