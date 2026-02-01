"""
================================================================================
Problem: 191. Number of 1 Bits (Hamming Weight)
Platform: LeetCode
URL: https://leetcode.com/problems/number-of-1-bits/
Difficulty: Easy
Topics: Bit Manipulation
================================================================================

PROBLEM DESCRIPTION:
Given a positive integer n, write a function that returns the number of set 
bits in its binary representation (also known as the Hamming weight).

CONSTRAINTS:
- 1 <= n <= 2^31 - 1

EXAMPLES:

Example 1:
Input: n = 11
Output: 3
Explanation: Binary 1011 has three set bits.

Example 2:
Input: n = 128
Output: 1
Explanation: Binary 10000000 has one set bit.

Example 3:
Input: n = 2147483645
Output: 30
Explanation: Binary 1111111111111111111111111111101 has thirty set bits.

================================================================================
INTUITION:
We need to count how many 1s exist in the binary representation.

Three core strategies:

1. CHECK EACH BIT (Brute Force)
   - Check all 32 bits one by one
   - Always exactly 32 iterations

2. BRIAN KERNIGHAN'S ALGORITHM (Optimal)
   - Key trick: n & (n-1) removes the lowest set bit
   - Only iterates as many times as there are 1 bits
   - If answer is 3, only 3 iterations!

3. LOOKUP TABLE (Best for repeated calls)
   - Precompute bit counts for all 8-bit values (0-255)
   - Split 32-bit number into four 8-bit chunks
   - Look up each chunk's count

WHY n & (n-1) WORKS:
  n     = ...1 0 0 0  (some pattern ending in lowest set bit)
  n - 1 = ...0 1 1 1  (flips lowest set bit and all bits below it)
  n & (n-1) = ...0 0 0 0  (lowest set bit is cleared, everything else stays)

Example:
  n     = 1 0 1 1 0 0  (44 in decimal)
  n - 1 = 1 0 1 0 1 1  (43)
  n&(n-1)= 1 0 1 0 0 0  (40) — cleared the lowest set bit (bit 2)

COMPLEXITY:
- Brute force: O(1) time (always 32 iterations), O(1) space
- Kernighan's: O(1) time (at most 32 iterations, often fewer), O(1) space
- Lookup table: O(1) time (4 lookups), O(1) space (256 entry table)

================================================================================
"""


class Solution:
    """LC 191: Number of 1 Bits - Brian Kernighan's Algorithm (Optimal)"""
    
    def hammingWeight(self, n: int) -> int:
        """
        Count set bits using Brian Kernighan's trick.
        
        Each iteration removes exactly one set bit.
        Loop runs exactly (number of set bits) times.
        
        Args:
            n: Positive 32-bit integer
            
        Returns:
            Number of 1 bits in binary representation
            
        Algorithm: Brian Kernighan's
        Time: O(1) — at most 32 iterations
        Space: O(1)
        """
        count = 0
        
        while n:
            # Clear the lowest set bit
            n &= n - 1
            count += 1
        
        return count


class SolutionCheckEachBit:
    """Check each of the 32 bits individually"""
    
    def hammingWeight(self, n: int) -> int:
        """
        Check every bit position from 0 to 31.
        
        Always runs exactly 32 iterations regardless of input.
        """
        count = 0
        
        for i in range(32):
            # Check if bit at position i is set
            if n & (1 << i):
                count += 1
        
        return count


class SolutionShiftAndMask:
    """Shift right and check LSB each time"""
    
    def hammingWeight(self, n: int) -> int:
        """
        Shift n right each iteration, check if rightmost bit is 1.
        
        Equivalent to CheckEachBit but shifts input instead of mask.
        """
        count = 0
        
        while n:
            # Check rightmost bit
            count += n & 1
            # Shift right to expose next bit
            n >>= 1
        
        return count


