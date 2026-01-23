"""
================================================================================
CONTAINS DUPLICATE SERIES - Complete Solutions (LC 217, 219, 220)
Platform: LeetCode
Difficulty: Easy → Easy → Hard
Topics: Array, Hash Table, Sliding Window, Bucketing
================================================================================

This file contains solutions to the complete "Contains Duplicate" series:
- LC 217: Contains Duplicate (Easy)
- LC 219: Contains Duplicate II (Easy)  
- LC 220: Contains Duplicate III (Hard)

Each problem builds on the previous one, adding more constraints and complexity.
This demonstrates pattern progression from basic hash set to advanced bucketing.

================================================================================
PROBLEM PROGRESSION OVERVIEW
================================================================================

┌─────────────────────────────────────────────────────────────────────────┐
│ LC 217: Contains Duplicate                                              │
│ Question: Does array have any duplicate?                                │
│ Pattern:  Hash Set for O(1) lookup                                      │
│ Time:     O(n)                                                           │
│ Space:    O(n)                                                           │
└─────────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────────┐
│ LC 219: Contains Duplicate II                                           │
│ Question: Duplicate exists within distance k?                           │
│ Pattern:  Hash Map with index tracking / Sliding Window                 │
│ Time:     O(n)                                                           │
│ Space:    O(min(n, k))                                                   │
└─────────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────────┐
│ LC 220: Contains Duplicate III                                          │
│ Question: Close indices AND close values?                               │
│ Pattern:  Bucketing / Generalized Bucket Sort                           │
│ Time:     O(n)                                                           │
│ Space:    O(min(n, indexDiff))                                           │
└─────────────────────────────────────────────────────────────────────────┘

================================================================================
"""

from typing import List, Dict, Set
import time


# ╔═══════════════════════════════════════════════════════════════════════════╗
# ║                        PROBLEM 1: CONTAINS DUPLICATE                      ║
# ║                              (LC 217 - Easy)                              ║
# ╚═══════════════════════════════════════════════════════════════════════════╝

"""
================================================================================
Problem: 217. Contains Duplicate
URL: https://leetcode.com/problems/contains-duplicate/
Difficulty: Easy
Topics: Array, Hash Table
================================================================================

PROBLEM DESCRIPTION:
Given an integer array nums, return true if any value appears at least twice 
in the array, and return false if every element is distinct.

CONSTRAINTS:
- 1 <= nums.length <= 10^5
- -10^9 <= nums[i] <= 10^9

EXAMPLES:
Input: nums = [1,2,3,1]
Output: true

Input: nums = [1,2,3,4]
Output: false

Input: nums = [1,1,1,3,3,4,3,2,4,2]
Output: true

================================================================================
APPROACH 1: Set Length Comparison (Most Pythonic)

INTUITION:
A set only stores unique elements. If converting the array to a set results in
fewer elements, duplicates must exist.

COMPLEXITY:
- Time: O(n) - converting to set iterates once
- Space: O(n) - set stores up to n unique elements

================================================================================
APPROACH 2: Early Exit with Set (Often Faster in Practice)

INTUITION:
Instead of building the complete set, we can exit early as soon as we find
the first duplicate. This is faster when duplicates appear early in the array.

COMPLEXITY:
- Time: O(n) worst case, O(1) best case (duplicate at start)
- Space: O(n) worst case
================================================================================
"""

class Solution1_ContainsDuplicate:
    """LC 217: Contains Duplicate"""
    
    def containsDuplicate_Pythonic(self, nums: List[int]) -> bool:
        """
        Most concise solution using set length comparison.
        
        Time: O(n)
        Space: O(n)
        """
        return len(nums) != len(set(nums))
    
    def containsDuplicate(self, nums: List[int]) -> bool:
        """
        Optimized solution with early exit.
        
        This is often faster in practice when duplicates appear early,
        since we don't need to process the entire array.
        
        Time: O(n) worst case, O(1) best case
        Space: O(n) worst case
        """
        # Edge case: single element or empty
        if len(nums) <= 1:
            return False
        
        seen = set()
        
        for num in nums:
            # Found duplicate - exit immediately
            if num in seen:
                return True
            seen.add(num)
        
        return False


