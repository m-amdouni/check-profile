"""SQLite database manager for storing LinkedIn profiles"""
import sqlite3
from pathlib import Path
from typing import List, Optional
from contextlib import contextmanager

from .models import LinkedInProfile


class DatabaseManager:
    """Manages SQLite database operations for LinkedIn profiles"""

    def __init__(self, db_path: str = "./data/profiles.db"):
        """
        Initialize database manager

        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    @contextmanager
    def get_connection(self):
        """Context manager for database connections"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def _init_db(self):
        """Initialize database schema"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS profiles (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    profile_id TEXT UNIQUE NOT NULL,
                    name TEXT NOT NULL,
                    headline TEXT,
                    school TEXT,
                    degree TEXT,
                    field_of_study TEXT,
                    graduation_year TEXT,
                    current_company TEXT,
                    current_position TEXT,
                    is_open_to_work BOOLEAN DEFAULT 0,
                    location TEXT,
                    profile_url TEXT,
                    about TEXT,
                    connections INTEGER,
                    scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Create indexes for faster queries
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_school
                ON profiles(school)
            """)
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_job_status
                ON profiles(is_open_to_work, current_company)
            """)

    def save_profile(self, profile: LinkedInProfile) -> bool:
        """
        Save or update a profile

        Args:
            profile: LinkedInProfile instance

        Returns:
            True if saved successfully, False otherwise
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT OR REPLACE INTO profiles (
                        profile_id, name, headline, school, degree,
                        field_of_study, graduation_year, current_company,
                        current_position, is_open_to_work, location,
                        profile_url, about, connections, scraped_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    profile.profile_id,
                    profile.name,
                    profile.headline,
                    profile.school,
                    profile.degree,
                    profile.field_of_study,
                    profile.graduation_year,
                    profile.current_company,
                    profile.current_position,
                    profile.is_open_to_work,
                    profile.location,
                    profile.profile_url,
                    profile.about,
                    profile.connections,
                    profile.scraped_at
                ))
            return True
        except Exception as e:
            print(f"Error saving profile: {e}")
            return False

    def get_profile(self, profile_id: str) -> Optional[LinkedInProfile]:
        """
        Get a profile by ID

        Args:
            profile_id: LinkedIn profile ID

        Returns:
            LinkedInProfile if found, None otherwise
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM profiles WHERE profile_id = ?",
                (profile_id,)
            )
            row = cursor.fetchone()

            if row:
                return LinkedInProfile(
                    profile_id=row["profile_id"],
                    name=row["name"],
                    headline=row["headline"],
                    school=row["school"],
                    degree=row["degree"],
                    field_of_study=row["field_of_study"],
                    graduation_year=row["graduation_year"],
                    current_company=row["current_company"],
                    current_position=row["current_position"],
                    is_open_to_work=bool(row["is_open_to_work"]),
                    location=row["location"],
                    profile_url=row["profile_url"],
                    about=row["about"],
                    connections=row["connections"],
                    scraped_at=row["scraped_at"]
                )
            return None

    def get_profiles_by_school(
        self,
        school: str,
        job_status: Optional[str] = None
    ) -> List[LinkedInProfile]:
        """
        Get profiles by school name

        Args:
            school: School name to filter by
            job_status: Optional job status filter ('seeking', 'employed', 'unknown')

        Returns:
            List of LinkedInProfile instances
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()

            query = "SELECT * FROM profiles WHERE school LIKE ?"
            params = [f"%{school}%"]

            if job_status == "seeking":
                query += " AND is_open_to_work = 1"
            elif job_status == "employed":
                query += " AND is_open_to_work = 0 AND current_company IS NOT NULL"
            elif job_status == "unknown":
                query += " AND is_open_to_work = 0 AND current_company IS NULL"

            cursor.execute(query, params)
            rows = cursor.fetchall()

            profiles = []
            for row in rows:
                profiles.append(LinkedInProfile(
                    profile_id=row["profile_id"],
                    name=row["name"],
                    headline=row["headline"],
                    school=row["school"],
                    degree=row["degree"],
                    field_of_study=row["field_of_study"],
                    graduation_year=row["graduation_year"],
                    current_company=row["current_company"],
                    current_position=row["current_position"],
                    is_open_to_work=bool(row["is_open_to_work"]),
                    location=row["location"],
                    profile_url=row["profile_url"],
                    about=row["about"],
                    connections=row["connections"],
                    scraped_at=row["scraped_at"]
                ))

            return profiles

    def get_all_profiles(self) -> List[LinkedInProfile]:
        """Get all profiles from database"""
        return self.get_profiles_by_school("")

    def delete_profile(self, profile_id: str) -> bool:
        """Delete a profile by ID"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "DELETE FROM profiles WHERE profile_id = ?",
                    (profile_id,)
                )
            return True
        except Exception as e:
            print(f"Error deleting profile: {e}")
            return False

    def get_statistics(self) -> dict:
        """Get database statistics"""
        with self.get_connection() as conn:
            cursor = conn.cursor()

            # Total profiles
            cursor.execute("SELECT COUNT(*) as total FROM profiles")
            total = cursor.fetchone()["total"]

            # Job seekers
            cursor.execute(
                "SELECT COUNT(*) as seeking FROM profiles WHERE is_open_to_work = 1"
            )
            seeking = cursor.fetchone()["seeking"]

            # Employed
            cursor.execute("""
                SELECT COUNT(*) as employed FROM profiles
                WHERE is_open_to_work = 0 AND current_company IS NOT NULL
            """)
            employed = cursor.fetchone()["employed"]

            # Schools distribution
            cursor.execute("""
                SELECT school, COUNT(*) as count
                FROM profiles
                WHERE school IS NOT NULL
                GROUP BY school
                ORDER BY count DESC
                LIMIT 10
            """)
            schools = cursor.fetchall()

            return {
                "total_profiles": total,
                "job_seekers": seeking,
                "employed": employed,
                "top_schools": [dict(row) for row in schools]
            }
