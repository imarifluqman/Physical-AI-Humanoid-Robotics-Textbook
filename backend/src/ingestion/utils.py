"""
Utility functions for the book content ingestion system.
"""
import os
import glob
from pathlib import Path
from typing import List, Tuple
import re


def find_markdown_files(docs_path: str) -> List[str]:
    """
    Find all markdown files in the documentation directory structure.

    Args:
        docs_path: Path to the documentation directory

    Returns:
        List of paths to markdown files found in the directory structure
    """
    pattern = os.path.join(docs_path, "**", "*.md")
    md_files = glob.glob(pattern, recursive=True)

    # Filter out files that don't match the module/chapter pattern
    valid_files = []
    for file_path in md_files:
        # Check if the file is in a module subdirectory
        rel_path = os.path.relpath(file_path, docs_path)
        path_parts = rel_path.split(os.sep)

        # Should have at least module/chapter.md structure
        if len(path_parts) >= 2 and path_parts[0].startswith('module'):
            valid_files.append(file_path)

    return sorted(valid_files)


def extract_module_chapter(file_path: str) -> Tuple[str, str]:
    """
    Extract module and chapter names from a file path.

    Args:
        file_path: Path to a markdown file

    Returns:
        Tuple of (module_name, chapter_name)
    """
    path = Path(file_path)
    # Get the relative path from docs directory
    parts = path.parent.parts

    # Find the module part (directory that starts with 'module')
    module_part = ""
    chapter_part = path.stem  # filename without extension

    for part in reversed(parts):
        if part.startswith('module'):
            module_part = part
            break

    return module_part, chapter_part


def clean_markdown_content(content: str) -> str:
    """
    Clean markdown content by removing metadata, comments, and other non-content elements.

    Args:
        content: Raw markdown content

    Returns:
        Cleaned content with non-content elements removed
    """
    # Remove YAML frontmatter if present (between ---)
    content = re.sub(r'^---\s*\n.*?\n---\s*\n', '', content, flags=re.DOTALL | re.MULTILINE)

    # Remove HTML comments
    content = re.sub(r'<!--.*?-->', '', content, flags=re.DOTALL)

    # Remove extra whitespace while preserving paragraph structure
    content = re.sub(r'\n\s+\n', '\n\n', content)  # Multiple blank lines to single
    content = content.strip()

    return content


def read_file_with_encoding(file_path: str) -> str:
    """
    Read a file with proper encoding handling.

    Args:
        file_path: Path to the file to read

    Returns:
        File content as string

    Raises:
        UnicodeDecodeError: If the file cannot be decoded with common encodings
    """
    encodings = ['utf-8', 'utf-8-sig', 'latin-1', 'cp1252']

    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                return f.read()
        except UnicodeDecodeError:
            continue

    # If all encodings fail, raise an error
    raise UnicodeDecodeError(f"Could not decode file {file_path} with any of the attempted encodings")