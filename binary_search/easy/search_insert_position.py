"""
================================================================================
Problem: 35. Search Insert Position
Platform: LeetCode
URL: https://leetcode.com/problems/search-insert-position/
Difficulty: Easy
Topics: Binary Search, Array
================================================================================
PROBLEM DESCRIPTION:
Given a sorted array of distinct integers nums and a target value,
return the index if the target is found.
If not, return the index where it would be if it were inserted in order.

You must write an algorithm with O(log n) runtime complexity.

CONSTRAINTS:
- 1 <= nums.length <= 10^4
- -10^4 <= nums[i] <= 10^4
- nums contains distinct values sorted in ascending order
- -10^4 <= target <= 10^4

EXAMPLES:
Example 1:
Input: nums = [1,3,5,6], target = 5
Output: 2

Example 2:
Input: nums = [1,3,5,6], target = 2
Output: 1

Example 3:
Input: nums = [1,3,5,6], target = 7
Output: 4
================================================================================
INTUITION:
This is a classic binary search variation — we want the insertion point.

Key insight:
- When target is not found, the loop ends with left pointing to the smallest index
  where nums[left] >= target (or left == len(nums) if target is larger than all elements)
- This is exactly the insertion position we need!

So we can reuse the standard binary search template, and at the end:
→ if found → return mid
→ if not found → return left (which is the correct insertion index)

This is the most elegant and commonly used solution in interviews.
================================================================================
SOLUTION
================================================================================
"""

from typing import List

class Solution:
    def searchInsert(self, nums: List[int], target: int) -> int:
        """
        Find the insertion position to keep array sorted using binary search.
        
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
        
        # When loop ends, left is the correct insertion position
        return left


# Alternative style (very clean and popular)
class SolutionClean:
    def searchInsert(self, nums: List[int], target: int) -> int:
        l, r = 0, len(nums)
        
        while l < r:
            m = l + (r - l) // 2
            if nums[m] < target:
                l = m + 1
            else:
                r = m
                
        return l


# =============================================================================
# TEST CASES
# =============================================================================
if __name__ == "__main__":
    solution = Solution()
    
    test_cases = [
        ([1,3,5,6], 5, 2, "Found in array"),
        ([1,3,5,6], 2, 1, "Insert between 1 and 3"),
        ([1,3,5,6], 7, 4, "Insert after last element"),
        ([1,3,5,6], 0, 0, "Insert before first element"),
        ([1], 0, 0, "Single element - smaller"),
        ([1], 1, 0, "Single element - equal"),
        ([1], 2, 1, "Single element - larger"),
        ([1,2,3,4,5], 3, 2, "Found in middle"),
        ([1,2,3,4,5], 6, 5, "Larger than all"),
    ]
    
    print("=" * 60)
    print("35. SEARCH INSERT POSITION - TEST CASES")
    print("=" * 60)
    
    passed = 0
    for nums, target, expected, desc in test_cases:
        result = solution.searchInsert(nums, target)
        if result == expected:
            print(f"✓ {desc:50} → {result}")
            passed += 1
        else:
            print(f"✗ {desc:50} → got {result}, expected {expected}")
    
    print(f"\n{passed}/{len(test_cases)} test cases passed")
    print("=" * 60)

"""

Visualizations

Case 1: Target exists in array  
nums = [1, 3, 5, 6], target = 5

```
 indices:   0   1   2   3
 values:   [1,  3,  5,  6]

Initial:   l           r
           ↑           ↑

mid = 1 → 3 < 5 → l = 2

           l     r
                 ↑

mid = 2 → 5 == 5 → return 2

Result: 2

#### Case 2: Target should be inserted between two elements  
nums = [1, 3, 5, 6], target = 2

```
 indices:   0   1   2   3
 values:   [1,  3,  5,  6]

Initial:   l           r

mid = 1 → 3 > 2 → r = 0

           l     r
           ↑     ↑

mid = 0 → 1 < 2 → l = 1

                 l
                 ↑   (loop ends)

return l → 1

Result: 1 (insert position before 3)

#### Case 3: Target larger than all elements  
nums = [1, 3, 5, 6], target = 7

```
 indices:   0   1   2   3
 values:   [1,  3,  5,  6]

Initial:   l           r

mid = 1 → 3 < 7 → l = 2

                 l     r

mid = 2 → 5 < 7 → l = 3

                       l     r

mid = 3 → 6 < 7 → l = 4

                             l   (l == len(nums))

return l → 4


Result: 4 (append position)

#### Case 4: Target smaller than all elements  
nums = [1, 3, 5, 6], target = 0

```
 indices:   0   1   2   3
 values:   [1,  3,  5,  6]

Initial:   l           r

mid = 1 → 3 > 0 → r = 0

           l     r

mid = 0 → 1 > 0 → r = -1

     l
     ↑   (l > r)

return l → 0


Result: 0 (insert at beginning)

Common Binary Search Template Comparison

| Problem                          | Goal                              | Return when not found       | Loop condition   | Final return when not found |
|:---------------------------------|:----------------------------------|:----------------------------|:-----------------|:----------------------------|
| LC 704 Binary Search             | find exact match                  | -1                          | `left <= right`  | -1                          |
| LC 35  Search Insert Position    | find exact or insert position     | insertion index             | `left <= right`  | `left`                      |
| lower_bound (C++ style)          | first ≥ target                    | insertion point             | `left < right`   | `left`                      |
| upper_bound (C++ style)          | first > target                    | insertion point             | `left < right`   | `left`                      |

### Learning Notes – Key Insights & Patterns

1. **The magic of `left` at the end**  
   When using the `left <= right` template and always moving `left = mid + 1` or `right = mid - 1`,  
   → at the moment the loop ends (`left > right`),  
   `left` is the **smallest index** where `nums[left] >= target`  
   (or `len(nums)` if target is larger than everything)

   This single property is why the same template solves both:
   - classic binary search (LC 704)
   - search insert position (LC 35)
   - lower_bound behavior

2. **Two most popular loop styles**

   **Style A – most interview-friendly (used above)**

   ```python
   left, right = 0, len(nums) - 1
   while left <= right:
       mid = left + (right - left) // 2
       if nums[mid] < target:
           left = mid + 1
       else:
           right = mid - 1
   return left
   ```

   **Style B – exclusive right boundary (also very clean)**

   ```python
   left, right = 0, len(nums)
   while left < right:
       mid = left + (right - left) // 2
       if nums[mid] < target:
           left = mid + 1
       else:
           right = mid
   return left
   ```

   Both give the same result for search-insert.

3. **Why `mid = left + (right - left) // 2` instead of `(left + right) // 2`?**

   - prevents integer overflow in languages like Java/C++ when `left` and `right` are large
   - in Python it's not dangerous (unlimited int), but it's good habit & shows awareness

4. **When to prefer which variant in interviews**

   | Situation                              | Recommended style          | Why?                                   |
   |:---------------------------------------|:---------------------------|:---------------------------------------|
   | Asked for "binary search"              | `left <= right`            | most people learned it this way        |
   | Asked for "insertion point" / lower_bound | either (both accepted)   | both correct & clean                   |
   | Very strict time constraints           | `left < right` sometimes   | slightly fewer comparisons in practice |
   | Want to be very explicit               | `left <= right` + comment  | clearest intent                        |

5. **Common follow-up questions**

   - How would you modify it to find the last position ≤ target? (upper bound - 1)
   - What if array can have duplicates? → need to decide leftmost or rightmost
   - How to implement it recursively?
   - How to find first bad version? (LC 278 – almost identical pattern)

"""