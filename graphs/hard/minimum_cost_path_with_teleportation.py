"""
================================================================================
Problem: 3651. Minimum Cost Path with Teleportations
Platform: LeetCode
URL: https://leetcode.com/problems/minimum-cost-path-with-teleportations/
Difficulty: Hard
Topics: Graph, Shortest Path, Dijkstra's Algorithm, Dynamic Programming, Grid
================================================================================

PROBLEM DESCRIPTION:
You are given an m x n 2D integer array grid and an integer k. You start at the 
top-left cell (0, 0) and your goal is to reach the bottom-right cell (m-1, n-1).

Two types of moves available:
1. Normal move: Move right or down. Cost = value of destination cell.
2. Teleportation: Teleport to any cell with value <= current cell. Cost = 0.
   You may teleport at most k times.

Return the minimum total cost to reach cell (m-1, n-1) from (0, 0).

CONSTRAINTS:
- 2 <= m, n <= 80
- m == grid.length
- n == grid[i].length
- 0 <= grid[i][j] <= 10^4
- 0 <= k <= 10

EXAMPLES:

Example 1:
Input: grid = [[1,3,3],[2,5,4],[4,3,5]], k = 2
Output: 7
Explanation:
- (0,0) → (1,0): cost 2 (move down)
- (1,0) → (1,1): cost 5 (move right)
- (1,1) → (2,2): cost 0 (teleport, grid[2][2]=5 <= grid[1][1]=5)
- Total: 7

Example 2:
Input: grid = [[1,2],[2,3],[3,4]], k = 1
Output: 9
Explanation: Standard path without using teleportation.

================================================================================
INTUITION:
This is a shortest path problem with state-dependent edges. The twist is that
we can teleport for free, but only to cells with smaller/equal values, and
we have a limited number of teleports.

KEY INSIGHTS:

1. State Definition
   - We need to track: (row, col, teleports_remaining)
   - Same cell with different teleports remaining = different states

2. Graph Edges
   - Normal moves: (i,j,t) → (i+1,j,t) or (i,j+1,t) with cost grid[dest]
   - Teleport: (i,j,t) → (x,y,t-1) with cost 0, if grid[x][y] <= grid[i][j]

3. Algorithm Choice
   - Dijkstra's algorithm is perfect here (non-negative weights)
   - State space: O(m × n × k)
   - Need priority queue to always process lowest-cost state first

APPROACH:
1. Use Dijkstra with state (row, col, teleports_used)
2. From each state, try:
   - Move right/down (normal moves)
   - Teleport to all valid cells (if teleports remaining)
3. Track minimum cost to reach (m-1, n-1) with any number of teleports used

COMPLEXITY ANALYSIS:
- Time: O(m × n × k × (m × n) × log(m × n × k))
  - States: m × n × k
  - For each state: potentially check all m × n cells for teleportation
  - Priority queue operations: log(states)
  - In practice, much faster due to early termination
- Space: O(m × n × k) for distance tracking and priority queue

OPTIMIZATION:
- Early termination when destination is reached
- Skip states that are already processed with better cost
- Pre-sort cells by value for efficient teleport target lookup

================================================================================
"""

from typing import List, Tuple
from heapq import heappush, heappop
import collections


