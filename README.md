# Automation and Robotics - Laboratory Materials

This repository contains laboratory materials and exercises for the Automation and Robotics course, focusing on optimization techniques, programming, and machine learning applications in industrial contexts.

**Polskie wersje laboratoriów 0–6:** [notatniki i instrukcja pracy w Google Colab](pl/README.md).

## Course Overview

The laboratory sessions cover a range of topics from basic linear programming to advanced optimization techniques and machine learning applications in automation:

### Lab 0: Python Foundations for Optimization

<a target="_blank" href="https://colab.research.google.com/github/AdoHaha/automation_robotics_lab/blob/master/lab_auto_0.ipynb">
  <img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/>
</a>

- Variables, units, dictionaries, loops, functions, and readable error messages
- Tables, CSV, NumPy, and feasibility checks for a robot-kit factory
- Building and labeling plots, then connecting a slider to a Python function

### Lab 1: Product Mix and Resource Allocation with PuLP

<a target="_blank" href="https://colab.research.google.com/github/AdoHaha/automation_robotics_lab/blob/master/lab_auto_1.ipynb">
  <img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/>
</a>

- Translating a factory story into variables, an objective, and resource constraints
- Plotting the feasible region and interpreting slack, binding constraints, and solver status
- Building controls that re-solve the model; checking local shadow prices against scenario sweeps
- Comparing continuous production plans with optimal whole-kit decisions

### Lab 2: Blending — Recipes, Quality, and Cost

<a target="_blank" href="https://colab.research.google.com/github/AdoHaha/automation_robotics_lab/blob/master/lab_auto_2.ipynb">
  <img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/>
</a>

- Modeling kilograms, shares, mass balance, and weighted quality requirements
- Comparing recipe and quality plots; interpreting slack, surplus, and equality residuals
- Exploring quality–cost tradeoffs, ingredient price shocks, and infeasible requirements
- Extending a slider callback and checking sensitivity by re-solving

### Lab 3: Transportation, Network Flow, and Cutting Stock

<a target="_blank" href="https://colab.research.google.com/github/AdoHaha/automation_robotics_lab/blob/master/lab_auto_3.ipynb">
  <img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/>
</a>

- Allocating shipments with supply limits and demand equalities
- Generalizing to capacitated flows with hubs and conservation at every node
- Enumerating cutting patterns and choosing integer numbers of stock bars
- Reading network, heatmap, and cutting-layout plots; testing changed assumptions
- Comparing LP bounds with integer decisions, coverage, overproduction, and trim waste

Labs 0–3 follow **predict → run → change → explain**. Worked starter code runs as supplied;
markdown TODO tasks ask students to build or extend code and justify decisions. Each notebook
includes an experiment log or report template. Lab 3 has core and extension tracks so its three
problem families can also be taught over two sessions.
Supplied checking and plotting helpers are scaffolding. Students should focus first
on the model, its interpretation, and building one plot/control, then complete extensions.

### Lab 4: Production Scheduling - Job-Shop Optimization

<a target="_blank" href="https://colab.research.google.com/github/AdoHaha/automation_robotics_lab/blob/master/lab_auto_4.ipynb">
  <img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/>
</a>

- Understanding job-shop scheduling in a robot-cell context
- Building a PuLP mixed-integer model with start times and no-overlap constraints
- Validating and interpreting schedules with Gantt charts

### Lab 5: Network Methods - CPM/PERT in Python

<a target="_blank" href="https://colab.research.google.com/github/AdoHaha/automation_robotics_lab/blob/master/lab_auto_5.ipynb">
  <img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/>
</a>

- Planning a robotics demo project with CPM, PERT, and Gantt charts
- Interpreting slack, critical paths, supplier choices, and crashing decisions
- Estimating deadline risk with PERT and Monte Carlo simulation

### Lab 6: Machine learning and statistics in optimization of automation tasks

<a target="_blank" href="https://colab.research.google.com/github/AdoHaha/automation_robotics_lab/blob/master/lab_auto_6.ipynb">
  <img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/>
</a>

- Learning timeseries forecasting
- Learning categorization
- Using Machine Learning and Operations reasearch together

## Repository Structure

- **Jupyter Notebooks**: Each lab is provided as a Jupyter notebook (`lab_auto_X.ipynb`)
- **Polish notebooks**: Localized versions of Labs 0–6, including explanations, comments, and interactive controls, are in `pl/`
- **Data**: Sample datasets for exercises in the `data/` directory
- **Images**: Visual resources used in the notebooks

## Prerequisites

To work with these laboratory materials, you'll need:

1. Python 3.10 or higher (or the current Google Colab Python runtime)
2. Jupyter Notebook or JupyterLab
3. Required Python packages:
   - PuLP (for linear programming)
   - NumPy and Pandas (for data manipulation)
   - Matplotlib (for visualization)
   - scikit-learn (for machine learning)
   - SciPy and statsmodels (for statistics and forecasting)
   - NetworkX (for networks) and ipywidgets (for interactive controls)

You can install the required packages using pip:

```bash
python -m pip install -r requirements.txt
python -m pip install jupyter
```

## Getting Started

For **Google Colab**, open a badge above, save a copy in Drive, and run the setup cell followed by
the remaining cells in order. Labs 0–3 embed their teaching data and draw their illustrations in
Python: no clone, Drive mount, external images, or local `requirements.txt` is needed. Setup
requires internet to install packages. If controls do not display, use the direct function calls
and editable parameter cells beside them. To try a locally revised notebook before it is on the
repository's `master` branch, upload the `.ipynb` through Colab's **File → Upload notebook**.

For **local Jupyter**, clone the repository, install the packages above, launch `jupyter notebook`,
and begin with `lab_auto_0.ipynb`. A fresh kernel and execution in cell order avoid hidden state.
PuLP is kept on version 3.x for a consistent modeling API across the course.

## License

This educational material is provided for academic purposes. Please respect the intellectual property rights of all referenced works.
