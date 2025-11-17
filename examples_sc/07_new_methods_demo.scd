/*
 * Example 7: New Search Methods Demo
 *
 * Demonstrates the consonant, metallic, and mirror search methods.
 */

// Load the aliasing calculator
(thisProcess.nowExecutingPath.dirname +/+ "../supercollider/aliasing_calc.scd").load;

(
fork {
	var result, aliasedFreqs, originalFreq, aliasedFreq;

	1.wait;

	"======================================".postln;
	"Example 7: New Search Methods".postln;
	"======================================".postln;
	"".postln;

	// Test CONSONANT method
	"--------------------------------------".postln;
	"CONSONANT Method - Musical Intervals".postln;
	"--------------------------------------".postln;
	"".postln;

	result = ~aliasingSearch.(440, 48000, \consonant, 8, 2, 64);

	"Best decimation: %x".format(result[\decimationRate]).postln;
	"".postln;

	// Check for intervals
	aliasedFreqs = ~aliasingGetAliasedFreqs.(result).sort;
	"Looking for musical intervals:".postln;
	aliasedFreqs.size.do({ |i|
		(i + 1).do({ |j|
			var ratio;
			if(j < aliasedFreqs.size, {
				ratio = aliasedFreqs[j] / aliasedFreqs[i];
				if((ratio - 2.0).abs < 0.05, {
					"  Octave: % Hz : % Hz (ratio: %)".format(
						aliasedFreqs[i].round(0.1),
						aliasedFreqs[j].round(0.1),
						ratio.round(0.001)
					).postln;
				});
				if((ratio - 1.5).abs < 0.05, {
					"  Fifth: % Hz : % Hz (ratio: %)".format(
						aliasedFreqs[i].round(0.1),
						aliasedFreqs[j].round(0.1),
						ratio.round(0.001)
					).postln;
				});
			});
		});
	});

	2.wait;

	// Test METALLIC method
	"".postln;
	"--------------------------------------".postln;
	"METALLIC Method - Bell-like Ratios".postln;
	"--------------------------------------".postln;
	"".postln;

	result = ~aliasingSearch.(880, 48000, \metallic, 10, 2, 32);

	"Best decimation: %x".format(result[\decimationRate]).postln;
	"Decimated SR: % Hz".format(result[\decimatedSampleRate]).postln;
	"".postln;

	"Partial ratios (relative to fundamental):".postln;
	aliasedFreqs = ~aliasingGetAliasedFreqs.(result).sort;
	aliasedFreqs.do({ |freq, i|
		var ratio;
		if(i > 0, {
			ratio = freq / aliasedFreqs[0];
			"  Partial %: %x (target bell ratios: 2.0, 3.0, 4.4, 5.4, 6.8, 8.2)".format(
				i + 1,
				ratio.round(0.01)
			).postln;
		});
	});

	2.wait;

	// Test MIRROR method
	"".postln;
	"--------------------------------------".postln;
	"MIRROR Method - Symmetric Patterns".postln;
	"--------------------------------------".postln;
	"".postln;

	result = ~aliasingSearch.(440, 48000, \mirror, 8, 2, 64);

	"Best decimation: %x".format(result[\decimationRate]).postln;
	"Nyquist: % Hz".format(result[\nyquistFreq]).postln;
	"Center: % Hz".format(result[\nyquistFreq] / 2.0).postln;
	"".postln;

	"Partial distances from center:".postln;
	aliasedFreqs = ~aliasingGetAliasedFreqs.(result);
	aliasedFreqs.do({ |freq, i|
		var distance;
		distance = (freq - (result[\nyquistFreq] / 2.0)).abs;
		"  Partial %: % Hz from center".format(
			i + 1,
			distance.round(0.01)
		).postln;
	});

	2.wait;

	// Compare all 9 methods
	"".postln;
	"======================================".postln;
	"All 9 Search Methods Comparison".postln;
	"======================================".postln;
	"".postln;

	"Method       Dec   Fund(Hz)  Folded".postln;
	"--------------------------------------".postln;

	[\nearest, \purest, \richest, \consonant, \subharmonic, \metallic, \sparse, \freeze, \mirror].do({ |method|
		result = ~aliasingSearch.(440, 48000, method, 8, 2, 64);
		"%   %x   %    %/%".format(
			method.asString.padRight(11),
			result[\decimationRate].asString.padLeft(3),
			result[\partials][0][\aliasedFreq].round(0.01).asString.padLeft(8),
			~aliasingCountFolded.(result),
			result[\numPartials]
		).postln;
		0.5.wait;
	});

	"".postln;
	"Demo complete!".postln;
}
)
