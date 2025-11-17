/*
 * Example 2: Search Methods
 *
 * Demonstrates different search methods to find optimal decimation rates.
 */

// Load the aliasing calculator
(thisProcess.nowExecutingPath.dirname +/+ "../supercollider/aliasing_calc.scd").load;

(
fork {
	var result, methods;

	1.wait;

	"======================================".postln;
	"Example 2: Search Methods Comparison".postln;
	"======================================".postln;
	"".postln;

	methods = [\nearest, \purest, \richest, \consonant, \subharmonic, \metallic, \sparse, \freeze, \mirror];

	methods.do({ |method|
		"".postln;
		"--------------------------------------".postln;
		"Method: %".format(method.asString.toUpper).postln;
		"--------------------------------------".postln;

		result = ~aliasingSearch.(440, 48000, method, 8, 2, 64);

		"Best decimation rate: %x".format(result[\decimationRate]).postln;
		"Decimated SR: % Hz".format(result[\decimatedSampleRate]).postln;
		"Aliased fundamental: % Hz".format(result[\partials][0][\aliasedFreq].round(0.01)).postln;
		"Folded partials: %/%".format(
			~aliasingCountFolded.(result),
			result[\numPartials]
		).postln;

		1.wait;
	});

	"".postln;
	"Search complete!".postln;
}
)
