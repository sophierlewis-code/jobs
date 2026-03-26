#!/usr/bin/env python3
"""
Job Search Tool - Main Entry Point

Orchestrates the entire job search workflow:
1. Load user profile and configuration
2. Fetch jobs from sources
3. Score and filter jobs
4. Output results
"""

import json
import yaml
from pathlib import Path
from datetime import datetime
from typing import List, Tuple
import pandas as pd

from src.models import Job, UserProfile, ScoringResult
from src.job_fetcher import JobFetcher
from src.job_scorer import JobScorer

def load_user_profile(config_path: str = "config/user_profile.yaml") -> Tuple[UserProfile, dict]:
    """Load user profile from YAML config"""
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    
    profile = UserProfile(
        name=config['personal']['name'],
        citizenship=config['personal']['citizenship'],
        current_location=config['personal']['current_location'],
        working_languages=config['language']['working_languages'],
        professional_themes=config['professional_fit']['themes'],
        blocked_patterns=config['work_authorization']['blocked_patterns'],
        allowed_countries=config['work_authorization']['allowed_countries'],
        default_eligibility=config['work_authorization']['default_eligibility']
    )
    
    keyword_boosts = config['scoring']['keyword_boosts']
    
    return profile, keyword_boosts

def load_jobs() -> List[Job]:
    """Load jobs from sources"""
    print("📥 Loading jobs...")
    return JobFetcher.get_sample_jobs()

def score_jobs(jobs: List[Job], profile: UserProfile, keyword_boosts: dict) -> ScoringResult:
    """Score and filter jobs"""
    print("🎯 Scoring jobs...")
    
    scorer = JobScorer(profile, keyword_boosts)
    assessments = scorer.score_batch(jobs)
    
    # Count by status
    eligible = [a for a in assessments if a.eligibility.value == "ELIGIBLE"]
    review = [a for a in assessments if a.eligibility.value == "REVIEW"]
    ineligible = [a for a in assessments if a.eligibility.value == "INELIGIBLE"]
    
    # Get top jobs
    top_jobs = sorted(
        [a for a in assessments if a.eligibility.value in ["ELIGIBLE", "REVIEW"]],
        key=lambda x: x.score,
        reverse=True
    )[:10]
    
    return ScoringResult(
        assessments=assessments,
        total_jobs_evaluated=len(jobs),
        eligible_count=len(eligible),
        review_count=len(review),
        ineligible_count=len(ineligible),
        top_jobs=top_jobs
    )

def save_raw_json(result: ScoringResult, output_path: str = "output/jobs_raw.json"):
    """Save raw job data to JSON"""
    print(f"💾 Saving raw data to {output_path}...")
    
    data = {
        'generated_at': datetime.now().isoformat(),
        'summary': {
            'total_evaluated': result.total_jobs_evaluated,
            'eligible': result.eligible_count,
            'review': result.review_count,
            'ineligible': result.ineligible_count
        },
        'jobs': []
    }
    
    for assessment in result.assessments:
        data['jobs'].append({
            'id': assessment.job.id,
            'title': assessment.job.title,
            'organization': assessment.job.organization,
            'location': assessment.job.location,
            'job_type': assessment.job.job_type,
            'url': assessment.job.url,
            'salary_range': assessment.job.salary_range,
            'description': assessment.job.description,
            'eligibility': assessment.eligibility.value,
            'score': assessment.score,
            'keyword_matches': assessment.keyword_matches,
            'rejection_reasons': assessment.rejection_reasons,
            'language_fit': assessment.language_fit,
            'location_fit': assessment.location_fit
        })
    
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w') as f:
        json.dump(data, f, indent=2)

