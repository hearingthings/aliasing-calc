/*
 * Aliasing Calculator for SuperCollider
 *
 * A creative tool for calculating and exploring aliasing effects in audio decimation.
 * Environment variable functions for easy integration into SC sessions.
 *
 * Author: Aliasing Calculator Contributors
 * License: MIT
 */

// ============================================================================
// Core Calculation Functions
// ============================================================================

/*
 * Calculate aliased frequency for a given frequency and sample rate
 *
 * Args:
 *   freq - Input frequency in Hz
 *   sampleRate - Sample rate in Hz
 *
 * Returns:
 *   Dictionary with keys:
 *     \aliasedFreq - The aliased frequency in Hz
 *     \folded - Boolean, true if frequency was above Nyquist
 */
~aliasingCalculateAliasedFrequency = { |freq, sampleRate|
	var nyquist, normalized, quotient, remainder, aliasedFreq, folded;

	nyquist = sampleRate / 2.0;

	if(freq <= nyquist, {
		aliasedFreq = freq;
		folded = false;
	}, {
		// Calculate how many times the frequency wraps around Nyquist
		normalized = freq / nyquist;
		quotient = normalized.floor;
		remainder = normalized - quotient;

		if(quotient.odd, {
			// Odd number of folds: frequency is reflected
			aliasedFreq = nyquist * (1.0 - remainder);
		}, {
			// Even number of folds: frequency wraps back up
			aliasedFreq = nyquist * remainder;
		});

		folded = true;
	});

	(aliasedFreq: aliasedFreq, folded: folded)
};

/*
 * Calculate aliasing for a specific decimation rate
 *
 * Args:
 *   fundamentalFreq - Fundamental frequency in Hz (e.g., 440.0 for A4)
 *   sampleRate - Sample rate in Hz (e.g., 48000)
 *   decimationRate - Decimation factor (e.g., 16)
 *   numPartials - Number of partials to analyze (default: 8)
 *
 * Returns:
 *   Dictionary with keys:
 *     \decimationRate - Decimation factor
 *     \originalSampleRate - Original sample rate in Hz
 *     \decimatedSampleRate - Decimated sample rate in Hz
 *     \nyquistFreq - Nyquist frequency in Hz
 *     \fundamentalFreq - Fundamental frequency in Hz
 *     \partials - Array of partial dictionaries
 *     \numPartials - Number of partials
 */
~aliasingCalculate = { |fundamentalFreq, sampleRate, decimationRate, numPartials = 8|
	var decimatedSR, nyquist, partials, result, originalFreq, aliasResult;

	decimatedSR = sampleRate / decimationRate;
	nyquist = decimatedSR / 2.0;
	partials = Array.newClear(numPartials);

	numPartials.do({ |i|
		originalFreq = fundamentalFreq * (i + 1);
		aliasResult = ~aliasingCalculateAliasedFrequency.(originalFreq, decimatedSR);

		partials[i] = (
			partialNumber: i + 1,
			originalFreq: originalFreq,
			aliasedFreq: aliasResult[\aliasedFreq],
			folded: aliasResult[\folded]
		);
	});

	result = (
		decimationRate: decimationRate,
		originalSampleRate: sampleRate,
		decimatedSampleRate: decimatedSR,
		nyquistFreq: nyquist,
		fundamentalFreq: fundamentalFreq,
		partials: partials,
		numPartials: numPartials
	);

	result
};

// ============================================================================
// Utility Functions
// ============================================================================

/*
 * Get array of aliased frequencies from result
 */
~aliasingGetAliasedFreqs = { |result|
	var freqs;
	freqs = result[\partials].collect({ |p| p[\aliasedFreq] });
	freqs
};

/*
 * Get array of original frequencies from result
 */
~aliasingGetOriginalFreqs = { |result|
	var freqs;
	freqs = result[\partials].collect({ |p| p[\originalFreq] });
	freqs
};

/*
 * Count how many partials were folded
 */
~aliasingCountFolded = { |result|
	var count;
	count = result[\partials].count({ |p| p[\folded] });
	count
};

/*
 * Print result in a formatted way
 */
