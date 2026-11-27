from slrresearch.agents.search_agent import SearchAgent


agent = SearchAgent()

articles = agent.search_all(
    query="agentic AI education",
    max_results=5,
)

print("\n========== SEARCH AGENT RESULTS ==========")
print("Total articles:", len(articles))

for index, article in enumerate(articles, start=1):

    print(f"\nArticle {index}")
    print("Title:", article.title)
    print("Authors:", article.authors)
    print("Year:", article.year)
    print("DOI:", article.doi)
    print("Source:", article.source)