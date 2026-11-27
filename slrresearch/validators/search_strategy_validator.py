
import re

from slrresearch.schemas.search_strategy import (
    SearchStrategyResult,
)


class SearchStrategyValidator:

    def validate(
        self,
        result: SearchStrategyResult,
        concepts: list,
        valid_rq_ids: set,
        expected_topic: str = None,
    ) -> list[str]:

        errors = []

        # 1. Check topic consistency
        if expected_topic is not None:
            if result.topic.strip() != expected_topic.strip():
                errors.append(
                    "The generated topic does not match the original topic."
                )

        # 2. Build valid concept names
        valid_concept_names = {
            concept.name.strip().lower()
            for concept in concepts
        }

        queries = result.search_queries

        if not queries:
            errors.append("At least one search query is required.")

        # 3. Validate each query
        for index, search_query in enumerate(queries, start=1):

            query = search_query.query.strip()

            # Check empty query
            if not query:
                errors.append(
                    f"Query {index}: search query is empty."
                )
                continue

            # Check Boolean operators
            if not re.search(r"\bAND\b", query):
                errors.append(
                    f"Query {index}: AND operator is missing."
                )

            if not re.search(r"\bOR\b", query):
                errors.append(
                    f"Query {index}: OR operator is missing."
                )

            # Check balanced parentheses
            if query.count("(") != query.count(")"):
                errors.append(
                    f"Query {index}: unbalanced parentheses."
                )

            # Check quotation marks
            if query.count('"') % 2 != 0:
                errors.append(
                    f"Query {index}: unbalanced quotation marks."
                )

            # Check related concepts
            if not search_query.related_concepts:
                errors.append(
                    f"Query {index}: no related concepts."
                )

            for concept_name in search_query.related_concepts:

                if concept_name.strip().lower() not in valid_concept_names:
                    errors.append(
                        f"Query {index}: unknown concept "
                        f"'{concept_name}'."
                    )

            # Check related research questions
            if not search_query.related_rqs:
                errors.append(
                    f"Query {index}: no related research questions."
                )

            for rq_id in search_query.related_rqs:

                if rq_id not in valid_rq_ids:
                    errors.append(
                        f"Query {index}: unknown research question "
                        f"'{rq_id}'."
                    )

        return errors
