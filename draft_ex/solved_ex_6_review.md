# Solved Ex 6 Review

Run context:

- Branch reviewed: `master`; the top-level snapshot below reflects the current working copy after the first issue-fix pass.
- Notebook: `lab_auto_6.ipynb`.
- Check script: `scripts/check_lab_auto_6.py` passed.
- Full code-cell execution passed in `/tmp/automation_robotics_lab_venv`.
- The run used live FRED data for public ingredient prices where available and fallback data for `plant_filler`.

## Current Output Snapshot After Fix Pass

Key outputs after applying the first exercise changes:

- Selected maintenance: machines **1** and **2**.
- Makespan without preventive maintenance: **225 min**.
- Makespan with selected maintenance before production: **270 min**.
- Project expected duration: **525.9 min**.
- PERT deadline: **545 min**.
- Estimated deadline probability: **77.3%**.
- Scenario table now includes `maintained_machines` and `max_recipe_share_change`.
- Chicken supply shock changes recipe shares with max share change about **0.287**.

Current scenario results:

| Scenario | Ingredient cost | Maintenance cost | Expected failure loss | Makespan | Maintained machines | Max recipe share change | Total expected cost |
|---|---:|---:|---:|---:|---|---:|---:|
| base | 15,706.18 | 1,150 | 10,916.56 | 270 | 1,2 | 0.000 | 27,772.74 |
| chicken supply shock | 24,361.13 | 1,150 | 10,916.56 | 270 | 1,2 | 0.287 | 36,427.69 |
| high failure risk | 15,706.18 | 1,150 | 11,450.00 | 270 | 1,2 | 0.000 | 28,306.18 |
| tight maintenance capacity | 15,706.18 | 700 | 13,277.21 | 225 | 2 | 0.000 | 29,683.40 |
| no preventive maintenance | 15,706.18 | 0 | 18,232.80 | 225 | none | 0.000 | 33,938.99 |

The detailed sections below preserve the initial point-by-point solve diagnosis. Use `draft_ex/notes_issues_e6.md` as the current issue-tracking file for what was fixed and what still remains.

## Overall Verdict

The integrated capstone works technically and produces coherent outputs. It is much stronger than the previous disconnected Lab 6.

Main concerns:

- Some tasks are interpretive enough to be educational, but a few have almost no real decision tension.
- Maintenance is selected, but it does **not** increase makespan in the solved instance, which conflicts with the wording of Task 7.
- Scenario analysis changes costs, but almost never changes operational decisions; this makes the "robustness" discussion weaker than intended.
- The notebook uses raw GitHub links to the `ex6` branch even though the work is now merged to `master`.
- Hard-coded 2026 target months will become stale after the course year.

## Point-By-Point Solutions And Review

### Task 1 - Read The System

Expected solution:

- Likely bottleneck by base route time:
  - Mixer: 65 min total base work.
  - Packaging robot: 58 min.
  - Thermal processor: 50 min.
  - Vision inspection: 27 min.
- So the natural first answer is **Mixer**, with **Packaging robot** also plausible after demand scaling.
- Stricter product: **Protein Plus**, because it has higher protein and fat requirements.
- Expensive but valuable maintenance option: **Thermal processor**, because it has high service cost but also the highest failure cost and risk reduction.

Assessment:

- Expected? Yes.
- Issues? Minor: "bottleneck" can be answered from base route totals, but the true bottleneck after scaled jobs and maintenance may differ.
- Difficulty: Easy and useful as orientation.

Recommended change:

- Ask students to compute both "base route load" and "scheduled station load" later, so they see bottleneck intuition can change after optimization.

### Task 2 - Document Units

Expected solution:

