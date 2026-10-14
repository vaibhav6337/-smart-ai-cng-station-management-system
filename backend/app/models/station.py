from __future__ import annotations

from datetime import datetime
from typing import List, TYPE_CHECKING

from sqlalchemy import (
    String,
    Integer,
    Float,
    Boolean,
    DateTime,
    ForeignKey,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.database.base import Base
from app.models.admin import Admin

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.camera import Camera
    from app.models.queue import Queue
    from app.models.alert import Alert
    from app.models.vehicle_log import VehicleLog


class Station(Base):
    __tablename__ = "stations"

    # -----------------------------------------
    # PRIMARY KEY
    # -----------------------------------------

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    # -----------------------------------------
    # OWNER / USER
    # -----------------------------------------

    owner_id: Mapped[int | None] = mapped_column(
        ForeignKey(
            "users.id",
            ondelete="CASCADE"
        ),
        nullable=True,
        index=True,
    )

    # -----------------------------------------
    # STATION INFORMATION
    # -----------------------------------------

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )
    source: Mapped[str] = mapped_column(
        String(20),
        default="managed",
        nullable=False
    )
    address: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    city: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    state: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    latitude: Mapped[float] = mapped_column(
        Float
    )

    longitude: Mapped[float] = mapped_column(
        Float
    )

    total_dispensers: Mapped[int] = mapped_column(
        Integer,
        default=1
    )

    active_dispensers: Mapped[int] = mapped_column(
        Integer,
        default=1
    )

    average_fueling_time: Mapped[int] = mapped_column(
        Integer,
        default=4
    )
    average_waiting_time: Mapped[float] = mapped_column(
        Float,
        default=0
    )

    cng_price: Mapped[float | None] = mapped_column(
        Float,
        nullable=True
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )

    # -----------------------------------------
    # LIVE QUEUE DATA
    # -----------------------------------------

    queue_length: Mapped[int] = mapped_column(
        Integer,
        default=0
    )

    estimated_waiting_time: Mapped[float] = mapped_column(
        Float,
        default=0
    )

    last_updated: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    # -----------------------------------------
    # TIMESTAMPS
    # -----------------------------------------

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    # -----------------------------------------
    # RELATIONSHIPS
    # -----------------------------------------

    # One station belongs to one user.
    # One user can have multiple stations.
    owner: Mapped["User | None"] = relationship(
        "User",
        back_populates="stations"
    )

    @property
    def owner_username(self) -> str | None:
        """Expose the linked owner's username without adding a DB column."""
        return self.owner.username if self.owner is not None else None

    # -----------------------------------------
    # CAMERAS
    # -----------------------------------------

    cameras: Mapped[List["Camera"]] = relationship(
        "Camera",
        back_populates="station",
        cascade="all, delete-orphan"
    )

    # -----------------------------------------
    # QUEUES
    # -----------------------------------------

    queues: Mapped[List["Queue"]] = relationship(
        "Queue",
        back_populates="station",
        cascade="all, delete-orphan"
    )

    # -----------------------------------------
    # ALERTS
    # -----------------------------------------

    alerts: Mapped[List["Alert"]] = relationship(
        "Alert",
        back_populates="station",
        cascade="all, delete-orphan"
    )

    # -----------------------------------------
    # VEHICLE LOGS
    # -----------------------------------------

    vehicle_logs: Mapped[List["VehicleLog"]] = relationship(
        "VehicleLog",
        back_populates="station",
        cascade="all, delete-orphan"
    )

    # -----------------------------------------
    # ADMINS
    # -----------------------------------------

    admins: Mapped[List["Admin"]] = relationship(
        "Admin",
        back_populates="station",
        cascade="all, delete-orphan"
    )
