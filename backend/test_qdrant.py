#!/usr/bin/env python3
"""
Test script to directly test Qdrant retrieval functionality
"""
import asyncio
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from agent.services.qdrant_service import qdrant_service

async def test_qdrant_retrieval():
    """Test Qdrant retrieval directly"""
    print("Testing Qdrant retrieval directly...")

    # Test query
    test_query = "What is Physical AI?"

    try:
        # Retrieve content directly using the service
        results = qdrant_service.retrieve_content_by_text(test_query, top_k=5)

        print(f"Found {len(results)} results for query: '{test_query}'")

        for i, result in enumerate(results):
            print(f"\nResult {i+1}:")
            print(f"  Module: {result.module}")
            print(f"  Chapter: {result.chapter}")
            print(f"  Similarity: {result.similarity_score}")
            print(f"  Content preview: {result.text_content[:200]}...")

    except Exception as e:
        print(f"Error during Qdrant retrieval: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_qdrant_retrieval())