from enum import Enum
from pydantic import BaseModel

class EligibilityStatus(Enum):
    ELIGIBLE = "eligible"
    INELIGIBLE = "ineligible"
    PENDING = "pending"

class Job(BaseModel):
    id: int
    title: str
    description: str
    location: str
    salary: float

class JobAssessment(BaseModel):
    job_id: int
    assessment_date: str
    score: float
    status: EligibilityStatus

class AssessmentSummary(BaseModel):
    job_id: int
    total_assessments: int
    average_score: float
    eligibility_status: EligibilityStatus