"""
Logging infrastructure for the book content ingestion system using rich.
"""
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from typing import Optional
import time
from datetime import datetime


class IngestionLogger:
    """
    Logging infrastructure for the ingestion process using rich for formatted output.
    """
    def __init__(self):
        self.console = Console()
        self.progress = None

    def log_info(self, message: str) -> None:
        """Log an informational message."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.console.print(f"[blue][{timestamp}][/blue] [bold blue]INFO[/bold blue]: {message}")

    def log_success(self, message: str) -> None:
        """Log a success message."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.console.print(f"[blue][{timestamp}][/blue] [bold green]SUCCESS[/bold green]: {message}")

    def log_warning(self, message: str) -> None:
        """Log a warning message."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.console.print(f"[blue][{timestamp}][/blue] [bold yellow]WARNING[/bold yellow]: {message}")

    def log_error(self, message: str) -> None:
        """Log an error message."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.console.print(f"[blue][{timestamp}][/blue] [bold red]ERROR[/bold red]: {message}")

    def create_progress_tracker(self) -> Progress:
        """Create a progress tracker for the ingestion process."""
        self.progress = Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            console=self.console
        )
        return self.progress

    def log_module_status(self, module: str, chapter: str, status: str, progress: float = 0.0) -> None:
        """Log the status of a module/chapter processing."""
        status_emoji = {
            "pending": "⏳",
            "processing": "🔄",
            "completed": "✅",
            "failed": "❌"
        }.get(status, "❓")

        self.console.print(
            f"{status_emoji} Module: [bold]{module}[/bold], "
            f"Chapter: [bold]{chapter}[/bold], "
            f"Status: [bold]{status}[/bold] "
            f"({progress*100:.1f}%)"
        )

    def log_ingestion_summary(self, total_files: int, processed_files: int,
                            total_embeddings: int, start_time: float) -> None:
        """Log a summary of the ingestion process."""
        duration = time.time() - start_time
        table = Table(title="Ingestion Summary")
        table.add_column("Metric", style="bold")
        table.add_column("Value", justify="right")

        table.add_row("Total Files", str(total_files))
        table.add_row("Processed Files", str(processed_files))
        table.add_row("Total Embeddings", str(total_embeddings))
        table.add_row("Duration", f"{duration:.2f}s")
        table.add_row("Rate", f"{processed_files/duration:.2f} files/s" if duration > 0 else "N/A")

        self.console.print(table)

    def log_embedding_stats(self, vector_size: int, text_length: int) -> None:
        """Log statistics about embeddings."""
        panel = Panel(
            f"Vector Size: {vector_size}\n"
            f"Text Length: {text_length} chars",
            title="Embedding Stats",
            expand=False
        )
        self.console.print(panel)


# Global logger instance
logger = IngestionLogger()