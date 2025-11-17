#!/usr/bin/env python3
"""
20 Comprehensive Examples of Aliasing Calculator Usage

This script demonstrates various use cases, from basic calculations to
advanced creative sound design applications.
"""

from aliasing_calc import AliasingCalculator
import sys


def example_01_basic_calculation():
    """Example 1: Basic aliasing calculation at a specific decimation rate."""
    print("\n" + "=" * 80)
    print("Example 1: Basic Aliasing Calculation")
    print("=" * 80)
    print("Calculate aliasing for A4 (440 Hz) at 16x decimation")

    calc = AliasingCalculator(fundamental_freq=440.0, sample_rate=48000, num_partials=8)
    result = calc.calculate(16)

    print(f"\nResult: {result.decimation_rate}x decimation")
    print(f"Decimated SR: {result.decimated_sample_rate} Hz")
    print(f"Fundamental: {result.partials[0].original_freq} → {result.partials[0].aliased_freq:.2f} Hz")
    print(f"Folded partials: {sum(1 for p in result.partials if p.folded)}/{len(result.partials)}")


def example_02_search_nearest():
    """Example 2: Find decimation rate that keeps fundamental closest to original."""
    print("\n" + "=" * 80)
    print("Example 2: Search for Nearest Pitch")
    print("=" * 80)
    print("Find decimation where 440 Hz stays closest to 440 Hz")

    calc = AliasingCalculator(fundamental_freq=440.0, sample_rate=48000, num_partials=6)
    result = calc.search(method='nearest', max_decimation=32)

    print(f"\nBest decimation: {result.decimation_rate}x")
    print(f"Fundamental shift: {result.partials[0].aliased_freq - 440:.2f} Hz")


def example_03_subharmonic_bass():
    """Example 3: Generate deep bass by lowering the pitch."""
    print("\n" + "=" * 80)
    print("Example 3: Subharmonic Bass Generator")
    print("=" * 80)
    print("Turn 110 Hz (A2) into sub-bass frequencies")

    calc = AliasingCalculator(fundamental_freq=110.0, sample_rate=48000, num_partials=8)
    result = calc.search(method='subharmonic', max_decimation=64)

    original = result.partials[0].original_freq
    aliased = result.partials[0].aliased_freq

    print(f"\nBest decimation: {result.decimation_rate}x")
    print(f"Pitch drop: {original:.2f} Hz → {aliased:.2f} Hz ({original - aliased:.2f} Hz lower)")
    print(f"Ratio: {aliased/original:.3f}x")


def example_04_metallic_percussion():
    """Example 4: Create bell-like metallic timbres."""
    print("\n" + "=" * 80)
    print("Example 4: Metallic Percussion Designer")
    print("=" * 80)
    print("Design inharmonic ratios for bell/gong sounds")

    calc = AliasingCalculator(fundamental_freq=880.0, sample_rate=48000, num_partials=10)
    result = calc.search(method='metallic', max_decimation=32)

    print(f"\nBest decimation: {result.decimation_rate}x")
    print("\nPartial ratios (relative to fundamental):")
    fund = result.partials[0].aliased_freq
    for i, p in enumerate(result.partials[:6]):
        ratio = p.aliased_freq / fund
        print(f"  Partial {i+1}: {ratio:.2f}x")


def example_05_frozen_spectrum():
    """Example 5: Create frozen, subsonic spectrum."""
    print("\n" + "=" * 80)
    print("Example 5: Frozen Spectrum Effect")
    print("=" * 80)
    print("Alias partials to very low frequencies (< 50 Hz)")

    calc = AliasingCalculator(fundamental_freq=440.0, sample_rate=48000, num_partials=10)
    result = calc.search(method='freeze', max_decimation=64)

    frozen = [p.aliased_freq for p in result.partials if p.aliased_freq < 50]

    print(f"\nBest decimation: {result.decimation_rate}x")
    print(f"Frozen partials: {len(frozen)}/{len(result.partials)}")
    print(f"Frozen frequencies: {', '.join(f'{f:.1f}' for f in frozen[:8])} Hz")


