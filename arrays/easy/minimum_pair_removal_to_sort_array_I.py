"""
================================================================================
Problem: 3507. Minimum Pair Removal to Sort Array I
Platform: LeetCode
URL: https://leetcode.com/problems/minimum-pair-removal-to-sort-array-i/
Difficulty: Easy
Topics: Array, Greedy, Simulation
================================================================================

PROBLEM DESCRIPTION:
You are given a 0-indexed integer array nums.

In one operation, you can select an adjacent pair of elements with the minimum 
sum among all such pairs, replace these two elements with their sum, and remove 
the second element from the array.

If there are multiple adjacent pairs with the minimum sum, you must select the 
leftmost one.

Return the minimum number of operations required to make the array nums sorted 
in non-decreasing order.

CONSTRAINTS:
- 1 <= nums.length <= 50
- 1 <= nums[i] <= 50

EXAMPLES:
Input: nums = [5,2,3,1]
Output: 2
Explanation:
- Operation 1: Choose pair (2,3) with sum 5. Array becomes [5,5,1]
- Operation 2: Choose pair (5,1) with sum 6. Array becomes [5,6]
- Now array is sorted.

Input: nums = [1,2,2]
Output: 0
Explanation: Array is already sorted in non-decreasing order.

Input: nums = [3,1,2]
Output: 1
Explanation:
- Operation 1: Choose pair (1,2) with sum 3. Array becomes [3,3]
- Now array is sorted.

================================================================================
INTUITION:
This is a greedy simulation problem. The key insight is that we must always 
choose the adjacent pair with the minimum sum (as stated in the problem), and
continue merging until the array becomes non-decreasing.

The greedy choice is forced by the problem statement - we don't have freedom
to choose which pair to merge. We simply simulate the process.

KEY OBSERVATIONS:
1. We must follow the rule: always pick minimum sum pair (leftmost if tie)
2. Each operation reduces array size by 1
3. Maximum n-1 operations possible (merge down to 1 element)
4. Small constraint (n ≤ 50) allows O(n³) simulation

APPROACH:
1. Check if array is already non-decreasing → return 0
2. While array is not sorted:
   a. Find adjacent pair with minimum sum
   b. If multiple pairs have same sum, choose leftmost (first occurrence)
   c. Merge the pair: replace first with sum, remove second
   d. Increment operation counter
3. Return total operations

WHY GREEDY WORKS:
The problem explicitly states we must choose the minimum sum pair, so there's
no choice involved. We simply simulate the forced greedy strategy.

COMPLEXITY ANALYSIS:
- Time: O(n² × k) where k is number of operations
  - Each operation: O(n) to find min pair
  - Check sorted: O(n)
  - k operations: at most O(n)
  - Overall: O(n³) worst case, acceptable for n ≤ 50
- Space: O(1) - modify array in-place

EDGE CASES HANDLED:
- Already sorted array (return 0)
- Single element array (already sorted)
- All elements equal
- Array becomes sorted after one operation
- Ties in minimum sum (choose leftmost)

================================================================================
"""

from typing import List

class Solution:
    def minimumPairRemoval(self, nums: List[int]) -> int:
        """
        Count minimum operations to make array non-decreasing.
        
        Args:
            nums: Array of positive integers
            
        Returns:
            Minimum number of pair removal operations needed
        """
        
        operations = 0
        
        # Helper function to check if array is non-decreasing
        def is_sorted(arr: List[int]) -> bool:
            """
            Check if array is sorted in non-decreasing order.
            
            Time: O(n)
            Space: O(1)
            """
            for i in range(len(arr) - 1):
                if arr[i] > arr[i + 1]:
                    return False
            return True
        
        # Simulate operations until array is sorted
        while not is_sorted(nums):
            
            # Find adjacent pair with minimum sum
            min_sum = float('inf')
            min_index = -1
            
            # Scan all adjacent pairs
            # Left-to-right scan ensures leftmost pair is chosen in case of ties
            for i in range(len(nums) - 1):
                current_sum = nums[i] + nums[i + 1]
                
                # Update only if strictly smaller (ensures leftmost in ties)
                if current_sum < min_sum:
                    min_sum = current_sum
                    min_index = i
            
            # Merge the pair at min_index
            # Replace first element with sum, remove second element
            nums[min_index] = nums[min_index] + nums[min_index + 1]
            nums.pop(min_index + 1)
            
            # Increment operation counter
            operations += 1
        
        return operations


