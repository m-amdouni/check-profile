#!/usr/bin/env python3
"""
Example script showing how to use the LinkedIn Profile Scraper programmatically
"""

from src.scrapers.api_scraper import ProxycurlScraper
from src.database.db_manager import DatabaseManager
from src.filters.profile_filter import ProfileFilter
from src.utils.export import ProfileExporter
from src.utils.config import Config

def example_basic_scrape():
    """Example: Basic scraping"""
    print("Example 1: Basic Scraping")
    print("-" * 50)

    # Initialize scraper
    scraper = ProxycurlScraper(api_key="your_api_key_here")

    # Scrape profiles
    profiles = scraper.scrape_school_alumni(
        school_name="Harvard University",
        max_profiles=10
    )

    print(f"Found {len(profiles)} profiles")
    for profile in profiles:
        print(f"  - {profile.name}: {profile.job_status}")

    return profiles


def example_filter_job_seekers():
    """Example: Filter for job seekers only"""
    print("\nExample 2: Finding Job Seekers")
    print("-" * 50)

    scraper = ProxycurlScraper(api_key="your_api_key_here")

    # Scrape only job seekers
    profiles = scraper.scrape_school_alumni(
        school_name="MIT",
        max_profiles=20,
        job_status_filter="seeking"
    )

    print(f"Found {len(profiles)} job seekers")
    for profile in profiles:
        if profile.is_open_to_work:
            print(f"  - {profile.name}")
            print(f"    Previous: {profile.headline or 'N/A'}")
            print(f"    Location: {profile.location or 'N/A'}")

    return profiles


def example_database_operations():
    """Example: Working with database"""
    print("\nExample 3: Database Operations")
    print("-" * 50)

    # Initialize database
    db = DatabaseManager("./data/profiles.db")

    # Save some profiles (assuming we have them)
    # profile = LinkedInProfile(...)
    # db.save_profile(profile)

    # Query profiles
    profiles = db.get_profiles_by_school("Stanford University")
    print(f"Found {len(profiles)} Stanford profiles in database")

    # Get statistics
    stats = db.get_statistics()
    print(f"\nDatabase stats:")
    print(f"  Total profiles: {stats['total_profiles']}")
    print(f"  Job seekers: {stats['job_seekers']}")
    print(f"  Employed: {stats['employed']}")

    return profiles


def example_export():
    """Example: Export profiles"""
    print("\nExample 4: Exporting Data")
    print("-" * 50)

    # Get profiles from database
    db = DatabaseManager("./data/profiles.db")
    profiles = db.get_all_profiles()

    if not profiles:
        print("No profiles to export")
        return

    # Export to different formats
    exporter = ProfileExporter()

    # CSV
    exporter.to_csv(profiles, "./exports/profiles.csv")
    print("✓ Exported to CSV")

    # JSON
    exporter.to_json(profiles, "./exports/profiles.json")
    print("✓ Exported to JSON")

    # Markdown
    exporter.to_markdown(profiles, "./exports/profiles.md")
    print("✓ Exported to Markdown")


def example_statistics():
    """Example: Analyze profiles"""
    print("\nExample 5: Statistics & Analysis")
    print("-" * 50)

    db = DatabaseManager("./data/profiles.db")
    profiles = db.get_profiles_by_school("Harvard")

    if not profiles:
        print("No profiles found")
        return

    # Get statistics
    stats = ProfileFilter.get_statistics(profiles)

    print(f"Total profiles: {stats['total']}")
    print(f"Job seekers: {stats['seeking']} ({stats['seeking_percentage']}%)")
    print(f"Employed: {stats['employed']} ({stats['employed_percentage']}%)")

    print("\nTop schools:")
    for school, count in stats['top_schools']:
        print(f"  {school}: {count}")

    print("\nTop companies:")
    for company, count in stats['top_companies']:
        print(f"  {company}: {count}")


def main():
    """Run all examples"""
    print("\n" + "=" * 60)
    print("LinkedIn Profile Scraper - Examples")
    print("=" * 60)

    # NOTE: Replace 'your_api_key_here' with actual API key
    # or set PROXYCURL_API_KEY in .env file

    # Example 1: Basic scraping
    # Uncomment to run (requires API key)
    # profiles = example_basic_scrape()

    # Example 2: Filter job seekers
    # Uncomment to run (requires API key)
    # profiles = example_filter_job_seekers()

    # Example 3: Database operations
    # example_database_operations()

    # Example 4: Export
    # example_export()

    # Example 5: Statistics
    # example_statistics()

    print("\n" + "=" * 60)
    print("To run these examples:")
    print("1. Set PROXYCURL_API_KEY in .env file")
    print("2. Uncomment the example you want to run")
    print("3. Run: python example.py")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
