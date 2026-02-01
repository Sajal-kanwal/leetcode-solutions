"""
================================================================================
Problem: 136. Single Number
Platform: LeetCode
URL: https://leetcode.com/problems/single-number/
Difficulty: Easy
Topics: Array, Bit Manipulation
================================================================================

PROBLEM DESCRIPTION:
Given a non-empty array of integers nums, every element appears twice except
for one. Find that single one.

You must implement a solution with a linear runtime complexity and use only
constant extra space.

CONSTRAINTS:
- 1 <= nums.length <= 3 * 10^4
- -3 * 10^4 <= nums[i] <= 3 * 10^4
- Each element appears twice except for one element which appears only once

EXAMPLES:

Example 1:
Input: nums = [2,2,1]
Output: 1

Example 2:
Input: nums = [4,1,2,1,2]
Output: 4

Example 3:
Input: nums = [1]
Output: 1

================================================================================
INTUITION:
The constraint "O(n) time and O(1) space" immediately points to XOR.

XOR PROPERTIES:
- a ^ a = 0       (any number XORed with itself is 0)
- a ^ 0 = a       (any number XORed with 0 is itself)
- a ^ b = b ^ a   (commutative)
- (a ^ b) ^ c = a ^ (b ^ c)  (associative)

KEY INSIGHT:
If we XOR all elements together:
- Every element that appears twice cancels itself out (a ^ a = 0)
- The single element remains (x ^ 0 = x)

EXAMPLE:
nums = [4, 1, 2, 1, 2]
4 ^ 1 ^ 2 ^ 1 ^ 2
= 4 ^ (1 ^ 1) ^ (2 ^ 2)   (rearrange by associativity/commutativity)
= 4 ^ 0 ^ 0                (pairs cancel)
= 4                         (single element remains)

COMPLEXITY:
- Time: O(n) - single pass
- Space: O(1) - only one variable

================================================================================
"""

from typing import List
from functools import reduce


class Solution:
    """LC 136: Single Number - XOR approach"""
    
    def singleNumber(self, nums: List[int]) -> int:
        """
        Find the single number using XOR.
        
        Args:
            nums: Array where every element appears twice except one
            
        Returns:
            The element that appears only once
            
        Algorithm: XOR all elements
        Time: O(n)
        Space: O(1)
        """
        result = 0
        
        for num in nums:
            result ^= num
        
        return result


class SolutionOneLiner:
    """Pythonic one-liner using reduce"""
    
    def singleNumber(self, nums: List[int]) -> int:
        """
        Functional approach using reduce.
        
        reduce applies XOR cumulatively across all elements.
        Equivalent to: nums[0] ^ nums[1] ^ nums[2] ^ ...
        """
        return reduce(lambda a, b: a ^ b, nums)


class SolutionMathematic:
    """
    Mathematical approach using set sum formula.
    
    2 * sum(set(nums)) - sum(nums) = single number
    
    Why: 
    - sum(set) contains each unique value once
    - 2 * sum(set) = what total would be if all appeared twice
    - Subtract actual sum = removes all pairs, leaves single element
    
    Time: O(n)
    Space: O(n) - set creation (doesn't meet O(1) space constraint strictly)
    """
    
    def singleNumber(self, nums: List[int]) -> int:
        return 2 * sum(set(nums)) - sum(nums)


class SolutionHashMap:
    """
    Hash map approach for comparison.
    
    NOT optimal - O(n) space. Included for educational purposes only.
    Shows why XOR is the correct approach for this problem.
    """
    
    def singleNumber(self, nums: List[int]) -> int:
        counts = {}
        
        for num in nums:
            counts[num] = counts.get(num, 0) + 1
        
        for num, count in counts.items():
            if count == 1:
                return num
        
        return -1  # Should never reach here


