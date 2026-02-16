"""
Recommendation Stability Score (RSS) computation.
"""
import sys
import os
from typing import Dict, List
from collections import Counter

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from inference.predict_crop import predict_crop
from evaluation.noise_injection import NoiseInjector


class RSSCalculator:
    """Calculate Recommendation Stability Score."""
    
    @staticmethod
    def compute_rss(
        base_input: Dict,
        noise_percentage: float = 0.2,
        num_runs: int = 50
    ) -> Dict:
        """
        Compute Recommendation Stability Score.
        
        RSS = percentage of predictions that remain unchanged under noise
        
        Args:
            base_input: Original input parameters
            noise_percentage: Noise level (default 20%)
            num_runs: Number of noisy predictions to run
            
        Returns:
            Dictionary with RSS metrics
        """
        print(f"Computing RSS with {num_runs} runs at {noise_percentage*100}% noise...")
        
        # Get baseline prediction
        baseline_result = predict_crop(**base_input)
        baseline_crop = baseline_result['recommended_crop']
        
        print(f"Baseline prediction: {baseline_crop}")
        
        # Generate noisy inputs
        noisy_inputs = NoiseInjector.generate_noisy_inputs(
            base_input,
            noise_percentage,
            num_runs
        )
        
        # Run predictions on noisy inputs
        predictions = []
        for noisy_input in noisy_inputs:
            result = predict_crop(**noisy_input)
            predictions.append(result['recommended_crop'])
        
        # Count how many predictions match baseline
        matches = sum(1 for pred in predictions if pred == baseline_crop)
        rss = matches / num_runs
        
        # Count prediction changes
        prediction_changes = num_runs - matches
        
        # Get distribution of predictions
        prediction_counts = Counter(predictions)
        
        return {
            'rss': round(rss, 4),
            'baseline_crop': baseline_crop,
            'total_runs': num_runs,
            'matches': matches,
            'prediction_changes': prediction_changes,
            'noise_percentage': noise_percentage,
            'prediction_distribution': dict(prediction_counts)
        }
    
    @staticmethod
    def compute_rss_multi_level(
        base_input: Dict,
        noise_levels: List[float] = None,
        runs_per_level: int = 50
    ) -> Dict:
        """
        Compute RSS at multiple noise levels.
        
        Args:
            base_input: Original input parameters
            noise_levels: List of noise percentages
            runs_per_level: Number of runs per noise level
            
        Returns:
            Dictionary with RSS at each noise level
        """
        if noise_levels is None:
            noise_levels = [0.1, 0.2, 0.3, 0.4]
        
        results = {}
        
        for noise_level in noise_levels:
            print(f"\nNoise level: {noise_level*100}%")
            rss_result = RSSCalculator.compute_rss(
                base_input,
                noise_level,
                runs_per_level
            )
            results[noise_level] = rss_result
        
        return results


if __name__ == "__main__":
    # Test RSS calculation
    print("\n" + "=" * 60)
    print("TESTING RECOMMENDATION STABILITY SCORE (RSS)")
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
    
    print("Input:")
    for key, value in test_input.items():
        print(f"  {key}: {value}")
    print()
    
    # Compute RSS
    rss_result = RSSCalculator.compute_rss(test_input, noise_percentage=0.2, num_runs=50)
    
    print("\nRSS Results:")
    print(f"  RSS Score: {rss_result['rss']:.4f} ({rss_result['rss']*100:.2f}%)")
    print(f"  Baseline Crop: {rss_result['baseline_crop']}")
    print(f"  Matches: {rss_result['matches']}/{rss_result['total_runs']}")
    print(f"  Prediction Changes: {rss_result['prediction_changes']}")
    print(f"  Noise Level: {rss_result['noise_percentage']*100}%")
    print(f"\n  Prediction Distribution:")
    for crop, count in rss_result['prediction_distribution'].items():
        percentage = (count / rss_result['total_runs']) * 100
        print(f"    {crop}: {count} ({percentage:.1f}%)")
    print()
