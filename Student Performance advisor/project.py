from __future__ import annotations

import json
import tkinter as tk
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from tkinter import messagebox, ttk, filedialog
import numpy as np

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestRegressor
from sklearn.isotonic import IsotonicRegression
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler


APP_TITLE = "Student Performance Advisor"
DATA_FILE = Path(__file__).with_name("global_university_students_performance_habits_10000.csv")
APP_DATA_DIR = Path(__file__).with_name("advisor_data")
LAST_INPUTS_FILE = APP_DATA_DIR / "advisor_last_inputs.json"
HISTORY_FILE = APP_DATA_DIR / "advisor_history.json"
CHECKLIST_FILE = APP_DATA_DIR / "advisor_checklist.json"
PROFILES_DIR = APP_DATA_DIR / "profiles"
LEGACY_LAST_INPUTS_FILE = Path(__file__).with_name("advisor_last_inputs.json")
LEGACY_HISTORY_FILE = Path(__file__).with_name("advisor_history.json")
LEGACY_CHECKLIST_FILE = Path(__file__).with_name("advisor_checklist.json")
TARGET_COLUMN = "final_exam_score"

CHECKLIST_TASKS = [
	"Complete planned study hours",
	"Sleep at least 7 hours",
	"Keep screen time below 4 hours",
	"Revise weak topic for 45 minutes",
	"Do at least 20 minutes of exercise",
	"Prepare tomorrow's mini-study plan",
]

FEATURES = [
	"GPA",
	"university_year",
	"study_hours_per_day",
	"class_attendance_percent",
	"sleep_hours",
	"screen_time_hours",
	"social_media_hours",
	"gaming_hours",
	"exercise_hours_per_week",
	"part_time_job",
	"mental_stress_level",
	"AI_tool_usage_hours",
	"exam_preparation_days",
	"coffee_consumption_per_day",
]

# Tooltip descriptions for each feature to explain why it matters
FEATURE_TOOLTIPS = {
	"GPA": "Higher GPA correlates strongly with exam scores. Reflects your academic foundation.",
	"university_year": "Year of study. Senior students often have better study strategies.",
	"study_hours_per_day": "More study hours generally improve scores. 4-6 hours/day is the sweet spot.",
	"class_attendance_percent": "Attending classes regularly boosts understanding and marks.",
	"sleep_hours": "Sleep < 7h reduces memory consolidation by ~20%. Aim for 7-8h.",
	"screen_time_hours": "Excess screen time reduces focus and study efficiency.",
	"social_media_hours": "Social media is a major distraction. Keep it under 2h/day.",
	"gaming_hours": "Gaming > 1.5h/day negatively impacts study time allocation.",
	"exercise_hours_per_week": "Regular exercise improves concentration and reduces stress.",
	"mental_stress_level": "High stress impairs memory and exam performance.",
	"AI_tool_usage_hours": "AI tools can help if used for learning, not shortcuts.",
	"exam_preparation_days": "Starting exam prep 2+ weeks early gives better recall.",
	"coffee_consumption_per_day": "Moderate coffee is fine. >3 cups disrupts sleep quality.",
}


@dataclass(frozen=True)
class FieldSpec:
	key: str
	label: str
	minimum: float
	maximum: float
	default: float
	step: float = 0.1


@dataclass(frozen=True)
class ModelBundle:
	model: object
	calibrator: IsotonicRegression
	residual_std: float
	name: str


FIELD_SPECS = [
	FieldSpec("GPA", "Current GPA (0-10)", 0.0, 10.0, 8.0, 0.01),
	FieldSpec("university_year", "University Year", 1, 4, 2, 1),
	FieldSpec("study_hours_per_day", "Study Hours / Day", 0.0, 12.0, 4.0, 0.1),
	FieldSpec("class_attendance_percent", "Class Attendance %", 0.0, 100.0, 90.0, 0.1),
	FieldSpec("sleep_hours", "Sleep Hours", 0.0, 12.0, 7.0, 0.1),
	FieldSpec("screen_time_hours", "Screen Time Hours", 0.0, 16.0, 4.0, 0.1),
	FieldSpec("social_media_hours", "Social Media Hours", 0.0, 16.0, 2.0, 0.1),
	FieldSpec("gaming_hours", "Gaming Hours", 0.0, 16.0, 1.0, 0.1),
	FieldSpec("exercise_hours_per_week", "Exercise Hours / Week", 0.0, 30.0, 3.0, 0.1),
	FieldSpec("mental_stress_level", "Mental Stress Level", 0.0, 10.0, 4.5, 0.1),
	FieldSpec("AI_tool_usage_hours", "AI Tool Usage Hours", 0.0, 10.0, 1.0, 0.1),
	FieldSpec("exam_preparation_days", "Exam Prep Days", 0.0, 60.0, 14.0, 1.0),
	FieldSpec("coffee_consumption_per_day", "Coffee / Day", 0.0, 10.0, 2.0, 0.1),
]

# --- Dark and Light theme palettes ---
THEMES = {
	"dark": {
		"bg": "#0f172a",
		"card": "#111827",
		"fg": "#e5eefc",
		"accent": "#38bdf8",
		"subtitle": "#cbd5e1",
		"panel_fg": "#f8fafc",
		"btn_accent": "#2563eb",
		"btn_accent_active": "#1d4ed8",
		"btn_reset": "#334155",
		"btn_reset_active": "#475569",
		"trough": "#1e293b",
		"text_bg": "#0b1220",
		"lf_border": "#111827",
	},
	"light": {
		"bg": "#f1f5f9",
		"card": "#ffffff",
		"fg": "#1e293b",
		"accent": "#2563eb",
		"subtitle": "#475569",
		"panel_fg": "#0f172a",
		"btn_accent": "#2563eb",
		"btn_accent_active": "#1d4ed8",
		"btn_reset": "#94a3b8",
		"btn_reset_active": "#64748b",
		"trough": "#e2e8f0",
		"text_bg": "#ffffff",
		"lf_border": "#e2e8f0",
	},
}


def load_dataset(path: Path) -> pd.DataFrame:
	if not path.exists():
		raise FileNotFoundError(f"Dataset not found: {path}")

	df = pd.read_csv(path)
	required_columns = FEATURES + [TARGET_COLUMN]
	missing_columns = [column for column in required_columns if column not in df.columns]
	if missing_columns:
		raise ValueError(f"Missing required columns: {', '.join(missing_columns)}")

	df = df.copy()
	df["part_time_job"] = (
		df["part_time_job"].astype(str).str.strip().str.lower().map({"yes": 1, "no": 0})
	)

	for column in required_columns:
		df[column] = pd.to_numeric(df[column], errors="coerce")

	df = df.dropna(subset=[TARGET_COLUMN])

	for column in FEATURES:
		median_value = df[column].median()
		df[column] = df[column].fillna(median_value)

	return df


