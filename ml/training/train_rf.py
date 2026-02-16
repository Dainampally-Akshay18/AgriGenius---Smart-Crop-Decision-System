"""
Random Forest training script for crop recommendation.
"""
import os
import pickle
from datetime import datetime
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import sys

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from preprocessing.clean import load_dataset
from preprocessing.encode import CropLabelEncoder
from preprocessing.scale import FeatureScaler
from features.feature_builder import prepare_features
from training.split import split_data


def train_random_forest(dataset_path: str, models_dir: str):
    """
    Train Random Forest model for crop recommendation.
    
    Args:
        dataset_path: Path to CSV dataset
        models_dir: Directory to save trained models
    """
    print("=" * 60)
    print("RANDOM FOREST TRAINING - CROP RECOMMENDATION")
    print("=" * 60)
    print(f"Start time: {datetime.now()}")
    print()
    
    # Step 1: Load and clean data
    print("Step 1: Loading and cleaning data...")
    df = load_dataset(dataset_path)
    print()
    
    # Step 2: Feature engineering
    print("Step 2: Feature engineering...")
    X = prepare_features(df)
    y = df['label']
    print(f"Features shape: {X.shape}")
    print(f"Labels shape: {y.shape}")
    print()
    
    # Step 3: Encode labels
    print("Step 3: Encoding labels...")
    label_encoder = CropLabelEncoder()
    label_encoder.fit(y)
    y_encoded = label_encoder.transform(y)
    print()
    
    # Step 4: Scale features
    print("Step 4: Scaling features...")
    scaler = FeatureScaler()
    X_scaled = scaler.fit_transform(X)
    print()
    
    # Step 5: Split data
    print("Step 5: Splitting data (80/20)...")
    X_train, X_test, y_train, y_test = split_data(X_scaled, y_encoded)
    print()
    
    # Step 6: Train Random Forest
    print("Step 6: Training Random Forest...")
    rf_model = RandomForestClassifier(
        n_estimators=100,
        max_depth=20,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=42,
        n_jobs=-1,
        verbose=1
    )
    rf_model.fit(X_train, y_train)
    print("Training complete!")
    print()
    
    # Step 7: Evaluate model
    print("Step 7: Evaluating model...")
    y_pred_train = rf_model.predict(X_train)
    y_pred_test = rf_model.predict(X_test)
    
    train_accuracy = accuracy_score(y_train, y_pred_train)
    test_accuracy = accuracy_score(y_test, y_pred_test)
    
    # Import additional metrics
    from sklearn.metrics import precision_score, recall_score, f1_score
    test_precision = precision_score(y_test, y_pred_test, average='weighted', zero_division=0)
    test_recall = recall_score(y_test, y_pred_test, average='weighted', zero_division=0)
    test_f1 = f1_score(y_test, y_pred_test, average='weighted', zero_division=0)
    
    print(f"Train Accuracy: {train_accuracy:.4f}")
    print(f"Test Accuracy: {test_accuracy:.4f}")
    print(f"Test Precision: {test_precision:.4f}")
    print(f"Test Recall: {test_recall:.4f}")
    print(f"Test F1 Score: {test_f1:.4f}")
    print()
    
    print("Classification Report (Test Set):")
    print(classification_report(
        y_test,
        y_pred_test,
        target_names=label_encoder.encoder.classes_
    ))
    print()
    
    # Step 8: Save artifacts
    print("Step 8: Saving model artifacts...")
    os.makedirs(models_dir, exist_ok=True)
    
    # Save Random Forest model
    rf_path = os.path.join(models_dir, 'rf.pkl')
    with open(rf_path, 'wb') as f:
        pickle.dump(rf_model, f)
    print(f"Model saved to {rf_path}")
    
    # Save scaler
    scaler_path = os.path.join(models_dir, 'scaler.pkl')
    scaler.save(scaler_path)
    
    # Save encoder
    encoder_path = os.path.join(models_dir, 'encoder.pkl')
    label_encoder.save(encoder_path)
    
    print()
    print("=" * 60)
    print("TRAINING COMPLETE")
    print("=" * 60)
    print(f"End time: {datetime.now()}")
    print(f"Test Accuracy: {test_accuracy:.4f}")
    print(f"Acceptance Criteria: ≥ 0.95")
    
    if test_accuracy >= 0.95:
        print("✓ Model meets acceptance criteria!")
    else:
        print("✗ Model does not meet acceptance criteria")
    
    return {
        'model': 'Random Forest',
        'accuracy': test_accuracy,
        'precision': test_precision,
        'recall': test_recall,
        'f1': test_f1
    }


if __name__ == "__main__":
    # Paths
    dataset_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        'dataset',
        'Crop_recommendation.csv'
    )
    models_dir = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        'models'
    )
    
    # Train model
    train_random_forest(dataset_path, models_dir)
