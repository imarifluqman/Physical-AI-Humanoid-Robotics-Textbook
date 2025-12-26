"""
Cohere API integration module for the book content ingestion system.
Generates vector embeddings for text content.
"""
import cohere
from typing import List, Optional
from .models import Chunk, EmbeddingRecord
from .logging import logger
from .errors import APIError, retry_with_backoff, handle_api_call_with_retry
import uuid


class CohereEmbedder:
    """
    Module to integrate with Cohere API for generating embeddings.
    """
    def __init__(self, api_key: str, model: str = "embed-english-v3.0"):
        self.client = cohere.Client(api_key)
        self.model = model

    @retry_with_backoff(max_retries=3, base_delay=1.0, exceptions=(APIError,))
    def generate_embeddings(self, chunks: List[Chunk]) -> List[EmbeddingRecord]:
        """
        Generate embeddings for a list of text chunks.

        Args:
            chunks: List of text chunks to embed

        Returns:
            List of EmbeddingRecord objects with vectors and metadata
        """
        if not chunks:
            return []

        # Extract just the text content for embedding
        texts = [chunk.text for chunk in chunks]

        try:
            # Generate embeddings using Cohere API
            response = self.client.embed(
                texts=texts,
                model=self.model,
                input_type="search_document"  # Optimize for search use case
            )

            # Verify the response has the expected structure
            if not hasattr(response, 'embeddings') or not response.embeddings:
                raise APIError("Cohere API response does not contain embeddings")

            # Create EmbeddingRecord objects from the response
            embedding_records = []
            for i, embedding_vector in enumerate(response.embeddings):
                chunk = chunks[i]

                # Validate that the embedding vector has the expected length
                if not embedding_vector or len(embedding_vector) == 0:
                    raise APIError(f"Received empty embedding vector for chunk {i}")

                record = EmbeddingRecord(
                    id=str(uuid.uuid4()),  # Generate unique ID
                    vector=embedding_vector,
                    text=chunk.text,
                    module=chunk.module,
                    chapter=chunk.chapter,
                    chunk_index=chunk.chunk_index,
                    source_file=chunk.source_file
                )
                embedding_records.append(record)

            logger.log_success(f"Generated {len(embedding_records)} embeddings for {len(chunks)} chunks")
            return embedding_records

        except Exception as e:
            error_msg = f"Failed to generate embeddings with Cohere API: {str(e)}"
            logger.log_error(error_msg)
            raise APIError(error_msg) from e

    @retry_with_backoff(max_retries=3, base_delay=1.0, exceptions=(APIError,))
    def generate_single_embedding(self, text: str, module: str, chapter: str,
                                chunk_index: Optional[int] = None,
                                source_file: str = "") -> EmbeddingRecord:
        """
        Generate a single embedding for a text.

        Args:
            text: Text to embed
            module: Module identifier
            chapter: Chapter identifier
            chunk_index: Chunk index if text was split
            source_file: Path to source file

        Returns:
            EmbeddingRecord object with vector and metadata
        """
        try:
            response = self.client.embed(
                texts=[text],
                model=self.model,
                input_type="search_document"
            )

            if not response.embeddings or len(response.embeddings) == 0:
                raise APIError("Cohere API returned no embeddings")

            embedding_vector = response.embeddings[0]

            if not embedding_vector or len(embedding_vector) == 0:
                raise APIError("Received empty embedding vector")

            record = EmbeddingRecord(
                id=str(uuid.uuid4()),
                vector=embedding_vector,
                text=text,
                module=module,
                chapter=chapter,
                chunk_index=chunk_index,
                source_file=source_file
            )

            logger.log_info(f"Generated single embedding for: {module}/{chapter}")
            return record

        except Exception as e:
            error_msg = f"Failed to generate single embedding with Cohere API: {str(e)}"
            logger.log_error(error_msg)
            raise APIError(error_msg) from e

    def validate_api_connection(self) -> bool:
        """
        Validate that the Cohere API connection is working.

        Returns:
            True if connection is valid, False otherwise
        """
        try:
            # Test with a simple embedding request
            test_text = ["test"]
            response = self.client.embed(
                texts=test_text,
                model=self.model,
                input_type="search_document"
            )
            return len(response.embeddings) > 0
        except Exception as e:
            logger.log_error(f"Cohere API connection validation failed: {str(e)}")
            return False