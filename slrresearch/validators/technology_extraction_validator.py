
from slrresearch.schemas.technology import (
    TechnologyExtractionResult,
)


class TechnologyExtractionValidator:

    ALLOWED_CATEGORIES = {
        "Technology",
        "Domain",
        "Application",
        "Outcome",
        "Method",
        "Other",
    }

    def validate(
    self,
    result: TechnologyExtractionResult,
    research_questions: list,
    expected_topic: str = None,
    expected_objective: str = None,
) -> list[str]:

        errors = []
        # Check topic consistency
        if expected_topic is not None:
            if result.topic.strip() != expected_topic.strip():
                errors.append(
                    "The generated topic does not match the original topic."
                )

        # Check objective consistency
        if expected_objective is not None:
            if result.objective.strip() != expected_objective.strip():
                errors.append(
                    "The generated objective does not match the original objective."
                )

        concepts = result.concepts

        # 1. Check that at least one concept exists
        if not concepts:
            errors.append("At least one concept is required.")

        # 2. Check topic and objective
        if not result.topic.strip():
            errors.append("Research topic is empty.")

        if not result.objective.strip():
            errors.append("Research objective is empty.")

        # Build the list of valid RQ identifiers
        valid_rq_ids = {
            rq.id for rq in research_questions
        }

        # Track concept names to detect duplicates
        concept_names = []

        for concept in concepts:

            # 3. Check concept name
            if not concept.name.strip():
                errors.append("Concept name is empty.")

            concept_names.append(
                concept.name.strip().lower()
            )

            # 4. Check category
            if concept.category not in self.ALLOWED_CATEGORIES:
                errors.append(
                    f"{concept.name}: invalid category "
                    f"'{concept.category}'."
                )

            # 5. Check keywords
            valid_keywords = [
                keyword.strip().lower()
                for keyword in concept.keywords
                if keyword.strip()
            ]

            if not valid_keywords:
                errors.append(
                    f"{concept.name}: no valid keywords."
                )

            if len(valid_keywords) != len(set(valid_keywords)):
                errors.append(
                    f"{concept.name}: duplicate keywords detected."
                )

            # 6. Check related research questions
            if not concept.related_rqs:
                errors.append(
                    f"{concept.name}: no related research questions."
                )

            for rq_id in concept.related_rqs:
                if rq_id not in valid_rq_ids:
                    errors.append(
                        f"{concept.name}: unknown research "
                        f"question '{rq_id}'."
                    )

        # 7. Check duplicate concepts
        if len(concept_names) != len(set(concept_names)):
            errors.append("Duplicate concepts detected.")

        return errors
