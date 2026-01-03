import uuid
import logging
from typing import Dict, List, Any, Optional
from sentence_transformers import SentenceTransformer
from .processors import DoclingProcessor
from .store import VectorStore

logger = logging.getLogger(__name__)

class RAGManager:
    def __init__(self):
        # Initialize heavy models once
        logger.info("Initializing RAG models...")
        # device='cuda' will auto-select the first GPU if available
        # On production environments with NVIDIA cards, this is critical.
        # Fallback to cpu happens if cuda is not available inside the library usually, 
        # but explicit check is safer.
        import torch
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
        logger.info(f"Using device: {device}")
        
        self.encoder = SentenceTransformer("google/embeddinggemma-300M", device=device)
        self.processor = DoclingProcessor()
        
        # Session storage
        # { session_id: { 'store': VectorStore, 'files': set(paper_ids) } }
        self.sessions: Dict[str, Dict[str, Any]] = {}
        logger.info("RAG Manager initialized.")

    def create_session(self) -> str:
        """Create a new RAG session and return its ID."""
        session_id = str(uuid.uuid4())
        self.sessions[session_id] = {
            'store': VectorStore(self.encoder),
            'files': set()
        }
        return session_id

    def delete_session(self, session_id: str) -> bool:
        """Delete a session given its ID."""
        if session_id in self.sessions:
            del self.sessions[session_id]
            return True
        return False

    def add_paper(self, session_id: str, paper_id: str, file_path: str) -> str:
        """
        Process a PDF and add it to the session's vector store.
        Returns a status message.
        """
        if session_id not in self.sessions:
            raise ValueError(f"Session {session_id} not found.")

        session = self.sessions[session_id]
        
        # Check if already added
        if paper_id in session['files']:
            return f"Paper {paper_id} already in session."

        try:
            # Process PDF
            chunks = self.processor.process_pdf(file_path)
            
            # Add paper_id to metadata for filtering if needed later
            for chunk in chunks:
                chunk['metadata']['paper_id'] = paper_id

            # Add to vector store
            session['store'].add_documents(chunks)
            session['files'].add(paper_id)
            
            return f"Successfully added paper {paper_id} to session {session_id}. Processed {len(chunks)} chunks."
            
        except Exception as e:
            logger.error(f"Failed to add paper {paper_id}: {e}")
            raise

    def query(self, session_id: str, query_text: str, k: int = 5) -> List[Dict[str, Any]]:
        """
        Query the session's knowledge base.
        """
        if session_id not in self.sessions:
            raise ValueError(f"Session {session_id} not found.")
            
        store = self.sessions[session_id]['store']
        results = store.search(query_text, k=k)
        
        # Format results
        formatted_results = []
        for doc, distance in results:
            formatted_results.append({
                'text': doc['text'],
                'metadata': doc['metadata'],
                'score': float(distance) # lower is better for L2
            })
            
        return formatted_results

    def list_sessions(self) -> List[str]:
        return list(self.sessions.keys())

    def get_session_info(self, session_id: str) -> Dict[str, Any]:
        if session_id in self.sessions:
            return {
                'id': session_id,
                'paper_count': len(self.sessions[session_id]['files']),
                'active_papers': list(self.sessions[session_id]['files'])
            }
        return {}
