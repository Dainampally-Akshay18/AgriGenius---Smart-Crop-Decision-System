"""
Multi-model comparison and agreement analysis.
"""
import sys
import os
from typing import Dict, List
from collections import Counter

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from inference.predict_all_models import predict_all_models


class ModelComparison:
    """Compare predictions across multiple models."""
    
    @staticmethod
    def compute_agreement(
        N: float,
        P: float,
        K: float,
        temperature: float,
        humidity: float,
        ph: float,
        rainfall: float
    ) -> Dict:
        """
        Compute agreement across all available models.
        
        Args:
            Input features for prediction
            
        Returns:
            Dictionary with agreement metrics
        """
        print("Computing multi-model agreement...")
        
        # Get predictions from all models
        predictions = predict_all_models(
            N=N, P=P, K=K,
            temperature=temperature,
            humidity=humidity,
            ph=ph,
            rainfall=rainfall
        )
        
        if not predictions:
            return {
                'error': 'No models available',
                'agreement_ratio': 0.0
            }
        
        print(f"Models available: {len(predictions)}")
        for model_name, crop in predictions.items():
            print(f"  {model_name.upper()}: {crop}")
        
        # Count predictions
        prediction_counts = Counter(predictions.values())
        most_common_crop, most_common_count = prediction_counts.most_common(1)[0]
        
        # Compute agreement ratio
        total_models = len(predictions)
        agreement_ratio = most_common_count / total_models
        
        # Check if all models agree
        all_agree = (len(prediction_counts) == 1)
        
        return {
            'predictions': predictions,
            'total_models': total_models,
            'most_common_crop': most_common_crop,
            'agreement_count': most_common_count,
            'agreement_ratio': round(agreement_ratio, 4),
            'all_agree': all_agree,
            'prediction_distribution': dict(prediction_counts)
        }
    
    @staticmethod
    def evaluate_model_stability(
        base_input: Dict,
        noise_percentage: float = 0.2,
        num_runs: int = 20
    ) -> Dict:
        """
        Evaluate stability of model agreement under noise.
        
        Args:
            base_input: Original input parameters
            noise_percentage: Noise level
            num_runs: Number of noisy runs
            
        Returns:
            Dictionary with stability metrics
        """
        from evaluation.noise_injection import NoiseInjector
        
        print(f"\nEvaluating model agreement stability ({num_runs} runs)...")
        
        # Baseline agreement
        baseline_agreement = ModelComparison.compute_agreement(**base_input)
        baseline_crop = baseline_agreement['most_common_crop']
        
        # Generate noisy inputs
        noisy_inputs = NoiseInjector.generate_noisy_inputs(
            base_input,
            noise_percentage,
            num_runs
        )
        
        # Track agreement across noisy inputs
        agreement_ratios = []
        stable_predictions = 0
        
        for noisy_input in noisy_inputs:
            agreement = ModelComparison.compute_agreement(**noisy_input)
            agreement_ratios.append(agreement['agreement_ratio'])
            
            if agreement['most_common_crop'] == baseline_crop:
                stable_predictions += 1
        
        # Compute statistics
        avg_agreement = sum(agreement_ratios) / len(agreement_ratios)
        stability_score = stable_predictions / num_runs
        
        return {
            'baseline_crop': baseline_crop,
            'baseline_agreement': baseline_agreement['agreement_ratio'],
            'avg_agreement_under_noise': round(avg_agreement, 4),
            'stability_score': round(stability_score, 4),
            'stable_predictions': stable_predictions,
            'total_runs': num_runs
        }


if __name__ == "__main__":
    # Test model comparison
    print("\n" + "=" * 60)
    print("TESTING MULTI-MODEL COMPARISON")
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
    
    # Compute agreement
    agreement = ModelComparison.compute_agreement(**test_input)
    
    print("\nAgreement Results:")
    print(f"  Total models: {agreement['total_models']}")
    print(f"  Most common crop: {agreement['most_common_crop']}")
    print(f"  Agreement ratio: {agreement['agreement_ratio']:.4f}")
    print(f"  All agree: {agreement['all_agree']}")
    print(f"\n  Prediction distribution:")
    for crop, count in agreement['prediction_distribution'].items():
        print(f"    {crop}: {count}")
    print()
