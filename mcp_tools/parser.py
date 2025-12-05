"""Parse markdown templates and extract variables."""

import re
from jinja2 import Environment, StrictUndefined

from .models import Template, TemplateVariable

# Regex patterns
FRONTMATTER_PATTERN = re.compile(r"^---\s*\n(.*?)\n---", re.DOTALL)
VARIABLE_PATTERN = re.compile(r"<([a-z][a-z0-9_]*)>")
SECTION_PATTERN = re.compile(r"(###\s*[^:\n]+:)")
COMMENT_PATTERN = re.compile(r"<!--[\s\S]*?-->")


def _extract_frontmatter(content: str) -> dict[str, str]:
    """Extract YAML frontmatter fields."""
    match = FRONTMATTER_PATTERN.match(content)
    if not match:
        return {}

    frontmatter = match.group(1)
    result = {}

    for field in ("name", "about"):
        field_match = re.search(rf"^{field}:\s*(.+)$", frontmatter, re.MULTILINE)
        if field_match:
            result[field] = field_match.group(1).strip()

    return result


def _extract_sections(content: str) -> dict[str, str]:
    """Extract markdown sections (### Header:) and their content."""
    parts = SECTION_PATTERN.split(content)
    sections = {}

    for i in range(1, len(parts), 2):
        if i + 1 < len(parts):
            header = re.sub(r"^###\s*|\s*:$", "", parts[i].strip())
            sections[header] = parts[i + 1]

    return sections


def _extract_variable_info(
    var_name: str, sections: dict[str, str], content: str
) -> TemplateVariable:
    """Extract description and example for a variable."""
    var = TemplateVariable(name=var_name)

    # Find which section contains this variable
    for section_name, section_content in sections.items():
        if f"<{var_name}>" not in section_content:
            continue

        var.description = section_name

        # Look for comment before the variable
        comment_match = re.search(rf"<!--([\s\S]*?)-->\s*<{var_name}>", section_content)
        if comment_match:
            comment = comment_match.group(1).strip()
            example_match = re.search(r"Example:?\s*([\s\S]*)", comment, re.IGNORECASE)

            if example_match:
                var.example = example_match.group(1).strip()
            else:
                var.description = f"{section_name}: {comment}"
        break

    # Handle frontmatter variables (like title)
    if not var.description and re.search(
        rf"title:\s*'[^']*<{var_name}>[^']*'", content
    ):
        var.description = "Issue title"

    return var


def parse(template: Template) -> Template:
    """
    Parse a template and extract variables with their metadata.

    Args:
        template: Template with raw content

    Returns:
        Template with parsed variables, name, and about
    """
    content = template.content
    frontmatter = _extract_frontmatter(content)
    sections = _extract_sections(content)

    # Find unique variables (preserve order)
    var_names = list(dict.fromkeys(VARIABLE_PATTERN.findall(content)))

    # Extract info for each variable
    variables = [_extract_variable_info(name, sections, content) for name in var_names]

    return Template(
        name=frontmatter.get("name", template.name),
        about=frontmatter.get("about", ""),
        content=content,
        source=template.source,
        variables=variables,
    )


def render(
    template: Template, values: dict[str, str], remove_comments: bool = True
) -> str:
    """
    Render a template with the given values.

    Args:
        template: Parsed template
        values: Variable values to substitute
        remove_comments: Whether to remove HTML comments

    Returns:
        Rendered markdown string
    """
    content = template.content

    # Temporarily replace comments to avoid Jinja2 parsing issues
    comments: list[str] = []

    def save_comment(match: re.Match) -> str:
        comments.append(match.group(0))
        return f"__COMMENT_{len(comments) - 1}__"

    escaped = COMMENT_PATTERN.sub(save_comment, content)

    # Render with custom delimiters for <variable> syntax
    env = Environment(
        undefined=StrictUndefined,
        autoescape=False,
        keep_trailing_newline=True,
        variable_start_string="<",
        variable_end_string=">",
    )
    rendered = env.from_string(escaped).render(**values)

    # Handle comments
    if remove_comments:
        rendered = re.sub(r"__COMMENT_\d+__\s*\n?", "", rendered)
    else:
        for i, comment in enumerate(comments):
            rendered = rendered.replace(f"__COMMENT_{i}__", comment)

    return rendered
