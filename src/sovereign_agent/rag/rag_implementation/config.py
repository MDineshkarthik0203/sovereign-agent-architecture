import os

from dotenv import load_dotenv

load_dotenv()


# =========================
# OPENAI
# =========================

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "dummy-local-key")

OPENAI_CHAT_MODEL = "gpt-4o-mini"

OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"


# =========================
# STORAGE
# =========================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

DOCUMENT_DIR = os.path.join(
    BASE_DIR,
    "data",
    "documents"
)

CHROMA_DIR = os.path.join(
    BASE_DIR,
    "chroma_db"
)

COLLECTION_NAME = "sovereign_knowledge"


# =========================
# CHUNKING
# =========================

CHUNK_SIZE = 500

CHUNK_OVERLAP = 100


# =========================
# RETRIEVAL
# =========================

RETRIEVAL_K = 10

FINAL_K = 4