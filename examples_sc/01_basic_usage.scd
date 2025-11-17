/*
 * Example 1: Basic Usage
 *
 * This example demonstrates basic aliasing calculation and result inspection.
 */

// Load the aliasing calculator
(thisProcess.nowExecutingPath.dirname +/+ "../supercollider/aliasing_calc.scd").load;

// Wait for it to load
(
fork {
	1.wait;

	"======================================".postln;
	"Example 1: Basic Aliasing Calculation".postln;
	"======================================".postln;
	"".postln;

	// Calculate aliasing for A4 (440 Hz) at 16x decimation
	var result;
	result = ~aliasingCalculate.(440, 48000, 16, 8);

	"Calculating 440 Hz at 16x decimation:".postln;
	"".postln;
	~aliasingPrintResult.(result);

	"".postln;
	"--------------------------------------".postln;
	"Extracting specific information:".postln;
	"--------------------------------------".postln;

	"Aliased frequencies: %".format(~aliasingGetAliasedFreqs.(result)).postln;
	"Original frequencies: %".format(~aliasingGetOriginalFreqs.(result)).postln;
	"Folded count: %".format(~aliasingCountFolded.(result)).postln;
}
)
