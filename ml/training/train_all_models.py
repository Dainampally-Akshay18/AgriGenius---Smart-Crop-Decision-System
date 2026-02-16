"""
Train all models and generate comparison report.
"""
import os
import sys
from datetime import datetime
from tabulate import tabulate

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from training.train_rf import train_random_forest
from training.train_xgb import train_xgboost
from training.train_svm import train_svm
from training.train_mlp import train_mlp


def train_all_models():
    """Train all classification models and generate comparison."""
    
    print("\n" + "=" * 80)
    print("TRAINING ALL MODELS - CROP RECOMMENDATION")
    print("=" * 80)
    print(f"Start time: {datetime.now()}")
    print()
    
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
    
    results = []
    
    # Train Random Forest
    print("\n" + "=" * 80)
    print("TRAINING MODEL 1/4: RANDOM FOREST")
    print("=" * 80 + "\n")
    try:
        rf_result = train_random_forest(dataset_path, models_dir)
        results.append(rf_result)
    except Exception as e:
        print(f"Error training Random Forest: {e}")
        results.append({
            'model': 'Random Forest',
            'accuracy': 0,
            'precision': 0,
            'recall': 0,
            'f1': 0
        })
    
    # Train XGBoost
    print("\n" + "=" * 80)
    print("TRAINING MODEL 2/4: XGBOOST")
    print("=" * 80 + "\n")
    try:
        xgb_result = train_xgboost(dataset_path, models_dir)
        results.append(xgb_result)
    except Exception as e:
        print(f"Error training XGBoost: {e}")
        results.append({
            'model': 'XGBoost',
            'accuracy': 0,
            'precision': 0,
            'recall': 0,
            'f1': 0
        })
    
    # Train SVM
    print("\n" + "=" * 80)
    print("TRAINING MODEL 3/4: SVM")
    print("=" * 80 + "\n")
    try:
        svm_result = train_svm(dataset_path, models_dir)
        results.append(svm_result)
    except Exception as e:
        print(f"Error training SVM: {e}")
        results.append({
            'model': 'SVM',
            'accuracy': 0,
            'precision': 0,
            'recall': 0,
            'f1': 0
        })
    
    # Train MLP
    print("\n" + "=" * 80)
    print("TRAINING MODEL 4/4: MLP (NEURAL NETWORK)")
    print("=" * 80 + "\n")
    try:
        mlp_result = train_mlp(dataset_path, models_dir)
        results.append(mlp_result)
    except Exception as e:
        print(f"Error training MLP: {e}")
        results.append({
            'model': 'MLP',
            'accuracy': 0,
            'precision': 0,
            'recall': 0,
            'f1': 0
        })
    
    # Generate comparison table
    print("\n" + "=" * 80)
    print("MODEL COMPARISON SUMMARY")
    print("=" * 80 + "\n")
    
    # Prepare table data
    table_data = []
    for result in results:
        table_data.append([
            result['model'],
            f"{result['accuracy']:.4f}",
            f"{result['precision']:.4f}",
            f"{result['recall']:.4f}",
            f"{result['f1']:.4f}"
        ])
    
    # Sort by accuracy (descending)
    table_data.sort(key=lambda x: float(x[1]), reverse=True)
    
    # Print table
    headers = ['Model', 'Accuracy', 'Precision', 'Recall', 'F1 Score']
    print(tabulate(table_data, headers=headers, tablefmt='grid'))
    print()
    
    # Find best model
    best_model = max(results, key=lambda x: x['accuracy'])
    print(f"Best Model: {best_model['model']} (Accuracy: {best_model['accuracy']:.4f})")
    print()
    
    # Check acceptance criteria (≥95% accuracy)
    print("Acceptance Criteria: Accuracy ≥ 0.95")
    for result in results:
        status = "✓ PASS" if result['accuracy'] >= 0.95 else "✗ FAIL"
        print(f"  {result['model']}: {result['accuracy']:.4f} [{status}]")
    print()
    
    print("=" * 80)
    print(f"End time: {datetime.now()}")
    print("=" * 80)
    print()
    
    return results


if __name__ == "__main__":
    train_all_models()