# ╔═══════════════════════════════════════════════════════════════════════════╗
# ║                     PROBLEM 2: CONTAINS DUPLICATE II                      ║
# ║                              (LC 219 - Easy)                              ║
# ╚═══════════════════════════════════════════════════════════════════════════╝

"""
================================================================================
Problem: 219. Contains Duplicate II
URL: https://leetcode.com/problems/contains-duplicate-ii/
Difficulty: Easy
Topics: Array, Hash Table, Sliding Window
================================================================================

PROBLEM DESCRIPTION:
Given an integer array nums and an integer k, return true if there are two 
distinct indices i and j in the array such that nums[i] == nums[j] and 
abs(i - j) <= k.

CONSTRAINTS:
- 1 <= nums.length <= 10^5
- -10^9 <= nums[i] <= 10^9
- 0 <= k <= 10^5

EXAMPLES:
Input: nums = [1,2,3,1], k = 3
Output: true
Explanation: Indices 0 and 3 have value 1, distance is 3 <= 3

Input: nums = [1,0,1,1], k = 1
Output: true
Explanation: Indices 2 and 3 have value 1, distance is 1 <= 1

Input: nums = [1,2,3,1,2,3], k = 2
Output: false
Explanation: All duplicates are more than distance 2 apart

================================================================================
APPROACH: Hash Map with Index Tracking

INTUITION:
We need to track not just IF a value exists, but WHERE (at what index).
Store the most recent index for each value. When we see a value again, check
if the distance from its last occurrence is within k.

KEY INSIGHT:
We only need to store the MOST RECENT index for each value, because:
- If current index is i and we saw the value at j
- Distance i - j will be minimal when j is as large as possible (most recent)

OPTIMIZATIONS:
1. Early exit if no duplicates exist at all
2. Early exit if array length <= k+1 (all elements are within range)
3. Only store most recent index (not all indices)

COMPLEXITY:
- Time: O(n) - single pass with O(1) hash map operations
- Space: O(min(n, k+1)) - map size limited by window
================================================================================
"""

class Solution2_ContainsDuplicateII:
    """LC 219: Contains Duplicate II"""
    
    def containsNearbyDuplicate(self, nums: List[int], k: int) -> bool:
        """
        Optimized solution with early exits and hash map index tracking.
        
        Time: O(n)
        Space: O(min(n, k+1))
        """
        # Optimization 1: If no duplicates exist at all, return False
        if len(set(nums)) == len(nums):
            return False
        
        # Optimization 2: If array length <= k+1, all elements are within range
        # Since we know duplicates exist (from check above), return True
        if len(nums) <= k + 1:
            return True
        
        # Hash map: value -> most recent index
        index_map = {}
        
        for idx, value in enumerate(nums):
            # Check if we've seen this value before
            if value in index_map:
                # Check if distance is within k
                if abs(index_map[value] - idx) <= k:
                    return True
            
            # Update to most recent index
            # This ensures minimum distance with next occurrence
            index_map[value] = idx
        
        return False


# ╔═══════════════════════════════════════════════════════════════════════════╗
# ║                    PROBLEM 3: CONTAINS DUPLICATE III                      ║
# ║                              (LC 220 - Hard)                              ║
# ╚═══════════════════════════════════════════════════════════════════════════╝

