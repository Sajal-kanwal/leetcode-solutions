"""
================================================================================
Problem: 222. Count Complete Tree Nodes
Platform: LeetCode
URL: https://leetcode.com/problems/count-complete-tree-nodes/
Difficulty: Easy
Topics: Binary Tree, Recursion, Binary Search
================================================================================

PROBLEM DESCRIPTION:
Given the root of a complete binary tree, return the number of nodes in the tree.

Every level, except possibly the last, is completely filled. All nodes in the 
last level are as far left as possible.

Design an algorithm that runs in less than O(n) time complexity.

CONSTRAINTS:
- Number of nodes in range [0, 5 * 10^4]
- 0 <= Node.val <= 5 * 10^4
- Tree is guaranteed to be complete

EXAMPLES:

Example 1:
Input: root = [1,2,3,4,5,6]
Output: 6

        1
       / \
      2   3
     / \ /
    4  5 6

Example 2:
Input: root = []
Output: 0

Example 3:
Input: root = [1]
Output: 1

================================================================================
KEY INSIGHT — COMPLETE BINARY TREE PROPERTIES:
================================================================================

A complete binary tree has a special structure we can exploit:

1. All levels except the last are FULLY filled
2. Last level fills from LEFT to RIGHT

Perfect binary tree of height h has: 2^(h+1) - 1 nodes

For a complete tree, two cases when comparing left and right subtrees:

CASE A: Left subtree is a PERFECT tree
        (left height == right height)
  
        1              Left subtree is perfect
       / \             (height 2, nodes = 2^2 - 1 = 3)
      2   3            Right subtree needs recursion
     / \ / \
    4  5 6  7
   / \
  8   9

  Left height (going leftmost) = right height (going leftmost)
  → Left subtree is perfect → count it directly: 2^h - 1
  → Recurse only on RIGHT subtree

CASE B: Right subtree is a PERFECT tree  
        (left height != right height)

        1              Right subtree is perfect
       / \             (height 1, nodes = 2^1 - 1 = 1)
      2   3            Left subtree needs recursion  
     / \
    4   5

  Left height != right height
  → Right subtree is perfect (one level shorter) → count directly: 2^(h-1) - 1
  → Recurse only on LEFT subtree

WHY THIS IS O(log²n):
- Each recursive call: O(log n) to measure heights
- Recursion depth: O(log n) (tree height)
- Total: O(log n × log n) = O(log²n)

================================================================================
APPROACH COMPARISON:
================================================================================

| Approach | Time | Space | Exploits Complete Property? |
|----------|------|-------|-----------------------------|
| Simple Recursion | O(n) | O(log n) | ❌ No |
| Binary Search (Optimal) | O(log²n) | O(log n) | ✅ Yes |
| Iterative BFS | O(n) | O(n) | ❌ No |

The problem explicitly asks for less than O(n), so the binary search
approach is the intended solution.

================================================================================
"""


# Definition for a binary tree node
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    """LC 222: Count Complete Tree Nodes — O(log²n) Optimal"""
    
    def countNodes(self, root: TreeNode) -> int:
        """
        Count nodes exploiting complete binary tree structure.
        
        At each node, measure left and right subtree heights.
        One of them is guaranteed to be a perfect subtree —
        count it directly with 2^h - 1, recurse on the other.
        
        Args:
            root: Root of complete binary tree
            
        Returns:
            Total number of nodes
            
        Algorithm: Binary Search on Complete Tree
        Time: O(log²n) — log n levels × log n height measurement
        Space: O(log n) — recursion stack depth
        """
        if not root:
            return 0
        
        # Measure heights by going all the way left
        left_height = self._get_height(root.left)
        right_height = self._get_height(root.right)
        
        if left_height == right_height:
            # Left subtree is PERFECT (height = left_height)
            # Perfect tree nodes = 2^h - 1
            # Plus current node = 2^h
            # Recurse on right subtree
            return (1 << left_height) + self.countNodes(root.right)
        else:
            # Right subtree is PERFECT (height = right_height)
            # Perfect tree nodes = 2^h - 1
            # Plus current node = 2^h
            # Recurse on left subtree
            return (1 << right_height) + self.countNodes(root.left)
    
    def _get_height(self, node: TreeNode) -> int:
        """
        Get height of tree by going all the way left.
        
        In a complete binary tree, the leftmost path gives the height.
        
        Returns 0 for None (empty subtree).
        """
        height = 0
        while node:
            height += 1
            node = node.left
        return height


