"""Tests for search algorithms."""

import pytest
from aliasing_calc.core import AliasingCalculator
from aliasing_calc.search import (
    calculate_nearest_score,
    calculate_purest_score,
    calculate_richest_score,
    search_decimation_rate
)


class TestScoreFunctions:
    """Test the scoring functions."""

    def test_nearest_score(self):
        """Test nearest score calculation."""
        calc = AliasingCalculator(440, 48000, 4)

        # No decimation should give score of 0 (fundamental unchanged)
        result = calc.calculate(1)
        score = calculate_nearest_score(result)
        assert score == 0.0

        # Higher decimation should give higher score
        result = calc.calculate(16)
        score = calculate_nearest_score(result)
        assert score >= 0.0

    def test_purest_score(self):
        """Test purest score calculation."""
        calc = AliasingCalculator(440, 48000, 8)
        result = calc.calculate(4)
        score = calculate_purest_score(result)
        assert isinstance(score, float)
        assert score >= 0.0

    def test_richest_score(self):
        """Test richest score calculation."""
        calc = AliasingCalculator(440, 48000, 8)
        result = calc.calculate(4)
        score = calculate_richest_score(result)
        assert isinstance(score, float)


class TestSearchDecimationRate:
    """Test the search function."""

    def test_search_unknown_method(self):
        """Test search with unknown method."""
        calc = AliasingCalculator(440, 48000, 8)
        with pytest.raises(ValueError, match="Unknown search method"):
            search_decimation_rate(calc, method="unknown")

    def test_search_returns_valid_result(self):
        """Test that search returns a valid result."""
        calc = AliasingCalculator(440, 48000, 8)

        for method in ["nearest", "purest", "richest"]:
            result = search_decimation_rate(
                calc,
                method=method,
                min_decimation=2,
                max_decimation=16
            )

            assert result is not None
            assert 2 <= result.decimation_rate <= 16
            assert len(result.partials) == 8

    def test_search_narrow_range(self):
        """Test search with narrow decimation range."""
        calc = AliasingCalculator(440, 48000, 4)
        result = search_decimation_rate(
            calc,
            method="nearest",
            min_decimation=8,
            max_decimation=8
        )

        assert result.decimation_rate == 8
