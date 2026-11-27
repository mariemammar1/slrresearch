
from slrresearch.agents.screening_agent import ScreeningAgent

from slrresearch.schemas.article import Article
from slrresearch.schemas.screening_criteria import ScreeningCriteria


class FakeLLM:

    def __init__(self, response):
        self.response = response

    def generate(self, **kwargs):
        return self.response


def create_article():
    return Article(
        title="Agentic AI in Education",
        authors=["John Smith"],
        year=2025,
        abstract=(
            "This article explores the applications of "
            "Agentic AI in educational environments."
        ),
        source="OpenAlex",
        url="https://example.com/article"
    )


def create_criteria():
    return ScreeningCriteria(
        inclusion_criteria=[
            "Focuses on Agentic AI in Education",
            "Presents an educational application"
        ],
        exclusion_criteria=[
            "Does not concern education",
            "Does not address agentic AI"
        ]
    )


def test_screening_agent_accepts_valid_include():

    fake_llm = FakeLLM({
        "decision": "include",
        "justification": "The article presents an educational application of Agentic AI.",
        "matched_criteria": [
            "Focuses on Agentic AI in Education",
            "Presents an educational application"
        ],
        "exclusion_reasons": []
    })

    agent = ScreeningAgent(llm_service=fake_llm)

    response = agent.screen_article(
        article=create_article(),
        criteria=create_criteria()
    )

    assert response["status"] == "accepted"
    assert response["result"].decision == "include"


def test_screening_agent_accepts_valid_exclude():

    fake_llm = FakeLLM({
        "decision": "exclude",
        "justification": "The article does not concern education.",
        "matched_criteria": [],
        "exclusion_reasons": [
            "Does not concern education"
        ]
    })

    agent = ScreeningAgent(llm_service=fake_llm)

    response = agent.screen_article(
        article=create_article(),
        criteria=create_criteria()
    )

    assert response["status"] == "accepted"
    assert response["result"].decision == "exclude"


def test_screening_agent_accepts_uncertain():

    fake_llm = FakeLLM({
        "decision": "uncertain",
        "justification": "The abstract does not provide enough information.",
        "matched_criteria": [],
        "exclusion_reasons": []
    })

    agent = ScreeningAgent(llm_service=fake_llm)

    response = agent.screen_article(
        article=create_article(),
        criteria=create_criteria()
    )

    assert response["status"] == "accepted"
    assert response["result"].decision == "uncertain"


def test_screening_agent_rejects_invalid_result():

    fake_llm = FakeLLM({
        "decision": "exclude",
        "justification": "The article is not relevant.",
        "matched_criteria": [],
        "exclusion_reasons": []
    })

    agent = ScreeningAgent(llm_service=fake_llm)

    response = agent.screen_article(
        article=create_article(),
        criteria=create_criteria()
    )

    assert response["status"] == "invalid"
    assert len(response["errors"]) > 0
