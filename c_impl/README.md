# Aliasing Calculator - C Implementation

A lightweight, embedded-friendly C library for calculating aliasing effects in audio decimation.

## Features

- **Zero dependencies** - Only standard C library (math.h for float operations)
- **Minimal memory footprint** - 12 bytes for calculator, 536 bytes for results with 32 partials
- **No dynamic allocation** - Fixed-size structures suitable for embedded systems
- **C99 compatible** - Works with any modern C compiler
- **Well-documented** - Comprehensive API documentation in headers
- **Real-time ready** - Fast calculations suitable for audio-rate processing

## Building

### Prerequisites
- C compiler (gcc, clang, or any C99-compatible compiler)
- Make (optional, for build automation)

### Quick Build
```bash
make all
```

This builds the library and all examples.

### Manual Build
```bash
# Compile library
gcc -c c_impl/aliasing_calc.c -o build/aliasing_calc.o

# Compile example
gcc examples_c/basic_example.c build/aliasing_calc.o -lm -o basic_example
```

## Usage

### Basic Example

```c
#include "aliasing_calc.h"

int main(void) {
    aliasing_calculator_t calc;
    aliasing_result_t result;

    /* Initialize calculator for A4 (440 Hz) at 48kHz with 8 partials */
    aliasing_calculator_init(&calc, 440.0f, 48000.0f, 8);

    /* Calculate aliasing at 16x decimation */
    aliasing_calculate(&calc, 16, &result);

    /* Print results */
    aliasing_print_result(&result);

    return 0;
}
```

### Real-time / Embedded Usage

```c
/* During initialization (non-real-time) */
aliasing_calculator_t calc;
aliasing_result_t result;

aliasing_calculator_init(&calc, 440.0f, 48000.0f, 8);
aliasing_calculate(&calc, 16, &result);

/* During real-time processing */
float nyquist = result.nyquist_freq;
if (input_freq > nyquist) {
    /* Frequency will alias */
    float aliased_freq;
    bool folded;
    aliasing_calculate_aliased_frequency(input_freq,
                                         result.decimated_sample_rate,
                                         &aliased_freq, &folded);
}
```

## API Reference

### Structures

#### `aliasing_calculator_t`
Calculator configuration (12 bytes):
- `float fundamental_freq` - Fundamental frequency in Hz
- `float sample_rate` - Sample rate in Hz
- `uint8_t num_partials` - Number of partials to analyze

#### `aliasing_result_t`
Calculation results (536 bytes with 32 max partials):
- `uint32_t decimation_rate` - Decimation factor
- `float original_sample_rate` - Original sample rate
- `float decimated_sample_rate` - Decimated sample rate
- `float nyquist_freq` - Nyquist frequency
- `float fundamental_freq` - Fundamental frequency
- `aliasing_partial_t partials[]` - Array of partial results
- `uint8_t num_partials` - Number of partials

#### `aliasing_partial_t`
Information about a single partial (16 bytes):
- `uint8_t partial_number` - Partial number (1-based)
- `float original_freq` - Original frequency
- `float aliased_freq` - Aliased frequency
- `bool folded` - True if folded around Nyquist

### Functions

#### `aliasing_calculator_init()`
Initialize calculator with parameters.

```c
int aliasing_calculator_init(
    aliasing_calculator_t *calc,
    float fundamental_freq,
    float sample_rate,
    uint8_t num_partials
);
```

**Returns:**
- `ALIASING_OK` (0) on success
- `ALIASING_ERR_NULL_PTR` if calc is NULL
- `ALIASING_ERR_INVALID` if parameters are invalid
- `ALIASING_ERR_TOO_MANY` if num_partials exceeds max

#### `aliasing_calculate()`
Calculate aliasing for a decimation rate.

```c
int aliasing_calculate(
    const aliasing_calculator_t *calc,
    uint32_t decimation_rate,
    aliasing_result_t *result
);
```

#### `aliasing_calculate_aliased_frequency()`
Calculate aliased frequency for a single frequency.

```c
void aliasing_calculate_aliased_frequency(
    float freq,
    float sample_rate,
    float *aliased_freq,
    bool *folded
);
```

#### Utility Functions
- `aliasing_get_aliased_frequencies()` - Extract aliased frequencies to array
- `aliasing_get_original_frequencies()` - Extract original frequencies to array
- `aliasing_count_folded()` - Count folded partials
- `aliasing_print_result()` - Print result to stdout (for debugging)

## Configuration

### Maximum Partials
Adjust the maximum number of partials by defining `ALIASING_MAX_PARTIALS` before including the header:

```c
#define ALIASING_MAX_PARTIALS 64
#include "aliasing_calc.h"
```

Default is 32 partials.

## Examples

Three complete examples are provided in `examples_c/`:

1. **basic_example.c** - Basic usage and multiple decimation rates
2. **subharmonic_example.c** - Finding subharmonic bass frequencies
3. **realtime_example.c** - Real-time/embedded usage patterns

Build and run all examples:
```bash
make run-all
```

## Memory Usage

With default configuration (32 max partials):
- Calculator: **12 bytes**
- Result: **536 bytes**
- Total stack usage: **~550 bytes**

Perfect for microcontrollers with limited RAM.

## Performance

On a modern CPU (x86_64):
- Single calculation: **< 1 microsecond**
- Search through 64 decimation rates: **< 50 microseconds**

Suitable for real-time audio processing even on modest embedded systems.

## Integration

### Embedded Systems
1. Copy `aliasing_calc.h` and `aliasing_calc.c` to your project
2. Add to your build system
3. Link with math library (-lm)
4. No other dependencies required

### Arduino/Platform IO
```cpp
extern "C" {
    #include "aliasing_calc.h"
}

void setup() {
    aliasing_calculator_t calc;
    aliasing_calculator_init(&calc, 440.0f, 48000.0f, 8);
    // ... use calculator
}
```

### Real-time Audio (JUCE, VST, etc.)
Pre-calculate during parameter changes, not in audio callback:

```c
void prepareToPlay(double sampleRate) {
    aliasing_calculator_init(&calc, 440.0f, (float)sampleRate, 8);
    aliasing_calculate(&calc, decimation_rate, &result);
}
```

## Error Handling

All functions return error codes or status:
- `ALIASING_OK` (0) - Success
- `ALIASING_ERR_NULL_PTR` (-1) - Null pointer argument
- `ALIASING_ERR_INVALID` (-2) - Invalid parameter
- `ALIASING_ERR_TOO_MANY` (-3) - Too many partials

Always check return values in production code.

## Thread Safety

The library is thread-safe as long as:
- Different threads use different calculator/result structures
- No concurrent writes to the same structures

No global state is used.

## License

MIT License - see LICENSE file
