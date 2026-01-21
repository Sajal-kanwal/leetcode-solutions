---

### **PATTERNS.md (Quick Reference)**
````markdown
# 🧩 LeetCode Patterns — Quick Reference Guide

> **"Pattern recognition is the key to solving problems faster."**

This guide catalogs common algorithmic patterns I've identified while solving 250+ LeetCode problems.

---

## Table of Contents
1. [Sliding Window](#1️⃣-sliding-window)
2. [Two Pointers](#2️⃣-two-pointers)
3. [Fast & Slow Pointers](#3️⃣-fast--slow-pointers)
4. [Binary Search](#4️⃣-binary-search)
5. [Backtracking](#5️⃣-backtracking)
6. [Dynamic Programming](#6️⃣-dynamic-programming)
7. [Graph Traversal](#7️⃣-graph-traversal)
8. [Tree Patterns](#8️⃣-tree-patterns)

---

## 1️⃣ Sliding Window

### When to Use
- **Contiguous** subarray/substring problems
- Keywords: "maximum sum subarray", "longest substring", "minimum window"
- Usually involves maintaining a window that expands/contracts

### Pattern Recognition
✅ Input is linear (array/string)  
✅ Asked about contiguous sequence  
✅ Need to optimize over all windows  

### Template (Variable Size Window)
```python
def sliding_window(arr, target):
    left = 0
    window_sum = 0
    result = float('inf')  # or 0, depending on problem
    
    for right in range(len(arr)):
        # Expand window
        window_sum += arr[right]
        
        # Shrink window while condition is violated
        while window_sum >= target:  # Adjust condition
            result = min(result, right - left + 1)
            window_sum -= arr[left]
            left += 1
    
    return result if result != float('inf') else 0
```

### Template (Fixed Size Window)
```python
def sliding_window_fixed(arr, k):
    window_sum = sum(arr[:k])
    max_sum = window_sum
    
    for i in range(k, len(arr)):
        window_sum += arr[i] - arr[i - k]
        max_sum = max(max_sum, window_sum)
    
    return max_sum
```

### Classic Problems
- [x] Maximum Sum Subarray of Size K
- [x] Longest Substring Without Repeating Characters (LC 3)
- [x] Minimum Window Substring (LC 76) ⭐ Hard
- [x] Longest Repeating Character Replacement (LC 424)
- [x] Permutation in String (LC 567)

### Key Insights
💡 Use hash map to track character frequencies  
💡 Two pointers (left, right) define the window  
💡 Shrink from left when condition is violated  

---

## 2️⃣ Two Pointers

### When to Use
- **Sorted array** problems
- Finding pairs/triplets with specific sum
- Comparing elements from both ends

### Pattern Recognition
✅ Array is sorted (or can be sorted)  
✅ Need to find pair/triplet  
✅ Asked about "target sum"  

### Template
```python
def two_pointers(arr, target):
    left, right = 0, len(arr) - 1
    
    while left < right:
        current_sum = arr[left] + arr[right]
        
        if current_sum == target:
            return [left, right]
        elif current_sum < target:
            left += 1  # Need larger sum
        else:
            right -= 1  # Need smaller sum
    
    return []
```

### Classic Problems
- [x] Two Sum II - Input Array Is Sorted (LC 167)
- [x] 3Sum (LC 15) ⭐
- [x] Container With Most Water (LC 11)
- [x] Trapping Rain Water (LC 42) ⭐ Hard
- [x] Remove Duplicates from Sorted Array (LC 26)

### Key Insights
💡 Sort first if not already sorted  
💡 Move pointers based on comparison with target  
💡 Skip duplicates to avoid redundant work  

---

## 3️⃣ Fast & Slow Pointers

### When to Use
- **Linked list** cycle detection
- Finding middle element
- Detecting loops

### Pattern Recognition
✅ Linked list structure  
✅ Asked about cycle/loop  
✅ Need to find middle without extra space  

### Template (Cycle Detection)
```python
def has_cycle(head):
    slow = fast = head
    
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        
        if slow == fast:
            return True
    
    return False
```

### Template (Find Cycle Start)
```python
def detect_cycle(head):
    slow = fast = head
    
    # Detect cycle
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            break
    else:
        return None  # No cycle
    
    # Find start of cycle
    slow = head
    while slow != fast:
        slow = slow.next
        fast = fast.next
    
    return slow
```

### Classic Problems
- [x] Linked List Cycle (LC 141)
- [x] Linked List Cycle II (LC 142)
- [x] Middle of the Linked List (LC 876)
- [x] Happy Number (LC 202)
- [x] Palindrome Linked List (LC 234)

### Key Insights
💡 Fast moves 2x speed of slow  
💡 They meet inside cycle (if exists)  
💡 Distance from head to cycle start = distance from meeting point to cycle start  

---

## 4️⃣ Binary Search

### When to Use
- **Sorted array** search
- Search space can be divided in half
- Finding minimum/maximum in sorted/rotated array

### Pattern Recognition
✅ Array is sorted (or rotated sorted)  
✅ O(log n) time complexity expected  
✅ "Find minimum/maximum" in constrained space  

### Template (Standard)
```python
def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    
    while left <= right:
        mid = left + (right - left) // 2  # Avoid overflow
        
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return -1
```

### Template (Search Space Reduction)
```python
def binary_search_condition(arr):
    left, right = 0, len(arr)
    
    while left < right:
        mid = left + (right - left) // 2
        
        if condition(mid):
            right = mid  # Search left half
        else:
            left = mid + 1  # Search right half
    
    return left
```

### Classic Problems
- [x] Binary Search (LC 704)
- [x] Search in Rotated Sorted Array (LC 33) ⭐
- [x] Find Minimum in Rotated Sorted Array (LC 153)
- [x] Search a 2D Matrix (LC 74)
- [x] Median of Two Sorted Arrays (LC 4) ⭐ Hard

### Key Insights
💡 Use `left + (right - left) // 2` to avoid integer overflow  
💡 Decide if search space includes mid or excludes it  
💡 Template varies based on inclusive/exclusive bounds  

---

## 5️⃣ Backtracking

### When to Use
- Generate **all possibilities** (permutations, combinations, subsets)
- Constraint satisfaction (N-Queens, Sudoku)
- Explore all paths in decision tree

### Pattern Recognition
✅ "Find all", "generate all"  
✅ Need to explore multiple paths  
✅ Constraint satisfaction problems  

### Template
```python
def backtrack(path, choices, result):
    # Base case: valid solution found
    if is_valid_solution(path):
        result.append(path[:])  # Make a copy
        return
    
    # Explore all choices
    for choice in choices:
        # Make choice
        path.append(choice)
        
        # Recurse with updated state
        backtrack(path, get_remaining_choices(), result)
        
        # Undo choice (backtrack)
        path.pop()
```

### Classic Problems
- [x] Subsets (LC 78)
- [x] Permutations (LC 46)
- [x] Combination Sum (LC 39)
- [x] N-Queens (LC 51) ⭐ Hard
- [x] Sudoku Solver (LC 37) ⭐ Hard

### Key Insights
💡 Always undo the choice after exploring (backtrack)  
💡 Use `path[:]` or `path.copy()` when storing results  
💡 Prune invalid branches early for optimization  

---

## 6️⃣ Dynamic Programming

### When to Use
- **Overlapping subproblems** + **optimal substructure**
- Optimization problems (min/max)
- Counting problems

### Pattern Recognition
✅ "Minimum/maximum", "count ways"  
✅ Can break into smaller subproblems  
✅ Subproblems overlap  

### Template (1D DP)
```python
def dp_1d(n):
    # Step 1: Define DP array
    dp = [0] * (n + 1)
    
    # Step 2: Base case
    dp[0] = base_case_value
    
    # Step 3: Fill DP table using recurrence
    for i in range(1, n + 1):
        dp[i] = recurrence_relation(dp[i-1], dp[i-2], ...)
    
    # Step 4: Return answer
    return dp[n]
```

### Template (2D DP)
```python
def dp_2d(m, n):
    # Step 1: Create DP table
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    # Step 2: Initialize base cases
    for i in range(m + 1):
        dp[i][0] = base_case_i
    for j in range(n + 1):
        dp[0][j] = base_case_j
    
    # Step 3: Fill table
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            dp[i][j] = transition(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])
    
    # Step 4: Return result
    return dp[m][n]
```

### Classic Problems

**1D DP:**
- [x] Climbing Stairs (LC 70)
- [x] House Robber (LC 198)
- [x] Coin Change (LC 322) ⭐

**2D DP:**
- [x] Unique Paths (LC 62)
- [x] Longest Common Subsequence (LC 1143)
- [x] Edit Distance (LC 72) ⭐ Hard

**Advanced:**
- [x] Longest Increasing Subsequence (LC 300)
- [x] Word Break (LC 139)
- [x] Partition Equal Subset Sum (LC 416)

### DP Subcategories

1. **Fibonacci-style** (LC 70, 198)
2. **0/1 Knapsack** (LC 416, 494)
3. **Unbounded Knapsack** (LC 322, 518)
4. **LCS variants** (LC 1143, 72, 583)
5. **Palindrome DP** (LC 5, 647, 516)

### Key Insights
💡 Always define: state, base case, transition  
💡 Draw the DP table for small examples  
💡 Space can often be optimized (2D → 1D)  

---

## 7️⃣ Graph Traversal

### When to Use
- Problems involving **nodes and edges**
- Shortest path, connectivity, cycles

### Pattern Recognition
✅ Input is graph (explicit or implicit)  
✅ Need to explore all nodes  
✅ Asked about paths, connectivity, cycles  

### Template (DFS - Recursive)
```python
def dfs(node, visited):
    if node in visited:
        return
    
    visited.add(node)
    
    for neighbor in graph[node]:
        dfs(neighbor, visited)
```

### Template (BFS)
```python
from collections import deque

def bfs(start):
    queue = deque([start])
    visited = {start}
    
    while queue:
        node = queue.popleft()
        
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
```

### Template (Dijkstra's Shortest Path)
```python
import heapq

def dijkstra(graph, start):
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    
    pq = [(0, start)]  # (distance, node)
    
    while pq:
        current_dist, node = heapq.heappop(pq)
        
        if current_dist > distances[node]:
            continue
        
        for neighbor, weight in graph[node]:
            distance = current_dist + weight
            
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(pq, (distance, neighbor))
    
    return distances
```

### Classic Problems

**DFS:**
- [x] Number of Islands (LC 200)
- [x] Clone Graph (LC 133)

**BFS:**
- [x] Binary Tree Level Order Traversal (LC 102)
- [x] Word Ladder (LC 127) ⭐

**Dijkstra:**
- [x] Network Delay Time (LC 743)
- [x] Cheapest Flights Within K Stops (LC 787)

**Topological Sort:**
- [x] Course Schedule (LC 207) ⭐
- [x] Course Schedule II (LC 210)

**Union-Find:**
- [x] Number of Connected Components (LC 323)
- [x] Redundant Connection (LC 684)

### Key Insights
💡 BFS for shortest path in unweighted graphs  
💡 DFS for path existence, cycle detection  
💡 Dijkstra for shortest path in weighted graphs  
💡 Topological sort for dependency ordering  

---

## 8️⃣ Tree Patterns

### When to Use
- Binary tree/BST problems
- Hierarchical data structures

### Pattern Recognition
✅ Input is tree structure  
✅ Recursion is natural fit  
✅ Asked about paths, depth, traversal  

### Template (DFS - Inorder)
```python
def inorder(root, result):
    if not root:
        return
    
    inorder(root.left, result)
    result.append(root.val)
    inorder(root.right, result)
```

### Template (BFS - Level Order)
```python
from collections import deque

def level_order(root):
    if not root:
        return []
    
    result = []
    queue = deque([root])
    
    while queue:
        level_size = len(queue)
        current_level = []
        
        for _ in range(level_size):
            node = queue.popleft()
            current_level.append(node.val)
            
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        
        result.append(current_level)
    
    return result
```

### Classic Problems

**DFS:**
- [x] Maximum Depth of Binary Tree (LC 104)
- [x] Invert Binary Tree (LC 226)
- [x] Diameter of Binary Tree (LC 543)

**BFS:**
- [x] Binary Tree Level Order Traversal (LC 102)
- [x] Binary Tree Right Side View (LC 199)

**BST:**
- [x] Validate Binary Search Tree (LC 98) ⭐
- [x] Lowest Common Ancestor of BST (LC 235)

**Advanced:**
- [x] Serialize and Deserialize Binary Tree (LC 297) ⭐ Hard
- [x] Binary Tree Maximum Path Sum (LC 124) ⭐ Hard

### Key Insights
💡 Most tree problems have elegant recursive solutions  
💡 BFS for level-based problems  
💡 For BST: inorder traversal gives sorted order  

---

## 🎯 Pattern Selection Flowchart
````
Problem Type?
├─ Array/String
│  ├─ Contiguous? → Sliding Window
│  ├─ Sorted? → Two Pointers
│  └─ Search? → Binary Search
│
├─ Linked List → Fast & Slow Pointers
│
├─ Tree
│  ├─ Level-based? → BFS
│  └─ Path/Depth? → DFS
│
├─ Graph → DFS/BFS/Dijkstra
│
├─ Optimization (min/max)
│  ├─ Overlapping subproblems? → DP
│  └─ Constraints? → Greedy
│
└─ Generate all → Backtracking