class Solution:
    """LC 3651: Minimum Cost Path with Teleportations"""
    
    def minCost(self, grid: List[List[int]], k: int) -> int:
        """
        Find minimum cost path with teleportation ability.
        
        Args:
            grid: m×n grid of integers
            k: Maximum number of teleportations allowed
            
        Returns:
            Minimum cost to reach bottom-right from top-left
            
        Algorithm: Dijkstra's with 3D state space
        Time: O(m × n × k × m × n × log(m × n × k))
        Space: O(m × n × k)
        """
        m, n = len(grid), len(grid[0])
        
        # Edge case: already at destination
        if m == 1 and n == 1:
            return 0
        
        # Priority queue: (cost, row, col, teleports_used)
        pq = [(0, 0, 0, 0)]  # Start at (0,0) with 0 cost, 0 teleports used
        
        # Track minimum cost to reach each state: (row, col, teleports_used)
        # Use dictionary for sparse storage
        min_cost = {}
        min_cost[(0, 0, 0)] = 0
        
        # Directions for normal moves: down, right
        directions = [(1, 0), (0, 1)]
        
        # Dijkstra's algorithm
        while pq:
            cost, r, c, tele_used = heappop(pq)
            
            # Early termination: reached destination
            if r == m - 1 and c == n - 1:
                return cost
            
            # Skip if we've found a better path to this state
            state = (r, c, tele_used)
            if state in min_cost and cost > min_cost[state]:
                continue
            
            # Option 1: Normal moves (down or right)
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                
                # Check bounds
                if 0 <= nr < m and 0 <= nc < n:
                    new_cost = cost + grid[nr][nc]
                    new_state = (nr, nc, tele_used)
                    
                    # Update if this is a better path
                    if new_state not in min_cost or new_cost < min_cost[new_state]:
                        min_cost[new_state] = new_cost
                        heappush(pq, (new_cost, nr, nc, tele_used))
            
            # Option 2: Teleportation (if we have teleports remaining)
            if tele_used < k:
                current_value = grid[r][c]
                
                # Try teleporting to all cells with value <= current
                for tr in range(m):
                    for tc in range(n):
                        # Can only teleport to cells with smaller/equal value
                        if grid[tr][tc] <= current_value:
                            # Skip if same cell
                            if tr == r and tc == c:
                                continue
                            
                            # Teleportation costs 0
                            new_cost = cost
                            new_state = (tr, tc, tele_used + 1)
                            
                            # Update if this is a better path
                            if new_state not in min_cost or new_cost < min_cost[new_state]:
                                min_cost[new_state] = new_cost
                                heappush(pq, (new_cost, tr, tc, tele_used + 1))
        
        # If we couldn't reach destination (shouldn't happen with valid input)
        return -1


class SolutionOptimized:
    """
    Optimized version with pre-sorted cells for faster teleport lookup
    """
    
    def minCost(self, grid: List[List[int]], k: int) -> int:
        """
        Optimized solution that pre-sorts cells by value.
        
        This allows us to quickly find all valid teleport destinations.
        """
        m, n = len(grid), len(grid[0])
        
        if m == 1 and n == 1:
            return 0
        
        # Pre-sort all cells by their values for efficient teleport lookup
        # cells_by_value[v] = list of (row, col) with grid[row][col] = v
        cells_by_value = collections.defaultdict(list)
        for i in range(m):
            for j in range(n):
                cells_by_value[grid[i][j]].append((i, j))
        
        # Sort values for easier lookup
        sorted_values = sorted(cells_by_value.keys())
        
        # Dijkstra's algorithm
        pq = [(0, 0, 0, 0)]  # (cost, row, col, teleports_used)
        min_cost = {}
        min_cost[(0, 0, 0)] = 0
        
        directions = [(1, 0), (0, 1)]
        
        while pq:
            cost, r, c, tele_used = heappop(pq)
            
            # Early termination
            if r == m - 1 and c == n - 1:
                return cost
            
            state = (r, c, tele_used)
            if state in min_cost and cost > min_cost[state]:
                continue
            
            # Normal moves
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                
                if 0 <= nr < m and 0 <= nc < n:
                    new_cost = cost + grid[nr][nc]
                    new_state = (nr, nc, tele_used)
                    
                    if new_state not in min_cost or new_cost < min_cost[new_state]:
                        min_cost[new_state] = new_cost
                        heappush(pq, (new_cost, nr, nc, tele_used))
            
            # Teleportation (optimized lookup)
            if tele_used < k:
                current_value = grid[r][c]
                
                # Find all cells with value <= current_value
                for v in sorted_values:
                    if v > current_value:
                        break  # All remaining values are too large
                    
                    for tr, tc in cells_by_value[v]:
                        if tr == r and tc == c:
                            continue
                        
                        new_cost = cost  # Teleport is free
                        new_state = (tr, tc, tele_used + 1)
                        
                        if new_state not in min_cost or new_cost < min_cost[new_state]:
                            min_cost[new_state] = new_cost
                            heappush(pq, (new_cost, tr, tc, tele_used + 1))
        
        return -1