# ================================================================================
# TEST CASES
# ================================================================================
if __name__ == "__main__":
    solution = Solution()
    solution_reduce = SolutionOneLiner()
    solution_math = SolutionMathematic()
    solution_hash = SolutionHashMap()
    
    test_cases = [
        (
            [2, 2, 1],
            1,
            "Example 1: Single at end"
        ),
        (
            [4, 1, 2, 1, 2],
            4,
            "Example 2: Single at start"
        ),
        (
            [1],
            1,
            "Example 3: Single element array"
        ),
        (
            [1, 1, 2, 2, 3],
            3,
            "Single at end, sorted"
        ),
        (
            [3, 1, 1, 2, 2],
            3,
            "Single at start, unsorted"
        ),
        (
            [1, 2, 3, 2, 1],
            3,
            "Single in middle"
        ),
        (
            [-1, -1, 5],
            5,
            "Negative numbers"
        ),
        (
            [-3, -3, -1, -1, 0],
            0,
            "Zero is the single number"
        ),
        (
            [30000, -30000, -30000],
            30000,
            "Boundary values"
        ),
        (
            [7, 7, 7, 7, 3, 3, 5],
            5,
            "Multiple pairs"
        ),
    ]
    
    print("=" * 70)
    print("TESTING SINGLE NUMBER")
    print("=" * 70)
    print()
    
    solutions = [
        ("XOR Loop", solution),
        ("XOR Reduce", solution_reduce),
        ("Math (2*set - sum)", solution_math),
        ("Hash Map", solution_hash),
    ]
    
    for sol_name, sol in solutions:
        print(f"Testing: {sol_name}")
        print("-" * 70)
        
        passed = 0
        for nums, expected, description in test_cases:
            result = sol.singleNumber(nums)
            
            if result == expected:
                print(f"  ✅ {description}: {nums} → {result}")
                passed += 1
            else:
                print(f"  ❌ {description}: {nums}")
                print(f"     Expected: {expected}, Got: {result}")
        
        print(f"\n  Results: {passed}/{len(test_cases)} passed\n")
    
    print("=" * 70)
    print("🎉 All solutions tested!")
    print("=" * 70)


# ================================================================================
# VISUALIZATION: XOR Step-by-Step
# ================================================================================
"""
Example: nums = [4, 1, 2, 1, 2]

Binary representations:
  4 = 100
  1 = 001
  2 = 010

XOR truth table:
  0 ^ 0 = 0
  0 ^ 1 = 1
  1 ^ 0 = 1
  1 ^ 1 = 0  ← same bits cancel!

Step-by-step XOR:

  result = 0        →  000
  result ^= 4       →  000 ^ 100 = 100  (4)
  result ^= 1       →  100 ^ 001 = 101  (5)
  result ^= 2       →  101 ^ 010 = 111  (7)
  result ^= 1       →  111 ^ 001 = 110  (6)  ← 1 cancels with previous 1
  result ^= 2       →  110 ^ 010 = 100  (4)  ← 2 cancels with previous 2

Final: 100 = 4 ✓

Visual cancellation:
  4  →  100
  1  →  001  ┐
  2  →  010  │ pairs cancel each other
  1  →  001  ┘ (1^1 = 0)
  2  →  010  ┘ (2^2 = 0)
  ─────────────
  Result: 100 = 4 (only unpaired number remains)

Another way to see it (reordered by associativity/commutativity):
  4 ^ 1 ^ 2 ^ 1 ^ 2
  = 4 ^ (1 ^ 1) ^ (2 ^ 2)
  = 4 ^ 0 ^ 0
  = 4
"""


# ================================================================================
# XOR DEEP DIVE: Why It Works on Negative Numbers
# ================================================================================
"""
Python handles negative numbers in XOR using two's complement representation.

Example: -1 in binary (two's complement, 32-bit):
  -1 = ...11111111 (all 1s)
   1 = ...00000001

  -1 ^ -1 = 0  ✓ (still cancels with itself)
  -1 ^ 0  = -1 ✓ (identity property holds)

So XOR works correctly for negative numbers in Python!

Example: nums = [-3, -3, 5]
  -3 ^ -3 = 0
  0 ^ 5 = 5
  Result: 5 ✓
"""


