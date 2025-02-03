from datetime import datetime
from blog.config import Post, Tag, Pages, ConversionError
import pytest

def test_post_creation():
    post = Post(
        filename="test.md",
        title="Test Post",
        date=datetime.now(),
        tags=["test", "python"],
        content="# Test Content"
    )
    assert post.html_filename == "test.html"

def test_post_from_markdown():
    metadata = {
        "title": "Test Post",
        "date": datetime.now(),
        "tags": ["test", "python"]
    }
    content = "# Test Content"

    post = Post.from_markdown("test.md", metadata, content)
    assert post.title == "Test Post"
    assert post.tags == ["test", "python"]

def test_post_from_markdown_missing_metadata():
    metadata = {"title": "Test Post"}  # Missing required fields
    content = "# Test Content"

    with pytest.raises(ConversionError):
        Post.from_markdown("test.md", metadata, content)

def test_tag_creation():
    post = Post(
        filename="test.md",
        title="Test Post",
        date=datetime.now(),
        tags=["test"],
        content="# Test Content"
    )
    tag = Tag(name="test", posts=[post])
    assert tag.html_filename == "test.html"

def test_pages_creation():
    post = Post(
        filename="test.md",
        title="Test Post",
        date=datetime.now(),
        tags=["test"],
        content="# Test Content"
    )
    tag = Tag(name="test", posts=[post])
    pages = Pages(posts=[post], tags=[tag])
    assert len(pages.posts) == 1
    assert len(pages.tags) == 1
