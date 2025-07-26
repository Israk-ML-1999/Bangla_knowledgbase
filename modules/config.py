import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# PDF and vector store paths
# File paths and directories
DATA_PATH = os.getenv('DATA_PATH', 'data/New_10m.txt')
VECTOR_DIR = os.getenv('VECTOR_DIR', 'vector_store')
INDEX_PATH = os.getenv('INDEX_PATH', os.path.join(VECTOR_DIR, 'index.faiss'))
HISTORY_FILE = os.getenv('HISTORY_FILE', 'chat_data.json')

# Embedding model
EMBED_MODEL = os.getenv('EMBED_MODEL', 'sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')

# OpenAI API
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo')  # Available models: gpt-4, gpt-3.5-turbo

# Chunking
CHUNK_SIZE = int(os.getenv('CHUNK_SIZE', 512))
CHUNK_OVERLAP = int(os.getenv('CHUNK_OVERLAP', 128))

# Short-term memory
SHORT_TERM_HISTORY = int(os.getenv('SHORT_TERM_HISTORY', 25)) 