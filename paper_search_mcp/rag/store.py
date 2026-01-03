import numpy as np
from typing import List, Dict, Any, Tuple, Optional
try:
    import faiss
except ImportError:
    faiss = None

class VectorStore:
    def __init__(self, encoder):
        """
        Initialize with a pre-loaded encoder (SentenceTransformer model).
        """
        self.encoder = encoder
        self.dimension = self.encoder.get_sentence_embedding_dimension()
        
        if faiss:
            self.index = faiss.IndexFlatL2(self.dimension)
        else:
            self.index = None
            
        self.documents: List[Dict[str, Any]] = []

    def add_documents(self, documents: List[Dict[str, Any]]):
        """
        Embed and add documents to the store.
        documents: List of dicts with 'text' and 'metadata'.
        """
        texts = [doc['text'] for doc in documents]
        if not texts:
            return

        embeddings = self.encoder.encode(texts)
        
        # Add to FAISS index
        if self.index:
            self.index.add(np.array(embeddings).astype('float32'))
        
        # Keep track of documents to map index back to content
        self.documents.extend(documents)

    def search(self, query: str, k: int = 5) -> List[Tuple[Dict[str, Any], float]]:
        """
        Search for relevant documents.
        Returns list of (document, distance).
        """
        if not self.documents:
            return []
            
        query_vector = self.encoder.encode([query])
        
        if self.index:
            distances, indices = self.index.search(np.array(query_vector).astype('float32'), k)
            
            results = []
            for i, idx in enumerate(indices[0]):
                if idx != -1 and idx < len(self.documents):
                    results.append((self.documents[idx], float(distances[0][i])))
            return results
        
        return []

    def clear(self):
        if self.index:
            self.index.reset()
        self.documents = []
