from pathlib import Path
from blog.converter import MarkdownConverter
from blog.config import ConversionError
import pytest
import tempfile

@pytest.fixture
def test_posts_dir():
    """Create a temporary directory for test posts"""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)

@pytest.fixture
def valid_markdown_file(test_posts_dir):
    """Create a valid markdown file in the test directory"""
    file_path = test_posts_dir / "valid_post.md"
    file_path.write_text("""---
title: Test Post
date: 2023-11-14
tags: [test, python]
---

# Test Content

Some test content here.
""")
    return file_path

@pytest.fixture
def invalid_markdown_file(test_posts_dir):
    """Create an invalid markdown file in the test directory"""
    file_path = test_posts_dir / "invalid_post.md"
    file_path.write_text("""# No Front Matter
Just content
""")
    return file_path

def test_parse_valid_markdown(valid_markdown_file):
    converter = MarkdownConverter(str(valid_markdown_file.parent))
    post = converter.parse_markdown_file(valid_markdown_file)
    assert post.title == "Test Post"
    assert "test" in post.tags
    assert "<h1>Test Content</h1>" in post.content
    assert "<p>Some test content here.</p>" in post.content

def test_parse_invalid_markdown(invalid_markdown_file):
    converter = MarkdownConverter(str(invalid_markdown_file.parent))
    with pytest.raises(ConversionError):
        converter.parse_markdown_file(invalid_markdown_file)

def test_convert_all(test_posts_dir):
    # Create multiple test posts in the directory
    post1 = test_posts_dir / "post1.md"
    post1.write_text("""---
title: Post 1
date: 2023-11-14
tags: [test, python]
---
# Post 1
Content 1""")

    post2 = test_posts_dir / "post2.md"
    post2.write_text("""---
title: Post 2
date: 2023-11-15
tags: [test, blog]
---
# Post 2
Content 2""")

    converter = MarkdownConverter(str(test_posts_dir))
    posts = converter.convert_all()

    assert len(posts) == 2
    assert any(post.title == "Post 1" for post in posts)
    assert any(post.title == "Post 2" for post in posts)
    # Add checks for converted HTML content
    assert any("<h1>Post 1</h1>" in post.content for post in posts)
    assert any("<h1>Post 2</h1>" in post.content for post in posts)
