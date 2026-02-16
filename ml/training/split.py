"""
Train/test split utilities.
"""
from sklearn.model_selection import train_test_split
import pandas as pd
from typing import Tuple


def split_data(
    X: pd.DataFrame,
    y: pd.Series,
    test_size: float = 0.2,
    random_state: int = 42
) -> Tuple:
    """
    Split data into train and test sets.
    
    Args:
        X: Features
        y: Labels
        test_size: Proportion of test set
        random_state: Random seed
        
    Returns:
        Tuple of (X_train, X_test, y_train, y_test)
    """
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=test_size,
        random_state=random_state,
        stratify=y  # Maintain class distribution
    )
    
    print(f"Train set size: {len(X_train)}")
    print(f"Test set size: {len(X_test)}")
    print(f"Train set shape: {X_train.shape}")
    print(f"Test set shape: {X_test.shape}")
    
    return X_train, X_test, y_train, y_test
