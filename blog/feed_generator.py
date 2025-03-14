from pathlib import Path
from feedgen.feed import FeedGenerator as FG
from .config import Pages, Tag


class BlogFeedGenerator:
    def __init__(self, site_url: str, title: str, description: str):
        self.site_url = site_url.rstrip('/')
        self.title = title
        self.description = description

    def generate_main_feed(self, pages: Pages, output_dir: Path) -> Path:
        """Generate main RSS feed for all posts"""

        fg = FG()
        fg.title(self.title)
        fg.description(self.description)
        fg.link(href=self.site_url, rel='alternate')
        fg.link(href=f"{self.site_url}/feed.xml", rel='self')
        fg.language('en')

        # Add entries for each post
        for post in pages.posts:
            entry = fg.add_entry()
            entry.title(post.title)
            entry.link(href=f"{self.site_url}/posts/{post.html_filename}")
            entry.published(post.date.strftime('%Y-%m-%dT%H:%M:%SZ'))
            entry.content(post.content, type='html')

            # Add tags
            for tag in post.tags:
                entry.category(term=tag)

        # Write the feed
        output_path = output_dir / 'feed.xml'
        fg.rss_file(str(output_path))

        print(f"Generated main RSS feed: {output_path}")

        return output_path

    def generate_tag_feed(self, tag: Tag, output_dir: Path) -> Path:
        """Generate RSS feed for a specific tag"""

        fg = FG()
        fg.title(f"{self.title} - Posts tagged '{tag.name}'")
        fg.description(f"Posts tagged with '{tag.name}' from {self.title}")
        fg.link(href=f"{self.site_url}/{tag.html_filename}", rel='alternate')
        fg.link(href=f"{self.site_url}/feeds/{tag.name}.xml", rel='self')
        fg.language('en')

        # Add entries for each post with this tag
        for post in tag.posts:
            entry = fg.add_entry()
            entry.title(post.title)
            entry.link(href=f"{self.site_url}/posts/{post.html_filename}")
            entry.published(post.date.strftime('%Y-%m-%dT%H:%M:%SZ'))
            entry.content(post.content, type='html')

            # Add tags
            for tag_name in post.tags:
                entry.category(term=tag_name)

        # Write the feed
        feeds_dir = output_dir / 'feeds'
        feeds_dir.mkdir(exist_ok=True)
        output_path = feeds_dir / f"{tag.name}.xml"
        fg.rss_file(str(output_path))

        print(f"Generated tag RSS feed: {output_path}")

        return output_path
