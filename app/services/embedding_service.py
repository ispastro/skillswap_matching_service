from sentence_transformers import SentenceTransformer
from typing import List
import numpy as np
import logging

logger = logging.getLogger(__name__)

class EmbeddingService:
    def __init__(self):
        self._model = None  # Lazy loading
        logger.info("EmbeddingService initialized (model will load on first use)")
    
    @property
    def model(self):
        """Lazy load model only when needed"""
        if self._model is None:
            logger.info("Loading Sentence Transformer model (first use)...")
            # Use smaller, faster model for free tier
            self._model = SentenceTransformer('all-MiniLM-L6-v2')
            logger.info("Model loaded successfully")
        return self._model

    def generate_embeddings(self, text:str) -> List[float]:
        embedding= self.model.encode(text)
        return embedding.tolist()
    
    def generate_embeddings_batch(self, texts:List[str]) -> List[List[float]]:
        embeddings = self.model.encode(texts)
        return  embeddings.tolist()
embedding_service= EmbeddingService()    