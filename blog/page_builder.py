from pathlib import Path
from typing import List
from collections import defaultdict
from .config import Post, Tag, Pages
from .converter import MarkdownConverter

class PageBuilder:
    """Builds pages (posts and tag pages) from markdown files"""

    def __init__(self, posts_dir: str):
        self.converter = MarkdownConverter(posts_dir)

    def build_tags(self, posts: List[Post]) -> List[Tag]:
        """
        Build tag objects from posts.
        Returns a list of Tag objects.
        """
        # Group posts by tag
        tag_posts = defaultdict(list)
        for post in posts:
            for tag_name in post.tags:
                tag_posts[tag_name].append(post)

        # Create Tag objects and sort them by name
        return sorted(
            [
                Tag(
                    name=name,
                    # Sort posts within each tag by date
                    posts=sorted(posts, key=lambda x: x.date, reverse=True)
                )
                for name, posts in tag_posts.items()
            ],
            key=lambda x: x.name
        )

    def build_pages(self) -> Pages:
        """
        Build all pages (posts and tags).
        Returns a Pages object containing all posts and tags.
        """
        # Convert markdown files to posts
        posts = self.converter.convert_all()

        # Sort posts by date (newest first)
        sorted_posts = sorted(posts, key=lambda x: x.date, reverse=True)

        # Build tags
        tags = self.build_tags(sorted_posts)

        return Pages(posts=sorted_posts, tags=tags)
