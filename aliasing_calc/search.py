"""Search algorithms for finding optimal decimation rates."""

import numpy as np
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .core import AliasingCalculator, AliasingResult


def calculate_nearest_score(result: "AliasingResult") -> float:
    """
    Score based on how close the aliased fundamental is to the original.

    Lower score is better.
    """
    fundamental_partial = result.partials[0]
    distance = abs(fundamental_partial.aliased_freq - fundamental_partial.original_freq)
    return distance


def calculate_purest_score(result: "AliasingResult") -> float:
    """
    Score based on harmonicity - how close aliased partials are to harmonic series.

    The "purest" result has minimal beating between partials, meaning the aliased
    frequencies form a harmonic or near-harmonic series.

    Lower score is better.
    """
    aliased_freqs = result.get_aliased_frequencies()

    # Sort frequencies
    sorted_freqs = np.sort(aliased_freqs)

    # Calculate the implied fundamental from all pairs of partials
    # For a harmonic series, f_n = n * f0, so f0 = f_n / n
    # We use the GCD (greatest common divisor) approach in frequency space

    if len(sorted_freqs) < 2:
        return 0.0

    # Calculate all frequency differences
    diffs = []
    for i in range(len(sorted_freqs)):
        for j in range(i + 1, len(sorted_freqs)):
            diffs.append(sorted_freqs[j] - sorted_freqs[i])

    if not diffs:
        return 0.0

    # The "fundamental" should divide evenly into all frequencies
    # We'll estimate it as the GCD of all frequencies
    # For floating point, we use the smallest difference as an estimate
    min_diff = min(diffs)

    # Calculate how well each frequency fits into a harmonic series based on min_diff
    harmonicity_error = 0.0
    for freq in sorted_freqs:
        # Find closest multiple of min_diff
        ratio = freq / min_diff
        closest_int = round(ratio)
        error = abs(ratio - closest_int)
        harmonicity_error += error

    # Also penalize if frequencies are too close together (beating)
    beating_penalty = 0.0
    for i in range(len(sorted_freqs) - 1):
        diff = sorted_freqs[i + 1] - sorted_freqs[i]
        # Penalize very small differences (< 5 Hz creates noticeable beating)
        if diff < 5.0:
            beating_penalty += (5.0 - diff) * 10.0

    return harmonicity_error + beating_penalty


def calculate_richest_score(result: "AliasingResult") -> float:
    """
    Score based on spectral complexity/inharmonicity.

    Higher inharmonicity = richer, more complex spectrum.
    We negate the score so lower is still better for consistency.
    """
    aliased_freqs = result.get_aliased_frequencies()

    if len(aliased_freqs) < 2:
        return 0.0

    # Calculate spectral spread
    spread = np.std(aliased_freqs)

    # Calculate inharmonicity - deviation from harmonic ratios
    sorted_freqs = np.sort(aliased_freqs)
    fundamental_est = sorted_freqs[0]

    inharmonicity = 0.0
    for i, freq in enumerate(sorted_freqs):
        expected_harmonic = fundamental_est * (i + 1)
        deviation = abs(freq - expected_harmonic) / fundamental_est
        inharmonicity += deviation

    # Count unique frequency bins (avoid duplicates/unisons)
    unique_freqs = len(set(np.round(aliased_freqs, 1)))

    # Higher is better, so negate
    richness = spread * inharmonicity * unique_freqs
    return -richness  # Negate so lower is better


def search_decimation_rate(
    calculator: "AliasingCalculator",
    method: str = "nearest",
    min_decimation: int = 2,
    max_decimation: int = 64
) -> "AliasingResult":
    """
    Search for optimal decimation rate using specified method.

    Args:
        calculator: AliasingCalculator instance
        method: Search method - "nearest", "purest", or "richest"
        min_decimation: Minimum decimation rate to consider
        max_decimation: Maximum decimation rate to consider

    Returns:
        AliasingResult for the best decimation rate found

    Raises:
        ValueError: If method is not recognized
    """
    score_functions = {
        "nearest": calculate_nearest_score,
        "purest": calculate_purest_score,
        "richest": calculate_richest_score,
    }

    if method not in score_functions:
        raise ValueError(
            f"Unknown search method: {method}. "
            f"Available: {', '.join(score_functions.keys())}"
        )

    score_func = score_functions[method]

    best_result = None
    best_score = float('inf')

    for decimation in range(min_decimation, max_decimation + 1):
        result = calculator.calculate(decimation)
        score = score_func(result)

        if score < best_score:
            best_score = score
            best_result = result

    return best_result
