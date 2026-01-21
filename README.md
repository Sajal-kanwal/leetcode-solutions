# 🚀 LeetCode Solutions — A Structured Approach

> **"The only way to do great work is to love what you do."** — Steve Jobs

[![LeetCode](https://img.shields.io/badge/LeetCode-250+-FFA116?style=for-the-badge&logo=leetcode&logoColor=black)](https://leetcode.com/sajal-kanwal)
[![Python](https://img.shields.io/badge/Python-100%25-3776AB?style=for-the-badge&logo=python&logoColor=white)](#)
[![Last Commit](https://img.shields.io/github/last-commit/Sajal-kanwal/leetcode-solutions?style=for-the-badge)](https://github.com/Sajal-kanwal/leetcode-solutions)

---

## 📊 Quick Stats

| Metric                    | Count      | Progress                                                    |
| ------------------------- | ---------- | ----------------------------------------------------------- |
| **Total Problems Solved** | 250+       | ![](https://progress-bar.xyz/65?title=Target:400&width=200) |
| **Easy**                  | 120        | 48%                                                         |
| **Medium**                | 95         | 38%                                                         |
| **Hard**                  | 35         | 14%                                                         |
| **Topics Covered**        | 12         | Arrays, Strings, DP, Graphs, Trees...                       |
| **Current Streak**        | 47 days 🔥 | Longest: 62 days                                            |

📈 [View Detailed Progress →](./PROGRESS.md)

---

## 🎯 Repository Purpose

This repository documents my journey in mastering **Data Structures & Algorithms** through deliberate practice on LeetCode.

### What makes this different?

Each solution includes:

✅ **Clear problem statement & constraints**  
✅ **Detailed approach explanation** (the "why" behind the code)  
✅ **Time & Space complexity analysis**  
✅ **Comprehensive test cases** including edge cases  
✅ **Pattern recognition notes** for similar problems

This isn't just code — it's a **learning journal** that demonstrates:

- Problem-solving methodology
- Communication skills
- Understanding of algorithmic tradeoffs
- Consistent practice habits

---

## 📂 Repository Structure

```
leetcode-solutions/
├── arrays/              # 45 problems (Two Pointers, Sliding Window, Kadane's)
├── strings/             # 32 problems (KMP, Palindromes, Sliding Window)
├── linked_lists/        # 18 problems (Fast/Slow Pointers, Reversal)
├── trees/               # 38 problems (DFS, BFS, Morris Traversal)
├── graphs/              # 28 problems (Dijkstra, Union-Find, Topological Sort)
├── dynamic_programming/ # 42 problems (Knapsack, LIS, Matrix Chain)
├── backtracking/        # 15 problems (N-Queens, Sudoku, Subsets)
├── heaps/               # 12 problems (Top K, Merge K Lists)
├── binary_search/       # 20 problems (Search Space, Rotated Arrays)
├── bit_manipulation/    # 10 problems (XOR Tricks, Subsets)
├── math/                # 20 problems (GCD, Primes, Combinatorics)
├── sliding_window/      # 16 problems (Fixed/Variable Size Windows)
├── resources/           # Templates, patterns, study notes
└── scripts/             # Automation tools
```

---

## 🗂️ Topics & Key Problems

<details>
<summary><b>📌 Arrays (45 problems)</b></summary>

**Key Patterns:**

- Two Pointers
- Sliding Window
- Prefix Sum
- Kadane's Algorithm

**Must-Know Problems:**

- ⭐ [Two Sum](./arrays/easy/two_sum.py) — Hash Table pattern
- ⭐ [3Sum](./arrays/medium/three_sum.py) — Two Pointers after sorting
- ⭐ [Container With Most Water](./arrays/medium/container_with_most_water.py) — Greedy approach
- ⭐ [Trapping Rain Water](./arrays/hard/trapping_rain_water.py) — Two Pointers advanced
- ⭐ [Maximum Subarray](./arrays/easy/maximum_subarray.py) — Kadane's Algorithm

[View all Array problems →](./arrays)

</details>

<details>
<summary><b>🌲 Trees (38 problems)</b></summary>

**Key Patterns:**

- DFS (Preorder, Inorder, Postorder)
- BFS (Level-order traversal)
- Binary Search Tree properties
- Lowest Common Ancestor

**Must-Know Problems:**

- ⭐ [Invert Binary Tree](./trees/easy/invert_binary_tree.py) — DFS basics
- ⭐ [Binary Tree Level Order Traversal](./trees/medium/level_order_traversal.py) — BFS pattern
- ⭐ [Validate BST](./trees/medium/validate_bst.py) — BST properties
- ⭐ [Serialize and Deserialize Binary Tree](./trees/hard/serialize_deserialize.py) — DFS/BFS
- ⭐ [Lowest Common Ancestor](./trees/medium/lca_binary_tree.py) — Recursive thinking

[View all Tree problems →](./trees)

</details>

<details>
<summary><b>💎 Dynamic Programming (42 problems)</b></summary>

**Key Patterns:**

- 1D DP (Fibonacci-style)
- 2D DP (Grid, LCS)
- Knapsack variants
- DP on strings

**Must-Know Problems:**

- ⭐ [Climbing Stairs](./dynamic_programming/easy/climbing_stairs.py) — 1D DP intro
- ⭐ [Coin Change](./dynamic_programming/medium/coin_change.py) — Unbounded Knapsack
- ⭐ [Longest Increasing Subsequence](./dynamic_programming/medium/lis.py) — Classic DP
- ⭐ [Edit Distance](./dynamic_programming/hard/edit_distance.py) — 2D DP
- ⭐ [Word Break](./dynamic_programming/medium/word_break.py) — DP on strings

[View all DP problems →](./dynamic_programming)

</details>

<details>
<summary><b>🕸️ Graphs (28 problems)</b></summary>

**Key Patterns:**

- DFS/BFS traversal
- Dijkstra's algorithm
- Union-Find (Disjoint Set)
- Topological Sort

**Must-Know Problems:**

- ⭐ [Number of Islands](./graphs/medium/number_of_islands.py) — DFS/BFS basics
- ⭐ [Course Schedule](./graphs/medium/course_schedule.py) — Topological Sort (cycle detection)
- ⭐ [Network Delay Time](./graphs/medium/network_delay_time.py) — Dijkstra's
- ⭐ [Word Ladder](./graphs/hard/word_ladder.py) — BFS shortest path
- ⭐ [Alien Dictionary](./graphs/hard/alien_dictionary.py) — Topological Sort advanced

[View all Graph problems →](./graphs)

</details>

<details>
<summary><b>🔗 Linked Lists (18 problems)</b></summary>

**Key Patterns:**

- Fast & Slow Pointers (Floyd's Cycle)
- Reversal techniques
- Dummy node usage

**Must-Know Problems:**

- ⭐ [Reverse Linked List](./linked_lists/easy/reverse_linked_list.py) — Fundamental technique
- ⭐ [Linked List Cycle](./linked_lists/easy/linked_list_cycle.py) — Fast/Slow pointers
- ⭐ [Merge Two Sorted Lists](./linked_lists/easy/merge_two_lists.py) — Two pointers
- ⭐ [Reorder List](./linked_lists/medium/reorder_list.py) — Multiple techniques combined
- ⭐ [Merge K Sorted Lists](./linked_lists/hard/merge_k_lists.py) — Heap approach

[View all Linked List problems →](./linked_lists)

</details>

---

## 🔥 Highlighted Solutions

### **Hard Problems I'm Proud Of**

These showcase deep understanding and optimal implementation:

| Problem                                                                     | Key Insight                          | Complexity       |
| --------------------------------------------------------------------------- | ------------------------------------ | ---------------- |
| [Median of Two Sorted Arrays](./arrays/hard/median_two_sorted_arrays.py)    | Binary search on smaller array       | O(log(min(m,n))) |
| [Serialize Binary Tree](./trees/hard/serialize_deserialize.py)              | Level-order with null markers        | O(n)             |
| [Word Ladder II](./graphs/hard/word_ladder_ii.py)                           | BFS + Backtracking hybrid            | O(N × 26^L)      |
| [Trapping Rain Water](./arrays/hard/trapping_rain_water.py)                 | Two-pointer optimization             | O(n), O(1) space |
| [Regular Expression Matching](./dynamic_programming/hard/regex_matching.py) | 2D DP with careful state transitions | O(m×n)           |

### **Pattern Showcase**

Problems that demonstrate mastery of specific patterns:

- **Sliding Window:** [Minimum Window Substring](./sliding_window/hard/minimum_window_substring.py)
- **Binary Search:** [Search in Rotated Sorted Array](./binary_search/medium/search_rotated_array.py)
- **Backtracking:** [N-Queens](./backtracking/hard/n_queens.py)
- **Union-Find:** [Number of Connected Components](./graphs/medium/connected_components.py)

---

## 🛠️ Languages & Tools

- **Language:** Python 3.11+
- **Style:** Clean, readable, well-commented code
- **Testing:** Built-in assertions for all solutions
- **Type Hints:** Used throughout for clarity

---

## 📚 Learning Resources

### Books

- _Cracking the Coding Interview_ by Gayle Laakmann McDowell
- _Elements of Programming Interviews in Python_

### Online Courses

- **NeetCode** — Structured problem-solving roadmap
- **Striver's A2Z DSA** — Comprehensive coverage

### Quick References

- [LeetCode Patterns Guide](./PATTERNS.md) — My curated list
- [Time Complexity Cheat Sheet](./resources/notes/time_complexity_cheatsheet.md)
- [Common Templates](./resources/templates/) — Reusable code patterns

---

## 🎓 My Approach

### Problem-Solving Framework

```
1. UNDERSTAND
   ├─ Read problem 2-3 times
   ├─ Identify constraints
   └─ Ask clarifying questions

2. PLAN
   ├─ Brainstorm approaches
   ├─ Analyze time/space complexity
   └─ Choose optimal approach

3. IMPLEMENT
   ├─ Write clean code
   ├─ Add comments for tricky parts
   └─ Handle edge cases

4. TEST
   ├─ Run provided examples
   ├─ Test edge cases
   └─ Dry run with small input

5. OPTIMIZE
   ├─ Review for improvements
   └─ Document learnings
```

### Quality Over Quantity

> I believe in **deliberate practice**. Each solution here is:
>
> 1. **Well-tested** — handles edge cases explicitly
> 2. **Well-documented** — explains the thought process
> 3. **Optimized** — considers time/space tradeoffs
> 4. **Reviewed** — revisited after initial solve

---

## 📈 Progress Tracking

### Weekly Goals

- Solve 10-15 problems per week
- Focus on 1-2 topics in depth
- Review and optimize previous solutions
- Document patterns and learnings

### Monthly Milestones

- ✅ January 2026: 42 problems (Graphs, DP focus)
- ✅ December 2025: 38 problems (Trees, Backtracking)
- 🎯 February 2026: Target 45 problems (Advanced DP, Hard problems)

[View detailed progress →](./PROGRESS.md)

---

## 🌟 How This Helps My Journey

As a **Computer Science student** seeking internships, this repository:

1. **Demonstrates consistency** — Regular commits show discipline
2. **Proves technical depth** — Not just solving, but understanding
3. **Shows communication skills** — Clear explanations matter in interviews
4. **Complements my projects** — Algorithms used in [Spendora](https://github.com/Sajal-kanwal/Spendora) came from here

### Real-world applications:

- **Graph algorithms** → Used in NetSight for network topology visualization
- **Dynamic programming** → Optimized resource allocation in ML projects
- **Tree traversals** → File system navigation in projects

---

## 📬 Connect With Me

- **LeetCode:** [@your_username](https://leetcode.com/sajal-kanwal)
- **LinkedIn:** [Your Name](https://linkedin.com/in/sajal-kanwal)
- **Portfolio:** [yourwebsite.com](https://sajal-kanwal.vercel.app)
- **Email:** sajal.kanwal02@gmail.com

---

## 📝 Notes

- Problem statements belong to LeetCode — this repository contains only my solutions and learning notes
- Solutions are written for clarity and learning, not just to pass test cases
- All code is original work based on my understanding of the problems

---

## ⭐ Star This Repo

If you find this helpful for your own LeetCode journey, consider giving it a star! It motivates me to keep learning and sharing.

---

<p align="center">
  <i>Last Updated: January 2026</i>
</p>
