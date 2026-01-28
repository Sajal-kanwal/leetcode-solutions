"""
================================================================================
Problem: 704. Binary Search
Platform: LeetCode
URL: https://leetcode.com/problems/binary-search/
Difficulty: Easy
Topics: Binary Search, Array
================================================================================
PROBLEM DESCRIPTION:
Given a sorted array of integers nums (ascending order) and a target value,
return the index of target if it exists, otherwise return -1.

You must write an algorithm that runs in O(log n) time.

CONSTRAINTS:
- 1 <= nums.length <= 10^4
- -10^4 < nums[i], target < 10^4
- All integers in nums are unique
- nums is sorted in ascending order

EXAMPLES:
Example 1:
Input: nums = [-1,0,3,5,9,12], target = 9
Output: 4

Example 2:
Input: nums = [-1,0,3,5,9,12], target = 2
Output: -1
================================================================================
INTUITION:
Since the array is sorted and we need O(log n) time → classic binary search.

We maintain two pointers:
- left  = start of current search space
- right = end of current search space

At each step:
1. Find middle
2. If nums[mid] == target → found!
3. If nums[mid] < target → search right half
4. If nums[mid] > target → search left half

Repeat until left > right → not found

KEY POINTS:
- Use left <= right (most common and safe version)
- Update mid = left + (right - left) // 2 to avoid integer overflow
- When not found, loop ends naturally with left > right
================================================================================
SOLUTION
================================================================================
"""

from typing import List

class Solution:
    def search(self, nums: List[int], target: int) -> int:
        """
        Search target in sorted array using binary search.
        
        Time:  O(log n)
        Space: O(1)
        """
        left = 0
        right = len(nums) - 1
        
        while left <= right:
            mid = left + (right - left) // 2
            
            if nums[mid] == target:
                return mid
            
            if nums[mid] < target:
                left = mid + 1
            else:
                right = mid - 1
                
        return -1


# Alternative clean style (very popular on LeetCode)
class SolutionTwoPointerStyle:
    def search(self, nums: List[int], target: int) -> int:
        l, r = 0, len(nums) - 1
        
        while l <= r:
            m = l + (r - l) // 2
            
            if nums[m] > target:
                r = m - 1
            elif nums[m] < target:
                l = m + 1
            else:
                return m
                
        return -1


# =============================================================================
# TEST CASES
# =============================================================================
if __name__ == "__main__":
    solution = Solution()
    
    test_cases = [
        ([-1, 0, 3, 5, 9, 12], 9, 4, "Target exists in middle"),
        ([-1, 0, 3, 5, 9, 12], 2, -1, "Target not present"),
        ([5], 5, 0, "Single element - found"),
        ([2], 3, -1, "Single element - not found"),
        ([-1, 0, 3], -1, 0, "Target at start"),
        ([-1, 0, 3], 3, 2, "Target at end"),
        ([1,2,3,4,5,6,7,8,9], 1, 0, "First element"),
        ([1,2,3,4,5,6,7,8,9], 9, 8, "Last element"),
    ]
    
    print("=" * 60)
    print("704. BINARY SEARCH - TEST CASES")
    print("=" * 60)
    
    passed = 0
    for nums, target, expected, desc in test_cases:
        result = solution.search(nums, target)
        if result == expected:
            print(f"✓ {desc:50} → {result}")
            passed += 1
        else:
            print(f"✗ {desc:50} → got {result}, expected {expected}")
    
    print(f"\n{passed}/{len(test_cases)} test cases passed")
    print("=" * 60)