"""
================================================================================
Problem: 220. Contains Duplicate III
URL: https://leetcode.com/problems/contains-duplicate-iii/
Difficulty: Hard
Topics: Array, Sliding Window, Sorting, Bucket Sort, Ordered Set
================================================================================

PROBLEM DESCRIPTION:
You are given an integer array nums and two integers indexDiff and valueDiff.

Find a pair of indices (i, j) such that:
- i != j
- abs(i - j) <= indexDiff
- abs(nums[i] - nums[j]) <= valueDiff

Return true if such pair exists or false otherwise.

CONSTRAINTS:
- 2 <= nums.length <= 10^5
- -10^9 <= nums[i] <= 10^9
- 1 <= indexDiff <= nums.length
- 0 <= valueDiff <= 10^9

EXAMPLES:
Input: nums = [1,2,3,1], indexDiff = 3, valueDiff = 0
Output: true
Explanation: Indices 0 and 3 (values 1 and 1) satisfy both conditions

Input: nums = [1,5,9,1,5,9], indexDiff = 2, valueDiff = 3
Output: false
Explanation: No pair within distance 2 has value difference <= 3

================================================================================
APPROACH 1: Brute Force (TLE) - O(n × indexDiff)

Check every pair within the sliding window. This works but times out.

for i in range(len(nums)):
    for j in range(i+1, min(i+indexDiff+1, len(nums))):
        if abs(nums[i] - nums[j]) <= valueDiff:
            return True
return False

================================================================================
APPROACH 2: Bucketing (Optimal) - O(n)

INTUITION:
Think of bucketing like organizing numbers into bins:
- If two numbers are in the SAME bucket, they're definitely close enough
- If in ADJACENT buckets, they MIGHT be close enough (check manually)
- If in non-adjacent buckets, they're definitely TOO FAR apart

BUCKET DESIGN:
- Bucket width = valueDiff + 1
- Bucket ID for number x = x // (valueDiff + 1)

WHY THIS WORKS:
- Two numbers in same bucket: difference < bucket_width = valueDiff + 1
  Therefore difference <= valueDiff ✓
- Two numbers in adjacent buckets: might have difference <= valueDiff
  Must check manually
- Two numbers 2+ buckets apart: difference > valueDiff ✗

EXAMPLE:
valueDiff = 3, so bucket_width = 4
Numbers:  0  1  2  3  | 4  5  6  7  | 8  9  10 11
Buckets:  [  Bucket 0  ] [ Bucket 1  ] [ Bucket 2 ]

- 0 and 3 are in bucket 0 → difference = 3 <= 3 ✓ (auto-valid)
- 3 and 4 are in buckets 0 and 1 → must check: |3-4| = 1 <= 3 ✓
- 0 and 8 are in buckets 0 and 2 → skip (too far)

SLIDING WINDOW:
We maintain a window of size indexDiff. When we move forward:
1. Add current element to its bucket
2. Remove element that's now too old (index i - indexDiff)

COMPLEXITY:
- Time: O(n) - each element processed once with O(1) operations
- Space: O(min(n, indexDiff)) - bucket map size limited by window

================================================================================
"""

class Solution3_ContainsDuplicateIII:
    """LC 220: Contains Duplicate III"""
    
    def containsNearbyAlmostDuplicate(
        self, 
        nums: List[int], 
        indexDiff: int, 
        valueDiff: int
    ) -> bool:
        """
        Optimal bucketing solution.
        
        Args:
            nums: Array of integers
            indexDiff: Maximum index distance
            valueDiff: Maximum value difference
            
        Returns:
            True if valid pair exists
            
        Time: O(n)
        Space: O(min(n, indexDiff))
        """
        # Edge cases
        if indexDiff <= 0 or valueDiff < 0:
            return False
        
        # Bucket width
        # If valueDiff = 0, width = 1 (exact matches only)
        # If valueDiff = 3, width = 4 (values 0,1,2,3 in same bucket)
        width = valueDiff + 1
        
        # Buckets: {bucket_id: value}
        # We only store ONE value per bucket (most recent in window)
        buckets = {}
        
        for i, num in enumerate(nums):
            # Calculate bucket ID for current number
            bucket_id = num // width
            
            # Case 1: Same bucket exists
            # If there's already a number in this bucket within our window,
            # their difference is guaranteed to be < width, so <= valueDiff
            if bucket_id in buckets:
                return True
            
            # Case 2: Check left adjacent bucket
            # Numbers in bucket (bucket_id - 1) might be close enough
            if bucket_id - 1 in buckets:
                if abs(num - buckets[bucket_id - 1]) <= valueDiff:
                    return True
            
            # Case 3: Check right adjacent bucket
            # Numbers in bucket (bucket_id + 1) might be close enough
            if bucket_id + 1 in buckets:
                if abs(num - buckets[bucket_id + 1]) <= valueDiff:
                    return True
            
            # Add current number to its bucket
            buckets[bucket_id] = num
            
            # Maintain sliding window: remove element outside window
            if i >= indexDiff:
                old_num = nums[i - indexDiff]
                old_bucket_id = old_num // width
                del buckets[old_bucket_id]
        
        return False


