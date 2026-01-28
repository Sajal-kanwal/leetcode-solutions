""""
================================================================================
Problem: 16. 3Sum Closest
Platform: LeetCode
URL: https://leetcode.com/problems/3sum-closest/
Difficulty: Medium
Topics: Array, Two Pointers, Sorting
================================================================================
PROBLEM DESCRIPTION:
Given an integer array nums of length n and an integer target,
find three integers in nums (distinct indices) whose sum is closest to target.

Return the sum of these three integers.

Assumption: Each input has exactly one solution (no need to handle multiple closest sums).

CONSTRAINTS:
- 3 <= nums.length <= 500
- -1000 <= nums[i] <= 1000
- -10^4 <= target <= 10^4

EXAMPLES:
Example 1:
Input: nums = [-1,2,1,-4], target = 1
Output: 2
Explanation: (-1 + 2 + 1) = 2 → closest to 1

Example 2:
Input: nums = [0,0,0], target = 1
Output: 0
Explanation: (0+0+0)=0 is closest possible
================================================================================
INTUITION:
Brute force = O(n³) → too slow for n=500

Better: Sort + Two Pointers (like 3Sum, but minimize |sum - target|)

Key steps:
1. Sort the array → O(n log n)
2. Fix one number (i from 0 to n-3)
3. Use two pointers (left = i+1, right = n-1) to find pair that makes sum closest
4. Track global minimum difference and corresponding sum
5. Skip duplicates if needed (but not strictly necessary here since we just want closest)

Time: O(n²) — acceptable for n ≤ 500
================================================================================
SOLUTION
================================================================================
"""

from typing import List

class Solution:
    def threeSumClosest(self, nums: List[int], target: int) -> int:
        """
        Find three numbers whose sum is closest to target using sorting + two pointers.
        
        Time:  O(n²)
        Space: O(1) or O(n) depending on sorting implementation
        """
        n = len(nums)
        nums.sort()  # crucial step
        
        closest_sum = nums[0] + nums[1] + nums[2]  # initial guess
        min_diff = abs(closest_sum - target)
        
        for i in range(n - 2):
            # Optional: skip duplicates for same i value
            if i > 0 and nums[i] == nums[i - 1]:
                continue
                
            left = i + 1
            right = n - 1
            
            while left < right:
                current_sum = nums[i] + nums[left] + nums[right]
                current_diff = abs(current_sum - target)
                
                # Update if closer
                if current_diff < min_diff:
                    min_diff = current_diff
                    closest_sum = current_sum
                
                # Early return if exact match (best possible)
                if current_sum == target:
                    return target
                
                # Move pointers based on sum vs target
                if current_sum < target:
                    left += 1
                else:
                    right -= 1
        
        return closest_sum


# =============================================================================
# TEST CASES
# =============================================================================
if __name__ == "__main__":
    solution = Solution()
    
    test_cases = [
        ([-1,2,1,-4], 1, 2, "Example 1: closest sum = 2"),
        ([0,0,0], 1, 0, "Example 2: all zeros"),
        ([1,2,3,4,5], 10, 9, "Largest three sum to 12, closest 9=1+3+5"),
        ([-4,-2,0,2,4], 0, 0, "Symmetric around zero"),
        ([-1,-1,-1,-1], -3, -3, "All same negative"),
        ([1,1,1,1], 4, 3, "All same positive"),
        ([-1000,-1000,-1000,1000], -1000, -2000, "Boundary values"),
    ]
    
    print("=" * 60)
    print("16. 3SUM CLOSEST - TEST CASES")
    print("=" * 60)
    
    passed = 0
    for nums, target, expected, desc in test_cases:
        result = solution.threeSumClosest(nums, target)
        if result == expected:
            print(f"✓ {desc:50} → {result}")
            passed += 1
        else:
            print(f"✗ {desc:50} → got {result}, expected {expected}")
    
    print(f"\n{passed}/{len(test_cases)} test cases passed")
    print("=" * 60)
"""Visualizations (Example 1: nums = [-1,2,1,-4], target = 1)
After sorting: [-4, -1, 1, 2]
i = 0, nums[0] = -4
→ left=1 (-1), right=3 (2) → sum = -4-1+2 = -3 → diff = | -3 - 1 | = 4
→ -3 < 1 → left++ → left=2 (1) → sum = -4+1+2 = -1 → diff = | -1 - 1 | = 2 (better)
→ -1 < 1 → left++ → end
i = 1, nums[1] = -1
→ left=2 (1), right=3 (2) → sum = -1+1+2 = 2 → diff = |2-1| = 1 (best so far!)
→ 2 > 1 → right-- → end
i = 2 → not enough elements left
Closest sum found = 2
Learning Notes – Key Insights & Patterns

Why sort first?
Sorting allows two-pointer technique to efficiently scan pairs for each fixed element.
Two-pointer movement logic
sum < target → increase sum → move left pointer right
sum > target → decrease sum → move right pointer left
This guarantees we explore all possible combinations without missing any

Early return optimization
If we ever hit exactly target → return immediately (best possible)
Difference tracking
We always keep track of minimum |sum - target| seen so far
→ update only when current_diff < min_diff
Duplicates
Skipping duplicates for i is optional (speeds up slightly)
Not needed for left/right because we just want closest, not all combinations

Common follow-ups
3Sum (LC 15): find all unique triplets that sum to 0 → need to skip duplicates carefully
4Sum → fix two elements + two pointers (O(n³))
k-Sum Closest → generalize with recursion or dynamic programming

Time & Space
Time: O(n log n) for sort + O(n²) for two-pointer loops → O(n²) overall
Space: O(1) extra (ignoring sort space)
"""