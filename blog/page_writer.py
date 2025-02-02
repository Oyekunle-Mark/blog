from pathlib import Path
from .config import Post, Tag, Pages, WriterError
from .template_handler import TemplateHandler
from .sitemap_generator import SitemapGenerator

class PageWriter:
    def __init__(self, output_dir: str, templates_dir: str, site_url: str):
        self.output_dir = Path(output_dir)
        self.template_handler = TemplateHandler(templates_dir)
        self.sitemap_generator = SitemapGenerator(site_url)

    def write_post(self, post: Post) -> Path:
        """Write a single post"""
        try:
            self.output_dir.mkdir(parents=True, exist_ok=True)
            output_path = self.output_dir / post.html_filename

            html_content = self.template_handler.render_post(post)
            output_path.write_text(html_content)

            print(f"\nProcessed: {post.filename}")
            print(f"  Title: {post.title}")
            print(f"  Date: {post.date}")
            print(f"  Tags: {', '.join(post.tags)}")

            return output_path
        except Exception as e:
            raise WriterError(f"Failed to write {post.filename}: {str(e)}")

    def write_index(self, pages: Pages) -> Path:
        """Write the index page"""
        try:
            self.output_dir.parent.mkdir(parents=True, exist_ok=True)
            output_path = self.output_dir.parent / "index.html"

            html_content = self.template_handler.render_index(pages)
            output_path.write_text(html_content)

            print("\nGenerated index page")
            return output_path
        except Exception as e:
            raise WriterError(f"Failed to write index.html: {str(e)}")

    def write_tag(self, tag: Tag) -> Path:
        """Write a tag page"""
        try:
            self.output_dir.parent.mkdir(parents=True, exist_ok=True)
            output_path = self.output_dir.parent / tag.html_filename

            html_content = self.template_handler.render_tag(tag)
            output_path.write_text(html_content)

            print(f"\nGenerated tag page: {tag.name}")
            return output_path
        except Exception as e:
            raise WriterError(f"Failed to write tag page {tag.name}: {str(e)}")

    def write_all(self, pages: Pages) -> int:
        """Write all pages and generate sitemap"""
        successful_count = 0
        failed_writes = []

        # Write posts
        for post in pages.posts:
            try:
                self.write_post(post)
                successful_count += 1
            except WriterError as e:
                failed_writes.append((post, str(e)))

        # If we have successful posts, write index and tag pages
        if successful_count > 0:
            try:
                self.write_index(pages)

                # Write tag pages
                for tag in pages.tags:
                    self.write_tag(tag)

                # Generate sitemap
                self.sitemap_generator.generate_sitemap(pages, self.output_dir.parent)

            except WriterError as e:
                print(f"\nFailed to generate index or tag pages: {e}")

        # Report any failures
        if failed_writes:
            print("\nFailed to write the following posts:")
            for post, error in failed_writes:
                print(f"- {post.filename}: {error}")

        return successful_count
