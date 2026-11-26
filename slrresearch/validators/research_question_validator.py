from slrresearch.schemas.research_question import ResearchQuestionResult


class ResearchQuestionValidator:

    def validate(
        self,
        result: ResearchQuestionResult,
    ) -> list[str]:

        errors = []

        questions = result.research_questions

        # 1. Check the number of research questions
        if not 3 <= len(questions) <= 5:
            errors.append(
                "The number of research questions must be between 3 and 5."
            )

        # 2. Check sequential identifiers
        expected_ids = [
            f"RQ{i}" for i in range(1, len(questions) + 1)
        ]

        actual_ids = [rq.id for rq in questions]

        if actual_ids != expected_ids:
            errors.append(
                f"Expected identifiers {expected_ids}, "
                f"but received {actual_ids}."
            )

        # 3. Check empty questions and rationales
        for rq in questions:
            if not rq.question.strip():
                errors.append(f"{rq.id}: question is empty.")

            if not rq.rationale.strip():
                errors.append(f"{rq.id}: rationale is empty.")

        # 4. Check duplicate questions
        normalized_questions = [
            rq.question.strip().lower()
            for rq in questions
        ]

        if len(normalized_questions) != len(set(normalized_questions)):
            errors.append("Duplicate research questions detected.")

        # 5. Check empty topic and objective
        if not result.topic.strip():
            errors.append("Research topic is empty.")

        if not result.objective.strip():
            errors.append("Research objective is empty.")

        return errors