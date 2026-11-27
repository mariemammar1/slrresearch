
from slrresearch.services.search.openalex_service import (
    OpenAlexService,
)

from slrresearch.services.search.openalex_mapper import (
    OpenAlexMapper,
)

from slrresearch.services.search.crossref_service import (
    CrossrefService,
)

from slrresearch.services.search.crossref_mapper import (
    CrossrefMapper,
)
from slrresearch.services.search.article_deduplicator import (
    ArticleDeduplicator,
)


class SearchAgent:

    def __init__(
        self,
        openalex_service=None,
        crossref_service=None,
    ):

        self.openalex = (
            openalex_service or OpenAlexService()
        )

        self.crossref = (
            crossref_service or CrossrefService()
        )

    def search_openalex(
        self,
        query,
        max_results=10,
    ):

        raw_results = self.openalex.search(
            query=query,
            max_results=max_results,
        )

        articles = []

        for raw_article in raw_results:

            article = OpenAlexMapper.map_article(
                raw_article
            )

            articles.append(article)

        return articles

    def search_crossref(
          self,
          query,
          max_results=10,
      ):

          raw_results = self.crossref.search(
              query=query,
              max_results=max_results,
          )

          articles = []

          for raw_article in raw_results:

              article = CrossrefMapper.map_article(
                  raw_article
              )

              articles.append(article)

          return articles

    def search_all(
      self,
      query,
      max_results=10,
  ):

      articles = []

      articles.extend(
          self.search_openalex(
              query=query,
              max_results=max_results,
          )
      )

      articles.extend(
          self.search_crossref(
              query=query,
              max_results=max_results,
          )
      )

      unique_articles = ArticleDeduplicator.deduplicate(
          articles
      )

      return unique_articles
    def search_from_strategy(
      self,
      strategy,
      max_results=10,
  ):

      all_articles = []

      for search_query in strategy.search_queries:

          query = search_query.query

          articles = self.search_all(
              query=query,
              max_results=max_results,
          )

          all_articles.extend(articles)

      unique_articles = ArticleDeduplicator.deduplicate(
          all_articles
      )

      return unique_articles
