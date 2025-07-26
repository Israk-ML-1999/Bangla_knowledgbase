import os
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from modules.config import EMBED_MODEL, INDEX_PATH, VECTOR_DIR

class Retriever:
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(model_name=EMBED_MODEL)
        # Load the vectorstore
        self.vectorstore = FAISS.load_local(
            os.path.dirname(INDEX_PATH),
            self.embeddings,
            allow_dangerous_deserialization=True
        )

    def retrieve(self, query, top_k=5):
        """
        Retrieve relevant text chunks using similarity search.
        Args:
            query: The search query
            top_k: Number of most relevant chunks to return
        Returns:
            List of relevant text chunks
        """
        docs = self.vectorstore.similarity_search(query, k=top_k)
        return [doc.page_content for doc in docs]  