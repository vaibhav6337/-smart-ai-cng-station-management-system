from __future__ import annotations

from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class Camera(Base):
    __tablename__ = "cameras"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    station_id: Mapped[int] = mapped_column(
        ForeignKey("stations.id", ondelete="CASCADE"),
        nullable=False
    )

    camera_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    camera_type: Mapped[str] = mapped_column(
        String(30),
        default="IP"
    )

    camera_url: Mapped[str] = mapped_column(
        String(500),
        nullable=False
    )

    camera_position: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    resolution: Mapped[str] = mapped_column(
        String(20),
        default="1920x1080"
    )

    fps: Mapped[int] = mapped_column(
        Integer,
        default=30
    )

    status: Mapped[str] = mapped_column(
        String(20),
        default="OFFLINE"
    )

    is_recording: Mapped[bool] = mapped_column(
        Boolean,
        default=False
    )

    last_seen: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    station: Mapped["Station"] = relationship(
        back_populates="cameras"
    )
    
    vehicle_logs: Mapped[list["VehicleLog"]] = relationship(
    back_populates="camera",
    cascade="all, delete-orphan"
    )