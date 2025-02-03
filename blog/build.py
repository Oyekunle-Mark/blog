from pathlib import Path
import shutil
from .page_builder import PageBuilder
from .page_writer import PageWriter
from .css_generator import CssGenerator

def cleanup_generated_files(static_dir: Path) -> None:
    """Remove all generated files"""
    print("\nCleaning up generated files...")

    # Remove generated HTML files in posts directory
    posts_dir = static_dir / "posts"
    if posts_dir.exists():
        # List files being removed
        files = list(posts_dir.glob('*.html'))
        if files:
            print(f"Removing {len(files)} HTML files from {posts_dir}:")
            for file in files:
                print(f"  - {file.name}")
        # Remove the directory
        shutil.rmtree(posts_dir)
        print(f"Removed directory: {posts_dir}")
    else:
        print(f"No posts directory found at {posts_dir}")

    # Remove index.html and tag pages
    for html_file in static_dir.glob('*.html'):
        html_file.unlink()
        print(f"Removed file: {html_file}")

    # Remove sitemap.xml
    sitemap_file = static_dir / 'sitemap.xml'
    if sitemap_file.exists():
        sitemap_file.unlink()
        print("Removed file: sitemap.xml")

    # Remove RSS feeds
    feeds_dir = static_dir / 'feeds'
    if feeds_dir.exists():
        shutil.rmtree(feeds_dir)
        print(f"Removed directory: {feeds_dir}")

    main_feed = static_dir / 'feed.xml'
    if main_feed.exists():
        main_feed.unlink()
        print(f"Removed file: {main_feed}")

    # Remove generated pygments.css
    pygments_css = static_dir / "css" / "pygments.css"
    if pygments_css.exists():
        pygments_css.unlink()
        print(f"Removed file: {pygments_css}")
    else:
        print(f"No pygments.css found at {pygments_css}")

def main():
    # Get project root directory
    project_root = Path(__file__).parent.parent

    # Setup paths
    posts_dir = project_root / "blog" / "posts"
    static_dir = project_root / "static"
    templates_dir = project_root / "blog" / "templates"
    css_dir = project_root / "static" / "css"

    # Cleanup previously generated files
    cleanup_generated_files(static_dir)

    # Generate CSS files
    try:
        css_generator = CssGenerator(str(css_dir))
        css_generator.generate_pygments_css()
    except Exception as e:
        print(f"Warning: Failed to generate CSS: {e}")

    try:
        # Build pages from markdown files
        builder = PageBuilder(str(posts_dir))
        pages = builder.build_pages()

        # Write all pages
        writer = PageWriter(
            output_dir=str(static_dir / "posts"),
            templates_dir=str(templates_dir),
            site_url="https://www.oyeoloyede.com"
        )
        successful_count = writer.write_all(pages)

        # Print final summary
        print(f"\nTotal posts generated: {successful_count}")

        return 0 if successful_count > 0 else 1

    except Exception as e:
        print(f"\nError during processing: {str(e)}")
        return 1
