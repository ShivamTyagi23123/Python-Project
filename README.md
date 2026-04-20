<div align="center">

# 🐍 Python Projects Portfolio

### Built by **Shivam Tyagi** | UPES Computer Science

[![Python](https://img.shields.io/badge/Python-3.6+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Tkinter](https://img.shields.io/badge/GUI-Tkinter-blue?style=for-the-badge)](https://docs.python.org/3/library/tkinter.html)
[![scikit-learn](https://img.shields.io/badge/ML-scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org)

</div>

---

> This repository contains two **desktop GUI applications** built with Python — one focused on **algorithm performance analysis** and the other on **machine learning-based student score prediction**. Both feature dark-themed interfaces, interactive visualizations, and detailed results.

---

## 📂 Projects at a Glance

| | ⚡ Sorting & Searching Analyzer | 🎓 Student Performance Advisor |
|---|---|---|
| **What it does** | Compares 5 algorithms side-by-side | Predicts exam scores using ML |
| **Category** | Algorithm Analysis | Machine Learning |
| **GUI Framework** | Tkinter | Tkinter + Matplotlib |
| **External Libraries** | None (100% built-in) | pandas, scikit-learn, matplotlib |
| **Lines of Code** | ~514 | ~987 |
| **Key Feature** | Bar charts & winner detection | What-if suggestions & goal planner |
| **Theme** | 🌙 Dark (Navy + Crimson) | 🌙 Dark (Navy + Teal) |

---

---

# ⚡ Project 1: Sorting & Searching Performance Analyzer

> A desktop GUI application that lets you compare the performance of **3 sorting algorithms** and **2 searching algorithms** side-by-side — with a sleek dark-themed interface, bar charts, and performance metrics.

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
python "Sorting & Searching Performance Analyzer.py"
```

A window will open. Here's what to do:

1. **Enter numbers** in the first text box, separated by spaces (e.g. `64 34 25 12 22`).
2. **Enter a search target** in the second text box (e.g. `25`).
3. Click **▶ ANALYZE** to run all 5 algorithms and see the results.
4. Click **🎲 Random Data** to auto-generate a random list and target.
5. Click **✕ Clear** to reset everything.

> **Tip:** You need at least 2 numbers for a meaningful comparison.

---

## 🗂️ Program Structure

```
Sorting & Searching Performance Analyzer.py  (514 lines, single file)
│
├── IMPORTS ─────────────────────── tkinter, time, random
│
├── COLOR PALETTE ───────────────── Dark theme colors (constants)
│
├── SORTING ALGORITHMS
│   ├── bubble_sort(arr)         → returns (sorted_list, comparisons, swaps, time)
│   ├── selection_sort(arr)      → returns (sorted_list, comparisons, swaps, time)
│   └── insertion_sort(arr)      → returns (sorted_list, comparisons, swaps, time)
│
├── SEARCHING ALGORITHMS
│   ├── linear_search(arr, target) → returns (found, index, comparisons)
│   └── binary_search(arr, target) → returns (found, index, comparisons)
│
└── GUI APPLICATION
    └── class PerformanceAnalyzerApp
        ├── __init__()              → Sets up the window, canvas, scrollbar
        ├── _configure_styles()     → Defines fonts and colors for widgets
        ├── _build_header()         → Title bar at the top
        ├── _build_input_section()  → Text fields + buttons
        ├── _build_results_container() → Empty frame that gets filled after analysis
        ├── _generate_random()      → Fills in random numbers
        ├── _clear_all()            → Clears inputs + results
        ├── _run_analysis()         → THE MAIN FUNCTION — runs all algorithms
        ├── _sort_card()            → Creates a result card for each sorting algorithm
        ├── _search_card()          → Creates a result card for each search algorithm
        ├── _comparison_table()     → Builds the side-by-side comparison table
        └── _bar_chart()            → Draws horizontal bars comparing times
```

---

## 📖 How Each Algorithm Works

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

**Key points:**
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

**Key points:**
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

**Key points:**
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

**Key points:**
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

**Key points:**
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

---

## 🔑 Sorting Algorithms Comparison

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

## 🔑 Searching Algorithms Comparison

| Property | Linear Search | Binary Search |
|---|---|---|
| **Time Complexity** | O(n) | O(log n) |
| **Requires Sorted Input?** | ❌ No | ✅ Yes |
| **Best Case** | O(1) — first element | O(1) — middle element |
| **Worst Case** | O(n) — last or not found | O(log n) |
| **Space Complexity** | O(1) | O(1) |

---

## ✅ Requirements

- **Python 3.6+** (uses f-strings)
- **No external libraries** — only uses `tkinter`, `time`, `random` (all built-in)
- Works on **Windows, macOS, and Linux**

---

---

# 🎓 Project 2: Student Performance Advisor

> A desktop GUI application built with **Python**, **Tkinter**, **scikit-learn**, **pandas**, and **matplotlib** that predicts a student's **final exam score** based on their daily habits — and gives **personalized advice** to improve it.

---

## 📌 Quick Overview

| Detail | Info |
|---|---|
| **Language** | Python 3 |
| **GUI Library** | Tkinter (built-in) |
| **ML Library** | scikit-learn (for machine learning models) |
| **Data Library** | pandas (for reading and processing CSV data) |
| **Chart Library** | matplotlib (for graphs inside the GUI) |
| **Dataset** | 10,000 student records (CSV file) |
| **ML Models Used** | Random Forest Regressor, PCA + Linear Regression |
| **What it Predicts** | Final exam score (0–100) |
| **What it Provides** | Score prediction, risk alerts, rule-based advice, ML what-if suggestions, weekly planner, progress tracker, daily checklist |

---

## 🚀 How to Run

### Step 1: Install Required Libraries
```bash
pip install pandas scikit-learn matplotlib
```
> **Note:** `tkinter`, `json`, `datetime`, `pathlib`, `time` are all built into Python — no install needed.

### Step 2: Make Sure the Dataset File Exists
The file `global_university_students_performance_habits_10000.csv` must be in the **same folder** as the script.

### Step 3: Run the Program
```bash
python project.py
```

### What Happens When You Run It
1. The program **loads the CSV dataset** (10,000 student records).
2. It **trains two ML models** (Random Forest and PCA + Linear Regression) and picks the better one.
3. A **GUI window** opens where you can:
   - Enter your daily habits (study hours, sleep, screen time, etc.)
   - Click **"Analyze My Profile"** to get your predicted score + advice
   - Use **presets** (Focused / Balanced / At Risk) for quick testing
   - Set a **goal score** and get a step-by-step plan to reach it
   - View **charts** comparing your habits to the dataset median
   - Track your **progress** across multiple analyses
   - Use a **daily checklist** to build good habits

---

## 🗂️ Program Structure

```
project.py  (987 lines, single file)
│
├── IMPORTS ──────────────────────── json, tkinter, datetime, pathlib, pandas,
│                                    sklearn, matplotlib
│
├── CONSTANTS
│   ├── File paths (DATA_FILE, HISTORY_FILE, CHECKLIST_FILE, etc.)
│   ├── FEATURES list (14 input features)
│   ├── FIELD_SPECS (label, min, max, default, step for each field)
│   └── CHECKLIST_TASKS (6 daily habit tasks)
│
├── DATA LOADING
│   └── load_dataset(path)         → Reads CSV, cleans data, returns DataFrame
│
├── MODEL TRAINING
│   └── train_model(df)            → Trains 2 models, picks best, returns bundle
│
├── PREDICTION
│   ├── clamp(value)               → Keeps score between 0 and 100
│   ├── performance_band(score)    → Returns "Excellent"/"Strong"/"Moderate"/"Needs Attention"
│   ├── predict_score(bundle, values) → Returns (predicted, low, high)
│   └── predict_point(bundle, values) → Returns just the predicted score
│
├── ADVICE ENGINE
│   ├── rule_based_advice(values, medians) → Checks habits against thresholds
│   └── ml_improvement_opportunities()     → Tries changing 1 feature at a time
│
└── GUI APPLICATION
    └── class PerformanceAdvisorApp
        ├── __init__()               → Window setup, loads models, builds UI
        ├── setup_styles()           → Dark theme configuration
        ├── build_ui()               → Main layout (left panel + right panel)
        ├── build_form()             → Input fields + spinboxes + presets
        ├── build_output()           → 5-tab notebook (Overview, Planner, Progress, Checklist, Charts)
        ├── analyze_profile()        → THE MAIN FUNCTION — predicts, advises, displays
        ├── compute_risk_alert()     → Checks 6 risk factors, returns alert level
        ├── suggest_goal_plan()      → Greedy search: which habit changes reach the goal?
        ├── build_weekly_plan()      → Generates a 7-day study plan
        ├── update_charts()          → Draws habit comparison + progress line chart
        └── on_close()               → Saves everything before closing
```

---

## 📖 How Each Part Works

---

### 1️⃣ Data Loading (`load_dataset`)

**What it does:** Reads the CSV file containing 10,000 student records and prepares it for machine learning.

**Step by step:**
```
1. Check if the CSV file exists → if not, raise an error
2. Read the CSV using pandas → creates a DataFrame (like a spreadsheet in Python)
3. Check that all required columns exist (14 features + final_exam_score)
4. Convert "part_time_job" from "Yes"/"No" text → 1/0 numbers
5. Convert all columns to numbers, mark invalid entries as NaN
6. Drop any rows where final_exam_score is missing
7. Fill missing feature values with the column's median
8. Return the clean DataFrame
```

**Key code:**
```python
df = pd.read_csv(path)                                    # Read CSV file
df["part_time_job"] = df["part_time_job"].map({"yes": 1, "no": 0})  # Text → number
df[col] = pd.to_numeric(df[col], errors="coerce")         # Force numeric
df[col] = df[col].fillna(df[col].median())                # Fill blanks with median
```

**Why the median?** Unlike the mean (average), the median isn't affected by extreme values (outliers). If most students study 4 hours but one studies 20, the median stays reasonable.

---

### 2️⃣ Model Training (`train_model`)

**What it does:** Trains TWO machine learning models and automatically picks the better one.

**The two models:**

| Model | What it is | How it works |
|---|---|---|
| **Random Forest** | An ensemble of 220 decision trees | Each tree learns slightly different patterns; predictions are averaged for accuracy |
| **PCA + Linear Regression** | Dimensionality reduction + linear model | PCA reduces 14 features down to 8 components, then Linear Regression fits a line through the data |

**Training pipeline:**
```
Full Dataset (10,000 rows)
    │
    ├── 80% Training Set (8,000 rows)
    │       ├── 80% → Train the model (6,400 rows)
    │       └── 20% → Validation set for calibration (1,600 rows)
    │
    └── 20% Test Set (2,000 rows) → Final accuracy check
```

**What is Isotonic Calibration?**
After a model makes predictions, they might be systematically off (e.g., always 3 points too high). Isotonic Regression learns this bias from the validation set and corrects future predictions. Think of it as "fine-tuning" the model's output.

**Model selection:**
```python
if pca_result["mae"] < rf_result["mae"]:
    selected = pca_bundle      # PCA wins if it has lower error
else:
    selected = rf_bundle       # Otherwise Random Forest wins
```

**Metrics tracked:**
| Metric | What it means |
|---|---|
| **R² (R-squared)** | How much of the score variation the model explains (1.0 = perfect, 0.0 = useless) |
| **MAE (Mean Absolute Error)** | Average difference between predicted and actual scores |

---

### 3️⃣ Prediction (`predict_score`)

**What it does:** Takes your habit values, runs them through the trained model, and returns a predicted exam score.

**The prediction pipeline:**
```
Your inputs → Model predicts raw score → Calibrator adjusts → Habit penalties applied → Final score
```

**Habit penalties** (conservative adjustments):
| Condition | Penalty |
|---|---|
| Study hours < 4/day | +0.8 points deducted |
| Attendance < 90% | +0.8 points deducted |
| Sleep < 7 hours | +0.6 points deducted |
| Screen time > 5 hours | +0.6 points deducted |
| Stress > 6/10 | +0.6 points deducted |
| Exam prep < 14 days | +0.7 points deducted |

**Why penalties?** The dataset has many students scoring exactly 100, which skews the model optimistically. Penalties make predictions more realistic and conservative.

---

### 4️⃣ Advice Engine

#### Rule-Based Advice (`rule_based_advice`)
Compares your habits against **hardcoded thresholds** and gives common-sense suggestions:

```python
if values["study_hours_per_day"] < 4.0:
    advice.append("Increase study time to at least 4.0 hours/day...")
if values["sleep_hours"] < 7.0:
    advice.append("Aim for 7-8 hours of sleep...")
```

This is **NOT** machine learning — it's simple if-else rules based on educational research.

#### ML What-If Suggestions (`ml_improvement_opportunities`)
This IS machine learning. It works by:
```
1. Get your current predicted score (baseline)
2. For each habit (study hours, sleep, screen time, etc.):
   a. Change JUST that one habit to a better value
   b. Predict the new score
   c. Calculate the gain (new score - baseline)
3. Show the top 5 improvements sorted by gain
```

Example output:
> "If you study 1.5 hours more per day, the model predicts about 82.3/100 (+3.2 points from your current profile)."

---

### 5️⃣ Risk Alert System (`compute_risk_alert`)

Checks 6 danger indicators and gives an alert level:

| Risk Factor | Threshold |
|---|---|
| Study hours | < 3.0/day |
| Attendance | < 85% |
| Sleep | < 6 hours |
| Stress | > 7/10 |
| Screen time | > 6 hours |
| Exam prep | < 10 days |

| Risk Count | Alert Level |
|---|---|
| 0–1 | 🟢 Low |
| 2–3 | 🟡 Moderate |
| 4+ | 🔴 High |

---

### 6️⃣ Goal Planner (`suggest_goal_plan`)

Uses a **greedy algorithm** to find the smallest habit changes needed to reach your target score:

```
1. Set target (e.g., 95)
2. Calculate current predicted score (e.g., 78)
3. For each habit, try small, medium, and large improvements
4. Pick the change that gives the BIGGEST score boost
5. Apply it and repeat up to 6 times
6. Show the step-by-step plan
```

This is like climbing a hill — at each step, you take the steepest path upward.

---

### 7️⃣ GUI Application (5 Tabs)

| Tab | What it Shows |
|---|---|
| **Overview** | Predicted score, confidence range, performance band, risk alert, model accuracy info |
| **Goal + Planner** | Set a target score → get a step-by-step plan; or generate a 7-day weekly study plan |
| **Progress** | Table of all past analyses (timestamp, score, range, band) — persisted across sessions |
| **Checklist** | 6 daily habit checkboxes (e.g., "Sleep at least 7 hours") — state saved to JSON |
| **Charts** | Bar chart comparing your habits vs dataset median; line chart of your score history |

---

## 📊 The 14 Input Features

| # | Feature | Range | What it Means |
|---|---|---|---|
| 1 | GPA | 0–10 | Current academic grade point average (displayed as 0-10, internally converted to 0-4 scale) |
| 2 | University Year | 1–4 | Current year of study |
| 3 | Study Hours/Day | 0–12 | Hours spent studying each day |
| 4 | Class Attendance % | 0–100 | Percentage of classes attended |
| 5 | Sleep Hours | 0–12 | Hours of sleep per night |
| 6 | Screen Time Hours | 0–16 | Total non-study screen time per day |
| 7 | Social Media Hours | 0–16 | Time on social media per day |
| 8 | Gaming Hours | 0–16 | Time playing games per day |
| 9 | Exercise Hours/Week | 0–30 | Weekly exercise hours |
| 10 | Part-Time Job | Yes/No | Whether the student has a part-time job (converted to 1/0) |
| 11 | Mental Stress Level | 0–10 | Self-reported stress (0 = none, 10 = extreme) |
| 12 | AI Tool Usage Hours | 0–10 | Hours using AI tools (ChatGPT, etc.) per day |
| 13 | Exam Prep Days | 0–60 | How many days before the exam the student starts preparing |
| 14 | Coffee/Day | 0–10 | Cups of coffee consumed per day |

**Target variable:** `final_exam_score` (0–100)

---

## 🔑 Key ML Concepts Used

### Machine Learning Pipeline
```
Raw Data → Clean → Split → Train Models → Calibrate → Predict → Post-process
```

### Train/Validation/Test Split
- **Training set (64%)** — model learns from this
- **Validation set (16%)** — used for calibration (adjusting predictions)
- **Test set (20%)** — final accuracy check (model NEVER sees this during training)

Why 3 splits? If you calibrate on the same data you test on, your accuracy metrics would be misleadingly high (data leakage).

### Random Forest Regressor
- An **ensemble** of 220 decision trees
- Each tree is trained on a random subset of data and features
- Final prediction = **average** of all 220 trees' predictions
- Key parameters: `max_depth=14`, `min_samples_leaf=2`, `n_jobs=-1` (use all CPU cores)

### PCA (Principal Component Analysis)
- Reduces 14 features to 8 **principal components**
- Each component is a weighted combination of original features
- Removes noise and redundancy (e.g., social_media_hours and screen_time_hours are correlated)
- `StandardScaler` normalizes features first (important because PCA is sensitive to scale)

### Isotonic Calibration
- Fits a **monotonically increasing function** over the residuals (errors)
- Maps raw predictions to calibrated predictions
- `out_of_bounds="clip"` handles new predictions outside the calibration range

### Data Persistence (JSON)
The app saves 3 files inside `advisor_data/`:
| File | What it Stores |
|---|---|
| `advisor_last_inputs.json` | Your most recent form inputs (restored on next launch) |
| `advisor_history.json` | All past predictions (up to 100 entries) |
| `advisor_checklist.json` | Checkbox states for the daily checklist |

---

## ✅ Requirements

| Requirement | Version |
|---|---|
| Python | 3.6+ (uses f-strings) |
| pandas | Any recent version |
| scikit-learn | Any recent version |
| matplotlib | Any recent version |
| tkinter | Built into Python |

Install all external libraries at once:
```bash
pip install pandas scikit-learn matplotlib
```

---

---

# 🔑 Shared Concepts Across Both Projects

## 💡 Common Python Concepts

### `time.perf_counter()`
- Most precise timer available in Python
- Returns time in **seconds** (as a float)
- Used in the Sorting project (×10⁶ for microseconds)
- Why not `time.time()`? → `perf_counter()` has **nanosecond resolution** and is not affected by system clock changes

### List Slicing `arr[:]`
- Creates a **copy** of the list so the original isn't modified
- Critical in the Sorting project — without this, only the first sort would do real work

### `tkinter` (Used in Both)
- Python's **built-in** GUI library — no `pip install` needed
- Uses **widgets** like `Label`, `Entry`, `Button`, `Canvas`, `Frame`
- `ttk` = themed tkinter widgets (more modern look)
- `messagebox` = popup dialog boxes for errors/warnings

### Object-Oriented Programming (OOP)
- Both GUIs are built as **classes** (`PerformanceAnalyzerApp` and `PerformanceAdvisorApp`)
- `self` refers to the current instance of the class
- `__init__` is the **constructor** — runs when the object is created
- Methods starting with `_` are **private** (convention, not enforced)

### `if __name__ == "__main__":`
- Python guard that checks whether the file is being **run directly** (not imported as a module)
- Both projects use this pattern to launch the GUI

### f-strings
- Formatted string literals (Python 3.6+)
- Embed expressions inside strings using `{}`
- Example: `f"Result: {value:.2f}"`

---

## 📝 Formulas to Remember

### From the Sorting & Searching Project

| Formula | Meaning |
|---|---|
| **n(n-1)/2** | Number of comparisons in Selection Sort (always) and Bubble Sort (worst case) |
| **log₂(n)** | Maximum comparisons in Binary Search |
| **O(n²)** | Quadratic — time grows with square of input |
| **O(n)** | Linear — time grows proportionally with input |
| **O(log n)** | Logarithmic — time grows very slowly |
| **O(1)** | Constant — time doesn't change with input size |
| **1 second = 10⁶ microseconds** | Unit conversion used in timing |

### From the Student Performance Advisor

| Formula | Meaning |
|---|---|
| **R² = 1 − (SS_res / SS_tot)** | Fraction of variance explained by the model |
| **MAE = (1/n) Σ\|yᵢ − ŷᵢ\|** | Average absolute prediction error |
| **StandardScaler: z = (x − μ) / σ** | Normalize to mean=0, std=1 |
| **PCA** | Finds directions of maximum variance in the data |
| **Train/Val/Test = 64/16/20%** | Data split ratios used in this project |
| **clamp(x) = max(0, min(100, x))** | Keep score in valid range |

---

## 📁 Repository Structure

```
python-projects/
│
├── Sorting & Searching Performance Analyzer/
│   ├── Sorting & Searching Performance Analyzer.py   ← Algorithm comparison GUI
│   └── Sorting & Searching Performance Analyzer.md   ← Documentation
│
├── Student performance advisor/
│   ├── project.py                                     ← ML prediction GUI
│   ├── project_readme.md                              ← Documentation
│   ├── global_university_...csv                       ← Dataset (10,000 records)
│   └── advisor_data/                                  ← Auto-created saved state
│       ├── advisor_last_inputs.json
│       ├── advisor_history.json
│       └── advisor_checklist.json
│
├── Python Projects.md                                 ← This combined README
└── github front page.md                               ← GitHub profile README
```

---

<div align="center">

### 🛠️ Built with Python | 📊 Data-Driven | 🎨 Dark-Themed

**Made by [Shivam Tyagi](https://github.com/ShivamTyagi23123)**

</div>
