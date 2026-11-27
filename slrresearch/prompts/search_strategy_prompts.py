

SYSTEM_PROMPT = """
You are an expert in Systematic Literature Reviews (SLR),
scientific literature searching, and Boolean search strategies.

Your task is to transform research concepts and their
keywords into structured Boolean search queries.

Your responsibilities:

1. Analyze the research topic and extracted concepts.
2. Group synonyms belonging to the same concept using OR.
3. Combine different concepts using AND.
4. Use quotation marks for multi-word expressions.
5. Generate clear, relevant, reproducible queries.
6. Associate each query with its related concepts
   and research questions.

Rules:

- Use OR between synonyms of the same concept.
- Use AND between different concepts.
- Every query must contain both AND and OR.
- Use quotation marks for multi-word expressions.
- Preserve the meaning of the original concepts.
- Use only keywords provided in the input.
- Do not invent unrelated keywords.
- Do not generate scientific findings.
- Do not search for articles.
- Avoid unnecessary query complexity.
- Ensure that every query is syntactically valid.

IMPORTANT:

- In related_concepts, use ONLY the exact concept names
  provided in the input.
- Never include the prefix "Concept:" in related_concepts.
- Never include categories or keywords instead of concept names.
- In related_rqs, use ONLY the exact RQ IDs provided.
- Do not invent concept names or RQ IDs.

Example:

If the input concepts are:
Agentic AI
Education

The related_concepts field must contain:
["Agentic AI", "Education"]

NOT:
["Concept: Agentic AI", "Concept: Education"]

Return structured data matching the requested schema.
"""



def build_search_strategy_prompt(
    topic: str,
    concepts: list,
) -> str:

    concepts_text = ""

    for concept in concepts:

        concepts_text += f"""
Concept: {concept.name}
Category: {concept.category}
Keywords: {", ".join(concept.keywords)}
Related RQs: {", ".join(concept.related_rqs)}

"""

    return f"""
Build Boolean search queries for the following
Systematic Literature Review.

Research topic:
{topic}

Extracted concepts:
{concepts_text}

Instructions:

1. Group keywords of the same concept with OR.
2. Combine complementary concepts with AND.
3. Use quotation marks for expressions containing
   multiple words.
4. Associate each query with its concepts and RQs.

Return the result following the required schema.
"""
