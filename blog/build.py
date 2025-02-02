from pathlib import Path
from .post_writer import PostWriter
from .css_generator import CssGenerator

def main():
    # Get project root directory
    project_root = Path(__file__).parent.parent

    # Setup paths
    posts_dir = project_root / "blog" / "posts"
    static_dir = project_root / "static" / "posts"
    templates_dir = project_root / "blog" / "templates"
    css_dir = project_root / "static" / "css"

    # Generate CSS files
    try:
        css_generator = CssGenerator(str(css_dir))
        css_generator.generate_pygments_css()
    except Exception as e:
        print(f"Warning: Failed to generate CSS: {e}")

    # Initialize writer and process posts
    writer = PostWriter(
        posts_dir=str(posts_dir),
        output_dir=str(static_dir),
        templates_dir=str(templates_dir)
    )
    successful_count = writer.process_posts()

    # Print final summary
    print(f"\nTotal posts generated: {successful_count}")

    return 0 if successful_count > 0 else 1
