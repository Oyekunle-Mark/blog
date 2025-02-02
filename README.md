[![Netlify Status](https://api.netlify.com/api/v1/badges/b7cadc8a-76d9-4a23-8f75-fb080436f27b/deploy-status)](https://app.netlify.com/sites/oyekunleblog/deploys)

# Blog

Source code of my personal website.

Found live at www.oyeoloyede.com

This blog is custom built. The `markdown`, `pyyaml` and `jinja2` Python libraries provide support for markdown file conversion to HTML, post metadata parsing, and HTML templating respectively. Everything else has been stitched together to produce a minimalist Python static site generator.

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
