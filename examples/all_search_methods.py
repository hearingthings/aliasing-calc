#!/usr/bin/env python3
"""Demonstration of all 9 search methods for aliasing calculation."""

from aliasing_calc import AliasingCalculator


def demonstrate_all_methods():
    """Demonstrate all search methods with detailed explanations."""

    # Configuration
    freq = 440.0  # A4
    sr = 48000
    partials = 10
    max_dec = 64

    calc = AliasingCalculator(
        fundamental_freq=freq,
        sample_rate=sr,
        num_partials=partials
    )

    methods = [
        ("nearest", "Keep fundamental close to original pitch"),
        ("purest", "Minimize beating, maximize harmonicity"),
        ("richest", "Maximize spectral complexity"),
        ("consonant", "Form musical intervals between partials"),
        ("subharmonic", "Lower the fundamental pitch"),
        ("metallic", "Create bell-like inharmonic ratios"),
        ("sparse", "Maximize gaps between partials"),
        ("freeze", "Alias partials near DC (very low frequencies)"),
        ("mirror", "Create symmetric spectrum patterns"),
    ]

    print("=" * 80)
    print(f"Demonstrating All Search Methods")
    print(f"Input: {freq} Hz with {partials} partials at {sr} Hz")
    print(f"Search range: 2x to {max_dec}x decimation")
    print("=" * 80)

    for method, description in methods:
        print(f"\n{'=' * 80}")
        print(f"Method: {method.upper()}")
        print(f"Description: {description}")
        print('=' * 80)

        result = calc.search(method=method, max_decimation=max_dec)

        print(f"\nBest decimation rate: {result.decimation_rate}x")
        print(f"Sample rate: {result.original_sample_rate:.0f} Hz → {result.decimated_sample_rate:.0f} Hz")
        print(f"Nyquist: {result.nyquist_freq:.2f} Hz")

        # Calculate some statistics
        aliased_freqs = result.get_aliased_frequencies()
        num_folded = sum(1 for p in result.partials if p.folded)
        fundamental_shift = result.partials[0].aliased_freq - freq

        print(f"\nStatistics:")
        print(f"  Fundamental: {freq:.2f} Hz → {result.partials[0].aliased_freq:.2f} Hz "
              f"({fundamental_shift:+.2f} Hz)")
        print(f"  Folded partials: {num_folded}/{partials}")
        print(f"  Frequency range: {min(aliased_freqs):.2f} - {max(aliased_freqs):.2f} Hz")

        # Show some partials
        print(f"\nFirst 5 partials:")
        for i in range(min(5, len(result.partials))):
            p = result.partials[i]
            fold_marker = " [FOLDED]" if p.folded else ""
            print(f"  {i+1}. {p.original_freq:.2f} Hz → {p.aliased_freq:.2f} Hz{fold_marker}")

        # Method-specific insights
        if method == "subharmonic":
            if fundamental_shift < -10:
                print(f"\n  ✓ Successfully lowered pitch by {abs(fundamental_shift):.2f} Hz!")

        elif method == "freeze":
            frozen = [p.aliased_freq for p in result.partials if p.aliased_freq < 50]
            if frozen:
                print(f"\n  ✓ {len(frozen)} partials frozen near DC: {', '.join(f'{f:.2f}' for f in frozen[:5])} Hz")

        elif method == "consonant":
            # Check for octaves
            for i in range(len(result.partials) - 1):
                for j in range(i + 1, len(result.partials)):
                    ratio = result.partials[j].aliased_freq / result.partials[i].aliased_freq
                    if abs(ratio - 2.0) < 0.05:
                        print(f"\n  ✓ Found octave: partials {i+1} and {j+1} "
                              f"({result.partials[i].aliased_freq:.1f} : {result.partials[j].aliased_freq:.1f} Hz)")
                        break

        elif method == "sparse":
            gaps = []
            sorted_freqs = sorted(aliased_freqs)
            for i in range(len(sorted_freqs) - 1):
                gaps.append(sorted_freqs[i+1] - sorted_freqs[i])
            avg_gap = sum(gaps) / len(gaps)
            print(f"\n  ✓ Average gap between partials: {avg_gap:.2f} Hz")


def compare_search_results():
    """Compare results from all methods side-by-side."""
    print("\n\n" + "=" * 80)
    print("COMPARISON TABLE: All Search Methods")
    print("=" * 80)

    freq = 440.0
    calc = AliasingCalculator(fundamental_freq=freq, sample_rate=48000, num_partials=8)

    methods = ["nearest", "purest", "richest", "consonant", "subharmonic",
               "metallic", "sparse", "freeze", "mirror"]

    print(f"\n{'Method':<12} {'Dec':<5} {'Fund (Hz)':<12} {'Shift (Hz)':<12} {'Folded':<8} {'SR (Hz)':<10}")
    print("-" * 80)

    for method in methods:
        result = calc.search(method=method, max_decimation=64)
        aliased_fund = result.partials[0].aliased_freq
        shift = aliased_fund - freq
        num_folded = sum(1 for p in result.partials if p.folded)

        print(f"{method:<12} {result.decimation_rate:<5} {aliased_fund:<12.2f} "
              f"{shift:+12.2f} {num_folded}/{len(result.partials):<5} "
              f"{result.decimated_sample_rate:<10.0f}")


if __name__ == "__main__":
    demonstrate_all_methods()
    compare_search_results()
