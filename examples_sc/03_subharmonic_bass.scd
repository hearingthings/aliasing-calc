/*
 * Example 3: Subharmonic Bass Generator
 *
 * Find decimation rates that create deep bass by lowering the pitch.
 */

// Load the aliasing calculator
(thisProcess.nowExecutingPath.dirname +/+ "../supercollider/aliasing_calc.scd").load;

(
fork {
	var result, originalFreq, aliasedFreq, drop;

	1.wait;

	"======================================".postln;
	"Example 3: Subharmonic Bass Generator".postln;
	"======================================".postln;
	"".postln;

	// Search for subharmonic decimation for 440 Hz
	"Searching for subharmonic decimation for 440 Hz...".postln;
	result = ~aliasingSearch.(440, 48000, \subharmonic, 10, 2, 64);

	"".postln;
	"Best decimation found: %x".format(result[\decimationRate]).postln;

	originalFreq = result[\fundamentalFreq];
	aliasedFreq = result[\partials][0][\aliasedFreq];
	drop = originalFreq - aliasedFreq;

	"Pitch transformation:".postln;
	"  Original: % Hz".format(originalFreq.round(0.01)).postln;
	"  Aliased: % Hz".format(aliasedFreq.round(0.01)).postln;
	"  Drop: % Hz".format(drop.round(0.01)).postln;
	"  Ratio: %x".format((aliasedFreq / originalFreq).round(0.001)).postln;

	"".postln;
	"Full spectrum:".postln;
	~aliasingPrintResult.(result);
}
)
