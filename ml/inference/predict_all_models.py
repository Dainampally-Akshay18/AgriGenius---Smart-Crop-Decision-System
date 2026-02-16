"""
Multi-model prediction for model comparison (stub for evaluation).
"""
import os
import pickle
import sys
import pandas as pd
from typing import Dict

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from preprocessing.encode import CropLabelEncoder
from preprocessing.scale import FeatureScaler
from features.feature_builder import build_features, get_feature_columns


class MultiModelPredictor:
    """Predictor that runs multiple models for comparison."""
    
    _instance = None
    _loaded = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MultiModelPredictor, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not self._loaded:
            self._load_models()
            MultiModelPredictor._loaded = True
    
    def _load_models(self):
        """Load all trained model artifacts."""
        models_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            'models'
        )
        
        print("Loading model artifacts for multi-model prediction...")
        
        # Load Random Forest (required)
        rf_path = os.path.join(models_dir, 'rf.pkl')
        if os.path.exists(rf_path):
            with open(rf_path, 'rb') as f:
                self.rf_model = pickle.load(f)
            print(f"✓ Random Forest loaded")
        else:
            self.rf_model = None
            print("✗ Random Forest not found")
        
        # Load XGBoost (optional)
        xgb_path = os.path.join(models_dir, 'xgb.pkl')
        if os.path.exists(xgb_path):
            with open(xgb_path, 'rb') as f:
                self.xgb_model = pickle.load(f)
            print(f"✓ XGBoost loaded")
        else:
            self.xgb_model = None
            print("✗ XGBoost not found (will be trained in Phase 7)")
        
        # Load SVM (optional)
        svm_path = os.path.join(models_dir, 'svm.pkl')
        if os.path.exists(svm_path):
            with open(svm_path, 'rb') as f:
                self.svm_model = pickle.load(f)
            print(f"✓ SVM loaded")
        else:
            self.svm_model = None
            print("✗ SVM not found (will be trained in Phase 7)")
        
        # Load MLP (optional)
        mlp_path = os.path.join(models_dir, 'mlp.pkl')
        if os.path.exists(mlp_path):
            with open(mlp_path, 'rb') as f:
                self.mlp_model = pickle.load(f)
            print(f"✓ MLP loaded")
        else:
            self.mlp_model = None
            print("✗ MLP not found (will be trained in Phase 7)")
        
        # Load scaler and encoder
        scaler_path = os.path.join(models_dir, 'scaler.pkl')
        self.scaler = FeatureScaler.load(scaler_path)
        
        encoder_path = os.path.join(models_dir, 'encoder.pkl')
        self.encoder = CropLabelEncoder.load(encoder_path)
    
    def predict_all(
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
        Predict using all available models.
        
        Args:
            N: Nitrogen content
            P: Phosphorus content
            K: Potassium content
            temperature: Temperature in Celsius
            humidity: Humidity percentage
            ph: Soil pH
            rainfall: Rainfall in mm
            
        Returns:
            Dictionary with predictions from all models
        """
        # Prepare input
        input_data = pd.DataFrame([{
            'N': N, 'P': P, 'K': K,
            'temperature': temperature,
            'humidity': humidity,
            'ph': ph,
            'rainfall': rainfall
        }])
        
        input_features = build_features(input_data)
        feature_cols = get_feature_columns()
        X = input_features[feature_cols]
        X_scaled = self.scaler.transform(X)
        
        predictions = {}
        
        # Random Forest
        if self.rf_model:
            pred = self.rf_model.predict(X_scaled)[0]
            predictions['rf'] = self.encoder.inverse_transform([pred])[0]
        
        # XGBoost
        if self.xgb_model:
            pred = self.xgb_model.predict(X_scaled)[0]
            predictions['xgb'] = self.encoder.inverse_transform([pred])[0]
        
        # SVM
        if self.svm_model:
            pred = self.svm_model.predict(X_scaled)[0]
            predictions['svm'] = self.encoder.inverse_transform([pred])[0]
        
        # MLP
        if self.mlp_model:
            pred = self.mlp_model.predict(X_scaled)[0]
            predictions['mlp'] = self.encoder.inverse_transform([pred])[0]
        
        return predictions


def predict_all_models(
    N: float,
    P: float,
    K: float,
    temperature: float,
    humidity: float,
    ph: float,
    rainfall: float
) -> Dict:
    """
    Convenience function for multi-model prediction.
    
    Returns:
        Dictionary with predictions from all available models
    """
    predictor = MultiModelPredictor()
    return predictor.predict_all(N, P, K, temperature, humidity, ph, rainfall)


if __name__ == "__main__":
    # Test multi-model prediction
    print("\n" + "=" * 60)
    print("TESTING MULTI-MODEL PREDICTION")
    print("=" * 60 + "\n")
    
    test_input = {
        'N': 90, 'P': 42, 'K': 43,
        'temperature': 20.87,
        'humidity': 82.00,
        'ph': 6.50,
        'rainfall': 202.93
    }
    
    predictions = predict_all_models(**test_input)
    
    print("Predictions from all models:")
    for model_name, crop in predictions.items():
        print(f"  {model_name.upper()}: {crop}")
    print()
