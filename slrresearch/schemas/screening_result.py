from typing import Literal

from pydantic import BaseModel, Field


class ScreeningResult(BaseModel):

    decision: Literal["include", "exclude", "uncertain"] = Field(
        description="Screening decision for the article"
    )

    justification: str = Field(
        description="Explanation of the screening decision"
    )

    matched_criteria: list[str] = Field(
        default_factory=list,
        description="Criteria that the article satisfies"
    )

    exclusion_reasons: list[str] = Field(
        default_factory=list,
        description="Reasons why the article should be excluded"
    )