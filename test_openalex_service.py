
from slrresearch.services.search.openalex_service import OpenAlexService


service = OpenAlexService()

results = service.search(
    query="agentic AI education",
    max_results=5,
)

print("\n========== OPENALEX RESULTS ==========")

print("Number of results:", len(results))

for index, article in enumerate(results, start=1):

    print(f"\nArticle {index}")

    print("Title:", article.get("title"))

    print("Publication year:", article.get("publication_year"))

    print("DOI:", article.get("doi"))

    print("OpenAlex ID:", article.get("id"))
