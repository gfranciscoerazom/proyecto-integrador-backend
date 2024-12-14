"""
This module defines the application's settings using Pydantic's BaseSettings

It centralizes configuration parameters, loading them from environment variables 
with the help of `pydantic-settings`. These settings are crucial for various 
aspects of the application, including:

- **Security:** Managing the secret key and algorithm for JWT token generation.
- **Database:** Specifying the database connection URL.
- **Token Management:** Defining the token expiration time.

The settings are made accessible throughout the application using FastAPI's 
dependency injection system via the `SettingsDependency` variable.

**Key Settings:**

- `SECRET_KEY`: A secret key used for signing JWT tokens. It should be a 
   strong, randomly generated string.
- `ALGORITHM`: The algorithm used for signing JWT tokens (e.g., HS256).
- `ACCESS_TOKEN_EXPIRE_MINUTES`: The duration (in minutes) for which access 
   tokens are valid.
- `DATABASE_URL`: The connection URL for the database, including the database 
   type, credentials, and database name.

This approach ensures that configuration is well-organized, type-safe, and 
easily accessible across the application.
"""

from functools import lru_cache
from pathlib import Path
from typing import Annotated, Final

from fastapi import Depends
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


# region classes
class Settings(BaseSettings):
    """
    Settings for the application.

    Settings for the application that are loaded from the environment variables.
    """
    SECRET_KEY: Final[str] = Field(
        title="Secret Key",
        description="Secret key for JWT token",
        examples=[
            "42f2029d884cb2707f9abd7ba591a060ed031d7e99dff1e86bc2f0de665f4b39",
            "b872cd1a34b3cb6122b18466dcd01cae48572b453e03116f79f1ecc276aadb2d",
        ],
        max_length=64,
        min_length=64,
    )
    ALGORITHM: Final[str] = Field(
        title="Algorithm",
        description="Algorithm for JWT token",
        examples=["HS256"],
    )
    ACCESS_TOKEN_EXPIRE_MINUTES: Final[int] = Field(
        title="Access Token Expire Minutes",
        description="Time duration after which the token will expire",
        examples=[30],

        ge=1,
    )
    DATABASE_URL: Final[str] = Field(
        title="Database URL",
        description="URL for the database",
        examples=[
            "sqlite:///this/is/an/example.db",
            "postgresql://user:password@localhost/db",
        ],
    )

    model_config = SettingsConfigDict(
        env_file=Path.cwd() / ".env",
        env_file_encoding='utf-8'
    )
# endregion


# region functions
@lru_cache
def get_settings() -> Settings:
    """
    Get the settings for the application. This function is cached.

    Returns:
        Settings: The settings for the application.
    """
    return Settings()  # type: ignore
# endregion


# region variables
settings: Settings = get_settings()

SettingsDependency = Annotated[Settings, Depends(get_settings)]
# endregion
