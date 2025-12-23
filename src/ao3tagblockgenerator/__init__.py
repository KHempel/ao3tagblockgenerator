"""ao3tagblockgenerator package.

Provides a simple CLI to parse comma-separated lists of strings.
"""
__all__ = ["parse_tags", "main"]
__version__ = "0.0.1"

from .cli import parse_tags, main
