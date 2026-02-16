"""
Weather service for fetching weather data.
"""
import httpx
from typing import Dict, Optional
from app.config import config
from app.utils.logger import logger


class WeatherService:
    """Service for fetching weather data from OpenWeather API."""
    
    BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
    
    @staticmethod
    async def get_weather(location: str) -> Dict:
        """
        Fetch weather data for a location.
        
        Args:
            location: City name or location
            
        Returns:
            Dictionary with temperature, humidity, rainfall
            
        Raises:
            Exception: If weather API fails
        """
        if not config.WEATHER_API_KEY:
            logger.warning("Weather API key not configured, using default values")
            return WeatherService._get_default_weather()
        
        try:
            async with httpx.AsyncClient() as client:
                params = {
                    "q": location,
                    "appid": config.WEATHER_API_KEY,
                    "units": "metric"  # Celsius
                }
                
                response = await client.get(
                    WeatherService.BASE_URL,
                    params=params,
                    timeout=10.0
                )
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Extract weather data
                    temperature = data['main']['temp']
                    humidity = data['main']['humidity']
                    
                    # Rainfall (if available in last 1h or 3h)
                    rainfall = 0.0
                    if 'rain' in data:
                        rainfall = data['rain'].get('1h', data['rain'].get('3h', 0.0))
                    
                    weather_data = {
                        "temperature": round(temperature, 2),
                        "humidity": round(humidity, 2),
                        "rainfall": round(rainfall, 2)
                    }
                    
                    logger.info(f"Weather fetched for {location}: {weather_data}")
                    return weather_data
                
                else:
                    logger.error(f"Weather API error: {response.status_code}")
                    return WeatherService._get_default_weather()
        
        except Exception as e:
            logger.error(f"Weather API exception: {str(e)}")
            return WeatherService._get_default_weather()
    
    @staticmethod
    def _get_default_weather() -> Dict:
        """
        Get default weather values when API is unavailable.
        
        Returns:
            Dictionary with default weather values
        """
        return {
            "temperature": 25.0,
            "humidity": 70.0,
            "rainfall": 100.0
        }
