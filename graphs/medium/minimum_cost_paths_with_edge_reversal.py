"""
================================================================================
Problem: 3650. Minimum Cost Path with Edge Reversals
Platform: LeetCode
URL: https://leetcode.com/problems/minimum-cost-path-with-edge-reversals/
Difficulty: Medium
Topics: Graph, Shortest Path, Dijkstra's Algorithm, Greedy
================================================================================

PROBLEM DESCRIPTION:
You are given a directed, weighted graph with n nodes labeled from 0 to n-1,
and an array edges where edges[i] = [ui, vi, wi] represents a directed edge
from node ui to node vi with cost wi.

Each node ui has a switch that can be used at most once: when you arrive at ui
and have not yet used its switch, you may activate it on one of its incoming
edges vi → ui, reverse that edge to ui → vi and immediately traverse it.

The reversal is only valid for that single move, and using a reversed edge
costs 2 * wi.

Return the minimum total cost to travel from node 0 to node n-1. If it is not
possible, return -1.

CONSTRAINTS:
- 2 <= n <= 5 * 10^4
- 1 <= edges.length <= 10^5
- edges[i] = [ui, vi, wi]
- 0 <= ui, vi <= n - 1
- 1 <= wi <= 1000

EXAMPLES:

Example 1:
Input: n = 4, edges = [[0,1,3],[3,1,1],[2,3,4],[0,2,2]]
Output: 5
Explanation:
- Use the path 0 → 1 (cost 3)
- At node 1, reverse the original edge 3 → 1 into 1 → 3 and traverse at cost 2*1=2
- Total cost: 3 + 2 = 5

Example 2:
Input: n = 4, edges = [[0,2,1],[2,1,1],[1,3,1],[2,3,3]]
Output: 3
Explanation:
- No reversal needed. Path: 0 → 2 (cost 1) → 1 (cost 1) → 3 (cost 1)
- Total cost: 1 + 1 + 1 = 3

================================================================================
INTUITION:
This is a shortest path problem with a twist: we can reverse edges for 2x cost.

KEY INSIGHT:
We can model edge reversal as adding "reverse edges" to our graph upfront:
- Original edge u → v with cost w stays as is
- Add reverse edge v → u with cost 2w (representing the reversal)

This transforms the problem into a standard shortest path problem on a modified
graph, which we can solve with Dijkstra's algorithm.

WHY THIS WORKS:
- The problem says we can reverse "at most once per node"
- But since we're finding the shortest path, we'll naturally only use each
  edge reversal if it's beneficial
- Dijkstra's greedy nature ensures we take the optimal path

APPROACH:
1. Build a bidirectional graph:
   - For each edge u → v with cost w:
     - Add forward edge: u → v with cost w
     - Add reverse edge: v → u with cost 2w
2. Run Dijkstra's algorithm from node 0 to find shortest path to node n-1
3. Return the shortest distance, or -1 if unreachable

COMPLEXITY ANALYSIS:
- Time: O((E + V) log V) where E = edges, V = nodes
  - Building graph: O(E)
  - Dijkstra with min heap: O((E + V) log V)
- Space: O(E + V)
  - Adjacency list: O(E)
  - Distance array: O(V)
  - Priority queue: O(V) in worst case

EDGE CASES HANDLED:
- No path exists: return -1
- Empty graph (n=0): return 0
- No edges but n>1: return -1
- Direct path is optimal: no reversals used
- Multiple paths: Dijkstra finds the optimal one

================================================================================
"""

from typing import List, Dict, Tuple
from collections import defaultdict
from heapq import heappush, heappop


