from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.schemas.camera import (
    CameraCreate,
    CameraUpdate,
    CameraResponse
)
from app.services import camera_service

router = APIRouter(
    prefix="/cameras",
    tags=["Cameras"]
)


@router.post(
    "/",
    response_model=CameraResponse,
    status_code=status.HTTP_201_CREATED
)
def create_camera(
    camera: CameraCreate,
    db: Session = Depends(get_db)
):
    return camera_service.create_camera(db, camera)


@router.get(
    "/",
    response_model=list[CameraResponse]
)
def get_cameras(
    db: Session = Depends(get_db)
):
    return camera_service.get_all_cameras(db)


@router.get(
    "/{camera_id}",
    response_model=CameraResponse
)
def get_camera(
    camera_id: int,
    db: Session = Depends(get_db)
):
    return camera_service.get_camera(db, camera_id)


@router.put(
    "/{camera_id}",
    response_model=CameraResponse
)
def update_camera(
    camera_id: int,
    camera: CameraUpdate,
    db: Session = Depends(get_db)
):
    return camera_service.update_camera(
        db,
        camera_id,
        camera
    )


@router.delete(
    "/{camera_id}",
    status_code=status.HTTP_200_OK
)
def delete_camera(
    camera_id: int,
    db: Session = Depends(get_db)
):
    return camera_service.delete_camera(
        db,
        camera_id
    )