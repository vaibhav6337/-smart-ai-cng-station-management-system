from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class VehicleLogBase(BaseModel):
    camera_id: int

    vehicle_type: str = Field(..., min_length=2, max_length=50)

    entry_time: datetime | None = None

    exit_time: datetime | None = None

    status: str = "IN_QUEUE"


class VehicleLogCreate(VehicleLogBase):
    pass


class VehicleLogUpdate(BaseModel):
    camera_id: int | None = None
    vehicle_type: str | None = None
    entry_time: datetime | None = None
    exit_time: datetime | None = None
    status: str | None = None


class VehicleLogResponse(VehicleLogBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)