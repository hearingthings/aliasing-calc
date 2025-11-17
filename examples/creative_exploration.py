#!/usr/bin/env python3
"""Creative exploration examples - using aliasing for sound design."""

from aliasing_calc import AliasingCalculator
import numpy as np


def explore_frequency(freq, name):
    """Explore aliasing patterns for a given frequency."""
    print(f"\n{'=' * 60}")
    print(f"Exploring: {name} ({freq:.2f} Hz)")
    print('=' * 60)

    calc = AliasingCalculator(
        fundamental_freq=freq,
        sample_rate=48000,
        num_partials=10
    )

    # Test several decimation rates
    interesting_rates = [3, 5, 7, 11, 13, 16, 24, 32]

    for rate in interesting_rates:
        result = calc.calculate(rate)

        # Calculate some interesting metrics
        aliased_freqs = result.get_aliased_frequencies()
        fundamental_shift = result.partials[0].aliased_freq - freq
        num_folded = sum(1 for p in result.partials if p.folded)

        # Find beat frequencies (close partials)
        sorted_freqs = np.sort(aliased_freqs)
        min_distance = min(sorted_freqs[i+1] - sorted_freqs[i]
                          for i in range(len(sorted_freqs) - 1))

        print(f"\nDecimation {rate}x:")
        print(f"  Fundamental: {freq:.1f} → {result.partials[0].aliased_freq:.1f} Hz "
              f"({fundamental_shift:+.1f} Hz)")
        print(f"  Folded: {num_folded}/{len(result.partials)} partials")
        print(f"  Closest partials: {min_distance:.2f} Hz apart")

        # Show interesting patterns
        if abs(fundamental_shift) < 5:
            print("  → Near-original pitch!")
        if min_distance < 5:
            print(f"  → Beating at ~{min_distance:.1f} Hz!")
        if num_folded == len(result.partials):
            print("  → All partials aliased!")


def find_subharmonic_decimation():
    """Find decimation rates that create subharmonic content."""
    print(f"\n{'=' * 60}")
    print("Finding Subharmonic Decimation Rates")
    print('=' * 60)

    freq = 440.0
    calc = AliasingCalculator(
        fundamental_freq=freq,
        sample_rate=48000,
        num_partials=8
    )

    print(f"\nLooking for decimation rates where fundamental aliases below {freq} Hz:\n")

    for rate in range(2, 65):
        result = calc.calculate(rate)
        aliased_fundamental = result.partials[0].aliased_freq

        # Check if aliased fundamental is significantly lower
        if aliased_fundamental < freq * 0.8:  # At least 20% lower
            ratio = freq / aliased_fundamental
            print(f"  {rate}x: {freq:.1f} → {aliased_fundamental:.1f} Hz "
                  f"(~{ratio:.2f}x lower)")


def find_consonant_intervals():
    """Find decimation rates that create consonant intervals between partials."""
    print(f"\n{'=' * 60}")
    print("Finding Consonant Interval Patterns")
    print('=' * 60)

    freq = 440.0
    calc = AliasingCalculator(
        fundamental_freq=freq,
        sample_rate=48000,
        num_partials=4
    )

    # Musical intervals (ratios)
    intervals = {
        "Octave": 2.0,
        "Fifth": 1.5,
        "Fourth": 4/3,
        "Major Third": 5/4,
    }

    print(f"\nLooking for decimation rates creating musical intervals:\n")

    for rate in range(2, 33):
        result = calc.calculate(rate)
        aliased_freqs = sorted(result.get_aliased_frequencies())

        # Check ratios between consecutive partials
        for i in range(len(aliased_freqs) - 1):
            if aliased_freqs[i] > 0:  # Avoid division by zero
                ratio = aliased_freqs[i + 1] / aliased_freqs[i]

                # Check if close to any musical interval
                for interval_name, interval_ratio in intervals.items():
                    if abs(ratio - interval_ratio) < 0.02:  # Within 2% tolerance
                        print(f"  {rate}x: Partials {i+1}-{i+2} form ~{interval_name} "
                              f"({aliased_freqs[i]:.1f} : {aliased_freqs[i+1]:.1f} Hz)")


def explore_beating_patterns():
    """Find decimation rates that create interesting beat patterns."""
    print(f"\n{'=' * 60}")
    print("Exploring Beat Frequency Patterns")
    print('=' * 60)

    freq = 440.0
    calc = AliasingCalculator(
        fundamental_freq=freq,
        sample_rate=48000,
        num_partials=8
    )

    target_beats = [1, 2, 3, 5, 7, 10]  # Target beat frequencies in Hz

    print(f"\nFinding decimation rates with specific beat frequencies:\n")

    for rate in range(2, 65):
        result = calc.calculate(rate)
        aliased_freqs = sorted(result.get_aliased_frequencies())

        # Find minimum distance between partials
        min_dist = float('inf')
        closest_pair = None

        for i in range(len(aliased_freqs) - 1):
            dist = aliased_freqs[i + 1] - aliased_freqs[i]
            if dist < min_dist:
                min_dist = dist
                closest_pair = (i + 1, i + 2)

        # Check if close to any target beat frequency
        for target in target_beats:
            if abs(min_dist - target) < 0.5:
                print(f"  {rate}x: ~{target} Hz beating between partials "
                      f"{closest_pair[0]}-{closest_pair[1]} "
                      f"({min_dist:.2f} Hz)")
                break


if __name__ == "__main__":
    # Explore different musical pitches
    explore_frequency(440.0, "A4")
    explore_frequency(220.0, "A3")
    explore_frequency(880.0, "A5")

    # Creative explorations
    find_subharmonic_decimation()
    find_consonant_intervals()
    explore_beating_patterns()
