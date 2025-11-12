"""Data models for LinkedIn profiles"""
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Optional


@dataclass
class LinkedInProfile:
    """LinkedIn profile data model"""

    profile_id: str
    name: str
    headline: Optional[str] = None
    school: Optional[str] = None
    degree: Optional[str] = None
    field_of_study: Optional[str] = None
    graduation_year: Optional[str] = None
    current_company: Optional[str] = None
    current_position: Optional[str] = None
    is_open_to_work: bool = False
    location: Optional[str] = None
    profile_url: Optional[str] = None
    about: Optional[str] = None
    connections: Optional[int] = None
    scraped_at: Optional[str] = None

    def __post_init__(self):
        """Set scraped_at timestamp if not provided"""
        if self.scraped_at is None:
            self.scraped_at = datetime.utcnow().isoformat()

    def to_dict(self) -> dict:
        """Convert profile to dictionary"""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "LinkedInProfile":
        """Create profile from dictionary"""
        return cls(**data)

    @property
    def is_employed(self) -> bool:
        """Check if profile is currently employed"""
        return bool(self.current_company and self.current_position)

    @property
    def job_status(self) -> str:
        """Get job status string"""
        if self.is_open_to_work:
            return "seeking"
        elif self.is_employed:
            return "employed"
        else:
            return "unknown"
