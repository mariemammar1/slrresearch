from slrresearch.agents.search_agent import SearchAgent


class FakeOpenAlexService:

    def search(self, query, max_results=10):
        return [
            {
                "title": "Article OpenAlex",
                "authorships": [],
                "publication_year": 2025,
                "doi": None,
                "abstract_inverted_index": None,
                "id": "https://openalex.org/W123",
            }
        ]


class FakeCrossrefService:

    def search(self, query, max_results=10):
        return [
            {
                "title": ["Article Crossref"],
                "author": [],
                "published": {
                    "date-parts": [[2024]]
                },
                "DOI": "10.1234/test",
                "abstract": None,
                "URL": "https://doi.org/10.1234/test",
            }
        ]


def test_search_all_returns_articles_from_both_sources():

    agent = SearchAgent(
        openalex_service=FakeOpenAlexService(),
        crossref_service=FakeCrossrefService(),
    )

    articles = agent.search_all("agentic AI education")

    assert len(articles) == 2

    assert articles[0].source == "OpenAlex"
    assert articles[1].source == "Crossref"


def test_search_openalex_returns_one_article():

    agent = SearchAgent(
        openalex_service=FakeOpenAlexService(),
        crossref_service=FakeCrossrefService(),
    )

    articles = agent.search_openalex("education")

    assert len(articles) == 1
    assert articles[0].title == "Article OpenAlex"


def test_search_crossref_returns_one_article():

    agent = SearchAgent(
        openalex_service=FakeOpenAlexService(),
        crossref_service=FakeCrossrefService(),
    )

    articles = agent.search_crossref("education")

    assert len(articles) == 1
    assert articles[0].title == "Article Crossref"
from slrresearch.schemas.search_strategy import (
    SearchStrategyResult,
    SearchQuery,
)


class StrategyFakeOpenAlex:

    def search(self, query, max_results=10):

        return [
            {
                "title": "Agentic AI in Education",
                "authorships": [],
                "publication_year": 2025,
                "doi": "https://doi.org/10.1234/example",
                "abstract_inverted_index": None,
                "id": "https://openalex.org/W123",
            }
        ]


class StrategyFakeCrossref:

    def search(self, query, max_results=10):

        return [
            {
                "title": ["Agentic AI in Education"],
                "author": [],
                "published": {
                    "date-parts": [[2025]]
                },
                "DOI": "10.1234/example",
                "abstract": None,
                "URL": "https://doi.org/10.1234/example",
            }
        ]


def test_search_from_strategy_deduplicates_articles():

    strategy = SearchStrategyResult(
        topic="Agentic AI in Education",
        search_queries=[
            SearchQuery(
                query='"agentic AI" AND education',
                related_concepts=["Agentic AI", "Education"],
                related_rqs=["RQ1"],
            ),
            SearchQuery(
                query='"AI agents" AND learning',
                related_concepts=["AI Agents", "Learning"],
                related_rqs=["RQ1"],
            ),
        ],
    )

    agent = SearchAgent(
        openalex_service=StrategyFakeOpenAlex(),
        crossref_service=StrategyFakeCrossref(),
    )

    articles = agent.search_from_strategy(strategy)

    assert len(articles) == 1
    assert articles[0].title == "Agentic AI in Education"