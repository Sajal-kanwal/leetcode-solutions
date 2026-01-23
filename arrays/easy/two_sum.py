"""
================================================================================
Problem: 1. Two Sum
Platform: LeetCode
URL: https://leetcode.com/problems/two-sum/
Difficulty: Easy
Topics: Array, Hash Table
================================================================================

PROBLEM DESCRIPTION:
Given an array of integers nums and an integer target, return indices of the 
two numbers such that they add up to target.

You may assume that each input would have exactly one solution, and you may 
not use the same element twice.

You can return the answer in any order.

CONSTRAINTS:
- 2 <= nums.length <= 10^4
- -10^9 <= nums[i] <= 10^9
- -10^9 <= target <= 10^9
- Only one valid answer exists

EXAMPLES:
Input: nums = [2,7,11,15], target = 9
Output: [0,1]
Explanation: Because nums[0] + nums[1] == 9, we return [0, 1].

Input: nums = [3,2,4], target = 6
Output: [1,2]

Input: nums = [3,3], target = 6
Output: [0,1]

================================================================================
INTUITION:
The brute force approach would check every pair of numbers (O(n²)). However,
we can optimize using a hash map to achieve O(n) time complexity.

KEY INSIGHT:
For each number, we need to find if (target - current_number) exists in the
array. Instead of searching the entire array each time, we can use a hash map
to store numbers we've already seen with their indices.

APPROACH:
1. Create a hash map to store: {number → index}
2. For each element in the array:
   - Calculate complement = target - current_number
   - Check if complement exists in hash map
   - If yes: return [complement_index, current_index]
   - If no: add current number to hash map
3. Continue until we find the pair

WHY HASH MAP WORKS:
- Hash map provides O(1) average lookup time
- We only need one pass through the array
- We build the hash map as we go, so we don't revisit elements

COMPLEXITY ANALYSIS:
- Time: O(n) - single pass through array with O(1) hash map operations
- Space: O(n) - hash map storage in worst case (all elements stored)

EDGE CASES HANDLED:
- Duplicate values in array (hash map stores most recent index)
- Negative numbers (work seamlessly)
- Zero in array or target
- Target can be positive, negative, or zero
- Solution always exists (per problem constraints)

================================================================================
"""

from typing import List

class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        """
        Find indices of two numbers that add up to target.
        
        Args:
            nums: Array of integers
            target: Target sum
            
        Returns:
            List of two indices [i, j] where nums[i] + nums[j] == target
            
        Algorithm: Hash Map (One-Pass)
        Time: O(n) - single iteration through array
        Space: O(n) - hash map storage
        
        Key Insight:
        Instead of checking all pairs (O(n²)), we use a hash map to
        remember previously seen numbers and their indices.
        """
        
        # Hash map to store: {number: index}
        seen = {}
        
        # Iterate through array with indices
        for i, num in enumerate(nums):
            # Calculate what number we need to find
            complement = target - num
            
            # Check if complement exists in hash map
            if complement in seen:
                # Found the pair! Return indices
                return [seen[complement], i]
            
            # Store current number with its index for future lookups
            seen[num] = i
        
        # No solution found (shouldn't happen per problem constraints)
        return [-1, -1]


# ================================================================================
# ALTERNATIVE SOLUTIONS
# ================================================================================

class SolutionBruteForce:
    """
    Brute Force Approach - For Comparison
    
    Time: O(n²) - nested loops
    Space: O(1) - no extra space
    """
    
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        """
        Check all possible pairs.
        
        Not optimal, but demonstrates the naive approach.
        """
        n = len(nums)
        
        for i in range(n):
            for j in range(i + 1, n):
                if nums[i] + nums[j] == target:
                    return [i, j]
        
        return [-1, -1]


class SolutionTwoPass:
    """
    Two-Pass Hash Map Approach
    
    Time: O(n) - two passes through array
    Space: O(n) - hash map storage
    """
    
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        """
        Build complete hash map first, then search.
        
        Less efficient than one-pass, but easier to understand.
        """
        # First pass: build hash map
        num_to_index = {num: i for i, num in enumerate(nums)}
        
        # Second pass: find complement
        for i, num in enumerate(nums):
            complement = target - num
            
            # Check if complement exists and is not the same element
            if complement in num_to_index and num_to_index[complement] != i:
                return [i, num_to_index[complement]]
        
        return [-1, -1]


