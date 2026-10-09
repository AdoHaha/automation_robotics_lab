# Introductory labs: independent student trial

Instructor review notes, 2026-10-09. This file is an answer/review record; it should not be inserted into the student notebooks.

## Method and result

I read the notebook sources and attempted the tasks independently, without using the builders as evidence. All four supplied notebooks completed in separate fresh local Jupyter kernels through `nbclient`: Lab 0, 43 cells; Lab 1, 40; Lab 2, 25; Lab 3, 37. No cell errors occurred. PuLP 3.3.2/CBC was available. I separately ran hand-derived scenario calculations, changed model inputs, built the requested plotting/slider callbacks, and checked the resulting quantities against the physical rules. Local rendered transportation, flow, and cutting diagrams were readable.

This verifies fresh **local execution**, not an actual Colab browser session. Embedded data, `%pip` setup, bundled CBC, the Colab widget-manager hook, and normal function-call fallbacks support portability. Browser widget rendering, Google-hosted package installation, and the published GitHub/Colab badge destinations were not tested in a real Colab session.

The root agent corrected issues found during this trial: Lab 1 now reaches the assembly-capacity plateau, its large capacity purchase crosses that plateau, the integer comparison is core work, Lab 2's large sensitivity test crosses an active-set change, and Lab 3's own-control task is explicitly optional. I inspected those final source changes and independently evaluated the revised numerical scenarios. The fresh-kernel run used notebook snapshots taken during review; the root agent separately ran the final integration checker.

## Lab 0: Python and checking a chosen plan

| Mini | Pro | Profit (PLN) | Assembly use/slack (min) | Testing use/slack (min) | Feasible |
|---:|---:|---:|---:|---:|:---|
| 4 | 3 | 370 | 200 / 150 | 90 / 90 | Yes |
| 6 | 2 | 380 | 200 / 150 | 110 / 70 | Yes |
| 8 | 5 | 670 | 360 / −10 | 170 / 10 | No |
| 9 | 4 | 640 | 340 / 10 | 175 / 5 | Yes |

- Checkpoint A: five Mini kits use 100 assembly minutes and contribute 200 PLN. Restore four before continuing.
- B: `time_min[("testing", "Mini")]` is 15 min/kit. Changing `plan["Pro"]` changes the chosen quantity, not the coefficient.
- C: baseline testing use is `15*4 + 10*3 = 90`. Rewriting the comprehension with an outer resource loop and inner product loop returned exactly the same dictionary.
- D: saving `evaluate_plan({"Mini": 6, "Pro": 2}, ...)` and reading `my_result["profit_pln"]` gives 380. The overloaded plan's 670 PLN cannot justify executing it.
- E: assembly capacity 370 with the unchanged baseline still gives 370 PLN; checking capacity does not choose extra production. One more Pro adds 40 assembly min, 10 testing min, and 70 PLN. Enumerating the stated whole-number ranges confirms the best baseline whole-kit plan is `(9,4)`.

I built the quantity bar chart and a `plot_two_profits(mini=4, pro=3)` callback using the demonstrated API. Connecting two matching sliders and changing Pro to four produced the expected parameters and contributions. The normal call works independently of widgets.

Expected learning: labels/units prevent misleading arithmetic, Python can check a plan chosen by the student, and plots communicate but do not choose an optimum. The baseline has substantial unused time, so this is a useful bridge to Lab 1.

## Lab 1: product mix, slack, and sensitivity

Task 1's first three candidates are feasible: `(10,0)` uses `(200,150)` min and earns 400 PLN; `(0,8)` uses `(320,80)` and earns 560; `(5,6)` uses `(340,135)` and earns 620. The final notebook also includes `(8,5)`: it uses `(360,170)` min and earns 670 PLN, but exceeds Assembly capacity by 10 min and is infeasible. Mini earns 2 PLN/assembly min versus Pro 1.75, while Pro earns 7 PLN/testing min versus Mini 2.6667. The rankings conflict.

