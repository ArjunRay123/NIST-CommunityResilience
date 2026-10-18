# NIST Community Resilience — Installation Guide

## 1. Prerequisites

- Python 3.10 or newer
- Git
- Jupyter Notebook or VS Code with Jupyter extension

## 2. Clone Repository

```bash
git clone https://github.com/ArjunRay123/NIST-CommunityResilience.git
cd NIST-CommunityResilience
```

## 3. Install Dependencies

Create and activate a Conda environment:

```bash
conda create -n nist-resilience python=3.11 pip -y
conda activate nist-resilience
```

Install required packages:

```bash
python -m pip install -r requirements.txt
```

## 4. TraCR Dataset Setup

Download the **TraCR v1 dataset** from the official NIST website:

https://data.nist.gov/od/id/mds2-3978

1. Download `TraCR_v1_database.csv`.
2. Place the CSV in the same folder as `NIST_TraCR_EDA.ipynb`.
3. Open the notebook in Jupyter or VS Code.
4. Select the `nist-resilience` Python environment and click **Run All**.

The notebook explores missing values, dataset structure, geographic coverage, and resilience indicators.

## 5. UScityURL Dataset Setup

*To be completed *

## 6. Troubleshooting

- **ModuleNotFoundError:** Run `python -m pip install -r requirements.txt`.
- **FileNotFoundError:** Check that the CSV is in the correct folder.
- **Kernel errors:** Select the correct Python environment and restart the kernel.
