import numpy as np
from collections import defaultdict

class VibrationAnalyzer:
    # Base frequencies (Hz) for cultural tuning
    BASE_FREQUENCIES = {
        'western': 440.0,  # Standard concert pitch
        'slavic': 432.0,   # Ancient Slavic tuning
        'vedic': 432.0,    # Ancient Indian tuning
        'egyptian': 432.0, # Ancient Egyptian tuning
        'default': 432.0   # Natural resonance
    }
    
    # Harmonic ratios from sacred geometry
    HARMONIC_RATIOS = [1.0, 1.618034, 2.0, 2.236068, 3.0, 4.0]  # Including golden ratio
    
    # Letter resonance patterns based on sound formation
    LETTER_QUALITIES = {
        'a': {'openness': 0.9, 'power': 0.7, 'frequency_mod': 1.0},
        'e': {'openness': 0.8, 'power': 0.5, 'frequency_mod': 1.2},
        'i': {'openness': 0.6, 'power': 0.3, 'frequency_mod': 1.4},
        'o': {'openness': 0.7, 'power': 0.8, 'frequency_mod': 0.9},
        'u': {'openness': 0.5, 'power': 0.6, 'frequency_mod': 1.1},
        'y': {'openness': 0.4, 'power': 0.4, 'frequency_mod': 1.3}
    }
    
    @staticmethod
    def calculate_letter_frequency(letter, base_frequency):
        """Calculate vibrational frequency for a letter with cultural consideration."""
        # Basic frequency calculation
        basic_freq = ord(letter.lower()) - 96
        if basic_freq < 1 or basic_freq > 26:
            return 0
            
        # Apply letter qualities if available
        qualities = VibrationAnalyzer.LETTER_QUALITIES.get(letter.lower(), 
                                                         {'frequency_mod': 1.0})
        
        # Calculate modified frequency
        freq = base_frequency * (basic_freq / 13) * qualities['frequency_mod']
        return freq
    
    @staticmethod
    def calculate_resonance(frequencies, cultural_weight=1.0):
        """Calculate resonance pattern using harmonic series."""
        if not frequencies:
            return 0
        
        # Calculate fundamental frequency
        fundamental = np.mean(frequencies)
        
        # Generate harmonics with cultural weighting
        harmonics = [fundamental * ratio * cultural_weight 
                    for ratio in VibrationAnalyzer.HARMONIC_RATIOS]
        
        # Calculate resonance strength
        resonance = sum(1 / (1 + min(abs(f - h) for h in harmonics)) 
                       for f in frequencies)
        
        return resonance / len(frequencies)
    
    @staticmethod
    def get_frequency_meaning(freq):
        """Interpret the meaning of a frequency range."""
        if freq > 800:
            return "spiritual/transcendent"
        elif freq > 600:
            return "intuitive/insightful"
        elif freq > 400:
            return "balanced/harmonious"
        else:
            return "grounding/practical"
    
    @staticmethod
    def analyze_name_vibration(name, base_frequency=432, cultural_weight=1.0):
        """Perform comprehensive vibrational analysis of a name."""
        name = name.lower()
        
        # Calculate letter frequencies
        frequencies = []
        letter_resonances = {}
        
        for char in name:
            if char.isalpha():
                freq = VibrationAnalyzer.calculate_letter_frequency(char, base_frequency)
                frequencies.append(freq)
                letter_resonances[char] = freq
        
        if not frequencies:
            return None
            
        # Calculate resonance with cultural weighting
        resonance = VibrationAnalyzer.calculate_resonance(frequencies, cultural_weight)
        
        # Analyze harmonic patterns
        harmonic_groups = defaultdict(list)
        for i, freq in enumerate(frequencies):
            for ratio in VibrationAnalyzer.HARMONIC_RATIOS:
                if any(abs(freq/other - ratio) < 0.01 for other in frequencies[i+1:]):
                    harmonic_groups[ratio].append(freq)
        
        # Calculate coherence
        frequency_ratios = [f2/f1 for i, f1 in enumerate(frequencies) 
                          for f2 in frequencies[i+1:]]
        coherence = np.mean([min(abs(ratio - h) for h in VibrationAnalyzer.HARMONIC_RATIOS)
                           for ratio in frequency_ratios]) if frequency_ratios else 1
        
        # Analyze overall frequency character
        avg_freq = np.mean(frequencies)
        frequency_character = VibrationAnalyzer.get_frequency_meaning(avg_freq)
        
        return {
            "base_frequency": round(avg_freq, 2),
            "resonance_strength": round(resonance, 3),
            "coherence": round(1 - coherence, 3),
            "harmonic_count": len([g for g in harmonic_groups.values() if len(g) > 1]),
            "frequency_range": round(max(frequencies) - min(frequencies), 2),
            "strongest_harmonic": max(harmonic_groups.items(), 
                                   key=lambda x: len(x[1]))[0] if harmonic_groups else None,
            "frequency_character": frequency_character,
            "cultural_influence": cultural_weight
        }
