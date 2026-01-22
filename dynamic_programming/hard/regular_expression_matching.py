"""
================================================================================
Problem: 10. Regular Expression Matching
Platform: LeetCode
URL: https://leetcode.com/problems/regular-expression-matching/
Difficulty: Hard
Topics: String, Dynamic Programming, Recursion
================================================================================

PROBLEM DESCRIPTION:
Given an input string s and a pattern p, implement regular expression matching 
with support for '.' and '*' where:
- '.' Matches any single character
- '*' Matches zero or more of the preceding element

The matching should cover the entire input string (not partial).

CONSTRAINTS:
- 1 <= s.length <= 20
- 1 <= p.length <= 20
- s contains only lowercase English letters
- p contains only lowercase English letters, '.', and '*'
- It is guaranteed for each appearance of '*', there will be a previous valid character to match

EXAMPLES:
Input: s = "aa", p = "a"
Output: false
Explanation: "a" does not match the entire string "aa"

Input: s = "aa", p = "a*"
Output: true
Explanation: '*' means zero or more of the preceding element, 'a'

Input: s = "ab", p = ".*"
Output: true
Explanation: ".*" means "zero or more (*) of any character (.)"

================================================================================
APPROACH (Top-Down DP with Memoization):

This approach uses recursion with memoization, which often performs better
than bottom-up DP due to early pruning of impossible states.

STATE DEFINITION:
dp(i, j) = whether s[i:] matches p[j:]

BASE CASES:
- If j == len(p): return i == len(s) (pattern exhausted)
- If i == len(s): only true if remaining pattern is all "x*" pairs

RECURRENCE:
1. Check if current characters match: s[i] == p[j] or p[j] == '.'
2. If next character is '*':
   - Option 1: Skip pattern (0 occurrences): dp(i, j+2)
   - Option 2: Use pattern (if match): dp(i+1, j)
3. Otherwise: first_match AND dp(i+1, j+1)

OPTIMIZATIONS APPLIED:
1. Memoization to avoid recomputing states
2. Early termination when pattern is exhausted
3. Efficient state exploration (doesn't build full table)

COMPLEXITY ANALYSIS:
- Time: O(m × n) - each state computed once
- Space: O(m × n) - memoization cache
  (Can be optimized to O(n) with bottom-up approach)

================================================================================
"""

from typing import Dict, Tuple

class Solution:
    def isMatch(self, s: str, p: str) -> bool:
        memo: Dict[Tuple[int, int], bool] = {}
        
        def dp(i: int, j: int) -> bool:
            """
            Returns whether s[i:] matches p[j:]
            
            Args:
                i: current index in string s
                j: current index in pattern p
            """
            # Base case: pattern exhausted
            if j == len(p):
                return i == len(s)
            
            # Check memoization cache
            if (i, j) in memo:
                return memo[(i, j)]
            
            # Check if current characters match
            first_match = i < len(s) and (p[j] == s[i] or p[j] == '.')
            
            # Handle '*' pattern (looks ahead one character)
            if j + 1 < len(p) and p[j + 1] == '*':
                # Two options:
                # 1. Skip the "x*" pattern (0 occurrences)
                # 2. Use the pattern if current char matches (1+ occurrences)
                result = (
                    dp(i, j + 2) or                    # 0 occurrences
                    (first_match and dp(i + 1, j))     # 1+ occurrences
                )
            else:
                # Regular character: must match and advance both pointers
                result = first_match and dp(i + 1, j + 1)
            
            # Store in cache
            memo[(i, j)] = result
            return result
        
        return dp(0, 0)


# ================================================================================
# ALTERNATIVE: Space-Optimized Bottom-Up DP (O(n) space)
# ================================================================================
class SolutionSpaceOptimized:
    def isMatch(self, s: str, p: str) -> bool:
        m, n = len(s), len(p)
        
        # Only need current and previous row
        dp = [False] * (n + 1)
        dp[0] = True
        
        # Initialize first row (empty string matching pattern)
        for j in range(2, n + 1):
            if p[j - 1] == '*':
                dp[j] = dp[j - 2]
        
        for i in range(1, m + 1):
            prev_diag = dp[0]
            dp[0] = False  # Empty pattern can't match non-empty string
            
            for j in range(1, n + 1):
                temp = dp[j]
                
                if p[j - 1] == s[i - 1] or p[j - 1] == '.':
                    # Characters match
                    dp[j] = prev_diag
                elif p[j - 1] == '*':
                    # Star pattern: check zero or more occurrences
                    dp[j] = dp[j - 2]  # Zero occurrences
                    
                    preceding_char = p[j - 2]
                    if preceding_char == s[i - 1] or preceding_char == '.':
                        dp[j] = dp[j] or temp  # One or more occurrences
                else:
                    dp[j] = False
                
                prev_diag = temp
        
        return dp[n]


