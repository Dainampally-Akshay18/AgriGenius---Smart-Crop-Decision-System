"""
Confidence estimation combining multiple metrics.
"""
import sys
import os
from typing import Dict

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from inference.predict_crop import predict_crop
from evaluation.rss import RSSCalculator
from evaluation.model_comparison import ModelComparison


class ConfidenceEstimator:
    """Estimate prediction confidence from multiple sources."""
    
    @staticmethod
    def compute_confidence(
        base_input: Dict,
        include_rss: bool = True,
        include_agreement: bool = True,
        rss_runs: int = 30,
        noise_level: float = 0.2
    ) -> Dict:
        """
        Compute comprehensive confidence score.
        
        Confidence is derived from:
        1. Model probability (from Random Forest)
        2. Stability under perturbations (RSS)
        3. Agreement across models (if multiple models available)
        
        Args:
            base_input: Input parameters
            include_rss: Whether to compute RSS
            include_agreement: Whether to compute model agreement
            rss_runs: Number of runs for RSS calculation
            noise_level: Noise level for RSS
            
        Returns:
            Dictionary with confidence metrics
        """
        print("Computing comprehensive confidence score...")
        
        # 1. Get base prediction with probability
        prediction_result = predict_crop(**base_input)
        crop = prediction_result['recommended_crop']
        probability = prediction_result['confidence']
        
        print(f"Predicted crop: {crop}")
        print(f"Model probability: {probability:.4f}")
        
        confidence_components = {
            'probability': probability
        }
        
        # 2. Compute RSS (stability)
        stability_score = None
        if include_rss:
            print(f"\nComputing stability (RSS with {rss_runs} runs)...")
            rss_result = RSSCalculator.compute_rss(
                base_input,
                noise_percentage=noise_level,
                num_runs=rss_runs
            )
            stability_score = rss_result['rss']
            confidence_components['stability'] = stability_score
            print(f"Stability score: {stability_score:.4f}")
        
        # 3. Compute model agreement
        agreement_score = None
        if include_agreement:
            print("\nComputing model agreement...")
            agreement_result = ModelComparison.compute_agreement(**base_input)
            agreement_score = agreement_result['agreement_ratio']
            confidence_components['agreement'] = agreement_score
            print(f"Agreement score: {agreement_score:.4f}")
        
        # 4. Combine scores
        # Weighted average: probability (50%), stability (30%), agreement (20%)
        weights = {
            'probability': 0.5,
            'stability': 0.3,
            'agreement': 0.2
        }
        
        total_weight = 0
        weighted_sum = 0
        
        for component, score in confidence_components.items():
            if score is not None:
                weighted_sum += score * weights[component]
                total_weight += weights[component]
        
        # Normalize by actual weights used
        final_confidence = weighted_sum / total_weight if total_weight > 0 else 0
        
        print(f"\nFinal confidence: {final_confidence:.4f}")
        
        return {
            'crop': crop,
            'confidence': round(final_confidence, 4),
            'components': {
                'probability': round(probability, 4),
                'stability': round(stability_score, 4) if stability_score else None,
                'agreement': round(agreement_score, 4) if agreement_score else None
            },
            'weights': weights
        }
    
    @staticmethod
    def get_confidence_level(confidence: float) -> str:
        """
        Get confidence level label.
        
        Args:
            confidence: Confidence score (0-1)
            
        Returns:
            Confidence level string
        """
        if confidence >= 0.9:
            return "Very High"
        elif confidence >= 0.75:
            return "High"
        elif confidence >= 0.6:
            return "Medium"
        elif confidence >= 0.4:
            return "Low"
        else:
            return "Very Low"


if __name__ == "__main__":
    # Test confidence estimation
    print("\n" + "=" * 60)
    print("TESTING CONFIDENCE ESTIMATION")
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
    
    # Compute confidence
    confidence_result = ConfidenceEstimator.compute_confidence(
        test_input,
        include_rss=True,
        include_agreement=True,
        rss_runs=30
    )
    
    print("\n" + "=" * 60)
    print("CONFIDENCE RESULTS")
    print("=" * 60)
    print(f"Crop: {confidence_result['crop']}")
    print(f"Final Confidence: {confidence_result['confidence']:.4f}")
    print(f"Confidence Level: {ConfidenceEstimator.get_confidence_level(confidence_result['confidence'])}")
    print("\nComponents:")
    for component, score in confidence_result['components'].items():
        if score is not None:
            weight = confidence_result['weights'][component]
            print(f"  {component.capitalize()}: {score:.4f} (weight: {weight})")
    print()
