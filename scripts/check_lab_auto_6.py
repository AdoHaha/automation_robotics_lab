"""Lightweight structural checks for the generated Lab 6 notebook."""

from __future__ import annotations

from pathlib import Path

import nbformat


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK_PATH = ROOT / "lab_auto_6.ipynb"
DATA_DIR = ROOT / "data"

REQUIRED_TITLES = [
    "# Lab 6: Forecast-Driven Operation of a Smart Robotic Production Cell",
    "## System overview",
    "## 0. Imports and configuration",
    "## 1. Starter business data",
    "## 2. Ingredient-price data from the internet",
    "## 3. Forecasting",
    "## 4. Failure-risk machine learning",
    "## 5. Blending linear program",
    "## 6. Preventive-maintenance binary optimization",
    "## 7. Robot-cell job-shop scheduling",
    "## 8. CPM/PERT project planning",
    "## 9. Scenario analysis",
    "## 10. Final recommendation",
]

REQUIRED_FUNCTIONS = [
    "def download_if_missing",
    "def ensure_lab6_data",
    "def load_fred_series",
    "def evaluate_forecasters",
    "def forecast_targets",
    "def make_failure_features",
    "def evaluate_classifier",
    "def choose_threshold_by_cost",
    "def solve_blend",
    "def solve_maintenance_plan",
    "def solve_job_shop",
    "def validate_schedule",
    "def compute_cpm",
    "def run_scenario",
]

REQUIRED_DATA = [
    "lab6_orders.csv",
    "lab6_ingredients.csv",
    "lab6_stations.csv",
    "lab6_routes.csv",
    "lab6_maintenance_options.csv",
    "lab6_price_fallback.csv",
]


def fail(message: str) -> None:
    raise SystemExit(f"ERROR: {message}")


def main() -> None:
    if not NOTEBOOK_PATH.exists():
        fail(f"Missing notebook: {NOTEBOOK_PATH}")

    nb = nbformat.read(NOTEBOOK_PATH, as_version=4)
    all_source = "\n".join("".join(cell.get("source", "")) for cell in nb.cells)

    for title in REQUIRED_TITLES:
        if title not in all_source:
            fail(f"Missing section title: {title}")

    for function in REQUIRED_FUNCTIONS:
        if function not in all_source:
            fail(f"Missing required helper: {function}")

    if "https://raw.githubusercontent.com/AdoHaha/automation_robotics_lab/ex6/lab_auto_6_illustration.png" not in all_source:
        fail("Missing GitHub raw illustration link.")

    if all_source.count("TODO") < 8:
        fail("Expected at least 8 TODO markers for student work.")

    for cell in nb.cells:
        if cell.cell_type == "code":
            if cell.get("execution_count") is not None:
                fail("Notebook has non-empty execution counts.")
            outputs = cell.get("outputs", [])
            if outputs:
                fail("Notebook has committed code-cell outputs.")
            source = "".join(cell.get("source", ""))
            if "base64" in source.lower():
                fail("Notebook source appears to contain base64 content.")

    for filename in REQUIRED_DATA:
        path = DATA_DIR / filename
        if not path.exists():
            fail(f"Missing data file: {path.relative_to(ROOT)}")
        if path.stat().st_size == 0:
            fail(f"Empty data file: {path.relative_to(ROOT)}")

    print("Lab 6 notebook checks passed.")


if __name__ == "__main__":
    main()
