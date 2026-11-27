
from slrresearch.agents.search_strategy_agent import (
    SearchStrategyAgent,
)

from slrresearch.schemas.technology import TechnologyConcept

from slrresearch.schemas.research_question import ResearchQuestion


topic = "Agentic AI in Education"

concepts = [
    TechnologyConcept(
        name="Agentic AI",
        category="Technology",
        keywords=[
            "AI agents",
            "Autonomous agents",
            "Agentic artificial intelligence",
        ],
        related_rqs=["RQ1", "RQ2"],
    ),
    TechnologyConcept(
        name="Education",
        category="Domain",
        keywords=[
            "Educational settings",
            "Learning environments",
            "Higher education",
        ],
        related_rqs=["RQ1", "RQ3"],
    ),
    TechnologyConcept(
        name="Applications",
        category="Application",
        keywords=[
            "Educational applications",
            "Teaching support",
            "Personalized learning",
        ],
        related_rqs=["RQ1"],
    ),
]

research_questions = [
    ResearchQuestion(
        id="RQ1",
        question="What are the applications of agentic AI in education?",
        rationale="Identify educational applications.",
    ),
    ResearchQuestion(
        id="RQ2",
        question="What architectures and roles do AI agents adopt?",
        rationale="Analyze architectures and roles.",
    ),
    ResearchQuestion(
        id="RQ3",
        question="What are the benefits and challenges of agentic AI?",
        rationale="Analyze benefits and challenges.",
    ),
]


agent = SearchStrategyAgent()

response = agent.run(
    topic=topic,
    concepts=concepts,
    research_questions=research_questions,
)


print("\n========== SEARCH STRATEGY RESULT ==========")

print("Status:", response["status"])
print("Repair attempts:", response["repair_attempts"])

for index, query in enumerate(
    response["result"].search_queries,
    start=1,
):
    print(f"\nQuery {index}:")
    print(query.query)

    print("Related concepts:", query.related_concepts)
    print("Related RQs:", query.related_rqs)

print("\nValidation errors:", response["errors"])
