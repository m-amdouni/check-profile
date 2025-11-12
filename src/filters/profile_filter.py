"""Profile filtering utilities"""
from typing import List, Optional
from ..database.models import LinkedInProfile


class ProfileFilter:
    """Filter and analyze LinkedIn profiles"""

    @staticmethod
    def filter_by_school(
        profiles: List[LinkedInProfile],
        school_name: str,
        exact_match: bool = False
    ) -> List[LinkedInProfile]:
        """
        Filter profiles by school name

        Args:
            profiles: List of profiles to filter
            school_name: School name to match
            exact_match: If True, require exact match; otherwise partial match

        Returns:
            Filtered list of profiles
        """
        if exact_match:
            return [
                p for p in profiles
                if p.school and p.school.lower() == school_name.lower()
            ]
        else:
            return [
                p for p in profiles
                if p.school and school_name.lower() in p.school.lower()
            ]

    @staticmethod
    def filter_by_job_status(
        profiles: List[LinkedInProfile],
        status: str
    ) -> List[LinkedInProfile]:
        """
        Filter profiles by job status

        Args:
            profiles: List of profiles to filter
            status: Job status ('seeking', 'employed', 'unknown')

        Returns:
            Filtered list of profiles
        """
        if status == "seeking":
            return [p for p in profiles if p.is_open_to_work]
        elif status == "employed":
            return [p for p in profiles if p.is_employed and not p.is_open_to_work]
        elif status == "unknown":
            return [p for p in profiles if not p.is_employed and not p.is_open_to_work]
        else:
            return profiles

    @staticmethod
    def filter_by_location(
        profiles: List[LinkedInProfile],
        location: str
    ) -> List[LinkedInProfile]:
        """
        Filter profiles by location

        Args:
            profiles: List of profiles to filter
            location: Location string to match

        Returns:
            Filtered list of profiles
        """
        return [
            p for p in profiles
            if p.location and location.lower() in p.location.lower()
        ]

    @staticmethod
    def filter_by_degree(
        profiles: List[LinkedInProfile],
        degree: str
    ) -> List[LinkedInProfile]:
        """
        Filter profiles by degree

        Args:
            profiles: List of profiles to filter
            degree: Degree string to match (e.g., 'Bachelor', 'Master', 'PhD')

        Returns:
            Filtered list of profiles
        """
        return [
            p for p in profiles
            if p.degree and degree.lower() in p.degree.lower()
        ]

    @staticmethod
    def get_statistics(profiles: List[LinkedInProfile]) -> dict:
        """
        Get statistics about profiles

        Args:
            profiles: List of profiles to analyze

        Returns:
            Dictionary with statistics
        """
        if not profiles:
            return {
                "total": 0,
                "seeking": 0,
                "employed": 0,
                "unknown": 0
            }

        seeking = sum(1 for p in profiles if p.is_open_to_work)
        employed = sum(
            1 for p in profiles
            if p.is_employed and not p.is_open_to_work
        )
        unknown = len(profiles) - seeking - employed

        # School distribution
        schools = {}
        for p in profiles:
            if p.school:
                schools[p.school] = schools.get(p.school, 0) + 1

        # Location distribution
        locations = {}
        for p in profiles:
            if p.location:
                locations[p.location] = locations.get(p.location, 0) + 1

        # Company distribution (for employed)
        companies = {}
        for p in profiles:
            if p.current_company:
                companies[p.current_company] = companies.get(p.current_company, 0) + 1

        return {
            "total": len(profiles),
            "seeking": seeking,
            "employed": employed,
            "unknown": unknown,
            "seeking_percentage": round(seeking / len(profiles) * 100, 1),
            "employed_percentage": round(employed / len(profiles) * 100, 1),
            "top_schools": sorted(
                schools.items(),
                key=lambda x: x[1],
                reverse=True
            )[:5],
            "top_locations": sorted(
                locations.items(),
                key=lambda x: x[1],
                reverse=True
            )[:5],
            "top_companies": sorted(
                companies.items(),
                key=lambda x: x[1],
                reverse=True
            )[:5]
        }
