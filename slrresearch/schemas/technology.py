
from pydantic import BaseModel, Field


class TechnologyConcept(BaseModel):
    name: str = Field(
        description="The main concept identified"
    )

    category: str = Field(
        description="The category of the concept, "
                    "such as Technology, Domain, "
                    "Application or Outcome"
    )

    keywords: list[str] = Field(
        min_length=1,
        description="Alternative keywords and expressions "
                    "used in scientific literature"
    )

    related_rqs: list[str] = Field(
        min_length=1,
        description="Research question identifiers "
                    "related to this concept"
    )


class TechnologyExtractionResult(BaseModel):
    topic: str = Field(
        description="The original research topic"
    )

    objective: str = Field(
        description="The original research objective"
    )

    concepts: list[TechnologyConcept] = Field(
        min_length=1,
        description="The concepts extracted from "
                    "the research questions"
    )
