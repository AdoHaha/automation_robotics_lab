"""Generate the self-contained, Colab-ready Lab 2 blending notebook."""
from pathlib import Path
import textwrap
import nbformat as nbf

ROOT = Path(__file__).resolve().parents[1]


def build_notebook():
    cells = []

    def md(source):
        cells.append(nbf.v4.new_markdown_cell(textwrap.dedent(source).strip()))

    def code(source):
        cells.append(nbf.v4.new_code_cell(textwrap.dedent(source).strip()))

    md(r'''
    # Lab 2: Blending — design a low-cost recipe

    [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/AdoHaha/automation_robotics_lab/blob/master/lab_auto_2.ipynb)

    A robotic mixer prepares **100 kg of a teaching pet-food blend**. Five ingredients have different costs and compositions. Can we meet the quality targets without overspending?

    This is the classic **blending linear program**: choose ingredient quantities, minimize cost, and meet weighted-average specifications. The same idea appears in alloys, fuel, fertilizers, and food production.

    Lab 0 explored Python tables, plotting, and controls; Lab 1 used PuLP to choose a product mix. Here the same tools choose a recipe. Work through the recipe, units, and margins, then compare sensitivity and build a custom control. The supplied checking and plotting helpers support experiments with the model equations and their results.

    By the end you will be able to:

    - translate recipe percentages into linear constraints with consistent units;
    - build and interpret a PuLP minimization model;
    - check recipe quality, binding constraints, and infeasibility;
    - explore cost–quality trade-offs with plots, sliders, and local sensitivity;
    - recommend a recipe using evidence.

    Run the cells from top to bottom with **Runtime → Run all** in Google Colab. All data and diagrams are included in this notebook. The package install needs internet once; the experiments need no external files. These simplified compositions and prices are teaching data, not real formulation advice.
    ''')
    code('''
    # Install the notebook libraries into this runtime, including the course PuLP API.
    %pip install -q 'pulp>=3.3,<4' numpy pandas matplotlib ipywidgets

    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    from matplotlib.patches import FancyBboxPatch
    from IPython.display import display, clear_output
    import ipywidgets as widgets
    import pulp

    # Colab needs this for custom widget rendering; ordinary Jupyter does not.
    try:
        from google.colab import output
        output.enable_custom_widget_manager()
    except ImportError:
        pass

    plt.rcParams.update({"figure.dpi": 110, "axes.spines.top": False,
                         "axes.spines.right": False})
    SOLVER = pulp.PULP_CBC_CMD(msg=False)
    print("PuLP", pulp.__version__, "| CBC available:", bool(SOLVER.available()))
    if not SOLVER.available():
        raise RuntimeError("CBC is missing. Rerun the install cell in a fresh Colab runtime.")
    ''')
    md('''
    ## 1. Read the recipe story

    The purchasing team supplies five ingredients. The mixer can measure fractional kilograms, so quantities are **continuous variables**. A recipe must contain exactly the requested batch mass.

    Every row below describes **one kilogram** of an ingredient. For example, `protein = 0.38` means 0.38 kg protein per kg chicken, or 38% protein by mass. The rest of the mass can include carbohydrates, ash, and other components; the listed fractions need not sum to one.

    The share limits reflect practical recipe rules: at least 10% chicken and 5% plant filler, and no more than the stated maximum shares. They are proportional limits, not warehouse stock limits.
    ''')
    code('''
    # Embed per-kg prices/compositions and proportional recipe limits for reproducible experiments.
    ingredients = pd.DataFrame([
        # name,       PLN/kg, protein, fat, moisture, min share, max share
        ("chicken",      6.95,   0.380, 0.090, 0.46, 0.10, 0.60),
        ("beef",         9.60,   0.340, 0.170, 0.40, 0.00, 0.45),
        ("eggs",         5.40,   0.130, 0.110, 0.72, 0.00, 0.25),
        ("milk",         1.15,   0.034, 0.033, 0.88, 0.00, 0.20),
        ("plant_filler", 1.05,   0.160, 0.030, 0.10, 0.05, 0.35),
    ], columns=["ingredient", "cost_pln_per_kg", "protein", "fat", "moisture",
                "min_share", "max_share"]).set_index("ingredient")

    # Reuse ingredient colors across the story, recipe charts, and quality sweeps.
    COLORS = dict(zip(ingredients.index,
                      ["#4393c3", "#b35806", "#e8b923", "#8073ac", "#49a06c"]))
    display(ingredients)
    ''')
    code('''
    # Draw ingredient inputs, their arrows, and the mixer output without external image files.
    fig, ax = plt.subplots(figsize=(11, 4.5))
    ax.set(xlim=(0, 11), ylim=(-0.8, 4.8))
    ax.axis("off")
    for y, (name, row) in enumerate(ingredients.iterrows()):
        box = FancyBboxPatch((0.1, y - 0.33), 3.5, 0.66, boxstyle="round,pad=0.05",
                             facecolor=COLORS[name], edgecolor="white", alpha=0.25)
        ax.add_patch(box)
        ax.text(0.25, y, f"{name.replace('_', ' ').title()}  |  {row.cost_pln_per_kg:.2f} PLN/kg"
                f"\\nProtein {row.protein:.1%}; fat {row.fat:.1%}", va="center", fontsize=10)
        ax.annotate("", xy=(5, 2), xytext=(3.7, y),
                    arrowprops={"arrowstyle": "->", "color": COLORS[name], "lw": 1.8})
    ax.add_patch(FancyBboxPatch((5, 1.25), 2.2, 1.5, boxstyle="round,pad=0.1",
                               facecolor="#e6edf3", edgecolor="#345"))
    ax.text(6.1, 2, "ROBOTIC MIXER\\nChoose kg of each\\ningredient", ha="center", va="center")
    ax.annotate("", xy=(8.1, 2), xytext=(7.25, 2), arrowprops={"arrowstyle": "->", "lw": 2})
    ax.text(9.4, 2, "100 kg batch\\nProtein ≥ 24%\\nFat ≥ 8%\\nMoisture ≤ 60%", ha="center", va="center",
            bbox={"boxstyle": "round", "facecolor": "#edf7ed", "edgecolor": "#486"})
    ax.set_title("Input compositions → recipe decisions → quality targets", fontsize=14)
    plt.show()
    ''')
    md(r'''
    ### Predict before you run

    1. Which ingredient is cheapest? Why might an all-cheapest recipe fail?
    2. Is the ingredient with the most protein necessarily the best purchase? Compare **cost per kg protein**, then explain why that ratio alone cannot choose the full recipe.
    3. If the batch doubles and all rules are percentages, do you expect different ingredient shares?

    ## 2. Warm-up: only chicken and plant filler

    Ignore fat, moisture, and share limits for a moment. Make 100 kg with at least 24% protein. Let $c$ be chicken kg and $f$ be filler kg:

    $$\min 6.95c + 1.05f,\qquad c+f=100,\qquad 0.38c+0.16f\geq24,\qquad c,f\geq0.$$

    Substitute $f=100-c$ by hand. What is the smallest feasible $c$? Because chicken costs more, that boundary is the cheapest feasible recipe. Predict the answer before executing the PuLP version.
    ''')
    code('''
    # Build the two-ingredient cost model so every equation is visible before generalization.
    warmup = pulp.LpProblem("Two_ingredient_recipe", pulp.LpMinimize)
    chicken_kg = pulp.LpVariable("chicken_kg", lowBound=0)
    filler_kg = pulp.LpVariable("filler_kg", lowBound=0)
    warmup += 6.95 * chicken_kg + 1.05 * filler_kg, "Cost_PLN"
    warmup += chicken_kg + filler_kg == 100, "Batch_kg"
    warmup += 0.38 * chicken_kg + 0.16 * filler_kg >= 24, "Protein_kg"
    # Check the solve status before plotting or reading a candidate recipe.
    warmup.solve(SOLVER)
    warmup_status = pulp.LpStatus[warmup.status]
    print("Status:", warmup_status)
    if warmup_status == "Optimal":
        print(f"Chicken: {chicken_kg.value():.2f} kg; filler: {filler_kg.value():.2f} kg")
        print(f"Cost: {pulp.value(warmup.objective):.2f} PLN")
        # With filler = 100 - chicken, one grid shows both quality and cost.
        grid = np.linspace(0, 100, 301)
        protein_percent = 0.38 * grid + 0.16 * (100 - grid)
        costs = 6.95 * grid + 1.05 * (100 - grid)
        fig, axes = plt.subplots(1, 2, figsize=(10, 3.5))
        axes[0].plot(grid, protein_percent)
        axes[0].axhline(24, color="#ba332b", linestyle="--", label="24% target")
        axes[0].fill_between(grid, 0, 40, where=protein_percent >= 24, color="#68ab75", alpha=0.15)
        axes[0].set(xlabel="Chicken in 100 kg batch (kg)", ylabel="Protein (%)", ylim=(0, 40))
        axes[0].legend()
        axes[1].plot(grid, costs)
        axes[1].scatter([chicken_kg.value()], [pulp.value(warmup.objective)], color="#ba332b",
                        zorder=3, label="Cheapest feasible recipe")
        axes[1].set(xlabel="Chicken in 100 kg batch (kg)", ylabel="Batch cost (PLN)")
        axes[1].legend()
        plt.tight_layout()
        plt.show()
    ''')
    md(r'''
    ## 3. From two ingredients to a full linear program

    Let $x_i$ be **kg of ingredient $i$** and $B=100$ kg the fixed batch size. For each ingredient, $c_i$ is PLN/kg, $p_i$, $f_i$, and $m_i$ are nutrient mass fractions, and $l_i$, $u_i$ are share bounds.

    $$\begin{aligned}
    \min\quad &\sum_i c_i x_i &&\text{cost in PLN}\\
    \text{subject to}\quad &\sum_i x_i=B &&\text{batch mass in kg}\\
    &\sum_i p_i x_i\geq 0.24B &&\text{at least 24 kg protein per 100 kg}\\
    &\sum_i f_i x_i\geq 0.08B &&\text{at least 8 kg fat per 100 kg}\\
    &\sum_i m_i x_i\leq 0.60B &&\text{at most 60 kg water per 100 kg}\\
    &l_i B\leq x_i\leq u_i B &&\text{ingredient share bounds.}
    \end{aligned}$$

    **Why linear?** Weighted-average protein is $\sum_i p_i x_i/B$. Since $B$ is a positive fixed input, multiply both sides of the percentage requirement by $B$. All coefficients are constants; we never multiply two decision variables. A share formulation using $s_i=x_i/B$ is also linear, with $\sum_i s_i=1$.

    **Units check:** `(kg protein / kg ingredient) × kg ingredient = kg protein`. Entering `24` instead of `0.24` on the right side would ask for 2400 kg protein in a 100 kg batch.

    First read this explicit model. Match each code line to one line of the equations.
    ''')
    code('''
    # Express decisions as ingredient kg; fixed batch mass converts percentages to kg targets.
    batch_kg = 100
    full_model = pulp.LpProblem("Five_ingredient_recipe", pulp.LpMinimize)
    x = {name: pulp.LpVariable(f"kg_{name}", lowBound=0) for name in ingredients.index}
    full_model += pulp.lpSum(ingredients.loc[i, "cost_pln_per_kg"] * x[i] for i in x), "Cost_PLN"
    full_model += pulp.lpSum(x.values()) == batch_kg, "Batch_kg"
    full_model += pulp.lpSum(ingredients.loc[i, "protein"] * x[i] for i in x) >= 0.24 * batch_kg, "Protein_kg"
    full_model += pulp.lpSum(ingredients.loc[i, "fat"] * x[i] for i in x) >= 0.08 * batch_kg, "Fat_kg"
    full_model += pulp.lpSum(ingredients.loc[i, "moisture"] * x[i] for i in x) <= 0.60 * batch_kg, "Moisture_kg"
    for i in x:
        full_model += x[i] >= ingredients.loc[i, "min_share"] * batch_kg, f"Min_{i}"
        full_model += x[i] <= ingredients.loc[i, "max_share"] * batch_kg, f"Max_{i}"
    # Read ingredient quantities only after the full constrained model is optimal.
    full_model.solve(SOLVER)
    print("Status:", pulp.LpStatus[full_model.status])
    if full_model.status == pulp.LpStatusOptimal:
        display(pd.Series({i: x[i].value() for i in x}, name="Quantity (kg)").to_frame())
        print(f"Minimum cost: {pulp.value(full_model.objective):.2f} PLN")
    ''')
    md('''
    ### Task 1 — inspect and change the model

    - **Predict:** Which constraints should be tight when expensive ingredients are avoided?
    - **Run:** Check the computed recipe against your prediction.
    - **Change:** In the explicit model, raise the protein requirement from `0.24` to `0.28`. Rerun that cell and compare cost and quantities. Restore it to `0.24` afterwards.
    - **Explain:** Why does a minimum requirement use `>=`, while moisture uses `<=`? Why would rounding every ingredient to whole kg risk violating a specification?

    ## 4. A reusable solver with checks

    Rebuilding a fresh model for each experiment avoids accidentally accumulating old constraints. The helpers below separate a simple diagnostic bound from the complete optimization model.

    ### Helper: an optimistic protein bound

    `maximum_protein_from_share_limits(data)` accepts an ingredient table with protein fractions and lower/upper recipe shares. It reserves the minimum shares, then allocates the remaining share to the highest-protein ingredients up to their caps. It returns one **protein fraction**, not a recipe, and does not display anything or call a solver. It ignores fat and moisture, so the bound can diagnose an impossible request but cannot prove a full recipe is feasible. Reusing this calculation in a failed solve and a stand-alone experiment keeps their explanations consistent. The share minima must fit one batch and the maxima must be able to fill it.
    ''')
    code('''
    def maximum_protein_from_share_limits(data):
        """Return an optimistic maximum protein fraction for a share-limited batch.

        data is an indexed ingredient DataFrame with protein (kg protein/kg
        ingredient), min_share, and max_share fractions. Minimum shares must
        sum to at most one and maximum shares to at least one, with each
        minimum no greater than its maximum. There are no default arguments.
        Reserve minima, then fill remaining share by descending protein.
        Return a float fraction, ignoring fat/moisture; no display, solver,
        or global ingredient table is used, and data is not modified.
        """
        # Reserve required ingredients before spending the remaining batch share.
        shares = data["min_share"].copy()
        remaining = 1.0 - shares.sum()
        # Greedy allocation is valid for this one-quality bound, not the full blend LP.
        for name in data.sort_values("protein", ascending=False).index:
            addition = min(remaining, data.loc[name, "max_share"] - shares[name])
            shares[name] += addition
            remaining -= addition
        return float((shares * data["protein"]).sum())
    ''')
    md('''
    ### Helper: solve and verify one recipe

    `solve_blend(batch_kg=100, min_protein=0.24, min_fat=0.08, max_moisture=0.60,
    chicken_cost_multiplier=1.0, data=None)` accepts a batch mass in kg, three quality
    fractions, a multiplier on chicken's PLN/kg price, and an optional ingredient table.
    `data=None` copies the shared `ingredients` table; passing your own table also copies
    it, so experiments do not alter baseline data. For example,
    `solve_blend(batch_kg=200, min_protein=0.28)` changes only batch size and protein target.

    The helper validates inputs, builds the same cost and quality equations as above,
    solves with the shared `SOLVER`, and checks status. For an optimum it recomputes recipe
    mass, quality, and margins before returning a dictionary with `recipe`, `quality`,
    `constraints`, `quantities_kg`, and `cost_pln`, alongside the model and status. It does
    not display anything. Tables, plots, sweeps, and controls reuse this checked structure.

    **Trust the status first.** Nonoptimal results contain diagnostics and `None` solution
    fields. The helper returns before reading decision values because a solver's values
    after an infeasible solve are not a usable recipe. The optimistic protein helper
    supplies one possible diagnosis; interacting quality constraints may need closer study.
    ''')
    code('''
    def solve_blend(batch_kg=100, min_protein=0.24, min_fat=0.08,
                    max_moisture=0.60, chicken_cost_multiplier=1.0, data=None):
        """Solve and verify one continuous blending LP, without displaying output.

        batch_kg=100 is positive kg; min_protein=0.24, min_fat=0.08, and
        max_moisture=0.60 are mass fractions. chicken_cost_multiplier=1.0
        scales only chicken's PLN/kg price. data=None copies global ingredients;
        an optional indexed DataFrame supplies costs, compositions, and shares.
        Uses global SOLVER and maximum_protein_from_share_limits for diagnostics.

        Return a dict with status, model, batch_kg, and diagnostic strings.
        An optimum also contains cost_pln, quantities_kg (Series), recipe
        (DataFrame with kg, share_pct, and cost contributions), quality
        (actual/target percentages, margins, and checks), and constraints
        (achieved/bound kg, units, slack/surplus, binding, and LP duals).
        Those solution fields remain None unless status is Optimal.
        Copies input data; invalid inputs raise ValueError.
        """
        # Work on a copy so a price shock never changes another experiment's inputs.
        table = ingredients.copy(deep=True) if data is None else data.copy(deep=True)
        # Validate units, fractions, prices, and share limits before model construction.
        parameters = [batch_kg, min_protein, min_fat, max_moisture, chicken_cost_multiplier]
        if not np.isfinite(parameters).all() or batch_kg <= 0 or chicken_cost_multiplier < 0:
            raise ValueError("Use a positive finite batch and a nonnegative finite price multiplier.")
        if not all(0 <= v <= 1 for v in [min_protein, min_fat, max_moisture]):
            raise ValueError("Nutrient limits must be fractions between 0 and 1.")
        required = ["cost_pln_per_kg", "protein", "fat", "moisture", "min_share", "max_share"]
        if table.empty or not table.index.is_unique or "chicken" not in table.index:
            raise ValueError("Ingredient names must be unique and include chicken.")
        if not np.isfinite(table[required].to_numpy()).all():
            raise ValueError("Ingredient data must contain finite numeric values.")
        fractions = table[["protein", "fat", "moisture", "min_share", "max_share"]]
        if ((fractions < 0) | (fractions > 1)).any().any():
            raise ValueError("Composition and share values must be fractions in [0, 1].")
        if (table["cost_pln_per_kg"] < 0).any() or (table.min_share > table.max_share).any():
            raise ValueError("Costs must be nonnegative; minimum shares cannot exceed maximum shares.")
        # Build a fresh model: cost objective, mass balance, quality, and share bounds.
        table.loc["chicken", "cost_pln_per_kg"] *= chicken_cost_multiplier
        model = pulp.LpProblem("Blend", pulp.LpMinimize)
        variables = {i: pulp.LpVariable(f"kg_{i}", lowBound=0) for i in table.index}
        model += pulp.lpSum(table.loc[i, "cost_pln_per_kg"] * variables[i] for i in table.index), "Cost_PLN"
        model += pulp.lpSum(variables.values()) == batch_kg, "Batch_kg"
        model += pulp.lpSum(table.loc[i, "protein"] * variables[i] for i in table.index) >= min_protein * batch_kg, "Protein_kg"
        model += pulp.lpSum(table.loc[i, "fat"] * variables[i] for i in table.index) >= min_fat * batch_kg, "Fat_kg"
        model += pulp.lpSum(table.loc[i, "moisture"] * variables[i] for i in table.index) <= max_moisture * batch_kg, "Moisture_kg"
        for i in table.index:
            model += variables[i] >= table.loc[i, "min_share"] * batch_kg, f"Min_{i}"
            model += variables[i] <= table.loc[i, "max_share"] * batch_kg, f"Max_{i}"
        # Record status first; failed solves must not expose leftover variable values.
        model.solve(SOLVER)
        result = {"status": pulp.LpStatus[model.status], "model": model,
                  "batch_kg": batch_kg, "cost_pln": None, "quantities_kg": None,
                  "recipe": None, "quality": None, "constraints": None, "diagnostics": []}
        if model.status != pulp.LpStatusOptimal:
            # Explain simple necessary-bound violations; they do not cover every conflict.
            if table.min_share.sum() > 1 + 1e-9:
                result["diagnostics"].append("Minimum ingredient shares add to more than 100%.")
            elif table.max_share.sum() < 1 - 1e-9:
                result["diagnostics"].append("Maximum ingredient shares cannot fill a whole batch.")
            else:
                upper = maximum_protein_from_share_limits(table)
                if min_protein > upper + 1e-9:
                    result["diagnostics"].append(
                        f"Requested protein {min_protein:.1%} exceeds the share-limited upper bound {upper:.1%}.")
            if min_fat > table.fat.max() + 1e-9:
                result["diagnostics"].append("Requested fat exceeds the fattiest ingredient.")
            if max_moisture < table.moisture.min() - 1e-9:
                result["diagnostics"].append("Allowed moisture is below the driest ingredient.")
            if not result["diagnostics"]:
                result["diagnostics"].append(
                    "No simple bound explains this status. Inspect interacting quality/share constraints; relax one at a time.")
            return result

        # Extract only an optimum and recompute ingredient shares/costs in original units.
        quantities = pd.Series({i: variables[i].value() for i in table.index}, name="kg")
        recipe = table.copy()
        recipe["kg"] = quantities
        recipe["share_pct"] = 100 * quantities / batch_kg
        recipe["ingredient_cost_pln"] = quantities * table.cost_pln_per_kg
        targets = {"protein": (min_protein, ">="), "fat": (min_fat, ">="),
                   "moisture": (max_moisture, "<=")}
        # Convert weighted totals to percentages and sign-aware quality margins.
        quality_rows = []
        for nutrient, (target, sense) in targets.items():
            actual = float((quantities * table[nutrient]).sum() / batch_kg)
            margin = actual - target if sense == ">=" else target - actual
            quality_rows.append({"nutrient": nutrient, "actual_pct": 100 * actual,
                                 "target_pct": 100 * target, "rule": sense,
                                 "margin_percentage_points": 100 * margin,
                                 "meets_target": margin >= -1e-7})

        # Describe each model row with its achieved value, bound, margin, and local dual.
        checks = []
        for name, constraint in model.constraints.items():
            # PuLP stores (left - right); sign-aware slack is positive when allowed.
            residual = float(pulp.value(constraint))
            slack = (-residual if constraint.sense == pulp.LpConstraintLE else
                     residual if constraint.sense == pulp.LpConstraintGE else abs(residual))
            units = {"Protein_kg": "kg protein", "Fat_kg": "kg fat",
                     "Moisture_kg": "kg water"}.get(name, "kg ingredient/batch")
            checks.append({"constraint": name, "sense": {0: "=", 1: ">=", -1: "<="}[constraint.sense],
                           "achieved_kg": residual - constraint.constant,
                           "bound_kg": -constraint.constant, "units": units,
                           "slack_or_surplus_kg": slack, "binding": abs(slack) <= 1e-5,
                           "dual_pln_per_rhs_kg": constraint.pi})
        quality = pd.DataFrame(quality_rows).set_index("nutrient")
        constraint_table = pd.DataFrame(checks).set_index("constraint")
        # Independent arithmetic checks before presenting the solution.
        assert abs(quantities.sum() - batch_kg) <= 1e-5 * max(1, batch_kg)
        assert quality.meets_target.all(), "Returned recipe fails a nutrient target."
        assert (constraint_table.slack_or_surplus_kg >= -1e-5 * max(1, batch_kg)).all()
        result.update(cost_pln=float(pulp.value(model.objective)), quantities_kg=quantities,
                      recipe=recipe, quality=quality, constraints=constraint_table)
        return result


    # Keep the default result so all baseline tables and plots describe the same recipe.
    baseline = solve_blend()
    print("Baseline status:", baseline["status"])
    if baseline["status"] == "Optimal":
        display(baseline["recipe"][["kg", "share_pct", "ingredient_cost_pln"]].round(3))
        display(baseline["quality"].round(4))
        print(f"Cost = {baseline['cost_pln']:.2f} PLN; {baseline['cost_pln'] / 100:.3f} PLN/kg")
    ''')
    md('''
    ## 5. See the answer and its margins

    The recipe chart answers **what goes into the mixer**. The quality chart answers **whether the blend meets the targets**. A minimum line must lie at or below its bar; a maximum line must lie at or above its bar.

    A **binding constraint** lies on its limit. For a `<=` rule, **slack = bound − achieved**; for a `>=` rule, **surplus = achieved − bound**. Both are nonnegative margins for a feasible recipe. The table reports achieved values, bounds, units, and `slack_or_surplus_kg`. Protein surplus is extra kg protein above the requirement; moisture slack is the allowed kg water left unused.

    The quality table expresses the same margins in **percentage points**. For equality constraints, the column contains the absolute numerical residual: it should be close to zero, and it is not a resource we can spend. A binding constraint has zero margin within numerical tolerance. A dual value answers a different question: how cost changes when a bound moves.

    `plot_blend(result)` accepts a `solve_blend` result dictionary. It checks status before
    reading a recipe, prints the batch cost, plots ingredient kg and quality percentages,
    then displays the quality table. A nonoptimal result prints its diagnostics instead.
    It returns `None` and never re-solves the model. The shared `COLORS` gives each ingredient
    a consistent color, with gray for new names. Reusing this renderer for the baseline,
    named experiments, and callbacks makes their status and quality checks easy to compare.
    ''')
    code('''
    def plot_blend(result):
        """Display recipe and quality charts for a solve_blend result; return None.

        result is a solver-result dict with status/diagnostics and, if Optimal,
        batch_kg, cost_pln, recipe (kg and share_pct), and quality (actual/target
        percentages and >=/<= rules). Nonoptimal status prints diagnostics
        without reading solution fields. An optimum prints cost, shows two
        matplotlib panels, and displays the quality DataFrame. Uses global
        COLORS, np, plt, and display; does not change data or solve again.
        """
        # Check status before attempting to read any numeric recipe fields.
        if result["status"] != "Optimal":
            print("Status:", result["status"], "— no recipe to plot.")
            for message in result["diagnostics"]:
                print(" •", message)
            return
        # Keep the checked recipe and quality table as the sole source of chart values.
        recipe, quality = result["recipe"], result["quality"]
        print(f"Optimal {result['batch_kg']:g} kg batch: {result['cost_pln']:.2f} PLN"
              f" ({result['cost_pln'] / result['batch_kg']:.3f} PLN/kg)")
        fig, axes = plt.subplots(1, 2, figsize=(11, 4))
        # Annotate ingredient masses with shares so both unit systems remain visible.
        axes[0].barh(recipe.index, recipe.kg, color=[COLORS.get(i, "#777") for i in recipe.index])
        for j, (_, row) in enumerate(recipe.iterrows()):
            axes[0].text(row.kg + result["batch_kg"] * 0.012, j,
                         f"{row.kg:.1f} kg / {row.share_pct:.1f}%", va="center", fontsize=9)
        axes[0].set(xlabel="Ingredient mass (kg)", title="Recipe", xlim=(0, result["batch_kg"] * 0.85))
        # Compare each achieved quality percentage with its minimum or maximum line.
        positions = np.arange(len(quality))
        axes[1].bar(positions, quality.actual_pct, color="#4393c3", alpha=0.7, label="Actual")
        for pos, (_, row) in zip(positions, quality.iterrows()):
            axes[1].plot([pos - 0.38, pos + 0.38], [row.target_pct] * 2, color="#ba332b", lw=2)
            axes[1].text(pos, max(row.actual_pct, row.target_pct) + 2,
                         f"{row.rule} {row.target_pct:g}%", ha="center", fontsize=9)
        axes[1].plot([], [], color="#ba332b", lw=2, label="Target")
        axes[1].set(xticks=positions, xticklabels=quality.index,
                    ylabel="Batch composition (%)", title="Quality check", ylim=(0, 100))
        axes[1].legend()
        plt.tight_layout()
        plt.show()
        # Show exact table fields beside the visual quality check, rounded for readability.
        display(quality.round(4))


    plot_blend(baseline)
    if baseline["status"] == "Optimal":
        display(baseline["constraints"].round(5))
    ''')
    md('''
    ### Build a plot yourself

    A chart consists of a **figure** (the canvas) and an **axes** object (one plotting area). `ax.barh(labels, values)` draws a horizontal bar for each value; `ax.set(...)` labels the axes. Here is a small working chart you can modify without reading the entire plotting helper.
    ''')
    code('''
    # Plot verified ingredient cost contributions, not unit prices or unverified variable values.
    if baseline["status"] == "Optimal":
        fig, ax = plt.subplots(figsize=(7, 3))  # create one canvas and one plotting area
        ax.barh(baseline["recipe"].index, baseline["recipe"].ingredient_cost_pln,
                color=[COLORS[i] for i in baseline["recipe"].index])
        ax.set(xlabel="Ingredient cost contribution (PLN)", title="Where does the bill come from?")
        plt.tight_layout()  # leave room for labels
        plt.show()
    ''')
    md('''
    **Plotting task:** change the bars from cost contributions to ingredient share percentages, then update the axis label and title. Add a vertical line with `ax.axvline(...)` for a meaningful ingredient-share reference and explain why that line is a reference, not a universal recipe constraint.

    ### Task 2 — explain the recipe

    1. Which ingredients reach their lower or upper share limits? Does an unused ingredient always mean it is poor quality?
    2. Which quality constraints bind? Identify the same boundary in the table and plot.
    3. Add 1 kg of the cheapest ingredient and remove 1 kg of chicken **on paper**. Recalculate protein and fat. Does the modified blend remain feasible?
    4. Compare this recipe with the two-ingredient warm-up. Explain why the warm-up cost is lower: it was solving a different set of constraints.

    ## 6. A tighter target can make the model infeasible

    The largest ingredient protein fraction is 38%, but share caps prevent using only chicken. To obtain a necessary protein upper bound, start at the minimum shares and fill the remaining batch with the highest-protein available ingredients up to their caps. This ignores other quality requirements, so it is an **optimistic upper bound**, not a guaranteed feasible recipe.

    Predict whether **36% protein** is achievable. Then run the scenario below. Infeasibility is an expected experimental result: there is no recipe satisfying every rule. It is different from a Python exception or a missing solver.
    ''')
    code('''
    # Compare a necessary share-limited bound with an intentionally impossible quality target.
    protein_upper_bound = maximum_protein_from_share_limits(ingredients)
    print(f"Share-limited protein upper bound: {protein_upper_bound:.1%}")
    impossible = solve_blend(min_protein=0.36)
    plot_blend(impossible)
    assert impossible["status"] == "Infeasible"
    assert impossible["quantities_kg"] is None
    ''')
    md('''
    ### Task 3 — diagnose, then propose a repair

    - Which assumption would you change: protein target, chicken cap, or ingredient menu?
    - Make one change in `ingredients.copy()` and pass it as `data=...` to the helper. Do not erase the baseline table.
    - Rerun and check **all** quality constraints. A protein upper bound above the target does not prove feasibility when fat and moisture rules also apply.
    - Explain why increasing the batch from 100 kg to 200 kg cannot repair incompatible percentage rules.

    ## 7. Cost–quality trade-off: sweep before choosing

    Management proposes a higher protein label. Each point below is a **new optimization**, not the old recipe with a new label. Predict the shape: can the minimum cost decrease when a minimum protein target rises and all other inputs stay fixed?
    ''')
    code('''
    # Re-optimize every target; infeasible cases retain status but have no numeric cost.
    sweep_rows = []
    for target in np.linspace(0.14, 0.38, 25):
        result = solve_blend(min_protein=float(target))
        row = {"protein_target_pct": 100 * target, "status": result["status"],
               "cost_pln_per_kg": np.nan}
        if result["status"] == "Optimal":
            row["cost_pln_per_kg"] = result["cost_pln"] / result["batch_kg"]
            row.update({f"share_{i}": result["recipe"].loc[i, "share_pct"] for i in ingredients.index})
        sweep_rows.append(row)
    sweep = pd.DataFrame(sweep_rows)
    # Separate valid recipes from failed solves before drawing costs and composition shares.
    feasible = sweep[sweep.status == "Optimal"]
    infeasible = sweep[sweep.status != "Optimal"]
    fig, axes = plt.subplots(1, 2, figsize=(11, 4))
    axes[0].plot(feasible.protein_target_pct, feasible.cost_pln_per_kg, "o-", color="#345f93")
    if not infeasible.empty:
        axes[0].scatter(infeasible.protein_target_pct, np.zeros(len(infeasible)), marker="x",
                        color="#ba332b", label="Infeasible (marker at 0, no cost)")
    axes[0].set(xlabel="Minimum protein target (%)", ylabel="Minimum cost (PLN/kg)",
                title="Cost of a stronger specification")
    axes[0].legend()
    share_columns = [f"share_{i}" for i in ingredients.index]
    axes[1].stackplot(feasible.protein_target_pct, *[feasible[c] for c in share_columns],
                      labels=ingredients.index, colors=[COLORS[i] for i in ingredients.index], alpha=0.85)
    axes[1].set(xlabel="Minimum protein target (%)", ylabel="Ingredient share (%)",
                ylim=(0, 100), title="How the optimal recipe changes")
    axes[1].legend(fontsize=8, loc="upper left")
    plt.tight_layout()
    plt.show()
    display(sweep[["protein_target_pct", "status", "cost_pln_per_kg"]].round(3))
    ''')
    md('''
    ### Task 4 — interpret a frontier

    Find a flat cost region, a rising region, and the transition to infeasibility. Explain each using recipe constraints. A flat region can occur when another rule already forces more protein than requested. Kinks occur when the active constraints or selected ingredients change.

    Choose between 24%, 28%, and 32% protein. Compare the additional cost **per batch** and **per kg**, and describe the recipe changes. A higher target is a specification choice; the optimizer cannot decide whether customers value it enough.

    ## 8. Local sensitivity: what does one extra requirement cost?

    CBC reports an LP **dual value**, also called a shadow price, for each constraint. For `Protein_kg`, its units are **PLN per additional kg of required protein**, with the other right-hand sides fixed. For this minimization model, a positive value means tightening the minimum protein requirement raises cost locally.

    Moving the target from 24% to 24.01% adds **0.01 kg required protein** to a 100 kg batch: `100 × (0.2401 − 0.24)`. A one-percentage-point increase would add 1 kg required protein.

    Dual values describe a local slope of a continuous LP. They can change at a kink, may be nonunique at a degenerate optimum, and are not a valid guarantee for large changes or integer models. We check a small re-solve instead of treating the reported value as a global promise.
    ''')
    code('''
    # Convert the target change to required protein kg before interpreting the LP dual units.
    delta_fraction = 0.0001  # 0.01 percentage points
    slightly_stricter = solve_blend(min_protein=0.24 + delta_fraction)
    if baseline["status"] == slightly_stricter["status"] == "Optimal":
        delta_required_kg = baseline["batch_kg"] * delta_fraction
        local_slope = (slightly_stricter["cost_pln"] - baseline["cost_pln"]) / delta_required_kg
        dual = baseline["model"].constraints["Protein_kg"].pi
        print(f"CBC dual: {dual:.4f} PLN per kg required protein")
        print(f"Small re-solve slope: {local_slope:.4f} PLN per kg required protein")
        print(f"Observed cost increase: {slightly_stricter['cost_pln'] - baseline['cost_pln']:.4f} PLN")
        if dual is not None:
            print(f"Local dual prediction: {dual * delta_required_kg:.4f} PLN")
    ''')
    md('''
    ### Task 5 — test the limit of the prediction

    Change `delta_fraction` to `0.08` (eight percentage points: 24% → 32%). Does the original shadow price still predict the observed increase? Inspect which constraints bind before and after. As an intermediate check, try `0.04`: a larger change can still follow the local slope if the same active constraints remain valid. A zero dual can mean a small tightening has no cost; binding does not always imply a nonzero dual.

    ## 9. Live recipe explorer

    Move one control at a time, predict the effect, then read the status and both plots. The controls **re-solve the LP**, so price shocks can change the recipe, not just the displayed bill.

    - **Batch:** 50–250 kg. With percentage rules alone, shares stay the same and cost scales with batch size. A fixed warehouse-stock constraint would change that behavior.
    - **Protein:** 18–38%. High settings are intentionally infeasible.
    - **Chicken price ×:** a multiplier applied only to the chicken price.

    If widgets are unavailable, the following parameter cell runs exactly the same experiment. Do not require sliders to complete the lab.
    ''')
    code('''
    # Fallback parameter experiment: edit these three numbers and rerun this cell.
    experiment_batch_kg = 100
    experiment_min_protein = 0.28
    experiment_chicken_cost_multiplier = 1.0

    # Named arguments link each editable parameter to the solver input, preserving other defaults.
    experiment = solve_blend(batch_kg=experiment_batch_kg,
                             min_protein=experiment_min_protein,
                             chicken_cost_multiplier=experiment_chicken_cost_multiplier)
    plot_blend(experiment)
    ''')
    md('''
    ### Helper: update the live experiment

    `update_explorer(change=None)` is called after an observed slider-value change; the
    optional change event is accepted but not read. It uses the shared batch, protein,
    and chicken-price controls rather than receiving those values as arguments. Controls
    start at 100 kg, 24%, and a price multiplier of 1.0. The callback converts protein to
    a fraction, creates a named `parameters` dictionary, and passes it to `solve_blend`.
    `plot_blend` checks status before showing tables and plots inside `explorer_output`.
    The callback returns `None` and replaces the old display instead of accumulating figures.
    Reusing the solver and renderer keeps live updates consistent with the fallback above.
    ''')
    code('''
    # Create controls in student-facing units; the callback converts percentages to fractions.
    batch_slider = widgets.IntSlider(value=100, min=50, max=250, step=10,
                                      description="Batch (kg)", continuous_update=False)
    protein_slider = widgets.FloatSlider(value=24, min=18, max=38, step=0.5,
                                         description="Protein (%)", continuous_update=False)
    price_slider = widgets.FloatSlider(value=1.0, min=0.5, max=2.5, step=0.1,
                                       description="Chicken ×", continuous_update=False)
    explorer_output = widgets.Output()

    def update_explorer(change=None):
        """Replace the live recipe display from the current control values.

        change=None accepts an unused ipywidgets observation event. Uses global
        batch_slider (kg), protein_slider (%), and price_slider (multiplier),
        initially 100, 24, and 1.0. Converts values to solve_blend keyword inputs,
        solves afresh, and uses plot_blend's status guard for tables/plots.
        Displays in global explorer_output, clearing its previous contents;
        returns None. Also depends on clear_output, solve_blend, and plot_blend.
        """
        # 1. Read control values and convert percent to fraction.
        parameters = {"batch_kg": batch_slider.value,
                      "min_protein": protein_slider.value / 100,
                      "chicken_cost_multiplier": price_slider.value}
        with explorer_output:  # keep the answer in one output area
            clear_output(wait=True)  # replace the old answer
            # 2. Build a fresh model and solve it with these parameters.
            result = solve_blend(**parameters)
            # 3. Check status; 4. show the checked table and plots.
            plot_blend(result)

    for control in [batch_slider, protein_slider, price_slider]:
        # .observe calls our callback whenever this control's value changes.
        control.observe(update_explorer, names="value")
    display(widgets.VBox([batch_slider, protein_slider, price_slider, explorer_output]))
    update_explorer()  # render the initial values, before anyone moves a slider
    ''')
    md('''
    ### Build one more control

    The data flow is **slider value → parameter conversion → fresh model → status check → table and plot**. `observe` connects a control to the callback; it does not solve anything itself. `continuous_update=False` waits until you release the slider, avoiding many unnecessary solves. The keyword unpacking `solve_blend(**parameters)` is equivalent to passing each named argument separately.

    **Task:** add a `moisture_slider` with a 20–80% range and initial value 60. Add `"max_moisture": moisture_slider.value / 100` to `parameters`, include the control in the `observe` loop and `VBox`, and rerun the entire dashboard cell. Test two settings and verify that both the moisture target line and the status/recipe change as appropriate. You have now built a new optimization control.

    ### Task 6 — controlled experiments

    Keep a short results table with parameter settings, status, cost/kg, and one recipe observation.

    1. Compare 50 kg and 200 kg at the same targets and prices. Verify equal shares and four times the total cost.
    2. Compare chicken price multipliers `0.5`, `1.0`, and `2.0` at 24% protein. Which ingredients replace chicken, if any? Explain the role of its minimum share.
    3. Find an infeasible protein setting. Identify a simple necessary bound that rules it out.
    4. Optional: add a fixed chicken-stock constraint, such as `chicken_kg <= 80`, to your own model. Explain why batch size now affects feasibility and recipe shares.

    ## 10. Your recommendation

    Submit a short recommendation to the production team containing:

    - your chosen batch and protein target, status, exact recipe table, and cost/kg;
    - the recipe and quality plots, plus the binding constraints;
    - one feasible alternative and its additional cost;
    - one infeasible scenario, a diagnosis, and a proposed repair;
    - a chicken-price shock experiment and a sentence on local sensitivity;
    - one limitation: simplified data, continuous quantities, constant unit costs, or missing production/stock constraints.

    **Before handing over a recipe:** verify mass balance, every nutrient target, and every share bound. Reporting a solver objective without checking its status and units is not enough.

    Lab 3 moves from **what goes into a blend** to **where goods flow and how raw material is cut**. Lab 6 will connect blending to uncertain prices and the operation of a robotic production cell.
    ''')
    # New explanatory cells receive named IDs; existing course links retain their IDs.
    cell_ids = ([f"lab2-{i:02d}" for i in range(11)]
                + ["lab2-solver-intro", "lab2-solver"]
                + [f"lab2-{i:02d}" for i in range(11, 23)]
                + ["lab2-explorer-intro", "lab2-23", "lab2-24"])
    for cell, cell_id in zip(cells, cell_ids, strict=True):
        cell.id = cell_id
    notebook = nbf.v4.new_notebook(cells=cells, metadata={
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "version": "3.11"},
        "colab": {"provenance": [], "name": "lab_auto_2.ipynb"},
    })
    nbf.validate(notebook)
    return notebook


if __name__ == "__main__":
    path = ROOT / "lab_auto_2.ipynb"
    nbf.write(build_notebook(), path)
    print(f"Wrote {path}")
