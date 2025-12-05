"""MCP Tools - Generate MCP tools from markdown templates."""

from .models import Template, TemplateVariable
from .loader import (
    load,
    load_from_url,
    load_from_path,
    load_from_directory,
    is_url,
)
from .parser import parse, render
from .generator import register_template
from .server import app, mcp, starlette_app

__all__ = [
    # Models
    "Template",
    "TemplateVariable",
    # Loader
    "load",
    "load_from_url",
    "load_from_path",
    "load_from_directory",
    "is_url",
    # Parser
    "parse",
    "render",
    # Generator
    "register_template",
    # Server
    "app",
    "mcp",
    "starlette_app",
]
