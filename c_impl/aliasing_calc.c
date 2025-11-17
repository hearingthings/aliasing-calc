/**
 * @file aliasing_calc.c
 * @brief Implementation of aliasing calculator
 */

#include "aliasing_calc.h"
#include <stdio.h>
#include <math.h>
#include <string.h>

int aliasing_calculator_init(
    aliasing_calculator_t *calc,
    float fundamental_freq,
    float sample_rate,
    uint8_t num_partials
) {
    if (calc == NULL) {
        return ALIASING_ERR_NULL_PTR;
    }

    if (fundamental_freq <= 0.0f || sample_rate <= 0.0f) {
        return ALIASING_ERR_INVALID;
    }

    if (num_partials == 0 || num_partials > ALIASING_MAX_PARTIALS) {
        return ALIASING_ERR_TOO_MANY;
    }

    calc->fundamental_freq = fundamental_freq;
    calc->sample_rate = sample_rate;
    calc->num_partials = num_partials;

    return ALIASING_OK;
}

void aliasing_calculate_aliased_frequency(
    float freq,
    float sample_rate,
    float *aliased_freq,
    bool *folded
) {
    float nyquist = sample_rate / 2.0f;

    if (freq <= nyquist) {
        *aliased_freq = freq;
        *folded = false;
        return;
    }

    /* Calculate how many times the frequency wraps around Nyquist */
    float normalized = freq / nyquist;
    int quotient = (int)normalized;
    float remainder = normalized - (float)quotient;

    if (quotient % 2 == 1) {
        /* Odd number of folds: frequency is reflected */
        *aliased_freq = nyquist * (1.0f - remainder);
    } else {
        /* Even number of folds: frequency wraps back up */
        *aliased_freq = nyquist * remainder;
    }

    *folded = true;
}

int aliasing_calculate(
    const aliasing_calculator_t *calc,
    uint32_t decimation_rate,
    aliasing_result_t *result
) {
    if (calc == NULL || result == NULL) {
        return ALIASING_ERR_NULL_PTR;
    }

    if (decimation_rate == 0) {
        return ALIASING_ERR_INVALID;
    }

    /* Clear result structure */
    memset(result, 0, sizeof(aliasing_result_t));

    /* Fill in basic info */
    result->decimation_rate = decimation_rate;
    result->original_sample_rate = calc->sample_rate;
    result->decimated_sample_rate = calc->sample_rate / (float)decimation_rate;
    result->nyquist_freq = result->decimated_sample_rate / 2.0f;
    result->fundamental_freq = calc->fundamental_freq;
    result->num_partials = calc->num_partials;

    /* Calculate aliasing for each partial */
    for (uint8_t i = 0; i < calc->num_partials; i++) {
        uint8_t partial_num = i + 1;
        float original_freq = calc->fundamental_freq * (float)partial_num;
        float aliased_freq;
        bool folded;

        aliasing_calculate_aliased_frequency(
            original_freq,
            result->decimated_sample_rate,
            &aliased_freq,
            &folded
        );

        result->partials[i].partial_number = partial_num;
        result->partials[i].original_freq = original_freq;
        result->partials[i].aliased_freq = aliased_freq;
        result->partials[i].folded = folded;
    }

    return ALIASING_OK;
}

uint8_t aliasing_get_aliased_frequencies(
    const aliasing_result_t *result,
    float *frequencies
) {
    if (result == NULL || frequencies == NULL) {
        return 0;
    }

    for (uint8_t i = 0; i < result->num_partials; i++) {
        frequencies[i] = result->partials[i].aliased_freq;
    }

    return result->num_partials;
}

uint8_t aliasing_get_original_frequencies(
    const aliasing_result_t *result,
    float *frequencies
) {
    if (result == NULL || frequencies == NULL) {
        return 0;
    }

    for (uint8_t i = 0; i < result->num_partials; i++) {
        frequencies[i] = result->partials[i].original_freq;
    }

    return result->num_partials;
}

uint8_t aliasing_count_folded(const aliasing_result_t *result) {
    if (result == NULL) {
        return 0;
    }

    uint8_t count = 0;
    for (uint8_t i = 0; i < result->num_partials; i++) {
        if (result->partials[i].folded) {
            count++;
        }
    }

    return count;
}

void aliasing_print_result(const aliasing_result_t *result) {
    if (result == NULL) {
        printf("Error: NULL result\n");
        return;
    }

    printf("Decimation Rate: %ux\n", (unsigned int)result->decimation_rate);
    printf("Sample Rate: %.0f Hz -> %.0f Hz\n",
           result->original_sample_rate,
           result->decimated_sample_rate);
    printf("Nyquist: %.2f Hz\n", result->nyquist_freq);
    printf("Fundamental: %.2f Hz\n\n", result->fundamental_freq);

    printf("Partials:\n");
    for (uint8_t i = 0; i < result->num_partials; i++) {
        const aliasing_partial_t *p = &result->partials[i];
        printf("  Partial %u: %.2f Hz -> %.2f Hz",
               p->partial_number,
               p->original_freq,
               p->aliased_freq);

        if (p->folded) {
            printf(" [FOLDED]");
        }
        printf("\n");
    }

    printf("\nFolded partials: %u/%u\n",
           aliasing_count_folded(result),
           result->num_partials);
}
