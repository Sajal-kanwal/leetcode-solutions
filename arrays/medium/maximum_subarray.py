"""
================================================================================
Problem: 53. Maximum Subarray
Platform: LeetCode
URL: https://leetcode.com/problems/maximum-subarray/
Difficulty: Medium
Topics: Array, Divide and Conquer, Dynamic Programming, Kadane's Algorithm
================================================================================

PROBLEM DESCRIPTION:
Given an integer array nums, find the subarray with the largest sum, and return 
its sum.

A subarray is a contiguous non-empty sequence of elements within an array.

CONSTRAINTS:
- 1 <= nums.length <= 10^5
- -10^4 <= nums[i] <= 10^4

EXAMPLES:

Example 1:
Input: nums = [-2,1,-3,4,-1,2,1,-5,4]
Output: 6
Explanation: The subarray [4,-1,2,1] has the largest sum 6.

Example 2:
Input: nums = [1]
Output: 1
Explanation: The subarray [1] has the largest sum 1.

Example 3:
Input: nums = [5,4,-1,7,8]
Output: 23
Explanation: The subarray [5,4,-1,7,8] has the largest sum 23.

================================================================================
APPROACH 1: KADANE'S ALGORITHM (OPTIMAL)
================================================================================

INTUITION:
At each position, we have two choices:
1. Extend the current subarray by including current element
2. Start a new subarray from current element

We choose the option that gives us the larger sum.

KEY INSIGHT:
If the current subarray sum becomes negative, it's better to start fresh from
the next element because adding a negative sum will only decrease future sums.

ALGORITHM:
- Maintain two variables:
  - current_sum: maximum sum ending at current position
  - max_sum: overall maximum sum seen so far
- For each element:
  - current_sum = max(element, current_sum + element)
  - max_sum = max(max_sum, current_sum)

WHY IT WORKS:
- We're essentially asking: "Should I include the previous subarray, or start new?"
- If previous sum is negative, starting new is always better
- If previous sum is positive, adding it increases our total

COMPLEXITY:
- Time: O(n) - single pass through array
- Space: O(1) - only two variables

================================================================================
APPROACH 2: DIVIDE AND CONQUER
================================================================================

INTUITION:
The maximum subarray can be in three places:
1. Entirely in the left half
2. Entirely in the right half
3. Crosses the middle (includes elements from both halves)

ALGORITHM:
1. Divide array into left and right halves
2. Recursively find max subarray in left half
3. Recursively find max subarray in right half
4. Find max subarray crossing the middle
5. Return maximum of the three

COMPLEXITY:
- Time: O(n log n) - T(n) = 2T(n/2) + O(n)
- Space: O(log n) - recursion stack

================================================================================
APPROACH 3: DYNAMIC PROGRAMMING (EXPLICIT)
================================================================================

INTUITION:
Define dp[i] = maximum subarray sum ending at index i

RECURRENCE:
dp[i] = max(nums[i], dp[i-1] + nums[i])

Base case: dp[0] = nums[0]

Answer: max(dp[0], dp[1], ..., dp[n-1])

COMPLEXITY:
- Time: O(n)
- Space: O(n) - can be optimized to O(1) like Kadane's

================================================================================
"""

from typing import List


class Solution:
    """LC 53: Maximum Subarray - Kadane's Algorithm (Optimal)"""
    
    def maxSubArray(self, nums: List[int]) -> int:
        """
        Find maximum subarray sum using Kadane's algorithm.
        
        Args:
            nums: Array of integers
            
        Returns:
            Maximum subarray sum
            
        Algorithm: Kadane's Algorithm
        Time: O(n)
        Space: O(1)
        """
        # Initialize with first element
        max_sum = nums[0]
        current_sum = 0
        
        for num in nums:
            # If current sum is negative, reset to 0
            # (starting fresh is better than carrying negative sum)
            if current_sum < 0:
                current_sum = 0
            
            # Add current element
            current_sum += num
            
            # Update global maximum
            max_sum = max(max_sum, current_sum)
        
        return max_sum


