# Student Performance Advisor

A desktop application that predicts a student's final exam score based on their daily habits and provides personalized advice to improve performance.

---

## How to Run

```bash
pip install pandas scikit-learn matplotlib
python project_simple.py
```

Make sure the dataset file `global_university_students_performance_habits_10000.csv` is in the same folder as the script.

---

## What This Program Does

The program takes 14 student habit inputs (like study hours, sleep, screen time, etc.), feeds them into a trained Machine Learning model, and:

1. **Predicts** the student's likely final exam score (0-100)
2. **Gives advice** on what habits to change for a better score
3. **Tracks progress** across multiple runs
4. **Builds a weekly study plan** tailored to the student's profile

---

## Program Structure

```
project_simple.py
|
|-- Data Loading
|   load_dataset()          --> Reads CSV, cleans data, fills missing values
|
|-- Model Training
|   train_model()           --> Trains 2 models, picks the better one
|       Random Forest       --> Tree-based ML model (usually wins)
|       PCA + Linear Reg.   --> Simpler fallback model
|
|-- Prediction
|   predict_score()         --> Predicts score + confidence range
|   predict_point()         --> Returns just the score number
|
|-- Advice Engine
|   rule_based_advice()     --> If-else rules (e.g., "sleep < 7h -> sleep more")
|   ml_improvement_opportunities() --> Tests "what if" changes using the model
|
|-- GUI (Tkinter)
|   PerformanceAdvisorApp   --> The main window with 5 tabs
```

---

## How Each Part Works

### 1. Data Loading (`load_dataset`)

- Reads 10,000 student records from a CSV file
- Converts "Yes"/"No" part-time job column to 1/0
- Fills any missing values with the median of that column
- Returns a clean DataFrame ready for training

### 2. Model Training (`train_model`)

Two models are trained and compared:

| Model | How It Works |
|---|---|
| **Random Forest** | Builds 220 decision trees, each voting on the score. Takes the average vote. Handles complex patterns well. |
| **PCA + Linear Regression** | Reduces 14 features down to 8 using PCA (Principal Component Analysis), then fits a straight-line model. Simpler but sometimes enough. |

**Auto-selection**: The model with lower MAE (Mean Absolute Error) on test data is automatically chosen.

**Calibration**: After training, an Isotonic Regression calibrator is applied. This adjusts the raw predictions to better match actual scores, especially at the extremes.

**Data split**:
```
Full Dataset (10,000 rows)
    |-- 80% Training set
    |       |-- 80% for model training
    |       |-- 20% for calibration (validation set)
    |-- 20% Test set (final accuracy check)
```

### 3. Prediction (`predict_score`)

When you click "Analyze My Profile":

1. Your 14 inputs are put into a DataFrame
2. The model predicts a raw score
3. The calibrator adjusts it
4. A **conservative penalty** is applied based on risky habits:
   - Study < 4h/day → penalty
   - Attendance < 90% → penalty
   - Sleep < 7h → penalty
   - Screen time > 5h → penalty
   - Stress > 6 → penalty
   - Exam prep < 14 days → penalty
5. A **confidence range** (low-high) is calculated using the model's residual standard deviation
6. Returns: predicted score, low estimate, high estimate

### 4. Rule-Based Advice (`rule_based_advice`)

Simple if-else checks against recommended thresholds:

```
If study_hours < 4.0  -->  "Increase study time..."
If sleep < 7.0        -->  "Aim for 7-8 hours of sleep..."
If screen_time > 4.0  -->  "Reduce screen time..."
...and so on for 12 different habits
```

### 5. ML What-If Suggestions (`ml_improvement_opportunities`)

This is smarter than rule-based advice. It:

1. Takes your current profile
2. Tries changing one habit at a time (e.g., "what if you studied 1.5h more?")
3. Re-runs the prediction with that change
4. Reports the top 5 changes that would boost your score the most

Example output:
```
If you study 1.5 hours more per day, the model predicts about 82.3/100
(+3.2 points from your current profile).
```

