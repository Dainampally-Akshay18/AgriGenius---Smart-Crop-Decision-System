"""
Missing feature simulation for robustness testing.
"""
import sys
import os
from typing import Dict, List

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from inference.predict_crop import predict_crop


class MissingDataSimulator:
    """Simulate missing features and measure impact."""
    
    # Default values for missing features
    FEATURE_DEFAULTS = {
        'N': 50,
        'P': 35,
        'K': 40,
        'temperature': 25.0,
        'humidity': 70.0,
        'ph': 6.5,
        'rainfall': 100.0
    }
    
    @staticmethod
    def simulate_missing_feature(
        base_input: Dict,
        missing_feature: str,
        default_value: float = None
    ) -> Dict:
        """
        Create input with one feature replaced by default.
        
        Args:
            base_input: Original input
            missing_feature: Feature to simulate as missing
            default_value: Value to use (if None, uses FEATURE_DEFAULTS)
            
        Returns:
            Modified input dictionary
        """
        modified_input = base_input.copy()
        
        if default_value is None:
            default_value = MissingDataSimulator.FEATURE_DEFAULTS.get(missing_feature, 0)
        
        modified_input[missing_feature] = default_value
        
        return modified_input
    
    @staticmethod
    def evaluate_missing_features(
        base_input: Dict,
        features_to_test: List[str] = None
    ) -> Dict:
        """
        Evaluate impact of missing features.
        
        Args:
            base_input: Original input with all features
            features_to_test: List of features to test (default: all)
            
        Returns:
            Dictionary with results for each missing feature scenario
        """
        if features_to_test is None:
            features_to_test = ['N', 'P', 'K', 'temperature', 'humidity', 'rainfall']
        
        print("Evaluating missing feature scenarios...")
        
        # Baseline prediction
        baseline_result = predict_crop(**base_input)
        baseline_crop = baseline_result['recommended_crop']
        baseline_confidence = baseline_result['confidence']
        
        print(f"Baseline: {baseline_crop} (confidence: {baseline_confidence:.4f})")
        
        results = {
            'baseline': {
                'crop': baseline_crop,
                'confidence': baseline_confidence,
                'changed': False
            }
        }
        
        # Test each missing feature
        for feature in features_to_test:
            print(f"\nTesting missing feature: {feature}")
            
            # Create input with missing feature
            modified_input = MissingDataSimulator.simulate_missing_feature(
                base_input,
                feature
            )
            
            # Predict with missing feature
            result = predict_crop(**modified_input)
            predicted_crop = result['recommended_crop']
            confidence = result['confidence']
            
            # Check if prediction changed
            changed = (predicted_crop != baseline_crop)
            
            results[f'missing_{feature}'] = {
                'crop': predicted_crop,
                'confidence': confidence,
                'changed': changed,
                'confidence_drop': baseline_confidence - confidence
            }
            
            status = "CHANGED" if changed else "SAME"
            print(f"  Result: {predicted_crop} (confidence: {confidence:.4f}) [{status}]")
        
        # Compute summary statistics
        total_tests = len(features_to_test)
        changes = sum(1 for key in results if key != 'baseline' and results[key]['changed'])
        stability = 1 - (changes / total_tests)
        
        results['summary'] = {
            'total_tests': total_tests,
            'prediction_changes': changes,
            'stability_score': round(stability, 4)
        }
        
        return results


if __name__ == "__main__":
    # Test missing data simulation
    print("\n" + "=" * 60)
    print("TESTING MISSING FEATURE SIMULATION")
    print("=" * 60 + "\n")
    
    test_input = {
        'N': 90,
        'P': 42,
        'K': 43,
        'temperature': 20.87,
        'humidity': 82.00,
        'ph': 6.50,
        'rainfall': 202.93
    }
    
    print("Base Input:")
    for key, value in test_input.items():
        print(f"  {key}: {value}")
    print()
    
    # Evaluate missing features
    results = MissingDataSimulator.evaluate_missing_features(test_input)
    
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Total tests: {results['summary']['total_tests']}")
    print(f"Prediction changes: {results['summary']['prediction_changes']}")
    print(f"Stability score: {results['summary']['stability_score']:.4f}")
    print()
