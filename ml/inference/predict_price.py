"""
Price prediction inference module (stub for LSTM).
"""
import numpy as np
from typing import List, Dict


class PricePredictor:
    """Price prediction using LSTM (stub implementation)."""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(PricePredictor, cls).__new__(cls)
        return cls._instance
    
    def predict(self, crop: str, months: int = 6) -> List[float]:
        """
        Predict future prices for a crop (stub implementation).
        
        Args:
            crop: Crop name
            months: Number of months to predict
            
        Returns:
            List of predicted prices
        """
        # Stub implementation - returns mock prices
        # TODO: Implement LSTM model loading and prediction
        
        # Base prices for common crops (mock data)
        base_prices = {
            'rice': 2100,
            'wheat': 1800,
            'maize': 1500,
            'cotton': 3500,
            'sugarcane': 2800,
            'jute': 2200,
            'coffee': 4500,
            'tea': 3800
        }
        
        # Get base price (default to 2000 if crop not in dict)
        base_price = base_prices.get(crop.lower(), 2000)
        
        # Generate mock future prices with slight upward trend
        prices = []
        for i in range(months):
            # Add small random variation and upward trend
            variation = np.random.uniform(-50, 100)
            trend = i * 20  # Upward trend
            price = base_price + variation + trend
            prices.append(round(price, 2))
        
        return prices


def predict_price(crop: str, months: int = 6) -> Dict:
    """
    Convenience function for price prediction.
    
    Args:
        crop: Crop name
        months: Number of months to predict
        
    Returns:
        Dictionary with price predictions
    """
    predictor = PricePredictor()
    future_prices = predictor.predict(crop, months)
    
    return {
        'crop': crop,
        'months': months,
        'future_prices': future_prices,
        'note': 'Stub implementation - LSTM model not yet trained'
    }


if __name__ == "__main__":
    # Test price prediction
    print("\n" + "=" * 60)
    print("TESTING PRICE PREDICTION (STUB)")
    print("=" * 60 + "\n")
    
    result = predict_price('rice', months=6)
    
    print(f"Crop: {result['crop']}")
    print(f"Prediction months: {result['months']}")
    print(f"Future prices: {result['future_prices']}")
    print(f"Note: {result['note']}")
    print()
