"""Export utilities for profile data"""
import json
import csv
from pathlib import Path
from typing import List
from ..database.models import LinkedInProfile


class ProfileExporter:
    """Export profile data to various formats"""

    @staticmethod
    def to_csv(profiles: List[LinkedInProfile], output_path: str) -> bool:
        """
        Export profiles to CSV

        Args:
            profiles: List of profiles to export
            output_path: Output file path

        Returns:
            True if successful, False otherwise
        """
        try:
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)

            with open(output_path, "w", newline="", encoding="utf-8") as f:
                if not profiles:
                    return True

                writer = csv.DictWriter(f, fieldnames=profiles[0].to_dict().keys())
                writer.writeheader()

                for profile in profiles:
                    writer.writerow(profile.to_dict())

            return True

        except Exception as e:
            print(f"Error exporting to CSV: {e}")
            return False

    @staticmethod
    def to_json(profiles: List[LinkedInProfile], output_path: str) -> bool:
        """
        Export profiles to JSON

        Args:
            profiles: List of profiles to export
            output_path: Output file path

        Returns:
            True if successful, False otherwise
        """
        try:
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)

            data = [profile.to_dict() for profile in profiles]

            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            return True

        except Exception as e:
            print(f"Error exporting to JSON: {e}")
            return False

    @staticmethod
    def to_markdown(profiles: List[LinkedInProfile], output_path: str) -> bool:
        """
        Export profiles to Markdown

        Args:
            profiles: List of profiles to export
            output_path: Output file path

        Returns:
            True if successful, False otherwise
        """
        try:
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)

            with open(output_path, "w", encoding="utf-8") as f:
                f.write("# LinkedIn Profiles\n\n")

                for profile in profiles:
                    f.write(f"## {profile.name}\n\n")
                    f.write(f"- **Headline**: {profile.headline or 'N/A'}\n")
                    f.write(f"- **School**: {profile.school or 'N/A'}\n")
                    f.write(f"- **Degree**: {profile.degree or 'N/A'}\n")

                    if profile.current_company:
                        f.write(f"- **Current Company**: {profile.current_company}\n")
                    if profile.current_position:
                        f.write(f"- **Current Position**: {profile.current_position}\n")

                    f.write(f"- **Job Status**: {profile.job_status}\n")
                    f.write(f"- **Location**: {profile.location or 'N/A'}\n")

                    if profile.profile_url:
                        f.write(f"- **Profile**: [{profile.profile_url}]({profile.profile_url})\n")

                    f.write("\n---\n\n")

            return True

        except Exception as e:
            print(f"Error exporting to Markdown: {e}")
            return False
