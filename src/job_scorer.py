"""Job scoring and eligibility assessment engine"""
from typing import List, Dict, Tuple
import re
from src.models import Job, JobAssessment, EligibilityStatus, UserProfile

class JobScorer:
    """Score and filter jobs based on user profile"""
    
    def __init__(self, user_profile: UserProfile, keyword_boosts: Dict[str, float]):
        self.profile = user_profile
        self.keyword_boosts = keyword_boosts
        
    def assess_job(self, job: Job) -> JobAssessment:
        """Assess a single job against user profile"""
        # Check eligibility first
        eligibility, rejection_reasons = self._check_eligibility(job)
        
        # Calculate score
        score = self._calculate_score(job, eligibility)
        
        # Find keyword matches
        keyword_matches = self._find_keyword_matches(job)
        
        # Language fit
        language_fit = self._check_language_fit(job)
        
        # Location fit
        location_fit = self._check_location_fit(job)
        
        return JobAssessment(
            job=job,
            eligibility=eligibility,
            score=score,
            keyword_matches=keyword_matches,
            rejection_reasons=rejection_reasons,
            language_fit=language_fit,
            location_fit=location_fit
        )
    
    def _check_eligibility(self, job: Job) -> Tuple[EligibilityStatus, List[str]]:
        """Check if job meets basic eligibility criteria"""
        rejection_reasons = []
        
        # Check for blocked patterns
        job_text = f"{job.title} {job.description} {job.location}".lower()
        for pattern in self.profile.blocked_patterns:
            if pattern.lower() in job_text:
                rejection_reasons.append(f"Blocked pattern: {pattern}")
                return EligibilityStatus.INELIGIBLE, rejection_reasons
        
        # Check location requirements
        if job.job_type.lower() not in ["remote", "home-based", "work from anywhere"]:
            # If not remote, check if location is allowed
            location_lower = job.location.lower()
            allowed = any(
                country.lower() in location_lower 
                for country in self.profile.allowed_countries
            )
            if not allowed:
                rejection_reasons.append(f"Location {job.location} not in allowed countries")
                return EligibilityStatus.INELIGIBLE, rejection_reasons
        
        # Check language requirements
        job_text_lower = job.description.lower()
        if "fluent thai" in job_text_lower or "native thai" in job_text_lower:
            if "thai" not in [l.lower() for l in self.profile.working_languages]:
                rejection_reasons.append("Requires fluent Thai")
                return EligibilityStatus.INELIGIBLE, rejection_reasons
        
        # If no rejection reasons, mark as eligible with optional review
        if len(rejection_reasons) == 0:
            if self.profile.default_eligibility == "REVIEW":
                return EligibilityStatus.REVIEW, []
            return EligibilityStatus.ELIGIBLE, []
        
        return EligibilityStatus.REVIEW, rejection_reasons
    
    def _calculate_score(self, job: Job, eligibility: EligibilityStatus) -> float:
        """Calculate job match score (0.0 to 1.0)"""
        base_score = 0.5  # Start with 0.5
        
        # Apply eligibility multiplier
        if eligibility == EligibilityStatus.ELIGIBLE:
            base_score *= 1.0
        elif eligibility == EligibilityStatus.REVIEW:
            base_score *= 0.5
        else:
            return 0.0
        
        # Add keyword match boost
        keyword_boost = self._calculate_keyword_boost(job)
        base_score = min(1.0, base_score + keyword_boost * 0.3)
        
        # Remote bonus
        if job.job_type.lower() in ["remote", "work from anywhere", "home-based"]:
            base_score = min(1.0, base_score + 0.15)
        
        # Relevant location bonus
        if "southeast asia" in job.location.lower() or job.location.lower() in ["international", "global"]:
            base_score = min(1.0, base_score + 0.10)
        
        return base_score
    
    def _calculate_keyword_boost(self, job: Job) -> float:
        """Calculate boost from keyword matches"""
        matches = self._find_keyword_matches(job)
        return min(1.0, len(matches) * 0.15)
    
    def _find_keyword_matches(self, job: Job) -> List[str]:
        """Find matching keywords in job"""
        job_text = f"{job.title} {job.description}".lower()
        matches = []
        
        for keyword, boost in self.keyword_boosts.items():
            if keyword.lower() in job_text:
                matches.append(keyword)
        
        return list(set(matches))
    
    def _check_language_fit(self, job: Job) -> bool:
        """Check if job language requirements match profile"""
        job_text = f"{job.title} {job.description}".lower()
        
        # Check for language requirements
        for lang in self.profile.working_languages:
            if lang.lower() in job_text:
                return True
        
        # If no specific language requirement, assume fit
        if "english" in job_text or "english" not in job_text:
            return True
        
        return False
    
    def _check_location_fit(self, job: Job) -> bool:
        """Check if job location matches profile"""
        location_lower = job.location.lower()
        
        for country in self.profile.allowed_countries:
            if country.lower() in location_lower:
                return True
        
        if job.job_type.lower() in ["remote", "work from anywhere", "home-based", "international", "global"]:
            return True
        
        return False
    
    def score_batch(self, jobs: List[Job]) -> List[JobAssessment]:
        """Score multiple jobs"""
        return [self.assess_job(job) for job in jobs]