import json

from slrresearch.schemas.article import Article
from slrresearch.services.search.article_exporter import ArticleExporter


def test_export_articles_to_json(tmp_path):
    articles = [
        Article(
            title="Agentic AI in Education",
            authors=["John Smith"],
            year=2025,
            doi="10.1234/example",
            abstract="An article about agentic AI in education.",
            source="OpenAlex",
            url="https://example.com/article",
        )
    ]

    filepath = tmp_path / "raw" / "results.json"

    returned_path = ArticleExporter.export(
        articles,
        filepath=filepath,
    )

    assert filepath.exists()
    assert returned_path == filepath

    with filepath.open("r", encoding="utf-8") as file:
        data = json.load(file)

    assert len(data) == 1
    assert data[0]["title"] == "Agentic AI in Education"
    assert data[0]["authors"] == ["John Smith"]
    assert data[0]["year"] == 2025