~aliasingPrintResult = { |result|
	var foldedCount;

	foldedCount = ~aliasingCountFolded.(result);

	"Decimation Rate: %x".format(result[\decimationRate]).postln;
	"Sample Rate: % Hz -> % Hz".format(
		result[\originalSampleRate],
		result[\decimatedSampleRate]
	).postln;
	"Nyquist: % Hz".format(result[\nyquistFreq]).postln;
	"Fundamental: % Hz".format(result[\fundamentalFreq]).postln;
	"".postln;
	"Partials:".postln;

	result[\partials].do({ |p|
		var foldedStr;
		foldedStr = if(p[\folded], " [FOLDED]", "");
		"  Partial %: % Hz -> % Hz%".format(
			p[\partialNumber],
			p[\originalFreq].round(0.01),
			p[\aliasedFreq].round(0.01),
			foldedStr
		).postln;
	});

	"".postln;
	"Folded partials: %/%".format(foldedCount, result[\numPartials]).postln;
};

// ============================================================================
// Search Methods - Scoring Functions
// ============================================================================

/*
 * Score based on how close aliased fundamental is to original
 * Lower score is better
 */
~aliasingScoreNearest = { |result|
	var fundamental, distance;
	fundamental = result[\partials][0];
	distance = abs(fundamental[\aliasedFreq] - fundamental[\originalFreq]);
	distance
};

/*
 * Score based on harmonicity - minimal beating between partials
 * Lower score is better
 */
~aliasingScorePurest = { |result|
	var aliasedFreqs, sortedFreqs, diffs, minDiff, harmonicityError, beatingPenalty;
	var ratio, closestInt, error, diff, i, j;

	aliasedFreqs = ~aliasingGetAliasedFreqs.(result);
	sortedFreqs = aliasedFreqs.sort;

	if(sortedFreqs.size < 2, { ^0.0 });

	// Calculate all frequency differences
	diffs = [];
	sortedFreqs.size.do({ |i|
		(i + 1).do({ |j|
			if(j < sortedFreqs.size, {
				diffs = diffs.add(sortedFreqs[j] - sortedFreqs[i]);
			});
		});
	});

	if(diffs.size == 0, { ^0.0 });

	minDiff = diffs.minItem;

	// Calculate how well each frequency fits into harmonic series
	harmonicityError = 0.0;
	sortedFreqs.do({ |freq|
		ratio = freq / minDiff;
		closestInt = ratio.round;
		error = abs(ratio - closestInt);
		harmonicityError = harmonicityError + error;
	});

	// Penalize very small differences (beating)
	beatingPenalty = 0.0;
	(sortedFreqs.size - 1).do({ |i|
		diff = sortedFreqs[i + 1] - sortedFreqs[i];
		if(diff < 5.0, {
			beatingPenalty = beatingPenalty + ((5.0 - diff) * 10.0);
		});
	});

	harmonicityError + beatingPenalty
};

/*
 * Score based on spectral complexity/inharmonicity
 * Higher inharmonicity = better, so we negate
 */
~aliasingScoreRichest = { |result|
	var aliasedFreqs, sortedFreqs, spread, fundamentalEst, inharmonicity;
	var expectedHarmonic, deviation, uniqueFreqs, richness;

	aliasedFreqs = ~aliasingGetAliasedFreqs.(result);

	if(aliasedFreqs.size < 2, { ^0.0 });

	spread = aliasedFreqs.stdDev;
	sortedFreqs = aliasedFreqs.sort;
	fundamentalEst = sortedFreqs[0];

	if(fundamentalEst < 1.0, { fundamentalEst = 1.0 });

	inharmonicity = 0.0;
	sortedFreqs.do({ |freq, i|
		expectedHarmonic = fundamentalEst * (i + 1);
		deviation = abs(freq - expectedHarmonic) / fundamentalEst;
		inharmonicity = inharmonicity + deviation;
	});

	// Count unique frequencies (rounded to 0.1 Hz)
	uniqueFreqs = aliasedFreqs.collect({ |f| f.round(0.1) }).asSet.size;

	richness = spread * inharmonicity * uniqueFreqs;
	richness.neg  // Negate so lower is better
};

/*
 * Score based on subharmonic content (lower fundamental)
 * Lower score is better (smaller aliased freq = better)
 */
~aliasingScoreSubharmonic = { |result|
	var fundamental, originalFreq, aliasedFreq, ratio;

	fundamental = result[\partials][0];
	originalFreq = fundamental[\originalFreq];
	aliasedFreq = fundamental[\aliasedFreq];

	// We want aliased to be lower than original
	if(aliasedFreq >= (originalFreq * 0.95), {
		^inf  // Not significantly lowered
	});

	ratio = aliasedFreq / originalFreq;
	ratio  // Lower ratio = more lowering = better score
};

/*
 * Score based on how many partials alias near DC (< 50 Hz)
 * Lower score is better
 */
