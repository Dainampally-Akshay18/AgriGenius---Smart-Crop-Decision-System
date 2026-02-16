"""
Evaluation request/response schemas.
"""
from pydantic import BaseModel, Field
from typing import Dict, Optional, List


class EvaluationRequest(BaseModel):
    """Evaluation request (same as crop prediction)."""
    
    soilType: str = Field(..., description="Soil type")
    season: str = Field(..., description="Season")
    N: float = Field(..., ge=0, le=140, description="Nitrogen content")
    P: float = Field(..., ge=0, le=140, description="Phosphorus content")
    K: float = Field(..., ge=0, le=140, description="Potassium content")
    location: str = Field(..., min_length=2, description="Location/city name")


class NoiseEvaluationResponse(BaseModel):
    """Noise injection evaluation response."""
    
    predicted_crop: str
    rss: float = Field(..., description="Recommendation Stability Score")
    prediction_changes: int
    total_runs: int
    noise_percentage: float
    prediction_distribution: Dict[str, int]


class MissingFeatureEvaluationResponse(BaseModel):
    """Missing feature evaluation response."""
    
    predicted_crop: str
    baseline_confidence: float
    stability_score: float
    total_tests: int
    prediction_changes: int
    feature_results: Dict[str, Dict]


class AgreementEvaluationResponse(BaseModel):
    """Model agreement evaluation response."""
    
    predicted_crop: str
    total_models: int
    agreement_ratio: float
    all_agree: bool
    predictions: Dict[str, str]
    prediction_distribution: Dict[str, int]


class FullEvaluationResponse(BaseModel):
    """Full evaluation response with all metrics."""
    
    predicted_crop: str
    confidence: float
    confidence_level: str
    
    # Confidence components
    probability: float
    stability: Optional[float]
    agreement: Optional[float]
    
    # Robustness metrics
    rss_score: float
    missing_feature_stability: float
    model_agreement_ratio: float
    
    # Detailed results
    noise_test: Dict
    missing_feature_test: Dict
    model_agreement_test: Dict