| Ingredient | FRED series | Original unit | Conversion used |
|---|---:|---|---:|
| beef | `APU0000703112` | USD/lb | multiply by 2.20462 |
| chicken | `APU0000FF1101` | USD/lb | multiply by 2.20462 |
| eggs | `APU0000708111` | USD/dozen | divide by approx. 0.68 kg/dozen |
| milk | `APU0000709112` | USD/gallon | divide by approx. 3.90 kg/gallon |
| plant_filler | fallback | already cost/kg | multiply by 1 |

Assessment:

- Expected? Yes.
- Issues? The egg and milk conversions are teaching approximations. Students may challenge them, which is good, but the notebook should say these are approximate equivalent kg conversions, not exact nutrition/product conversions.
- Difficulty: Easy-medium. Good first data-cleaning task.

Recommended change:

- Add a small partially filled `unit_conversions` table task cell where students must fill a `justification` column.

### Task 3 - Forecasting Interpretation

Observed validation scores:

| Ingredient | Best model | Best MAE | Notes |
|---|---|---:|---|
| chicken | exp_smoothing | 0.063 | clearly beats baselines |
| beef | exp_smoothing | 1.367 | volatile/high-error relative to others |
| eggs | drift | 1.171 | seasonal naive and smoothing perform poorly |
| milk | exp_smoothing | 0.020 | easy/low-error series |
| plant_filler | exp_smoothing | 0.034 | synthetic fallback, easy |

Forecast output for target months:

| Ingredient | 2026-06 forecast | 2026-09 forecast | Selected model |
|---|---:|---:|---|
| chicken | 9.239 | 9.226 | exp_smoothing |
| beef | 15.438 | 15.668 | exp_smoothing |
| eggs | 3.578 | 3.593 | drift |
| milk | 1.068 | 1.079 | exp_smoothing |
| plant_filler | 1.492 | 1.403 | exp_smoothing |

Expected answers:

- Hardest ingredients: **beef** by absolute MAE, **eggs** by MAPE/instability.
- Exponential smoothing does **not** beat the baseline for every ingredient; eggs choose drift.
- If a simple baseline wins, use it because validation performance matters more than model sophistication.

Assessment:

- Expected? Yes.
- Issues? Live FRED data can change the exact answer. Offline fallback gives materially different egg/milk/beef values.
- Difficulty: Medium. Good challenge if students understand train/test validation.

Recommended changes:

- Freeze expected answers around fallback mode for grading, or explicitly say live-data answers may differ.
- Add one short cell that compares `use_live=True` vs `use_live=False` for one ingredient.

### Task 4 - ML Interpretation

Observed class balance:

- `near_failure = 1`: about 8.0%.
- `near_failure = 0`: about 92.0%.

Observed model comparison:

| Model | Accuracy | Precision | Recall | F1 | ROC-AUC |
|---|---:|---:|---:|---:|---:|
| random_forest | 0.966 | 0.754 | 0.867 | 0.807 | 0.987 |
| logistic_regression | 0.789 | 0.241 | 0.749 | 0.364 | 0.860 |

Cost-sensitive threshold:

- Best threshold in grid: **0.20**.
- Expected classification cost at threshold 0.20: **337,600**.
- Cost at threshold 0.50: **376,200**.

Expected answers:

- Accuracy is misleading because always predicting "not near failure" would already be high-ish due to class imbalance.
- Recall is likely more important than precision when missed failures are much more expensive than unnecessary service.
- If failure cost doubles, students should lower the threshold, or at least rerun `choose_threshold_by_cost` with higher false-negative cost.

Assessment:

- Expected? Yes, and pedagogically strong.
- Issues? This is probably the hardest conceptual section for students. The current guidance is better after the added comments, but students may still need a small hand-worked confusion matrix example before the code.
- Difficulty: Medium-hard but appropriate for a capstone if instructor support is available.

Recommended changes:

- Add a small 2x2 confusion matrix warm-up with made-up numbers before training models.
- In the threshold task, provide the exact code line students should modify:
  `choose_threshold_by_cost(y_test, best_p_hat, false_negative_cost=10000, false_positive_cost=600)`.

