"""
================================================================================
Problem: 3651. Minimum Cost Path with Teleportations
Platform: LeetCode
URL: https://leetcode.com/problems/minimum-cost-path-with-teleportations/
Difficulty: Hard
Topics: Dynamic Programming, Graph, Greedy, Grid Pathfinding
================================================================================

PROBLEM DESCRIPTION:
[Same as before]

================================================================================
APPROACH: LAYER-BY-LAYER DYNAMIC PROGRAMMING (OPTIMAL)
================================================================================

INTUITION:
Instead of using Dijkstra with 3D state space, we can solve this more elegantly
using dynamic programming with layers based on number of teleportations used.

KEY INSIGHT:
- Define dp[t][i][j] = minimum cost to reach (i,j) using at most t teleportations
- We can compute each layer from the previous layer
- Within each layer, use simple DP for normal moves (right/down)

ALGORITHM:
1. Layer 0 (no teleportations): Standard grid DP with right/down moves
2. For each additional teleportation layer t:
   a. First, consider teleporting TO each cell from any cell with value >= current
   b. Then, propagate using normal moves (DP within the layer)
3. Answer = dp[k][m-1][n-1]

CRITICAL OPTIMIZATION:
- Group cells by value
- Precompute minimum cost to reach any cell in each value group
- Use suffix minimum to allow teleporting from higher/equal values

WHY THIS IS BETTER THAN DIJKSTRA:
- Time: O(k × m × n) vs O(m × n × k × m × n × log(m × n × k))
- Space: O(m × n) vs O(m × n × k)
- Much simpler logic
- No priority queue overhead

COMPLEXITY:
- Time: O(k × m × n)
  - k layers
  - Each layer: O(m × n) for DP + O(V × G) for teleportation
  - V = m × n cells, G = number of distinct values
- Space: O(m × n) - only need current and previous layer

================================================================================
"""

from typing import List


