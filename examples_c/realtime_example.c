/**
 * @file realtime_example.c
 * @brief Example showing real-time usage for embedded systems
 *
 * This example demonstrates how to use the aliasing calculator in a
 * real-time or embedded context with minimal memory footprint.
 */

#include "../c_impl/aliasing_calc.h"
#include <stdio.h>
#include <string.h>

/**
 * @brief Simulated audio configuration
 */
typedef struct {
    float sample_rate;
    uint32_t decimation_rate;
    float fundamental_freq;
} audio_config_t;

/**
 * @brief Pre-calculate aliasing information for audio processing
 *
 * In a real embedded system, you would call this during initialization
 * or when parameters change, not during real-time processing.
 */
void audio_init(const audio_config_t *config, aliasing_result_t *result) {
    aliasing_calculator_t calc;

    /* Initialize calculator */
    aliasing_calculator_init(
        &calc,
        config->fundamental_freq,
        config->sample_rate,
        8  /* Number of partials to track */
    );

    /* Pre-calculate aliasing */
    aliasing_calculate(&calc, config->decimation_rate, result);

    printf("Audio initialized:\n");
    printf("  Sample rate: %.0f Hz\n", config->sample_rate);
    printf("  Decimation: %ux\n", config->decimation_rate);
    printf("  Fundamental: %.2f Hz\n", config->fundamental_freq);
    printf("  Nyquist: %.2f Hz\n", result->nyquist_freq);
}

/**
 * @brief Simulate checking if a frequency will alias
 *
 * This could be used in real-time to determine if a generated
 * frequency will alias based on pre-calculated Nyquist.
 */
bool will_alias(float freq, float nyquist) {
    return freq > nyquist;
}

/**
 * @brief Get the aliased frequency for a given input
 *
 * Fast inline calculation suitable for real-time use
 */
float get_aliased_freq_fast(float freq, float sample_rate) {
    float nyquist = sample_rate / 2.0f;

    if (freq <= nyquist) {
        return freq;
    }

    float normalized = freq / nyquist;
    int quotient = (int)normalized;
    float remainder = normalized - (float)quotient;

    if (quotient % 2 == 1) {
        return nyquist * (1.0f - remainder);
    } else {
        return nyquist * remainder;
    }
}

int main(void) {
    audio_config_t config = {
        .sample_rate = 48000.0f,
        .decimation_rate = 16,
        .fundamental_freq = 440.0f
    };

    aliasing_result_t result;

    printf("==================================================\n");
    printf("Real-time / Embedded Usage Example\n");
    printf("==================================================\n\n");

    /* Initialization phase (not real-time) */
    audio_init(&config, &result);

    printf("\n\nReal-time phase - testing frequencies:\n");
    printf("--------------------------------------------------\n");

    /* Simulated real-time processing */
    float test_freqs[] = {440.0f, 880.0f, 1320.0f, 1760.0f, 2200.0f};

    for (int i = 0; i < 5; i++) {
        float freq = test_freqs[i];
        bool aliases = will_alias(freq, result.nyquist_freq);
        float aliased = get_aliased_freq_fast(freq, result.decimated_sample_rate);

        printf("Input: %.1f Hz -> ", freq);
        if (aliases) {
            printf("%.2f Hz [ALIASED]\n", aliased);
        } else {
            printf("%.2f Hz [CLEAN]\n", aliased);
        }
    }

    printf("\n\nMemory usage:\n");
    printf("--------------------------------------------------\n");
    printf("Calculator struct: %zu bytes\n", sizeof(aliasing_calculator_t));
    printf("Result struct: %zu bytes\n", sizeof(aliasing_result_t));
    printf("Partial struct: %zu bytes\n", sizeof(aliasing_partial_t));
    printf("Max partials: %d\n", ALIASING_MAX_PARTIALS);

    printf("\n\nChanging decimation rate (parameter update):\n");
    printf("--------------------------------------------------\n");

    /* Simulate parameter change */
    config.decimation_rate = 32;
    audio_init(&config, &result);

    printf("\nNew configuration active.\n");

    return 0;
}