class SolutionLookupTable:
    """
    Lookup table approach — best for repeated calls.
    
    Precomputes bit counts for all 8-bit values (0 to 255).
    Then splits any 32-bit number into four 8-bit chunks
    and sums up their precomputed counts.
    """
    
    def __init__(self):
        # Build lookup table for all 8-bit values
        # table[i] = number of 1 bits in i (for 0 <= i <= 255)
        self.table = [0] * 256
        
        for i in range(1, 256):
            # Use Kernighan's trick to build the table
            # Or simply: table[i] = table[i >> 1] + (i & 1)
            self.table[i] = self.table[i >> 1] + (i & 1)
    
    def hammingWeight(self, n: int) -> int:
        """
        Split 32-bit number into four bytes, look up each count.
        
        Only 4 operations regardless of how many bits are set!
        
        Byte layout (32 bits):
        [byte3: bits 24-31] [byte2: bits 16-23] [byte1: bits 8-15] [byte0: bits 0-7]
        """
        return (
            self.table[n & 0xFF] +            # Bits 0-7
            self.table[(n >> 8) & 0xFF] +     # Bits 8-15
            self.table[(n >> 16) & 0xFF] +    # Bits 16-23
            self.table[(n >> 24) & 0xFF]      # Bits 24-31
        )


class SolutionPythonic:
    """Python one-liner using bin()"""
    
    def hammingWeight(self, n: int) -> int:
        """
        bin(n) converts to binary string like '0b1011'.
        count('1') counts the 1 characters.
        
        Simple but not educational about bit manipulation.
        """
        return bin(n).count('1')


# ================================================================================
# TEST CASES
# ================================================================================
if __name__ == "__main__":
    solution = Solution()
    solution_check = SolutionCheckEachBit()
    solution_shift = SolutionShiftAndMask()
    solution_table = SolutionLookupTable()
    solution_py = SolutionPythonic()
    
    test_cases = [
        (
            11,
            3,
            "Example 1: 1011"
        ),
        (
            128,
            1,
            "Example 2: 10000000"
        ),
        (
            2147483645,
            30,
            "Example 3: 30 bits set"
        ),
        (
            1,
            1,
            "Single bit: 1"
        ),
        (
            2147483647,  # 2^31 - 1
            31,
            "Max value: all 31 bits set"
        ),
        (
            1073741824,  # 2^30
            1,
            "Power of 2: single bit"
        ),
        (
            7,
            3,
            "111 in binary"
        ),
        (
            255,
            8,
            "11111111: full byte"
        ),
        (
            256,
            1,
            "100000000: just above full byte"
        ),
        (
            1431655765,  # 0x55555555 = 01010101...
            16,
            "Alternating bits: 16 ones"
        ),
    ]
    
    print("=" * 70)
    print("TESTING NUMBER OF 1 BITS")
    print("=" * 70)
    print()
    
    solutions = [
        ("Kernighan's", solution),
        ("Check Each Bit", solution_check),
        ("Shift & Mask", solution_shift),
        ("Lookup Table", solution_table),
        ("Pythonic", solution_py),
    ]
    
    for sol_name, sol in solutions:
        print(f"Testing: {sol_name}")
        print("-" * 70)
        
        passed = 0
        for n, expected, description in test_cases:
            result = sol.hammingWeight(n)
            
            if result == expected:
                print(f"  ✅ {description}: {format(n, '032b')} → {result}")
                passed += 1
            else:
                print(f"  ❌ {description}")
                print(f"     Input:    {format(n, '032b')}")
                print(f"     Expected: {expected}, Got: {result}")
        
        print(f"\n  Results: {passed}/{len(test_cases)} passed\n")
    
    print("=" * 70)
    print("🎉 All solutions tested!")
    print("=" * 70)


# ================================================================================
# VISUALIZATION: Brian Kernighan's Algorithm
# ================================================================================
"""
Example: n = 11 (binary: 1011)

Kernighan's trick: n & (n-1) clears the lowest set bit

Iteration 1:
  n     =  1 0 1 1
  n - 1 =  1 0 1 0
  n&(n-1)= 1 0 1 0   → cleared bit 0
  count = 1

Iteration 2:
  n     =  1 0 1 0
  n - 1 =  1 0 0 1
  n&(n-1)= 1 0 0 0   → cleared bit 1
  count = 2

Iteration 3:
  n     =  1 0 0 0
  n - 1 =  0 1 1 1
  n&(n-1)= 0 0 0 0   → cleared bit 3
  count = 3

n = 0, loop exits.
Answer: 3 ✓

═══════════════════════════════════════════════════════════════
WHY n & (n-1) CLEARS THE LOWEST SET BIT:
═══════════════════════════════════════════════════════════════

Consider any number n with lowest set bit at position k:

  n   = X X X X 1 0 0 0   ← bit k is the lowest set bit
                ↑
          position k

  n-1 = X X X X 0 1 1 1   ← subtracting 1 flips bit k
                            and sets all bits below k

  n & (n-1):
        X X X X 1 0 0 0
      & X X X X 0 1 1 1
      = X X X X 0 0 0 0   ← bit k cleared, bits below unchanged (were 0)
                            ← bits above k unchanged (same in both)

═══════════════════════════════════════════════════════════════
LARGER EXAMPLE: n = 44 (binary: 101100)
═══════════════════════════════════════════════════════════════

Iteration 1:
  n     = 1 0 1 1 0 0
  n - 1 = 1 0 1 0 1 1
  n&(n-1)= 1 0 1 0 0 0   → cleared bit 2 (lowest set bit)
  count = 1

Iteration 2:
  n     = 1 0 1 0 0 0
  n - 1 = 1 0 0 1 1 1
  n&(n-1)= 1 0 0 0 0 0   → cleared bit 3
  count = 2

Iteration 3:
  n     = 1 0 0 0 0 0
  n - 1 = 0 1 1 1 1 1
  n&(n-1)= 0 0 0 0 0 0   → cleared bit 5
  count = 3

Answer: 3 ✓ (44 = 101100, three 1-bits)
"""


