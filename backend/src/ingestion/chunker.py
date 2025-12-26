"""
Text chunking module for the book content ingestion system.
Splits large text content into smaller chunks for better embeddings.
"""
import re
from typing import List
from .models import Chunk


class TextChunker:
    """
    Module to split large text content into smaller chunks.
    """
    def __init__(self, chunk_size: int = 512):
        """
        Initialize the chunker with a specific chunk size.

        Args:
            chunk_size: Maximum size of text chunks in tokens (approximately characters for simplicity)
        """
        self.chunk_size = chunk_size

    def chunk_text(self, text: str, module: str, chapter: str,
                   source_file: str = "", overlap: int = 50) -> List[Chunk]:
        """
        Split text into chunks of approximately chunk_size characters.

        Args:
            text: Text to be chunked
            module: Module identifier for the text
            chapter: Chapter identifier for the text
            source_file: Source file path
            overlap: Number of characters to overlap between chunks for context

        Returns:
            List of Chunk objects
        """
        if len(text) <= self.chunk_size:
            # If text is smaller than chunk size, return as single chunk
            return [Chunk(
                text=text,
                module=module,
                chapter=chapter,
                chunk_index=0,
                source_file=source_file
            )]

        chunks = []
        start_idx = 0
        chunk_index = 0

        while start_idx < len(text):
            # Determine the end index for this chunk
            end_idx = start_idx + self.chunk_size

            # If this is not the last chunk, try to break at a sentence or paragraph boundary
            if end_idx < len(text):
                # Look for a good breaking point near the end of the chunk
                search_start = end_idx - overlap
                break_point = end_idx

                # Look for paragraph breaks first
                for i in range(min(end_idx, len(text)) - 1, search_start - 1, -1):
                    if text[i] in ['\n', '\r'] and i > start_idx + 50:  # Ensure minimum chunk size
                        if i + 1 < len(text) and text[i + 1] in ['\n', '\r']:  # Paragraph break
                            break_point = i + 2
                            break
                        elif text[i] in ['\n', '\r']:  # Single line break
                            break_point = i + 1
                            break

                # If no paragraph break found, look for sentence ends
                if break_point == end_idx:
                    for i in range(min(end_idx, len(text)) - 1, search_start - 1, -1):
                        if text[i] in ['.', '!', '?'] and i > start_idx + 50:
                            break_point = i + 1
                            break

                # If still no good break point found, look for word boundaries
                if break_point == end_idx:
                    for i in range(min(end_idx, len(text)) - 1, search_start - 1, -1):
                        if text[i] in [' ', '\t'] and i > start_idx + 50:
                            break_point = i + 1
                            break

                end_idx = break_point

            # Extract the chunk text
            chunk_text = text[start_idx:end_idx].strip()

            # Only add non-empty chunks
            if chunk_text:
                chunks.append(Chunk(
                    text=chunk_text,
                    module=module,
                    chapter=chapter,
                    chunk_index=chunk_index,
                    source_file=source_file
                ))
                chunk_index += 1

            # Move to the next position
            start_idx = end_idx - overlap if end_idx < len(text) else end_idx

            # Prevent infinite loops in case of issues
            if start_idx <= start_idx:
                break

        return chunks

    def chunk_by_sentences(self, text: str, module: str, chapter: str,
                          source_file: str = "", max_chunk_size: int = 1000) -> List[Chunk]:
        """
        Split text into chunks by sentences, respecting a maximum chunk size.

        Args:
            text: Text to be chunked
            module: Module identifier for the text
            chapter: Chapter identifier for the text
            source_file: Source file path
            max_chunk_size: Maximum size of chunks in characters

        Returns:
            List of Chunk objects
        """
        # Split text into sentences
        sentences = re.split(r'(?<=[.!?])\s+', text)

        chunks = []
        current_chunk = ""
        chunk_index = 0

        for sentence in sentences:
            # If adding this sentence would exceed the max size
            if len(current_chunk) + len(sentence) > max_chunk_size and current_chunk:
                # Save the current chunk
                chunks.append(Chunk(
                    text=current_chunk.strip(),
                    module=module,
                    chapter=chapter,
                    chunk_index=chunk_index,
                    source_file=source_file
                ))
                chunk_index += 1
                current_chunk = sentence + " "
            else:
                current_chunk += sentence + " "

        # Add the last chunk if it has content
        if current_chunk.strip():
            chunks.append(Chunk(
                text=current_chunk.strip(),
                module=module,
                chapter=chapter,
                chunk_index=chunk_index,
                source_file=source_file
            ))

        return chunks