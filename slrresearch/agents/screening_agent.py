
from slrresearch.services.llm_service import LLMService

from slrresearch.schemas.article import Article
from slrresearch.schemas.screening_result import ScreeningResult
from slrresearch.schemas.screening_criteria import ScreeningCriteria

from slrresearch.validators.screening_validator import ScreeningValidator
from slrresearch.prompts.screening_prompts import SYSTEM_PROMPT


class ScreeningAgent:

    def __init__(self, llm_service=None):
        self.llm = llm_service or LLMService()

    def screen_article(
        self,
        article: Article,
        criteria: ScreeningCriteria
    ) -> dict:

        user_prompt = f"""
        Screen the following scientific article.

        ARTICLE TITLE:
        {article.title}

        ARTICLE ABSTRACT:
        {article.abstract or "Abstract not available"}

        INCLUSION CRITERIA:
        {criteria.inclusion_criteria}

        EXCLUSION CRITERIA:
        {criteria.exclusion_criteria}
        """

        raw_result = self.llm.generate(
            system_prompt=SYSTEM_PROMPT,
            user_prompt=user_prompt,
            response_format=ScreeningResult.model_json_schema()
        )

        result = ScreeningResult.model_validate(raw_result)

        errors = ScreeningValidator.validate(
            result=result,
            criteria=criteria
        )

        if errors:
            return {
                "status": "invalid",
                "errors": errors,
                "result": result
            }

        return {
            "status": "accepted",
            "errors": [],
            "result": result
        }
