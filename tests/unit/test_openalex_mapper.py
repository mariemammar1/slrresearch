
from slrresearch.services.search.openalex_mapper import (
    OpenAlexMapper,
)


def test_map_article_fields():

    raw_article = {
        "title": "Agentic AI in Education",
        "publication_year": 2025,
        "doi": "https://doi.org/10.1234/example",
        "id": "https://openalex.org/W123456",
        "authorships": [
            {
                "author": {
                    "display_name": "Author One"
                }
            }
        ],
        "abstract_inverted_index": {
            "Agentic": [0],
            "AI": [1],
            "in": [2],
            "education": [3],
        },
    }

    article = OpenAlexMapper.map_article(raw_article)

    assert article.title == "Agentic AI in Education"
    assert article.authors == ["Author One"]
    assert article.year == 2025
    assert article.doi == "https://doi.org/10.1234/example"
    assert article.abstract == "Agentic AI in education"
    assert article.source == "OpenAlex"
    assert article.url == "https://openalex.org/W123456"


def test_map_article_without_abstract():

    raw_article = {
        "title": "Article without abstract",
        "authorships": [],
        "abstract_inverted_index": None,
    }

    article = OpenAlexMapper.map_article(raw_article)

    assert article.title == "Article without abstract"
    assert article.abstract is None


def test_map_article_without_authors():

    raw_article = {
        "title": "Article without authors",
        "authorships": [],
    }

    article = OpenAlexMapper.map_article(raw_article)

    assert article.authors == []


def test_reconstruct_abstract_order():

    inverted_index = {
        "education": [3],
        "AI": [1],
        "Agentic": [0],
        "in": [2],
    }

    abstract = OpenAlexMapper.reconstruct_abstract(
        inverted_index
    )

    assert abstract == "Agentic AI in education"


def test_reconstruct_empty_abstract():

    abstract = OpenAlexMapper.reconstruct_abstract({})

    assert abstract is None
