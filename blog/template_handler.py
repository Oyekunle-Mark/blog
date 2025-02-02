from typing import List
from jinja2 import Environment, FileSystemLoader, select_autoescape
from datetime import datetime
from .config import Post

class TemplateHandler:
    def __init__(self, templates_dir: str):
        self.env = Environment(
            loader=FileSystemLoader(templates_dir),
            autoescape=select_autoescape(['html', 'xml'])
        )

        # Load templates
        self.post_template = self.env.get_template('post.html')
        self.index_template = self.env.get_template('index.html')

        # Common context for all templates
        self.common_context = {
            'current_year': datetime.now().year
        }

    def render_post(self, post: Post) -> str:
        """Render a single post"""
        context = {
            'title': post.title,
            'date': post.date,
            'tags': post.tags,
            'content': post.content,
            'css_path': '../css',    # Posts are in posts/ subdirectory
            'root_path': '../',      # Go up one level to reach root
            **self.common_context
        }
        return self.post_template.render(context)

    def render_index(self, posts: List[Post]) -> str:
        """Render the index page with all posts"""
        # Sort posts by date, newest first
        sorted_posts = sorted(posts, key=lambda x: x.date, reverse=True)
        context = {
            'posts': sorted_posts,
            'css_path': 'css',       # Index is at root
            'root_path': './',       # Already at root
            **self.common_context
        }
        return self.index_template.render(context)
