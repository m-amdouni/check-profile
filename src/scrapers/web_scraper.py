"""
Web-based LinkedIn scraper for academic and educational purposes only

⚠️ IMPORTANT DISCLAIMERS:
1. This is for ACADEMIC/EDUCATIONAL USE ONLY with small sample sizes
2. Web scraping may violate LinkedIn's Terms of Service
3. Use at your own risk and only for research purposes
4. Always respect rate limits and robots.txt
5. Consider the ethical implications of data collection
6. This should NOT be used for commercial purposes
7. Maximum 20 profiles per session recommended

For legal, production use, consider:
- LinkedIn Official API (limited but legal)
- RapidAPI alternatives when they become available
- Official partnerships with data providers
"""

import time
import random
from typing import List, Optional
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from ..database.models import LinkedInProfile
from ..utils.logger import setup_logger

logger = setup_logger(__name__)

# Academic use configuration
MAX_PROFILES_PER_SESSION = 20  # Limit to small samples for academic use
MIN_DELAY_BETWEEN_REQUESTS = 5  # Minimum seconds between requests
MAX_DELAY_BETWEEN_REQUESTS = 10  # Maximum seconds between requests


class LinkedInWebScraper:
    """
    Web scraper for LinkedIn profiles - ACADEMIC USE ONLY

    ⚠️ WARNING: This scraper is intended for academic research with small
    sample sizes only. Web scraping may violate LinkedIn's Terms of Service.
    """

    def __init__(self, email: str = None, password: str = None, headless: bool = True):
        """
        Initialize the web scraper

        Args:
            email: LinkedIn account email (required for authentication)
            password: LinkedIn account password (required for authentication)
            headless: Run browser in headless mode

        Note:
            You need a valid LinkedIn account to use this scraper.
            The account may be at risk of suspension.
        """
        if not email or not password:
            raise ValueError(
                "LinkedIn credentials required. Set LINKEDIN_EMAIL and "
                "LINKEDIN_PASSWORD in your .env file.\n"
                "⚠️ WARNING: Using this scraper may violate LinkedIn ToS "
                "and risk account suspension."
            )

        self.email = email
        self.password = password
        self.driver = None
        self.headless = headless
        self.profiles_scraped = 0

        logger.warning(
            "⚠️ Web scraping initialized. Use responsibly for academic purposes only."
        )

    def _setup_driver(self):
        """Setup Selenium WebDriver with appropriate options"""
        chrome_options = Options()

        if self.headless:
            chrome_options.add_argument("--headless")

        # Make the browser look more like a real user
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)

        # Set a realistic user agent
        chrome_options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )

        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.driver.execute_script(
            "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
        )

        logger.info("Chrome WebDriver initialized")

    def _login(self):
        """Login to LinkedIn"""
        if not self.driver:
            self._setup_driver()

        logger.info("Attempting to log in to LinkedIn...")

        try:
            self.driver.get("https://www.linkedin.com/login")
            time.sleep(random.uniform(2, 4))

            # Enter email
            email_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "username"))
            )
            email_field.send_keys(self.email)

            # Enter password
            password_field = self.driver.find_element(By.ID, "password")
            password_field.send_keys(self.password)

            # Click login button
            login_button = self.driver.find_element(
                By.CSS_SELECTOR, "button[type='submit']"
            )
            login_button.click()

            # Wait for login to complete
            time.sleep(random.uniform(3, 5))

            # Check if login was successful
            if "feed" in self.driver.current_url or "checkpoint" in self.driver.current_url:
                logger.info("✓ Login successful")

                if "checkpoint" in self.driver.current_url:
                    logger.warning(
                        "⚠️ LinkedIn security checkpoint detected. "
                        "You may need to verify your login manually."
                    )
                    input("Press Enter after completing the security check...")

                return True
            else:
                logger.error("✗ Login failed")
                return False

        except Exception as e:
            logger.error(f"Login error: {e}")
            return False

    def _respectful_delay(self):
        """Add a random delay between requests to be respectful"""
        delay = random.uniform(
            MIN_DELAY_BETWEEN_REQUESTS,
            MAX_DELAY_BETWEEN_REQUESTS
        )
        logger.debug(f"Waiting {delay:.1f} seconds before next request...")
        time.sleep(delay)

    def search_profiles_by_school(
        self,
        school_name: str,
        max_results: int = 10
    ) -> List[str]:
        """
        Search for LinkedIn profiles by school name

        Args:
            school_name: Name of the school/university
            max_results: Maximum number of profile URLs (max 20 for academic use)

        Returns:
            List of LinkedIn profile URLs
        """
        # Enforce academic use limits
        max_results = min(max_results, MAX_PROFILES_PER_SESSION)

        if max_results > 20:
            logger.warning(
                f"⚠️ Limiting to {MAX_PROFILES_PER_SESSION} profiles for "
                "academic use. Requested: {max_results}"
            )

        logger.info(f"Searching profiles from {school_name} (max: {max_results})...")

        if not self.driver:
            if not self._login():
                return []

        try:
            # Build search URL
            search_url = (
                f"https://www.linkedin.com/search/results/people/?"
                f"keywords={school_name.replace(' ', '%20')}"
                f"&origin=GLOBAL_SEARCH_HEADER"
            )

            self.driver.get(search_url)
            self._respectful_delay()

            # Scroll to load results
            profile_urls = []
            scroll_attempts = 0
            max_scrolls = 3  # Limit scrolling for academic use

            while len(profile_urls) < max_results and scroll_attempts < max_scrolls:
                # Find profile links
                links = self.driver.find_elements(
                    By.CSS_SELECTOR,
                    "a.app-aware-link[href*='/in/']"
                )

                for link in links:
                    href = link.get_attribute("href")
                    if href and "/in/" in href and href not in profile_urls:
                        # Clean URL
                        clean_url = href.split("?")[0]
                        profile_urls.append(clean_url)

                        if len(profile_urls) >= max_results:
                            break

                # Scroll down
                if len(profile_urls) < max_results:
                    self.driver.execute_script(
                        "window.scrollTo(0, document.body.scrollHeight);"
                    )
                    time.sleep(random.uniform(2, 3))
                    scroll_attempts += 1

            logger.info(f"Found {len(profile_urls)} profile URLs")
            return profile_urls[:max_results]

        except Exception as e:
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

        # Enforce session limits
        if self.profiles_scraped >= MAX_PROFILES_PER_SESSION:
            logger.warning(
                f"⚠️ Reached maximum profiles per session "
                f"({MAX_PROFILES_PER_SESSION}) for academic use"
            )
            return None

        self._respectful_delay()

        try:
            self.driver.get(profile_url)
            time.sleep(random.uniform(2, 4))

            # Extract profile ID from URL
            profile_id = profile_url.rstrip("/").split("/")[-1]

            # Extract name
            try:
                name_element = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, "h1.text-heading-xlarge")
                    )
                )
                name = name_element.text
            except:
                name = "Unknown"

            # Extract headline
            try:
                headline = self.driver.find_element(
                    By.CSS_SELECTOR,
                    "div.text-body-medium"
                ).text
            except:
                headline = None

            # Extract location
            try:
                location = self.driver.find_element(
                    By.CSS_SELECTOR,
                    "span.text-body-small.inline"
                ).text
            except:
                location = None

            # Check if open to work
            is_open_to_work = False
            try:
                self.driver.find_element(
                    By.XPATH,
                    "//*[contains(text(), 'Open to work')]"
                )
                is_open_to_work = True
            except:
                pass

            # Extract current company and position (from experience section)
            current_company = None
            current_position = None
            try:
                experience_section = self.driver.find_element(
                    By.ID, "experience"
                ).find_element(By.XPATH, "..")

                # Get first experience item
                first_exp = experience_section.find_element(
                    By.CSS_SELECTOR,
                    "li.artdeco-list__item"
                )

                current_position = first_exp.find_element(
                    By.CSS_SELECTOR,
                    "span[aria-hidden='true']"
                ).text

                current_company = first_exp.find_element(
                    By.CSS_SELECTOR,
                    "span.t-14.t-normal span[aria-hidden='true']"
                ).text
            except:
                pass

            # Extract education
            school = None
            degree = None
            field_of_study = None
            graduation_year = None

            try:
                education_section = self.driver.find_element(
                    By.ID, "education"
                ).find_element(By.XPATH, "..")

                # Get first education item
                first_edu = education_section.find_element(
                    By.CSS_SELECTOR,
                    "li.artdeco-list__item"
                )

                school = first_edu.find_element(
                    By.CSS_SELECTOR,
                    "span[aria-hidden='true']"
                ).text

                # Try to get degree info
                try:
                    degree_text = first_edu.find_element(
                        By.CSS_SELECTOR,
                        "span.t-14.t-normal span[aria-hidden='true']"
                    ).text
                    # Parse degree and field
                    if "," in degree_text:
                        degree, field_of_study = degree_text.split(",", 1)
                        degree = degree.strip()
                        field_of_study = field_of_study.strip()
                    else:
                        degree = degree_text
                except:
                    pass
            except:
                pass

            # Extract about section
            about = None
            try:
                about_section = self.driver.find_element(
                    By.ID, "about"
                ).find_element(By.XPATH, "..")
                about = about_section.find_element(
                    By.CSS_SELECTOR,
                    "span[aria-hidden='true']"
                ).text
            except:
                pass

            # Extract connections count
            connections = None
            try:
                connections_text = self.driver.find_element(
                    By.CSS_SELECTOR,
                    "span.t-bold"
                ).text
                if "connection" in connections_text.lower():
                    connections = int(connections_text.split()[0].replace(",", ""))
            except:
                pass

            profile = LinkedInProfile(
                profile_id=profile_id,
                name=name,
                headline=headline,
                school=school,
                degree=degree,
                field_of_study=field_of_study,
                graduation_year=graduation_year,
                current_company=current_company,
                current_position=current_position,
                is_open_to_work=is_open_to_work,
                location=location,
                profile_url=profile_url,
                about=about,
                connections=connections
            )

            self.profiles_scraped += 1
            logger.info(
                f"✓ {name} - {profile.job_status} "
                f"({self.profiles_scraped}/{MAX_PROFILES_PER_SESSION})"
            )

            return profile

        except Exception as e:
            logger.error(f"Error fetching profile {profile_url}: {e}")
            return None

    def scrape_school_alumni(
        self,
        school_name: str,
        max_profiles: int = 10,
        job_status_filter: Optional[str] = None
    ) -> List[LinkedInProfile]:
        """
        Scrape alumni profiles from a school - ACADEMIC USE ONLY

        Args:
            school_name: School/university name
            max_profiles: Maximum profiles (max 20 for academic use)
            job_status_filter: Filter by job status ('seeking', 'employed', None)

        Returns:
            List of LinkedInProfile objects
        """
        # Enforce academic use limits
        max_profiles = min(max_profiles, MAX_PROFILES_PER_SESSION)

        logger.warning(
            "⚠️ Starting web scraping session - ACADEMIC USE ONLY\n"
            f"   School: {school_name}\n"
            f"   Max profiles: {max_profiles}\n"
            "   Please use responsibly and respect LinkedIn's ToS"
        )

        # Login
        if not self.driver:
            if not self._login():
                logger.error("Login failed. Cannot proceed with scraping.")
                return []

        # Search for profiles
        profile_urls = self.search_profiles_by_school(school_name, max_profiles)

        if not profile_urls:
            logger.warning("No profiles found")
            return []

        # Fetch detailed information
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

            if len(profiles) >= max_profiles:
                break

        logger.info(
            f"Scraping completed. Collected {len(profiles)} profiles "
            "for academic research."
        )

        return profiles

    def close(self):
        """Close the browser"""
        if self.driver:
            self.driver.quit()
            logger.info("Browser closed")

    def __enter__(self):
        """Context manager entry"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()