# ================================================================================
# TEST CASES
# ================================================================================
if __name__ == "__main__":
    solution = Solution()
    
    # Test Case 1: Example from problem
    nums1 = [2, 7, 11, 15]
    target1 = 9
    result1 = solution.twoSum(nums1, target1)
    assert sorted(result1) == [0, 1], f"Test 1 failed: {result1}"
    print(f"✅ Test 1 passed: nums={nums1}, target={target1} → {result1}")
    
    # Test Case 2: Different order
    nums2 = [3, 2, 4]
    target2 = 6
    result2 = solution.twoSum(nums2, target2)
    assert sorted(result2) == [1, 2], f"Test 2 failed: {result2}"
    print(f"✅ Test 2 passed: nums={nums2}, target={target2} → {result2}")
    
    # Test Case 3: Duplicates
    nums3 = [3, 3]
    target3 = 6
    result3 = solution.twoSum(nums3, target3)
    assert sorted(result3) == [0, 1], f"Test 3 failed: {result3}"
    print(f"✅ Test 3 passed: nums={nums3}, target={target3} → {result3}")
    
    # Test Case 4: Negative numbers
    nums4 = [-1, -2, -3, -4, -5]
    target4 = -8
    result4 = solution.twoSum(nums4, target4)
    assert sorted(result4) == [2, 4], f"Test 4 failed: {result4}"
    print(f"✅ Test 4 passed: nums={nums4}, target={target4} → {result4}")
    
    # Test Case 5: Zero target
    nums5 = [0, 4, 3, 0]
    target5 = 0
    result5 = solution.twoSum(nums5, target5)
    assert sorted(result5) == [0, 3], f"Test 5 failed: {result5}"
    print(f"✅ Test 5 passed: nums={nums5}, target={target5} → {result5}")
    
    # Test Case 6: Negative target
    nums6 = [-3, 4, 3, 90]
    target6 = 0
    result6 = solution.twoSum(nums6, target6)
    assert sorted(result6) == [0, 2], f"Test 6 failed: {result6}"
    print(f"✅ Test 6 passed: nums={nums6}, target={target6} → {result6}")
    
    # Test Case 7: Large numbers
    nums7 = [1000000, 2000000, 3000000]
    target7 = 3000000
    result7 = solution.twoSum(nums7, target7)
    assert sorted(result7) == [0, 1], f"Test 7 failed: {result7}"
    print(f"✅ Test 7 passed: nums={nums7}, target={target7} → {result7}")
    
    # Test Case 8: Answer at end
    nums8 = [1, 2, 3, 4, 5]
    target8 = 9
    result8 = solution.twoSum(nums8, target8)
    assert sorted(result8) == [3, 4], f"Test 8 failed: {result8}"
    print(f"✅ Test 8 passed: nums={nums8}, target={target8} → {result8}")
    
    # Test Case 9: Two elements only
    nums9 = [5, 10]
    target9 = 15
    result9 = solution.twoSum(nums9, target9)
    assert sorted(result9) == [0, 1], f"Test 9 failed: {result9}"
    print(f"✅ Test 9 passed: nums={nums9}, target={target9} → {result9}")
    
    # Test Case 10: Negative and positive
    nums10 = [-5, 10, 3, -3]
    target10 = 0
    result10 = solution.twoSum(nums10, target10)
    assert sorted(result10) == [2, 3], f"Test 10 failed: {result10}"
    print(f"✅ Test 10 passed: nums={nums10}, target={target10} → {result10}")
    
    print("\n🎉 All test cases passed!")
    
    # Performance comparison
    print("\n" + "="*60)
    print("PERFORMANCE COMPARISON")
    print("="*60)
    
    import time
    
    # Test with larger array
    large_nums = list(range(10000))
    large_target = 19999
    
    # Hash Map Solution (Optimal)
    start = time.perf_counter()
    for _ in range(100):
        solution.twoSum(large_nums.copy(), large_target)
    hash_time = time.perf_counter() - start
    print(f"Hash Map (Optimal):  {hash_time:.6f} seconds")
    
    # Brute Force Solution (Slow)
    brute = SolutionBruteForce()
    start = time.perf_counter()
    for _ in range(1):  # Only 1 iteration - too slow otherwise
        brute.twoSum(large_nums.copy(), large_target)
    brute_time = time.perf_counter() - start
    print(f"Brute Force (Slow):  {brute_time:.6f} seconds (1 iteration)")
    
    print(f"\nHash Map is ~{int(brute_time * 100 / hash_time)}x faster!")


