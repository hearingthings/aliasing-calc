"""Tests for core aliasing calculation functions."""

import pytest
import numpy as np
from aliasing_calc.core import (
    calculate_aliased_frequency,
    AliasingCalculator,
    PartialInfo,
    AliasingResult
)


class TestCalculateAliasedFrequency:
    """Test the calculate_aliased_frequency function."""

    def test_no_aliasing_below_nyquist(self):
        """Frequencies below Nyquist should not alias."""
        freq, folded = calculate_aliased_frequency(100, 1000)
        assert freq == 100.0
        assert folded is False

    def test_aliasing_above_nyquist(self):
        """Frequencies above Nyquist should fold back."""
        # 600 Hz with SR=1000 (Nyquist=500)
        # Should fold to 500 - (600-500) = 400
        freq, folded = calculate_aliased_frequency(600, 1000)
        assert abs(freq - 400.0) < 0.01
        assert folded is True

    def test_frequency_at_nyquist(self):
        """Frequency exactly at Nyquist should not alias."""
        freq, folded = calculate_aliased_frequency(500, 1000)
        assert freq == 500.0
        assert folded is False

    def test_multiple_folds(self):
        """Test frequency that folds multiple times."""
        # 1600 Hz with SR=1000 (Nyquist=500)
        # First fold: 1600 -> 500-(1600-500) = -600 -> 600 (wraps)
        # Actually: 1600/500 = 3.2, quotient=3 (odd), remainder=0.2
        # odd fold: 500*(1-0.2) = 400
        freq, folded = calculate_aliased_frequency(1600, 1000)
        assert abs(freq - 400.0) < 0.01
        assert folded is True

    def test_zero_frequency(self):
        """Zero frequency should remain zero."""
        freq, folded = calculate_aliased_frequency(0, 1000)
        assert freq == 0.0
        assert folded is False


class TestAliasingCalculator:
    """Test the AliasingCalculator class."""

    def test_init_valid_params(self):
        """Test initialization with valid parameters."""
        calc = AliasingCalculator(440, 48000, 8)
        assert calc.fundamental_freq == 440
        assert calc.sample_rate == 48000
        assert calc.num_partials == 8

    def test_init_invalid_frequency(self):
        """Test initialization with invalid frequency."""
        with pytest.raises(ValueError, match="Fundamental frequency must be positive"):
            AliasingCalculator(-440, 48000, 8)

    def test_init_invalid_sample_rate(self):
        """Test initialization with invalid sample rate."""
        with pytest.raises(ValueError, match="Sample rate must be positive"):
            AliasingCalculator(440, -48000, 8)

    def test_init_invalid_partials(self):
        """Test initialization with invalid number of partials."""
        with pytest.raises(ValueError, match="Must have at least 1 partial"):
            AliasingCalculator(440, 48000, 0)

    def test_calculate_no_decimation(self):
        """Test calculation with decimation rate of 1 (no decimation)."""
        calc = AliasingCalculator(440, 48000, 4)
        result = calc.calculate(1)

        assert result.decimation_rate == 1
        assert result.original_sample_rate == 48000
        assert result.decimated_sample_rate == 48000
        assert len(result.partials) == 4

        # No aliasing should occur
        for i, partial in enumerate(result.partials):
            assert partial.partial_number == i + 1
            assert partial.original_freq == 440 * (i + 1)
            assert partial.aliased_freq == partial.original_freq
            assert partial.folded is False

    def test_calculate_with_decimation(self):
        """Test calculation with actual decimation."""
        calc = AliasingCalculator(1000, 8000, 3)
        result = calc.calculate(4)  # 8000/4 = 2000 Hz, Nyquist = 1000 Hz

        assert result.decimation_rate == 4
        assert result.decimated_sample_rate == 2000
        assert result.nyquist_freq == 1000

        # Partial 1: 1000 Hz -> 1000 Hz (at Nyquist, no fold)
        assert result.partials[0].aliased_freq == 1000
        assert result.partials[0].folded is False

        # Partial 2: 2000 Hz -> folds to 0 Hz
        assert abs(result.partials[1].aliased_freq - 0) < 0.01
        assert result.partials[1].folded is True

        # Partial 3: 3000 Hz -> folds
        # 3000/1000 = 3.0, quotient=3 (odd), remainder=0
        # odd fold: 1000*(1-0) = 1000
        assert abs(result.partials[2].aliased_freq - 1000) < 0.01

    def test_get_aliased_frequencies(self):
        """Test getting array of aliased frequencies."""
        calc = AliasingCalculator(440, 48000, 3)
        result = calc.calculate(1)
        freqs = result.get_aliased_frequencies()

        assert isinstance(freqs, np.ndarray)
        assert len(freqs) == 3
        np.testing.assert_array_almost_equal(freqs, [440, 880, 1320])

    def test_get_original_frequencies(self):
        """Test getting array of original frequencies."""
        calc = AliasingCalculator(440, 48000, 3)
        result = calc.calculate(16)
        freqs = result.get_original_frequencies()

        assert isinstance(freqs, np.ndarray)
        assert len(freqs) == 3
        np.testing.assert_array_almost_equal(freqs, [440, 880, 1320])

    def test_search_nearest(self):
        """Test search with 'nearest' method."""
        calc = AliasingCalculator(440, 48000, 8)
        result = calc.search(method="nearest", min_decimation=2, max_decimation=16)

        assert result is not None
        assert 2 <= result.decimation_rate <= 16

    def test_search_purest(self):
        """Test search with 'purest' method."""
        calc = AliasingCalculator(440, 48000, 8)
        result = calc.search(method="purest", min_decimation=2, max_decimation=16)

        assert result is not None
        assert 2 <= result.decimation_rate <= 16

    def test_search_richest(self):
        """Test search with 'richest' method."""
        calc = AliasingCalculator(440, 48000, 8)
        result = calc.search(method="richest", min_decimation=2, max_decimation=16)

        assert result is not None
        assert 2 <= result.decimation_rate <= 16

    def test_invalid_decimation_rate(self):
        """Test calculation with invalid decimation rate."""
        calc = AliasingCalculator(440, 48000, 8)
        with pytest.raises(ValueError, match="Decimation rate must be at least 1"):
            calc.calculate(0)
