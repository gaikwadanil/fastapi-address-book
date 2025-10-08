from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class AddressBase(BaseModel):

    street: str = Field(..., min_length=1, max_length=255, description="Street address")
    city: str = Field(..., min_length=1, max_length=100, description="City name")
    state: Optional[str] = Field(None, max_length=100, description="State or province")
    country: str = Field(..., min_length=1, max_length=100, description="Country name")
    postal_code: Optional[str] = Field(None, max_length=20, description="Postal or ZIP code")
    latitude: float = Field(..., ge=-90, le=90, description="Latitude coordinate (-90 to 90)")
    longitude: float = Field(..., ge=-180, le=180, description="Longitude coordinate (-180 to 180)")

    @field_validator('street', 'city', 'country')
    @classmethod
    def validate_not_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Field cannot be empty or whitespace")
        return v.strip()

    @field_validator('state', 'postal_code')
    @classmethod
    def validate_optional_fields(cls, v: Optional[str]) -> Optional[str]:
        if v:
            return v.strip()
        return v


class AddressCreate(AddressBase):
    pass


class AddressUpdate(BaseModel):

    street: Optional[str] = Field(None, min_length=1, max_length=255)
    city: Optional[str] = Field(None, min_length=1, max_length=100)
    state: Optional[str] = Field(None, max_length=100)
    country: Optional[str] = Field(None, min_length=1, max_length=100)
    postal_code: Optional[str] = Field(None, max_length=20)
    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)

    @field_validator('street', 'city', 'country')
    @classmethod
    def validate_not_empty(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and (not v or not v.strip()):
            raise ValueError("Field cannot be empty or whitespace")
        return v.strip() if v else v


class AddressResponse(AddressBase):

    id: int = Field(..., description="Unique address identifier")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    class Config:
        from_attributes = True


class AddressWithDistance(AddressResponse):

    distance_km: float = Field(..., description="Distance in kilometers from reference point")


class LocationQuery(BaseModel):

    latitude: float = Field(..., ge=-90, le=90, description="Reference latitude")
    longitude: float = Field(..., ge=-180, le=180, description="Reference longitude")
    radius_km: float = Field(..., gt=0, description="Search radius in kilometers")