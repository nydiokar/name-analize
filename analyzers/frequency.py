from collections import Counter
import numpy as np
from rich.table import Table

def analyze_frequency(name):
    """Calculate frequency patterns in a name using numpy."""
    # Remove spaces and convert to lowercase
    name = name.lower().replace(" ", "")
    
    if not name:
        return {
            "average_frequency": 0,
            "character_distribution": {},
            "statistics": {},
            "visualization": None
        }
    
    # Count character frequencies using numpy
    unique_chars = np.array(list(set(name)))
    counts = np.array([name.count(char) for char in unique_chars])
    total_chars = len(name)
    
    # Calculate frequency distribution
    frequencies = counts / total_chars
    
    # Calculate statistics using numpy
    ascii_values = np.array([ord(char) for char in name])
    stats = {
        "mean": np.mean(ascii_values),
        "median": np.median(ascii_values),
        "std": np.std(ascii_values),
        "entropy": -np.sum(frequencies * np.log2(frequencies))
    }
    
    # Create frequency visualization
    distribution = dict(zip(unique_chars, frequencies))
    
    # Create visualization string
    viz_lines = []
    max_bar_length = 20
    
    for char, freq in sorted(distribution.items(), key=lambda x: x[1], reverse=True):
        bar_length = int(freq * max_bar_length)
        bar = "█" * bar_length
        viz_lines.append(f"{char}: {freq:.3f} {bar}")
    
    # Convert numpy types to Python native types for JSON serialization
    return {
        "average_frequency": float(np.mean(frequencies)),
        "character_distribution": {k: float(v) for k, v in distribution.items()},
        "statistics": {k: float(v) for k, v in stats.items()},
        "visualization": "\n".join(viz_lines)
    }
