from pathlib import Path
from typing import List
from .config import Post, WriterError
from .converter import MarkdownConverter
from .template_handler import TemplateHandler

class PostWriter:
    def __init__(self, posts_dir: str, output_dir: str, templates_dir: str):
        self.converter = MarkdownConverter(posts_dir)
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
            return output_path
        except Exception as e:
            raise WriterError(f"Failed to write {post.filename}: {str(e)}")

    def process_posts(self) -> int:
        """
        Convert and write all posts.
        Returns the number of successfully processed posts.
        Handles its own error reporting.
        """
        try:
            # Convert all markdown files to Post objects
            posts = self.converter.convert_all()

            # Write all posts to HTML files
            successful_count = 0
            failed_writes = []

            for post in posts:
                try:
                    self.write_post(post)
                    # Report successful write
                    print(f"\nProcessed: {post.filename}")
                    print(f"  Title: {post.title}")
                    print(f"  Date: {post.date}")
                    print(f"  Tags: {', '.join(post.tags)}")
                    successful_count += 1
                except WriterError as e:
                    failed_writes.append((post, str(e)))

            if failed_writes:
                print("\nFailed to write the following posts:")
                for post, error in failed_writes:
                    print(f"- {post.filename}: {error}")

            return successful_count

        except Exception as e:
            print(f"\nError during processing: {str(e)}")
            return 0
