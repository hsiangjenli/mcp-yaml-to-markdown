"""Generate FastAPI endpoints from templates."""

import re
from fastapi import FastAPI
from pydantic import Field, create_model

from .models import Template
from .parser import parse, render


def _slugify(text: str) -> str:
    """Convert text to a valid function/endpoint name."""
    # Remove emojis and special characters, convert to lowercase
    slug = re.sub(r"[^\w\s]", "", text).strip().lower().replace(" ", "_")
    return slug or "template"


def _create_input_model(tool_name: str, template: Template):
    """Create a Pydantic model for the tool's input parameters."""
    fields = {}

    for var in template.variables:
        description = var.description
        if var.example:
            description += f"\n\nExample:\n{var.example}"
        fields[var.name] = (str, Field(description=description))

    return create_model(f"{tool_name.title().replace('_', '')}Input", **fields)


def register_template(
    app: FastAPI,
    template: Template,
    *,
    tool_name: str | None = None,
    remove_comments: bool = True,
) -> None:
    """
    Register a template as a FastAPI endpoint.

    Args:
        app: FastAPI application
        template: Parsed template
        tool_name: Custom endpoint name (default: derived from template name)
        remove_comments: Whether to remove HTML comments in output
    """
    # Parse template if not already parsed
    if not template.variables:
        template = parse(template)

    # Generate tool name
    name = tool_name or f"create_{_slugify(template.name)}"
    description = template.about or f"Create content from {template.name} template"

    # Create input model
    InputModel = _create_input_model(name, template)

    # Capture in closure
    _template = template
    _remove_comments = remove_comments

    async def endpoint(input_data: InputModel) -> str:  # type: ignore[valid-type]
        return render(
            _template, input_data.model_dump(), remove_comments=_remove_comments
        )

    # Set metadata
    endpoint.__name__ = name
    endpoint.__doc__ = description

    # Register endpoint
    app.post(
        f"/{name}",
        name=name,
        description=description,
        summary=template.name or name,
        tags=["Template Tools"],
    )(endpoint)
