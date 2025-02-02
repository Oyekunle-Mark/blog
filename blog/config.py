from dataclasses import dataclass
from datetime import datetime
from typing import List
from pathlib import Path

class BlogError(Exception):
    """Base exception class for blog errors"""
    pass

class ConversionError(BlogError):
    """Exception raised for markdown conversion errors"""
    pass

class WriterError(BlogError):
    """Exception raised for file writing errors"""
    pass

class CssGenerationError(BlogError):
    """Exception raised for CSS generation errors"""
    pass

@dataclass
class Post:
    filename: str
    title: str
    date: datetime
    tags: List[str]
    content: str

    @classmethod
    def from_markdown(cls, filename: str, metadata: dict, content: str) -> 'Post':
        """
        Create a Post instance from markdown metadata and content.
        Raises KeyError if required metadata (title, tags) is missing.
        """

        try:
            date_value = metadata['date']

            return cls(
                filename=filename,
                title=metadata['title'],
                date=metadata['date'],
                tags=metadata['tags'],
                content=content
            )
        except KeyError as e:
            raise ConversionError(f"Required metadata field missing in {filename}: {e}")

    @property
    def html_filename(self) -> str:
        """Generate HTML filename from markdown filename"""
        return Path(self.filename).with_suffix('.html').name
