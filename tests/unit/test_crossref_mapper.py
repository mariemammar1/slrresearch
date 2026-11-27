
from slrresearch.services.search.crossref_mapper import (
    CrossrefMapper,
)


def test_map_article_fields():

    raw_article = {
        "title": ["Agentic AI in Education"],
        "author": [
            {
                "given": "John",
                "family": "Smith",
            }
        ],
        "published": {
            "date-parts": [[2025, 5, 10]],
        },
        "DOI": "10.1234/example",
        "URL": "https://doi.org/10.1234/example",
        "abstract": "<jats:p>Agentic AI in education.</jats:p>",
    }

    article = CrossrefMapper.map_article(raw_article)

    assert article.title == "Agentic AI in Education"
    assert article.authors == ["John Smith"]
    assert article.year == 2025
    assert article.doi == "10.1234/example"
    assert article.abstract == "Agentic AI in education."
    assert article.source == "Crossref"
    assert article.url == "https://doi.org/10.1234/example"


def test_extract_year_fallback():

    raw_article = {
        "published": {},
        "published-print": {
            "date-parts": [[2024]],
        },
    }

    year = CrossrefMapper.extract_year(raw_article)

    assert year == 2024


def test_article_without_authors():

    raw_article = {
        "title": ["Article without authors"],
        "author": [],
    }

    article = CrossrefMapper.map_article(raw_article)

    assert article.authors == []


def test_article_without_abstract():

    raw_article = {
        "title": ["Article without abstract"],
        "abstract": None,
    }

    article = CrossrefMapper.map_article(raw_article)

    assert article.abstract is None


def test_clean_abstract():

    abstract = "<jats:p>AI &amp; Education</jats:p>"

    cleaned = CrossrefMapper.clean_abstract(abstract)

    assert cleaned == "AI & Education"
