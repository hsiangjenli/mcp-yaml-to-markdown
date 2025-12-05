"""Data models for template parsing."""

from pydantic import BaseModel, Field


class TemplateVariable(BaseModel):
    """A variable extracted from a template."""

    name: str
    description: str = ""
    example: str = ""


class Template(BaseModel):
    """A parsed markdown template."""

    name: str = ""
    about: str = ""
    content: str = ""
    source: str = ""  # Where the template came from
    variables: list[TemplateVariable] = Field(default_factory=list)

    @property
    def variable_names(self) -> list[str]:
        return [v.name for v in self.variables]
