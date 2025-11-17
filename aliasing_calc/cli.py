"""Command-line interface for aliasing calculator."""

import argparse
import sys
from .core import AliasingCalculator


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Calculate aliasing effects for audio decimation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Calculate aliasing for 440Hz at 16x decimation
  aliasing-calc 440 --decimation 16

  # Search for best decimation rate using "purest" method
  aliasing-calc 440 --search purest

  # Search for subharmonic decimation (lower pitch)
  aliasing-calc 440 --search subharmonic --max-decimation 64

  # Find metallic/bell-like inharmonic pattern
  aliasing-calc 880 --search metallic --partials 10

  # Analyze 220Hz with 12 partials at 96kHz sample rate
  aliasing-calc 220 --sr 96000 --partials 12 --decimation 8

Search methods:
  nearest      - Keep fundamental close to original pitch
  purest       - Minimize beating, maximize harmonicity
  richest      - Maximize spectral complexity
  consonant    - Form musical intervals between partials
  subharmonic  - Lower the fundamental pitch
  metallic     - Create bell-like inharmonic ratios
  sparse       - Maximize gaps between partials
  freeze       - Alias partials near DC (low frequencies)
  mirror       - Create symmetric spectrum patterns
        """
    )

    parser.add_argument(
        "frequency",
        type=float,
        help="Fundamental frequency in Hz (e.g., 440 for A4)"
    )

    parser.add_argument(
        "--sr", "--sample-rate",
        type=float,
        default=48000.0,
        dest="sample_rate",
        help="Sample rate in Hz (default: 48000)"
    )

    parser.add_argument(
        "--partials",
        type=int,
        default=8,
        help="Number of partials/harmonics to analyze (default: 8)"
    )

    # Mutually exclusive: either specify decimation or search for it
    action_group = parser.add_mutually_exclusive_group(required=True)

    action_group.add_argument(
        "--decimation", "-d",
        type=int,
        help="Decimation rate (e.g., 2, 4, 8, 16)"
    )

    action_group.add_argument(
        "--search", "-s",
        choices=[
            "nearest", "purest", "richest", "consonant",
            "subharmonic", "metallic", "sparse", "freeze", "mirror"
        ],
        help="Search for optimal decimation rate using specified method"
    )

    parser.add_argument(
        "--min-decimation",
        type=int,
        default=2,
        help="Minimum decimation rate for search (default: 2)"
    )

    parser.add_argument(
        "--max-decimation",
        type=int,
        default=64,
        help="Maximum decimation rate for search (default: 64)"
    )

    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Show detailed output"
    )

    args = parser.parse_args()

    # Validate inputs
    if args.frequency <= 0:
        print("Error: Frequency must be positive", file=sys.stderr)
        return 1

    if args.sample_rate <= 0:
        print("Error: Sample rate must be positive", file=sys.stderr)
        return 1

    if args.partials < 1:
        print("Error: Must have at least 1 partial", file=sys.stderr)
        return 1

    # Create calculator
    try:
        calc = AliasingCalculator(
            fundamental_freq=args.frequency,
            sample_rate=args.sample_rate,
            num_partials=args.partials
        )
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    # Calculate or search
    try:
        if args.decimation:
            result = calc.calculate(args.decimation)
            print(result)
        else:
            print(f"Searching for optimal decimation rate using '{args.search}' method...")
            print(f"Range: {args.min_decimation}x to {args.max_decimation}x")
            print()

            result = calc.search(
                method=args.search,
                min_decimation=args.min_decimation,
                max_decimation=args.max_decimation
            )

            print(f"Best decimation rate found: {result.decimation_rate}x")
            print()
            print(result)

    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
