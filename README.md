# Bangla/English RAG Chatbot

A sophisticated Retrieval-Augmented Generation (RAG) chatbot that answers questions in both Bangla and English with high accuracy and confidence scoring.

## Features

- **Bilingual Support**: Handles both Bangla and English queries
- **RAG System**: Uses FAISS for efficient vector similarity search
- **Confidence Scoring**: Returns cosine similarity scores with responses
- **Session Management**: Maintains conversation history
- **FastAPI Backend**: High-performance async API with Swagger UI
- **PDF/Text Processing**: Handles PDF and text documents efficiently
- **Multilingual Embeddings**: Uses `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`
- **Configurable**: Easy to customize through environment variables
- **Smart Response Format**: Returns answers with confidence scores and relevant source chunks

## Technical Details

### Components

1. **Vector Store (FAISS)**
   - Uses HuggingFace embeddings (paraphrase-multilingual-MiniLM-L12-v2)
   - Chunk size: 512 tokens
   - Chunk overlap: 128 tokens
   - Efficient similarity search

2. **Chat Engine**
   - Model: GPT-3.5 Turbo (configurable to GPT-4)
   - Response format includes confidence scores
   - Maintains conversation context
   - Short-term memory management

3. **API Endpoints**
   - POST `/chat`: Main chat endpoint
   - Input: `{query, session_id?, user_id?}`
   - Output: `{answer, session_id, cosine_similarity}`

### Response Format

```json
{
  "answer": "Response text",
  "session_id": "unique_session_id",
  "cosine_similarity": {
    "score": 0.923,
    "top_chunk": "Most relevant source text"
  }
}
```

## Setup

1. **Environment Setup**
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Configuration**
   Create a `.env` file with:
   ```env
   OPENAI_API_KEY=your_api_key
   DATA_PATH=data/New_10m.txt
   VECTOR_DIR=vector_store
   OPENAI_MODEL=gpt-3.5-turbo
   CHUNK_SIZE=512
   CHUNK_OVERLAP=128
   ```

3. **Build Vector Store**
   ```bash
   python -m modules.pdf_index_builder
   ```

4. **Run Server**
   ```bash
   uvicorn main:app --reload
   ```

5. **Access API**
   - Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
   - ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

## Project Structure
```
10_min/
├── main.py                 # FastAPI application entry point
├── requirements.txt        # Project dependencies
├── chat_data.json         # Chat history storage
├── modules/
│   ├── __init__.py
│   ├── chat_engine.py     # Core chat logic
│   ├── chat_history.py    # History management
│   ├── config.py          # Configuration settings
│   ├── pdf_index_builder.py # Vector store builder
│   ├── retriever.py       # FAISS retrieval logic
│   └── web_search.py      # Web search integration
├── data/                  # Data storage
│   └── New_10m.txt        # Source text data
└── vector_store/         # FAISS index storage
    └── index.faiss       # Vector embeddings
```

## Usage

### API Endpoints

1. **Chat Endpoint (`POST /chat`)**
```bash
curl -X POST "http://localhost:8000/chat" \
     -H "Content-Type: application/json" \
     -d '{
       "query": "Your question here",
       "session_id": "optional_session_id",
       "user_id": "optional_user_id"
     }'
```

### Example Response

```json
{
  "answer": "১৯৪৬",
  "session_id": "abc123",
  "cosine_similarity": {
    "score": 0.923,
    "top_chunk": "১৯৪৬ সালে বাংলা একাডেমি প্রতিষ্ঠিত হয়।"
  }
}
```

## Dependencies

Key libraries used in this project:

- **FastAPI**: Web framework for building APIs
- **Langchain**: Framework for building LLM applications
- **FAISS**: Efficient similarity search and clustering
- **HuggingFace Transformers**: For multilingual embeddings
- **OpenAI API**: For chat completions
- **Pydantic**: Data validation using Python type annotations
- **Python-dotenv**: Environment variable management
- **uvicorn**: ASGI server for running FastAPI

## Notes

- The system uses cosine similarity scores to measure confidence in responses
- Higher similarity scores (closer to 1.0) indicate more reliable answers
- Session management allows for maintaining conversation context
- The vector store is built using multilingual embeddings for better Bangla support
- Configure chunk size and overlap based on your content needs
- Monitor OpenAI API usage through their dashboard
│   ├── kb_index.faiss       # FAISS index
│   └── kb_metadata.pkl      # Chunk metadata
```

## Usage
- Use the `/chat` endpoint in Swagger UI to ask questions in Bangla or English.
- The system will return only the answer (no explanation), based on the PDF content.

## Notes
- Only digital text and tables are used; images/graphics are ignored.
- Embeddings are multilingual, so both Bangla and English queries are supported.
- For best results, ensure your PDF is high quality and text-based.

## Author
- Adapted for your requirements by AI assistant 