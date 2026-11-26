from slrresearch.schemas.research_question import ResearchQuestionResult
from slrresearch.prompts.research_question_prompts import (
    SYSTEM_PROMPT,
    build_generation_prompt,
)
from slrresearch.services.llm_service import LLMService
from slrresearch.validators.research_question_validator import (
    ResearchQuestionValidator,
)


class ResearchQuestionAgent:

    def __init__(self, llm_service=None, validator=None):
        self.llm = llm_service or LLMService()
        self.validator = validator or ResearchQuestionValidator()

    def generate(self, topic, objective, context=""):
        prompt = build_generation_prompt(
            topic=topic,
            objective=objective,
            context=context,
        )

        raw_result = self.llm.generate(
            system_prompt=SYSTEM_PROMPT,
            user_prompt=prompt,
            response_format=ResearchQuestionResult.model_json_schema(),
        )

        return ResearchQuestionResult.model_validate(raw_result)

    def repair(self, result, errors):
        repair_prompt = f"""
The following research question result failed validation.

Validation errors:
{errors}

Invalid result:
{result.model_dump_json(indent=2)}

Correct all validation errors.

Preserve the original research topic and objective.
Do not introduce unnecessary changes.
Return the corrected result using the required schema.
"""

        raw_result = self.llm.generate(
            system_prompt=SYSTEM_PROMPT,
            user_prompt=repair_prompt,
            response_format=ResearchQuestionResult.model_json_schema(),
        )

        return ResearchQuestionResult.model_validate(raw_result)

    def run(self, topic, objective, context=""):

        # Step 1: Generate
        result = self.generate(topic, objective, context)

        # Step 2: Validate
        errors = self.validator.validate(result)

        if not errors:
            return {
                "status": "accepted",
                "result": result,
                "errors": [],
                "repair_attempts": 0,
            }

        # Step 3: Repair once
        try:
            repaired_result = self.repair(result, errors)

            # Step 4: Validate repaired result
            repaired_errors = self.validator.validate(repaired_result)

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