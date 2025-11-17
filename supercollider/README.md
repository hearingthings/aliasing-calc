# Aliasing Calculator - SuperCollider Implementation

A creative tool for calculating and exploring aliasing effects in audio decimation, implemented as SuperCollider environment variables for easy integration into live coding and composition sessions.

## Features

- **Environment variable functions** - Easy to use with `~` prefix
- **9 search methods** - Find optimal decimation rates for different creative goals
- **Real-time ready** - Calculate and apply aliasing in synthesis
- **Pure SuperCollider** - No external dependencies
- **Interactive workflow** - Perfect for live coding and exploration

## Installation

Simply load the file in SuperCollider:

```supercollider
(thisProcess.nowExecutingPath.dirname +/+ "aliasing_calc.scd").load;
```

Or place it in your SuperCollider extensions folder and load on startup.

## Quick Start

```supercollider
// Load the library
"path/to/aliasing_calc.scd".load;

// Calculate aliasing for 440 Hz at 16x decimation
~aliasingCalc.(440, 16).postln;

// Search for purest harmonic decimation
~aliasingFind.(440, \purest).postln;

// Get aliased frequencies for synthesis
(
var result = ~aliasingCalc.(220, 32, 48000, 12);
var freqs = ~aliasingGetAliasedFreqs.(result);
freqs.postln;  // Use these in a synth!
)
```

## Core Functions

### `~aliasingCalculate`
Calculate aliasing for a specific decimation rate.

```supercollider
~aliasingCalculate.(fundamentalFreq, sampleRate, decimationRate, numPartials)

// Example
result = ~aliasingCalculate.(440, 48000, 16, 8);
```

**Parameters:**
- `fundamentalFreq` - Fundamental frequency in Hz (e.g., 440 for A4)
- `sampleRate` - Sample rate in Hz (default: 48000)
- `decimationRate` - Decimation factor (e.g., 2, 4, 8, 16)
- `numPartials` - Number of partials to analyze (default: 8)

**Returns:** Dictionary with keys:
- `\decimationRate` - Decimation factor
- `\originalSampleRate` - Original sample rate
- `\decimatedSampleRate` - Decimated sample rate
- `\nyquistFreq` - Nyquist frequency
- `\fundamentalFreq` - Fundamental frequency
- `\partials` - Array of partial dictionaries
- `\numPartials` - Number of partials

### `~aliasingSearch`
Search for optimal decimation rate using specified method.

```supercollider
~aliasingSearch.(fundamentalFreq, sampleRate, method, numPartials, minDecimation, maxDecimation)

// Example
result = ~aliasingSearch.(440, 48000, \purest, 8, 2, 64);
```

**Parameters:**
- `fundamentalFreq` - Fundamental frequency in Hz
- `sampleRate` - Sample rate in Hz
- `method` - Search method (symbol):
  - `\nearest` - Keep fundamental close to original
  - `\purest` - Minimize beating, maximize harmonicity
  - `\richest` - Maximize spectral complexity
  - `\consonant` - Form musical intervals between partials
  - `\subharmonic` - Lower the fundamental pitch
  - `\metallic` - Create bell-like inharmonic ratios
  - `\sparse` - Maximize gaps between partials
  - `\freeze` - Alias partials near DC (< 50 Hz)
  - `\mirror` - Create symmetric spectrum patterns
- `numPartials` - Number of partials (default: 8)
- `minDecimation` - Minimum decimation rate (default: 2)
- `maxDecimation` - Maximum decimation rate (default: 64)

**Returns:** Same dictionary as `~aliasingCalculate`

## Convenience Functions

### `~aliasingCalc`
Quick calculation with defaults.

```supercollider
~aliasingCalc.(freq, decimation, sampleRate, partials)

// Examples
~aliasingCalc.(440, 16);          // 440 Hz at 16x
~aliasingCalc.(220, 32, 96000);   // 220 Hz at 32x, 96kHz SR
```

### `~aliasingFind`
Quick search with defaults.

```supercollider
~aliasingFind.(freq, method, sampleRate, partials, maxDecimation)

// Examples
~aliasingFind.(440, \purest);      // Search for purest
~aliasingFind.(880, \subharmonic); // Search for subharmonic
```

## Utility Functions

### `~aliasingGetAliasedFreqs`
Extract aliased frequencies as an array.

```supercollider
result = ~aliasingCalc.(440, 16);
freqs = ~aliasingGetAliasedFreqs.(result);
// Use in synthesis: { Mix(SinOsc.ar(freqs)) }.play;
```

### `~aliasingGetOriginalFreqs`
Extract original frequencies as an array.

```supercollider
freqs = ~aliasingGetOriginalFreqs.(result);
```

### `~aliasingCountFolded`
Count how many partials were folded around Nyquist.

```supercollider
foldedCount = ~aliasingCountFolded.(result);
```

### `~aliasingPrintResult`
Print formatted result to post window.

```supercollider
~aliasingPrintResult.(result);
```