~aliasingScoreFreeze = { |result|
	var aliasedFreqs, freezeThreshold, frozenPartials, frozenFreqs, avgFrozenDist, score;

	aliasedFreqs = ~aliasingGetAliasedFreqs.(result);
	freezeThreshold = 50.0;

	frozenPartials = aliasedFreqs.count({ |f| f < freezeThreshold });

	if(frozenPartials == 0, { ^inf });

	frozenFreqs = aliasedFreqs.select({ |f| f < freezeThreshold });
	avgFrozenDist = frozenFreqs.sum / frozenFreqs.size;

	score = avgFrozenDist / (frozenPartials ** 2);
	score
};

/*
 * Score based on maximizing gaps between partials
 * We negate the gaps so lower is better
 */
~aliasingScoreSparse = { |result|
	var aliasedFreqs, sortedFreqs, gaps, avgGap, minGap, sparseness;

	aliasedFreqs = ~aliasingGetAliasedFreqs.(result);
	sortedFreqs = aliasedFreqs.sort;

	if(sortedFreqs.size < 2, { ^0.0 });

	gaps = (sortedFreqs.size - 1).collect({ |i|
		sortedFreqs[i + 1] - sortedFreqs[i]
	});

	avgGap = gaps.sum / gaps.size;
	minGap = gaps.minItem;

	sparseness = avgGap + (minGap / 2.0);
	sparseness.neg  // Negate so lower is better
};

/*
 * Score based on how well aliased partials form musical intervals
 * Lower score is better
 */
~aliasingScoreConsonant = { |result|
	var aliasedFreqs, sortedFreqs, targetRatios, consonanceScore, numPairs;
	var ratio, bestMatchError, bestWeight, error, weight;

	aliasedFreqs = ~aliasingGetAliasedFreqs.(result);
	sortedFreqs = aliasedFreqs.select({ |f| f > 10 }).sort;  // Ignore very low freqs

	if(sortedFreqs.size < 2, { ^inf });

	// Musical interval ratios (ratio, name, weight)
	targetRatios = [
		[2.0, "octave", 1.0],      // Perfect consonance
		[1.5, "fifth", 0.8],       // Strong consonance
		[4/3, "fourth", 0.7],      // Strong consonance
		[5/4, "maj3rd", 0.6],      // Medium consonance
		[6/5, "min3rd", 0.5],      // Medium consonance
		[3.0, "octave+5th", 0.4],  // Compound interval
		[8/5, "min6th", 0.3],      // Weak consonance
		[5/3, "maj6th", 0.3]       // Weak consonance
	];

	consonanceScore = 0.0;
	numPairs = 0;

	// Check all pairs of partials
	sortedFreqs.size.do({ |i|
		(i + 1).do({ |j|
			if(j < sortedFreqs.size, {
				ratio = sortedFreqs[j] / sortedFreqs[i];

				// Find closest target ratio
				bestMatchError = inf;
				bestWeight = 0.0;

				targetRatios.do({ |targetData|
					var targetRatio, name, targetWeight;
					targetRatio = targetData[0];
					name = targetData[1];
					targetWeight = targetData[2];

					error = abs(ratio - targetRatio) / targetRatio;
					if(error < bestMatchError, {
						bestMatchError = error;
						bestWeight = targetWeight;
					});
				});

				// Weight by consonance strength
				consonanceScore = consonanceScore + (bestMatchError / (bestWeight + 0.1));
				numPairs = numPairs + 1;
			});
		});
	});

	consonanceScore / max(numPairs, 1)
};

/*
 * Score based on inharmonic ratios similar to metallic percussion
 * Lower score is better
 */
~aliasingScoreMetallic = { |result|
	var aliasedFreqs, sortedFreqs, targetRatios, fundamental, metallicScore;
	var ratio, minError, error, target;

	aliasedFreqs = ~aliasingGetAliasedFreqs.(result);
	sortedFreqs = aliasedFreqs.select({ |f| f > 10 }).sort;

	if(sortedFreqs.size < 3, { ^inf });

	// Target ratios for bell-like sounds (inharmonic)
	targetRatios = [2.0, 3.0, 4.4, 5.4, 6.8, 8.2];

	fundamental = sortedFreqs[0];
	metallicScore = 0.0;

	// Check ratios for partials above fundamental
	(sortedFreqs.size - 1).do({ |i|
		var freq;
		freq = sortedFreqs[i + 1];
		ratio = freq / fundamental;

		// Find closest target ratio
		minError = inf;
		targetRatios.do({ |tgt|
			error = abs(ratio - tgt);
			if(error < minError, { minError = error });
		});

		// Penalize if too close to integer (harmonic)
		if(abs(ratio - ratio.round) < 0.1, {
			metallicScore = metallicScore + 10.0;  // Big penalty for harmonic
		}, {
			metallicScore = metallicScore + minError;
		});
	});

	// Normalize by number of partials
	metallicScore / sortedFreqs.size
};

