"""
Qdrant database integration module for the book content ingestion system.
Uploads embeddings to the Qdrant vector database.
"""
from qdrant_client import QdrantClient
from qdrant_client.http import models
from typing import List, Optional
from .models import EmbeddingRecord
from .logging import logger
from .errors import DatabaseError, retry_with_backoff
import uuid


class QdrantUploader:
    """
    Module to handle Qdrant database integration for storing embeddings.
    """
    def __init__(self, url: str, api_key: Optional[str] = None, collection_name: str = "book_embeddings"):
        self.client = QdrantClient(url=url, api_key=api_key, prefer_grpc=False)
        self.collection_name = collection_name

    def create_collection(self, vector_size: int = 1024) -> None:
        """
        Create a collection in Qdrant if it doesn't exist.

        Args:
            vector_size: Size of the embedding vectors (default 1024 for Cohere embed-english-v3.0)
        """
        try:
            # Check if collection already exists
            collections = self.client.get_collections()
            collection_exists = any(col.name == self.collection_name for col in collections.collections)

            if not collection_exists:
                # Create collection with appropriate vector configuration
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=models.VectorParams(
                        size=vector_size,
                        distance=models.Distance.COSINE  # Cosine distance is good for text embeddings
                    )
                )
                logger.log_success(f"Created Qdrant collection: {self.collection_name}")
            else:
                logger.log_info(f"Qdrant collection already exists: {self.collection_name}")

            # Create payload index for efficient filtering by module and chapter
            self.client.create_payload_index(
                collection_name=self.collection_name,
                field_name="module",
                field_schema=models.PayloadSchemaType.KEYWORD
            )
            self.client.create_payload_index(
                collection_name=self.collection_name,
                field_name="chapter",
                field_schema=models.PayloadSchemaType.KEYWORD
            )
            logger.log_info("Created payload indexes for efficient filtering")

        except Exception as e:
            error_msg = f"Failed to create or verify Qdrant collection: {str(e)}"
            logger.log_error(error_msg)
            raise DatabaseError(error_msg) from e

    @retry_with_backoff(max_retries=3, base_delay=1.0, exceptions=(DatabaseError,))
    def upload_embeddings(self, embeddings: List[EmbeddingRecord], batch_size: int = 10) -> None:
        """
        Upload a list of embedding records to Qdrant.

        Args:
            embeddings: List of embedding records to upload
            batch_size: Number of records to upload in each batch
        """
        if not embeddings:
            logger.log_info("No embeddings to upload")
            return

        # Create collection if it doesn't exist (using the vector size from first embedding)
        if len(embeddings) > 0:
            self.create_collection(vector_size=len(embeddings[0].vector))

        total_embeddings = len(embeddings)
        uploaded_count = 0

        # Process in batches
        for i in range(0, total_embeddings, batch_size):
            batch = embeddings[i:i + batch_size]

            try:
                # Prepare points for insertion
                points = []
                for record in batch:
                    point = models.PointStruct(
                        id=record.id,
                        vector=record.vector,
                        payload={
                            "text": record.text,
                            "module": record.module,
                            "chapter": record.chapter,
                            "chunk_index": record.chunk_index,
                            "source_file": record.source_file,
                            "created_at": record.created_at.isoformat() if record.created_at else None
                        }
                    )
                    points.append(point)

                # Upload the batch
                self.client.upsert(
                    collection_name=self.collection_name,
                    points=points
                )

                uploaded_count += len(batch)
                logger.log_info(f"Uploaded batch: {uploaded_count}/{total_embeddings} embeddings")

            except Exception as e:
                error_msg = f"Failed to upload batch starting at index {i}: {str(e)}"
                logger.log_error(error_msg)
                raise DatabaseError(error_msg) from e

        logger.log_success(f"Successfully uploaded {uploaded_count} embeddings to collection '{self.collection_name}'")

    @retry_with_backoff(max_retries=3, base_delay=1.0, exceptions=(DatabaseError,))
    def upload_single_embedding(self, embedding: EmbeddingRecord) -> None:
        """
        Upload a single embedding record to Qdrant.

        Args:
            embedding: Single embedding record to upload
        """
        try:
            point = models.PointStruct(
                id=embedding.id,
                vector=embedding.vector,
                payload={
                    "text": embedding.text,
                    "module": embedding.module,
                    "chapter": embedding.chapter,
                    "chunk_index": embedding.chunk_index,
                    "source_file": embedding.source_file,
                    "created_at": embedding.created_at.isoformat() if embedding.created_at else None
                }
            )

            self.client.upsert(
                collection_name=self.collection_name,
                points=[point]
            )

            logger.log_info(f"Uploaded single embedding: {embedding.module}/{embedding.chapter}")

        except Exception as e:
            error_msg = f"Failed to upload single embedding: {str(e)}"
            logger.log_error(error_msg)
            raise DatabaseError(error_msg) from e

    def count_embeddings(self) -> int:
        """
        Count the number of embeddings in the collection.

        Returns:
            Number of embeddings in the collection
        """
        try:
            count_result = self.client.count(
                collection_name=self.collection_name
            )
            return count_result.count
        except Exception as e:
            error_msg = f"Failed to count embeddings in collection: {str(e)}"
            logger.log_error(error_msg)
            raise DatabaseError(error_msg) from e

    def search_similar(self, query_vector: List[float], limit: int = 10,
                      module_filter: Optional[str] = None,
                      chapter_filter: Optional[str] = None) -> List[EmbeddingRecord]:
        """
        Search for similar embeddings in the collection.

        Args:
            query_vector: Vector to search for similarity
            limit: Maximum number of results to return
            module_filter: Optional filter for specific module
            chapter_filter: Optional filter for specific chapter

        Returns:
            List of similar embedding records
        """
        try:
            # Build filters if needed
            filters = None
            if module_filter or chapter_filter:
                filter_conditions = []
                if module_filter:
                    filter_conditions.append(
                        models.FieldCondition(
                            key="module",
                            match=models.MatchValue(value=module_filter)
                        )
                    )
                if chapter_filter:
                    filter_conditions.append(
                        models.FieldCondition(
                            key="chapter",
                            match=models.MatchValue(value=chapter_filter)
                        )
                    )

                if filter_conditions:
                    filters = models.Filter(
                        must=filter_conditions
                    )

            # Perform search
            results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_vector,
                query_filter=filters,
                limit=limit
            )

            # Convert results to EmbeddingRecord objects
            embedding_records = []
            for result in results:
                record = EmbeddingRecord(
                    id=result.id,
                    vector=result.vector if result.vector else [],
                    text=result.payload.get("text", ""),
                    module=result.payload.get("module", ""),
                    chapter=result.payload.get("chapter", ""),
                    chunk_index=result.payload.get("chunk_index"),
                    source_file=result.payload.get("source_file", ""),
                )
                embedding_records.append(record)

            return embedding_records

        except Exception as e:
            error_msg = f"Failed to search for similar embeddings: {str(e)}"
            logger.log_error(error_msg)
            raise DatabaseError(error_msg) from e