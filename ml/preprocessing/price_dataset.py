"""
Price dataset preprocessing for LSTM training (Memory-Efficient).
"""
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from typing import Tuple, List
import pickle
import os


class PriceDatasetLoader:
    """Load and preprocess agricultural price dataset (memory-efficient)."""
    
    def __init__(self, dataset_dir: str):
        """
        Initialize dataset loader.
        
        Args:
            dataset_dir: Directory containing 2024.csv and 2025.csv
        """
        self.dataset_dir = dataset_dir
        self.df = None
        self.scaler = MinMaxScaler(feature_range=(0, 1))
    
    def load_data_chunked(self, commodity: str) -> pd.DataFrame:
        """
        Load and filter large CSV files in chunks (memory-efficient).
        
        Args:
            commodity: Crop/commodity name (e.g., 'rice', 'wheat')
            
        Returns:
            Filtered dataframe
        """
        print(f"Loading datasets from {self.dataset_dir}...")
        print("Using chunked reading for memory efficiency...")
        
        # Files to load
        files = ['2024.csv', '2025.csv']
        
        # Normalize commodity name
        commodity_lower = commodity.lower().strip()
        
        # Columns we need (optimize memory)
        usecols = ['Arrival_Date', 'Modal_Price', 'Commodity']
        
        # Data type optimization
        dtypes = {
            'Commodity': 'category',
            'Modal_Price': 'float32'
        }
        
        filtered_chunks = []
        total_rows = 0
        
        for filename in files:
            filepath = os.path.join(self.dataset_dir, filename)
            
            if not os.path.exists(filepath):
                print(f"Warning: {filename} not found, skipping...")
                continue
            
            print(f"Processing {filename}...")
            
            # Read in chunks
            chunk_size = 100000
            for chunk in pd.read_csv(filepath, usecols=usecols, dtype=dtypes, chunksize=chunk_size):
                # Lowercase column names
                chunk.columns = chunk.columns.str.lower().str.strip()
                
                # Filter by commodity immediately (reduce memory)
                chunk['commodity'] = chunk['commodity'].str.lower().str.strip()
                filtered = chunk[chunk['commodity'] == commodity_lower].copy()
                
                if len(filtered) > 0:
                    filtered_chunks.append(filtered[['arrival_date', 'modal_price']])
                    total_rows += len(filtered)
                
                # Clear chunk from memory
                del chunk
        
        if not filtered_chunks:
            raise ValueError(f"No data found for commodity: {commodity}")
        
        # Concatenate all filtered chunks
        print(f"Concatenating {len(filtered_chunks)} chunks...")
        self.df = pd.concat(filtered_chunks, ignore_index=True)
        
        # Rename columns
        self.df = self.df.rename(columns={
            'arrival_date': 'date',
            'modal_price': 'price'
        })
        
        print(f"Filtered for '{commodity}': {len(self.df)} records")
        
        return self.df
    
    def create_national_daily_series(self) -> pd.DataFrame:
        """
        Create national daily time series from data.
        
        Returns:
            Daily aggregated dataframe
        """
        print("Creating national daily time series...")
        
        # Convert date to datetime (robust automatic parsing)
        print("Parsing dates...")
        self.df['date'] = pd.to_datetime(self.df['date'], errors='coerce')
        
        # Validate date parsing
        if self.df['date'].isna().all():
            raise ValueError(
                "All dates failed to parse — check date format. "
                "Expected formats: YYYY-MM-DD, DD-MM-YYYY, or other standard formats."
            )
        
        # Count invalid dates
        invalid_dates = self.df['date'].isna().sum()
        if invalid_dates > 0:
            print(f"Warning: {invalid_dates} rows with invalid dates will be dropped")
        
        # Drop rows with invalid dates or prices
        self.df = self.df.dropna(subset=['date', 'price'])
        
        # Drop rows with zero or negative prices
        self.df = self.df[self.df['price'] > 0]
        
        print(f"Valid rows after cleaning: {len(self.df)}")
        
        # Sort chronologically
        self.df = self.df.sort_values('date')
        
        print(f"Valid date range after parsing: {self.df['date'].min()} to {self.df['date'].max()}")
        
        # Daily national average (aggregate across all markets/states)
        print("Computing daily national averages...")
        daily_avg = self.df.groupby('date')['price'].mean().reset_index()
        
        print(f"Total daily data points: {len(daily_avg)}")
        
        if len(daily_avg) == 0:
            raise ValueError("No daily data points after aggregation. Check data quality.")
        
        print(f"Daily date range: {daily_avg['date'].min()} to {daily_avg['date'].max()}")
        
        return daily_avg
    
    def fill_missing_days(self, daily_data: pd.DataFrame) -> pd.DataFrame:
        """
        Fill missing days with forward fill.
        
        Args:
            daily_data: Daily aggregated data
            
        Returns:
            Complete daily series
        """
        print("Filling missing days...")
        
        # Set date as index
        daily_data = daily_data.set_index('date')
        
        # Create complete date range (daily frequency)
        date_range = pd.date_range(
            start=daily_data.index.min(),
            end=daily_data.index.max(),
            freq='D'
        )
        
        # Reindex and forward fill
        daily_data = daily_data.reindex(date_range)
        daily_data = daily_data.fillna(method='ffill')
        
        # Reset index
        daily_data = daily_data.reset_index()
        daily_data = daily_data.rename(columns={'index': 'date'})
        
        print(f"Complete daily series: {len(daily_data)} days")
        
        return daily_data
    
    def create_sequences(
        self,
        data: pd.DataFrame,
        sequence_length: int = 12
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Create sliding window sequences for LSTM.
        
        Args:
            data: Daily dataframe with 'price' column
            sequence_length: Number of days to look back
            
        Returns:
            Tuple of (X sequences, y labels)
        """
        print(f"Creating sequences with window size: {sequence_length} days")
        
        # Check if we have enough data
        if len(data) < sequence_length + 1:
            raise ValueError(
                f"Not enough historical data for LSTM training. "
                f"Need at least {sequence_length + 1} days, got {len(data)} days."
            )
        
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
        
        # Check minimum sequences
        if len(X) < 24:
            raise ValueError(
                f"Not enough historical data for LSTM training. "
                f"Created only {len(X)} sequences, need at least 24."
            )
        
        print(f"X shape: {X.shape}")
        print(f"y shape: {y.shape}")
        
        return X, y
    
    def prepare_data(
        self,
        commodity: str,
        sequence_length: int = 12,
        train_split: float = 0.8
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, int]:
        """
        Complete data preparation pipeline.
        
        Args:
            commodity: Crop/commodity name
            sequence_length: Sequence window size (days)
            train_split: Train/test split ratio
            
        Returns:
            Tuple of (X_train, X_test, y_train, y_test, total_days)
        """
        # Load data (chunked, memory-efficient)
        self.load_data_chunked(commodity)
        
        # Create national daily series
        daily_data = self.create_national_daily_series()
        
        # Fill missing days
        daily_data = self.fill_missing_days(daily_data)
        
        total_days = len(daily_data)
        print(f"\nTotal days in dataset: {total_days}")
        
        # Create sequences
        X, y = self.create_sequences(daily_data, sequence_length)
        
        # Train/test split
        split_idx = int(len(X) * train_split)
        
        X_train = X[:split_idx]
        X_test = X[split_idx:]
        y_train = y[:split_idx]
        y_test = y[split_idx:]
        
        print(f"Train set: {len(X_train)} sequences")
        print(f"Test set: {len(X_test)} sequences")
        
        return X_train, X_test, y_train, y_test, total_days
    
    def get_last_sequence(
        self,
        commodity: str,
        sequence_length: int = 12
    ) -> np.ndarray:
        """
        Get the last N days of data for prediction.
        
        Args:
            commodity: Crop/commodity name
            sequence_length: Number of days
            
        Returns:
            Scaled sequence ready for prediction
        """
        self.load_data_chunked(commodity)
        daily_data = self.create_national_daily_series()
        daily_data = self.fill_missing_days(daily_data)
        
        # Get last N days
        last_prices = daily_data['price'].values[-sequence_length:]
        
        if len(last_prices) < sequence_length:
            raise ValueError(
                f"Not enough data. Need {sequence_length} days, got {len(last_prices)}"
            )
        
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
    
    dataset_dir = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        'dataset'
    )
    
    loader = PriceDatasetLoader(dataset_dir)
    
    # Test with rice
    print("\n" + "=" * 60)
    print("TESTING PRICE DATASET LOADER")
    print("=" * 60 + "\n")
    
    try:
        X_train, X_test, y_train, y_test, total_days = loader.prepare_data('rice', sequence_length=12)
        print("\nDataset preparation complete!")
        print(f"Total days: {total_days}")
        print(f"Total sequences: {len(X_train) + len(X_test)}")
    except Exception as e:
        print(f"Error: {e}")