def train_model(df: pd.DataFrame):
	X = df[FEATURES]
	y = df[TARGET_COLUMN]

	X_train_full, X_test, y_train_full, y_test = train_test_split(
		X, y, test_size=0.2, random_state=42
	)
	X_train, X_val, y_train, y_val = train_test_split(
		X_train_full, y_train_full, test_size=0.2, random_state=42
	)

	def evaluate_candidate(name: str, model_obj: object) -> tuple[ModelBundle, dict[str, float]]:
		model_obj.fit(X_train, y_train)
		val_predictions_raw = model_obj.predict(X_val)

		calibrator = IsotonicRegression(out_of_bounds="clip")
		calibrator.fit(val_predictions_raw, y_val)

		test_predictions_raw = model_obj.predict(X_test)
		test_predictions_calibrated = calibrator.predict(test_predictions_raw)
		test_predictions_calibrated = pd.Series(test_predictions_calibrated).clip(0, 100).to_numpy()

		val_predictions_calibrated = calibrator.predict(val_predictions_raw)
		residual_std = float(pd.Series(y_val - val_predictions_calibrated).std(ddof=1))
		if pd.isna(residual_std) or residual_std <= 0:
			residual_std = 3.0

		result = {
			"r2": r2_score(y_test, test_predictions_calibrated),
			"mae": mean_absolute_error(y_test, test_predictions_calibrated),
			"r2_raw": r2_score(y_test, test_predictions_raw),
			"mae_raw": mean_absolute_error(y_test, test_predictions_raw),
		}
		bundle = ModelBundle(
			model=model_obj,
			calibrator=calibrator,
			residual_std=residual_std,
			name=name,
		)
		return bundle, result

	rf_model = RandomForestRegressor(
		n_estimators=220,
		random_state=42,
		max_depth=14,
		min_samples_leaf=2,
		n_jobs=-1,
	)
	pca_model = make_pipeline(
		StandardScaler(),
		PCA(n_components=min(8, len(FEATURES))),
		LinearRegression(),
	)

	rf_bundle, rf_result = evaluate_candidate("Random Forest", rf_model)
	pca_bundle, pca_result = evaluate_candidate("PCA + Linear Regression", pca_model)

	if pca_result["mae"] < rf_result["mae"]:
		selected_bundle, selected_result = pca_bundle, pca_result
	else:
		selected_bundle, selected_result = rf_bundle, rf_result

	# Extract feature importances from Random Forest
	feature_importances = {}
	if hasattr(rf_model, "feature_importances_"):
		for feat, imp in zip(FEATURES, rf_model.feature_importances_):
			feature_importances[feat] = float(imp)

	# Compute correlation with target
	correlations = {}
	for feat in FEATURES:
		correlations[feat] = float(df[feat].corr(df[TARGET_COLUMN]))

	metrics = {
		"r2": selected_result["r2"],
		"mae": selected_result["mae"],
		"r2_raw": selected_result["r2_raw"],
		"mae_raw": selected_result["mae_raw"],
		"rows": len(df),
		"pct_perfect": float((df[TARGET_COLUMN] == 100).mean() * 100),
		"selected_model": selected_bundle.name,
		"rf_mae": rf_result["mae"],
		"rf_r2": rf_result["r2"],
		"pca_mae": pca_result["mae"],
		"pca_r2": pca_result["r2"],
		"feature_importances": feature_importances,
		"correlations": correlations,
	}

	medians = df[FEATURES].median().to_dict()
	medians["part_time_job"] = float(df["part_time_job"].mode(dropna=True).iloc[0])
	return selected_bundle, metrics, medians


def clamp_score(value: float) -> float:
	return max(0.0, min(100.0, float(value)))


def performance_band(score: float) -> str:
	if score >= 90:
		return "Excellent"
	if score >= 75:
		return "Strong"
	if score >= 60:
		return "Moderate"
	return "Needs Attention"


def band_color(band: str) -> str:
	"""Return a color hex code for each performance band."""
	colors = {
		"Excellent": "#22c55e",
		"Strong": "#3b82f6",
		"Moderate": "#eab308",
		"Needs Attention": "#ef4444",
	}
	return colors.get(band, "#22c55e")


def predict_score(bundle: ModelBundle, values: dict[str, float]) -> tuple[float, float, float]:
	frame = pd.DataFrame([values], columns=FEATURES)
	raw_score = float(bundle.model.predict(frame)[0])
	calibrated_score = float(bundle.calibrator.predict([raw_score])[0])

	# Conservative adjustment to avoid optimistic overestimation on top-skewed score distributions.
	uncertainty_penalty = max(1.0, bundle.residual_std * 0.45)
	habit_penalty = 0.0
	if values["study_hours_per_day"] < 4.0:
		habit_penalty += 0.8
	if values["class_attendance_percent"] < 90.0:
		habit_penalty += 0.8
	if values["sleep_hours"] < 7.0:
		habit_penalty += 0.6
	if values["screen_time_hours"] > 5.0:
		habit_penalty += 0.6
	if values["mental_stress_level"] > 6.0:
		habit_penalty += 0.6
	if values["exam_preparation_days"] < 14.0:
		habit_penalty += 0.7

	strict_penalty = min(5.0, uncertainty_penalty + habit_penalty)
	point = clamp_score(calibrated_score - strict_penalty)

	# Keep the range slightly asymmetric to remain conservative on the upper side.
	margin = max(2.0, bundle.residual_std * 0.9)
	return point, clamp_score(point - margin * 1.1), clamp_score(point + margin * 0.6)


def predict_point_score(bundle: ModelBundle, values: dict[str, float]) -> float:
	return predict_score(bundle, values)[0]


def rule_based_advice(values: dict[str, float], medians: dict[str, float]) -> list[str]:
	advice: list[str] = []

	study_target = max(4.0, float(medians["study_hours_per_day"]))
	attendance_target = max(90.0, float(medians["class_attendance_percent"]))

	if values["study_hours_per_day"] < study_target:
		advice.append(
			f"Increase study time to at least {study_target:.1f} hours/day for stronger recall and revision."
		)

	if values["class_attendance_percent"] < attendance_target:
		advice.append(
			f"Raise attendance to {attendance_target:.0f}% or more so you do not miss lecture-based marks."
		)

	if values["sleep_hours"] < 7.0:
		advice.append("Aim for 7-8 hours of sleep. Better rest usually improves focus and memory.")

	if values["screen_time_hours"] > 4.0:
		advice.append("Reduce screen time below 4 hours/day to protect study focus and reduce fatigue.")

	if values["social_media_hours"] > 2.5:
		advice.append("Cut social media usage a little and use that time for revision or practice questions.")

	if values["gaming_hours"] > 1.5:
		advice.append("Keep gaming limited until after study goals are done for the day.")

	if values["exercise_hours_per_week"] < 3.0:
		advice.append("Add at least 3 hours of exercise per week to improve energy and stress control.")

	if values["mental_stress_level"] > 6.0:
		advice.append("Your stress level is high. Use a fixed timetable, short breaks, and daily review sessions.")

	if values["exam_preparation_days"] < 14.0:
		advice.append("Start exam preparation earlier. Two weeks or more gives better recall and less panic.")

	if values["coffee_consumption_per_day"] > 3.0:
		advice.append("Reduce coffee to avoid sleep disruption and last-minute energy crashes.")

	if values["part_time_job"] > 0.5 and values["study_hours_per_day"] < 5.0:
		advice.append("Balance part-time work carefully. Protect a fixed study block each day.")

	if values["GPA"] < 3.0:
		advice.append("Focus on core subjects and weekly revision cycles to raise your academic base.")

	if not advice:
		advice.append("Your habits already look balanced. Keep the same routine and revise consistently.")

	return advice


def ml_improvement_opportunities(
	bundle: ModelBundle, values: dict[str, float]
) -> list[tuple[float, str]]:
	baseline = predict_point_score(bundle, values)
	candidates = {
		"study_hours_per_day": min(values["study_hours_per_day"] + 1.5, 8.0),
		"class_attendance_percent": min(values["class_attendance_percent"] + 5.0, 100.0),
		"sleep_hours": max(values["sleep_hours"], 7.0),
		"screen_time_hours": min(values["screen_time_hours"], 3.0),
		"social_media_hours": min(values["social_media_hours"], 2.0),
		"gaming_hours": min(values["gaming_hours"], 1.0),
		"exercise_hours_per_week": max(values["exercise_hours_per_week"], 4.0),
		"mental_stress_level": min(values["mental_stress_level"], 4.0),
		"exam_preparation_days": max(values["exam_preparation_days"], 14.0),
		"coffee_consumption_per_day": min(values["coffee_consumption_per_day"], 2.0),
	}

	action_text = {
		"study_hours_per_day": "study 1.5 hours more per day",
		"class_attendance_percent": "attend more classes",
		"sleep_hours": "sleep at least 7 hours",
		"screen_time_hours": "cut screen time to about 3 hours/day",
		"social_media_hours": "reduce social media use",
		"gaming_hours": "limit gaming to 1 hour/day or less",
		"exercise_hours_per_week": "exercise more each week",
		"mental_stress_level": "lower stress with better planning",
		"exam_preparation_days": "start exam prep earlier",
		"coffee_consumption_per_day": "reduce coffee intake",
	}

	improvements: list[tuple[float, str]] = []
	for feature, target_value in candidates.items():
		if abs(target_value - values[feature]) < 1e-9:
			continue

		candidate = dict(values)
		candidate[feature] = target_value
		new_score = predict_point_score(bundle, candidate)
		gain = new_score - baseline
		if gain > 0.25:
			text = (
				f"If you {action_text[feature]}, the model predicts about {new_score:.1f}/100 "
				f"({gain:+.1f} points from your current profile)."
			)
			improvements.append((gain, text))

	improvements.sort(key=lambda item: item[0], reverse=True)
	return improvements[:5]


