""""
================================================================================
Problem: 74. Search a 2D Matrix
Platform: LeetCode
URL: https://leetcode.com/problems/search-a-2d-matrix/
Difficulty: Medium
Topics: Binary Search, Matrix, Array
================================================================================
PROBLEM DESCRIPTION:
You are given an m × n integer matrix matrix with two properties:
• Each row is sorted in non-decreasing order.
• The first integer of each row is greater than the last integer of the previous row.

Given an integer target, return true if target is in matrix, else false.

You must solve it in O(log(m × n)) time complexity.

CONSTRAINTS:
- m == matrix.length, n == matrix[i].length
- 1 <= m, n <= 100
- -10^4 <= matrix[i][j], target <= 10^4

EXAMPLES:
Example 1:
matrix = [
  [1, 3, 5, 7],
  [10,11,16,20],
  [23,30,34,60]
], target = 3
Output: true

Example 2:
Same matrix, target = 13
Output: false
================================================================================
INTUITION:
The matrix is effectively a sorted 1D array when flattened because:
- Rows are sorted
- Next row starts > previous row ends

We can treat the entire matrix as one sorted list of m×n elements and perform binary search on it.

Map virtual index k (0 to m*n-1) to matrix position:
- row = k // n
- col = k % n

Then standard binary search: compare matrix[row][col] with target.

This gives O(log(m*n)) time, O(1) space — perfect.
================================================================================
SOLUTION
================================================================================
"""

from typing import List

class Solution:
    def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:
        """
        Search target in sorted 2D matrix using virtual 1D binary search.
        
        Time:  O(log(m × n))
        Space: O(1)
        """
        if not matrix or not matrix[0]:
            return False
        
        m, n = len(matrix), len(matrix[0])
        left, right = 0, m * n - 1
        
        while left <= right:
            mid = left + (right - left) // 2
            row = mid // n
            col = mid % n
            val = matrix[row][col]
            
            if val == target:
                return True
            elif val < target:
                left = mid + 1
            else:
                right = mid - 1
        
        return False


# Alternative: Binary search rows first, then column (also O(log m + log n))
class SolutionRowFirst:
    def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:
        if not matrix or not matrix[0]:
            return False
        
        m, n = len(matrix), len(matrix[0])
        
        # Step 1: Binary search to find candidate row
        top, bottom = 0, m - 1
        while top <= bottom:
            mid_row = top + (bottom - top) // 2
            if matrix[mid_row][0] <= target <= matrix[mid_row][-1]:
                # Step 2: Binary search in this row
                left, right = 0, n - 1
                while left <= right:
                    mid_col = left + (right - left) // 2
                    if matrix[mid_row][mid_col] == target:
                        return True
                    elif matrix[mid_row][mid_col] < target:
                        left = mid_col + 1
                    else:
                        right = mid_col - 1
                return False
            elif matrix[mid_row][0] > target:
                bottom = mid_row - 1
            else:
                top = mid_row + 1
        
        return False


# =============================================================================
# TEST CASES
# =============================================================================
if __name__ == "__main__":
    solution = Solution()
    
    test_cases = [
        ([[1,3,5,7],[10,11,16,20],[23,30,34,60]], 3, True, "Found in first row"),
        ([[1,3,5,7],[10,11,16,20],[23,30,34,60]], 13, False, "Not present"),
        ([[1,3,5,7],[10,11,16,20],[23,30,34,60]], 60, True, "Last element"),
        ([[1]], 1, True, "Single element - found"),
        ([[1]], 2, False, "Single element - not found"),
        ([[1,2,3]], 2, True, "Single row"),
        ([[1],[2],[3]], 2, True, "Single column"),
        ([[-10,-8,-6],[-4,-2,0],[2,4,6]], -2, True, "Negative numbers"),
    ]
    
    print("=" * 60)
    print("74. SEARCH A 2D MATRIX - TEST CASES")
    print("=" * 60)
    
    passed = 0
    for matrix, target, expected, desc in test_cases:
        result = solution.searchMatrix(matrix, target)
        if result == expected:
            print(f"✓ {desc:50} → {result}")
            passed += 1
        else:
            print(f"✗ {desc:50} → got {result}, expected {expected}")
    
    print(f"\n{passed}/{len(test_cases)} test cases passed")
    print("=" * 60)

"""
Visualizations
Example Matrix (target = 3)
text[ 1  3  5  7 ]   ← row 0
[10 11 16 20 ]   ← row 1
[23 30 34 60 ]   ← row 2

Virtual indices:
0: (0,0)=1   1: (0,1)=3   2: (0,2)=5   3: (0,3)=7
4: (1,0)=10  5: (1,1)=11  6: (1,2)=16  7: (1,3)=20
8: (2,0)=23  9: (2,1)=30 10: (2,2)=34 11: (2,3)=60

Binary search for 3:
mid ≈ 5 → (1,1)=11 > 3 → right = 4
mid ≈ 2 → (0,2)=5  > 3 → right = 1
mid = 1   → (0,1)=3 == 3 → found!
Target = 13 (not found)
Similar process ends with left > right without match → false
Learning Notes – Key Insights & Patterns

Why virtual 1D binary search works
The matrix properties guarantee the flattened array is sorted ascending:
Within row: non-decreasing
Across rows: matrix[i+1][0] > matrix[i][n-1]
→ Entire structure is monotonically increasing

Virtual 1D vs Row-first binary searchApproachStepsProsConsVirtual 1DOne binary searchSimpler code, single loopLess intuitive row logicRow-first + ColumnBinary on rows + binary on colsMore readable, respects structureTwo phases, slightly more codeBoth are O(log(m*n)), interviewers accept either. Virtual 1D is often preferred for elegance.
Edge cases to remember
Empty matrix / empty row → false
Target < matrix[0][0] or > matrix[m-1][n-1] → false
Single row / single column
Target at boundaries (first/last element)

Common follow-ups
What if rows are sorted but no row-start > prev-end guarantee? → Can't do O(log(mn)), need O(m log n)
Search for position (not just existence)? → Similar to LC 35, return virtual index or (row, col)
Matrix sorted in columns instead? → Transpose logic
Duplicates allowed? → Still works (non-decreasing)

Interview tips
Start by saying: "Since the matrix is sorted row-wise and rows are chained, I can treat it as a 1D sorted array."
Draw the virtual indexing on whiteboard
Mention time complexity clearly: O(log(m*n))
Prefer virtual 1D for speed in coding
"""