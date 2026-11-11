# NIST Community Resilience

### Community Resilience Analysis Using NLP

This project supports an academic research collaboration involving **Johns Hopkins University**, **Michigan State University**, and researchers associated with the **Community Resilience Program at the National Institute of Standards and Technology (NIST)**.

The project studies how resilience planning is discussed, documented, and implemented by municipalities across the United States. It provides reproducible workflows for preparing structured resilience data, collecting municipal documents, and asking locally generated questions about the collected material.

The project has three main parts:

- A cleaned NIST Tracking Community Resilience (TraCR) dataset for county-level analysis.
- A USCityURL audit and pipeline-ready municipal website directory.
- A local Retrieval-Augmented Generation (RAG) assistant built with Ollama and Chroma.

The RAG assistant runs locally and does not require a paid model API. An internet connection is still required when municipal websites are crawled or the USCityURL source data are refreshed.

## Quick start

For a shorter installation-focused guide and run instructions, see [INSTALL.md](INSTALL.md).

### Build the first persistent database

The repository already includes:

- `datasets_USCityPipeline/USCityURL_audit.csv`
- `datasets_USCityPipeline/USCityURL_Pipeline.csv`

You do **not** need to run `USCityURL_Dataset.ipynb` before using the RAG assistant. The repository defaults both scopes to empty. Create the initial scope directly (for the demo, we use Orlando, Florida and flood) from the supplied CSV with both flags:

```bash
python main.py --place "Orlando, Florida" --keyword flood
```

This command saves the place and keyword in `setting.py`, crawls matching Orlando content, creates `Persistent_db`, generates embeddings, opens the Chroma database, and starts question mode.

Ask a question:

```text
What flood-related information, maps, and resources does Orlando provide?
```

Exit with:

```text
exit
```

### Reuse the database

After the database has been built, start the assistant without crawling again:

```bash
python main.py
```

Plain `python main.py` opens an existing database. It does not create missing embeddings when no place-keyword coverage has been built.

## Supplied data and optional notebooks

The CSV files required by the local RAG assistant are committed to the repository. Running the notebooks is optional unless the underlying data need to be refreshed or the EDA itself is being reproduced.

| File | Purpose | Required before `main.py`? |
|---|---|---:|
| `datasets_USCityPipeline/USCityURL_Pipeline.csv` | Pipeline-ready municipality, state, GEOID, and official website records. | Already supplied |
| `datasets_USCityPipeline/USCityURL_audit.csv` | Homepage access results used to recognize unavailable municipalities. | Already supplied |
| [USCityURL_Dataset.ipynb](USCityURL_Dataset.ipynb) | Download USCityURL again, audit live homepages, replace the supplied CSVs, and synchronize the configured persistent database. | Only for a data refresh |
| [USCityURL_Pipeline.ipynb](USCityURL_Pipeline.ipynb) | Run the bounded Orlando EDA demo and additional multi-city comparison. | No |
| [TraCR_dataset.ipynb](TraCR_dataset.ipynb) | Explore TraCR and create the cleaned project dataset. | No |

Municipal crawl results are live. Websites can change even when the supplied pipeline CSV remains unchanged.

### TraCR dataset setup

`TraCR_dataset.ipynb` explores the NIST Tracking Community Resilience (TraCR) dataset, focusing on data completeness, geographic coverage, and resilience indicators.

The dataset is already included in the repository under `datasets_TRaCr/TraCR_v1_database.csv`. **No additional download is required.**

**Original dataset source (optional):**

https://data.nist.gov/od/id/mds2-3978

1. Confirm the environment from the installation guide is active (`nist-resilience`).
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

### Refresh the supplied USCityURL data

**The dataset is already included in the repository under `datasets_USCityPipeline`. No additional download is required.**

