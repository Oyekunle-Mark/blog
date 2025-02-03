from blog.sitemap_generator import SitemapGenerator
from blog.config import Post, Tag, Pages
from datetime import datetime
import tempfile
from pathlib import Path
import pytest

@pytest.fixture
def test_pages():
    post1 = Post(
        filename="test1.md",
        title="Test Post 1",
        date=datetime(2023, 1, 1),
        tags=["test", "python"],
        content="Test content 1"
    )

    post2 = Post(
        filename="test2.md",
        title="Test Post 2",
        date=datetime(2023, 1, 2),
        tags=["test"],
        content="Test content 2"
    )

    tag1 = Tag(name="test", posts=[post1, post2])
    tag2 = Tag(name="python", posts=[post1])

    return Pages(posts=[post1, post2], tags=[tag1, tag2])

def test_generate_sitemap(test_pages):
    with tempfile.TemporaryDirectory() as tmpdir:
        generator = SitemapGenerator(site_url="https://example.com")
        output_path = generator.generate_sitemap(test_pages, Path(tmpdir))

        # Check that sitemap was created
        assert output_path.exists()

        # Read sitemap content
        content = output_path.read_text()

        # Check basic structure
        assert '<?xml version="1.0" encoding="UTF-8"?>' in content
        assert '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' in content

        # Check URLs
        assert 'https://example.com</loc>' in content
        assert 'https://example.com/posts/test1.html</loc>' in content
        assert 'https://example.com/posts/test2.html</loc>' in content
        assert 'https://example.com/test.html</loc>' in content
        assert 'https://example.com/python.html</loc>' in content

        # Check dates
        assert '2023-01-01' in content  # First post date
        assert '2023-01-02' in content  # Second post date

def test_generate_sitemap_empty_pages():
    with tempfile.TemporaryDirectory() as tmpdir:
        generator = SitemapGenerator(site_url="https://example.com")
        pages = Pages(posts=[], tags=[])
        output_path = generator.generate_sitemap(pages, Path(tmpdir))

        # Check that sitemap was created
        assert output_path.exists()

        # Read sitemap content
        content = output_path.read_text()

        # Should only contain the index page
        assert content.count('<url>') == 1
        assert 'https://example.com</loc>' in content
