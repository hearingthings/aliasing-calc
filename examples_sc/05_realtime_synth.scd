/*
 * Example 5: Real-time Synthesis with Aliasing
 *
 * Use aliasing calculations to inform synthesis parameters in real-time.
 */

// Load the aliasing calculator
(thisProcess.nowExecutingPath.dirname +/+ "../supercollider/aliasing_calc.scd").load;

(
fork {
	var result, aliasedFreqs, synth;

	1.wait;

	"======================================".postln;
	"Example 5: Real-time Synthesis Example".postln;
	"======================================".postln;
	"".postln;

	// Calculate aliasing for 220 Hz at 32x decimation
	result = ~aliasingCalculate.(220, 48000, 32, 12);

	"Calculating aliased partials for synthesis...".postln;
	~aliasingPrintResult.(result);

	// Extract aliased frequencies for synthesis
	aliasedFreqs = ~aliasingGetAliasedFreqs.(result);

	"".postln;
	"Creating additive synth with aliased partials...".postln;

	// Create a SynthDef using the aliased frequencies
	SynthDef(\aliasingAdditive, { |out = 0, amp = 0.1, gate = 1|
		var sig, env, freqs;

		freqs = \freqs.kr(Array.fill(12, 440));
		env = EnvGen.kr(Env.asr(0.01, 1, 0.1), gate, doneAction: 2);

		sig = Mix.ar(
			freqs.collect({ |freq, i|
				var partialAmp;
				partialAmp = (1 / (i + 1)) * 0.5;  // Natural harmonic rolloff
				SinOsc.ar(freq, 0, partialAmp)
			})
		);

		sig = sig * env * amp;
		Out.ar(out, sig ! 2);
	}).add;

	1.wait;

	"Playing synth with aliased partials...".postln;
	"(Press Cmd+. to stop)".postln;
	"".postln;

	synth = Synth(\aliasingAdditive, [
		\freqs, aliasedFreqs,
		\amp, 0.2
	]);

	4.wait;

	"Changing to different decimation rate (16x)...".postln;
	result = ~aliasingCalculate.(220, 48000, 16, 12);
	aliasedFreqs = ~aliasingGetAliasedFreqs.(result);
	synth.set(\freqs, aliasedFreqs);

	4.wait;

	"Changing to subharmonic decimation...".postln;
	result = ~aliasingSearch.(220, 48000, \subharmonic, 12, 2, 64);
	aliasedFreqs = ~aliasingGetAliasedFreqs.(result);
	synth.set(\freqs, aliasedFreqs);

	4.wait;

	synth.release;

	"".postln;
	"Example complete!".postln;
}
)
