import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Paths
DATA_DIR = "data"
CHROMA_DIR = "chroma_db"
METADATA_FILE = "data/metadata_manifest.json"

# Chunking
CHUNK_SIZE = 500
OVERLAP_SIZE = 50

# Retrieval
TOP_K = 5
COLLECTION_NAME = "policy_documents"

# Embedding Model
EMBED_MODEL = "BAAI/bge-small-en-v1.5"

# LLM
LLM_MODEL = "gemini-2.5-flash"
LLM_TEMPERATURE = 0.1 # low temperature for more factual responses and less creativity