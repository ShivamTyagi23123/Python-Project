import tkinter as tk
from tkinter import ttk, messagebox
import time
import random

# ═══════════════════════════════════════════════════════════════════
#   SORTING & SEARCHING PERFORMANCE ANALYZER — GUI VERSION
# ═══════════════════════════════════════════════════════════════════

# --- Color Palette ---
BG_DARK       = "#0f0f1a"
BG_CARD       = "#1a1a2e"
BG_INPUT      = "#16213e"
ACCENT        = "#e94560"
ACCENT_HOVER  = "#ff6b81"
ACCENT2       = "#0f3460"
TEXT_PRIMARY   = "#eaeaea"
TEXT_SECONDARY = "#a0a0b0"
TEXT_MUTED     = "#6c6c80"
GOLD          = "#ffd700"
GREEN         = "#00e676"
CYAN          = "#00e5ff"
PURPLE        = "#bb86fc"
ORANGE        = "#ff9100"
BAR_COLORS    = ["#e94560", "#bb86fc", "#00e5ff"]


# ═══════════════════════════════════════════════════════════════════
#   SORTING ALGORITHMS
# ═══════════════════════════════════════════════════════════════════

def bubble_sort(arr):
    a = arr[:]
    n = len(a)
    comparisons = 0
    swaps = 0
    start = time.perf_counter()
    for i in range(n - 1):
        swapped = False
        for j in range(n - 1 - i):
            comparisons += 1
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                swaps += 1
                swapped = True
        if not swapped:
            break
    end = time.perf_counter()
    return a, comparisons, swaps, (end - start) * 1e6   # microseconds


def selection_sort(arr):
    a = arr[:]
    n = len(a)
    comparisons = 0
    swaps = 0
    start = time.perf_counter()
    for i in range(n - 1):
        min_idx = i
        for j in range(i + 1, n):
            comparisons += 1
            if a[j] < a[min_idx]:
                min_idx = j
        if min_idx != i:
            a[i], a[min_idx] = a[min_idx], a[i]
            swaps += 1
    end = time.perf_counter()
    return a, comparisons, swaps, (end - start) * 1e6


def insertion_sort(arr):
    a = arr[:]
    n = len(a)
    comparisons = 0
    swaps = 0
    start = time.perf_counter()
    for i in range(1, n):
        key = a[i]
        j = i - 1
        while j >= 0 and a[j] > key:
            comparisons += 1
            a[j + 1] = a[j]
            swaps += 1
            j -= 1
        if j >= 0:
            comparisons += 1
        a[j + 1] = key
    end = time.perf_counter()
    return a, comparisons, swaps, (end - start) * 1e6


# ═══════════════════════════════════════════════════════════════════
#   SEARCHING ALGORITHMS
# ═══════════════════════════════════════════════════════════════════

def linear_search(arr, target):
    comparisons = 0
    for i in range(len(arr)):
        comparisons += 1
        if arr[i] == target:
            return True, i, comparisons
    return False, -1, comparisons


def binary_search(arr, target):
    comparisons = 0
    low = 0
    high = len(arr) - 1
    while low <= high:
        mid = (low + high) // 2
        comparisons += 1
        if arr[mid] == target:
            return True, mid, comparisons
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return False, -1, comparisons


# ═══════════════════════════════════════════════════════════════════
#   GUI APPLICATION
# ═══════════════════════════════════════════════════════════════════

class PerformanceAnalyzerApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Sorting & Searching Performance Analyzer")
        self.root.configure(bg=BG_DARK)
        self.root.minsize(960, 720)
        self.root.geometry("1080x820")

        # Style setup
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self._configure_styles()

        # Main scrollable canvas
        self.canvas = tk.Canvas(root, bg=BG_DARK, highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(root, orient="vertical", command=self.canvas.yview)
        self.scroll_frame = tk.Frame(self.canvas, bg=BG_DARK)

        self.scroll_frame.bind("<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Enable mouse-wheel scrolling
        self.canvas.bind_all("<MouseWheel>",
            lambda e: self.canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"))

        self._build_header()
        self._build_input_section()
        self._build_results_container()

    # ── style helpers ──────────────────────────────────────────────

    def _configure_styles(self):
        self.style.configure("TFrame", background=BG_DARK)
        self.style.configure("Card.TFrame", background=BG_CARD)
        self.style.configure("TLabel", background=BG_DARK, foreground=TEXT_PRIMARY,
                             font=("Segoe UI", 10))
        self.style.configure("Header.TLabel", background=BG_DARK, foreground=TEXT_PRIMARY,
                             font=("Segoe UI", 22, "bold"))
        self.style.configure("Sub.TLabel", background=BG_DARK, foreground=TEXT_SECONDARY,
                             font=("Segoe UI", 10))
        self.style.configure("CardTitle.TLabel", background=BG_CARD, foreground=ACCENT,
                             font=("Segoe UI", 13, "bold"))
        self.style.configure("CardBody.TLabel", background=BG_CARD, foreground=TEXT_PRIMARY,
                             font=("Consolas", 10))
        self.style.configure("Metric.TLabel", background=BG_CARD, foreground=TEXT_SECONDARY,
                             font=("Segoe UI", 9))
        self.style.configure("Value.TLabel", background=BG_CARD, foreground=TEXT_PRIMARY,
                             font=("Segoe UI", 12, "bold"))
        self.style.configure("Gold.TLabel", background=BG_CARD, foreground=GOLD,
                             font=("Segoe UI", 11, "bold"))
        self.style.configure("Green.TLabel", background=BG_CARD, foreground=GREEN,
                             font=("Segoe UI", 11, "bold"))

    # ── header ─────────────────────────────────────────────────────

    def _build_header(self):
        hdr = tk.Frame(self.scroll_frame, bg=BG_DARK)
        hdr.pack(fill="x", padx=30, pady=(24, 0))

        title = tk.Label(hdr, text="⚡  Sorting & Searching Performance Analyzer",
                         bg=BG_DARK, fg=TEXT_PRIMARY, font=("Segoe UI", 20, "bold"))
        title.pack(anchor="w")
        sub = tk.Label(hdr, text="Compare Bubble, Selection & Insertion sort alongside Linear & Binary search",
                       bg=BG_DARK, fg=TEXT_SECONDARY, font=("Segoe UI", 10))
        sub.pack(anchor="w", pady=(2, 0))

    # ── input section ──────────────────────────────────────────────

    def _build_input_section(self):
        frame = tk.Frame(self.scroll_frame, bg=BG_CARD, highlightbackground=ACCENT2,
                         highlightthickness=1)
        frame.pack(fill="x", padx=30, pady=18)

        inner = tk.Frame(frame, bg=BG_CARD)
        inner.pack(fill="x", padx=20, pady=16)

        # Numbers input
        tk.Label(inner, text="Numbers (space-separated):", bg=BG_CARD, fg=TEXT_SECONDARY,
                 font=("Segoe UI", 10)).grid(row=0, column=0, sticky="w", pady=(0, 4))
        self.entry_numbers = tk.Entry(inner, bg=BG_INPUT, fg=TEXT_PRIMARY,
                                      insertbackground=TEXT_PRIMARY,
                                      font=("Consolas", 11), relief="flat",
                                      highlightbackground=ACCENT2, highlightthickness=1)
        self.entry_numbers.grid(row=1, column=0, sticky="ew", padx=(0, 12), ipady=6)

        # Target input
        tk.Label(inner, text="Search target:", bg=BG_CARD, fg=TEXT_SECONDARY,
                 font=("Segoe UI", 10)).grid(row=0, column=1, sticky="w", pady=(0, 4))
        self.entry_target = tk.Entry(inner, bg=BG_INPUT, fg=TEXT_PRIMARY,
                                     insertbackground=TEXT_PRIMARY,
                                     font=("Consolas", 11), relief="flat", width=14,
                                     highlightbackground=ACCENT2, highlightthickness=1)
        self.entry_target.grid(row=1, column=1, sticky="ew", padx=(0, 12), ipady=6)

        inner.columnconfigure(0, weight=4)
        inner.columnconfigure(1, weight=1)

        # Buttons row
        btn_row = tk.Frame(inner, bg=BG_CARD)
        btn_row.grid(row=2, column=0, columnspan=2, sticky="w", pady=(14, 0))

        self.btn_analyze = tk.Button(btn_row, text="▶  ANALYZE", bg=ACCENT, fg="white",
                                     activebackground=ACCENT_HOVER, activeforeground="white",
                                     font=("Segoe UI", 11, "bold"), relief="flat",
                                     cursor="hand2", padx=22, pady=6,
                                     command=self._run_analysis)
        self.btn_analyze.pack(side="left")

        self.btn_random = tk.Button(btn_row, text="🎲  Random Data", bg=ACCENT2, fg=TEXT_PRIMARY,
                                    activebackground="#1a4a8a", activeforeground="white",
                                    font=("Segoe UI", 10), relief="flat",
                                    cursor="hand2", padx=14, pady=6,
                                    command=self._generate_random)
        self.btn_random.pack(side="left", padx=(10, 0))

        self.btn_clear = tk.Button(btn_row, text="✕  Clear", bg="#2a2a3e", fg=TEXT_SECONDARY,
                                   activebackground="#3a3a4e", activeforeground=TEXT_PRIMARY,
                                   font=("Segoe UI", 10), relief="flat",
                                   cursor="hand2", padx=14, pady=6,
                                   command=self._clear_all)
        self.btn_clear.pack(side="left", padx=(10, 0))

    # ── results container ──────────────────────────────────────────

    def _build_results_container(self):
        self.results_frame = tk.Frame(self.scroll_frame, bg=BG_DARK)
        self.results_frame.pack(fill="x", padx=30, pady=(0, 30))

    # ── actions ────────────────────────────────────────────────────

    def _generate_random(self):
        count = random.randint(8, 20)
        nums = [random.randint(1, 999) for _ in range(count)]
        self.entry_numbers.delete(0, "end")
        self.entry_numbers.insert(0, " ".join(str(n) for n in nums))
        target = random.choice(nums)
        self.entry_target.delete(0, "end")
        self.entry_target.insert(0, str(target))

    def _clear_all(self):
        self.entry_numbers.delete(0, "end")
        self.entry_target.delete(0, "end")
        for w in self.results_frame.winfo_children():
            w.destroy()

    def _run_analysis(self):
        # Validate input
        raw = self.entry_numbers.get().strip()
        raw_target = self.entry_target.get().strip()
        if not raw or not raw_target:
            messagebox.showwarning("Input Required",
                                   "Please enter both a list of numbers and a search target.")
            return
        try:
            numbers = list(map(int, raw.split()))
        except ValueError:
            messagebox.showerror("Invalid Input",
                                 "Number list must contain only integers separated by spaces.")
            return
        try:
            target = int(raw_target)
        except ValueError:
            messagebox.showerror("Invalid Input", "Search target must be an integer.")
            return

        if len(numbers) < 2:
            messagebox.showwarning("Too Few Elements",
                                   "Please enter at least 2 numbers for a meaningful comparison.")
            return

        # Clear previous results
        for w in self.results_frame.winfo_children():
            w.destroy()

        # ── Run algorithms ──
        sorted1, comp1, swap1, time1 = bubble_sort(numbers)
        sorted2, comp2, swap2, time2 = selection_sort(numbers)
        sorted3, comp3, swap3, time3 = insertion_sort(numbers)
        found_l, idx_l, comps_l = linear_search(numbers, target)
        sorted_list = sorted1
        found_b, idx_b, comps_b = binary_search(sorted_list, target)

        # ── Display original list ──
        orig_lbl = tk.Label(self.results_frame,
                            text=f"Original list ({len(numbers)} elements):  {numbers}",
                            bg=BG_DARK, fg=TEXT_SECONDARY, font=("Consolas", 9),
                            wraplength=900, justify="left")
        orig_lbl.pack(anchor="w", pady=(8, 6))

        # ── Sorting Results ──
        self._section_header("SORTING RESULTS")

        sort_data = [
            ("Bubble Sort", sorted1, comp1, swap1, time1, BAR_COLORS[0]),
            ("Selection Sort", sorted2, comp2, swap2, time2, BAR_COLORS[1]),
            ("Insertion Sort", sorted3, comp3, swap3, time3, BAR_COLORS[2]),
        ]
        for name, s_list, comps, swps, t, color in sort_data:
            self._sort_card(name, s_list, comps, swps, t, color)

        # ── Performance Comparison ──
        self._section_header("PERFORMANCE COMPARISON")
        self._comparison_table(sort_data)
        self._bar_chart(sort_data)

        # Best performers
        times = {"Bubble Sort": time1, "Selection Sort": time2, "Insertion Sort": time3}
        comps_d = {"Bubble Sort": comp1, "Selection Sort": comp2, "Insertion Sort": comp3}
        swaps_d = {"Bubble Sort": swap1, "Selection Sort": swap2, "Insertion Sort": swap3}

        fastest = min(times, key=times.get)
        fewest_comps = min(comps_d, key=comps_d.get)
        fewest_swaps = min(swaps_d, key=swaps_d.get)

        best_frame = tk.Frame(self.results_frame, bg=BG_CARD,
                              highlightbackground=GOLD, highlightthickness=1)
        best_frame.pack(fill="x", pady=(8, 4))
        bp = tk.Frame(best_frame, bg=BG_CARD)
        bp.pack(fill="x", padx=16, pady=12)

        tk.Label(bp, text="🏆", bg=BG_CARD, font=("Segoe UI", 14)).grid(row=0, column=0, rowspan=3, padx=(0, 12))
        tk.Label(bp, text=f"Fastest algorithm:  {fastest}  ({times[fastest]:.2f} microseconds)",
                 bg=BG_CARD, fg=GOLD, font=("Segoe UI", 10, "bold")).grid(row=0, column=1, sticky="w")
        tk.Label(bp, text=f"Fewest comparisons:  {fewest_comps}  ({comps_d[fewest_comps]})",
                 bg=BG_CARD, fg=GREEN, font=("Segoe UI", 10)).grid(row=1, column=1, sticky="w")
        tk.Label(bp, text=f"Fewest swaps:  {fewest_swaps}  ({swaps_d[fewest_swaps]})",
                 bg=BG_CARD, fg=CYAN, font=("Segoe UI", 10)).grid(row=2, column=1, sticky="w")

        # ── Searching Results ──
        self._section_header("SEARCHING RESULTS")
        self._search_card("Linear Search", "original list", target, found_l, idx_l, comps_l, ORANGE)
        self._search_card("Binary Search", "sorted list", target, found_b, idx_b, comps_b, PURPLE)

        # ── Search summary ──
        sf = tk.Frame(self.results_frame, bg=BG_CARD, highlightbackground=ACCENT2,
                      highlightthickness=1)
        sf.pack(fill="x", pady=(8, 4))
        si = tk.Frame(sf, bg=BG_CARD)
        si.pack(fill="x", padx=16, pady=12)

        tk.Label(si, text="Search Summary", bg=BG_CARD, fg=ACCENT,
                 font=("Segoe UI", 12, "bold")).pack(anchor="w")
        tk.Label(si, text=f"Linear Search comparisons : {comps_l}", bg=BG_CARD,
                 fg=TEXT_PRIMARY, font=("Consolas", 10)).pack(anchor="w", pady=(6, 0))
        tk.Label(si, text=f"Binary Search comparisons : {comps_b}", bg=BG_CARD,
                 fg=TEXT_PRIMARY, font=("Consolas", 10)).pack(anchor="w", pady=(2, 0))

        winner = "Binary Search" if comps_b < comps_l else "Linear Search"
        tk.Label(si, text=f"More efficient : {winner}", bg=BG_CARD,
                 fg=GREEN, font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=(6, 0))

        # Scroll to top
        self.canvas.yview_moveto(0)

    # ── widget builders ────────────────────────────────────────────

    def _section_header(self, text):
        hdr = tk.Frame(self.results_frame, bg=BG_DARK)
        hdr.pack(fill="x", pady=(16, 6))
        tk.Frame(hdr, bg=ACCENT, height=2).pack(fill="x")
        tk.Label(hdr, text=f"  {text}", bg=BG_DARK, fg=TEXT_PRIMARY,
                 font=("Segoe UI", 13, "bold")).pack(anchor="w", pady=(6, 0))

    def _sort_card(self, name, sorted_list, comps, swaps, t_us, color):
        card = tk.Frame(self.results_frame, bg=BG_CARD,
                        highlightbackground=color, highlightthickness=1)
        card.pack(fill="x", pady=4)
        inner = tk.Frame(card, bg=BG_CARD)
        inner.pack(fill="x", padx=16, pady=12)

        # Title row
        tk.Label(inner, text=f"▸ {name}", bg=BG_CARD, fg=color,
                 font=("Segoe UI", 12, "bold")).grid(row=0, column=0, columnspan=4, sticky="w")

        # Sorted list (truncated if long)
        list_str = str(sorted_list)
        if len(list_str) > 90:
            list_str = list_str[:87] + "..."
        tk.Label(inner, text=f"Sorted: {list_str}", bg=BG_CARD, fg=TEXT_MUTED,
                 font=("Consolas", 9)).grid(row=1, column=0, columnspan=4, sticky="w", pady=(4, 8))

        # Metrics
        for col, (label, value) in enumerate([
            ("Comparisons", str(comps)),
            ("Swaps", str(swaps)),
            ("Time", f"{t_us:.2f} microseconds"),
        ]):
            tk.Label(inner, text=label, bg=BG_CARD, fg=TEXT_SECONDARY,
                     font=("Segoe UI", 9)).grid(row=2, column=col, sticky="w", padx=(0, 30))
            tk.Label(inner, text=value, bg=BG_CARD, fg=TEXT_PRIMARY,
                     font=("Segoe UI", 12, "bold")).grid(row=3, column=col, sticky="w", padx=(0, 30))

    def _search_card(self, name, list_type, target, found, idx, comps, color):
        card = tk.Frame(self.results_frame, bg=BG_CARD,
                        highlightbackground=color, highlightthickness=1)
        card.pack(fill="x", pady=4)
        inner = tk.Frame(card, bg=BG_CARD)
        inner.pack(fill="x", padx=16, pady=12)

        tk.Label(inner, text=f"▸ {name}  (on {list_type})", bg=BG_CARD, fg=color,
                 font=("Segoe UI", 12, "bold")).pack(anchor="w")
        tk.Label(inner, text=f"Target: {target}", bg=BG_CARD, fg=TEXT_SECONDARY,
                 font=("Consolas", 10)).pack(anchor="w", pady=(4, 0))

        if found:
            tk.Label(inner, text=f"✔ Found at index {idx}", bg=BG_CARD, fg=GREEN,
                     font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=(4, 0))
        else:
            tk.Label(inner, text="✘ Not found", bg=BG_CARD, fg=ACCENT,
                     font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=(4, 0))

        tk.Label(inner, text=f"Comparisons: {comps}", bg=BG_CARD, fg=TEXT_PRIMARY,
                 font=("Segoe UI", 10)).pack(anchor="w", pady=(4, 0))

    def _comparison_table(self, sort_data):
        table = tk.Frame(self.results_frame, bg=BG_CARD,
                         highlightbackground=ACCENT2, highlightthickness=1)
        table.pack(fill="x", pady=4)

        # Header row
        headers = ["Algorithm", "Comparisons", "Swaps", "Time (microseconds)"]
        for col, h in enumerate(headers):
            tk.Label(table, text=h, bg="#22223a", fg=TEXT_SECONDARY,
                     font=("Segoe UI", 10, "bold"), padx=16, pady=8,
                     anchor="w").grid(row=0, column=col, sticky="ew")

        # Data rows
        for row, (name, _, comps, swaps, t, color) in enumerate(sort_data, start=1):
            bg = BG_CARD if row % 2 == 1 else "#1e1e32"
            tk.Label(table, text=name, bg=bg, fg=color,
                     font=("Segoe UI", 10, "bold"), padx=16, pady=6,
                     anchor="w").grid(row=row, column=0, sticky="ew")
            tk.Label(table, text=str(comps), bg=bg, fg=TEXT_PRIMARY,
                     font=("Consolas", 10), padx=16, pady=6,
                     anchor="e").grid(row=row, column=1, sticky="ew")
            tk.Label(table, text=str(swaps), bg=bg, fg=TEXT_PRIMARY,
                     font=("Consolas", 10), padx=16, pady=6,
                     anchor="e").grid(row=row, column=2, sticky="ew")
            tk.Label(table, text=f"{t:.2f}", bg=bg, fg=TEXT_PRIMARY,
                     font=("Consolas", 10), padx=16, pady=6,
                     anchor="e").grid(row=row, column=3, sticky="ew")

        for c in range(4):
            table.columnconfigure(c, weight=1)

    def _bar_chart(self, sort_data):
        """Draw a simple horizontal bar chart for time comparison."""
        chart_frame = tk.Frame(self.results_frame, bg=BG_CARD,
                               highlightbackground=ACCENT2, highlightthickness=1)
        chart_frame.pack(fill="x", pady=4)
        tk.Label(chart_frame, text="  Time Comparison (microseconds)", bg=BG_CARD, fg=TEXT_SECONDARY,
                 font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=12, pady=(10, 4))

        max_time = max(t for _, _, _, _, t, _ in sort_data) or 1

        for name, _, _, _, t, color in sort_data:
            row = tk.Frame(chart_frame, bg=BG_CARD)
            row.pack(fill="x", padx=16, pady=3)

            tk.Label(row, text=f"{name:>16s}", bg=BG_CARD, fg=TEXT_SECONDARY,
                     font=("Consolas", 9), width=18, anchor="e").pack(side="left")

            bar_canvas = tk.Canvas(row, bg=BG_CARD, height=20, highlightthickness=0)
            bar_canvas.pack(side="left", fill="x", expand=True, padx=(8, 4))
            bar_canvas.update_idletasks()

            w = bar_canvas.winfo_width() or 400
            bar_w = max(int((t / max_time) * w), 4)
            bar_canvas.create_rectangle(0, 2, bar_w, 18, fill=color, outline="")

            tk.Label(row, text=f"{t:.2f}", bg=BG_CARD, fg=TEXT_PRIMARY,
                     font=("Consolas", 9), width=10, anchor="w").pack(side="left")

        tk.Label(chart_frame, text="", bg=BG_CARD).pack(pady=(0, 6))


# ═══════════════════════════════════════════════════════════════════
#   ENTRY POINT
# ═══════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    root = tk.Tk()
    app = PerformanceAnalyzerApp(root)
    root.mainloop()
