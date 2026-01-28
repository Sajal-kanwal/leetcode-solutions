"""
================================================================================
Problem: 26. Remove Duplicates from Sorted Array
Platform: LeetCode
URL: https://leetcode.com/problems/remove-duplicates-from-sorted-array/
Difficulty: Easy
Topics: Array, Two Pointers
================================================================================

PROBLEM DESCRIPTION:
Given an integer array nums sorted in non-decreasing order, remove the duplicates
in-place such that each unique element appears only once. The relative order of 
the elements should be kept the same. Then return the number of unique elements 
in nums.

Consider the number of unique elements of nums to be k, to get accepted, you 
need to do the following things:
- Change the array nums such that the first k elements contain the unique elements
- Return k

CONSTRAINTS:
- 1 <= nums.length <= 3 * 10^4
- -100 <= nums[i] <= 100
- nums is sorted in non-decreasing order

EXAMPLES:

Example 1:
Input: nums = [1,1,2]
Output: 2, nums = [1,2,_]
Explanation: Your function should return k = 2, with the first two elements of 
nums being 1 and 2 respectively. It does not matter what you leave beyond the 
returned k.

Example 2:
Input: nums = [0,0,1,1,1,2,2,3,3,4]
Output: 5, nums = [0,1,2,3,4,_,_,_,_,_]
Explanation: Your function should return k = 5, with the first five elements of 
nums being 0, 1, 2, 3, and 4 respectively.

================================================================================
INTUITION:
Since the array is already sorted, all duplicates are adjacent. We can use two
pointers to keep track of:
1. Where to write the next unique element (slow pointer)
2. Current element we're examining (fast pointer)

KEY INSIGHT:
In a sorted array, duplicates are always consecutive. We only need to check if
current element differs from the previous one.

APPROACH: Two Pointers (Slow & Fast)
1. Slow pointer: tracks position where next unique element should be placed
2. Fast pointer: scans through the array
3. When we find a new unique element, place it at slow position and advance slow

WHY IT WORKS:
- First element is always unique (no comparison needed)
- For each element, compare with previous element
- If different, it's a new unique element → copy to slow position
- If same, skip it (fast moves forward, slow stays)

COMPLEXITY ANALYSIS:
- Time: O(n) - single pass through array
- Space: O(1) - only using two pointers, modifying in-place

EDGE CASES HANDLED:
- Empty array (though constraints say length >= 1)
- Single element array
- All elements identical
- All elements unique
- Negative numbers

================================================================================
"""

from typing import List


class Solution:
    """LC 26: Remove Duplicates from Sorted Array"""
    
    def removeDuplicates(self, nums: List[int]) -> int:
        """
        Remove duplicates in-place and return count of unique elements.
        
        Args:
            nums: Sorted array of integers (modified in-place)
            
        Returns:
            Number of unique elements
            
        Algorithm: Two Pointers
        Time: O(n)
        Space: O(1)
        """
        # Edge case: empty or single element
        if len(nums) <= 1:
            return len(nums)
        
        # Slow pointer: position to write next unique element
        # Start at 1 because index 0 is always kept
        slow = 1
        
        # Fast pointer: scan through array
        for fast in range(1, len(nums)):
            # Found a new unique element
            # (different from previous element in original array)
            if nums[fast] != nums[fast - 1]:
                nums[slow] = nums[fast]
                slow += 1
        
        # slow now points to the position after last unique element
        # which equals the count of unique elements
        return slow


class SolutionAlternative:
    """Alternative: Compare with last unique element"""
    
    def removeDuplicates(self, nums: List[int]) -> int:
        """
        Alternative approach: compare with last written unique element.
        
        Slightly different but equivalent logic.
        """
        if len(nums) <= 1:
            return len(nums)
        
        slow = 1
        
        for fast in range(1, len(nums)):
            # Compare with last written unique element
            # (at position slow-1)
            if nums[fast] != nums[slow - 1]:
                nums[slow] = nums[fast]
                slow += 1
        
        return slow


