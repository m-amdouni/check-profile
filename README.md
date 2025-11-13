# LinkedIn Profile Scraper

A legal and compliant tool to search and analyze public LinkedIn profiles using **Proxycurl API**. Find alumni from a given high school or university and check their current job status.

## Table of Contents

- [Overview](#overview)
- [Solution Architecture](#solution-architecture)
- [Why This Approach?](#why-this-approach)
- [Technology Stack](#technology-stack)
- [Features](#features)
- [Installation](#installation)
- [Configuration](#configuration)
- [Quick Start - Demo Mode](#quick-start---demo-mode-no-api-key-required)
- [Usage Examples](#usage-examples)
- [Detailed Execution Guide](#detailed-execution-guide)
- [Project Structure](#project-structure)
- [Data Model](#data-model)
- [API Reference](#api-reference)
- [FAQ](#faq)
- [Troubleshooting](#troubleshooting)

---

## Overview

This project solves a common recruitment and networking challenge: **finding alumni from specific schools and understanding their current job search status**. Instead of manually searching LinkedIn, this tool automates the process using a legal, API-based approach.

### Problem Statement

You want to:
- ✅ Find profiles of people who studied at a specific high school or university
- ✅ Check if they are currently searching for jobs ("Open to Work")
- ✅ Identify their current employment status
- ✅ Export and analyze this data for recruitment, networking, or research

### Solution

A Python-based CLI tool that uses **Proxycurl API** to legally access LinkedIn data, stores it locally in SQLite, and provides powerful filtering and export capabilities.

---

## Solution Architecture

### High-Level Architecture

```
┌─────────────────┐
│   User (CLI)    │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│         Main Application (main.py)       │
│  ┌────────────────────────────────────┐ │
│  │  CLI Parser (argparse)             │ │
│  │  • scrape, list, export, stats     │ │
│  └────────────────────────────────────┘ │
└─────────┬────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────┐
│         Application Layer                │
│  ┌────────────────┐  ┌────────────────┐│
│  │  API Scraper   │  │  DB Manager    ││
│  │  (Proxycurl)   │  │  (SQLite)      ││
│  └────────────────┘  └────────────────┘│
│  ┌────────────────┐  ┌────────────────┐│
│  │ Profile Filter │  │  Exporter      ││
│  │ (Statistics)   │  │  (CSV/JSON/MD) ││
│  └────────────────┘  └────────────────┘│
└─────────┬────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────┐
│         External Services                │
│  ┌────────────────────────────────────┐ │
│  │      Proxycurl API                 │ │
│  │  (LinkedIn Data Provider)          │ │
│  └────────────────────────────────────┘ │
└─────────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────┐
│         Local Storage                    │
│  ┌────────────────┐  ┌────────────────┐│
│  │  SQLite DB     │  │  Export Files  ││
│  │  (profiles.db) │  │  (CSV/JSON/MD) ││
│  └────────────────┘  └────────────────┘│
└─────────────────────────────────────────┘
```

### Data Flow

1. **User Input** → CLI command (e.g., `scrape --school "Harvard"`)
2. **API Request** → Proxycurl API searches LinkedIn profiles
3. **Data Processing** → Parse and structure profile data
4. **Storage** → Save to SQLite database
5. **Analysis** → Apply filters, generate statistics
6. **Output** → Display in terminal or export to file

---

## Why This Approach?

### ❌ What We DIDN'T Do (and Why)

#### 1. **Web Scraping with Beautiful Soup / Selenium**
```python
# ❌ NOT USED - Violates LinkedIn ToS
from selenium import webdriver
driver.get("https://linkedin.com/...")
```

**Problems:**
- ❌ Violates LinkedIn Terms of Service
- ❌ Risk of account suspension or legal action
- ❌ Brittle - breaks when LinkedIn changes HTML
- ❌ Requires maintaining cookies/sessions
- ❌ Slow and unreliable
- ❌ Requires handling CAPTCHAs

#### 2. **LinkedIn Official API**
```python
# ❌ Limited - Insufficient for our use case
linkedin_api.search_people(...)
```

**Problems:**
- ❌ Very limited access (mostly for logged-in user data)
- ❌ Requires LinkedIn Partnership for broader access
- ❌ Can't search by school for public profiles
- ❌ Expensive for startups

### ✅ What We DID (and Why)

#### **Proxycurl API Approach**

```python
# ✅ USED - Legal, reliable, professional
proxycurl.search_person(school="Harvard")
```

**Advantages:**
- ✅ **Legal & Compliant** - No ToS violations
- ✅ **No Account Risk** - Don't need LinkedIn credentials
- ✅ **Reliable** - Professional SLA and uptime
- ✅ **Maintained** - They handle LinkedIn changes
- ✅ **Rate Limiting Built-in** - Respectful API usage
- ✅ **Structured Data** - Clean JSON responses
- ✅ **Fast** - Optimized for bulk operations
- ✅ **Support** - Professional customer support

### Why Not Build Our Own Scraper?

| Aspect | Custom Scraper | Proxycurl API |
|--------|---------------|---------------|
| **Legal** | ❌ Violates ToS | ✅ Compliant |
| **Maintenance** | ❌ High (weekly fixes) | ✅ None |
| **Speed** | ❌ Slow (rate limited) | ✅ Fast |
| **Reliability** | ❌ Breaks often | ✅ 99.9% uptime |
| **Account Risk** | ❌ High | ✅ None |
| **Development Time** | ❌ Weeks | ✅ Hours |
| **Cost** | ❌ Time + Proxy costs | ✅ Predictable |

**Verdict:** For production use, Proxycurl API is the only viable option.

---

## Technology Stack

### Core Dependencies

We kept dependencies minimal for maintainability:

```txt
requests==2.31.0          # HTTP client
python-dotenv==1.0.0      # Environment configuration
pandas==2.1.3             # Data export capabilities
rich==13.7.0              # Beautiful CLI output
```

### Why These Libraries?

#### 1. **requests** - HTTP Client
```python
response = requests.get(url, headers=headers)
```

**Why chosen:**
- ✅ Industry standard for HTTP requests
- ✅ Simple, reliable, well-documented
- ✅ Handles authentication, timeouts, retries
- ✅ 50M+ downloads/month

**Alternatives considered:**
- `urllib` - Too low-level
- `httpx` - Overkill for our needs
- `aiohttp` - Async not needed (API is fast enough)

#### 2. **python-dotenv** - Configuration
```python
load_dotenv()
api_key = os.getenv("PROXYCURL_API_KEY")
```

**Why chosen:**
- ✅ Standard for environment variable management
- ✅ Keeps secrets out of code
- ✅ Easy .env file format
- ✅ Production-ready (works with Docker, etc.)

**Alternatives considered:**
- `configparser` - Less flexible
- `pyyaml` - Overkill for simple config
- Environment variables only - Not developer-friendly

#### 3. **pandas** - Data Export
```python
df = pd.DataFrame(profiles)
df.to_csv("output.csv")
```

**Why chosen:**
- ✅ Industry standard for data manipulation
- ✅ Easy CSV/JSON/Excel export
- ✅ Future-proofing (can add analytics later)
- ✅ Great for data cleaning/transformation

**Alternatives considered:**
- Native `csv` module - Too basic
- `openpyxl` - Excel-specific
- Custom export code - Reinventing the wheel

#### 4. **rich** - CLI Output
```python
console.print(table)
console.print("[green]✓ Success[/green]")
```

**Why chosen:**
- ✅ Beautiful terminal output with colors
- ✅ Tables, progress bars, syntax highlighting
- ✅ Professional UX for CLI tools
- ✅ Emoji support, markdown rendering

**Alternatives considered:**
- `click` - Focus on CLI parsing, not output
- `colorama` - Too basic
- Plain `print()` - Ugly, unprofessional

#### 5. **SQLite (Built-in)** - Database
```python
import sqlite3
conn = sqlite3.connect("profiles.db")
```

**Why chosen:**
- ✅ No external database server needed
- ✅ Built into Python (zero dependencies)
- ✅ Fast for < 100K records
- ✅ Single file - easy backup/sharing
- ✅ Full SQL support

**Alternatives considered:**
- PostgreSQL/MySQL - Overkill, requires server
- JSON files - No querying capabilities
- CSV files - Can't handle relationships

---

## Features

- 🔍 **Search by School**: Find profiles of people who studied at a specific institution
- 💼 **Job Status Detection**: Identify who is "Open to Work" vs currently employed
- 💾 **SQLite Database**: Store and manage profiles locally
- 📊 **Statistics**: Analyze job seeking trends among alumni
- 📤 **Export**: Export results to CSV, JSON, or Markdown
- ⚡ **Rate Limiting**: Built-in respectful API usage
- 🎨 **Beautiful CLI**: Rich terminal interface with tables and colors
- 🔒 **Secure**: API keys stored in .env file, never in code
- 📝 **Logging**: Comprehensive logging for debugging

---

## Installation

### Prerequisites

- Python 3.9 or higher
- pip (Python package manager)
- Proxycurl API key (sign up at [https://nubela.co/proxycurl/](https://nubela.co/proxycurl/))

### Step 1: Clone Repository

```bash
git clone https://github.com/yourusername/check-profile.git
cd check-profile
```

### Step 2: Create Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs only 4 lightweight dependencies:
- `requests` - HTTP client
- `python-dotenv` - Config management
- `pandas` - Data export
- `rich` - Beautiful CLI

### Step 4: Get API Key

1. Sign up at [Proxycurl](https://nubela.co/proxycurl/)
2. Navigate to dashboard
3. Copy your API key
4. Proxycurl offers a free tier with limited credits

### Step 5: Configure Environment

```bash
# Copy example configuration
cp .env.example .env

# Edit .env file
nano .env  # or use any text editor
```

Add your API key:
```env
PROXYCURL_API_KEY=your_actual_api_key_here
TARGET_SCHOOL=Harvard University
MAX_PROFILES=50
```

### Step 6: Verify Installation

```bash
# Check if everything is installed
python main.py --help
```

You should see the help menu with available commands.

---

## Configuration

### Environment Variables (.env)

```env
# ============================================
# API Configuration (Required)
# ============================================
PROXYCURL_API_KEY=your_api_key_here

# ============================================
# Search Configuration
# ============================================
# Default school to search (can be overridden via CLI)
TARGET_SCHOOL=Harvard University

# Maximum number of profiles to scrape per search
MAX_PROFILES=50

# Optional search keywords
SEARCH_KEYWORDS=

# ============================================
# Rate Limiting
# ============================================
# Maximum API requests per minute
REQUESTS_PER_MINUTE=10

# Delay between requests in seconds
DELAY_BETWEEN_REQUESTS=6

# ============================================
# Database
# ============================================
# Path to SQLite database file
DATABASE_PATH=./data/profiles.db

# ============================================
# Export Options
# ============================================
# Default export format (csv, json, markdown)
EXPORT_FORMAT=csv

# Directory for exported files
EXPORT_PATH=./exports/

# ============================================
# Logging
# ============================================
# Log level (DEBUG, INFO, WARNING, ERROR)
LOG_LEVEL=INFO

# Path to log file
LOG_FILE=./logs/scraper.log
```

---

## Quick Start - Demo Mode (No API Key Required)

Want to test the tool immediately without an API key? Use the demo mode:

```bash
# Generate 10 sample profiles and export them
python demo_data.py
```

This will:
- ✅ Create 10 realistic sample profiles in the database
- ✅ Export to CSV, JSON, and Markdown formats automatically
- ✅ Show statistics and job seeker breakdown
- ✅ No API key needed!

Check the generated files in `./exports/`:
```bash
ls -lh exports/
# demo_profiles.csv
# demo_profiles.json
# demo_profiles.md
```

---

## Usage Examples

### Basic Commands

#### 1. **Scrape Profiles from a School**

```bash
python main.py scrape --school "Harvard University" --max-profiles 50
```

**Expected Output:**
```
    ╔══════════════════════════════════════════════════════════════╗
    ║          LinkedIn Profile Scraper v1.0.0                     ║
    ║                                                              ║
    ║  ✓ Uses Proxycurl API (Legal & Compliant)                   ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝

🔍 Searching profiles from Harvard University...

Searching profiles from Harvard University...
Found 50 profile URLs
Fetching profile: https://linkedin.com/in/john-doe
✓ John Doe - employed (1/50)
Fetching profile: https://linkedin.com/in/jane-smith
✓ Jane Smith - seeking (2/50)
...
Scraping completed. Found 50 profiles.

💾 Saving to database...
✓ Saved 50 profiles

📊 Statistics:
┏━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━┳━━━━━━━━━━━━┓
┃ Metric                 ┃ Count ┃ Percentage ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━╇━━━━━━━━━━━━┩
│ Total Profiles         │    50 │       100% │
│ Job Seekers           │    12 │        24% │
│ Employed              │    35 │        70% │
│ Unknown Status        │     3 │         6% │
└────────────────────────┴───────┴────────────┘

✓ Done!
```

#### 2. **Find Only Job Seekers**

```bash
python main.py scrape --school "MIT" --job-status seeking --max-profiles 30
```

**Use Case:** You're a recruiter looking for available talent from MIT.

**Expected Output:**
```
🔍 Searching profiles from MIT...
Found 30 job seekers from MIT

💾 Saving to database...
✓ Saved 30 profiles

📊 Statistics:
┏━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━┳━━━━━━━━━━━━┓
┃ Metric                 ┃ Count ┃ Percentage ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━╇━━━━━━━━━━━━┩
│ Total Profiles         │    30 │       100% │
│ Job Seekers           │    30 │       100% │
│ Employed              │     0 │         0% │
│ Unknown Status        │     0 │         0% │
└────────────────────────┴───────┴────────────┘
```

#### 3. **Find Only Employed Alumni**

```bash
python main.py scrape --school "Stanford University" --job-status employed --max-profiles 40
```

**Use Case:** Research career paths of employed Stanford alumni.

#### 4. **List Stored Profiles**

```bash
python main.py list --school "Harvard University"
```

**Expected Output:**
```
Found 50 profiles:

┏━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━┓
┃ Name            ┃ School             ┃ Status      ┃ Company        ┃
┡━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━┩
│ John Doe        │ Harvard University │ 💼 employed │ Google         │
│ Jane Smith      │ Harvard University │ 🔍 seeking  │ N/A            │
│ Bob Johnson     │ Harvard University │ 💼 employed │ Microsoft      │
│ ...             │ ...                │ ...         │ ...            │
└─────────────────┴────────────────────┴─────────────┴────────────────┘
```

#### 5. **Export to CSV**

```bash
python main.py export --format csv --output alumni_report.csv
```

**Expected Output:**
```
📤 Exporting to CSV...
✓ Exported to alumni_report.csv
```

**CSV Contents:**
```csv
profile_id,name,headline,school,degree,field_of_study,graduation_year,current_company,current_position,is_open_to_work,location,profile_url,about,connections,scraped_at
john-doe-123,John Doe,Software Engineer,Harvard University,Bachelor of Science,Computer Science,2019,Google,Senior Engineer,False,San Francisco CA,https://linkedin.com/in/john-doe-123,...,500,2025-11-12T10:00:00Z
```

#### 6. **Export to JSON**

```bash
python main.py export --format json --output profiles.json
```

**JSON Output:**
```json
[
  {
    "profile_id": "john-doe-123",
    "name": "John Doe",
    "headline": "Software Engineer at Google",
    "school": "Harvard University",
    "degree": "Bachelor of Science",
    "field_of_study": "Computer Science",
    "graduation_year": "2019",
    "current_company": "Google",
    "current_position": "Senior Software Engineer",
    "is_open_to_work": false,
    "location": "San Francisco, CA",
    "profile_url": "https://linkedin.com/in/john-doe-123",
    "about": "Passionate software engineer...",
    "connections": 500,
    "scraped_at": "2025-11-12T10:00:00Z"
  }
]
```

#### 7. **View Statistics**

```bash
python main.py stats
```

**Expected Output:**
```
📊 Statistics:
┏━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━┳━━━━━━━━━━━━┓
┃ Metric                 ┃ Count ┃ Percentage ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━╇━━━━━━━━━━━━┩
│ Total Profiles         │   150 │       100% │
│ Job Seekers           │    36 │        24% │
│ Employed              │   105 │        70% │
│ Unknown Status        │     9 │         6% │
└────────────────────────┴───────┴────────────┘

🎓 Top Schools:
  • Harvard University: 50
  • MIT: 30
  • Stanford University: 40
  • Yale University: 20
  • Princeton University: 10

📍 Top Locations:
  • San Francisco, CA: 35
  • New York, NY: 28
  • Boston, MA: 22
  • Seattle, WA: 18
  • Austin, TX: 12

🏢 Top Companies:
  • Google: 15
  • Microsoft: 12
  • Amazon: 10
  • Meta: 8
  • Apple: 7
```

---

## Detailed Execution Guide

### Scenario 1: Recruitment Campaign

**Goal:** Find software engineers from top CS schools who are actively job seeking.

```bash
# Step 1: Scrape job seekers from MIT
python main.py scrape --school "MIT" --job-status seeking --max-profiles 50

# Step 2: Scrape job seekers from Stanford
python main.py scrape --school "Stanford University" --job-status seeking --max-profiles 50

# Step 3: Export combined results
python main.py export --format csv --job-status seeking --output job_seekers_cs.csv

# Step 4: View statistics
python main.py stats
```

### Scenario 2: Alumni Network Analysis

**Goal:** Understand where your school's alumni are working.

```bash
# Step 1: Scrape all alumni profiles
python main.py scrape --school "Your University" --max-profiles 200

# Step 2: View in terminal
python main.py list --school "Your University"

# Step 3: Export for analysis
python main.py export --school "Your University" --format json --output alumni_network.json

# Step 4: View statistics
python main.py stats
```

### Scenario 3: Market Research

**Goal:** Analyze employment trends at competitor companies.

```bash
# Step 1: Scrape profiles from target school
python main.py scrape --school "Harvard Business School" --max-profiles 100

# Step 2: Export to CSV for Excel analysis
python main.py export --school "Harvard Business School" --format csv --output hbs_alumni.csv

# Open in Excel and filter by current_company column
```

### Scenario 4: Programmatic Usage

**Use the tool in your own Python scripts:**

```python
# example_usage.py
from src.scrapers.api_scraper import ProxycurlScraper
from src.database.db_manager import DatabaseManager
from src.filters.profile_filter import ProfileFilter

# Initialize
scraper = ProxycurlScraper()
db = DatabaseManager()

# Scrape profiles
profiles = scraper.scrape_school_alumni(
    school_name="MIT",
    max_profiles=50,
    job_status_filter="seeking"
)

# Save to database
for profile in profiles:
    db.save_profile(profile)

# Analyze
stats = ProfileFilter.get_statistics(profiles)
print(f"Found {stats['seeking']} job seekers")

# Get job seekers only
job_seekers = [p for p in profiles if p.is_open_to_work]

# Export
from src.utils.export import ProfileExporter
exporter = ProfileExporter()
exporter.to_csv(job_seekers, "job_seekers.csv")
```

---

## Project Structure

```
check-profile/
├── main.py                       # CLI entry point (359 lines)
├── example.py                    # Programmatic usage examples
├── requirements.txt              # 4 minimal dependencies
├── .env.example                  # Configuration template
├── .gitignore                    # Git ignore rules
├── LICENSE                       # MIT License
├── README.md                     # This file
│
└── src/                          # Source code
    ├── __init__.py
    │
    ├── scrapers/                 # Data collection
    │   ├── __init__.py
    │   └── api_scraper.py        # Proxycurl API integration
    │
    ├── database/                 # Data persistence
    │   ├── __init__.py
    │   ├── models.py             # Profile data model
    │   └── db_manager.py         # SQLite CRUD operations
    │
    ├── filters/                  # Data analysis
    │   ├── __init__.py
    │   └── profile_filter.py     # Filtering & statistics
    │
    └── utils/                    # Utilities
        ├── __init__.py
        ├── config.py             # Configuration management
        ├── rate_limiter.py       # API rate limiting
        ├── logger.py             # Logging setup
        └── export.py             # CSV/JSON/Markdown export

# Runtime directories (created automatically)
data/                             # SQLite database
├── profiles.db                   # Profile storage

exports/                          # Exported files
├── alumni_report.csv
└── profiles.json

logs/                             # Log files
└── scraper.log
```

### Key Modules

#### `src/scrapers/api_scraper.py`
- **Purpose:** Interface with Proxycurl API
- **Key Methods:**
  - `search_profiles_by_school()` - Search for profiles
  - `get_profile_details()` - Fetch full profile data
  - `scrape_school_alumni()` - Complete scraping workflow
- **Features:** Rate limiting, error handling, data parsing

#### `src/database/db_manager.py`
- **Purpose:** SQLite database operations
- **Key Methods:**
  - `save_profile()` - Insert/update profiles
  - `get_profiles_by_school()` - Query by school
  - `get_statistics()` - Aggregate statistics
- **Features:** Connection pooling, indexes, transactions

#### `src/filters/profile_filter.py`
- **Purpose:** Data filtering and analysis
- **Key Methods:**
  - `filter_by_job_status()` - Filter by employment status
  - `filter_by_school()` - Filter by education
  - `get_statistics()` - Generate analytics
- **Features:** Multiple filter types, statistics generation

#### `src/utils/config.py`
- **Purpose:** Configuration management
- **Features:** Environment variables, validation, defaults

#### `src/utils/rate_limiter.py`
- **Purpose:** API rate limiting
- **Algorithm:** Sliding window
- **Features:** Automatic backoff, configurable limits

---

## Data Model

### Profile Schema

Each profile contains the following fields:

```python
{
    # Identity
    "profile_id": str,          # LinkedIn profile ID (e.g., "john-doe-123")
    "name": str,                # Full name
    "headline": str,            # Professional headline

    # Education
    "school": str,              # University/school name
    "degree": str,              # Degree type (BS, MS, PhD, etc.)
    "field_of_study": str,      # Major/field
    "graduation_year": str,     # Year graduated

    # Employment
    "current_company": str,     # Current employer
    "current_position": str,    # Current job title
    "is_open_to_work": bool,    # Job seeking status

    # Additional Info
    "location": str,            # City, State/Country
    "profile_url": str,         # LinkedIn profile URL
    "about": str,               # About/summary section
    "connections": int,         # Number of connections

    # Metadata
    "scraped_at": str          # ISO timestamp of data collection
}
```

### Database Schema

```sql
CREATE TABLE profiles (
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
);

-- Indexes for performance
CREATE INDEX idx_school ON profiles(school);
CREATE INDEX idx_job_status ON profiles(is_open_to_work, current_company);
```

---

## API Reference

### CLI Commands

#### `scrape` - Scrape new profiles

```bash
python main.py scrape [OPTIONS]

Options:
  --school TEXT         School/university name (required)
  --max-profiles INT    Maximum profiles to scrape [default: 50]
  --job-status TEXT     Filter: seeking | employed | unknown

Examples:
  python main.py scrape --school "MIT" --max-profiles 100
  python main.py scrape --school "Harvard" --job-status seeking
```

#### `list` - View stored profiles

```bash
python main.py list [OPTIONS]

Options:
  --school TEXT         Filter by school name
  --job-status TEXT     Filter: seeking | employed | unknown

Examples:
  python main.py list
  python main.py list --school "Stanford"
  python main.py list --job-status seeking
```

#### `export` - Export profiles

```bash
python main.py export [OPTIONS]

Options:
  --format TEXT         Format: csv | json | markdown [default: csv]
  --output TEXT         Output file path (required)
  --school TEXT         Filter by school
  --job-status TEXT     Filter: seeking | employed | unknown

Examples:
  python main.py export --format csv --output report.csv
  python main.py export --format json --output data.json --school "MIT"
  python main.py export --format markdown --output alumni.md
```

#### `stats` - Show statistics

```bash
python main.py stats

Example:
  python main.py stats
```

---

## FAQ

### General Questions

#### Q: Is this legal?
**A:** Yes! This tool uses Proxycurl API, which provides LinkedIn data through legal means. No Terms of Service violations or web scraping involved.

#### Q: Do I need a LinkedIn account?
**A:** No! Proxycurl handles data access through their API. No LinkedIn credentials needed.

#### Q: How much does it cost?
**A:** Proxycurl pricing:
- Free Tier: Limited credits to test
- Starter: $79/month (3,000 credits)
- Professional: $249/month (10,000 credits)
- Each profile lookup costs ~1-2 credits

#### Q: How accurate is the data?
**A:** Data is as accurate as what users make public on LinkedIn. Proxycurl updates data regularly and provides a freshness indicator.

#### Q: Can I scrape private profiles?
**A:** No. Only public profile data is accessible. This respects user privacy settings.

### Technical Questions

#### Q: Why SQLite instead of PostgreSQL?
**A:** SQLite is perfect for < 1M records, requires no server setup, and makes the tool portable. For larger datasets, you can easily migrate to PostgreSQL.

#### Q: Can I run this on a schedule?
**A:** Yes! Use cron (Linux/Mac) or Task Scheduler (Windows):
```bash
# Cron example - run daily at 2 AM
0 2 * * * cd /path/to/check-profile && python main.py scrape --school "MIT" --max-profiles 50
```

#### Q: How do I handle rate limits?
**A:** The tool has built-in rate limiting. Adjust in `.env`:
```env
REQUESTS_PER_MINUTE=5
DELAY_BETWEEN_REQUESTS=12
```

#### Q: Can I use multiple API keys?
**A:** Not currently, but you can modify `src/scrapers/api_scraper.py` to implement key rotation.

#### Q: How do I backup my data?
**A:** Simply copy the SQLite file:
```bash
cp data/profiles.db data/profiles_backup.db
```

---

## Troubleshooting

### Common Issues

#### 1. "PROXYCURL_API_KEY is required"

**Problem:** API key not configured

**Solution:**
```bash
# Create .env file
cp .env.example .env

# Edit and add your API key
echo "PROXYCURL_API_KEY=your_actual_key" >> .env
```

#### 2. "No profiles found"

**Possible causes:**
- School name spelling is incorrect
- No public profiles for that school
- API key has no remaining credits

**Solutions:**
```bash
# Try common school name format
python main.py scrape --school "Harvard University"  # Not "Harvard"

# Check API credits at Proxycurl dashboard
```

#### 3. "Rate limit exceeded"

**Problem:** Too many requests too quickly

**Solution:** Adjust rate limits in `.env`:
```env
REQUESTS_PER_MINUTE=5
DELAY_BETWEEN_REQUESTS=12
```

#### 4. "Database locked"

**Problem:** Another process is using the database

**Solution:**
```bash
# Check for other running instances
ps aux | grep main.py

# Kill if necessary
kill <process_id>
```

#### 5. "Import Error: No module named 'src'"

**Problem:** Running from wrong directory

**Solution:**
```bash
# Make sure you're in the project root
cd /path/to/check-profile

# Run from there
python main.py scrape --school "MIT"
```

#### 6. Export file already exists

**Problem:** Output file already exists

**Solution:**
```bash
# Delete old file
rm alumni_report.csv

# Or use different filename
python main.py export --output alumni_report_v2.csv
```

### Debug Mode

Enable detailed logging:

```bash
# Edit .env
LOG_LEVEL=DEBUG

# Check logs
tail -f logs/scraper.log
```

### Getting Help

1. **Check logs:** `cat logs/scraper.log`
2. **Verbose output:** Set `LOG_LEVEL=DEBUG` in `.env`
3. **GitHub Issues:** [Report bugs](https://github.com/yourusername/check-profile/issues)
4. **Proxycurl Support:** [API Documentation](https://nubela.co/proxycurl/docs)

---

## Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup

```bash
# Clone your fork
git clone https://github.com/yourusername/check-profile.git

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run tests (if available)
python -m pytest
```

---

## License

MIT License - See [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- **Proxycurl** - Legal LinkedIn data access
- **Rich** - Beautiful terminal output
- **Python Community** - Amazing open-source tools

---

## Roadmap

Future enhancements:

- [ ] Add more filtering options (location, industry, etc.)
- [ ] Implement profile comparison features
- [ ] Add data visualization (charts, graphs)
- [ ] Support for bulk operations
- [ ] API key rotation for high-volume use
- [ ] Export to Excel with formatting
- [ ] Email alerts for new job seekers
- [ ] Integration with ATS (Applicant Tracking Systems)

---

**Built with ❤️ for ethical recruitment and career research**

For questions or support, contact: support@example.com
