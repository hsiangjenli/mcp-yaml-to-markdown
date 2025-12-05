#!/bin/bash

echo "Building documentation..."

echo "Step 1: Exporting OpenAPI schema..."
uv run scripts/export_openapi.py

echo "Step 2: Converting OpenAPI to Markdown..."
uv run scripts/openapi_to_markdown.py

echo "Documentation build complete!"