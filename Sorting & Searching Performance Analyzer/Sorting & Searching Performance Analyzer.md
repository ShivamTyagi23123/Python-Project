# ⚡ Sorting & Searching Performance Analyzer

> A desktop GUI application built with **Python** and **Tkinter** that lets you compare the performance of **3 sorting algorithms** and **2 searching algorithms** side-by-side — with a sleek dark-themed interface, bar charts, and performance metrics.

---

## 📌 Quick Overview

| Detail | Info |
|---|---|
| **Language** | Python 3 |
| **GUI Library** | Tkinter (built into Python — no install needed) |
| **Other Modules** | `time` (for measuring speed), `random` (for generating test data) |
| **Sorting Algorithms** | Bubble Sort, Selection Sort, Insertion Sort |
| **Searching Algorithms** | Linear Search, Binary Search |
| **What it Measures** | Comparisons, Swaps, Execution Time (in microseconds) |

---

## 🚀 How to Run

```bash
python 16aprproject.py
```

A window will open. Here's what to do:

1. **Enter numbers** in the first text box, separated by spaces (e.g. `64 34 25 12 22`).
2. **Enter a search target** in the second text box (e.g. `25`).
3. Click **▶ ANALYZE** to run all 5 algorithms and see the results.
4. Click **🎲 Random Data** to auto-generate a random list and target.
5. Click **✕ Clear** to reset everything.

> **Tip:** You need at least 2 numbers for a meaningful comparison.

---

## 🗂️ Program Structure (File Map)

```
16aprproject.py  (514 lines, single file)
│
├── IMPORTS ─────────────────────── tkinter, time, random
│
├── COLOR PALETTE (lines 10–25) ── Dark theme colors (constants)
│
├── SORTING ALGORITHMS (lines 32–89)
│   ├── bubble_sort(arr)         → returns (sorted_list, comparisons, swaps, time)
│   ├── selection_sort(arr)      → returns (sorted_list, comparisons, swaps, time)
│   └── insertion_sort(arr)      → returns (sorted_list, comparisons, swaps, time)
│
├── SEARCHING ALGORITHMS (lines 96–118)
│   ├── linear_search(arr, target) → returns (found, index, comparisons)
│   └── binary_search(arr, target) → returns (found, index, comparisons)
│
└── GUI APPLICATION (lines 125–513)
    └── class PerformanceAnalyzerApp
        ├── __init__()              → Sets up the window, canvas, scrollbar
        ├── _configure_styles()     → Defines fonts and colors for widgets
        ├── _build_header()         → Title bar at the top
        ├── _build_input_section()  → Text fields + buttons
        ├── _build_results_container() → Empty frame that gets filled after analysis
        ├── _generate_random()      → Fills in random numbers
        ├── _clear_all()            → Clears inputs + results
        ├── _run_analysis()         → THE MAIN FUNCTION — runs all algorithms, shows output
        ├── _sort_card()            → Creates a result card for each sorting algorithm
        ├── _search_card()          → Creates a result card for each search algorithm
        ├── _comparison_table()     → Builds the side-by-side comparison table
        └── _bar_chart()            → Draws horizontal bars comparing times
```

---

## 📖 How Each Algorithm Works (Simple Explanations)

---

### 1️⃣ Bubble Sort

**One-line idea:** Walk through the list, compare neighbours, swap if wrong — repeat until sorted.

**Step-by-step example:**

```
Start:  [64, 34, 25, 12]

Pass 1: Compare 64 & 34 → swap → [34, 64, 25, 12]
        Compare 64 & 25 → swap → [34, 25, 64, 12]
        Compare 64 & 12 → swap → [34, 25, 12, 64]  ← 64 bubbled to the end

Pass 2: Compare 34 & 25 → swap → [25, 34, 12, 64]
        Compare 34 & 12 → swap → [25, 12, 34, 64]

Pass 3: Compare 25 & 12 → swap → [12, 25, 34, 64]  ✅ SORTED!
```

