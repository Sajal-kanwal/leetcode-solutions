"""
================================================================================
Problem: 4. Median of Two Sorted Arrays
Platform: LeetCode
URL: https://leetcode.com/problems/median-of-two-sorted-arrays/
Difficulty: Hard
Topics: Array, Binary Search, Divide and Conquer
================================================================================

PROBLEM DESCRIPTION:
Given two sorted arrays nums1 and nums2 of size m and n respectively, return 
the median of the two sorted arrays.

The overall run time complexity should be O(log (m+n)).

CONSTRAINTS:
- nums1.length == m
- nums2.length == n
- 0 <= m <= 1000
- 0 <= n <= 1000
- 1 <= m + n <= 2000
- -10^6 <= nums1[i], nums2[i] <= 10^6

EXAMPLES:
Input: nums1 = [1,3], nums2 = [2]
Output: 2.00000
Explanation: merged array = [1,2,3] and median is 2.

Input: nums1 = [1,2], nums2 = [3,4]
Output: 2.50000
Explanation: merged array = [1,2,3,4] and median is (2 + 3) / 2 = 2.5.

================================================================================
INTUITION:
The naive approach of merging both arrays and finding the median would be O(m+n).
However, we can use binary search on the smaller array to partition both arrays
such that:
1. Left partition has (m+n+1)//2 elements
2. All elements in left partition <= all elements in right partition

This gives us O(log(min(m,n))) time complexity.

KEY INSIGHT:
We perform binary search on the SMALLER array to minimize operations. For each
partition of nums1, we can calculate the corresponding partition of nums2 to
ensure both halves have equal elements.

APPROACH:
1. Ensure nums1 is the smaller array (swap if needed)
2. Binary search on nums1 to find the correct partition
3. For each partition in nums1, calculate the corresponding partition in nums2
4. Check if partition is valid:
   - maxLeft1 <= minRight2 AND maxLeft2 <= minRight1
5. If valid:
   - Even total length: median = (max of left elements + min of right elements) / 2
   - Odd total length: median = min of right elements
6. If invalid:
   - If maxLeft1 > minRight2: search left half
   - Else: search right half

WHY BINARY SEARCH WORKS:
- If maxLeft1 > minRight2: we took too many elements from nums1, move left
- If maxLeft2 > minRight1: we took too few elements from nums1, move right
- The search space reduces by half each iteration

COMPLEXITY ANALYSIS:
- Time: O(log(min(m,n))) - binary search on smaller array
- Space: O(1) - only using constant extra space

EDGE CASES HANDLED:
- Empty array (one array can be empty)
- Single element arrays
- Arrays of vastly different sizes
- Even vs odd total length
- All elements in one array are smaller than the other

================================================================================
"""

from typing import List

class Solution:
    def findMedianSortedArrays(self, nums1: List[int], nums2: List[int]) -> float:
        # Ensure nums1 is the smaller array for optimization
        if len(nums1) > len(nums2):
            nums1, nums2 = nums2, nums1
        
        m, n = len(nums1), len(nums2)
        total_length = m + n
        half = total_length // 2  # Elements needed in left partition
        
        left, right = 0, m
        
        while left <= right:
            # Partition nums1
            partition1 = (left + right) // 2
            # Partition nums2 accordingly to maintain half elements on left
            partition2 = half - partition1
            
            # Get boundary elements (use infinity for out of bounds)
            max_left1 = float('-inf') if partition1 == 0 else nums1[partition1 - 1]
            min_right1 = float('inf') if partition1 == m else nums1[partition1]
            max_left2 = float('-inf') if partition2 == 0 else nums2[partition2 - 1]
            min_right2 = float('inf') if partition2 == n else nums2[partition2]
            
            # Check if partition is correct
            if max_left1 <= min_right2 and max_left2 <= min_right1:
                # Found the correct partition
                if total_length % 2 == 0:
                    # Even length: average of two middle elements
                    return (max(max_left1, max_left2) + min(min_right1, min_right2)) / 2.0
                else:
                    # Odd length: the smaller of the two right elements
                    return float(min(min_right1, min_right2))
            
            elif max_left1 > min_right2:
                # Too many elements from nums1, search left
                right = partition1 - 1
            else:
                # Too few elements from nums1, search right
                left = partition1 + 1
        
        # Should never reach here if inputs are valid
        return 0.0


