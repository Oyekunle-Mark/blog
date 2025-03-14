import os
import http.server
import socketserver
import webbrowser
from pathlib import Path
from typing import Optional
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from .build import main as build_site


class BlogServerHandler(http.server.SimpleHTTPRequestHandler):
    """Custom request handler that sets headers for development"""

    def end_headers(self):
        # Add headers to prevent caching during development
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()


class BlogBuilder(FileSystemEventHandler):
    """Handles file system events to trigger rebuilds"""

    def on_modified(self, event):
        if event.src_path.endswith('.md'):
            print(f"\nDetected changes in {event.src_path}")
            build_site()


class DevServer:
    """Development server with auto-rebuild capability"""

    def __init__(self, static_dir: Path, port: int = 8000):
        self.static_dir = static_dir
        self.port = port
        self.server: Optional[socketserver.TCPServer] = None
        self.observer: Optional[Observer] = None

    def start(self, watch: bool = True):
        """Start the development server and optionally watch for changes"""
        # Ensure we're serving from the static directory
        os.chdir(self.static_dir)

        # Create the server
        handler = BlogServerHandler
        self.server = socketserver.TCPServer(("", self.port), handler)

        # Set up file watching if requested
        if watch:
            self.observer = Observer()
            self.observer.schedule(
                BlogBuilder(),
                str(self.static_dir.parent / "blog" / "posts"),
                recursive=False
            )
            self.observer.start()

        # Open the browser
        webbrowser.open(f"http://localhost:{self.port}")

        print(f"\nServing at http://localhost:{self.port}")
        print("Press Ctrl+C to stop")

        try:
            self.server.serve_forever()
        except KeyboardInterrupt:
            self.stop()

    def stop(self):
        """Stop the server and file watcher"""
        if self.observer:
            self.observer.stop()
            self.observer.join()

        if self.server:
            self.server.shutdown()
            self.server.server_close()

        print("\nServer stopped")
