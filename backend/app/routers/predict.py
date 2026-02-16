"""
Prediction endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException, status, Header
from google.cloud.firestore import Client
from typing import Optional

from app.dependencies import get_db
from app.schemas.crop import CropPredictionRequest, CropPredictionResponse
from app.services.weather_service import WeatherService
from app.services.prediction_service import PredictionService
from app.utils.jwt import JWTHandler
from app.utils.logger import logger

router = APIRouter(prefix="/predict", tags=["Prediction"])


async def get_current_user(authorization: Optional[str] = Header(None)) -> Optional[str]:
    """
    Extract user ID from JWT token (optional authentication).
    
    Args:
        authorization: Authorization header
        
    Returns:
        User ID if authenticated, None otherwise
    """
    if not authorization or not authorization.startswith("Bearer "):
        return None
    
    token = authorization.replace("Bearer ", "")
    payload = JWTHandler.verify_token(token)
    
    if payload:
        return payload.get("user_id")
    
    return None


@router.post("/crop", response_model=CropPredictionResponse)
async def predict_crop(
    request: CropPredictionRequest,
    db: Client = Depends(get_db),
    user_id: Optional[str] = Depends(get_current_user)
):
    """
    Predict crop recommendation based on soil and weather data.
    
    Args:
        request: Crop prediction request
        db: Firestore client
        user_id: User ID (optional, from JWT)
        
    Returns:
        Crop recommendations with yield and price
    """
    try:
        logger.info(f"Crop prediction request from user: {user_id or 'anonymous'}")
        
        # Step 1: Fetch weather data
        logger.info(f"Fetching weather for location: {request.location}")
        weather_data = await WeatherService.get_weather(request.location)
        
        # Step 2: Call ML prediction service
        prediction_result = await PredictionService.predict_crop_recommendation(
            N=request.N,
            P=request.P,
            K=request.K,
            soil_type=request.soilType,
            season=request.season,
            temperature=weather_data['temperature'],
            humidity=weather_data['humidity'],
            rainfall=weather_data['rainfall']
        )
        
        # Step 3: Store prediction history (if user is authenticated)
        if user_id:
            try:
                history_entry = PredictionService.create_prediction_history_entry(
                    user_id=user_id,
                    input_data={
                        'soilType': request.soilType,
                        'season': request.season,
                        'N': request.N,
                        'P': request.P,
                        'K': request.K,
                        'location': request.location,
                        'weather': weather_data
                    },
                    result_data=prediction_result
                )
                
                db.collection('prediction_history').add(history_entry)
                logger.info(f"Prediction history saved for user: {user_id}")
            
            except Exception as e:
                logger.error(f"Failed to save prediction history: {str(e)}")
                # Don't fail the request if history save fails
        
        # Step 4: Return prediction result
        return CropPredictionResponse(**prediction_result)
    
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Prediction failed: {str(e)}"
        )
