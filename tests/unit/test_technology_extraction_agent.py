
import pytest

from slrresearch.agents.technology_extraction_agent import (
    TechnologyExtractionAgent,
)

from slrresearch.schemas.research_question import ResearchQuestion

from slrresearch.schemas.technology import (
    TechnologyConcept,
    TechnologyExtractionResult,
)


# --------------------------------------------------
# 1. Fake LLM
# --------------------------------------------------

class FakeLLM:

    def __init__(self, responses):
        self.responses = responses

    def generate(self, **kwargs):
        response = self.responses.pop(0)

        if isinstance(response, Exception):
            raise response

        return response.model_dump()


# --------------------------------------------------
# 2. Test data
# --------------------------------------------------

def create_research_questions():

    return [
        ResearchQuestion(
            id="RQ1",
            question="What are the applications of agentic AI in education?",
            rationale="Identify educational applications.",
        ),
        ResearchQuestion(
            id="RQ2",
            question="How does agentic AI affect learning?",
            rationale="Understand its impact on learning.",
        ),
        ResearchQuestion(
            id="RQ3",
            question="What challenges affect the adoption of agentic AI?",
            rationale="Identify adoption challenges.",
        ),
    ]


def create_valid_extraction():

    return TechnologyExtractionResult(
        topic="Agentic AI in Education",
        objective="Analyze agentic AI in education.",
        concepts=[
            TechnologyConcept(
                name="Agentic AI",
                category="Technology",
                keywords=["AI agents", "Autonomous agents"],
                related_rqs=["RQ1", "RQ2"],
            ),
            TechnologyConcept(
                name="Education",
                category="Domain",
                keywords=["Educational settings", "Learning environments"],
                related_rqs=["RQ1", "RQ3"],
            ),
            TechnologyConcept(
                name="Applications",
                category="Application",
                keywords=["Use cases", "Educational tasks"],
                related_rqs=["RQ1"],
            ),
        ],
    )


def create_invalid_extraction():

    result = create_valid_extraction()

    data = result.model_dump()

    # RQ99 does not exist in our research questions
    data["concepts"][0]["related_rqs"] = ["RQ99"]

    return TechnologyExtractionResult.model_validate(data)


# --------------------------------------------------
# 3. Tests
# --------------------------------------------------

def test_agent_accepts_valid_extraction():

    questions = create_research_questions()
    valid_result = create_valid_extraction()

    fake_llm = FakeLLM([valid_result])

    agent = TechnologyExtractionAgent(
        llm_service=fake_llm
    )

    response = agent.run(
        topic="Agentic AI in Education",
        objective="Analyze agentic AI in education.",
        research_questions=questions,
    )

    assert response["status"] == "accepted"
    assert response["repair_attempts"] == 0
    assert response["errors"] == []


def test_agent_repairs_invalid_extraction():

    questions = create_research_questions()

    invalid_result = create_invalid_extraction()
    valid_result = create_valid_extraction()

    fake_llm = FakeLLM([
        invalid_result,
        valid_result,
    ])

    agent = TechnologyExtractionAgent(
        llm_service=fake_llm
    )

    response = agent.run(
        topic="Agentic AI in Education",
        objective="Analyze agentic AI in education.",
        research_questions=questions,
    )

    assert response["status"] == "repaired"
    assert response["repair_attempts"] == 1
    assert response["errors"] == []


def test_agent_requires_human_after_failed_repair():

    questions = create_research_questions()

    invalid_result = create_invalid_extraction()

    fake_llm = FakeLLM([
        invalid_result,
        invalid_result,
    ])

    agent = TechnologyExtractionAgent(
        llm_service=fake_llm
    )

    response = agent.run(
        topic="Agentic AI in Education",
        objective="Analyze agentic AI in education.",
        research_questions=questions,
    )

    assert response["status"] == "human_required"
    assert response["repair_attempts"] == 1
    assert len(response["errors"]) > 0


def test_agent_requires_human_when_repair_raises_error():

    questions = create_research_questions()

    invalid_result = create_invalid_extraction()

    fake_llm = FakeLLM([
        invalid_result,
        RuntimeError("LLM repair failed"),
    ])

    agent = TechnologyExtractionAgent(
        llm_service=fake_llm
    )

    response = agent.run(
        topic="Agentic AI in Education",
        objective="Analyze agentic AI in education.",
        research_questions=questions,
    )

    assert response["status"] == "human_required"
    assert response["repair_attempts"] == 1
    assert "repair_error" in response
