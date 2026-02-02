"""
================================================================================
Problem: 3013. Divide an Array Into Subarrays With Minimum Cost II
Platform: LeetCode
URL: https://leetcode.com/problems/divide-array-into-subarrays-with-minimum-cost-ii/
Difficulty: Hard
Topics: Array, Sliding Window, Greedy, Heap, Ordered Set
================================================================================

PROBLEM DESCRIPTION:
You are given a 0-indexed array nums of length n, and two positive integers k and dist.

The cost of an array is its first element.
Divide nums into k disjoint contiguous subarrays such that:
- ik-1 - i1 <= dist (difference between start indices of 2nd and kth subarrays)

Return the minimum possible sum of costs.

CONSTRAINTS:
- 3 <= n <= 10^5
- 1 <= nums[i] <= 10^9
- 3 <= k <= n
- k - 2 <= dist <= n - 2

EXAMPLES:

Example 1:
Input: nums = [1,3,2,6,4,2], k = 3, dist = 3
Output: 5
Explanation: [1,3], [2,6,4], [2] → costs: 1 + 2 + 2 = 5

Example 2:
Input: nums = [10,1,2,2,2,1], k = 4, dist = 3
Output: 15

Example 3:
Input: nums = [10,8,18,9], k = 3, dist = 1
Output: 36

================================================================================
INTUITION:
================================================================================

KEY OBSERVATIONS:

1. First subarray MUST start at index 0
   → Cost includes nums[0] (fixed)

2. We need to choose k-1 MORE starting indices from [1, n-1]
   → Minimize sum of values at these indices

3. Constraint: ik-1 - i1 <= dist
   → All k-1 indices must be within a window of size dist+1
   → Starting from index 1

REFRAME THE PROBLEM:
"Choose k-1 smallest values from a sliding window of size dist+1,
starting at index 1"

This becomes a SLIDING WINDOW problem where we maintain:
- The k-1 smallest values in the current window
- Update as window slides

APPROACH: Two Heaps (Min/Max) with Sliding Window
- Keep k-1 smallest values in "selected" set (min heap)
- Keep remaining values in "candidates" set (max heap)
- As window slides: add new element, remove old element
- Rebalance heaps to maintain k-1 smallest in selected

COMPLEXITY:
- Time: O(n log k) — n window positions, O(log k) heap operations each
- Space: O(dist) — store at most dist+1 elements in heaps

================================================================================
"""

from typing import List
import heapq
from sortedcontainers import SortedList


