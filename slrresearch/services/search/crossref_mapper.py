
import re
from html import unescape

from slrresearch.schemas.article import Article


class CrossrefMapper:

    @staticmethod
    def clean_abstract(abstract):

        if not abstract:
            return None

        # Remove HTML/XML tags
        abstract = re.sub(
            r"<[^>]+>",
            " ",
            abstract,
        )

        # Decode HTML entities
        abstract = unescape(abstract)

        # Normalize whitespace
        abstract = " ".join(abstract.split())

        return abstract

    @staticmethod
    def extract_year(raw_article):

        date_fields = [
            "published",
            "published-print",
            "published-online",
            "created",
        ]

        for field in date_fields:

            date_data = raw_article.get(field, {})

            date_parts = date_data.get(
                "date-parts", []
            )

            if date_parts and date_parts[0]:

                year = date_parts[0][0]

                if isinstance(year, int):
                    return year

        return None

    @staticmethod
    def extract_authors(raw_article):

        authors = []

        for author in raw_article.get(
            "author", []
        ):

            given = author.get("given", "")
            family = author.get("family", "")

            name = " ".join(
                part for part in [given, family]
                if part
            ).strip()

            if name:
                authors.append(name)

        return authors

    @classmethod
    def map_article(cls, raw_article):

        titles = raw_article.get("title", [])

        title = (
            titles[0]
            if titles
            else "Untitled"
        )

        article = Article(
            title=title,
            authors=cls.extract_authors(raw_article),
            year=cls.extract_year(raw_article),
            doi=raw_article.get("DOI"),
            abstract=cls.clean_abstract(
                raw_article.get("abstract")
            ),
            source="Crossref",
            url=raw_article.get("URL"),
        )

        return article