class SolutionSimpleRecursion:
    """
    Simple O(n) recursion — for comparison only.
    
    Visits every node exactly once.
    Does NOT exploit complete tree property.
    """
    
    def countNodes(self, root: TreeNode) -> int:
        """
        Count = 1 (current) + left subtree count + right subtree count
        """
        if not root:
            return 0
        
        return 1 + self.countNodes(root.left) + self.countNodes(root.right)


class SolutionIterativeBFS:
    """
    BFS level-order traversal — O(n) time, O(n) space.
    
    Counts nodes level by level.
    Also does NOT exploit complete tree property.
    """
    
    def countNodes(self, root: TreeNode) -> int:
        if not root:
            return 0
        
        from collections import deque
        
        queue = deque([root])
        count = 0
        
        while queue:
            node = queue.popleft()
            count += 1
            
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        
        return count


# ================================================================================
# HELPER: Build tree from level-order list (for testing)
# ================================================================================

def build_tree(values: list) -> TreeNode:
    """
    Build a binary tree from level-order list.
    None values represent missing nodes.
    
    Example: [1,2,3,4,5,6] builds:
            1
           / \
          2   3
         / \ /
        4  5 6
    """
    if not values or values[0] is None:
        return None
    
    from collections import deque
    
    root = TreeNode(values[0])
    queue = deque([root])
    i = 1
    
    while queue and i < len(values):
        node = queue.popleft()
        
        # Left child
        if i < len(values) and values[i] is not None:
            node.left = TreeNode(values[i])
            queue.append(node.left)
        i += 1
        
        # Right child
        if i < len(values) and values[i] is not None:
            node.right = TreeNode(values[i])
            queue.append(node.right)
        i += 1
    
    return root


