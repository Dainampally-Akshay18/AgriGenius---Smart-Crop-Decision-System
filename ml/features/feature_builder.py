"""
Feature engineering utilities.
"""
import pandas as pd


def build_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Build engineered features from raw data.
    
    Args:
        df: Raw dataframe with base features
        
    Returns:
        Dataframe with engineered features
    """
    df = df.copy()
    
    # Derived feature: nutrient_ratio
    df['nutrient_ratio'] = (df['N'] + df['P'] + df['K']) / 3
    
    # Derived feature: climate_index
    df['climate_index'] = df['temperature'] * df['humidity']
    
    print(f"Features after engineering: {df.columns.tolist()}")
    
    return df


def get_feature_columns() -> list:
    """
    Get list of feature columns for model training.
    
    Returns:
        List of feature column names
    """
    return [
        'N', 'P', 'K',
        'temperature', 'humidity', 'ph', 'rainfall',
        'nutrient_ratio', 'climate_index'
    ]


def prepare_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Prepare features for model training.
    
    Args:
        df: Dataframe with raw features
        
    Returns:
        Dataframe with selected features
    """
    df = build_features(df)
    feature_cols = get_feature_columns()
    return df[feature_cols]