class Solution:
    """LC 3650: Minimum Cost Path with Edge Reversals"""
    
    def minCost(self, n: int, edges: List[List[int]]) -> int:
        """
        Find minimum cost path from 0 to n-1 with optional edge reversals.
        
        Args:
            n: Number of nodes (0 to n-1)
            edges: List of [u, v, w] representing directed edge u→v with cost w
            
        Returns:
            Minimum cost to reach node n-1 from node 0, or -1 if impossible
            
        Algorithm: Dijkstra's Shortest Path with Modified Graph
        Time: O((E + V) log V)
        Space: O(E + V)
        """
        # Edge cases
        if n == 0:
            return 0
        if not edges and n > 1:
            return -1
        
        # Build bidirectional adjacency list
        # For each edge u → v with cost w:
        #   - Add forward edge: u → v, cost w
        #   - Add reverse edge: v → u, cost 2w (represents reversal)
        adj = defaultdict(list)
        for u, v, w in edges:
            adj[u].append((v, w))      # Original edge
            adj[v].append((u, 2 * w))  # Reversed edge (costs 2x)
        
        # Dijkstra's algorithm initialization
        # Priority queue: (distance, node)
        pq = [(0, 0)]  # Start at node 0 with cost 0
        
        # Track minimum distance to each node
        min_cost = {i: float('inf') for i in range(n)}
        min_cost[0] = 0
        
        # Dijkstra's main loop
        while pq:
            current_dist, u = heappop(pq)
            
            # Early exit: reached destination
            if u == n - 1:
                return current_dist
            
            # Skip if we've found a better path to u already
            # This happens when a node is added to pq multiple times
            if current_dist > min_cost[u]:
                continue
            
            # Explore all neighbors of u
            for v, weight in adj[u]:
                new_dist = current_dist + weight
                
                # If found a shorter path to v, update and add to queue
                if new_dist < min_cost[v]:
                    min_cost[v] = new_dist
                    heappush(pq, (new_dist, v))
        
        # Return result
        return min_cost[n - 1] if min_cost[n - 1] != float('inf') else -1


class SolutionWithComments:
    """
    Heavily commented version for learning purposes
    """
    
    def minCost(self, n: int, edges: List[List[int]]) -> int:
        """
        Enhanced version with detailed inline comments
        """
        INF = float('inf')
        
        # === EDGE CASE HANDLING ===
        if n == 0:
            return 0  # No nodes, no cost
        
        if not edges and n > 1:
            return -1  # Can't reach n-1 with no edges
        
        # === GRAPH CONSTRUCTION ===
        # Build adjacency list representation
        # Key insight: Model reversals as bidirectional edges
        adj = defaultdict(list)
        
        for u, v, w in edges:
            # Original edge: u can go to v at cost w
            adj[u].append((v, w))
            
            # Reverse edge: v can go to u at cost 2w
            # This represents using the switch at v to reverse edge v←u
            adj[v].append((u, 2 * w))
        
        # === DIJKSTRA'S ALGORITHM ===
        # Priority queue stores (distance, node)
        # Python's heapq is a min-heap, so smallest distance comes first
        pq = [(0, 0)]  # Start: distance 0 to node 0
        
        # Track the minimum known distance to each node
        # Initialize all nodes to infinity except starting node
        min_cost = {i: INF for i in range(n)}
        min_cost[0] = 0
        
        # Main Dijkstra loop
        while pq:
            # Get node with smallest distance
            dist, node = heappop(pq)
            
            # Optimization: Early exit when we reach destination
            # Since we process nodes in order of increasing distance,
            # the first time we reach n-1 is guaranteed to be optimal
            if node == n - 1:
                return dist
            
            # Skip outdated entries
            # This happens when we find multiple paths to the same node
            # and add it to the queue multiple times
            if dist > min_cost[node]:
                continue
            
            # Explore all outgoing edges from current node
            for neighbor, edge_cost in adj[node]:
                new_distance = dist + edge_cost
                
                # If we found a shorter path to neighbor
                if new_distance < min_cost[neighbor]:
                    # Update the shortest distance
                    min_cost[neighbor] = new_distance
                    
                    # Add to priority queue for future exploration
                    heappush(pq, (new_distance, neighbor))
        
        # If we exit the loop without reaching n-1, check final distance
        return min_cost[n - 1] if min_cost[n - 1] != INF else -1


