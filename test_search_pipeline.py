
from slrresearch.agents.search_strategy_agent import SearchStrategyAgent
from slrresearch.agents.search_agent import SearchAgent
from slrresearch.schemas.technology import TechnologyConcept
from slrresearch.schemas.research_question import ResearchQuestion
from slrresearch.services.search.article_exporter import ArticleExporter

topic = "Agentic AI in Education"

concepts = [
    TechnologyConcept(
        name="Agentic AI",
        category="Technology",
        keywords=["AI agents", "autonomous agents", "agentic artificial intelligence"],
        related_rqs=["RQ1", "RQ2"],
    ),
    TechnologyConcept(
        name="Education",
        category="Context",
        keywords=["educational settings", "learning environments", "higher education"],
        related_rqs=["RQ1", "RQ2", "RQ3"],
    ),
    TechnologyConcept(
        name="Applications",
        category="Application",
        keywords=["educational applications", "teaching support", "personalized learning"],
        related_rqs=["RQ1", "RQ3"],
    ),
]

research_questions = [
    ResearchQuestion(
        id="RQ1",
        question="What are the applications of agentic AI in education?",
        rationale="Identify the applications of agentic AI in educational settings.",
    ),
    ResearchQuestion(
        id="RQ2",
        question="What architectures are used by agentic AI systems in education?",
        rationale="Identify the architectures of educational agentic AI systems.",
    ),
    ResearchQuestion(
        id="RQ3",
        question="What are the benefits and challenges of agentic AI in education?",
        rationale="Analyze benefits and challenges.",
    ),
]

# 1. Generate search strategy
strategy_agent = SearchStrategyAgent()

strategy_response = strategy_agent.run(
    topic=topic,
    concepts=concepts,
    research_questions=research_questions,
)

if strategy_response["status"] not in ("accepted", "repaired"):
    print("Strategy generation failed:")
    print(strategy_response["errors"])
    exit()

strategy = strategy_response["result"]

# 2. Execute the generated strategy
search_agent = SearchAgent()

articles = search_agent.search_from_strategy(
    strategy=strategy,
    max_results=5,
)
# 3. Export articles to JSON
filepath = ArticleExporter.export(articles)

print("Articles saved to:", filepath)
# 3. Display results
print("\n========== SEARCH PIPELINE ==========")
print("Topic:", topic)
print("Generated queries:", len(strategy.search_queries))
print("Articles found:", len(articles))

for i, query in enumerate(strategy.search_queries, start=1):
    print(f"\nQuery {i}:")
    print(query.query)

print("\n========== ARTICLES ==========")

for i, article in enumerate(articles, start=1):
    print(f"\nArticle {i}")
    print("Title:", article.title)
    print("Year:", article.year)
    print("Source:", article.source)
    print("DOI:", article.doi)