# ================================================================================
# LEARNING NOTES
# ================================================================================
"""
PATTERN: XOR for Finding Unique Elements

XOR is one of the most powerful bit manipulation tricks in competitive
programming and interviews.

XOR PROPERTIES (memorize these):
  1. a ^ a = 0        (self-inverse)
  2. a ^ 0 = a        (identity)
  3. a ^ b = b ^ a    (commutative)
  4. (a^b)^c = a^(b^c) (associative)

WHEN TO USE XOR:
- "Find the element that appears odd number of times"
- "Find the missing number"
- "Find two unique numbers when rest appear twice"
- "Swap two variables without temp"
- Any problem where pairs need to cancel

RELATED PROBLEMS:

1. LC 137: Single Number II (Medium)
   - Every element appears THREE times except one
   - Can't use simple XOR
   - Need bit counting approach

2. LC 260: Single Number III (Medium)
   - TWO elements appear once, rest appear twice
   - Use XOR to find XOR of the two singles
   - Then use a set bit to separate them

3. LC 389: Find the Difference (Easy)
   - Two strings, one has extra character
   - XOR all characters from both strings

4. LC 268: Missing Number (Easy)
   - Array of 0 to n with one missing
   - XOR all numbers 0..n with all array elements

5. LC 421: Maximum XOR of Two Numbers (Hard)
   - Find max a^b from array
   - Uses trie data structure

APPROACH COMPARISON:

| Approach | Time | Space | Meets Constraint? |
|----------|------|-------|-------------------|
| XOR      | O(n) | O(1)  | ✅ Yes            |
| Math     | O(n) | O(n)  | ❌ Space          |
| HashMap  | O(n) | O(n)  | ❌ Space          |
| Sorting  | O(n log n) | O(1) | ❌ Time      |

XOR is the ONLY approach that satisfies both constraints!

INTERVIEW TIPS:

1. Recognize the Pattern
   "O(n) time, O(1) space, pairs cancel" → XOR

2. Explain XOR Properties
   "XOR has two key properties: a^a=0 and a^0=a"
   "So XORing all elements, pairs cancel and the single remains"

3. Show with Example
   Walk through binary representations
   Show how pairs cancel bit by bit

4. Handle Follow-ups
   - "What if there are TWO single numbers?" → LC 260
   - "What if elements appear 3 times?" → LC 137
   - "What about negative numbers?" → XOR handles them correctly

5. Code Cleanly
   The solution is literally 4 lines of code
   Focus on explaining WHY, not the code itself

COMMON MISTAKES:

❌ Using a hash set (O(n) space)
❌ Sorting first (O(n log n) time)
❌ Not knowing XOR properties
❌ Overthinking a simple problem

BIT MANIPULATION CHEAT SHEET:

  a & b    → AND (common bits)
  a | b    → OR  (any set bit)
  a ^ b    → XOR (different bits)
  ~a       → NOT (flip all bits)
  a << n   → Left shift (multiply by 2^n)
  a >> n   → Right shift (divide by 2^n)

  Common tricks:
  - Check if number is power of 2: n & (n-1) == 0
  - Get lowest set bit: n & (-n)
  - Remove lowest set bit: n & (n-1)
  - Check if bit i is set: (n >> i) & 1
  - Toggle bit i: n ^ (1 << i)
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
    
    sizes = [100, 1000, 10000, 30000]
    
    for size in sizes:
        # Generate test data: pairs + one single
        pairs = random.sample(range(-30000, 30000), size // 2)
        single = random.choice(range(-30000, 30000))
        while single in pairs:
            single = random.choice(range(-30000, 30000))
        
        nums = pairs + pairs + [single]
        random.shuffle(nums)
        
        # Benchmark XOR
        start = time.perf_counter()
        for _ in range(1000):
            solution.singleNumber(nums)
        time_xor = (time.perf_counter() - start)
        
        # Benchmark Math
        start = time.perf_counter()
        for _ in range(1000):
            solution_math.singleNumber(nums)
        time_math = (time.perf_counter() - start)
        
        # Benchmark HashMap
        start = time.perf_counter()
        for _ in range(1000):
            solution_hash.singleNumber(nums)
        time_hash = (time.perf_counter() - start)
        
        print(f"Size {size:>6,} (array len={len(nums)}):")
        print(f"  XOR:     {time_xor:>8.4f}s")
        print(f"  Math:    {time_math:>8.4f}s")
        print(f"  HashMap: {time_hash:>8.4f}s")
        print()
    
    print("=" * 70)