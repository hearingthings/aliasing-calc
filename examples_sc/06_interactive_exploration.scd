/*
 * Example 6: Interactive Exploration
 *
 * Define some helper functions for interactive exploration in the IDE.
 */

// Load the aliasing calculator
(thisProcess.nowExecutingPath.dirname +/+ "../supercollider/aliasing_calc.scd").load;

(
"======================================".postln;
"Example 6: Interactive Helper Functions".postln;
"======================================".postln;
"".postln;

// Quick print function
~ap = { |freq = 440, dec = 16, sr = 48000, partials = 8|
	var result;
	result = ~aliasingCalculate.(freq, sr, dec, partials);
	~aliasingPrintResult.(result);
};

// Quick search function
~as = { |freq = 440, method = \purest, sr = 48000, partials = 8|
	var result;
	result = ~aliasingSearch.(freq, sr, method, partials, 2, 64);
	"Search method: %".format(method).postln;
	"".postln;
	~aliasingPrintResult.(result);
};

// Compare multiple methods
~acompare = { |freq = 440, sr = 48000, partials = 8|
	var methods, result;

	methods = [\nearest, \purest, \richest, \subharmonic, \freeze, \sparse];

	"Method      Dec   Fund(Hz)   Folded".postln;
	"--------------------------------------".postln;

	methods.do({ |method|
		result = ~aliasingSearch.(freq, sr, method, partials, 2, 64);
		"%   %x    %     %/%".format(
			method.asString.padRight(10),
			result[\decimationRate].asString.padLeft(3),
			result[\partials][0][\aliasedFreq].round(0.01).asString.padLeft(8),
			~aliasingCountFolded.(result),
			result[\numPartials]
		).postln;
	});
};

"Interactive functions loaded:".postln;
"".postln;
"  ~ap.(440, 16)              // Print aliasing for 440 Hz at 16x".postln;
"  ~as.(440, \\purest)         // Search for purest decimation".postln;
"  ~acompare.(440)            // Compare all search methods".postln;
"".postln;
"Try them out!".postln;
"".postln;
)

// Example usage - uncomment to try:
// ~ap.(440, 24);
// ~as.(220, \subharmonic);
// ~acompare.(880);
