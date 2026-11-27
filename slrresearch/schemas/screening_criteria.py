from pydantic import BaseModel, Field


class ScreeningCriteria(BaseModel):

    inclusion_criteria: list[str] = Field(
        description="Conditions an article must satisfy to be included"
    )

    exclusion_criteria: list[str] = Field(
        description="Conditions that disqualify an article from the review"
    )