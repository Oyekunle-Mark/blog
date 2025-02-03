from blog.feed_generator import BlogFeedGenerator
from blog.config import Post, Tag, Pages
from datetime import datetime
import tempfile
from pathlib import Path
import pytest
import xml.etree.ElementTree as ET

@pytest.fixture
def test_pages():
    post1 = Post(
        filename="test1.md",
        title="Test Post 1",
        date=datetime(2023, 1, 1),  # Earlier date
        tags=["test", "python"],
        content="<h1>Test content 1</h1>"
    )

    post2 = Post(
        filename="test2.md",
        title="Test Post 2",
        date=datetime(2023, 1, 2),  # Later date
        tags=["test"],
        content="<h1>Test content 2</h1>"
    )

    tag1 = Tag(name="test", posts=[post1, post2])
    tag2 = Tag(name="python", posts=[post1])

    return Pages(posts=[post1, post2], tags=[tag1, tag2])

def test_generate_main_feed(test_pages):
    with tempfile.TemporaryDirectory() as tmpdir:
        generator = BlogFeedGenerator(
            site_url="https://example.com",
            title="Test Blog",
            description="Test Description"
        )
        output_path = generator.generate_main_feed(test_pages, Path(tmpdir))

        # Check that feed was created
        assert output_path.exists()

        # Parse and validate feed content
        tree = ET.parse(output_path)
        root = tree.getroot()

        # Check channel information
        channel = root.find('channel')
        assert channel.find('title').text == "Test Blog"
        assert channel.find('description').text == "Test Description"

        # Check items (posts)
        items = channel.findall('item')
        assert len(items) == 2

        # Check newest post first (Test Post 2)
        assert items[0].find('title').text == "Test Post 2"
        assert items[0].find('link').text == "https://example.com/posts/test2.html"

        # Check older post second (Test Post 1)
        assert items[1].find('title').text == "Test Post 1"
        assert items[1].find('link').text == "https://example.com/posts/test1.html"

        # Check categories (tags) for first post
        categories = items[1].findall('category')
        assert len(categories) == 2
        assert {cat.text for cat in categories} == {"test", "python"}

def test_generate_tag_feed(test_pages):
    with tempfile.TemporaryDirectory() as tmpdir:
        generator = BlogFeedGenerator(
            site_url="https://example.com",
            title="Test Blog",
            description="Test Description"
        )

        # Get the 'test' tag which has two posts
        test_tag = next(tag for tag in test_pages.tags if tag.name == "test")
        output_path = generator.generate_tag_feed(test_tag, Path(tmpdir))

        # Check that feed was created
        assert output_path.exists()
        assert output_path.parent.name == "feeds"

        # Parse and validate feed content
        tree = ET.parse(output_path)
        root = tree.getroot()

        # Check channel information
        channel = root.find('channel')
        assert channel.find('title').text == "Test Blog - Posts tagged 'test'"

        # Check items (posts)
        items = channel.findall('item')
        assert len(items) == 2  # Should have both posts with 'test' tag

        # Verify all posts have the 'test' tag
        for item in items:
            categories = item.findall('category')
            assert any(cat.text == "test" for cat in categories)

def test_feed_dates(test_pages):
    with tempfile.TemporaryDirectory() as tmpdir:
        generator = BlogFeedGenerator(
            site_url="https://example.com",
            title="Test Blog",
            description="Test Description"
        )
        output_path = generator.generate_main_feed(test_pages, Path(tmpdir))

        # Parse and check dates
        tree = ET.parse(output_path)
        channel = tree.getroot().find('channel')
        items = channel.findall('item')

        # Check date format (should be RFC 822 or ISO 8601)
        pubDate = items[0].find('pubDate')
        assert pubDate is not None
        # The date string should contain the year 2023
        assert "2023" in pubDate.text

def test_empty_pages():
    with tempfile.TemporaryDirectory() as tmpdir:
        generator = BlogFeedGenerator(
            site_url="https://example.com",
            title="Test Blog",
            description="Test Description"
        )
        empty_pages = Pages(posts=[], tags=[])
        output_path = generator.generate_main_feed(empty_pages, Path(tmpdir))

        # Check that feed was created
        assert output_path.exists()

        # Parse and validate feed content
        tree = ET.parse(output_path)
        root = tree.getroot()

        # Check channel information exists but has no items
        channel = root.find('channel')
        assert channel is not None
        items = channel.findall('item')
        assert len(items) == 0

def test_feed_content_encoding(test_pages):
    with tempfile.TemporaryDirectory() as tmpdir:
        generator = BlogFeedGenerator(
            site_url="https://example.com",
            title="Test Blog",
            description="Test Description"
        )
        output_path = generator.generate_main_feed(test_pages, Path(tmpdir))

        # Read the raw content
        content = output_path.read_text()

        # Check XML declaration
        assert "<?xml version=\'1.0\'" in content

        # Check content type/encoding
        tree = ET.parse(output_path)
        root = tree.getroot()

        # Verify HTML content is properly encoded
        channel = root.find('channel')
        items = channel.findall('item')
        description = items[0].find('description')
        assert description is not None
        assert '<h1>' in description.text  # HTML should be preserved
