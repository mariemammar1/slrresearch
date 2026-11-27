from slrresearch.agents.screening_agent import ScreeningAgent
from slrresearch.schemas.article import Article
from slrresearch.schemas.screening_criteria import ScreeningCriteria


article = Article(
    title="Agentic AI in Education: Applications and Challenges",
    authors=["John Smith"],
    year=2025,
    abstract=(
        "This paper explores the applications of agentic AI "
        "in educational environments, including autonomous "
        "learning assistants and personalized tutoring systems."
    ),
    source="OpenAlex",
    url="https://example.com/article"
)

criteria = ScreeningCriteria(
    inclusion_criteria=[
        "Focuses on Agentic AI in Education",
        "Presents an educational application"
    ],
    exclusion_criteria=[
        "Does not concern education",
        "Does not address agentic AI"
    ]
)

agent = ScreeningAgent()

response = agent.screen_article(
    article=article,
    criteria=criteria
)

print("\n========== SCREENING RESULT ==========")
print("Status:", response["status"])

if response["status"] == "accepted":
    result = response["result"]

    print("Decision:", result.decision)
    print("Justification:", result.justification)
    print("Matched criteria:", result.matched_criteria)
    print("Exclusion reasons:", result.exclusion_reasons)

else:
    print("Errors:", response["errors"])