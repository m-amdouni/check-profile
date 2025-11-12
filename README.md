# LinkedIn Profile Scraper

A legal and compliant tool to search and analyze public LinkedIn profiles using **Proxycurl API**. Find alumni from a given high school or university and check their current job status.

## ✅ Legal & Compliant

This tool uses **Proxycurl API**, a legal third-party service that provides LinkedIn data in compliance with Terms of Service. No web scraping or account credentials required.

## Features

- 🔍 **Search by School**: Find profiles of people who studied at a specific institution
- 💼 **Job Status Detection**: Identify who is "Open to Work" vs currently employed
- 💾 **SQLite Database**: Store and manage profiles locally
- 📊 **Statistics**: Analyze job seeking trends among alumni
- 📤 **Export**: Export results to CSV, JSON, or Markdown
- ⚡ **Rate Limiting**: Built-in respectful API usage
- 🎨 **Beautiful CLI**: Rich terminal interface with tables and colors

## Quick Start

### 1. Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd check-profile

# Install dependencies
pip install -r requirements.txt
```

### 2. Get API Key

Sign up for Proxycurl and get your API key:
👉 [https://nubela.co/proxycurl/](https://nubela.co/proxycurl/)

Proxycurl offers a free tier with limited credits to get started.

### 3. Configuration

Create a `.env` file:

```bash
cp .env.example .env
```

Edit `.env` and add your API key:

```env
PROXYCURL_API_KEY=your_api_key_here
TARGET_SCHOOL=Harvard University
MAX_PROFILES=50
```

### 4. Run

```bash
# Search for profiles
python main.py scrape --school "Harvard University" --max-profiles 50

# Find job seekers only
python main.py scrape --school "MIT" --job-status seeking

# View stored profiles
python main.py list --school "Stanford University"

# Export to CSV
python main.py export --format csv --output alumni_report.csv

# Show statistics
python main.py stats
```

## Usage Examples

### Search Alumni from Your School

```bash
python main.py scrape --school "University of California" --max-profiles 100
```

### Find Only Job Seekers

```bash
python main.py scrape --school "MIT" --job-status seeking --max-profiles 30
```

### Export Results

```bash
# Export to CSV
python main.py export --format csv --output job_seekers.csv

# Export to JSON
python main.py export --format json --output profiles.json

# Export specific school only
python main.py export --school "Harvard" --format csv --output harvard_alumni.csv
```

### View Statistics

```bash
python main.py stats
```

Output example:
```
📊 Statistics:
┏━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━┳━━━━━━━━━━━━┓
┃ Metric                 ┃ Count ┃ Percentage ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━╇━━━━━━━━━━━━┩
│ Total Profiles         │    50 │       100% │
│ Job Seekers           │    12 │        24% │
│ Employed              │    35 │        70% │
│ Unknown Status        │     3 │         6% │
└────────────────────────┴───────┴────────────┘
```

## Project Structure

```
check-profile/
├── src/
│   ├── scrapers/
│   │   └── api_scraper.py       # Proxycurl API integration
│   ├── database/
│   │   ├── models.py             # Profile data model
│   │   └── db_manager.py         # SQLite operations
│   ├── filters/
│   │   └── profile_filter.py     # Filter and analyze profiles
│   └── utils/
│       ├── config.py             # Configuration management
│       ├── rate_limiter.py       # API rate limiting
│       ├── logger.py             # Logging setup
│       └── export.py             # Export utilities
├── main.py                       # CLI entry point
├── requirements.txt              # Python dependencies
├── .env.example                  # Example configuration
└── README.md
```

## CLI Commands

### `scrape` - Search and scrape profiles

```bash
python main.py scrape --school "SCHOOL_NAME" [OPTIONS]

Options:
  --school TEXT         School/university name (required)
  --max-profiles INT    Maximum profiles to scrape (default: 50)
  --job-status TEXT     Filter: seeking | employed | unknown
```

### `list` - View profiles from database

```bash
python main.py list [OPTIONS]

Options:
  --school TEXT         Filter by school name
  --job-status TEXT     Filter: seeking | employed | unknown
