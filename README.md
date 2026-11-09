# NIST Community Resilience

### Community Resilience Analysis Using NLP

This project supports an academic research collaboration involving **Johns Hopkins University**, **Michigan State University**, and researchers associated with the **Community Resilience Program at the National Institute of Standards and Technology (NIST)**.

The project focuses on understanding how resilience planning is discussed, documented, and implemented by municipalities across the United States. Rather than studying a single organization or community, the goal is to develop methods and tools that can support broader research on community resilience and inform future resilience-planning guidance.

A particular focus is placed on how local governments describe resilience priorities, identify risks and barriers, and communicate planning decisions and tradeoffs through publicly available documents.

## Project Overview

Communities across the United States face increasing risks from hazards such as extreme weather events, wildfires, floods, and earthquakes. Understanding how municipalities prepare for and respond to these risks requires analyzing a large and continually changing collection of public planning documents.

The primary goal of this project is to develop a reproducible and maintainable data pipeline that collects resilience-related information from municipal websites and converts it into a structured dataset suitable for Natural Language Processing (NLP) analysis.

The workflow begins with a collection of municipal URLs and is designed to:

- Retrieve documents and web content from municipal sources.
- Extract resilience-related text and relevant metadata.
- Store the extracted information in a structured and reusable dataset.
- Support repeated runs so that new or updated documents can be incorporated over time.
- Prepare the collected text for downstream NLP and resilience research.

Once the data-collection pipeline is established, the resulting dataset can be used to investigate how municipalities discuss resilience, identify common themes and priorities, and determine which types of documents are most useful for further NLP analysis.

The project also includes a local Retrieval-Augmented Generation (RAG) assistant that crawls selected municipal sources, stores embeddings in a persistent Chroma database, and answers questions with local Ollama models.

The **reproducible workflow is the primary project deliverable**. The resulting dataset and initial research findings are important secondary outcomes.

## Installation

For instructions on setting up the environment, installing dependencies, running the notebooks, and using the local RAG assistant, see [INSTALL.md](INSTALL.md).

## Local RAG Demo

Create a clean Orlando flood index:

```bash
python main.py --update --place "Orlando, Florida" --keyword flood
```

Ask a question at the prompt, then type `exit`. Add Tampa and a new hurricane keyword without rebuilding Orlando's existing flood coverage:

```bash
python main.py --place "Tampa, Florida" --keyword hurricane
```

Ask the assistant to compare flood and hurricane information in Orlando and Tampa. Run `python main.py` afterward to reuse the persistent database without crawling again. See INSTALL.md for the complete demonstration sequence.

## Local RAG Behavior

- The assistant uses local Ollama models and does not require a paid model API.
- `USCityURL_Dataset.ipynb` creates the audit and pipeline CSVs, then synchronizes the configured persistent database.
- `INDEX_PLACES` accepts states, municipalities, or `"City, State"`. `KEYWORDS` uses generic English stemming, so `flood` also matches forms such as floods, flooded, and flooding.
- If either configuration tuple is empty, a rebuild produces an empty database. `("all",)` selects every municipality in `INDEX_PLACES` or disables keyword filtering in `KEYWORDS`.
- `--update` starts a new database on the current CSV by clearing Chroma, the extracted-document cache, `INDEX_PLACES`, and `KEYWORDS` before applying new flags.
- With the same CSV, new places and keywords are added without rebuilding completed place-keyword coverage.
- Answers are restricted to retrieved municipal context and list the retrieved URLs once at the end.

Using `("all",)` in both configuration tuples requests an unfiltered crawl of every accessible municipality and can take a long time.

## Main Files

| File | Purpose |
|---|---|
| [USCityURL_Dataset.ipynb](USCityURL_Dataset.ipynb) | Audit municipal homepages, create the pipeline CSV, and synchronize the configured persistent database. |
| [USCityURL_Pipeline.ipynb](USCityURL_Pipeline.ipynb) | Run the bounded Orlando EDA demo and additional multi-city comparison. |
| [TraCR_dataset.ipynb](TraCR_dataset.ipynb) | Explore TraCR and create the cleaned project dataset. |
| [main.py](main.py) | Run the terminal RAG assistant and process reset, place, and keyword flags. |
| [rag.py](rag.py) | Crawl, extract, cache, chunk, embed, retrieve, and generate grounded answers. |
| [setting.py](setting.py) | Store paths, models, scopes, crawl limits, parallelization, chunking, and retrieval settings. |
| [requirements.txt](requirements.txt) | List the Python dependencies for the notebooks and local RAG workflow. |

## Exploratory Data Analysis

Our team conducted preliminary exploratory data analysis (EDA) to evaluate datasets and identify their potential applications in community resilience planning.

| Notebook | EDA Goal |
|---|---|
| [TraCR Dataset EDA](TraCR_dataset.ipynb) | Evaluate the structure, completeness, and geographic coverage of the NIST TraCR dataset, then create one usable project dataset. |
| [USCityURL Dataset](USCityURL_Dataset.ipynb) | Test each unique municipal homepage, create the audit and pipeline-ready datasets, and synchronize the selected municipal RAG database. |
| [USCityURL Pipeline](USCityURL_Pipeline.ipynb) | Use the pipeline-ready municipal directory to locate Orlando’s official website, crawl a limited set of on-domain pages, discover resilience-related links from anchor text and URLs, extract HTML or PDF text, and run preliminary topic-mention analysis on the usable sample. |

## Current Progress

Explored the NIST TraCR dataset to identify data quality issues and potential applications.

Tested unique UScityURL homepages and created an access audit and pipeline-ready municipal dataset.

Used UScityURL to locate Orlando’s official municipal website and crawl a limited set of on-domain pages, keeping links whose anchor text or URL matched resilience-related keywords.

Extracted and quality-checked a sample of HTML or PDF candidates, then ran preliminary topic-mention EDA on the usable documents.

Established installation instructions and project dependencies to support reproducibility.

Added a local municipal RAG assistant with persistent embeddings, additive place and keyword updates, and retrieved source links.

## Research Questions

The project is guided by three main research questions:

1. **How can we build a reproducible workflow that starts with municipal URLs and produces a structured, updateable dataset of resilience-related text?**

2. **What metadata and document structure are necessary to make the dataset easy to search, maintain, refresh, and extend?**

3. **What initial patterns can be identified in how municipalities describe resilience goals, risks, barriers, and planning priorities?**

## Goal

The overall goal is to create a scalable and reusable foundation for collecting, organizing, and analyzing municipal resilience documents using NLP methods.
