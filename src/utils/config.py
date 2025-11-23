"""Configuration management for LinkedIn scraper"""
import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Configuration class for scraper settings"""

    # API Configuration
    PROXYCURL_API_KEY: Optional[str] = os.getenv("PROXYCURL_API_KEY")
    PROXYCURL_BASE_URL: str = "https://nubela.co/proxycurl/api/v2"

    # Search Configuration
    TARGET_SCHOOL: str = os.getenv("TARGET_SCHOOL", "")
    MAX_PROFILES: int = int(os.getenv("MAX_PROFILES", "50"))
    SEARCH_KEYWORDS: str = os.getenv("SEARCH_KEYWORDS", "")

    # Rate Limiting
    REQUESTS_PER_MINUTE: int = int(os.getenv("REQUESTS_PER_MINUTE", "10"))
    DELAY_BETWEEN_REQUESTS: int = int(os.getenv("DELAY_BETWEEN_REQUESTS", "6"))

    # Database
    DATABASE_PATH: str = os.getenv("DATABASE_PATH", "./data/profiles.db")

    # Export
    EXPORT_FORMAT: str = os.getenv("EXPORT_FORMAT", "csv")
    EXPORT_PATH: str = os.getenv("EXPORT_PATH", "./exports/")

    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE: str = os.getenv("LOG_FILE", "./logs/scraper.log")

    @classmethod
    def validate(cls, require_api: bool = False) -> list[str]:
        """
        Validate configuration and return list of errors

        Args:
            require_api: If True, validate API key is present.
                        If False, skip API validation (for offline mode)
        """
        errors = []

        # Only validate API key if explicitly required (for scraping)
        if require_api and not cls.PROXYCURL_API_KEY:
            errors.append("PROXYCURL_API_KEY is required for scraping")
            errors.append("Get your API key at: https://nubela.co/proxycurl/")
            errors.append("Or use demo mode: python demo_data.py")

        return errors

    @classmethod
    def has_api_key(cls) -> bool:
        """Check if API key is configured"""
        return bool(cls.PROXYCURL_API_KEY and cls.PROXYCURL_API_KEY.strip())

    @classmethod
    def ensure_directories(cls):
        """Ensure all required directories exist"""
        Path(cls.DATABASE_PATH).parent.mkdir(parents=True, exist_ok=True)
        Path(cls.EXPORT_PATH).mkdir(parents=True, exist_ok=True)
        Path(cls.LOG_FILE).parent.mkdir(parents=True, exist_ok=True)
