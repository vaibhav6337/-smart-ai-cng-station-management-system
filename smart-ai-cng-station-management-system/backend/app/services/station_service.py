from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.station import Station
from app.schemas.station import StationCreate, StationUpdate


def create_station(db: Session, station: StationCreate):
    """Create a new station"""

    db_station = Station(**station.model_dump())

    db.add(db_station)
    db.commit()
    db.refresh(db_station)

    return db_station


def get_all_stations(db: Session):
    """Get all stations"""

    return db.query(Station).all()


def get_station(db: Session, station_id: int):
    """Get a station by ID"""

    station = db.query(Station).filter(Station.id == station_id).first()

    if station is None:
        raise HTTPException(
            status_code=404,
            detail="Station not found"
        )

    return station


def update_station(
    db: Session,
    station_id: int,
    station_data: StationUpdate
):
    """Update an existing station"""

    station = db.query(Station).filter(Station.id == station_id).first()

    if station is None:
        raise HTTPException(
            status_code=404,
            detail="Station not found"
        )

    update_data = station_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(station, field, value)

    db.commit()
    db.refresh(station)

    return station


def delete_station(db: Session, station_id: int):
    """Delete a station"""

    station = db.query(Station).filter(Station.id == station_id).first()

    if station is None:
        raise HTTPException(
            status_code=404,
            detail="Station not found"
        )

    db.delete(station)
    db.commit()

    return {
        "success": True,
        "message": "Station deleted successfully"
    }