# ================================================================================
# TEST CASES
# ================================================================================
if __name__ == "__main__":
    solution = Solution()
    
    test_cases = [
        # (n, edges, expected, description)
        (
            4,
            [[0, 1, 3], [3, 1, 1], [2, 3, 4], [0, 2, 2]],
            5,
            "Example 1: Use reversal 3→1 becomes 1→3"
        ),
        (
            4,
            [[0, 2, 1], [2, 1, 1], [1, 3, 1], [2, 3, 3]],
            3,
            "Example 2: No reversal needed, direct path optimal"
        ),
        (
            2,
            [[0, 1, 5]],
            5,
            "Simple case: Direct edge"
        ),
        (
            2,
            [[1, 0, 5]],
            10,
            "Reverse edge needed: cost doubles"
        ),
        (
            3,
            [[0, 1, 2], [1, 2, 3]],
            5,
            "Chain of edges"
        ),
        (
            3,
            [[2, 1, 2], [1, 0, 3]],
            10,
            "All edges reversed: 2→1 (cost 4) + 1→0 (cost 6)"
        ),
        (
            4,
            [[0, 1, 1], [1, 2, 1], [2, 3, 1]],
            3,
            "Long path, no reversals"
        ),
        (
            3,
            [[0, 1, 5], [1, 2, 10]],
            15,
            "High cost edges"
        ),
        (
            4,
            [[0, 1, 1], [0, 2, 10], [1, 3, 1], [2, 3, 1]],
            2,
            "Multiple paths: choose optimal"
        ),
        (
            3,
            [[0, 1, 5]],
            -1,
            "Disconnected graph: no path to n-1"
        ),
    ]
    
    print("=" * 80)
    print("TESTING MINIMUM COST PATH WITH EDGE REVERSALS")
    print("=" * 80)
    print()
    
    passed = 0
    for i, (n, edges, expected, description) in enumerate(test_cases, 1):
        result = solution.minCost(n, edges)
        
        if result == expected:
            print(f"✅ Test {i}: {description}")
            print(f"   n={n}, edges={edges}")
            print(f"   Result: {result}")
            passed += 1
        else:
            print(f"❌ Test {i}: {description}")
            print(f"   n={n}, edges={edges}")
            print(f"   Expected: {expected}")
            print(f"   Got: {result}")
        print()
    
    print("=" * 80)
    print(f"RESULTS: {passed}/{len(test_cases)} tests passed")
    print("=" * 80)


# ================================================================================
# VISUALIZATION: Example 1
# ================================================================================
"""
Example 1: n = 4, edges = [[0,1,3],[3,1,1],[2,3,4],[0,2,2]]

Original Graph (directed):
    0 ──3──> 1 <──1── 3
    |                 ↑
    2                 |
    └──────> 2 ───4───┘

After adding reverse edges (bidirectional with 2x cost):
    0 ←─6─→ 1 ←─2─→ 3
    ↓       ↑       ↑
    2       |       |
    └───4───┘       |
    ←───8───────────┘

Dijkstra's Execution:

Initial: pq = [(0, 0)], min_cost = {0:0, 1:∞, 2:∞, 3:∞}

Step 1: Process node 0 (dist=0)
  - Explore 0→1 (cost 3): min_cost[1] = 3, pq = [(3,1), (4,2)]
  - Explore 0→2 (cost 2): min_cost[2] = 2, already added

Step 2: Process node 2 (dist=2)
  - Explore 2→3 (cost 4): min_cost[3] = 6, pq = [(3,1), (6,3), ...]
  - Other neighbors...

Step 3: Process node 1 (dist=3)
  - Explore 1→3 (reversed edge, cost 2): min_cost[3] = min(6, 3+2) = 5 ✓
  - Update pq = [(5,3), ...]

Step 4: Process node 3 (dist=5)
  - Reached destination! Return 5

Optimal Path: 0 → 1 → 3 (with reversal)
Cost: 3 + 2 = 5
"""


