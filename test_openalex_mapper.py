
from slrresearch.services.search.openalex_mapper import (
    OpenAlexMapper,
)

fake_article = {
    "title": "Agentic AI in Education",
    "publication_year": 2025,
    "doi": "https://doi.org/10.1234/example",
    "id": "https://openalex.org/W123456",
    "authorships": [
        {
            "author": {
                "display_name": "Author One"
            }
        },
        {
            "author": {
                "display_name": "Author Two"
            }
        },
    ],
    "abstract_inverted_index": {
        "Agentic": [0],
        "AI": [1],
        "in": [2],
        "education": [3],
    },
}

article = OpenAlexMapper.map_article(
    fake_article
)

print("\n========== MAPPED ARTICLE ==========")

print("Title:", article.title)
print("Authors:", article.authors)
print("Year:", article.year)
print("DOI:", article.doi)
print("Abstract:", article.abstract)
print("Source:", article.source)
print("URL:", article.url)
