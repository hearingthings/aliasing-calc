#!/usr/bin/env python3
"""Basic usage examples for aliasing calculator."""

from aliasing_calc import AliasingCalculator


def example_basic_calculation():
    """Example: Calculate aliasing for a specific decimation rate."""
    print("=" * 60)
    print("Example 1: Basic Aliasing Calculation")
    print("=" * 60)

    # Create calculator for A4 (440 Hz) with 8 partials
    calc = AliasingCalculator(
        fundamental_freq=440.0,
        sample_rate=48000,
        num_partials=8
    )

    # Calculate what happens at 16x decimation
    result = calc.calculate(decimation_rate=16)
    print(result)
    print()


def example_search_nearest():
    """Example: Search for decimation rate that keeps fundamental closest."""
    print("=" * 60)
    print("Example 2: Search for 'Nearest' Decimation Rate")
    print("=" * 60)

    calc = AliasingCalculator(
        fundamental_freq=440.0,
        sample_rate=48000,
        num_partials=8
    )

    result = calc.search(method="nearest", max_decimation=32)
    print(f"Best decimation rate: {result.decimation_rate}x")
    print()
    print(result)
    print()


def example_search_purest():
    """Example: Search for most harmonic aliasing pattern."""
    print("=" * 60)
    print("Example 3: Search for 'Purest' (Most Harmonic) Pattern")
    print("=" * 60)

    calc = AliasingCalculator(
        fundamental_freq=220.0,  # A3
        sample_rate=48000,
        num_partials=12
    )

    result = calc.search(method="purest", max_decimation=64)
    print(f"Best decimation rate: {result.decimation_rate}x")
    print()
    print(result)
    print()


def example_search_richest():
    """Example: Search for most complex/inharmonic pattern."""
    print("=" * 60)
    print("Example 4: Search for 'Richest' (Most Inharmonic) Pattern")
    print("=" * 60)

    calc = AliasingCalculator(
        fundamental_freq=880.0,  # A5
        sample_rate=48000,
        num_partials=6
    )

    result = calc.search(method="richest", max_decimation=32)
    print(f"Best decimation rate: {result.decimation_rate}x")
    print()
    print(result)
    print()


def example_compare_methods():
    """Example: Compare different search methods."""
    print("=" * 60)
    print("Example 5: Compare Search Methods")
    print("=" * 60)

    calc = AliasingCalculator(
        fundamental_freq=440.0,
        sample_rate=48000,
        num_partials=8
    )

    methods = ["nearest", "purest", "richest"]

    for method in methods:
        result = calc.search(method=method, max_decimation=64)
        print(f"\nMethod: {method.upper()}")
        print(f"  Decimation Rate: {result.decimation_rate}x")
        print(f"  Decimated SR: {result.decimated_sample_rate:.0f} Hz")
        print(f"  Aliased Fundamental: {result.partials[0].aliased_freq:.2f} Hz")
        print(f"  Folded Partials: {sum(1 for p in result.partials if p.folded)}/{len(result.partials)}")


if __name__ == "__main__":
    example_basic_calculation()
    example_search_nearest()
    example_search_purest()
    example_search_richest()
    example_compare_methods()
