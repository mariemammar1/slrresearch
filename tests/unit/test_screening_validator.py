from slrresearch.schemas.screening_result import ScreeningResult
from slrresearch.schemas.screening_criteria import ScreeningCriteria
from slrresearch.validators.screening_validator import ScreeningValidator


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


def test_valid_include_result():
    criteria = create_criteria()

    result = ScreeningResult(
        decision="include",
        justification="The article presents an educational application of Agentic AI.",
        matched_criteria=[
            "Focuses on Agentic AI in Education",
            "Presents an educational application"
        ]
    )

    errors = ScreeningValidator.validate(result, criteria)

    assert errors == []


def test_exclude_without_reason():
    criteria = create_criteria()

    result = ScreeningResult(
        decision="exclude",
        justification="The article is not relevant.",
        exclusion_reasons=[]
    )

    errors = ScreeningValidator.validate(result, criteria)

    assert any("at least one exclusion reason" in error for error in errors)


def test_unknown_inclusion_criterion():
    criteria = create_criteria()

    result = ScreeningResult(
        decision="include",
        justification="The article is relevant.",
        matched_criteria=["Unknown criterion"]
    )

    errors = ScreeningValidator.validate(result, criteria)

    assert any("Unknown inclusion criterion" in error for error in errors)


def test_unknown_exclusion_reason():
    criteria = create_criteria()

    result = ScreeningResult(
        decision="exclude",
        justification="The article is irrelevant.",
        exclusion_reasons=["Unknown reason"]
    )

    errors = ScreeningValidator.validate(result, criteria)

    assert any("Unknown exclusion criterion" in error for error in errors)


def test_include_with_exclusion_reasons():
    criteria = create_criteria()

    result = ScreeningResult(
        decision="include",
        justification="The article is relevant.",
        exclusion_reasons=["Does not concern education"]
    )

    errors = ScreeningValidator.validate(result, criteria)

    assert any("cannot have exclusion reasons" in error for error in errors)


def test_empty_justification():
    criteria = create_criteria()

    result = ScreeningResult(
        decision="uncertain",
        justification="   "
    )

    errors = ScreeningValidator.validate(result, criteria)

    assert any("Justification cannot be empty" in error for error in errors)