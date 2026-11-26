
from slrresearch.schemas.research_question import (
    ResearchQuestion,
    ResearchQuestionResult,
)
from slrresearch.agents.research_question_agent import (
    ResearchQuestionAgent,
)


def create_valid_result():
    return ResearchQuestionResult(
        topic="Agentic AI in Education",
        objective="Analyze agentic AI in education.",
        research_questions=[
            ResearchQuestion(
                id="RQ1",
                question="What are the applications of agentic AI?",
                rationale="Identifies applications.",
            ),
            ResearchQuestion(
                id="RQ2",
                question="What architectures are used?",
                rationale="Explores architectures.",
            ),
            ResearchQuestion(
                id="RQ3",
                question="What challenges exist?",
                rationale="Identifies challenges.",
            ),
        ],
    )


def create_invalid_result():
    result = create_valid_result()
    result.research_questions[1].id = "RQ5"
    return result


class FakeLLM:

    def __init__(self, responses):
        self.responses = responses

    def generate(
        self,
        system_prompt,
        user_prompt,
        response_format=None,
    ):
        response = self.responses.pop(0)

        if isinstance(response, Exception):
            raise response

        return response.model_dump()


def test_agent_accepted():
    fake_llm = FakeLLM([create_valid_result()])

    agent = ResearchQuestionAgent(llm_service=fake_llm)

    response = agent.run(
        topic="Agentic AI",
        objective="Analyze agentic AI.",
    )

    assert response["status"] == "accepted"
    assert response["repair_attempts"] == 0
    assert response["errors"] == []


def test_agent_repaired():
    fake_llm = FakeLLM([
        create_invalid_result(),
        create_valid_result(),
    ])

    agent = ResearchQuestionAgent(llm_service=fake_llm)

    response = agent.run(
        topic="Agentic AI",
        objective="Analyze agentic AI.",
    )

    assert response["status"] == "repaired"
    assert response["repair_attempts"] == 1
    assert response["errors"] == []


def test_agent_human_required():
    fake_llm = FakeLLM([
        create_invalid_result(),
        create_invalid_result(),
    ])

    agent = ResearchQuestionAgent(llm_service=fake_llm)

    response = agent.run(
        topic="Agentic AI",
        objective="Analyze agentic AI.",
    )

    assert response["status"] == "human_required"
    assert response["repair_attempts"] == 1
    assert response["errors"] != []


def test_agent_repair_exception():
    fake_llm = FakeLLM([
        create_invalid_result(),
        RuntimeError("Simulated LLM failure"),
    ])

    agent = ResearchQuestionAgent(llm_service=fake_llm)

    response = agent.run(
        topic="Agentic AI",
        objective="Analyze agentic AI.",
    )

    assert response["status"] == "human_required"
    assert response["repair_attempts"] == 1
    assert "repair_error" in response
