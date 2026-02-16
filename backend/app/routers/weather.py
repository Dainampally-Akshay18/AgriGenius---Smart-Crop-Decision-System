"""
Weather API wrapper endpoints.
"""
from fastapi import APIRouter, Query
from app.services.weather_service import WeatherService
from app.utils.logger import logger

router = APIRouter(prefix="/weather", tags=["Weather"])


@router.get("")
async def get_weather(location: str = Query(..., min_length=2, description="City or location name")):
    """
    Get weather data for a location.
    
    Args:
        location: City or location name
        
    Returns:
        Weather data with temperature, humidity, rainfall
    """
    logger.info(f"Weather request for location: {location}")
    weather_data = await WeatherService.get_weather(location)
    return weather_data
