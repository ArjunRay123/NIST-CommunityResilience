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

## 5. USCityURL EDA Setup

`USCityURL_EDA.ipynb` is a limited Orlando demo. It does not require a local data file. It loads the municipal website directory from the [UScityURL](https://github.com/caimeng2/UScityURL) repository and then crawls Orlando’s public website.

Source CSV:

https://raw.githubusercontent.com/caimeng2/UScityURL/master/UScityURL.csv

The notebook uses the `MUNICIPALITY`, `STATE`, and `WEBSITE_URL` columns.

1. Confirm the environment from section 3 is active (`nist-resilience`).
2. Open `USCityURL_EDA.ipynb` in Jupyter or VS Code.
3. Select the `nist-resilience` Python environment.
4. Click **Run All**. An internet connection is required to load UScityURL and to request pages from orlando.gov.

The notebook:

- Loads UScityURL and selects the Orlando, Florida row (`https://www.orlando.gov/`).
- Crawls up to 60 pages, staying on the official Orlando domain.
- Keeps links whose anchor text or URL match resilience-related keywords (for example resilience, flood, hurricane, hazard mitigation, and comprehensive plan).
- Extracts text from up to 15 HTML or PDF candidates with BeautifulSoup or PyMuPDF.
- Marks a document usable if it has at least 100 words, drops exact duplicates, and runs preliminary topic-mention EDA on that sample.

Demo limits are set in the first code cell (`MAX_PAGES_TO_CRAWL = 60`, `MAX_DOCUMENTS_TO_ANALYZE = 15`). Results describe only the collected sample.

## 6. Troubleshooting

- **ModuleNotFoundError:** Run `python -m pip install -r requirements.txt`.
- **FileNotFoundError:** Check that the CSV is in the correct folder.
- **Kernel errors:** Select the correct Python environment and restart the kernel.
- **Connection or timeout errors in USCityURL_EDA.ipynb:** The notebook needs internet access to load the UScityURL CSV and to request pages from orlando.gov. Check the connection and rerun the notebook.
- **No usable documents in USCityURL_EDA.ipynb:** Review the candidate-link and failure tables in the notebook. Pages with fewer than 100 extracted words are not used in the EDA. Crawl results can change if the city website updates.
