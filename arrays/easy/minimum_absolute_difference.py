"""
================================================================================
Problem: 1200. Minimum Absolute Difference
Platform: LeetCode
URL: https://leetcode.com/problems/minimum-absolute-difference/
Difficulty: Easy
Topics: Array, Sorting
================================================================================

PROBLEM DESCRIPTION:
Given an array of distinct integers arr, find all pairs of elements with the 
minimum absolute difference of any two elements.

Return a list of pairs in ascending order (with respect to pairs), where each 
pair [a, b] follows:
- a, b are from arr
- a < b
- b - a equals to the minimum absolute difference of any two elements in arr

CONSTRAINTS:
- 2 <= arr.length <= 10^5
- -10^6 <= arr[i] <= 10^6
- All integers in arr are distinct

EXAMPLES:
Input: arr = [4,2,1,3]
Output: [[1,2],[2,3],[3,4]]
Explanation: The minimum absolute difference is 1. List all pairs with 
difference equal to 1 in ascending order.

Input: arr = [1,3,6,10,15]
Output: [[1,3]]

Input: arr = [3,8,-10,23,19,-4,-14,27]
Output: [[-14,-10],[19,23],[23,27]]

================================================================================
INTUITION:
The minimum absolute difference between any two elements will always be found
between adjacent elements in a sorted array.

Why? Consider three numbers a < b < c:
- |b - a| is the difference between adjacent elements
- |c - a| = (c - b) + (b - a) > |b - a|

Therefore, we only need to check adjacent pairs after sorting.

KEY INSIGHT:
After sorting, the minimum difference must occur between consecutive elements.
We don't need to check all O(n²) pairs - just O(n) adjacent pairs.

APPROACH:
1. Sort the array
2. Calculate differences between all adjacent pairs
3. Find the minimum difference
4. Collect all pairs with that minimum difference

COMPLEXITY ANALYSIS:
- Time: O(n log n) - dominated by sorting
- Space: O(n) - for the output list (or O(log n) for sorting if counting)

EDGE CASES HANDLED:
- Two elements only (return single pair)
- Negative numbers (absolute difference works correctly)
- Multiple pairs with same minimum difference (collect all)
- Large values (up to 10^6)

================================================================================
"""

from typing import List
import numpy as np


class Solution:
    """LC 1200: Minimum Absolute Difference - Pure Python"""
    
    def minimumAbsDifference(self, arr: List[int]) -> List[List[int]]:
        """
        Find all pairs with minimum absolute difference.
        
        Args:
            arr: Array of distinct integers
            
        Returns:
            List of pairs [a, b] where b - a equals minimum difference
            
        Algorithm: Sort + Adjacent Pairs
        Time: O(n log n) - sorting dominates
        Space: O(n) - output list
        """
        # Step 1: Sort the array
        # After sorting, minimum differences are between adjacent elements
        arr.sort()
        
        # Step 2: Find minimum difference among adjacent pairs
        min_diff = float('inf')
        
        for i in range(len(arr) - 1):
            diff = arr[i + 1] - arr[i]
            min_diff = min(min_diff, diff)
        
        # Step 3: Collect all pairs with minimum difference
        result = []
        
        for i in range(len(arr) - 1):
            if arr[i + 1] - arr[i] == min_diff:
                result.append([arr[i], arr[i + 1]])
        
        return result


class SolutionOptimized:
    """Optimized version with single pass after sorting"""
    
    def minimumAbsDifference(self, arr: List[int]) -> List[List[int]]:
        """
        Single-pass solution after sorting.
        
        Time: O(n log n)
        Space: O(n)
        """
        # Sort array
        arr.sort()
        
        # Track minimum difference and result pairs
        min_diff = float('inf')
        result = []
        
        # Single pass: find min and collect pairs simultaneously
        for i in range(len(arr) - 1):
            diff = arr[i + 1] - arr[i]
            
            if diff < min_diff:
                # Found new minimum - reset result
                min_diff = diff
                result = [[arr[i], arr[i + 1]]]
            elif diff == min_diff:
                # Found another pair with same minimum
                result.append([arr[i], arr[i + 1]])
        
        return result


class SolutionNumPy:
    """NumPy-based solution (your original approach)"""
    
    def minimumAbsDifference(self, arr: List[int]) -> List[List[int]]:
        """
        NumPy vectorized solution.
        
        Pros: Concise, leverages optimized C code
        Cons: Requires NumPy dependency, overkill for LeetCode
        
        Time: O(n log n)
        Space: O(n)
        """
        # Convert to NumPy array and sort
        a = np.sort(np.array(arr))
        
        # Calculate differences between consecutive elements
        # np.diff(a)[i] = a[i+1] - a[i]
        diff_a = np.diff(a)
        
        # Find minimum difference
        min_abs = np.min(diff_a)
        
        # Find all indices where difference equals minimum
        # np.where returns tuple, unpack with comma
        inds, = np.where(diff_a == min_abs)
        
        # Build result pairs
        return [[int(a[i]), int(a[i + 1])] for i in inds]


