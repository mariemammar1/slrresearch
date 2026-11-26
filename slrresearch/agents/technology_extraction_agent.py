
from slrresearch.schemas.technology import (
    TechnologyExtractionResult,
)

from slrresearch.prompts.technology_extraction_prompts import (
    SYSTEM_PROMPT,
    build_extraction_prompt,
)

from slrresearch.services.llm_service import LLMService

from slrresearch.validators.technology_extraction_validator import (
    TechnologyExtractionValidator,
)


class TechnologyExtractionAgent:

    def __init__(self, llm_service=None, validator=None):
        self.llm = llm_service or LLMService()
        self.validator = validator or TechnologyExtractionValidator()

    def generate(
        self,
        topic,
        objective,
        research_questions,
    ):

        prompt = build_extraction_prompt(
            topic=topic,
            objective=objective,
            research_questions=research_questions,
        )

        raw_result = self.llm.generate(
            system_prompt=SYSTEM_PROMPT,
            user_prompt=prompt,
            response_format=TechnologyExtractionResult.model_json_schema(),
        )

        return TechnologyExtractionResult.model_validate(raw_result)

    def repair(self, result, errors, research_questions):

        repair_prompt = f"""
The following technology extraction result failed validation.

Validation errors:
{errors}

Invalid result:
{result.model_dump_json(indent=2)}

Valid Research Question identifiers:
{[rq.id for rq in research_questions]}

Correct all validation errors.

Rules:
- Preserve the original topic and objective.
- Keep concepts relevant to the research questions.
- Use only valid research question identifiers.
- Do not introduce unrelated concepts.
- Do not remove valid information unnecessarily.
- Return the corrected result using the required schema.
"""

        raw_result = self.llm.generate(
            system_prompt=SYSTEM_PROMPT,
            user_prompt=repair_prompt,
            response_format=TechnologyExtractionResult.model_json_schema(),
        )

        return TechnologyExtractionResult.model_validate(raw_result)

    def run(
        self,
        topic,
        objective,
        research_questions,
    ):

        # Step 1: Generate
        result = self.generate(
            topic,
            objective,
            research_questions,
        )

        # Step 2: Validate
        errors = self.validator.validate(
    result,
    research_questions,
    expected_topic=topic,
    expected_objective=objective,
)

        if not errors:
            return {
                "status": "accepted",
                "result": result,
                "errors": [],
                "repair_attempts": 0,
            }

        # Step 3: Repair once
        try:
            repaired_result = self.repair(
                result,
                errors,
                research_questions,
            )

            # Step 4: Validate repaired result
            repaired_errors = self.validator.validate(
    repaired_result,
    research_questions,
    expected_topic=topic,
    expected_objective=objective,
)

            if not repaired_errors:
                return {
                    "status": "repaired",
                    "result": repaired_result,
                    "errors": [],
                    "repair_attempts": 1,
                }

            return {
                "status": "human_required",
                "result": repaired_result,
                "errors": repaired_errors,
                "repair_attempts": 1,
            }

        except Exception as exc:
            return {
                "status": "human_required",
                "result": result,
                "errors": errors,
                "repair_attempts": 1,
                "repair_error": str(exc),
            }