def save_filtered_csv(result: ScoringResult, output_path: str = "output/jobs_filtered.csv"):
    """Save filtered jobs to CSV"""
    print(f"📊 Saving filtered data to {output_path}...")
    
    rows = []
    for assessment in result.assessments:
        rows.append({
            'Job_ID': assessment.job.id,
            'Title': assessment.job.title,
            'Organization': assessment.job.organization,
            'Location': assessment.job.location,
            'Job_Type': assessment.job.job_type,
            'Salary_Range': assessment.job.salary_range,
            'Eligibility': assessment.eligibility.value,
            'Score': assessment.score,
            'Keywords_Matched': '; '.join(assessment.keyword_matches),
            'Rejection_Reasons': '; '.join(assessment.rejection_reasons),
            'Language_Fit': 'Yes' if assessment.language_fit else 'No',
            'Location_Fit': 'Yes' if assessment.location_fit else 'No',
            'URL': assessment.job.url
        })
    
    df = pd.DataFrame(rows)
    df = df.sort_values('Score', ascending=False)
    
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)

def save_shortlist_markdown(result: ScoringResult, output_path: str = "output/shortlist.md"):
    """Save shortlist to Markdown"""
    print(f"📝 Saving shortlist to {output_path}...")
    
    with open(output_path, 'w') as f:
        f.write("# Job Search Shortlist\n\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        f.write("## Summary\n\n")
        f.write(f"- **Total Jobs Evaluated**: {result.total_jobs_evaluated}\n")
        f.write(f"- **Eligible**: {result.eligible_count}\n")
        f.write(f"- **Review**: {result.review_count}\n")
        f.write(f"- **Ineligible**: {result.ineligible_count}\n\n")
        
        f.write("## Top Opportunities\n\n")
        
        for idx, assessment in enumerate(result.top_jobs, 1):
            job = assessment.job
            f.write(f"### {idx}. {job.title}\n\n")
            f.write(f"**Organization**: {job.organization}\n\n")
            f.write(f"**Location**: {job.location} ({job.job_type})\n\n")
            f.write(f"**Score**: {assessment.score:.2f}/1.00\n\n")
            f.write(f"**Status**: {assessment.eligibility.value}\n\n")
            f.write(f"**Salary**: {job.salary_range or 'Not specified'}\n\n")
            
            if assessment.keyword_matches:
                f.write(f"**Matching Keywords**: {', '.join(assessment.keyword_matches)}\n\n")
            
            if assessment.rejection_reasons:
                f.write(f"**Concerns**: {', '.join(assessment.rejection_reasons)}\n\n")
            
            f.write(f"**URL**: [{job.url}]({job.url})\n\n")
            f.write("---\n\n")

def print_summary(result: ScoringResult):
    """Print summary to console"""
    print("\n" + "="*60)
    print("JOB SEARCH RESULTS")
    print("="*60)
    print(f"\n📊 Summary:")
    print(f"   Total Jobs Evaluated: {result.total_jobs_evaluated}")
    print(f"   ✅ Eligible: {result.eligible_count}")
    print(f"   ⏳ Review: {result.review_count}")
    print(f"   ❌ Ineligible: {result.ineligible_count}")
    
    print(f"\n🎯 Top Opportunities:")
    for idx, assessment in enumerate(result.top_jobs[:5], 1):
        print(f"\n   {idx}. {assessment.job.title}")
        print(f"      Organization: {assessment.job.organization}")
        print(f"      Score: {assessment.score:.2f} | Status: {assessment.eligibility.value}")
    
    print("\n" + "="*60 + "\n")

def main():
    """Main entry point"""
    print("\n🚀 Job Search Tool Started\n")
    
    # Load configuration
    print("⚙️  Loading configuration...")
    profile, keyword_boosts = load_user_profile()
    print(f"   User: {profile.name}")
    print(f"   Location: {profile.current_location}")
    print(f"   Citizenship: {profile.citizenship}\n")
    
    # Load jobs
    jobs = load_jobs()
    print(f"   Loaded {len(jobs)} jobs\n")
    
    # Score jobs
    result = score_jobs(jobs, profile, keyword_boosts)
    
    # Save outputs
    save_raw_json(result)
    save_filtered_csv(result)
    save_shortlist_markdown(result)
    
    # Print summary
    print_summary(result)
    
    print("✨ Job search complete!")
    print(f"📁 Results saved to output/ folder")
    print(f"   - jobs_raw.json")
    print(f"   - jobs_filtered.csv")
    print(f"   - shortlist.md\n")

if __name__ == "__main__":
    main()