from datetime import datetime

from pydantic import BaseModel, ConfigDict


class StationCreate(BaseModel):
    """Fields accepted when creating a station."""

    name: str
    address: str
    city: str
    state: str

    latitude: float | None = None
    longitude: float | None = None

    total_dispensers: int = 1
    active_dispensers: int = 1
    average_fueling_time: int = 4
    average_waiting_time: float = 0

    cng_price: float | None = None
    is_active: bool = True

    source: str = "managed"
    owner_id: int | None = None


class StationUpdate(BaseModel):
    """Fields that can be updated on an existing station."""

    name: str | None = None
    address: str | None = None
    city: str | None = None
    state: str | None = None

    latitude: float | None = None
    longitude: float | None = None

    total_dispensers: int | None = None
    active_dispensers: int | None = None
    average_fueling_time: int | None = None
    average_waiting_time: float | None = None

    cng_price: float | None = None
    is_active: bool | None = None

    source: str | None = None
    queue_length: int | None = None
    estimated_waiting_time: float | None = None


class StationResponse(BaseModel):
    """Station data returned by the API, including its actual owner name."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    owner_id: int | None = None
    owner_username: str | None = None

    name: str
    source: str
    address: str
    city: str
    state: str

    latitude: float | None = None
    longitude: float | None = None

    total_dispensers: int
    active_dispensers: int
    average_fueling_time: int
    average_waiting_time: float

    cng_price: float | None = None
    is_active: bool
    queue_length: int
    estimated_waiting_time: float

    last_updated: datetime | None = None
    created_at: datetime
    updated_at: datetime