### Task 5 - Blending Interpretation

Observed recipe costs:

| Product | Month | Cost |
|---|---|---:|
| Budget Blend | 2026-06 | 3,476.96 |
| Budget Blend | 2026-09 | 3,915.06 |
| Protein Plus | 2026-06 | 3,709.02 |
| Protein Plus | 2026-09 | 4,605.14 |

Observed recipes:

| Product | Ingredient | 2026-06 kg | 2026-09 kg |
|---|---|---:|---:|
| Budget Blend | beef | 41.85 | 47.25 |
| Budget Blend | chicken | 212.35 | 239.75 |
| Budget Blend | eggs | 155.00 | 175.00 |
| Budget Blend | milk | 0.00 | 0.00 |
| Budget Blend | plant_filler | 210.80 | 238.00 |
| Protein Plus | beef | 73.61 | 91.14 |
| Protein Plus | chicken | 252.00 | 312.00 |
| Protein Plus | eggs | 49.68 | 61.51 |
| Protein Plus | milk | 0.00 | 0.00 |
| Protein Plus | plant_filler | 44.71 | 55.35 |

Expected answers:

- September quantities are mostly scaled-up versions of June because September demand is higher.
- Milk is never used despite low cost because its protein/fat are too low and moisture is high.
- Chicken hits its max-share in Protein Plus, so nutrition constraints drive the recipe strongly.

Assessment:

- Expected? Yes.
- Issues? The "compare June and September" task is less interesting than intended because recipes mostly scale with demand; price changes do not change the ingredient pattern.
- Difficulty: Medium for solving, easy for interpretation once the table exists.

Recommended changes:

- Add a required `share = kg / demand_kg` comparison, not just kg. This reveals that the recipe proportions are almost unchanged.
- Make at least one price scenario alter recipe composition, e.g. spike chicken or eggs separately, not all prices together.

### Task 6 - Maintenance Interpretation

Observed maintenance plan:

| Machine | Station | p_failure | Expected avoided loss | Service cost | Time | Maintain |
|---:|---|---:|---:|---:|---:|---:|
| 1 | Mixer | 0.843 | 2,360.66 | 450 | 45 | 1 |
| 2 | Thermal processor | 0.944 | 4,955.59 | 700 | 60 | 1 |
| 3 | Packaging robot | 0.968 | 3,725.92 | 600 | 50 | 0 |
| 4 | Vision inspection | 0.977 | 1,904.65 | 350 | 35 | 0 |

Selected maintenance:

- Machines 1 and 2.
- Total service time: 105 min of 120.
- Total cost: 1,150 of 1,200.

Simple rule:

- Maintains all four machines because all have positive net value.
- Not feasible: 190 min and 2,100 cost.

Assessment:

- Expected? Yes.
- Issues? Very high failure probabilities for all machines make the decision look artificial. The optimization is still useful because constraints force a trade-off.
- Difficulty: Medium and good.

Recommended change:

- Show a sorted `net_value per service minute` column so students can reason about why machine 3 is skipped despite high net value.

### Task 7 - Scheduling Interpretation

Observed results:

| Case | Makespan |
|---|---:|
| no preventive maintenance | 225 |
| selected preventive maintenance | 225 |

Late jobs:

- No late production jobs.

Expected answer from current notebook:

- Maintenance does **not** increase makespan in this solved instance.
- It still reduces expected disruption cost enough to be justified in the cost model.

Assessment:

- Expected? The numeric output is valid, but it contradicts the task wording: "Preventive maintenance usually increases planned makespan."
- Issue severity: High for pedagogy. Students may think they made a mistake.
- Difficulty: The scheduling model is hard, but the interpretation is unexpectedly trivial because makespan does not change.

Recommended changes:

- Either change wording to: "Preventive maintenance may increase planned makespan. Did it in your result?"
- Or make selected maintenance actually affect makespan by forcing maintenance before production with a release-time/pre-production constraint, or by tightening due dates/capacity.
- Add station-load summary before and after maintenance.