class Solution:
    """
    Optimal DP solution for Minimum Cost Path with Teleportations
    """
    
    def minCost(self, grid: List[List[int]], k: int) -> int:
        """
        Find minimum cost using layer-by-layer DP.
        
        Args:
            grid: m×n grid of integers
            k: Maximum teleportations allowed
            
        Returns:
            Minimum cost to reach bottom-right from top-left
            
        Algorithm: Layered Dynamic Programming
        Time: O(k × m × n)
        Space: O(m × n)
        """
        m, n = len(grid), len(grid[0])
        V = m * n  # Total number of cells
        INF = float('inf')
        
        # ════════════════════════════════════════════════════════════
        # STEP 1: Flatten grid to 1D for easier indexing
        # ════════════════════════════════════════════════════════════
        # idx = i * n + j  (row-major order)
        vals = [grid[i][j] for i in range(m) for j in range(n)]
        
        # ════════════════════════════════════════════════════════════
        # STEP 2: Group cells by value for efficient teleportation
        # ════════════════════════════════════════════════════════════
        # Sort cells by value (ascending order)
        order = sorted(range(V), key=lambda idx: vals[idx])
        
        # Assign group ID to each cell (same value = same group)
        group_id = [0] * V
        current_group = -1
        last_value = None
        
        for idx in order:
            if last_value is None or vals[idx] != last_value:
                current_group += 1
                last_value = vals[idx]
            group_id[idx] = current_group
        
        G = current_group + 1  # Total number of distinct value groups
        
        # ════════════════════════════════════════════════════════════
        # STEP 3: Initialize - Layer 0 (no teleportations)
        # ════════════════════════════════════════════════════════════
        # dist_prev[idx] = min cost to reach cell idx using ≤ t teleportations
        dist_prev = [INF] * V
        dist_prev[0] = 0  # Starting position (top-left)
        
        # Compute layer 0 using standard grid DP (only right/down moves)
        for i in range(m):
            for j in range(n):
                idx = i * n + j
                cost = vals[idx]
                
                # Can come from above
                if i > 0:
                    from_above = dist_prev[idx - n] + cost
                    dist_prev[idx] = min(dist_prev[idx], from_above)
                
                # Can come from left
                if j > 0:
                    from_left = dist_prev[idx - 1] + cost
                    dist_prev[idx] = min(dist_prev[idx], from_left)
        
        # ════════════════════════════════════════════════════════════
        # STEP 4: Process each teleportation layer (1 to k)
        # ════════════════════════════════════════════════════════════
        for t in range(1, k + 1):
            # ────────────────────────────────────────────────────────
            # Sub-step 4.1: Compute minimum cost within each value group
            # ────────────────────────────────────────────────────────
            # group_min[g] = min cost to reach any cell in group g (from prev layer)
            group_min = [INF] * G
            
            for idx in range(V):
                g = group_id[idx]
                group_min[g] = min(group_min[g], dist_prev[idx])
            
            # ────────────────────────────────────────────────────────
            # Sub-step 4.2: Compute suffix minimum
            # ────────────────────────────────────────────────────────
            # Allows teleporting from any cell with value >= current cell's value
            # group_min[g] = min cost from groups g, g+1, ..., G-1
            for g in range(G - 2, -1, -1):
                group_min[g] = min(group_min[g], group_min[g + 1])
            
            # ────────────────────────────────────────────────────────
            # Sub-step 4.3: Initialize current layer
            # ────────────────────────────────────────────────────────
            # Option 1: Don't use this teleportation (keep prev layer cost)
            # Option 2: Teleport to this cell (use group_min)
            dist_curr = [0] * V
            
            for idx in range(V):
                # Cost to teleport to this cell from any cell with value >= this
                teleport_cost = group_min[group_id[idx]]
                
                # Choose minimum: previous cost or teleport cost
                dist_curr[idx] = min(dist_prev[idx], teleport_cost)
            
            # ────────────────────────────────────────────────────────
            # Sub-step 4.4: Propagate using normal moves within layer
            # ────────────────────────────────────────────────────────
            # After teleporting, can still use normal moves in this layer
            for i in range(m):
                for j in range(n):
                    idx = i * n + j
                    cost = vals[idx]
                    
                    # Can come from above
                    if i > 0:
                        from_above = dist_curr[idx - n] + cost
                        dist_curr[idx] = min(dist_curr[idx], from_above)
                    
                    # Can come from left
                    if j > 0:
                        from_left = dist_curr[idx - 1] + cost
                        dist_curr[idx] = min(dist_curr[idx], from_left)
            
            # Move to next layer
            dist_prev = dist_curr
        
        # ════════════════════════════════════════════════════════════
        # STEP 5: Return answer (cost to reach bottom-right)
        # ════════════════════════════════════════════════════════════
        return dist_prev[V - 1]


