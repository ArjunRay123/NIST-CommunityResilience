"""Single configuration file for the local USCityURL RAG system."""

from pathlib import Path


# Data and storage
PROJECT_ROOT = Path(__file__).resolve().parent
SETTING_FILE = PROJECT_ROOT / "setting.py"
USCITYURL_SOURCE_URL = "https://raw.githubusercontent.com/caimeng2/UScityURL/master/UScityURL.csv"
AUDIT_CSV = PROJECT_ROOT / "datasets_USCityPipeline" / "USCityURL_audit.csv"
PIPELINE_CSV = PROJECT_ROOT / "datasets_USCityPipeline" / "USCityURL_Pipeline.csv"
PERSISTENT_DIR = PROJECT_ROOT / "Persistent_db"
STATUS_CSV = PERSISTENT_DIR / "municipality_status.csv"
CHROMA_DIR = PERSISTENT_DIR / "chroma"
DOCUMENT_CACHE_DIR = PERSISTENT_DIR / "document_cache"
EMBED_MODEL_FILE = PERSISTENT_DIR / "embedding_model.txt"
BUILD_STATE_FILE = PERSISTENT_DIR / "build_state.json"
MAIN_LOCK_FILE = PERSISTENT_DIR / "main.lock"
COLLECTION_NAME = "uscityurl_municipal_content"

# State names and municipality names are both accepted. "City, State" disambiguates.
# Use () to select nothing. Use ("all",) to select every pipeline municipality.
# Removing one named place does not delete its embeddings; an empty scope clears the build.

# Use () to select nothing. Use ("all",) to disable keyword filtering.
# Multiple named keywords use OR matching.
INDEX_PLACES = ()
KEYWORDS = ()

# Local Ollama models
DEFAULT_EMBED_MODEL = "embeddinggemma"
DEFAULT_LLM_MODEL = "llama3.2:3b"

# General Ollama runtime behavior. These values are not tied to a Mac model.
# Each model remains loaded for 30 minutes after use, at most two models may
# remain loaded, and this single-user application serves one request at a time.
OLLAMA_KEEP_ALIVE = "30m"
OLLAMA_KEEP_ALIVE_SECONDS = 30 * 60
OLLAMA_MAX_LOADED_MODELS = 2
OLLAMA_NUM_PARALLEL = 1

# General parallelism defaults for modern high-performance laptops.
# These values assume computing power similar to an M3 Pro but are not OS-specific.
MAX_AUDIT_WORKERS = 40
MAX_MUNICIPALITY_WORKERS = 20
MAX_PAGE_WORKERS_PER_MUNICIPALITY = 4
MAX_HTTP_CONNECTIONS = 40
MAX_EMBEDDING_WORKERS = 1
EMBEDDING_BATCH_SIZE = 128

# Crawl behavior. Zero means no page limit.
AUDIT_CONNECT_TIMEOUT = 5
AUDIT_READ_TIMEOUT = 10
AUDIT_SAMPLE_BYTES = 65_536
AUDIT_USER_AGENT = "CMSE495-USCityURL-Access-Audit/1.0 (educational research)"
MAX_PAGES_PER_MUNICIPALITY = 0
REQUEST_TIMEOUT = 20
REQUEST_DELAY = 0.15
MAX_DOCUMENT_BYTES = 20_000_000
MIN_DOCUMENT_WORDS = 20
MAX_SITEMAPS_PER_MUNICIPALITY = 100
USER_AGENT = "NIST-CommunityResilience-RAG/1.0 (educational research)"

# Chunking and retrieval
CHUNK_SIZE = 1_200
CHUNK_OVERLAP = 200
TOP_K = 5
BROAD_TOP_K = 24
BROAD_FETCH_K = 100
BROAD_FETCH_MULTIPLIER = 2
BROAD_MAX_CHUNKS_PER_MUNICIPALITY = 2
CHROMA_WRITE_BATCH_SIZE = 1_000
REGISTRY_SAVE_INTERVAL = 10

# File types that are not indexed. HTML and PDF remain enabled.
SKIP_EXTENSIONS = (
    ".7z", ".avi", ".bmp", ".css", ".csv", ".doc", ".docx", ".gif",
    ".gz", ".ico", ".jpeg", ".jpg", ".js", ".json", ".mov", ".mp3",
    ".mp4", ".png", ".ppt", ".pptx", ".rar", ".rss", ".svg", ".tar",
    ".tif", ".tiff", ".wav", ".webp", ".xls", ".xlsx", ".xml", ".zip",
)