### Task 8 - CPM/PERT Interpretation

Observed critical path:

1. A - Collect price data
2. B - Validate forecasts
3. E - Order ingredients
4. H - Produce batches
5. I - Quality check
6. J - Ship order

Observed project duration:

- Expected duration: **479.8 min**.
- Deadline: **760 min**.
- Deadline probability: **100.0%** under the normal approximation.

Largest non-critical slack:

- G - Configure recipes: about **61.7 min**.
- C, D, F have about **3.3 min** slack each.

Crash candidate:

- If late, crash a critical task, not G.
- Best candidates from the given data: **Order ingredients**, **Produce batches**, or **Quality check**.

Assessment:

- Expected? Critical path calculation is coherent.
- Issues? The deadline is far too loose, giving 100% probability and removing risk tension.
- Difficulty: CPM computation is medium-hard; interpretation is too easy because deadline risk is nonexistent.

Recommended changes:

- Set deadline closer to project duration, e.g. 500-520 min, so PERT risk is meaningful.
- Add a small crash-options table with cost/minute, otherwise "which task to crash" is under-specified.

### Task 9 - Scenario Interpretation

Observed scenario results:

| Scenario | Ingredient cost | Maintenance cost | Expected failure loss | Makespan | Late jobs | Total expected cost |
|---|---:|---:|---:|---:|---:|---:|
| base | 15,706.18 | 1,150 | 10,916.56 | 225 | 0 | 27,772.74 |
| high ingredient prices | 18,062.11 | 1,150 | 10,916.56 | 225 | 0 | 30,128.67 |
| high failure risk | 15,706.18 | 1,150 | 11,450.00 | 225 | 0 | 28,306.18 |
| tight maintenance capacity | 15,706.18 | 700 | 13,277.21 | 225 | 0 | 29,683.40 |
| no preventive maintenance | 15,706.18 | 0 | 18,232.80 | 225 | 0 | 33,938.99 |

Expected answer:

- Biggest total-cost change is **no preventive maintenance**.
- High ingredient prices also matter, but they do not change the recipe structure because all prices are multiplied uniformly.
- Tight maintenance capacity changes selected maintenance cost/loss but not schedule makespan.

Assessment:

- Expected? Yes.
- Issues? Scenarios mostly change costs, not decisions. Uniform ingredient multiplier cannot change recipe composition.
- Difficulty: Easy after pipeline exists; could be more challenging.

Recommended changes:

- Replace uniform high-price scenario with ingredient-specific shocks:
  - chicken +40%,
  - eggs +60%,
  - beef +25%.
- Add a "packaging robot unavailable" or "maintenance must happen before production" scenario to affect the schedule.
- Add a tight deadline scenario where late jobs become possible.

### Final Recommendation Memo

Reasonable final memo:

> Use the optimized recipe plan for both June and September. Protein Plus uses chicken at its upper share with beef and eggs to satisfy the higher protein/fat requirements; Budget Blend uses more filler and eggs while avoiding milk. Maintain the Mixer and Thermal processor before production. This uses 105 of 120 technician minutes and 1,150 of the 1,200 maintenance budget. Expected ingredient cost is about 15,706, maintenance cost is 1,150, and expected residual failure loss is about 10,917, for a total expected cost of about 27,773. The planned robot-cell makespan is 225 minutes with no late production jobs. The project critical path is A-B-E-H-I-J. The largest operational risk is machine failure if preventive maintenance is skipped; no-maintenance raises total expected cost to about 33,939. The plan is cost-robust but not decision-sensitive under current scenarios, because recipe and schedule decisions barely change across scenarios.

Assessment:

- Expected? Yes.
- Issues? The final recommendation is too stable. This is good for solvability but weak for capstone trade-off discussion.
- Difficulty: Medium if students must synthesize all sections.

