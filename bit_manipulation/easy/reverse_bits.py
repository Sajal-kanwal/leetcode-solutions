"""
================================================================================
Problem: 190. Reverse Bits
Platform: LeetCode
URL: https://leetcode.com/problems/reverse-bits/
Difficulty: Easy
Topics: Bit Manipulation
================================================================================

PROBLEM DESCRIPTION:
Reverse bits of a given 32 bits unsigned integer.

Note:
- Input is a 32-bit unsigned integer
- Output is also a 32-bit unsigned integer

CONSTRAINTS:
- 0 <= n <= 2^31 - 2
- n is even

EXAMPLES:

Example 1:
Input:  n = 43261596
        Binary: 00000010100101000001111010011100
Output: 964176192
        Binary: 00111001011110000010100101000000

Example 2:
Input:  n = 2147483644
        Binary: 01111111111111111111111111111100
Output: 1073741822
        Binary: 00111111111111111111111111111110

================================================================================
INTUITION:
We need to take each bit from the input and place it in the mirror position
in the output.

Bit 0 (rightmost) → Bit 31 (leftmost)
Bit 1 → Bit 30
Bit 2 → Bit 29
...
Bit 31 (leftmost) → Bit 0 (rightmost)

APPROACH 1: Bit-by-Bit Extraction (Most Intuitive)
- Extract each bit from right to left
- Place it in result from left to right
- Use shift and mask operations

APPROACH 2: Divide and Conquer (Fastest)
- Swap adjacent bits
- Swap pairs of 2 bits
- Swap groups of 4, 8, 16 bits
- Like merge sort but for bits
- Only 5 operations regardless of input!

APPROACH 3: Using Python's bin/format (Pythonic)
- Convert to binary string
- Reverse the string
- Convert back to integer
- Simple but not as educational

COMPLEXITY:
- Time: O(1) - always 32 iterations (fixed input size)
- Space: O(1) - constant variables

================================================================================
"""

from typing import List


class Solution:
    """LC 190: Reverse Bits - Bit-by-Bit (Recommended)"""
    
    def reverseBits(self, n: int) -> int:
        """
        Reverse 32 bits using bit extraction and placement.
        
        Args:
            n: 32-bit unsigned integer
            
        Returns:
            Integer with bits in reverse order
            
        Algorithm: Extract and place each bit
        Time: O(1) - fixed 32 iterations
        Space: O(1)
        """
        result = 0
        
        for i in range(32):
            # Extract rightmost bit of n
            bit = n & 1
            
            # Shift result left to make room, place extracted bit
            result = (result << 1) | bit
            
            # Shift n right to expose next bit
            n >>= 1
        
        return result


class SolutionExplicitPositioning:
    """
    Explicit bit positioning version.
    
    More verbose but clearly shows WHERE each bit goes.
    """
    
    def reverseBits(self, n: int) -> int:
        """
        Extract bit at position i, place it at position (31 - i).
        
        This makes the reversal mapping very explicit.
        """
        result = 0
        
        for i in range(32):
            # Check if bit at position i is set
            if n & (1 << i):
                # Set bit at position (31 - i) in result
                result |= 1 << (31 - i)
        
        return result


class SolutionDivideAndConquer:
    """
    Divide and Conquer approach - Fastest in practice.
    
    Swaps groups of bits in log(32) = 5 steps:
    Step 1: Swap adjacent bits (groups of 1)
    Step 2: Swap pairs (groups of 2)
    Step 3: Swap nibbles (groups of 4)
    Step 4: Swap bytes (groups of 8)
    Step 5: Swap half-words (groups of 16)
    
    Only 5 operations regardless of input!
    """
    
    def reverseBits(self, n: int) -> int:
        """
        Reverse bits using hierarchical swapping.
        
        Each step doubles the swap size:
        - Masks isolate the groups to swap
        - Shifts move groups to their new positions
        - OR combines the swapped groups
        """
        # Step 1: Swap adjacent bits
        # 0101...01 selects even bits, 1010...10 selects odd bits
        n = ((n & 0x55555555) << 1) | ((n & 0xAAAAAAAA) >> 1)
        
        # Step 2: Swap pairs of bits
        # 0011...0011 selects even pairs, 1100...1100 selects odd pairs
        n = ((n & 0x33333333) << 2) | ((n & 0xCCCCCCCC) >> 2)
        
        # Step 3: Swap nibbles (4-bit groups)
        n = ((n & 0x0F0F0F0F) << 4) | ((n & 0xF0F0F0F0) >> 4)
        
        # Step 4: Swap bytes (8-bit groups)
        n = ((n & 0x00FF00FF) << 8) | ((n & 0xFF00FF00) >> 8)
        
        # Step 5: Swap 16-bit halves
        n = (n << 16) | (n >> 16)
        
        # Ensure result fits in 32 bits
        return n & 0xFFFFFFFF