class SolutionKadaneAlternative:
    """Alternative Kadane's formulation (more intuitive for some)"""
    
    def maxSubArray(self, nums: List[int]) -> int:
        """
        Kadane's algorithm - alternative formulation.
        
        At each position, decide: extend previous subarray or start new?
        """
        max_sum = nums[0]
        current_sum = nums[0]
        
        for i in range(1, len(nums)):
            # Either extend previous subarray or start new from current
            current_sum = max(nums[i], current_sum + nums[i])
            
            # Update global maximum
            max_sum = max(max_sum, current_sum)
        
        return max_sum


class SolutionDivideConquer:
    """Divide and Conquer approach (O(n log n))"""
    
    def maxSubArray(self, nums: List[int]) -> int:
        """
        Find maximum subarray using divide and conquer.
        
        Time: O(n log n)
        Space: O(log n) - recursion stack
        """
        return self._max_subarray_helper(nums, 0, len(nums) - 1)
    
    def _max_subarray_helper(self, nums: List[int], left: int, right: int) -> int:
        """
        Helper function for divide and conquer.
        
        Returns maximum subarray sum in nums[left:right+1]
        """
        # Base case: single element
        if left == right:
            return nums[left]
        
        # Find middle
        mid = (left + right) // 2
        
        # Maximum subarray in left half
        left_max = self._max_subarray_helper(nums, left, mid)
        
        # Maximum subarray in right half
        right_max = self._max_subarray_helper(nums, mid + 1, right)
        
        # Maximum subarray crossing the middle
        cross_max = self._max_crossing_sum(nums, left, mid, right)
        
        # Return maximum of the three
        return max(left_max, right_max, cross_max)
    
    def _max_crossing_sum(self, nums: List[int], left: int, mid: int, right: int) -> int:
        """
        Find maximum subarray sum that crosses the middle point.
        
        This subarray must include nums[mid] and nums[mid+1].
        """
        # Find max sum in left half (must include mid)
        left_sum = float('-inf')
        current_sum = 0
        
        # Start from mid and go left
        for i in range(mid, left - 1, -1):
            current_sum += nums[i]
            left_sum = max(left_sum, current_sum)
        
        # Find max sum in right half (must include mid+1)
        right_sum = float('-inf')
        current_sum = 0
        
        # Start from mid+1 and go right
        for i in range(mid + 1, right + 1):
            current_sum += nums[i]
            right_sum = max(right_sum, current_sum)
        
        # Return sum of both halves
        return left_sum + right_sum


class SolutionDynamicProgramming:
    """Dynamic Programming approach (explicit DP array)"""
    
    def maxSubArray(self, nums: List[int]) -> int:
        """
        DP solution with explicit state array.
        
        Time: O(n)
        Space: O(n) - can be optimized to O(1)
        """
        n = len(nums)
        
        # dp[i] = maximum subarray sum ending at index i
        dp = [0] * n
        dp[0] = nums[0]
        max_sum = nums[0]
        
        for i in range(1, n):
            # Either extend previous subarray or start new
            dp[i] = max(nums[i], dp[i - 1] + nums[i])
            max_sum = max(max_sum, dp[i])
        
        return max_sum


class SolutionWithIndices:
    """Kadane's algorithm that also tracks the subarray indices"""
    
    def maxSubArray(self, nums: List[int]) -> int:
        """
        Returns both the maximum sum and the subarray indices.
        
        Returns:
            Tuple of (max_sum, start_index, end_index)
        """
        max_sum = nums[0]
        current_sum = 0
        
        # Track indices
        start = 0
        end = 0
        temp_start = 0
        
        for i in range(len(nums)):
            if current_sum < 0:
                current_sum = 0
                temp_start = i  # Potential new start
            
            current_sum += nums[i]
            
            if current_sum > max_sum:
                max_sum = current_sum
                start = temp_start
                end = i
        
        return max_sum, start, end
    
    def maxSubArraySum(self, nums: List[int]) -> int:
        """Just return the sum (compatible with base problem)"""
        return self.maxSubArray(nums)[0]


