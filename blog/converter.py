import yaml
import markdown
from pathlib import Path
from typing import List
from .config import Post, ConversionError

class MarkdownConverter:
    def __init__(self, posts_dir: str):
        self.posts_dir = Path(posts_dir)
        self.md = markdown.Markdown(
            extensions=['extra', 'codehilite', 'meta']
        )

    def parse_markdown_file(self, file_path: Path) -> Post:
        """
        Parse a markdown file with YAML front matter.
        Returns a Post object.
        Raises ConversionError if parsing fails.
        """
        try:
            content = file_path.read_text()
        except Exception as e:
            raise ConversionError(f"Failed to read {file_path}: {str(e)}")

        if not content.startswith('---'):
            raise ConversionError(f"No front matter found in {file_path}")

        try:
            _, front_matter, markdown_content = content.split('---', 2)
        except ValueError:
            raise ConversionError(f"Invalid front matter format in {file_path}")

        try:
            metadata = yaml.safe_load(front_matter)
            if not isinstance(metadata, dict):
                raise ConversionError(f"Invalid YAML front matter in {file_path}")
        except yaml.YAMLError as e:
            raise ConversionError(f"Failed to parse YAML front matter in {file_path}: {str(e)}")

        html_content = self.md.convert(markdown_content)

        return Post.from_markdown(
            filename=file_path.name,
            metadata=metadata,
            content=html_content
        )

    def convert_all(self) -> List[Post]:
        """
        Convert all markdown files in the posts directory.
        Returns a list of Post objects.
        """
        posts = []
        failed_files = []

        for md_file in self.posts_dir.glob('*.md'):
            try:
                post = self.parse_markdown_file(md_file)
                posts.append(post)
            except ConversionError as e:
                failed_files.append((md_file, str(e)))

        if failed_files:
            errors = "\n".join(f"- {file.name}: {error}" for file, error in failed_files)
            raise ConversionError(f"Failed to convert the following files:\n{errors}")

        return posts
