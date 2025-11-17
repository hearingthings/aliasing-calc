"""Core aliasing calculation functions."""

import numpy as np
from typing import List, Tuple, Optional
from dataclasses import dataclass


@dataclass
class PartialInfo:
    """Information about a single partial (harmonic)."""
    partial_number: int
    original_freq: float
    aliased_freq: float
    folded: bool  # True if frequency folded around Nyquist

    def __repr__(self):
        fold_marker = " [FOLDED]" if self.folded else ""
        return f"Partial {self.partial_number}: {self.original_freq:.2f} Hz → {self.aliased_freq:.2f} Hz{fold_marker}"


@dataclass
class AliasingResult:
    """Complete result of aliasing calculation."""
    decimation_rate: int
    original_sample_rate: float
    decimated_sample_rate: float
    nyquist_freq: float
    fundamental_freq: float
    partials: List[PartialInfo]

    def __repr__(self):
        lines = [
            f"Decimation Rate: {self.decimation_rate}x",
            f"Sample Rate: {self.original_sample_rate:.0f} Hz → {self.decimated_sample_rate:.0f} Hz",
            f"Nyquist: {self.nyquist_freq:.2f} Hz",
            f"Fundamental: {self.fundamental_freq:.2f} Hz",
            "\nPartials:"
        ]
        for p in self.partials:
            lines.append(f"  {p}")
        return "\n".join(lines)

    def get_aliased_frequencies(self) -> np.ndarray:
        """Get array of aliased frequencies."""
        return np.array([p.aliased_freq for p in self.partials])

    def get_original_frequencies(self) -> np.ndarray:
        """Get array of original frequencies."""
        return np.array([p.original_freq for p in self.partials])


def calculate_aliased_frequency(freq: float, sample_rate: float) -> Tuple[float, bool]:
    """
    Calculate the aliased frequency for a given frequency and sample rate.

    When a frequency is above Nyquist (sample_rate/2), it aliases to a lower frequency
    through spectral folding. This function calculates where the frequency ends up.

    Args:
        freq: Input frequency in Hz
        sample_rate: Sample rate in Hz

    Returns:
        Tuple of (aliased_frequency, folded)
        - aliased_frequency: The resulting frequency after aliasing
        - folded: True if the frequency was above Nyquist and folded

    Examples:
        >>> calculate_aliased_frequency(100, 1000)
        (100.0, False)  # Below Nyquist, no aliasing

        >>> calculate_aliased_frequency(600, 1000)
        (400.0, True)  # Above Nyquist (500), folds to 500 - (600-500) = 400
    """
    nyquist = sample_rate / 2.0

    if freq <= nyquist:
        return freq, False

    # Calculate how many times the frequency wraps around Nyquist
    # The frequency "bounces" between 0 and Nyquist
    normalized = freq / nyquist
    quotient = int(normalized)
    remainder = normalized - quotient

    if quotient % 2 == 1:
        # Odd number of folds: frequency is reflected
        aliased = nyquist * (1 - remainder)
    else:
        # Even number of folds: frequency wraps back up
        aliased = nyquist * remainder

    return aliased, True


class AliasingCalculator:
    """
    Calculate aliasing effects for audio decimation.

    This class models what happens when you decimate (downsample) an audio signal
    containing multiple harmonics. Each harmonic can alias to a different frequency
    based on the new Nyquist frequency.
    """

    def __init__(
        self,
        fundamental_freq: float,
        sample_rate: float = 48000.0,
        num_partials: int = 8
    ):
        """
        Initialize the aliasing calculator.

        Args:
            fundamental_freq: Fundamental frequency in Hz (e.g., 440.0 for A4)
            sample_rate: Current sample rate in Hz (default: 48000)
            num_partials: Number of harmonics to analyze including fundamental (default: 8)
        """
        if fundamental_freq <= 0:
            raise ValueError("Fundamental frequency must be positive")
        if sample_rate <= 0:
            raise ValueError("Sample rate must be positive")
        if num_partials < 1:
            raise ValueError("Must have at least 1 partial")

        self.fundamental_freq = fundamental_freq
        self.sample_rate = sample_rate
        self.num_partials = num_partials

    def calculate(self, decimation_rate: int) -> AliasingResult:
        """
        Calculate aliasing for a specific decimation rate.

        Args:
            decimation_rate: Integer decimation factor (e.g., 2, 4, 8, 16)

        Returns:
            AliasingResult containing detailed information about all partials
        """
        if decimation_rate < 1:
            raise ValueError("Decimation rate must be at least 1")

        decimated_sr = self.sample_rate / decimation_rate
        nyquist = decimated_sr / 2.0

        partials = []
        for n in range(1, self.num_partials + 1):
            original_freq = self.fundamental_freq * n
            aliased_freq, folded = calculate_aliased_frequency(original_freq, decimated_sr)

            partials.append(PartialInfo(
                partial_number=n,
                original_freq=original_freq,
                aliased_freq=aliased_freq,
                folded=folded
            ))

        return AliasingResult(
            decimation_rate=decimation_rate,
            original_sample_rate=self.sample_rate,
            decimated_sample_rate=decimated_sr,
            nyquist_freq=nyquist,
            fundamental_freq=self.fundamental_freq,
            partials=partials
        )

    def search(
        self,
        method: str = "nearest",
        min_decimation: int = 2,
        max_decimation: int = 64
    ) -> AliasingResult:
        """
        Search for optimal decimation rate using specified method.

        Args:
            method: Search method - "nearest", "purest", or "richest"
            min_decimation: Minimum decimation rate to consider
            max_decimation: Maximum decimation rate to consider

        Returns:
            AliasingResult for the best decimation rate found
        """
        from .search import search_decimation_rate
        return search_decimation_rate(
            self,
            method=method,
            min_decimation=min_decimation,
            max_decimation=max_decimation
        )
