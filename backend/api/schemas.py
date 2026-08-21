from pydantic import BaseModel, Field
from typing import List

class PredictRequest(BaseModel):
    text: str = Field(..., min_length=5, max_length=1500, description="The situation to analyze")

class PredictResponse(BaseModel):
    needs_more_context: bool = False
    cooked_score: int = 0
    cooked_level: str = ""
    level_int: int = 0
    confidence: float = 0.0
    category: str = ""
    urgency: int = 0
    preparation: int = 0
    consequences: int = 0
    recoverability: int = 0
    key_factors: List[str] = Field(default_factory=list)
    reasons: List[str] = Field(default_factory=list) # kept for backward compatibility with baseline
    verdict: str = ""
    recommendations: List[str] = Field(default_factory=list)

class SituationAnalysis(BaseModel):
    needs_more_context: bool = Field(False, description="Set to true if there is not enough information to judge the situation")
    category: str = Field(..., description="academic, career, financial, relationship, coding, deadline, personal, or other")
    urgency: int = Field(..., ge=0, le=10)
    preparation: int = Field(..., ge=0, le=10)
    consequences: int = Field(..., ge=0, le=10)
    recoverability: int = Field(..., ge=0, le=10)
    time_remaining: str
    key_factors: List[str]
    explicit_facts: List[str]
    uncertainties: List[str]
    confidence: float = Field(..., ge=0.0, le=1.0)
    interpretation_notes: str = ""
