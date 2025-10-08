import logging
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.crud import address as crud
from app.db.database import get_db
from app.models.address import AddressResponse, AddressCreate, AddressUpdate, AddressWithDistance, LocationQuery

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post(
    "/addresses",
    response_model=AddressResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_address(
        address: AddressCreate,
        db: Session = Depends(get_db)
):
    try:
        return crud.create_address(db=db, address=address)
    except Exception as e:
        logger.error(f"Error creating address: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create address"
        )


@router.get(
    "/addresses",
    response_model=List[AddressResponse]
)
async def get_addresses(
        skip: int = Query(0, ge=0, description="Number of records to skip"),
        limit: int = Query(100, ge=1, le=1000, description="Maximum records to return"),
        db: Session = Depends(get_db)
):
    try:
        addresses = crud.get_addresses(db=db, skip=skip, limit=limit)
        return addresses
    except Exception as e:
        logger.error(f"Error fetching addresses: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch addresses"
        )


@router.get(
    "/addresses/{address_id}",
    response_model=AddressResponse
)
async def get_address(
        address_id: int,
        db: Session = Depends(get_db)
):
    db_address = crud.get_address(db=db, address_id=address_id)
    if db_address is None:
        logger.warning(f"Address with ID {address_id} not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Address with ID {address_id} not found"
        )
    return db_address


@router.put(
    "/addresses/{address_id}",
    response_model=AddressResponse
)
async def update_address(
        address_id: int,
        address_update: AddressUpdate,
        db: Session = Depends(get_db)
):
    db_address = crud.update_address(
        db=db,
        address_id=address_id,
        address_update=address_update
    )
    if db_address is None:
        logger.warning(f"Address with ID {address_id} not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Address with ID {address_id} not found"
        )
    return db_address


@router.delete(
    "/addresses/{address_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_address(
        address_id: int,
        db: Session = Depends(get_db)
):
    success = crud.delete_address(db=db, address_id=address_id)
    if not success:
        logger.warning(f"Address with ID {address_id} not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Address with ID {address_id} not found"
        )
    return None


@router.post(
    "/addresses/nearby",
    response_model=List[AddressWithDistance]
)
async def get_nearby_addresses(
        location: LocationQuery,
        db: Session = Depends(get_db)
):
    try:
        addresses = crud.get_addresses_within_radius(
            db=db,
            latitude=location.latitude,
            longitude=location.longitude,
            radius_km=location.radius_km
        )

        addresses_with_distance = []
        for address in addresses:
            distance = crud.calculate_distance(
                location.latitude,
                location.longitude,
                address.latitude,
                address.longitude
            )
            address_dict = {
                **address.__dict__,
                "distance_km": round(distance, 2)
            }
            addresses_with_distance.append(address_dict)

        addresses_with_distance.sort(key=lambda x: x["distance_km"])

        return addresses_with_distance
    except Exception as e:
        logger.error(f"Error finding nearby addresses: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to find nearby addresses"
        )