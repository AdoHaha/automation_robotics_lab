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
"""
        ),
        code(
            r"""
# In Google Colab, uncomment and run once if needed:
# %pip install pandas numpy matplotlib networkx pulp scikit-learn statsmodels

from __future__ import annotations

import math
import re
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
np.random.seed(RANDOM_SEED)
warnings.filterwarnings("ignore", category=FutureWarning)

DATA_DIR = Path("data")
TARGET_MONTHS = [pd.Timestamp("2026-06-01"), pd.Timestamp("2026-09-01")]
TECHNICIAN_TIME_LIMIT_MIN = 120
MAINTENANCE_BUDGET = 1200
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

The live data source is FRED. The suggested series are:

| Ingredient | FRED series | Original unit |
|---|---:|---|
| beef | `APU0000703112` | USD/lb |
| eggs | `APU0000708111` | USD/dozen |
| milk | `APU0000709112` | USD/gallon |
| chicken | `APU0000FF1101` | USD/lb |

The notebook also includes `data/lab6_price_fallback.csv`, so the exercise still works offline.
"""
        ),
        code(
            r"""
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
    '''Load a FRED monthly price series and convert it to a tidy DataFrame.

    If live loading fails, return the offline fallback rows for that ingredient.
    '''
    if not use_live:
        return fallback_df[fallback_df["ingredient"] == ingredient].copy()

    url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={series_id}"
    try:
        raw = pd.read_csv(url)
        date_col = raw.columns[0]
        value_col = raw.columns[1]
        df = raw.rename(columns={date_col: "date", value_col: "raw_value"})
        df["date"] = pd.to_datetime(df["date"])
        df["raw_value"] = pd.to_numeric(df["raw_value"], errors="coerce")
        df = df.dropna(subset=["raw_value"])

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
"""
        ),
        code(
            r"""
def train_test_split_series(y, test_size=12):
    if len(y) <= test_size + 12:
        raise ValueError("Need more history for a 12-month validation split.")
    return y.iloc[:-test_size], y.iloc[-test_size:]


def seasonal_naive_forecast(train, horizon, season_length=12):
    values = [train.iloc[-season_length + (h % season_length)] for h in range(horizon)]
    return pd.Series(values)


def drift_forecast(train, horizon):
    x = np.arange(len(train))
    coef = np.polyfit(x, train.values, deg=1)
    future_x = np.arange(len(train), len(train) + horizon)
    return pd.Series(np.polyval(coef, future_x))


def exponential_smoothing_forecast(train, horizon):
    try:
        model = ExponentialSmoothing(
            train,
            trend="add",
            seasonal="add",
            seasonal_periods=12,
            initialization_method="estimated",
        )
        fit = model.fit(optimized=True)
        return pd.Series(fit.forecast(horizon).values)
    except Exception:
        return drift_forecast(train, horizon)


def mape(y_true, y_pred):
    y_true = np.asarray(y_true)
    y_pred = np.asarray(y_pred)
    mask = y_true != 0
    return float(np.mean(np.abs((y_true[mask] - y_pred[mask]) / y_true[mask])))