# ================================================================================
# LEARNING NOTES
# ================================================================================
"""
PATTERN: Graph Modification + Dijkstra's Algorithm

This problem teaches a powerful technique: transforming a complex problem into
a standard shortest path problem by modifying the graph structure.

KEY INSIGHTS:

1. Edge Reversal as Bidirectional Edges
   - Instead of handling reversals during pathfinding
   - Pre-compute all possible moves (including reversals) in the graph
   - Reversal costs 2x → add reverse edge with weight 2w

2. Why Dijkstra Works Here
   - All edge weights are positive (w ≥ 1, 2w ≥ 2)
   - We need single-source shortest path
   - Greedy approach finds optimal solution

3. "At Most Once Per Node" Constraint
   - Problem states each node's switch can be used once
   - But in optimal path, we never visit same node twice
   - So this constraint is automatically satisfied

SIMILAR PROBLEMS:

1. LC 743: Network Delay Time
   - Standard Dijkstra application
   - No modifications needed

2. LC 787: Cheapest Flights Within K Stops
   - Dijkstra with additional constraint (limited stops)
   - Similar graph + shortest path structure

3. LC 1514: Path with Maximum Probability
   - Modified Dijkstra (maximize instead of minimize)
   - Shows pattern flexibility

4. LC 2065: Maximum Path Quality of a Graph
   - Similar graph modification concept
   - Different objective function

DIJKSTRA'S ALGORITHM TEMPLATE:
```python
def dijkstra(graph, start, end):
    pq = [(0, start)]  # (distance, node)
    dist = {node: float('inf') for node in graph}
    dist[start] = 0
    
    while pq:
        d, u = heappop(pq)
        
        if u == end:
            return d  # Early exit optimization
        
        if d > dist[u]:
            continue  # Skip outdated entries
        
        for v, weight in graph[u]:
            new_dist = d + weight
            if new_dist < dist[v]:
                dist[v] = new_dist
                heappush(pq, (new_dist, v))
    
    return dist[end] if dist[end] != float('inf') else -1
```

OPTIMIZATION TECHNIQUES:

1. Early Exit
   - Return immediately when reaching destination
   - Valid because Dijkstra processes nodes in increasing distance order

2. Skip Outdated Entries
   - Check `if d > dist[u]: continue`
   - Handles duplicate entries in priority queue

3. Sparse Graph Optimization
   - Use adjacency list instead of matrix
   - Better for real-world graphs (usually sparse)

COMMON MISTAKES:

❌ Forgetting to add reverse edges
   - Must add both u→v and v→u for each original edge

❌ Wrong reverse cost
   - Reverse edge costs 2w, not w

❌ Using BFS instead of Dijkstra
   - BFS only works for unweighted graphs
   - Here we have weighted edges

❌ Not handling unreachable nodes
   - Must return -1 if no path exists

❌ Forgetting early exit optimization
   - Can return as soon as we pop destination from queue

INTERVIEW TIPS:

1. Recognize the Pattern
   - "Shortest path" + "weighted graph" → Think Dijkstra
   - "Edge modification" → Consider graph transformation

2. Explain the Transformation
   - "We can model edge reversals as adding reverse edges upfront"
   - Draw the transformed graph

3. Discuss Complexity
   - "Dijkstra with binary heap is O((E+V) log V)"
   - "For dense graphs, this is O(V² log V)"
   - "For sparse graphs, closer to O(E log V)"

4. Alternative Approaches
   - "Could use Bellman-Ford if edges were negative (they're not here)"
   - "Could use BFS if all edges cost 1 (they don't here)"
   - "Dijkstra is optimal for this problem"

REAL-WORLD APPLICATIONS:

- Network routing with failover paths
- Transportation networks with reversible lanes
- Supply chain optimization with route flexibility
- Game pathfinding with teleportation/special moves

COMPLEXITY COMPARISON:

Dijkstra (Binary Heap):     O((E+V) log V)  ← This solution
Dijkstra (Fibonacci Heap):  O(E + V log V)  (Better but complex)
Bellman-Ford:               O(VE)           (Handles negative edges)
BFS:                        O(V+E)          (Only for unweighted)

For this problem: Binary heap Dijkstra is the sweet spot.
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
    
    test_sizes = [
        (100, 500),    # (nodes, edges)
        (1000, 5000),
        (5000, 25000),
    ]
    
    for n, e_count in test_sizes:
        # Generate random graph
        edges = []
        for _ in range(e_count):
            u = random.randint(0, n - 2)
            v = random.randint(u + 1, n - 1)
            w = random.randint(1, 100)
            edges.append([u, v, w])
        
        # Benchmark
        start = time.perf_counter()
        result = solution.minCost(n, edges)
        elapsed = (time.perf_counter() - start) * 1000
        
        print(f"n={n:>5}, edges={e_count:>6}: {elapsed:>8.3f}ms (cost={result})")
    
    print("\n" + "=" * 80)