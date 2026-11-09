# NIST Community Resilience — Installation Guide

## 1. Prerequisites

- Python 3.10 or newer
- Git
- Jupyter Notebook or VS Code with Jupyter extension
- [Ollama](https://ollama.com/) for the local RAG assistant

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

Install the local embedding and language models:

```bash
ollama pull embeddinggemma
ollama pull llama3.2:3b
```

## 4. TraCR Dataset Setup

`TraCR_dataset.ipynb` explores the NIST Tracking Community Resilience (TraCR) dataset, focusing on data completeness, geographic coverage, and resilience indicators.

The dataset is already included in the repository under `datasets_TRaCr/TraCR_v1_database.csv`. **No additional download is required.**

**Original dataset source (optional):**

https://data.nist.gov/od/id/mds2-3978

1. Confirm the environment from Section 3 is active (`nist-resilience`).
2. Open `TraCR_dataset.ipynb` in Jupyter or VS Code.
3. Select the `nist-resilience` Python environment.
4. Click **Run All** to execute the analysis.

The notebook:

- Examines dataset structure and missing values.
- Explores geographic coverage, particularly Florida and Orange County.
- Evaluates data completeness and the usefulness of resilience indicators.
- Identifies limitations of the dataset for further community resilience analysis.
- Creates `datasets_TRaCr/processed/tracr_project_dataset.csv` for later analysis.

Results are based on the TraCR v1 dataset included in the repository.

## 5. USCityURL Dataset and Pipeline Setup

`USCityURL_Dataset.ipynb` loads the municipal website directory from the [UScityURL](https://github.com/caimeng2/UScityURL) repository, tests each unique homepage, and creates the audit and pipeline-ready datasets. `USCityURL_Pipeline.ipynb` then uses the pipeline-ready dataset for a limited Orlando demo and a comparison of available cities such as Seattle.

Source CSV:

https://raw.githubusercontent.com/caimeng2/UScityURL/master/UScityURL.csv

The workflow uses the `GEOID`, `MUNICIPALITY`, `STATE`, and `WEBSITE_URL` columns.

1. Confirm the environment from section 3 is active (`nist-resilience`).
2. Open `USCityURL_Dataset.ipynb` in Jupyter or VS Code.
3. Select the `nist-resilience` Python environment.
4. Click **Run All**. An internet connection is required to test the municipal homepages. This creates `datasets_USCityPipeline/USCityURL_audit.csv` and `datasets_USCityPipeline/USCityURL_Pipeline.csv`, then synchronizes the persistent RAG database for the places and keywords selected in `setting.py`.
5. Open `USCityURL_Pipeline.ipynb`, select the same environment, and click **Run All**. An internet connection is required to request pages from Orlando and the available comparison cities.

The workflow:

- Tests each unique UScityURL homepage in parallel and records the access result.
- Keeps successful HTML homepages in the pipeline-ready dataset.
- Loads the pipeline-ready UScityURL dataset and selects the Orlando, Florida row (`https://www.orlando.gov/`).
- Crawls up to 60 pages, staying on the official Orlando domain.
- Repeats the original comparison rules for available cities such as Seattle.
- Keeps links whose anchor text or URL match resilience-related keywords (for example resilience, flood, hurricane, hazard mitigation, and comprehensive plan).
- Extracts text from up to 15 HTML or PDF candidates with BeautifulSoup or PyMuPDF.
- Marks a document usable if it has at least 100 words, drops exact duplicates, and runs preliminary topic-mention EDA on that sample.

Demo limits are set in the first code cell (`MAX_PAGES_TO_CRAWL = 60`, `MAX_DOCUMENTS_TO_ANALYZE = 15`). Results describe only the collected sample.

## 6. Local RAG Assistant

`setting.py` contains the selected municipalities or states in `INDEX_PLACES`, the crawl terms in `KEYWORDS`, the local Ollama models, and the crawl, chunking, parallelization, and retrieval settings. Use `INDEX_PLACES = ()` to select nothing or `INDEX_PLACES = ("all",)` to select every municipality in the pipeline CSV. An empty `KEYWORDS` tuple disables keyword filtering.

After running `USCityURL_Dataset.ipynb`, start the terminal assistant:

```bash
python main.py
```

Type a question at the prompt or type `exit` to stop. Only one `main.py` session can run at a time.

Add a municipality or state and synchronize its missing keyword coverage:

```bash
python main.py --place "Ann Arbor, Michigan"
```

Add a keyword and synchronize it across the selected municipalities:

```bash
python main.py --keyword flood
```

Both flags can be used in one command. `--update` retries any missing configured place-keyword coverage without adding a new setting:

```bash
python main.py --place "Ann Arbor, Michigan" --keyword flood
python main.py --update
```

New places and keywords are saved in `setting.py`. Existing place-keyword coverage is not recrawled. A changed pipeline CSV clears the previous Chroma snapshot and extracted-document cache, then rebuilds the places selected by `INDEX_PLACES`. With the same CSV, updates are additive. Extracted HTML and PDF content is cached under `Persistent_db/document_cache` and revalidated before reuse.

Ollama is started automatically if it is installed but not running. Both required models must already be installed with the commands in Section 3.

## 7. Troubleshooting

- **ModuleNotFoundError:** Run `python -m pip install -r requirements.txt`.
- **FileNotFoundError:** Check that the CSV is in the correct folder.
- **Kernel errors:** Select the correct Python environment and restart the kernel.
- **Connection or timeout errors in the USCityURL notebooks:** The notebooks need internet access to test municipal homepages and request pages from Orlando and the available comparison cities. Check the connection and rerun the notebook.
- **No usable documents in USCityURL_Pipeline.ipynb:** Review the candidate-link and failure tables in the notebook. Pages with fewer than 100 extracted words are not used in the EDA. Crawl results can change if the city website updates.
- **Ollama model error:** Run `ollama pull embeddinggemma` and `ollama pull llama3.2:3b`, then rerun `python main.py`.
- **Another main.py session is already running:** Exit the other terminal session before starting a new one.
