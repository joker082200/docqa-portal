import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
EMBED_MODEL = "text-embedding-3-small"
LLM_MODEL = "gpt-4.1-mini"

# Paths
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
VECTORSTORE_DIR = DATA_DIR / "vectorstore"
FAISS_INDEX_PATH = str(VECTORSTORE_DIR / "index.faiss")
FAISS_META_PATH = str(VECTORSTORE_DIR / "metadata.json")
