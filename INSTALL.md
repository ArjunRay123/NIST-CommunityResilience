# NIST Community Resilience — Installation Guide

## 1. Prerequisites

- Python 3.10 or newer
- Git
- Jupyter Notebook or VS Code with Jupyter extension
- [Ollama](https://ollama.com/) for the local RAG assistant
- An internet connection for crawling municipal websites and for optional source-data refreshes

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
