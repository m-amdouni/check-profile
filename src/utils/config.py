"""Configuration management for LinkedIn scraper"""
import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Configuration class for scraper settings"""

    # API Configuration (for API-based scraping - currently unavailable)
    PROXYCURL_API_KEY: Optional[str] = os.getenv("PROXYCURL_API_KEY")
    PROXYCURL_BASE_URL: str = "https://nubela.co/proxycurl/api/v2"

    # Web Scraper Configuration (for academic use only)
    LINKEDIN_EMAIL: Optional[str] = os.getenv("LINKEDIN_EMAIL")
    LINKEDIN_PASSWORD: Optional[str] = os.getenv("LINKEDIN_PASSWORD")
    SCRAPER_TYPE: str = os.getenv("SCRAPER_TYPE", "web")  # "api" or "web"
    HEADLESS_BROWSER: bool = os.getenv("HEADLESS_BROWSER", "true").lower() == "true"

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
    def validate(cls) -> list[str]:
        """Validate configuration and return list of errors"""
        errors = []

        # Check scraper type configuration
        if cls.SCRAPER_TYPE == "api":
            if not cls.PROXYCURL_API_KEY:
                errors.append(
                    "PROXYCURL_API_KEY is required for API-based scraping. "
                    "Note: Proxycurl API key registration has been unavailable since 2025. "
                    "Consider using SCRAPER_TYPE=web for academic purposes."
                )
        elif cls.SCRAPER_TYPE == "web":
            if not cls.LINKEDIN_EMAIL or not cls.LINKEDIN_PASSWORD:
                errors.append(
                    "LINKEDIN_EMAIL and LINKEDIN_PASSWORD are required for web scraping. "
                    "⚠️ WARNING: Web scraping is for ACADEMIC USE ONLY and may violate LinkedIn ToS."
                )

        if not cls.TARGET_SCHOOL:
            errors.append("TARGET_SCHOOL is required")

        return errors

    @classmethod
    def ensure_directories(cls):
        """Ensure all required directories exist"""
        Path(cls.DATABASE_PATH).parent.mkdir(parents=True, exist_ok=True)
        Path(cls.EXPORT_PATH).mkdir(parents=True, exist_ok=True)
        Path(cls.LOG_FILE).parent.mkdir(parents=True, exist_ok=True)