The LP is `max 40m+70p`, with `20m+40p≤A`, `15m+10p≤T`, and nonnegativity. At baseline, solving both binding equations gives `(m,p)=(9.25,4.125)` and 658.75 PLN/day. Both slacks are zero. Resource duals are 1.625 PLN per added assembly minute and 0.5 PLN per added testing minute.

| Scenario | Mini | Pro | Profit (PLN/day) | Assembly slack | Testing slack |
|---|---:|---:|---:|---:|---:|
| LP baseline | 9.25 | 4.125 | 658.75 | 0 | 0 |
| Integer baseline | 9 | 4 | 640 | 10 | 5 |
| Assembly 500 | 5.5 | 9.75 | 902.50 | 0 | 0 |
| Assembly 800 | 0 | 18 | 1260 | 80 | 0 |
| Testing 181 | 9.35 | 4.075 | 659.25 | 0 | 0 |
| Minimum 13 Mini, Testing 180 | — | — | Infeasible | — | — |
| Minimum 13 Mini, Testing 200 | 13 | 0.5 | 555 | 70 | 0 |

With testing fixed at 180, assembly capacity stops adding value at 720 min: all 18 Pro kits fit. For capacities 240–720, the LP profit slope is 1.625; below 240 it is 2; above 720 it is zero. This explains the final sweep and the plateau at 800. Increasing testing at Assembly 800 changes the bottleneck again: Testing 200 gives 20 Pro, profit 1400, and both resource rows binding.

The revised purchase decisions are:

- A, +10 assembly minutes for 15 PLN: actual LP gain 16.25, net **+1.25 PLN/day**; accept under the LP assumptions.
- B, +500 for 750 PLN: profit at 850 is 1260, actual gain 601.25, net **−148.75 PLN/day**; reject. Blind dual extrapolation predicts 812.50 and a misleading positive net 62.50.
- Adding one testing minute raises LP profit by exactly 0.50 PLN locally.

For literal whole kits, evaluate purchase scenarios with the integer model: A gives `(8,5)`, profit 670, gain 30, net +15; B gives 18 Pro, gain 620, net −130. The conclusions agree, but the marginal values differ. Rounding the baseline LP down happens to equal the integer optimum here; this example does not itself demonstrate suboptimal floor rounding. Its integrality gap is 18.75 PLN.

At Pro profit 20, only 12 Mini are made, profit 480, Assembly slack 110; Pro's reduced cost is −6.6667 PLN/kit. At Pro profit 80, `(0,8.75)` and `(6.25,5.625)` are both feasible and earn 700 PLN; they have different testing slack. A solver returning one plan does not establish uniqueness.

I built the requested callback with Assembly, Testing, and Pro-profit arguments and matching controls. Direct calls and interactive callback outputs agreed. Adding a candidate marker requires editing inside the plot helper before `plt.show()`; this is solvable, though a beginner may need help locating the correct axes.

## Lab 2: blending, units, and recipe changes

All cheapest filler would violate protein, fat, and its 35% share cap. Cost per kg protein is lowest for filler (6.5625 PLN/kg protein), then chicken (18.2895), beef (28.2353), milk (33.8235), and eggs (41.5385). This ratio ignores fat and the recipe bounds.

The two-ingredient warm-up gives chicken `400/11 = 36.363636` kg, filler 63.636364 kg, cost **319.545455 PLN**. It is cheaper because it omits the full model's fat/share constraints; it is not a feasible full-model recipe.

The verified 100-kg baseline is:

| Ingredient | kg | Baseline share-bound observation |
|---|---:|---|
| chicken | 24.956609 | Interior |
| beef | 24.689586 | Interior |
| eggs | 0 | At lower bound |
| milk | 15.353805 | Interior |
| plant filler | 35 | At upper bound |

Cost is **464.875334 PLN**, or **4.648753 PLN/kg**. Protein 24% and fat 8% bind; moisture is 38.367223%, with 21.632777 percentage points of slack. Batch equality residual is approximately zero. Replacing 1 kg chicken with 1 kg filler gives protein 23.78%, fat 7.94%, and filler 36%; it fails three rules.