# ================================================================================
# TEST CASES
# ================================================================================
if __name__ == "__main__":
    # Test all solutions
    solution = Solution()
    solution_alt = SolutionKadaneAlternative()
    solution_dc = SolutionDivideConquer()
    solution_dp = SolutionDynamicProgramming()
    solution_idx = SolutionWithIndices()
    
    test_cases = [
        (
            [-2, 1, -3, 4, -1, 2, 1, -5, 4],
            6,
            "Example 1: Subarray [4,-1,2,1]"
        ),
        (
            [1],
            1,
            "Example 2: Single element"
        ),
        (
            [5, 4, -1, 7, 8],
            23,
            "Example 3: Entire array"
        ),
        (
            [-1],
            -1,
            "Single negative element"
        ),
        (
            [-2, -1],
            -1,
            "All negative: choose least negative"
        ),
        (
            [1, 2, 3, 4, 5],
            15,
            "All positive: entire array"
        ),
        (
            [-2, 1, -3, 4, -1, 2, 1, -5, 4],
            6,
            "Mixed: optimal subarray in middle"
        ),
        (
            [8, -19, 5, -4, 20],
            21,
            "Large gaps: [5,-4,20]"
        ),
        (
            [-1, -2, -3, -4],
            -1,
            "All negative: maximum is -1"
        ),
        (
            [0],
            0,
            "Single zero"
        ),
    ]
    
    print("=" * 80)
    print("TESTING ALL APPROACHES")
    print("=" * 80)
    print()
    
    solutions = [
        ("Kadane's Algorithm", solution),
        ("Kadane's Alternative", solution_alt),
        ("Divide and Conquer", solution_dc),
        ("Dynamic Programming", solution_dp),
    ]
    
    for sol_name, sol in solutions:
        print(f"Testing: {sol_name}")
        print("-" * 80)
        
        passed = 0
        for nums, expected, description in test_cases:
            result = sol.maxSubArray(nums.copy())
            
            if result == expected:
                print(f"  ✅ {description}")
                passed += 1
            else:
                print(f"  ❌ {description}")
                print(f"     Input: {nums}")
                print(f"     Expected: {expected}")
                print(f"     Got: {result}")
        
        print(f"\n  Results: {passed}/{len(test_cases)} passed\n")
    
    # Test solution with indices
    print("Testing: Kadane's with Indices")
    print("-" * 80)
    
    test_with_indices = [
        ([-2, 1, -3, 4, -1, 2, 1, -5, 4], 6, 3, 6),
        ([5, 4, -1, 7, 8], 23, 0, 4),
        ([1], 1, 0, 0),
    ]
    
    for nums, expected_sum, expected_start, expected_end in test_with_indices:
        result_sum, start, end = solution_idx.maxSubArray(nums)
        
        if result_sum == expected_sum and start == expected_start and end == expected_end:
            print(f"  ✅ {nums} → sum={result_sum}, indices=[{start}:{end}]")
        else:
            print(f"  ❌ {nums}")
            print(f"     Expected: sum={expected_sum}, indices=[{expected_start}:{expected_end}]")
            print(f"     Got: sum={result_sum}, indices=[{start}:{end}]")
    
    print("\n" + "=" * 80)
    print("🎉 All solutions tested!")
    print("=" * 80)


