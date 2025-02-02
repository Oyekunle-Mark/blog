from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from .config import Post

class TemplateHandler:
    def __init__(self, templates_dir: str):
        self.env = Environment(
            loader=FileSystemLoader(templates_dir),
            autoescape=True
        )
        self.post_template = self.env.get_template('post.html')

    def render_post(self, post: Post) -> str:
        """
        Render a post using the template.
        """
        return self.post_template.render(
            title=post.title,
            date=post.date,
            tags=post.tags,
            content=post.content
        )
