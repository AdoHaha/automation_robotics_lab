# Instructor notes: Lab 5 rewrite

## Why rewrite instead of patching

The current Lab 5 has useful ingredients, but it is not yet a coherent two-hour exercise. It begins with a larger product-launch task network, later switches to two unrelated four-task mini-projects, and treats PERT as a bonus rather than as part of the same project-management decision. The existing notebook also relies on the external `criticalpath` package and contains saved execution output with a `Node` name error, so students may encounter a reproducibility problem before reaching the modelling ideas.

The rewritten notebook keeps the topic focus on CPM, PERT, and Gantt charts, but makes the lab closer to the improved Lab 4 style: concrete robotics story, learning goals, warm-up, reusable functions, plotted interpretation, decision exercises, and a final report.

## Intended two-hour flow

| Time | Section | Main activity |
|---:|---|---|
| 0-10 min | Warm-up | Compute a four-task CPM example by hand. |
| 10-35 min | Baseline project | Build and validate a project network; compute ES, EF, LS, LF, slack, and critical path. |
| 35-50 min | Visual interpretation | Read the network plot and Gantt chart; connect slack to managerial attention. |
| 50-70 min | Supplier decision | Compare standard vs express suppliers and explain why only critical-path changes help. |
| 70-90 min | Crashing | Enumerate acceleration choices and find the cheapest plan that meets a deadline. |
| 90-110 min | PERT and risk | Compute expected durations, variance, approximate deadline probability, and evaluate risk reduction. |
| 110-120 min | Report/challenge | Write a short recommendation and optionally run Monte Carlo simulation. |

## Baseline answer checks

For the deterministic baseline data in the rewritten notebook:

- Project duration: **33 days**.
- Critical path: **A → D → H → I → J → K → M → N**.
- The express LiDAR supplier reduces the project to **31 days** and costs **2400 PLN**.
- The express battery supplier alone saves **0 days**, because battery procurement is not on the critical path in the baseline.
- Using both express suppliers still gives **31 days**, not less, because another branch becomes binding.

## Crashing answer checks

For the target deadline of day 30, the cheapest enumerated plan is:

- Use express LiDAR procurement.
- Crash task **F** by **1 day**.
- New project duration: **30 days**.
- Extra cost: **3300 PLN**.

This is deliberately designed to show that after one critical activity is shortened, a different activity can become critical or near-critical.

## PERT answer checks

Using PERT expected durations:

- Baseline expected project duration: about **35.67 days**.
- Approximate standard deviation along the expected critical path: about **2.52 days**.
- Approximate probability of finishing by day 36: about **55%**.

With the added sensor-interface review:

- Deterministic duration remains **33 days**.
- Expected duration drops to about **35.17 days**.
- Approximate probability of finishing by day 36 rises to about **64%**.

The point is that risk mitigation may be valuable even when it does not shorten the deterministic CPM duration.

## Suggested grading focus

A strong student submission should not only compute the critical path. It should explain:

1. why accelerating a non-critical task may have no effect,
2. why the critical path can change after a decision,
3. how Gantt charts and slack tables support the decision,
4. why PERT probabilities are approximations rather than guarantees,
5. whether the recommended plan is based on time, cost, risk, or a trade-off among them.

## Implementation notes

The rewritten notebook avoids the `criticalpath` package. CPM is implemented directly with `networkx` topological order, which makes the forward pass and backward pass transparent. The notebook is saved without outputs so it should open cleanly in Jupyter or Colab.

The root `lab_auto_5.ipynb` is now a student-facing version. It intentionally does not preprint the critical path, does not show the sorted cheapest crashing plan, and uses editable TODO cells for supplier scenarios and the selected acceleration plan. The numerical checks above are for instructors or validation.
