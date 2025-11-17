# Aliasing Calculator

A creative tool for calculating and exploring aliasing effects in audio decimation, turning aliasing from a problem into a compositional feature.

## Features

- **Aliasing Calculation**: Calculate how harmonics alias when decimating audio signals
- **9 Creative Search Methods**: Find optimal decimation rates using different strategies
  - `nearest`: Keep aliased fundamental close to original pitch
  - `purest`: Minimize beating between partials (most harmonic)
  - `richest`: Maximize spectral complexity/inharmonicity
  - `consonant`: Form musical intervals between partials (octaves, fifths, thirds)
  - `subharmonic`: Lower the fundamental pitch (subharmonic generation)
  - `metallic`: Create bell-like inharmonic ratios
  - `sparse`: Maximize gaps between partials (open spectrum)
  - `freeze`: Alias partials near DC (frozen, very low frequencies)
  - `mirror`: Create symmetric spectrum patterns
- **Comprehensive Analysis**: Detailed spectrum analysis pre/post aliasing with folding detection
- **Multi-platform**: Python library with planned SuperCollider and embedded C ports

## Installation

```bash
pip install -e .
```

## Quick Start

```python
from aliasing_calc import AliasingCalculator

# Create calculator for 440Hz signal at 48kHz
calc = AliasingCalculator(
    fundamental_freq=440.0,
    sample_rate=48000,
    num_partials=8
)

# Find optimal decimation rate using "purest" method
result = calc.search(method='purest', max_decimation=64)
print(result)
```

## CLI Usage

```bash
# Calculate aliasing for 440Hz with 8 partials at 16x decimation
python3 -m aliasing_calc.cli 440 --decimation 16

# Search for best decimation rate using different methods
python3 -m aliasing_calc.cli 440 --search purest --max-decimation 64
python3 -m aliasing_calc.cli 440 --search subharmonic --max-decimation 64
python3 -m aliasing_calc.cli 880 --search metallic --partials 10
python3 -m aliasing_calc.cli 440 --search freeze --max-decimation 64
python3 -m aliasing_calc.cli 220 --search consonant --max-decimation 32

# Run with custom parameters
python3 -m aliasing_calc.cli 220 --sr 96000 --partials 12 --decimation 8
```

### Search Methods Explained

- **nearest**: Finds decimation rates where the fundamental stays close to its original pitch
- **purest**: Minimizes beating and inharmonicity for the cleanest, most harmonic sound
- **richest**: Maximizes spectral complexity and inharmonicity for dense, complex timbres
- **consonant**: Creates musical intervals (octaves, fifths, etc.) between aliased partials
- **subharmonic**: Lowers the pitch by aliasing the fundamental below its original frequency
- **metallic**: Generates inharmonic ratios similar to bells and metallic percussion
- **sparse**: Creates wide gaps between partials for open, spacious spectra
- **freeze**: Aliases partials to very low frequencies (< 50 Hz) for frozen, rumbling effects
- **mirror**: Creates symmetric patterns around the center of the spectrum

## C Implementation

A lightweight embedded C implementation is available in `c_impl/`:

```c
#include "aliasing_calc.h"

aliasing_calculator_t calc;
aliasing_result_t result;

aliasing_calculator_init(&calc, 440.0f, 48000.0f, 8);
aliasing_calculate(&calc, 16, &result);
aliasing_print_result(&result);
```

**Features:**
- Zero dependencies (only standard C library)
- Minimal footprint: 12 bytes calculator, 536 bytes results
- No dynamic allocation
- Real-time ready
- C99 compatible

See [`c_impl/README.md`](c_impl/README.md) for full documentation.

**Build and run:**
```bash
make all
make run-all
```

## SuperCollider Implementation

A complete SuperCollider implementation using environment variables is available in `supercollider/`:

```supercollider
// Load the library
"supercollider/aliasing_calc.scd".load;

// Quick calculation
~aliasingCalc.(440, 16);  // 440 Hz at 16x decimation

// Search for optimal decimation
~aliasingFind.(440, \purest);

// Use in synthesis
(
var result = ~aliasingCalc.(220, 32, 48000, 12);
var freqs = ~aliasingGetAliasedFreqs.(result);
{ Mix(SinOsc.ar(freqs, 0, 1/freqs.size)) * 0.3 ! 2 }.play;
)
```

**Features:**
- Environment variable functions (`~aliasingCalc`, `~aliasingFind`, etc.)
- 6 search methods (\nearest, \purest, \richest, \subharmonic, \freeze, \sparse)
- Real-time synthesis integration
- Perfect for live coding and interactive exploration
- Pure SuperCollider (no external dependencies)

**6 Example files in `examples_sc/`:**
- Basic usage and result inspection
- Search method comparisons
- Subharmonic bass generation
- Real-time synthesis with aliased partials
- Interactive exploration helpers
- Pattern integration

See [`supercollider/README.md`](supercollider/README.md) for full documentation.

## Development Roadmap

- [x] Core aliasing calculation
- [x] Basic search methods (nearest, purest, richest)
- [x] Advanced search methods (consonant, subharmonic, metallic, sparse, freeze, mirror)
- [x] Comprehensive test suite
- [x] Embedded C implementation
- [x] 20+ example scripts
- [x] SuperCollider implementation
- [ ] Beat frequency targeting
- [ ] Cascade optimization (multi-stage decimation)
- [ ] Visualization tools (matplotlib spectrum plots)
- [ ] Musical preset library

## License

MIT
