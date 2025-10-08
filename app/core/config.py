from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Address Book API"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "API for managing addresses with geolocation capabilities"

    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = True

    # Database
    DATABASE_URL: str = "sqlite:///./address_book.db"

    # Geolocation
    EARTH_RADIUS_KM: float = 6371.0

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()