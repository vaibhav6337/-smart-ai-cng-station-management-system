from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class VehicleLog(Base):
    __tablename__ = "vehicle_logs"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    camera_id: Mapped[int] = mapped_column(
        ForeignKey("cameras.id", ondelete="CASCADE"),
        nullable=False
    )

    vehicle_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    entry_time: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    exit_time: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )

    status: Mapped[str] = mapped_column(
        String(20),
        default="IN_QUEUE"
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

    camera: Mapped["Camera"] = relationship(
        back_populates="vehicle_logs"
    )