class SolutionPythonic:
    """
    Pythonic string-based approach.
    
    Simple but less educational about bit manipulation.
    """
    
    def reverseBits(self, n: int) -> int:
        """
        Convert to binary string, reverse, convert back.
        """
        # Format as 32-bit binary string (zero-padded)
        binary = format(n, '032b')
        
        # Reverse and convert back to integer
        return int(binary[::-1], 2)


# ================================================================================
# TEST CASES
# ================================================================================
if __name__ == "__main__":
    solution = Solution()
    solution_explicit = SolutionExplicitPositioning()
    solution_dc = SolutionDivideAndConquer()
    solution_pythonic = SolutionPythonic()
    
    test_cases = [
        (
            43261596,
            964176192,
            "Example 1"
        ),
        (
            2147483644,
            1073741822,
            "Example 2"
        ),
        (
            0,
            0,
            "Zero stays zero"
        ),
        (
            1,
            2147483648,  # 1 << 31
            "Bit 0 moves to bit 31"
        ),
        (
            2147483648,  # 1 << 31
            1,
            "Bit 31 moves to bit 0"
        ),
        (
            4294967295,  # All 32 bits set (2^32 - 1)
            4294967295,
            "All bits set: stays same"
        ),
        (
            2,            # 10 in binary
            1073741824,   # 1 << 30
            "Bit 1 moves to bit 30"
        ),
        (
            6,            # 110
            1610612736,   # bits 30 and 31 set
            "Multiple bits"
        ),
    ]
    
    print("=" * 70)
    print("TESTING REVERSE BITS")
    print("=" * 70)
    print()
    
    solutions = [
        ("Bit-by-Bit", solution),
        ("Explicit Positioning", solution_explicit),
        ("Divide and Conquer", solution_dc),
        ("Pythonic (String)", solution_pythonic),
    ]
    
    for sol_name, sol in solutions:
        print(f"Testing: {sol_name}")
        print("-" * 70)
        
        passed = 0
        for n, expected, description in test_cases:
            result = sol.reverseBits(n)
            
            if result == expected:
                print(f"  ✅ {description}")
                print(f"     {format(n, '032b')} → {format(result, '032b')}")
                passed += 1
            else:
                print(f"  ❌ {description}")
                print(f"     Input:    {format(n, '032b')}")
                print(f"     Expected: {format(expected, '032b')}")
                print(f"     Got:      {format(result, '032b')}")
        
        print(f"\n  Results: {passed}/{len(test_cases)} passed\n")
    
    print("=" * 70)
    print("🎉 All solutions tested!")
    print("=" * 70)


