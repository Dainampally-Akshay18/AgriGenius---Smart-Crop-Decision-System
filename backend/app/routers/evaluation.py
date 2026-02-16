"""
Robustness evaluation endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException, status, Header
from google.cloud.firestore import Client
from typing import Optional

from app.dependencies import get_db
from app.schemas.evaluation import (
    EvaluationRequest,
    NoiseEvaluationResponse,
    MissingFeatureEvaluationResponse,
    AgreementEvaluationResponse,
    FullEvaluationResponse
)
from app.services.weather_service import WeatherService
from app.services.evaluation_service import EvaluationService
from app.utils.jwt import JWTHandler
from app.utils.logger import logger

router = APIRouter(prefix="/evaluate", tags=["Evaluation"])


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


@router.post("/noise", response_model=NoiseEvaluationResponse)
async def evaluate_noise(
    request: EvaluationRequest,
    db: Client = Depends(get_db),
    user_id: Optional[str] = Depends(get_current_user)
):
    """
    Evaluate prediction stability under noise perturbations.
    
    Runs prediction multiple times with noisy inputs and computes
    Recommendation Stability Score (RSS).
    
    Args:
        request: Evaluation request with crop parameters
        db: Firestore client
        user_id: User ID (optional, from JWT)
        
    Returns:
        RSS and noise test results
    """
    try:
        logger.info(f"Noise evaluation request from user: {user_id or 'anonymous'}")
        
        # Fetch weather data
        weather_data = await WeatherService.get_weather(request.location)
        
        # Run noise evaluation
        result = await EvaluationService.evaluate_noise(
            N=request.N,
            P=request.P,
            K=request.K,
            temperature=weather_data['temperature'],
            humidity=weather_data['humidity'],
            rainfall=weather_data['rainfall']
        )
        
        # Store evaluation history (if authenticated)
        if user_id:
            try:
                history_entry = EvaluationService.create_evaluation_history_entry(
                    user_id=user_id,
                    evaluation_type='noise',
                    input_data={
                        'soilType': request.soilType,
                        'season': request.season,
                        'N': request.N,
                        'P': request.P,
                        'K': request.K,
                        'location': request.location,
                        'weather': weather_data
                    },
                    result_data=result
                )
                db.collection('evaluation_history').add(history_entry)
                logger.info(f"Evaluation history saved for user: {user_id}")
            except Exception as e:
                logger.error(f"Failed to save evaluation history: {str(e)}")
        
        return NoiseEvaluationResponse(**result)
    
    except Exception as e:
        logger.error(f"Noise evaluation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Noise evaluation failed: {str(e)}"
        )


@router.post("/missing", response_model=MissingFeatureEvaluationResponse)
async def evaluate_missing_features(
    request: EvaluationRequest,
    db: Client = Depends(get_db),
    user_id: Optional[str] = Depends(get_current_user)
):
    """
    Evaluate prediction robustness when features are missing.
    
    Tests prediction with each feature removed one at a time.
    
    Args:
        request: Evaluation request with crop parameters
        db: Firestore client
        user_id: User ID (optional, from JWT)
        
    Returns:
        Missing feature test results
    """
    try:
        logger.info(f"Missing feature evaluation request from user: {user_id or 'anonymous'}")
        
        # Fetch weather data
        weather_data = await WeatherService.get_weather(request.location)
        
        # Run missing feature evaluation
        result = await EvaluationService.evaluate_missing_features(
            N=request.N,
            P=request.P,
            K=request.K,
            temperature=weather_data['temperature'],
            humidity=weather_data['humidity'],
            rainfall=weather_data['rainfall']
        )
        
        # Store evaluation history (if authenticated)
        if user_id:
            try:
                history_entry = EvaluationService.create_evaluation_history_entry(
                    user_id=user_id,
                    evaluation_type='missing',
                    input_data={
                        'soilType': request.soilType,
                        'season': request.season,
                        'N': request.N,
                        'P': request.P,
                        'K': request.K,
                        'location': request.location,
                        'weather': weather_data
                    },
                    result_data=result
                )
                db.collection('evaluation_history').add(history_entry)
            except Exception as e:
                logger.error(f"Failed to save evaluation history: {str(e)}")
        
        return MissingFeatureEvaluationResponse(**result)
    
    except Exception as e:
        logger.error(f"Missing feature evaluation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Missing feature evaluation failed: {str(e)}"
        )


@router.post("/agreement", response_model=AgreementEvaluationResponse)
async def evaluate_model_agreement(
    request: EvaluationRequest,
    db: Client = Depends(get_db),
    user_id: Optional[str] = Depends(get_current_user)
):
    """
    Evaluate agreement across multiple models.
    
    Compares predictions from Random Forest, XGBoost, SVM, and MLP.
    
    Args:
        request: Evaluation request with crop parameters
        db: Firestore client
        user_id: User ID (optional, from JWT)
        
    Returns:
        Model agreement results
    """
    try:
        logger.info(f"Model agreement evaluation request from user: {user_id or 'anonymous'}")
        
        # Fetch weather data
        weather_data = await WeatherService.get_weather(request.location)
        
        # Run agreement evaluation
        result = await EvaluationService.evaluate_agreement(
            N=request.N,
            P=request.P,
            K=request.K,
            temperature=weather_data['temperature'],
            humidity=weather_data['humidity'],
            rainfall=weather_data['rainfall']
        )
        
        # Store evaluation history (if authenticated)
        if user_id:
            try:
                history_entry = EvaluationService.create_evaluation_history_entry(
                    user_id=user_id,
                    evaluation_type='agreement',
                    input_data={
                        'soilType': request.soilType,
                        'season': request.season,
                        'N': request.N,
                        'P': request.P,
                        'K': request.K,
                        'location': request.location,
                        'weather': weather_data
                    },
                    result_data=result
                )
                db.collection('evaluation_history').add(history_entry)
            except Exception as e:
                logger.error(f"Failed to save evaluation history: {str(e)}")
        
        return AgreementEvaluationResponse(**result)
    
    except Exception as e:
        logger.error(f"Model agreement evaluation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Model agreement evaluation failed: {str(e)}"
        )


@router.post("/full", response_model=FullEvaluationResponse)
async def evaluate_full_pipeline(
    request: EvaluationRequest,
    db: Client = Depends(get_db),
    user_id: Optional[str] = Depends(get_current_user)
):
    """
    Run complete evaluation pipeline with all metrics.
    
    Combines:
    - Noise injection test (RSS)
    - Missing feature test
    - Model agreement test
    - Comprehensive confidence scoring
    
    Args:
        request: Evaluation request with crop parameters
        db: Firestore client
        user_id: User ID (optional, from JWT)
        
    Returns:
        Full evaluation results with confidence score
    """
    try:
        logger.info(f"Full evaluation request from user: {user_id or 'anonymous'}")
        
        # Fetch weather data
        weather_data = await WeatherService.get_weather(request.location)
        
        # Run full evaluation
        result = await EvaluationService.evaluate_full(
            N=request.N,
            P=request.P,
            K=request.K,
            temperature=weather_data['temperature'],
            humidity=weather_data['humidity'],
            rainfall=weather_data['rainfall']
        )
        
        # Store evaluation history (if authenticated)
        if user_id:
            try:
                history_entry = EvaluationService.create_evaluation_history_entry(
                    user_id=user_id,
                    evaluation_type='full',
                    input_data={
                        'soilType': request.soilType,
                        'season': request.season,
                        'N': request.N,
                        'P': request.P,
                        'K': request.K,
                        'location': request.location,
                        'weather': weather_data
                    },
                    result_data=result
                )
                db.collection('evaluation_history').add(history_entry)
            except Exception as e:
                logger.error(f"Failed to save evaluation history: {str(e)}")
        
        return FullEvaluationResponse(**result)
    
    except Exception as e:
        logger.error(f"Full evaluation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Full evaluation failed: {str(e)}"
        )

