# Bangla/English RAG Chatbot

A sophisticated Retrieval-Augmented Generation (RAG) chatbot that answers questions in both Bangla and English with high accuracy and confidence scoring.

"But this PDF is not digital text, so OCR or PDF extraction models cannot properly extract the text."

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
   - Chunk size: 500 tokens
   - Chunk overlap: 200 tokens
   - Efficient similarity search

2. **Chat Engine**
   - Model: GPT-40 Turbo (configurable to GPT-4)
   - Response format includes confidence scores
   - Maintains conversation context
   - Short-term memory management
   - long-term memory management


3. **API Endpoints**
   - POST `/chat`: Main chat endpoint
   - Input: `{query, session_id?, user_id?}`
   - Output: `{answer, session_id, cosine_similarity}`

### Response Format

```json
{
  "answer": "Response text",
  "session_id": "unique_session_id",
  "user_id":"Unique"
}
```

## Setup

1. **Environment Setup**
   ```bash
   python -m venv env
   source env/bin/activate // Windows: env\Scripts\activate
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
│   
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
│   └── index.pkl      # Chunk metadata

## Input
```
{
  "query": "অনুপমের ভাষায় সুপুরুষ কাকে বলা হয়েছে ?",
  "session_id": "string",
  "user_id": "anonymous"
}
```
## Output
```
{
  "answer": "শম্ভুনাথ",
  "session_id": "string"
}
```
```

## Usage
- Use the `/chat` endpoint in Swagger UI to ask questions in Bangla or English.
- The system will return only the answer (no explanation), based on the PDF content and User History .

## Notes
- Only digital text and tables are used; images/graphics are ignored.
- Embeddings are multilingual, so both Bangla and English queries are supported.
- For best results, ensure your PDF is high quality and text-based.

## Author
- Adapted for your requirements by AI assistant

<img width="1135" height="904" alt="Image" src="https://github.com/user-attachments/assets/8811e6d6-6662-4d19-817d-d114302a932e" />