# ╔═══════════════════════════════════════════════════════════════════════════╗
# ║                            TEST FRAMEWORK                                  ║
# ╚═══════════════════════════════════════════════════════════════════════════╝

def run_all_tests():
    """Run comprehensive tests for all three problems"""
    
    print("╔" + "═" * 78 + "╗")
    print("║" + " " * 20 + "CONTAINS DUPLICATE SERIES - TEST SUITE" + " " * 20 + "║")
    print("╚" + "═" * 78 + "╝")
    print()
    
    # ═══════════════════════════════════════════════════════════════════
    # TEST PROBLEM 1: Contains Duplicate
    # ═══════════════════════════════════════════════════════════════════
    
    print("┌" + "─" * 78 + "┐")
    print("│ Problem 1: LC 217 - Contains Duplicate" + " " * 39 + "│")
    print("└" + "─" * 78 + "┘")
    
    solution1 = Solution1_ContainsDuplicate()
    
    test_cases_1 = [
        ([1, 2, 3, 1], True, "Example 1: Duplicate exists"),
        ([1, 2, 3, 4], False, "Example 2: All distinct"),
        ([1, 1, 1, 3, 3, 4, 3, 2, 4, 2], True, "Example 3: Multiple duplicates"),
        ([1], False, "Single element"),
        ([1, 2], False, "Two distinct elements"),
        ([1, 1], True, "Two same elements"),
        (list(range(1000)), False, "Large array - all distinct"),
        ([5] * 1000, True, "Large array - all same"),
    ]
    
    passed_1 = 0
    for nums, expected, desc in test_cases_1:
        result = solution1.containsDuplicate(nums)
        if result == expected:
            print(f"  ✅ {desc}")
            passed_1 += 1
        else:
            print(f"  ❌ {desc}")
            print(f"     Expected: {expected}, Got: {result}")
    
    print(f"\n  Results: {passed_1}/{len(test_cases_1)} passed\n")
    
    # ═══════════════════════════════════════════════════════════════════
    # TEST PROBLEM 2: Contains Duplicate II
    # ═══════════════════════════════════════════════════════════════════
    
    print("┌" + "─" * 78 + "┐")
    print("│ Problem 2: LC 219 - Contains Duplicate II" + " " * 36 + "│")
    print("└" + "─" * 78 + "┘")
    
    solution2 = Solution2_ContainsDuplicateII()
    
    test_cases_2 = [
        ([1, 2, 3, 1], 3, True, "Example 1: Distance exactly k"),
        ([1, 0, 1, 1], 1, True, "Example 2: Adjacent duplicates"),
        ([1, 2, 3, 1, 2, 3], 2, False, "Example 3: Distance too large"),
        ([1, 2, 3, 4], 5, False, "No duplicates"),
        ([99, 99], 2, True, "Two elements, k larger than array"),
        ([1, 2, 1], 0, False, "k=0 edge case"),
        ([1, 2, 3, 4, 5, 1], 4, False, "Duplicate at distance k+1"),
        ([1, 2, 3, 4, 5, 1], 5, True, "Duplicate at distance k"),
    ]
    
    passed_2 = 0
    for nums, k, expected, desc in test_cases_2:
        result = solution2.containsNearbyDuplicate(nums, k)
        if result == expected:
            print(f"  ✅ {desc}")
            passed_2 += 1
        else:
            print(f"  ❌ {desc}")
            print(f"     Expected: {expected}, Got: {result}")
    
    print(f"\n  Results: {passed_2}/{len(test_cases_2)} passed\n")
    
    # ═══════════════════════════════════════════════════════════════════
    # TEST PROBLEM 3: Contains Duplicate III
    # ═══════════════════════════════════════════════════════════════════
    
    print("┌" + "─" * 78 + "┐")
    print("│ Problem 3: LC 220 - Contains Duplicate III" + " " * 35 + "│")
    print("└" + "─" * 78 + "┘")
    
    solution3 = Solution3_ContainsDuplicateIII()
    
    test_cases_3 = [
        ([1, 2, 3, 1], 3, 0, True, "Example 1: Exact match"),
        ([1, 5, 9, 1, 5, 9], 2, 3, False, "Example 2: No valid pair"),
        ([1, 2, 3, 1], 3, 0, True, "Duplicate with valueDiff=0"),
        ([2147483647, -1, 2147483647], 1, 2147483647, False, "Integer overflow edge"),
        ([10, 15, 18, 24], 3, 3, True, "15 and 18 differ by 3"),
        ([1, 2], 1, 1, True, "Simple case: adjacent values within range"),
        ([0, 2147483647], 1, 2147483647, True, "Max value difference"),
        ([-1, -1], 1, 0, True, "Negative duplicates"),
    ]
    
    passed_3 = 0
    for nums, indexDiff, valueDiff, expected, desc in test_cases_3:
        result = solution3.containsNearbyAlmostDuplicate(nums, indexDiff, valueDiff)
        if result == expected:
            print(f"  ✅ {desc}")
            passed_3 += 1
        else:
            print(f"  ❌ {desc}")
            print(f"     Expected: {expected}, Got: {result}")
    
    print(f"\n  Results: {passed_3}/{len(test_cases_3)} passed\n")
    
    # ═══════════════════════════════════════════════════════════════════
    # SUMMARY
    # ═══════════════════════════════════════════════════════════════════
    
    total_passed = passed_1 + passed_2 + passed_3
    total_tests = len(test_cases_1) + len(test_cases_2) + len(test_cases_3)
    
    print("╔" + "═" * 78 + "╗")
    print(f"║  OVERALL RESULTS: {total_passed}/{total_tests} tests passed" + " " * (78 - 28 - len(str(total_passed)) - len(str(total_tests))) + "║")
    print("╚" + "═" * 78 + "╝")
    print()
    
    if total_passed == total_tests:
        print("🎉 All tests passed! Series complete.")
    else:
        print(f"⚠️  {total_tests - total_passed} test(s) failed.")


