"""Build Lab 6 notebook and supporting starter data.

The notebook is generated with nbformat so the committed notebook remains
consistent and output-free.
"""

from __future__ import annotations

import csv
import math
import random
from pathlib import Path

import nbformat as nbf


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
NOTEBOOK_PATH = ROOT / "lab_auto_6.ipynb"
RANDOM_SEED = 42


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def build_lab6_data() -> None:
    """Create small, readable data files used by the notebook."""

    write_csv(
        DATA_DIR / "lab6_orders.csv",
        [
            {
                "product": "Protein Plus",
                "target_month": "2026-06-01",
                "demand_kg": 420,
                "due_min": 430,
                "min_protein": 0.32,
                "min_fat": 0.10,
                "max_moisture": 0.68,
            },
            {
                "product": "Budget Blend",
                "target_month": "2026-06-01",
                "demand_kg": 620,
                "due_min": 430,
                "min_protein": 0.24,
                "min_fat": 0.08,
                "max_moisture": 0.72,
            },
            {
                "product": "Protein Plus",
                "target_month": "2026-09-01",
                "demand_kg": 520,
                "due_min": 500,
                "min_protein": 0.32,
                "min_fat": 0.10,
                "max_moisture": 0.68,
            },
            {
                "product": "Budget Blend",
                "target_month": "2026-09-01",
                "demand_kg": 700,
                "due_min": 500,
                "min_protein": 0.24,
                "min_fat": 0.08,
                "max_moisture": 0.72,
            },
        ],
        [
            "product",
            "target_month",
            "demand_kg",
            "due_min",
            "min_protein",
            "min_fat",
            "max_moisture",
        ],
    )

    write_csv(
        DATA_DIR / "lab6_ingredients.csv",
        [
            {
                "ingredient": "chicken",
                "protein": 0.38,
                "fat": 0.09,
                "moisture": 0.64,
                "min_share": 0.10,
                "max_share": 0.60,
                "fallback_cost_per_kg": 6.95,
            },
            {
                "ingredient": "beef",
                "protein": 0.34,
                "fat": 0.17,
                "moisture": 0.58,
                "min_share": 0.00,
                "max_share": 0.45,
                "fallback_cost_per_kg": 9.60,
            },
            {
                "ingredient": "eggs",
                "protein": 0.13,
                "fat": 0.11,
                "moisture": 0.76,
                "min_share": 0.00,
                "max_share": 0.25,
                "fallback_cost_per_kg": 5.40,
            },
            {
                "ingredient": "milk",
                "protein": 0.034,
                "fat": 0.033,
                "moisture": 0.88,
                "min_share": 0.00,
                "max_share": 0.20,
                "fallback_cost_per_kg": 1.15,
            },
            {
                "ingredient": "plant_filler",
                "protein": 0.16,
                "fat": 0.03,
                "moisture": 0.10,
                "min_share": 0.05,
                "max_share": 0.35,
                "fallback_cost_per_kg": 1.05,
            },
        ],
        [
            "ingredient",
            "protein",
            "fat",
            "moisture",
            "min_share",
            "max_share",
            "fallback_cost_per_kg",
        ],
    )

    write_csv(
        DATA_DIR / "lab6_stations.csv",
        [
            {"station": "Mixer", "machine_id": 1},
            {"station": "Thermal processor", "machine_id": 2},
            {"station": "Packaging robot", "machine_id": 3},
            {"station": "Vision inspection", "machine_id": 4},
        ],
        ["station", "machine_id"],
    )

    write_csv(
        DATA_DIR / "lab6_routes.csv",
        [
            {"product": "Protein Plus", "operation": 1, "station": "Mixer", "base_duration_min": 35},
            {
                "product": "Protein Plus",
                "operation": 2,
                "station": "Thermal processor",
                "base_duration_min": 50,
            },
            {
                "product": "Protein Plus",
                "operation": 3,
                "station": "Packaging robot",
                "base_duration_min": 30,
            },
            {
                "product": "Protein Plus",
                "operation": 4,
                "station": "Vision inspection",
                "base_duration_min": 15,
            },
            {"product": "Budget Blend", "operation": 1, "station": "Mixer", "base_duration_min": 30},
            {
                "product": "Budget Blend",
                "operation": 2,
                "station": "Packaging robot",
                "base_duration_min": 28,
            },
            {
                "product": "Budget Blend",
                "operation": 3,
                "station": "Vision inspection",
                "base_duration_min": 12,
            },
        ],
        ["product", "operation", "station", "base_duration_min"],
    )

    write_csv(
        DATA_DIR / "lab6_maintenance_options.csv",
        [
            {
                "machine_id": 1,
                "station": "Mixer",
                "service_time_min": 45,
                "service_cost": 450,
                "failure_cost": 4000,
                "risk_reduction": 0.70,
            },
            {
                "machine_id": 2,
                "station": "Thermal processor",
                "service_time_min": 60,
                "service_cost": 700,
                "failure_cost": 7000,
                "risk_reduction": 0.75,
            },
            {
                "machine_id": 3,
                "station": "Packaging robot",
                "service_time_min": 50,
                "service_cost": 600,
                "failure_cost": 5500,
                "risk_reduction": 0.70,
            },
            {
                "machine_id": 4,
                "station": "Vision inspection",
                "service_time_min": 35,
                "service_cost": 350,
                "failure_cost": 3000,
                "risk_reduction": 0.65,
            },
        ],
        [
            "machine_id",
            "station",
            "service_time_min",
            "service_cost",
            "failure_cost",
            "risk_reduction",
        ],
    )

    rng = random.Random(RANDOM_SEED)
    specs = {
        "chicken": (6.1, 0.032, 0.28),
        "beef": (8.5, 0.045, 0.36),
        "eggs": (4.4, 0.030, 0.48),
        "milk": (1.0, 0.004, 0.08),
        "plant_filler": (0.86, 0.006, 0.04),
    }
    rows: list[dict[str, object]] = []
    year_months = [(year, month) for year in range(2018, 2026) for month in range(1, 13)]
    for ingredient, (base, trend, noise) in specs.items():
        for idx, (year, month) in enumerate(year_months):
            seasonal = 0.06 * math.sin(2 * math.pi * idx / 12)
            shock = 0.0
            if ingredient == "eggs" and year in {2022, 2023}:
                shock = 0.9 * math.exp(-abs(idx - 58) / 10)
            value = base + trend * idx + seasonal + shock + rng.gauss(0, noise)
            rows.append(
                {
                    "date": f"{year:04d}-{month:02d}-01",
                    "ingredient": ingredient,
                    "cost_per_kg": round(max(value, 0.05), 3),
                    "source": "synthetic fallback for offline teaching",
                }
            )
    write_csv(
        DATA_DIR / "lab6_price_fallback.csv",
        rows,
        ["date", "ingredient", "cost_per_kg", "source"],
    )


def md(text: str) -> nbf.NotebookNode:
    return nbf.v4.new_markdown_cell(text.strip())


def code(text: str) -> nbf.NotebookNode:
    return nbf.v4.new_code_cell(text.strip())