# ================================================================================
# TEST CASES
# ================================================================================
if __name__ == "__main__":
    solution = Solution()
    solution_opt = SolutionOptimized()
    
    test_cases = [
        # (grid, k, expected, description)
        (
            [[1, 3, 3], [2, 5, 4], [4, 3, 5]],
            2,
            7,
            "Example 1: Use teleportation twice"
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
            "No teleportation allowed: 2+4=6"
        ),
        (
            [[5, 1], [1, 5]],
            1,
            1,
            "Teleport to cheap cell: 0→(0,1) costs 1"
        ),
        (
            [[1]],
            0,
            0,
            "Single cell grid"
        ),
        (
            [[10, 5, 3], [8, 4, 2], [7, 6, 1]],
            3,
            1,
            "Descending values: teleport to (2,2) with value 1"
        ),
        (
            [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
            0,
            33,
            "Ascending: 2+3+5+6+8+9=33"
        ),
        (
            [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
            2,
            0,
            "All zeros: teleport costs 0, destination has 0"
        ),
    ]
    
    print("=" * 80)
    print("TESTING MINIMUM COST PATH WITH TELEPORTATIONS")
    print("=" * 80)
    print()
    
    for sol_name, sol in [("Standard", solution), ("Optimized", solution_opt)]:
        print(f"Testing: {sol_name} Solution")
        print("-" * 80)
        
        passed = 0
        for grid, k, expected, description in test_cases:
            result = sol.minCost(grid, k)
            
            if result == expected:
                print(f"  ✅ {description}")
                print(f"     Grid: {grid}, k={k}")
                print(f"     Result: {result}")
                passed += 1
            else:
                print(f"  ❌ {description}")
                print(f"     Grid: {grid}, k={k}")
                print(f"     Expected: {expected}")
                print(f"     Got: {result}")
            print()
        
        print(f"Results: {passed}/{len(test_cases)} passed\n")
    
    print("=" * 80)
    print("🎉 All solutions tested!")
    print("=" * 80)


# ================================================================================
# VISUALIZATION: Example 1
# ================================================================================
"""
Grid: [[1,3,3],[2,5,4],[4,3,5]], k=2

Visual representation:
    0   1   2
  ┌───┬───┬───┐
0 │ 1 │ 3 │ 3 │
  ├───┼───┼───┤
1 │ 2 │ 5 │ 4 │
  ├───┼───┼───┤
2 │ 4 │ 3 │ 5 │
  └───┴───┴───┘

Dijkstra's execution:

Initial state: (0,0) with cost 0, teleports_used = 0

Step 1: Process (0,0), cost=0
  Normal moves:
    - Down to (1,0): cost = 0 + 2 = 2 ✓
    - Right to (0,1): cost = 0 + 3 = 3
  Teleport (grid[0][0]=1, can teleport to cells <= 1):
    - Only cell with value <= 1 is (0,0) itself (skip)
  
  Queue: [(2, 1,0, 0), (3, 0,1, 0)]

Step 2: Process (1,0), cost=2
  Normal moves:
    - Down to (2,0): cost = 2 + 4 = 6
    - Right to (1,1): cost = 2 + 5 = 7 ✓
  Teleport (grid[1][0]=2, can teleport to cells <= 2):
    - (0,0): cost = 2, state = (0,0,1) (already have better)
    - (1,0): skip self
  
  Queue: [(3, 0,1, 0), (6, 2,0, 0), (7, 1,1, 0)]

Step 3: Process (0,1), cost=3
  Normal moves:
    - Down to (1,1): cost = 3 + 5 = 8
    - Right to (0,2): cost = 3 + 3 = 6
  Teleport options...
  
  Queue: [(6, 0,2, 0), (6, 2,0, 0), (7, 1,1, 0), ...]

Step 4: Process (0,2), cost=6
  Normal moves:
    - Down to (1,2): cost = 6 + 4 = 10
  Teleport (grid[0][2]=3):
    - Can teleport to (0,0)=1, (1,0)=2, (2,1)=3
  
  Continue...

Step N: Process (1,1), cost=7
  Normal moves:
    - Down to (2,1): cost = 7 + 3 = 10
    - Right to (1,2): cost = 7 + 4 = 11
  Teleport (grid[1][1]=5, can teleport to all cells):
    - Teleport to (2,2): cost = 7 + 0 = 7 ✓ (DESTINATION!)

Answer: 7

Optimal path:
(0,0) --move down--> (1,0) --move right--> (1,1) --teleport--> (2,2)
Costs:      0              +2                +5                 +0      = 7
"""


# ================================================================================
# STEP-BY-STEP STATE EXPLORATION
# ================================================================================
"""
State format: (row, col, teleports_used, cost)

Priority Queue evolution:

Initial:
  pq = [(0, 0, 0, 0)]

Pop (0, 0, 0, 0):
  Add: (2, 1, 0, 0) - move down
  Add: (3, 0, 1, 0) - move right
  pq = [(2, 1, 0, 0), (3, 0, 1, 0)]

Pop (2, 1, 0, 0):
  Add: (6, 2, 0, 0) - move down
  Add: (7, 1, 1, 0) - move right
  Teleport: (2, 0, 0, 1) - teleport to (0,0)
  pq = [(2, 0, 0, 1), (3, 0, 1, 0), (6, 2, 0, 0), (7, 1, 1, 0)]

... (many states explored) ...

Pop (7, 1, 1, 0):
  Normal moves would cost more
  Teleport to (2, 2): cost = 7, teleports = 1
  Add: (7, 2, 2, 1) - teleport to destination!
  pq = [... (7, 2, 2, 1) ...]

Pop (7, 2, 2, 1):
  This is the destination! Return 7.

Final answer: 7
"""


# ================================================================================
# LEARNING NOTES
# ================================================================================
"""
PATTERN: State-Space Dijkstra with Action Constraints

This problem combines several advanced concepts:
1. Shortest path in implicit graph
2. State-dependent edges (teleportation depends on current cell value)
3. Limited resource (k teleportations)
4. Multi-dimensional state space

KEY TECHNIQUES:

1. State Definition
   - (row, col, teleports_used) forms the complete state
   - Same position with different teleports = different states
   - State space size: O(m × n × k)

2. Edge Generation
   - Dynamic edges based on current state
   - Teleportation creates O(m × n) potential edges per state
   - Need to check all cells for valid teleport targets

3. Dijkstra's Algorithm
   - Perfect for non-negative weights
   - Priority queue ensures optimal path found first
   - Early termination when destination reached

4. Optimization Strategies
   - Pre-sort cells by value for faster teleport lookup
   - Skip already-processed states
   - Early termination at destination

SIMILAR PROBLEMS:

1. LC 1631: Path With Minimum Effort
   - Grid pathfinding with effort constraint
   - Use Dijkstra or binary search + BFS

2. LC 1976: Number of Ways to Arrive at Destination
   - Shortest paths with counting
   - Dijkstra + DP combination

3. LC 787: Cheapest Flights Within K Stops
   - Similar constraint on number of special moves
   - State includes remaining stops

4. LC 1293: Shortest Path in Grid with Obstacles Elimination
   - Can remove up to k obstacles
   - State: (row, col, obstacles_removed)

5. LC 2290: Minimum Obstacle Removal to Reach Corner
   - 0-1 BFS variant
   - Grid with free/costly moves

COMPLEXITY ANALYSIS DEEP DIVE:

State Space:
- Total states: m × n × (k+1)
- Each state can be added to queue once

Edge Generation:
- Normal moves: 2 edges per state
- Teleportation: up to m × n edges per state
- Total edges per state: O(m × n)

Priority Queue:
- Size: O(m × n × k)
- Each operation: O(log(m × n × k))

Overall:
- Worst case: O(m × n × k × m × n × log(m × n × k))
- Practical: Much better due to early termination and pruning

OPTIMIZATION TECHNIQUES:

1. Pre-sorting Cells
   - Sort cells by value once: O(m × n × log(m × n))
   - Binary search for valid teleport targets: O(log(m × n))
   - Reduces teleport edge generation time

2. Lazy State Expansion
   - Don't generate all teleport edges upfront
   - Only create edges when state is processed

3. Bidirectional Search
   - Could search from both start and end
   - Meet in the middle for potentially 2× speedup

4. A* Heuristic
   - Use Manhattan distance as heuristic
   - Reduces states explored

COMMON MISTAKES:

❌ Forgetting to track teleports used in state
   - Results in incorrect path costs

❌ Not handling state duplicates properly
   - Same cell with different teleport counts = different states

❌ Checking teleport validity incorrectly
   - Must check grid[dest] <= grid[current], not 

❌ Not considering all teleport targets
   - Must check all cells, not just reachable ones

❌ Inefficient teleport target lookup
   - Checking all m×n cells every time is slow

INTERVIEW TIPS:

1. Start with State Definition
   "We need to track (row, col, teleports_used) as our state"

2. Explain Edge Cases
   "Teleportation is only valid when destination value <= current value"

3. Justify Dijkstra
   "All costs are non-negative, so Dijkstra guarantees optimal path"

4. Discuss Optimization
   "We could pre-sort cells by value for faster teleport lookup"

5. Analyze Complexity
   "State space is O(m×n×k), each state can generate O(m×n) edges"

6. Mention Alternatives
   "Could use DP, but Dijkstra handles the teleportation elegantly"

REAL-WORLD APPLICATIONS:

- Navigation apps with toll roads (limited "free pass" usage)
- Network routing with fast lanes (limited bandwidth)
- Game pathfinding with teleportation abilities
- Resource allocation with constraints
- Logistics with express shipping options

WHY THIS PROBLEM IS HARD:

1. Multi-dimensional state space (3D: row, col, teleports)
2. Dynamic edge generation (depends on current cell value)
3. Large branching factor (O(m×n) edges per state)
4. Requires deep understanding of Dijkstra
5. Optimization needed for efficiency

PATTERN RECOGNITION:

See these keywords → Think this approach:
- "Grid" + "minimum cost" → Graph/Dijkstra
- "Limited resource" → State includes resource count
- "Special moves" → Multi-dimensional state
- "Shortest path" + "constraints" → Modified Dijkstra

This problem teaches you to:
1. Model complex problems as graph search
2. Design appropriate state spaces
3. Optimize state-space search
4. Handle action constraints elegantly
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
    solution_opt = SolutionOptimized()
    
    test_configs = [
        (10, 10, 2),   # Small grid
        (20, 20, 3),   # Medium grid
        (40, 40, 5),   # Large grid
    ]
    
    for m, n, k in test_configs:
        # Generate random grid
        grid = [[random.randint(0, 100) for _ in range(n)] for _ in range(m)]
        
        # Standard solution
        start = time.perf_counter()
        result_std = solution.minCost(grid, k)
        time_std = (time.perf_counter() - start) * 1000
        
        # Optimized solution
        start = time.perf_counter()
        result_opt = solution_opt.minCost(grid, k)
        time_opt = (time.perf_counter() - start) * 1000
        
        print(f"Grid size: {m}×{n}, k={k}")
        print(f"  Standard:  {time_std:>8.3f}ms (result={result_std})")
        print(f"  Optimized: {time_opt:>8.3f}ms (result={result_opt})")
        print(f"  Speedup:   {time_std/time_opt:>8.2f}x")
        print()
    
    print("=" * 80)