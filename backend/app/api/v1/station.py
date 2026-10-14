from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
# import StationUpdate
from fastapi import APIRouter, Depends, status
from app.database.dependencies import get_db
from app.schemas.station import StationCreate, StationResponse
from app.services import station_service

router = APIRouter(
    prefix="/stations",
    tags=["Stations"]
)


#######################
from app.schemas.station import (
    StationCreate,
    StationUpdate,
    StationResponse
)
#####################

@router.post(
    "/",
    response_model=StationResponse,
    status_code=status.HTTP_201_CREATED
)
def create_station(
    station: StationCreate,
    db: Session = Depends(get_db)
):
    return station_service.create_station(db, station)



@router.get("/", response_model=list[StationResponse])
def get_stations(
    db: Session = Depends(get_db)
):
    return station_service.get_all_stations(db)


@router.get("/{station_id}", response_model=StationResponse)
def get_station(
    station_id: int,
    db: Session = Depends(get_db)
):
    return station_service.get_station(db, station_id)


@router.put("/{station_id}", response_model=StationResponse)
def update_station(
    station_id: int,
    station: StationUpdate,
    db: Session = Depends(get_db)
):
    return station_service.update_station(
        db,
        station_id,
        station
    )


    
@router.delete(
    "/{station_id}",
    status_code=status.HTTP_200_OK
)
def delete_station(
    station_id: int,
    db: Session = Depends(get_db)
):
    return station_service.delete_station(db, station_id)