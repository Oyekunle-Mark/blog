from pathlib import Path
import shutil
from .post_writer import PostWriter
from .css_generator import CssGenerator

def cleanup_generated_files(static_dir: Path) -> None:
    """Remove all generated files (HTML files, pygments.css, and index.html)"""
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

    # Remove index.html
    index_file = static_dir / "index.html"
    if index_file.exists():
        index_file.unlink()
        print(f"Removed file: {index_file}")
    else:
        print("No index.html found")

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

    # Initialize writer and process posts
    writer = PostWriter(
        posts_dir=str(posts_dir),
        output_dir=str(static_dir / "posts"),
        templates_dir=str(templates_dir)
    )
    successful_count = writer.process_posts()

    # Print final summary
    print(f"\nTotal posts generated: {successful_count}")

    return 0 if successful_count > 0 else 1
