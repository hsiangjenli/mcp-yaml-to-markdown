from fastapi import FastAPI
from fastmcp import FastMCP

from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware

from pathlib import Path
import os

from .tool_generator import register_templates_from_directory

TITLE = os.getenv("MCP_TITLE", "Python MCP Template")
DESCRIPTION = os.getenv(
    "MCP_DESCRIPTION", "A template for creating MCP-compliant FastAPI"
)

# Templates directory - can be configured via environment variable
TEMPLATES_DIR = os.getenv("MCP_TEMPLATES_DIR", ".github/ISSUE_TEMPLATE")

app = FastAPI(
    title=TITLE,
    description=DESCRIPTION,
)

# Register all templates from the templates directory as FastAPI endpoints
# This must happen BEFORE creating the MCP server
templates_path = Path(TEMPLATES_DIR)
if templates_path.exists():
    register_templates_from_directory(app, templates_path)
else:
    print(f"Templates directory not found: {templates_path}")

# Create MCP server from FastAPI app (includes all registered endpoints as tools)
mcp = FastMCP.from_fastapi(app=app, stateless_http=True, json_response=True)

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

starlette_app.mount("/api", app=app)  # (Optional) Keep the original FastAPI app at /api