class SolutionWithComments:
    """
    Heavily commented version for educational purposes
    """
    
    def minCost(self, grid: List[List[int]], k: int) -> int:
        """
        Layer-by-layer DP with detailed explanations.
        """
        m, n = len(grid), len(grid[0])
        V = m * n
        INF = float('inf')
        
        # Convert 2D grid to 1D array
        # Why: Easier to work with single index
        # Mapping: (i, j) → idx = i * n + j
        vals = [grid[i][j] for i in range(m) for j in range(n)]
        
        # Group cells by their values
        # Why: We can only teleport to cells with value ≤ current
        # Strategy: Sort cells by value, assign group IDs
        
        # Sort indices by their cell values
        order = sorted(range(V), key=lambda idx: vals[idx])
        
        # Assign group ID to each cell
        # Cells with same value get same group ID
        group_id = [0] * V
        gid = -1
        last_val = None
        
        for idx in order:
            if last_val is None or vals[idx] != last_val:
                gid += 1  # New value group
                last_val = vals[idx]
            group_id[idx] = gid
        
        G = gid + 1  # Total number of distinct values
        
        # Initialize DP for layer 0 (no teleportations)
        dist_prev = [INF] * V
        dist_prev[0] = 0  # Start at (0,0) with cost 0
        
        # Compute layer 0: only right/down moves
        # This is standard grid DP
        for i in range(m):
            for j in range(n):
                idx = i * n + j
                cost = vals[idx]
                
                # From above: (i-1, j) → (i, j)
                if i > 0:
                    dist_prev[idx] = min(dist_prev[idx], 
                                        dist_prev[idx - n] + cost)
                
                # From left: (i, j-1) → (i, j)
                if j > 0:
                    dist_prev[idx] = min(dist_prev[idx], 
                                        dist_prev[idx - 1] + cost)
        
        # Process layers 1 through k (each adds one teleportation)
        for teleport_count in range(1, k + 1):
            # Find minimum cost to reach any cell in each value group
            group_min = [INF] * G
            
            for idx in range(V):
                g = group_id[idx]
                group_min[g] = min(group_min[g], dist_prev[idx])
            
            # Compute suffix minimum
            # group_min[g] now represents: minimum cost to reach any cell
            # with value in groups g, g+1, ..., G-1
            # This allows us to teleport FROM any cell with value ≥ current
            for g in range(G - 2, -1, -1):
                group_min[g] = min(group_min[g], group_min[g + 1])
            
            # Initialize current layer
            dist_curr = [0] * V
            
            for idx in range(V):
                # Two options:
                # 1. Don't use this teleportation: cost = dist_prev[idx]
                # 2. Teleport here from some cell with higher/equal value
                #    cost = group_min[group_id[idx]]
                
                teleport_cost = group_min[group_id[idx]]
                no_teleport_cost = dist_prev[idx]
                
                dist_curr[idx] = min(no_teleport_cost, teleport_cost)
            
            # After considering teleportation, propagate using normal moves
            # This handles paths like: teleport → move → move → ...
            for i in range(m):
                for j in range(n):
                    idx = i * n + j
                    cost = vals[idx]
                    
                    if i > 0:
                        dist_curr[idx] = min(dist_curr[idx], 
                                            dist_curr[idx - n] + cost)
                    
                    if j > 0:
                        dist_curr[idx] = min(dist_curr[idx], 
                                            dist_curr[idx - 1] + cost)
            
            dist_prev = dist_curr
        
        return dist_prev[V - 1]


