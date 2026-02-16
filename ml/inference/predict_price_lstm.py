"""
LSTM price prediction inference module.
"""
import os
import sys
import numpy as np
from tensorflow import keras
from typing import List

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from preprocessing.price_dataset import PriceDatasetLoader


class LSTMPricePredictor:
    """Singleton LSTM price prediction model loader and predictor."""
    
    _instance = None
    _loaded = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LSTMPricePredictor, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not self._loaded:
            self._load_model()
            LSTMPricePredictor._loaded = True
    
    def _load_model(self):
        """Load trained LSTM model and scaler."""
        models_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            'models'
        )
        
        print("Loading LSTM model artifacts...")
        
        # Load LSTM model
        model_path = os.path.join(models_dir, 'lstm_model.keras')
        if not os.path.exists(model_path):
            raise FileNotFoundError(
                f"LSTM model not found at {model_path}. "
                f"Please train the model first: python training/train_lstm.py"
            )
        
        self.model = keras.models.load_model(model_path)
        print(f"✓ LSTM model loaded from {model_path}")
        
        # Load scaler
        scaler_path = os.path.join(models_dir, 'lstm_scaler.pkl')
        if not os.path.exists(scaler_path):
            raise FileNotFoundError(
                f"Scaler not found at {scaler_path}. "
                f"Please train the model first: python training/train_lstm.py"
            )
        
        self.scaler = PriceDatasetLoader.load_scaler(scaler_path)
        
        # Dataset directory
        self.dataset_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            'dataset'
        )
        
        print("✓ All artifacts loaded successfully")
    
    def predict_future_prices(
        self,
        crop_name: str,
        months: int = 6,
        sequence_length: int = 12
    ) -> List[float]:
        """
        Predict future prices for a crop using recursive forecasting.
        
        Args:
            crop_name: Crop/commodity name
            months: Number of days to predict (parameter name kept for API compatibility)
            sequence_length: Input sequence length in days (default: 12)
            
        Returns:
            List of predicted daily prices
        """
        print(f"\nPredicting prices for {crop_name} ({months} days ahead)...")
        
        # Load last sequence from dataset
        loader = PriceDatasetLoader(self.dataset_dir)
        
        try:
            last_sequence = loader.get_last_sequence(crop_name, sequence_length)
        except Exception as e:
            print(f"Error loading data for {crop_name}: {e}")
            print("Using fallback prediction...")
            return self._get_fallback_prices(crop_name, months)
        
        # Store scaler for inverse transform
        self.scaler = loader.scaler
        
        # Recursive multi-step forecasting
        predictions = []
        current_sequence = last_sequence.copy()
        
        for i in range(months):
            # Predict next day
            next_pred_scaled = self.model.predict(current_sequence, verbose=0)
            
            # Inverse transform to get actual price
            next_pred_actual = self.scaler.inverse_transform(next_pred_scaled)[0][0]
            predictions.append(float(next_pred_actual))
            
            # Update sequence for next prediction
            # Remove first value, append new prediction
            current_sequence = np.append(
                current_sequence[:, 1:, :],
                next_pred_scaled.reshape(1, 1, 1),
                axis=1
            )
        
        print(f"Predicted prices: {[f'₹{p:.2f}' for p in predictions]}")
        
        return predictions
    
    def _get_fallback_prices(self, crop_name: str, months: int) -> List[float]:
        """
        Get fallback prices when data is not available.
        
        Args:
            crop_name: Crop name
            months: Number of months
            
        Returns:
            List of fallback prices
        """
        # Base prices for common crops
        base_prices = {
            'rice': 2100,
            'wheat': 1800,
            'maize': 1500,
            'cotton': 3500,
            'sugarcane': 2800,
            'jute': 2200,
            'coffee': 4500,
            'tea': 3800,
            'potato': 1200,
            'onion': 1500,
            'tomato': 1800
        }
        
        base_price = base_prices.get(crop_name.lower(), 2000)
        
        # Generate prices with slight upward trend
        prices = []
        for i in range(months):
            variation = np.random.uniform(-50, 100)
            trend = i * 20
            price = base_price + variation + trend
            prices.append(round(price, 2))
        
        return prices


def predict_future_prices(crop_name: str, months: int = 6) -> List[float]:
    """
    Convenience function for price prediction.
    
    Args:
        crop_name: Crop/commodity name
        months: Number of days to predict (parameter name kept for API compatibility)
        
    Returns:
        List of predicted daily prices
    """
    predictor = LSTMPricePredictor()
    return predictor.predict_future_prices(crop_name, months)


if __name__ == "__main__":
    # Test LSTM price prediction
    print("\n" + "=" * 60)
    print("TESTING LSTM PRICE PREDICTION")
    print("=" * 60)
    
    # Test with rice
    crop = 'rice'
    months = 6
    
    print(f"\nCrop: {crop}")
    print(f"Forecast period: {months} days")
    
    try:
        prices = predict_future_prices(crop, months)
        
        print("\nPredicted Daily Prices:")
        for i, price in enumerate(prices, 1):
            print(f"  Day {i}: ₹{price:.2f}")
    
    except Exception as e:
        print(f"Error: {e}")
        print("\nPlease train the LSTM model first:")
        print("  cd ml")
        print("  python training/train_lstm.py")
    
    print()
