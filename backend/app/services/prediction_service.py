"""
Prediction service that integrates ML inference.
"""
from typing import Dict, List
from datetime import datetime

# Import from ml module (path configured at startup)
from ml.inference.predict_crop import predict_crop
from ml.inference.predict_price import predict_price

# Import LSTM price predictor
try:
    from ml.inference.predict_price_lstm import predict_future_prices
    LSTM_AVAILABLE = True
except Exception as e:
    LSTM_AVAILABLE = False
    predict_future_prices = None

from app.utils.logger import logger


class PredictionService:
    """Service for crop and price predictions."""
    
    # Default NPK values by soil type (from PRD Section 14.3)
    SOIL_DEFAULTS = {
        'black': {'N': 70, 'P': 40, 'K': 50},
        'red': {'N': 40, 'P': 30, 'K': 35},
        'alluvial': {'N': 60, 'P': 35, 'K': 40}
    }
    
    @staticmethod
    def apply_soil_defaults(N: float, P: float, K: float, soil_type: str) -> tuple:
        """
        Apply default NPK values if user enters 0.
        
        Args:
            N: Nitrogen value
            P: Phosphorus value
            K: Potassium value
            soil_type: Soil type
            
        Returns:
            Tuple of (N, P, K) with defaults applied
        """
        soil_key = soil_type.lower()
        defaults = PredictionService.SOIL_DEFAULTS.get(soil_key, {'N': 50, 'P': 35, 'K': 40})
        
        if N == 0:
            N = defaults['N']
        if P == 0:
            P = defaults['P']
        if K == 0:
            K = defaults['K']
        
        return N, P, K
    
    @staticmethod
    async def predict_crop_recommendation(
        N: float,
        P: float,
        K: float,
        soil_type: str,
        season: str,
        temperature: float,
        humidity: float,
        rainfall: float,
        ph: float = 6.5  # Default pH
    ) -> Dict:
        """
        Get crop recommendation using ML model.
        
        Args:
            N: Nitrogen content
            P: Phosphorus content
            K: Potassium content
            soil_type: Soil type
            season: Season
            temperature: Temperature in Celsius
            humidity: Humidity percentage
            rainfall: Rainfall in mm
            ph: Soil pH (default 6.5)
            
        Returns:
            Dictionary with crop recommendations
        """
        # Apply soil defaults if needed
        N, P, K = PredictionService.apply_soil_defaults(N, P, K, soil_type)
        
        logger.info(f"Predicting crop for N={N}, P={P}, K={K}, temp={temperature}, humidity={humidity}, rainfall={rainfall}")
        
        # Call ML inference
        result = predict_crop(
            N=N,
            P=P,
            K=K,
            temperature=temperature,
            humidity=humidity,
            ph=ph,
            rainfall=rainfall
        )
        
        # Get price predictions for top 3 crops
        recommendations = []
        for crop_data in result['top_3_recommendations']:
            crop_name = crop_data['crop']
            
            # Get price prediction using LSTM (with fallback to stub)
            try:
                if LSTM_AVAILABLE:
                    # Use real LSTM model for 6-day forecast
                    future_prices = predict_future_prices(crop_name, months=6)
                    estimated_price = future_prices[0] if future_prices else 2000.0
                    logger.info(f"LSTM prediction for {crop_name}: {future_prices[:3]}...")
                else:
                    # Fallback to stub
                    price_result = predict_price(crop_name, months=1)
                    estimated_price = price_result['future_prices'][0] if price_result['future_prices'] else 2000.0
                    logger.info(f"Using stub prediction for {crop_name}")
            except Exception as e:
                # Graceful fallback on any error
                logger.warning(f"LSTM prediction failed for {crop_name}: {e}. Using fallback.")
                price_result = predict_price(crop_name, months=1)
                estimated_price = price_result['future_prices'][0] if price_result['future_prices'] else 2000.0
            
            recommendations.append({
                'crop': crop_name,
                'yield': crop_data['yield_percentage'],
                'price': estimated_price
            })
        
        logger.info(f"Prediction complete: {recommendations}")
        
        return {
            'recommendedCrops': recommendations
        }
    
    @staticmethod
    def create_prediction_history_entry(
        user_id: str,
        input_data: Dict,
        result_data: Dict
    ) -> Dict:
        """
        Create prediction history entry for Firestore.
        
        Args:
            user_id: User document ID
            input_data: Input parameters
            result_data: Prediction results
            
        Returns:
            Dictionary for Firestore document
        """
        return {
            'user_id': user_id,
            'input_payload': input_data,
            'result_payload': result_data,
            'timestamp': datetime.utcnow()
        }