`USCityURL_Dataset.ipynb` is only needed when the source directory and homepage-access results should be refreshed. It downloads the municipal website directory from the [UScityURL](https://github.com/caimeng2/UScityURL) repository, tests each unique homepage, and replaces the supplied audit and pipeline-ready CSVs.

Source CSV:

https://raw.githubusercontent.com/caimeng2/UScityURL/master/UScityURL.csv

The RAG workflow uses the `GEOID`, `MUNICIPALITY`, `STATE`, and `WEBSITE_URL` columns.

To refresh the supplied CSVs:

1. Confirm the environment from the installation guide is active (`nist-resilience`).
2. Open `USCityURL_Dataset.ipynb` in Jupyter or VS Code.
3. Select the `nist-resilience` Python environment.
4. Click **Run All**. This creates `datasets_USCityPipeline/USCityURL_audit.csv` and `datasets_USCityPipeline/USCityURL_Pipeline.csv`, then synchronizes the persistent RAG database for the places and keywords selected in `setting.py`.
5. Optionally open `USCityURL_Pipeline.ipynb`, select the same environment, and click **Run All** to reproduce the bounded Orlando EDA and available multi-city comparison.

The optional notebook workflow:

- Tests each unique UScityURL homepage in parallel and records the access result.
- Keeps successful HTML homepages in the pipeline-ready dataset.
- Loads the pipeline-ready UScityURL dataset and selects the Orlando, Florida row (`https://www.orlando.gov/`).
- Crawls up to 60 pages, staying on the official Orlando domain.
- Repeats the original comparison rules for available cities.
- Keeps links whose anchor text or URL match resilience-related keywords (for example resilience, flood, hurricane, hazard mitigation, and comprehensive plan).
- Extracts text from up to 15 HTML or PDF candidates with BeautifulSoup or PyMuPDF.
- Marks a document usable if it has at least 100 words, drops exact duplicates, and runs preliminary topic-mention EDA on that sample.

Demo limits are set in the first code cell (`MAX_PAGES_TO_CRAWL = 60`, `MAX_DOCUMENTS_TO_ANALYZE = 15`). Results describe only the collected sample.

If the pipeline CSV hash changes, the dataset notebook clears the previous Chroma snapshot and extracted-document cache before rebuilding the configured scope. It does not clear `INDEX_PLACES` or `KEYWORDS`. If the CSV hash is unchanged, completed coverage is retained.

## How the RAG workflow works

1. `INDEX_PLACES` selects municipalities or states from the supplied pipeline CSV.
2. `KEYWORDS` selects relevant sitemap URLs, links, titles, and extracted page text.
3. The crawler stays on the official municipal domain and respects `robots.txt` when it is available.
4. HTML and searchable PDF text are extracted and deduplicated.
5. Extracted documents are cached under `Persistent_db/document_cache` and revalidated with HTTP metadata before reuse.
6. Documents are split into overlapping chunks and embedded locally with `embeddinggemma`.
7. Chroma stores the vectors and municipality metadata.
8. Questions are geographically scoped, relevant chunks are retrieved, and `llama3.2:3b` writes an answer using only those excerpts.
9. Retrieved URLs are printed once at the end of the answer.

Unavailable places and zero-result keyword coverage do not stop the entire program. The assistant uses whatever indexed context is available and reports when requested context is missing.

## Configure places and keywords

All settings are in [setting.py](setting.py). Places and keywords can be added with terminal flags or edited manually.

Use an empty tuple to select nothing. Use `INDEX_PLACES = ("all",)` to select every municipality in the pipeline CSV or `KEYWORDS = ("all",)` to disable keyword filtering. Using `("all",)` in both tuples loads all municipal content without place or keyword filtering. If either tuple is empty, the rebuilt persistent database is empty.

### Terminal flags

Add one exact municipality:

```bash
python main.py --place "Tampa, Florida"
```

Add a state, which selects every available municipality in that state:

```bash
python main.py --place Florida
```

Add a keyword across every currently selected municipality:

```bash
python main.py --keyword hurricane
```

Add a new place and keyword together:

```bash
python main.py --place "Tampa, Florida" --keyword hurricane
```

Existing place-keyword coverage is retained. A new keyword is added to existing selected places, while a new place receives all currently configured keywords.

Do not use `--update` to apply manual settings because it clears both tuples first.

### Keyword rules
- `INDEX_PLACES = ()` selects nothing.
- `INDEX_PLACES = ("all",)` selects every municipality in the pipeline CSV.
- `"City, State"` selects one exact municipality.
- A state name selects every pipeline municipality in that state.
- A bare municipality name selects all same-named municipalities in the pipeline CSV.
- Removing one named place from `setting.py` does not delete its existing chunks during an additive update.
- Multiple named keywords use OR matching.
- Generic English stemming and prefix matching include grammatical variants and compounds.
- Multi-word keywords are matched as stemmed phrases.
- Completed zero-result coverage is recorded so the same place-keyword pair is not retried on every run.
- There is no fixed keyword list; any relevant word or phrase can be added.

## Keywords and their uses

Keywords control which municipal pages are selected for extraction and embedding. They are discovery filters, not fixed topic labels. A matching page may cover several topics, and a page can be stored once even when it matches more than one configured keyword.

Common project keywords include:

| Keyword | Intended use |
|---|---|
| `flood` | Flooding, floodplains, flood maps, flood insurance, drainage problems, mitigation, and reporting resources. |
| `hurricane` | Hurricane preparedness, evacuation, storm impacts, shelters, recovery, and local guidance. |
| `wildfire` | Wildfire mitigation, burn restrictions, smoke, evacuation, recovery, and fire-related planning. |
| `tornado` | Tornado warnings, shelters, severe-weather preparation, response, and recovery information. |
| `emergency` | Emergency management departments, alerts, response plans, emergency contacts, and preparedness resources. |
| `rain` | Heavy rainfall, drainage, stormwater, flash flooding, and rain-related service information. |
| `resilience` | Resilience plans, resilience offices, adaptation programs, community priorities, and planning documents. |
| `hazard mitigation` | Hazard-mitigation plans, risk assessments, mitigation projects, grants, and planning updates. |
| `comprehensive plan` | Long-range land-use, infrastructure, development, and community-planning documents. |
| `all` | Disable keyword filtering and accept all discovered municipal content. This can create a very large crawl. |

The matcher does not automatically add conceptual synonyms. For example, `flood` covers forms such as floods, flooded, flooding, and floodplain, but it does not guarantee that a page containing only `stormwater` will match. Add both terms when both concepts are required.

## Reset and rebuild behavior

Create a completely new database on the current CSV:

Running the reset alone leaves an empty database and empty settings:

```bash
python main.py --update
```

```bash
python main.py --update --place "Orlando, Florida" --keyword flood
```

`--update` performs these steps in order:

1. Deletes the existing Chroma vectors.
2. Deletes the extracted-document cache.
3. Resets municipality document counts, chunk counts, errors, and keyword coverage.
4. Clears `INDEX_PLACES` and `KEYWORDS` in `setting.py`.
5. Applies any `--place` and `--keyword` arguments from the same command.
6. Builds the newly requested scope from the existing pipeline CSV.


This reset does not regenerate either USCityURL CSV.

When `USCityURL_Dataset.ipynb` produces a pipeline CSV with a new hash, the old Chroma database and document cache are also cleared. Unlike `--update`, the notebook keeps the current `INDEX_PLACES` and `KEYWORDS` and rebuilds that configured scope. If the CSV hash is unchanged, completed coverage is retained.

## Persistent files

`Persistent_db` is generated locally and is excluded from Git. Each user creates it from the supplied CSV and live municipal websites.

| Path | Contents |
|---|---|
| `Persistent_db/chroma` | Chroma vectors, chunk text, and metadata. |
| `Persistent_db/document_cache` | Extracted page content plus ETag, Last-Modified, and content hashes. |
| `Persistent_db/municipality_status.csv` | Per-municipality status, keyword coverage, document counts, chunk counts, and crawl errors. |
| `Persistent_db/build_state.json` | Pipeline CSV hash, embedding model, configured scope, and build completion state. |
| `Persistent_db/embedding_model.txt` | Embedding model used to create the current vectors. |
| `Persistent_db/main.lock` | Prevents two `main.py` sessions from running simultaneously. |

Do not commit `Persistent_db` to GitHub. It contains generated vectors, cached live content, and machine-local state.

## Parallelism and performance

The defaults in `setting.py` are general settings for a modern high-performance laptop with computing power similar to an M3 Pro. They are not tied to macOS and can be used on similarly capable Linux or Windows systems.

| Setting | Default | Purpose |
|---|---:|---|
| `MAX_AUDIT_WORKERS` | 40 | Parallel homepage checks in `USCityURL_Dataset.ipynb`. |
| `MAX_MUNICIPALITY_WORKERS` | 20 | Municipalities prepared concurrently during an index build. |
| `MAX_PAGE_WORKERS_PER_MUNICIPALITY` | 4 | Pages fetched concurrently from one municipality. |
| `MAX_HTTP_CONNECTIONS` | 40 | Global HTTP request limit across active municipalities. |
| `MAX_EMBEDDING_WORKERS` | 1 | Concurrent Ollama embedding requests. One avoids local model contention. |
| `EMBEDDING_BATCH_SIZE` | 128 | Chunks sent in each embedding batch. |

The crawler also uses `REQUEST_DELAY = 0.15` between page requests. Increasing worker counts does not guarantee a faster run: municipal servers may throttle requests, and Ollama embedding throughput is limited by the local model and available memory.

`MAX_PAGES_PER_MUNICIPALITY = 0` means no page limit. This is appropriate when complete coverage is required, but it can produce a very large crawl when the place or keyword scope is broad.

Ollama keeps both local models available for 30 minutes after use. The first query after model loading can still be slower than later queries.

Ollama is started automatically if it is installed but not running. Both required models must already be installed with the commands in the installation guide.

## Local RAG demonstration

Create a clean Orlando flood database:

```bash
python main.py --update --place "Orlando, Florida" --keyword flood
```

Ask:

```text
What flood-related information, hazards, maps, and resources does Orlando provide?
```

Exit, then add Tampa and a new hurricane keyword:

```text
exit
```

```bash
python main.py --place "Tampa, Florida" --keyword hurricane
```

Orlando keeps its flood coverage and receives hurricane coverage. Tampa is new, so it receives both configured keywords.

Ask:

```text
Compare the flood and hurricane information, preparedness guidance, and resources available in Orlando and Tampa, Florida.
```

```text
How do Orlando and Tampa differ in the flood information they provide?
```

```text
What hurricane preparedness resources are available in Orlando and Tampa?
```

Exit and demonstrate persistence:

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

```bash
python main.py
```

The final command opens the stored database without crawling or rebuilding.

Ask:

```text
Compare flood preparedness resources in Orlando and Tampa, Florida.
```

Then exit:

```text
exit
```

## Project files

| File | Purpose |
|---|---|
| [main.py](main.py) | Terminal entry point, configuration flags, database validation, geographic scope resolution, and interactive questions. |
| [rag.py](rag.py) | Crawling, parsing, caching, chunking, embedding, Chroma updates, retrieval, and grounded answer generation. |
| [setting.py](setting.py) | Paths, scopes, models, worker counts, crawl behavior, chunking, and retrieval settings. |
| [requirements.txt](requirements.txt) | Python packages used by the notebooks and RAG workflow. |
| [USCityURL_Dataset.ipynb](USCityURL_Dataset.ipynb) | Optional live refresh of the supplied audit and pipeline CSVs. |
| [USCityURL_Pipeline.ipynb](USCityURL_Pipeline.ipynb) | Optional Orlando and multi-city EDA. |
| [TraCR_dataset.ipynb](TraCR_dataset.ipynb) | TraCR exploration and project-dataset creation. |

## Troubleshooting

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

## Current limitations

- Keyword-first discovery can miss a relevant page when the keyword appears only in the page body and not in its URL, title, or incoming anchor text.
- Live municipal sites can block requests, redirect pages, change templates, or publish scanned PDFs without searchable text.
- `("all",)` in both scopes can produce an extremely large crawl.
- The persistent database represents the municipal content available when it was last crawled; the supplied CSV identifies starting websites but does not contain downloaded page text.

## Research questions

The project is guided by three main research questions:

1. **How can we build a reproducible workflow that starts with municipal URLs and produces a structured, updateable dataset of resilience-related text?**
2. **What metadata and document structure are necessary to make the dataset easy to search, maintain, refresh, and extend?**
3. **What initial patterns can be identified in how municipalities describe resilience goals, risks, barriers, and planning priorities?**

## Goal

The overall goal is to create a scalable and reusable foundation for collecting, organizing, and analyzing municipal resilience documents using NLP methods.