# ================================================================================
# VISUALIZATION: Lookup Table Approach
# ================================================================================
"""
32-bit number split into four 8-bit bytes:

n = 1431655765
Binary: 01010101 01010101 01010101 01010101
        ^^^^^^^^ ^^^^^^^^ ^^^^^^^^ ^^^^^^^^
        byte 3   byte 2   byte 1   byte 0

Lookup table (first 16 entries):
  table[0]   = 0    (00000000)
  table[1]   = 1    (00000001)
  table[2]   = 1    (00000010)
  table[3]   = 2    (00000011)
  table[4]   = 1    (00000100)
  table[5]   = 2    (00000101)
  ...
  table[85]  = 4    (01010101) ← this is 0x55
  ...
  table[255] = 8    (11111111)

Computing hamming weight:
  byte 0 = 01010101 = 85  → table[85] = 4
  byte 1 = 01010101 = 85  → table[85] = 4
  byte 2 = 01010101 = 85  → table[85] = 4
  byte 3 = 01010101 = 85  → table[85] = 4

  Total = 4 + 4 + 4 + 4 = 16 ✓

Building the table with DP:
  table[i] = table[i >> 1] + (i & 1)

  Why?
  - i >> 1 removes the last bit (same count as i without last bit)
  - i & 1 adds 1 if last bit is set, 0 otherwise
  
  Example: table[11] where 11 = 1011
  - table[11] = table[5] + (11 & 1)
  - table[5]  = table[2] + (5 & 1)  = 1 + 1 = 2
  - table[11] = 2 + 1 = 3  ✓ (1011 has three 1s)
"""