def build_notebook() -> nbf.NotebookNode:
    nb = nbf.v4.new_notebook()
    nb.metadata["kernelspec"] = {
        "display_name": "Python 3",
        "language": "python",
        "name": "python3",
    }
    nb.metadata["language_info"] = {"name": "python", "pygments_lexer": "ipython3"}

    cells = [
        md(
            r"""
# Lab 6: Forecast-Driven Operation of a Smart Robotic Production Cell

In this capstone lab you are the operations/data team for a small automated production cell. The cell prepares two pet-food products for two delivery months:

- **Protein Plus**
- **Budget Blend**

Ingredient prices are uncertain, and machines may fail during production unless preventive maintenance is scheduled. Your job is to connect data, forecasting, machine learning, optimization, scheduling, and project planning into one operating recommendation.

This lab reuses:

- **Lab 4**: job-shop scheduling, no-overlap binary variables, and Gantt charts,
- **Lab 5**: CPM/PERT, critical path, slack, deadline risk, and crashing decisions,
- earlier LP examples: blending and cost minimization.
"""
        ),
        md(
            r"""
## System overview

![Smart robotic production cell with forecasting, ML risk, network planning, and scheduling overlays](https://raw.githubusercontent.com/AdoHaha/automation_robotics_lab/master/lab_auto_6_illustration.png)

The illustration shows the whole capstone idea: a robot production cell connected to forecasting, machine-risk monitoring, network planning, and schedule optimization.
"""
        ),
        md(
            r"""
## Learning goals

After this lab you should be able to:

1. collect and clean public time-series price data,
2. compare forecasting models using a validation period,
3. train and evaluate an introductory failure-risk classifier,
4. choose a probability threshold using expected cost instead of accuracy alone,
5. formulate and solve a blending linear program,
6. formulate and solve a preventive-maintenance binary optimization model,
7. adapt job-shop scheduling to a robot production cell,
8. connect a robot-cell makespan to a CPM/PERT project plan,
9. explain a final operating plan under several scenarios.
"""
        ),
        md(
            r"""
## 0. Imports and configuration

The lab is designed for Google Colab and local Jupyter. If a package is missing, run the install line once and restart the kernel if needed.

New tools used in this lab:

- `pathlib.Path`: handles file paths in a way that works on Windows, Linux, Colab, and Jupyter.
- `scikit-learn`: trains and evaluates the failure-risk machine-learning models.
- `statsmodels`: gives us a simple exponential-smoothing forecasting model.
- `pulp`: builds and solves the linear and binary optimization models.
- `networkx`: represents the CPM/PERT project network as a graph.

### Follow the data-loading functions

`download_if_missing(filename)` takes a file name, checks the local `data/`
folder, and returns its `Path`. It downloads the file only when it is absent or
empty. `ensure_lab6_data()` calls that helper for each name in
`REQUIRED_DATA_FILES` and returns a list of paths. Neither function reads the
CSV contents into a table: we do that in the next section.

Read the function definition first, then find the `ensure_lab6_data()` call
at the end of the cell. Defining a function stores its instructions; the call
runs them. Default arguments such as `data_dir=DATA_DIR` let the helper use our
configuration while still allowing another folder in a named call.
"""
        ),
        code(
            r"""
# In Google Colab, uncomment and run once if needed:
# %pip install pandas numpy matplotlib networkx pulp scikit-learn statsmodels

from __future__ import annotations

import math
import re
import urllib.error
import urllib.request
import warnings
from itertools import combinations
from pathlib import Path

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd
import pulp

from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from statsmodels.tsa.holtwinters import ExponentialSmoothing

RANDOM_SEED = 42
# Fix random choices so repeated runs use the same teaching-data sample.
np.random.seed(RANDOM_SEED)
warnings.filterwarnings("ignore", category=FutureWarning)

DATA_DIR = Path("data")
TARGET_MONTHS = [pd.Timestamp("2026-06-01"), pd.Timestamp("2026-09-01")]
TECHNICIAN_TIME_LIMIT_MIN = 120
MAINTENANCE_BUDGET = 1200

# If the notebook is opened directly in Colab, the repository files are not
# automatically copied into /content. This helper downloads the required data
# files when they are missing. If you clone the repository first, it does nothing.
GITHUB_RAW_BASES = [
    "https://raw.githubusercontent.com/AdoHaha/automation_robotics_lab/master",
]

REQUIRED_DATA_FILES = [
    "lab6_orders.csv",
    "lab6_ingredients.csv",
    "lab6_stations.csv",
    "lab6_routes.csv",
    "lab6_maintenance_options.csv",
    "lab6_price_fallback.csv",
    "sensor_readings_timeseries.csv",
]


def download_if_missing(filename, data_dir=DATA_DIR, raw_bases=GITHUB_RAW_BASES):
    '''Return the path of a local data file, downloading it if necessary.

    Args:
        filename: CSV file name, without the data-folder prefix.
        data_dir: pathlib.Path for the local folder; defaults to DATA_DIR.
        raw_bases: List of GitHub raw URL roots to try; defaults to GITHUB_RAW_BASES.

    Returns:
        A Path to a nonempty file. Prints the URL when a download is attempted.

    Raises:
        FileNotFoundError when the file cannot be found locally or downloaded.
    '''
    # Make the folder first, then reuse an existing nonempty file.
    data_dir.mkdir(parents=True, exist_ok=True)
    target = data_dir / filename
    if target.exists() and target.stat().st_size > 0:
        return target

    last_error = None
    for raw_base in raw_bases:
        # Each repository root supplies the same relative data/filename path.
        url = f"{raw_base}/data/{filename}"
        try:
            print(f"Downloading {filename} from {url}")
            urllib.request.urlretrieve(url, target)
            if target.exists() and target.stat().st_size > 0:
                return target
        except (urllib.error.URLError, OSError) as exc:
            last_error = exc

    raise FileNotFoundError(
        f"Could not find or download {filename}. "
        "Clone the repository or upload the data/ folder before continuing."
    ) from last_error


def ensure_lab6_data():
    '''Ensure every name in REQUIRED_DATA_FILES has a local file.

    Uses download_if_missing and its default folder/URL settings.
    Returns a list of Paths; raises if a required file cannot be obtained.
    '''
    # One helper call per file; collect the returned paths into a list.
    return [download_if_missing(filename) for filename in REQUIRED_DATA_FILES]


ensure_lab6_data()
"""
        ),
        md(
            r"""
## 1. Starter business data

These tables define the production problem. Nutrition values are simplified teaching values, not real formulation advice.

Read the tables as operations data:

- `orders`: what must be produced and when,
- `ingredients`: nutrition and allowed recipe shares,
- `routes`: station sequence for each product,
- `stations`: which machine belongs to each station,
- `maintenance_options`: time, cost, and benefit of preventive maintenance.
"""
        ),
        code(
            r"""
# Path / filename joins folder and file names; parse_dates creates usable date values.
orders = pd.read_csv(DATA_DIR / "lab6_orders.csv", parse_dates=["target_month"])
ingredients = pd.read_csv(DATA_DIR / "lab6_ingredients.csv")
stations = pd.read_csv(DATA_DIR / "lab6_stations.csv")
routes = pd.read_csv(DATA_DIR / "lab6_routes.csv")
maintenance_options = pd.read_csv(DATA_DIR / "lab6_maintenance_options.csv")

display(orders)
display(ingredients)
display(routes)
display(maintenance_options)
"""
        ),
        md(
            r"""
### Task 1 - read the system

Answer before modeling:

1. Which station looks most likely to become a bottleneck?
2. Which product has stricter recipe constraints?
3. Which maintenance option looks expensive but potentially valuable?
"""
        ),
        md(
            r"""
## 2. Ingredient-price data from the internet

The live data source is [FRED](https://fred.stlouisfed.org/), the Federal Reserve Economic Data portal.

Start from the [FRED commodities category](https://fred.stlouisfed.org/categories/32217) or use the FRED search bar. As one worked example, [chicken breast, boneless, per lb](https://fred.stlouisfed.org/series/APU0000FF1101) has series ID `APU0000FF1101`.

Your job is to find and verify comparable monthly price series for beef, eggs, and milk. The code cell below includes a starter mapping so the notebook can run, but you should still check the pages and units.

| Ingredient | Student action | Original unit to verify |
|---|---|---|
| chicken | worked example: `APU0000FF1101` | USD/lb |
| beef | find/verify a ground beef series | USD/lb |
| eggs | find/verify an eggs series | USD/dozen |
| milk | find/verify a whole milk series | USD/gallon |

The notebook also includes `data/lab6_price_fallback.csv`, so the exercise still works offline.

New idea: a public time series rarely has exactly the unit we need. FRED may report USD/lb, USD/gallon, or USD/dozen. Before using prices in an optimization model, we convert everything to the same teaching unit: cost per kg.

### Loading functions: one ingredient, then one combined table

`load_fred_series` accepts a series ID, ingredient label, fallback table, and
`use_live` switch. It reads dates and prices, converts the units, and returns
columns `date`, `ingredient`, `cost_per_kg`, and `source`. A failed download
returns that ingredient's fallback rows instead.

`load_price_history(use_live=True)` calls the first function for every entry in
`fred_series`, adds the offline filler prices, and joins the results with
`pd.concat`. Call `load_price_history(use_live=False)` to use the provided
historical data without requesting live prices. The returned table, rather
than the loading function itself, is the input to forecasting.
"""
        ),
        code(
            r"""
# FRED IDs are stable identifiers for public monthly price series.
# The chicken ID is given as a worked example. Verify or replace the other IDs
# after searching FRED yourself.
fred_series = {
    "beef": "APU0000703112",
    "eggs": "APU0000708111",
    "milk": "APU0000709112",
    "chicken": "APU0000FF1101",
}

unit_conversions = pd.DataFrame([
    {"ingredient": "beef", "fred_unit": "USD/lb", "conversion_to_cost_per_kg": 2.20462},
    {"ingredient": "chicken", "fred_unit": "USD/lb", "conversion_to_cost_per_kg": 2.20462},
    {"ingredient": "eggs", "fred_unit": "USD/dozen", "conversion_to_cost_per_kg": 1 / 0.68},
    {"ingredient": "milk", "fred_unit": "USD/gallon", "conversion_to_cost_per_kg": 1 / 3.90},
    {"ingredient": "plant_filler", "fred_unit": "offline starter cost/kg", "conversion_to_cost_per_kg": 1.0},
])

fallback_prices = pd.read_csv(DATA_DIR / "lab6_price_fallback.csv", parse_dates=["date"])


def load_fred_series(series_id, ingredient, fallback_df, use_live=True):
    '''Return monthly prices for one ingredient in the common cost-per-kg unit.

    Args:
        series_id: FRED series ID string.
        ingredient: Label used in unit_conversions and fallback_df.
        fallback_df: Table with date, ingredient, cost_per_kg, and source columns.
        use_live: True (default) requests FRED; False selects fallback rows directly.

    Returns:
        A DataFrame with date, ingredient, cost_per_kg, and source columns.
        Uses the global unit_conversions table for live data. If loading fails,
        prints the reason and returns a copy of this ingredient's fallback rows.
    '''
    if not use_live:
        return fallback_df[fallback_df["ingredient"] == ingredient].copy()

    url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={series_id}"
    try:
        # FRED supplies a date column and a price column; normalize their names.
        raw = pd.read_csv(url)
        date_col = raw.columns[0]
        value_col = raw.columns[1]
        df = raw.rename(columns={date_col: "date", value_col: "raw_value"})
        df["date"] = pd.to_datetime(df["date"])
        df["raw_value"] = pd.to_numeric(df["raw_value"], errors="coerce")  # Missing markers become NaN.
        df = df.dropna(subset=["raw_value"])

        # Convert from the original FRED unit into the common unit used by the LP.
        multiplier = unit_conversions.set_index("ingredient").loc[
            ingredient, "conversion_to_cost_per_kg"
        ]
        df["cost_per_kg"] = df["raw_value"] * multiplier
        df["ingredient"] = ingredient
        df["source"] = f"FRED:{series_id}"
        return df[["date", "ingredient", "cost_per_kg", "source"]]
    except Exception as exc:
        print(f"Using fallback for {ingredient}: {exc}")
        return fallback_df[fallback_df["ingredient"] == ingredient].copy()


def load_price_history(use_live=True):
    '''Join the ingredient histories into one date-sorted price table.

    Args:
        use_live: True (default) attempts FRED loading; False uses fallback data.

    Returns:
        A DataFrame with date, ingredient, cost_per_kg, and source columns.
        Uses fred_series, fallback_prices, and load_fred_series defined above.
        Plant filler always uses the offline history.
    '''
    # A list of separate tables becomes one table through concat.
    frames = [
        load_fred_series(series_id, ingredient, fallback_prices, use_live=use_live)
        for ingredient, series_id in fred_series.items()
    ]
    frames.append(fallback_prices[fallback_prices["ingredient"] == "plant_filler"].copy())
    prices = pd.concat(frames, ignore_index=True)
    prices = prices.sort_values(["ingredient", "date"])
    return prices


price_history = load_price_history(use_live=True)
price_history.groupby("ingredient").tail(3)
"""
        ),
        md(
            r"""
### Task 2 - document units

TODO: Inspect the FRED pages for each live series. Create a short table in your own notebook explaining the original unit and the conversion you used before optimization.
"""
        ),
        code(
            r"""
# Group rows by ingredient, then draw each history on the same axes for comparison.
fig, ax = plt.subplots(figsize=(10, 4))
for ingredient, group in price_history.groupby("ingredient"):
    ax.plot(group["date"], group["cost_per_kg"], label=ingredient)
ax.set_title("Ingredient cost history")
ax.set_ylabel("Cost per kg, teaching currency")
ax.legend()
plt.show()
"""
        ),
        md(
            r"""
## 3. Forecasting

Do not forecast with one black-box model and stop. Use a validation period and compare models.

This section includes:

- seasonal naive baseline,
- drift/trend baseline,
- exponential smoothing from `statsmodels`.

New tool: `statsmodels.tsa.holtwinters.ExponentialSmoothing`.

The three forecasting methods represent increasing complexity:

- **seasonal naive**: "next June looks like last June",
- **drift**: "continue the long-run linear trend",
- **exponential smoothing**: combine level, trend, and yearly seasonality.

The important habit is not the specific model. The important habit is to keep the last 12 months as validation data and check whether a more complex model actually improves error.

### Read the forecasting helpers as a pipeline

The input `y` is a pandas **Series**: one numeric price column ordered by month.
`train_test_split_series` returns two Series, the earlier training history and
the last `test_size` observations. `.iloc` selects by position, so this split
keeps the chronological order.

The three forecasting functions each accept `train` and a `horizon` (number of
future months) and return a Series of predictions. Seasonal naive repeats the
last yearly cycle; drift extends a fitted line; exponential smoothing fits
level, trend, and seasonality, with drift as its fallback.

`mape` returns a fractional error rate: 0.10 means 10%, not 0.10%.
`evaluate_forecasters(price_df, ingredient)` filters one ingredient, builds a
monthly index, fills missing months, and compares predictions against the
held-out observations. It returns a table of MAE and MAPE scores. Trace the
input table → monthly Series → split → predictions → score table in the code.
"""
        ),
        code(
            r"""
def train_test_split_series(y, test_size=12):
    '''Split an ordered monthly price Series into training and validation data.

    Args:
        y: Numeric pandas Series ordered by month.
        test_size: Number of final observations to hold out; defaults to 12.

    Returns:
        (train, test), two Series preserving the original index and price units.
        Requires more than test_size + 12 observations; otherwise raises ValueError.
    '''
    if len(y) <= test_size + 12:
        raise ValueError("Need more history for a 12-month validation split.")
    return y.iloc[:-test_size], y.iloc[-test_size:]  # Earlier rows, then the held-out tail.


def seasonal_naive_forecast(train, horizon, season_length=12):
    '''Repeat the final observed seasonal cycle to predict future prices.

    Args:
        train: Ordered price Series with at least season_length observations.
        horizon: Number of future observations to predict.
        season_length: Observations per cycle; defaults to 12 for monthly prices.

    Returns:
        A Series of horizon prices, in the input units, indexed from zero.
    '''
    # Reuse the last observed value from the same month of the seasonal cycle.
    # For monthly data and season_length=12, forecasted March uses last March.
    values = [train.iloc[-season_length + (h % season_length)] for h in range(horizon)]
    return pd.Series(values)


def drift_forecast(train, horizon):
    '''Extend a least-squares linear trend through the observed prices.

    Args:
        train: Numeric price Series ordered by month.
        horizon: Number of future months to predict.

    Returns:
        A Series of horizon prices in the input units, indexed from zero.
    '''
    # Fit a simple straight line through history and extend that line forward.
    x = np.arange(len(train))
    coef = np.polyfit(x, train.values, deg=1)  # Fit slope and intercept to positions and prices.
    future_x = np.arange(len(train), len(train) + horizon)
    return pd.Series(np.polyval(coef, future_x))


def exponential_smoothing_forecast(train, horizon):
    '''Forecast monthly prices using additive trend and yearly seasonality.

    Args:
        train: Ordered monthly price Series used to fit the smoothing model.
        horizon: Number of future months to predict.

    Returns:
        A zero-indexed Series of horizon prices. If fitting or forecasting fails,
        returns drift_forecast(train, horizon) instead, in the same price units.
    '''
    try:
        # Additive trend and additive seasonality are readable defaults for a first lab.
        model = ExponentialSmoothing(
            train,
            trend="add",
            seasonal="add",
            seasonal_periods=12,
            initialization_method="estimated",
        )
        fit = model.fit(optimized=True)  # Estimate the smoothing parameters from history.
        return pd.Series(fit.forecast(horizon).values)
    except Exception:
        # Keep the pipeline runnable when a smoothing fit cannot be obtained.
        return drift_forecast(train, horizon)


def mape(y_true, y_pred):
    '''Return mean absolute percentage error as a fraction, excluding zero actuals.

    Args:
        y_true: Actual prices; same length and order as y_pred.
        y_pred: Predicted prices in the same units.

    Returns:
        A float, e.g. 0.10 for 10% error. Zero actuals are excluded to avoid division
        by zero; if all actuals are zero, the empty average is NaN.
    '''
    y_true = np.asarray(y_true)
    y_pred = np.asarray(y_pred)
    mask = y_true != 0  # Only evaluate rows with a meaningful percentage denominator.
    return float(np.mean(np.abs((y_true[mask] - y_pred[mask]) / y_true[mask])))


def evaluate_forecasters(price_df, ingredient):
    '''Compare three forecasting methods on the final 12 monthly observations.

    Args:
        price_df: Table with ingredient, date, and numeric cost_per_kg columns.
        ingredient: Label identifying the history to evaluate.

    Returns:
        One row per model with ingredient, model, MAE (cost/kg), and MAPE (fraction).
        Uses the splitting and forecasting helpers above. Missing monthly values
        are interpolated before the split.
    '''
    # One ingredient at a time: clean the monthly index, split history, forecast test months.
    series = (
        price_df[price_df["ingredient"] == ingredient]
        .sort_values("date")
        .set_index("date")["cost_per_kg"]
        .asfreq("MS")
        .interpolate()
    )
    train, test = train_test_split_series(series, test_size=12)
    # Each prediction has the same length as the held-out validation period.
    predictions = {
        "seasonal_naive": seasonal_naive_forecast(train, len(test)),
        "drift": drift_forecast(train, len(test)),
        "exp_smoothing": exponential_smoothing_forecast(train, len(test)),
    }
    rows = []
    for model_name, pred in predictions.items():
        # Compare arrays by position: first prediction to first validation month, etc.
        rows.append({
            "ingredient": ingredient,
            "model": model_name,
            "MAE": float(np.mean(np.abs(test.values - pred.values))),
            "MAPE": mape(test.values, pred.values),
        })
    return pd.DataFrame(rows)


forecast_scores = pd.concat(
    [evaluate_forecasters(price_history, ingredient) for ingredient in ingredients["ingredient"]],
    ignore_index=True,
)
forecast_scores.sort_values(["ingredient", "MAE"])
"""
        ),
        md(
            r"""
### Turn historical scores into future prices

`forecast_targets(price_df, target_months)` returns one row per ingredient and
delivery month. It uses the ingredient labels from `ingredients`, selects the
lowest-MAE method, refits it on the full history, and extracts each target
month's prediction. `target_months` must be after the last observation of every
ingredient history. The `low_cost` and `high_cost` columns are scenario
multipliers, not statistical confidence intervals.

The call below saves this table as `forecast_prices`; later LPs select prices
from it by ingredient and delivery month. Follow `horizon` (how many months to
predict) and `step` (which prediction to select) through the loop.
"""
        ),
        code(
            r"""
def forecast_targets(price_df, target_months):
    '''Forecast each ingredient price for the requested future delivery months.

    Args:
        price_df: Table with ingredient, date, and cost_per_kg columns.
        target_months: Nonempty list of monthly pandas Timestamps after each history.

    Returns:
        A DataFrame with ingredient, target_month, forecast_cost, low_cost,
        high_cost, selected_model, and validation_MAE columns. Prices use the
        history's cost/kg units; low/high are 0.90/1.15 scenario multipliers.
        Uses the global ingredients table and the forecasting helpers above.
    '''
    rows = []
    for ingredient in ingredients["ingredient"]:
        series = (
            price_df[price_df["ingredient"] == ingredient]
            .sort_values("date")
            .set_index("date")["cost_per_kg"]
            .asfreq("MS")
            .interpolate()
        )
        # Select the model with the lowest validation MAE for this ingredient.
        scores = evaluate_forecasters(price_df, ingredient)
        selected = scores.sort_values("MAE").iloc[0]
        last_date = series.index.max()
        # Period subtraction counts months; predict far enough to reach the latest target.
        horizon = max((month.to_period("M") - last_date.to_period("M")).n for month in target_months)

        # Refit the selected model on all available data, then forecast to the target months.
        if selected["model"] == "seasonal_naive":
            pred = seasonal_naive_forecast(series, horizon)
        elif selected["model"] == "drift":
            pred = drift_forecast(series, horizon)
        else:
            pred = exponential_smoothing_forecast(series, horizon)

        for month in target_months:
            step = (month.to_period("M") - last_date.to_period("M")).n
            # step=1 means the first future month, stored at zero-based position 0.
            forecast_cost = float(max(pred.iloc[step - 1], 0.01))
            rows.append({
                "ingredient": ingredient,
                "target_month": month,
                "forecast_cost": forecast_cost,
                "low_cost": 0.90 * forecast_cost,
                "high_cost": 1.15 * forecast_cost,
                "selected_model": selected["model"],
                "validation_MAE": selected["MAE"],
            })
    return pd.DataFrame(rows)


forecast_prices = forecast_targets(price_history, TARGET_MONTHS)
forecast_prices
"""
        ),
        md(
            r"""
### Task 3 - forecasting interpretation

TODO:

1. Which ingredients are hardest to forecast?
2. Did exponential smoothing beat the seasonal naive baseline for every ingredient?
3. If a simple baseline wins, why is it reasonable to use it?
"""
        ),
        md(
            r"""
## 4. Failure-risk machine learning

This is an introduction to supervised machine learning. The target is `near_failure`: whether a reading occurred shortly before a simulated failure.

Important idea: readings from the same machine lifecycle are related. If we split individual rows randomly, the model can see almost the same lifecycle in both train and test data. That is leakage. We split by `instance_id` instead.

New tool: `scikit-learn`.

The ML workflow in this lab has five steps:

1. choose a target column (`near_failure`),
2. create useful feature columns from raw sensor readings,
3. split data into train and test sets without leakage,
4. train one or more classifiers,
5. evaluate using maintenance-relevant metrics, not only accuracy.

Vocabulary:

- **feature**: an input column used by the model,
- **target**: the answer the model learns to predict,
- **classifier**: a model that predicts classes such as failure/no failure,
- **probability threshold**: the cutoff where we convert a probability into an action.
"""
        ),
        md(
            r"""
### ML warm-up: read a confusion matrix

Before training a model, read this small example. Rows are actual outcomes; columns are model predictions.

- A **false negative** is dangerous here: the model predicts "not near failure", but the machine is actually near failure.
- A **false positive** is annoying but less severe: the model asks for maintenance that was not needed.

This is why a maintenance model should not be judged by accuracy alone.
"""
        ),
        code(
            r"""
# A cell counts examples with one actual outcome and one predicted outcome.
toy_confusion = pd.DataFrame(
    [[920, 40], [18, 22]],
    index=["actual not near failure", "actual near failure"],
    columns=["predicted not near failure", "predicted near failure"],
)

toy_false_negative_cost = 5000
toy_false_positive_cost = 600
# Multiply each type of error by its consequence, then add the two losses.
toy_expected_cost = (
    toy_confusion.loc["actual near failure", "predicted not near failure"] * toy_false_negative_cost
    + toy_confusion.loc["actual not near failure", "predicted near failure"] * toy_false_positive_cost
)

display(toy_confusion)
print(f"Expected error cost in this toy example: {toy_expected_cost}")
"""
        ),
        code(
            r"""
# Load sensor rows; the earlier download helper ensures the file exists.
sensor_path = DATA_DIR / "sensor_readings_timeseries.csv"
if sensor_path.exists():
    sensor_df = pd.read_csv(sensor_path)
else:
    raise FileNotFoundError("Expected data/sensor_readings_timeseries.csv")

# Keep the lab fast. Sample complete lifecycles, not random rows.
sampled_instances = (
    sensor_df["instance_id"]
    .drop_duplicates()
    .sample(n=min(900, sensor_df["instance_id"].nunique()), random_state=RANDOM_SEED)
)
sensor_sample = sensor_df[sensor_df["instance_id"].isin(sampled_instances)].copy()

print(sensor_sample.shape)
print(sensor_sample["near_failure"].value_counts(normalize=True).rename("rate"))
sensor_sample.head()
"""
        ),
        md(
            r"""
### Build feature columns without mixing machine lifecycles

`make_failure_features(df)` takes the sensor table and returns **two answers**:
an enriched table and a list of column names to use as model inputs. The call
`features_df, feature_cols = ...` unpacks that pair into separate variables.

Inside the function, sorting makes time order explicit. `groupby("instance_id")`
keeps each lifecycle separate; `rolling(3)` summarizes the current and previous
two readings, and `diff()` calculates the change from the previous reading.
The original table is copied before adding columns. After the function call,
the code splits complete lifecycles, then selects `X` (features) and `y` (labels).
"""
        ),
        code(
            r"""
def make_failure_features(df):
    '''Add past/current sensor summaries and return the table plus feature names.

    Args:
        df: Table with instance_id, time, machine_id, sensor_temp, and sensor_vib.
            Rows represent ordered readings within each machine lifecycle.

    Returns:
        (features, feature_cols): a sorted copy with rolling/change columns and
        a list of input column names. Keeps original columns, including labels.
        Rolling windows contain up to three readings within one instance_id;
        changes for the first reading are filled with zero.
    '''
    # Always sort time series before calculating rolling means or changes.
    df = df.sort_values(["instance_id", "time"]).copy()
    grouped = df.groupby("instance_id", group_keys=False)

    # Rolling features summarize recent behavior, which is often more useful
    # than one instantaneous sensor reading.
    df["temp_roll_mean_3"] = (
        grouped["sensor_temp"].rolling(3, min_periods=1).mean().reset_index(level=0, drop=True)
    )
    df["vib_roll_mean_3"] = (
        grouped["sensor_vib"].rolling(3, min_periods=1).mean().reset_index(level=0, drop=True)
    )
    df["vib_roll_max_3"] = (
        grouped["sensor_vib"].rolling(3, min_periods=1).max().reset_index(level=0, drop=True)
    )
    # Change features approximate a simple trend: is the signal rising or falling?
    df["temp_change"] = grouped["sensor_temp"].diff().fillna(0)
    df["vib_change"] = grouped["sensor_vib"].diff().fillna(0)

    # Return feature names explicitly so training and prediction select the same columns.
    feature_cols = [
        "machine_id",
        "time",
        "sensor_temp",
        "sensor_vib",
        "temp_roll_mean_3",
        "vib_roll_mean_3",
        "vib_roll_max_3",
        "temp_change",
        "vib_change",
    ]
    return df, feature_cols


features_df, feature_cols = make_failure_features(sensor_sample)

# Split whole lifecycles, not individual rows. This prevents leakage.
instances = features_df["instance_id"].drop_duplicates().sample(frac=1, random_state=RANDOM_SEED)
split = int(0.75 * len(instances))
train_instances = set(instances.iloc[:split])
test_instances = set(instances.iloc[split:])

train_df = features_df[features_df["instance_id"].isin(train_instances)]
test_df = features_df[features_df["instance_id"].isin(test_instances)]

# X contains input columns; y contains the known outcome to learn and evaluate.
X_train = train_df[feature_cols]
y_train = train_df["near_failure"]
X_test = test_df[feature_cols]
y_test = test_df["near_failure"]

print(X_train.shape, X_test.shape)
print("Train failure rate:", y_train.mean().round(4))
print("Test failure rate:", y_test.mean().round(4))
"""
        ),
        md(
            r"""
### Fit classifiers, then evaluate their predictions

`positive_class_probability(model, X)` accepts a fitted binary classifier and
an input table. For our models, `predict_proba(X)` returns two columns: class-0
and class-1 probabilities; `[:, 1]` selects the near-failure probability for
every row. The helper can also return decision scores for a model without
probabilities; scores do not have the same interpretation as probabilities.

`evaluate_classifier(y_true, p_hat, threshold=0.5)` compares known labels with
predictions at a chosen cutoff and returns a dictionary of metrics. The loop
fits each model on `X_train, y_train`, evaluates on `X_test, y_test`, and stores
both fitted models and predictions for later analysis. `make_pipeline` applies
scaling and logistic regression in sequence, fitting scaling on training data.
"""
        ),
        code(
            r"""
def positive_class_probability(model, X):
    '''Return class-1 probabilities, or decision scores when probabilities are absent.

    Args:
        model: Fitted binary classifier; predict_proba columns must be ordered [0, 1].
        X: Feature table with the columns/order expected by the fitted model.

    Returns:
        One numeric value per input row. For our classifiers it is a probability
        in [0, 1]; the fallback decision_function returns scores, not probabilities.
    '''
    # hasattr checks which prediction API the fitted estimator supplies.
    if hasattr(model, "predict_proba"):
        return model.predict_proba(X)[:, 1]
    return model.decision_function(X)


def evaluate_classifier(y_true, p_hat, threshold=0.5):
    '''Return binary classification metrics for one prediction cutoff.

    Args:
        y_true: Actual binary labels in the same row order as p_hat; both classes
            must be present for ROC AUC.
        p_hat: Class-1 probabilities (or ranking scores for ROC AUC).
        threshold: Cutoff for predicting class 1; defaults to 0.5 for probabilities.

    Returns:
        A dictionary of threshold, accuracy, precision, recall, f1, and roc_auc.
        Undefined precision/recall/F1 values are reported as zero.
    '''
    # Probabilities become yes/no predictions only after we choose a threshold.
    y_pred = (p_hat >= threshold).astype(int)
    return {
        "threshold": threshold,
        "accuracy": accuracy_score(y_true, y_pred),
        "precision": precision_score(y_true, y_pred, zero_division=0),
        "recall": recall_score(y_true, y_pred, zero_division=0),
        "f1": f1_score(y_true, y_pred, zero_division=0),
        "roc_auc": roc_auc_score(y_true, p_hat),
    }


models = {
    # Logistic regression is a simple, interpretable baseline. Scaling helps it fit.
    "logistic_regression": make_pipeline(
        StandardScaler(),
        LogisticRegression(max_iter=2000, class_weight="balanced"),
    ),
    # Random forests can capture nonlinear patterns in sensor readings.
    "random_forest": RandomForestClassifier(
        n_estimators=80,
        min_samples_leaf=5,
        class_weight="balanced",
        random_state=RANDOM_SEED,
        n_jobs=-1,
    ),
}

model_rows = []
fitted_models = {}
probabilities = {}
for name, model in models.items():
    # fit = learn from training data; predict_proba = estimate failure probabilities
    model.fit(X_train, y_train)
    p_hat = positive_class_probability(model, X_test)
    fitted_models[name] = model
    probabilities[name] = p_hat
    row = evaluate_classifier(y_test, p_hat, threshold=0.5)
    row["model"] = name
    model_rows.append(row)

model_comparison = pd.DataFrame(model_rows).sort_values("roc_auc", ascending=False)
model_comparison
"""
        ),
        code(
            r"""
# The comparison was sorted by ROC AUC; iloc[0] selects its leading row.
best_model_name = model_comparison.iloc[0]["model"]
best_model = fitted_models[best_model_name]
best_p_hat = probabilities[best_model_name]

print("Selected model:", best_model_name)
print(classification_report(y_test, best_p_hat >= 0.5, zero_division=0))
pd.DataFrame(
    confusion_matrix(y_test, best_p_hat >= 0.5),
    index=["actual 0", "actual 1"],
    columns=["predicted 0", "predicted 1"],
)
"""
        ),
        md(
            r"""
### Convert classification errors into a cost comparison

`expected_classification_cost` takes labels, probabilities, a cutoff, and the
two error costs. `confusion_matrix(...).ravel()` unpacks the 2×2 matrix as
true negatives, false positives, false negatives, and true positives. The
function charges only the errors and returns one total cost.

`choose_threshold_by_cost` repeats that calculation for 19 cutoffs and returns
the cheapest row **and** the complete comparison table. In
`best_threshold, threshold_table = ...`, the first variable is a pandas Series,
not a scalar: read `best_threshold["threshold"]` for its cutoff. Change an error
cost by a named argument to see how the preferred action changes.
"""
        ),
        code(
            r"""
def expected_classification_cost(
    y_true,
    p_hat,
    threshold,
    false_negative_cost=5000,
    false_positive_cost=600,
):
    '''Calculate total error cost at one cutoff on labelled binary examples.

    Args:
        y_true: Actual 0/1 labels; both classes must be represented.
        p_hat: Class-1 probabilities aligned with y_true.
        threshold: Probability cutoff for predicting near failure.
        false_negative_cost: Cost per missed failure; defaults to 5000.
        false_positive_cost: Cost per unnecessary service alert; defaults to 600.

    Returns:
        False-positive count × its cost + false-negative count × its cost,
        in the same teaching currency as the two input costs.
    '''
    # False negatives are missed failures. False positives are unnecessary service calls.
    y_pred = (p_hat >= threshold).astype(int)
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
    return fp * false_positive_cost + fn * false_negative_cost


def choose_threshold_by_cost(
    y_true,
    p_hat,
    false_negative_cost=5000,
    false_positive_cost=600,
):
    '''Compare 19 cutoffs and return the cheapest row plus all candidate costs.

    Args:
        y_true: Actual binary labels; both classes must be present.
        p_hat: Aligned near-failure probabilities.
        false_negative_cost: Cost per missed failure; defaults to 5000.
        false_positive_cost: Cost per unnecessary service alert; defaults to 600.

    Returns:
        (best, result): a pandas Series for the selected row and a DataFrame
        with threshold and expected_cost columns. Calls expected_classification_cost.
    '''
    rows = []
    for threshold in np.linspace(0.05, 0.95, 19):
        # Try several thresholds and keep the one with the lowest expected cost.
        rows.append({
            "threshold": threshold,
            "expected_cost": expected_classification_cost(
                y_true,
                p_hat,
                threshold,
                false_negative_cost=false_negative_cost,
                false_positive_cost=false_positive_cost,
            ),
        })
    result = pd.DataFrame(rows)
    # Keep all candidates for explanation, even though only one row is selected.
    best = result.sort_values("expected_cost").iloc[0]
    return best, result


best_threshold, threshold_table = choose_threshold_by_cost(y_test, best_p_hat)
display(threshold_table)
best_threshold
"""
        ),
        code(
            r"""
# Select the final observed reading in each lifecycle before aggregating by machine.
latest_rows = (
    features_df.sort_values(["instance_id", "time"])
    .groupby("instance_id", as_index=False)
    .tail(1)
    .copy()
)
# Use the latest reading from each lifecycle as a proxy for current machine condition.
latest_rows["p_failure"] = best_model.predict_proba(latest_rows[feature_cols])[:, 1]

machine_risk = (
    latest_rows.groupby("machine_id")
    .agg(
        p_failure=("p_failure", "mean"),
        current_temp=("sensor_temp", "mean"),
        current_vib=("sensor_vib", "mean"),
    )
    .reset_index()
    # Attach service times, costs, and risk-reduction assumptions using machine_id.
    .merge(maintenance_options, on="machine_id", how="left")
)
machine_risk["expected_avoided_loss"] = (
    # Expected avoided loss is the value that maintenance can protect.
    machine_risk["p_failure"]
    * machine_risk["failure_cost"]
    * machine_risk["risk_reduction"]
)
machine_risk
"""
        ),
        md(
            r"""
### Task 4 - ML interpretation

TODO:

1. Why can accuracy be misleading when `near_failure` is rare?
2. Which is more important here: precision or recall? Explain using business cost.
3. What threshold would you choose if an unexpected failure became twice as expensive?
"""
        ),
        md(
            r"""
## 5. Blending linear program

Now the forecasts become an optimization input. For each product and target month, choose ingredient kilograms to minimize cost while satisfying nutrition and share constraints.

New tool: `PuLP`.

PuLP models have the same ingredients as the hand-written LPs from earlier labs:

- **decision variables**: unknown values the solver chooses,
- **objective**: the expression we minimize or maximize,
- **constraints**: equations or inequalities the answer must obey,
- **status**: whether the solver found an optimal feasible solution.

### One recipe function call, then a table of all orders

`solve_blend(product_name, target_month, price_table, orders, ingredients)`
selects one order and the prices for its month. It creates kilogram variables,
adds the cost objective and recipe constraints, solves, checks status, and
returns one row per ingredient. `price_col` selects the price column to use;
for example, a named `price_col="high_cost"` call tests that alternative input.

Read the units in the comments: an ingredient fraction multiplied by its kg
gives nutrient kg; unit price multiplied by ingredient kg gives cost.
`itertuples(index=False)` visits table rows with names such as `row.product`.
The list of recipe tables is joined with `pd.concat`; `merge` attaches each
order's batch size so `kg / demand_kg` can be interpreted as a recipe share.
"""
        ),
        code(
            r"""
def solve_blend(product_name, target_month, price_table, orders, ingredients, price_col="forecast_cost"):
    '''Minimize ingredient cost for one product's order in one delivery month.

    Args:
        product_name: Product label identifying one row in orders for target_month.
        target_month: Delivery month, convertible to a pandas Timestamp.
        price_table: Ingredient/month prices with ingredient, target_month, and price_col.
        orders: Table with product, target_month, demand_kg, min_protein, min_fat,
            and max_moisture; nutrient limits are mass fractions.
        ingredients: Table with ingredient, protein, fat, moisture, min_share,
            and max_share; composition/share values are mass fractions.
        price_col: Cost-per-kg column name; defaults to forecast_cost.

    Returns:
        A DataFrame with product, target_month, ingredient, kg, unit_cost, and
        cost columns. Raises ValueError if CBC does not find an optimal recipe.
    '''
    # One call solves one product in one delivery month.
    order_row = orders[
        (orders["product"] == product_name)
        & (orders["target_month"] == pd.Timestamp(target_month))
    ].iloc[0]
    demand = float(order_row["demand_kg"])
    prices = (
        # Fix the delivery month before converting ingredient-labelled prices to a dictionary.
        price_table[price_table["target_month"] == pd.Timestamp(target_month)]
        .set_index("ingredient")[price_col]
        .to_dict()
    )

    # x[ingredient] is the number of kilograms of that ingredient in the batch.
    model_name = f"blend_{re.sub(r'[^A-Za-z0-9_]+', '_', product_name)}_{pd.Timestamp(target_month):%Y_%m}"
    model = pulp.LpProblem(model_name, pulp.LpMinimize)
    x = {
        row.ingredient: pulp.LpVariable(f"kg_{row.ingredient}", lowBound=0)
        for row in ingredients.itertuples(index=False)
    }

    # Objective: minimize total ingredient cost.
    model += pulp.lpSum(prices[i] * x[i] for i in x)

    # Recipe constraints: total mass and nutrition requirements.
    model += pulp.lpSum(x[i] for i in x) == demand
    model += pulp.lpSum(row.protein * x[row.ingredient] for row in ingredients.itertuples(index=False)) >= float(order_row["min_protein"]) * demand
    model += pulp.lpSum(row.fat * x[row.ingredient] for row in ingredients.itertuples(index=False)) >= float(order_row["min_fat"]) * demand
    model += pulp.lpSum(row.moisture * x[row.ingredient] for row in ingredients.itertuples(index=False)) <= float(order_row["max_moisture"]) * demand

    for row in ingredients.itertuples(index=False):
        # Share bounds prevent unrealistic recipes such as 100% filler.
        model += x[row.ingredient] >= float(row.min_share) * demand
        model += x[row.ingredient] <= float(row.max_share) * demand

    status = model.solve(pulp.PULP_CBC_CMD(msg=False))
    if pulp.LpStatus[status] != "Optimal":
        raise ValueError(f"Blend model did not solve optimally: {pulp.LpStatus[status]}")

    # Read kilogram decisions only after the status check; report each cost contribution.
    result = pd.DataFrame([
        {
            "product": product_name,
            "target_month": pd.Timestamp(target_month),
            "ingredient": ingredient,
            "kg": pulp.value(var),
            "unit_cost": prices[ingredient],
            "cost": pulp.value(var) * prices[ingredient],
        }
        for ingredient, var in x.items()
    ])
    return result


# Run one independent recipe model per order and stack their ingredient rows.
recipe_plan = pd.concat(
    [
        solve_blend(row.product, row.target_month, forecast_prices, orders, ingredients)
        for row in orders.itertuples(index=False)
    ],
    ignore_index=True,
)

display(recipe_plan)
recipe_summary = recipe_plan.groupby(["product", "target_month"], as_index=False)["cost"].sum()

recipe_shares = recipe_plan.merge(
    orders[["product", "target_month", "demand_kg"]],
    on=["product", "target_month"],
    how="left",
)
recipe_shares["share"] = recipe_shares["kg"] / recipe_shares["demand_kg"]

display(recipe_summary)
recipe_shares.pivot_table(
    index=["product", "ingredient"],
    columns="target_month",
    values="share",
)
"""
        ),
        md(
            r"""
### Task 5 - blending interpretation

TODO: Compare June and September recipes using both kilograms and shares. Which ingredient shares change, and are those changes explained by forecasted prices or by nutrition constraints?
"""
        ),
        md(
            r"""
## 6. Preventive-maintenance binary optimization

The ML model estimates failure probability. The maintenance model turns that estimate into a decision.

This is a small **binary optimization** model. A binary variable can only be 0 or 1:

- `z[m] = 1`: maintain machine `m`,
- `z[m] = 0`: do not maintain machine `m`.

The objective rewards maintenance only when the expected avoided loss is larger than the service cost, while the constraints enforce limited technician time and budget.

### What the maintenance helper takes and returns

`solve_maintenance_plan(machine_risk, time_limit_min, budget)` uses one row per
machine, including its expected avoided loss, service time, and cost. It creates
one binary choice per machine, maximizes net value, and enforces the two limits.
The returned table preserves the risk data and adds `maintain` (0 or 1) and
`net_value`; it is the input to the scheduling helper, not a schedule itself.

The dictionary key `int(row.machine_id)` connects each machine's variable to
its table row. After an optimal solve, `.map(...)` writes those decisions back
to the copied table. Rounding here removes solver noise from a binary value;
it does not turn a continuous relaxation into an integer solution.
"""
        ),
        code(
            r"""
def solve_maintenance_plan(machine_risk, time_limit_min, budget):
    '''Choose preventive maintenance actions within technician time and budget.

    Args:
        machine_risk: One-row-per-machine table with machine_id,
            expected_avoided_loss, service_cost, and service_time_min.
        time_limit_min: Maximum available technician minutes.
        budget: Maximum service expenditure, in the same currency as service_cost.

    Returns:
        A copy of machine_risk with maintain (binary decision) and net_value
        (expected avoided loss minus service cost) columns. Raises ValueError
        unless CBC reports an optimal solution.
    '''
    model = pulp.LpProblem("maintenance_selection", pulp.LpMaximize)

    # Binary decision: choose whether each machine receives service.
    z = {
        int(row.machine_id): pulp.LpVariable(f"maintain_{int(row.machine_id)}", cat="Binary")
        for row in machine_risk.itertuples(index=False)
    }
    # Net value is what the objective earns by selecting this maintenance action.
    net_value = {
        int(row.machine_id): float(row.expected_avoided_loss - row.service_cost)
        for row in machine_risk.itertuples(index=False)
    }

    # Objective: maximize total maintenance value.
    model += pulp.lpSum(net_value[m] * z[m] for m in z)

    # Resource constraints: technicians cannot exceed time or budget.
    model += pulp.lpSum(
        float(row.service_time_min) * z[int(row.machine_id)]
        for row in machine_risk.itertuples(index=False)
    ) <= time_limit_min
    model += pulp.lpSum(
        float(row.service_cost) * z[int(row.machine_id)]
        for row in machine_risk.itertuples(index=False)
    ) <= budget

    status = model.solve(pulp.PULP_CBC_CMD(msg=False))
    if pulp.LpStatus[status] != "Optimal":
        raise ValueError(f"Maintenance model did not solve optimally: {pulp.LpStatus[status]}")

    # Preserve the input risk table; attach checked decisions to a separate copy.
    result = machine_risk.copy()
    result["maintain"] = result["machine_id"].map(lambda m: int(round(pulp.value(z[int(m)]))))
    result["net_value"] = result["expected_avoided_loss"] - result["service_cost"]
    return result


maintenance_plan = solve_maintenance_plan(
    machine_risk,
    TECHNICIAN_TIME_LIMIT_MIN,
    MAINTENANCE_BUDGET,
)
maintenance_plan
"""
        ),
        code(
            r"""
# Compare the optimization with choosing every individually profitable service.
simple_rule = machine_risk.copy()
simple_rule["maintain_by_simple_rule"] = (
    simple_rule["expected_avoided_loss"] > simple_rule["service_cost"]
).astype(int)
simple_rule[[
    "machine_id",
    "station",
    "expected_avoided_loss",
    "service_cost",
    "service_time_min",
    "maintain_by_simple_rule",
]]
"""
        ),
        md(
            r"""
### Task 6 - maintenance interpretation

TODO: Compare the optimized maintenance plan with the simple rule. Does the simple rule fit within the technician time limit and budget?
"""
        ),
        md(
            r"""
## 7. Robot-cell job-shop scheduling

Each production batch is a job moving through shared stations. Selected maintenance tasks become blocking operations on those same stations.

This section reuses Lab 4. The main modeling idea is still:

1. each operation has a start time,
2. operations inside the same job must follow route order,
3. two operations cannot use the same station at the same time,
4. the objective minimizes the final completion time, called the makespan.

Maintenance is represented as an extra job that occupies one station for its service duration.
In this version, selected maintenance must finish before production can start on that same station.

### Prepare operations before choosing their start times

`build_job_operations(orders, routes)` returns one row per production operation:
job, station, route position, duration, and due time. It scales the route's
reference durations with batch size (within the stated teaching limits) and
rounds them upward to whole minutes.

`add_maintenance_jobs(operations, maintenance_plan)` adds an operation only for
rows where `maintain == 1`. It returns a new combined table. These functions
prepare inputs; the solver in the following cell chooses start times. Trace
one order through its route rows and find which extra row occupies a station
when maintenance is selected.
"""
        ),
        code(
            r"""
def build_job_operations(orders, routes, reference_batch_kg=500):
    '''Expand each production order into its ordered station operations.

    Args:
        orders: Table with product, target_month (Timestamp), demand_kg, and due_min.
        routes: Table with product, operation, station, and base_duration_min.
        reference_batch_kg: Batch size represented by route times; defaults to 500 kg.

    Returns:
        A DataFrame with job, product, operation, station, duration, and due_min.
        Durations are whole minutes, scaled by demand/reference within [0.7, 1.5].
    '''
    rows = []
    for batch in orders.itertuples(index=False):
        route = routes[routes["product"] == batch.product].sort_values("operation")  # Preserve route order.
        # Larger demand creates a longer batch. Clamp the scale so the toy instance
        # remains small enough for a classroom MILP.
        scale = max(0.7, min(1.5, float(batch.demand_kg) / reference_batch_kg))
        job_name = f"{batch.target_month:%b} {batch.product}"
        for op in route.itertuples(index=False):
            rows.append({
                "job": job_name,
                "product": batch.product,
                "operation": int(op.operation),
                "station": op.station,
                "duration": int(math.ceil(float(op.base_duration_min) * scale)),
                "due_min": float(batch.due_min),
            })
    return pd.DataFrame(rows)


def add_maintenance_jobs(operations, maintenance_plan):
    '''Append station-blocking service operations for selected maintenance actions.

    Args:
        operations: Production operation table returned by build_job_operations.
        maintenance_plan: Table with maintain, station, and service_time_min columns.

    Returns:
        A new operation DataFrame. Each selected service is a one-operation job
        with duration in minutes and no due date; existing production rows remain.
    '''
    # Convert to row dictionaries so we can append jobs with the same columns.
    rows = operations.to_dict("records")
    for row in maintenance_plan[maintenance_plan["maintain"] == 1].itertuples(index=False):
        # A selected service action blocks the same station as production would.
        rows.append({
            "job": f"Maintenance: {row.station}",
            "product": "Maintenance",
            "operation": 1,
            "station": row.station,
            "duration": int(row.service_time_min),
            "due_min": np.nan,
        })
    return pd.DataFrame(rows)


operations_without_maintenance = build_job_operations(orders, routes)
operations = add_maintenance_jobs(operations_without_maintenance, maintenance_plan)
operations
"""
        ),
        md(
            r"""
### Solve start times, then independently validate the returned schedule

`safe_name(text)` prepares labels for solver variable names.
`solve_job_shop(operations)` accepts the operation table, creates start times,
adds route, maintenance-before-production, and no-overlap rules, and minimizes
makespan. It returns `(makespan, schedule)`; the latter adds `op_id`, `start`,
and `end` columns. Tuple unpacking saves those two results separately below.

`combinations(rows, 2)` visits each competing pair on a station once. A binary
variable chooses their order; `horizon` relaxes the unused ordering constraint.
Follow the four constraint groups rather than treating the model as one block.

`validate_schedule(schedule)` checks route order and station overlaps using the
returned numeric times. It returns a confirmation string or raises an error.
This validator checks those two physical rules; the maintenance-precedence
rules are enforced in the solver. Its small tolerance accommodates numeric noise.
"""
        ),
        code(
            r"""
def safe_name(text):
    '''Return text with punctuation replaced by underscores for solver names.

    Args:
        text: Any value convertible to a string.

    Returns:
        A string containing letters, digits, and underscores, with outer underscores removed.
    '''
    # A regular expression matches characters outside the allowed set.
    return re.sub(r"[^A-Za-z0-9_]+", "_", str(text)).strip("_")


def solve_job_shop(operations):
    '''Schedule production and selected maintenance to minimize makespan.

    Args:
        operations: Table with job, product, operation, station, and duration
            (minutes), plus any other reporting columns such as due_min.
            Maintenance rows have product equal to "Maintenance".

    Returns:
        (makespan, schedule): completion time in minutes and an operation table
        with op_id, start, and end columns sorted by start/station.
        Uses safe_name for CBC variable labels. Raises ValueError on nonoptimal status.
    '''
    # Give each operation its own ID; identical stations/jobs still have distinct variables.
    operations = operations.copy().reset_index(drop=True)
    operations["op_id"] = operations.index
    # A safe upper bound for "very late" in the no-overlap constraints.
    horizon = int(operations["duration"].sum() + 100)

    model = pulp.LpProblem("robot_cell_job_shop", pulp.LpMinimize)
    start = {
        row.op_id: pulp.LpVariable(f"start_{row.op_id}_{safe_name(row.job)}", lowBound=0)
        for row in operations.itertuples(index=False)
    }
    c_max = pulp.LpVariable("makespan", lowBound=0)

    # Constraint group 1: route order inside each job.
    for job, group in operations.groupby("job"):
        group = group.sort_values("operation")
        job_ops = list(group.itertuples(index=False))
        for prev, nxt in zip(job_ops, job_ops[1:]):
            model += start[nxt.op_id] >= start[prev.op_id] + float(prev.duration)

    # Constraint group 2: selected maintenance must happen before production
    # on the same station. This makes the maintenance decision visible in the schedule.
    maintenance_rows = operations[operations["product"] == "Maintenance"]
    production_rows = operations[operations["product"] != "Maintenance"]
    for maint in maintenance_rows.itertuples(index=False):
        same_station = production_rows[production_rows["station"] == maint.station]
        for prod in same_station.itertuples(index=False):
            model += start[prod.op_id] >= start[maint.op_id] + float(maint.duration)

    # Constraint group 3: no overlap on the same station.
    # The binary y chooses which operation goes first.
    for station, group in operations.groupby("station"):
        rows = list(group.itertuples(index=False))
        for a, b in combinations(rows, 2):
            y = pulp.LpVariable(f"{safe_name(station)}_{a.op_id}_before_{b.op_id}", cat="Binary")
            model += start[a.op_id] + float(a.duration) <= start[b.op_id] + horizon * (1 - y)
            model += start[b.op_id] + float(b.duration) <= start[a.op_id] + horizon * y

    # Constraint group 4: makespan is at least every operation's finish time.
    for row in operations.itertuples(index=False):
        model += c_max >= start[row.op_id] + float(row.duration)

    model += c_max
    status = model.solve(pulp.PULP_CBC_CMD(msg=False))
    if pulp.LpStatus[status] != "Optimal":
        raise ValueError(f"Schedule model did not solve optimally: {pulp.LpStatus[status]}")

    # Map optimized start variables back to their operation IDs for a readable table.
    schedule = operations.copy()
    schedule["start"] = schedule["op_id"].map(lambda op_id: pulp.value(start[op_id]))
    schedule["end"] = schedule["start"] + schedule["duration"]
    return float(pulp.value(c_max)), schedule.sort_values(["start", "station"])


def validate_schedule(schedule, tolerance=1e-7):
    '''Check route order and station no-overlap using computed start/end times.

    Args:
        schedule: Operation table with job, operation, station, start, and end,
            where times are minutes.
        tolerance: Allowed numerical comparison noise in minutes; defaults to 1e-7.

    Returns:
        "Schedule is valid." when both checks pass. Raises AssertionError listing
        violations otherwise. Does not separately check maintenance precedence.
    '''
    # Solver output should always be checked before interpreting a Gantt chart.
    errors = []
    for job, group in schedule.groupby("job"):
        # The next operation must start after the previous operation ends.
        group = group.sort_values("operation")
        previous_end = None
        for row in group.itertuples(index=False):
            if previous_end is not None and row.start + tolerance < previous_end:
                errors.append(f"Route violation for {job}")
            previous_end = row.end

    for station, group in schedule.groupby("station"):
        # Sort by time before comparing adjacent operations on the same station.
        rows = sorted(group.itertuples(index=False), key=lambda row: row.start)
        for a, b in zip(rows, rows[1:]):
            if a.end > b.start + tolerance:
                errors.append(f"Overlap on {station}: {a.job} and {b.job}")

    if errors:
        raise AssertionError("\\n".join(errors))
    return "Schedule is valid."


makespan, schedule = solve_job_shop(operations)
print(f"Makespan with selected maintenance: {makespan:.0f} min")
print(validate_schedule(schedule))
schedule
"""
        ),
        md(
            r"""
### Draw a Gantt chart from the checked schedule

`plot_gantt(schedule, title=...)` takes numeric start times, durations, job labels,
and station labels. It maps each job to a row and each station to a color,
then draws a bar with `left=start` and width `duration`. This places an operation
at its actual scheduled time instead of starting every bar at zero.

It returns the Matplotlib `(fig, ax)` pair so you can change the plot afterward.
The call is followed by `plt.show()` to display it. Try a named `title` argument
or use the returned `ax` to change a label; the schedule itself stays the same.
"""
        ),
        code(
            r"""
def plot_gantt(schedule, title="Robot-cell schedule"):
    '''Draw operation bars by job and station; return the Matplotlib figure and axes.

    Args:
        schedule: Table with job, station, start, and duration columns; times in minutes.
        title: Plot title; defaults to "Robot-cell schedule".

    Returns:
        (fig, ax), allowing further annotations. Draws bars but leaves plt.show()
        to the caller. Does not solve or validate the schedule.
    '''
    fig, ax = plt.subplots(figsize=(11, 0.45 * schedule["job"].nunique() + 2))
    jobs = list(schedule["job"].drop_duplicates())
    y_pos = {job: idx for idx, job in enumerate(jobs)}  # Convert job labels to row positions.
    station_colors = {
        station: color
        for station, color in zip(
            schedule["station"].drop_duplicates(),
            plt.cm.Set2(np.linspace(0, 1, schedule["station"].nunique())),
        )
    }
    for row in schedule.itertuples(index=False):
        # A bar's horizontal position is its start; its width is processing time.
        ax.barh(
            y_pos[row.job],
            row.duration,
            left=row.start,
            color=station_colors[row.station],
            edgecolor="black",
        )
        ax.text(row.start + row.duration / 2, y_pos[row.job], row.station, ha="center", va="center", fontsize=8)
    ax.set_yticks(range(len(jobs)))
    ax.set_yticklabels(jobs)
    ax.set_xlabel("Minutes")
    ax.set_title(title)
    ax.grid(axis="x", alpha=0.25)
    # Small colored rectangles make one legend entry per station.
    handles = [
        plt.Rectangle((0, 0), 1, 1, color=color, ec="black")
        for color in station_colors.values()
    ]
    ax.legend(handles, station_colors.keys(), loc="upper right")
    plt.tight_layout()
    return fig, ax


plot_gantt(schedule)
plt.show()
"""
        ),
        code(
            r"""
# Change only the maintenance decisions and re-solve to compare planned completion time.
no_maintenance_plan = maintenance_plan.copy()
no_maintenance_plan["maintain"] = 0
no_maintenance_makespan, no_maintenance_schedule = solve_job_shop(
    add_maintenance_jobs(operations_without_maintenance, no_maintenance_plan)
)

schedule_comparison = pd.DataFrame([
    {"case": "no preventive maintenance", "makespan": no_maintenance_makespan},
    {"case": "selected preventive maintenance", "makespan": makespan},
])
schedule_comparison
"""
        ),
        md(
            r"""
### Task 7 - scheduling interpretation

TODO: Selected preventive maintenance is scheduled before production on its station. How much does it increase planned makespan? Does the risk reduction justify the extra planned time in your result?
"""
        ),
        md(
            r"""
## 8. CPM/PERT project planning

The production schedule is only one part of the project. Now use the job-shop makespan as the duration of the `Produce batches` task in a CPM/PERT network.

New tool: `networkx`.

CPM treats the project as a directed graph:

- nodes are tasks,
- arrows point from predecessor to successor,
- earliest times come from a forward pass,
- latest times come from a backward pass,
- tasks with zero slack form the critical path.

PERT adds uncertainty by storing optimistic (`a`), most likely (`m`), and pessimistic (`b`) durations.
"""
        ),
        code(
            r"""
# Each row is a project task; predecessor strings name which tasks must finish first.
project_tasks = pd.DataFrame([
    {"id": "A", "task": "Collect price data", "a": 20, "m": 30, "b": 50, "predecessors": ""},
    {"id": "B", "task": "Validate forecasts", "a": 25, "m": 40, "b": 70, "predecessors": "A"},
    {"id": "C", "task": "Train failure model", "a": 30, "m": 50, "b": 90, "predecessors": ""},
    {"id": "D", "task": "Select maintenance plan", "a": 10, "m": 20, "b": 35, "predecessors": "C"},
    {"id": "E", "task": "Order ingredients", "a": 60, "m": 90, "b": 150, "predecessors": "B"},
    {"id": "F", "task": "Maintain selected machines", "a": 60, "m": 90, "b": 130, "predecessors": "D"},
    {"id": "G", "task": "Configure recipes", "a": 20, "m": 30, "b": 60, "predecessors": "B"},
    {"id": "H", "task": "Produce batches", "a": makespan * 0.90, "m": makespan, "b": makespan * 1.25, "predecessors": "E;F;G"},
    {"id": "I", "task": "Quality check", "a": 30, "m": 45, "b": 80, "predecessors": "H"},
    {"id": "J", "task": "Ship order", "a": 20, "m": 30, "b": 50, "predecessors": "I"},
])

# PERT expected duration and variance.
project_tasks["duration"] = (project_tasks["a"] + 4 * project_tasks["m"] + project_tasks["b"]) / 6
project_tasks["variance"] = ((project_tasks["b"] - project_tasks["a"]) / 6) ** 2
project_tasks
"""
        ),
        md(
            r"""
### Calculate project dates from the task table

`parse_predecessors(text)` converts a string such as `"E;F;G"` into the list
`["E", "F", "G"]`; a blank entry becomes an empty list. `.apply(...)` runs it
on each entry of the `predecessors` column.

`compute_cpm(tasks, duration_col="duration")` builds the directed graph and
visits tasks in **topological order**: predecessors come before successors.
The forward pass calculates earliest dates; the backward pass calculates
latest dates. Dictionary results are mapped back into table columns by task ID.

It returns three objects: the dated task table, the graph, and the project
finish time. The call below unpacks them into `cpm_table`, `project_graph`, and
`project_duration`. A `critical` row has zero slack; the displayed rows are the
critical-task set. Use predecessor links to trace a connected critical path.
"""
        ),
        code(
            r"""
def parse_predecessors(text):
    '''Convert a semicolon-separated predecessor entry to a list of task IDs.

    Args:
        text: A string such as "A;B", a blank value, or a missing pandas value.

    Returns:
        A list of trimmed nonempty labels; blank or missing input returns [].
    '''
    # Tasks with no predecessors must be represented by an empty list.
    if pd.isna(text) or str(text).strip() == "":
        return []
    return [item.strip() for item in str(text).split(";") if item.strip()]


def compute_cpm(tasks, duration_col="duration"):
    '''Compute earliest/latest dates and slack for an acyclic project network.

    Args:
        tasks: Table with unique id, predecessors (semicolon-separated IDs),
            and numeric duration_col entries. All named predecessors must exist.
        duration_col: Name of the duration column; defaults to "duration".

    Returns:
        (result, graph, project_finish): a copy with ES, EF, LS, LF, slack, and
        critical columns; a NetworkX DiGraph; and a numeric finish time.
        All time values use the duration column's units (minutes in this lab).
        Calls parse_predecessors. Raises ValueError if the graph contains a cycle.
    '''
    tasks = tasks.copy()
    tasks["pred_list"] = tasks["predecessors"].apply(parse_predecessors)

    # Build the project graph from predecessor links.
    graph = nx.DiGraph()
    for row in tasks.itertuples(index=False):
        graph.add_node(row.id)
        for pred in row.pred_list:
            graph.add_edge(pred, row.id)
    if not nx.is_directed_acyclic_graph(graph):
        raise ValueError("Project network must be acyclic.")

    duration = tasks.set_index("id")[duration_col].to_dict()
    topo = list(nx.topological_sort(graph))  # An order in which predecessor dates already exist.
    es, ef = {}, {}

    # Forward pass: earliest start/finish.
    for node in topo:
        preds = list(graph.predecessors(node))
        es[node] = max([ef[p] for p in preds], default=0)
        ef[node] = es[node] + duration[node]

    project_finish = max(ef.values())
    lf, ls = {}, {}

    # Backward pass: latest finish/start without delaying the project.
    for node in reversed(topo):
        succs = list(graph.successors(node))
        lf[node] = min([ls[s] for s in succs], default=project_finish)
        ls[node] = lf[node] - duration[node]

    # map selects each dictionary value using the ID in that table row.
    result = tasks.drop(columns=["pred_list"]).copy()
    result["ES"] = result["id"].map(es)
    result["EF"] = result["id"].map(ef)
    result["LS"] = result["id"].map(ls)
    result["LF"] = result["id"].map(lf)
    result["slack"] = result["LS"] - result["ES"]
    result["critical"] = np.isclose(result["slack"], 0)
    return result, graph, project_finish


cpm_table, project_graph, project_duration = compute_cpm(project_tasks)
critical_path = cpm_table.loc[cpm_table["critical"], ["id", "task", "duration"]]
print(f"Expected project duration: {project_duration:.1f} min")
critical_path
"""
        ),
        md(
            r"""
### From a standardized deadline to an approximate probability

`normal_cdf(x)` returns the probability that a standard normal variable is at
most `x`; for example, `normal_cdf(0)` is 0.5. The code converts the deadline
to a unitless z-score using the estimated project mean and standard deviation,
then calls this function.

The variance sum uses the rows marked critical in this example. Read the result
as a PERT approximation tied to that task set, not a guarantee; multiple
critical paths or changing paths need a more careful risk analysis.
"""
        ),
        code(
            r"""
def normal_cdf(x):
    '''Return the standard normal cumulative probability at a unitless z-score.

    Args:
        x: Numeric standardized value (e.g. deadline minus mean, divided by SD).

    Returns:
        A probability in [0, 1], calculated using the error function math.erf.
    '''
    # This identity converts the error function into a standard normal CDF.
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))


# Compare the deadline with the estimated mean in units of standard deviation.
deadline_min = 545
critical_variance = cpm_table.loc[cpm_table["critical"], "variance"].sum()
z_score = (deadline_min - project_duration) / math.sqrt(critical_variance)
deadline_probability = normal_cdf(z_score)

print(f"Deadline: {deadline_min} min")
print(f"Estimated probability of finishing by deadline: {deadline_probability:.1%}")
"""
        ),
        md(
            r"""
### Task 8 - CPM/PERT interpretation

TODO:

1. Which tasks are on the critical path?
2. Which non-critical task has the most slack?
3. If the project is late, which task would you crash first and why?
"""
        ),
        md(
            r"""
## 9. Scenario analysis

A useful operations plan should be tested under stress. The function below reruns the integrated pipeline under changed prices, failure risk, and maintenance capacity.

Scenario analysis answers "what if?" questions. Here each scenario reruns the same pipeline:

forecast prices -> blending LP -> maintenance optimization -> job-shop schedule -> cost summary

The point is to see whether the recommendation is stable or whether one assumption changes the decision.

### Read `run_scenario` as a sequence of five decisions

The arguments describe the **changed assumptions**: a scenario name, general
or ingredient-specific price multipliers, a risk multiplier, technician
minutes, and whether maintenance is allowed. Defaults reproduce the base case;
`ingredient_multipliers={"chicken": 2.0}` changes only chicken's price.

The numbered stages copy and change inputs, re-solve recipes, choose maintenance,
rebuild the operation schedule, and summarize costs. The returned dictionary
contains one scenario's business results; it does not contain every intermediate
recipe or schedule. Global baseline tables are used for comparison and remain
unchanged. Read each function call as the next stage's input preparation.

In `run_scenario(**kwargs)`, `**` unpacks a dictionary into named arguments:
`{"scenario_name": "base"}` acts like `run_scenario(scenario_name="base")`.
The final list of dictionaries becomes the rows of `scenario_results`.
"""
        ),
        code(
            r"""
def run_scenario(
    scenario_name,
    price_multiplier=1.0,
    ingredient_multipliers=None,
    failure_multiplier=1.0,
    technician_time_limit=TECHNICIAN_TIME_LIMIT_MIN,
    allow_maintenance=True,
):
    '''Re-optimize a complete operations scenario and return one summary dictionary.

    Args:
        scenario_name: Label for the result row.
        price_multiplier: Multiplier for every forecast price; defaults to 1.0.
        ingredient_multipliers: Optional ingredient-to-price-multiplier dictionary;
            applied in addition to price_multiplier, defaults to None.
        failure_multiplier: Multiplier for failure probabilities, capped at 1;
            defaults to 1.0.
        technician_time_limit: Available service minutes; defaults to the configured limit.
        allow_maintenance: True (default) optimizes service; False selects no service.

    Returns:
        A dictionary with scenario, ingredient_cost, maintenance_cost,
        expected_failure_loss, total_expected_cost (common teaching currency),
        makespan (minutes), late_jobs (count), maintained_machines (label string),
        and max_recipe_share_change (fraction relative to baseline).
        Uses forecast_prices, orders, ingredients, recipe_shares, machine_risk,
        operations_without_maintenance, MAINTENANCE_BUDGET, and the solving helpers.
        Solver failures propagate from those helpers; inputs are copied before changes.
    '''
    # 1. Adjust the forecast table for the scenario.
    scenario_prices = forecast_prices.copy()
    scenario_prices["forecast_cost"] = scenario_prices["forecast_cost"] * price_multiplier
    if ingredient_multipliers is not None:
        for ingredient, multiplier in ingredient_multipliers.items():
            mask = scenario_prices["ingredient"] == ingredient
            scenario_prices.loc[mask, "forecast_cost"] *= multiplier

    # 2. Re-solve all recipe LPs with the adjusted prices.
    scenario_recipes = pd.concat(
        [
            solve_blend(row.product, row.target_month, scenario_prices, orders, ingredients)
            for row in orders.itertuples(index=False)
        ],
        ignore_index=True,
    )
    scenario_recipe_shares = scenario_recipes.merge(
        # Attach order masses to ingredient rows using both product and delivery month.
        orders[["product", "target_month", "demand_kg"]],
        on=["product", "target_month"],
        how="left",
    )
    scenario_recipe_shares["share"] = (
        scenario_recipe_shares["kg"] / scenario_recipe_shares["demand_kg"]
    )
    share_comparison = scenario_recipe_shares.merge(
        recipe_shares[["product", "target_month", "ingredient", "share"]].rename(
            columns={"share": "base_share"}
        ),
        on=["product", "target_month", "ingredient"],
        how="left",
    )
    # A share difference compares recipe composition even when batch masses differ.
    max_recipe_share_change = (
        share_comparison["share"] - share_comparison["base_share"]
    ).abs().max()

    # 3. Adjust machine risk and re-solve maintenance.
    scenario_risk = machine_risk.copy()
    scenario_risk["p_failure"] = np.minimum(1.0, scenario_risk["p_failure"] * failure_multiplier)
    scenario_risk["expected_avoided_loss"] = (
        scenario_risk["p_failure"]
        * scenario_risk["failure_cost"]
        * scenario_risk["risk_reduction"]
    )
    if allow_maintenance:
        scenario_maintenance = solve_maintenance_plan(
            scenario_risk,
            technician_time_limit,
            MAINTENANCE_BUDGET,
        )
    else:
        scenario_maintenance = scenario_risk.copy()
        scenario_maintenance["maintain"] = 0
        scenario_maintenance["net_value"] = scenario_maintenance["expected_avoided_loss"] - scenario_maintenance["service_cost"]

    # 4. Rebuild and solve the robot-cell schedule.
    scenario_operations = add_maintenance_jobs(operations_without_maintenance, scenario_maintenance)
    scenario_makespan, scenario_schedule = solve_job_shop(scenario_operations)

    # 5. Summarize the business outcomes.
    ingredient_cost = scenario_recipes["cost"].sum()
    maintenance_cost = scenario_maintenance.loc[
        scenario_maintenance["maintain"] == 1, "service_cost"
    ].sum()
    maintained_machines = ",".join(
        str(int(machine_id))
        for machine_id in scenario_maintenance.loc[
            scenario_maintenance["maintain"] == 1, "machine_id"
        ]
    )
    expected_failure_loss = (
        scenario_maintenance["p_failure"]
        * scenario_maintenance["failure_cost"]
        * (1 - scenario_maintenance["risk_reduction"] * scenario_maintenance["maintain"])
    ).sum()
    late_jobs = (
        # Count jobs finishing after their due time; exclude maintenance with no due date.
        scenario_schedule.dropna(subset=["due_min"])
        .groupby("job")
        .apply(lambda group: group["end"].max() > group["due_min"].iloc[0])
        .sum()
    )

    return {
        "scenario": scenario_name,
        "ingredient_cost": ingredient_cost,
        "maintenance_cost": maintenance_cost,
        "expected_failure_loss": expected_failure_loss,
        "makespan": scenario_makespan,
        "late_jobs": int(late_jobs),
        "maintained_machines": maintained_machines if maintained_machines else "none",
        "max_recipe_share_change": float(max_recipe_share_change),
        "total_expected_cost": ingredient_cost + maintenance_cost + expected_failure_loss,
    }


# Each dictionary supplies only the assumptions that differ from the function defaults.
scenario_inputs = [
    {"scenario_name": "base"},
    {
        "scenario_name": "chicken supply shock",
        "ingredient_multipliers": {"chicken": 2.00},
    },
    {"scenario_name": "high failure risk", "failure_multiplier": 1.40},
    {"scenario_name": "tight maintenance capacity", "technician_time_limit": 60},
    {"scenario_name": "no preventive maintenance", "allow_maintenance": False},
]

scenario_results = pd.DataFrame([run_scenario(**kwargs) for kwargs in scenario_inputs])
scenario_results
"""
        ),
        md(
            r"""
### Task 9 - scenario interpretation

TODO: Which scenario changes the decision the most? Look for changes in recipe shares, selected maintenance, makespan, late jobs, and total expected cost. Is your base plan robust, or does one stress case force a different recommendation?
"""
        ),
        md(
            r"""
## 10. Final recommendation

Write a short operations memo. Your memo must answer:

1. Which recipes should be used in June and September?
2. Which machines should receive preventive maintenance?
3. What is the expected production cost?
4. What is the planned robot-cell makespan?
5. What is the critical path of the overall project?
6. What is the largest operational risk?
7. What changes under the chicken-supply-shock or high-failure scenario?
8. What decision would you recommend to management?
"""
        ),
    ]
    # Fixed IDs keep regenerated teaching notebooks stable in version control.
    for index, cell in enumerate(cells):
        cell["id"] = f"lab6-{index:02d}"
    nb["cells"] = cells
    return nb


def main() -> None:
    build_lab6_data()
    nb = build_notebook()
    for cell in nb["cells"]:
        if cell["cell_type"] == "code":
            cell["execution_count"] = None
            cell["outputs"] = []
    nbf.write(nb, NOTEBOOK_PATH)
    print(f"Wrote {NOTEBOOK_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
