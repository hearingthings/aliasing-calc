# Aliasing Calculator

A creative tool for calculating and exploring aliasing effects in audio decimation, turning aliasing from a problem into a compositional feature.

## Features

- **Aliasing Calculation**: Calculate how harmonics alias when decimating audio signals
- **Multiple Search Methods**: Find optimal decimation rates using different strategies
  - `nearest`: Keep aliased fundamental close to original
  - `purest`: Minimize beating between partials (most harmonic)
  - `richest`: Maximize spectral complexity/inharmonicity
  - And more to come...
- **Multi-stage Cascades**: Chain decimators for richer effects
- **Frequency Analysis**: Detailed spectrum analysis pre/post aliasing
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
aliasing-calc 440 --sr 48000 --partials 8 --decimation 16

# Search for best decimation rate
aliasing-calc 440 --search purest --max-decimation 64
```

## Development Roadmap

- [x] Core aliasing calculation
- [x] Basic search methods
- [ ] Advanced search methods (consonant, mirror, metallic, etc.)
- [ ] Cascade optimization
- [ ] Visualization tools
- [ ] Musical preset library
- [ ] SuperCollider port
- [ ] Embedded C port

## License

MIT
