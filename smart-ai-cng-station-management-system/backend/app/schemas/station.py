from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class StationBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    address: str
    city: str
    state: str
    latitude: float
    longitude: float
    total_dispensers: int = Field(..., gt=0)
    cng_price: float = Field(..., gt=0)
    is_active: bool = True


class StationCreate(StationBase):
    pass


class StationUpdate(BaseModel):
    name: str | None = None
    address: str | None = None
    city: str | None = None
    state: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    total_dispensers: int | None = None
    cng_price: float | None = None
    is_active: bool | None = None


class StationResponse(StationBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)