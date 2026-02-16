"""
Data cleaning utilities.
"""
import pandas as pd
import numpy as np


def validate_and_clean(df: pd.DataFrame) -> pd.DataFrame:
    """
    Validate and clean the crop recommendation dataset.
    
    Args:
        df: Raw dataframe
        
    Returns:
        Cleaned dataframe
    """
    print(f"Original dataset shape: {df.shape}")
    
    # Check for nulls
    null_counts = df.isnull().sum()
    if null_counts.sum() > 0:
        print(f"Warning: Found null values:\n{null_counts[null_counts > 0]}")
    
    # Validate NPK values (0-140)
    for col in ['N', 'P', 'K']:
        df[col] = df[col].clip(lower=0, upper=140)
    
    # Validate pH (0-14)
    df['ph'] = df['ph'].clip(lower=0, upper=14)
    
    # Validate temperature (0-60)
    df['temperature'] = df['temperature'].clip(lower=0, upper=60)
    
    # Validate humidity (0-100)
    df['humidity'] = df['humidity'].clip(lower=0, upper=100)
    
    # Validate rainfall (non-negative)
    df['rainfall'] = df['rainfall'].clip(lower=0)
    
    # Clip extreme outliers at 1st and 99th percentile
    numeric_cols = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']
    for col in numeric_cols:
        lower = df[col].quantile(0.01)
        upper = df[col].quantile(0.99)
        df[col] = df[col].clip(lower=lower, upper=upper)
    
    print(f"Cleaned dataset shape: {df.shape}")
    print(f"Dataset info:\n{df.describe()}")
    
    return df


def load_dataset(csv_path: str) -> pd.DataFrame:
    """
    Load and clean the crop recommendation dataset.
    
    Args:
        csv_path: Path to CSV file
        
    Returns:
        Cleaned dataframe
    """
    df = pd.read_csv(csv_path)
    df = validate_and_clean(df)
    return df