| Protein target | Chicken kg | Beef kg | Milk kg | Filler kg | Cost/batch PLN | Cost/kg PLN |
|---:|---:|---:|---:|---:|---:|---:|
| 24% | 24.956609 | 24.689586 | 15.353805 | 35 | 464.875334 | 4.648753 |
| 28% | 43.247664 | 17.079439 | 4.672897 | 35 | 506.657711 | 5.066577 |
| 32% | 60 | 15.555556 | 0 | 24.444444 | 592.000004 | 5.920000 |

Eggs are zero in these three recipes. Additional cost over baseline is 41.782377 PLN/batch for 28%, and 127.124670 for 32%. The sweep is flat at 14–17%, rises afterward, and becomes infeasible at 36%. The optimistic share-limited upper bound is 35.5%: chicken 60%, beef 35%, filler 5%. Changing only chicken's maximum share to 90% repairs 36% protein: chicken 90 kg, beef 1.111111, filler 8.888889, cost 645.50; all quality checks pass. Doubling a batch cannot repair incompatible percentage rules.

Protein dual is **10.445594 PLN per kg of required protein**. A target increase of 0.0001 adds 0.01 kg required protein and cost 0.104455 PLN. The old +0.04 test remained on the same active set and exactly matched the dual. The revised +0.08 test predicts 83.564752 PLN but actually adds 127.124670: chicken reaches its cap, milk becomes zero, filler leaves its cap, and fat becomes nonbinding.

Batch 50 costs 232.437663 PLN; batch 200 costs 929.750668, four times as much within solver precision, with equal shares. At chicken price ×0.5 the recipe is `(chicken,beef,eggs,milk,filler)=(60,0,16.818182,18.181818,5)` and costs 325.477274. At ×2 it is `(10,41.601307,0,13.398693,35)` and costs 590.531044; chicken's minimum prevents its complete removal.

I built the moisture slider through `.observe`, percentage conversion, and the helper parameter. Moisture 20% gave Infeasible; 80% gave the baseline recipe with the changed target line. There is enough API guidance to complete this exercise. A share-percentage chart is obtained by replacing the existing plot's cost column with `share_pct` and changing the label; a reference line is not a universal constraint on every ingredient.

## Lab 3: transport, flow, and cutting

**Transportation.** Baseline cost is **185 PLN**: North sends Assembly 30, Test 0, Packing 10 kg; South sends 0,35,5. North has 10 kg unused, South none; all demand residuals are zero. Closing South→Test raises cost to **360**: North sends 15,35,0; South 15,0,15. Assembly demand 55 makes total demand 105 > available 90, hence Infeasible. Closing both Assembly lanes is also Infeasible even though total stock is adequate. Packing demand 20 costs 205. For Packing demand 5,10,15,20,25, cost is 145,165,185,205,225; demands 30 and 35 are infeasible. A 20-kg North→Assembly lane bound raises cost to **240**, with shipment rows North `(20,5,15)`, South `(10,30,0)`.

**Flow.** Baseline cost is **185 PLN**. Factory→A/B are 40/40 kg; A→Assembly/Test/Packing are 30/0/10; B→Assembly/Test/Packing 0/35/5. Factory→B is saturated. Reducing its capacity to 30 gives cost **210**, Factory→A/B 50/30, and A→Test rises to 5. Capacity 20 is infeasible because the source cut has only `50+20=70 <80` kg. Restoring 30→40 saves 25 PLN, so paying 20 is justified (net 5). Raising B capacity to 50 reduces cost to 175; further increases give no savings. Separately changing B→Test capacity to 20,30,40 gives costs 235,200,185. An A→B transfer arc of capacity 20 improves baseline cost to 175 if free; at 1 PLN/kg it produces no strict saving, and at 3 it is unused. The student must supply the proposed arc's cost and capacity; the task deliberately permits multiple answers.

