import logging
import uuid
from datetime import datetime
from typing import List, Optional
from openai import OpenAI
import os

from ..config import MODEL_NAME
from ..exceptions import AgentProcessingException, ContentRetrievalException
from ..models.query_models import QueryRequest, QueryResponse, RetrievedContent
from ..services.qdrant_service import qdrant_service

logger = logging.getLogger("agent")


class RetrievalAgent:
    """
    AI Agent that retrieves relevant content from Qdrant and generates responses
    """

    def __init__(self):
        self.qdrant_service = qdrant_service
        # Store the last retrieved content for access after agent run
        self.last_retrieved_content = []

        # Initialize OpenAI client for response generation
        self.openai_client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=os.getenv("OPENROUTER_API_KEY")
            )

    async def process_query(self, query_request: QueryRequest) -> QueryResponse:
        """
        Process a user query by retrieving relevant content and generating a response
        """
        try:
            logger.info(f"Processing query: {query_request.query}")

            # Retrieve content from Qdrant directly
            retrieved_content = qdrant_service.retrieve_content_by_text(
                query_text=query_request.query, top_k=5
            )

            # Check if the retrieved content is relevant to the query by comparing similarity scores
            # If all retrieved items have very low similarity scores or no content was retrieved,
            # it means the query doesn't match book content
            if not retrieved_content or all(item.similarity_score < 0.2 for item in retrieved_content):
                # Query doesn't match book content
                answer = f"Sorry, the query '{query_request.query}' does not match any content in the Physical AI & Humanoid Robotics book. The book covers topics like ROS 2, robotics, AI, Physical AI, humanoid robotics, etc. Please ask questions related to these topics."

                return QueryResponse(
                    response_id=str(uuid.uuid4()),
                    query=query_request.query,
                    answer=answer,
                    retrieved_content=[],
                    confidence=0.0,
                    source_modules=[]
                )

            # Extract source modules from retrieved content
            source_modules = list(set([item.module for item in retrieved_content]))

            # Add provenance tracking information to each retrieved content item
            for item in retrieved_content:
                # Add provenance tracking information to metadata
                if not item.metadata:
                    item.metadata = {}
                item.metadata["retrieval_timestamp"] = datetime.now().isoformat()
                item.metadata["retrieval_query"] = query_request.query[
                    :100
                ]  # First 100 chars of query
                item.metadata["retrieval_agent"] = "QdrantRetrievalAgent"

            # Calculate confidence based on similarity scores
            avg_similarity = (
                sum([item.similarity_score for item in retrieved_content])
                / len(retrieved_content)
                if retrieved_content
                else 0.0
            )

            # Generate detailed answer if we have high-quality content
            high_quality_content = [item for item in retrieved_content if item.similarity_score >= 0.25]

            if high_quality_content:
                content_texts = []
                source_info = []

                # Collect only high-quality content (top 3 most relevant)
                for item in high_quality_content[:3]:
                    if item.text_content:
                        content_texts.append(item.text_content)
                        # Add source information
                        source_detail = f"- Source: Module {item.module}, Chapter {item.chapter}"
                        if item.section:
                            source_detail += f", Section {item.section}"
                        source_detail += f" (Similarity: {item.similarity_score:.2f})"
                        source_info.append(source_detail)

                if content_texts:
                    # Combine the content to create context for the LLM
                    context = "\n\n".join(content_texts)
                    sources_text = "\n".join(source_info)

                    # Create a prompt for OpenAI to generate a detailed explanation
                    prompt = f"""
                    Based on the following content from the Physical AI & Humanoid Robotics book, please provide a detailed explanation about '{query_request.query}':

                    {context}

                    Please explain this concept in detail, as if teaching it to a student. Include key concepts, importance, and practical applications. Then provide the sources where this information can be found in the book.
                    """

                    try:
                        response = self.openai_client.chat.completions.create(
                            model="gpt-3.5-turbo",
                            messages=[{"role": "user", "content": prompt}],
                            temperature=0.3
                        )

                        generated_answer = response.choices[0].message.content
                        answer = f"{generated_answer}"
                    except Exception as e:
                        logger.error(f"Error generating response with OpenAI: {e}")
                        # Fallback to using the raw content if OpenAI fails
                        answer = f"I found relevant content in the book about '{query_request.query}'. Here's what I can tell you based on the retrieved information:\n\n{content_texts[0][:500]}...\n\nSources in book:\n{sources_text}"
                else:
                    answer = "I found relevant content in the book but couldn't extract specific information about your query."
            else:
                # If no high-quality content, don't generate an answer based on poor matches
                answer = f"Sorry, the query '{query_request.query}' does not match any content in the Physical AI & Humanoid Robotics book. The book covers topics like ROS 2, robotics, AI, Physical AI, humanoid robotics, etc. Please ask questions related to these topics."

            response = QueryResponse(
                response_id=str(uuid.uuid4()),
                query=query_request.query,
                answer=answer,
                retrieved_content=retrieved_content,
                confidence=avg_similarity,
                source_modules=source_modules,
            )

            logger.info(
                f"Successfully processed query, returning response with {len(retrieved_content)} content items"
            )
            return response

        except ContentRetrievalException as e:
            logger.error(f"Content retrieval error in agent: {e}")
            raise AgentProcessingException(f"Failed to retrieve content: {str(e)}")
        except Exception as e:
            logger.error(f"Error processing query in agent: {e}")
            raise AgentProcessingException(f"Error processing query: {str(e)}")

    def validate_response(self, response: QueryResponse) -> bool:
        """
        Validate that the response is grounded in the retrieved content
        """
        # Basic validation to ensure response has content
        if not response.answer or len(response.answer.strip()) == 0:
            return False

        # Check that retrieved content exists if there's an answer
        if len(response.retrieved_content) == 0 and len(response.answer) > 0:
            logger.warning(
                "Response has content but no retrieved content - may be hallucinated"
            )
            return False

        return True

    def verify_content_grounding(
        self, query: str, response: str, retrieved_content: List[RetrievedContent]
    ) -> bool:
        """
        Verify that the response is grounded in the retrieved content by checking
        if the key information in the response is supported by the retrieved content
        """
        if not retrieved_content:
            logger.warning("No retrieved content to ground the response")
            return False

        # Convert response to lowercase for comparison
        response_lower = response.lower()

        # Check if key phrases or concepts from retrieved content appear in the response
        content_supports_response = False

        for content_item in retrieved_content:
            # Check if significant portions of the content appear in the response
            content_text_lower = content_item.text_content.lower()

            # Look for overlapping phrases or key terms between content and response
            content_words = set(
                content_text_lower.split()[:50]
            )  # Use first 50 words as representative
            response_words = set(response_lower.split())

            # If there's significant overlap in terms, consider it grounded
            common_words = content_words.intersection(response_words)
            if len(common_words) > 0:  # If there are common words
                content_supports_response = True
                break

        if not content_supports_response:
            logger.warning(
                "Response does not seem to be grounded in the retrieved content"
            )
            return False

        return True

    def calculate_grounding_score(
        self, response: str, retrieved_content: List[RetrievedContent]
    ) -> float:
        """
        Calculate a grounding score based on how well the response aligns with retrieved content
        """
        if not retrieved_content:
            return 0.0

        total_score = 0.0
        content_count = len(retrieved_content)

        for content_item in retrieved_content:
            content_text_lower = content_item.text_content.lower()
            response_lower = response.lower()

            # Count overlapping words
            content_words = set(content_text_lower.split())
            response_words = set(response_lower.split())

            common_words = content_words.intersection(response_words)
            if content_words:  # Avoid division by zero
                overlap_ratio = len(common_words) / len(content_words)
                total_score += (
                    overlap_ratio * content_item.similarity_score
                )  # Weight by similarity

        return total_score / content_count if content_count > 0 else 0.0

    async def get_fallback_response(self, query: str) -> str:
        """
        Generate a fallback response when no relevant content is found
        """
        try:
            return "I couldn't find relevant content in the book to answer your question. Please try rephrasing your query or check other sources."
        except Exception as e:
            logger.error(f"Error generating fallback response: {e}")
            return "I couldn't find relevant content in the book to answer your question. Please try rephrasing your query."


# Singleton instance
retrieval_agent = RetrievalAgent()