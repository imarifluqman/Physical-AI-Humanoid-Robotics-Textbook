"""
Main ingestion workflow orchestrator for the book content ingestion system.
"""
import sys
import time
from typing import List
from .config import load_config, validate_config
from .reader import FileReader
from .embedder import CohereEmbedder
from .uploader import QdrantUploader
from .chunker import TextChunker
from .models import Chunk, EmbeddingRecord
from .logging import logger, IngestionLogger
from .errors import IngestionError, ConfigurationError
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn


def main():
    """
    Main entry point for the book content ingestion process.
    """
    start_time = time.time()
    logger.log_info("Starting book content ingestion process")

    try:
        # Load and validate configuration
        config = load_config()
        validate_config(config)
        logger.log_success("Configuration loaded and validated successfully")

        # Initialize components
        file_reader = FileReader(config.frontend_docs_path)
        embedder = CohereEmbedder(config.cohere_api_key)
        uploader = QdrantUploader(
            url=config.qdrant_url,
            api_key=config.qdrant_api_key,
            collection_name=config.collection_name
        )
        chunker = TextChunker(chunk_size=config.chunk_size)

        # Verify API connections
        logger.log_info("Verifying API connections...")
        if not embedder.validate_api_connection():
            raise IngestionError("Cohere API connection validation failed")
        logger.log_success("Cohere API connection validated")

        # Read all files from the documentation directory
        logger.log_info("Reading book content from documentation directory...")
        all_chunks = file_reader.read_all_modules_and_chapters()

        if not all_chunks:
            logger.log_warning("No content found to process")
            return

        logger.log_info(f"Found {len(all_chunks)} content chunks to process")

        # Process chunks in batches for better memory management
        total_processed = 0
        total_embeddings = 0

        with logger.create_progress_tracker() as progress:
            overall_task = progress.add_task(
                "[green]Processing all content...",
                total=len(all_chunks)
            )

            # Process in batches
            batch_size = config.batch_size
            for i in range(0, len(all_chunks), batch_size):
                batch = all_chunks[i:i + batch_size]

                # If any chunk is too large, split it into smaller pieces
                processed_batch_chunks = []
                for chunk in batch:
                    if len(chunk.text) > config.chunk_size:
                        # Split large chunks into smaller ones
                        sub_chunks = chunker.chunk_text(
                            chunk.text,
                            module=chunk.module,
                            chapter=chunk.chapter,
                            source_file=chunk.source_file
                        )
                        processed_batch_chunks.extend(sub_chunks)
                    else:
                        # Add the original chunk with proper chunk_index
                        updated_chunk = Chunk(
                            text=chunk.text,
                            module=chunk.module,
                            chapter=chunk.chapter,
                            chunk_index=chunk.chunk_index,
                            source_file=chunk.source_file
                        )
                        processed_batch_chunks.append(updated_chunk)

                # Generate embeddings for the batch
                embedding_records = embedder.generate_embeddings(processed_batch_chunks)

                # Upload embeddings to Qdrant
                uploader.upload_embeddings(embedding_records, batch_size=config.batch_size)

                # Update progress
                total_processed += len(batch)
                total_embeddings += len(embedding_records)
                progress.update(overall_task, advance=len(batch))

                logger.log_info(f"Processed batch: {total_processed}/{len(all_chunks)} files")

        # Log final summary
        logger.log_ingestion_summary(
            total_files=len(all_chunks),
            processed_files=total_processed,
            total_embeddings=total_embeddings,
            start_time=start_time
        )

        logger.log_success("Book content ingestion completed successfully!")

    except ConfigurationError as e:
        logger.log_error(f"Configuration error: {str(e)}")
        sys.exit(1)
    except IngestionError as e:
        logger.log_error(f"Ingestion error: {str(e)}")
        sys.exit(1)
    except Exception as e:
        logger.log_error(f"Unexpected error during ingestion: {str(e)}")
        sys.exit(1)

    total_duration = time.time() - start_time
    logger.log_info(f"Ingestion process completed in {total_duration:.2f} seconds")


def run_ingestion_with_config(config):
    """
    Run the ingestion process with a pre-loaded configuration.
    This function can be called programmatically with a config object.
    """
    start_time = time.time()
    logger.log_info("Starting book content ingestion process")

    try:
        # Initialize components
        file_reader = FileReader(config.frontend_docs_path)
        embedder = CohereEmbedder(config.cohere_api_key)
        uploader = QdrantUploader(
            url=config.qdrant_url,
            api_key=config.qdrant_api_key,
            collection_name=config.collection_name
        )
        chunker = TextChunker(chunk_size=config.chunk_size)

        # Verify API connections
        logger.log_info("Verifying API connections...")
        if not embedder.validate_api_connection():
            raise IngestionError("Cohere API connection validation failed")
        logger.log_success("Cohere API connection validated")

        # Read all files from the documentation directory
        logger.log_info("Reading book content from documentation directory...")
        all_chunks = file_reader.read_all_modules_and_chapters()

        if not all_chunks:
            logger.log_warning("No content found to process")
            return

        logger.log_info(f"Found {len(all_chunks)} content chunks to process")

        # Process chunks in batches for better memory management
        total_processed = 0
        total_embeddings = 0

        with logger.create_progress_tracker() as progress:
            overall_task = progress.add_task(
                "[green]Processing all content...",
                total=len(all_chunks)
            )

            # Process in batches
            batch_size = config.batch_size
            for i in range(0, len(all_chunks), batch_size):
                batch = all_chunks[i:i + batch_size]

                # If any chunk is too large, split it into smaller pieces
                processed_batch_chunks = []
                for chunk in batch:
                    if len(chunk.text) > config.chunk_size:
                        # Split large chunks into smaller ones
                        sub_chunks = chunker.chunk_text(
                            chunk.text,
                            module=chunk.module,
                            chapter=chunk.chapter,
                            source_file=chunk.source_file
                        )
                        processed_batch_chunks.extend(sub_chunks)
                    else:
                        # Add the original chunk with proper chunk_index
                        updated_chunk = Chunk(
                            text=chunk.text,
                            module=chunk.module,
                            chapter=chunk.chapter,
                            chunk_index=chunk.chunk_index,
                            source_file=chunk.source_file
                        )
                        processed_batch_chunks.append(updated_chunk)

                # Generate embeddings for the batch
                embedding_records = embedder.generate_embeddings(processed_batch_chunks)

                # Upload embeddings to Qdrant
                uploader.upload_embeddings(embedding_records, batch_size=config.batch_size)

                # Update progress
                total_processed += len(batch)
                total_embeddings += len(embedding_records)
                progress.update(overall_task, advance=len(batch))

                logger.log_info(f"Processed batch: {total_processed}/{len(all_chunks)} files")

        # Log final summary
        logger.log_ingestion_summary(
            total_files=len(all_chunks),
            processed_files=total_processed,
            total_embeddings=total_embeddings,
            start_time=start_time
        )

        logger.log_success("Book content ingestion completed successfully!")

    except Exception as e:
        logger.log_error(f"Error during ingestion: {str(e)}")
        raise

    total_duration = time.time() - start_time
    logger.log_info(f"Ingestion process completed in {total_duration:.2f} seconds")


if __name__ == "__main__":
    main()