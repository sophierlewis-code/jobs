# Sophie's Job Search Tool

A Python tool to search job websites, filter by legal eligibility, and rank opportunities against your CV and professional fit.

## Features

✅ **Legal Eligibility Filtering**: Automatically rejects jobs you can't apply for (Thai nationals only, fluent Thai required, onsite Thailand, etc.)

✅ **Remote-First**: Prioritizes remote, work-from-anywhere, and international consultant roles

✅ **Keyword Matching**: Scores jobs based on your professional themes (forest governance, land rights, MEL, etc.)

✅ **Multi-Format Output**:
- `jobs_raw.json` - Complete data with all assessments
- `jobs_filtered.csv` - Sortable spreadsheet of all jobs
- `shortlist.md` - Top opportunities formatted for review

## Setup

### 1. Clone/Open Repository
```bash
cd jobs
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Your Profile
Edit `config/user_profile.yaml` with your details:
- Personal info (name, citizenship, location)
- Work authorization rules
- Professional themes and interests
- Keyword scoring weights

### 4. Add Your CV
Place your CV PDF at `Sophie Rose Lewis_CV_2026.pdf` (already in repo)

### 5. Run the Tool
```bash
python main.py
```

## Project Structure

```
.
├── config/
│   └── user_profile.yaml          # Your profile and constraints
├── src/
│   ├── models.py                  # Pydantic data models
│   ├── job_scorer.py              # Eligibility & scoring logic
│   ├── job_fetcher.py             # Job source adapters
│   ├── cv_parser.py               # CV keyword extraction
│   └── bookmark_parser.py         # HTML bookmark parser
├── output/
│   ├── jobs_raw.json              # All jobs with scores
│   ├── jobs_filtered.csv          # Spreadsheet format
│   └── shortlist.md               # Top opportunities
├── main.py                        # Entry point
├── requirements.txt               # Dependencies
└── README.md                      # This file
```

## Configuration

### user_profile.yaml

**Work Authorization**:
```yaml
allowed_countries:
  - "UK"
  - "Remote"
  - "International"

blocked_patterns:
  - "Thai nationals only"
  - "Thai citizenship required"
  - "Fluent Thai required"
  - "must already hold Thai work permit"
```

**Professional Fit**:
```yaml
themes:
  - "Forest governance"
  - "Land and resource rights"
  - "Tenure"
  - "MEL"
  - "Donor reporting"
```

**Keyword Scoring**:
```yaml
keyword_boosts:
  forest: 0.15
  forestry: 0.15
  land: 0.15
  tenure: 0.15
  indigenous: 0.12
  mel: 0.12
  remote: 0.20
```

## How It Works

### 1. **Eligibility Check** (ELIGIBLE/REVIEW/INELIGIBLE)
   - ❌ INELIGIBLE if blocked patterns match
   - ❌ INELIGIBLE if location not allowed and job is onsite
   - ❌ INELIGIBLE if requires fluent Thai
   - ⏳ REVIEW if no information about location/language
   - ✅ ELIGIBLE if passes all checks

### 2. **Score Calculation** (0.0 - 1.0)
   - Base: 0.5
   - Eligibility: ×1.0 (ELIGIBLE), ×0.5 (REVIEW), ×0.0 (INELIGIBLE)
   - Keywords: +0.3 boost per match
   - Remote: +0.15 bonus
   - Southeast Asia: +0.10 bonus
   - Max: 1.0

### 3. **Output**
   - Jobs sorted by score (highest first)
   - Markdown shortlist with top opportunities
   - CSV for filtering/sorting
   - JSON for programmatic access

## Usage Examples

### Run locally
```bash
python main.py
```

### Use programmatically
```python
from src.job_fetcher import JobFetcher
from src.job_scorer import JobScorer
from src.models import UserProfile
import yaml

# Load profile
with open('config/user_profile.yaml') as f:
    config = yaml.safe_load(f)

profile = UserProfile(...)
jobs = JobFetcher.get_sample_jobs()
scorer = JobScorer(profile, config['scoring']['keyword_boosts'])
assessments = scorer.score_batch(jobs)
```

## Next Steps

1. **Add Real Job Sources**:
   - ReliefWeb API for NGO jobs
   - LinkedIn Job API
   - DevEx for development roles
   - Custom web scrapers

2. **Expand CV Parsing**:
   - Extract experience years
   - Parse education section
   - Map CV skills to job requirements

3. **Add Email Alerts**:
   - Subscribe to new jobs matching criteria
   - Daily digest of top opportunities

4. **Job Application Tracking**:
   - Track which jobs you've applied to
   - Status updates (applied, interviewed, rejected, offer)

## Notes

- Tool uses **sample job data** by default. Add real APIs in `src/job_fetcher.py`
- CV parsing extracts keywords from PDF. Accuracy depends on CV format
- Eligibility is conservative: when in doubt, marks as REVIEW
- All outputs overwritten on each run (consider adding versioning)

## Questions?

Edit `config/user_profile.yaml` to customize filtering rules. Look at `src/job_scorer.py` to modify scoring logic.