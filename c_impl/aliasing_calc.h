/**
 * @file aliasing_calc.h
 * @brief Aliasing calculator for audio decimation effects
 *
 * A lightweight C library for calculating aliasing effects when decimating
 * audio signals. Designed for embedded systems and real-time audio applications.
 *
 * @author Aliasing Calculator Contributors
 * @date 2025
 * @license MIT
 */

#ifndef ALIASING_CALC_H
#define ALIASING_CALC_H

#include <stdint.h>
#include <stdbool.h>

#ifdef __cplusplus
extern "C" {
#endif

/* Configuration - adjust for your needs */
#ifndef ALIASING_MAX_PARTIALS
#define ALIASING_MAX_PARTIALS 32  /**< Maximum number of partials to analyze */
#endif

/**
 * @brief Information about a single partial (harmonic component)
 */
typedef struct {
    uint8_t partial_number;    /**< Partial number (1-based) */
    float original_freq;       /**< Original frequency in Hz */
    float aliased_freq;        /**< Aliased frequency after decimation in Hz */
    bool folded;              /**< True if frequency folded around Nyquist */
} aliasing_partial_t;

/**
 * @brief Complete aliasing calculation result
 */
typedef struct {
    uint32_t decimation_rate;           /**< Decimation factor */
    float original_sample_rate;         /**< Original sample rate in Hz */
    float decimated_sample_rate;        /**< Decimated sample rate in Hz */
    float nyquist_freq;                 /**< Nyquist frequency in Hz */
    float fundamental_freq;             /**< Fundamental frequency in Hz */
    aliasing_partial_t partials[ALIASING_MAX_PARTIALS]; /**< Array of partials */
    uint8_t num_partials;              /**< Actual number of partials */
} aliasing_result_t;

/**
 * @brief Calculator configuration and state
 */
typedef struct {
    float fundamental_freq;    /**< Fundamental frequency in Hz */
    float sample_rate;        /**< Sample rate in Hz */
    uint8_t num_partials;     /**< Number of partials to analyze */
} aliasing_calculator_t;

/**
 * @brief Initialize an aliasing calculator
 *
 * @param calc Pointer to calculator structure to initialize
 * @param fundamental_freq Fundamental frequency in Hz (e.g., 440.0 for A4)
 * @param sample_rate Sample rate in Hz (e.g., 48000.0)
 * @param num_partials Number of partials to analyze (1 to ALIASING_MAX_PARTIALS)
 * @return 0 on success, negative error code on failure
 */
int aliasing_calculator_init(
    aliasing_calculator_t *calc,
    float fundamental_freq,
    float sample_rate,
    uint8_t num_partials
);

/**
 * @brief Calculate aliased frequency for a given frequency and sample rate
 *
 * This function computes where a frequency ends up after spectral folding
 * around the Nyquist frequency.
 *
 * @param freq Input frequency in Hz
 * @param sample_rate Sample rate in Hz
 * @param aliased_freq Output: aliased frequency in Hz
 * @param folded Output: true if frequency was above Nyquist and folded
 */
void aliasing_calculate_aliased_frequency(
    float freq,
    float sample_rate,
    float *aliased_freq,
    bool *folded
);

/**
 * @brief Calculate aliasing for a specific decimation rate
 *
 * @param calc Pointer to initialized calculator
 * @param decimation_rate Decimation factor (e.g., 2, 4, 8, 16)
 * @param result Pointer to result structure to fill
 * @return 0 on success, negative error code on failure
 */
int aliasing_calculate(
    const aliasing_calculator_t *calc,
    uint32_t decimation_rate,
    aliasing_result_t *result
);

/**
 * @brief Get array of aliased frequencies from result
 *
 * @param result Pointer to aliasing result
 * @param frequencies Output array (must be at least result->num_partials in size)
 * @return Number of frequencies written
 */
uint8_t aliasing_get_aliased_frequencies(
    const aliasing_result_t *result,
    float *frequencies
);

/**
 * @brief Get array of original frequencies from result
 *
 * @param result Pointer to aliasing result
 * @param frequencies Output array (must be at least result->num_partials in size)
 * @return Number of frequencies written
 */
uint8_t aliasing_get_original_frequencies(
    const aliasing_result_t *result,
    float *frequencies
);

/**
 * @brief Count how many partials were folded
 *
 * @param result Pointer to aliasing result
 * @return Number of folded partials
 */
uint8_t aliasing_count_folded(const aliasing_result_t *result);

/**
 * @brief Print aliasing result to stdout (useful for debugging)
 *
 * @param result Pointer to aliasing result to print
 */
void aliasing_print_result(const aliasing_result_t *result);

/* Error codes */
#define ALIASING_OK              0   /**< Success */
#define ALIASING_ERR_NULL_PTR   -1   /**< Null pointer argument */
#define ALIASING_ERR_INVALID    -2   /**< Invalid parameter value */
#define ALIASING_ERR_TOO_MANY   -3   /**< Too many partials requested */

#ifdef __cplusplus
}
#endif

#endif /* ALIASING_CALC_H */