/*
 * Score based on symmetric aliasing pattern around center frequency
 * Lower score is better
 */
~aliasingScoreMirror = { |result|
	var aliasedFreqs, nyquist, center, distances, sortedDists, symmetryError;
	var pairDiff, i;

	aliasedFreqs = ~aliasingGetAliasedFreqs.(result);
	nyquist = result[\nyquistFreq];

	if(aliasedFreqs.size < 3, { ^inf });

	// Check symmetry around Nyquist/2
	center = nyquist / 2.0;

	// Calculate distances from center
	distances = aliasedFreqs.collect({ |f| abs(f - center) });

	// Sort distances and check if they come in pairs
	sortedDists = distances.sort;

	symmetryError = 0.0;
	i = 0;
	while({ i < (sortedDists.size - 1) }, {
		// Check if consecutive pairs are similar
		pairDiff = abs(sortedDists[i] - sortedDists[i + 1]);
		symmetryError = symmetryError + pairDiff;
		i = i + 2;
	});

	// Normalize by number of partials
	symmetryError / aliasedFreqs.size
};

// ============================================================================
// Search Function
// ============================================================================

/*
 * Search for optimal decimation rate using specified method
 *
 * Args:
 *   fundamentalFreq - Fundamental frequency in Hz
 *   sampleRate - Sample rate in Hz
 *   method - Search method: \nearest, \purest, \richest, \consonant, \subharmonic,
 *            \metallic, \sparse, \freeze, \mirror
 *   numPartials - Number of partials to analyze (default: 8)
 *   minDecimation - Minimum decimation rate (default: 2)
 *   maxDecimation - Maximum decimation rate (default: 64)
 *
 * Returns:
 *   Result dictionary for best decimation rate found
 */
~aliasingSearch = { |fundamentalFreq, sampleRate, method = \purest, numPartials = 8,
                     minDecimation = 2, maxDecimation = 64|
	var scoreFuncs, scoreFunc, bestResult, bestScore, result, score;

	scoreFuncs = (
		nearest: ~aliasingScoreNearest,
		purest: ~aliasingScorePurest,
		richest: ~aliasingScoreRichest,
		consonant: ~aliasingScoreConsonant,
		subharmonic: ~aliasingScoreSubharmonic,
		metallic: ~aliasingScoreMetallic,
		sparse: ~aliasingScoreSparse,
		freeze: ~aliasingScoreFreeze,
		mirror: ~aliasingScoreMirror
	);

	scoreFunc = scoreFuncs[method];

	if(scoreFunc.isNil, {
		Error("Unknown search method: %. Available: %".format(
			method, scoreFuncs.keys
		)).throw;
	});

	bestResult = nil;
	bestScore = inf;

	(minDecimation..maxDecimation).do({ |decimation|
		result = ~aliasingCalculate.(fundamentalFreq, sampleRate, decimation, numPartials);
		score = scoreFunc.(result);

		// Keep first result as fallback
		if(bestResult.isNil, { bestResult = result });

		if(score < bestScore, {
			bestScore = score;
			bestResult = result;
		});
	});

	bestResult
};

// ============================================================================
// Convenience Functions
// ============================================================================

/*
 * Quick calculation with default parameters
 */
~aliasingCalc = { |freq = 440, decimation = 16, sr = 48000, partials = 8|
	~aliasingCalculate.(freq, sr, decimation, partials)
};

/*
 * Quick search with default parameters
 */
~aliasingFind = { |freq = 440, method = \purest, sr = 48000, partials = 8, maxDec = 64|
	~aliasingSearch.(freq, sr, method, partials, 2, maxDec)
};

"Aliasing Calculator for SuperCollider loaded.".postln;
"".postln;
"Usage:".postln;
"  ~aliasingCalc.(440, 16)                    // Calculate 440 Hz at 16x decimation".postln;
"  ~aliasingFind.(440, \\purest)               // Search for purest decimation".postln;
"  ~aliasingSearch.(440, 48000, \\subharmonic) // Search for subharmonic".postln;
"".postln;
