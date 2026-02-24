import requests
from typing import List
import logging
import os

logger = logging.getLogger(__name__)

class HuggingFaceEmbeddingService:
    """
    Alternative embedding service using HuggingFace Inference API
    FREE tier: 30,000 requests/month
    No local model = No memory usage!
    """
    def __init__(self):
        self.api_url = "https://api-inference.huggingface.co/pipeline/feature-extraction/sentence-transformers/all-MiniLM-L6-v2"
        self.headers = {"Authorization": f"Bearer {os.getenv('HUGGINGFACE_API_KEY', '')}"}
        logger.info("HuggingFace Embedding Service initialized (API-based, no local model)")
    
    def generate_embeddings(self, text: str) -> List[float]:
        """Generate embeddings via API call"""
        try:
            response = requests.post(
                self.api_url,
                headers=self.headers,
                json={"inputs": text, "options": {"wait_for_model": True}},
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"HuggingFace API error: {e}")
            raise
    
    def generate_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for multiple texts"""
        try:
            response = requests.post(
                self.api_url,
                headers=self.headers,
                json={"inputs": texts, "options": {"wait_for_model": True}},
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"HuggingFace API batch error: {e}")
            raise

# Use this instead of local model for free tier
# embedding_service = HuggingFaceEmbeddingService()
