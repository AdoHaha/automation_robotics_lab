"""Execute Labs 0–3 in fresh kernels and check their mathematical teaching claims.

Run from any directory. Install nbclient and ipykernel for this developer check.
Notebook code itself installs its runtime dependencies, as it does in Colab.
No repository data or builder functions are available to the execution kernels.
"""

from __future__ import annotations

import argparse
import base64
import tempfile
from pathlib import Path

import nbformat
from nbclient import NotebookClient


ROOT = Path(__file__).resolve().parents[1]

CHECKS = {
    0: r'''
import math
assert baseline["feasible"] and baseline["profit_pln"] == 370
assert baseline["used_min"] == {"assembly": 200, "testing": 90}
assert baseline["slack_min"] == {"assembly": 150, "testing": 90}
invalid = evaluate_plan({"Mini": 8, "Pro": 5}, profit_pln, time_min, capacity_min)
assert not invalid["feasible"]
assert not evaluate_plan({"Mini": -1, "Pro": 0}, profit_pln, time_min, capacity_min)["feasible"]
# Direct parameter path works without front-end widget rendering.
assert show_plan(4, 3, 350, 180)["feasible"]
plot_mini_profit(5)
if "controls" in globals():
    controls["pro"].value = 5
    update_plan(4, 5, 350, 180)
print("Lab 0: Python totals, feasibility, plots, and callback checks passed.")
''',
    1: r'''
import math
base = solve_product_mix()
# Independent algebra: intersect 20m+40p=350 and 15m+10p=180.
assert base["status"] == "Optimal"
assert math.isclose(base["quantities"]["Mini"], 9.25, abs_tol=1e-6)
assert math.isclose(base["quantities"]["Pro"], 4.125, abs_tol=1e-6)
assert math.isclose(base["profit"], 658.75, abs_tol=1e-5)
assert base["resources"]["binding"].all()
whole = solve_product_mix(integer=True)
# Exhaustively search this small whole-kit instance, without PuLP.
feasible = [(40*m+70*p, m, p) for m in range(18) for p in range(9)
            if 20*m+40*p <= 350 and 15*m+10*p <= 180]
assert math.isclose(whole["profit"], max(feasible)[0], abs_tol=1e-6)
assert whole["profit"] <= base["profit"]
for asm in [100, 350, 500, 720, 800, 900]:
    r = solve_product_mix(assembly_min=asm)
    assert r["status"] == "Optimal"
    assert (r["resources"].slack_min >= -1e-5).all()
assert math.isclose(solve_product_mix(assembly_min=800)["profit"], 1260, abs_tol=1e-5)
assert math.isclose(solve_product_mix(assembly_min=900)["profit"], 1260, abs_tol=1e-5)
dual = base["resources"].loc["Assembly", "shadow_PLN_per_min"]
assert math.isclose(dual, 1.625, abs_tol=1e-6)
gain10 = solve_product_mix(assembly_min=360)["profit"] - base["profit"]
gain500 = solve_product_mix(assembly_min=850)["profit"] - base["profit"]
assert math.isclose(gain10, dual*10, abs_tol=1e-5)
assert gain10 - 15 > 0 and gain500 - 750 < 0
assert not math.isclose(gain500, dual*500, abs_tol=1e-4)
assert solve_product_mix(minimum={"Mini": 13})["status"] == "Infeasible"
assert solve_product_mix(minimum={"Mini": 13})["quantities"] is None
assert solve_product_mix(testing_min=200, minimum={"Mini": 13})["status"] == "Optimal"
assert not (solve_product_mix(pro_profit=20)["variables"].loc["Pro", "reduced_cost_PLN_per_kit"] >= 0)
assert math.isclose(solve_product_mix(pro_profit=80)["profit"], 700, abs_tol=1e-5)
controls["assembly_min"].value = 800
assert mix_experiment(800, 180)["status"] == "Optimal"
assert mix_experiment(350, 180, min_mini=13)["status"] == "Infeasible"
print("Lab 1: analytic optimum, brute-force integer optimum, plateau, dual, and callbacks passed.")
''',
    2: r'''
import math
base = solve_blend()
assert base["status"] == "Optimal"
assert math.isclose(base["cost_pln"], 464.87530432, abs_tol=1e-3)
assert math.isclose(base["recipe"].kg.sum(), 100, abs_tol=1e-5)
assert base["quality"].meets_target.all()
assert base["constraints"].loc["Protein_kg", "binding"]
assert base["constraints"].loc["Fat_kg", "binding"]
assert not base["constraints"].loc["Moisture_kg", "binding"]
assert math.isclose(maximum_protein_from_share_limits(ingredients), .355, abs_tol=1e-8)
failed = solve_blend(min_protein=.36)
assert failed["status"] == "Infeasible" and failed["quantities_kg"] is None
assert failed["diagnostics"]
double = solve_blend(batch_kg=200)
assert np.allclose(base["recipe"].share_pct, double["recipe"].share_pct, atol=1e-5)
assert math.isclose(double["cost_pln"], 2*base["cost_pln"], abs_tol=1e-3)
last_cost = -np.inf
for target in [.18, .24, .28, .32, .35]:
    r = solve_blend(min_protein=target)
    assert r["status"] == "Optimal" and r["quality"].meets_target.all()
    assert r["cost_pln"] >= last_cost - 1e-4
    last_cost = r["cost_pln"]
small = solve_blend(min_protein=.2401)
predicted = base["model"].constraints["Protein_kg"].pi * .01
assert math.isclose(small["cost_pln"] - base["cost_pln"], predicted, abs_tol=1e-3)
for price in [.5, 1, 2]:
    r = solve_blend(chicken_cost_multiplier=price)
    assert r["status"] == "Optimal" and r["quality"].meets_target.all()
protein_slider.value = 36
update_explorer()
protein_slider.value = 24
update_explorer()
print("Lab 2: recipe, quality, scaling, monotonicity, dual, infeasibility and callbacks passed.")
''',
    3: r'''
import math
base = solve_transport()
assert base["status"] == "Optimal" and math.isclose(base["cost"], 185)
assert np.allclose(base["shipments"].sum(axis=0), pd.Series(DEMAND), atol=1e-6)
assert (base["shipments"].sum(axis=1) <= pd.Series(SUPPLY) + 1e-6).all()
closed = solve_transport(closed_lanes=[("South", "Test")])
assert closed["status"] == "Optimal" and math.isclose(closed["cost"], 360)
assert closed["shipments"].loc["South", "Test"] == 0
bad = solve_transport(demand={**DEMAND, "Assembly": 55})
assert bad["status"] == "Infeasible" and bad["shipments"] is None
disconnected = solve_transport(closed_lanes=[("North", "Assembly"), ("South", "Assembly")])
assert disconnected["status"] == "Infeasible"
for capacity, objective in [(40, 185), (30, 210)]:
    r = flow_with_hub_b_capacity(capacity)
    assert r["status"] == "Optimal" and math.isclose(r["cost"], objective)
    for node, required in r["balance"].items():
        net = sum(f for (u,v),f in r["flows"].items() if u==node) - sum(
            f for (u,v),f in r["flows"].items() if v==node)
        assert math.isclose(net, required, abs_tol=1e-6)
    assert all(0 <= f <= r["arcs"][a][0]+1e-6 for a,f in r["flows"].items())
assert flow_with_hub_b_capacity(20)["status"] == "Infeasible"
assert 210 - 185 - 20 > 0  # restoring capacity pays back its premium
patterns = enumerate_patterns(10, (6,4,3))
assert len(patterns) == 10
# Independent cartesian enumeration ensures no fitting pattern is omitted.
expected = {(a,b,c) for a in range(2) for b in range(3) for c in range(4)
            if a+b+c > 0 and 6*a+4*b+3*c <= 10}
assert set(patterns) == expected
lp, ip = solve_cutting(integer=False), solve_cutting()
assert math.isclose(lp["bars"], 13/3, abs_tol=1e-6) and ip["bars"] == 5
# Explicit five-bar construction; a material-volume bound proves optimality.
construction = np.array([(1,1,0)]*3 + [(0,0,2)]*2)
assert np.all(construction.sum(axis=0) >= np.array(PIECE_DEMAND))
assert math.ceil(np.dot(PIECE_LENGTHS, PIECE_DEMAND)/10) == 5
for stock in [10, 11, 12, 14]:
    lower, whole = solve_cutting(stock_length=stock, integer=False), solve_cutting(stock_length=stock)
    assert lower["status"] == whole["status"] == "Optimal"
    assert lower["bars"] <= whole["bars"]+1e-6
    assert (whole["produced"] >= np.array(PIECE_DEMAND)).all()
    assert math.isclose(stock*whole["bars"], np.dot(PIECE_LENGTHS, PIECE_DEMAND) +
                        whole["trim"] + whole["extra_material"], abs_tol=1e-5)
assert solve_cutting(stock_length=5)["status"] == "Infeasible"
assert solve_cutting(demand=(0,0,0))["bars"] == 0
assert np.allclose(solve_cutting(exact_demand=True)["produced"], PIECE_DEMAND)
cutting_explorer(12, 6)
cutting_explorer(5, 4)
print("Lab 3: shipments, flows, pattern completeness, cutting bounds and callbacks passed.")
''',
}


