
from slrresearch.services.search.crossref_mapper import (
    CrossrefMapper,
)


fake_article = {
    "title": ["Agentic AI in Education"],
    "author": [
        {
            "given": "John",
            "family": "Smith",
        },
        {
            "given": "Jane",
            "family": "Doe",
        },
    ],
    "published": {
        "date-parts": [[2025, 5, 10]],
    },
    "DOI": "10.1234/example",
    "URL": "https://doi.org/10.1234/example",
    "abstract": "<jats:p>Agentic AI in education.</jats:p>",
}

article = CrossrefMapper.map_article(
    fake_article
)

print("\n========== MAPPED CROSSREF ARTICLE ==========")

print("Title:", article.title)
print("Authors:", article.authors)
print("Year:", article.year)
print("DOI:", article.doi)
print("Abstract:", article.abstract)
print("Source:", article.source)
print("URL:", article.url)