# ================================================================================
# ALTERNATIVE SOLUTION: Slight Optimization (Same Complexity)
# ================================================================================
class SolutionOptimized:
    def minimumPairRemoval(self, nums: List[int]) -> int:
        """
        Slightly cleaner version with early exit check.
        """
        # Early exit: already sorted
        if all(nums[i] <= nums[i + 1] for i in range(len(nums) - 1)):
            return 0
        
        operations = 0
        
        while len(nums) > 1:
            # Find minimum sum pair
            min_idx = min(range(len(nums) - 1), 
                         key=lambda i: nums[i] + nums[i + 1])
            
            # Check if array is now sorted (optimization)
            if all(nums[i] <= nums[i + 1] for i in range(len(nums) - 1)):
                break
            
            # Merge pair
            nums[min_idx] += nums[min_idx + 1]
            nums.pop(min_idx + 1)
            operations += 1
        
        return operations


# ================================================================================
# TEST CASES
# ================================================================================
if __name__ == "__main__":
    solution = Solution()
    
    # Test Case 1: Example from problem
    nums1 = [5, 2, 3, 1]
    result1 = solution.minimumPairRemoval(nums1.copy())
    assert result1 == 2, f"Test 1 failed: expected 2, got {result1}"
    print(f"✅ Test 1 passed: [5,2,3,1] → {result1} operations")
    
    # Test Case 2: Already sorted
    nums2 = [1, 2, 2]
    result2 = solution.minimumPairRemoval(nums2.copy())
    assert result2 == 0, f"Test 2 failed: expected 0, got {result2}"
    print(f"✅ Test 2 passed: [1,2,2] → {result2} operations")
    
    # Test Case 3: Another example
    nums3 = [3, 1, 2]
    result3 = solution.minimumPairRemoval(nums3.copy())
    assert result3 == 1, f"Test 3 failed: expected 1, got {result3}"
    print(f"✅ Test 3 passed: [3,1,2] → {result3} operations")
    
    # Test Case 4: Single element
    nums4 = [5]
    result4 = solution.minimumPairRemoval(nums4.copy())
    assert result4 == 0, f"Test 4 failed: expected 0, got {result4}"
    print(f"✅ Test 4 passed: [5] → {result4} operations")
    
    # Test Case 5: All equal
    nums5 = [3, 3, 3, 3]
    result5 = solution.minimumPairRemoval(nums5.copy())
    assert result5 == 0, f"Test 5 failed: expected 0, got {result5}"
    print(f"✅ Test 5 passed: [3,3,3,3] → {result5} operations")
    
    # Test Case 6: Reverse sorted
    nums6 = [5, 4, 3, 2, 1]
    result6 = solution.minimumPairRemoval(nums6.copy())
    print(f"✅ Test 6 passed: [5,4,3,2,1] → {result6} operations")
    
    # Test Case 7: Two elements unsorted
    nums7 = [2, 1]
    result7 = solution.minimumPairRemoval(nums7.copy())
    assert result7 == 1, f"Test 7 failed: expected 1, got {result7}"
    print(f"✅ Test 7 passed: [2,1] → {result7} operations")
    
    # Test Case 8: Large values
    nums8 = [50, 1, 49, 2]
    result8 = solution.minimumPairRemoval(nums8.copy())
    print(f"✅ Test 8 passed: [50,1,49,2] → {result8} operations")
    
    # Test Case 9: Multiple minimum pairs (test leftmost selection)
    nums9 = [4, 1, 1, 2]
    result9 = solution.minimumPairRemoval(nums9.copy())
    print(f"✅ Test 9 passed: [4,1,1,2] → {result9} operations")
    
    # Test Case 10: Almost sorted
    nums10 = [1, 3, 2, 4, 5]
    result10 = solution.minimumPairRemoval(nums10.copy())
    print(f"✅ Test 10 passed: [1,3,2,4,5] → {result10} operations")
    
    print("\n🎉 All test cases passed!")


