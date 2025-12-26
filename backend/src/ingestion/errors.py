"""
Error handling and retry mechanisms for the book content ingestion system.
"""
import time
import random
from typing import Callable, Type, Tuple, Any
from functools import wraps


class IngestionError(Exception):
    """Base exception for ingestion-related errors."""
    pass


class ConfigurationError(IngestionError):
    """Raised when there's an issue with configuration."""
    pass


class FileReadError(IngestionError):
    """Raised when there's an issue reading a file."""
    pass


class APIError(IngestionError):
    """Raised when there's an issue with an external API."""
    pass


class DatabaseError(IngestionError):
    """Raised when there's an issue with the database."""
    pass


def retry_with_backoff(
    max_retries: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    backoff_factor: float = 2.0,
    exceptions: Tuple[Type[Exception], ...] = (Exception,)
):
    """
    Decorator to retry a function with exponential backoff.

    Args:
        max_retries: Maximum number of retry attempts
        base_delay: Initial delay between retries in seconds
        max_delay: Maximum delay between retries in seconds
        backoff_factor: Multiplier for delay after each retry
        exceptions: Tuple of exception types to catch and retry on
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            last_exception = None

            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e

                    if attempt == max_retries:
                        # Final attempt failed, raise the exception
                        raise last_exception

                    # Calculate delay with exponential backoff and jitter
                    delay = min(base_delay * (backoff_factor ** attempt), max_delay)
                    jitter = random.uniform(0, delay * 0.1)  # Add up to 10% jitter
                    total_delay = delay + jitter

                    print(f"Attempt {attempt + 1} failed: {str(e)}. "
                          f"Retrying in {total_delay:.2f} seconds...")

                    time.sleep(total_delay)

            # This line should never be reached, but included for type safety
            raise last_exception

        return wrapper

    return decorator


def handle_api_call_with_retry(api_call: Callable, max_retries: int = 3,
                              base_delay: float = 1.0) -> Any:
    """
    Handle an API call with retry logic.

    Args:
        api_call: Function to call
        max_retries: Maximum number of retry attempts
        base_delay: Base delay between retries

    Returns:
        Result of the API call

    Raises:
        APIError: If all retry attempts fail
    """
    last_exception = None

    for attempt in range(max_retries + 1):
        try:
            return api_call()
        except Exception as e:
            last_exception = e

            if attempt == max_retries:
                # Final attempt failed
                raise APIError(f"API call failed after {max_retries} retries: {str(e)}")

            # Exponential backoff
            delay = base_delay * (2 ** attempt)  # Exponential backoff
            print(f"API call attempt {attempt + 1} failed: {str(e)}. "
                  f"Retrying in {delay:.2f} seconds...")
            time.sleep(delay)

    # This should never be reached
    raise last_exception


def circuit_breaker(max_failures: int = 5, reset_timeout: float = 60.0):
    """
    Circuit breaker decorator to prevent repeated failures.

    Args:
        max_failures: Maximum number of failures before opening the circuit
        reset_timeout: Time in seconds before attempting to close the circuit again
    """
    def decorator(func: Callable) -> Callable:
        # Use function attributes to store circuit state
        func.failure_count = 0
        func.last_failure_time = None
        func.is_open = False

        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            if func.is_open:
                # Check if it's time to try resetting
                if (time.time() - func.last_failure_time) >= reset_timeout:
                    # Attempt to close the circuit by trying once
                    try:
                        result = func(*args, **kwargs)
                        # Success! Reset the circuit
                        func.failure_count = 0
                        func.is_open = False
                        return result
                    except Exception as e:
                        # Still failing, keep circuit open
                        func.last_failure_time = time.time()
                        raise e
                else:
                    # Circuit still open, fail fast
                    raise IngestionError("Circuit breaker is open - API temporarily unavailable")

            try:
                result = func(*args, **kwargs)
                # Success! Reset failure count
                func.failure_count = 0
                return result
            except Exception as e:
                # Failure occurred
                func.failure_count += 1
                func.last_failure_time = time.time()

                if func.failure_count >= max_failures:
                    # Open the circuit
                    func.is_open = True
                    print(f"Circuit breaker opened after {max_failures} failures")

                raise e

        return wrapper

    return decorator


def validate_and_handle_errors(func: Callable) -> Callable:
    """
    Decorator to add error handling and validation to functions.
    """
    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        try:
            # Add any pre-validation here if needed
            result = func(*args, **kwargs)
            return result
        except IngestionError:
            # Re-raise ingestion-specific errors as-is
            raise
        except Exception as e:
            # Wrap other exceptions in IngestionError
            raise IngestionError(f"Unexpected error in {func.__name__}: {str(e)}") from e

    return wrapper