```

### `export` - Export profiles

```bash
python main.py export --output FILE [OPTIONS]

Options:
  --format TEXT         Format: csv | json | markdown (default: csv)
  --output TEXT         Output file path (required)
  --school TEXT         Filter by school
  --job-status TEXT     Filter: seeking | employed | unknown
```

### `stats` - Show statistics

```bash
python main.py stats
```

## Data Model

Each profile contains:

```python
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
  "about": "Passionate about...",
  "connections": 500,
  "scraped_at": "2025-11-12T10:00:00Z"
}
```

## Configuration Options

### Environment Variables (.env)

```env
# Proxycurl API Key (Required)
PROXYCURL_API_KEY=your_api_key_here

# Search Configuration
TARGET_SCHOOL=Harvard University
MAX_PROFILES=50
SEARCH_KEYWORDS=

# Rate Limiting
REQUESTS_PER_MINUTE=10
DELAY_BETWEEN_REQUESTS=6

# Database
DATABASE_PATH=./data/profiles.db

# Export
EXPORT_FORMAT=csv
EXPORT_PATH=./exports/

# Logging
LOG_LEVEL=INFO
LOG_FILE=./logs/scraper.log
```

## Pricing

### Proxycurl API

- **Free Tier**: Limited credits to get started
- **Starter**: $79/month - 3,000 credits
- **Professional**: $249/month - 10,000 credits
- **Business**: Custom pricing

Each profile lookup typically costs 1-2 credits.

👉 [View Proxycurl Pricing](https://nubela.co/proxycurl/pricing)

## Use Cases

1. **Recruitment**: Find alumni from target schools who are job seeking
2. **Networking**: Connect with fellow alumni based on job status
3. **Market Research**: Analyze career paths of school alumni
4. **Career Services**: Help universities understand alumni employment
5. **Talent Mapping**: Identify talent pools from specific institutions

## FAQ

### Q: Is this legal?

**A:** Yes! This tool uses Proxycurl API, which provides LinkedIn data through legal means. No ToS violations or web scraping involved.

### Q: Do I need a LinkedIn account?

**A:** No! Proxycurl handles data access through their API. No LinkedIn credentials needed.

### Q: How accurate is the "Open to Work" detection?

**A:** Proxycurl extracts this directly from public LinkedIn profiles. It's as accurate as the data users make public.

### Q: Can I scrape my own LinkedIn connections?

**A:** This tool focuses on public search by school. For connections, use LinkedIn's official API.

### Q: How many profiles can I scrape?

**A:** Limited by your Proxycurl API plan. Start with the free tier to test.

## Ethical Guidelines

1. ✅ Use for legitimate recruitment or research purposes
2. ✅ Respect individuals' privacy settings
3. ✅ Store data securely
4. ✅ Delete data when no longer needed
5. ❌ Don't spam or harass individuals found through this tool
6. ❌ Don't sell or share personal data
7. ❌ Don't use for discriminatory purposes

## Troubleshooting

### "PROXYCURL_API_KEY is required"

Make sure you've created a `.env` file with your API key:
```env
PROXYCURL_API_KEY=your_actual_key_here
```

### "No profiles found"

- Check the school name spelling
- Try a more common school name format (e.g., "Harvard University" not "Harvard")
- Verify your API key has remaining credits

### Rate Limiting

If you hit rate limits, adjust in `.env`:
```env
REQUESTS_PER_MINUTE=5
DELAY_BETWEEN_REQUESTS=12
```

## Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Add tests for new features
4. Submit a pull request

## License

MIT License - See LICENSE file

## Support

- 📧 Email: support@example.com
- 🐛 Issues: [GitHub Issues](https://github.com/yourusername/check-profile/issues)
- 📚 Proxycurl Docs: [https://nubela.co/proxycurl/docs](https://nubela.co/proxycurl/docs)

## Acknowledgments

- **Proxycurl** for providing legal LinkedIn data access
- **Rich** library for beautiful terminal output
- Contributors and users of this tool

---

**Built with ❤️ for ethical recruitment and career research**
