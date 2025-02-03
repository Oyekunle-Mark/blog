[![Netlify Status](https://api.netlify.com/api/v1/badges/b7cadc8a-76d9-4a23-8f75-fb080436f27b/deploy-status)](https://app.netlify.com/sites/oyekunleblog/deploys)

# Blog

Source code of my personal website, found live at www.oyeoloyede.com

This is a hand-rolled Static Site Generator.

## Why hand-roll my own Static Site Generator?

It's kinda fun.

## Features

- Markdown files with YAML front matter
- Code syntax highlighting
- Tag system with dedicated tag pages
- Main RSS feed
- Tag-specific RSS feeds
- Sitemap generation
- Live development server
- Auto-rebuild on file changes
- Local preview at http://localhost:8000
- Test suites

## Dependencies

- **markdown**: Converts markdown files to HTML
- **pyyaml**: Parses YAML front matter in blog posts
- **jinja2**: HTML templating for the blog
- **pygments**: Code syntax highlighting
- **feedgen**: Generates RSS feeds
- **watchdog**: Enables live reloading during development (development only)
- **pytest**: Testing framework (development only)

## Commands

#### Build the blog
`poetry run blog build`

#### Start development server (default port 8000)
`poetry run blog serve`

#### Start server on different port
`poetry run blog serve --port 8080`

#### Start server without auto-rebuild
`poetry run blog serve --no-watch`

#### Clean generated files
`poetry run blog clean`

#### Run tests
`poetry run test`