def evaluate_forecasters(price_df, ingredient):
    series = (
        price_df[price_df["ingredient"] == ingredient]
        .sort_values("date")
        .set_index("date")["cost_per_kg"]
        .asfreq("MS")
        .interpolate()
    )
    train, test = train_test_split_series(series, test_size=12)
    predictions = {
        "seasonal_naive": seasonal_naive_forecast(train, len(test)),
        "drift": drift_forecast(train, len(test)),
        "exp_smoothing": exponential_smoothing_forecast(train, len(test)),
    }
    rows = []
    for model_name, pred in predictions.items():
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
        code(
            r"""
def forecast_targets(price_df, target_months):
    rows = []
    for ingredient in ingredients["ingredient"]:
        series = (
            price_df[price_df["ingredient"] == ingredient]
            .sort_values("date")
            .set_index("date")["cost_per_kg"]
            .asfreq("MS")
            .interpolate()
        )
        scores = evaluate_forecasters(price_df, ingredient)
        selected = scores.sort_values("MAE").iloc[0]
        last_date = series.index.max()
        horizon = max((month.to_period("M") - last_date.to_period("M")).n for month in target_months)

        if selected["model"] == "seasonal_naive":
            pred = seasonal_naive_forecast(series, horizon)
        elif selected["model"] == "drift":
            pred = drift_forecast(series, horizon)
        else:
            pred = exponential_smoothing_forecast(series, horizon)

        for month in target_months:
            step = (month.to_period("M") - last_date.to_period("M")).n
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
"""
        ),
        code(
            r"""
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
        code(
            r"""
def make_failure_features(df):
    df = df.sort_values(["instance_id", "time"]).copy()
    grouped = df.groupby("instance_id", group_keys=False)

    df["temp_roll_mean_3"] = (
        grouped["sensor_temp"].rolling(3, min_periods=1).mean().reset_index(level=0, drop=True)
    )
    df["vib_roll_mean_3"] = (
        grouped["sensor_vib"].rolling(3, min_periods=1).mean().reset_index(level=0, drop=True)
    )
    df["vib_roll_max_3"] = (
        grouped["sensor_vib"].rolling(3, min_periods=1).max().reset_index(level=0, drop=True)
    )
    df["temp_change"] = grouped["sensor_temp"].diff().fillna(0)
    df["vib_change"] = grouped["sensor_vib"].diff().fillna(0)

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

instances = features_df["instance_id"].drop_duplicates().sample(frac=1, random_state=RANDOM_SEED)
split = int(0.75 * len(instances))
train_instances = set(instances.iloc[:split])
test_instances = set(instances.iloc[split:])

train_df = features_df[features_df["instance_id"].isin(train_instances)]
test_df = features_df[features_df["instance_id"].isin(test_instances)]

X_train = train_df[feature_cols]
y_train = train_df["near_failure"]
X_test = test_df[feature_cols]
y_test = test_df["near_failure"]

print(X_train.shape, X_test.shape)
print("Train failure rate:", y_train.mean().round(4))
print("Test failure rate:", y_test.mean().round(4))
"""
        ),
        code(
            r"""
def positive_class_probability(model, X):
    if hasattr(model, "predict_proba"):
        return model.predict_proba(X)[:, 1]
    return model.decision_function(X)


def evaluate_classifier(y_true, p_hat, threshold=0.5):
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
    "logistic_regression": make_pipeline(
        StandardScaler(),
        LogisticRegression(max_iter=2000, class_weight="balanced"),
    ),
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
        code(
            r"""
def expected_classification_cost(
    y_true,
    p_hat,
    threshold,
    false_negative_cost=5000,
    false_positive_cost=600,
):
    y_pred = (p_hat >= threshold).astype(int)
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
    return fp * false_positive_cost + fn * false_negative_cost


def choose_threshold_by_cost(
    y_true,
    p_hat,
    false_negative_cost=5000,
    false_positive_cost=600,
):
    rows = []
    for threshold in np.linspace(0.05, 0.95, 19):
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
    best = result.sort_values("expected_cost").iloc[0]
    return best, result


best_threshold, threshold_table = choose_threshold_by_cost(y_test, best_p_hat)
display(threshold_table)
best_threshold
"""
        ),
        code(
            r"""
latest_rows = (
    features_df.sort_values(["instance_id", "time"])
    .groupby("instance_id", as_index=False)
    .tail(1)
    .copy()
)
latest_rows["p_failure"] = best_model.predict_proba(latest_rows[feature_cols])[:, 1]

machine_risk = (
    latest_rows.groupby("machine_id")
    .agg(
        p_failure=("p_failure", "mean"),
        current_temp=("sensor_temp", "mean"),
        current_vib=("sensor_vib", "mean"),
    )
    .reset_index()
    .merge(maintenance_options, on="machine_id", how="left")
)
machine_risk["expected_avoided_loss"] = (
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
"""
        ),
        code(
            r"""
def solve_blend(product_name, target_month, price_table, orders, ingredients, price_col="forecast_cost"):
    order_row = orders[
        (orders["product"] == product_name)
        & (orders["target_month"] == pd.Timestamp(target_month))
    ].iloc[0]
    demand = float(order_row["demand_kg"])
    prices = (
        price_table[price_table["target_month"] == pd.Timestamp(target_month)]
        .set_index("ingredient")[price_col]
        .to_dict()
    )

    model_name = f"blend_{re.sub(r'[^A-Za-z0-9_]+', '_', product_name)}_{pd.Timestamp(target_month):%Y_%m}"
    model = pulp.LpProblem(model_name, pulp.LpMinimize)
    x = {
        row.ingredient: pulp.LpVariable(f"kg_{row.ingredient}", lowBound=0)
        for row in ingredients.itertuples(index=False)
    }

    model += pulp.lpSum(prices[i] * x[i] for i in x)
    model += pulp.lpSum(x[i] for i in x) == demand
    model += pulp.lpSum(row.protein * x[row.ingredient] for row in ingredients.itertuples(index=False)) >= float(order_row["min_protein"]) * demand
    model += pulp.lpSum(row.fat * x[row.ingredient] for row in ingredients.itertuples(index=False)) >= float(order_row["min_fat"]) * demand
    model += pulp.lpSum(row.moisture * x[row.ingredient] for row in ingredients.itertuples(index=False)) <= float(order_row["max_moisture"]) * demand

    for row in ingredients.itertuples(index=False):
        model += x[row.ingredient] >= float(row.min_share) * demand
        model += x[row.ingredient] <= float(row.max_share) * demand

    status = model.solve(pulp.PULP_CBC_CMD(msg=False))
    if pulp.LpStatus[status] != "Optimal":
        raise ValueError(f"Blend model did not solve optimally: {pulp.LpStatus[status]}")

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


recipe_plan = pd.concat(
    [
        solve_blend(row.product, row.target_month, forecast_prices, orders, ingredients)
        for row in orders.itertuples(index=False)
    ],
    ignore_index=True,
)

display(recipe_plan)
recipe_summary = recipe_plan.groupby(["product", "target_month"], as_index=False)["cost"].sum()
recipe_summary
"""
        ),
        md(
            r"""
### Task 5 - blending interpretation

TODO: Compare June and September recipes. Which ingredient quantities change, and are those changes explained by forecasted prices or by nutrition constraints?
"""
        ),
        md(
            r"""
## 6. Preventive-maintenance binary optimization

The ML model estimates failure probability. The maintenance model turns that estimate into a decision.
"""
        ),
        code(
            r"""
def solve_maintenance_plan(machine_risk, time_limit_min, budget):
    model = pulp.LpProblem("maintenance_selection", pulp.LpMaximize)
    z = {
        int(row.machine_id): pulp.LpVariable(f"maintain_{int(row.machine_id)}", cat="Binary")
        for row in machine_risk.itertuples(index=False)
    }
    net_value = {
        int(row.machine_id): float(row.expected_avoided_loss - row.service_cost)
        for row in machine_risk.itertuples(index=False)
    }

    model += pulp.lpSum(net_value[m] * z[m] for m in z)
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
"""
        ),
        code(
            r"""
def build_job_operations(orders, routes, reference_batch_kg=500):
    rows = []
    for batch in orders.itertuples(index=False):
        route = routes[routes["product"] == batch.product].sort_values("operation")
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
    rows = operations.to_dict("records")
    for row in maintenance_plan[maintenance_plan["maintain"] == 1].itertuples(index=False):
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
        code(
            r"""
def safe_name(text):
    return re.sub(r"[^A-Za-z0-9_]+", "_", str(text)).strip("_")


def solve_job_shop(operations):
    operations = operations.copy().reset_index(drop=True)
    operations["op_id"] = operations.index
    horizon = int(operations["duration"].sum() + 100)

    model = pulp.LpProblem("robot_cell_job_shop", pulp.LpMinimize)
    start = {
        row.op_id: pulp.LpVariable(f"start_{row.op_id}_{safe_name(row.job)}", lowBound=0)
        for row in operations.itertuples(index=False)
    }
    c_max = pulp.LpVariable("makespan", lowBound=0)

    # Route order inside each job.
    for job, group in operations.groupby("job"):
        group = group.sort_values("operation")
        for prev, nxt in zip(group.itertuples(index=False), list(group.itertuples(index=False))[1:]):
            model += start[nxt.op_id] >= start[prev.op_id] + float(prev.duration)

    # No overlap on the same station.
    for station, group in operations.groupby("station"):
        rows = list(group.itertuples(index=False))
        for a, b in combinations(rows, 2):
            y = pulp.LpVariable(f"{safe_name(station)}_{a.op_id}_before_{b.op_id}", cat="Binary")
            model += start[a.op_id] + float(a.duration) <= start[b.op_id] + horizon * (1 - y)
            model += start[b.op_id] + float(b.duration) <= start[a.op_id] + horizon * y

    for row in operations.itertuples(index=False):
        model += c_max >= start[row.op_id] + float(row.duration)

    model += c_max
    status = model.solve(pulp.PULP_CBC_CMD(msg=False))
    if pulp.LpStatus[status] != "Optimal":
        raise ValueError(f"Schedule model did not solve optimally: {pulp.LpStatus[status]}")

    schedule = operations.copy()
    schedule["start"] = schedule["op_id"].map(lambda op_id: pulp.value(start[op_id]))
    schedule["end"] = schedule["start"] + schedule["duration"]
    return float(pulp.value(c_max)), schedule.sort_values(["start", "station"])


def validate_schedule(schedule, tolerance=1e-7):
    errors = []
    for job, group in schedule.groupby("job"):
        group = group.sort_values("operation")
        previous_end = None
        for row in group.itertuples(index=False):
            if previous_end is not None and row.start + tolerance < previous_end:
                errors.append(f"Route violation for {job}")
            previous_end = row.end

    for station, group in schedule.groupby("station"):
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
        code(
            r"""
def plot_gantt(schedule, title="Robot-cell schedule"):
    fig, ax = plt.subplots(figsize=(11, 0.45 * schedule["job"].nunique() + 2))
    jobs = list(schedule["job"].drop_duplicates())
    y_pos = {job: idx for idx, job in enumerate(jobs)}
    station_colors = {
        station: color
        for station, color in zip(
            schedule["station"].drop_duplicates(),
            plt.cm.Set2(np.linspace(0, 1, schedule["station"].nunique())),
        )
    }
    for row in schedule.itertuples(index=False):
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

TODO: Preventive maintenance usually increases planned makespan. Does the risk reduction justify the extra planned time in your result?
"""
        ),
        md(
            r"""
## 8. CPM/PERT project planning

The production schedule is only one part of the project. Now use the job-shop makespan as the duration of the `Produce batches` task in a CPM/PERT network.
"""
        ),
        code(
            r"""
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

project_tasks["duration"] = (project_tasks["a"] + 4 * project_tasks["m"] + project_tasks["b"]) / 6
project_tasks["variance"] = ((project_tasks["b"] - project_tasks["a"]) / 6) ** 2
project_tasks
"""
        ),
        code(
            r"""
def parse_predecessors(text):
    if pd.isna(text) or str(text).strip() == "":
        return []
    return [item.strip() for item in str(text).split(";") if item.strip()]


def compute_cpm(tasks, duration_col="duration"):
    tasks = tasks.copy()
    tasks["pred_list"] = tasks["predecessors"].apply(parse_predecessors)
    graph = nx.DiGraph()
    for row in tasks.itertuples(index=False):
        graph.add_node(row.id)
        for pred in row.pred_list:
            graph.add_edge(pred, row.id)
    if not nx.is_directed_acyclic_graph(graph):
        raise ValueError("Project network must be acyclic.")

    duration = tasks.set_index("id")[duration_col].to_dict()
    topo = list(nx.topological_sort(graph))
    es, ef = {}, {}
    for node in topo:
        preds = list(graph.predecessors(node))
        es[node] = max([ef[p] for p in preds], default=0)
        ef[node] = es[node] + duration[node]

    project_finish = max(ef.values())
    lf, ls = {}, {}
    for node in reversed(topo):
        succs = list(graph.successors(node))
        lf[node] = min([ls[s] for s in succs], default=project_finish)
        ls[node] = lf[node] - duration[node]

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
        code(
            r"""
def normal_cdf(x):
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))


deadline_min = 760
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
"""
        ),
        code(
            r"""
def run_scenario(
    scenario_name,
    price_multiplier=1.0,
    failure_multiplier=1.0,
    technician_time_limit=TECHNICIAN_TIME_LIMIT_MIN,
    allow_maintenance=True,
):
    scenario_prices = forecast_prices.copy()
    scenario_prices["forecast_cost"] = scenario_prices["forecast_cost"] * price_multiplier

    scenario_recipes = pd.concat(
        [
            solve_blend(row.product, row.target_month, scenario_prices, orders, ingredients)
            for row in orders.itertuples(index=False)
        ],
        ignore_index=True,
    )

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

    scenario_operations = add_maintenance_jobs(operations_without_maintenance, scenario_maintenance)
    scenario_makespan, scenario_schedule = solve_job_shop(scenario_operations)

    ingredient_cost = scenario_recipes["cost"].sum()
    maintenance_cost = scenario_maintenance.loc[
        scenario_maintenance["maintain"] == 1, "service_cost"
    ].sum()
    expected_failure_loss = (
        scenario_maintenance["p_failure"]
        * scenario_maintenance["failure_cost"]
        * (1 - scenario_maintenance["risk_reduction"] * scenario_maintenance["maintain"])
    ).sum()
    late_jobs = (
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
        "total_expected_cost": ingredient_cost + maintenance_cost + expected_failure_loss,
    }


scenario_inputs = [
    {"scenario_name": "base"},
    {"scenario_name": "high ingredient prices", "price_multiplier": 1.15},
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

TODO: Which scenario changes the decision the most? Is your base plan robust, or does one stress case force a different recommendation?
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
7. What changes under the high-price or high-failure scenario?
8. What decision would you recommend to management?
"""
        ),
    ]
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
