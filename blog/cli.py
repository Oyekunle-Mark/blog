import click
from pathlib import Path
from .build import main as build_site, cleanup_generated_files
from .dev_server import DevServer

@click.group()
def cli():
    """Blog management CLI"""
    pass

@cli.command()
def build():
    """Build the blog"""
    return build_site()

@cli.command()
@click.option('--port', '-p', default=8000, help='Port to serve on')
@click.option('--no-watch', is_flag=True, help='Disable auto-rebuild on changes')
def serve(port: int, no_watch: bool):
    """Start development server"""
    project_root = Path(__file__).parent.parent
    static_dir = project_root / "static"

    # Ensure site is built
    build_site()

    # Start the server
    server = DevServer(static_dir, port)
    server.start(watch=not no_watch)

@cli.command()
def clean():
    """Clean all generated files"""
    project_root = Path(__file__).parent.parent
    static_dir = project_root / "static"
    cleanup_generated_files(static_dir)
