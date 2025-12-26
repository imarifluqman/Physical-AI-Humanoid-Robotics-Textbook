"""
File reader module for the book content ingestion system.
Traverses the /docs directory structure and reads book content.
"""
from typing import List, Tuple
import os
from .models import Chunk
from .utils import find_markdown_files, extract_module_chapter, clean_markdown_content, read_file_with_encoding
from .logging import logger
from .errors import FileReadError


class FileReader:
    """
    Module to read book content from the /docs directory structure.
    """
    def __init__(self, docs_path: str):
        self.docs_path = docs_path

    def get_all_files(self) -> List[str]:
        """
        Get all markdown files from the documentation directory.

        Returns:
            List of paths to markdown files
        """
        logger.log_info(f"Searching for markdown files in: {self.docs_path}")
        files = find_markdown_files(self.docs_path)
        logger.log_success(f"Found {len(files)} markdown files")
        return files

    def read_file(self, file_path: str) -> str:
        """
        Read content from a single file.

        Args:
            file_path: Path to the file to read

        Returns:
            Content of the file as a string

        Raises:
            FileReadError: If the file cannot be read
        """
        try:
            content = read_file_with_encoding(file_path)
            logger.log_info(f"Successfully read file: {file_path}")
            return content
        except Exception as e:
            error_msg = f"Failed to read file {file_path}: {str(e)}"
            logger.log_error(error_msg)
            raise FileReadError(error_msg) from e

    def read_all_modules_and_chapters(self) -> List[Chunk]:
        """
        Read all modules and chapters from the documentation directory.

        Returns:
            List of Chunks representing the content
        """
        files = self.get_all_files()
        chunks = []

        for file_path in files:
            try:
                module, chapter = extract_module_chapter(file_path)
                content = self.read_file(file_path)
                cleaned_content = clean_markdown_content(content)

                # Create a chunk for the entire file content
                chunk = Chunk(
                    text=cleaned_content,
                    module=module,
                    chapter=chapter,
                    chunk_index=0,
                    source_file=file_path
                )
                chunks.append(chunk)
                logger.log_info(f"Processed: {module}/{chapter}")

            except Exception as e:
                logger.log_error(f"Failed to process file {file_path}: {str(e)}")
                # Continue processing other files
                continue

        logger.log_success(f"Successfully processed {len(chunks)} chunks from {len(files)} files")
        return chunks

    def get_module_structure(self) -> dict:
        """
        Get the structure of modules and chapters.

        Returns:
            Dictionary with modules as keys and lists of chapters as values
        """
        files = self.get_all_files()
        structure = {}

        for file_path in files:
            module, chapter = extract_module_chapter(file_path)
            if module not in structure:
                structure[module] = []
            structure[module].append(chapter)

        return structure