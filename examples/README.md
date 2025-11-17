# Examples

This directory contains comprehensive examples demonstrating the aliasing calculator library.

## Available Examples

### 20_examples.py - Complete Example Suite

Run all 20 examples:
```bash
python3 examples/20_examples.py
```

Run a specific example (1-20):
```bash
python3 examples/20_examples.py 1  # Run example 1
python3 examples/20_examples.py 13 # Run example 13
```

#### Example List

1. **Basic Calculation** - Simple aliasing calculation at a specific decimation rate
2. **Search Nearest** - Find decimation rate keeping fundamental closest to original
3. **Subharmonic Bass** - Generate deep bass by lowering pitch through aliasing
4. **Metallic Percussion** - Create bell-like metallic timbres
5. **Frozen Spectrum** - Alias partials to subsonic frequencies (< 50 Hz)
6. **Consonant Harmonies** - Find musical interval relationships
7. **Sparse Spectrum** - Maximize gaps between partials for open sound
8. **High Sample Rate** - Working with 96kHz sample rate
9. **Low Frequency** - Aliasing effects on low frequencies (55 Hz)
10. **Many Partials** - Analyze complex waveforms with 20 partials
11. **Compare Decimations** - Side-by-side comparison of different decimation rates
12. **MIDI Notes** - Explore aliasing for different MIDI note frequencies
13. **Rich Texture** - Maximize spectral complexity for rich textures
14. **Mirror Symmetry** - Find symmetric spectrum patterns
15. **Narrow Search Range** - Search within specific decimation range
16. **Beating Detection** - Detect close partials that create beating
17. **Octave Relationships** - Find octave relationships between partials
18. **Extreme Decimation** - Explore very high decimation rates (128x)
19. **Prime Decimations** - Compare prime number decimation rates
20. **All Methods Comparison** - Compare all 9 search methods side-by-side

### basic_usage.py

Introduction to the library with simple examples:
```bash
python3 examples/basic_usage.py
```

Demonstrates:
- Basic aliasing calculation
- Search methods (nearest, purest, richest)
- Method comparison

### creative_exploration.py

Advanced creative techniques:
```bash
python3 examples/creative_exploration.py
```

Demonstrates:
- Frequency exploration for different pitches
- Subharmonic decimation finding
- Consonant interval patterns
- Beat frequency patterns

### all_search_methods.py

Comprehensive demonstration of all 9 search methods:
```bash
python3 examples/all_search_methods.py
```

Demonstrates:
- All 9 search methods with detailed statistics
- Method-specific insights
- Comparison table

## Use Cases Covered

### Sound Design
- Bass enhancement (subharmonic)
- Metallic/bell-like sounds (metallic)
- Frozen/subsonic effects (freeze)
- Rich textures (richest)
- Sparse/minimal textures (sparse)

### Musical Applications
- Consonant harmonies (consonant)
- Octave relationships
- MIDI note exploration
- Different sample rates

### Technical Exploration
- Beating detection
- Prime number decimations
- Extreme decimation rates
- Spectral analysis

## Running Examples

All examples can be run with:
```bash
PYTHONPATH=/path/to/aliasing-calc python3 examples/example_name.py
```

Or if the package is installed:
```bash
python3 examples/example_name.py
```
