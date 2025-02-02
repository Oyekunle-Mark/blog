from pathlib import Path
from typing import List
from .config import Post, WriterError
from .template_handler import TemplateHandler

class PostWriter:
    """Writes posts and index page using templates"""

    def __init__(self, output_dir: str, templates_dir: str):
        self.output_dir = Path(output_dir)
        self.template_handler = TemplateHandler(templates_dir)

    def write_post(self, post: Post) -> Path:
        """
        Write a single post to the output directory.
        Returns the path to the written file.
        """
        try:
            self.output_dir.mkdir(parents=True, exist_ok=True)
            output_path = self.output_dir / post.html_filename

            # Render the post using the template
            html_content = self.template_handler.render_post(post)

            # Write the rendered HTML to file
            output_path.write_text(html_content)
            print(f"\nProcessed: {post.filename}")
            print(f"  Title: {post.title}")
            print(f"  Date: {post.date}")
            print(f"  Tags: {', '.join(post.tags)}")

            return output_path
        except Exception as e:
            raise WriterError(f"Failed to write {post.filename}: {str(e)}")

    def write_index(self, posts: List[Post]) -> Path:
        """
        Write the index page.
        Returns the path to the written file.
        """
        try:
            self.output_dir.parent.mkdir(parents=True, exist_ok=True)
            output_path = self.output_dir.parent / "index.html"

            # Render the index using the template
            html_content = self.template_handler.render_index(posts)

            # Write the rendered HTML to file
            output_path.write_text(html_content)
            print("\nGenerated index page")

            return output_path
        except Exception as e:
            raise WriterError(f"Failed to write index.html: {str(e)}")

    def write_all(self, posts: List[Post]) -> int:
        """
        Write all posts and index page.
        Returns number of successfully written posts.
        """
        successful_count = 0
        failed_writes = []

        # Write individual posts
        for post in posts:
            try:
                self.write_post(post)
                successful_count += 1
            except WriterError as e:
                failed_writes.append((post, str(e)))

        # Write index if we have successful posts
        if successful_count > 0:
            try:
                self.write_index(posts)
            except WriterError as e:
                print(f"\nFailed to generate index page: {e}")

        # Report any failures
        if failed_writes:
            print("\nFailed to write the following posts:")
            for post, error in failed_writes:
                print(f"- {post.filename}: {error}")

        return successful_count