### 6. Risk Alert (`compute_risk_alert`)

Checks 6 danger signals and counts how many apply:

| Check | Threshold |
|---|---|
| Study hours | < 3.0 hours/day |
| Attendance | < 85% |
| Sleep | < 6 hours |
| Stress level | > 7.0 |
| Screen time | > 6 hours |
| Exam prep | < 10 days |

- 0-1 flags → **Low risk**
- 2-3 flags → **Moderate risk**
- 4+ flags → **High risk** (immediate action needed)

### 7. Goal Planner (`suggest_goal_plan`)

If you set a target score (e.g., 90):

1. Checks if you already meet the target
2. If not, iteratively tries the best single-habit change
3. Applies it, then looks for the next best change
4. Repeats up to 6 steps or until the target is reached
5. Outputs a step-by-step plan like:
   ```
   - Increase study hours/day to 5.5 (about +2.10 predicted points)
   - Improve attendance to 95.0 (about +1.30 predicted points)
   ```

### 8. Weekly Plan (`build_weekly_plan`)

Generates a fixed 7-day study schedule based on your current inputs:
- Monday through Sunday activities
- Personalized daily goals (study hours, sleep target, screen limit)
- Top 4 priority habits pulled from rule-based advice

---

## The 14 Input Features

| Feature | What It Means | Range |
|---|---|---|
| GPA | Current grade point average | 0 - 10 |
| University Year | Year of study | 1 - 4 |
| Study Hours/Day | Hours spent studying per day | 0 - 12 |
| Class Attendance % | Percentage of classes attended | 0 - 100 |
| Sleep Hours | Hours of sleep per night | 0 - 12 |
| Screen Time Hours | Total screen time per day | 0 - 16 |
| Social Media Hours | Time on social media per day | 0 - 16 |
| Gaming Hours | Time gaming per day | 0 - 16 |
| Exercise Hours/Week | Weekly exercise hours | 0 - 30 |
| Mental Stress Level | Self-reported stress (0 = none) | 0 - 10 |
| AI Tool Usage Hours | Time using AI tools per day | 0 - 10 |
| Exam Prep Days | Days spent preparing for exams | 0 - 60 |
| Coffee/Day | Cups of coffee per day | 0 - 10 |
| Part-Time Job | Whether working part-time | Yes / No |

---

## GUI Tabs

| Tab | What It Shows |
|---|---|
| **Overview** | Predicted score, confidence range, performance band, risk alert, model accuracy stats |
| **Goal + Planner** | Set a target score and get a step-by-step plan, or generate a weekly study schedule |
| **Progress** | Table of all past predictions (timestamp, score, range, band) |
| **Checklist** | 6 daily tasks to check off (saved between sessions) |
| **Charts** | Bar chart comparing your habits vs dataset median, line chart of score history |

---

## Presets

Three quick profiles to try without entering every field:

| Preset | Description |
|---|---|
| **Focused** | High GPA, 6h study, 97% attendance, low screen time |
| **Balanced** | Average student with decent habits |
| **At Risk** | Low study, high screen/gaming, high stress, late exam prep |

---

## Files Created by the Program

The program saves data in an `advisor_data` folder next to the script:

| File | Purpose |
|---|---|
| `advisor_last_inputs.json` | Remembers your last entered values |
| `advisor_history.json` | Stores up to 100 past predictions |
| `advisor_checklist.json` | Saves checklist tick states |

---

## Key Libraries Used

| Library | Purpose |
|---|---|
| `pandas` | Data loading and manipulation |
| `scikit-learn` | Machine learning models (Random Forest, PCA, Linear Regression, Isotonic Regression) |
| `matplotlib` | Charts inside the GUI |
| `tkinter` | Desktop GUI (built into Python) |

---

## Requirements

- Python 3.6 or higher
- pandas
- scikit-learn
- matplotlib
- The CSV dataset file in the same directory
