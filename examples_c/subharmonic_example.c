/**
 * @file subharmonic_example.c
 * @brief Example demonstrating subharmonic bass generation
 */

#include "../c_impl/aliasing_calc.h"
#include <stdio.h>

/**
 * @brief Find decimation rate that lowers fundamental the most
 */
uint32_t find_subharmonic_decimation(
    const aliasing_calculator_t *calc,
    uint32_t max_decimation
) {
    uint32_t best_decimation = 1;
    float lowest_freq = calc->fundamental_freq;

    for (uint32_t dec = 2; dec <= max_decimation; dec++) {
        aliasing_result_t result;

        if (aliasing_calculate(calc, dec, &result) == ALIASING_OK) {
            float aliased_fund = result.partials[0].aliased_freq;

            /* We want frequencies lower than original */
            if (aliased_fund < calc->fundamental_freq * 0.95f) {
                if (aliased_fund < lowest_freq) {
                    lowest_freq = aliased_fund;
                    best_decimation = dec;
                }
            }
        }
    }

    return best_decimation;
}

int main(void) {
    aliasing_calculator_t calc;
    aliasing_result_t result;

    printf("==================================================\n");
    printf("Subharmonic Bass Generator Example\n");
    printf("==================================================\n\n");

    /* Initialize for bass frequency - A2 (110 Hz) */
    aliasing_calculator_init(&calc, 110.0f, 48000.0f, 8);

    printf("Original frequency: %.2f Hz (A2)\n", calc.fundamental_freq);
    printf("Searching for subharmonic decimation rates...\n\n");

    /* Find best subharmonic decimation */
    uint32_t best_dec = find_subharmonic_decimation(&calc, 64);

    if (best_dec > 1) {
        aliasing_calculate(&calc, best_dec, &result);

        printf("Best decimation found: %ux\n", best_dec);
        printf("Fundamental: %.2f Hz -> %.2f Hz\n",
               calc.fundamental_freq,
               result.partials[0].aliased_freq);
        printf("Frequency drop: %.2f Hz\n",
               calc.fundamental_freq - result.partials[0].aliased_freq);
        printf("Ratio: %.3fx\n\n",
               result.partials[0].aliased_freq / calc.fundamental_freq);

        printf("Full spectrum:\n");
        aliasing_print_result(&result);
    } else {
        printf("No subharmonic decimation found in range 2-64\n");
    }

    printf("\n\nCompare with 440 Hz (A4):\n");
    printf("--------------------------------------------------\n");

    aliasing_calculator_init(&calc, 440.0f, 48000.0f, 8);
    best_dec = find_subharmonic_decimation(&calc, 64);

    if (best_dec > 1) {
        aliasing_calculate(&calc, best_dec, &result);

        printf("Best decimation: %ux\n", best_dec);
        printf("Fundamental: %.2f Hz -> %.2f Hz\n",
               calc.fundamental_freq,
               result.partials[0].aliased_freq);
        printf("Frequency drop: %.2f Hz\n",
               calc.fundamental_freq - result.partials[0].aliased_freq);
    }

    return 0;
}
