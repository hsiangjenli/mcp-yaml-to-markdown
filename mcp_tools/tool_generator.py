"""
Dynamically generate MCP tools from markdown templates.
"""

from pathlib import Path
from typing import Any
from pydantic import Field, create_model
from fastapi import FastAPI

from .template_parser import parse_template, render_template


def create_tool_from_template(
    app: FastAPI,
    template_path: Path | str,
    tool_name: str | None = None,
    remove_comments: bool = True,
):
    """
    Create a FastAPI endpoint from a markdown template.

    The endpoint will:
    - Parse the template to extract variables
    - Create a Pydantic model for input validation
    - Register the endpoint with FastAPI (which will be converted to MCP tool)

    Parameters
    ----------
    app : FastAPI
        The FastAPI app to register the endpoint with
    template_path : Path | str
        Path to the markdown template
    tool_name : str | None
        Custom tool name (defaults to template name)
    remove_comments : bool
        Whether to remove HTML comments from rendered output

    Returns
    -------
    The registered endpoint function
    """
    template_path = Path(template_path)
    parsed = parse_template(template_path)

    # Generate tool name from template name if not provided
    if tool_name is None:
        # Convert "🐞 Bug" to "bug_report" style
        name = parsed.name or template_path.stem
        # Remove emojis and special characters
        import re

        name = re.sub(r"[^\w\s]", "", name).strip().lower().replace(" ", "_")
        tool_name = f"create_{name}" if name else f"create_{template_path.stem}"

    # Build parameter info for the dynamic function
    param_info = []
    for var in parsed.variables:
        description = var.description
        if var.example:
            description += f"\n\nExample:\n{var.example}"
        param_info.append((var.name, description))

    # Create a Pydantic model for the input
    field_definitions = {}
    for name, desc in param_info:
        field_definitions[name] = (str, Field(description=desc))

    InputModel = create_model(
        f"{tool_name.title().replace('_', '')}Input", **field_definitions
    )

    # Store template_path in closure
    _template_path = str(template_path)
    _remove_comments = remove_comments
    _description = parsed.about or f"Create content from {parsed.name} template"

    # Create the endpoint function
    async def endpoint_func(input_data: InputModel) -> str:
        """Render the template with provided values."""
        return render_template(
            _template_path, input_data.model_dump(), remove_comments=_remove_comments
        )

    # Update function metadata
    endpoint_func.__name__ = tool_name
    endpoint_func.__doc__ = _description

    # Register with FastAPI as POST endpoint
    app.post(
        f"/{tool_name}",
        name=tool_name,
        description=_description,
        summary=parsed.name or tool_name,
        tags=["Template Tools"],
    )(endpoint_func)

    return endpoint_func


def register_templates_from_directory(
    app: FastAPI,
    templates_dir: Path | str,
    pattern: str = "*.md",
    remove_comments: bool = True,
):
    """
    Register all templates from a directory as FastAPI endpoints.

    Parameters
    ----------
    app : FastAPI
        The FastAPI app
    templates_dir : Path | str
        Directory containing templates
    pattern : str
        Glob pattern for template files
    remove_comments : bool
        Whether to remove HTML comments

    Returns
    -------
    list
        List of registered endpoint functions
    """
    templates_dir = Path(templates_dir)
    tools = []

    for template_path in templates_dir.glob(pattern):
        try:
            tool = create_tool_from_template(
                app, template_path, remove_comments=remove_comments
            )
            tools.append(tool)
            print(f"Registered endpoint from: {template_path}")
        except Exception as e:
            print(f"Failed to register {template_path}: {e}")

    return tools
