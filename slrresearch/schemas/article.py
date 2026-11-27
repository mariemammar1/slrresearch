
from pydantic import BaseModel, Field


class Article(BaseModel):

    title: str = Field(
        description="Title of the scientific article"
    )

    authors: list[str] = Field(
        default_factory=list,
        description="Authors of the article"
    )

    year: int | None = Field(
        default=None,
        description="Publication year"
    )

    doi: str | None = Field(
        default=None,
        description="Digital Object Identifier"
    )

    abstract: str | None = Field(
        default=None,
        description="Abstract of the article"
    )

    source: str = Field(
        description="Database source, such as OpenAlex or Crossref"
    )

    url: str | None = Field(
        default=None,
        description="URL of the article"
    )
