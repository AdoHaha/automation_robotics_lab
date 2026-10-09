"""Build a self-contained, Colab-ready product-mix teaching notebook."""

from pathlib import Path
from textwrap import dedent

import nbformat as nbf

ROOT = Path(__file__).resolve().parents[1]


def build():
    cells = []

    def md(source):
        cells.append(nbf.v4.new_markdown_cell(dedent(source).strip()))

    def code(source):
        cells.append(nbf.v4.new_code_cell(dedent(source).strip()))

    md(r"""
    # Lab 1: Product Mix and Resource Allocation with PuLP

    [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/AdoHaha/automation_robotics_lab/blob/master/lab_auto_1.ipynb)

    **Question:** how should a small robot-kit factory allocate its limited assembly and testing time?

    Lab 0 introduced Python dictionaries, functions, tables, plots, and sliders. Now those tools
    become an optimization experiment. You will build a model, interpret it, and make a recommendation.

    By the end you should be able to identify **parameters, decision variables, objective,
    constraints, feasible region, slack, binding constraints, and shadow prices**; distinguish an LP
    from an integer model; and build a slider that re-solves and plots a changed assumption.

    Work through the story and hand calculation, the first PuLP model, geometry and slack,
    then plotting, interactive experiments, sensitivity, and your recommendation.
    The whole-kit comparison is a short core step; reduced costs are an optional extension.

    In Colab, save your own copy with **File → Save a copy in Drive**, then use
    **Runtime → Run all**. All teaching data are embedded. Setup needs internet once for packages;
    the examples need no repository checkout, Drive mount, or downloaded CSV. On a fresh runtime,
    run cells from the top. If widgets do not render, use the adjacent parameter cells.
    """)
    md("""
    ## 0. Runtime setup

    PuLP describes the optimization model; its bundled CBC solver computes a solution.
    We use PuLP 3.x because these course notebooks teach its 3.x modeling API.
    Matplotlib draws the figures, pandas makes tables, and ipywidgets connects controls to Python.
    """)
    code(r"""
    # Install into this notebook kernel and keep the modeling API consistent across Colab runs.
    %pip install -q "pulp>=3.3,<4" numpy pandas matplotlib ipywidgets
    %matplotlib inline

    import pulp
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    import ipywidgets as widgets
    from IPython.display import display

    try:
        from google.colab import output
        output.enable_custom_widget_manager()
    except ImportError:
        pass  # Local Jupyter does not need the Colab widget manager.

    SOLVER = pulp.PULP_CBC_CMD(msg=False)
    if not SOLVER.available():
        raise RuntimeError("CBC is missing. Re-run setup in a fresh Colab runtime.")
    plt.rcParams.update({"figure.figsize": (9, 4), "axes.grid": False})
    print("PuLP", pulp.__version__, "| CBC available")
    """)
    md("""
    ## 1. Story: two kits, two shared stations

    The factory sells **Mini** and **Pro** educational robot kits. It has 350 assembly minutes
    and 180 testing minutes per day. Assume unlimited demand, constant contribution profit,
    and no setup losses. The coefficients below are **illustrative teaching data**, not quotations.

    | Product | Profit (PLN/kit) | Assembly (min/kit) | Testing (min/kit) |
    |:--|--:|--:|--:|
    | Mini | 40 | 20 | 15 |
    | Pro | 70 | 40 | 10 |

    The first model treats production as a **divisible planning quantity**; fractional kits represent
    average daily output across repeated days. For literal whole kits today, we will solve an integer model.
    """)
    code(r"""
    # Store the story as reusable product, profit, time, and capacity parameters.
    PRODUCTS = ["Mini", "Pro"]
    PROFIT = {"Mini": 40.0, "Pro": 70.0}
    TIME = {
        "Assembly": {"Mini": 20.0, "Pro": 40.0},
        "Testing": {"Mini": 15.0, "Pro": 10.0},
    }
    CAPACITY = {"Assembly": 350.0, "Testing": 180.0}
    data = pd.DataFrame({
        "profit_PLN_per_kit": PROFIT,
        "assembly_min_per_kit": TIME["Assembly"],
        "testing_min_per_kit": TIME["Testing"],
    })
    display(data)

    fig, ax = plt.subplots(figsize=(10, 3))
    ax.axis("off")
    boxes = [(0.12, "Choose a mix\nMini + Pro"),
             (0.43, "Shared assembly\n350 min/day"),
             (0.74, "Shared testing\n180 min/day")]
    for x_pos, label in boxes:
        ax.text(x_pos, 0.55, label, ha="center", va="center", transform=ax.transAxes,
                bbox=dict(boxstyle="round,pad=0.8", fc="#e6f2ff", ec="#2471a3"))
    for x_start, x_end in [(0.23, 0.32), (0.56, 0.63)]:
        ax.annotate("", xy=(x_end, 0.55), xytext=(x_start, 0.55),
                    xycoords="axes fraction", arrowprops=dict(arrowstyle="->", lw=2))
    ax.text(0.5, 0.10, "Goal: earn the most profit while respecting both daily time limits",
            transform=ax.transAxes, ha="center")
    plt.show()
    """)
    md("""
    ### Task 1 — predict before solving

    TODO: calculate time use and profit for `(Mini, Pro) = (10, 0), (0, 8), (5, 6), (8, 5)`.
    Which are feasible? Why might choosing only the kit with the highest profit fail?
    Compare **profit per assembly minute** and **profit per testing minute**: do the rankings agree?
    Record your predicted best mix before the next cell.
    """)
    code(r"""
    # Evaluate the hand-picked plans before asking a solver to choose one.
    candidates = [(10, 0), (0, 8), (5, 6), (8, 5)]
    candidate_rows = []
    for mini, pro in candidates:
        assembly = 20 * mini + 40 * pro
        testing = 15 * mini + 10 * pro
        candidate_rows.append({
            "Mini": mini, "Pro": pro,
            "assembly_min": assembly, "testing_min": testing,
            "profit_PLN": 40 * mini + 70 * pro,
            "feasible": assembly <= 350 and testing <= 180,
        })
    display(pd.DataFrame(candidate_rows))
    """)
    md(r"""
    ## 2. Translate the story into a linear program

    A **parameter** is known input (350 minutes); a **decision variable** is an unknown the solver
    chooses ($m$ Mini kits and $p$ Pro kits). The **objective** measures how good a decision is.
    A **constraint** describes a rule every acceptable decision must obey.

    $$\max\; Z = 40m + 70p\quad\text{PLN/day}$$
    $$20m + 40p \le 350\quad\text{assembly min/day}$$
    $$15m + 10p \le 180\quad\text{testing min/day},\qquad m,p\ge0.$$

    Each term multiplies a **constant** by one variable. For example,
    `(min/kit) × (kits/day) = min/day`. Products of decisions such as $mp$ are not linear.
    The model assumes additive time and profit, fixed coefficients, and divisible quantities.

    The **feasible region** contains all decisions satisfying every constraint.
    An **optimal solution** is a feasible decision with the best objective value.
    A bounded, feasible LP has an optimum at a vertex; multiple optima can also lie along an edge.
    """)
    md("""
    ### Build the first model slowly

    `LpProblem` specifies maximize/minimize. `LpVariable` gives bounds and a category.
    The first `model += expression` below is the objective; expressions with `<=`, `>=`, or `==`
    are constraints. Names make rows easier to inspect. `lpSum` will generalize this to many products.
    """)
    code(r"""
    # Define nonnegative continuous quantities, then add the profit and station limits.
    first_model = pulp.LpProblem("first_product_mix", pulp.LpMaximize)
    mini = pulp.LpVariable("Mini", lowBound=0, cat="Continuous")
    pro = pulp.LpVariable("Pro", lowBound=0, cat="Continuous")

    first_model += 40 * mini + 70 * pro, "daily_profit"
    first_model += 20 * mini + 40 * pro <= 350, "Assembly"
    first_model += 15 * mini + 10 * pro <= 180, "Testing"
    print(first_model)
    """)
    md("""
    ### Status comes before numbers

    **Optimal:** a best feasible solution was found. **Infeasible:** the rules conflict.
    **Unbounded:** the objective can improve without limit (often a missing constraint).
    **Not Solved/Undefined:** do not claim an optimum. Variable values left after a failed solve
    are not a usable production plan.
    """)
    code(r"""
    # Solve the model; status must be optimal before quantities and profit are read.
    first_model.solve(SOLVER)
    first_status = pulp.LpStatus[first_model.status]
    print("Status:", first_status)
    if first_status == "Optimal":
        print(f"Mini = {mini.value():.3f}, Pro = {pro.value():.3f}")
        print(f"Profit = {pulp.value(first_model.objective):.2f} PLN/day")
    else:
        print("Investigate the model before using variable values.")
    """)
    md("""
    ## 3. A reusable solver for experiments

    Rebuild a fresh model for every scenario so slider changes do not accumulate constraints.
    A dictionary creates one variable per product; a loop creates one row per resource.
    `solve_product_mix(assembly_min=350, testing_min=180, pro_profit=70, minimum=None,
    integer=False)` accepts station capacities in minutes/day, Pro profit in PLN/kit,
    an optional product-to-minimum-order dictionary in kits/day, and a whole-kit switch.
    For example, `solve_product_mix(testing_min=200, minimum={"Mini": 13})` changes only
    testing capacity and the Mini order; all omitted arguments retain their defaults.

    The helper validates inputs, builds variables and constraints, solves, checks status,
    and verifies the result against the story. It returns a dictionary: `status` and `model`
    plus the scenario inputs, and, for an optimum, `quantities`, `profit`, `resources`, and
    `variables` tables. Nonoptimal results leave those solution fields as `None`.
    It uses the shared `PRODUCTS`, `TIME`, and `SOLVER`, without displaying anything itself.
    Reusing this return structure lets plots, sliders, and sensitivity experiments compare
    the same checked quantities rather than build separate versions of the model.
    """)
    code(r"""
    def solve_product_mix(assembly_min=350, testing_min=180,
                          pro_profit=70, minimum=None, integer=False):
        '''Optimize Mini/Pro production for one scenario, without displaying output.

        assembly_min=350 and testing_min=180 are minutes/day; pro_profit=70
        is PLN/Pro kit. minimum=None means no required orders; otherwise give
        a product-to-kits/day dictionary. integer=False allows divisible kits;
        True requires whole kits. Mini profit remains 40 PLN/kit.
        Uses global PRODUCTS, TIME (min/kit), and SOLVER.

        Return a dict containing status, model, capacities, profits, minimum,
        and integer. An optimal result also contains quantities (kits/day),
        profit (PLN/day), resources (used/slack minutes and LP duals), and
        variables (production and LP reduced costs); otherwise these are None.
        Invalid numeric inputs or unknown order names raise ValueError.
        '''
        # Check scenario inputs before creating an optimization model.
        capacities = {"Assembly": float(assembly_min), "Testing": float(testing_min)}
        if any(not np.isfinite(v) or v < 0 for v in capacities.values()):
            raise ValueError("Capacities must be finite and nonnegative.")
        if not np.isfinite(pro_profit):
            raise ValueError("Profit must be finite.")
        minimum = {} if minimum is None else dict(minimum)
        if set(minimum) - set(PRODUCTS):
            raise ValueError("Unknown product in minimum orders.")
        if any(not np.isfinite(v) or v < 0 for v in minimum.values()):
            raise ValueError("Minimum orders must be finite and nonnegative.")

        # Build a fresh maximization model: quantities, profit, then station/order limits.
        profits = {"Mini": 40.0, "Pro": float(pro_profit)}
        model = pulp.LpProblem("product_mix", pulp.LpMaximize)
        x = {product: pulp.LpVariable(product, lowBound=0,
                                      cat="Integer" if integer else "Continuous")
             for product in PRODUCTS}
        model += pulp.lpSum(profits[product] * x[product] for product in PRODUCTS), "profit"
        for resource in TIME:
            model += pulp.lpSum(TIME[resource][product] * x[product]
                                for product in PRODUCTS) <= capacities[resource], resource
        for product, amount in minimum.items():
            model += x[product] >= amount, f"minimum_{product}"
        # Solve once; nonoptimal statuses must never supply production values to a plot.
        model.solve(SOLVER)
        status = pulp.LpStatus[model.status]
        result = {"status": status, "model": model, "quantities": None, "profit": None,
                  "resources": None, "variables": None, "capacities": capacities,
                  "profits": profits, "minimum": minimum, "integer": integer}
        if status != "Optimal":
            return result

        # Translate the optimum into production and independently computed resource use.
        quantities = {product: float(x[product].value()) for product in PRODUCTS}
        resource_rows = []
        for resource in TIME:
            used = sum(TIME[resource][product] * quantities[product] for product in PRODUCTS)
            slack = capacities[resource] - used
            resource_rows.append({
                "resource": resource, "used_min": used, "available_min": capacities[resource],
                "slack_min": slack, "binding": abs(slack) < 1e-6,
                "shadow_PLN_per_min": None if integer else model.constraints[resource].pi,
            })
        # LP marginal values are reported only for the continuous model, not whole kits.
        result.update({
            "quantities": quantities, "profit": float(pulp.value(model.objective)),
            "resources": pd.DataFrame(resource_rows).set_index("resource"),
            "variables": pd.DataFrame([
                {"product": product, "kits_per_day": quantities[product],
                 "reduced_cost_PLN_per_kit": None if integer else x[product].dj}
                for product in PRODUCTS
            ]).set_index("product"),
        })
        # Verify against the original story, independently of the solver's status.
        assert all(v >= -1e-6 for v in quantities.values())
        assert all(row["slack_min"] >= -1e-5 for row in resource_rows)
        assert all(quantities[p] >= amount - 1e-6 for p, amount in minimum.items())
        if integer:
            assert all(abs(v - round(v)) < 1e-6 for v in quantities.values())
        return result

    # Keep one default scenario for later plots and comparisons.
    baseline = solve_product_mix()
    display(baseline["variables"])
    display(baseline["resources"])
    print(f"Baseline profit: {baseline['profit']:.2f} PLN/day")
    """)
    md(r"""
    ## 4. Slack, surplus, and binding constraints

    **Slack** is unused room in an upper-bound constraint. If $a^Tx\le b$,
    slack is $b-a^Tx$. For a minimum requirement $a^Tx\ge b$, **surplus** is $a^Tx-b$.
    For an equality, inspect the residual $a^Tx-b$: it should be near zero.
    Nonnegativity is also a constraint: $m=0$ makes its lower bound active.

    A row is **binding** when its gap is approximately zero (we use a numerical tolerance).
    Binding describes the current solution; it does not automatically mean that buying more of
    that resource will help. The **shadow price** estimates the objective change per extra unit
    of a constraint's right-hand side in a continuous LP, while the optimal basis stays valid.
    It is a local rate, not a promise for a large change and not an integer-model marginal value.

    ### Task 2 — interpret the resource table

    TODO: identify binding rows, explain the units of every column, and calculate both slacks by hand.
    Does zero slack mean zero remaining time or zero value? How would you report a `>=` order gap?
    """)
    md("""
    ## 5. Learn to plot: start with one resource chart

    A figure is the whole canvas; an `Axes` is the drawing area. `barh` puts values on a horizontal
    bar chart; `left=used` stacks unused time after used time. Labels explain units.
    `plt.show()` displays the figure. Make the table first, then plot the same values.
    """)
    code(r"""
    # Stack used and unused minutes from the same verified resource table.
    resources = baseline["resources"]
    fig, ax = plt.subplots(figsize=(8, 3))
    ax.barh(resources.index, resources["used_min"], label="used", color="#2471a3")
    ax.barh(resources.index, resources["slack_min"], left=resources["used_min"],
            label="slack", color="#d5d8dc")
    ax.set_xlabel("Minutes per day")
    ax.set_title("Which resources are fully used?")
    ax.legend()
    plt.tight_layout()
    plt.show()
    """)
    md("""
    TODO: copy the chart cell below your notes. Change the colors, add value labels using `ax.text`,
    and make a second plot of Mini and Pro quantities. State the question each chart answers.
    """)
    md("""
    ### A picture of the feasible region

    The horizontal axis is Mini production; the vertical axis is Pro production.
    Each line is a resource limit. The shaded region obeys **both** inequalities and nonnegativity.
    The dotted objective line passes through the optimum; parallel lines represent equal profit.
    This picture works for two variables; tables and resource plots still work with many variables.

    `plot_product_mix(result)` accepts the dictionary returned by `solve_product_mix`.
    It checks `status` first, calculates both boundary lines, shades their intersection with
    the order limits, and marks the optimum. In whole-kit mode it also adds feasible integer
    points. The second panel draws used capacity and slack from the resource table.
    The helper displays a figure and returns `None`; it does not re-solve or change the result.
    Reuse it as `plot_product_mix(solve_product_mix(assembly_min=800))` to compare scenarios
    with identical axes meanings. The station/profit coefficients in its geometry match
    this lab's fixed two-product story.
    """)
    code(r"""
    def plot_product_mix(result):
        '''Display feasible-region and resource-use charts for a solver result.

        result is a solve_product_mix dictionary: capacities in min/day,
        quantities in kits/day, profits in PLN/kit, minimum orders, and the
        integer flag. Nonoptimal status prints a message and returns None.
        Optimal status displays two matplotlib panels and returns None;
        integer mode adds feasible whole-kit points. Uses global np and plt
        and this story's fixed station coefficients; no optimization is run.
        '''
        # Reject invalid solution fields before calculating geometry.
        if result["status"] != "Optimal":
            print("No optimal feasible plan to plot:", result["status"])
            return
        # Derive axis ranges and resource boundaries from this scenario's capacities.
        caps = result["capacities"]
        q = result["quantities"]
        min_m = result["minimum"].get("Mini", 0)
        min_p = result["minimum"].get("Pro", 0)
        x_max = max(1.0, min(caps["Assembly"] / 20, caps["Testing"] / 15))
        y_max = max(1.0, min(caps["Assembly"] / 40, caps["Testing"] / 10))
        m_grid = np.linspace(0, x_max * 1.08, 400)
        assembly_line = (caps["Assembly"] - 20 * m_grid) / 40
        testing_line = (caps["Testing"] - 15 * m_grid) / 10
        upper = np.minimum(assembly_line, testing_line)
        fig, axes = plt.subplots(1, 2, figsize=(12, 4))
        ax = axes[0]
        # Shade only production quantities satisfying both station and order limits.
        ax.fill_between(m_grid, min_p, upper,
                        where=(m_grid >= min_m) & (upper >= min_p),
                        color="#d6eaf8", alpha=0.9, label="LP feasible region")
        ax.plot(m_grid, assembly_line, label="Assembly limit")
        ax.plot(m_grid, testing_line, label="Testing limit")
        if abs(result["profits"]["Pro"]) > 1e-9:
            ax.plot(m_grid, (result["profit"] - 40 * m_grid) / result["profits"]["Pro"],
                    "k:", label="Equal-profit line at optimum")
        if min_m > 0:
            ax.axvline(min_m, color="gray", linestyle="--", label="Minimum Mini")
        if min_p > 0:
            ax.axhline(min_p, color="gray", linestyle="--", label="Minimum Pro")
        # Whole-kit plans lie on grid points inside the continuous feasible region.
        if result["integer"]:
            feasible_points = [(m, p) for m in range(int(x_max) + 1)
                               for p in range(int(y_max) + 1)
                               if m >= min_m and p >= min_p and
                               20*m + 40*p <= caps["Assembly"] + 1e-6 and
                               15*m + 10*p <= caps["Testing"] + 1e-6]
            if feasible_points:
                points = np.array(feasible_points)
                ax.scatter(points[:, 0], points[:, 1], s=12, color="gray", label="Whole-kit plans")
        # Mark the selected optimum, then draw the checked resource totals beside it.
        ax.scatter(q["Mini"], q["Pro"], color="#c0392b", marker="*", s=180,
                   zorder=5, label="Chosen optimum")
        ax.set(xlim=(0, x_max * 1.08), ylim=(0, y_max * 1.12),
               xlabel="Mini kits/day", ylabel="Pro kits/day", title="Geometry of the product mix")
        ax.legend(fontsize=8)
        table = result["resources"]
        axes[1].barh(table.index, table["used_min"], label="used", color="#2471a3")
        axes[1].barh(table.index, table["slack_min"].clip(lower=0), left=table["used_min"],
                     label="slack", color="#d5d8dc")
        axes[1].set(xlabel="Minutes/day", title=f"Profit: {result['profit']:.2f} PLN/day")
        axes[1].legend()
        plt.tight_layout()
        plt.show()

    plot_product_mix(baseline)
    """)
    md("""
    ### Task 3 — read and extend the picture

    TODO: predict which boundary moves if assembly time increases. Run `solve_product_mix(assembly_min=800)`
    and plot it. Identify slack and explain why adding time eventually stops helping.
    Add a marker for one candidate from Task 1 and explain whether it lies inside the shaded region.
    """)
    md("""
    ## 6. Build your first solver slider

    A widget has **value**, **min**, **max**, **step**, and **description**. The slider name passed
    to `interact` must match the callback's argument name. `continuous_update=False` re-solves when
    you release the slider. The callback is ordinary Python: **parameter → model → status → table → plot**.
    First call it directly so you can debug without widgets, then connect one control.

    `assembly_experiment(assembly_min=350)` accepts one capacity in minutes/day. It calls
    the shared solver while keeping other inputs at their defaults, prints the status,
    then displays production, resources, and the figure only for an optimum. It returns
    `None`. Reusing this callback for both a named direct call and `interact` means a slider
    and the fallback parameter cell follow exactly the same checks and displays.
    """)
    code(r"""
    def assembly_experiment(assembly_min=350):
        '''Display one assembly-capacity experiment; return None.

        assembly_min defaults to 350 min/day; other model inputs keep the
        solve_product_mix defaults. Uses the shared solver and plotting helper,
        plus global display. Always prints status; shows tables/plot only
        when the result is optimal. Called directly or by the assembly slider.
        '''
        # Convert the control's capacity into a fresh solve, then guard the displays.
        result = solve_product_mix(assembly_min=assembly_min)
        print("Status:", result["status"])
        if result["status"] == "Optimal":
            display(result["variables"])
            display(result["resources"])
            plot_product_mix(result)

    # Parameter-cell fallback: change 350 and run this cell.
    assembly_experiment(assembly_min=350)
    """)
    code(r"""
    # Match the widget keyword to the callback argument, so each release re-solves once.
    assembly_slider = widgets.IntSlider(value=350, min=100, max=900, step=10,
                                       description="Assembly", continuous_update=False)
    assembly_control = widgets.interact(assembly_experiment, assembly_min=assembly_slider)
    """)
    md("""
    ### Task 4 — make a control yourself

    TODO: copy `assembly_experiment`, give it a `testing_min` argument, and pass both capacities
    into `solve_product_mix`. Add a second `IntSlider` to `widgets.interact`. Check that a direct
    function call and the same slider settings produce the same result.
    Then add a `pro_profit` control and change the plot title to show its value.

    **Predict → run → explain:** increase Assembly from 350 to 800. Does profit rise throughout?
    Now increase Testing: does this change which resource is binding? Record results before
    opening the supplied multi-control experiment below.
    """)
    md("""
    ### A complete experiment bench

    Minimum orders can make the model infeasible. The callback checks status and explains a
    necessary capacity check instead of plotting invalid values. The same function supports the fallback.

    `mix_experiment(assembly_min=350, testing_min=180, pro_profit=70, min_mini=0,
    integer=False)` accepts capacities in minutes/day, Pro profit in PLN/kit, a Mini order
    in kits/day, and the whole-kit switch. It packages that order as `minimum={"Mini": min_mini}`,
    calls the solver, prints status, and either explains the capacity check or displays
    the checked tables and plot. It returns the solver-result dictionary for further analysis.
    Reusing it keeps the direct named call below and the multi-control bench consistent.
    """)
    code(r"""
    def mix_experiment(assembly_min=350, testing_min=180, pro_profit=70,
                       min_mini=0, integer=False):
        '''Solve and display a product-mix experiment; return its result dict.

        Capacities default to 350/180 min/day, pro_profit to 70 PLN/kit,
        min_mini to zero kits/day, and integer to False (continuous LP).
        Uses solve_product_mix, plot_product_mix, and global display.
        Always prints status/model type. Nonoptimal results display a necessary
        Mini-order capacity check; optimal results display production/resource
        tables and the chart. The return structure is solve_product_mix's.
        '''
        # Map the simple Mini-order control to the solver's order dictionary.
        result = solve_product_mix(assembly_min, testing_min, pro_profit,
                                   minimum={"Mini": min_mini}, integer=integer)
        print("Status:", result["status"], "|", "Integer" if integer else "Continuous LP")
        # Stop before reading quantities or plotting if the model has no optimum.
        if result["status"] != "Optimal":
            print(f"The Mini order alone needs {20*min_mini} assembly and {15*min_mini} testing minutes.")
            print("Compare those amounts with the capacities; reduce the order or add enough time.")
            return result
        display(result["variables"].round(4))
        display(result["resources"].round(4))
        plot_product_mix(result)
        return result

    # Always available without sliders: change these assumptions and rerun.
    manual_result = mix_experiment(assembly_min=350, testing_min=180,
                                   pro_profit=70, min_mini=0, integer=False)
    """)
    md("""
    ### Connect the experiment to named controls

    `update_mix(**parameters)` is the display callback: it forwards a dictionary of named
    values to `mix_experiment`, which handles solving, status checks, tables, and plots.
    It returns `None`, so the widget output does not echo a large result dictionary.
    It uses the existing experiment helper rather than duplicating its model or checks.

    The `controls` dictionary maps each argument name to its widget. `interactive_output`
    reads the widget values and calls `update_mix` with those names; `**parameters` passes
    the resulting values as keyword arguments. Units and defaults match `mix_experiment`.
    The `VBox` arranges controls while `live_output` captures the helper's displays.
    """)
    code(r"""
    # interactive_output connects several named widgets to the callback.
    # The wrapper ignores the returned result so only our tables/plots are displayed.
    def update_mix(**parameters):
        '''Forward named widget values to mix_experiment; return None.

        parameters contains assembly_min/testing_min (min/day), pro_profit
        (PLN/kit), min_mini (kits/day), and integer (bool). Supplied controls
        start at 350, 180, 70, 0, and False; omitted values use the experiment's
        defaults. Uses global mix_experiment, whose status/table/plot displays
        appear in live_output. Deliberately does not echo its result dictionary.
        '''
        # Reuse the existing status-guarded experiment for every control change.
        mix_experiment(**parameters)

    # Keys are callback argument names; widgets supply values in the documented units.
    controls = {
        "assembly_min": widgets.IntSlider(value=350, min=100, max=900, step=10,
            description="Assembly", continuous_update=False),
        "testing_min": widgets.IntSlider(value=180, min=60, max=360, step=10,
            description="Testing", continuous_update=False),
        "pro_profit": widgets.IntSlider(value=70, min=20, max=140, step=5,
            description="Profit Pro", continuous_update=False),
        "min_mini": widgets.IntSlider(value=0, min=0, max=20, step=1,
            description="Min Mini", continuous_update=False),
        "integer": widgets.Checkbox(value=False, description="Whole kits"),
    }
    live_output = widgets.interactive_output(update_mix, controls)
    display(widgets.VBox(list(controls.values())), live_output)
    """)
    md("""
    ## 7. Sensitivity: a curve is more informative than one changed solve

    Sweep one assumption while holding the others fixed. Each row is a fresh optimization.
    A curve shows both the region where capacity has value and the plateau where another resource
    takes over. This is **scenario analysis**; a shadow price summarizes only a local part of the curve.
    """)
    code(r"""
    # Re-solve each capacity independently; compare profit and production on shared axes.
    sweep_rows = []
    for assembly_minutes in range(100, 901, 25):
        result = solve_product_mix(assembly_min=assembly_minutes)
        sweep_rows.append({"assembly_min": assembly_minutes, "status": result["status"],
                           "profit_PLN": result["profit"], **result["quantities"]})
    sweep = pd.DataFrame(sweep_rows)
    display(sweep.head())
    fig, axes = plt.subplots(1, 2, figsize=(11, 4))
    axes[0].plot(sweep["assembly_min"], sweep["profit_PLN"], "o-")
    axes[0].axvline(350, color="gray", linestyle="--", label="Baseline")
    axes[0].set(xlabel="Assembly capacity (min/day)", ylabel="Optimal profit (PLN/day)",
                title="When does more capacity stop helping?")
    axes[0].legend()
    for product in PRODUCTS:
        axes[1].plot(sweep["assembly_min"], sweep[product], "o-", label=product)
    axes[1].set(xlabel="Assembly capacity (min/day)", ylabel="Production (kits/day)",
                title="How does the mix change?")
    axes[1].legend()
    plt.tight_layout()
    plt.show()
    """)
    md("""
    ### Check a shadow price by re-solving

    CBC exposes an LP row's dual value as `.pi`. Compare the prediction `shadow price × extra minutes`
    with the actual objective change. At the baseline, both resource rows bind. After a large change,
    a different constraint can govern the plan. A zero shadow price can occur even on a binding row
    in a degenerate LP; do not equate “binding” with “valuable”.
    """)
    code(r"""
    # Compare the local shadow-price prediction with actual small and large re-solves.
    dual = baseline["resources"].loc["Assembly", "shadow_PLN_per_min"]
    sensitivity_rows = []
    for extra_min in [1, 10, 500]:
        changed = solve_product_mix(assembly_min=350 + extra_min)
        sensitivity_rows.append({
            "extra_assembly_min": extra_min,
            "dual_prediction_PLN": None if dual is None else dual * extra_min,
            "actual_profit_gain_PLN": changed["profit"] - baseline["profit"],
        })
    display(pd.DataFrame(sensitivity_rows))
    """)
    md("""
    ### Task 5 — capacity purchase decision

    TODO: offer A sells 10 extra assembly minutes for 15 PLN/day; offer B sells 500 for 750 PLN/day.
    Subtract each purchase cost from its **re-solved** profit gain. Would you buy either offer?
    Repeat the finite-difference check for one extra testing minute and explain the shadow-price units.
    Why is extrapolating the assembly shadow price to offer B misleading?
    """)
    md("""
    ### Extension: reduced cost and alternative optima

    An LP variable's `.dj` is its **reduced cost**. In a maximization model with a variable at its
    lower bound, a negative reduced cost describes the marginal loss from forcing that variable
    into the plan while re-optimizing the others. Its magnitude is the objective-coefficient
    improvement needed before it can become attractive, within the current LP basis.
    Basic positive variables normally have zero reduced cost. Bound conventions and degeneracy
    require care, so verify an interpretation by changing the coefficient and re-solving.

    Lower Pro's profit to 20 PLN/kit. TODO: explain why Pro is unused, inspect its reduced cost,
    then increase its profit gradually. At 80 PLN/kit, both products earn 2 PLN per assembly minute:
    test whether `(Mini, Pro) = (0, 8.75)` and `(6.25, 5.625)` are both optimal feasible LP plans.
    A solver reports one optimum; it does not list every alternative optimum.
    """)
    code(r"""
    # Change one profit coefficient to inspect reduced costs and alternative LP optima.
    low_pro_profit = solve_product_mix(pro_profit=20)
    display(low_pro_profit["variables"])
    alternate_optimum = solve_product_mix(pro_profit=80)
    print("One optimum at Pro profit 80:", alternate_optimum["quantities"],
          "| profit", alternate_optimum["profit"])
    """)
    md("""
    ## 8. Whole kits: continuous versus integer decisions

    An **LP relaxation** allows fractional quantities; the integer model restricts them to whole
    numbers. For maximization, the relaxation gives an **upper bound** on integer profit.
    Nearest rounding can violate capacities. Rounding down can be feasible but still suboptimal.
    Solve the integer model to choose the best whole-kit plan; LP shadow prices are not integer rates.
    """)
    code(r"""
    # Contrast rounding a divisible plan with optimizing whole-kit decisions directly.
    integer_result = solve_product_mix(integer=True)
    floor_plan = {p: int(np.floor(baseline["quantities"][p])) for p in PRODUCTS}
    floor_profit = sum(PROFIT[p] * floor_plan[p] for p in PRODUCTS)
    comparison = pd.DataFrame([
        {"plan": "LP relaxation", **baseline["quantities"], "profit_PLN": baseline["profit"]},
        {"plan": "Round LP down", **floor_plan, "profit_PLN": floor_profit},
        {"plan": "Integer optimum", **integer_result["quantities"], "profit_PLN": integer_result["profit"]},
    ])
    display(comparison)
    plot_product_mix(integer_result)
    print("Integrality gap (PLN):", baseline["profit"] - integer_result["profit"])
    """)
    md("""
    ## 9. Infeasibility is a result to interpret

    A 13-Mini minimum order needs 195 testing minutes before making any Pro kit; only 180 are
    available. That is a direct explanation of infeasibility. Raising assembly time alone cannot repair it.
    """)
    code(r"""
    # Hold the order fixed and repair the limiting station, not an unrelated capacity.
    impossible_order = solve_product_mix(minimum={"Mini": 13})
    print("13-Mini order:", impossible_order["status"])
    repaired_order = solve_product_mix(testing_min=200, minimum={"Mini": 13})
    print("After increasing Testing to 200:", repaired_order["status"])
    if repaired_order["status"] == "Optimal":
        display(repaired_order["resources"])
    """)
    md("""
    ## 10. Student investigation and recommendation

    Keep an experiment log. Change one assumption at a time before trying combinations.

    | Scenario | Prediction | Changed assumption + units | Status | Mix | Profit | Slack | Explanation |
    |:--|:--|:--|:--|:--|:--|:--|:--|
    | Baseline | | | | | | | |
    | More assembly | | | | | | | |
    | More testing | | | | | | | |
    | Pro price change | | | | | | | |
    | Required order | | | | | | | |

    TODO: submit your notebook with:

    1. The LP written in symbols and the meaning/units of each variable.
    2. A resource plot you modified and a two-control slider you built yourself.
    3. At least four changed scenarios, including an infeasible one and its repair.
    4. One shadow-price prediction checked by re-solving, and one large change where it fails.
    5. A recommended plan for **whole kits today**, its profit and resource slack, and the capacity
       purchase you would accept or reject. State one limitation of the assumptions.

    **Bridge:** Lab 2 minimizes blending cost while meeting quality requirements; it will use equality
    constraints and `>=` surplus. Lab 3 allocates shipments and cuts integer stock bars. Lab 4 adds
    start times and binary decisions to schedule shared stations.

    References for further reading: [PuLP source and 3.x releases](https://github.com/coin-or/pulp),
    [Matplotlib quick start](https://matplotlib.org/stable/users/explain/quick_start.html),
    [ipywidgets: Using Interact](https://ipywidgets.readthedocs.io/en/latest/examples/Using%20Interact.html).
    """)

    # Existing IDs stay stable when helper introductions are added.
    cell_ids = ([f"lab1-{i:02d}" for i in range(27)] + ["lab1-control-intro"]
                + [f"lab1-{i:02d}" for i in range(27, 40)])
    for cell, cell_id in zip(cells, cell_ids, strict=True):
        cell.id = cell_id
    notebook = nbf.v4.new_notebook(cells=cells)
    notebook.metadata = {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "version": "3.11"},
        "colab": {"name": "lab_auto_1.ipynb", "provenance": []},
    }
    nbf.validate(notebook)
    nbf.write(notebook, ROOT / "lab_auto_1.ipynb")
    print(f"Built lab_auto_1.ipynb ({len(cells)} cells)")


if __name__ == "__main__":
    build()
