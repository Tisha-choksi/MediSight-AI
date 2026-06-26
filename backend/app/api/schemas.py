from pydantic import BaseModel
from typing import Optional


class QualityResponse(BaseModel):
    quality_score: float
    status: str
    reason: Optional[str] = None


class PredictionResponse(BaseModel):
    prediction: str
    confidence: float


class ExplanationResponse(BaseModel):
    explanation_image: str


class MetricsResponse(BaseModel):
    accuracy: float
    precision: float
    recall: float
    f1: float
    roc_auc: float


class ExperimentResponse(BaseModel):
    id: str
    model_name: str
    accuracy: float
    created_at: str