def check(lab: int, artifacts_dir: Path | None) -> None:
    path = ROOT / f"lab_auto_{lab}.ipynb"
    notebook = nbformat.read(path, as_version=4)
    nbformat.validate(notebook)
    for cell in notebook.cells:
        if cell.cell_type == "code":
            assert cell.execution_count is None and not cell.outputs, f"Saved outputs in {path.name}"
    source = "\n".join(c.source for c in notebook.cells)
    assert "colab.research.google.com" in source
    assert "requirements.txt" not in "\n".join(c.source for c in notebook.cells if c.cell_type == "code")
    notebook.cells.append(nbformat.v4.new_code_cell(CHECKS[lab], id=f"lab{lab}-verification"))
    with tempfile.TemporaryDirectory(prefix=f"intro-lab{lab}-") as execution_dir:
        client = NotebookClient(notebook, timeout=180, kernel_name="python3",
                                resources={"metadata": {"path": execution_dir}})
        client.execute()
    # Callback exceptions can be captured in Output widgets instead of raised by the cell.
    widget_states = notebook.metadata.get("widgets", {}).get(
        "application/vnd.jupyter.widget-state+json", {}).get("state", {})
    for state in widget_states.values():
        for output in state.get("state", {}).get("outputs", []):
            assert output.get("output_type") != "error", f"Widget callback failed in Lab {lab}: {output}"
    if artifacts_dir:
        artifacts_dir.mkdir(parents=True, exist_ok=True)
        nbformat.write(notebook, artifacts_dir / f"lab_auto_{lab}.executed.ipynb")
        for index, cell in enumerate(notebook.cells):
            for output_index, output in enumerate(cell.get("outputs", [])):
                image = output.get("data", {}).get("image/png")
                if image:
                    (artifacts_dir / f"lab{lab}-cell{index:02d}-{output_index}.png").write_bytes(
                        base64.b64decode(image))
    print(f"PASS Lab {lab}: fresh execution + mathematical checks", flush=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--artifacts-dir", type=Path)
    args = parser.parse_args()
    for lab in range(4):
        check(lab, args.artifacts_dir)


if __name__ == "__main__":
    main()