# ================================================================================
# STEP-BY-STEP VISUALIZATION (for nums=[2,7,11,15], target=9):
# ================================================================================
#
# Initial state:
# seen = {}
# target = 9
#
# Iteration 1: i=0, num=2
# ├─ complement = 9 - 2 = 7
# ├─ Is 7 in seen? No
# └─ Add to seen: {2: 0}
#
# Iteration 2: i=1, num=7
# ├─ complement = 9 - 7 = 2
# ├─ Is 2 in seen? Yes! ✓
# ├─ seen[2] = 0
# └─ Return [0, 1]
#
# Answer: [0, 1] ✓
#
# ================================================================================


# ================================================================================
# STEP-BY-STEP VISUALIZATION (for nums=[3,3], target=6):
# ================================================================================
#
# Initial state:
# seen = {}
# target = 6
#
# Iteration 1: i=0, num=3
# ├─ complement = 6 - 3 = 3
# ├─ Is 3 in seen? No
# └─ Add to seen: {3: 0}
#
# Iteration 2: i=1, num=3
# ├─ complement = 6 - 3 = 3
# ├─ Is 3 in seen? Yes! ✓
# ├─ seen[3] = 0
# └─ Return [0, 1]
#
# Answer: [0, 1] ✓
#
# Note: This works because we check BEFORE adding to hash map.
# If we checked AFTER, we'd incorrectly return [1, 1] (same element twice).
#
# ================================================================================


# ================================================================================
# LEARNING NOTES:
# ================================================================================
#
# PATTERN: Hash Map for O(1) Lookup
# This is one of the most fundamental patterns in algorithm design.
# 
# KEY INSIGHT:
# "Can I trade space for time?"
# - Brute force: O(n²) time, O(1) space
# - Hash map: O(n) time, O(n) space
# 
# WHEN TO USE THIS PATTERN:
# - Need to find pairs, triplets, or complements
# - Looking for "target sum" problems
# - Want to avoid nested loops
# - Can afford O(n) extra space
# 
# COMMON VARIATIONS:
# 1. Two Sum (this problem)
# 2. Two Sum II - Sorted Array (use two pointers instead)
# 3. 3Sum (sort + two pointers)
# 4. 4Sum (sort + two pointers with outer loops)
# 5. Two Sum IV - BST (in-order traversal + hash set)
# 
# WHY CHECK BEFORE ADDING?
# Consider nums = [3,3], target = 6:
# 
# Correct (check first, add later):
# - i=0: check for 3 in seen (not found), add 3
# - i=1: check for 3 in seen (found!), return [0,1] ✓
# 
# Wrong (add first, check later):
# - i=0: add 3 to seen, check for 3 in seen (found!)
# - Would incorrectly return [0,0] ✗
# 
# INTERVIEW TIPS:
# 1. Always clarify if solution exists (affects return value)
# 2. Ask about duplicates (can same value appear twice?)
# 3. Discuss space-time tradeoff
# 4. Mention that if array were sorted, two pointers work (O(1) space)
# 5. Consider follow-up: "What if there are multiple solutions?"
# 
# COMMON MISTAKES:
# - Using same element twice (checking after adding to map)
# - Not handling negative numbers correctly
# - Forgetting that hash map stores most recent index for duplicates
# - Returning [i, i] instead of [-1, -1] when no solution
# 
# OPTIMIZATION NOTES:
# - One-pass is optimal (better than two-pass)
# - Can't do better than O(n) time without sorting
# - If sorted, two pointers gives O(1) space but O(n log n) time to sort
# 
# RELATED PROBLEMS:
# - LC 167: Two Sum II - Input Array Is Sorted (two pointers)
# - LC 15: 3Sum (sort + two pointers)
# - LC 18: 4Sum
# - LC 454: 4Sum II (hash map variation)
# - LC 560: Subarray Sum Equals K (prefix sum + hash map)
# 
# REAL-WORLD APPLICATIONS:
# - Database joins (hash joins)
# - Finding matching records
# - Recommendation systems (collaborative filtering)
# - Network packet matching
# 
# ================================================================================