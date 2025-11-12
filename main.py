#!/usr/bin/env python3
"""
LinkedIn Profile Scraper - Main Entry Point

Uses Proxycurl API (legal and compliant method) to search LinkedIn profiles
by school and analyze their job search status.
"""
import argparse
import sys
from rich.console import Console
from rich.table import Table

from src.utils.config import Config
from src.utils.logger import setup_logger
from src.utils.export import ProfileExporter
from src.database.db_manager import DatabaseManager
from src.filters.profile_filter import ProfileFilter
from src.scrapers.api_scraper import ProxycurlScraper

console = Console()
logger = setup_logger()


def print_banner():
    """Print application banner"""
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║          LinkedIn Profile Scraper v1.0.0                     ║
    ║                                                              ║
    ║  ✓ Uses Proxycurl API (Legal & Compliant)                   ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    console.print(banner, style="bold cyan")


def validate_config():
    """Validate configuration"""
    errors = Config.validate()

    if errors:
        console.print("\n[red]Configuration errors:[/red]")
        for error in errors:
            console.print(f"  ❌ {error}", style="red")
        console.print(
            "\n[yellow]Please check your .env file or command-line arguments.[/yellow]"
        )
        console.print(
            "[cyan]Get your Proxycurl API key at: https://nubela.co/proxycurl/[/cyan]"
        )
        return False

    return True


def print_statistics(stats: dict):
    """Print profile statistics"""
    console.print("\n[bold cyan]📊 Statistics:[/bold cyan]")

    # Create statistics table
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Metric", style="cyan")
    table.add_column("Count", justify="right", style="green")
    table.add_column("Percentage", justify="right", style="yellow")

    table.add_row("Total Profiles", str(stats["total"]), "100%")
    table.add_row(
        "Job Seekers (Open to Work)",
        str(stats["seeking"]),
        f"{stats['seeking_percentage']}%"
    )
    table.add_row(
        "Employed",
        str(stats["employed"]),
        f"{stats['employed_percentage']}%"
    )
    table.add_row(
        "Unknown Status",
        str(stats["unknown"]),
        f"{round((stats['unknown'] / stats['total']) * 100, 1)}%"
    )

    console.print(table)

    # Top schools
    if stats.get("top_schools"):
        console.print("\n[bold cyan]🎓 Top Schools:[/bold cyan]")
        for school, count in stats["top_schools"]:
            console.print(f"  • {school}: {count}")

    # Top locations
    if stats.get("top_locations"):
        console.print("\n[bold cyan]📍 Top Locations:[/bold cyan]")
        for location, count in stats["top_locations"]:
            console.print(f"  • {location}: {count}")

    # Top companies
    if stats.get("top_companies"):
        console.print("\n[bold cyan]🏢 Top Companies:[/bold cyan]")
        for company, count in stats["top_companies"]:
            console.print(f"  • {company}: {count}")


def scrape_profiles(args, db: DatabaseManager):
    """Scrape profiles using Proxycurl API"""
    try:
        scraper = ProxycurlScraper()

        console.print(
            f"\n[cyan]🔍 Searching profiles from {args.school}...[/cyan]"
        )

        profiles = scraper.scrape_school_alumni(
            school_name=args.school,
            max_profiles=args.max_profiles,
            job_status_filter=args.job_status
        )

        if not profiles:
            console.print("[yellow]No profiles found.[/yellow]")
            return []

        # Save to database
        console.print("\n[cyan]💾 Saving to database...[/cyan]")
        for profile in profiles:
            db.save_profile(profile)

        console.print(f"[green]✓ Saved {len(profiles)} profiles[/green]")

        # Display statistics
        stats = ProfileFilter.get_statistics(profiles)
        print_statistics(stats)

        return profiles

    except ValueError as e:
        console.print(f"[red]Error: {e}[/red]")
        console.print(
            "[yellow]Please set PROXYCURL_API_KEY in your .env file[/yellow]"
        )
        console.print(
            "[cyan]Get your API key at: https://nubela.co/proxycurl/[/cyan]"
        )
        sys.exit(1)
    except Exception as e:
        console.print(f"[red]Error during scraping: {e}[/red]")
        logger.exception(e)
        sys.exit(1)


def export_profiles(profiles, format_type: str, output_path: str):
    """Export profiles to file"""
    console.print(f"\n[cyan]📤 Exporting to {format_type.upper()}...[/cyan]")

    exporter = ProfileExporter()

    if format_type == "csv":
        success = exporter.to_csv(profiles, output_path)
    elif format_type == "json":
        success = exporter.to_json(profiles, output_path)
    elif format_type == "markdown":
        success = exporter.to_markdown(profiles, output_path)
    else:
        console.print(f"[red]Unknown export format: {format_type}[/red]")
        return False

    if success:
        console.print(f"[green]✓ Exported to {output_path}[/green]")
    else:
        console.print(f"[red]✗ Export failed[/red]")

    return success


