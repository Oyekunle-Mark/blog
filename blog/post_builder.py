from pathlib import Path
from typing import List
from .config import Post
from .converter import MarkdownConverter

class PostBuilder:
    """Builds posts from markdown files using MarkdownConverter"""

    def __init__(self, posts_dir: str):
        self.converter = MarkdownConverter(posts_dir)

    def build_posts(self) -> List[Post]:
        """
        Convert all markdown files to Post objects.
        Returns a list of Post objects sorted by date (newest first).
        """
        posts = self.converter.convert_all()
        return sorted(posts, key=lambda x: x.date, reverse=True)