class SolutionVerbose:
    """Heavily commented version for learning"""
    
    def removeDuplicates(self, nums: List[int]) -> int:
        """
        Remove duplicates with detailed step-by-step logic.
        """
        n = len(nums)
        
        # Edge case
        if n <= 1:
            return n
        
        # Initialize pointers
        # slow: next position to write unique element
        # fast: current element being examined
        slow = 1  # Start at 1 since nums[0] is always unique
        
        # Scan through array with fast pointer
        for fast in range(1, n):
            # Check if current element is different from previous
            # Since array is sorted, duplicates are consecutive
            if nums[fast] != nums[fast - 1]:
                # Found a new unique element
                # Write it to slow position
                nums[slow] = nums[fast]
                
                # Move slow forward to next write position
                slow += 1
                
                # Implicit: fast moves forward automatically (loop)
        
        # At this point:
        # - nums[0:slow] contains all unique elements in order
        # - slow equals the count of unique elements
        return slow


class SolutionWithoutExtraComparison:
    """
    More intuitive: compare current with last unique
    This is actually the same as your original solution!
    """
    
    def removeDuplicates(self, nums: List[int]) -> int:
        """
        Your original solution - already optimal!
        """
        if len(nums) <= 1:
            return len(nums)
        
        slow = 1
        
        for fast in range(1, len(nums)):
            # This comparison (nums[fast] != nums[fast-1]) is elegant
            # because in a sorted array, if current != previous,
            # then current is guaranteed to be unique so far
            if nums[fast] != nums[fast - 1]:
                nums[slow] = nums[fast]
                slow += 1
        
        return slow


# ================================================================================
# TEST CASES
# ================================================================================
if __name__ == "__main__":
    solution = Solution()
    
    test_cases = [
        # (input, expected_k, expected_array_prefix, description)
        (
            [1, 1, 2],
            2,
            [1, 2],
            "Example 1: Two duplicates"
        ),
        (
            [0, 0, 1, 1, 1, 2, 2, 3, 3, 4],
            5,
            [0, 1, 2, 3, 4],
            "Example 2: Many duplicates"
        ),
        (
            [1],
            1,
            [1],
            "Single element"
        ),
        (
            [1, 2, 3, 4, 5],
            5,
            [1, 2, 3, 4, 5],
            "All unique elements"
        ),
        (
            [1, 1, 1, 1, 1],
            1,
            [1],
            "All same elements"
        ),
        (
            [1, 1, 2, 2, 3, 3],
            3,
            [1, 2, 3],
            "All pairs"
        ),
        (
            [-3, -1, 0, 0, 0, 3, 3],
            4,
            [-3, -1, 0, 3],
            "Negative numbers"
        ),
        (
            [1, 1, 1, 2, 2, 2, 3, 3, 3],
            3,
            [1, 2, 3],
            "Triples"
        ),
    ]
    
    print("=" * 80)
    print("TESTING REMOVE DUPLICATES FROM SORTED ARRAY")
    print("=" * 80)
    print()
    
    passed = 0
    for nums, expected_k, expected_prefix, description in test_cases:
        # Make a copy for testing
        nums_copy = nums.copy()
        
        # Run solution
        result_k = solution.removeDuplicates(nums_copy)
        
        # Check result
        k_correct = result_k == expected_k
        prefix_correct = nums_copy[:result_k] == expected_prefix
        
        if k_correct and prefix_correct:
            print(f"✅ {description}")
            print(f"   Input: {nums}")
            print(f"   Output: k={result_k}, nums={nums_copy[:result_k]}")
            passed += 1
        else:
            print(f"❌ {description}")
            print(f"   Input: {nums}")
            print(f"   Expected: k={expected_k}, nums={expected_prefix}")
            print(f"   Got: k={result_k}, nums={nums_copy[:result_k]}")
            if not k_correct:
                print(f"   ⚠️  k mismatch!")
            if not prefix_correct:
                print(f"   ⚠️  array prefix mismatch!")
        print()
    
    print("=" * 80)
    print(f"RESULTS: {passed}/{len(test_cases)} tests passed")
    print("=" * 80)


