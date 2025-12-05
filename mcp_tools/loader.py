"""Load templates from various sources (local files, directories, URLs)."""

import httpx
from pathlib import Path
from typing import Iterator
from urllib.parse import urlparse

from .models import Template


def is_url(source: str) -> bool:
    """Check if source is a URL."""
    parsed = urlparse(source)
    return parsed.scheme in ("http", "https")


def fetch_url(url: str, timeout: int = 30) -> str:
    """Fetch content from a URL."""
    with httpx.Client(follow_redirects=True, timeout=timeout) as client:
        response = client.get(url)
        response.raise_for_status()
        return response.text


def load_from_path(path: Path) -> Template:
    """Load a template from a local file."""
    return Template(
        name=path.stem,
        content=path.read_text(encoding="utf-8"),
        source=str(path),
    )


def load_from_url(url: str) -> Template:
    """Load a template from a URL."""
    parsed = urlparse(url)
    name = Path(parsed.path).stem or "template"

    return Template(
        name=name,
        content=fetch_url(url),
        source=url,
    )


def load_from_directory(directory: Path, pattern: str = "*.md") -> Iterator[Template]:
    """Load all templates from a directory."""
    for path in directory.glob(pattern):
        if path.is_file():
            yield load_from_path(path)


def load(source: str, pattern: str = "*.md") -> Iterator[Template]:
    """
    Load templates from a source.

    Supports:
    - URL: https://example.com/template.md
    - Local file: /path/to/template.md
    - Local directory: /path/to/templates/

    Args:
        source: Path or URL to load from
        pattern: Glob pattern for directories (default: "*.md")

    Yields:
        Template objects
    """
    if is_url(source):
        yield load_from_url(source)
        return

    path = Path(source)

    if path.is_file():
        yield load_from_path(path)
    elif path.is_dir():
        yield from load_from_directory(path, pattern)
    else:
        raise ValueError(f"Invalid source: {source}")