def example_06_consonant_harmonies():
    """Example 6: Find musical interval relationships."""
    print("\n" + "=" * 80)
    print("Example 6: Consonant Harmony Finder")
    print("=" * 80)
    print("Find decimation creating musical intervals")

    calc = AliasingCalculator(fundamental_freq=220.0, sample_rate=48000, num_partials=8)
    result = calc.search(method='consonant', max_decimation=64)

    print(f"\nBest decimation: {result.decimation_rate}x")
    print("\nPartial ratios (checking for octaves, fifths, etc.):")

    freqs = sorted(result.get_aliased_frequencies())
    for i in range(len(freqs) - 1):
        for j in range(i + 1, min(i + 3, len(freqs))):
            ratio = freqs[j] / freqs[i]
            if abs(ratio - 2.0) < 0.05:
                print(f"  Octave: {freqs[i]:.1f} : {freqs[j]:.1f} Hz")
            elif abs(ratio - 1.5) < 0.05:
                print(f"  Fifth: {freqs[i]:.1f} : {freqs[j]:.1f} Hz")


def example_07_sparse_spectrum():
    """Example 7: Create open, spacious spectrum."""
    print("\n" + "=" * 80)
    print("Example 7: Sparse Spectrum Designer")
    print("=" * 80)
    print("Maximize gaps between partials for open sound")

    calc = AliasingCalculator(fundamental_freq=440.0, sample_rate=48000, num_partials=6)
    result = calc.search(method='sparse', max_decimation=48)

    sorted_freqs = sorted(result.get_aliased_frequencies())
    gaps = [sorted_freqs[i+1] - sorted_freqs[i] for i in range(len(sorted_freqs) - 1)]

    print(f"\nBest decimation: {result.decimation_rate}x")
    print(f"Average gap: {sum(gaps)/len(gaps):.2f} Hz")
    print(f"Gaps: {', '.join(f'{g:.1f}' for g in gaps)} Hz")


def example_08_high_sample_rate():
    """Example 8: Working with higher sample rates (96kHz)."""
    print("\n" + "=" * 80)
    print("Example 8: High Sample Rate Exploration (96kHz)")
    print("=" * 80)

    calc = AliasingCalculator(fundamental_freq=440.0, sample_rate=96000, num_partials=12)
    result = calc.search(method='richest', max_decimation=64)

    print(f"\nBest decimation: {result.decimation_rate}x")
    print(f"Original SR: {result.original_sample_rate} Hz")
    print(f"Decimated SR: {result.decimated_sample_rate} Hz")
    print(f"Nyquist: {result.nyquist_freq:.2f} Hz")


def example_09_low_frequency():
    """Example 9: Aliasing effects on low frequencies."""
    print("\n" + "=" * 80)
    print("Example 9: Low Frequency Aliasing (55 Hz - A1)")
    print("=" * 80)

    calc = AliasingCalculator(fundamental_freq=55.0, sample_rate=48000, num_partials=20)
    result = calc.calculate(32)

    print(f"\nDecimation: {result.decimation_rate}x")
    print(f"Decimated SR: {result.decimated_sample_rate} Hz")
    print(f"\nFirst 8 partials:")
    for p in result.partials[:8]:
        marker = "[FOLDED]" if p.folded else ""
        print(f"  {p.partial_number}. {p.original_freq:.1f} → {p.aliased_freq:.1f} Hz {marker}")


def example_10_many_partials():
    """Example 10: Analyzing signals with many partials."""
    print("\n" + "=" * 80)
    print("Example 10: Many Partials (Complex Waveform)")
    print("=" * 80)
    print("Analyze 20 partials to see complex aliasing patterns")

    calc = AliasingCalculator(fundamental_freq=440.0, sample_rate=48000, num_partials=20)
    result = calc.calculate(24)

    num_folded = sum(1 for p in result.partials if p.folded)

    print(f"\nDecimation: {result.decimation_rate}x")
    print(f"Total partials: {len(result.partials)}")
    print(f"Folded partials: {num_folded}")
    print(f"Spectral range: {min(result.get_aliased_frequencies()):.1f} - "
          f"{max(result.get_aliased_frequencies()):.1f} Hz")


def example_11_compare_decimations():
    """Example 11: Compare multiple decimation rates for same input."""
    print("\n" + "=" * 80)
    print("Example 11: Decimation Rate Comparison")
    print("=" * 80)
    print("Compare 2x, 8x, 16x, and 32x decimation for 440 Hz")

    calc = AliasingCalculator(fundamental_freq=440.0, sample_rate=48000, num_partials=8)

    print(f"\n{'Dec':<6} {'Fund (Hz)':<12} {'Folded':<10} {'Range (Hz)':<20}")
    print("-" * 60)

    for dec in [2, 8, 16, 32]:
        result = calc.calculate(dec)
        fund = result.partials[0].aliased_freq
        folded = sum(1 for p in result.partials if p.folded)
        freqs = result.get_aliased_frequencies()

        print(f"{dec}x     {fund:<12.2f} {folded}/{len(result.partials):<7} "
              f"{min(freqs):.1f} - {max(freqs):.1f}")


