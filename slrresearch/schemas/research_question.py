from pydantic import BaseModel, Field


class ResearchQuestion(BaseModel):
    id: str = Field(description="Research question identifier, e.g. RQ1")
    question: str = Field(description="The research question")
    rationale: str = Field(description="Why this research question is relevant")


class ResearchQuestionResult(BaseModel):
    topic: str = Field(description="The research topic")
    objective: str = Field(description="The research objective")
    research_questions: list[ResearchQuestion] = Field(
        min_length=1,
        description="List of generated research questions"
    )