# ╔═══════════════════════════════════════════════════════════════════════════╗
# ║                         PERFORMANCE BENCHMARKS                             ║
# ╚═══════════════════════════════════════════════════════════════════════════╝

def run_benchmarks():
    """Benchmark all three solutions"""
    
    print("\n╔" + "═" * 78 + "╗")
    print("║" + " " * 25 + "PERFORMANCE BENCHMARKS" + " " * 31 + "║")
    print("╚" + "═" * 78 + "╝")
    print()
    
    sizes = [1000, 10000, 100000]
    
    solution1 = Solution1_ContainsDuplicate()
    solution2 = Solution2_ContainsDuplicateII()
    solution3 = Solution3_ContainsDuplicateIII()
    
    # Benchmark Problem 1
    print("Problem 1: Contains Duplicate")
    print("─" * 50)
    for size in sizes:
        # Worst case: no duplicates
        test_data = list(range(size))
        
        start = time.perf_counter()
        for _ in range(10):
            solution1.containsDuplicate(test_data)
        elapsed = (time.perf_counter() - start) * 100  # ms per iteration
        
        print(f"  Size {size:>6,}: {elapsed:.3f}ms (avg of 10 runs)")
    print()
    
    # Benchmark Problem 2
    print("Problem 2: Contains Duplicate II")
    print("─" * 50)
    for size in sizes:
        test_data = list(range(size))
        k = size // 2
        
        start = time.perf_counter()
        for _ in range(10):
            solution2.containsNearbyDuplicate(test_data, k)
        elapsed = (time.perf_counter() - start) * 100
        
        print(f"  Size {size:>6,}: {elapsed:.3f}ms (avg of 10 runs)")
    print()
    
    # Benchmark Problem 3
    print("Problem 3: Contains Duplicate III")
    print("─" * 50)
    for size in sizes:
        test_data = list(range(0, size * 10, 10))  # Spread out values
        indexDiff = size // 2
        valueDiff = 5
        
        start = time.perf_counter()
        for _ in range(10):
            solution3.containsNearbyAlmostDuplicate(test_data, indexDiff, valueDiff)
        elapsed = (time.perf_counter() - start) * 100
        
        print(f"  Size {size:>6,}: {elapsed:.3f}ms (avg of 10 runs)")
    print()


