/*
 * SIMD Floating-Point Non-Associativity Demo
 * 
 * To compile and run on an x86/amd64 machine:
 *     g++ -O3 -msse3 simd_demo.cpp -o simd_demo
 *     ./simd_demo
 * 
 * Note: Ensure you use a capital 'O' in -O3 (optimization level 3), not a zero.
 */

#include <iostream>
#include <vector>
#include <iomanip>
#include <immintrin.h> // Header for SSE/AVX intrinsics

// Native Hardware SIMD Vector Accumulation
float hardware_simd_sum(float* arr, size_t size) {
    // Load 4 floats at a time into a 128-bit hardware SSE register
    // In our payload, this loads [1.0, 1.0, 1.0, 1.0] into a single register
    __m128 sum_vec = _mm_setzero_ps(); 
    for (size_t i = 1; i < size; i += 4) {
        __m128 data = _mm_loadu_ps(&arr[i]); // Force unaligned load
        sum_vec = _mm_add_ps(sum_vec, data); // Hardware parallel addition
    }

    // Now we must horizontally reduce the 4 accumulated lanes back into 1 scalar float.
    // _mm_hadd_ps does horizontal adds: [A+B, C+D, A+B, C+D]
    __m128 hsum = _mm_hadd_ps(sum_vec, sum_vec);
    hsum = _mm_hadd_ps(hsum, hsum);
    
    // Extract the final reduced sum (which is exactly 4.0)
    float tail_sum = _mm_cvtss_f32(hsum); 

    // Finally, add it back to the massive leading number that didn't fit in the SIMD batch
    return arr[0] + tail_sum; 
}

int main() {
    // We want to trigger an IEEE 754 precision loss scenario.
    // float32 mantissa holds 24 bits. 2^24 = 16777216.0f.
    // At this exact threshold, float32 cannot represent odd numbers.
    alignas(16) float nums[5] = {16777216.0f, 1.0f, 1.0f, 1.0f, 1.0f};
    
    // 1. Sequential Loop (Standard Scalar Addition)
    // 16777216.0 + 1.0 = 16777216.0 (The mantissa is too small; 1.0 is truncated)
    float seq_sum = 0.0f;
    for(int i=0; i < 5; i++) {
        seq_sum += nums[i];
    }
    
    // 2. Native Hardware SIMD Addition (SSE Horizontal Reduction)
    // The CPU adds the four 1.0s together *simultaneously* inside the 128-bit register
    // Because 1.0 + 1.0 + 1.0 + 1.0 = 4.0, it is large enough to survive addition to 16,777,216.
    float tree_sum = hardware_simd_sum(nums, 5);
    
    std::cout << std::fixed << std::setprecision(1);
    std::cout << "Sequential Sum:  " << seq_sum << " (Lost the +4.0 completely due to repeated mantissa truncation)" << std::endl;
    std::cout << "Native SIMD Sum: " << tree_sum << " (Successfully reduced the lanes to 4.0 first, preserving precision!)" << std::endl;
    std::cout << "Hardware Delta:  " << std::abs(seq_sum - tree_sum) << std::endl;
    return 0;
}
