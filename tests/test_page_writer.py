from blog.page_writer import PageWriter
from blog.config import Post, Tag, Pages
from datetime import datetime
import tempfile
from pathlib import Path
import pytest

@pytest.fixture
def test_site():
    with tempfile.TemporaryDirectory() as tmpdir:
        templates_dir = Path(tmpdir) / "templates"
        templates_dir.mkdir()

        # Create test templates
        (templates_dir / "base.html").write_text("""
<!DOCTYPE html>
<html>
<body>{% block content %}{% endblock %}</body>
</html>""")

        (templates_dir / "post.html").write_text("""
{% extends "base.html" %}
{% block content %}{{ content }}{% endblock %}""")

        (templates_dir / "index.html").write_text("""
{% extends "base.html" %}
{% block content %}
{% for post in posts %}<h2>{{ post.title }}</h2>{% endfor %}
{% endblock %}""")

        (templates_dir / "tag.html").write_text("""
{% extends "base.html" %}
{% block content %}
<h1>Posts tagged "{{ tag.name }}"</h1>
{% for post in tag.posts %}<h2>{{ post.title }}</h2>{% endfor %}
{% endblock %}""")

        yield tmpdir

def test_write_post(test_site):
    writer = PageWriter(
        output_dir=str(Path(test_site) / "posts"),
        templates_dir=str(Path(test_site) / "templates")
    )

    post = Post(
        filename="test.md",
        title="Test Post",
        date=datetime.now(),
        tags=["test"],
        content="<h1>Test</h1>"
    )

    output_path = writer.write_post(post)
    assert output_path.exists()
    assert "&lt;h1&gt;Test&lt;/h1&gt;" in output_path.read_text()

def test_write_all(test_site):
    writer = PageWriter(
        output_dir=str(Path(test_site) / "posts"),
        templates_dir=str(Path(test_site) / "templates")
    )

    post = Post(
        filename="test.md",
        title="Test Post",
        date=datetime.now(),
        tags=["test"],
        content="<h1>Test</h1>"
    )

    tag = Tag(name="test", posts=[post])
    pages = Pages(posts=[post], tags=[tag])

    count = writer.write_all(pages)
    assert count == 1

    # Check that all files were created
    assert (Path(test_site) / "posts" / "test.html").exists()
    assert (Path(test_site) / "index.html").exists()
    assert (Path(test_site) / "test.html").exists()

    # Check tag page content
    tag_page = (Path(test_site) / "test.html").read_text()
    assert 'Posts tagged "test"' in tag_page
    assert "Test Post" in tag_page
