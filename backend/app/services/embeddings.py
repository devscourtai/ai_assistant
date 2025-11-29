"""
Embedding service using HuggingFace (free, local embeddings).
"""

import os
from typing import List
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings

load_dotenv()


class EmbeddingService:
    """
    Generate embeddings using HuggingFace sentence-transformers.
    These run locally and don't require an API key!
    """

    def __init__(self, model: str = "sentence-transformers/all-MiniLM-L6-v2"):
        """
        Initialize embedding service with HuggingFace model.

        Default model: all-MiniLM-L6-v2
        - Fast and efficient
        - 384 dimensions
        - Good quality for most tasks
        - Runs locally (no API key needed!)
        """

        # Use HuggingFace embeddings (local, free)
        self.embeddings = HuggingFaceEmbeddings(
            model_name=model,
            model_kwargs={'device': 'cpu'},  # Use 'mps' for Mac GPU if available
            encode_kwargs={'normalize_embeddings': True}
        )

        self.model = model

    def embed_text(self, text: str) -> List[float]:
        """Embed a single text."""
        return self.embeddings.embed_query(text)

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Embed multiple texts."""
        return self.embeddings.embed_documents(texts)

    def get_embedding_dimension(self) -> int:
        """Return dimension based on model."""
        if "all-MiniLM-L6-v2" in self.model:
            return 384
        if "all-mpnet-base-v2" in self.model:
            return 768
        # Default for most sentence-transformers models
        return 384


# Singleton
_embedding_service = None


def get_embedding_service() -> EmbeddingService:
    global _embedding_service
    if _embedding_service is None:
        _embedding_service = EmbeddingService()
    return _embedding_service