# ================================================================================
# VISUALIZATION: Step-by-Step Execution
# ================================================================================
"""
Example: nums = [0, 0, 1, 1, 1, 2, 2, 3, 3, 4]

Initial state:
Index:  0  1  2  3  4  5  6  7  8  9
Value:  0  0  1  1  1  2  2  3  3  4
        ↑
       slow
       fast

Step-by-step execution:

Step 0: slow=1, fast=1
  nums[1]=0 == nums[0]=0 → duplicate, skip
  slow=1

Step 1: slow=1, fast=2
  nums[2]=1 != nums[1]=0 → unique!
  nums[1] = 1
  slow=2
  Array: [0, 1, 1, 1, 1, 2, 2, 3, 3, 4]
              ↑
             slow

Step 2: slow=2, fast=3
  nums[3]=1 == nums[2]=1 → duplicate, skip
  slow=2

Step 3: slow=2, fast=4
  nums[4]=1 == nums[3]=1 → duplicate, skip
  slow=2

Step 4: slow=2, fast=5
  nums[5]=2 != nums[4]=1 → unique!
  nums[2] = 2
  slow=3
  Array: [0, 1, 2, 1, 1, 2, 2, 3, 3, 4]
                 ↑
                slow

Step 5: slow=3, fast=6
  nums[6]=2 == nums[5]=2 → duplicate, skip
  slow=3

Step 6: slow=3, fast=7
  nums[7]=3 != nums[6]=2 → unique!
  nums[3] = 3
  slow=4
  Array: [0, 1, 2, 3, 1, 2, 2, 3, 3, 4]
                    ↑
                   slow

Step 7: slow=4, fast=8
  nums[8]=3 == nums[7]=3 → duplicate, skip
  slow=4

Step 8: slow=4, fast=9
  nums[9]=4 != nums[8]=3 → unique!
  nums[4] = 4
  slow=5
  Array: [0, 1, 2, 3, 4, 2, 2, 3, 3, 4]
                       ↑
                      slow

Final result:
  k = slow = 5
  First 5 elements: [0, 1, 2, 3, 4] ✓
  Remaining elements don't matter
"""


