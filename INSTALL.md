# NIST Community Resilience — Installation Guide

## 1. Prerequisites

- Python 3.10 or newer
- Git
- Jupyter Notebook or VS Code with Jupyter extension
- [Ollama](https://ollama.com/) for the local RAG assistant
- An internet connection for downloading USCityURL and crawling municipal websites

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
4. Click **Run All**. This creates `datasets_USCityPipeline/USCityURL_audit.csv` and `datasets_USCityPipeline/USCityURL_Pipeline.csv`, then synchronizes the persistent RAG database for the places and keywords selected in `setting.py`.
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

If the pipeline CSV hash changes, the dataset notebook clears the previous Chroma snapshot and extracted-document cache before rebuilding the configured scope. It does not clear `INDEX_PLACES` or `KEYWORDS`. If the CSV hash is unchanged, completed coverage is retained.

## 6. Local RAG Assistant

`setting.py` contains the selected municipalities or states in `INDEX_PLACES`, the crawl terms in `KEYWORDS`, the local Ollama models, and the crawl, chunking, parallelization, and retrieval settings. Use an empty tuple to select nothing. Use `INDEX_PLACES = ("all",)` to select every municipality in the pipeline CSV or `KEYWORDS = ("all",)` to disable keyword filtering. Using `("all",)` in both tuples loads all municipal content without place or keyword filtering. If either tuple is empty, the rebuilt persistent database is empty.

A one-item Python tuple requires a trailing comma:

```python
INDEX_PLACES = ("Orlando, Florida",)
KEYWORDS = ("flood",)
```

State names select every available municipality in that state. A bare municipality name selects every same-named municipality in the pipeline CSV, while `"City, State"` selects one exact municipality. Keyword matching uses generic English stemming and prefix matching, so a keyword such as `flood` also covers forms such as floods, flooded, flooding, and floodplain.

The repository defaults both scopes to empty. After running `USCityURL_Dataset.ipynb`, create the initial scope with both flags:

```bash
python main.py --place "Orlando, Florida" --keyword flood
```

After embeddings have been built, start the terminal assistant without update flags:

```bash
python main.py
```

Type a question at the prompt or type `exit` to stop. Only one `main.py` session can run at a time.

Add a municipality or state and synchronize its missing keyword coverage:

```bash
python main.py --place "Tampa, Florida"
```

Add a keyword and synchronize it across the selected municipalities:

```bash
python main.py --keyword hurricane
```

Both flags can be used in one command. `--update` clears the current Chroma database, extracted-document cache, `INDEX_PLACES`, and `KEYWORDS` before applying any place or keyword flags:

```bash
python main.py --place "Jacksonville, Florida" --keyword tornado
python main.py --update
python main.py --update --place "Orlando, Florida" --keyword flood
```

New places and keywords are saved in `setting.py`. Existing place-keyword coverage is not recrawled. A changed pipeline CSV clears the previous Chroma snapshot and extracted-document cache, then rebuilds the configured place and keyword scope. With the same CSV and nonempty scopes, updates are additive. Extracted HTML and PDF content is cached under `Persistent_db/document_cache` and revalidated before reuse.

The main persistent files are:

- `Persistent_db/chroma`: Chroma vectors and metadata.
- `Persistent_db/document_cache`: Extracted HTML and PDF content with HTTP revalidation metadata.
- `Persistent_db/municipality_status.csv`: Place, keyword-coverage, document-count, chunk-count, and error status.
- `Persistent_db/build_state.json`: CSV hash, configured scope, model, and build completion state.

The worker defaults in `setting.py` are tuned for an M3 Pro. Reduce the audit, municipality, page, or HTTP worker settings if another machine experiences high memory use, connection failures, or website throttling. `MAX_PAGES_PER_MUNICIPALITY = 0` means no page limit. Combining that setting with `("all",)` in both scopes can produce a very large and slow crawl.

Ollama is started automatically if it is installed but not running. Both required models must already be installed with the commands in Section 3.

## 7. Local RAG Demonstration

Open a terminal in the repository and activate the environment:

```bash
conda activate nist-resilience
```

Confirm that both Ollama models are installed:

```bash
ollama list
```

Create a clean database containing Orlando flood information:

```bash
python main.py --update --place "Orlando, Florida" --keyword flood
```

At the question prompt, enter:

```text
What flood-related information, hazards, maps, and resources does Orlando provide?
```

After the answer, exit:

```text
exit
```

Add Tampa as a new municipality and hurricane as a new keyword:

```bash
python main.py --place "Tampa, Florida" --keyword hurricane
```

Orlando keeps its existing flood embeddings and receives only the new hurricane coverage. Tampa is new, so it receives both flood and hurricane coverage.

At the question prompt, enter each comparison question separately:

```text
Compare the flood and hurricane information, preparedness guidance, and resources available in Orlando and Tampa, Florida.
```

```text
How do Orlando and Tampa differ in the flood information they provide?
```

```text
What hurricane preparedness resources are available in Orlando and Tampa?
```

Exit after the questions:

```text
exit
```

Confirm the saved configuration:

```bash
python - <<'PY'
from setting import INDEX_PLACES, KEYWORDS

print("INDEX_PLACES:", INDEX_PLACES)
print("KEYWORDS:", KEYWORDS)
PY
```

The expected configuration is:

```text
INDEX_PLACES: ('Orlando, Florida', 'Tampa, Florida')
KEYWORDS: ('flood', 'hurricane')
```

Demonstrate persistent reuse without crawling or rebuilding:

```bash
python main.py
```

Ask:

```text
Compare flood preparedness resources in Orlando and Tampa, Florida.
```

Then exit:

```text
exit
```

## 8. Troubleshooting

- **ModuleNotFoundError:** Run `python -m pip install -r requirements.txt`.
- **FileNotFoundError:** Check that the CSV is in the correct folder.
- **Kernel errors:** Select the correct Python environment and restart the kernel.
- **Connection or timeout errors in the USCityURL notebooks:** The notebooks need internet access to test municipal homepages and request pages from Orlando and the available comparison cities. Check the connection and rerun the notebook.
- **No usable documents in USCityURL_Pipeline.ipynb:** Review the candidate-link and failure tables in the notebook. Pages with fewer than 100 extracted words are not used in the EDA. Crawl results can change if the city website updates.
- **Ollama model error:** Run `ollama pull embeddinggemma` and `ollama pull llama3.2:3b`, then rerun `python main.py`.
- **Another main.py session is already running:** Exit the other terminal session before starting a new one.
- **Persistent_db has no usable embeddings:** Confirm that both `INDEX_PLACES` and `KEYWORDS` contain values, then build with `python main.py --place "City, State" --keyword keyword`. Plain `python main.py` opens an existing database; it does not build missing embeddings.
- **A configured place does not load:** Confirm that the municipality or state exists in `datasets_USCityPipeline/USCityURL_Pipeline.csv`. Missing places and unreadable websites are reported and skipped.
- **No keyword matches:** The crawler records zero coverage for that place-keyword pair and continues. Questions about unavailable context report that no context is available instead of generating an unsupported answer.