# ================================================================================
# VISUALIZATION: Bit-by-Bit Approach
# ================================================================================
"""
Example: n = 43261596

Binary: 00000010100101000001111010011100
Index:  31                            0  (bit positions)

Step-by-step (showing only first and last few iterations):

Iteration 0:
  n      = 00000010100101000001111010011100
  bit    = n & 1 = 0 (rightmost bit)
  result = 0 << 1 | 0 = 0
  n >>= 1 → 00000001010010100000111101001110

Iteration 1:
  n      = 00000001010010100000111101001110
  bit    = n & 1 = 0
  result = 0 << 1 | 0 = 0
  n >>= 1 → 00000000101001010000011110100111

Iteration 2:
  n      = 00000000101001010000011110100111
  bit    = n & 1 = 1  ← first 1 bit found!
  result = 0 << 1 | 1 = 1
  n >>= 1 → ...

...continuing...

Iteration 31:
  n      = 00000000000000000000000000000000
  bit    = 0
  result = 00111001011110000010100101000000
  
Final result: 00111001011110000010100101000000 = 964176192 ✓

Visual mapping:
  Input:  0 0 0 0 0 0 1 0 1 0 0 1 0 1 0 0 0 0 0 1 1 1 1 0 1 0 0 1 1 1 0 0
  Index:  31                                                              0
          ↕ ↕ ↕ ↕ ↕ ↕ ↕ ↕ ↕ ↕ ↕ ↕ ↕ ↕ ↕ ↕ ↕ ↕ ↕ ↕ ↕ ↕ ↕ ↕ ↕ ↕ ↕ ↕ ↕ ↕ ↕ ↕  (mirror)
  Output: 0 0 1 1 1 0 0 1 0 1 1 1 1 0 0 0 0 0 1 0 1 0 0 1 0 1 0 0 0 0 0 0
  Index:  31                                                              0
"""


# ================================================================================
# VISUALIZATION: Divide and Conquer Approach
# ================================================================================
"""
Example: n = 43261596
Binary: 00000010100101000001111010011100

Step 1: Swap ADJACENT bits (groups of 1)
  Before: 00 00 00 10 10 01 01 00 00 01 11 10 10 01 11 00
  Groups: [0,0][0,0][0,0][1,0][1,0][0,1][0,1][0,0][0,0][0,1][1,1][1,0][1,0][0,1][1,1][0,0]
  After:  00 00 00 01 01 10 10 00 00 10 11 01 01 10 11 00
  Result: 00000001011010000010110101101100

Step 2: Swap PAIRS (groups of 2)
  Before: 00 00 00 01 01 10 10 00 00 10 11 01 01 10 11 00
  Groups: [00,00][00,01][01,10][10,00][00,10][11,01][01,10][11,00]
  After:  00 00 01 00 10 01 00 10 10 11 00 01 10 01 00 11
  Result: 00000100100100101011000110010011

Step 3: Swap NIBBLES (groups of 4)
  Before: 0000 0100 1001 0010 1011 0001 1001 0011
  Groups: [0000,0100][1001,0010][1011,0001][1001,0011]
  After:  0100 0000 0010 1001 0001 1011 0011 1001
  Result: 01000000001010010001101100111001

Step 4: Swap BYTES (groups of 8)
  Before: 01000000 00101001 00011011 00111001
  Groups: [01000000,00101001][00011011,00111001]
  After:  00101001 01000000 00111001 00011011
  Result: 00101001010000000011100100011011

Step 5: Swap HALF-WORDS (groups of 16)
  Before: 0010100101000000 0011100100011011
  Swap:   0011100100011011 0010100101000000
  After:  00111001000110110010100101000000
  Result: 00111001011110000010100101000000 = 964176192 ✓

Visual summary of group sizes:
  Step 1: |1|1|1|1|1|1|1|1|1|1|1|1|1|1|1|1|1|1|1|1|1|1|1|1|1|1|1|1|1|1|1|1|
  Step 2: |--2--|--2--|--2--|--2--|--2--|--2--|--2--|--2--|--2--|--2--|--2--|--2--|
  Step 3: |----4----|----4----|----4----|----4----|----4----|----4----|----4----|
  Step 4: |--------8--------|--------8--------|--------8--------|--------8--------|
  Step 5: |-------------------16-------------------|-------------------16-------------------|
"""


