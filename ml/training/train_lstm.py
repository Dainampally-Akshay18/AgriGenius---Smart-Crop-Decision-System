"""
LSTM training script for crop price forecasting.
"""
import os
import sys
from datetime import datetime
import numpy as np
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from sklearn.metrics import mean_squared_error, mean_absolute_error
import matplotlib.pyplot as plt

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from preprocessing.price_dataset import PriceDatasetLoader


def build_lstm_model(sequence_length: int = 12) -> Sequential:
    """
    Build LSTM model architecture.
    
    Args:
        sequence_length: Input sequence length
        
    Returns:
        Compiled LSTM model
    """
    model = Sequential([
        # First LSTM layer
        LSTM(units=50, return_sequences=True, input_shape=(sequence_length, 1)),
        Dropout(0.2),
        
        # Second LSTM layer
        LSTM(units=50, return_sequences=False),
        Dropout(0.2),
        
        # Dense output layer
        Dense(units=1)
    ])
    
    model.compile(
        optimizer='adam',
        loss='mean_squared_error',
        metrics=['mae']
    )
    
    return model


def train_lstm(
    commodity: str,
    dataset_path: str,
    models_dir: str,
    sequence_length: int = 12,
    epochs: int = 100,
    batch_size: int = 32
):
    """
    Train LSTM model for price forecasting.
    
    Args:
        commodity: Crop/commodity name
        dataset_path: Path to CSV dataset
        models_dir: Directory to save trained models
        sequence_length: Input sequence length
        epochs: Training epochs
        batch_size: Batch size
    """
    print("=" * 60)
    print(f"LSTM TRAINING - PRICE FORECASTING ({commodity.upper()})")
    print("=" * 60)
    print(f"Start time: {datetime.now()}")
    print()
    
    # Step 1: Load and prepare data
    print("Step 1: Loading and preparing data...")
    loader = PriceDatasetLoader(dataset_path)
    X_train, X_test, y_train, y_test = loader.prepare_data(
        commodity=commodity,
        sequence_length=sequence_length,
        train_split=0.8
    )
    print()
    
    # Step 2: Build model
    print("Step 2: Building LSTM model...")
    model = build_lstm_model(sequence_length)
    print(model.summary())
    print()
    
    # Step 3: Setup callbacks
    print("Step 3: Setting up training callbacks...")
    os.makedirs(models_dir, exist_ok=True)
    
    checkpoint_path = os.path.join(models_dir, f'lstm_{commodity}_best.keras')
    callbacks = [
        EarlyStopping(
            monitor='val_loss',
            patience=10,
            restore_best_weights=True,
            verbose=1
        ),
        ModelCheckpoint(
            checkpoint_path,
            monitor='val_loss',
            save_best_only=True,
            verbose=1
        )
    ]
    print()
    
    # Step 4: Train model
    print("Step 4: Training LSTM model...")
    history = model.fit(
        X_train, y_train,
        epochs=epochs,
        batch_size=batch_size,
        validation_data=(X_test, y_test),
        callbacks=callbacks,
        verbose=1
    )
    print("Training complete!")
    print()
    
    # Step 5: Evaluate model
    print("Step 5: Evaluating model...")
    
    # Predictions
    y_pred_train = model.predict(X_train)
    y_pred_test = model.predict(X_test)
    
    # Inverse transform to get actual prices
    y_train_actual = loader.scaler.inverse_transform(y_train)
    y_test_actual = loader.scaler.inverse_transform(y_test)
    y_pred_train_actual = loader.scaler.inverse_transform(y_pred_train)
    y_pred_test_actual = loader.scaler.inverse_transform(y_pred_test)
    
    # Calculate metrics
    train_rmse = np.sqrt(mean_squared_error(y_train_actual, y_pred_train_actual))
    test_rmse = np.sqrt(mean_squared_error(y_test_actual, y_pred_test_actual))
    train_mae = mean_absolute_error(y_train_actual, y_pred_train_actual)
    test_mae = mean_absolute_error(y_test_actual, y_pred_test_actual)
    
    print(f"Train RMSE: {train_rmse:.2f}")
    print(f"Test RMSE: {test_rmse:.2f}")
    print(f"Train MAE: {train_mae:.2f}")
    print(f"Test MAE: {test_mae:.2f}")
    
    # Calculate percentage error
    avg_price = np.mean(y_test_actual)
    rmse_percentage = (test_rmse / avg_price) * 100
    print(f"Test RMSE as % of avg price: {rmse_percentage:.2f}%")
    print()
    
    # Step 6: Save artifacts
    print("Step 6: Saving model artifacts...")
    
    # Save final model
    model_path = os.path.join(models_dir, 'lstm_model.keras')
    model.save(model_path)
    print(f"Model saved to {model_path}")
    
    # Save scaler
    scaler_path = os.path.join(models_dir, 'lstm_scaler.pkl')
    loader.save_scaler(scaler_path)
    
    print()
    print("=" * 60)
    print("TRAINING COMPLETE")
    print("=" * 60)
    print(f"End time: {datetime.now()}")
    print(f"Test RMSE: {test_rmse:.2f}")
    print(f"Acceptance Criteria: RMSE ≤ 10% of avg price")
    
    if rmse_percentage <= 10:
        print("✓ Model meets acceptance criteria!")
    else:
        print("✗ Model does not meet acceptance criteria")
    print()
    
    return {
        'train_rmse': train_rmse,
        'test_rmse': test_rmse,
        'train_mae': train_mae,
        'test_mae': test_mae,
        'rmse_percentage': rmse_percentage
    }


if __name__ == "__main__":
    # Paths
    dataset_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        'dataset',
        'Prices.csv'
    )
    models_dir = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        'models'
    )
    
    # Train model for rice
    commodity = 'rice'
    print(f"\nTraining LSTM model for: {commodity}")
    
    train_lstm(
        commodity=commodity,
        dataset_path=dataset_path,
        models_dir=models_dir,
        sequence_length=12,
        epochs=100,
        batch_size=32
    )

