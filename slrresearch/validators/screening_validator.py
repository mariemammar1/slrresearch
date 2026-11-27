from slrresearch.schemas.screening_result import ScreeningResult
from slrresearch.schemas.screening_criteria import ScreeningCriteria


class ScreeningValidator:

    @staticmethod
    def validate(
        result: ScreeningResult,
        criteria: ScreeningCriteria
    ) -> list[str]:

        errors = []

        # Check justification
        if not result.justification.strip():
            errors.append("Justification cannot be empty.")

        # Check matched inclusion criteria
        for criterion in result.matched_criteria:
            if criterion not in criteria.inclusion_criteria:
                errors.append(
                    f"Unknown inclusion criterion: {criterion}"
                )

        # Check exclusion reasons
        for reason in result.exclusion_reasons:
            if reason not in criteria.exclusion_criteria:
                errors.append(
                    f"Unknown exclusion criterion: {reason}"
                )

        # Check decision consistency
        if result.decision == "exclude":
            if not result.exclusion_reasons:
                errors.append(
                    "An excluded article must have at least one exclusion reason."
                )

        if result.decision == "include":
            if result.exclusion_reasons:
                errors.append(
                    "An included article cannot have exclusion reasons."
                )

        return errors