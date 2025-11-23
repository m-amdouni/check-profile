"""Import utilities for profile data from external sources"""
import json
import csv
from pathlib import Path
from typing import List, Optional
from ..database.models import LinkedInProfile


class ProfileImporter:
    """Import profile data from various formats"""

    @staticmethod
    def from_csv(input_path: str) -> List[LinkedInProfile]:
        """
        Import profiles from CSV file

        Args:
            input_path: Path to CSV file

        Returns:
            List of LinkedInProfile objects
        """
        try:
            profiles = []

            with open(input_path, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)

                for row in reader:
                    # Convert string 'True'/'False' to boolean
                    is_open_to_work = row.get("is_open_to_work", "False")
                    if isinstance(is_open_to_work, str):
                        is_open_to_work = is_open_to_work.lower() in ["true", "1", "yes"]

                    # Convert connections to int if present
                    connections = row.get("connections")
                    if connections and connections.strip():
                        try:
                            connections = int(connections)
                        except ValueError:
                            connections = None
                    else:
                        connections = None

                    profile = LinkedInProfile(
                        profile_id=row.get("profile_id", ""),
                        name=row.get("name", "Unknown"),
                        headline=row.get("headline") or None,
                        school=row.get("school") or None,
                        degree=row.get("degree") or None,
                        field_of_study=row.get("field_of_study") or None,
                        graduation_year=row.get("graduation_year") or None,
                        current_company=row.get("current_company") or None,
                        current_position=row.get("current_position") or None,
                        is_open_to_work=is_open_to_work,
                        location=row.get("location") or None,
                        profile_url=row.get("profile_url") or None,
                        about=row.get("about") or None,
                        connections=connections,
                        scraped_at=row.get("scraped_at") or None
                    )

                    profiles.append(profile)

            print(f"✅ Imported {len(profiles)} profiles from CSV")
            return profiles

        except FileNotFoundError:
            print(f"❌ Error: File not found: {input_path}")
            return []
        except Exception as e:
            print(f"❌ Error importing from CSV: {e}")
            import traceback
            traceback.print_exc()
            return []

    @staticmethod
    def from_json(input_path: str) -> List[LinkedInProfile]:
        """
        Import profiles from JSON file

        Args:
            input_path: Path to JSON file

        Returns:
            List of LinkedInProfile objects
        """
        try:
            with open(input_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            if not isinstance(data, list):
                print(f"❌ Error: JSON file must contain a list of profiles")
                return []

            profiles = []
            for item in data:
                try:
                    profile = LinkedInProfile.from_dict(item)
                    profiles.append(profile)
                except Exception as e:
                    print(f"⚠️  Warning: Skipping invalid profile: {e}")
                    continue

            print(f"✅ Imported {len(profiles)} profiles from JSON")
            return profiles

        except FileNotFoundError:
            print(f"❌ Error: File not found: {input_path}")
            return []
        except json.JSONDecodeError as e:
            print(f"❌ Error: Invalid JSON format: {e}")
            return []
        except Exception as e:
            print(f"❌ Error importing from JSON: {e}")
            import traceback
            traceback.print_exc()
            return []

    @staticmethod
    def import_to_database(profiles: List[LinkedInProfile], db_manager) -> int:
        """
        Import profiles directly to database

        Args:
            profiles: List of profiles to import
            db_manager: DatabaseManager instance

        Returns:
            Number of profiles successfully imported
        """
        count = 0
        for profile in profiles:
            if db_manager.save_profile(profile):
                count += 1

        return count