# ================================================================================
# TEST CASES
# ================================================================================
if __name__ == "__main__":
    solution = Solution()
    solution_simple = SolutionSimpleRecursion()
    solution_bfs = SolutionIterativeBFS()
    
    test_cases = [
        (
            [1, 2, 3, 4, 5, 6],
            6,
            "Example 1: 6-node complete tree"
        ),
        (
            [],
            0,
            "Example 2: Empty tree"
        ),
        (
            [1],
            1,
            "Example 3: Single node"
        ),
        (
            [1, 2, 3],
            3,
            "Perfect tree height 1"
        ),
        (
            [1, 2, 3, 4, 5, 6, 7],
            7,
            "Perfect tree height 2"
        ),
        (
            [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
            15,
            "Perfect tree height 3"
        ),
        (
            [1, 2, 3, 4],
            4,
            "Last level: 1 node"
        ),
        (
            [1, 2, 3, 4, 5],
            5,
            "Last level: 2 nodes"
        ),
        (
            [1, 2, 3, 4, 5, 6, 7, 8],
            8,
            "Last level: 1 node (height 3)"
        ),
        (
            [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
            12,
            "Last level: 5 nodes"
        ),
    ]
    
    print("=" * 70)
    print("TESTING COUNT COMPLETE TREE NODES")
    print("=" * 70)
    print()
    
    solutions = [
        ("Optimal O(log²n)", solution),
        ("Simple O(n)", solution_simple),
        ("BFS O(n)", solution_bfs),
    ]
    
    for sol_name, sol in solutions:
        print(f"Testing: {sol_name}")
        print("-" * 70)
        
        passed = 0
        for values, expected, description in test_cases:
            root = build_tree(values)
            result = sol.countNodes(root)
            
            if result == expected:
                print(f"  ✅ {description}: {result} nodes")
                passed += 1
            else:
                print(f"  ❌ {description}")
                print(f"     Input: {values}")
                print(f"     Expected: {expected}, Got: {result}")
        
        print(f"\n  Results: {passed}/{len(test_cases)} passed\n")
    
    print("=" * 70)
    print("🎉 All solutions tested!")
    print("=" * 70)


# ================================================================================
# VISUALIZATION: How the Optimal Solution Works
# ================================================================================
"""
Example: 12-node complete tree

                1                   ← height 3
              /    \
            2        3              ← height 2
          /   \    /   \
        4      5  6     7           ← height 1
       / \   / \ /
      8   9 10 11 12                ← height 0 (last level)

═══════════════════════════════════════════════════════════════
CALL 1: countNodes(1)
═══════════════════════════════════════════════════════════════

  left_height  = height(2) = 3  (path: 2→4→8)
  right_height = height(3) = 2  (path: 3→6)

  left_height != right_height
  → RIGHT subtree (rooted at 3) is PERFECT with height 2
  → Nodes in right subtree = 2^2 - 1 = 3  (nodes 3, 6, 7)
  → Plus current node: 2^2 = 4
  → Recurse on LEFT subtree (rooted at 2)

  return 4 + countNodes(2)

═══════════════════════════════════════════════════════════════
CALL 2: countNodes(2)
═══════════════════════════════════════════════════════════════

            2
          /   \
        4      5
       / \   / \
      8   9 10 11 12... wait, 12 is under 6, not 5

  Corrected subtree rooted at 2:
            2
          /   \
        4      5
       / \   / \
      8   9 10 11

  left_height  = height(4) = 2  (path: 4→8)
  right_height = height(5) = 2  (path: 5→10)

  left_height == right_height
  → LEFT subtree (rooted at 4) is PERFECT with height 2
  → Nodes in left subtree = 2^2 - 1 = 3  (nodes 4, 8, 9)
  → Plus current node: 2^2 = 4
  → Recurse on RIGHT subtree (rooted at 5)

  return 4 + countNodes(5)

═══════════════════════════════════════════════════════════════
CALL 3: countNodes(5)
═══════════════════════════════════════════════════════════════

        5
       / \
      10  11

  left_height  = height(10) = 1
  right_height = height(11) = 1

  left_height == right_height
  → LEFT subtree is PERFECT with height 1
  → Nodes in left = 2^1 - 1 = 1  (node 10)
  → Plus current: 2^1 = 2
  → Recurse on RIGHT (node 11)

  return 2 + countNodes(11)

═══════════════════════════════════════════════════════════════
CALL 4: countNodes(11)
═══════════════════════════════════════════════════════════════

  left_height  = 0
  right_height = 0

  Equal → left is perfect (empty, height 0)
  return 2^0 + countNodes(None) = 1 + 0 = 1

═══════════════════════════════════════════════════════════════
UNWINDING:
═══════════════════════════════════════════════════════════════

  countNodes(11) = 1
  countNodes(5)  = 2 + 1 = 3
  countNodes(2)  = 4 + 3 = 7  (wait, but we need to also count node 12)

  Hmm — node 12 is under node 6 (right subtree of root).
  That was already counted in CALL 1 as part of the perfect
  right subtree... but the right subtree of root (rooted at 3)
  is NOT perfect here (it has node 12).

  Let me re-trace:
  
  Actually for 12 nodes, right subtree of 1 is:
        3
       / \
      6   7
     /
    12

  right_height = height(3→7) = 1... wait, we go LEFTMOST:
  height(3) goes 3→6→12 = 2

  So at root:
  left_height  = 3 (1→2→4→8)
  right_height = 2 (1→3→6→12... wait no)

  _get_height measures from the CHILD, not root.
  left_height  = get_height(root.left=2)  → 2→4→8 = 3
  right_height = get_height(root.right=3) → 3→6→12 = 3

  left_height == right_height = 3
  → Left subtree is PERFECT
  → Left has 2^3 - 1 = 7 nodes
  → return 2^3 + countNodes(3) = 8 + countNodes(3)

  countNodes(3):
    left_height  = get_height(6) = 2 (6→12)
    right_height = get_height(7) = 1 (7, no children)
    
    Not equal → right subtree (7) is perfect height 1
    return 2^1 + countNodes(6) = 2 + countNodes(6)

  countNodes(6):
    left_height  = get_height(12) = 1
    right_height = get_height(None) = 0
    
    Not equal → right is perfect height 0
    return 2^0 + countNodes(12) = 1 + 1 = 2

  countNodes(3) = 2 + 2 = 4
  countNodes(1) = 8 + 4 = 12 ✓
"""


# ================================================================================
# LEARNING NOTES
# ================================================================================
"""
PATTERN: Exploiting Complete Binary Tree Structure

This problem teaches a crucial interview skill:
recognizing when a data structure's properties can reduce complexity.

═══════════════════════════════════════════════════════════════
WHY THE NAIVE APPROACH IS WRONG HERE
═══════════════════════════════════════════════════════════════

Simple recursion (1 + left + right) is O(n).
The problem explicitly asks for LESS than O(n).

This is a signal: the "complete" property must be exploited.

═══════════════════════════════════════════════════════════════
THE KEY REALIZATION
═══════════════════════════════════════════════════════════════

In a complete binary tree, at any node, one of its two subtrees
is ALWAYS a perfect binary tree.

Perfect binary tree → we know the exact node count: 2^h - 1
No need to recurse into it!

This cuts the problem in half at each step → O(log n) depth.
Each step costs O(log n) for height measurement → O(log²n) total.

═══════════════════════════════════════════════════════════════
HOW TO DETERMINE WHICH SUBTREE IS PERFECT
═══════════════════════════════════════════════════════════════

Measure heights by going all the way LEFT in each subtree.

left_height == right_height:
  → Last level nodes exist in left subtree
  → Left subtree is perfect (fully filled including last level)
  → Right subtree might not be → recurse right

left_height != right_height:
  → Left subtree extends one level deeper
  → Right subtree is perfect (filled up to one level above last)
  → Left subtree might not be → recurse left

═══════════════════════════════════════════════════════════════
PERFECT TREE NODE COUNT FORMULA
═══════════════════════════════════════════════════════════════

Height h perfect tree:
  Level 0: 1 node   (root)
  Level 1: 2 nodes
  Level 2: 4 nodes
  ...
  Level h: 2^h nodes

  Total = 1 + 2 + 4 + ... + 2^h = 2^(h+1) - 1

In the code:
  Perfect subtree of height h has 2^h - 1 nodes
  Plus current node: total contribution = 2^h
  We use (1 << h) which is 2^h

═══════════════════════════════════════════════════════════════
RELATED PROBLEMS
═══════════════════════════════════════════════════════════════

1. LC 104: Maximum Depth of Binary Tree
   - Similar height measurement
   - But no optimization needed (must visit all nodes)

2. LC 226: Invert Binary Tree
   - Recursive tree transformation

3. LC 114: Flatten Binary Tree to Linked List
   - Tree structure manipulation

4. LC 297: Serialize and Deserialize Binary Tree
   - Complete tree serialization is simpler (level order)

═══════════════════════════════════════════════════════════════
INTERVIEW TIPS
═══════════════════════════════════════════════════════════════

1. Acknowledge the constraint
   "The problem asks for less than O(n), so I need to exploit
   the complete tree property somehow"

2. State the key insight clearly
   "In a complete binary tree, one subtree at each node is
   always perfect — I can count those directly"

3. Explain height measurement
   "Going all the way left gives the height because in a
   complete tree, the leftmost path is always the longest"

4. Derive the complexity
   "O(log n) recursive calls, each doing O(log n) height
   measurement = O(log²n) total"

5. Mention the naive approach first
   "The simple approach would be O(n) recursion visiting
   every node — but we can do better here"

COMMON MISTAKES:

❌ Measuring height incorrectly
   - Must go all the way LEFT (not right)
   - In complete tree, leftmost path = height

❌ Wrong perfect tree formula
   - Perfect tree of height h: 2^(h+1) - 1 nodes
   - But in our code h is measured from child: use 2^h

❌ Forgetting to count current node
   - return (1 << h) includes current node (2^h = 2^h - 1 + 1)

❌ Not handling empty tree
   - Must check if root is None at the start
"""


# ================================================================================
# PERFORMANCE BENCHMARK
# ================================================================================
if __name__ == "__main__":
    import time
    
    print("\n" + "=" * 70)
    print("PERFORMANCE BENCHMARK: O(log²n) vs O(n)")
    print("=" * 70)
    print()
    
    # Build complete trees of increasing sizes
    # Perfect trees are easiest to generate: 2^h - 1 nodes
    
    for h in range(5, 17):  # Heights 5 to 16
        size = (1 << h) - 1  # 2^h - 1 = perfect tree
        values = list(range(1, size + 1))
        root = build_tree(values)
        
        # Optimal solution
        start = time.perf_counter()
        for _ in range(1000):
            solution.countNodes(root)
        time_opt = (time.perf_counter() - start) * 1000
        
        # Simple recursion
        start = time.perf_counter()
        for _ in range(1000):
            solution_simple.countNodes(root)
        time_simple = (time.perf_counter() - start) * 1000
        
        print(f"  Height {h:>2}, Nodes {size:>6,}: "
              f"Optimal {time_opt:>8.2f}ms | "
              f"Simple {time_simple:>8.2f}ms | "
              f"Ratio {time_simple/time_opt:>5.1f}x")
    
    print("\n" + "=" * 70)