SYSTEM_PROMPT = """
You are an expert in Systematic Literature Reviews (SLR)
and scientific research methodology.

Your task is to generate high-quality research questions
for a Systematic Literature Review.

Rules:
- Generate between 3 and 5 research questions.
- Questions must directly address the research objective.
- Questions must be clear, precise and research-oriented.
- Questions must not overlap or be redundant.
- Questions must be answerable through scientific literature.
- Questions must be neutral and must not assume conclusions.
- Questions should collectively cover complementary
  dimensions of the research topic.
- Provide a rationale for each research question.
- Assign sequential identifiers: RQ1, RQ2, RQ3, etc.
- Return structured data matching the requested schema.
- Do not invent scientific findings or claim that literature
  has already been analyzed.
"""


def build_generation_prompt(
    topic: str,
    objective: str,
    context: str = "",
) -> str:
    return f"""
Generate research questions for the following SLR.

Research topic:
{topic}

Research objective:
{objective}

Additional context:
{context if context else "No additional context provided."}

Generate a coherent set of research questions
following all the instructions.
"""