class SolutionOneLiner:
    """Pythonic one-liner (for fun)"""
    
    def minimumAbsDifference(self, arr: List[int]) -> List[List[int]]:
        """
        Ultra-concise solution.
        
        Not recommended for interviews (readability matters),
        but demonstrates Python's expressiveness.
        """
        arr.sort()
        min_diff = min(arr[i + 1] - arr[i] for i in range(len(arr) - 1))
        return [[arr[i], arr[i + 1]] for i in range(len(arr) - 1) 
                if arr[i + 1] - arr[i] == min_diff]


# ================================================================================
# TEST CASES
# ================================================================================
if __name__ == "__main__":
    # Test all solutions
    solution = Solution()
    solution_opt = SolutionOptimized()
    solution_np = SolutionNumPy()
    solution_one = SolutionOneLiner()
    
    test_cases = [
        (
            [4, 2, 1, 3],
            [[1, 2], [2, 3], [3, 4]],
            "Example 1: All consecutive pairs"
        ),
        (
            [1, 3, 6, 10, 15],
            [[1, 3]],
            "Example 2: Single pair"
        ),
        (
            [3, 8, -10, 23, 19, -4, -14, 27],
            [[-14, -10], [19, 23], [23, 27]],
            "Example 3: Negative numbers, multiple pairs"
        ),
        (
            [1, 2],
            [[1, 2]],
            "Edge case: Two elements only"
        ),
        (
            [5, 10, 15, 20, 25],
            [[5, 10], [10, 15], [15, 20], [20, 25]],
            "Arithmetic sequence"
        ),
        (
            [-100, 0, 100],
            [[-100, 0], [0, 100]],
            "Large gaps, symmetric around zero"
        ),
        (
            [1, 1000000],
            [[1, 1000000]],
            "Maximum constraint values"
        ),
        (
            [10, 9, 8, 7, 6, 5, 4, 3, 2, 1],
            [[1, 2], [2, 3], [3, 4], [4, 5], [5, 6], 
             [6, 7], [7, 8], [8, 9], [9, 10]],
            "Reverse sorted input"
        ),
    ]
    
    print("=" * 80)
    print("TESTING ALL SOLUTIONS")
    print("=" * 80)
    print()
    
    solutions = [
        ("Pure Python", solution),
        ("Optimized Single-Pass", solution_opt),
        ("NumPy Vectorized", solution_np),
        ("One-Liner", solution_one),
    ]
    
    for sol_name, sol in solutions:
        print(f"Testing: {sol_name}")
        print("-" * 80)
        
        passed = 0
        for arr, expected, description in test_cases:
            result = sol.minimumAbsDifference(arr.copy())
            
            if result == expected:
                print(f"  ✅ {description}")
                passed += 1
            else:
                print(f"  ❌ {description}")
                print(f"     Input: {arr}")
                print(f"     Expected: {expected}")
                print(f"     Got: {result}")
        
        print(f"\n  Results: {passed}/{len(test_cases)} passed\n")
    
    print("=" * 80)
    print("🎉 All solutions tested!")
    print("=" * 80)


# ================================================================================
# STEP-BY-STEP VISUALIZATION (for arr = [4,2,1,3]):
# ================================================================================
#
# Original array: [4, 2, 1, 3]
#
# Step 1: Sort
# Sorted array: [1, 2, 3, 4]
#
# Step 2: Calculate adjacent differences
# Index:     0  1  2  3
# Array:     1  2  3  4
# Diff:        1  1  1
#            └──┘
#             diff[0] = 2-1 = 1
#               └──┘
#                diff[1] = 3-2 = 1
#                  └──┘
#                   diff[2] = 4-3 = 1
#
# Step 3: Find minimum difference
# min_diff = min(1, 1, 1) = 1
#
# Step 4: Collect all pairs where diff == 1
# i=0: arr[0]=1, arr[1]=2, diff=1 → [1,2] ✓
# i=1: arr[1]=2, arr[2]=3, diff=1 → [2,3] ✓
# i=2: arr[2]=3, arr[3]=4, diff=1 → [3,4] ✓
#
# Result: [[1,2], [2,3], [3,4]]
#
# ================================================================================


