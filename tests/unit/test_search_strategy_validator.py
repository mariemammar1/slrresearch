
from slrresearch.validators.search_strategy_validator import (
    SearchStrategyValidator,
)

from slrresearch.schemas.search_strategy import (
    SearchQuery,
    SearchStrategyResult,
)

from slrresearch.schemas.technology import TechnologyConcept


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
            keywords=["Educational settings"],
            related_rqs=["RQ1"],
        ),
    ]


def create_valid_result():

    return SearchStrategyResult(
        topic="Agentic AI in Education",
        search_queries=[
            SearchQuery(
                query=(
                    '("AI agents" OR "Autonomous agents") '
                    'AND ("Educational settings")'
                ),
                related_concepts=["Agentic AI", "Education"],
                related_rqs=["RQ1", "RQ2"],
            )
        ],
    )


def test_valid_search_strategy():

    validator = SearchStrategyValidator()

    errors = validator.validate(
        result=create_valid_result(),
        concepts=create_concepts(),
        valid_rq_ids={"RQ1", "RQ2"},
        expected_topic="Agentic AI in Education",
    )

    assert errors == []


def test_missing_and_operator():

    validator = SearchStrategyValidator()
    result = create_valid_result()

    result.search_queries[0].query = (
        '("AI agents" OR "Autonomous agents")'
    )

    errors = validator.validate(
        result,
        create_concepts(),
        {"RQ1", "RQ2"},
    )

    assert any("AND operator is missing" in e for e in errors)


def test_missing_or_operator():

    validator = SearchStrategyValidator()
    result = create_valid_result()

    result.search_queries[0].query = (
        '"AI agents" AND "Educational settings"'
    )

    errors = validator.validate(
        result,
        create_concepts(),
        {"RQ1", "RQ2"},
    )

    assert any("OR operator is missing" in e for e in errors)


def test_unbalanced_parentheses():

    validator = SearchStrategyValidator()
    result = create_valid_result()

    result.search_queries[0].query = (
        '("AI agents" OR "Autonomous agents" '
        'AND ("Educational settings")'
    )

    errors = validator.validate(
        result,
        create_concepts(),
        {"RQ1", "RQ2"},
    )

    assert any("unbalanced parentheses" in e for e in errors)


def test_unbalanced_quotes():

    validator = SearchStrategyValidator()
    result = create_valid_result()

    result.search_queries[0].query = (
        '("AI agents OR "Autonomous agents") '
        'AND ("Educational settings")'
    )

    errors = validator.validate(
        result,
        create_concepts(),
        {"RQ1", "RQ2"},
    )

    assert any("unbalanced quotation marks" in e for e in errors)


def test_unknown_concept():

    validator = SearchStrategyValidator()
    result = create_valid_result()

    result.search_queries[0].related_concepts.append(
        "Unknown Concept"
    )

    errors = validator.validate(
        result,
        create_concepts(),
        {"RQ1", "RQ2"},
    )

    assert any("unknown concept" in e for e in errors)


def test_unknown_research_question():

    validator = SearchStrategyValidator()
    result = create_valid_result()

    result.search_queries[0].related_rqs.append("RQ99")

    errors = validator.validate(
        result,
        create_concepts(),
        {"RQ1", "RQ2"},
    )

    assert any("unknown research question" in e for e in errors)


def test_wrong_topic():

    validator = SearchStrategyValidator()

    errors = validator.validate(
        result=create_valid_result(),
        concepts=create_concepts(),
        valid_rq_ids={"RQ1", "RQ2"},
        expected_topic="AI in Healthcare",
    )

    assert any("topic does not match" in e for e in errors)
