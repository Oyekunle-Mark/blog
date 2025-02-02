from pathlib import Path
from datetime import datetime
from typing import List
from .config import Post, Pages

class SitemapGenerator:
    def __init__(self, site_url: str):
        self.site_url = site_url.rstrip('/')

    def generate_sitemap(self, pages: Pages, output_dir: Path) -> Path:
        """Generate sitemap.xml"""
        urls = []

        # Add index page
        urls.append({
            'loc': self.site_url,
            'lastmod': datetime.now().date().isoformat()
        })

        # Add posts
        for post in pages.posts:
            urls.append({
                'loc': f"{self.site_url}/posts/{post.html_filename}",
                'lastmod': post.date.isoformat()[:10]  # Get YYYY-MM-DD format
            })

        # Add tag pages
        for tag in pages.tags:
            urls.append({
                'loc': f"{self.site_url}/{tag.html_filename}",
                'lastmod': max(p.date for p in tag.posts).isoformat()[:10]  # Get YYYY-MM-DD format
            })

        # Generate sitemap content
        sitemap_content = ['<?xml version="1.0" encoding="UTF-8"?>']
        sitemap_content.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')

        for url in urls:
            sitemap_content.append('  <url>')
            sitemap_content.append(f'    <loc>{url["loc"]}</loc>')
            sitemap_content.append(f'    <lastmod>{url["lastmod"]}</lastmod>')
            sitemap_content.append('  </url>')

        sitemap_content.append('</urlset>')

        # Write sitemap
        output_path = output_dir / 'sitemap.xml'
        output_path.write_text('\n'.join(sitemap_content))
        print(f"Generated sitemap: {output_path}")

        return output_path
