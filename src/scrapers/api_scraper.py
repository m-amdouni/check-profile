"""API-based LinkedIn scraper using Proxycurl"""
import requests
from typing import List, Optional
from ..database.models import LinkedInProfile
from ..utils.config import Config
from ..utils.rate_limiter import RateLimiter
from ..utils.logger import setup_logger

logger = setup_logger(__name__)


class ProxycurlScraper:
    """Scraper using Proxycurl API for LinkedIn data"""

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Proxycurl scraper

        Args:
            api_key: Proxycurl API key (defaults to config)
        """
        self.api_key = api_key or Config.PROXYCURL_API_KEY
        self.base_url = Config.PROXYCURL_BASE_URL
        self.rate_limiter = RateLimiter(
            max_requests=Config.REQUESTS_PER_MINUTE,
            time_window=60
        )

        if not self.api_key:
            raise ValueError("Proxycurl API key is required")

        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def search_profiles_by_school(
        self,
        school_name: str,
        max_results: int = 50
    ) -> List[str]:
        """
        Search for LinkedIn profiles by school name

        Args:
            school_name: Name of the school/university
            max_results: Maximum number of profile URLs to return

        Returns:
            List of LinkedIn profile URLs
        """
        logger.info(f"Searching profiles from {school_name}...")

        # Apply rate limiting
        self.rate_limiter.wait_if_needed()

        endpoint = f"{self.base_url}/search/person/"

        params = {
            "country": "us",
            "education_school_name": school_name,
            "page_size": min(max_results, 100),
            "enrich_profiles": "skip"
        }

        try:
            response = requests.get(
                endpoint,
                headers=self.headers,
                params=params,
                timeout=30
            )
            response.raise_for_status()

            data = response.json()
            profile_urls = []

            if "results" in data:
                for result in data["results"][:max_results]:
                    if "linkedin_profile_url" in result:
                        profile_urls.append(result["linkedin_profile_url"])

            logger.info(f"Found {len(profile_urls)} profiles")
            return profile_urls

        except requests.exceptions.RequestException as e:
            logger.error(f"Error searching profiles: {e}")
            return []

    def get_profile_details(self, profile_url: str) -> Optional[LinkedInProfile]:
        """
        Get detailed profile information

        Args:
            profile_url: LinkedIn profile URL

        Returns:
            LinkedInProfile object or None if error
        """
        logger.info(f"Fetching profile: {profile_url}")

        # Apply rate limiting
        self.rate_limiter.wait_if_needed()

        endpoint = f"{self.base_url}/linkedin"

        params = {
            "url": profile_url,
            "use_cache": "if-present"
        }

        try:
            response = requests.get(
                endpoint,
                headers=self.headers,
                params=params,
                timeout=30
            )
            response.raise_for_status()

            data = response.json()
            return self._parse_profile(data, profile_url)

        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching profile {profile_url}: {e}")
            return None

    def _parse_profile(
        self,
        data: dict,
        profile_url: str
    ) -> Optional[LinkedInProfile]:
        """Parse Proxycurl API response into LinkedInProfile"""
        try:
            # Extract profile ID from URL
            profile_id = profile_url.rstrip("/").split("/")[-1]

            # Get current position
            current_company = None
            current_position = None
            if data.get("experiences") and len(data["experiences"]) > 0:
                current_exp = data["experiences"][0]
                if not current_exp.get("ends_at"):  # Still current
                    current_company = current_exp.get("company")
                    current_position = current_exp.get("title")

            # Get education info
            school = None
            degree = None
            field_of_study = None
            graduation_year = None

            if data.get("education") and len(data["education"]) > 0:
                # Get most recent or most relevant education
                for edu in data["education"]:
                    school = edu.get("school")
                    degree = edu.get("degree_name")
                    field_of_study = edu.get("field_of_study")
                    ends_at = edu.get("ends_at")
                    if ends_at and "year" in ends_at:
                        graduation_year = str(ends_at["year"])
                    break

            # Check if open to work
            is_open_to_work = False
            if "extra" in data and data["extra"]:
                is_open_to_work = data["extra"].get("open_to_work", False)

            profile = LinkedInProfile(
                profile_id=profile_id,
                name=data.get("full_name", "Unknown"),
                headline=data.get("headline"),
                school=school,
                degree=degree,
                field_of_study=field_of_study,
                graduation_year=graduation_year,
                current_company=current_company,
                current_position=current_position,
                is_open_to_work=is_open_to_work,
                location=data.get("city") or data.get("country"),
                profile_url=profile_url,
                about=data.get("summary"),
                connections=data.get("connections")
            )

            return profile

        except Exception as e:
            logger.error(f"Error parsing profile data: {e}")
            return None

    def scrape_school_alumni(
        self,
        school_name: str,
        max_profiles: int = 50,
        job_status_filter: Optional[str] = None
    ) -> List[LinkedInProfile]:
        """
        Scrape alumni profiles from a school

        Args:
            school_name: School/university name
            max_profiles: Maximum number of profiles to scrape
            job_status_filter: Filter by job status ('seeking', 'employed', None)

        Returns:
            List of LinkedInProfile objects
        """
        logger.info(f"Starting scrape for {school_name} alumni...")

        # Search for profiles
        profile_urls = self.search_profiles_by_school(school_name, max_profiles)

        if not profile_urls:
            logger.warning("No profiles found")
            return []

        # Fetch detailed information for each profile
        profiles = []
        for url in profile_urls[:max_profiles]:
            profile = self.get_profile_details(url)

            if profile:
                # Apply job status filter if specified
                if job_status_filter:
                    if job_status_filter == "seeking" and not profile.is_open_to_work:
                        continue
                    elif job_status_filter == "employed" and not profile.is_employed:
                        continue

                profiles.append(profile)
                logger.info(
                    f"✓ {profile.name} - {profile.job_status} "
                    f"({len(profiles)}/{max_profiles})"
                )

            if len(profiles) >= max_profiles:
                break

        logger.info(f"Scraping completed. Found {len(profiles)} profiles.")
        return profiles
