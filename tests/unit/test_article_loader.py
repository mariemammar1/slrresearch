import json

from slrresearch.services.search.article_loader import ArticleLoader
from slrresearch.schemas.article import Article


def test_load_articles(tmp_path):
    filepath = tmp_path / "articles.json"

    data = [
        {
            "title": "Agentic AI in Education",
            "authors": ["John Smith"],
            "year": 2025,
            "doi": "10.1234/example",
            "abstract": "An article about agentic AI.",
            "source": "OpenAlex",
            "url": "https://example.com/article",
        }
    ]

    with filepath.open("w", encoding="utf-8") as file:
        json.dump(data, file)

    articles = ArticleLoader.load(filepath)

    assert len(articles) == 1
    assert isinstance(articles[0], Article)
    assert articles[0].title == "Agentic AI in Education"