# ================================================================================
# LEARNING NOTES
# ================================================================================
"""
PATTERN: Bit Counting — Multiple Approaches

This problem teaches three distinct bit manipulation techniques.
Knowing all three shows depth in interviews.

═══════════════════════════════════════════════════════════════
BRIAN KERNIGHAN'S ALGORITHM — THE STAR
═══════════════════════════════════════════════════════════════

The key insight: n & (n-1) removes exactly the lowest set bit.

Use this trick whenever you see:
- "Count set bits"
- "Is n a power of 2?" → n & (n-1) == 0 (only one bit set)
- "Remove lowest set bit"
- Any problem where iterating over SET bits is needed

Related trick: n & (-n) isolates the lowest set bit
  n   =  1 0 1 1 0 0
  -n  =  0 1 0 1 0 0  (two's complement)
  n&-n=  0 0 0 1 0 0  ← just the lowest set bit

═══════════════════════════════════════════════════════════════
FOLLOW-UP: "If called many times, how to optimize?"
═══════════════════════════════════════════════════════════════

This is the classic follow-up for this problem.

Answer: Lookup Table

Why it's better for repeated calls:
- Precompute once: O(256) — negligible
- Each call: exactly 4 table lookups — O(1)
- No loops, no conditionals in the hot path
- CPU cache friendly (256-entry table fits in L1 cache)

Even better: 16-bit lookup table
- table size: 65536 entries
- Each call: only 2 lookups
- Trade more memory for fewer operations

In production systems:
- Many CPUs have a POPCNT instruction
- Does this in single clock cycle
- Python's bin(n).count('1') may use this under the hood

═══════════════════════════════════════════════════════════════
RELATED PROBLEMS
═══════════════════════════════════════════════════════════════

1. LC 136: Single Number
   - XOR all elements, pairs cancel

2. LC 190: Reverse Bits
   - Shift and place each bit in mirror position

3. LC 231: Power of Two
   - n > 0 and n & (n-1) == 0

4. LC 338: Counting Bits
   - Count bits for ALL numbers 0 to n
   - DP: dp[i] = dp[i >> 1] + (i & 1)
   - Same recurrence used to build lookup table!

5. LC 461: Hamming Distance
   - XOR two numbers, count 1 bits in result
   - Combines LC 136 pattern with this problem

6. LC 1356: Sort Integers by Number of 1 Bits
   - Sort array by hamming weight
   - Use this function as sort key

═══════════════════════════════════════════════════════════════
APPROACH COMPARISON
═══════════════════════════════════════════════════════════════

| Approach | Iterations | Best Case | Worst Case | Repeated Calls |
|----------|-----------|-----------|------------|----------------|
| Kernighan's | = popcount | 1 | 32 | Good |
| Check Each Bit | 32 always | 32 | 32 | OK |
| Shift & Mask | = bit length | 1 | 32 | OK |
| Lookup Table | 4 always | 4 | 4 | Best |
| Pythonic | internal | - | - | Depends |

Pick for interview: Kernighan's (shows knowledge, elegant)
Pick for production: Lookup Table (consistent, fast)

═══════════════════════════════════════════════════════════════
COMMON MISTAKES
═══════════════════════════════════════════════════════════════

❌ Using n % 2 instead of n & 1
   - Both work but & is idiomatic for bit manipulation

❌ Forgetting while n (using for i in range(32) with Kernighan's)
   - Kernighan's loop condition is while n != 0
   - Exits early when all bits are cleared

❌ Off-by-one in lookup table size
   - 8-bit table needs 256 entries (0 to 255)
   - 16-bit table needs 65536 entries

❌ Not handling n=0
   - Kernighan's handles it naturally (loop doesn't execute)
   - Check each bit handles it (all checks fail)

═══════════════════════════════════════════════════════════════
INTERVIEW TIPS
═══════════════════════════════════════════════════════════════

1. Start with Kernighan's
   - Most impressive, shows deep understanding
   - Explain the n & (n-1) trick clearly

2. Walk through the example
   - Show binary at each step
   - Highlight which bit gets cleared

3. Answer the follow-up
   - "For repeated calls, use a lookup table"
   - Explain the byte-splitting approach
   - Mention trade-off: memory vs speed

4. Connect to other problems
   - "This trick also checks power of 2"
   - "Combined with XOR, solves Hamming Distance"

5. Mention hardware
   - "Modern CPUs have POPCNT instruction for this"
   - Shows awareness of systems-level optimization
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
    
    # Generate test inputs — mix of sparse and dense bit patterns
    test_inputs = [random.randint(1, 2**31 - 1) for _ in range(50000)]
    
    benchmarks = [
        ("Kernighan's", solution),
        ("Check Each Bit", solution_check),
        ("Shift & Mask", solution_shift),
        ("Lookup Table", solution_table),
        ("Pythonic", solution_py),
    ]
    
    for name, sol in benchmarks:
        start = time.perf_counter()
        
        for _ in range(100):
            for n in test_inputs:
                sol.hammingWeight(n)
        
        elapsed = (time.perf_counter() - start) * 1000
        
        print(f"  {name:<22}: {elapsed:>10.2f}ms (50k inputs × 100 passes)")
    
    # Demonstrate Kernighan's advantage on sparse inputs
    print()
    print("Kernighan's advantage on SPARSE inputs (few bits set):")
    print("-" * 70)
    
    # Powers of 2 (only 1 bit set each)
    sparse_inputs = [1 << i for i in range(31)]
    
    start = time.perf_counter()
    for _ in range(100000):
        for n in sparse_inputs:
            solution.hammingWeight(n)
    time_kernighan = (time.perf_counter() - start) * 1000
    
    start = time.perf_counter()
    for _ in range(100000):
        for n in sparse_inputs:
            solution_check.hammingWeight(n)
    time_check = (time.perf_counter() - start) * 1000
    
    print(f"  Kernighan's (1 iteration each): {time_kernighan:>8.2f}ms")
    print(f"  Check Each Bit (32 iterations): {time_check:>8.2f}ms")
    print(f"  Speedup: {time_check / time_kernighan:.1f}x")
    
    print("\n" + "=" * 70)