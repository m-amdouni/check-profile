#!/usr/bin/env python3
"""
Demo data generator for testing without API calls
Creates sample LinkedIn profiles for testing the scraper functionality
"""
from src.database.models import LinkedInProfile
from src.database.db_manager import DatabaseManager
from src.utils.export import ProfileExporter
from datetime import datetime


def generate_demo_profiles():
    """Generate sample profiles for testing"""
    profiles = [
        LinkedInProfile(
            profile_id="demo-001",
            name="Marie Dubois",
            headline="Software Engineer looking for new opportunities",
            school="École Polytechnique",
            degree="Master of Engineering",
            field_of_study="Computer Science",
            graduation_year="2020",
            current_company=None,
            current_position=None,
            is_open_to_work=True,
            location="Paris, France",
            profile_url="https://linkedin.com/in/demo-marie-dubois",
            about="Passionate about AI and machine learning",
            connections=500
        ),
        LinkedInProfile(
            profile_id="demo-002",
            name="Jean Martin",
            headline="Senior Data Scientist at Google",
            school="École Polytechnique",
            degree="PhD in Data Science",
            field_of_study="Artificial Intelligence",
            graduation_year="2018",
            current_company="Google",
            current_position="Senior Data Scientist",
            is_open_to_work=False,
            location="London, UK",
            profile_url="https://linkedin.com/in/demo-jean-martin",
            about="Building scalable ML systems",
            connections=1200
        ),
        LinkedInProfile(
            profile_id="demo-003",
            name="Sophie Bernard",
            headline="Product Manager | Open to opportunities",
            school="École Polytechnique",
            degree="MSc Engineering",
            field_of_study="Industrial Engineering",
            graduation_year="2019",
            current_company=None,
            current_position=None,
            is_open_to_work=True,
            location="Berlin, Germany",
            profile_url="https://linkedin.com/in/demo-sophie-bernard",
            about="10 years in product management, seeking new challenges",
            connections=800
        ),
        LinkedInProfile(
            profile_id="demo-004",
            name="Pierre Petit",
            headline="Full Stack Developer at Stripe",
            school="École Polytechnique",
            degree="Bachelor of Computer Science",
            field_of_study="Software Engineering",
            graduation_year="2021",
            current_company="Stripe",
            current_position="Full Stack Developer",
            is_open_to_work=False,
            location="San Francisco, USA",
            profile_url="https://linkedin.com/in/demo-pierre-petit",
            about="Building payment infrastructure",
            connections=350
        ),
        LinkedInProfile(
            profile_id="demo-005",
            name="Camille Rousseau",
            headline="UX Designer seeking remote opportunities",
            school="École Polytechnique",
            degree="Master of Design",
            field_of_study="User Experience Design",
            graduation_year="2020",
            current_company=None,
            current_position=None,
            is_open_to_work=True,
            location="Montreal, Canada",
            profile_url="https://linkedin.com/in/demo-camille-rousseau",
            about="Creating delightful user experiences",
            connections=600
        ),
        LinkedInProfile(
            profile_id="demo-006",
            name="Thomas Laurent",
            headline="DevOps Engineer at Amazon",
            school="École Polytechnique",
            degree="Master of Engineering",
            field_of_study="Cloud Computing",
            graduation_year="2019",
            current_company="Amazon Web Services",
            current_position="Senior DevOps Engineer",
            is_open_to_work=False,
            location="Seattle, USA",
            profile_url="https://linkedin.com/in/demo-thomas-laurent",
            about="Automating everything",
            connections=950
        ),
        LinkedInProfile(
            profile_id="demo-007",
            name="Isabelle Moreau",
            headline="Business Analyst | Actively job hunting",
            school="École Polytechnique",
            degree="MBA",
            field_of_study="Business Administration",
            graduation_year="2022",
            current_company=None,
            current_position=None,
            is_open_to_work=True,
            location="Brussels, Belgium",
            profile_url="https://linkedin.com/in/demo-isabelle-moreau",
            about="Data-driven decision making enthusiast",
            connections=450
        ),
        LinkedInProfile(
            profile_id="demo-008",
            name="Antoine Leroy",
            headline="Machine Learning Engineer at Meta",
            school="École Polytechnique",
            degree="PhD in Machine Learning",
            field_of_study="Computer Vision",
            graduation_year="2017",
            current_company="Meta",
            current_position="ML Engineer",
            is_open_to_work=False,
            location="Menlo Park, USA",
            profile_url="https://linkedin.com/in/demo-antoine-leroy",
            about="Pushing the boundaries of computer vision",
            connections=1500
        ),
        LinkedInProfile(
            profile_id="demo-009",
            name="Émilie Simon",
            headline="Marketing Manager seeking new role",
            school="École Polytechnique",
            degree="Master in Marketing",
            field_of_study="Digital Marketing",
            graduation_year="2020",
            current_company=None,
            current_position=None,
            is_open_to_work=True,
            location="Lyon, France",
            profile_url="https://linkedin.com/in/demo-emilie-simon",
            about="Growth hacker with proven track record",
            connections=700
        ),
        LinkedInProfile(
            profile_id="demo-010",
            name="Lucas Fournier",
            headline="Security Engineer at Microsoft",
            school="École Polytechnique",
            degree="MSc in Cybersecurity",
            field_of_study="Information Security",
            graduation_year="2021",
            current_company="Microsoft",
            current_position="Security Engineer",
            is_open_to_work=False,
            location="Redmond, USA",
            profile_url="https://linkedin.com/in/demo-lucas-fournier",
            about="Protecting systems and data",
            connections=550
        )
    ]

    return profiles