# ================================================================================
# TEST CASES
# ================================================================================
if __name__ == "__main__":
    solution = Solution()
    
    # Test Case 1: Basic odd-length case
    assert solution.findMedianSortedArrays([1, 3], [2]) == 2.0
    print("✅ Test 1 passed: [1,3], [2] → 2.0")
    
    # Test Case 2: Basic even-length case
    assert solution.findMedianSortedArrays([1, 2], [3, 4]) == 2.5
    print("✅ Test 2 passed: [1,2], [3,4] → 2.5")
    
    # Test Case 3: Empty first array
    assert solution.findMedianSortedArrays([], [1]) == 1.0
    print("✅ Test 3 passed: [], [1] → 1.0")
    
    # Test Case 4: Empty second array
    assert solution.findMedianSortedArrays([2], []) == 2.0
    print("✅ Test 4 passed: [2], [] → 2.0")
    
    # Test Case 5: One array much larger
    assert solution.findMedianSortedArrays([1, 2], [3, 4, 5, 6, 7, 8]) == 4.5
    print("✅ Test 5 passed: [1,2], [3,4,5,6,7,8] → 4.5")
    
    # Test Case 6: All elements in nums1 smaller
    assert solution.findMedianSortedArrays([1, 2, 3], [4, 5, 6]) == 3.5
    print("✅ Test 6 passed: [1,2,3], [4,5,6] → 3.5")
    
    # Test Case 7: All elements in nums2 smaller
    assert solution.findMedianSortedArrays([4, 5, 6], [1, 2, 3]) == 3.5
    print("✅ Test 7 passed: [4,5,6], [1,2,3] → 3.5")
    
    # Test Case 8: Negative numbers
    assert solution.findMedianSortedArrays([-5, -3, -1], [0, 2, 4]) == -0.5
    print("✅ Test 8 passed: [-5,-3,-1], [0,2,4] → -0.5")
    
    # Test Case 9: Single element each
    assert solution.findMedianSortedArrays([100000], [100001]) == 100000.5
    print("✅ Test 9 passed: [100000], [100001] → 100000.5")
    
    # Test Case 10: Duplicates
    assert solution.findMedianSortedArrays([1, 1, 1], [1, 1, 1]) == 1.0
    print("✅ Test 10 passed: [1,1,1], [1,1,1] → 1.0")
    
    print("\n🎉 All test cases passed!")

# ================================================================================
# VISUALIZATION (for [1,3] and [2]):
#
# nums1: [1, 3]        partition1 = 1
# nums2: [2]           partition2 = 1
#
# Left partition:  [1] from nums1, [2] from nums2  → max = 2
# Right partition: [3] from nums1, [] from nums2   → min = 3
#
# Median (odd length) = min(right) = 3... wait, that's wrong in this visualization
#
# Actually:
# half = 3 // 2 = 1
# partition1 = 1: maxLeft1 = 1, minRight1 = 3
# partition2 = 1 - 1 = 0: maxLeft2 = -inf, minRight2 = 2
#
# maxLeft1 (1) <= minRight2 (2) ✓
# maxLeft2 (-inf) <= minRight1 (3) ✓
#
# Odd length: return min(minRight1, minRight2) = min(3, 2) = 2 ✓
# ================================================================================

# ================================================================================
# LEARNING NOTES:
# - This is one of the hardest binary search problems on LeetCode
# - Key insight: perform binary search on the SMALLER array
# - Always ensure left partition has correct number of elements
# - Use infinity values for boundary conditions (cleaner than multiple if-checks)
# - The partition indices can be tricky - draw it out!
# - Related problems: Kth Element of Two Sorted Arrays
# 
# COMMON MISTAKES TO AVOID:
# - Not ensuring nums1 is the smaller array (leads to index out of bounds)
# - Wrong calculation of partition2 (should be half - partition1, not half - partition1 + 1)
# - Not handling edge cases with -inf and +inf properly
# - Forgetting that for odd length, we return the MINIMUM of right elements
# ================================================================================