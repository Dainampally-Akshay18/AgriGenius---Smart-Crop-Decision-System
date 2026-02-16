"""
Evaluation pipeline orchestrator.
"""
import sys
import os
from typing import Dict

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from evaluation.noise_injection import NoiseInjector
from evaluation.rss import RSSCalculator
from evaluation.missing_data import MissingDataSimulator
from evaluation.model_comparison import ModelComparison
from evaluation.confidence import ConfidenceEstimator


class EvaluationRunner:
    """Orchestrate complete evaluation pipeline."""
    
    @staticmethod
    def run_full_evaluation(
        base_input: Dict,
        rss_runs: int = 50,
        noise_level: float = 0.2
    ) -> Dict:
        """
        Run complete evaluation pipeline.
        
        Args:
            base_input: Input parameters
            rss_runs: Number of runs for RSS
            noise_level: Noise level for perturbations
            
        Returns:
            Dictionary with all evaluation results
        """
        print("\n" + "=" * 80)
        print("RUNNING FULL EVALUATION PIPELINE")
        print("=" * 80 + "\n")
        
        print("Input Parameters:")
        for key, value in base_input.items():
            print(f"  {key}: {value}")
        print()
        
        results = {}
        
        # 1. Noise Injection Test
        print("\n" + "-" * 80)
        print("1. NOISE INJECTION TEST")
        print("-" * 80)
        rss_result = RSSCalculator.compute_rss(
            base_input,
            noise_percentage=noise_level,
            num_runs=rss_runs
        )
        results['noise_test'] = rss_result
        
        # 2. Missing Feature Test
        print("\n" + "-" * 80)
        print("2. MISSING FEATURE TEST")
        print("-" * 80)
        missing_result = MissingDataSimulator.evaluate_missing_features(base_input)
        results['missing_feature_test'] = missing_result
        
        # 3. Model Agreement Test
        print("\n" + "-" * 80)
        print("3. MODEL AGREEMENT TEST")
        print("-" * 80)
        agreement_result = ModelComparison.compute_agreement(**base_input)
        results['model_agreement'] = agreement_result
        
        # 4. Confidence Estimation
        print("\n" + "-" * 80)
        print("4. CONFIDENCE ESTIMATION")
        print("-" * 80)
        confidence_result = ConfidenceEstimator.compute_confidence(
            base_input,
            include_rss=True,
            include_agreement=True,
            rss_runs=30,
            noise_level=noise_level
        )
        results['confidence'] = confidence_result
        
        # Summary
        print("\n" + "=" * 80)
        print("EVALUATION SUMMARY")
        print("=" * 80)
        print(f"Recommended Crop: {rss_result['baseline_crop']}")
        print(f"Final Confidence: {confidence_result['confidence']:.4f}")
        print(f"Confidence Level: {ConfidenceEstimator.get_confidence_level(confidence_result['confidence'])}")
        print(f"\nRobustness Metrics:")
        print(f"  RSS (Stability): {rss_result['rss']:.4f}")
        print(f"  Missing Feature Stability: {missing_result['summary']['stability_score']:.4f}")
        print(f"  Model Agreement: {agreement_result['agreement_ratio']:.4f}")
        print()
        
        return results


if __name__ == "__main__":
    # Run full evaluation
    test_input = {
        'N': 90,
        'P': 42,
        'K': 43,
        'temperature': 20.87,
        'humidity': 82.00,
        'ph': 6.50,
        'rainfall': 202.93
    }
    
    results = EvaluationRunner.run_full_evaluation(
        test_input,
        rss_runs=50,
        noise_level=0.2
    )
