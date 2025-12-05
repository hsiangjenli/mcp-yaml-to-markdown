"""
Main entry point for the MCP server.

Re-exports from server module for backwards compatibility.
"""

from .server import app, mcp, starlette_app

__all__ = ["app", "mcp", "starlette_app"]
