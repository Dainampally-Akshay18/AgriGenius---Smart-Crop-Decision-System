"""
Crop prediction request/response schemas.
"""
from pydantic import BaseModel, Field
from typing import List


class CropPredictionRequest(BaseModel):
    """Crop prediction request."""
    
    soilType: str = Field(..., description="Soil type (e.g., Black, Red, Alluvial)")
    season: str = Field(..., description="Season (e.g., Kharif, Rabi, Summer)")
    N: float = Field(..., ge=0, le=140, description="Nitrogen content (0-140)")
    P: float = Field(..., ge=0, le=140, description="Phosphorus content (0-140)")
    K: float = Field(..., ge=0, le=140, description="Potassium content (0-140)")
    location: str = Field(..., min_length=2, description="Location/city name")


class CropRecommendation(BaseModel):
    """Single crop recommendation."""
    
    crop: str
    yield_percentage: int = Field(..., alias="yield")
    price: float


class CropPredictionResponse(BaseModel):
    """Crop prediction response."""
    
    recommendedCrops: List[CropRecommendation]
    
    class Config:
        populate_by_name = True
