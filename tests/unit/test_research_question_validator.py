
from slrresearch.schemas.research_question import (
    ResearchQuestion,
    ResearchQuestionResult,
)
from slrresearch.validators.research_question_validator import (
    ResearchQuestionValidator,
)


def create_valid_result():
    return ResearchQuestionResult(
        topic="Agentic AI in Education",
        objective="Analyze agentic AI in education.",
        research_questions=[
            ResearchQuestion(
                id="RQ1",
                question="What are the applications of agentic AI in education?",
                rationale="Identifies practical applications.",
            ),
            ResearchQuestion(
                id="RQ2",
                question="What architectures are used in agentic AI?",
                rationale="Explores technical architectures.",
            ),
            ResearchQuestion(
                id="RQ3",
                question="What are the challenges of agentic AI?",
                rationale="Identifies implementation challenges.",
            ),
        ],
    )


def test_valid_result():
    validator = ResearchQuestionValidator()
    result = create_valid_result()

    errors = validator.validate(result)

    assert errors == []


def test_invalid_number_of_questions():
    validator = ResearchQuestionValidator()
    result = create_valid_result()

    result.research_questions = result.research_questions[:2]

    errors = validator.validate(result)

    assert any(
        "between 3 and 5" in error for error in errors
    )


def test_invalid_identifiers():
    validator = ResearchQuestionValidator()
    result = create_valid_result()

    result.research_questions[1].id = "RQ5"

    errors = validator.validate(result)

    assert any(
        "identifiers" in error for error in errors
    )


def test_duplicate_questions():
    validator = ResearchQuestionValidator()
    result = create_valid_result()

    result.research_questions[1].question = (
        result.research_questions[0].question
    )

    errors = validator.validate(result)

    assert any(
        "Duplicate research questions" in error
        for error in errors
    )


def test_empty_topic():
    validator = ResearchQuestionValidator()
    result = create_valid_result()

    result.topic = "   "

    errors = validator.validate(result)

    assert any(
        "Research topic is empty" in error
        for error in errors
    )