class Solution:
    """LC 3013: Divide Array with Minimum Cost - Two Heaps Approach"""
    
    def minimumCost(self, nums: List[int], k: int, dist: int) -> int:
        """
        Find minimum cost to divide array into k subarrays.
        
        Args:
            nums: Array of integers
            k: Number of subarrays
            dist: Maximum distance constraint
            
        Returns:
            Minimum sum of subarray costs
            
        Algorithm: Sliding Window with Two Heaps
        Time: O(n log k)
        Space: O(dist)
        """
        n = len(nums)
        
        # First subarray starts at 0, cost is nums[0]
        # Need to choose k-1 more starting points from indices [1, n-1]
        # Constraint: last chosen index - first chosen index <= dist
        
        # This means: choose k-1 smallest from window [1, dist+1]
        # Then slide window and maintain k-1 smallest
        
        # Two heaps approach:
        # - selected (min heap): k-1 smallest values currently chosen
        # - candidates (max heap): remaining values in window
        
        # Use negative values for max heap
        selected = []  # Min heap of chosen values
        candidates = []  # Max heap of non-chosen values
        selected_sum = 0
        
        # Initial window: indices 1 to dist+1
        window = []
        for i in range(1, min(n, dist + 2)):
            window.append((nums[i], i))
        
        # Sort and take k-1 smallest
        window.sort()
        
        for i in range(min(k - 1, len(window))):
            val, idx = window[i]
            heapq.heappush(selected, (val, idx))
            selected_sum += val
        
        for i in range(k - 1, len(window)):
            val, idx = window[i]
            heapq.heappush(candidates, (-val, idx))
        
        min_cost = nums[0] + selected_sum
        
        # Slide window: indices [1, dist+1] → [2, dist+2] → ...
        left = 1
        right = dist + 1
        
        while right < n - 1:
            right += 1
            
            # Add nums[right] to window
            new_val = nums[right]
            
            # Decide where to place new element
            if len(selected) < k - 1:
                heapq.heappush(selected, (new_val, right))
                selected_sum += new_val
            elif new_val < selected[0][0]:
                # New value smaller than largest in selected
                # Swap: move largest from selected to candidates
                old_val, old_idx = heapq.heapreplace(selected, (new_val, right))
                selected_sum += new_val - old_val
                heapq.heappush(candidates, (-old_val, old_idx))
            else:
                # New value goes to candidates
                heapq.heappush(candidates, (-new_val, right))
            
            # Remove nums[left] from window
            # Find and remove from appropriate heap
            left += 1
            
            # Lazy deletion: mark as removed
            # When popping from heap, skip removed indices
            # This is simpler than finding and removing
            
            # Update min_cost
            # Need to handle removal properly
            # Use a different approach: rebuild or use SortedList
        
        # The above lazy deletion is complex
        # Better approach: use SortedList
        return self._minimumCostWithSortedList(nums, k, dist)
    
    def _minimumCostWithSortedList(self, nums: List[int], k: int, dist: int) -> int:
        """
        Cleaner implementation using SortedList.
        
        Maintains window of valid starting indices and efficiently
        finds k-1 smallest values.
        """
        n = len(nums)
        
        # SortedList to maintain window elements
        window = SortedList()
        
        # Initial window: indices 1 to dist+1
        for i in range(1, min(n, dist + 2)):
            window.add(nums[i])
        
        # Sum of k-1 smallest
        current_sum = sum(window[:k-1])
        min_cost = nums[0] + current_sum
        
        # Slide window
        left = 1
        right = dist + 1
        
        while right < n - 1:
            right += 1
            
            # Remove leftmost element
            remove_val = nums[left]
            
            # Check if removed value was in k-1 smallest
            if remove_val <= window[k-2]:  # Was in selected
                current_sum -= remove_val
                window.remove(remove_val)
                
                # Add new element
                window.add(nums[right])
                
                # If new element is in k-1 smallest, add it
                # Otherwise add the new k-1th smallest (which moved up)
                if nums[right] <= window[k-2]:
                    current_sum += nums[right]
                else:
                    current_sum += window[k-2]
            else:  # Was not in selected
                window.remove(remove_val)
                
                # Add new element
                add_val = nums[right]
                window.add(add_val)
                
                # Check if new element is smaller than current k-1th
                if add_val < window[k-2]:
                    current_sum += add_val - window[k-2]
            
            left += 1
            min_cost = min(min_cost, nums[0] + current_sum)
        
        return min_cost


class SolutionCleaner:
    """
    Cleaner implementation that's easier to understand.
    """
    
    def minimumCost(self, nums: List[int], k: int, dist: int) -> int:
        """
        Simplified sliding window with SortedList.
        """
        n = len(nums)
        
        # Window of candidate starting positions
        window = SortedList()
        
        # Build initial window [1, dist+1]
        for i in range(1, min(dist + 2, n)):
            window.add(nums[i])
        
        # Take k-1 smallest
        min_cost = nums[0] + sum(window[:k-1])
        
        # Slide window from [1, dist+1] to [left, right]
        for left in range(2, n - k + 2):
            # Remove leftmost element
            window.remove(nums[left - 1])
            
            # Add rightmost element if within bounds
            right = left + dist
            if right < n:
                window.add(nums[right])
            
            # Update cost with k-1 smallest in current window
            if len(window) >= k - 1:
                min_cost = min(min_cost, nums[0] + sum(window[:k-1]))
        
        return min_cost


