from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.camera import Camera
from app.models.station import Station
from app.schemas.camera import CameraCreate, CameraUpdate


def create_camera(db: Session, camera: CameraCreate):
    station = db.query(Station).filter(
        Station.id == camera.station_id
    ).first()

    if station is None:
        raise HTTPException(
            status_code=404,
            detail="Station not found"
        )

    db_camera = Camera(**camera.model_dump())

    db.add(db_camera)
    db.commit()
    db.refresh(db_camera)

    return db_camera


def get_all_cameras(db: Session):
    return db.query(Camera).all()


def get_camera(db: Session, camera_id: int):
    camera = db.query(Camera).filter(
        Camera.id == camera_id
    ).first()

    if camera is None:
        raise HTTPException(
            status_code=404,
            detail="Camera not found"
        )

    return camera


def update_camera(
    db: Session,
    camera_id: int,
    camera_data: CameraUpdate
):
    camera = db.query(Camera).filter(
        Camera.id == camera_id
    ).first()

    if camera is None:
        raise HTTPException(
            status_code=404,
            detail="Camera not found"
        )

    update_data = camera_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(camera, field, value)

    db.commit()
    db.refresh(camera)

    return camera


def delete_camera(db: Session, camera_id: int):
    camera = db.query(Camera).filter(
        Camera.id == camera_id
    ).first()

    if camera is None:
        raise HTTPException(
            status_code=404,
            detail="Camera not found"
        )

    db.delete(camera)
    db.commit()

    return {
        "success": True,
        "message": "Camera deleted successfully"
    }