class CreateToolTip:
	"""Hover tooltip for any tkinter widget."""

	def __init__(self, widget, text):
		self.widget = widget
		self.text = text
		self.tooltip_window = None
		widget.bind("<Enter>", self._show)
		widget.bind("<Leave>", self._hide)

	def _show(self, event=None):
		if self.tooltip_window:
			return
		x = self.widget.winfo_rootx() + 20
		y = self.widget.winfo_rooty() + self.widget.winfo_height() + 5
		self.tooltip_window = tw = tk.Toplevel(self.widget)
		tw.wm_overrideredirect(True)
		tw.wm_geometry(f"+{x}+{y}")
		label = tk.Label(
			tw, text=self.text, justify="left",
			background="#1e293b", foreground="#e5eefc",
			relief="solid", borderwidth=1,
			font=("Segoe UI", 9), padx=8, pady=4,
			wraplength=280,
		)
		label.pack()

	def _hide(self, event=None):
		if self.tooltip_window:
			self.tooltip_window.destroy()
			self.tooltip_window = None


class PerformanceAdvisorApp:
	def __init__(self, root: tk.Tk, model_bundle: ModelBundle, metrics: dict[str, float], medians: dict[str, float]):
		self.root = root
		self.model_bundle = model_bundle
		self.metrics = metrics
		self.medians = medians
		self.current_theme = "dark"

		self.root.title(APP_TITLE)
		self.root.geometry("1280x820")
		self.root.minsize(1080, 680)
		self.root.configure(bg=THEMES["dark"]["bg"])

		self.style = ttk.Style()
		self.style.theme_use("clam")
		self._configure_styles()

		self.vars: dict[str, tk.StringVar] = {}
		self.part_time_var = tk.StringVar()
		self.target_score_var = tk.StringVar(value="95")
		self.checklist_vars: dict[str, tk.BooleanVar] = {}
		self.history_data: list[dict[str, object]] = []
		self.last_values: dict[str, float] = {}
		self.last_prediction: tuple[float, float, float] | None = None
		self.saved_profile: dict[str, float] | None = None  # For compare feature
		self._build_ui()
		self.reset_defaults()
		self.load_history()
		self.load_checklist_state()
		self.load_last_inputs()
		self.root.protocol("WM_DELETE_WINDOW", self.on_close)

	def _display_gpa_from_model(self, model_gpa: float) -> float:
		return max(0.0, min(10.0, model_gpa * 2.5))

	def _model_gpa_from_display(self, display_gpa: float) -> float:
		return max(0.0, min(4.0, display_gpa / 2.5))

	def _configure_styles(self):
		t = THEMES[self.current_theme]
		self.style.configure("App.TFrame", background=t["bg"])
		self.style.configure("Card.TFrame", background=t["card"])
		self.style.configure("App.TLabel", background=t["bg"], foreground=t["fg"], font=("Segoe UI", 11))
		self.style.configure(
			"Header.TLabel", background=t["bg"], foreground=t["accent"], font=("Segoe UI", 24, "bold")
		)
		self.style.configure(
			"SubHeader.TLabel", background=t["bg"], foreground=t["subtitle"], font=("Segoe UI", 11)
		)
		self.style.configure(
			"PanelTitle.TLabel", background=t["card"], foreground=t["panel_fg"], font=("Segoe UI", 13, "bold")
		)
		self.style.configure(
			"App.TLabelframe", background=t["card"], foreground=t["panel_fg"], borderwidth=1, relief="solid"
		)
		self.style.configure(
			"App.TLabelframe.Label", background=t["card"], foreground=t["panel_fg"], font=("Segoe UI", 10, "bold")
		)
		self.style.configure(
			"Accent.TButton",
			background=t["btn_accent"],
			foreground="white",
			padding=(14, 8),
			font=("Segoe UI", 10, "bold"),
		)
		self.style.map("Accent.TButton", background=[("active", t["btn_accent_active"])])
		self.style.configure(
			"Reset.TButton",
			background=t["btn_reset"],
			foreground="white",
			padding=(14, 8),
			font=("Segoe UI", 10, "bold"),
		)
		self.style.map("Reset.TButton", background=[("active", t["btn_reset_active"])])
		self.style.configure("App.TEntry", padding=5)
		self.style.configure("App.TCombobox", padding=5)
		self.style.configure("TNotebook", background=t["card"], borderwidth=0)
		self.style.configure("TNotebook.Tab", font=("Segoe UI", 11, "bold"), padding=(10, 6))
		self.style.map("TNotebook.Tab", background=[("selected", t["btn_accent"])], foreground=[("selected", "white")])
		self.style.configure("Treeview", font=("Segoe UI", 10), rowheight=24)
		self.style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))
		# Color-coded progress bar styles
		for bar_name, bar_color in [("Green", "#22c55e"), ("Blue", "#3b82f6"), ("Yellow", "#eab308"), ("Red", "#ef4444")]:
			self.style.configure(
				f"{bar_name}.Horizontal.TProgressbar",
				troughcolor=t["trough"],
				background=bar_color,
				bordercolor=t["trough"],
				lightcolor=bar_color,
				darkcolor=bar_color,
			)
		self.style.configure(
			"Accent.Horizontal.TProgressbar",
			troughcolor=t["trough"],
			background="#22c55e",
			bordercolor=t["trough"],
			lightcolor="#22c55e",
			darkcolor="#22c55e",
		)

	def _apply_theme(self, theme_name: str):
		"""Switch between dark and light themes."""
		self.current_theme = theme_name
		t = THEMES[theme_name]
		self.root.configure(bg=t["bg"])
		self._configure_styles()
		# Update text widgets
		if hasattr(self, "planner_text"):
			self.planner_text.configure(bg=t["text_bg"], fg=t["fg"], insertbackground=t["fg"])

	def toggle_theme(self):
		new_theme = "light" if self.current_theme == "dark" else "dark"
		self._apply_theme(new_theme)
		self.theme_btn.config(text="Dark Mode" if new_theme == "light" else "Light Mode")

	def _build_ui(self):
		main = ttk.Frame(self.root, style="App.TFrame")
		main.pack(fill=tk.BOTH, expand=True, padx=18, pady=18)

		header = ttk.Frame(main, style="App.TFrame")
		header.pack(fill=tk.X, pady=(0, 12))

		ttk.Label(header, text="Student Performance Advisor", style="Header.TLabel").pack(side=tk.LEFT, anchor="w")

		# Theme toggle + Export buttons in header
		header_buttons = ttk.Frame(header, style="App.TFrame")
		header_buttons.pack(side=tk.RIGHT)
		self.theme_btn = ttk.Button(header_buttons, text="Light Mode", style="Reset.TButton", command=self.toggle_theme)
		self.theme_btn.pack(side=tk.LEFT, padx=(0, 6))
		ttk.Button(header_buttons, text="Export Report", style="Reset.TButton", command=self.export_report).pack(side=tk.LEFT, padx=(0, 6))

		ttk.Label(
			main,
			text="Hybrid ML + rule-based advice from your student habits dataset",
			style="SubHeader.TLabel",
		).pack(anchor="w", pady=(0, 8))

		body = ttk.Frame(main, style="App.TFrame")
		body.pack(fill=tk.BOTH, expand=True)
		body.columnconfigure(0, weight=2)
		body.columnconfigure(1, weight=1)
		body.rowconfigure(0, weight=1)

		input_panel = ttk.Labelframe(body, text="Your Habits", style="App.TLabelframe", padding=12)
		input_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

		output_panel = ttk.Labelframe(body, text="Recommendations", style="App.TLabelframe", padding=12)
		output_panel.grid(row=0, column=1, sticky="nsew")

		self._build_form(input_panel)
		self._build_output(output_panel)

	def _build_form(self, parent: ttk.Labelframe):
		form = ttk.Frame(parent, style="Card.TFrame")
		form.pack(fill=tk.BOTH, expand=True)

		for column in range(4):
			form.columnconfigure(column, weight=1)

		for index, spec in enumerate(FIELD_SPECS):
			row = index // 2
			column = (index % 2) * 2

			label = ttk.Label(form, text=spec.label, style="PanelTitle.TLabel")
			label.grid(row=row * 2, column=column, sticky="w", padx=(0, 10), pady=(8, 2))

			# Add tooltip if available
			tooltip_text = FEATURE_TOOLTIPS.get(spec.key)
			if tooltip_text:
				CreateToolTip(label, tooltip_text)

			variable = tk.StringVar()
			self.vars[spec.key] = variable
			entry = tk.Spinbox(
				form,
				textvariable=variable,
				from_=spec.minimum,
				to=spec.maximum,
				increment=spec.step,
				font=("Segoe UI", 11),
				justify="center",
				width=12,
			)
			entry.grid(row=row * 2 + 1, column=column, sticky="ew", padx=(0, 10), pady=(0, 8))

			hint = ttk.Label(
				form,
				text=f"Range: {spec.minimum:g} to {spec.maximum:g}",
				style="App.TLabel",
				font=("Segoe UI", 8),
			)
			hint.grid(row=row * 2 + 1, column=column + 1, sticky="w", pady=(0, 8))

		part_time_label = ttk.Label(form, text="Part-Time Job", style="PanelTitle.TLabel")
		part_time_label.grid(row=14, column=0, sticky="w", pady=(8, 2))

		self.part_time_combo = ttk.Combobox(
			form,
			textvariable=self.part_time_var,
			values=["No", "Yes"],
			state="readonly",
			style="App.TCombobox",
			width=18,
		)
		self.part_time_combo.grid(row=15, column=0, sticky="ew", padx=(0, 10), pady=(0, 10))

		ttk.Label(
			form,
			text="Quick presets:",
			style="PanelTitle.TLabel",
		).grid(row=14, column=2, sticky="w", pady=(8, 2))

		presets = ttk.Frame(form, style="Card.TFrame")
		presets.grid(row=15, column=2, columnspan=2, sticky="w", pady=(0, 10))
		ttk.Button(presets, text="Focused", style="Reset.TButton", command=lambda: self.apply_preset("focused")).pack(side=tk.LEFT, padx=(0, 6))
		ttk.Button(presets, text="Balanced", style="Reset.TButton", command=lambda: self.apply_preset("balanced")).pack(side=tk.LEFT, padx=(0, 6))
		ttk.Button(presets, text="At Risk", style="Reset.TButton", command=lambda: self.apply_preset("risk")).pack(side=tk.LEFT)

		actions = ttk.Frame(form, style="Card.TFrame")
		actions.grid(row=16, column=0, columnspan=4, sticky="ew", pady=(10, 0))

		ttk.Button(actions, text="Analyze My Profile", style="Accent.TButton", command=self.analyze_profile).pack(
			side=tk.LEFT, padx=(0, 10)
		)
		ttk.Button(actions, text="Reset to Median", style="Reset.TButton", command=self.reset_defaults).pack(
			side=tk.LEFT, padx=(0, 10)
		)
		ttk.Button(actions, text="Save Profile", style="Reset.TButton", command=self.save_profile_to_file).pack(
			side=tk.LEFT, padx=(0, 10)
		)
		ttk.Button(actions, text="Load Profile", style="Reset.TButton", command=self.load_profile_from_file).pack(
			side=tk.LEFT, padx=(0, 10)
		)
		ttk.Button(actions, text="Compare", style="Reset.TButton", command=self.compare_profiles).pack(
			side=tk.LEFT
		)

	def _build_output(self, parent: ttk.Labelframe):
		self.score_var = tk.StringVar(value="Predicted Score: --")
		self.range_var = tk.StringVar(value="Likely Range: --")
		self.band_var = tk.StringVar(value="Performance Band: --")
		self.risk_var = tk.StringVar(value="Risk Alert: --")
		self.risk_detail_var = tk.StringVar(value="")
		self.metric_var = tk.StringVar(
			value=(
				f"Using {self.metrics['selected_model']} (auto-selected): R2 {self.metrics['r2']:.3f} | MAE {self.metrics['mae']:.2f}"
			)
		)
		self.comparison_var = tk.StringVar(
			value=(
				f"Model comparison -> RF MAE: {self.metrics['rf_mae']:.2f}, PCA MAE: {self.metrics['pca_mae']:.2f}"
			)
		)
		self.note_var = tk.StringVar(
			value=(
				f"Dataset note: {self.metrics['pct_perfect']:.1f}% scores are exactly 100, so estimates naturally skew high. "
				"Strict mode is active to keep predictions conservative."
			)
		)

		notebook = ttk.Notebook(parent)
		notebook.pack(fill=tk.BOTH, expand=True)

		overview_tab = ttk.Frame(notebook, style="Card.TFrame")
		planner_tab = ttk.Frame(notebook, style="Card.TFrame")
		tracker_tab = ttk.Frame(notebook, style="Card.TFrame")
		checklist_tab = ttk.Frame(notebook, style="Card.TFrame")
		charts_tab = ttk.Frame(notebook, style="Card.TFrame")
		importance_tab = ttk.Frame(notebook, style="Card.TFrame")
		heatmap_tab = ttk.Frame(notebook, style="Card.TFrame")

		notebook.add(overview_tab, text="Overview")
		notebook.add(planner_tab, text="Goal + Planner")
		notebook.add(tracker_tab, text="Progress")
		notebook.add(checklist_tab, text="Checklist")
		notebook.add(charts_tab, text="Charts")
		notebook.add(importance_tab, text="Importance")
		notebook.add(heatmap_tab, text="Heatmap")

		# --- Overview tab ---
		ttk.Label(overview_tab, textvariable=self.score_var, style="PanelTitle.TLabel").pack(anchor="w", pady=(8, 2), padx=8)
		ttk.Label(overview_tab, textvariable=self.range_var, style="App.TLabel").pack(anchor="w", padx=8)
		ttk.Label(overview_tab, textvariable=self.band_var, style="App.TLabel").pack(anchor="w", pady=(2, 2), padx=8)
		ttk.Label(overview_tab, textvariable=self.risk_var, style="PanelTitle.TLabel").pack(anchor="w", pady=(8, 2), padx=8)
		ttk.Label(overview_tab, textvariable=self.risk_detail_var, style="App.TLabel", wraplength=360).pack(anchor="w", pady=(0, 8), padx=8)
		ttk.Label(overview_tab, textvariable=self.metric_var, style="App.TLabel", wraplength=360).pack(anchor="w", pady=(0, 6), padx=8)
		ttk.Label(overview_tab, textvariable=self.comparison_var, style="App.TLabel", wraplength=360).pack(anchor="w", pady=(0, 6), padx=8)
		ttk.Label(overview_tab, textvariable=self.note_var, style="App.TLabel", wraplength=360).pack(anchor="w", pady=(0, 10), padx=8)

		self.score_bar = ttk.Progressbar(overview_tab, maximum=100, value=0, style="Green.Horizontal.TProgressbar")
		self.score_bar.pack(fill=tk.X, pady=(0, 8), padx=8)

		# --- Planner tab ---
		goal_row = ttk.Frame(planner_tab, style="Card.TFrame")
		goal_row.pack(fill=tk.X, padx=8, pady=(8, 6))
		ttk.Label(goal_row, text="Goal Score", style="PanelTitle.TLabel").pack(side=tk.LEFT)
		tk.Spinbox(goal_row, textvariable=self.target_score_var, from_=0, to=100, increment=1, width=6, justify="center", font=("Segoe UI", 11)).pack(side=tk.LEFT, padx=6)
		ttk.Button(goal_row, text="Suggest Goal Plan", style="Accent.TButton", command=self.suggest_goal_plan).pack(side=tk.LEFT, padx=(6, 0))
		ttk.Button(goal_row, text="Build Weekly Plan", style="Reset.TButton", command=self.build_weekly_plan).pack(side=tk.LEFT, padx=(6, 0))

		planner_frame = ttk.Frame(planner_tab, style="Card.TFrame")
		planner_frame.pack(fill=tk.BOTH, expand=True, padx=8, pady=(0, 8))
		self.planner_text = tk.Text(
			planner_frame,
			wrap="word",
			height=22,
			bg="#0b1220",
			fg="#e5eefc",
			font=("Segoe UI", 12),
			insertbackground="#e5eefc",
			relief="flat",
			padx=10,
			pady=10,
		)
		planner_scroll = ttk.Scrollbar(planner_frame, orient="vertical", command=self.planner_text.yview)
		self.planner_text.configure(yscrollcommand=planner_scroll.set)
		self.planner_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
		planner_scroll.pack(side=tk.RIGHT, fill=tk.Y)

		# --- Tracker tab with Clear History button ---
		tracker_top = ttk.Frame(tracker_tab, style="Card.TFrame")
		tracker_top.pack(fill=tk.X, padx=8, pady=(8, 4))
		ttk.Button(tracker_top, text="Clear History", style="Reset.TButton", command=self.clear_history).pack(side=tk.RIGHT)

		tracker_frame = ttk.Frame(tracker_tab, style="Card.TFrame")
		tracker_frame.pack(fill=tk.BOTH, expand=True, padx=8, pady=(0, 8))
		self.tracker_tree = ttk.Treeview(tracker_frame, columns=("time", "score", "range", "band"), show="headings", height=14)
		self.tracker_tree.heading("time", text="Timestamp")
		self.tracker_tree.heading("score", text="Score")
		self.tracker_tree.heading("range", text="Range")
		self.tracker_tree.heading("band", text="Band")
		self.tracker_tree.column("time", width=130, anchor="center")
		self.tracker_tree.column("score", width=80, anchor="center")
		self.tracker_tree.column("range", width=120, anchor="center")
		self.tracker_tree.column("band", width=100, anchor="center")
		tracker_scroll = ttk.Scrollbar(tracker_frame, orient="vertical", command=self.tracker_tree.yview)
		self.tracker_tree.configure(yscrollcommand=tracker_scroll.set)
		self.tracker_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
		tracker_scroll.pack(side=tk.RIGHT, fill=tk.Y)

		# --- Checklist tab ---
		checklist_frame = ttk.Frame(checklist_tab, style="Card.TFrame")
		checklist_frame.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)
		for task in CHECKLIST_TASKS:
			var = tk.BooleanVar(value=False)
			self.checklist_vars[task] = var
			cb = ttk.Checkbutton(checklist_frame, text=task, variable=var, command=self.save_checklist_state)
			cb.pack(anchor="w", pady=4)

		ttk.Button(checklist_frame, text="Save Checklist", style="Reset.TButton", command=self.save_checklist_state).pack(anchor="w", pady=(10, 0))

		# --- Charts tab ---
		charts_frame = ttk.Frame(charts_tab, style="Card.TFrame")
		charts_frame.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)
		self.chart_figure = Figure(figsize=(5, 4), dpi=100)
		self.chart_canvas = FigureCanvasTkAgg(self.chart_figure, master=charts_frame)
		self.chart_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

		# --- Feature Importance tab ---
		importance_frame = ttk.Frame(importance_tab, style="Card.TFrame")
		importance_frame.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)
		self.importance_figure = Figure(figsize=(5, 4), dpi=100)
		self.importance_canvas = FigureCanvasTkAgg(self.importance_figure, master=importance_frame)
		self.importance_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
		self._draw_feature_importance()

		# --- Correlation Heatmap tab ---
		heatmap_frame = ttk.Frame(heatmap_tab, style="Card.TFrame")
		heatmap_frame.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)
		self.heatmap_figure = Figure(figsize=(5, 4), dpi=100)
		self.heatmap_canvas = FigureCanvasTkAgg(self.heatmap_figure, master=heatmap_frame)
		self.heatmap_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
		self._draw_correlation_heatmap()

		self.output_text = None
		self._set_output_text("Use Goal + Planner tab to generate a weekly plan and a goal-reaching strategy.")

	# --- Feature Importance Chart ---
	def _draw_feature_importance(self):
		importances = self.metrics.get("feature_importances", {})
		if not importances:
			return
		self.importance_figure.clear()
		ax = self.importance_figure.add_subplot(111)
		sorted_features = sorted(importances.items(), key=lambda x: x[1], reverse=True)
		names = [f.replace("_", " ").title() for f, _ in sorted_features]
		values = [v for _, v in sorted_features]
		colors = ["#22c55e" if v > 0.08 else "#3b82f6" if v > 0.04 else "#64748b" for v in values]

		bars = ax.barh(range(len(names)), values, color=colors)
		ax.set_yticks(range(len(names)))
		ax.set_yticklabels(names, fontsize=8)
		ax.invert_yaxis()
		ax.set_xlabel("Importance", fontsize=9)
		ax.set_title("Random Forest Feature Importance", fontsize=11, fontweight="bold")

		for bar, val in zip(bars, values):
			ax.text(bar.get_width() + 0.002, bar.get_y() + bar.get_height() / 2,
			        f"{val:.3f}", va="center", fontsize=7)

		self.importance_figure.tight_layout()
		self.importance_canvas.draw_idle()

	# --- Correlation Heatmap ---
	def _draw_correlation_heatmap(self):
		correlations = self.metrics.get("correlations", {})
		if not correlations:
			return
		self.heatmap_figure.clear()
		ax = self.heatmap_figure.add_subplot(111)

		sorted_corr = sorted(correlations.items(), key=lambda x: abs(x[1]), reverse=True)
		names = [f.replace("_", " ").title() for f, _ in sorted_corr]
		values = [v for _, v in sorted_corr]
		colors = ["#22c55e" if v > 0 else "#ef4444" for v in values]

		bars = ax.barh(range(len(names)), values, color=colors)
		ax.set_yticks(range(len(names)))
		ax.set_yticklabels(names, fontsize=8)
		ax.invert_yaxis()
		ax.axvline(x=0, color="#64748b", linewidth=0.8)
		ax.set_xlabel("Correlation with Final Exam Score", fontsize=9)
		ax.set_title("Feature Correlation with Score", fontsize=11, fontweight="bold")

		for bar, val in zip(bars, values):
			offset = 0.01 if val >= 0 else -0.04
			ax.text(bar.get_width() + offset, bar.get_y() + bar.get_height() / 2,
			        f"{val:.3f}", va="center", fontsize=7)

		self.heatmap_figure.tight_layout()
		self.heatmap_canvas.draw_idle()

	# --- Score bar color coding ---
	def _update_score_bar_color(self, score: float):
		band = performance_band(score)
		style_map = {
			"Excellent": "Green.Horizontal.TProgressbar",
			"Strong": "Blue.Horizontal.TProgressbar",
			"Moderate": "Yellow.Horizontal.TProgressbar",
			"Needs Attention": "Red.Horizontal.TProgressbar",
		}
		self.score_bar.configure(style=style_map.get(band, "Green.Horizontal.TProgressbar"))
		self.score_bar["value"] = score

	# --- Export Report ---
	def export_report(self):
		if not self.last_values:
			messagebox.showinfo("Export", "Please analyze a profile first before exporting.")
			return

		filepath = filedialog.asksaveasfilename(
			defaultextension=".txt",
			filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
			title="Export Report",
			initialfile=f"advisor_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
		)
		if not filepath:
			return

		values = self.last_values
		predicted, low, high = self.last_prediction if self.last_prediction else (0, 0, 0)
		band = performance_band(predicted)
		rule_advice = rule_based_advice(values, self.medians)
		ml_advice = ml_improvement_opportunities(self.model_bundle, values)
		risk_title, risk_detail = self.compute_risk_alert(values)

		lines = [
			"=" * 60,
			"  STUDENT PERFORMANCE ADVISOR - ANALYSIS REPORT",
			"=" * 60,
			f"  Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
			f"  Model: {self.metrics['selected_model']}",
			f"  R2: {self.metrics['r2']:.3f} | MAE: {self.metrics['mae']:.2f}",
			"",
			"-" * 60,
			"  YOUR INPUTS",
			"-" * 60,
		]
		for spec in FIELD_SPECS:
			display_val = values.get(spec.key, 0)
			if spec.key == "GPA":
				display_val = self._display_gpa_from_model(display_val)
			lines.append(f"  {spec.label:<30}: {display_val:.2f}")
		lines.append(f"  {'Part-Time Job':<30}: {'Yes' if values.get('part_time_job', 0) > 0.5 else 'No'}")

		lines.extend([
			"",
			"-" * 60,
			"  PREDICTION RESULTS",
			"-" * 60,
			f"  Predicted Score     : {predicted:.1f} / 100",
			f"  Likely Range        : {low:.1f} to {high:.1f}",
			f"  Performance Band    : {band}",
			f"  {risk_title}",
			f"  {risk_detail}",
			"",
			"-" * 60,
			"  RULE-BASED ADVICE",
			"-" * 60,
		])
		for item in rule_advice:
			lines.append(f"  - {item}")

		lines.extend([
			"",
			"-" * 60,
			"  ML WHAT-IF SUGGESTIONS",
			"-" * 60,
		])
		if ml_advice:
			for i, (_, suggestion) in enumerate(ml_advice, 1):
				lines.append(f"  {i}. {suggestion}")
		else:
			lines.append("  Your profile is already close to the dataset's stronger patterns.")

		lines.extend(["", "=" * 60])

		try:
			Path(filepath).write_text("\n".join(lines), encoding="utf-8")
			messagebox.showinfo("Export", f"Report saved to:\n{filepath}")
		except OSError as e:
			messagebox.showerror("Export Error", f"Could not save report:\n{e}")

	# --- Profile Save/Load ---
	def save_profile_to_file(self):
		values = self._collect_inputs()
		if values is None:
			return
		PROFILES_DIR.mkdir(parents=True, exist_ok=True)
		filepath = filedialog.asksaveasfilename(
			defaultextension=".json",
			filetypes=[("JSON files", "*.json")],
			title="Save Profile",
			initialdir=str(PROFILES_DIR),
			initialfile=f"profile_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
		)
		if not filepath:
			return
		try:
			# Store display values for easy reload
			payload = {}
			for spec in FIELD_SPECS:
				payload[spec.key] = float(self.vars[spec.key].get())
			payload["part_time_job"] = self.part_time_var.get()
			Path(filepath).write_text(json.dumps(payload, indent=2), encoding="utf-8")
			messagebox.showinfo("Profile", f"Profile saved to:\n{filepath}")
		except OSError as e:
			messagebox.showerror("Error", f"Could not save profile:\n{e}")

	def load_profile_from_file(self):
		filepath = filedialog.askopenfilename(
			filetypes=[("JSON files", "*.json")],
			title="Load Profile",
			initialdir=str(PROFILES_DIR) if PROFILES_DIR.exists() else str(Path(__file__).parent),
		)
		if not filepath:
			return
		try:
			data = json.loads(Path(filepath).read_text(encoding="utf-8"))
		except (OSError, json.JSONDecodeError) as e:
			messagebox.showerror("Error", f"Could not load profile:\n{e}")
			return

		for spec in FIELD_SPECS:
			val = data.get(spec.key)
			if val is not None:
				try:
					self.vars[spec.key].set(self._format_default(float(val), spec))
				except (TypeError, ValueError):
					pass
		pt = data.get("part_time_job")
		if pt in {"Yes", "No"}:
			self.part_time_var.set(pt)
		messagebox.showinfo("Profile", "Profile loaded successfully!")

	# --- Compare Profiles ---
	def compare_profiles(self):
		current = self._collect_inputs()
		if current is None:
			return

		if self.saved_profile is None:
			# Save current as baseline
			self.saved_profile = dict(current)
			messagebox.showinfo("Compare", "Current profile saved as baseline.\n\nNow change your habits and click Compare again to see the difference.")
			return

		# Compare saved vs current
		saved = self.saved_profile
		score_saved = predict_point_score(self.model_bundle, saved)
		score_current = predict_point_score(self.model_bundle, current)
		diff = score_current - score_saved

		lines = [
			"Profile Comparison",
			"",
			f"Baseline predicted score: {score_saved:.1f}",
			f"Current predicted score:  {score_current:.1f}",
			f"Difference:              {diff:+.1f} points",
			"",
			"Changes made:",
		]

		for spec in FIELD_SPECS:
			old_val = saved.get(spec.key, 0)
			new_val = current.get(spec.key, 0)
			if abs(old_val - new_val) > 1e-6:
				if spec.key == "GPA":
					old_display = self._display_gpa_from_model(old_val)
					new_display = self._display_gpa_from_model(new_val)
				else:
					old_display = old_val
					new_display = new_val
				change = new_display - old_display
				lines.append(f"  {spec.label}: {old_display:.1f} -> {new_display:.1f} ({change:+.1f})")

		if diff > 0:
			lines.append(f"\nYour changes would improve your score by {diff:.1f} points!")
		elif diff < 0:
			lines.append(f"\nWarning: Your changes would lower your score by {abs(diff):.1f} points.")
		else:
			lines.append("\nNo significant change in predicted score.")

		lines.append("\n(Click Compare again to set a new baseline)")
		self.saved_profile = None  # Reset for next comparison
		self._set_output_text("\n".join(lines))

	# --- Clear History ---
	def clear_history(self):
		if not self.history_data:
			messagebox.showinfo("History", "History is already empty.")
			return
		if messagebox.askyesno("Clear History", "Are you sure you want to clear all prediction history?"):
			self.history_data = []
			self._save_json(HISTORY_FILE, self.history_data)
			self.refresh_tracker()
			self.update_charts(None)
			messagebox.showinfo("History", "History cleared.")

	def reset_defaults(self):
		for spec in FIELD_SPECS:
			default_value = self.medians.get(spec.key, spec.default)
			if spec.key == "GPA":
				default_value = self._display_gpa_from_model(float(default_value))
			if spec.key == "university_year":
				default_value = round(default_value)
			self.vars[spec.key].set(self._format_default(default_value, spec))

		self.part_time_var.set("Yes" if self.medians.get("part_time_job", 0.0) >= 0.5 else "No")
		self.target_score_var.set("95")
		self._set_output_text(
			"Use Goal + Planner tab to generate a weekly plan and a goal-reaching strategy."
		)
		self.score_var.set("Predicted Score: --")
		self.range_var.set("Likely Range: --")
		self.band_var.set("Performance Band: --")
		self.risk_var.set("Risk Alert: --")
		self.risk_detail_var.set("")
		self.score_bar["value"] = 0
		self.update_charts(None)

	def apply_preset(self, preset_name: str):
		presets = {
			"focused": {
				"GPA": 9.25,
				"university_year": 2,
				"study_hours_per_day": 6.0,
				"class_attendance_percent": 97.0,
				"sleep_hours": 7.5,
				"screen_time_hours": 2.5,
				"social_media_hours": 1.2,
				"gaming_hours": 0.4,
				"exercise_hours_per_week": 4.0,
				"mental_stress_level": 3.8,
				"AI_tool_usage_hours": 1.3,
				"exam_preparation_days": 20.0,
				"coffee_consumption_per_day": 1.2,
				"part_time_job": "No",
			},
			"balanced": {
				"GPA": 8.25,
				"university_year": 2,
				"study_hours_per_day": 4.3,
				"class_attendance_percent": 91.0,
				"sleep_hours": 7.0,
				"screen_time_hours": 3.8,
				"social_media_hours": 2.1,
				"gaming_hours": 1.0,
				"exercise_hours_per_week": 3.0,
				"mental_stress_level": 4.8,
				"AI_tool_usage_hours": 1.0,
				"exam_preparation_days": 14.0,
				"coffee_consumption_per_day": 2.0,
				"part_time_job": "No",
			},
			"risk": {
				"GPA": 6.75,
				"university_year": 2,
				"study_hours_per_day": 2.5,
				"class_attendance_percent": 78.0,
				"sleep_hours": 5.8,
				"screen_time_hours": 7.0,
				"social_media_hours": 4.0,
				"gaming_hours": 3.0,
				"exercise_hours_per_week": 1.0,
				"mental_stress_level": 7.5,
				"AI_tool_usage_hours": 0.4,
				"exam_preparation_days": 6.0,
				"coffee_consumption_per_day": 4.0,
				"part_time_job": "Yes",
			},
		}

		preset = presets.get(preset_name)
		if preset is None:
			return

		for spec in FIELD_SPECS:
			self.vars[spec.key].set(self._format_default(float(preset[spec.key]), spec))
		self.part_time_var.set(str(preset["part_time_job"]))
		self.save_last_inputs()

	def load_last_inputs(self) -> None:
		path = LAST_INPUTS_FILE if LAST_INPUTS_FILE.exists() else LEGACY_LAST_INPUTS_FILE
		if not path.exists():
			return

		try:
			data = json.loads(path.read_text(encoding="utf-8"))
		except (OSError, json.JSONDecodeError):
			return

		if not isinstance(data, dict):
			return

		for spec in FIELD_SPECS:
			value = data.get(spec.key)
			if value is None:
				continue
			try:
				numeric_value = float(value)
			except (TypeError, ValueError):
				continue
			if spec.minimum <= numeric_value <= spec.maximum:
				# Backward compatibility with older saves where GPA was stored on 0-4 scale.
				if spec.key == "GPA" and numeric_value <= 4.0:
					numeric_value = self._display_gpa_from_model(numeric_value)
				self.vars[spec.key].set(self._format_default(numeric_value, spec))

		part_time = data.get("part_time_job")
		if part_time in {"Yes", "No"}:
			self.part_time_var.set(part_time)

		target_score = data.get("target_score")
		if target_score is not None:
			try:
				target_value = float(target_score)
			except (TypeError, ValueError):
				target_value = None
			if target_value is not None and 0 <= target_value <= 100:
				self.target_score_var.set(str(int(round(target_value))))

	def save_last_inputs(self) -> None:
		payload: dict[str, float | str] = {}

		for spec in FIELD_SPECS:
			raw_value = self.vars[spec.key].get().strip()
			if not raw_value:
				continue
			try:
				numeric_value = float(raw_value)
			except ValueError:
				continue
			if spec.minimum <= numeric_value <= spec.maximum:
				payload[spec.key] = numeric_value

		if self.part_time_var.get() in {"Yes", "No"}:
			payload["part_time_job"] = self.part_time_var.get()

		try:
			target_value = float(self.target_score_var.get())
		except ValueError:
			target_value = None
		if target_value is not None and 0 <= target_value <= 100:
			payload["target_score"] = target_value

		if not payload:
			return

		try:
			APP_DATA_DIR.mkdir(parents=True, exist_ok=True)
			LAST_INPUTS_FILE.write_text(json.dumps(payload, indent=2), encoding="utf-8")
		except OSError:
			# Failing to save should not break prediction flow.
			return

	def on_close(self) -> None:
		self.save_last_inputs()
		self.save_checklist_state()
		self.root.destroy()

	def _load_json(self, path: Path, default: object) -> object:
		if not path.exists():
			return default
		try:
			return json.loads(path.read_text(encoding="utf-8"))
		except (OSError, json.JSONDecodeError):
			return default

	def _save_json(self, path: Path, payload: object) -> None:
		try:
			APP_DATA_DIR.mkdir(parents=True, exist_ok=True)
			path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
		except OSError:
			return

	def load_history(self) -> None:
		path = HISTORY_FILE if HISTORY_FILE.exists() else LEGACY_HISTORY_FILE
		loaded = self._load_json(path, [])
		if isinstance(loaded, list):
			self.history_data = [item for item in loaded if isinstance(item, dict)]
		else:
			self.history_data = []
		self.refresh_tracker()
		self.update_charts(self.last_values if self.last_values else None)

	def add_history_entry(self, score: float, low: float, high: float, band: str, values: dict[str, float] | None = None) -> None:
		entry = {
			"timestamp": datetime.now().strftime("%d/%m %H:%M"),
			"score": round(score, 1),
			"low": round(low, 1),
			"high": round(high, 1),
			"band": band,
		}
		# Store input values with each history entry for reference
		if values:
			entry["inputs"] = {k: round(v, 2) for k, v in values.items()}
		self.history_data.append(entry)
		self.history_data = self.history_data[-100:]
		self._save_json(HISTORY_FILE, self.history_data)
		self.refresh_tracker()

	def refresh_tracker(self) -> None:
		if not hasattr(self, "tracker_tree"):
			return
		for item in self.tracker_tree.get_children():
			self.tracker_tree.delete(item)
		for entry in reversed(self.history_data[-30:]):
			self.tracker_tree.insert(
				"",
				tk.END,
				values=(
					entry.get("timestamp", "-"),
					entry.get("score", "-"),
					f"{entry.get('low', '-')}-{entry.get('high', '-')}",
					entry.get("band", "-"),
				),
			)

	def load_checklist_state(self) -> None:
		path = CHECKLIST_FILE if CHECKLIST_FILE.exists() else LEGACY_CHECKLIST_FILE
		loaded = self._load_json(path, {})
		if not isinstance(loaded, dict):
			return
		for task, var in self.checklist_vars.items():
			var.set(bool(loaded.get(task, False)))

	def save_checklist_state(self) -> None:
		payload = {task: var.get() for task, var in self.checklist_vars.items()}
		self._save_json(CHECKLIST_FILE, payload)

	def compute_risk_alert(self, values: dict[str, float]) -> tuple[str, str]:
		risk_points = 0
		reasons: list[str] = []
		if values["study_hours_per_day"] < 3.0:
			risk_points += 1
			reasons.append("low study hours")
		if values["class_attendance_percent"] < 85.0:
			risk_points += 1
			reasons.append("attendance below 85%")
		if values["sleep_hours"] < 6.0:
			risk_points += 1
			reasons.append("sleep below 6h")
		if values["mental_stress_level"] > 7.0:
			risk_points += 1
			reasons.append("high stress")
		if values["screen_time_hours"] > 6.0:
			risk_points += 1
			reasons.append("excess screen time")
		if values["exam_preparation_days"] < 10.0:
			risk_points += 1
			reasons.append("late exam prep")

		if risk_points >= 4:
			return "Risk Alert: HIGH", "Immediate action needed: " + ", ".join(reasons) + "."
		if risk_points >= 2:
			return "Risk Alert: MODERATE", "Watch these areas: " + ", ".join(reasons) + "."
		return "Risk Alert: LOW", "Current profile looks stable. Keep consistency in core habits."

	def build_weekly_plan(self) -> None:
		values = self._collect_inputs()
		if values is None:
			return
		advice = rule_based_advice(values, self.medians)
		study_goal = max(4.0, values["study_hours_per_day"])
		sleep_goal = max(7.0, values["sleep_hours"])
		screen_goal = min(4.0, values["screen_time_hours"])
		lines = [
			"Weekly Study Planner",
			"",
			f"Daily baseline goals: Study {study_goal:.1f}h, Sleep {sleep_goal:.1f}h, Screen <= {screen_goal:.1f}h",
			"",
			"Monday: Core subject revision + 20 min recap at night.",
			"Tuesday: Practice questions (timed) + attendance focus.",
			"Wednesday: Weak-topic repair day + summary notes.",
			"Thursday: Mock test (45-60 mins) + error review.",
			"Friday: Assignment and concept consolidation.",
			"Saturday: Long revision block + stress reset (walk/exercise).",
			"Sunday: Weekly review, set targets for next week, light rest.",
			"",
			"Priority habits this week:",
		]
		for item in advice[:4]:
			lines.append(f"- {item}")
		self._set_output_text("\n".join(lines))

	def suggest_goal_plan(self) -> None:
		values = self._collect_inputs()
		if values is None:
			return
		try:
			target = float(self.target_score_var.get())
		except ValueError:
			messagebox.showerror("Input Error", "Goal score must be a number between 0 and 100.")
			return
		if target < 0 or target > 100:
			messagebox.showerror("Input Error", "Goal score must be between 0 and 100.")
			return

		current = dict(values)
		base = predict_point_score(self.model_bundle, current)
		if base >= target:
			self._set_output_text(
				f"Goal already achieved. Current predicted score is {base:.1f}, target is {target:.1f}."
			)
			return

		steps: list[str] = []
		used_features: set[str] = set()
		action_catalog = [
			("study_hours_per_day", [0.5, 1.0, 1.5], 0.0, 12.0, "Increase study hours/day"),
			("class_attendance_percent", [2.0, 4.0, 6.0], 0.0, 100.0, "Improve attendance"),
			("sleep_hours", [0.5, 1.0, 1.5], 0.0, 12.0, "Increase sleep hours"),
			("exam_preparation_days", [2.0, 4.0, 6.0], 0.0, 60.0, "Start exam prep earlier"),
			("exercise_hours_per_week", [0.5, 1.0, 2.0], 0.0, 30.0, "Increase weekly exercise"),
			("screen_time_hours", [-0.5, -1.0, -1.5], 0.0, 16.0, "Reduce screen time"),
			("social_media_hours", [-0.5, -1.0, -1.5], 0.0, 16.0, "Reduce social media"),
			("gaming_hours", [-0.5, -1.0, -1.5], 0.0, 16.0, "Reduce gaming time"),
			("mental_stress_level", [-0.5, -1.0, -1.5], 0.0, 10.0, "Lower stress level"),
		]
		for _ in range(6):
			if predict_point_score(self.model_bundle, current) >= target:
				break
			candidates = []
			for feature, deltas, minimum, maximum, display_name in action_catalog:
				if feature in used_features:
					continue
				best_for_feature = None
				for delta in deltas:
					trial = dict(current)
					trial_value = max(minimum, min(maximum, trial[feature] + delta))
					if abs(trial_value - trial[feature]) < 1e-9:
						continue
					trial[feature] = trial_value
					gain = predict_point_score(self.model_bundle, trial) - predict_point_score(self.model_bundle, current)
					if gain > 0.05:
						candidate = (gain, feature, trial_value, trial, display_name)
						if best_for_feature is None or gain > best_for_feature[0]:
							best_for_feature = candidate
				if best_for_feature is not None:
					candidates.append(best_for_feature)

			if not candidates:
				break
			candidates.sort(key=lambda item: item[0], reverse=True)
			best_gain, best_feature, best_value, best_trial, display_name = candidates[0]
			current = best_trial
			used_features.add(best_feature)
			steps.append(f"- {display_name} to {best_value:.1f} (about +{best_gain:.2f} predicted points)")

		final_score = predict_point_score(self.model_bundle, current)
		lines = [
			"Goal Mode Plan",
			"",
			f"Current predicted score: {base:.1f}",
			f"Target score: {target:.1f}",
			f"Projected score after plan: {final_score:.1f}",
			"",
			"Recommended step-by-step changes:",
		]
		if steps:
			lines.extend(steps)
		else:
			lines.append("- No strong single-step improvements found. Try broad routine changes.")
		self._set_output_text("\n".join(lines))

	def update_charts(self, values: dict[str, float] | None) -> None:
		if not hasattr(self, "chart_figure"):
			return
		self.chart_figure.clear()
		ax1 = self.chart_figure.add_subplot(211)
		ax2 = self.chart_figure.add_subplot(212)

		metrics_for_chart = [
			"study_hours_per_day",
			"class_attendance_percent",
			"sleep_hours",
			"screen_time_hours",
			"mental_stress_level",
			"exam_preparation_days",
		]
		labels = [m.replace("_", " ").title() for m in metrics_for_chart]
		current_values = []
		median_values = []
		for key in metrics_for_chart:
			spec = next((s for s in FIELD_SPECS if s.key == key), None)
			if spec is None:
				continue
			mid = float(self.medians.get(key, spec.default))
			cur = float(values.get(key, mid)) if values is not None else mid
			scale = spec.maximum - spec.minimum
			if scale <= 0:
				scale = 1.0
			current_values.append((cur - spec.minimum) / scale * 100)
			median_values.append((mid - spec.minimum) / scale * 100)

		positions = list(range(len(current_values)))
		ax1.bar([p - 0.2 for p in positions], median_values, width=0.4, label="Dataset Median", color="#334155")
		ax1.bar([p + 0.2 for p in positions], current_values, width=0.4, label="Your Profile", color="#22c55e")
		ax1.set_title("Habit Position vs Dataset (normalized %)", fontsize=9)
		ax1.set_xticks(positions)
		ax1.set_xticklabels(labels, rotation=20, ha="right", fontsize=7)
		ax1.set_ylim(0, 100)
		ax1.legend(fontsize=7)

		history_scores = [float(item.get("score", 0.0)) for item in self.history_data[-12:]]
		if history_scores:
			ax2.plot(range(1, len(history_scores) + 1), history_scores, marker="o", color="#38bdf8")
			ax2.set_ylim(0, 100)
			ax2.set_title("Recent Predicted Scores", fontsize=9)
			ax2.set_xlabel("Run", fontsize=8)
			ax2.set_ylabel("Score", fontsize=8)
		else:
			ax2.text(0.5, 0.5, "No progress data yet", ha="center", va="center", transform=ax2.transAxes)
			ax2.set_axis_off()

		self.chart_figure.tight_layout()
		self.chart_canvas.draw_idle()

	def _format_default(self, value: float, spec: FieldSpec) -> str:
		if spec.step >= 1:
			return str(int(round(value)))
		return f"{value:.2f}".rstrip("0").rstrip(".")

	def _collect_inputs(self) -> dict[str, float] | None:
		values: dict[str, float] = {}

		for spec in FIELD_SPECS:
			raw_value = self.vars[spec.key].get().strip()
			if not raw_value:
				messagebox.showerror("Input Error", f"Please enter a value for {spec.label}.")
				return None

			try:
				parsed_value = float(raw_value)
			except ValueError:
				messagebox.showerror("Input Error", f"{spec.label} must be a number.")
				return None

			if parsed_value < spec.minimum or parsed_value > spec.maximum:
				messagebox.showerror(
					"Input Error",
					f"{spec.label} must be between {spec.minimum:g} and {spec.maximum:g}.",
				)
				return None

			if spec.key == "university_year":
				parsed_value = round(parsed_value)
			if spec.key == "GPA":
				parsed_value = self._model_gpa_from_display(parsed_value)

			values[spec.key] = parsed_value

		values["part_time_job"] = 1.0 if self.part_time_var.get() == "Yes" else 0.0
		return values

	def analyze_profile(self):
		values = self._collect_inputs()
		if values is None:
			return
		self.save_last_inputs()
		self.last_values = dict(values)

		predicted_score, low_score, high_score = predict_score(self.model_bundle, values)
		self.last_prediction = (predicted_score, low_score, high_score)
		band = performance_band(predicted_score)
		rule_advice = rule_based_advice(values, self.medians)
		ml_advice = ml_improvement_opportunities(self.model_bundle, values)
		risk_title, risk_detail = self.compute_risk_alert(values)

		self.score_var.set(f"Predicted Score: {predicted_score:.1f} / 100")
		self.range_var.set(f"Likely Range: {low_score:.1f} to {high_score:.1f}")
		self.band_var.set(f"Performance Band: {band}")
		self.risk_var.set(risk_title)
		self.risk_detail_var.set(risk_detail)
		self._update_score_bar_color(predicted_score)
		self.add_history_entry(predicted_score, low_score, high_score, band, values)
		self.update_charts(values)

		lines = [
			f"Model trained on {self.metrics['rows']:,} student records.",
			f"Auto-selected predictor: {self.metrics['selected_model']}.",
			f"RF (calibrated): R2 {self.metrics['rf_r2']:.3f} | MAE {self.metrics['rf_mae']:.2f}.",
			f"PCA + Linear (calibrated): R2 {self.metrics['pca_r2']:.3f} | MAE {self.metrics['pca_mae']:.2f}.",
			f"Held-out calibrated accuracy: R2 {self.metrics['r2']:.3f} | MAE {self.metrics['mae']:.2f} points.",
			f"Raw model accuracy (before calibration): R2 {self.metrics['r2_raw']:.3f} | MAE {self.metrics['mae_raw']:.2f} points.",
			f"Estimated likely score range for your profile: {low_score:.1f} to {high_score:.1f}.",
			f"Dataset is top-skewed: {self.metrics['pct_perfect']:.1f}% final exam scores are exactly 100.",
			"",
			"Rule-based advice:",
		]
		for item in rule_advice:
			lines.append(f"- {item}")

		lines.append("")
		lines.append("ML-based what-if suggestions:")
		if ml_advice:
			for index, (_, suggestion) in enumerate(ml_advice, start=1):
				lines.append(f"{index}. {suggestion}")
		else:
			lines.append("- Your current profile is already close to the dataset's stronger patterns.")

		lines.append("")
		lines.append("Fast focus plan:")
		top_two_rules = rule_advice[:2]
		if top_two_rules:
			for item in top_two_rules:
				lines.append(f"- {item}")
		else:
			lines.append("- Keep your routine steady and continue regular revision.")

		self._set_output_text("\n".join(lines))

	def _set_output_text(self, text: str):
		if hasattr(self, "planner_text") and self.planner_text is not None:
			self.planner_text.config(state="normal")
			self.planner_text.delete("1.0", tk.END)
			self.planner_text.insert(tk.END, text)
			self.planner_text.config(state="disabled")
			return

		if self.output_text is None:
			return
		self.output_text.config(state="normal")
		self.output_text.delete("1.0", tk.END)
		self.output_text.insert(tk.END, text)
		self.output_text.config(state="disabled")


def main():
	# Print model accuracy to console on startup
	print("=" * 50)
	print("  Student Performance Advisor - Starting...")
	print("=" * 50)

	try:
		print(f"  Loading dataset from: {DATA_FILE.name}")
		df = load_dataset(DATA_FILE)
		print(f"  Dataset loaded: {len(df):,} records")
		print("  Training models...")
		model_bundle, metrics, medians = train_model(df)
		print(f"  Selected model: {metrics['selected_model']}")
		print(f"  R2: {metrics['r2']:.3f} | MAE: {metrics['mae']:.2f}")
		print(f"  RF MAE: {metrics['rf_mae']:.2f} | PCA MAE: {metrics['pca_mae']:.2f}")
		print("=" * 50)
		print("  Ready! Launching GUI...")
		print("=" * 50)
	except Exception as exc:  # pragma: no cover - UI startup guard
		print(f"  ERROR: {exc}")
		root = tk.Tk()
		root.withdraw()
		messagebox.showerror("Startup Error", f"Could not start the advisor:\n\n{exc}")
		root.destroy()
		return

	root = tk.Tk()
	PerformanceAdvisorApp(root, model_bundle, metrics, medians)
	root.mainloop()


if __name__ == "__main__":
	main()
