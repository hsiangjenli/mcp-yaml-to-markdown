"""
MCP server for markdown templates.

Loads templates from configured sources and exposes them as MCP tools.
"""

import os
from pathlib import Path

from fastapi import FastAPI
from fastmcp import FastMCP
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware

from .loader import load, is_url
from .parser import parse
from .generator import register_template

# Configuration from environment
TITLE = os.getenv("MCP_TITLE", "Python MCP Template")
DESCRIPTION = os.getenv(
    "MCP_DESCRIPTION", "A template for creating MCP-compliant FastAPI"
)
TEMPLATES_SOURCE = os.getenv("MCP_TEMPLATES_SOURCE", ".github/ISSUE_TEMPLATE")

# FastAPI app
app = FastAPI(title=TITLE, description=DESCRIPTION)


def register_from_source(source: str) -> int:
    """
    Register templates from a source.

    Returns the number of templates registered.
    """
    count = 0

    for template in load(source):
        try:
            parsed = parse(template)
            register_template(app, parsed)
            print(f"  ✓ Registered: {parsed.name} from {template.source}")
            count += 1
        except Exception as e:
            print(f"  ✗ Failed: {template.source} - {e}")

    return count


def _should_use_loader(source: str) -> bool:
    """Check if source needs the loader (URL or non-existent local path)."""
    if is_url(source):
        return True
    path = Path(source)
    return path.exists()


# Load templates from configured sources (comma-separated)
print(f"Loading templates from: {TEMPLATES_SOURCE}")
for source in (s.strip() for s in TEMPLATES_SOURCE.split(",") if s.strip()):
    try:
        if _should_use_loader(source):
            register_from_source(source)
        else:
            print(f"  ✗ Source not found: {source}")
    except Exception as e:
        print(f"  ✗ Error loading {source}: {e}")

# Create MCP server
mcp = FastMCP.from_fastapi(app=app, stateless_http=True, json_response=True)

# Starlette app with CORS middleware
starlette_app = mcp.http_app(
    middleware=[
        Middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
    ]
)

# Mount FastAPI at /api for direct access
starlette_app.mount("/api", app=app)
