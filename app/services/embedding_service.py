from sentence_transformers import SentenceTransformer
from typing import List

import numpy as np

class EmbeddingService:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')

    def generate_embeddings(self, text:str) -> List[float]:
        embedding= self.model.encode(text)
        return embedding.tolist()
    
    def generate_embeddings_batch(self, texts:List[str]) -> List[List[float]]:
        embeddings = self.model.encode(texts)
        return  embeddings.tolist()
embedding_service= EmbeddingService()    