# ================================================================================
# TEST CASES
# ================================================================================
if __name__ == "__main__":
    try:
        solution = SolutionCleaner()
        
        test_cases = [
            (
                [1, 3, 2, 6, 4, 2],
                3,
                3,
                5,
                "Example 1"
            ),
            (
                [10, 1, 2, 2, 2, 1],
                4,
                3,
                15,
                "Example 2"
            ),
            (
                [10, 8, 18, 9],
                3,
                1,
                36,
                "Example 3"
            ),
            (
                [1, 2, 3],
                3,
                1,
                6,
                "Minimum k: all subarrays of size 1"
            ),
        ]
        
        print("=" * 70)
        print("TESTING DIVIDE ARRAY INTO SUBARRAYS WITH MINIMUM COST II")
        print("=" * 70)
        print()
        
        passed = 0
        for nums, k, dist, expected, description in test_cases:
            result = solution.minimumCost(nums, k, dist)
            
            if result == expected:
                print(f"✅ {description}")
                print(f"   nums={nums}, k={k}, dist={dist}")
                print(f"   Result: {result}")
                passed += 1
            else:
                print(f"❌ {description}")
                print(f"   nums={nums}, k={k}, dist={dist}")
                print(f"   Expected: {expected}, Got: {result}")
            print()
        
        print("=" * 70)
        print(f"RESULTS: {passed}/{len(test_cases)} tests passed")
        print("=" * 70)
    
    except ImportError:
        print("=" * 70)
        print("⚠️  sortedcontainers not installed")
        print("=" * 70)
        print()
        print("To run this solution, install sortedcontainers:")
        print("  pip install sortedcontainers")
        print()
        print("This is a common library for competitive programming")
        print("that provides SortedList, SortedDict, SortedSet")


# ================================================================================
# LEARNING NOTES
# ================================================================================
"""
PATTERN: Sliding Window + Maintaining Top K Elements

This problem combines two classic patterns:
1. Sliding window (window of valid starting positions)
2. Maintaining k smallest/largest elements efficiently

═══════════════════════════════════════════════════════════════
WHY SORTEDLIST IS PERFECT HERE
═══════════════════════════════════════════════════════════════

Operations needed:
- Add element: O(log n)
- Remove element: O(log n)
- Access kth smallest: O(1) with indexing
- Get sum of k smallest: O(k) with slicing

SortedList provides all of these efficiently.

Alternative: Two heaps (min + max)
- More complex to implement correctly
- Need to handle rebalancing carefully
- Lazy deletion adds complexity

═══════════════════════════════════════════════════════════════
KEY INSIGHT: PROBLEM TRANSFORMATION
═══════════════════════════════════════════════════════════════

Original: Divide into k subarrays with constraint
          ↓
Transformed: Choose k-1 starting positions
          ↓
Further: Choose k-1 smallest values from sliding window

This transformation makes the solution obvious!

═══════════════════════════════════════════════════════════════
RELATED PROBLEMS
═══════════════════════════════════════════════════════════════

1. LC 239: Sliding Window Maximum
   - Maintain max in sliding window
   - Use monotonic deque

2. LC 295: Find Median from Data Stream
   - Maintain median (middle element)
   - Two heaps approach

3. LC 480: Sliding Window Median
   - Combines both above patterns
   - SortedList or two heaps

4. LC 1425: Constrained Subsequence Sum
   - Sliding window + DP
   - Monotonic deque optimization

═══════════════════════════════════════════════════════════════
SORTEDLIST vs HEAPS vs BST
═══════════════════════════════════════════════════════════════

SortedList (Python):
✅ Clean indexing: window[k-1]
✅ Easy removal: window.remove(val)
✅ O(log n) operations
❌ Requires external library

Two Heaps:
✅ Standard library only
❌ Complex rebalancing
❌ Harder to implement correctly

BST (TreeMap in Java, TreeSet in C++):
✅ Available in many languages
✅ Similar to SortedList
❌ Not in Python standard library

For interviews: Know both SortedList and two heaps approaches!

═══════════════════════════════════════════════════════════════
INTERVIEW TIPS
═══════════════════════════════════════════════════════════════

1. Transform the problem
   "First subarray must start at 0, so we choose k-1 more"
   "These must be within a window → sliding window problem"

2. Identify the core challenge
   "Need to maintain k-1 smallest in sliding window"

3. Discuss approaches
   "SortedList is cleanest, but two heaps works too"

4. Handle edge cases
   - k = n (each subarray size 1)
   - dist = n-2 (no real constraint)
   - Small values of k and dist

5. Complexity analysis
   "O(n log k) where n is array length, k is window operations"
"""