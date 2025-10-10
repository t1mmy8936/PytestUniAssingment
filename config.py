# config.py
# Lightweight environment-aware configuration for the Flask app and tests.
import os
from dataclasses import dataclass
from typing import Type
try:
    # Load variables from a .env file when running locally (no-op in CI unless provided)
    from dotenv import load_dotenv  # type: ignore
    load_dotenv()
except Exception:
    pass

@dataclass
class BaseConfig:
    TESTING: bool = False
    DEBUG: bool = False
    APP_ENV: str = os.getenv("APP_ENV", "staging")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "unsafe_dev_default")
    DISABLE_EMAILS: bool = os.getenv("DISABLE_EMAILS", "true").lower() in ("1", "true", "yes")

@dataclass
class StagingConfig(BaseConfig):
    DEBUG: bool = True

@dataclass
class ProductionConfig(BaseConfig):
    DEBUG: bool = False

def get_config() -> Type[BaseConfig]:
    env = os.getenv("APP_ENV", "staging").lower()
    if env == "production":
        return ProductionConfig
    return StagingConfig