# ================================================================================
# VISUALIZATION: Kadane's Algorithm Step-by-Step
# ================================================================================
"""
Example: nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]

Index    Value    current_sum (before)    current_sum (after)    max_sum
-----    -----    --------------------    -------------------    -------
  0       -2              0                      -2               -2
  1        1              0 (reset)              1                1
  2       -3              1                      -2               1
  3        4              0 (reset)              4                4
  4       -1              4                      3                4
  5        2              3                      5                5
  6        1              5                      6                6  ← Maximum!
  7       -5              6                      1                6
  8        4              1                      5                6

Step-by-step explanation:

i=0, num=-2:
  current_sum = 0 (initial)
  current_sum += -2 → current_sum = -2
  max_sum = max(-∞, -2) = -2

i=1, num=1:
  current_sum = -2 < 0 → reset to 0
  current_sum += 1 → current_sum = 1
  max_sum = max(-2, 1) = 1

i=2, num=-3:
  current_sum = 1 > 0 → keep it
  current_sum += -3 → current_sum = -2
  max_sum = max(1, -2) = 1

i=3, num=4:
  current_sum = -2 < 0 → reset to 0
  current_sum += 4 → current_sum = 4
  max_sum = max(1, 4) = 4
  [Start of optimal subarray]

i=4, num=-1:
  current_sum = 4 > 0 → keep it
  current_sum += -1 → current_sum = 3
  max_sum = max(4, 3) = 4

i=5, num=2:
  current_sum = 3 > 0 → keep it
  current_sum += 2 → current_sum = 5
  max_sum = max(4, 5) = 5

i=6, num=1:
  current_sum = 5 > 0 → keep it
  current_sum += 1 → current_sum = 6
  max_sum = max(5, 6) = 6
  [End of optimal subarray]

i=7, num=-5:
  current_sum = 6 > 0 → keep it
  current_sum += -5 → current_sum = 1
  max_sum = max(6, 1) = 6

i=8, num=4:
  current_sum = 1 > 0 → keep it
  current_sum += 4 → current_sum = 5
  max_sum = max(6, 5) = 6

Final answer: 6
Optimal subarray: [4, -1, 2, 1] (indices 3-6)
"""


# ================================================================================
# DIVIDE AND CONQUER VISUALIZATION
# ================================================================================
"""
Example: nums = [4, -1, 2, 1]

                    maxSubArray([4,-1,2,1])
                            |
                ┌───────────┴───────────┐
                |                       |
         maxSubArray([4,-1])     maxSubArray([2,1])
                |                       |
        ┌───────┴───────┐       ┌───────┴───────┐
        |               |       |               |
  maxSubArray([4]) maxSubArray([-1])  maxSubArray([2]) maxSubArray([1])
        |               |       |               |
      return 4      return -1   return 2      return 1

    Left max = max(4, -1, crossing) = 4
    Right max = max(2, 1, crossing) = 3
    Crossing = maxCrossing([4,-1], [2,1]) = 4 + 3 = 7... wait that's wrong

Let me recalculate crossing sum properly:

Crossing sum at top level (mid between -1 and 2):
  Left part (going left from -1): -1 + 4 = 3
  Right part (going right from 2): 2 + 1 = 3
  Crossing sum = 3 + 3 = 6

Final: max(4, 3, 6) = 6 ✓
"""


# ================================================================================
# PERFORMANCE BENCHMARK
# ================================================================================
if __name__ == "__main__":
    import time
    import random
    
    print("\n" + "=" * 80)
    print("PERFORMANCE BENCHMARK")
    print("=" * 80)
    print()
    
    sizes = [100, 1000, 10000, 100000]
    
    for size in sizes:
        # Generate random test data
        test_data = [random.randint(-100, 100) for _ in range(size)]
        
        # Kadane's Algorithm
        start = time.perf_counter()
        for _ in range(100):
            solution.maxSubArray(test_data)
        time_kadane = (time.perf_counter() - start) * 10  # ms per iteration
        
        # Divide and Conquer (only for smaller sizes - too slow for large)
        if size <= 10000:
            start = time.perf_counter()
            for _ in range(100):
                solution_dc.maxSubArray(test_data)
            time_dc = (time.perf_counter() - start) * 10
        else:
            time_dc = None
        
        print(f"Size {size:>6,}:")
        print(f"  Kadane's Algorithm:     {time_kadane:>8.3f}ms")
        if time_dc:
            print(f"  Divide and Conquer:     {time_dc:>8.3f}ms")
            print(f"  Speed ratio (D&C / Kadane): {time_dc/time_kadane:.1f}x slower")
        else:
            print(f"  Divide and Conquer:     (skipped - too slow)")
        print()


