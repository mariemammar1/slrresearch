
from slrresearch.services.search.crossref_service import (
    CrossrefService,
)


service = CrossrefService()

results = service.search(
    query="agentic AI education",
    max_results=5,
)

print("\n========== CROSSREF RESULTS ==========")

print("Number of results:", len(results))

for index, article in enumerate(results, start=1):

    print(f"\nArticle {index}")

    title = article.get("title", [])

    print("Title:", title[0] if title else None)

    print("Publication year:", article.get("published"))

    print("DOI:", article.get("DOI"))

    print("URL:", article.get("URL"))
