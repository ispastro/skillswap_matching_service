from sentence_transformers import SentenceTransformer
from typing import List
import numpy as np
import logging

logger = logging.getLogger(__name__)

class EmbeddingService:
    def __init__(self):
        logger.info("Loading Sentence Transformer model...")
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        logger.info("Model loaded successfully")

    def generate_embeddings(self, text:str) -> List[float]:
        embedding= self.model.encode(text)
        return embedding.tolist()
    
    def generate_embeddings_batch(self, texts:List[str]) -> List[List[float]]:
        embeddings = self.model.encode(texts)
        return  embeddings.tolist()
embedding_service= EmbeddingService()    