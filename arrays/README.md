# Arrays — Problems & Patterns

> **Total Problems: 45** | Easy: 20 | Medium: 18 | Hard: 7

---

## 📌 Key Patterns

| Pattern | Count | Difficulty | Key Problems |
|---------|-------|------------|--------------|
| **Two Pointers** | 15 | Easy-Hard | Two Sum II, 3Sum, Trapping Rain Water |
| **Sliding Window** | 12 | Easy-Medium | Maximum Subarray, Best Time to Buy/Sell |
| **Prefix Sum** | 8 | Easy-Medium | Subarray Sum Equals K, Range Sum Query |
| **Kadane's Algorithm** | 5 | Easy-Medium | Maximum Subarray, Maximum Product Subarray |
| **Dutch National Flag** | 3 | Medium | Sort Colors, Sort Array By Parity |
| **Greedy** | 2 | Medium-Hard | Jump Game, Container With Most Water |

---

## 🟢 Easy Problems (20)

### Must-Know
- [x] [Two Sum](./easy/two_sum.py) — Hash table pattern ⭐
- [x] [Best Time to Buy and Sell Stock](./easy/best_time_to_buy_sell_stock.py) — One pass ⭐
- [x] [Contains Duplicate](./easy/contains_duplicate.py) — Hash set
- [x] [Maximum Subarray](./easy/maximum_subarray.py) — Kadane's algorithm ⭐
- [x] [Majority Element](./easy/majority_element.py) — Boyer-Moore voting

### Practice
- [x] [Remove Duplicates from Sorted Array](./easy/remove_duplicates.py)
- [x] [Plus One](./easy/plus_one.py)
- [x] [Merge Sorted Array](./easy/merge_sorted_array.py)
- [x] [Pascal's Triangle](./easy/pascals_triangle.py)

[View all 20 easy problems →](./easy/)

---

## 🟡 Medium Problems (18)

### Must-Know
- [x] [3Sum](./medium/three_sum.py) — Two pointers after sorting ⭐
- [x] [Container With Most Water](./medium/container_with_most_water.py) — Greedy ⭐
- [x] [Product of Array Except Self](./medium/product_except_self.py) — Prefix/suffix ⭐
- [x] [Maximum Product Subarray](./medium/maximum_product_subarray.py) — DP variation
- [x] [Find Peak Element](./medium/find_peak_element.py) — Binary search

### Practice
- [x] [Rotate Array](./medium/rotate_array.py)
- [x] [Jump Game](./medium/jump_game.py)
- [x] [Subarray Sum Equals K](./medium/subarray_sum_k.py)
- [x] [Sort Colors](./medium/sort_colors.py) — Dutch flag

[View all 18 medium problems →](./medium/)

---

## 🔴 Hard Problems (7)

### Must-Know
- [x] [Trapping Rain Water](./hard/trapping_rain_water.py) — Two pointers ⭐⭐
- [x] [Median of Two Sorted Arrays](./hard/median_two_sorted_arrays.py) — Binary search ⭐⭐
- [x] [First Missing Positive](./hard/first_missing_positive.py) — In-place marking ⭐

### Practice
- [x] [Best Time to Buy and Sell Stock III](./hard/best_time_buy_sell_iii.py)
- [x] [Sliding Window Maximum](./hard/sliding_window_maximum.py) — Deque
- [x] [Longest Consecutive Sequence](./hard/longest_consecutive.py) — Hash set O(n)

[View all 7 hard problems →](./hard/)

---

## 🎓 Study Notes



### Two Pointers Pattern

```python

# Use when array is sorted or can be sorted

left, right = 0, len(arr) - 1

while left < right:

    if condition:

        # Process and move pointers

        left += 1

    else:

        right -= 1

```



### Sliding Window Pattern

```python

# For contiguous subarray problems

left = 0

for right in range(len(arr)):

    # Expand window

    while condition_violated:

        # Shrink window

        left += 1

```



### Kadane's Algorithm

```python

# Maximum subarray sum

max_ending_here = max_so_far = arr[0]

for num in arr[1:]:

    max_ending_here = max(num, max_ending_here + num)

    max_so_far = max(max_so_far, max_ending_here)

```



---



## 📊 Progress

````

Easy:   ████████████████████ 20/20 (100%)

Medium: ██████████████████░░ 18/25 (72%)

Hard:   ███████░░░░░░░░░░░░░  7/15 (47%)
