# LinkedIn Profile Scraper - Web Scraping Edition

⚠️ **IMPORTANT: FOR ACADEMIC AND EDUCATIONAL USE ONLY**

A Python tool to collect small samples of LinkedIn profile data for academic research and educational purposes using web scraping.

## ⚠️ Critical Disclaimers

**READ BEFORE USE:**

1. **Terms of Service Warning**: Web scraping LinkedIn may violate LinkedIn's Terms of Service. Use at your own risk.
2. **Academic Use Only**: This tool is intended ONLY for academic research, educational purposes, and small sample data collection.
3. **Ethical Limits**: The tool is hard-coded to limit scraping to a maximum of 20 profiles per session to encourage responsible use.
4. **Account Risk**: Using this tool may result in your LinkedIn account being suspended or banned.
5. **Legal Responsibility**: You are solely responsible for compliance with applicable laws and regulations in your jurisdiction.
6. **No Commercial Use**: This tool should NOT be used for commercial purposes, recruitment at scale, or mass data collection.

**Why This Approach?**

The original API-based solution used Proxycurl API, which is the legal and compliant way to access LinkedIn data. However, since 2025, the Proxycurl API key registration site has been unavailable. This web scraping solution is provided as an alternative for academic purposes only, with strict ethical limitations built-in.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Ethical Guidelines](#ethical-guidelines)
- [Troubleshooting](#troubleshooting)
- [Project Structure](#project-structure)
- [FAQ](#faq)
- [License](#license)

---

## Overview

This tool helps researchers and students collect small samples of LinkedIn profile data for academic analysis, such as:

- ✅ Finding alumni from specific schools (for career path research)
- ✅ Analyzing job search patterns (academic labor market research)
- ✅ Understanding employment trends (educational outcomes studies)
- ✅ Creating small datasets for coursework or thesis research

### Solution Architecture

```
User → CLI → Web Scraper (Selenium) → LinkedIn → Local Database (SQLite) → Export (CSV/JSON)
```

**Key Components:**
- **Selenium WebDriver**: Automates browser interactions with LinkedIn
- **Rate Limiting**: Built-in delays (5-10 seconds) between requests
- **Session Limits**: Maximum 20 profiles per session for ethical use
- **SQLite Database**: Local storage for collected data
- **Export Tools**: Export to CSV, JSON, or Markdown

---

## Features

- 🔍 **Search by School**: Find profiles of people who studied at a specific institution
- 💼 **Job Status Detection**: Identify who is "Open to Work" vs currently employed
- 💾 **SQLite Database**: Store and manage profiles locally
- 📊 **Statistics**: Analyze job seeking trends among alumni
- 📤 **Export**: Export results to CSV, JSON, or Markdown
- ⚡ **Rate Limiting**: Built-in respectful delays (5-10 seconds between requests)
- 🎨 **Beautiful CLI**: Rich terminal interface with tables and colors
- 🔒 **Secure**: LinkedIn credentials stored in .env file, never in code
- ⚠️ **Ethical Limits**: Hard-coded 20 profile limit per session
- 📝 **Logging**: Comprehensive logging for debugging

---

## Prerequisites

- Python 3.9 or higher
- pip (Python package manager)
- Google Chrome browser (for Selenium WebDriver)
- A LinkedIn account ⚠️ **(account may be at risk of suspension)**
- Basic command line knowledge

---

## Installation

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

This installs:
- `selenium` - Browser automation
- `webdriver-manager` - Automatic Chrome driver management
- `requests` - HTTP client (for future API support)
- `python-dotenv` - Environment variable management
- `pandas` - Data export capabilities
- `rich` - Beautiful CLI output

### Step 4: Install Chrome Browser

Make sure Google Chrome is installed on your system. Selenium will automatically download the appropriate ChromeDriver.

### Step 5: Configure Environment

```bash
# Copy example configuration
cp .env.example .env

# Edit .env file
nano .env  # or use any text editor
```

**Add your LinkedIn credentials:**

```env
SCRAPER_TYPE=web
LINKEDIN_EMAIL=your_email@example.com
LINKEDIN_PASSWORD=your_password
TARGET_SCHOOL=Harvard University
MAX_PROFILES=10
HEADLESS_BROWSER=true
```

⚠️ **Security Note**: Never commit your `.env` file to version control. It's already in `.gitignore`.

### Step 6: Verify Installation

```bash
# Check if everything is installed
python main.py --help
```

---

## Configuration

### Environment Variables (.env)

```env
# ============================================
# SCRAPER CONFIGURATION
# ============================================
SCRAPER_TYPE=web  # Use "web" for web scraping

# ============================================
# WEB SCRAPER CONFIGURATION (Academic Use Only)
# ============================================
LINKEDIN_EMAIL=your_email@example.com
LINKEDIN_PASSWORD=your_password
HEADLESS_BROWSER=true  # Set to false to see the browser

# ============================================
# SEARCH CONFIGURATION
# ============================================
TARGET_SCHOOL=Harvard University
MAX_PROFILES=10  # Max 20 enforced for ethical use

# ============================================
# DATABASE & EXPORT
# ============================================
DATABASE_PATH=./data/profiles.db
EXPORT_FORMAT=csv
EXPORT_PATH=./exports/

# ============================================
# LOGGING
# ============================================
LOG_LEVEL=INFO
LOG_FILE=./logs/scraper.log
```

---

## Usage

### Basic Commands

#### 1. Scrape Profiles from a School (Small Sample)

```bash
python main.py scrape --school "Harvard University" --max-profiles 10
```

**Expected Output:**
```
╔══════════════════════════════════════════════════════════════╗
║          LinkedIn Profile Scraper v2.0.0                     ║
║                                                              ║
║  Mode: Web Scraping (Academic Use)                          ║
║                                                              ║
║  ⚠️  WARNING: Academic/Educational Use Only                 ║
║  ⚠️  May violate LinkedIn Terms of Service                  ║
║  ⚠️  Use at your own risk                                   ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

⚠️  Using Web Scraping Mode - Academic Use Only
⚠️  This may violate LinkedIn's Terms of Service
⚠️  Limited to 20 profiles per session for ethical use

🔍 Searching profiles from Harvard University...
⚠️ Web scraping initialized. Use responsibly for academic purposes only.
✓ Login successful
Found 10 profile URLs
✓ John Doe - employed (1/20)
✓ Jane Smith - seeking (2/20)
...
✓ Saved 10 profiles

📊 Statistics:
┏━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━┳━━━━━━━━━━━━┓
┃ Metric                 ┃ Count ┃ Percentage ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━╇━━━━━━━━━━━━┩
│ Total Profiles         │    10 │       100% │
│ Job Seekers           │     2 │        20% │
│ Employed              │     7 │        70% │
│ Unknown Status        │     1 │        10% │
└────────────────────────┴───────┴────────────┘
```

#### 2. Find Only Job Seekers (Academic Research)

```bash
python main.py scrape --school "MIT" --job-status seeking --max-profiles 5
```

Use Case: Research on career transitions or job market analysis.

#### 3. List Stored Profiles

```bash
python main.py list --school "Harvard University"
```

#### 4. Export to CSV for Analysis

```bash
python main.py export --format csv --output research_data.csv
```

#### 5. Export to JSON

```bash
python main.py export --format json --output research_data.json
```

#### 6. View Statistics

```bash
python main.py stats
```

### Running with Visible Browser (Debugging)

Set `HEADLESS_BROWSER=false` in `.env` to see the browser in action:

```env
HEADLESS_BROWSER=false
```

---

## Ethical Guidelines

### ✅ DO:

- ✅ Use for academic research with small sample sizes (< 20 profiles)
- ✅ Use for educational purposes and learning
- ✅ Respect rate limits and delays
- ✅ Cite data sources in your research
- ✅ Keep data secure and private
- ✅ Delete data when research is complete
- ✅ Use headless mode to reduce server load

### ❌ DON'T:

- ❌ Use for commercial purposes
- ❌ Scrape large volumes of data (>20 profiles per session)
- ❌ Share or sell scraped data
- ❌ Use for spam or unwanted outreach
- ❌ Bypass LinkedIn security measures
- ❌ Run scraper continuously or at high frequency
- ❌ Use multiple accounts to circumvent limits

### Best Practices:

1. **Minimize Impact**: Use the tool sparingly (once per day max)
2. **Small Samples**: Stick to 10-15 profiles for most academic needs
3. **Respect Privacy**: Only collect data that's publicly visible
4. **Data Security**: Encrypt exported data if it contains personal information
5. **Transparency**: Be transparent about your data collection methods in research
6. **Account Safety**: Use a dedicated research account, not your personal account

---

## Troubleshooting

### Common Issues

#### 1. "LINKEDIN_EMAIL and LINKEDIN_PASSWORD are required"

**Problem:** LinkedIn credentials not configured

**Solution:**
```bash
# Edit .env file
nano .env

# Add:
LINKEDIN_EMAIL=your_email@example.com
LINKEDIN_PASSWORD=your_password
```

#### 2. Login Failed

**Possible causes:**
- Incorrect credentials
- LinkedIn security checkpoint (CAPTCHA, 2FA)
- Account flagged for suspicious activity

**Solutions:**
```bash
# Run in non-headless mode to see what's happening
# Edit .env:
HEADLESS_BROWSER=false

# Try logging in manually first
# LinkedIn may require 2FA or CAPTCHA verification
```

#### 3. "No profiles found"

**Possible causes:**
- School name spelling is incorrect
- LinkedIn detected automation
- Search returned no results

**Solutions:**
```bash
# Try exact school name from LinkedIn
python main.py scrape --school "Massachusetts Institute of Technology"

# Check logs for errors
cat logs/scraper.log
```

#### 4. Browser Crashes or Timeout

**Problem:** ChromeDriver issues

**Solutions:**
```bash
# Update Chrome browser to latest version
# Clear cache and try again

# If issue persists, update webdriver-manager:
pip install --upgrade webdriver-manager
```

#### 5. Account Suspended

**Problem:** LinkedIn detected automated activity

**Prevention:**
- Use tool sparingly (max once per day)
- Stick to small sample sizes (< 10 profiles)
- Add longer delays
- Use headless mode
- Don't run multiple sessions in short time

**If it happens:**
- You may need to verify your account
- Consider switching to API-based approach when available
- Use a dedicated research account, not your personal one

### Debug Mode

Enable detailed logging:

```bash
# Edit .env
LOG_LEVEL=DEBUG

# Check logs
tail -f logs/scraper.log
```

---

## Project Structure

```
check-profile/
├── main.py                       # CLI entry point
├── example.py                    # Programmatic usage examples
├── requirements.txt              # Dependencies
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
    │   ├── api_scraper.py        # Proxycurl API (unavailable)
    │   └── web_scraper.py        # Selenium web scraper
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
        ├── rate_limiter.py       # Rate limiting (for API mode)
        ├── logger.py             # Logging setup
        └── export.py             # CSV/JSON/Markdown export
```

---

## FAQ

### Q: Is this legal?

**A:** Web scraping LinkedIn is a gray area and may violate LinkedIn's Terms of Service. This tool is provided for academic and educational purposes only. Users are responsible for complying with applicable laws and regulations. For production use, consider LinkedIn's official API or authorized data providers.

### Q: Will my LinkedIn account get banned?

**A:** There is a risk. LinkedIn actively detects and blocks automated scraping. To minimize risk:
- Use a dedicated research account
- Limit usage to small samples (< 10 profiles)
- Use the tool sparingly (max once per day)
- Respect the built-in rate limits

### Q: Why not use the Proxycurl API?

**A:** The Proxycurl API is the legal and recommended way to access LinkedIn data. However, their API key registration site has been unavailable since 2025. If it becomes available again, we strongly recommend using the API mode instead of web scraping.

### Q: How do I switch to API mode when it's available?

**A:** Simply change your `.env` file:
```env
SCRAPER_TYPE=api
PROXYCURL_API_KEY=your_api_key_here
```

### Q: Can I scrape 100+ profiles?

**A:** No. The tool is hard-coded to limit scraping to 20 profiles per session for ethical use. For large-scale data collection, use official APIs or authorized data providers when available.

### Q: Can I use this for recruitment?

**A:** This tool is for academic research only. For recruitment purposes, use:
- LinkedIn Recruiter (official, paid service)
- LinkedIn Talent Solutions
- Authorized recruiting platforms

### Q: How accurate is the "Open to Work" detection?

**A:** The accuracy depends on LinkedIn's public display settings. Users who make their job-seeking status public will be detected. Private settings won't be captured.

---

## Contributing

Contributions are welcome for:
- Bug fixes
- Documentation improvements
- Enhanced ethical safeguards
- Alternative legal data sources

**Please do NOT contribute:**
- Features that bypass LinkedIn security
- Code to increase scraping limits
- Commercial use features

---

## License

MIT License - See [LICENSE](LICENSE) file for details.

**Use of this software is subject to the disclaimers and warnings above.**

---

## Acknowledgments

- **Selenium** - Browser automation framework
- **Rich** - Beautiful terminal output
- **Python Community** - Amazing open-source tools

---

## Alternatives to Consider

If LinkedIn web scraping doesn't meet your needs, consider:

1. **LinkedIn Official API** (when available for your use case)
2. **RapidAPI LinkedIn alternatives** (when services are available)
3. **Academic data providers** (ICPSR, Harvard Dataverse, etc.)
4. **Survey-based research** (collect data directly from participants)
5. **Public resume databases** (Indeed, Glassdoor, etc.)

---

**Built for ethical academic research and educational purposes**

For questions or issues, please open a GitHub issue. Remember to use responsibly and respect LinkedIn's platform and users' privacy.

---

## Version History

- **v2.0.0** - Web scraping edition (Academic use only)
  - Added Selenium-based web scraper
  - Implemented ethical limits (20 profiles max)
  - Enhanced disclaimers and warnings
  - Original API mode preserved for when Proxycurl becomes available

- **v1.0.0** - API-based edition (Proxycurl API)
  - Legal API-based scraping
  - No longer available due to API key registration issues
