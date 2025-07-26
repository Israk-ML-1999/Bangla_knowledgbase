import os
import json
from datetime import datetime
import time
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from modules.config import (
    EMBED_MODEL,
    CHUNK_SIZE,
    CHUNK_OVERLAP,
    DATA_PATH,
    VECTOR_DIR,
    INDEX_PATH
)

UNWANTED_PHRASES = {
    'HSC 26',
    'অনলাইন ব্যাচ',
    'বাংলা ইংরেজি আইসিটি',
    'শিখনফল',
    'MINUTE',
    'SCHOOL',
    'শিক্ষা বোর্ড',
    'প্রশ্ন',
    'উত্তর',
    'নম্বর',
    'মার্ক',
    'পৃষ্ঠা',
}

os.makedirs(VECTOR_DIR, exist_ok=True)

def clean_text_file(path):
    with open(path, encoding='utf-8') as f:
        lines = f.readlines()
    cleaned = [line.strip() for line in lines if line.strip() and line.strip() not in UNWANTED_PHRASES]
    return '\n'.join(cleaned)

def build_vector_store():
    start_time = time.time()
    
    # 1. Clean the text
    print("1. Cleaning text...")
    cleaned_text = clean_text_file(DATA_PATH)
    
    # 2. Split into chunks
    print("2. Splitting into chunks...")
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )
    docs = splitter.create_documents([cleaned_text])
    print(f"Created {len(docs)} chunks")
    
    # 3. Create embeddings
    print("3. Creating embeddings...")
    embedding_start = time.time()
    embeddings = HuggingFaceEmbeddings(model_name=EMBED_MODEL)
    vectorstore = FAISS.from_documents(docs, embeddings)
    embedding_end = time.time()
    
    # 4. Save vector store
    print("4. Saving vector store...")
    vectorstore.save_local(VECTOR_DIR)
    
    # Save process information as JSON
    process_info = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_chunks": len(docs),
        "chunk_settings": {
            "chunk_size": CHUNK_SIZE,
            "chunk_overlap": CHUNK_OVERLAP
        },
        "embedding_model": EMBED_MODEL,
        "timing": {
            "embedding_duration": f"{embedding_end - embedding_start:.2f} seconds",
            "total_duration": f"{time.time() - start_time:.2f} seconds"
        },
        "chunks_preview": [
            {
                "id": i,
                "length": len(doc.page_content),
                "preview": doc.page_content[:100] + "..." if len(doc.page_content) > 100 else doc.page_content
            }
            for i, doc in enumerate(docs)
        ]
    }
    
    # Save process info to JSON
    info_path = os.path.join(VECTOR_DIR, "embedding_info.json")
    with open(info_path, "w", encoding='utf-8') as f:
        json.dump(process_info, f, ensure_ascii=False, indent=2)
    
    # Save embedding process information
    process_info = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_chunks": len(docs),
        "chunk_settings": {
            "chunk_size": CHUNK_SIZE,
            "chunk_overlap": CHUNK_OVERLAP
        },
        "embedding_model": EMBED_MODEL,
        "timing": {
            "embedding_duration": f"{embedding_end - embedding_start:.2f} seconds",
            "total_duration": f"{time.time() - start_time:.2f} seconds"
        },
        "chunks_preview": [
            {
                "id": i,
                "length": len(doc.page_content),
                "preview": doc.page_content[:100] + "..." if len(doc.page_content) > 100 else doc.page_content
            }
            for i, doc in enumerate(docs)
        ]
    }
    
    # Save process info to JSON
    info_path = os.path.join(VECTOR_DIR, "embedding_info.json")
    with open(info_path, "w", encoding='utf-8') as f:
        json.dump(process_info, f, ensure_ascii=False, indent=2)
    
    print(f"\nProcess Summary:")
    print(f"- Total chunks: {len(docs)}")
    print(f"- Embedding time: {process_info['timing']['embedding_duration']}")
    print(f"- Total time: {process_info['timing']['total_duration']}")
    print(f"\nVector store saved to {VECTOR_DIR}/")
    print(f"Embedding info saved to {info_path}")

if __name__ == "__main__":
    build_vector_store() 