def example_12_midi_notes():
    """Example 12: Explore aliasing for different MIDI note frequencies."""
    print("\n" + "=" * 80)
    print("Example 12: MIDI Note Exploration")
    print("=" * 80)

    # MIDI notes: C3, E3, G3, C4 (C major chord)
    notes = {
        'C3': 130.81,
        'E3': 164.81,
        'G3': 196.00,
        'C4': 261.63
    }

    print(f"\n{'Note':<6} {'Freq (Hz)':<12} {'Best Dec':<10} {'Method':<12}")
    print("-" * 60)

    for note, freq in notes.items():
        calc = AliasingCalculator(fundamental_freq=freq, sample_rate=48000, num_partials=6)
        result = calc.search(method='purest', max_decimation=32)
        print(f"{note:<6} {freq:<12.2f} {result.decimation_rate}x{' ':<7} purest")


def example_13_richest_texture():
    """Example 13: Maximize spectral complexity for rich textures."""
    print("\n" + "=" * 80)
    print("Example 13: Rich Texture Generator")
    print("=" * 80)
    print("Find most complex, inharmonic aliasing pattern")

    calc = AliasingCalculator(fundamental_freq=880.0, sample_rate=48000, num_partials=12)
    result = calc.search(method='richest', max_decimation=64)

    freqs = sorted(result.get_aliased_frequencies())

    print(f"\nBest decimation: {result.decimation_rate}x")
    print(f"Spectral density: {len(freqs)} partials in {max(freqs) - min(freqs):.1f} Hz range")
    print(f"Folded partials: {sum(1 for p in result.partials if p.folded)}/{len(result.partials)}")


def example_14_mirror_symmetry():
    """Example 14: Find symmetric spectrum patterns."""
    print("\n" + "=" * 80)
    print("Example 14: Mirror Symmetry Finder")
    print("=" * 80)
    print("Create symmetric aliasing patterns")

    calc = AliasingCalculator(fundamental_freq=440.0, sample_rate=48000, num_partials=8)
    result = calc.search(method='mirror', max_decimation=64)

    center = result.nyquist_freq / 2.0

    print(f"\nBest decimation: {result.decimation_rate}x")
    print(f"Spectrum center: {center:.2f} Hz")
    print(f"\nPartial distances from center:")
    for i, p in enumerate(result.partials[:6]):
        dist = abs(p.aliased_freq - center)
        print(f"  Partial {i+1}: {dist:.2f} Hz from center")


def example_15_narrow_search_range():
    """Example 15: Search within a specific decimation range."""
    print("\n" + "=" * 80)
    print("Example 15: Narrow Search Range")
    print("=" * 80)
    print("Search only between 16x and 24x decimation")

    calc = AliasingCalculator(fundamental_freq=440.0, sample_rate=48000, num_partials=8)
    result = calc.search(method='purest', min_decimation=16, max_decimation=24)

    print(f"\nSearch range: 16x - 24x")
    print(f"Best found: {result.decimation_rate}x")
    print(f"Decimated SR: {result.decimated_sample_rate} Hz")


def example_16_beating_detection():
    """Example 16: Detect close partials that create beating."""
    print("\n" + "=" * 80)
    print("Example 16: Beating Detection")
    print("=" * 80)
    print("Find partials close together that will create beating")

    calc = AliasingCalculator(fundamental_freq=440.0, sample_rate=48000, num_partials=10)
    result = calc.calculate(27)

    sorted_freqs = sorted(result.get_aliased_frequencies())

    print(f"\nDecimation: {result.decimation_rate}x")
    print("\nClose partials (< 10 Hz apart):")

    for i in range(len(sorted_freqs) - 1):
        diff = sorted_freqs[i+1] - sorted_freqs[i]
        if diff < 10:
            beat_rate = diff
            print(f"  {sorted_freqs[i]:.2f} Hz & {sorted_freqs[i+1]:.2f} Hz "
                  f"→ {beat_rate:.2f} Hz beating")


def example_17_octave_relationships():
    """Example 17: Find octave relationships between partials."""
    print("\n" + "=" * 80)
    print("Example 17: Octave Relationship Finder")
    print("=" * 80)

    calc = AliasingCalculator(fundamental_freq=220.0, sample_rate=48000, num_partials=12)
    result = calc.calculate(29)

    freqs = sorted(result.get_aliased_frequencies())

    print(f"\nDecimation: {result.decimation_rate}x")
    print("\nOctave relationships found:")

    octaves_found = 0
    for i in range(len(freqs)):
        for j in range(i + 1, len(freqs)):
            ratio = freqs[j] / freqs[i]
            if abs(ratio - 2.0) < 0.05:  # Within 5% of perfect octave
                octaves_found += 1
                print(f"  {freqs[i]:.2f} Hz : {freqs[j]:.2f} Hz (ratio: {ratio:.3f})")

    if octaves_found == 0:
        print("  No octaves found")