## Search Methods Explained

### `\nearest`
Finds decimation rates where the fundamental stays close to its original pitch. Useful when you want minimal pitch shift but still want some aliasing effects.

### `\purest`
Minimizes beating and inharmonicity for the cleanest, most harmonic sound. Great for tonal, consonant textures.

### `\richest`
Maximizes spectral complexity and inharmonicity for dense, complex timbres. Perfect for noisy, chaotic sounds.

### `\consonant`
Creates musical intervals (octaves, fifths, fourths, thirds) between aliased partials. Perfect for harmonic, tonal textures with clear interval relationships.

### `\subharmonic`
Lowers the pitch by aliasing the fundamental below its original frequency. Excellent for bass enhancement and octave-down effects.

### `\metallic`
Generates inharmonic ratios similar to bells and metallic percussion (2.0, 3.0, 4.4, 5.4, 6.8, 8.2). Creates bell-like, gong-like timbres.

### `\sparse`
Creates wide gaps between partials for open, spacious spectra. Good for minimal, transparent sounds.

### `\freeze`
Aliases partials to very low frequencies (< 50 Hz) for frozen, rumbling, subsonic effects. Creates deep, slow-moving timbres.

### `\mirror`
Creates symmetric patterns around the center of the spectrum. Results in balanced frequency distribution with mirrored partials.

## Usage Examples

### Basic Calculation

```supercollider
(
// Calculate and print
var result = ~aliasingCalculate.(440, 48000, 16, 8);
~aliasingPrintResult.(result);
)
```

### Compare Search Methods

```supercollider
(
[\nearest, \purest, \richest, \subharmonic].do({ |method|
    var result = ~aliasingSearch.(440, 48000, method);
    "Method: % -> Decimation: %x".format(method, result[\decimationRate]).postln;
});
)
```

### Real-time Synthesis

```supercollider
(
// Calculate aliased partials
var result = ~aliasingCalculate.(220, 48000, 32, 12);
var freqs = ~aliasingGetAliasedFreqs.(result);

// Use in additive synthesis
{
    var sig = Mix.ar(
        freqs.collect({ |freq, i|
            SinOsc.ar(freq, 0, 1 / (i + 1))
        })
    );
    sig = sig * 0.2 ! 2;
}.play;
)
```

### Dynamic Decimation

```supercollider
(
// Sweep through decimation rates
fork {
    (2..32).do({ |dec|
        var result = ~aliasingCalculate.(440, 48000, dec, 8);
        var freqs = ~aliasingGetAliasedFreqs.(result);

        "Decimation: %x".format(dec).postln;
        { Mix(SinOsc.ar(freqs, 0, 1 / freqs.size)) * 0.3 ! 2 }.play;

        1.wait;
    });
}
)
```

### Subharmonic Bass

```supercollider
(
// Find best subharmonic decimation
var result = ~aliasingSearch.(110, 48000, \subharmonic, 8, 2, 64);

"Original: % Hz".format(result[\fundamentalFreq]).postln;
"Aliased: % Hz".format(result[\partials][0][\aliasedFreq]).postln;

// Play the deep bass
{ SinOsc.ar(result[\partials][0][\aliasedFreq]) * 0.5 ! 2 }.play;
)
```

## Examples

Six complete examples are provided in `examples_sc/`:

1. **01_basic_usage.scd** - Basic calculation and result inspection
2. **02_search_methods.scd** - Compare all search methods
3. **03_subharmonic_bass.scd** - Subharmonic bass generation
4. **04_compare_decimations.scd** - Side-by-side decimation comparison
5. **05_realtime_synth.scd** - Real-time synthesis with aliased partials
6. **06_interactive_exploration.scd** - Interactive helper functions

Run examples:
```supercollider
"examples_sc/01_basic_usage.scd".loadRelative;
```

## Tips for Live Coding

```supercollider
// Quick shortcuts for interactive use
~ap = { |f=440, d=16| ~aliasingCalc.(f,d); };  // Aliasing Print
~as = { |f=440, m=\purest| ~aliasingFind.(f,m); };  // Aliasing Search

// Use in performance
~ap.(220, 24);
~as.(880, \subharmonic);
```

## Integration with Patterns

```supercollider
(
// Use aliased frequencies in Pbind
var result = ~aliasingCalc.(440, 32, 48000, 8);
var freqs = ~aliasingGetAliasedFreqs.(result);

Pbind(
    \instrument, \default,
    \freq, Pseq(freqs, inf),
    \dur, 0.25,
    \amp, 0.3
).play;
)
```

## Performance Considerations

- Calculation functions are fast enough for interactive use
- Pre-calculate decimation tables for real-time parameter modulation
- Use environment variables for easy access in live coding sessions
- Search functions iterate through all decimation rates - cache results if needed

## Limitations

- Maximum decimation rate is configurable but typically 2-128
- Calculations assume integer decimation rates only
- All functions use single-precision floats (standard for SuperCollider)

## License

MIT License
