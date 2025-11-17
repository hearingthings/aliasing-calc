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


def calculate_consonant_score(result: "AliasingResult") -> float:
    """
    Score based on how well aliased partials form musical intervals.

    Rewards decimation rates where partials form consonant intervals like
    octaves (2:1), fifths (3:2), fourths (4:3), major thirds (5:4), etc.

    Lower score is better.
    """
    aliased_freqs = result.get_aliased_frequencies()

    # Musical interval ratios (sorted by consonance)
    target_ratios = [
        (2.0, "octave", 1.0),      # Perfect consonance
        (1.5, "fifth", 0.8),       # Strong consonance
        (4/3, "fourth", 0.7),      # Strong consonance
        (5/4, "maj3rd", 0.6),      # Medium consonance
        (6/5, "min3rd", 0.5),      # Medium consonance
        (3.0, "octave+5th", 0.4),  # Compound interval
        (8/5, "min6th", 0.3),      # Weak consonance
        (5/3, "maj6th", 0.3),      # Weak consonance
    ]

    sorted_freqs = np.sort([f for f in aliased_freqs if f > 10])  # Ignore very low freqs

    if len(sorted_freqs) < 2:
        return float('inf')

    consonance_score = 0.0
    num_pairs = 0

    # Check all pairs of partials
    for i in range(len(sorted_freqs)):
        for j in range(i + 1, len(sorted_freqs)):
            ratio = sorted_freqs[j] / sorted_freqs[i]

            # Find closest target ratio
            best_match_error = float('inf')
            best_weight = 0.0

            for target_ratio, name, weight in target_ratios:
                error = abs(ratio - target_ratio) / target_ratio
                if error < best_match_error:
                    best_match_error = error
                    best_weight = weight

            # Weight by consonance strength
            consonance_score += best_match_error / (best_weight + 0.1)
            num_pairs += 1

    return consonance_score / max(num_pairs, 1)


def calculate_subharmonic_score(result: "AliasingResult") -> float:
    """
    Score based on how much the fundamental is lowered (subharmonic content).

    Rewards decimation rates where the aliased fundamental is significantly
    below the original pitch.

    Lower score is better.
    """
    fundamental_partial = result.partials[0]
    original_freq = fundamental_partial.original_freq
    aliased_freq = fundamental_partial.aliased_freq

    # We want aliased to be lower than original
    if aliased_freq >= original_freq * 0.95:
        # Not significantly lowered
        return float('inf')

    # Score = ratio (higher ratio = more lowering = better, so negate)
    # We want maximum lowering
    ratio = aliased_freq / original_freq

    # Return inverted ratio so lower is better (smaller aliased freq = better score)
    return ratio


def calculate_metallic_score(result: "AliasingResult") -> float:
    """
    Score based on inharmonic ratios similar to metallic percussion.

    Rewards non-integer frequency ratios that create bell-like timbres.
    Looks for ratios around 2.0, 3.0, 4.4, 5.4 (bell-like partials).

    Lower score is better.
    """
    aliased_freqs = result.get_aliased_frequencies()
    sorted_freqs = np.sort([f for f in aliased_freqs if f > 10])

    if len(sorted_freqs) < 3:
        return float('inf')

    # Target ratios for bell-like sounds (inharmonic)
    # Based on actual bell partials
    target_ratios = [2.0, 3.0, 4.4, 5.4, 6.8, 8.2]

    fundamental = sorted_freqs[0]
    metallic_score = 0.0

    for i, freq in enumerate(sorted_freqs[1:], 1):
        ratio = freq / fundamental

        # Check if ratio is close to any target
        min_error = float('inf')
        for target in target_ratios:
            # Look for close matches but NOT exact harmonic matches
            error = abs(ratio - target)
            if error < min_error:
                min_error = error

        # Penalize if too close to integer (harmonic)
        if abs(ratio - round(ratio)) < 0.1:
            metallic_score += 10.0  # Big penalty for harmonic
        else:
            metallic_score += min_error

    # Also reward having several partials
    metallic_score /= len(sorted_freqs)

    return metallic_score