def example_18_extreme_decimation():
    """Example 18: Explore extreme decimation rates."""
    print("\n" + "=" * 80)
    print("Example 18: Extreme Decimation (128x)")
    print("=" * 80)
    print("See what happens at very high decimation rates")

    calc = AliasingCalculator(fundamental_freq=440.0, sample_rate=48000, num_partials=8)
    result = calc.calculate(128)

    print(f"\nDecimation: {result.decimation_rate}x")
    print(f"Decimated SR: {result.decimated_sample_rate} Hz")
    print(f"Nyquist: {result.nyquist_freq:.2f} Hz")
    print(f"\nAll partials:")
    for p in result.partials:
        print(f"  {p.original_freq:.1f} → {p.aliased_freq:.2f} Hz [FOLDED]")


def example_19_prime_decimations():
    """Example 19: Compare prime number decimation rates."""
    print("\n" + "=" * 80)
    print("Example 19: Prime Decimation Rates")
    print("=" * 80)
    print("Prime numbers often create interesting patterns")

    calc = AliasingCalculator(fundamental_freq=440.0, sample_rate=48000, num_partials=8)
    primes = [3, 5, 7, 11, 13, 17, 19, 23]

    print(f"\n{'Dec':<6} {'Fund':<12} {'Folded':<10} {'Unique Freqs':<15}")
    print("-" * 60)

    for prime in primes:
        result = calc.calculate(prime)
        folded = sum(1 for p in result.partials if p.folded)
        unique = len(set(round(f, 1) for f in result.get_aliased_frequencies()))

        print(f"{prime}x     {result.partials[0].aliased_freq:<12.2f} "
              f"{folded}/{len(result.partials):<7} {unique}")


def example_20_all_methods_comparison():
    """Example 20: Compare all 9 search methods for same input."""
    print("\n" + "=" * 80)
    print("Example 20: All Search Methods Comparison")
    print("=" * 80)
    print("Compare all methods for 440 Hz")

    calc = AliasingCalculator(fundamental_freq=440.0, sample_rate=48000, num_partials=8)

    methods = ['nearest', 'purest', 'richest', 'consonant', 'subharmonic',
               'metallic', 'sparse', 'freeze', 'mirror']

    print(f"\n{'Method':<12} {'Dec':<6} {'Fund (Hz)':<12} {'Folded':<10}")
    print("-" * 60)

    for method in methods:
        result = calc.search(method=method, max_decimation=64)
        folded = sum(1 for p in result.partials if p.folded)

        print(f"{method:<12} {result.decimation_rate}x{' ':<3} "
              f"{result.partials[0].aliased_freq:<12.2f} {folded}/{len(result.partials)}")


def run_all_examples():
    """Run all 20 examples sequentially."""
    examples = [
        example_01_basic_calculation,
        example_02_search_nearest,
        example_03_subharmonic_bass,
        example_04_metallic_percussion,
        example_05_frozen_spectrum,
        example_06_consonant_harmonies,
        example_07_sparse_spectrum,
        example_08_high_sample_rate,
        example_09_low_frequency,
        example_10_many_partials,
        example_11_compare_decimations,
        example_12_midi_notes,
        example_13_richest_texture,
        example_14_mirror_symmetry,
        example_15_narrow_search_range,
        example_16_beating_detection,
        example_17_octave_relationships,
        example_18_extreme_decimation,
        example_19_prime_decimations,
        example_20_all_methods_comparison,
    ]

    print("\n" + "=" * 80)
    print("RUNNING ALL 20 EXAMPLES")
    print("=" * 80)

    for i, example_func in enumerate(examples, 1):
        try:
            example_func()
        except Exception as e:
            print(f"\n[ERROR in Example {i}]: {e}")
            import traceback
            traceback.print_exc()

    print("\n" + "=" * 80)
    print(f"COMPLETED: {len(examples)} examples")
    print("=" * 80)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Run specific example by number
        example_num = int(sys.argv[1])
        example_name = f"example_{example_num:02d}"

        # Get the function from globals
        example_func = globals().get(example_name + "_" +
                                     [n for n in globals() if n.startswith(example_name)][0].split('_', 2)[2])
        if example_func:
            example_func()
        else:
            print(f"Example {example_num} not found")
    else:
        # Run all examples
        run_all_examples()
