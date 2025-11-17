/*
 * Example 4: Compare Multiple Decimation Rates
 *
 * Side-by-side comparison of different decimation rates.
 */

// Load the aliasing calculator
(thisProcess.nowExecutingPath.dirname +/+ "../supercollider/aliasing_calc.scd").load;

(
fork {
	var decimations, result;

	1.wait;

	"======================================".postln;
	"Example 4: Decimation Rate Comparison".postln;
	"======================================".postln;
	"".postln;

	"Comparing decimation rates for 440 Hz:".postln;
	"".postln;

	"Dec    Fund(Hz)  Folded   SR(Hz)".postln;
	"--------------------------------------".postln;

	decimations = [2, 4, 8, 16, 24, 32, 48, 64];

	decimations.do({ |dec|
		result = ~aliasingCalculate.(440, 48000, dec, 8);

		"%x     %      %/%    %".format(
			dec.asString.padLeft(4),
			result[\partials][0][\aliasedFreq].round(0.01).asString.padLeft(8),
			~aliasingCountFolded.(result),
			result[\numPartials],
			result[\decimatedSampleRate].asInteger
		).postln;
	});

	"".postln;
}
)