# ================================================================================
# VISUALIZATION (for arr = [3,8,-10,23,19,-4,-14,27]):
# ================================================================================
#
# Original: [3, 8, -10, 23, 19, -4, -14, 27]
#
# Step 1: Sort
# Sorted: [-14, -10, -4, 3, 8, 19, 23, 27]
#
# Step 2: Adjacent differences
# Index:    0    1    2   3   4   5   6   7
# Array:  -14  -10   -4   3   8  19  23  27
# Diff:       4    6   7   5  11   4   4
#           └──┘
#            -10-(-14) = 4 ← minimum
#               └──┘
#                -4-(-10) = 6
#                  └──┘
#                   3-(-4) = 7
#                     └──┘
#                      8-3 = 5
#                        └──┘
#                         19-8 = 11
#                            └──┘
#                             23-19 = 4 ← minimum
#                               └──┘
#                                27-23 = 4 ← minimum
#
# Step 3: min_diff = 4
#
# Step 4: Collect pairs where diff == 4
# i=0: diff=4 → [-14, -10] ✓
# i=5: diff=4 → [19, 23] ✓
# i=6: diff=4 → [23, 27] ✓
#
# Result: [[-14,-10], [19,23], [23,27]]
#
# ================================================================================


# ================================================================================
# PERFORMANCE COMPARISON
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
        test_data = random.sample(range(-1000000, 1000000), size)
        
        # Pure Python
        start = time.perf_counter()
        solution.minimumAbsDifference(test_data.copy())
        time_python = (time.perf_counter() - start) * 1000
        
        # Optimized
        start = time.perf_counter()
        solution_opt.minimumAbsDifference(test_data.copy())
        time_opt = (time.perf_counter() - start) * 1000
        
        # NumPy
        start = time.perf_counter()
        solution_np.minimumAbsDifference(test_data.copy())
        time_numpy = (time.perf_counter() - start) * 1000
        
        print(f"Size {size:>6,}:")
        print(f"  Pure Python:  {time_python:>8.3f}ms")
        print(f"  Optimized:    {time_opt:>8.3f}ms")
        print(f"  NumPy:        {time_numpy:>8.3f}ms")
        print()


# ================================================================================
# LEARNING NOTES
# ================================================================================
"""
PATTERN: Sort + Adjacent Comparison

This is a common pattern when dealing with "minimum difference" problems:
1. Sort the array
2. Compare adjacent elements
3. Process based on comparison

WHY SORTING HELPS:
- Minimum difference is always between adjacent elements after sorting
- Reduces O(n²) comparisons to O(n) comparisons
- Sorting cost O(n log n) is worth it

SIMILAR PROBLEMS:
- LC 164: Maximum Gap (similar idea, different metric)
- LC 532: K-diff Pairs in an Array (two pointers after sorting)
- LC 2016: Maximum Difference Between Increasing Elements

OPTIMIZATION TECHNIQUES:

1. Single Pass vs Two Pass
   Two pass (clearer):
   - First pass: find minimum
   - Second pass: collect pairs
   
   Single pass (faster):
   - Track minimum and pairs simultaneously
   - Reset pairs when new minimum found

2. NumPy vs Pure Python
   NumPy Pros:
   - Concise, vectorized operations
   - Potentially faster for very large arrays (C implementation)
   
   Pure Python Pros:
   - No dependencies
   - Better for LeetCode/interviews
   - More readable for others

INTERVIEW TIPS:

1. Clarify sorting is allowed (modifies array)
   - If can't modify, copy first: arr_copy = arr.copy()

2. Explain the insight
   - "After sorting, minimum difference must be between adjacent elements"
   - Draw example: [1, 5, 2] → [1, 2, 5]
   - Show: |5-1| > |2-1| and |5-2|

3. Discuss complexity
   - Sorting: O(n log n)
   - Finding pairs: O(n)
   - Total: O(n log n)
   - "We can't do better than O(n log n) because we need to sort"

4. Handle edge cases
   - Two elements: return single pair
   - All same difference: return all adjacent pairs
   - Negative numbers: still works (we use differences, not absolute values)

COMMON MISTAKES:

❌ Checking all pairs (O(n²)) - unnecessary after sorting
❌ Using abs(arr[i] - arr[i+1]) - not needed, array is sorted
❌ Forgetting to sort before comparing
❌ Not handling the case where all differences are equal
❌ Modifying input array without clarifying with interviewer

ALTERNATIVE APPROACHES:

1. Brute Force (Not Recommended)
   for i in range(n):
       for j in range(i+1, n):
           check difference
   Time: O(n²), Space: O(1)

2. Using Counter (Overcomplicated)
   Track all differences in a counter, find min, extract pairs
   Time: O(n log n), Space: O(n)
   Not better, just different

3. Heap (Overkill)
   Could use min heap to track smallest differences
   Time: O(n log n), Space: O(n)
   Same complexity, more complex code

WHEN TO USE THIS PATTERN:
- "Minimum/maximum difference" problems
- "Closest pairs" problems
- "Find all pairs with property X" where sorting helps
- Problems where relative order doesn't matter initially

================================================================================
"""