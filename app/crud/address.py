import logging
from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.address import AddressCreate, AddressUpdate
from app.schemas.address import Address

logger = logging.getLogger(__name__)


def create_address(db: Session, address: AddressCreate) -> Address:
    """
    Create a new address in the database.

    Args:
        db: Database session
        address: Address data to create

    Returns:
        Created Address object
    """
    logger.info(f"Creating new address in {address.city}, {address.country}")

    db_address = Address(**address.model_dump())
    db.add(db_address)
    db.commit()
    db.refresh(db_address)

    logger.info(f"Address created successfully with ID: {db_address.id}")
    return db_address


def get_address(db: Session, address_id: int) -> Optional[Address]:
    """
    Retrieve a single address by ID.

    Args:
        db: Database session
        address_id: ID of the address to retrieve

    Returns:
        Address object if found, None otherwise
    """
    logger.debug(f"Fetching address with ID: {address_id}")
    return db.query(Address).filter(Address.id == address_id).first()


def get_addresses(db: Session, skip: int = 0, limit: int = 100) -> List[Address]:
    """
    Retrieve multiple addresses with pagination.

    Args:
        db: Database session
        skip: Number of records to skip (for pagination)
        limit: Maximum number of records to return

    Returns:
        List of Address objects
    """
    logger.debug(f"Fetching addresses with skip={skip}, limit={limit}")
    return db.query(Address).offset(skip).limit(limit).all()


def update_address(
        db: Session,
        address_id: int,
        address_update: AddressUpdate
) -> Optional[Address]:
    """
    Update an existing address.

    Args:
        db: Database session
        address_id: ID of the address to update
        address_update: Fields to update

    Returns:
        Updated Address object if found, None otherwise
    """
    logger.info(f"Updating address with ID: {address_id}")

    db_address = get_address(db, address_id)
    if not db_address:
        logger.warning(f"Address with ID {address_id} not found")
        return None

    update_data = address_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_address, field, value)

    db.commit()
    db.refresh(db_address)

    logger.info(f"Address {address_id} updated successfully")
    return db_address


def delete_address(db: Session, address_id: int) -> bool:
    """
    Delete an address from the database.

    Args:
        db: Database session
        address_id: ID of the address to delete

    Returns:
        True if address was deleted, False if not found
    """
    logger.info(f"Deleting address with ID: {address_id}")

    db_address = get_address(db, address_id)
    if not db_address:
        logger.warning(f"Address with ID {address_id} not found")
        return False

    db.delete(db_address)
    db.commit()

    logger.info(f"Address {address_id} deleted successfully")
    return True


def get_addresses_within_radius(
        db: Session,
        latitude: float,
        longitude: float,
        radius_km: float
) -> List[Address]:
    """
    Retrieve all addresses within a given radius from a location.
    Uses the Haversine formula for distance calculation.

    Args:
        db: Database session
        latitude: Reference latitude
        longitude: Reference longitude
        radius_km: Search radius in kilometers

    Returns:
        List of Address objects within the radius
    """
    logger.info(
        f"Searching addresses within {radius_km}km of "
        f"coordinates ({latitude}, {longitude})"
    )

    all_addresses = db.query(Address).all()

    nearby_addresses = []
    for address in all_addresses:
        distance = calculate_distance(
            latitude, longitude,
            address.latitude, address.longitude
        )
        if distance <= radius_km:
            nearby_addresses.append(address)

    logger.info(f"Found {len(nearby_addresses)} addresses within radius")
    return nearby_addresses


def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate the great circle distance between two points on Earth.
    Uses the Haversine formula.

    Args:
        lat1: Latitude of first point
        lon1: Longitude of first point
        lat2: Latitude of second point
        lon2: Longitude of second point

    Returns:
        Distance in kilometers
    """
    from math import radians, sin, cos, sqrt, atan2
    from app.core.config import settings

    lat1_rad = radians(lat1)
    lon1_rad = radians(lon1)
    lat2_rad = radians(lat2)
    lon2_rad = radians(lon2)

    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    a = sin(dlat / 2) ** 2 + cos(lat1_rad) * cos(lat2_rad) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = settings.EARTH_RADIUS_KM * c

    return distance