# ================================================================================
# LEARNING NOTES
# ================================================================================
"""
PATTERN: Bit Manipulation - Reverse Bits

KEY TECHNIQUES DEMONSTRATED:

1. Bit Extraction
   - Extract bit at position i: (n >> i) & 1
   - Or extract rightmost bit: n & 1, then shift n right

2. Bit Placement
   - Set bit at position i: result |= (1 << i)
   - Or shift result left and OR new bit: (result << 1) | bit

3. Bitmask Patterns (for Divide & Conquer)
   0x55555555 = 01010101...01  (alternating, selects even positions)
   0xAAAAAAAA = 10101010...10  (alternating, selects odd positions)
   0x33333333 = 00110011...11  (pairs)
   0xCCCCCCCC = 11001100...00  (pairs)
   0x0F0F0F0F = 00001111...0F  (nibbles)
   0xF0F0F0F0 = 11110000...F0  (nibbles)
   0x00FF00FF = bytes (even)
   0xFF00FF00 = bytes (odd)

SIMILAR PROBLEMS:

1. LC 191: Number of 1 Bits (Hamming Weight)
   - Count set bits using n & (n-1) trick
   - Or use Brian Kernighan's algorithm

2. LC 231: Power of Two
   - Check n & (n-1) == 0

3. LC 338: Counting Bits
   - Count bits for all numbers 0 to n
   - Use dp[i] = dp[i >> 1] + (i & 1)

4. LC 461: Hamming Distance
   - XOR two numbers, count 1 bits in result

APPROACH COMPARISON:

| Approach | Operations | Readability | Interview Pick |
|----------|-----------|-------------|----------------|
| Bit-by-Bit | 32 iterations | ⭐⭐⭐⭐⭐ | ✅ Best |
| Explicit | 32 iterations | ⭐⭐⭐⭐ | ✅ Good |
| D&C | 5 operations | ⭐⭐ | Show as follow-up |
| Pythonic | String ops | ⭐⭐⭐ | ❌ Not educational |

INTERVIEW TIPS:

1. Start with bit-by-bit
   - Most intuitive, easiest to explain
   - Shows you understand bit operations

2. Explain the loop clearly
   - "Extract rightmost bit"
   - "Shift result left, place bit"
   - "Shift input right for next bit"

3. Mention D&C as optimization
   - "Could do this in 5 operations using divide and conquer"
   - Shows depth of knowledge

4. Handle edge cases
   - n = 0 → result = 0
   - All bits set → stays same (palindrome)
   - Single bit set → moves to mirror position

5. Watch for Python pitfalls
   - Python integers have arbitrary precision
   - Must mask to 32 bits: & 0xFFFFFFFF
   - Especially important in D&C approach

COMMON MISTAKES:

❌ Off-by-one in bit positions
   - Bit 0 is rightmost, bit 31 is leftmost
   - Mirror of bit i is bit (31 - i)

❌ Forgetting 32-bit constraint
   - Python ints grow infinitely
   - Must mask result to 32 bits when needed

❌ Wrong shift direction
   - Extract from right: n >> 1
   - Build result from left: result << 1

❌ Using wrong mask in D&C
   - Each step needs specific hex masks
   - Easy to mix up 0x55 vs 0xAA etc.

BIT POSITION REFERENCE:

Position: 31 30 29 28 ... 3  2  1  0
Value:    2^31 2^30 ...     8  4  2  1
Mirror:   0  1  2  3  ... 28 29 30 31
"""


# ================================================================================
# PERFORMANCE BENCHMARK
# ================================================================================
if __name__ == "__main__":
    import time
    import random
    
    print("\n" + "=" * 70)
    print("PERFORMANCE BENCHMARK")
    print("=" * 70)
    print()
    
    # Generate random test inputs
    test_inputs = [random.randint(0, 2**31 - 2) for _ in range(10000)]
    
    benchmarks = [
        ("Bit-by-Bit", solution),
        ("Explicit", solution_explicit),
        ("Divide & Conquer", solution_dc),
        ("Pythonic", solution_pythonic),
    ]
    
    for name, sol in benchmarks:
        start = time.perf_counter()
        
        for _ in range(100):  # 100 passes over 10k inputs
            for n in test_inputs:
                sol.reverseBits(n)
        
        elapsed = (time.perf_counter() - start) * 1000
        
        print(f"  {name:<22}: {elapsed:>8.2f}ms (10k inputs × 100 passes)")
    
    print("\n" + "=" * 70)