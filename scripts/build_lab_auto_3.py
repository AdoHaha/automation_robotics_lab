"""Generate the self-contained, output-free Colab notebook for Lab 3."""
from pathlib import Path
import textwrap
import nbformat as nbf

ROOT = Path(__file__).resolve().parents[1]


def build_notebook():
    cells = []
    def add(kind, source):
        cell = getattr(nbf.v4, f"new_{kind}_cell")(textwrap.dedent(source).strip())
        cell.id = f"lab3-{len(cells):02d}"
        cells.append(cell)
    def md(source): add("markdown", source)
    def code(source): add("code", source)

    md(r'''
    # Lab 3: Move Materials, Route Flow, and Cut Stock

    [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/AdoHaha/automation_robotics_lab/blob/master/lab_auto_3.ipynb)

    A robotics lab is preparing demonstration kits. Materials must reach the right stations, pass through a handling network, and be cut into useful pieces. You are the operations planner: recommend a feasible plan and explain what changes when a lane closes or demand grows.

    Lab 0 explores Python tables, loops, functions, and plotting. Labs 1 and 2 use PuLP for allocation and blending. Here we reuse the same **variables → objective → constraints → solve → check → interpret** workflow for movement and cutting decisions.

    We will formulate transportation and flow LPs, read cost and capacity bottlenecks, generate cutting patterns, and explain why a fractional solution cannot be used as a physical cutting plan.

    All inputs are embedded; this notebook works in a fresh Google Colab runtime without uploading files.
    ''')
    md(r'''
    ## 0. Runtime setup

    Run cells from top to bottom. The setup installs the packages directly into the notebook runtime. PuLP calls its bundled CBC solver; no solver account or API key is needed. Widgets are optional: every experiment also has a normal function call.
    ''')
    code(r'''
    # Install notebook dependencies, then prepare plotting and the CBC solver.
    %pip install -q 'pulp>=3.3,<4' numpy pandas matplotlib networkx ipywidgets
    %matplotlib inline

    from itertools import product
    import math
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    from matplotlib.patches import Patch
    import networkx as nx
    import pulp
    from IPython.display import display

    # Enable the optional widget display only when running inside Colab.
    try:
        from google.colab import output
        output.enable_custom_widget_manager()
    except ImportError:
        pass  # Local Jupyter does not have google.colab.

    plt.rcParams.update({"figure.figsize": (9, 4), "axes.spines.top": False,
                         "axes.spines.right": False, "font.size": 11})
    CBC = pulp.PULP_CBC_CMD(msg=False)
    if not CBC.available():
        raise RuntimeError("CBC is unavailable. Rerun the setup cell in a fresh runtime.")
    print("PuLP", pulp.__version__, "| CBC ready")
    ''')
    md(r'''
    ## 1. Transportation: which supplier serves which station?

    Two stores send material to three robot-cell stations. We measure material in **kg** and shipping cost in **PLN/kg**. Stores have maximum available quantities; the stations require exact deliveries. Unused stock is allowed and free to keep. No transport capacity limit is assumed for an open lane.

    Before solving, look at the cost table: **predict** which store should supply Test. Can choosing the cheapest lane separately for every station violate a store's supply limit?
    ''')
    code(r'''
    # Tuple keys (store, station) identify one lane; costs are PLN per shipped kg.
    SUPPLY = {"North": 50, "South": 40}  # kg available
    DEMAND = {"Assembly": 30, "Test": 35, "Packing": 15}  # kg required
    COST = {("North", "Assembly"): 2, ("North", "Test"): 6,
            ("North", "Packing"): 4, ("South", "Assembly"): 5,
            ("South", "Test"): 2, ("South", "Packing"): 3}  # PLN/kg
    display(pd.DataFrame({j: {i: COST[i, j] for i in SUPPLY} for j in DEMAND})
            .rename_axis("Shipping cost (PLN/kg)"))
    display(pd.Series(SUPPLY, name="Available kg").to_frame())
    display(pd.Series(DEMAND, name="Required kg").to_frame())
    print("Available:", sum(SUPPLY.values()), "kg | Required:", sum(DEMAND.values()), "kg")
    ''')
    md(r'''
    ### From story to equations

    Let $x_{ij}\geq0$ be **kg sent from store $i$ to station $j$**. A lane is one directed store–station pair.

    $$\min \sum_{(i,j)\in A} c_{ij}x_{ij}\quad\text{(PLN)}$$
    $$\sum_{j:(i,j)\in A}x_{ij}\leq s_i\quad\text{for each store }i\quad\text{(kg)}$$
    $$\sum_{i:(i,j)\in A}x_{ij}=d_j\quad\text{for each station }j\quad\text{(kg)}$$

    $A$ contains the open lanes. We use **≤ for availability**, and **= for exact delivery**. Forcing every store to ship its full supply would be infeasible here: 90 kg are available but only 80 kg are ordered.

    The next cell is a small guided PuLP model. `lpSum` builds a linear expression; it does not choose the quantities. CBC chooses them when we call `solve`.
    ''')
    code(r'''
    # Build one variable per lane, then impose store availability and exact station orders.
    guided = pulp.LpProblem("Guided_transportation", pulp.LpMinimize)
    x = {lane: pulp.LpVariable(f"kg_{lane[0]}_{lane[1]}", lowBound=0)
         for lane in COST}
    guided += pulp.lpSum(COST[lane] * x[lane] for lane in COST), "shipping_PLN"
    for store in SUPPLY:
        guided += pulp.lpSum(x[store, station] for station in DEMAND) <= SUPPLY[store]
    for station in DEMAND:
        guided += pulp.lpSum(x[store, station] for store in SUPPLY) == DEMAND[station]
    # Solve before reading values; the status guard protects the delivery table.
    guided.solve(CBC)
    print("Status:", pulp.LpStatus[guided.status])
    if guided.status == pulp.LpStatusOptimal:
        print("Minimum shipping cost:", pulp.value(guided.objective), "PLN")
        display(pd.DataFrame([{"store": i, "station": j, "kg": v.value()}
                              for (i, j), v in x.items()]))
    else:
        print("There is no optimal delivery plan to display.")
    ''')
    md(r'''
    ### Reuse the model and check the result

    To compare scenarios safely, build a **new model for each scenario**. The helper returns status, objective, and a shipment table. It reads variable values only after an optimal solve. An infeasible model is a useful result: the requested service cannot be delivered under the assumptions.

    A status check is separate from a physical check: even an optimal model might encode the wrong story. The assertions below verify store limits, exact deliveries, and the cost calculation.

    **Helper workflow:** `solve_transport` accepts supply/demand dictionaries and a cost dictionary keyed by `(store, station)` tuples, with optional closed-lane tuples. It copies inputs, builds and solves a fresh model, checks the plan, and returns one result dictionary. The `shipments` DataFrame has stores as rows and stations as columns, making totals and plots easy to reuse for each scenario.
    ''')
    code(r'''
    def solve_transport(supply=None, demand=None, costs=None, closed_lanes=()):
        """Solve one transportation scenario using continuous shipment quantities.

        Supply and demand are dictionaries of kg indexed by store/station; None
        uses global SUPPLY/DEMAND. Costs maps (store, station) tuples to PLN/kg;
        None uses COST. closed_lanes defaults to an empty iterable of tuple keys.
        Uses global CBC. Returns a dictionary with status, cost (PLN), shipments
        (a DataFrame: store rows, station columns, kg), model, and copied inputs.
        Cost and shipments are None unless Optimal. Validates input availability,
        orders, and cost arithmetic; does not display or plot the result."""
        # Copy scenario inputs so experiments do not alter the shared base data.
        supply = dict(SUPPLY if supply is None else supply)
        demand = dict(DEMAND if demand is None else demand)
        costs = dict(COST if costs is None else costs)
        if any(v < 0 for v in [*supply.values(), *demand.values()]):
            raise ValueError("Supply and demand must be nonnegative.")
        # A tuple key denotes one directed lane; remove closed keys before modeling.
        closed = set(closed_lanes)
        lanes = [(i, j) for i in supply for j in demand if (i, j) not in closed]
        if any(lane not in costs for lane in lanes):
            raise ValueError("Each open lane needs a cost.")
        # Rebuild the objective and constraints for this scenario.
        model = pulp.LpProblem("Transportation", pulp.LpMinimize)
        ship = {lane: pulp.LpVariable(f"ship_{k}", lowBound=0)
                for k, lane in enumerate(lanes)}
        model += pulp.lpSum(costs[lane] * ship[lane] for lane in lanes), "shipping_cost"
        for k, i in enumerate(supply):
            model += pulp.lpSum(ship[i, j] for j in demand if (i, j) in ship) <= supply[i], f"supply_{k}"
        for k, j in enumerate(demand):
            model += pulp.lpSum(ship[i, j] for i in supply if (i, j) in ship) == demand[j], f"demand_{k}"
        # Only an optimal result supplies quantities for our physical checks.
        model.solve(CBC)
        status = pulp.LpStatus[model.status]
        result = {"status": status, "cost": None, "shipments": None, "model": model,
                  "supply": supply, "demand": demand, "costs": costs, "closed_lanes": closed}
        if status != "Optimal":
            return result
        # Put lane values into a store-by-station kg table and audit its totals.
        table = pd.DataFrame(0.0, index=list(supply), columns=list(demand))
        for lane, variable in ship.items():
            table.loc[lane[0], lane[1]] = max(0.0, variable.value())
        assert (table.sum(axis=1) <= pd.Series(supply) + 1e-6).all()
        assert np.allclose(table.sum(axis=0), pd.Series(demand), atol=1e-6)
        objective = pulp.value(model.objective)
        assert math.isclose(objective, sum(costs[lane] * table.loc[lane[0], lane[1]]
                                          for lane in lanes), abs_tol=1e-5)
        result.update(cost=objective, shipments=table)
        return result

    # Solve the base case and display supply slack and demand residuals.
    transport_base = solve_transport()
    display(transport_base["shipments"].rename_axis("Shipped kg"))
    supply_audit = pd.DataFrame({"available_kg": pd.Series(SUPPLY),
                                 "shipped_kg": transport_base["shipments"].sum(axis=1)})
    supply_audit["unused_kg (slack)"] = supply_audit["available_kg"] - supply_audit["shipped_kg"]
    supply_audit["binding"] = np.isclose(supply_audit["unused_kg (slack)"], 0)
    display(supply_audit)
    print("Demand equality residuals (delivered − ordered, kg):")
    display((transport_base["shipments"].sum(axis=0) - pd.Series(DEMAND)).to_frame("residual_kg"))
    print("Minimum cost:", transport_base["cost"], "PLN")
    ''')
    md(r'''
    ### Two views of the same delivery plan

    **Slack** in a supply constraint is available minus shipped kg. Zero slack means it is **binding** at this solution. A demand equality has a residual (delivered minus ordered), which should be zero; it does not have spare capacity. Binding does not by itself prove that buying more supply will save money. Try a scenario and compare its objective.

    Thick arrows carry more material. Each open lane is labeled **shipped kg / cost per kg**; a dashed line marks a closed lane. The heatmap helps you compare quantities without tracing crossing arrows. A zero shipment means the optimizer did not use that lane; it does not mean the lane is unavailable.

    **Plot helper:** pass a `solve_transport` result to `plot_transport`. It checks status, builds a directed graph from lane tuples, places stores/stations in two drawing columns, and renders the shipment table as a heatmap. Positions are chosen for readability, not geographic distances. Reuse it after any transportation experiment.
    ''')
    code(r'''
    def plot_transport(result):
        """Display a delivery network and shipment heatmap for solve_transport output.

        result is the dictionary returned by solve_transport, with kg quantities
        and PLN/kg lane costs. Prints a status message instead of a figure when
        not Optimal. Node positions are diagram coordinates, not real distances;
        line widths encode kg and heatmap cells show the shipment DataFrame.
        Uses global nx, np, and plt. Displays the figure and returns None."""
        # Guard the plot so infeasible solver values never appear as shipments.
        if result["status"] != "Optimal":
            print("No feasible plan to plot. Status:", result["status"])
            return
        table = result["shipments"]
        stores, stations = list(table.index), list(table.columns)
        graph = nx.DiGraph()
        graph.add_nodes_from(stores + stations)
        graph.add_edges_from((i, j) for i in stores for j in stations)
        # Separate stores and stations into two columns in drawing coordinates.
        positions = {i: (0, y) for i, y in zip(stores, np.linspace(1, -1, len(stores)))}
        positions.update({j: (2, y) for j, y in zip(stations, np.linspace(1.3, -1.3, len(stations)))})
        fig, axes = plt.subplots(1, 2, figsize=(15, 5), gridspec_kw={"width_ratios": [1.8, 1]})
        labels = {i: f"{i}\n≤ {result['supply'][i]} kg" for i in stores}
        labels.update({j: f"{j}\n= {result['demand'][j]} kg" for j in stations})
        nx.draw_networkx_nodes(graph, positions, nodelist=stores, node_color="#cce7ff", node_size=2700, ax=axes[0])
        nx.draw_networkx_nodes(graph, positions, nodelist=stations, node_color="#d3f0db", node_size=2700, ax=axes[0])
        nx.draw_networkx_labels(graph, positions, labels=labels, font_size=10, ax=axes[0])
        # Encode lane use with width; draw closures distinctly from unused open lanes.
        for lane in graph.edges:
            closed = lane in result["closed_lanes"]
            value = table.loc[lane[0], lane[1]]
            nx.draw_networkx_edges(graph, positions, edgelist=[lane], ax=axes[0],
                                   width=1 + value / 12, arrowsize=20, node_size=2700,
                                   edge_color="#c44e52" if closed else "#4878a8",
                                   style="dashed" if closed else "solid")
        edge_labels = {lane: "CLOSED" if lane in result["closed_lanes"] else
                       f"{table.loc[lane[0], lane[1]]:g} kg / {result['costs'][lane]:g} PLN/kg"
                       for lane in graph.edges}
        nx.draw_networkx_edge_labels(graph, positions, edge_labels=edge_labels,
                                     label_pos=0.68, font_size=8, rotate=False, ax=axes[0])
        axes[0].set_title("Delivery network: quantity / unit cost")
        axes[0].margins(0.25)
        axes[0].axis("off")
        # Draw the same shipment quantities as an annotated matrix.
        heat = axes[1].imshow(table.to_numpy(), cmap="Blues", vmin=0)
        axes[1].set_xticks(range(len(stations)), stations, rotation=20)
        axes[1].set_yticks(range(len(stores)), stores)
        for row in range(len(stores)):
            for col in range(len(stations)):
                axes[1].text(col, row, f"{table.iloc[row, col]:g}", ha="center", va="center",
                             color="white" if table.iloc[row, col] > table.to_numpy().max() / 2 else "black")
        fig.colorbar(heat, ax=axes[1], shrink=0.7, label="Shipped kg")
        axes[1].set_title(f"Minimum cost: {result['cost']:g} PLN")
        plt.tight_layout()
        plt.show()

    plot_transport(transport_base)
    ''')
    md(r'''
    ### Task 1 — close a lane and stress demand

    **Prediction:** What will happen to cost if South → Test closes? Can closing a lane ever reduce the optimal cost while all other data stay fixed?

    Run the comparisons below. A higher Assembly demand also tests feasibility. Total supply ≥ total demand is necessary, but with missing lanes it is not always sufficient.

    **Record:** scenario, changed parameter, status, cost change, one changed shipment. **Recommendation:** which disruption needs a new supplier rather than just rerouting?
    ''')
    code(r'''
    # Keep each scenario result, including infeasible statuses, in one comparison table.
    transport_scenarios = {
        "Base": transport_base,
        "South–Test closed": solve_transport(closed_lanes=[("South", "Test")]),
        "Assembly needs 55 kg": solve_transport(demand={**DEMAND, "Assembly": 55}),
        "Both Assembly lanes closed": solve_transport(closed_lanes=[("North", "Assembly"), ("South", "Assembly")]),
    }
    display(pd.DataFrame([{"scenario": name, "status": result["status"], "cost_PLN": result["cost"]}
                          for name, result in transport_scenarios.items()]))
    plot_transport(transport_scenarios["South–Test closed"])
    plot_transport(transport_scenarios["Assembly needs 55 kg"])
    ''')
    code(r'''
    # Runnable experiment workspace. Change ONE assumption, then rerun.
    my_transport = solve_transport(demand={**DEMAND, "Packing": 20})
    print("My scenario:", my_transport["status"], "| cost:", my_transport["cost"])
    plot_transport(my_transport)
    # TODO: sweep Packing demand from 5 to 35 kg, plot cost vs demand,
    # and mark infeasible cases separately (None is not a zero cost).
    ''')
    md(r'''
    ## 2. Network flow: add transfer hubs and lane capacities

    The robot cell now receives 80 kg from one factory through two handling hubs. A shipment can pass through several arcs before reaching a station. Each arc has a **capacity (kg)** and a **handling/shipping cost (PLN/kg)**. Flow may split at a node; this models divisible material, not the indivisible route of one truck.

    Transportation was a two-layer network. Adding intermediate nodes and per-arc capacities turns it into a **minimum-cost flow** model. We solve an actual LP on the graph; the diagram is a view of those decision variables.

    Let $f_{uv}$ be kg on arc $u\to v$, bounded by its capacity $U_{uv}$. Let $b_v$ be net supply: **positive at the source, zero at hubs, negative at consuming stations**.

    $$\min \sum_{(u,v)\in A}c_{uv}f_{uv}\qquad 0\leq f_{uv}\leq U_{uv}$$
    $$\sum_{w:(v,w)\in A}f_{vw}-\sum_{u:(u,v)\in A}f_{uv}=b_v\quad\text{at EVERY node}$$

    The sign is **outflow − inflow**. At a hub, it equals 0: no material appears or disappears. At Test, it equals −35: 35 kg are consumed. This example fixes source supply to the exact 80 kg needed; unlike section 1, there is no optional leftover supply inside this network. Check that $\sum_v b_v=0$.
    ''')
    code(r'''
    # Node net supplies use outflow minus inflow: sources positive, consumers negative.
    BALANCE = {"Factory": 80, "Hub A": 0, "Hub B": 0,
               "Assembly": -30, "Test": -35, "Packing": -15}
    # Dictionary value: (capacity kg, cost PLN/kg).
    ARCS = {("Factory", "Hub A"): (50, 1), ("Factory", "Hub B"): (40, 1),
            ("Hub A", "Assembly"): (40, 1), ("Hub A", "Test"): (40, 5),
            ("Hub A", "Packing"): (30, 3), ("Hub B", "Assembly"): (30, 4),
            ("Hub B", "Test"): (40, 1), ("Hub B", "Packing"): (30, 2)}
    display(pd.DataFrame([{"from": u, "to": v, "capacity_kg": cap, "cost_PLN_per_kg": cost}
                          for (u, v), (cap, cost) in ARCS.items()]))
    print("Total net supply:", sum(BALANCE.values()), "kg")
    ''')
    md(r'''
    ### Reusable flow solver

    `solve_flow(arcs, balance)` takes an arc dictionary keyed by `(from_node, to_node)` tuples and a dictionary of node net supplies. Each arc value is `(capacity_kg, cost_PLN_per_kg)`. It checks inputs, builds bounded flows and conservation equalities, solves with CBC, and audits the result. The returned dictionary stores an arc-to-kg `flows` mapping, cost, status, and model; reuse it in capacity scenarios and convert it into a DataFrame when you want a readable arc table.
    ''')
    code(r'''
    def solve_flow(arcs=None, balance=None):
        """Solve continuous minimum-cost flow with conservation at every node.

        arcs maps (from_node, to_node) tuples to (capacity kg, cost PLN/kg);
        None uses global ARCS. balance maps nodes to net supply kg (out minus in);
        None uses BALANCE. Uses global CBC. Returns a dictionary containing status,
        cost (PLN), flows (arc-to-kg mapping), model, and copied inputs. Cost and
        flows remain None unless Optimal. Validates balance, capacities, and the
        solved conservation equations; does not display or plot the result."""
        # Copy inputs and check that every node can participate in conservation.
        arcs = dict(ARCS if arcs is None else arcs)
        balance = dict(BALANCE if balance is None else balance)
        if not math.isclose(sum(balance.values()), 0, abs_tol=1e-8):
            raise ValueError("Net supplies must sum to zero.")
        if any(cap < 0 for cap, cost in arcs.values()):
            raise ValueError("Arc capacities must be nonnegative.")
        if any(u not in balance or v not in balance for u, v in arcs):
            raise ValueError("Every arc endpoint needs a node balance.")
        # Build one bounded continuous variable per arc and one equality per node.
        model = pulp.LpProblem("Minimum_cost_flow", pulp.LpMinimize)
        flow = {arc: pulp.LpVariable(f"flow_{k}", lowBound=0, upBound=arcs[arc][0])
                for k, arc in enumerate(arcs)}
        model += pulp.lpSum(arcs[arc][1] * flow[arc] for arc in arcs), "cost_PLN"
        for k, node in enumerate(balance):
            outgoing = pulp.lpSum(flow[u, v] for u, v in arcs if u == node)
            incoming = pulp.lpSum(flow[u, v] for u, v in arcs if v == node)
            model += outgoing - incoming == balance[node], f"conservation_{k}"
        # Solve first; return only status and inputs if no optimal flow exists.
        model.solve(CBC)
        status = pulp.LpStatus[model.status]
        result = {"status": status, "cost": None, "flows": None,
                  "model": model, "arcs": arcs, "balance": balance}
        if status != "Optimal":
            return result
        # Verify all-node conservation and arc capacities using solved kg quantities.
        values = {arc: max(0.0, variable.value()) for arc, variable in flow.items()}
        for node, required in balance.items():
            net = sum(value for (u, v), value in values.items() if u == node) - sum(
                      value for (u, v), value in values.items() if v == node)
            assert math.isclose(net, required, abs_tol=1e-6)
        assert all(-1e-6 <= values[arc] <= arcs[arc][0] + 1e-6 for arc in arcs)
        result.update(cost=pulp.value(model.objective), flows=values)
        return result

    # Display arc headroom and an explicit out-minus-in conservation audit.
    flow_base = solve_flow()
    print("Status:", flow_base["status"], "| Minimum cost:", flow_base["cost"], "PLN")
    if flow_base["status"] == "Optimal":
        display(pd.DataFrame([{"from": u, "to": v, "flow_kg": value,
                               "capacity_kg": ARCS[u, v][0],
                               "remaining_capacity_kg": ARCS[u, v][0] - value}
                              for (u, v), value in flow_base["flows"].items()]))
        conservation_audit = []
        for node, required in BALANCE.items():
            outgoing = sum(f for (u, v), f in flow_base["flows"].items() if u == node)
            incoming = sum(f for (u, v), f in flow_base["flows"].items() if v == node)
            conservation_audit.append({"node": node, "outflow_kg": outgoing,
                                       "inflow_kg": incoming, "net_supply_kg": required,
                                       "equality_residual_kg": outgoing - incoming - required})
        display(pd.DataFrame(conservation_audit))
    ''')
    md(r'''
    ### Read a bottleneck diagram

    Arc labels show **flow / capacity in kg**. Red arcs are at capacity; thin gray arcs are unused. An arc at capacity is not automatically worth expanding: there must also be a useful cheaper path for the extra material. Compare the scenario's objective to test its economic effect.

    **Plot helper:** `plot_flow(result)` reads a solved arc dictionary and node balances, draws the six example nodes at explicit `(x, y)` drawing positions, and labels quantities, capacities, and costs. It returns no data; reuse the numerical dictionary for calculations. Add positions if you extend the network with new nodes.
    ''')
    code(r'''
    def plot_flow(result):
        """Display the capacity diagram for a solve_flow result dictionary.

        Arc flows and capacities are kg; arc costs are PLN/kg. Non-optimal results
        print a status message. Fixed diagram positions cover the six example
        nodes, so extend pos when adding nodes. Red marks a saturated arc;
        width shows flow. Uses global nx and plt, displays a figure, returns None."""
        if result["status"] != "Optimal":
            print("No feasible network flow to plot. Status:", result["status"])
            return
        # Build the graph from model arc keys, then place the example nodes for readability.
        graph = nx.DiGraph()
        graph.add_nodes_from(result["balance"])
        graph.add_edges_from(result["arcs"])
        pos = {"Factory": (0, 0), "Hub A": (1.6, 1), "Hub B": (1.6, -1),
               "Assembly": (3.8, 1.5), "Test": (3.8, 0), "Packing": (3.8, -1.5)}
        fig, ax = plt.subplots(figsize=(12, 6))
        labels = {node: f"{node}\nb = {b:+g} kg" for node, b in result["balance"].items()}
        nx.draw_networkx_nodes(graph, pos, node_color="#dce9f3", node_size=3000, ax=ax)
        nx.draw_networkx_labels(graph, pos, labels=labels, font_size=10, ax=ax)
        # Compare flow with capacity to color saturated arcs; widths represent kg.
        for arc, (cap, cost) in result["arcs"].items():
            value = result["flows"][arc]
            color = "#c44e52" if abs(value - cap) < 1e-6 else ("#4878a8" if value > 1e-6 else "#aaaaaa")
            nx.draw_networkx_edges(graph, pos, edgelist=[arc], edge_color=color,
                                   width=1 + value / 14, node_size=3000, arrowsize=20, ax=ax)
        edge_labels = {arc: f"{result['flows'][arc]:g}/{cap:g} kg\n{cost:g} PLN/kg"
                       for arc, (cap, cost) in result["arcs"].items()}
        nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels,
                                     label_pos=0.66, rotate=False, font_size=8, ax=ax)
        ax.set_title(f"Minimum-cost flow: {result['cost']:g} PLN | red = saturated arc")
        ax.margins(0.18)
        ax.axis("off")
        plt.tight_layout()
        plt.show()

    plot_flow(flow_base)
    ''')
    md(r'''
    ### Task 2 — shrink the cheaper hub

    **Predict:** if Factory → Hub B capacity falls from 40 to 30 kg, can the cell still receive all 80 kg? Which flow must increase? What happens at 20 kg?

    Explain feasibility using a **cut**: draw a line separating Factory from all other nodes. The total capacity of outgoing arcs across that line must be at least 80 kg. This gives a hand-check for these scenarios, without running CBC.

    **Record:** capacity, solver status, cost, new saturated arcs. **Recommendation:** should the lab pay 20 PLN per shift to restore Hub B capacity from 30 to 40 kg? Compare the premium with shipping-cost savings.

    **Scenario helper:** `flow_with_hub_b_capacity(capacity)` accepts one capacity in kg, copies the shared arc table, replaces Factory → Hub B's limit, and calls `solve_flow`. It returns the same result dictionary, so a single call, a comparison loop, and a plot all use the same model construction.
    ''')
    code(r'''
    def flow_with_hub_b_capacity(capacity):
        """Solve the example network with a changed Factory-to-Hub-B limit in kg.

        capacity replaces only that arc capacity in a copy of global ARCS, keeping
        its PLN/kg cost. Uses solve_flow and its default BALANCE/CBC dependencies.
        Returns the same status-safe result dictionary as solve_flow; no display."""
        # Copy the arc table and change only the selected capacity, preserving costs.
        changed = dict(ARCS)
        changed["Factory", "Hub B"] = (capacity, ARCS["Factory", "Hub B"][1])
        return solve_flow(arcs=changed)

    # Reuse the same helper for feasible and infeasible capacity experiments.
    flow_scenarios = {capacity: flow_with_hub_b_capacity(capacity) for capacity in [40, 30, 20]}
    display(pd.DataFrame([{"Hub_B_capacity_kg": capacity, "status": result["status"],
                          "cost_PLN": result["cost"]}
                         for capacity, result in flow_scenarios.items()]))
    plot_flow(flow_scenarios[30])
    plot_flow(flow_scenarios[20])
    ''')
    code(r'''
    # Runnable sweep: missing costs remain NaN for infeasible scenarios.
    capacity_sweep = pd.DataFrame([
        {"capacity_kg": capacity, "status": (r := flow_with_hub_b_capacity(capacity))["status"],
         "cost_PLN": r["cost"]}
        for capacity in range(15, 56, 5)
    ])
    display(capacity_sweep)
    ax = capacity_sweep.plot(x="capacity_kg", y="cost_PLN", marker="o", legend=False)
    ax.set(xlabel="Factory → Hub B capacity (kg)", ylabel="Optimal cost (PLN)",
           title="Capacity value: where does adding capacity stop saving money?")
    ax.grid(alpha=0.3)
    plt.show()
    # TODO: change Hub B → Test capacity instead and compare the cost curve.
    # TODO: add an A → B transfer arc and explain whether it improves this network.
    ''')
    md(r'''
    ## 3. Cutting stock: how many whole bars must we buy?

    The frame-building robot needs pieces of three lengths: **6, 4, and 3 length units**. New bars are 10 units long. The orders are 3, 3, and 4 pieces respectively. To keep the arithmetic transparent, assume **zero saw kerf**, no reuse of offcuts, identical new bars, and permission to make extra pieces. These are teaching assumptions, not a complete fabrication process.

    A **pattern** is a recipe for cutting ONE bar, for example `(1, 1, 0)` means one 6-unit piece, one 4-unit piece, and no 3-unit pieces. It fits exactly: $6+4=10$. `(0, 1, 2)` also fits: $4+3+3=10$.

    **Predict:** ordered material totals $3(6)+3(4)+4(3)=42$ length units. Does $\lceil42/10\rceil=5$ guarantee a five-bar plan? Why might the lengths make a material-volume bound too optimistic?

    We will enumerate **all nonempty fitting patterns**, including patterns with unused space. For only three piece types this is small enough to inspect. Large industrial instances need more sophisticated pattern generation.

    **Pattern helper:** `enumerate_patterns(stock_length, lengths)` takes positive integer lengths in the same unit and returns tuples of piece counts in the order of `lengths`. It bounds each count, combines all possibilities with `itertools.product`, and keeps nonempty patterns that fit. The DataFrame below turns those tuples into labeled count, used-length, and trim columns for inspection.
    ''')
    code(r'''
    # All lengths share one teaching unit; tuple positions match lengths to demands.
    PIECE_LENGTHS = (6, 4, 3)
    PIECE_DEMAND = (3, 3, 4)
    STOCK_LENGTH = 10

    def enumerate_patterns(stock_length, lengths):
        """Return every nonempty fitting integer count tuple for one stock bar.

        stock_length and every item in lengths must be positive integers in the
        same length unit. Each returned tuple follows the order of lengths and
        contains piece counts, not piece lengths. With zero kerf, retain only
        combinations whose total piece length is at most stock_length. Uses
        itertools.product; no solver, global project data, or displays required."""
        if not isinstance(stock_length, int) or stock_length <= 0:
            raise ValueError("Stock length must be a positive integer.")
        if not lengths or any(not isinstance(length, int) or length <= 0 for length in lengths):
            raise ValueError("Piece lengths must be positive integers.")
        # Each piece count has a finite bound; product tests every count combination.
        ranges = [range(stock_length // length + 1) for length in lengths]
        return [counts for counts in product(*ranges)
                if any(counts) and sum(n * length for n, length in zip(counts, lengths)) <= stock_length]

    # Convert count tuples into a table with used length and trim for each pattern.
    patterns = enumerate_patterns(STOCK_LENGTH, PIECE_LENGTHS)
    pattern_table = pd.DataFrame(patterns, columns=[f"pieces_{length}" for length in PIECE_LENGTHS])
    pattern_table.index.name = "pattern_id"
    pattern_table["used_length"] = [sum(n * length for n, length in zip(p, PIECE_LENGTHS)) for p in patterns]
    pattern_table["trim_per_bar"] = STOCK_LENGTH - pattern_table["used_length"]
    display(pattern_table)
    print("Number of fitting nonempty patterns:", len(patterns))
    ''')
    md(r'''
    ### From cutting recipes to an integer model

    Let $y_p$ be the **number of whole bars cut using pattern $p$**, and let $a_{ip}$ count pieces of type $i$ in one use of that pattern.

    $$\min\sum_p y_p\quad\text{(bars)}$$
    $$\sum_p a_{ip}y_p\geq d_i\quad\text{for every piece type }i\quad\text{(pieces)}$$
    $$y_p\in\{0,1,2,\ldots\}$$

    **Why ≥?** We allow overproduction: some patterns can make an extra useful piece while still using the minimum number of bars. If extra pieces are forbidden, change every coverage constraint to equality and resolve; do not just remove pieces from the reported plan.

    **What are we minimizing?** Purchased bars, not trim by itself. Extra pieces occupy material too, so small trim does not necessarily mean no material beyond the order. With multiple optimal plans, CBC may choose any of them.

    The **LP relaxation** permits fractional $y_p$. It gives a lower bound on the required number of bars, but fractions of cutting recipes do not describe a physical plan. Solve the integer model separately: rounding each fractional variable can overbuy bars, and rounding down can miss demand. Even rounding the objective upward is only a lower bound, not a construction of a feasible plan.

    **Solver helper:** `solve_cutting` accepts stock length, piece lengths, piece demands, and switches for integer bars or exact coverage. It regenerates patterns, builds coverage constraints, solves, and checks production/material totals. It returns a dictionary whose `plan` DataFrame lists only used recipes; `produced` counts each piece type. Reuse the same helper for LP bounds, physical plans, and changed-stock experiments.
    ''')
    code(r'''
    def solve_cutting(stock_length=10, lengths=PIECE_LENGTHS, demand=PIECE_DEMAND,
                      integer=True, exact_demand=False):
        """Minimize purchased bars using all fitting patterns for the given lengths.

        stock_length defaults to 10 length units. lengths and demand default to
        PIECE_LENGTHS/PIECE_DEMAND: matching tuples of lengths and required piece
        counts. integer=True enforces whole bars; False solves the LP relaxation.
        exact_demand=False permits extra pieces; True enforces exact coverage.
        Uses enumerate_patterns and global CBC. Returns status, bars, plan (a
        DataFrame of pattern_id, pieces tuple, bars, trim_per_bar), produced piece
        counts, trim/extra_material in length units, model, and inputs. Numerical
        results remain None unless Optimal. Checks coverage, integrality when
        requested, and material accounting; does not display or plot the result."""
        # Match each demand to its piece length, then regenerate patterns for this stock.
        lengths, demand = tuple(lengths), tuple(demand)
        if len(lengths) != len(demand) or any(not isinstance(d, int) or d < 0 for d in demand):
            raise ValueError("Use one nonnegative integer demand per piece length.")
        patterns = enumerate_patterns(stock_length, lengths)
        # A variable counts uses of one whole-bar recipe (fractional only in the LP).
        model = pulp.LpProblem("Cutting_stock", pulp.LpMinimize)
        count = {p: pulp.LpVariable(f"pattern_{p}", lowBound=0,
                                  cat="Integer" if integer else "Continuous")
                 for p in range(len(patterns))}
        model += pulp.lpSum(count.values()), "bars_purchased"
        for i, required in enumerate(demand):
            made = pulp.lpSum(patterns[p][i] * count[p] for p in count)
            model += (made == required if exact_demand else made >= required), f"coverage_{i}"
        # Do not extract physical quantities from an infeasible solve.
        model.solve(CBC)
        status = pulp.LpStatus[model.status]
        result = {"status": status, "bars": None, "plan": None, "produced": None,
                  "trim": None, "extra_material": None, "model": model,
                  "stock_length": stock_length, "lengths": lengths, "demand": demand,
                  "patterns": patterns, "integer": integer}
        if status != "Optimal":
            return result
        quantities = np.array([count[p].value() or 0.0 for p in count], dtype=float)
        if integer:
            assert np.allclose(quantities, np.rint(quantities), atol=1e-6)
            quantities = np.rint(quantities).astype(int)  # Only remove numerical noise after integer solve.
        # Pattern counts times pattern contents yield total pieces of each length.
        produced = np.array([sum(pattern[i] * quantity for pattern, quantity in zip(patterns, quantities))
                             for i in range(len(lengths))])
        if exact_demand:
            assert np.allclose(produced, demand, atol=1e-6)
        else:
            assert (produced >= np.array(demand) - 1e-6).all()
        # Keep used patterns in a compact table and reconcile ordered/extra/trim material.
        plan = pd.DataFrame([{"pattern_id": p, "pieces": patterns[p], "bars": q,
                              "trim_per_bar": stock_length - sum(a * b for a, b in zip(patterns[p], lengths))}
                             for p, q in enumerate(quantities) if q > 1e-7],
                            columns=["pattern_id", "pieces", "bars", "trim_per_bar"])
        bars = float(quantities.sum())
        trim = bars * stock_length - float(np.dot(produced, lengths))
        extra_material = float(np.dot(produced - np.array(demand), lengths))
        assert trim >= -1e-6
        assert math.isclose(bars * stock_length, float(np.dot(demand, lengths)) + extra_material + trim,
                            abs_tol=1e-5)
        result.update(bars=bars, plan=plan, produced=produced, trim=trim,
                      extra_material=extra_material)
        return result

    # Compare the LP bound with a separate whole-bar integer solve.
    cutting_lp = solve_cutting(integer=False)
    cutting_ip = solve_cutting(integer=True)
    display(pd.DataFrame([{"model": label, "status": result["status"], "bars": result["bars"]}
                          for label, result in [("LP relaxation (lower bound)", cutting_lp),
                                                ("Integer cutting plan", cutting_ip)]]))
    if cutting_lp["status"] == "Optimal":
        print("Fractional pattern counts — inspect but do not use as a cutting plan:")
        display(cutting_lp["plan"])
    if cutting_ip["status"] == "Optimal":
        print("Whole-bar cutting plan:")
        display(cutting_ip["plan"])
        display(pd.DataFrame({"length": PIECE_LENGTHS, "ordered_pieces": PIECE_DEMAND,
                              "produced_pieces": cutting_ip["produced"],
                              "extra_pieces": cutting_ip["produced"] - np.array(PIECE_DEMAND)}))
        print("Total trim:", cutting_ip["trim"], "length units")
        print("Material in extra pieces:", cutting_ip["extra_material"], "length units")
    ''')
    md(r'''
    ### Visual inspection: one horizontal row is one purchased bar

    Colored segments are produced pieces; hatched gray segments are trim. The caption checks **purchased material = ordered material + material in extra pieces + trim**. Count the segments yourself and compare with the demand table. Two optimal solutions can have the same number of bars and different trim; report the actual returned plan.

    **Layout helper:** `plot_cutting(result)` takes an integer cutting-result dictionary. It guards status, expands each recipe's bar count into rows, draws pieces from left to right, hatches the remaining trim, and prints a material check. It displays a figure rather than returning a new plan; keep the solver result for numerical comparisons.
    ''')
    code(r'''
    def plot_cutting(result):
        """Display a physical cutting layout from an integer solve_cutting result.

        result contains stock/piece lengths in the same unit, a pattern-plan
        DataFrame, and integer bar counts. Prints a message for non-optimal,
        fractional, or zero-bar results. Expands each used pattern into whole-bar
        rows; piece widths show lengths and hatched space shows trim. Uses global
        plt and Patch. Displays a figure and material-accounting text; returns None."""
        if result["status"] != "Optimal":
            print("No feasible cutting plan to plot. Status:", result["status"])
            return
        if not result["integer"]:
            print("Fractional bars have no physical cutting diagram. Solve the integer model first.")
            return
        lengths, stock = result["lengths"], result["stock_length"]
        colors = plt.get_cmap("tab10").colors
        # Expand the pattern-plan DataFrame so every plotted row is one purchased bar.
        expanded = [row.pieces for row in result["plan"].itertuples() for _ in range(int(row.bars))]
        if not expanded:
            print("Zero demand: no bars are needed.")
            return
        fig, ax = plt.subplots(figsize=(11, max(3.5, 0.55 * len(expanded) + 2)))
        # Advance left along the bar as each piece is drawn; the remainder is trim.
        for row, pattern in enumerate(expanded):
            left = 0
            for i, (count, length) in enumerate(zip(pattern, lengths)):
                for _ in range(count):
                    ax.barh(row, length, left=left, height=0.72, color=colors[i], edgecolor="white")
                    ax.text(left + length / 2, row, str(length), ha="center", va="center", color="white")
                    left += length
            assert left <= stock
            if left < stock:
                ax.barh(row, stock - left, left=left, height=0.72,
                        color="#eeeeee", edgecolor="#777777", hatch="///")
                ax.text((left + stock) / 2, row, f"{stock-left} trim", ha="center", va="center", fontsize=9)
        ax.set_yticks(range(len(expanded)), [f"Bar {i+1}" for i in range(len(expanded))])
        ax.invert_yaxis()
        ax.set(xlim=(0, stock), xlabel="Length units along one stock bar",
               title=f"{len(expanded)} whole bars | trim {result['trim']:g} | extra-piece material {result['extra_material']:g}")
        # Use the same colors in the legend and check total material under the layout.
        legend = [Patch(facecolor=colors[i], label=f"{length}-unit piece") for i, length in enumerate(lengths)]
        legend.append(Patch(facecolor="#eeeeee", edgecolor="#777777", hatch="///", label="Trim"))
        ax.legend(handles=legend, loc="upper center", bbox_to_anchor=(0.5, -0.15), ncol=4)
        plt.tight_layout()
        plt.show()
        ordered_material = sum(d * length for d, length in zip(result["demand"], lengths))
        print(f"Material check: {result['bars']:g} × {stock} = {ordered_material} ordered + "
              f"{result['extra_material']:g} extra-piece material + {result['trim']:g} trim")

    plot_cutting(cutting_ip)
    ''')
    md(r'''
    ### Task 3 — change demand or stock length

    **Predict:** if the stock length increases from 10 to 11, which new patterns become available? Can more stock length ever increase the minimum number of bars if all other assumptions stay fixed?

    Compare the LP bound, the integer plan, and the visual material check. When you change stock length, **regenerate patterns**: reusing the old pattern list would hide new choices.

    **Record:** stock length, piece demand, LP bound, integer bars, trim, extra pieces. **Recommendation:** suppose an 11-unit bar costs 10% more than a 10-unit bar. Which would you buy for the base order? Compare `bars × price_per_bar`, not just trim.
    ''')
    code(r'''
    # Regenerate all patterns for each stock size; compare LP and integer results.
    cutting_scenarios = []
    for stock in [9, 10, 11, 12]:
        lower = solve_cutting(stock_length=stock, integer=False)
        whole = solve_cutting(stock_length=stock)
        cutting_scenarios.append({"stock_length": stock, "status": whole["status"],
                                  "LP_bars": lower["bars"], "integer_bars": whole["bars"],
                                  "trim": whole["trim"], "extra_material": whole["extra_material"]})
    display(pd.DataFrame(cutting_scenarios))
    plot_cutting(solve_cutting(stock_length=11))
    # A deliberate infeasible stress: a 6-unit piece cannot fit a 5-unit bar.
    too_short = solve_cutting(stock_length=5)
    print("Too-short stock:", too_short["status"])
    plot_cutting(too_short)
    ''')
    code(r'''
    # Runnable experiment workspace: keep a normal call as the widget fallback.
    my_cutting = solve_cutting(stock_length=10, demand=(3, 3, 6))
    print("My scenario:", my_cutting["status"], "| bars:", my_cutting["bars"])
    plot_cutting(my_cutting)
    # TODO: compare exact_demand=True with the default demand>= formulation.
    # TODO: produce a table for 3-unit-piece demand from 0 to 10.
    # Explain why whole-bar counts change in steps.
    ''')
    md(r'''
    ## 4. Optional live controls

    The sliders rerun the optimization and redraw the physical plan. Start with a prediction, move **one** control, then explain the result. If widget controls do not appear, edit the arguments in the normal call below; the numerical model and diagrams are identical.

    **Build your own interaction:** the function `cutting_explorer` is a *callback*: its parameters are inputs, and its body solves, prints a table, and draws a plot. `widgets.interactive` matches each slider name to a callback parameter and calls the function when that value changes. `continuous_update=False` waits until you release a slider, which avoids repeatedly running the solver while dragging.

    Compare the smooth, piecewise-linear LP lower bound with the integer plan's step changes when demand grows. The two curves answer different questions.

    This section is optional and is not needed to complete the lab.

    **Callback helper:** `cutting_explorer(stock_length, short_piece_demand)` accepts the two displayed control values, keeps the other piece demands fixed, solves the LP and integer models, and displays the pattern table and bar layout. It returns the integer result dictionary. Test it with a normal function call before connecting sliders, and reuse that call when widgets are unavailable.
    ''')
    code(r'''
    def cutting_explorer(stock_length=10, short_piece_demand=4):
        """Solve and display a cutting scenario from two control values.

        stock_length defaults to 10 length units; short_piece_demand defaults to
        4 pieces of length 3. The 6- and 4-unit demands stay at 3 pieces each.
        Calls solve_cutting twice (integer and LP) using its default piece lengths
        and global CBC, then displays status, a pattern DataFrame, and the integer
        layout through plot_cutting. Returns the integer result dictionary, so
        this callback can also be reused as an ordinary function without widgets."""
        # Convert control values to counts, solve both models, then redraw the whole-bar plan.
        result = solve_cutting(stock_length=int(stock_length), demand=(3, 3, int(short_piece_demand)))
        lower = solve_cutting(stock_length=int(stock_length), demand=(3, 3, int(short_piece_demand)), integer=False)
        print("Status:", result["status"], "| LP bound:", lower["bars"], "| Whole bars:", result["bars"])
        if result["status"] == "Optimal":
            display(result["plan"])
        plot_cutting(result)
        return result

    # Fallback: this works in Colab even when widgets are unavailable.
    explorer_example = cutting_explorer(stock_length=10, short_piece_demand=4)
    ''')
    code(r'''
    # Optional UI: parameter names connect controls to the ordinary callable above.
    try:
        import ipywidgets as widgets
        # Connect named controls to identically named callback parameters.
        controls = widgets.interactive(
            cutting_explorer,
            stock_length=widgets.IntSlider(value=10, min=6, max=14, step=1,
                                            description="Stock length", continuous_update=False),
            short_piece_demand=widgets.IntSlider(value=4, min=0, max=10, step=1,
                                                 description="3-unit demand", continuous_update=False),
        )
        display(controls)
    except (ImportError, RuntimeError) as error:
        print("Widget controls unavailable. Use cutting_explorer(...).", type(error).__name__)
    ''')
    md(r'''
    ### Optional Task 4 — build a plot and extend the control

    1. In a loop, call `solve_cutting(demand=(3, 3, d), integer=False)` and `solve_cutting(demand=(3, 3, d))` for `d` from 0 to 10. Plot both bar-count curves on one set of axes with labeled units and a legend. Explain one interval where integer bar count stays fixed while the LP bound changes.
    2. Add a `long_piece_demand` parameter to `cutting_explorer`; pass it into the first component of `demand`. Add an `IntSlider` with the **same name** to `widgets.interactive`. Keep a normal function-call fallback.
    3. Change the callback to display extra pieces beside the plot. Which representation makes a mismatch with the order easiest to see?

    Save a screenshot of your own control or plot and state one decision it helps a user make.
    ''')
    md(r'''
    ## 5. Optional extensions: move from a teaching model to a richer one

    Pick **one** extension. Write the changed equation before editing code.

    1. **Transportation:** impose a 20 kg maximum on North → Assembly. Is this a lane capacity or a store-supply limit? Add $x_{\mathrm{North,Assembly}}\leq20$, resolve, and compare cost.
    2. **Network:** create an additional source or intermediate node. Supply and demand must still balance; enforce conservation at the new node. Supply a plotting position for it when extending the diagram helper.
    3. **Cutting:** keep the demand **≥** rules and minimize trim *among minimum-bar plans*. First solve for minimum bars $B^*$, then add $\sum_p y_p=B^*$ and minimize $\sum_p \mathrm{trim}_p y_p$. Compare trim **and material in extra pieces**: reducing trim can merely produce more unneeded pieces. Explain why switching to exact demand with a fixed number of identical bars makes total trim constant, leaving this secondary objective nothing to improve.
    4. **Cutting with kerf:** propose a consistent saw-cut convention, for example each produced piece consumes its length plus one kerf unit. Change the pattern-fit rule and both material checks. Explain how your convention treats the final end of a bar.

    Keep the status guard. A changed model can become infeasible; never interpret returned solver values from an infeasible model as an executable plan.
    ''')
    md(r'''
    ## 6. Submit your operations recommendation

    Use this compact experiment record for **at least one experiment in each problem**:

    | Problem | Prediction | One changed input | Status and numerical result | Explanation | Recommended action |
    |---|---|---|---|---|---|
    | Transportation | ... | ... | ... | ... | ... |
    | Network flow | ... | ... | ... | ... | ... |
    | Cutting stock | ... | ... | ... | ... | ... |

    Include one annotated delivery diagram, one bottleneck diagram, and one cutting layout. Then answer:

    - Where did an inequality represent availability, and where did equality represent conservation or an exact order?
    - Why was an infeasible scenario useful to the planner?
    - Which quantities were continuous material flows, and which had to be integer decisions?
    - What did the LP relaxation tell you, and what did it **not** prove about a usable cutting plan?
    - Which assumption would you verify before giving these plans to a real robot-cell operator?

    Your recommendation should cite quantities and units, explain a tradeoff, and distinguish your prediction from the observed optimized result.
    ''')
    notebook = nbf.v4.new_notebook(cells=cells)
    notebook.metadata = {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
                         "language_info": {"name": "python", "version": "3.11"},
                         "colab": {"name": "lab_auto_3.ipynb", "provenance": []}}
    nbf.validate(notebook)
    return notebook


if __name__ == "__main__":
    nbf.write(build_notebook(), ROOT / "lab_auto_3.ipynb")