# ================================================================================
# TEST CASES
# ================================================================================
if __name__ == "__main__":
    solution = Solution()
    solution_opt = SolutionSpaceOptimized()
    
    test_cases = [
        ("aa", "a", False),
        ("aa", "a*", True),
        ("ab", ".*", True),
        ("aab", "c*a*b", True),
        ("mississippi", "mis*is*p*.", False),
        ("", "", True),
        ("", "a*", True),
        ("", ".*", True),
        ("a", "", False),
        ("ab", ".*c", False),
        ("aaa", "a*a", True),
        ("aaa", "ab*a*c*a", True),
        ("a", "ab*", True),
        ("bbbba", ".*a*a", True),
    ]
    
    print("Testing Top-Down DP Solution:")
    for i, (s, p, expected) in enumerate(test_cases, 1):
        result = solution.isMatch(s, p)
        status = "✅" if result == expected else "❌"
        print(f"{status} Test {i}: s='{s}', p='{p}' → {result} (expected {expected})")
    
    print("\nTesting Space-Optimized Solution:")
    for i, (s, p, expected) in enumerate(test_cases, 1):
        result = solution_opt.isMatch(s, p)
        status = "✅" if result == expected else "❌"
        print(f"{status} Test {i}: s='{s}', p='{p}' → {result} (expected {expected})")
    
    print("\n🎉 All test cases completed!")

# ================================================================================
# VISUALIZATION (for s="aab", p="c*a*b"):
#
# Top-down recursion trace:
# dp(0,0): s="aab", p="c*a*b"
#   ├─ p[1]='*', so check c*:
#   │  ├─ dp(0,2): skip "c*" → s="aab", p="a*b"
#   │  │  ├─ p[1]='*', so check a*:
#   │  │  │  ├─ dp(0,4): skip "a*" → s="aab", p="b" → False
#   │  │  │  └─ dp(1,2): use "a*" → s="ab", p="a*b"
#   │  │  │     ├─ dp(1,4): skip "a*" → s="ab", p="b" → False
#   │  │  │     └─ dp(2,2): use "a*" → s="b", p="a*b"
#   │  │  │        ├─ dp(2,4): skip "a*" → s="b", p="b"
#   │  │  │        │  └─ dp(3,5): match! → True ✓
#   └─ Result: True
#
# Bottom-up DP table:
#       ""  c   *   a   *   b
#   ""  T   F   T   F   T   F
#   a   F   F   F   T   T   F
#   a   F   F   F   F   T   F
#   b   F   F   F   F   F   T
#
# Answer: dp[3][5] = True ✓
# ================================================================================

# ================================================================================
# LEARNING NOTES:
# 
# WHEN TO USE EACH APPROACH:
# 1. Top-Down (Recursion + Memo):
#    - Cleaner, more intuitive code
#    - Better for sparse state spaces (early pruning)
#    - Easier to debug and understand
#    - Preferred in interviews
#
# 2. Bottom-Up (Iterative DP):
#    - Can optimize space to O(n)
#    - Slightly faster in practice (no recursion overhead)
#    - Better for dense state spaces
#
# KEY INSIGHTS:
# - '*' matches ZERO or more of PRECEDING character
# - Always look ahead when you see '*' (check p[j+1])
# - Two choices for '*': skip entirely OR use if match
# - Base case: pattern exhausted → check if string exhausted too
#
# COMMON MISTAKES:
# - Forgetting that '*' applies to preceding char, not itself
# - Not handling empty string/pattern correctly
# - Off-by-one errors in index calculations
# - Not considering both "skip" and "use" cases for '*'
#
# RELATED PROBLEMS:
# - LC 44: Wildcard Matching (similar but different rules)
# - LC 72: Edit Distance (different DP pattern)
# - LC 1143: Longest Common Subsequence (simpler DP)
# ================================================================================