## Cross-Cutting Issues

### 1. Colab Image Link Still Points To `ex6`

Current image link:

```text
https://raw.githubusercontent.com/AdoHaha/automation_robotics_lab/ex6/lab_auto_6_illustration.png
```

Since the work is now merged, this should point to `master` or to a stable commit SHA. If the `ex6` branch is deleted, the image will break.

Recommended fix:

```text
https://raw.githubusercontent.com/AdoHaha/automation_robotics_lab/master/lab_auto_6_illustration.png
```

### 2. Data Bootstrap Also Tries `ex6` First

The data downloader tries `ex6` then `master`. It works now, but after merge the first attempt is unnecessary and may produce visible failure/noise if the branch is deleted.

Recommended fix:

- Use `master` first.
- Optionally keep `ex6` second only while the PR branch exists.

### 3. Hard-Coded 2026 Target Months Will Age Badly

The notebook hard-codes:

```python
TARGET_MONTHS = [pd.Timestamp("2026-06-01"), pd.Timestamp("2026-09-01")]
```

This is fine for June 2026, but if the lab is reused in 2027, the target months are in the past. Live FRED history may also eventually extend beyond those dates, making the forecast horizon zero or negative.

Recommended fix:

- Use course-specific target names in the story, or
- compute target months relative to a configurable `COURSE_YEAR`, or
- force `use_live=False` for stable teaching results.

### 4. Live Data And Fallback Data Give Different Solutions

Offline fallback forecasts differ materially from live FRED forecasts. Example offline forecasts:

- eggs around 7.5 instead of live around 3.6,
- beef around 13.1 instead of live around 15.5,
- milk around 1.4 instead of live around 1.1.

This is acceptable for exploration, but it complicates grading.

Recommended fix:

- For classroom consistency, default to fallback mode and make live FRED an extension.
- Or state explicitly that numeric answers may differ.

### 5. Maintenance Does Not Affect Makespan

This is the most important modeling mismatch. The lab wants maintenance to connect ML to scheduling, but in the solved instance maintenance does not change makespan.

Recommended fixes:

- Make maintenance happen at time zero before production can start on that station.
- Add release times/due dates tight enough that maintenance affects lateness.
- Or change Task 7 wording so "no makespan change" is an acceptable discovery.

### 6. Deadline Risk Is Too Easy

Deadline probability is 100.0%, so PERT risk is not meaningful.

Recommended fix:

- Use a deadline around 500-520 min.
- Ask students to evaluate at least two deadlines.

### 7. Scenario Analysis Does Not Change Decisions Enough

The scenarios mostly change total cost. They rarely change recipes, maintenance, makespan, or lateness.

Recommended fixes:

- Use ingredient-specific shocks instead of uniform price multipliers.
- Use a station outage or reduced technician-time scenario.
- Include a tighter deadline.

## Difficulty Summary

| Section | Difficulty | Current quality |
|---|---|---|
| System reading | Easy | Good warm-up |
| Unit conversion | Easy-medium | Good, needs grading note |
| Forecasting | Medium | Good |
| ML risk model | Medium-hard | Good, needs warm-up |
| Blending LP | Medium | Good but composition changes are weak |
| Maintenance optimization | Medium | Good |
| Job-shop scheduling | Hard | Technically good, interpretation mismatch |
| CPM/PERT | Medium | Good mechanics, weak risk |
| Scenario analysis | Easy-medium | Needs stronger decision changes |
| Final memo | Medium | Good synthesis |

## Highest-Priority Exercise Changes

1. Change raw GitHub links from `ex6` to `master`.
2. Change Task 7 wording or force maintenance to affect schedule/lateness.
3. Make scenario analysis ingredient-specific so recipes can change.
4. Tighten PERT deadline so deadline probability is not 100%.
5. Add a small confusion-matrix warm-up before ML evaluation.
6. Add recipe-share comparison, not only kg comparison.