def list_profiles(args, db: DatabaseManager):
    """List profiles from database"""
    if args.school:
        profiles = db.get_profiles_by_school(args.school, args.job_status)
    else:
        profiles = db.get_all_profiles()

    if not profiles:
        console.print("[yellow]No profiles found in database.[/yellow]")
        return []

    console.print(f"\n[green]Found {len(profiles)} profiles:[/green]\n")

    # Create table
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Name", style="cyan")
    table.add_column("School", style="green")
    table.add_column("Status", style="yellow")
    table.add_column("Company", style="blue")

    for profile in profiles[:50]:  # Limit to 50 for display
        status_emoji = "🔍" if profile.is_open_to_work else "💼"
        table.add_row(
            profile.name,
            profile.school or "N/A",
            f"{status_emoji} {profile.job_status}",
            profile.current_company or "N/A"
        )

    console.print(table)

    if len(profiles) > 50:
        console.print(f"\n[yellow]... and {len(profiles) - 50} more[/yellow]")

    # Show statistics
    stats = ProfileFilter.get_statistics(profiles)
    print_statistics(stats)

    return profiles


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="LinkedIn Profile Scraper - Search alumni by school using Proxycurl API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Scrape profiles from a school
  python main.py scrape --school "Harvard University" --max-profiles 50

  # Find only job seekers
  python main.py scrape --school "MIT" --job-status seeking

  # List profiles from database
  python main.py list --school "Stanford University"

  # Export to CSV
  python main.py export --format csv --output results.csv

  # Show database statistics
  python main.py stats

Get your Proxycurl API key at: https://nubela.co/proxycurl/
        """
    )

    # Subcommands
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Scrape command
    scrape_parser = subparsers.add_parser("scrape", help="Scrape new profiles")
    scrape_parser.add_argument(
        "--school",
        type=str,
        required=True,
        help="School/university name to search"
    )
    scrape_parser.add_argument(
        "--max-profiles",
        type=int,
        default=50,
        help="Maximum number of profiles to scrape (default: 50)"
    )
    scrape_parser.add_argument(
        "--job-status",
        choices=["seeking", "employed", "unknown"],
        help="Filter by job status"
    )

    # List command
    list_parser = subparsers.add_parser("list", help="List profiles from database")
    list_parser.add_argument("--school", type=str, help="Filter by school")
    list_parser.add_argument(
        "--job-status",
        choices=["seeking", "employed", "unknown"],
        help="Filter by job status"
    )

    # Export command
    export_parser = subparsers.add_parser("export", help="Export profiles")
    export_parser.add_argument(
        "--format",
        choices=["csv", "json", "markdown"],
        default="csv",
        help="Export format (default: csv)"
    )
    export_parser.add_argument(
        "--output",
        type=str,
        required=True,
        help="Output file path"
    )
    export_parser.add_argument("--school", type=str, help="Filter by school")
    export_parser.add_argument(
        "--job-status",
        choices=["seeking", "employed", "unknown"],
        help="Filter by job status"
    )

    # Stats command
    stats_parser = subparsers.add_parser("stats", help="Show database statistics")

    args = parser.parse_args()

    # Print banner
    print_banner()

    # Override config with CLI arguments
    if hasattr(args, "school") and args.school:
        Config.TARGET_SCHOOL = args.school

    if hasattr(args, "max_profiles") and args.max_profiles:
        Config.MAX_PROFILES = args.max_profiles

    # Ensure directories exist
    Config.ensure_directories()

    # Initialize database
    db = DatabaseManager(Config.DATABASE_PATH)

    # Handle commands
    if args.command == "scrape":
        if not validate_config():
            sys.exit(1)

        profiles = scrape_profiles(args, db)

    elif args.command == "list":
        profiles = list_profiles(args, db)

    elif args.command == "export":
        # Get profiles from database
        if args.school:
            profiles = db.get_profiles_by_school(args.school, args.job_status)
        else:
            profiles = db.get_all_profiles()

        if not profiles:
            console.print("[yellow]No profiles to export.[/yellow]")
            sys.exit(0)

        export_profiles(profiles, args.format, args.output)

    elif args.command == "stats":
        stats = db.get_statistics()
        if stats["total_profiles"] == 0:
            console.print("[yellow]No profiles in database yet.[/yellow]")
            console.print(
                "\n[cyan]Run 'python main.py scrape --school \"Your School\"' "
                "to start scraping.[/cyan]"
            )
        else:
            print_statistics(stats)

    else:
        parser.print_help()
        sys.exit(1)

    console.print("\n[green]✓ Done![/green]\n")


if __name__ == "__main__":
    main()
