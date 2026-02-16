"""
Data scaling utilities.
"""
import pickle
from sklearn.preprocessing import StandardScaler
import pandas as pd
import numpy as np


class FeatureScaler:
    """Scaler for numerical features."""
    
    def __init__(self):
        self.scaler = StandardScaler()
        self.fitted = False
        self.feature_names = None
    
    def fit(self, features: pd.DataFrame):
        """
        Fit scaler on features.
        
        Args:
            features: Feature dataframe
        """
        self.scaler.fit(features)
        self.fitted = True
        self.feature_names = features.columns.tolist()
        print(f"Scaler fitted on {len(self.feature_names)} features")
        print(f"Features: {self.feature_names}")
    
    def transform(self, features: pd.DataFrame) -> np.ndarray:
        """
        Transform features using fitted scaler.
        
        Args:
            features: Feature dataframe
            
        Returns:
            Scaled features array
        """
        if not self.fitted:
            raise ValueError("Scaler not fitted yet")
        return self.scaler.transform(features)
    
    def fit_transform(self, features: pd.DataFrame) -> np.ndarray:
        """
        Fit and transform features.
        
        Args:
            features: Feature dataframe
            
        Returns:
            Scaled features array
        """
        self.fit(features)
        return self.transform(features)
    
    def inverse_transform(self, scaled_features: np.ndarray) -> np.ndarray:
        """
        Inverse transform scaled features.
        
        Args:
            scaled_features: Scaled feature array
            
        Returns:
            Original scale features
        """
        if not self.fitted:
            raise ValueError("Scaler not fitted yet")
        return self.scaler.inverse_transform(scaled_features)
    
    def save(self, path: str):
        """
        Save scaler to file.
        
        Args:
            path: File path
        """
        with open(path, 'wb') as f:
            pickle.dump({
                'scaler': self.scaler,
                'feature_names': self.feature_names
            }, f)
        print(f"Scaler saved to {path}")
    
    @staticmethod
    def load(path: str):
        """
        Load scaler from file.
        
        Args:
            path: File path
            
        Returns:
            FeatureScaler instance
        """
        scaler_obj = FeatureScaler()
        with open(path, 'rb') as f:
            data = pickle.load(f)
            scaler_obj.scaler = data['scaler']
            scaler_obj.feature_names = data['feature_names']
        scaler_obj.fitted = True
        print(f"Scaler loaded from {path}")
        return scaler_obj