**How the code works:**
```python
def bubble_sort(arr):
    a = arr[:]              # Make a copy so original isn't changed
    n = len(a)
    comparisons = 0
    swaps = 0
    for i in range(n - 1):          # Outer loop: n-1 passes
        swapped = False
        for j in range(n - 1 - i):  # Inner loop: shrinks each pass
            comparisons += 1
            if a[j] > a[j + 1]:     # Compare neighbours
                a[j], a[j + 1] = a[j + 1], a[j]  # Swap them
                swaps += 1
                swapped = True
        if not swapped:             # OPTIMIZATION: if no swaps, already sorted
            break
    return a, comparisons, swaps, time_taken
```

**Key points to remember:**
- **Two nested loops** → O(n²) time
- Has an **early exit optimization** (`swapped` flag)
- Best case: O(n) when list is already sorted
- Worst case: O(n²) when list is reverse sorted

---

### 2️⃣ Selection Sort

**One-line idea:** Find the smallest element, put it first. Find the next smallest, put it second. Repeat.

**Step-by-step example:**

```
Start: [64, 34, 25, 12]

Pass 1: Scan all → minimum is 12 → swap with index 0 → [12, 34, 25, 64]
Pass 2: Scan from index 1 → minimum is 25 → swap with index 1 → [12, 25, 34, 64]
Pass 3: Scan from index 2 → minimum is 34 → already in place → [12, 25, 34, 64]  ✅ SORTED!
```

**How the code works:**
```python
def selection_sort(arr):
    a = arr[:]
    n = len(a)
    for i in range(n - 1):
        min_idx = i                      # Assume current position has minimum
        for j in range(i + 1, n):        # Search for actual minimum
            comparisons += 1
            if a[j] < a[min_idx]:
                min_idx = j
        if min_idx != i:                 # Swap only if needed
            a[i], a[min_idx] = a[min_idx], a[i]
            swaps += 1
    return a, comparisons, swaps, time_taken
```

**Key points to remember:**
- Always does **exactly n(n-1)/2 comparisons** regardless of input
- Does **at most n-1 swaps** (fewest swaps of all three algorithms!)
- Time complexity: O(n²) in ALL cases (best = worst = average)
- Good when **writing/swapping is expensive** (e.g. writing to disk)

---

### 3️⃣ Insertion Sort

**One-line idea:** Pick each element and insert it into its correct position among the already-sorted elements on the left.

**Step-by-step example:**

```
Start: [64, 34, 25, 12]

Step 1: Take 34, insert into [64]        → Shift 64 right → [34, 64, 25, 12]
Step 2: Take 25, insert into [34, 64]    → Shift 34,64 right → [25, 34, 64, 12]
Step 3: Take 12, insert into [25, 34, 64]→ Shift all right → [12, 25, 34, 64]  ✅ SORTED!
```

**How the code works:**
```python
def insertion_sort(arr):
    a = arr[:]
    for i in range(1, n):            # Start from 2nd element
        key = a[i]                    # Element to insert
        j = i - 1
        while j >= 0 and a[j] > key: # Shift larger elements right
            comparisons += 1
            a[j + 1] = a[j]          # Shift
            swaps += 1
            j -= 1
        a[j + 1] = key               # Place the key in correct position
    return a, comparisons, swaps, time_taken
```

