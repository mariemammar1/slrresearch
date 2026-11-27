
from slrresearch.agents.search_strategy_agent import (
    SearchStrategyAgent,
)

from slrresearch.schemas.search_strategy import (
    SearchQuery,
    SearchStrategyResult,
)

from slrresearch.schemas.technology import (
    TechnologyConcept,
)

from slrresearch.schemas.research_question import (
    ResearchQuestion,
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

def create_concepts():

    return [
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
    ]


def create_research_questions():

    return [
        ResearchQuestion(
            id="RQ1",
            question="What are the applications of agentic AI in education?",
            rationale="Identify applications.",
        ),
        ResearchQuestion(
            id="RQ2",
            question="What architectures do AI agents use?",
            rationale="Analyze architectures.",
        ),
        ResearchQuestion(
            id="RQ3",
            question="What challenges affect adoption?",
            rationale="Identify challenges.",
        ),
    ]


def create_valid_result():

    return SearchStrategyResult(
        topic="Agentic AI in Education",
        search_queries=[
            SearchQuery(
                query=(
                    '("AI agents" OR "Autonomous agents") '
                    'AND ("Educational settings" OR "Learning environments")'
                ),
                related_concepts=["Agentic AI", "Education"],
                related_rqs=["RQ1", "RQ2", "RQ3"],
            )
        ],
    )


def create_invalid_result():

    result = create_valid_result()

    data = result.model_dump()

    # Unknown concept
    data["search_queries"][0]["related_concepts"] = [
        "Agentic AI",
        "Unknown Concept",
    ]

    return SearchStrategyResult.model_validate(data)


# --------------------------------------------------
# 3. Tests
# --------------------------------------------------

def test_agent_accepts_valid_strategy():

    concepts = create_concepts()
    questions = create_research_questions()

    fake_llm = FakeLLM([
        create_valid_result()
    ])

    agent = SearchStrategyAgent(
        llm_service=fake_llm
    )

    response = agent.run(
        topic="Agentic AI in Education",
        concepts=concepts,
        research_questions=questions,
    )

    assert response["status"] == "accepted"
    assert response["repair_attempts"] == 0
    assert response["errors"] == []


def test_agent_repairs_invalid_strategy():

    concepts = create_concepts()
    questions = create_research_questions()

    fake_llm = FakeLLM([
        create_invalid_result(),
        create_valid_result(),
    ])

    agent = SearchStrategyAgent(
        llm_service=fake_llm
    )

    response = agent.run(
        topic="Agentic AI in Education",
        concepts=concepts,
        research_questions=questions,
    )

    assert response["status"] == "repaired"
    assert response["repair_attempts"] == 1
    assert response["errors"] == []


def test_agent_requires_human_after_failed_repair():

    concepts = create_concepts()
    questions = create_research_questions()

    fake_llm = FakeLLM([
        create_invalid_result(),
        create_invalid_result(),
    ])

    agent = SearchStrategyAgent(
        llm_service=fake_llm
    )

    response = agent.run(
        topic="Agentic AI in Education",
        concepts=concepts,
        research_questions=questions,
    )

    assert response["status"] == "human_required"
    assert response["repair_attempts"] == 1
    assert len(response["errors"]) > 0


def test_agent_handles_repair_exception():

    concepts = create_concepts()
    questions = create_research_questions()

    fake_llm = FakeLLM([
        create_invalid_result(),
        RuntimeError("LLM repair failed"),
    ])

    agent = SearchStrategyAgent(
        llm_service=fake_llm
    )

    response = agent.run(
        topic="Agentic AI in Education",
        concepts=concepts,
        research_questions=questions,
    )

    assert response["status"] == "human_required"
    assert response["repair_attempts"] == 1
    assert "repair_error" in response
