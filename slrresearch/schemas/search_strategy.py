
from pydantic import BaseModel, Field


class SearchQuery(BaseModel):

    query: str = Field(
        description="The Boolean search query"
    )

    related_concepts: list[str] = Field(
        min_length=1,
        description="Concepts used in this query"
    )

    related_rqs: list[str] = Field(
        min_length=1,
        description="Research questions addressed by this query"
    )


class SearchStrategyResult(BaseModel):

    topic: str = Field(
        description="The original research topic"
    )

    search_queries: list[SearchQuery] = Field(
        min_length=1,
        description="Generated Boolean search queries"
    )