**Key points to remember:**
- Best case: O(n) when list is already sorted (inner loop doesn't execute)
- Worst case: O(n²) when list is reverse sorted
- **Best algorithm for small or nearly-sorted data** in practice
- Works like sorting playing cards in your hand

---

### 4️⃣ Linear Search

**One-line idea:** Check every element one by one from start to end.

**Step-by-step example:**

```
List:   [64, 34, 25, 12, 22]
Target: 25

Index 0: 64 ≠ 25  → next
Index 1: 34 ≠ 25  → next
Index 2: 25 = 25  → ✅ FOUND at index 2! (3 comparisons)
```

**How the code works:**
```python
def linear_search(arr, target):
    comparisons = 0
    for i in range(len(arr)):
        comparisons += 1
        if arr[i] == target:
            return True, i, comparisons   # Found!
    return False, -1, comparisons          # Not found
```

**Key points to remember:**
- Works on **unsorted AND sorted** lists
- Time: O(n) — must check every element in worst case
- No preprocessing needed
- Simple but slow for large data

---

### 5️⃣ Binary Search

**One-line idea:** On a **sorted** list, check the middle element. If target is smaller, search the left half. If larger, search the right half. Repeat.

**Step-by-step example:**

```
Sorted List: [3, 11, 12, 22, 25, 34, 45, 64, 78, 90]
Target: 45

Step 1: mid = index 4 → value 25 < 45  → search RIGHT half [34, 45, 64, 78, 90]
Step 2: mid = index 7 → value 64 > 45  → search LEFT half  [34, 45]
Step 3: mid = index 5 → value 34 < 45  → search RIGHT half [45]
Step 4: mid = index 6 → value 45 = 45  → ✅ FOUND! (4 comparisons)
```

**How the code works:**
```python
def binary_search(arr, target):
    comparisons = 0
    low = 0
    high = len(arr) - 1
    while low <= high:
        mid = (low + high) // 2       # Find the middle
        comparisons += 1
        if arr[mid] == target:
            return True, mid, comparisons
        elif arr[mid] < target:
            low = mid + 1              # Search right half
        else:
            high = mid - 1             # Search left half
    return False, -1, comparisons
```

**Key points to remember:**
- **REQUIRES sorted input** — the program uses the Bubble Sort output
- Time: O(log n) — cuts the search space in half each step
- For 1,000,000 elements: Linear Search needs up to 1,000,000 comparisons, Binary Search needs only ~20!
- Uses `low`, `high`, and `mid` pointers

---

## 📊 What the Program Measures

| Metric | What It Counts | How It's Measured |
|---|---|---|
| **Comparisons** | Number of times two elements are compared (`if a > b`) | Counter variable incremented inside the algorithm |
| **Swaps** | Number of times two elements exchange positions | Counter variable incremented when a swap happens |
| **Time** | How long the algorithm takes to run | `time.perf_counter()` before and after, converted to **microseconds** (×10⁶) |

> **Why microseconds?** These algorithms run so fast on small data that milliseconds would show `0.00`. Microseconds give us meaningful numbers to compare.

---

## 🎨 GUI Features

### Dark-Themed Interface

| Element | Color | Hex Code |
|---|---|---|
| Background | Deep navy | `#0f0f1a` |
| Cards | Dark blue-grey | `#1a1a2e` |
| Input fields | Navy blue | `#16213e` |
| Primary accent | Crimson red | `#e94560` |
| Success/Found | Green | `#00e676` |
| Info | Cyan | `#00e5ff` |
| Winner highlight | Gold | `#ffd700` |
| Secondary accent | Purple | `#bb86fc` |

### Input Section
- **Numbers field** — space-separated integers
- **Search target field** — the value to search for
- **ANALYZE button** — runs all 5 algorithms and displays results
- **Random Data button** — generates 8–20 random numbers (1–999)
- **Clear button** — resets all inputs and results

### Results Display (after clicking ANALYZE)

| Section | What It Shows |
|---|---|
| **Original List** | Your input data + element count |
| **Sorting Results** | One color-coded card per algorithm with sorted list, comparisons, swaps, time |
| **Comparison Table** | Side-by-side metrics table for all 3 sorting algorithms |
| **Bar Chart** | Horizontal bars visually comparing execution times |
| **🏆 Best Performers** | Gold box showing fastest algorithm, fewest comparisons, fewest swaps |
| **Search Results** | Cards for Linear Search (on original list) & Binary Search (on sorted list) |
| **Search Summary** | Which search method used fewer comparisons |

### Scrollable Layout
All results are inside a scrollable canvas with **mouse-wheel support**, so you can scroll through the results without resizing the window.

---

## 🔑 Key Takeaways (Comparison Tables)

### Sorting Algorithms Comparison

| Property | Bubble Sort | Selection Sort | Insertion Sort |
|---|---|---|---|
| **Best Case Time** | O(n) | O(n²) | O(n) |
| **Average Case Time** | O(n²) | O(n²) | O(n²) |
| **Worst Case Time** | O(n²) | O(n²) | O(n²) |
| **Space Complexity** | O(1) | O(1) | O(1) |
| **Stable?** | ✅ Yes | ❌ No | ✅ Yes |
| **Adaptive?** | ✅ Yes (early exit) | ❌ No | ✅ Yes |
| **Fewest Swaps?** | ❌ | ✅ Yes | ❌ |
| **Best For** | Teaching | Minimizing writes | Nearly-sorted data |

### Searching Algorithms Comparison

| Property | Linear Search | Binary Search |
|---|---|---|
| **Time Complexity** | O(n) | O(log n) |
| **Requires Sorted Input?** | ❌ No | ✅ Yes |
| **Best Case** | O(1) — first element | O(1) — middle element |
| **Worst Case** | O(n) — last or not found | O(log n) |
| **Space Complexity** | O(1) | O(1) |

---

## 💡 Important Concepts Used in the Code

### 1. `time.perf_counter()`
- Most precise timer available in Python
- Returns time in **seconds** (as a float)
- We multiply by `1e6` (1,000,000) to convert to **microseconds**
- Why not `time.time()`? → `perf_counter()` has **nanosecond resolution** and is not affected by system clock changes

### 2. List Slicing `arr[:]`
- Creates a **copy** of the list so the original isn't modified
- Without this, all 3 sorting functions would sort the same list, and only the first would do real work

### 3. `tkinter`
- Python's **built-in** GUI library — no `pip install` needed
- Uses **widgets** like `Label`, `Entry`, `Button`, `Canvas`, `Frame`
- `ttk` = themed tkinter widgets (more modern look)
- `messagebox` = popup dialog boxes for errors/warnings

### 4. `random` module
- `random.randint(a, b)` → random integer between a and b (inclusive)
- `random.choice(list)` → picks a random element from the list

### 5. Object-Oriented Programming (OOP)
- The GUI is built as a **class** (`PerformanceAnalyzerApp`)
- `self` refers to the current instance of the class
- `__init__` is the **constructor** — runs when the object is created
- Methods starting with `_` are **private** (convention, not enforced)

---

## ✅ Requirements

- **Python 3.6+** (uses f-strings like `f"Result: {value}"`)
- **No external libraries** — only uses `tkinter`, `time`, `random` (all built-in)
- Works on **Windows, macOS, and Linux**

---

---

# 🎓 VIVA QUESTIONS & ANSWERS

> Below are questions your examiner might ask during a viva. Answers are written to be clear and concise.

---

## Section A: General / Overview Questions

**Q1: What does your project do?**
> It's a GUI application that lets users enter a list of numbers and a search target, then runs 3 sorting algorithms (Bubble, Selection, Insertion) and 2 searching algorithms (Linear, Binary) on the data. It compares their performance by counting comparisons, swaps, and measuring execution time — and displays everything visually with cards, tables, and bar charts.

**Q2: Why did you choose these specific algorithms?**
> These are the fundamental comparison-based algorithms taught in computer science. They have different time complexities and behaviours, which makes them ideal for a performance comparison tool. Bubble, Selection, and Insertion sort are all O(n²) but differ in their number of comparisons and swaps. Linear and Binary search demonstrate O(n) versus O(log n) — a massive difference.

**Q3: Which libraries/modules did you use?**
> Three modules — all built into Python:
> - `tkinter` — for creating the GUI (windows, buttons, labels, etc.)
> - `time` — specifically `time.perf_counter()` for high-precision timing
> - `random` — for generating random test data

**Q4: Why did you use `time.perf_counter()` instead of `time.time()`?**
> `perf_counter()` provides the highest resolution timer available on the operating system. Unlike `time.time()`, it is not affected by system clock adjustments and has nanosecond precision, which is important because our algorithms run in microseconds.

**Q5: What is the significance of measuring performance in microseconds?**
> On small datasets, sorting algorithms complete in fractions of a millisecond. Using microseconds (1 second = 1,000,000 microseconds) gives us numbers that are large enough to compare meaningfully.

---

## Section B: Sorting Algorithm Questions

**Q6: Explain Bubble Sort in simple terms.**
> Walk through the list, compare adjacent elements, swap them if they're in the wrong order. The largest element "bubbles" to the end after each pass. Repeat until no swaps are needed.

**Q7: What is the optimization in your Bubble Sort?**
> The `swapped` flag. If no swaps happen during an entire pass, the list is already sorted, so we `break` out of the loop early. This makes Bubble Sort's best case O(n) instead of O(n²).

**Q8: Why does Selection Sort have the fewest swaps?**
> Because it does **at most one swap per pass** — it finds the minimum element and swaps it directly into position. Bubble Sort and Insertion Sort swap/shift multiple elements per pass.

**Q9: Why is Insertion Sort efficient on nearly-sorted data?**
> Because the inner `while` loop only runs when elements need to be shifted. If the list is nearly sorted, most elements are already in or close to their correct position, so the inner loop executes very few times — approaching O(n).

**Q10: What is the time complexity of all three sorting algorithms?**

| Algorithm | Best | Average | Worst |
|---|---|---|---|
| Bubble Sort | O(n) | O(n²) | O(n²) |
| Selection Sort | O(n²) | O(n²) | O(n²) |
| Insertion Sort | O(n) | O(n²) | O(n²) |

**Q11: What does "stable" sorting mean?**
> A stable sort preserves the **relative order** of elements that have equal values. For example, if two elements with value 5 appear in positions 2 and 7 in the input, a stable sort keeps the one from position 2 before the one from position 7. Bubble Sort and Insertion Sort are stable. Selection Sort is **not stable**.

**Q12: Why does Selection Sort always make the same number of comparisons?**
> Because it always scans the entire remaining unsorted portion to find the minimum, regardless of whether the data is sorted or not. It doesn't have an early exit mechanism. The formula is n(n-1)/2 comparisons always.

**Q13: What does `a = arr[:]` do? Why is it important?**
> It creates a **shallow copy** of the input list. Without this, all three sorting functions would modify the same list object, and only the first sort would do real work (the others would receive an already-sorted list, giving misleading performance data).

**Q14: What is the space complexity of these sorting algorithms?**
> All three are **O(1)** auxiliary space — they sort in-place (plus the copy we make). They don't require extra arrays proportional to input size.

**Q15: In what scenario would Bubble Sort outperform the others?**
> When the list is already sorted or almost sorted. Thanks to the `swapped` flag optimization, Bubble Sort can detect this in a single O(n) pass and exit early.

---

## Section C: Searching Algorithm Questions

**Q16: What is the difference between Linear Search and Binary Search?**
> Linear Search checks elements **one by one** from the start — works on any list, takes O(n) time. Binary Search checks the **middle element** and eliminates half the remaining list each step — takes O(log n) time, but **requires the list to be sorted first**.

**Q17: Why does Binary Search require sorted input?**
> Because it makes decisions based on whether the target is less than or greater than the middle element. If the list isn't sorted, the assumption that "all smaller elements are to the left" would be wrong, and the algorithm would miss valid results.

**Q18: In your program, which list does each search run on?**
> - **Linear Search** runs on the **original (unsorted)** list — because it doesn't need sorted data.
> - **Binary Search** runs on the **sorted list** produced by Bubble Sort — because it requires sorted input.

**Q19: If a list has 1,000,000 elements, how many comparisons would each search need in the worst case?**
> - **Linear Search:** 1,000,000 comparisons (checks every element)
> - **Binary Search:** ~20 comparisons (log₂(1,000,000) ≈ 19.93)

**Q20: What does the program return when an element is not found?**
> Both functions return `(False, -1, comparisons)`. `False` means not found, `-1` is a sentinel index indicating "no valid position," and `comparisons` shows how many checks were made.

**Q21: What is the best case for Binary Search?**
> When the target is exactly at the middle of the list — found in just **1 comparison**, giving O(1) best case.

---

## Section D: GUI / Tkinter Questions

**Q22: What is `tkinter`?**
> Tkinter is Python's standard GUI (Graphical User Interface) library. It comes pre-installed with Python — you don't need to `pip install` anything. It provides widgets like buttons, labels, text fields, canvases, and frames.

**Q23: What is the difference between `tk` and `ttk`?**
> `tk` is the original Tkinter with basic widgets. `ttk` (themed Tkinter) provides modern-looking, platform-native widgets with configurable styles and themes. In the project, `ttk.Style()` is used to create a custom dark theme.

**Q24: How does the scrollable layout work?**
> A `tk.Canvas` widget is created as the main container. A `tk.Frame` is placed inside the canvas using `create_window()`. The frame holds all the content. When the frame's size exceeds the canvas, a `ttk.Scrollbar` allows vertical scrolling. Mouse-wheel scrolling is enabled via the `<MouseWheel>` event binding.

**Q25: What does `messagebox.showwarning()` do?**
> It creates a popup dialog box with a warning icon, a title, and a message. Used for input validation — e.g., when the user doesn't enter numbers or enters invalid data.

**Q26: What design pattern does the GUI use?**
> It uses **Object-Oriented Programming (OOP)**. The entire GUI is a single class (`PerformanceAnalyzerApp`) whose constructor (`__init__`) builds the window, and whose methods handle user actions and build result widgets.

**Q27: Why are method names prefixed with `_` (underscore)?**
> By Python convention, a leading underscore indicates a **private method** — meaning it's intended for internal use within the class only, not to be called from outside. It's a convention, not enforced by Python.

---

## Section E: Python-Specific Questions

**Q28: What are f-strings?**
> F-strings (formatted string literals) were introduced in Python 3.6. They let you embed expressions inside string literals using `{}`. Example: `f"Result: {value:.2f}"` inserts the variable `value` formatted to 2 decimal places.

**Q29: What does `arr[:]` vs `arr` mean when passing lists?**
> `arr` passes a **reference** to the original list — any changes inside the function affect the original. `arr[:]` creates a **copy** — the function works on a new list, leaving the original unchanged.

**Q30: What is `time.perf_counter()` and why multiply by `1e6`?**
> `time.perf_counter()` returns the current time in **seconds** as a floating-point number with high precision. Multiplying by `1e6` (which is 1,000,000) converts seconds to **microseconds**, since 1 second = 1,000,000 microseconds.

**Q31: What does `if __name__ == "__main__":` mean?**
> This is a Python guard that checks whether the file is being **run directly** (not imported as a module). If you run `python 16aprproject.py`, `__name__` is set to `"__main__"`, so the GUI launches. If another file does `import 16aprproject`, this block is skipped.

**Q32: Explain this line: `a[j], a[j+1] = a[j+1], a[j]`**
> This is Python's **tuple unpacking** — it swaps two variables without needing a temporary variable. In languages like C, you'd need `temp = a; a = b; b = temp;`. Python does it in one line.

---

## Section F: Tricky / Deep Questions

**Q33: Would the results change if you sorted an already-sorted list?**
> Yes! Bubble Sort would be the **fastest** (O(n) due to early exit), Insertion Sort would also be fast (O(n)), but Selection Sort would take the same time as always (O(n²)) because it has no early exit mechanism.

**Q34: Is your timing measurement perfectly accurate?**
> No. `time.perf_counter()` measures wall-clock time, which includes any OS interruptions (other processes, garbage collection, etc.). For very small inputs, the timing may be inconsistent. For a more accurate measurement, you could run each algorithm multiple times and average the results.

**Q35: Why do all three sorting algorithms have O(1) space complexity even though you create a copy with `arr[:]`?**
> The copy is O(n) space, but in algorithm analysis, we typically refer to **auxiliary space** — the extra space used beyond the input. The copy is made for correctness (preserving the original), not as part of the algorithm itself. The sorting operations themselves use O(1) extra space (in-place).

**Q36: Can Binary Search be implemented recursively?**
> Yes. Instead of a while loop, you call the function again with updated `low`/`high`. Example:
> ```python
> def binary_search_recursive(arr, target, low, high):
>     if low > high:
>         return False
>     mid = (low + high) // 2
>     if arr[mid] == target:
>         return True
>     elif arr[mid] < target:
>         return binary_search_recursive(arr, target, mid + 1, high)
>     else:
>         return binary_search_recursive(arr, target, low, mid - 1)
> ```
> The iterative version (used in the project) is preferred because it uses O(1) space vs O(log n) stack space for recursion.

**Q37: What happens if you enter duplicate numbers?**
> The program handles duplicates correctly. Sorting algorithms will place duplicates next to each other. Searching will find the **first occurrence** (Linear Search finds the leftmost, Binary Search may find any occurrence depending on where mid lands).

**Q38: Why is Binary Search run on the Bubble Sort output specifically?**
> It could run on any sorted output (Selection Sort or Insertion Sort would give the same sorted list). Bubble Sort's output is used simply because it's the first sorting result computed. All three produce the same sorted list.

**Q39: What is the `highlightbackground` and `highlightthickness` used for?**
> These are Tkinter Frame properties that create a **colored border** around widgets. `highlightbackground` sets the border color, and `highlightthickness` sets the border width in pixels. This creates the card-like look with colored edges.

**Q40: How does the bar chart work without any charting library?**
> It uses a `tk.Canvas` widget and draws rectangles with `create_rectangle()`. The bar width is calculated as a proportion of the maximum time: `bar_width = (this_time / max_time) * canvas_width`. This creates a simple but effective horizontal bar chart using only Tkinter.

---

## Section G: Quick-Fire / Conceptual Questions

**Q41: What is an algorithm?**
> A step-by-step procedure for solving a problem or performing a computation in a finite number of steps.

**Q42: What is time complexity?**
> A measure of how the running time of an algorithm increases as the input size grows. Expressed using Big-O notation (e.g., O(n), O(n²), O(log n)).

**Q43: What does O(n²) mean in plain English?**
> If the input size doubles, the running time roughly **quadruples** (2² = 4). For example, sorting 100 elements takes ~10,000 operations; sorting 200 takes ~40,000.

**Q44: What does O(log n) mean in plain English?**
> If the input size doubles, the running time increases by only **one extra step**. For example, searching 1,000 elements takes ~10 steps; searching 2,000 takes ~11 steps.

**Q45: What is the difference between comparison-based and non-comparison-based sorting?**
> Comparison-based sorting (like Bubble, Selection, Insertion, Merge, Quick Sort) decides element order by comparing pairs. **Non-comparison-based** sorting (like Counting Sort, Radix Sort) uses element values directly. All comparison-based sorts have a lower bound of O(n log n). Our project uses comparison-based algorithms.

**Q46: What does "in-place sorting" mean?**
> An in-place sorting algorithm sorts the data using only a constant amount of extra memory (O(1) space), not creating a new array proportional to input size. All three sorting algorithms in this project are in-place.

**Q47: What is a GUI?**
> GUI stands for Graphical User Interface. It's a visual interface with windows, buttons, text fields, etc., as opposed to a CLI (Command Line Interface) where users type text commands.

**Q48: What is OOP (Object-Oriented Programming)?**
> A programming paradigm that organizes code into **classes** (blueprints) and **objects** (instances). Classes contain data (**attributes**) and behavior (**methods**). In this project, `PerformanceAnalyzerApp` is a class, and `app = PerformanceAnalyzerApp(root)` creates an object.

**Q49: Can you add more algorithms to this project?**
> Yes! You could add Merge Sort (O(n log n)), Quick Sort (O(n log n) average), or other algorithms. You'd define a new function with the same signature (taking a list, returning sorted list + metrics), then add it to the `sort_data` list in `_run_analysis()`.

**Q50: What improvements could be made to this project?**
> - Add more algorithms (Merge Sort, Quick Sort, Heap Sort)
> - Allow loading data from a file
> - Add animated visualizations showing how each algorithm works step-by-step
> - Use `timeit` module for more accurate benchmarking (averaging multiple runs)
> - Add graphs using `matplotlib` for better chart quality
> - Export results to a PDF or CSV file
> - Add ascending/descending sort options

---

## 📝 Formulas to Remember

| Formula | Meaning |
|---|---|
| **n(n-1)/2** | Number of comparisons in Selection Sort (always) and Bubble Sort (worst case) |
| **log₂(n)** | Maximum comparisons in Binary Search |
| **O(n²)** | Quadratic — time grows with square of input |
| **O(n)** | Linear — time grows proportionally with input |
| **O(log n)** | Logarithmic — time grows very slowly |
| **O(1)** | Constant — time doesn't change with input size |
| **1 second = 10⁶ microseconds** | Unit conversion used in timing |

---

*Good luck with your viva! 🎯*
