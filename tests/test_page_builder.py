from blog.page_builder import PageBuilder
import tempfile
from pathlib import Path
import pytest

@pytest.fixture
def test_posts_dir():
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create some test markdown files
        post1 = Path(tmpdir) / "post1.md"
        post1.write_text("""---
title: Post 1
date: 2023-11-14
tags: [test, python]
---
# Post 1
Content 1""")

        post2 = Path(tmpdir) / "post2.md"
        post2.write_text("""---
title: Post 2
date: 2023-11-15
tags: [test, blog]
---
# Post 2
Content 2""")

        yield tmpdir

def test_build_pages(test_posts_dir):
    builder = PageBuilder(test_posts_dir)
    pages = builder.build_pages()

    assert len(pages.posts) == 2
    assert len(pages.tags) == 3  # test, python, blog

    # Check posts are sorted by date
    assert pages.posts[0].title == "Post 2"  # Most recent first

    # Check tags are sorted alphabetically
    assert pages.tags[0].name == "blog"