# ================================================================================
# LEARNING NOTES
# ================================================================================
"""
PATTERN: Kadane's Algorithm - Canonical Maximum Subarray Solution

This is one of the most important algorithms to know for coding interviews.
It appears in countless variations and optimizations.

KEY INSIGHTS:

1. Why Kadane's Works
   - At each position, we're deciding: "Should I continue the current subarray
     or start a new one?"
   - If current sum is negative, starting fresh is always better
   - This greedy choice leads to the optimal solution

2. Why It's O(n)
   - Single pass through the array
   - Constant time operations at each step
   - No nested loops or recursion

3. When to Use This Pattern
   - "Maximum/minimum subarray sum"
   - "Maximum product subarray" (with modifications)
   - "Best time to buy/sell stock" (variation)
   - Any problem about contiguous subarrays with optimization

VARIATIONS AND RELATED PROBLEMS:

1. LC 152: Maximum Product Subarray
   - Similar to Kadane's but track both max and min (negative × negative = positive)
   
2. LC 918: Maximum Sum Circular Subarray
   - Maximum subarray in circular array
   - Use Kadane's twice: normal and inverted
   
3. LC 121: Best Time to Buy and Sell Stock
   - Find max(price[j] - price[i]) where j > i
   - Essentially Kadane's on the difference array
   
4. LC 1186: Maximum Subarray Sum with One Deletion
   - Allowed to delete at most one element
   - Use modified Kadane's with two states

5. LC 1425: Constrained Subsequence Sum
   - Similar to Kadane's but can skip elements (subsequence not subarray)

COMMON MISTAKES:

❌ Initializing max_sum to 0
   - Fails when all elements are negative
   - Should initialize to nums[0] or -infinity

❌ Not resetting current_sum correctly
   - Should reset to 0 when negative, not to current element

❌ Confusing subarray with subsequence
   - Subarray = contiguous elements
   - Subsequence = any elements in order (can skip)

❌ Forgetting edge cases
   - Single element array
   - All negative numbers
   - All positive numbers

INTERVIEW TIPS:

1. Start with Brute Force
   "We could check all O(n²) subarrays, each taking O(n) time → O(n³) total"

2. Mention Optimization
   "We can use prefix sums to get O(n²) → O(n²) time, O(n) space"

3. Introduce Kadane's
   "But optimal is Kadane's algorithm: O(n) time, O(1) space"
   
4. Explain the Insight
   "Key insight: if current sum is negative, starting fresh is always better"

5. Code Carefully
   - Initialize max_sum correctly (not 0!)
   - Handle the reset logic clearly
   - Test with all negative array

6. Mention Follow-up
   "The divide-and-conquer approach is O(n log n) but interesting for
   distributed systems or when we can't modify the array"

COMPLEXITY COMPARISON:

Brute Force:           O(n³) or O(n²) with prefix sums
Kadane's Algorithm:    O(n) time, O(1) space  ← Optimal
Divide and Conquer:    O(n log n) time, O(log n) space
Dynamic Programming:   O(n) time, O(n) or O(1) space

REAL-WORLD APPLICATIONS:

- Stock market: maximum profit in a time period
- Signal processing: finding strongest signal segment
- DNA sequencing: finding high-GC content regions
- Financial analysis: best time period for investment
- Time series analysis: detecting trends

WHY THIS PROBLEM MATTERS:

1. Teaches greedy algorithm design
2. Shows how local decisions lead to global optimum
3. Demonstrates space optimization (DP → Kadane's)
4. Common interview question (asked at all FAANG companies)
5. Foundation for many other problems

HISTORICAL NOTE:

Named after Jay Kadane (CMU professor) who discovered it in 1984.
It's an elegant example of how a complex problem can have a surprisingly
simple optimal solution.
"""