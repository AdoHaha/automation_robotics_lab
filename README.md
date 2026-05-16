# Automation and Robotics - Laboratory Materials

This repository contains laboratory materials and exercises for the Automation and Robotics course, focusing on optimization techniques, programming, and machine learning applications in industrial contexts.

## Course Overview

The laboratory sessions cover a range of topics from basic linear programming to advanced optimization techniques and machine learning applications in automation:

### Lab 1: Introduction to Python and PuLP

<a target="_blank" href="https://colab.research.google.com/github/AdoHaha/automation_robotics_lab/blob/master/lab_auto_1.ipynb">
  <img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/>
</a>

- Getting familiar with Python environment
- Installing and configuring PuLP library
- Solving first simple linear programming problem

### Lab 2: Advanced Linear Programming and Sensitivity Analysis

<a target="_blank" href="https://colab.research.google.com/github/AdoHaha/automation_robotics_lab/blob/master/lab_auto_2.ipynb">
  <img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/>
</a>

- Defining more complex linear programming tasks
- Learning different constraint types
- Sensitivity analysis

### Lab 3: Integer Programming

<a target="_blank" href="https://colab.research.google.com/github/AdoHaha/automation_robotics_lab/blob/master/lab_auto_3.ipynb">
  <img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/>
</a>

- Understanding integer programming concepts
- Modeling logical constraints
- Solving scheduling problems

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

- Learning critical path method
- Implementing algorithms for time calculations
- Getting familiar with PERT method

### Lab 6: Machine learning and statistics in optimization of automation tasks

<a target="_blank" href="https://colab.research.google.com/github/AdoHaha/automation_robotics_lab/blob/master/lab_auto_6.ipynb">
  <img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/>
</a>

- Learning timeseries forecasting
- Learning categorization
- Using Machine Learning and Operations reasearch together

## Repository Structure

- **Jupyter Notebooks**: Each lab is provided as a Jupyter notebook (`lab_auto_X.ipynb`)
- **Data**: Sample datasets for exercises in the `data/` directory
- **Images**: Visual resources used in the notebooks

## Prerequisites

To work with these laboratory materials, you'll need:

1. Python 3.6 or higher
2. Jupyter Notebook or JupyterLab
3. Required Python packages:
   - PuLP (for linear programming)
   - NumPy and Pandas (for data manipulation)
   - Matplotlib (for visualization)
   - scikit-learn (for machine learning)
   - SciPy (for optimization)

You can install the required packages using pip:

```bash
pip install pulp numpy pandas matplotlib scikit-learn scipy jupyter
```

## Getting Started

1. Clone this repository
2. Install the required dependencies
3. Launch Jupyter Notebook or JupyterLab
4. Open the notebook for the current lab session

## License

This educational material is provided for academic purposes. Please respect the intellectual property rights of all referenced works.
