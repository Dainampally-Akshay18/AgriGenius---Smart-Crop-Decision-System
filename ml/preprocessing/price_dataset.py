"""
Price dataset preprocessing for LSTM training.
"""
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from typing import Tuple, List
import pickle


class PriceDatasetLoader:
    """Load and preprocess agricultural price dataset."""
    
    def __init__(self, csv_path: str):
        """
        Initialize dataset loader.
        
        Args:
            csv_path: Path to Agriculture_price_dataset.csv
        """
        self.csv_path = csv_path
        self.df = None
        self.scaler = MinMaxScaler(feature_range=(0, 1))
    
    def load_data(self, commodity: str) -> pd.DataFrame:
        """
        Load and filter dataset by commodity.
        
        Args:
            commodity: Crop/commodity name (e.g., 'rice', 'wheat')
            
        Returns:
            Filtered dataframe
        """
        print(f"Loading dataset from {self.csv_path}...")
        self.df = pd.read_csv(self.csv_path)
        
        print(f"Original dataset shape: {self.df.shape}")
        print(f"Columns: {self.df.columns.tolist()}")
        
        # Rename columns to standardized names (case-insensitive)
        column_mapping = {}
        for col in self.df.columns:
            col_lower = col.lower().strip().replace(' ', '_')
            if 'commodity' in col_lower:
                column_mapping[col] = 'commodity'
            elif 'arrival' in col_lower and 'date' in col_lower:
                column_mapping[col] = 'date'
            elif 'modal' in col_lower and 'price' in col_lower:
                column_mapping[col] = 'modal_price'
        
        self.df = self.df.rename(columns=column_mapping)
        
        print(f"Renamed columns: {self.df.columns.tolist()}")
        
        # Verify required columns exist
        required_cols = ['commodity', 'date', 'modal_price']
        missing_cols = [col for col in required_cols if col not in self.df.columns]
        if missing_cols:
            raise ValueError(f"Missing required columns after mapping: {missing_cols}")
        
        # Filter by commodity (case-insensitive)
        self.df = self.df[self.df['commodity'].str.lower() == commodity.lower()].copy()
        
        print(f"Filtered for '{commodity}': {len(self.df)} records")
        
        if len(self.df) == 0:
            raise ValueError(f"No data found for commodity: {commodity}")
        
        return self.df
    
    def preprocess(self) -> pd.DataFrame:
        """
        Preprocess price data to create national monthly time series.
        
        Returns:
            Processed dataframe with monthly averages across all India
        """
        print("Preprocessing data...")
        
        # Convert date to datetime (handle DD-MM-YYYY format)
        self.df['date'] = pd.to_datetime(self.df['date'], format='%d-%m-%Y', errors='coerce')
        
        # Drop rows with invalid dates
        self.df = self.df.dropna(subset=['date'])
        
        # Sort chronologically
        self.df = self.df.sort_values('date')
        
        print(f"Date range in data: {self.df['date'].min()} to {self.df['date'].max()}")
        
        # Extract year-month for aggregation
        self.df['year_month'] = self.df['date'].dt.to_period('M')
        
        # Aggregate NATIONAL monthly average modal_price
        # (ignore state, district, market - aggregate across ALL India)
        monthly_avg = self.df.groupby('year_month')['modal_price'].mean().reset_index()
        monthly_avg['year_month'] = monthly_avg['year_month'].dt.to_timestamp()
        monthly_avg = monthly_avg.rename(columns={'year_month': 'date', 'modal_price': 'price'})
        
        print(f"National monthly aggregated data: {len(monthly_avg)} months")
        print(f"Date range: {monthly_avg['date'].min()} to {monthly_avg['date'].max()}")
        
        # Fill missing months using forward fill
        monthly_avg = monthly_avg.set_index('date')
        
        # Create complete date range
        date_range = pd.date_range(
            start=monthly_avg.index.min(),
            end=monthly_avg.index.max(),
            freq='MS'  # Month start frequency
        )
        
        # Reindex to include all months
        monthly_avg = monthly_avg.reindex(date_range)
        
        # Forward fill missing values
        monthly_avg = monthly_avg.fillna(method='ffill')
        
        # Reset index
        monthly_avg = monthly_avg.reset_index()
        monthly_avg = monthly_avg.rename(columns={'index': 'date'})
        
        print(f"After filling missing months: {len(monthly_avg)} months")
        print(f"Complete date range: {monthly_avg['date'].min()} to {monthly_avg['date'].max()}")
        
        return monthly_avg
    
    def create_sequences(
        self,
        data: pd.DataFrame,
        sequence_length: int = 12
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Create sliding window sequences for LSTM.
        
        Args:
            data: Preprocessed dataframe with 'price' column
            sequence_length: Number of months to look back (default: 12)
            
        Returns:
            Tuple of (X sequences, y labels)
        """
        print(f"Creating sequences with window size: {sequence_length}")
        
        # Extract prices
        prices = data['price'].values.reshape(-1, 1)
        
        # Normalize
        prices_scaled = self.scaler.fit_transform(prices)
        
        # Create sequences
        X, y = [], []
        
        for i in range(len(prices_scaled) - sequence_length):
            X.append(prices_scaled[i:i + sequence_length])
            y.append(prices_scaled[i + sequence_length])
        
        X = np.array(X)
        y = np.array(y)
        
        print(f"Created {len(X)} sequences")
        print(f"X shape: {X.shape}")
        print(f"y shape: {y.shape}")
        
        return X, y
    
    def prepare_data(
        self,
        commodity: str,
        sequence_length: int = 12,
        train_split: float = 0.8
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """
        Complete data preparation pipeline.
        
        Args:
            commodity: Crop/commodity name
            sequence_length: Sequence window size
            train_split: Train/test split ratio
            
        Returns:
            Tuple of (X_train, X_test, y_train, y_test)
        """
        # Load and preprocess
        self.load_data(commodity)
        monthly_data = self.preprocess()
        
        # Create sequences
        X, y = self.create_sequences(monthly_data, sequence_length)
        
        # Train/test split
        split_idx = int(len(X) * train_split)
        
        X_train = X[:split_idx]
        X_test = X[split_idx:]
        y_train = y[:split_idx]
        y_test = y[split_idx:]
        
        print(f"\nTrain set: {len(X_train)} sequences")
        print(f"Test set: {len(X_test)} sequences")
        
        return X_train, X_test, y_train, y_test
    
    def get_last_sequence(
        self,
        commodity: str,
        sequence_length: int = 12
    ) -> np.ndarray:
        """
        Get the last N months of data for prediction.
        
        Args:
            commodity: Crop/commodity name
            sequence_length: Number of months
            
        Returns:
            Scaled sequence ready for prediction
        """
        self.load_data(commodity)
        monthly_data = self.preprocess()
        
        # Get last N months
        last_prices = monthly_data['price'].values[-sequence_length:]
        
        if len(last_prices) < sequence_length:
            raise ValueError(f"Not enough data. Need {sequence_length} months, got {len(last_prices)}")
        
        # Normalize
        last_prices_scaled = self.scaler.fit_transform(last_prices.reshape(-1, 1))
        
        # Reshape for LSTM input
        return last_prices_scaled.reshape(1, sequence_length, 1)
    
    def save_scaler(self, path: str):
        """Save scaler to file."""
        with open(path, 'wb') as f:
            pickle.dump(self.scaler, f)
        print(f"Scaler saved to {path}")
    
    @staticmethod
    def load_scaler(path: str) -> MinMaxScaler:
        """Load scaler from file."""
        with open(path, 'rb') as f:
            scaler = pickle.load(f)
        print(f"Scaler loaded from {path}")
        return scaler


if __name__ == "__main__":
    # Test dataset loader
    import os
    
    dataset_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        'dataset',
        'Prices.csv'
    )
    
    loader = PriceDatasetLoader(dataset_path)
    
    # Test with rice
    print("\n" + "=" * 60)
    print("TESTING PRICE DATASET LOADER")
    print("=" * 60 + "\n")
    
    X_train, X_test, y_train, y_test = loader.prepare_data('rice', sequence_length=12)
    
    print("\nDataset preparation complete!")
