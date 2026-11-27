
from slrresearch.agents.screening_agent import ScreeningAgent
from slrresearch.schemas.screening_criteria import ScreeningCriteria
from slrresearch.services.search.article_loader import ArticleLoader
import json
from pathlib import Path

# 1. Load articles
articles = ArticleLoader.load()

# 2. Define screening criteria
criteria = ScreeningCriteria(
    inclusion_criteria=[
        "Addresses Agentic AI, AI agents, or autonomous agents",
        "Examines an application, architecture, design, or evaluation of agentic systems in education"
    ],
    exclusion_criteria=[
        "Does not address Agentic AI, AI agents, or autonomous agents",
        "Does not concern education, teaching, or learning",
        "Focuses exclusively on a non-educational application"
    ]
)

# 3. Initialize agent
agent = ScreeningAgent()

# 4. Screen all articles
results = []

for index, article in enumerate(articles, start=1):

    print(f"\nScreening article {index}/{len(articles)}")
    print("Title:", article.title)

    try:
        response = agent.screen_article(
            article=article,
            criteria=criteria
        )

        if response["status"] == "accepted":
            result = response["result"]

            results.append({
                "article": article,
                "decision": result.decision,
                "justification": result.justification,
                "matched_criteria": result.matched_criteria,
                "exclusion_reasons": result.exclusion_reasons
            })

            print("Decision:", result.decision)

        else:
            print("Invalid result:", response["errors"])

    except Exception as error:
        print("Screening error:", str(error))

# Save screening results
output_path = Path("data/processed/screening_results.json")
output_path.parent.mkdir(parents=True, exist_ok=True)

data = []

for item in results:
    data.append({
        "article": item["article"].model_dump(),
        "decision": item["decision"],
        "justification": item["justification"],
        "matched_criteria": item["matched_criteria"],
        "exclusion_reasons": item["exclusion_reasons"]
    })

with output_path.open("w", encoding="utf-8") as file:
    json.dump(data, file, indent=4, ensure_ascii=False)

print("\nScreening results saved to:", output_path)
# 5. Display summary
included = sum(
    1 for item in results if item["decision"] == "include"
)

excluded = sum(
    1 for item in results if item["decision"] == "exclude"
)

uncertain = sum(
    1 for item in results if item["decision"] == "uncertain"
)

print("\n========== SCREENING SUMMARY ==========")
print("Total articles:", len(articles))
print("Successfully screened:", len(results))
print("Included:", included)
print("Excluded:", excluded)
print("Uncertain:", uncertain)
print("Invalid or failed:", len(articles) - len(results))
