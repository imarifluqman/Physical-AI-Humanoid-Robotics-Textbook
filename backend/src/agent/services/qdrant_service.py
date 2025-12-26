import os
from typing import List, Optional, Dict, Any
from qdrant_client import QdrantClient
from qdrant_client.http import models
from openai import OpenAI
from ..models.query_models import RetrievedContent
from ..exceptions import ContentRetrievalException, QdrantConnectionException
from dotenv import load_dotenv
import logging

load_dotenv()

logger = logging.getLogger("agent")

class QdrantService:
    """
    Service class for interacting with Qdrant vector database
    """

    def __init__(self):
        self.collection_name = os.getenv("QDRANT_COLLECTION_NAME", "book_embeddings")
        self.default_similarity_threshold = 0.3  # Default threshold

        # Initialize Qdrant client - check for remote URL first, then fall back to local
        try:
            qdrant_url = os.getenv("QDRANT_URL")
            qdrant_api_key = os.getenv("QDRANT_API_KEY")

            if qdrant_url and qdrant_api_key:
                # Use remote Qdrant instance
                self.client = QdrantClient(
                    url=qdrant_url,
                    api_key=qdrant_api_key
                )
                logger.info(f"Connected to remote Qdrant at {qdrant_url}")
            else:
                # Fall back to local Qdrant
                self.host = os.getenv("QDRANT_HOST", "localhost")
                self.port = int(os.getenv("QDRANT_PORT", 6333))
                self.client = QdrantClient(
                    host=self.host,
                    port=self.port
                )
                logger.info(f"Connected to local Qdrant at {self.host}:{self.port}")
        except Exception as e:
            logger.error(f"Failed to connect to Qdrant: {e}")
            if qdrant_url and qdrant_api_key:
                raise QdrantConnectionException(f"Failed to connect to remote Qdrant at {qdrant_url}")
            else:
                raise QdrantConnectionException(f"Failed to connect to local Qdrant at {self.host}:{self.port}")

    def get_client(self) -> QdrantClient:
        """
        Returns the Qdrant client instance
        """
        return self.client

    def check_connection(self) -> bool:
        """
        Check if connection to Qdrant is successful
        """
        try:
            # Try to get collections to verify connection
            self.client.get_collections()
            return True
        except Exception as e:
            logger.error(f"Qdrant connection check failed: {e}")
            return False

    def search_content(self, query_vector: List[float], top_k: int = 5, metadata_filter: Optional[Dict] = None,
                      similarity_threshold: Optional[float] = None) -> List[RetrievedContent]:
        """
        Search for content in Qdrant based on query vector
        """
        try:
            # Prepare filters if provided
            qdrant_filter = None
            if metadata_filter:
                filter_conditions = []
                for key, value in metadata_filter.items():
                    filter_conditions.append(
                        models.FieldCondition(
                            key=f"metadata.{key}",
                            match=models.MatchValue(value=value)
                        )
                    )

                if filter_conditions:
                    qdrant_filter = models.Filter(
                        must=filter_conditions
                    )

            # Perform vector search with optional filtering
            search_results = self.client.query_points(
                collection_name=self.collection_name,
                query=query_vector,
                limit=top_k,
                query_filter=qdrant_filter
            ).points

            results = []
            for result in search_results:
                # Apply similarity threshold if specified
                if similarity_threshold is not None and result.score < similarity_threshold:
                    continue  # Skip results below threshold

                payload = result.payload
                retrieved_content = RetrievedContent(
                    content_id=str(result.id),
                    text_content=payload.get("text", ""),  # Changed from "text_content" to "text" to match ingestion
                    module=payload.get("module", ""),
                    chapter=payload.get("chapter", ""),
                    section=payload.get("section"),
                    similarity_score=result.score,
                    metadata=payload.get("metadata", {})
                )
                results.append(retrieved_content)

            logger.info(f"Successfully retrieved {len(results)} content items from Qdrant (threshold={similarity_threshold})")
            return results
        except Exception as e:
            logger.error(f"Error searching content in Qdrant: {e}")
            raise ContentRetrievalException(f"Error searching content in Qdrant: {str(e)}")

    def set_similarity_threshold(self, threshold: float) -> bool:
        """
        Set a default similarity threshold for content retrieval
        """
        if 0 <= threshold <= 1:
            self.default_similarity_threshold = threshold
            return True
        return False

    def get_similarity_score(self, content1: str, content2: str) -> float:
        """
        Calculate similarity score between two content strings
        This is a simple implementation; in production, you might use more sophisticated methods
        """
        # Simple word overlap similarity calculation
        words1 = set(content1.lower().split())
        words2 = set(content2.lower().split())

        if not words1 and not words2:
            return 1.0  # Both empty, perfectly similar
        if not words1 or not words2:
            return 0.0  # One empty, no similarity

        intersection = words1.intersection(words2)
        union = words1.union(words2)

        return len(intersection) / len(union)  # Jaccard similarity

    def get_content_by_id(self, content_id: str) -> Optional[RetrievedContent]:
        """
        Retrieve specific content by its ID
        """
        try:
            records = self.client.retrieve(
                collection_name=self.collection_name,
                ids=[content_id]
            )

            if records:
                record = records[0]
                payload = record.payload
                retrieved_content = RetrievedContent(
                    content_id=str(record.id),
                    text_content=payload.get("text", ""),  # Changed from "text_content" to "text" to match ingestion
                    module=payload.get("module", ""),
                    chapter=payload.get("chapter", ""),
                    section=payload.get("section"),
                    similarity_score=1.0,  # Exact match
                    metadata=payload.get("metadata", {})
                )
                logger.info(f"Successfully retrieved content by ID: {content_id}")
                return retrieved_content

            logger.warning(f"No content found with ID: {content_id}")
            return None
        except Exception as e:
            logger.error(f"Error retrieving content by ID from Qdrant: {e}")
            raise ContentRetrievalException(f"Error retrieving content by ID: {str(e)}")

    def retrieve_content_by_text(self, query_text: str, top_k: int = 5, metadata_filter: Optional[Dict] = None) -> List[RetrievedContent]:
        """
        Retrieve content based on text query by converting to embeddings and searching
        This is the main function for content retrieval that will be used by the agent
        """
        try:
            # Import here to avoid circular dependencies if needed
            import cohere
            client = cohere.Client(api_key=os.getenv("COHERE_API_KEY"))

            # Get embedding for the query text using Cohere
            response = client.embed(
                texts=[query_text],
                model="embed-english-v3.0",  # Using Cohere's free embedding model
                input_type="search_query"  # Specify this is a search query
            )
            query_vector = response.embeddings[0]  # Get the first embedding

            # Search for similar content using the embedding vector
            return self.search_content(query_vector, top_k, metadata_filter)
        except Exception as e:
            logger.error(f"Error retrieving content by text: {e}")
            raise ContentRetrievalException(f"Error retrieving content by text: {str(e)}")

    def retrieve_content_by_text_with_metadata_filter(self, query_text: str, top_k: int = 5,
                                                      module_filter: Optional[str] = None,
                                                      chapter_filter: Optional[str] = None,
                                                      metadata_filters: Optional[Dict] = None) -> List[RetrievedContent]:
        """
        Enhanced retrieval function with specific metadata filtering capabilities
        """
        try:
            # Prepare metadata filter
            combined_filters = {}

            if metadata_filters:
                combined_filters.update(metadata_filters)

            if module_filter:
                combined_filters["module"] = module_filter

            if chapter_filter:
                combined_filters["chapter"] = chapter_filter

            # Import here to avoid circular dependencies if needed
            from openai import OpenAI
            client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

            # Get embedding for the query text
            response = client.embeddings.create(
                input=query_text,
                model="text-embedding-ada-002"
            )
            query_vector = response.data[0].embedding

            # Search for similar content using the embedding vector with filters
            return self.search_content(query_vector, top_k, combined_filters if combined_filters else None)
        except Exception as e:
            logger.error(f"Error retrieving content by text with metadata filter: {e}")
            raise ContentRetrievalException(f"Error retrieving content by text with metadata filter: {str(e)}")

    def get_all_modules(self) -> List[str]:
        """
        Get all unique modules in the collection
        """
        try:
            # Get all records and extract unique modules
            records, _ = self.client.scroll(
                collection_name=self.collection_name,
                limit=10000,  # Adjust as needed
                with_payload=True
            )

            modules = set()
            for record in records:
                module = record.payload.get("module")
                if module:
                    modules.add(module)

            logger.info(f"Retrieved {len(modules)} unique modules from Qdrant")
            return list(modules)
        except Exception as e:
            logger.error(f"Error getting modules from Qdrant: {e}")
            raise ContentRetrievalException(f"Error getting modules: {str(e)}")


# Singleton instance
qdrant_service = QdrantService()