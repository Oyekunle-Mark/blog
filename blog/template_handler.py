from jinja2 import Environment, FileSystemLoader, select_autoescape
from datetime import datetime
from .config import Post, Tag, Pages


class TemplateHandler:
    def __init__(self, templates_dir: str):
        self.env = Environment(
            loader=FileSystemLoader(templates_dir),
            autoescape=select_autoescape(['html', 'xml'])
        )

        # Load templates
        self.post_template = self.env.get_template('post.html')
        self.index_template = self.env.get_template('index.html')
        self.tag_template = self.env.get_template('tag.html')

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
            'css_path': '../css',
            'root_path': '../',
            **self.common_context
        }

        return self.post_template.render(context)

    def render_index(self, pages: Pages) -> str:
        """Render the index page with all posts"""

        context = {
            'posts': pages.posts,
            'tags': pages.tags,
            'css_path': 'css',
            'root_path': './',
            **self.common_context
        }

        return self.index_template.render(context)

    def render_tag(self, tag: Tag) -> str:
        """Render a tag page"""

        context = {
            'tag': tag,
            'css_path': 'css',
            'root_path': './',
            **self.common_context
        }

        return self.tag_template.render(context)
