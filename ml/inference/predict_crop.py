"""
Crop prediction inference module.
"""
import os
import pickle
import sys
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from preprocessing.encode import CropLabelEncoder
from preprocessing.scale import FeatureScaler
from features.feature_builder import build_features, get_feature_columns


class CropPredictor:
    """Singleton crop prediction model loader and predictor."""
    
    _instance = None
    _loaded = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(CropPredictor, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not self._loaded:
            self._load_models()
            CropPredictor._loaded = True
    
    def _load_models(self):
        """Load trained model artifacts."""
        models_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            'models'
        )
        
        print("Loading model artifacts...")
        
        # Load Random Forest model
        rf_path = os.path.join(models_dir, 'rf.pkl')
        with open(rf_path, 'rb') as f:
            self.rf_model = pickle.load(f)
        print(f"✓ Random Forest model loaded from {rf_path}")
        
        # Load scaler
        scaler_path = os.path.join(models_dir, 'scaler.pkl')
        self.scaler = FeatureScaler.load(scaler_path)
        
        # Load encoder
        encoder_path = os.path.join(models_dir, 'encoder.pkl')
        self.encoder = CropLabelEncoder.load(encoder_path)
        
        print("✓ All artifacts loaded successfully")
    
    def predict(
        self,
        N: float,
        P: float,
        K: float,
        temperature: float,
        humidity: float,
        ph: float,
        rainfall: float
    ) -> Dict:
        """
        Predict crop recommendation.
        
        Args:
            N: Nitrogen content
            P: Phosphorus content
            K: Potassium content
            temperature: Temperature in Celsius
            humidity: Humidity percentage
            ph: Soil pH
            rainfall: Rainfall in mm
            
        Returns:
            Dictionary with prediction results
        """
        # Create input dataframe
        input_data = pd.DataFrame([{
            'N': N,
            'P': P,
            'K': K,
            'temperature': temperature,
            'humidity': humidity,
            'ph': ph,
            'rainfall': rainfall
        }])
        
        # Build features (add derived features)
        input_features = build_features(input_data)
        
        # Select feature columns
        feature_cols = get_feature_columns()
        X = input_features[feature_cols]
        
        # Scale features
        X_scaled = self.scaler.transform(X)
        
        # Predict
        prediction = self.rf_model.predict(X_scaled)[0]
        probabilities = self.rf_model.predict_proba(X_scaled)[0]
        
        # Get crop name
        crop_name = self.encoder.inverse_transform([prediction])[0]
        
        # Get confidence (probability of predicted class)
        confidence = float(probabilities[prediction])
        
        # Get top 3 predictions
        top_3_indices = np.argsort(probabilities)[-3:][::-1]
        top_3_crops = []
        
        for idx in top_3_indices:
            crop = self.encoder.inverse_transform([idx])[0]
            prob = float(probabilities[idx])
            top_3_crops.append({
                'crop': crop,
                'probability': prob,
                'yield_percentage': int(prob * 100)
            })
        
        return {
            'recommended_crop': crop_name,
            'confidence': confidence,
            'top_3_recommendations': top_3_crops
        }
    
    def predict_batch(self, inputs: List[Dict]) -> List[Dict]:
        """
        Predict crops for multiple inputs.
        
        Args:
            inputs: List of input dictionaries
            
        Returns:
            List of prediction results
        """
        results = []
        for input_data in inputs:
            result = self.predict(**input_data)
            results.append(result)
        return results


def predict_crop(
    N: float,
    P: float,
    K: float,
    temperature: float,
    humidity: float,
    ph: float,
    rainfall: float
) -> Dict:
    """
    Convenience function for crop prediction.
    
    Args:
        N: Nitrogen content
        P: Phosphorus content
        K: Potassium content
        temperature: Temperature in Celsius
        humidity: Humidity percentage
        ph: Soil pH
        rainfall: Rainfall in mm
        
    Returns:
        Dictionary with prediction results
    """
    predictor = CropPredictor()
    return predictor.predict(N, P, K, temperature, humidity, ph, rainfall)


if __name__ == "__main__":
    # Test prediction
    print("\n" + "=" * 60)
    print("TESTING CROP PREDICTION")
    print("=" * 60 + "\n")
    
    # Sample input
    test_input = {
        'N': 90,
        'P': 42,
        'K': 43,
        'temperature': 20.87,
        'humidity': 82.00,
        'ph': 6.50,
        'rainfall': 202.93
    }
    
    print("Input:")
    for key, value in test_input.items():
        print(f"  {key}: {value}")
    print()
    
    # Predict
    result = predict_crop(**test_input)
    
    print("Prediction Result:")
    print(f"  Recommended Crop: {result['recommended_crop']}")
    print(f"  Confidence: {result['confidence']:.4f}")
    print()
    print("  Top 3 Recommendations:")
    for i, rec in enumerate(result['top_3_recommendations'], 1):
        print(f"    {i}. {rec['crop']} - {rec['probability']:.4f} ({rec['yield_percentage']}%)")
    print()
