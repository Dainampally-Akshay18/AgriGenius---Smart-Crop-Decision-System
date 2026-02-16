"""
Noise injection engine for robustness testing.
"""
import numpy as np
from typing import Dict, List


class NoiseInjector:
    """Inject noise into input features for robustness testing."""
    
    @staticmethod
    def add_noise(value: float, noise_percentage: float) -> float:
        """
        Add random noise to a value.
        
        Args:
            value: Original value
            noise_percentage: Noise percentage (e.g., 0.2 for ±20%)
            
        Returns:
            Noisy value
        """
        noise_range = value * noise_percentage
        noise = np.random.uniform(-noise_range, noise_range)
        return value + noise
    
    @staticmethod
    def generate_noisy_inputs(
        base_input: Dict,
        noise_percentage: float,
        num_samples: int,
        features_to_perturb: List[str] = None
    ) -> List[Dict]:
        """
        Generate multiple noisy versions of input.
        
        Args:
            base_input: Original input dictionary
            noise_percentage: Noise percentage (0.1 to 0.4 for 10-40%)
            num_samples: Number of noisy samples to generate
            features_to_perturb: List of features to add noise to (default: N, P, K)
            
        Returns:
            List of noisy input dictionaries
        """
        if features_to_perturb is None:
            features_to_perturb = ['N', 'P', 'K']
        
        noisy_inputs = []
        
        for _ in range(num_samples):
            noisy_input = base_input.copy()
            
            for feature in features_to_perturb:
                if feature in noisy_input:
                    noisy_input[feature] = NoiseInjector.add_noise(
                        noisy_input[feature],
                        noise_percentage
                    )
                    # Ensure values stay within valid ranges
                    if feature in ['N', 'P', 'K']:
                        noisy_input[feature] = np.clip(noisy_input[feature], 0, 140)
                    elif feature == 'ph':
                        noisy_input[feature] = np.clip(noisy_input[feature], 0, 14)
                    elif feature == 'temperature':
                        noisy_input[feature] = np.clip(noisy_input[feature], 0, 60)
                    elif feature == 'humidity':
                        noisy_input[feature] = np.clip(noisy_input[feature], 0, 100)
                    elif feature == 'rainfall':
                        noisy_input[feature] = max(0, noisy_input[feature])
            
            noisy_inputs.append(noisy_input)
        
        return noisy_inputs
    
    @staticmethod
    def generate_noise_levels(
        base_input: Dict,
        noise_levels: List[float] = None,
        samples_per_level: int = 10
    ) -> Dict[float, List[Dict]]:
        """
        Generate noisy inputs at multiple noise levels.
        
        Args:
            base_input: Original input dictionary
            noise_levels: List of noise percentages (default: [0.1, 0.2, 0.3, 0.4])
            samples_per_level: Number of samples per noise level
            
        Returns:
            Dictionary mapping noise level to list of noisy inputs
        """
        if noise_levels is None:
            noise_levels = [0.1, 0.2, 0.3, 0.4]  # 10%, 20%, 30%, 40%
        
        noise_samples = {}
        
        for noise_level in noise_levels:
            noise_samples[noise_level] = NoiseInjector.generate_noisy_inputs(
                base_input,
                noise_level,
                samples_per_level
            )
        
        return noise_samples


if __name__ == "__main__":
    # Test noise injection
    print("\n" + "=" * 60)
    print("TESTING NOISE INJECTION")
    print("=" * 60 + "\n")
    
    base_input = {
        'N': 90,
        'P': 42,
        'K': 43,
        'temperature': 20.87,
        'humidity': 82.00,
        'ph': 6.50,
        'rainfall': 202.93
    }
    
    print("Base Input:")
    for key, value in base_input.items():
        print(f"  {key}: {value}")
    print()
    
    # Generate noisy samples at 20% noise
    noisy_samples = NoiseInjector.generate_noisy_inputs(base_input, 0.2, 5)
    
    print("Noisy Samples (20% noise):")
    for i, sample in enumerate(noisy_samples, 1):
        print(f"\nSample {i}:")
        for key in ['N', 'P', 'K']:
            original = base_input[key]
            noisy = sample[key]
            diff = ((noisy - original) / original) * 100
            print(f"  {key}: {noisy:.2f} (original: {original}, diff: {diff:+.1f}%)")
    print()