# ╔═══════════════════════════════════════════════════════════════════════════╗
# ║                         LEARNING NOTES & PATTERNS                          ║
# ╚═══════════════════════════════════════════════════════════════════════════╝

"""
================================================================================
PATTERN PROGRESSION: FROM SIMPLE TO ADVANCED
================================================================================

1. LC 217: Basic Hash Set Pattern
   - Question: "Does X exist?"
   - Tool: Hash Set (O(1) lookup)
   - Lesson: Space-for-time tradeoff

2. LC 219: Hash Map with Metadata
   - Question: "Does X exist at position Y?"
   - Tool: Hash Map storing indices
   - Lesson: Storing additional information (not just existence)

3. LC 220: Advanced Bucketing
   - Question: "Do similar X and Y exist near each other?"
   - Tool: Bucketing (generalized hash)
   - Lesson: Mapping continuous space to discrete buckets

================================================================================
KEY INSIGHTS
================================================================================

Problem 1: Contains Duplicate
├─ Pattern: Hash Set for existence check
├─ Trick: len(set) vs len(list) is Pythonic
└─ Alternative: Early exit can be faster in practice

Problem 2: Contains Duplicate II
├─ Pattern: Sliding window with hash map
├─ Trick: Store most recent index only
├─ Optimization: Check if duplicates exist first
└─ Edge case: k=0 means impossible (distinct indices required)

Problem 3: Contains Duplicate III
├─ Pattern: Bucketing (discretize continuous space)
├─ Trick: Bucket width = valueDiff + 1
├─ Why: Numbers in same bucket auto-satisfy condition
├─ Edge case: Must check adjacent buckets manually
└─ Complexity: Better than BST approach (O(n) vs O(n log n))

================================================================================
INTERVIEW TIPS
================================================================================

1. Recognize the Series
   - If interviewer asks Contains Duplicate, clarify which variant
   - Each builds on previous - show you understand progression

2. Explain Tradeoffs
   - Problem 1: "We trade O(n) space for O(n) time vs O(n²) brute force"
   - Problem 2: "We track indices, not just existence"
   - Problem 3: "Bucketing avoids expensive range searches"

3. Start Simple
   - Always mention brute force first
   - "For Problem 1, we could check all pairs in O(n²)..."
   - "But hash set gives us O(n) with O(n) space"

4. Problem 3 Deep Dive
   - Many candidates struggle with bucketing
   - Draw the bucket diagram on whiteboard
   - Explain why width = valueDiff + 1 (inclusive range)
   - Show why adjacent buckets need checking but others don't

================================================================================
COMMON MISTAKES
================================================================================

Problem 1:
❌ Using sorting (O(n log n) when O(n) exists)
❌ Not considering early exit optimization

Problem 2:
❌ Storing all indices instead of just most recent
❌ Not handling k=0 edge case
❌ Checking condition after adding to map (causes self-match)

Problem 3:
❌ Using width = valueDiff (should be valueDiff + 1)
❌ Forgetting to check adjacent buckets
❌ Not removing old elements from sliding window
❌ Integer overflow in bucket calculation (Python handles this automatically)
❌ Checking non-adjacent buckets (unnecessary and wrong)

================================================================================
RELATED PROBLEMS
================================================================================

Same Pattern Family:
- LC 1: Two Sum (hash map)
- LC 454: 4Sum II (hash map with counts)
- LC 447: Number of Boomerangs (hash map with distances)

Sliding Window:
- LC 3: Longest Substring Without Repeating Characters
- LC 438: Find All Anagrams in a String
- LC 567: Permutation in String

Bucketing:
- LC 164: Maximum Gap (bucket sort concept)
- LC 287: Find the Duplicate Number (advanced techniques)

================================================================================
"""


# ╔═══════════════════════════════════════════════════════════════════════════╗
# ║                              MAIN EXECUTION                                ║
# ╚═══════════════════════════════════════════════════════════════════════════╝

if __name__ == "__main__":
    # Run all tests
    run_all_tests()
    
    # Run performance benchmarks
    run_benchmarks()
    
    print("\n" + "═" * 80)
    print("✨ Contains Duplicate Series - Complete")
    print("═" * 80)