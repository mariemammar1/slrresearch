
from slrresearch.schemas.technology import (
    TechnologyConcept,
    TechnologyExtractionResult,
)

from slrresearch.schemas.research_question import ResearchQuestion

from slrresearch.validators.technology_extraction_validator import (
    TechnologyExtractionValidator,
)


def create_research_questions():

    return [
        ResearchQuestion(
            id="RQ1",
            question="What are the applications of agentic AI in education?",
            rationale="Identify applications.",
        ),
        ResearchQuestion(
            id="RQ2",
            question="How does agentic AI affect learning?",
            rationale="Understand learning impact.",
        ),
    ]


def create_valid_result():

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
                keywords=["Educational settings"],
                related_rqs=["RQ1"],
            ),
        ],
    )


def test_valid_extraction():

    validator = TechnologyExtractionValidator()

    result = create_valid_result()
    questions = create_research_questions()

    errors = validator.validate(result, questions)

    assert errors == []


def test_invalid_category():

    validator = TechnologyExtractionValidator()

    result = create_valid_result()
    questions = create_research_questions()

    result.concepts[0].category = "Unknown"

    errors = validator.validate(result, questions)

    assert any("invalid category" in error for error in errors)


def test_unknown_research_question():

    validator = TechnologyExtractionValidator()

    result = create_valid_result()
    questions = create_research_questions()

    result.concepts[0].related_rqs = ["RQ99"]

    errors = validator.validate(result, questions)

    assert any("unknown research question" in error for error in errors)


def test_duplicate_concepts():

    validator = TechnologyExtractionValidator()

    result = create_valid_result()
    questions = create_research_questions()

    duplicate = TechnologyConcept(
        name="Agentic AI",
        category="Technology",
        keywords=["AI agents"],
        related_rqs=["RQ1"],
    )

    result.concepts.append(duplicate)

    errors = validator.validate(result, questions)

    assert "Duplicate concepts detected." in errors


def test_duplicate_keywords():

    validator = TechnologyExtractionValidator()

    result = create_valid_result()
    questions = create_research_questions()

    result.concepts[0].keywords = [
        "AI agents",
        "ai agents",
    ]

    errors = validator.validate(result, questions)

    assert any("duplicate keywords" in error for error in errors)


def test_empty_concept_name():

    validator = TechnologyExtractionValidator()

    result = create_valid_result()
    questions = create_research_questions()

    result.concepts[0].name = "   "

    errors = validator.validate(result, questions)

    assert any("Concept name is empty" in error for error in errors)


def test_wrong_topic_is_detected():

    validator = TechnologyExtractionValidator()
    result = create_valid_result()
    questions = create_research_questions()

    errors = validator.validate(
        result,
        questions,
        expected_topic="Artificial Intelligence in Healthcare",
        expected_objective="Analyze agentic AI in education.",
    )

    assert any(
        "topic does not match" in error
        for error in errors
    )


def test_wrong_objective_is_detected():

    validator = TechnologyExtractionValidator()
    result = create_valid_result()
    questions = create_research_questions()

    errors = validator.validate(
        result,
        questions,
        expected_topic="Agentic AI in Education",
        expected_objective="Study AI in healthcare.",
    )

    assert any(
        "objective does not match" in error
        for error in errors
    )