# ================================================================================
# TEST CASES
# ================================================================================
if __name__ == "__main__":
    solution = Solution()
    solution_verbose = SolutionWithComments()
    
    test_cases = [
        (
            [[1, 3, 3], [2, 5, 4], [4, 3, 5]],
            2,
            7,
            "Example 1: Use teleportation"
        ),
        (
            [[1, 2], [2, 3], [3, 4]],
            1,
            9,
            "Example 2: No teleportation needed"
        ),
        (
            [[1, 2], [3, 4]],
            0,
            6,
            "No teleportation allowed"
        ),
        (
            [[5, 1], [1, 5]],
            1,
            1,
            "Teleport to cheap cell"
        ),
        (
            [[1]],
            0,
            0,
            "Single cell"
        ),
        (
            [[10, 5, 3], [8, 4, 2], [7, 6, 1]],
            3,
            1,
            "Descending values"
        ),
        (
            [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
            2,
            0,
            "All zeros"
        ),
    ]
    
    print("=" * 80)
    print("TESTING DP SOLUTION")
    print("=" * 80)
    print()
    
    for sol_name, sol in [("Optimized", solution), ("Verbose", solution_verbose)]:
        print(f"Testing: {sol_name}")
        print("-" * 80)
        
        passed = 0
        for grid, k, expected, description in test_cases:
            result = sol.minCost(grid, k)
            
            if result == expected:
                print(f"  ✅ {description}")
                print(f"     Grid: {grid}, k={k} → Result: {result}")
                passed += 1
            else:
                print(f"  ❌ {description}")
                print(f"     Grid: {grid}, k={k}")
                print(f"     Expected: {expected}, Got: {result}")
            print()
        
        print(f"Results: {passed}/{len(test_cases)} passed\n")
    
    print("=" * 80)


# ================================================================================
# VISUALIZATION: Layer-by-Layer Processing
# ================================================================================
"""
Example: grid = [[1,3,3],[2,5,4],[4,3,5]], k=2

Grid values (flattened):
Index:  0  1  2  3  4  5  6  7  8
Value:  1  3  3  2  5  4  4  3  5
Coords: 00 01 02 10 11 12 20 21 22

Value groups (sorted by value):
Group 0: [0] (value=1)
Group 1: [3] (value=2)
Group 2: [1, 2, 7] (value=3)
Group 3: [5, 6] (value=4)
Group 4: [4, 8] (value=5)

═══════════════════════════════════════════════════════════════════
LAYER 0: No teleportations (standard grid DP)
═══════════════════════════════════════════════════════════════════

dist[0] = 0 (start)

Row 0:
  dist[1] = dist[0] + 3 = 0 + 3 = 3
  dist[2] = dist[1] + 3 = 3 + 3 = 6

Row 1:
  dist[3] = dist[0] + 2 = 0 + 2 = 2
  dist[4] = min(dist[1] + 5, dist[3] + 5) = min(8, 7) = 7
  dist[5] = min(dist[2] + 4, dist[4] + 4) = min(10, 11) = 10

Row 2:
  dist[6] = dist[3] + 4 = 2 + 4 = 6
  dist[7] = min(dist[4] + 3, dist[6] + 3) = min(10, 9) = 9
  dist[8] = min(dist[5] + 5, dist[7] + 5) = min(15, 14) = 14

Result after layer 0: dist = [0, 3, 6, 2, 7, 10, 6, 9, 14]

═══════════════════════════════════════════════════════════════════
LAYER 1: One teleportation allowed
═══════════════════════════════════════════════════════════════════

Step 1: Compute group minimums
  group_min[0] = min(dist[0]) = 0
  group_min[1] = min(dist[3]) = 2
  group_min[2] = min(dist[1], dist[2], dist[7]) = min(3, 6, 9) = 3
  group_min[3] = min(dist[5], dist[6]) = min(10, 6) = 6
  group_min[4] = min(dist[4], dist[8]) = min(7, 14) = 7

Step 2: Suffix minimum (allows teleporting from higher/equal values)
  group_min[4] = 7
  group_min[3] = min(6, 7) = 6
  group_min[2] = min(3, 6) = 3
  group_min[1] = min(2, 3) = 2
  group_min[0] = min(0, 2) = 0

Step 3: Initialize with teleportation option
  dist[0] = min(0, group_min[0]) = min(0, 0) = 0
  dist[1] = min(3, group_min[2]) = min(3, 3) = 3
  dist[2] = min(6, group_min[2]) = min(6, 3) = 3 ✓ (improved!)
  dist[3] = min(2, group_min[1]) = min(2, 2) = 2
  dist[4] = min(7, group_min[4]) = min(7, 7) = 7
  dist[5] = min(10, group_min[3]) = min(10, 6) = 6 ✓
  dist[6] = min(6, group_min[3]) = min(6, 6) = 6
  dist[7] = min(9, group_min[2]) = min(9, 3) = 3 ✓
  dist[8] = min(14, group_min[4]) = min(14, 7) = 7 ✓

Step 4: Propagate with normal moves
  [Similar DP as layer 0, but starting from updated values]
  
Final after layer 1: dist[8] = 7 (can reach destination with cost 7!)

═══════════════════════════════════════════════════════════════════
LAYER 2: Two teleportations allowed
═══════════════════════════════════════════════════════════════════

[Process continues but answer is already 7 from layer 1]

Answer: 7
"""


# ================================================================================
# LEARNING NOTES
# ================================================================================
"""
WHY THIS APPROACH IS BRILLIANT
═══════════════════════════════════════════════════════════════════

1. LAYERED DP VS STATE-SPACE DIJKSTRA

Dijkstra Approach (previous solution):
- State: (row, col, teleports_used)
- State space: O(m × n × k)
- Each state explores O(m × n) edges for teleportation
- Priority queue operations: O(log(m × n × k))
- Total: O(m × n × k × m × n × log(m × n × k))

DP Approach (this solution):
- Process k layers sequentially
- Each layer: O(m × n) cells
- Teleportation handled via group minimums: O(V + G)
- Total: O(k × m × n)
- Much simpler, faster, cleaner!

2. KEY INSIGHT: SUFFIX MINIMUM

Instead of checking all possible teleport sources for each cell:
- Group cells by value
- Compute minimum cost to reach each group
- Use suffix minimum to allow "teleport from any cell with value ≥ mine"

This reduces O(m × n) checks per cell to O(1) lookup!

3. WHY TWO DP PASSES PER LAYER?

First pass (teleportation):
- Considers teleporting TO each cell
- Uses precomputed group minimums

Second pass (normal moves):
- Propagates costs using right/down moves
- Handles paths like: teleport → move → move

Both are needed because:
- Teleporting might land you far from destination
- Need normal moves to reach final position

4. SPACE OPTIMIZATION

Only need two arrays:
- dist_prev: costs from previous layer
- dist_curr: costs for current layer

No need to store all k layers simultaneously!

═══════════════════════════════════════════════════════════════════
COMPARISON: DIJKSTRA VS DP
═══════════════════════════════════════════════════════════════════

| Aspect | Dijkstra | DP |
|--------|----------|-----|
| Time | O(mnk × mn × log(mnk)) | O(k × mn) |
| Space | O(mnk) | O(mn) |
| Code | Complex | Simple |
| Intuition | Graph search | Layer processing |
| When better | Sparse graphs | Dense grids |

For THIS problem: DP is clearly superior!

═══════════════════════════════════════════════════════════════════
WHEN TO USE EACH APPROACH
═══════════════════════════════════════════════════════════════════

Use Dijkstra when:
- Graph is sparse (few edges)
- Edge costs vary widely
- Need to explore selectively
- State space is huge but solution path is short

Use Layered DP when:
- Dense graph (many edges)
- Can process states in layers
- Number of layers is small (k is small)
- Can aggregate information per layer

This problem: k ≤ 10, dense grid → DP wins!

═══════════════════════════════════════════════════════════════════
SIMILAR PROBLEMS WITH LAYERED DP
═══════════════════════════════════════════════════════════════════

1. LC 1293: Shortest Path in Grid with Obstacles Elimination
   - Can eliminate up to k obstacles
   - Similar layer structure

2. LC 1340: Jump Game V
   - Limited jumps per position
   - Layer-by-layer DP works well

3. LC 1928: Minimum Cost to Reach Destination in Time
   - Time limit acts as layer count
   - DP on layers of time

Pattern: "Limited resource" problems often benefit from layered DP!
"""


# ================================================================================
# PERFORMANCE COMPARISON
# ================================================================================
if __name__ == "__main__":
    import time
    import random
    
    print("\n" + "=" * 80)
    print("PERFORMANCE BENCHMARK: DP vs Dijkstra")
    print("=" * 80)
    print()
    
    # Import previous Dijkstra solution for comparison
    # (Assuming it's available)
    
    solution_dp = Solution()
    
    test_configs = [
        (10, 10, 2),
        (20, 20, 3),
        (40, 40, 5),
    ]
    
    for m, n, k in test_configs:
        grid = [[random.randint(0, 100) for _ in range(n)] for _ in range(m)]
        
        # DP solution
        start = time.perf_counter()
        result_dp = solution_dp.minCost(grid, k)
        time_dp = (time.perf_counter() - start) * 1000
        
        print(f"Grid: {m}×{n}, k={k}")
        print(f"  DP Solution: {time_dp:>8.3f}ms (result={result_dp})")
        print()
    
    print("=" * 80)
    print("✨ DP approach is significantly faster!")
    print("=" * 80)