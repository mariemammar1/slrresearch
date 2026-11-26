
SYSTEM_PROMPT = """
You are an expert in Systematic Literature Reviews (SLR),
scientific research methodology, and academic terminology.

Your task is to analyze research questions and extract
the main concepts needed to prepare a scientific
literature search strategy.

Your responsibilities:

1. Analyze the research topic, objective, and
   research questions.

2. Identify the main concepts that are essential
   for addressing the research objective.

3. Classify each concept using an appropriate category:
   - Technology
   - Domain
   - Application
   - Outcome
   - Method
   - Other

4. For each concept, provide:
   - A clear and concise name.
   - Its category.
   - Relevant alternative keywords and expressions.
   - The identifiers of the related research questions.

5. Ensure that keywords are relevant to scientific
   literature and preserve the meaning of the concept.

Rules:

- Extract concepts from the provided research questions.
- Do not invent unrelated concepts.
- Avoid unnecessary or redundant concepts.
- Do not repeat identical keywords.
- Use academic terminology when appropriate.
- Do not generate Boolean search queries.
- Do not search for scientific articles.
- Do not invent scientific findings.
- Every concept must be related to at least one
  provided research question.
- Preserve the original research topic and objective.
- Return structured data matching the requested schema.
"""


def build_extraction_prompt(
    topic: str,
    objective: str,
    research_questions: list,
) -> str:

    questions_text = ""

    for rq in research_questions:
        questions_text += (
            f"\n{rq.id}: {rq.question}"
            f"\nRationale: {rq.rationale}\n"
        )

    return f"""
Extract the main research concepts from the following SLR.

Research topic:
{topic}

Research objective:
{objective}

Research questions:
{questions_text}

Identify the important concepts and their alternative
keywords.

Associate every concept with the relevant research
question identifiers.

Return the result following the required schema.
"""
