
from pydantic import BaseModel, Field


class Paper(BaseModel):
    title: str = Field(min_length=1)

    authors: list[str] = Field(default_factory=list)
    year: int | None = None
    abstract: str | None = None
    doi: str | None = None
    source: str | None = None
    external_id: str | None = None

    keywords: list[str] = Field(default_factory=list)
    journal: str | None = None
    url: str | None = None
