# Production-control lectures and interactive companions

Five revised lectures for Automation and Robotics, with short Jupyter
demonstrations that complement the [laboratories](../README.md).

| Lecture | Slides | Interactive companion |
| --- | --- | --- |
| 1. Linear programming: product mix and capacity value | [PDF](lecture_1.pdf) | [Notebook](notebooks/lecture_1_linear_programming.ipynb) · [Colab](https://colab.research.google.com/github/AdoHaha/automation_robotics_lab/blob/master/lectures/notebooks/lecture_1_linear_programming.ipynb) |
| 2. Integer decisions, job-shop scheduling and dynamic programming | [PDF](lecture_2.pdf) | [Notebook](notebooks/lecture_2_discrete_optimization.ipynb) · [Colab](https://colab.research.google.com/github/AdoHaha/automation_robotics_lab/blob/master/lectures/notebooks/lecture_2_discrete_optimization.ipynb) |
| 3. Prediction, inventory uncertainty and operational cost | [PDF](lecture_3.pdf) | [Notebook](notebooks/lecture_3_predict_then_optimize.ipynb) · [Colab](https://colab.research.google.com/github/AdoHaha/automation_robotics_lab/blob/master/lectures/notebooks/lecture_3_predict_then_optimize.ipynb) |
| 4. Factory quality, maintenance and sensor feedback | [PDF](lecture_4.pdf) | [Notebook](notebooks/lecture_4_quality_and_maintenance.ipynb) · [Colab](https://colab.research.google.com/github/AdoHaha/automation_robotics_lab/blob/master/lectures/notebooks/lecture_4_quality_and_maintenance.ipynb) |
| 5. Project networks: CPM, PERT and deadline risk | [PDF](lecture_5.pdf) | [Notebook](notebooks/lecture_5_cpm_pert.ipynb) · [Colab](https://colab.research.google.com/github/AdoHaha/automation_robotics_lab/blob/master/lectures/notebooks/lecture_5_cpm_pert.ipynb) |

## Run locally

From the repository root, using Python 3.10 or later:

```bash
python -m pip install -r lectures/requirements.txt
python -m jupyterlab lectures/notebooks/
```

Open a notebook and choose **Restart Kernel and Run All Cells**. Each companion
has embedded or seeded synthetic data, worked outputs, numerical checks,
prediction questions and interactive controls. No dataset downloads, credentials
or separately installed solver are required. If widgets do not display, change
the arguments of the direct function calls beside them and rerun the cells.

For Colab, use a link above, save your own copy and run the cells in order.
If packages are missing, install them in a setup cell:

```python
%pip install numpy scipy matplotlib pandas ipywidgets
```

## Teaching connections

Companions are approximately 15–20-minute instructor demonstrations, with
optional extensions. Ask students to predict, run, change one assumption, then
explain the result. The laboratory notebooks provide the longer implementation
exercises.

- Lecture 1 supports Labs 1–3: product mix, blending and transportation.
- Lecture 2 supports Lab 3's integer decisions and Lab 4's scheduling.
- Lectures 3–4 prepare the prediction, validation and maintenance ideas in Lab 6.
- Lecture 5 supports Lab 5 and the project-planning layer of Lab 6.

One useful teaching order is **1, 2, 5, 3, 4**. The filenames retain their
original numbering. These materials cover the production-control and
optimization strand; separate teaching is needed for the syllabus's broader
robot kinematics, trajectory planning and control-theory topics.
