# Notes And Issues For Lab 6

This file collects issues found while solving `lab_auto_6.ipynb` as a student.

## Fixed In Current Working Copy

- Changed GitHub raw image/data links from the merged `ex6` branch to `master`.
- Added a small ML confusion-matrix warm-up before model training.
- Added recipe-share output and changed Task 5 to ask about shares, not only kilograms.
- Changed scheduling so selected maintenance must finish before production on the same station.
- Changed Task 7 wording to match the maintenance-before-production model.
- Tightened the PERT deadline from 760 min to 510 min so deadline risk is meaningful.
- Replaced uniform high-price scenario with a chicken supply shock that changes recipe shares.

## Remaining Issues To Revisit

### Target Months Are Hard-Coded To 2026

The notebook uses June and September 2026. This is good for the current course run but will age badly if the lab is reused later.

Possible fixes:

- Add `COURSE_YEAR = 2026` and derive all target months/orders from that.
- Default to offline fallback data for stable grading.
- Explicitly state that numeric results are course-year-specific.

### Live FRED Data Changes Expected Answers

The notebook defaults to `use_live=True`, so forecasts and recipes may vary across dates and environments.

Possible fixes:

- Use fallback data by default and make live FRED an extension task.
- Or add grading language: "Your numerical answer may differ if live data changed."

### ML Section Is Still The Hardest Section

The ML section is now better scaffolded, but students new to ML may still need help with:

- train/test split by lifecycle,
- precision vs recall,
- ROC-AUC,
- threshold tuning.

Possible fixes:

- Add a tiny hand calculation after the toy confusion matrix.
- Add a glossary cell immediately before model comparison.

### Failure Probabilities Are Very High

The sampled latest lifecycle rows produce high failure probabilities for all four machines. This makes the maintenance decision feel slightly artificial.

Possible fixes:

- Use not-only-latest rows for current condition.
- Create a small fixed `lab6_machine_status.csv` with more varied machine states.
- Calibrate or cap `p_failure` for teaching realism.

### Scenario Analysis Re-Solve Check

After introducing ingredient-specific price shocks and maintenance-before-production scheduling, the notebook was re-run. Current verification:

- Recipe shares change under chicken supply shock: max share change about 0.287.
- Maintenance affects makespan: 225 min without preventive maintenance vs 270 min with selected maintenance.
- PERT probability is no longer trivially 100%: about 77.3% for a 545 min deadline.
- Scenario table now shows maintained machines and max recipe-share change.

## Useful Acceptance Criteria

The lab is in a better shape when:

- base notebook executes end to end in Colab,
- raw image and data links work from `master`,
- selected maintenance changes the schedule or lateness,
- at least one scenario changes recipe shares or maintenance decisions,
- PERT deadline probability is between roughly 60% and 95%,
- students can answer each TODO from visible notebook tables.
