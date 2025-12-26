"""
Unit tests for the configuration module.
"""
import os
import tempfile
import pytest
from backend.src.ingestion.config import load_config, validate_config, Config


def test_load_config_success(monkeypatch):
    """Test successful loading of configuration."""
    # Set up environment variables
    monkeypatch.setenv("QDRANT_URL", "https://test.qdrant.tech:6333")
    monkeypatch.setenv("COHERE_API_KEY", "test-api-key")

    # Create a temporary directory for docs path
    with tempfile.TemporaryDirectory() as temp_dir:
        monkeypatch.setenv("FRONTEND_DOCS_PATH", temp_dir)

        config = load_config()

        assert config.qdrant_url == "https://test.qdrant.tech:6333"
        assert config.cohere_api_key == "test-api-key"
        assert config.frontend_docs_path == temp_dir
        assert config.collection_name == "book_embeddings"  # default value
        assert config.chunk_size == 512  # default value
        assert config.batch_size == 10  # default value
        assert config.retry_attempts == 3  # default value


def test_load_config_missing_qdrant_url(monkeypatch):
    """Test loading config with missing QDRANT_URL raises ValueError."""
    monkeypatch.delenv("QDRANT_URL", raising=False)
    monkeypatch.setenv("COHERE_API_KEY", "test-api-key")

    with tempfile.TemporaryDirectory() as temp_dir:
        monkeypatch.setenv("FRONTEND_DOCS_PATH", temp_dir)

        with pytest.raises(ValueError, match="QDRANT_URL environment variable is required"):
            load_config()


def test_load_config_missing_cohere_api_key(monkeypatch):
    """Test loading config with missing COHERE_API_KEY raises ValueError."""
    monkeypatch.setenv("QDRANT_URL", "https://test.qdrant.tech:6333")
    monkeypatch.delenv("COHERE_API_KEY", raising=False)

    with tempfile.TemporaryDirectory() as temp_dir:
        monkeypatch.setenv("FRONTEND_DOCS_PATH", temp_dir)

        with pytest.raises(ValueError, match="COHERE_API_KEY environment variable is required"):
            load_config()


def test_validate_config_valid():
    """Test validation of a valid configuration."""
    config = Config(
        qdrant_url="https://test.qdrant.tech:6333",
        qdrant_api_key="test-key",
        cohere_api_key="test-api-key",
        frontend_docs_path=tempfile.gettempdir(),
        chunk_size=512,
        batch_size=10,
        retry_attempts=3
    )

    # Should not raise any exceptions
    validate_config(config)


def test_validate_config_invalid_url():
    """Test validation of an invalid URL."""
    config = Config(
        qdrant_url="invalid-url",
        qdrant_api_key="test-key",
        cohere_api_key="test-api-key",
        frontend_docs_path=tempfile.gettempdir(),
        chunk_size=512,
        batch_size=10,
        retry_attempts=3
    )

    with pytest.raises(ValueError, match="QDRANT_URL must be a valid URL"):
        validate_config(config)


def test_validate_config_negative_chunk_size():
    """Test validation of a negative chunk size."""
    config = Config(
        qdrant_url="https://test.qdrant.tech:6333",
        qdrant_api_key="test-key",
        cohere_api_key="test-api-key",
        frontend_docs_path=tempfile.gettempdir(),
        chunk_size=-1,
        batch_size=10,
        retry_attempts=3
    )

    with pytest.raises(ValueError, match="CHUNK_SIZE must be positive"):
        validate_config(config)


def test_validate_config_docs_path_not_exists(monkeypatch):
    """Test validation when docs path doesn't exist."""
    config = Config(
        qdrant_url="https://test.qdrant.tech:6333",
        qdrant_api_key="test-key",
        cohere_api_key="test-api-key",
        frontend_docs_path="/non/existent/path",
        chunk_size=512,
        batch_size=10,
        retry_attempts=3
    )

    with pytest.raises(ValueError, match="FRONTEND_DOCS_PATH does not exist"):
        validate_config(config)