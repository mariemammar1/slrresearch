from slrresearch.services.search.article_deduplicator import (
    ArticleDeduplicator,
)

from slrresearch.schemas.article import Article


def create_article(title, doi=None):

    return Article(
        title=title,
        authors=[],
        year=2025,
        doi=doi,
        abstract=None,
        source="OpenAlex",
        url=None,
    )


def test_normalize_doi():

    result = ArticleDeduplicator.normalize_doi(
        "https://doi.org/10.1234/Example"
    )

    assert result == "10.1234/example"


def test_normalize_title():

    result = ArticleDeduplicator.normalize_title(
        "Agentic AI in Education!"
    )

    assert result == "agenticaiineducation"


def test_deduplicate_by_doi():

    articles = [
        create_article(
            "Article One",
            "https://doi.org/10.1234/example",
        ),
        create_article(
            "Different Title",
            "10.1234/example",
        ),
    ]

    result = ArticleDeduplicator.deduplicate(
        articles
    )

    assert len(result) == 1


def test_deduplicate_by_title():

    articles = [
        create_article(
            "Agentic AI in Education!",
        ),
        create_article(
            "Agentic AI in Education",
        ),
    ]

    result = ArticleDeduplicator.deduplicate(
        articles
    )

    assert len(result) == 1


def test_keep_unique_articles():

    articles = [
        create_article("Article One", "10.1111/a"),
        create_article("Article Two", "10.1111/b"),
        create_article("Article Three", "10.1111/c"),
    ]

    result = ArticleDeduplicator.deduplicate(
        articles
    )

    assert len(result) == 3