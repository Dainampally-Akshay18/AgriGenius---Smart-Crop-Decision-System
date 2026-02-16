"""
Data encoding utilities.
"""
import pickle
from sklearn.preprocessing import LabelEncoder
import pandas as pd


class CropLabelEncoder:
    """Encoder for crop labels."""
    
    def __init__(self):
        self.encoder = LabelEncoder()
        self.fitted = False
    
    def fit(self, labels: pd.Series):
        """
        Fit encoder on crop labels.
        
        Args:
            labels: Crop label series
        """
        self.encoder.fit(labels)
        self.fitted = True
        print(f"Encoder fitted on {len(self.encoder.classes_)} classes")
        print(f"Classes: {self.encoder.classes_}")
    
    def transform(self, labels: pd.Series):
        """
        Transform crop labels to numeric.
        
        Args:
            labels: Crop label series
            
        Returns:
            Encoded labels
        """
        if not self.fitted:
            raise ValueError("Encoder not fitted yet")
        return self.encoder.transform(labels)
    
    def inverse_transform(self, encoded_labels):
        """
        Transform numeric labels back to crop names.
        
        Args:
            encoded_labels: Numeric labels
            
        Returns:
            Crop names
        """
        if not self.fitted:
            raise ValueError("Encoder not fitted yet")
        return self.encoder.inverse_transform(encoded_labels)
    
    def save(self, path: str):
        """
        Save encoder to file.
        
        Args:
            path: File path
        """
        with open(path, 'wb') as f:
            pickle.dump(self.encoder, f)
        print(f"Encoder saved to {path}")
    
    @staticmethod
    def load(path: str):
        """
        Load encoder from file.
        
        Args:
            path: File path
            
        Returns:
            CropLabelEncoder instance
        """
        encoder_obj = CropLabelEncoder()
        with open(path, 'rb') as f:
            encoder_obj.encoder = pickle.load(f)
        encoder_obj.fitted = True
        print(f"Encoder loaded from {path}")
        return encoder_obj
