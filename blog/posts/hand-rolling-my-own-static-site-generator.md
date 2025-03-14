---
title: "Hand-Rolling My Own Static Site Generator"
date: 2025-03-14
tags: ["projects"]
---

I am still new to photography, so I naturally searched for resources that would provide the basics I needed to use my digital camera independently. The first resource I found was the [Hugo](https://gohugo.io/) website. That website helped me understand and apply fundamental photography concepts like the Exposure Triangle and image processing.

The personal blog you are reading was built with the Static Site Generator(SSG) originally. When I started this personal blog last year, that was the right choice as it allowed me to focus on writing and orginising my writings. I like having fine control over my tools, and Hugo has since gotten in my way a few times. I have also needed to spend some time understanding how to use Hugo to get the most from needs. I believed that for my simple needs, I needed a lightweight alternative that allowed me bend it to my will as much as I liked. This is the motivation for writing my own static site generator.

This post will walkthrough the implementation and functionalities of the static site generator(referred to as SSG for the rest of the post) I wrote to satisfy the need outlined in the previous paragraph.

An SSG is a simple project. The kind you knock-off in an evening using tools you are familiar with. I did just that with this project. This SSG is written in Python, a language I use heavily at work and play. 

## Dependencies

This project relies on the following Python libraries:

1. **markdown**: converts markdown files to HTML
2. **pyyaml**: parses YAML front matter in blog posts
3. **jinja2**: for HTML templating
4. **pygments**: for code syntax highlighting
5. **feedgen**: generates RSS feeds
6. **watchdog**: enables live reloading during development (development only)
7. **pytest**: the testing framework (development only)

With these libraries in place, the remaining effort is to write the code that orchestrates how files markdown files created to HTML files, along with other blog convenience features like enforcing a tags system and code syntax highlighting. 

## Markdown files conversion

I write my blog posts in markdown. It's a convenient file format. The main task the SSG would be performing is to convert these markdown files into HTML files for the browser. I created three classes for organising the data: `Post`, `Tag` and `Pages`. They are container classes and allow me pass data around cleanly.

A blog post(like this one you're reading) starts its life as a markdown file in the `posts` folder. All the markdown files in the `posts` folder gets read and marshalled into the `Post` class. From the `Post` classes created from all the markdown files, tags are extracted and marshalled into `Tag` classes. The `Pages` class organises tags and posts for the index page. A flow of this build can be seen in the `main` build function:

```py
def main():
    """The build function.
    Uses all the right classes and utilities to perform markdown to HTML conversion.
    Also generates the CSS, RSS feeds and sitemap.xml files.
    """

    # Get project root directory
    project_root = Path(__file__).parent.parent

    # Setup paths
    posts_dir = project_root / "blog" / "posts"
    static_dir = project_root / "static"
    templates_dir = project_root / "blog" / "templates"
    css_dir = project_root / "static" / "css"

    # Cleanup previously generated files
    cleanup_generated_files(static_dir)

    # Generate CSS files
    try:
        css_generator = CssGenerator(str(css_dir))
        css_generator.generate_pygments_css()
    except Exception as e:
        print(f"Warning: Failed to generate CSS: {e}")

    try:
        # Build pages from markdown files
        builder = PageBuilder(str(posts_dir))
        pages = builder.build_pages()

        # Write all pages
        writer = PageWriter(
            output_dir=str(static_dir / "posts"),
            templates_dir=str(templates_dir),
            site_url="https://www.oyeoloyede.com"
        )
        successful_count = writer.write_all(pages)

        # Print final summary
        print(f"\nTotal posts generated: {successful_count}")

        return 0 if successful_count > 0 else 1
    except Exception as e:
        print(f"\nError during processing: {str(e)}")
        return 1
```

The flow of this function is as follows:

1. Set the relevant directories.
2. Cleanup the files generated from the last build with the call to `cleanup_generated_files`
3. Create CSS files using the `CssGenerator` class.
4. Build the posts from markdown files. The `PageBuilder` class uses the **markdown** library to convert the markdown files into HTML strings. Tags and post metadata(title, date, etc) are also embedded into the markdown files as YAML front matter so the **yaml** library parses this front matter to a Python dict. `PageBuilder` delegates this coordination of extracting metadata and post content from the markdown file to a `MarkdownConverter` class.
5. The pages produced by `PageBuilder` are passed to `PageWriter` which, as you would expect, writes out all the blog content, including RSS feeds and sitemap files. `PageWriter` delegates building sitemaps and RSS feeds to the `SitemapGenerator` and `BlogFeedGenerator` class respectively. **jinja** templates are used for writing out the HTML files to enable as much reuse as possible, and there is a dedicated `TemplateHandler` class that `PageWriter` employs for handling template related tasks.
6. Report result of build.

## Styling

A `style.css` file is maintained in the `/static/css` folder. This file provides the styling for the entire blog.

Code syntax highlighting is provided by using the _codehilite_ **markdown** extension and generating a styling sheet with **pygments**.

## Development live server

Using the **watchdog** library, a development live server is provided. This also includes live reloading and building of the posts when a change is made to any markdown file. This makes for a pleasant writing experience as I can preview my content as I write.

## Conclusion

My requirement of having a minimalist static site generator capable of providing my blogging needs has been satisfied with this project. It is also a fun little distraction for an evening. In less than the time it would have taken me to get acclimitized with the documentation of any of the free, popular open source static site generators, I have spun up a tiny SSG that meets my needs. This is also something that can be hacked and remolded to meet any future need. I suspect there are more SSG hand-rolling in my future :)

You can find the full source of the SSG described in this post [on my GitHub](https://github.com/Oyekunle-Mark/blog).