**Cutting.** Pattern order is counts of `(6,4,3)`-unit pieces. Stock 10 has 10 nonempty fitting patterns. LP uses three `(1,1,0)` bars and `4/3` of `(0,0,3)`, giving **13/3 bars**. An integer optimum uses three `(1,1,0)`, one `(0,0,3)`, and one `(0,0,1)`: **5 bars**, exact order `(3,3,4)`, trim 8, no extra pieces. `5*10 = 42 ordered + 0 extra +8 trim`. This returned plan is one optimum; other minimum-bar plans can differ in extras/trim.

| Stock length | LP bound | Whole bars | Trim in returned plan | Extra-piece material |
|---:|---:|---:|---:|---:|
| 9 | 29/6 | 5 | 3 | 0 |
| 10 | 13/3 | 5 | 8 | 0 |
| 11 | 13/3 | 5 | 13 | 0 |
| 12 | 3.5 | 4 | 6 | 0 |

At stock 11 the new pattern is `(0,2,1)`, but it does not reduce minimum bars for this order. Buying five 11-unit bars at a 10% premium costs 5.5 baseline-price units versus 5 for stock 10: choose stock 10. Stock 5 is infeasible because the 6-unit piece cannot fit. Increasing stock length never removes old feasible patterns, so minimum bar count cannot increase.

For short-piece demand `d=0..10`, LP bounds are `3+d/3`; integer counts are `3,4,4,4,5,5,5,6,6,6,7`. Thus d=4→6 leaves whole bars at five while the LP rises from 4⅓ to 5. I constructed both curves on labeled axes, added the `long_piece_demand` callback/slider with matching names, and checked changing it updates the first demand component. The extra-piece table beside the physical layout directly exposes mismatches with the order.

Exact-demand baseline still uses five bars and has trim 8. With five identical bars and exact order, trim is fixed by `50−42=8`, so a second trim objective cannot improve it. The revised optional extension keeps demand≥: three `(1,1,0)` and two `(0,1,2)` bars yield zero trim but produce `(3,5,4)`, with 8 units in extra pieces. This is a useful warning that lower trim can merely shift excess material into unneeded output.

## Pedagogy and remaining friction

No remaining blocking numerical or execution defect was found in the core tasks after the reported fixes. Students can complete the requested controls using taught APIs. Status-safe helpers correctly leave objectives/physical plans absent for infeasible scenarios, and the tasks distinguish those outcomes from programming errors.

Estimated workload below is a novice reading/coding estimate, not a timed human study:

| Lab | Realistic guided novice time | Main source of load |
|---|---|---|
| 0 | 90–140 min | First exposure to lists, tuple keys, comprehensions, functions, pandas, plots, and callbacks in one session |
| 1 | 120–160 min | Translating LP plus geometry, custom controls, local duals, integer recommendation, and written experiments |
| 2 | 110–150 min | Units, full helper tables, active-set changes, infeasibility diagnosis, price/batch sweeps |
| 3 | 120–150 min core; +30–60 optional | Three model families, network conservation, pattern enumeration, integer physical checks |

The first draft's advertised windows were optimistic, particularly Lab 0's original 60–90 minutes with no programming prerequisite. Following this review, the final notebooks use longer guided windows (Lab 0: 90–120, Lab 1: 120–150, Lab 2: 110–150, Lab 3 core: 120–150 minutes), explicit shorter-session routes, and follow-up work. First-time programmers can split Lab 0 into two sessions. Do not expect a novice to understand every plotting/helper implementation: the notebooks mark that code as scaffolding, which helps.

Useful instructor prompts: explain Python zero-based indexing versus pandas label lookup; distinguish `DataFrame` column access from dictionary access; slow down at two-label keys and nested comprehensions; show where to add a new code/Markdown cell; and demonstrate one fresh-runtime rerun after an edit. `ax.text` and adding a candidate marker are less explicitly scaffolded than the bar/line examples but remain reasonable guided exercises. Rounding recipes or LP quantities should be checked rather than presented as a method.

The resulting sequence teaches a coherent progression: describe/check a plan → optimize allocation → formulate weighted recipe rules → allocate on networks → enforce whole-stock decisions. It is mathematically connected to robotics through production and material-handling decisions; it does not teach robot dynamics or hardware control, which is appropriate for these optimization labs.