def populate_demo_database(db_path: str = "./data/profiles.db"):
    """
    Populate database with demo data

    Args:
        db_path: Path to database file
    """
    print("🚀 Generating demo profiles...")

    profiles = generate_demo_profiles()
    db = DatabaseManager(db_path)

    print(f"💾 Saving {len(profiles)} demo profiles to database...")
    for profile in profiles:
        success = db.save_profile(profile)
        if success:
            status_emoji = "🔍" if profile.is_open_to_work else "💼"
            print(f"  {status_emoji} {profile.name} - {profile.job_status}")

    print(f"\n✅ Successfully saved {len(profiles)} profiles!")

    # Show statistics
    stats = db.get_statistics()
    print(f"\n📊 Database Statistics:")
    print(f"  Total profiles: {stats['total_profiles']}")
    print(f"  Job seekers: {stats['job_seekers']}")
    print(f"  Employed: {stats['employed']}")

    return profiles


def export_demo_data():
    """Export demo data to all formats"""
    print("\n📤 Exporting demo data...")

    db = DatabaseManager("./data/profiles.db")
    profiles = db.get_all_profiles()

    if not profiles:
        print("❌ No profiles found in database. Run populate_demo_database() first.")
        return

    exporter = ProfileExporter()

    # Export to CSV
    if exporter.to_csv(profiles, "./exports/demo_profiles.csv"):
        print("✅ CSV export: ./exports/demo_profiles.csv")
    else:
        print("❌ CSV export failed")

    # Export to JSON
    if exporter.to_json(profiles, "./exports/demo_profiles.json"):
        print("✅ JSON export: ./exports/demo_profiles.json")
    else:
        print("❌ JSON export failed")

    # Export to Markdown
    if exporter.to_markdown(profiles, "./exports/demo_profiles.md"):
        print("✅ Markdown export: ./exports/demo_profiles.md")
    else:
        print("❌ Markdown export failed")

    print(f"\n✅ Exported {len(profiles)} profiles successfully!")


def main():
    """Main demo function"""
    print("=" * 60)
    print("  LinkedIn Profile Scraper - Demo Mode")
    print("=" * 60)
    print()
    print("This demo generates sample profiles without needing an API key.")
    print()

    # Populate database with demo data
    profiles = populate_demo_database()

    # Export to all formats
    export_demo_data()

    print("\n" + "=" * 60)
    print("Demo completed! Check the ./exports/ directory for files.")
    print("=" * 60)


if __name__ == "__main__":
    main()
