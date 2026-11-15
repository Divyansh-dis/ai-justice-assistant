import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file from project root or backend dir
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
PROJECT_ROOT = BASE_DIR.parent

# Resolve LEGAL_DATA_DIR flexibly across local and containerized/PaaS environments
def resolve_dir(env_var: str, default_rel_path: str) -> str:
    val = os.getenv(env_var)
    if val and Path(val).exists():
        return str(Path(val).resolve())
    for candidate in [PROJECT_ROOT / default_rel_path, BASE_DIR / default_rel_path, Path(f"./{default_rel_path}")]:
        if candidate.exists():
            return str(candidate.resolve())
    return str((PROJECT_ROOT / default_rel_path).resolve())

LEGAL_DATA_DIR = resolve_dir("LEGAL_DATA_DIR", "legal_data")
CHROMA_PERSIST_DIR = resolve_dir("CHROMA_PERSIST_DIR", "chroma_db")
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR / 'app_data.db'}")

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", os.getenv("GEMINI_API_KEY", ""))
LLM_MODEL = os.getenv("LLM_MODEL", "gemini-1.5-flash")

CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "1000"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "200"))
TOP_K_RESULTS = int(os.getenv("TOP_K_RESULTS", "4"))
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