def calculate_sparse_score(result: "AliasingResult") -> float:
    """
    Score based on maximizing gaps between aliased partials.

    Rewards decimation rates with large frequency gaps between partials,
    creating a sparse, open spectrum.

    Lower score is better (we negate the gaps).
    """
    aliased_freqs = result.get_aliased_frequencies()
    sorted_freqs = np.sort(aliased_freqs)

    if len(sorted_freqs) < 2:
        return 0.0

    # Calculate average gap between consecutive partials
    gaps = []
    for i in range(len(sorted_freqs) - 1):
        gap = sorted_freqs[i + 1] - sorted_freqs[i]
        gaps.append(gap)

    avg_gap = np.mean(gaps)
    min_gap = np.min(gaps)

    # We want large gaps, so negate (larger gaps = better = lower score)
    # Also reward consistency (penalize if min_gap is too small)
    sparseness = avg_gap + (min_gap / 2.0)

    return -sparseness


def calculate_freeze_score(result: "AliasingResult") -> float:
    """
    Score based on how many partials alias near DC (near-zero frequency).

    Rewards decimation rates where partials alias to very low frequencies
    (< 50 Hz), creating a "frozen" spectrum effect.

    Lower score is better.
    """
    aliased_freqs = result.get_aliased_frequencies()

    freeze_threshold = 50.0  # Hz

    # Count partials near DC
    frozen_partials = sum(1 for f in aliased_freqs if f < freeze_threshold)

    if frozen_partials == 0:
        return float('inf')

    # Also calculate average distance from DC for frozen partials
    frozen_freqs = [f for f in aliased_freqs if f < freeze_threshold]
    avg_frozen_dist = np.mean(frozen_freqs) if frozen_freqs else freeze_threshold

    # Lower score = more frozen partials closer to DC
    score = avg_frozen_dist / (frozen_partials ** 2)

    return score


def calculate_mirror_score(result: "AliasingResult") -> float:
    """
    Score based on symmetric aliasing pattern around a center frequency.

    Rewards decimation rates where partials are symmetrically distributed
    around the Nyquist frequency or center of the spectrum.

    Lower score is better.
    """
    aliased_freqs = result.get_aliased_frequencies()
    nyquist = result.nyquist_freq

    if len(aliased_freqs) < 3:
        return float('inf')

    # Check symmetry around Nyquist/2
    center = nyquist / 2.0

    # Calculate distances from center
    distances = [abs(f - center) for f in aliased_freqs]

    # For perfect mirror symmetry, we'd have pairs at equal distances
    # Sort distances and check if they come in pairs
    sorted_dists = sorted(distances)

    symmetry_error = 0.0
    for i in range(0, len(sorted_dists) - 1, 2):
        # Check if consecutive pairs are similar
        pair_diff = abs(sorted_dists[i] - sorted_dists[i + 1])
        symmetry_error += pair_diff

    # Normalize by number of partials
    return symmetry_error / len(aliased_freqs)


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
        method: Search method name. Available methods:
            - "nearest": Keep fundamental close to original pitch
            - "purest": Minimize beating, maximize harmonicity
            - "richest": Maximize spectral complexity
            - "consonant": Form musical intervals between partials
            - "subharmonic": Lower the fundamental pitch
            - "metallic": Create bell-like inharmonic ratios
            - "sparse": Maximize gaps between partials
            - "freeze": Alias partials near DC (low frequencies)
            - "mirror": Create symmetric spectrum patterns
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
        "consonant": calculate_consonant_score,
        "subharmonic": calculate_subharmonic_score,
        "metallic": calculate_metallic_score,
        "sparse": calculate_sparse_score,
        "freeze": calculate_freeze_score,
        "mirror": calculate_mirror_score,
    }

    if method not in score_functions:
        raise ValueError(
            f"Unknown search method: {method}. "
            f"Available: {', '.join(sorted(score_functions.keys()))}"
        )

    score_func = score_functions[method]

    best_result = None
    best_score = float('inf')
    fallback_result = None

    for decimation in range(min_decimation, max_decimation + 1):
        result = calculator.calculate(decimation)
        score = score_func(result)

        # Keep first result as fallback
        if fallback_result is None:
            fallback_result = result

        if score < best_score:
            best_score = score
            best_result = result

    # If no valid result found (all scores were inf), return fallback
    return best_result if best_result is not None else fallback_result