# ================================================================================
# LEARNING NOTES
# ================================================================================
"""
PATTERN: Two Pointers (Slow & Fast)

This is one of the most fundamental two-pointer patterns for array manipulation.

KEY CONCEPTS:

1. In-Place Modification
   - Don't create new array
   - Modify the input array directly
   - Space complexity: O(1)

2. Two Pointer Roles
   - Slow (write pointer): where to place next unique element
   - Fast (read pointer): current element being examined

3. Why This Works in Sorted Arrays
   - Duplicates are ALWAYS adjacent
   - Only need to compare consecutive elements
   - Don't need to look ahead or behind

SIMILAR PROBLEMS (Same Pattern):

1. LC 27: Remove Element
   - Remove specific value instead of duplicates
   - Same two-pointer technique

2. LC 80: Remove Duplicates from Sorted Array II
   - Allow at most 2 duplicates
   - Slight modification: compare with nums[slow-2]

3. LC 283: Move Zeroes
   - Move zeros to end
   - Two-pointer swap pattern

4. LC 844: Backspace String Compare
   - Process strings with backspace
   - Two-pointer with stack simulation

VARIATIONS OF THIS PROBLEM:

Keep at most k duplicates:
```python
def removeDuplicates(nums, k):
    slow = 0
    for fast in range(len(nums)):
        if slow < k or nums[fast] != nums[slow - k]:
            nums[slow] = nums[fast]
            slow += 1
    return slow
```

Remove ALL duplicates (keep only unique):
```python
def removeAllDuplicates(nums):
    if not nums:
        return 0
    
    slow = 0
    fast = 0
    
    while fast < len(nums):
        # Count occurrences
        start = fast
        while fast < len(nums) and nums[fast] == nums[start]:
            fast += 1
        
        # If appears exactly once, keep it
        if fast - start == 1:
            nums[slow] = nums[start]
            slow += 1
    
    return slow
```

COMMON MISTAKES:

❌ Starting slow at 0
   - First element is always unique, start slow at 1

❌ Comparing nums[fast] != nums[slow]
   - Should compare consecutive elements: nums[fast] != nums[fast-1]
   - Or compare with last written: nums[fast] != nums[slow-1]

❌ Returning slow - 1
   - slow points to position AFTER last unique element
   - This equals the count, so return slow directly

❌ Not handling edge cases
   - Empty array (though constraints say length >= 1)
   - Single element

❌ Modifying array while reading
   - The two-pointer approach handles this correctly
   - slow writes, fast reads - no conflict

INTERVIEW TIPS:

1. Clarify In-Place Requirement
   "Should I modify the array in-place or can I create a new one?"

2. Explain the Pattern
   "I'll use two pointers: slow for writing unique elements, fast for reading"

3. Walk Through Example
   Show the array state after each step

4. Discuss Edge Cases
   - Single element
   - All same
   - All unique

5. Mention Time/Space
   "This is O(n) time with O(1) extra space"

6. Follow-up Questions
   Be ready for variations:
   - "What if we allow at most 2 duplicates?" (LC 80)
   - "What if array is not sorted?" (use hash set, can't use two pointers)

OPTIMIZATION NOTES:

Already Optimal:
- Can't do better than O(n) time (must examine each element)
- Can't do better than O(1) space (in-place requirement)

Early Termination:
- Could check if no duplicates exist first
- But would still be O(n) to check, so no real benefit

WHY YOUR SOLUTION IS EXCELLENT:

✅ Correct logic
✅ Optimal complexity
✅ Clean and readable
✅ Handles all edge cases
✅ Uses comparison with nums[fast-1] (slightly more intuitive than nums[slow-1])

The comparison `nums[fast] != nums[fast-1]` is elegant because:
- In sorted array, if current != previous, it's definitely unique so far
- No need to maintain extra state
- Very intuitive to understand

REAL-WORLD APPLICATIONS:

- Data deduplication in databases
- Log file processing (remove duplicate entries)
- Stream processing (remove consecutive duplicates)
- Array compression
- Unique element extraction from sorted data

COMPLEXITY ANALYSIS DEEP DIVE:

Time: O(n)
- Single pass: fast goes from 1 to n-1
- Each iteration: O(1) comparison and assignment
- Total: O(n)

Space: O(1)
- Only two integer variables (slow, fast)
- Loop variable doesn't count
- Array is modified in-place

Best case: O(n) - all unique, still need to scan
Worst case: O(n) - all same, still need to scan
Average case: O(n) - always linear

This is a perfectly optimal solution! 🎉
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
    
    solution = Solution()
    
    test_sizes = [100, 1000, 10000, 30000]
    
    for size in test_sizes:
        # Generate sorted array with duplicates
        # Each number appears 1-5 times
        nums = []
        current = 0
        while len(nums) < size:
            repeat = random.randint(1, 5)
            nums.extend([current] * repeat)
            current += 1
        
        nums = nums[:size]  # Trim to exact size
        
        # Benchmark
        nums_copy = nums.copy()
        start = time.perf_counter()
        
        for _ in range(100):
            nums_copy = nums.copy()
            solution.removeDuplicates(nums_copy)
        
        elapsed = (time.perf_counter() - start) * 10  # ms per iteration
        
        print(f"Size {size:>6,}: {elapsed:>8.3f}ms (avg of 100 runs)")
    
    print("\n" + "=" * 80)