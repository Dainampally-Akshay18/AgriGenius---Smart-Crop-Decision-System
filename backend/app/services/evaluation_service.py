"""
Evaluation service that integrates ML evaluation modules.
"""
from typing import Dict
from datetime import datetime

# Import from ml evaluation modules (path configured at startup)
from ml.evaluation.rss import RSSCalculator
from ml.evaluation.missing_data import MissingDataSimulator
from ml.evaluation.model_comparison import ModelComparison
from ml.evaluation.confidence import ConfidenceEstimator

from app.utils.logger import logger



class EvaluationService:
    """Service for robustness and confidence evaluation."""
    
    @staticmethod
    async def evaluate_noise(
        N: float,
        P: float,
        K: float,
        temperature: float,
        humidity: float,
        rainfall: float,
        ph: float = 6.5,
        noise_percentage: float = 0.2,
        num_runs: int = 50
    ) -> Dict:
        """
        Evaluate prediction stability under noise.
        
        Args:
            Input features and noise parameters
            
        Returns:
            Dictionary with RSS and noise test results
        """
        logger.info("Running noise evaluation...")
        
        base_input = {
            'N': N, 'P': P, 'K': K,
            'temperature': temperature,
            'humidity': humidity,
            'ph': ph,
            'rainfall': rainfall
        }
        
        # Call ML evaluation module
        rss_result = RSSCalculator.compute_rss(
            base_input,
            noise_percentage=noise_percentage,
            num_runs=num_runs
        )
        
        logger.info(f"Noise evaluation complete: RSS={rss_result['rss']:.4f}")
        
        return {
            'predicted_crop': rss_result['baseline_crop'],
            'rss': rss_result['rss'],
            'prediction_changes': rss_result['prediction_changes'],
            'total_runs': rss_result['total_runs'],
            'noise_percentage': rss_result['noise_percentage'],
            'prediction_distribution': rss_result['prediction_distribution']
        }
    
    @staticmethod
    async def evaluate_missing_features(
        N: float,
        P: float,
        K: float,
        temperature: float,
        humidity: float,
        rainfall: float,
        ph: float = 6.5
    ) -> Dict:
        """
        Evaluate prediction robustness with missing features.
        
        Args:
            Input features
            
        Returns:
            Dictionary with missing feature test results
        """
        logger.info("Running missing feature evaluation...")
        
        base_input = {
            'N': N, 'P': P, 'K': K,
            'temperature': temperature,
            'humidity': humidity,
            'ph': ph,
            'rainfall': rainfall
        }
        
        # Call ML evaluation module
        missing_result = MissingDataSimulator.evaluate_missing_features(base_input)
        
        logger.info(f"Missing feature evaluation complete: stability={missing_result['summary']['stability_score']:.4f}")
        
        return {
            'predicted_crop': missing_result['baseline']['crop'],
            'baseline_confidence': missing_result['baseline']['confidence'],
            'stability_score': missing_result['summary']['stability_score'],
            'total_tests': missing_result['summary']['total_tests'],
            'prediction_changes': missing_result['summary']['prediction_changes'],
            'feature_results': {k: v for k, v in missing_result.items() if k not in ['baseline', 'summary']}
        }
    
    @staticmethod
    async def evaluate_agreement(
        N: float,
        P: float,
        K: float,
        temperature: float,
        humidity: float,
        rainfall: float,
        ph: float = 6.5
    ) -> Dict:
        """
        Evaluate agreement across multiple models.
        
        Args:
            Input features
            
        Returns:
            Dictionary with model agreement results
        """
        logger.info("Running model agreement evaluation...")
        
        # Call ML evaluation module
        agreement_result = ModelComparison.compute_agreement(
            N=N, P=P, K=K,
            temperature=temperature,
            humidity=humidity,
            ph=ph,
            rainfall=rainfall
        )
        
        logger.info(f"Model agreement evaluation complete: agreement={agreement_result['agreement_ratio']:.4f}")
        
        return {
            'predicted_crop': agreement_result['most_common_crop'],
            'total_models': agreement_result['total_models'],
            'agreement_ratio': agreement_result['agreement_ratio'],
            'all_agree': agreement_result['all_agree'],
            'predictions': agreement_result['predictions'],
            'prediction_distribution': agreement_result['prediction_distribution']
        }
    
    @staticmethod
    async def evaluate_full(
        N: float,
        P: float,
        K: float,
        temperature: float,
        humidity: float,
        rainfall: float,
        ph: float = 6.5,
        rss_runs: int = 30,
        noise_level: float = 0.2
    ) -> Dict:
        """
        Run full evaluation pipeline with all metrics.
        
        Args:
            Input features and evaluation parameters
            
        Returns:
            Dictionary with comprehensive evaluation results
        """
        logger.info("Running full evaluation pipeline...")
        
        base_input = {
            'N': N, 'P': P, 'K': K,
            'temperature': temperature,
            'humidity': humidity,
            'ph': ph,
            'rainfall': rainfall
        }
        
        # Call ML evaluation module
        confidence_result = ConfidenceEstimator.compute_confidence(
            base_input,
            include_rss=True,
            include_agreement=True,
            rss_runs=rss_runs,
            noise_level=noise_level
        )
        
        # Get detailed results for each test
        rss_result = RSSCalculator.compute_rss(base_input, noise_level, rss_runs)
        missing_result = MissingDataSimulator.evaluate_missing_features(base_input)
        agreement_result = ModelComparison.compute_agreement(**base_input)
        
        logger.info(f"Full evaluation complete: confidence={confidence_result['confidence']:.4f}")
        
        return {
            'predicted_crop': confidence_result['crop'],
            'confidence': confidence_result['confidence'],
            'confidence_level': ConfidenceEstimator.get_confidence_level(confidence_result['confidence']),
            
            # Confidence components
            'probability': confidence_result['components']['probability'],
            'stability': confidence_result['components']['stability'],
            'agreement': confidence_result['components']['agreement'],
            
            # Robustness metrics
            'rss_score': rss_result['rss'],
            'missing_feature_stability': missing_result['summary']['stability_score'],
            'model_agreement_ratio': agreement_result['agreement_ratio'],
            
            # Detailed results
            'noise_test': rss_result,
            'missing_feature_test': missing_result,
            'model_agreement_test': agreement_result
        }
    
    @staticmethod
    def create_evaluation_history_entry(
        user_id: str,
        evaluation_type: str,
        input_data: Dict,
        result_data: Dict
    ) -> Dict:
        """
        Create evaluation history entry for Firestore.
        
        Args:
            user_id: User document ID
            evaluation_type: Type of evaluation (noise, missing, agreement, full)
            input_data: Input parameters
            result_data: Evaluation results
            
        Returns:
            Dictionary for Firestore document
        """
        return {
            'user_id': user_id,
            'evaluation_type': evaluation_type,
            'input_payload': input_data,
            'result_payload': result_data,
            'timestamp': datetime.utcnow()
        }