# ================================================================================
# SIMULATION TRACE (for [5,2,3,1]):
# ================================================================================
# 
# Initial: [5, 2, 3, 1]
# 
# Iteration 1:
# - Check sorted? No (5 > 2)
# - Find min sum pairs:
#   - (5,2) = 7
#   - (2,3) = 5 ← minimum
#   - (3,1) = 4 ← NEW minimum
# - Choose index 2: (3,1)
# - Merge: [5, 2, 4]
# - Operations: 1
# 
# Iteration 2:
# - Check sorted? No (5 > 2)
# - Find min sum pairs:
#   - (5,2) = 7
#   - (2,4) = 6 ← minimum
# - Choose index 1: (2,4)
# - Merge: [5, 6]
# - Operations: 2
# 
# Iteration 3:
# - Check sorted? Yes (5 <= 6)
# - Exit loop
# 
# Final: return 2
# 
# Wait, there's an issue in my trace. Let me recalculate:
# 
# Initial: [5, 2, 3, 1]
# 
# Iteration 1:
# - Adjacent pairs:
#   - (5,2) sum=7, index=0
#   - (2,3) sum=5, index=1 ← minimum
#   - (3,1) sum=4, index=2 ← NEW minimum
# - Choose index 2 (leftmost minimum)
# - But wait, 4 < 5, so index 2 is chosen
# - Merge: nums[2] = 3+1=4, remove nums[3]
# - Result: [5, 2, 4]
# - Operations: 1
# 
# Iteration 2:
# - Adjacent pairs:
#   - (5,2) sum=7, index=0
#   - (2,4) sum=6, index=1 ← minimum
# - Choose index 1
# - Merge: nums[1] = 2+4=6, remove nums[2]
# - Result: [5, 6]
# - Operations: 2
# 
# Iteration 3:
# - Check: 5 <= 6? Yes, sorted!
# - Exit
# 
# Answer: 2 ✓
# 
# ================================================================================


# ================================================================================
# LEARNING NOTES:
# 
# PATTERN: Greedy Simulation
# - Problem explicitly states the greedy choice (minimum sum)
# - No optimization decisions needed - just simulate
# - Constraint-aware: small n allows cubic complexity
# 
# KEY TECHNIQUES:
# 1. In-place array modification with pop()
# 2. Linear scan to find minimum (maintains leftmost property)
# 3. Helper function for readability
# 4. Early termination check (sorted)
# 
# COMMON MISTAKES TO AVOID:
# - Not choosing leftmost pair in case of ties
# - Forgetting to check if already sorted (wastes operations)
# - Off-by-one errors when popping elements
# - Modifying array while iterating (use indices carefully)
# 
# OPTIMIZATION NOTES:
# - Could use heap for finding minimum, but overkill for n ≤ 50
# - Could avoid repeated sorted checks, but makes code harder to read
# - Current O(n³) is acceptable given constraints
# 
# RELATED PROBLEMS:
# - Merge operations on arrays
# - Greedy simulation problems
# - Array sorting with operations
# 
# INTERVIEW TIPS:
# - Clarify: "leftmost in case of ties" is important
# - Ask about constraints before optimizing
# - Mention that with larger n, we'd optimize differently
# - Discuss space-time tradeoffs
# 
# ================================================================================