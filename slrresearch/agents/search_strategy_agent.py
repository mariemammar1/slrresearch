
from slrresearch.schemas.search_strategy import (
    SearchStrategyResult,
)

from slrresearch.prompts.search_strategy_prompts import (
    SYSTEM_PROMPT,
    build_search_strategy_prompt,
)

from slrresearch.services.llm_service import LLMService

from slrresearch.validators.search_strategy_validator import (
    SearchStrategyValidator,
)


class SearchStrategyAgent:

    def __init__(self, llm_service=None, validator=None):
        self.llm = llm_service or LLMService()
        self.validator = validator or SearchStrategyValidator()

    def generate(self, topic, concepts):

        prompt = build_search_strategy_prompt(
            topic=topic,
            concepts=concepts,
        )

        raw_result = self.llm.generate(
            system_prompt=SYSTEM_PROMPT,
            user_prompt=prompt,
            response_format=SearchStrategyResult.model_json_schema(),
        )

        return SearchStrategyResult.model_validate(raw_result)

    def repair(self, result, errors, concepts, valid_rq_ids):

        repair_prompt = f"""
The following Boolean search strategy failed validation.

Validation errors:
{errors}

Invalid result:
{result.model_dump_json(indent=2)}

Valid concept names:
{[concept.name for concept in concepts]}

Valid research question identifiers:
{list(valid_rq_ids)}

Correct all validation errors.

Rules:
- Preserve the original research topic.
- Use only the provided concepts.
- Use only valid research question identifiers.
- Use OR between synonyms of the same concept.
- Use AND between different concepts.
- Balance all parentheses and quotation marks.
- Preserve valid information.
- Return the corrected result using the required schema.
"""

        raw_result = self.llm.generate(
            system_prompt=SYSTEM_PROMPT,
            user_prompt=repair_prompt,
            response_format=SearchStrategyResult.model_json_schema(),
        )

        return SearchStrategyResult.model_validate(raw_result)

    def run(self, topic, concepts, research_questions):

        # Step 1: Generate
        result = self.generate(topic, concepts)

        # Step 2: Get valid RQ identifiers
        valid_rq_ids = {
            rq.id for rq in research_questions
        }

        # Step 3: Validate
        errors = self.validator.validate(
            result=result,
            concepts=concepts,
            valid_rq_ids=valid_rq_ids,
            expected_topic=topic,
        )

        if not errors:
            return {
                "status": "accepted",
                "result": result,
                "errors": [],
                "repair_attempts": 0,
            }

        # Step 4: Repair once
        try:
            repaired_result = self.repair(
                result=result,
                errors=errors,
                concepts=concepts,
                valid_rq_ids=valid_rq_ids,
            )

            # Step 5: Validate repaired result
            repaired_errors = self.validator.validate(
                result=repaired_result,
                concepts=concepts,
                valid_rq_ids=valid_rq_ids,
                expected_topic=topic,
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
