/**
 * @file basic_example.c
 * @brief Basic example of using the aliasing calculator in C
 */

#include "../c_impl/aliasing_calc.h"
#include <stdio.h>

int main(void) {
    aliasing_calculator_t calc;
    aliasing_result_t result;
    int ret;

    printf("==================================================\n");
    printf("Aliasing Calculator - Basic Example\n");
    printf("==================================================\n\n");

    /* Initialize calculator for A4 (440 Hz) with 8 partials */
    ret = aliasing_calculator_init(&calc, 440.0f, 48000.0f, 8);
    if (ret != ALIASING_OK) {
        fprintf(stderr, "Error initializing calculator: %d\n", ret);
        return 1;
    }

    printf("Example 1: Calculate aliasing at 16x decimation\n");
    printf("--------------------------------------------------\n");

    ret = aliasing_calculate(&calc, 16, &result);
    if (ret != ALIASING_OK) {
        fprintf(stderr, "Error calculating aliasing: %d\n", ret);
        return 1;
    }

    aliasing_print_result(&result);

    printf("\n\nExample 2: Compare different decimation rates\n");
    printf("--------------------------------------------------\n");

    uint32_t decimations[] = {2, 4, 8, 16, 32};
    printf("\nDec    Fund(Hz)   Folded    SR(Hz)\n");
    printf("-------------------------------------------\n");

    for (int i = 0; i < 5; i++) {
        ret = aliasing_calculate(&calc, decimations[i], &result);
        if (ret == ALIASING_OK) {
            printf("%-6ux %-10.2f %u/%-6u  %.0f\n",
                   decimations[i],
                   result.partials[0].aliased_freq,
                   aliasing_count_folded(&result),
                   result.num_partials,
                   result.decimated_sample_rate);
        }
    }

    printf("\n\nExample 3: Extract aliased frequencies\n");
    printf("--------------------------------------------------\n");

    /* Calculate at 24x decimation */
    ret = aliasing_calculate(&calc, 24, &result);
    if (ret == ALIASING_OK) {
        float aliased_freqs[ALIASING_MAX_PARTIALS];
        uint8_t count = aliasing_get_aliased_frequencies(&result, aliased_freqs);

        printf("Decimation: %ux\n", result.decimation_rate);
        printf("Aliased frequencies:\n");
        for (uint8_t i = 0; i < count; i++) {
            printf("  %.2f Hz", aliased_freqs[i]);
            if ((i + 1) % 4 == 0) printf("\n");
        }
        printf("\n");
    }

    return 0;
}
