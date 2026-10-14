from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class CameraBase(BaseModel):
    station_id: int

    camera_name: str = Field(..., min_length=2, max_length=100)

    camera_type: str = "IP"

    camera_url: str

    camera_position: str

    resolution: str = "1920x1080"

    fps: int = Field(default=30, gt=0)

    status: str = "OFFLINE"

    is_recording: bool = False

    last_seen: datetime | None = None

    is_active: bool = True


class CameraCreate(CameraBase):
    pass


class CameraUpdate(BaseModel):
    station_id: int | None = None
    camera_name: str | None = None
    camera_type: str | None = None
    camera_url: str | None = None
    camera_position: str | None = None
    resolution: str | None = None
    fps: int | None = None
    status: str | None = None
    is_recording: bool | None = None
    last_seen: datetime | None = None
    is_active: bool | None = None


class CameraResponse(CameraBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)