"""Data models for job search tool"""
from enum import Enum
from typing import List, Dict, Optional
from pydantic import BaseModel

class EligibilityStatus(Enum):
    """Job eligibility status"""
    ELIGIBLE = "ELIGIBLE"
    REVIEW = "REVIEW"
    INELIGIBLE = "INELIGIBLE"

class Job(BaseModel):
    """Job posting model"""
    id: str
    title: str
    organization: str
    description: str
    location: str
    job_type: str  # remote, hybrid, onsite
    url: str
    salary_range: Optional[str] = None
    posted_date: Optional[str] = None
    
class JobAssessment(BaseModel):
    """Assessment result for a job"""
    job: Job
    eligibility: EligibilityStatus
    score: float  # 0.0 to 1.0
    keyword_matches: List[str]
    rejection_reasons: List[str]
    language_fit: bool
    location_fit: bool
    
class UserProfile(BaseModel):
    """User profile and constraints"""
    name: str
    citizenship: str
    current_location: str
    working_languages: List[str]
    professional_themes: List[str]
    blocked_patterns: List[str]
    allowed_countries: List[str]
    default_eligibility: str

class ScoringResult(BaseModel):
    """Final scoring result"""
    assessments: List[JobAssessment]
    total_jobs_evaluated: int
    eligible_count: int
    review_count: int
    ineligible_count: int
    top_jobs: List[JobAssessment]